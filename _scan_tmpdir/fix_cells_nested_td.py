# -*- coding: utf-8 -*-
"""修复·2026-09-08：demo-data.js 192 条 row 的 cells 误带外层 <td> 标签
（list-generic 渲染时会再包一层 → 嵌套 td → 浏览器拆出空白列）
剥离规则：每个 cell 去掉首部 <td...> 与尾部 </td>（幂等，试点 17 条不含 <td> 不动）
"""
import sys, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DD = ROOT / 'P3-R01-包装租赁管理后台原型' / '_data' / 'demo-data.js'

raw = DD.read_bytes().decode('utf-8')
lines = raw.split('\n')
n_fix, n_row = 0, 0
out = []
for ln in lines:
    m = re.match(r"^(      'row': )({.*})(,)$", ln)
    if m:
        n_row += 1
        d = json.loads(m.group(2))
        cells = d.get('cells')
        if cells and any(isinstance(c, str) and c.lstrip().startswith('<td') for c in cells):
            d['cells'] = [re.sub(r'^\s*<td[^>]*>|</td>\s*$', '', c) for c in cells]
            out.append(m.group(1) + json.dumps(d, ensure_ascii=False) + m.group(3))
            n_fix += 1
            continue
    out.append(ln)
DD.write_bytes('\n'.join(out).encode('utf-8'))
print(f'row 行 {n_row}，修复 {n_fix}（预期 192）')
assert n_fix == 192, '修复计数不符'
# 复核：不应再有 cells 带 <td
raw2 = DD.read_bytes().decode('utf-8')
bad = [ln[:60] for ln in raw2.split('\n') if "'row':" in ln and re.search(r'"cells": \["<td', ln)]
assert not bad, f'仍有 {len(bad)} 行'
print('复核：cells 已无 <td> 外壳；demo-data.js 保持 LF')
