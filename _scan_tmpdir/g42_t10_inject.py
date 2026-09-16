#!/usr/bin/env python3
# G42 T10: 损益/看板财务单号互通
import io

DD = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js'
s = io.open(DD, encoding='utf-8').read()
assert 'AR-20260905-0029' in s and 'AR-20260831-0028' in s

# ---------- 1) projectDocs 两假键改实有键（键/fields/keyHtml/cells 全对齐实账单口径） ----------
e1_old = """    'AR-20260905-0029': { 'row': {"fields": {"type": "应收账单", "summary": "PRJ-2601 · 8 月下旬租金", "qty": "—", "status": "部分收款", "date": "2026-09-05", "ref": "SO-20260827-0036"}, "keyHtml": "<span class=\\"lk\\" onclick=\\"go('../财务协同/应收账单.html')\\">AR-20260905-0029</span>", "cells": ["PRJ-2601 · 8 月下旬租金", "<span class=\\"td-num\\">—</span>", "<span class=\\"tag tag-orange\\">部分收款</span>", "2026-09-05", "SO-20260827-0036"], "ops": [{"t": "查看单据", "act": "go('../财务协同/应收账单.html')"}]} },"""
e1_new = """    'AR-2026-08-PRJ2601': { 'row': {"fields": {"type": "应收账单", "summary": "PRJ-2601 · 8 月租金（按租赁出库汇总 486,200 元）", "qty": "—", "status": "部分收款", "date": "2026-08-31", "ref": "SO-20260827-0036"}, "keyHtml": "<span class=\\"lk\\" onclick=\\"go('../财务协同/应收账单.html')\\">AR-2026-08-PRJ2601</span>", "cells": ["PRJ-2601 · 8 月租金（按租赁出库汇总 486,200 元）", "<span class=\\"td-num\\">—</span>", "<span class=\\"tag tag-orange\\">部分收款</span>", "2026-08-31", "SO-20260827-0036"], "ops": [{"t": "查看单据", "act": "go('../财务协同/应收账单.html')"}]} },"""
e2_old = """    'AR-20260831-0028': { 'row': {"fields": {"type": "应收账单", "summary": "PRJ-2601 · 8 月中旬租金", "qty": "—", "status": "已收款", "date": "2026-08-31", "ref": "SO-20260820-0033"}, "keyHtml": "<span class=\\"lk\\" onclick=\\"go('../财务协同/应收账单.html')\\">AR-20260831-0028</span>", "cells": ["PRJ-2601 · 8 月中旬租金", "<span class=\\"td-num\\">—</span>", "<span class=\\"tag tag-green\\">已收款</span>", "2026-08-31", "SO-20260820-0033"], "ops": [{"t": "查看单据", "act": "go('../财务协同/应收账单.html')"}]} },"""
e2_new = """    'AR-2026-07-PRJ2601': { 'row': {"fields": {"type": "应收账单", "summary": "PRJ-2601 · 7 月租金（按租赁出库汇总 442,800 元 · 已结清）", "qty": "—", "status": "已结清", "date": "2026-07-31", "ref": "SO-20260820-0033"}, "keyHtml": "<span class=\\"lk\\" onclick=\\"go('../财务协同/应收账单.html')\\">AR-2026-07-PRJ2601</span>", "cells": ["PRJ-2601 · 7 月租金（按租赁出库汇总 442,800 元 · 已结清）", "<span class=\\"td-num\\">—</span>", "<span class=\\"tag tag-green\\">已结清</span>", "2026-07-31", "SO-20260820-0033"], "ops": [{"t": "查看单据", "act": "go('../财务协同/应收账单.html')"}]},"""
for old, new in [(e1_old, e1_new), (e2_old, e2_new)]:
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)

# opLogs 同名假单号同步（LOG-20260908-0890 摘要）
c = s.count('删除应收账单 AR-20260831-0028 失败')
assert c == 2, c
s = s.replace('删除应收账单 AR-20260831-0028 失败', '删除应收账单 AR-2026-07-PRJ2601 失败')

# ---------- 2) boardRows / profitRows 收入/成本格补实有单号 lk ----------
def lk(num, path):
    # 写入文件形态：JS 字符串内层转义（\" 与 \'）
    return ('<div style=\\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\\">'
            '<span class=\\"lk\\" onclick=\\"go(\'%s\')\\">%s</span></div>') % (path, num)

AR_PG_B = '../财务协同/应收账单.html'
AP_PG_B = '../财务协同/应付账单.html'
AR_PG_P = '应收账单.html'
AP_PG_P = '应付账单.html'

BOARD = {
    'PRJ-2601': ('486,200', [('AR-2026-08-PRJ2601', AR_PG_B)], '212,400', [('AP-20260901-008', AP_PG_B)]),
    'PRJ-2602': ('268,400', [('AR-2026-08-PRJ2602', AR_PG_B)], '96,200',  [('AP-20260830-007', AP_PG_B)]),
    'PRJ-2603': ('186,300', [('AR-2026-08-PRJ2603', AR_PG_B)], '58,900',  [('AP-20260903-009', AP_PG_B)]),
    'PRJ-2604': ('24,600',  [('AR-2026-09-PRJ2604-S1', AR_PG_B)], '-18,600', [('AP-20260903-010', AP_PG_B)]),
    'PRJ-2605': None,
    'PRJ-2599': None,
}
PROFIT = {
    'PRJ-2601': ('486,200.00', [('AR-2026-08-PRJ2601', AR_PG_P)], '261,900.00', [('AP-20260901-008', AP_PG_P)]),
    'PRJ-2602': ('186,400.00', [('AR-2026-08-PRJ2602', AR_PG_P)], '103,900.00', [('AP-20260830-007', AP_PG_P)]),
    'PRJ-2603': ('159,800.00', [('AR-2026-09-PRJ2603-U1', AR_PG_P)], '94,600.00', [('AP-20260903-009', AP_PG_P)]),
    'PRJ-2604': ('37,000.00',  [('AR-2026-09-PRJ2604-S1', AR_PG_P)], '55,600.00',  [('AP-20260903-010', AP_PG_P)]),
    'PRJ-2605': None,
    'PRJ-2599': None,
}

def esc_cell(num, bold=False):
    inner = ('<b>%s</b>' % num) if bold else num
    return '<span class=\\"td-num\\">%s</span>' % inner

def inject_lk(entity, plan):
    global s
    ent_start = s.index('  %s: {' % entity)
    for key, spec in plan.items():
        if spec is None:
            continue
        ks = s.index("    '%s': {" % key, ent_start)
        ke = s.index('\n', ks)
        blk = s[ks:ke]
        rev, revrefs, cost, costrefs = spec
        bold = (entity == 'profitRows')
        rev_old, cost_old = esc_cell(rev, bold), esc_cell(cost, bold)
        assert blk.count(rev_old) == 1, (entity, key, 'rev', blk.count(rev_old))
        assert blk.count(cost_old) == 1, (entity, key, 'cost', blk.count(cost_old))
        blk = blk.replace(rev_old, rev_old + ''.join(lk(n, p) for n, p in revrefs))
        blk = blk.replace(cost_old, cost_old + ''.join(lk(n, p) for n, p in costrefs))
        s = s[:ks] + blk + s[ke:]
        ent_start = ke

inject_lk('boardRows', BOARD)
inject_lk('profitRows', PROFIT)

assert s.count('AR-20260905-0029') == 0 and s.count('AR-20260831-0028') == 0
io.open(DD, 'w', encoding='utf-8').write(s)
print('T10 done')
