# -*- coding: utf-8 -*-
"""批1 Stage5/8（续）：打印出货单（L9）——组合出库改名8+8；销售出库新增6+6；demo-data ops"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"

def patch_file(path, old, new, expect, tag):
    raw = path.read_bytes(); txt = raw.decode('utf-8')
    n = txt.count(old)
    assert n == expect, f'{path.name} [{tag}] {n} 次（应为 {expect}）'
    path.write_bytes(txt.replace(old, new).encode('utf-8'))
    print(f' ✓ {path.name} [{tag}] {n} 处')

# 组合出库列表 页面静态行：打印 → 打印出货单
patch_file(PROTO / '租赁管理/组合出库列表.html',
           "this.classList.toggle('printed')\">打印</a>",
           "this.classList.toggle('printed')\">打印出货单</a>", 8, '页面打印→打印出货单')

# 销售出库列表 页面静态行：详情后追加 打印出货单
patch_file(PROTO / '销售管理/销售出库列表.html',
           '<a onclick="openModal(\'detailModal\')">详情</a>',
           '<a onclick="openModal(\'detailModal\')">详情</a><a onclick="window.print();this.classList.toggle(\'printed\')">打印出货单</a>',
           6, '页面新增打印出货单')

# demo-data.js：comboOutbounds 打印→打印出货单（8）；salesOutbounds 详情后追加（N 处）
dd = PROTO / '_data' / 'demo-data.js'
raw = dd.read_bytes(); txt = raw.decode('utf-8')

marks = [(m.start(), m.group(1)) for m in re.finditer(r'^  ([a-zA-Z_]+): \{', txt, re.M)]
marks.append((len(txt), 'END'))
segs = {}
for i in range(len(marks) - 1):
    segs[marks[i][1]] = (marks[i][0], marks[i + 1][0])

s, e = segs['comboOutbounds']
seg = txt[s:e]
old_op = '{"t": "打印", "act": "window.print();this.classList.toggle(\'printed\')"}'
new_op = '{"t": "打印出货单", "act": "window.print();this.classList.toggle(\'printed\')"}'
n = seg.count(old_op)
assert n == 8, f'comboOutbounds 打印 ops {n}'
txt = txt[:s] + seg.replace(old_op, new_op) + txt[e:]
print(f' ✓ demo-data comboOutbounds [打印→打印出货单] {n} 处')

s, e = segs['salesOutbounds']
seg = txt[s:e]
old_det = '{"t": "详情", "detail": true}'
new_det = '{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle(\'printed\')"}'
n = seg.count(old_det)
assert n == 6, f'salesOutbounds 详情 ops {n}'
txt = txt[:s] + seg.replace(old_det, new_det) + txt[e:]
print(f' ✓ demo-data salesOutbounds [新增打印出货单] {n} 处')

dd.write_bytes(txt.encode('utf-8'))
print('PASS 打印出货单改造完成')
