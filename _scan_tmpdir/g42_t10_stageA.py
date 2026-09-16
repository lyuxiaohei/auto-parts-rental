#!/usr/bin/env python3
# G42 T10 stage A: projectDocs 假键改实有键 + opLogs 同步（不含 lk 注入）
import io

DD = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js'
s = io.open(DD, encoding='utf-8').read()
assert 'AR-20260905-0029' in s and 'AR-20260831-0028' in s

e1_old = """    'AR-20260905-0029': { 'row': {"fields": {"type": "应收账单", "summary": "PRJ-2601 · 8 月下旬租金", "qty": "—", "status": "部分收款", "date": "2026-09-05", "ref": "SO-20260827-0036"}, "keyHtml": "<span class=\\"lk\\" onclick=\\"go('../财务协同/应收账单.html')\\">AR-20260905-0029</span>", "cells": ["PRJ-2601 · 8 月下旬租金", "<span class=\\"td-num\\">—</span>", "<span class=\\"tag tag-orange\\">部分收款</span>", "2026-09-05", "SO-20260827-0036"], "ops": [{"t": "查看单据", "act": "go('../财务协同/应收账单.html')"}]} },"""
e1_new = """    'AR-2026-08-PRJ2601': { 'row': {"fields": {"type": "应收账单", "summary": "PRJ-2601 · 8 月租金（按租赁出库汇总 486,200 元）", "qty": "—", "status": "部分收款", "date": "2026-08-31", "ref": "SO-20260827-0036"}, "keyHtml": "<span class=\\"lk\\" onclick=\\"go('../财务协同/应收账单.html')\\">AR-2026-08-PRJ2601</span>", "cells": ["PRJ-2601 · 8 月租金（按租赁出库汇总 486,200 元）", "<span class=\\"td-num\\">—</span>", "<span class=\\"tag tag-orange\\">部分收款</span>", "2026-08-31", "SO-20260827-0036"], "ops": [{"t": "查看单据", "act": "go('../财务协同/应收账单.html')"}]} },"""
e2_old = """    'AR-20260831-0028': { 'row': {"fields": {"type": "应收账单", "summary": "PRJ-2601 · 8 月中旬租金", "qty": "—", "status": "已收款", "date": "2026-08-31", "ref": "SO-20260820-0033"}, "keyHtml": "<span class=\\"lk\\" onclick=\\"go('../财务协同/应收账单.html')\\">AR-20260831-0028</span>", "cells": ["PRJ-2601 · 8 月中旬租金", "<span class=\\"td-num\\">—</span>", "<span class=\\"tag tag-green\\">已收款</span>", "2026-08-31", "SO-20260820-0033"], "ops": [{"t": "查看单据", "act": "go('../财务协同/应收账单.html')"}]} },"""
e2_new = """    'AR-2026-07-PRJ2601': { 'row': {"fields": {"type": "应收账单", "summary": "PRJ-2601 · 7 月租金（按租赁出库汇总 442,800 元 · 已结清）", "qty": "—", "status": "已结清", "date": "2026-07-31", "ref": "SO-20260820-0033"}, "keyHtml": "<span class=\\"lk\\" onclick=\\"go('../财务协同/应收账单.html')\\">AR-2026-07-PRJ2601</span>", "cells": ["PRJ-2601 · 7 月租金（按租赁出库汇总 442,800 元 · 已结清）", "<span class=\\"td-num\\">—</span>", "<span class=\\"tag tag-green\\">已结清</span>", "2026-07-31", "SO-20260820-0033"], "ops": [{"t": "查看单据", "act": "go('../财务协同/应收账单.html')"}]},"""
for old, new in [(e1_old, e1_new), (e2_old, e2_new)]:
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)

c = s.count('删除应收账单 AR-20260831-0028 失败')
assert c == 2, c
s = s.replace('删除应收账单 AR-20260831-0028 失败', '删除应收账单 AR-2026-07-PRJ2601 失败')
io.open(DD, 'w', encoding='utf-8').write(s)
print('stage A done')
