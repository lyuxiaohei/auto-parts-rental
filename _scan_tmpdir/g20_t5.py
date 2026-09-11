# -*- coding: utf-8 -*-
"""G20 T5（道远合并项）：租入单域「日租金」计价式→月租/按套口径（纪要 L72 无日租金）。
保留：否定式「无日租金」×N（feeSecTitle/pin#3/A03/A05）。"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROT = ROOT/'P3-R01-包装租赁管理后台原型'

# ---------- demo-data ----------
d_path = PROT/'_data'/'demo-data.js'
d = d_path.read_text(encoding='utf-8')
# 1a. rentInOrders 5 个 info 日租金→月租（值对齐档案参考价：WBX 45×n / PLT 12×n / BTC 10×n）
PAIRS = [
    ("'label': '日租金',\n          'text': '400.00 元 / 日（按单）'", "'label': '月租',\n          'text': '1,350.00 元 / 月（按单 · 45.00 元/只×30）'"),
    ("'label': '日租金',\n          'text': '1.20 元 / 日（按单）'", "'label': '月租',\n          'text': '600.00 元 / 月（按单 · 12.00 元/块×50）'"),
    ("'label': '日租金',\n          'text': '3.00 元 / 日（按单）'", "'label': '月租',\n          'text': '200.00 元 / 月（按单 · 10.00 元/只×20）'"),
    ("'label': '日租金',\n          'text': '2.50 元 / 日（按单）'", "'label': '月租',\n          'text': '150.00 元 / 月（按单 · 10.00 元/只×15）'"),
]
total = 0
for old, new in PAIRS:
    n = d.count(old)
    # 400.00 出现 2 次（30只/10只两行）——分别处理
    if old.find('400.00') != -1:
        n2 = n  # 2 处：1,350(×30) 与 450(×10)
        assert n == 2, f'400 锚 {n}'
        # 第一处（30 只行在前）→1350；第二处→450：按顺序替换
        i1 = d.find(old); i2 = d.find(old, i1+10)
        d = d[:i1] + new + d[i1+len(old):]
        j = d.find(old)
        d = d[:j] + "'label': '月租',\n          'text': '450.00 元 / 月（按单 · 45.00 元/只×10）'" + d[j+len(old):]
        total += 2
    else:
        assert n == 1, f'锚 {old[:24]} x{n}'
        d = d.replace(old, new)
        total += 1
assert total == 5, total
# 1b. dictItems BF-01 按天→按月（fields.abbr/name + cells 前2格 共4处）+ 释义行
old_bf = '"abbr": "按天", "name": "按天计租"'
assert d.count(old_bf) == 1, f'BF-01 fields {d.count(old_bf)}'
d = d.replace(old_bf, '"abbr": "按月", "name": "按月计租"')
old_cells = '"cells": ["按天", "按天计租",'
assert d.count(old_cells) == 1, f'BF-01 cells {d.count(old_cells)}'
d = d.replace(old_cells, '"cells": ["按月", "按月计租",')
old_d2 = '在租天数 × 日租金 · 围板箱/托盘租赁'
assert d.count(old_d2) == 1
d = d.replace(old_d2, '月租金 / 按套数单价 · 围板箱/托盘租赁')
# 复检：计价式「元 / 日」清零、否定式保留
assert '元 / 日' not in d, '仍有 元/日 计价式'
assert d.count('无日租金') >= 5, '否定式被误杀'
d_path.write_text(d, encoding='utf-8')
print('demo-data: 5 info→月租 + dictItems 按月计租 OK')

# ---------- 页面层 ----------
def patch(path, pairs):
    p = pathlib.Path(path)
    s = p.read_text(encoding='utf-8')
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, f'{path} 锚 {old[:26]} x{n}'
        s = s.replace(old, new)
    p.write_text(s, encoding='utf-8')

# 2. 租入单列表：th + dval（pin#1 在 A04 改；pin#3 否定式保留）
patch(PROT/'租赁管理'/'租入单列表.html', [
    ('<th>日租金(元)</th>', '<th>租金</th>'),
    ('（日租金 1.20 元/只）', '（月租 12.00 元/块）'),
])
# 3. 租入单审核弹窗 dval
patch(PROT/'租赁管理'/'弹窗'/'租入单审核.html', [
    ('（日租金 1.20 元/只）', '（月租 12.00 元/块）'),
])
# 4. 我的待办静态骨架
patch(PROT/'我的待办.html', [
    ('× 50 只 · 日租金 1.20</td>', '× 50 只 · 月租 12.00 元/块</td>'),
])
# 5. 数据字典静态骨架行（按天/按天计租/在租天数×日租金）
patch(PROT/'系统管理'/'数据字典.html', [
    ('<td>按天</td>', '<td>按月</td>'),
    ('<td>按天计租</td>', '<td>按月计租</td>'),
    ('<td>在租天数 × 日租金</td>', '<td>月租金 / 按套数单价</td>'),
])

# 6. A04 pin#1（租入单列表 pin-1 注入源）
a4 = (PROT/'P3-R01-A04-流程链标注数据.json').read_text(encoding='utf-8')
old_pin = '向路凯租入围板箱×30（日租金 400）'
assert a4.count(old_pin) == 1
a4 = a4.replace(old_pin, '向路凯租入围板箱×30（月租 45.00 元/只）')
(PROT/'P3-R01-A04-流程链标注数据.json').write_text(a4, encoding='utf-8')
import json; json.loads(a4)
print('pages + A04 pin OK')
