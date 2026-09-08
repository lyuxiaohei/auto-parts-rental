# -*- coding: utf-8 -*-
"""修复·2026-09-08（二）：两处页面原生列数不匹配（用户目检空白列暴露）
1) 器具档案：行缺「租金单价(元/天)」格（th12 vs td11，页面作者漏格）——从详情实体既有「日租金」补格
2) BOM维护：版本表行多「配方来源」格（th5 vs td6）——表头补 <th>配方来源</th> 对齐
"""
import sys, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
DD = PROTO / '_data' / 'demo-data.js'

RENT = {  # 取自 appliances 详情「日租金」既有值（数字部分），不自造
    'WBX-1210L': '38.00', 'WBX-1210M': '32.00', 'PLT-1210W': '12.00',
    'PLT-1210P': '18.00', 'BTC-6040S': '7.80', 'BTC-6040': '8.50',
}

# --- 1) demo-data.js appliances 6 条：参考单价（cells[6]）后插租金单价格 ---
raw = DD.read_bytes().decode('utf-8')
i0 = raw.find('  appliances: {')
i1 = raw.find('  parts: {')
seg = raw[i0:i1]
n_fix = 0
for k, v in RENT.items():
    ka = re.search(rf"^    '{re.escape(k)}': \{{\n(      'row': )({{.*}})(,)\n", seg, re.M)
    assert ka, f'未找到 {k} row 行'
    d = json.loads(ka.group(2))
    assert len(d['cells']) == 8, f'{k} cells 数 {len(d["cells"])} 非预期 8'
    d['cells'].insert(7, f'<span class="td-num">{v}</span>')
    seg = seg[:ka.start(2)] + json.dumps(d, ensure_ascii=False) + seg[ka.end(2):]
    n_fix += 1
raw = raw[:i0] + seg + raw[i1:]
assert n_fix == 6, f'器具补格 {n_fix} 非 6'
DD.write_bytes(raw.encode('utf-8'))
print('器具档案：6 条 row 补租金单价格（取详情日租金）')

# --- 2) BOM维护 版本表表头补 th ---
P = PROTO / '基础数据' / 'BOM维护.html'
raw2 = P.read_bytes()
crlf = raw2.count(b'\r\n') * 2 > raw2.count(b'\n')
nl = '\r\n' if crlf else '\n'
txt = raw2.decode('utf-8')
assert txt.count('<th>生效日期</th>') == 1, '生效日期 th 不唯一'
if '<th>配方来源</th>' not in txt:
    txt = txt.replace('<th>生效日期</th>', '<th>生效日期</th>' + nl + '          <th>配方来源</th>')
    P.write_bytes(txt.encode('utf-8'))
    print('BOM维护：版本表头补 <th>配方来源</th>（6=6 对齐，行尾 ' + ('CRLF' if crlf else 'LF') + '）')
else:
    print('BOM维护：已有配方来源 th，跳过')
