#!/usr/bin/env python3
# G42 T8: returnInbounds +TZRK-20260915-012（转租退租演示行）＋ stockEvents +EV-20260915-023
import io

DD = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js'
s = io.open(DD, encoding='utf-8').read()

# ---------- 1) returnInbounds 新行（插在实体闭合前） ----------
boundary = "  },  /* -------------------------------------------------------------------------- */\n  /* 租入归还单 rentInReturns"
assert s.count(boundary) == 1, 'returnInbounds boundary x' + str(s.count(boundary))
assert "'TZRK-20260915-012'" not in s

new_ri = """    'TZRK-20260915-012': {
      'row': {"fields": {"customer": "安吉智行物流", "project": "PRJ-2605", "appliance": "XNC-ZZ-WBX 围板箱 1200×1000×970", "mat": "XNC-ZZ-WBX", "matName": "围板箱 1200×1000×970", "qty": "100", "unit": "只", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-09-15", "result": "完好", "status": "已入库"}, "cells": ["安吉智行物流", "PRJ-2605", "XNC-ZZ-WBX 围板箱 1200×1000×970", "<span class=\\"td-num\\">100 只</span>", "转租物部分退回（终端在租 240 只中退 100 · 余 140 只继续在租）", "<span class=\\"tag tag-gray\\">自有回库</span>", "成品区 RB", "2026-09-15", "<span class=\\"tag tag-green\\">完好</span>", "<span class=\\"tag tag-green\\">已入库</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/退租入库详情.html?id=TZRK-20260915-012')"}]},
      'title': '退租入库单详情',
      'info': [
        {'label': '入库单号', 'text': 'TZRK-20260915-012', 'full': true},
        {'label': '状态', 'tag': '已入库'},
        {'label': '客户', 'text': '安吉智行物流', 'full': true},
        {'label': '所属项目', 'text': 'PRJ-2605'},
        {'label': '退租内容', 'text': 'XNC-ZZ-WBX 围板箱 1200×1000×970 × 100 只（部分退回）', 'full': true},
        {'label': '退租方式', 'text': '整套退回（不拆散）'},
        {'label': '拆散去向', 'text': '转租物经直接客户退回（XNC-ZZ-WBX · 客户转租出 → 退租入库）', 'full': true},
        {'label': '入库库房', 'text': '成品区 RB'},
        {'label': '入库日期', 'text': '2026-09-15'},
        {'label': '验收情况', 'text': '验收完好 · 止租日 2026-09-15（当日仍计租）', 'full': true}
      ],
      'feeSecTitle': '退回明细',
      'feeCols': ['物料编码', '物料名称', '来源', '单位', '数量', '去向'],
      'fees': [
        {'cells': ['XNC-ZZ-WBX', '围板箱 1200×1000×970', '客户转租', '只', '100', '自有回库 · 成品区 RB']}
      ],
      'chain': [
        {'role': '终端用户', 'name': '博世汽车部件（苏州） · 转租在租 240 只中退回 100 只'},
        {'role': '直接客户', 'name': '安吉智行物流（转租物经直接客户退回）'},
        {'role': '退租入库（本单）', 'name': 'TZRK-20260915-012', 'self': true}
      ],
      'timeline': [
        {'t': '09-15 10:00', 'text': '终端用户经直接客户退回转租围板箱 100 只', 'who': '张帆'},
        {'t': '09-15 15:30', 'text': '验收完好 · 整套回库（不勾稽原租赁单 D-106）', 'who': '张帆'},
        {'t': '—', 'text': '余 140 只继续终端在租 · 按持有量计租', 'who': '系统', 'off': true}
      ]
    },
"""
s = s.replace(boundary, new_ri + boundary)

# ---------- 2) stockEvents 追加行（EV-20260903-022 为末键·行带尾逗号） ----------
ev_line = None
for line in s.split('\n'):
    if line.strip().startswith("'EV-20260903-022':"):
        ev_line = line
        break
assert ev_line and s.count(ev_line) == 1, 'EV-022 anchor'
ev_new = """    'EV-20260915-023': { 'row': {"fields": {"date": "2026-09-15", "customer": "安吉智行物流", "project": "PRJ-2605", "mat": "XNC-ZZ-WBX", "matName": "围板箱 1200×1000×970", "qty": "100", "unit": "只", "dir": "退租", "doc": "TZRK-20260915-012", "side": "客户在租", "note": "转租物部分退回（终端在租 240 只退 100 · 余 140 只继续在租）"}, "cells": ["2026-09-15", "安吉智行物流", "PRJ-2605", "XNC-ZZ-WBX", "围板箱 1200×1000×970", "只", "<span class=\\"td-num\\">100</span>", "<span class=\\"tag tag-gray\\">退租</span>", "TZRK-20260915-012", "客户在租"]} },"""
s = s.replace(ev_line, ev_line + '\n' + ev_new)

assert s.count("'TZRK-20260915-012'") >= 2 and s.count("'EV-20260915-023'") == 1
io.open(DD, 'w', encoding='utf-8').write(s)
print('T8 injected: TZRK-20260915-012 + EV-20260915-023')
