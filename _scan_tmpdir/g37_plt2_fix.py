# -*- coding: utf-8 -*-
"""补插 XNC-ZZ-PLT2 行（T4 2a 的 blk 改动未回写主串的失误修复）"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
Q = chr(39)
P = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\_data\demo-data.js'
d = io.open(P, encoding='utf-8', newline='').read()
if Q + 'XNC-ZZ-PLT2' + Q + ': {' in d:
    print('已含（跳过）')
    sys.exit(0)
Q = chr(39)
BS = chr(92) + chr(34)  # \" 字面
PLT2 = """
    {Q}XNC-ZZ-PLT2{Q}: {{
      {Q}row{Q}: {{"fields": {{"name": "塑料托盘 1200×1000（长丰锂电·转租终端用户）", "cls": "租赁器具", "project": "PRJ-2603", "area": "转租终端仓", "loc": "—", "status": "客户转租出", "qtyByProject": {{"PRJ-2603": [0, 0, 80, 0]}}}}, "cells": ["塑料托盘 1200×1000（长丰锂电·转租终端用户）", "<span class={BS}tag tag-blue{BS}>租赁器具</span>", "PRJ-2603", "<span class={BS}td-num{BS}>0</span>", "<span class={BS}td-num{BS}>0</span>", "<span class={BS}td-num{BS}>80</span>", "<span class={BS}td-num{BS}>0</span>", "<span class={BS}td-num{BS}><b>80</b></span>", "<span class={BS}td-num{BS}>98.00</span>", "张", "转租终端仓"], "ops": [{{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=XNC-ZZ-PLT2')"}}, {{"t": "客户在租", "act": "openModal('rentDrillModal')"}}, {{"t": "终止转移", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260914-002')"}}]}},
    }},""".format(Q=Q, BS=BS)
i = d.index('stockFlows: {')
j = d.index('\n  },', i)
blk = d[i:j]
ki = blk.index(Q + 'XNC-ZZ-BTC' + Q + ': {')
ke = blk.index('\n    },', ki) + len('\n    },')
if '\r\n' in blk[:200]:
    PLT2 = PLT2.replace('\n', '\r\n')
blk = blk[:ke] + PLT2 + blk[ke:]
d = d[:i] + blk + d[j:]
io.open(P, 'w', encoding='utf-8', newline='').write(d)
print('PLT2 已插入')
