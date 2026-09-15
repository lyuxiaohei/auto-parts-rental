# -*- coding: utf-8 -*-
"""G36 C2（D-130）：stockFlows 每行 fields 增 qtyByProject（按库存实例项目归属的四态数量分摊）＋
总量口径修正（6 行 总量≠四态之和 → 改为四态之和，保证 全项目之和=不筛选总数）"""
import io, os, re, json

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
FP = os.path.join(ROOT, '_data', 'demo-data.js')
s = io.open(FP, encoding='utf-8', newline='').read()

# 行四态 = [在库, 退租在途, 客户端(租出), 退租待入库]；各项目分摊之和必须逐列等于行四态
QBP = {
    'XNC-AJZX-WBX': {'PRJ-2605': [0, 0, 640, 0]},
    'LJ-A100': {'PRJ-2601': [2500, 700, 500, 1200], 'PRJ-2602': [1600, 300, 200, 800], 'PRJ-2604': [1160, 200, 100, 400]},
    'LJ-B200': {'PRJ-2601': [1500, 250, 1000, 0], 'PRJ-2602': [1140, 150, 600, 0]},
    'LJ-C300': {'PRJ-2601': [1860, 0, 1600, 0]},
    'LJ-D400': {'PRJ-2601': [580, 280, 250, 600], 'PRJ-2604': [400, 200, 150, 400]},
    'LJ-F600': {'PRJ-2603': [900, 70, 0, 0], 'PRJ-2605': [620, 50, 0, 0]},
    'WBX-1210L': {'PRJ-2601': [1200, 100, 1800, 50], 'PRJ-2604': [920, 60, 1320, 30]},
    'WBX-1210M': {'PRJ-2602': [860, 40, 1020, 0]},
    'PLT-1210P': {'PRJ-2602': [800, 0, 1100, 40], 'PRJ-2603': [610, 0, 760, 20]},
    'BTC-6040': {'PRJ-2602': [3300, 40, 2480, 120]},
    'XNC-ZZ-WBX': {'PRJ-2605': [0, 0, 240, 0]},
    'XNC-ZZ-PLT': {'PRJ-2605': [0, 0, 120, 0]},
    'XNC-ZZ-BTC': {'PRJ-2605': [0, 0, 360, 0]},
    'RZRK-20260910-024': {'PRJ-2603': [500, 0, 0, 0]},
}
# 总量口径修正（原总量≠四态之和的 6 行；改后=四态之和，闭环对平）
TOTAL_FIX = {
    'LJ-A100': ('7,260', '9,660'),
    'LJ-D400': ('1,860', '2,860'),
    'WBX-1210L': ('2,480', '5,480'),
    'WBX-1210M': ('1,000', '1,920'),
    'PLT-1210P': ('1,700', '3,330'),
    'BTC-6040': ('3,940', '5,940'),
}

def rec_span(key):
    """stockFlows 键缩进为 5 空格且 CRLF——按正则定位记录起止"""
    pat = r'\r?\n[ ]*\'' + re.escape(key) + r'\': \{'
    m = re.search(pat, s)
    assert m, 'record not found: ' + key
    a = m.start()
    ent_close = s.index('\n  },', a)
    # 下一记录起始：键首字母大写（排除 'row'/'title'/'info' 等小写内层键）
    m2 = re.search(r'\r?\n[ ]*\'[A-Z][A-Za-z0-9\-\.]*\': \{', s[m.end():])
    b = m.end() + m2.start() if m2 else ent_close
    return a, min(b, ent_close)

for key, qbp in QBP.items():
    a, b = rec_span(key)
    blk = s[a:b]
    # 行四态原值校验：切出 cells 数组，按 '","' 分列取 idx3-7（在库/退租在途/客户端/退租待入库/总量）
    ca = blk.index('"cells": [')
    cb = blk.index('], "ops"', ca)
    cells_str = blk[ca + len('"cells": ['):cb]
    cells = cells_str.split('", "')
    assert len(cells) >= 8, key + ' cells split fail: %d' % len(cells)
    def cellnum(c):
        digits = re.findall(r'>[\d,]+<', c) or re.findall(r'[\d,]{2,}', c)
        return int(digits[-1].strip('><').replace(',', '')) if digits else 0
    row4 = [cellnum(cells[i]) for i in (3, 4, 5, 6)]
    total_cell_old = cells[7]
    # 分摊逐列求和必须等于行四态
    for ci in range(4):
        share_sum = sum(v[ci] for v in qbp.values())
        assert share_sum == row4[ci], '%s col%d: shares %d != row %d' % (key, ci, share_sum, row4[ci])
    # 插入 qtyByProject（fields 闭合前）
    assert 'qtyByProject' not in blk
    frag = ', "qtyByProject": ' + json.dumps(qbp, ensure_ascii=False, separators=(', ', ': ')) + '}, "cells"'
    assert blk.count('}, "cells"') == 1, key + ' cells anchor'
    blk2 = blk.replace('}, "cells"', frag)
    # 总量修正（仅本记录的总量 cell；逐列对平后 总量=四态之和）
    if key in TOTAL_FIX:
        old_v, new_v = TOTAL_FIX[key]
        m2 = re.search(r'([\d,]+)', total_cell_old)
        assert m2 and m2.group(1) == old_v, key + ' total cell mismatch: ' + total_cell_old[:60]
        new_total_cell = total_cell_old.replace(old_v, new_v, 1)
        assert blk2.count(total_cell_old) == 1, key + ' total cell not unique'
        blk2 = blk2.replace(total_cell_old, new_total_cell)
    s = s[:a] + blk2 + s[b:]
    print('%-16s qtyByProject %s 总量%s' % (key, list(qbp.keys()), '→' + TOTAL_FIX[key][1] if key in TOTAL_FIX else '='))

io.open(FP, 'w', encoding='utf-8', newline='').write(s)
print('C2 data DONE')
