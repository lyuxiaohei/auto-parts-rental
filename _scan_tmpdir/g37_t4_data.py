# -*- coding: utf-8 -*-
"""G37 T4：演示数据＋联动
1. demo-data +transferOutbounds（5 行·ZY- 前缀·PRJ-2605 按租出×3/PRJ-2603 按终端×1/已终止×1）
2. stockFlows：+XNC-ZZ-PLT2（PRJ-2603·客户转租出·80 张·对应 ZY-002）；XNC-ZZ-PLT 行回「客户端(租出)」（ZY-004 已终止）
3. 库存查询统计卡：客户转租出 720→680、在客户 12,480→12,600
4. detail-generic STATUS_CLS +待转移/已转移
5. 转移出库列表 ZY-002 行物料名改塑料托盘；新建页物料下拉动态取 products
幂等：各步守卫。"""
import io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
def rd(p): return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()
def wr(p, s): io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

# ============ 1. transferOutbounds 实体 ============
ENT = '''  transferOutbounds: {
    'ZY-20260915-005': {
      'row': {"fields": {"from": "安吉智行物流", "to": "博世汽车部件（苏州）", "material": "围板箱 1200×1000×970", "qty": "200 只", "settle": "按租出结算", "date": "2026-09-15", "project": "PRJ-2605", "status": "待转移"}, "cells": ["安吉智行物流", "博世汽车部件（苏州）", "围板箱 1200×1000×970", "<span class=\\"td-num\\">200 只</span>", "按租出结算", "2026-09-15", "<span class=\\"tag tag-orange\\">待转移</span>"], "ops": [{"t": "确认转移", "act": "zyConfirm(this)"}, {"t": "详情", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260915-005')"}]},
      title: '转移出库单详情',
      info: [
        { label: '转移单号', text: 'ZY-20260915-005', full: true },
        { label: '状态', tag: '待转移' },
        { label: '结算方式', text: '按租出结算（默认取项目档案，可按单覆盖）' },
        { label: '财务口径', text: '不生成应收账单——租金仍向直接客户（安吉智行物流）计收，转移单不进财务链路' },
        { label: '转移日期', text: '2026-09-15' },
        { label: '转出方（直接客户）', text: '安吉智行物流' },
        { label: '接收方（终端客户）', text: '博世汽车部件（苏州）' },
        { label: '关联项目', text: 'PRJ-2605 华骏重卡·蔚山基地 围板箱租赁扩建' },
        { label: '制单人', text: '沈婷' }
      ],
      feeCols: ['物料', '数量'],
      fees: [ { cells: ['围板箱 1200×1000×970', '200 只'] } ],
      chain: [
        { role: '直接客户', name: '安吉智行物流（在租 640 只）' },
        { role: '转移出库单（本单）', name: 'ZY-20260915-005', self: true },
        { role: '终端客户', name: '博世汽车部件（苏州）·待转移生效' }
      ],
      timeline: [
        { t: '09-15 09:20', text: '转移出库登记 · 提交', who: '沈婷' },
        { t: '—', text: '待确认转移 · 生效后库存状态转「客户转租出」', off: true }
      ]
    },
    'ZY-20260914-003': {
      'row': {"fields": {"from": "安吉智行物流", "to": "博世汽车部件（苏州）", "material": "料箱 600×400×340", "qty": "360 只", "settle": "按租出结算", "date": "2026-09-14", "project": "PRJ-2605", "status": "已转移"}, "cells": ["安吉智行物流", "博世汽车部件（苏州）", "料箱 600×400×340", "<span class=\\"td-num\\">360 只</span>", "按租出结算", "2026-09-14", "<span class=\\"tag tag-green\\">已转移</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260914-003')"}, {"t": "终止转移", "act": "zyStop(this)"}]},
      title: '转移出库单详情',
      info: [
        { label: '转移单号', text: 'ZY-20260914-003', full: true },
        { label: '状态', tag: '已转移' },
        { label: '结算方式', text: '按租出结算（默认取项目档案）' },
        { label: '财务口径', text: '不生成应收账单——租金仍向直接客户（安吉智行物流）计收，转移单不进财务链路' },
        { label: '转移日期', text: '2026-09-14' },
        { label: '转出方（直接客户）', text: '安吉智行物流' },
        { label: '接收方（终端客户）', text: '博世汽车部件（苏州）' },
        { label: '关联项目', text: 'PRJ-2605 华骏重卡·蔚山基地 围板箱租赁扩建' },
        { label: '库存状态', text: 'XNC-ZZ-BTC · 客户转租出（筛「客户转租出」可查）' },
        { label: '制单人', text: '沈婷' }
      ],
      feeCols: ['物料', '数量'],
      fees: [ { cells: ['料箱 600×400×340', '360 只'] } ],
      chain: [
        { role: '直接客户', name: '安吉智行物流' },
        { role: '转移出库单（本单）', name: 'ZY-20260914-003', self: true },
        { role: '终端客户', name: '博世汽车部件（苏州）' }
      ],
      timeline: [
        { t: '09-14 10:40', text: '转移出库登记 · 提交', who: '沈婷' },
        { t: '09-14 15:30', text: '确认转移 · 库存状态转「客户转租出」', who: '物流·赵磊' }
      ]
    },
    'ZY-20260914-002': {
      'row': {"fields": {"from": "长丰锂电科技", "to": "星辉动力电池有限公司", "material": "塑料托盘 1200×1000", "qty": "80 张", "settle": "按终端结算", "date": "2026-09-14", "project": "PRJ-2603", "status": "已转移"}, "cells": ["长丰锂电科技", "星辉动力电池有限公司", "塑料托盘 1200×1000", "<span class=\\"td-num\\">80 张</span>", "按终端结算", "2026-09-14", "<span class=\\"tag tag-green\\">已转移</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260914-002')"}, {"t": "终止转移", "act": "zyStop(this)"}]},
      title: '转移出库单详情',
      info: [
        { label: '转移单号', text: 'ZY-20260914-002', full: true },
        { label: '状态', tag: '已转移' },
        { label: '结算方式', text: '按终端结算（单据级覆盖·项目档案默认为按租出结算的特例项目）' },
        { label: '财务口径', text: '转移生效后后续应收账单主体切换为终端客户（星辉动力电池有限公司）·历史账单不回改' },
        { label: '转移日期', text: '2026-09-14' },
        { label: '转出方（直接客户）', text: '长丰锂电科技' },
        { label: '接收方（终端客户）', text: '星辉动力电池有限公司' },
        { label: '关联项目', text: 'PRJ-2603 长丰锂电·电池包周转箱租赁' },
        { label: '库存状态', text: 'XNC-ZZ-PLT2 · 客户转租出（筛「客户转租出」可查）' },
        { label: '制单人', text: '江强' }
      ],
      feeCols: ['物料', '数量'],
      fees: [ { cells: ['塑料托盘 1200×1000', '80 张'] } ],
      chain: [
        { role: '直接客户', name: '长丰锂电科技' },
        { role: '转移出库单（本单）', name: 'ZY-20260914-002', self: true },
        { role: '终端客户（账单主体）', name: '星辉动力电池有限公司' }
      ],
      timeline: [
        { t: '09-14 08:55', text: '转移出库登记 · 结算方式按终端（覆盖项目默认）', who: '江强' },
        { t: '09-14 14:10', text: '确认转移 · 库存状态转「客户转租出」· 后续账单主体切终端', who: '物流·赵磊' }
      ]
    },
    'ZY-20260914-001': {
      'row': {"fields": {"from": "安吉智行物流", "to": "博世汽车部件（苏州）", "material": "围板箱 1200×1000×970", "qty": "240 只", "settle": "按租出结算", "date": "2026-09-14", "project": "PRJ-2605", "status": "已转移"}, "cells": ["安吉智行物流", "博世汽车部件（苏州）", "围板箱 1200×1000×970", "<span class=\\"td-num\\">240 只</span>", "按租出结算", "2026-09-14", "<span class=\\"tag tag-green\\">已转移</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260914-001')"}, {"t": "终止转移", "act": "zyStop(this)"}]},
      title: '转移出库单详情',
      info: [
        { label: '转移单号', text: 'ZY-20260914-001', full: true },
        { label: '状态', tag: '已转移' },
        { label: '结算方式', text: '按租出结算（默认取项目档案）' },
        { label: '财务口径', text: '不生成应收账单——租金仍向直接客户（安吉智行物流）计收，转移单不进财务链路' },
        { label: '转移日期', text: '2026-09-14' },
        { label: '转出方（直接客户）', text: '安吉智行物流' },
        { label: '接收方（终端客户）', text: '博世汽车部件（苏州）' },
        { label: '关联项目', text: 'PRJ-2605 华骏重卡·蔚山基地 围板箱租赁扩建' },
        { label: '库存状态', text: 'XNC-ZZ-WBX · 客户转租出（筛「客户转租出」可查）' },
        { label: '制单人', text: '沈婷' }
      ],
      feeCols: ['物料', '数量'],
      fees: [ { cells: ['围板箱 1200×1000×970', '240 只'] } ],
      chain: [
        { role: '直接客户', name: '安吉智行物流' },
        { role: '转移出库单（本单）', name: 'ZY-20260914-001', self: true },
        { role: '终端客户', name: '博世汽车部件（苏州）' }
      ],
      timeline: [
        { t: '09-14 08:30', text: '转移出库登记 · 提交（库存查询「客户在租」行入口带出）', who: '沈婷' },
        { t: '09-14 11:20', text: '确认转移 · 库存状态转「客户转租出」', who: '物流·赵磊' }
      ]
    },
    'ZY-20260912-004': {
      'row': {"fields": {"from": "安吉智行物流", "to": "延锋汽车饰件（苏州）", "material": "塑料托盘 1200×1000", "qty": "120 张", "settle": "按租出结算", "date": "2026-09-12", "project": "PRJ-2605", "status": "已终止"}, "cells": ["安吉智行物流", "延锋汽车饰件（苏州）", "塑料托盘 1200×1000", "<span class=\\"td-num\\">120 张</span>", "按租出结算", "2026-09-12", "<span class=\\"tag tag-gray\\">已终止</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260912-004')"}]},
      title: '转移出库单详情',
      info: [
        { label: '转移单号', text: 'ZY-20260912-004', full: true },
        { label: '状态', tag: '已终止' },
        { label: '结算方式', text: '按租出结算（默认取项目档案）' },
        { label: '财务口径', text: '不生成应收账单——租金仍向直接客户（安吉智行物流）计收' },
        { label: '转移日期', text: '2026-09-12' },
        { label: '终止日期', text: '2026-09-13' },
        { label: '转出方（直接客户）', text: '安吉智行物流' },
        { label: '接收方（终端客户）', text: '延锋汽车饰件（苏州）' },
        { label: '关联项目', text: 'PRJ-2605 华骏重卡·蔚山基地 围板箱租赁扩建' },
        { label: '库存状态', text: '已回「在客户（租出）」· 安吉智行客户虚拟仓（XNC-ZZ-PLT）' },
        { label: '制单人', text: '沈婷' }
      ],
      feeCols: ['物料', '数量'],
      fees: [ { cells: ['塑料托盘 1200×1000', '120 张'] } ],
      chain: [
        { role: '直接客户', name: '安吉智行物流' },
        { role: '转移出库单（本单·已终止）', name: 'ZY-20260912-004', self: true },
        { role: '终端客户', name: '延锋汽车饰件（苏州）·已追回' }
      ],
      timeline: [
        { t: '09-12 14:00', text: '转移出库登记 · 提交', who: '沈婷' },
        { t: '09-12 17:45', text: '确认转移 · 库存状态转「客户转租出」', who: '物流·赵磊' },
        { t: '09-13 09:30', text: '终止转移 · 库存状态回「在客户（租出）」', who: '物流·赵磊' }
      ]
    },
  },
};'''

pd = os.path.join('_data', 'demo-data.js')
d = rd(pd)
if 'transferOutbounds' not in d:
    crlf = '\r\n' in d[-200:]
    ent = ENT.replace('\n', '\r\n') if crlf else ENT
    assert d.endswith('};'), 'demo-data 尾部形态异常'
    d = d[:-len('};')] + ent
    wr(pd, d)
    print('1 transferOutbounds 5 行已加（实体 39→40）')
else:
    print('1 transferOutbounds：已含（跳过）')

# ============ 2. stockFlows：PLT2 新行＋PLT 行回退 ============
d = rd(pd)
changed = False
if "'XNC-ZZ-PLT2'" not in d:
    # 2a. 新行插在 XNC-ZZ-BTC 记录后（stockFlows 内·行尾随宿主）
    i = d.index('stockFlows: {')
    j = d.index('\n  },', i)
    blk = d[i:j]
    ki = blk.index("'XNC-ZZ-BTC': {")
    ke = blk.index('\n    },', ki) + len('\n    },')
    PLT2 = '''
    'XNC-ZZ-PLT2': {
      'row': {"fields": {"name": "塑料托盘 1200×1000（长丰锂电·转租终端用户）", "cls": "租赁器具", "project": "PRJ-2603", "area": "转租终端仓", "loc": "—", "status": "客户转租出", "qtyByProject": {"PRJ-2603": [0, 0, 80, 0]}}, "cells": ["塑料托盘 1200×1000（长丰锂电·转租终端用户）", "<span class=\\"tag tag-blue\\">租赁器具</span>", "PRJ-2603", "<span class=\\"td-num\\">0</span>", "<span class=\\"td-num\\">0</span>", "<span class=\\"td-num\\">80</span>", "<span class=\\"td-num\\">0</span>", "<span class=\\"td-num\\"><b>80</b></span>", "<span class=\\"td-num\\">98.00</span>", "张", "转租终端仓"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=XNC-ZZ-PLT2')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}, {"t": "终止转移", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260914-002')"}]},
    },'''
    if '\r\n' in blk[:200]:
        PLT2 = PLT2.replace('\n', '\r\n')
    blk = blk[:ke] + PLT2 + blk[ke:]
    d = d[:i] + blk + d[j:]
    changed = True
    print('2a stockFlows +XNC-ZZ-PLT2 行（PRJ-2603·客户转租出·80 张）')

if changed or 'XNC-ZZ-PLT' in d:
    # 2b. XNC-ZZ-PLT 行回退：客户转租出→客户端(租出)·名称/area/loc 改
    d2 = rd(pd)
    i = d2.index('stockFlows: {')
    j = d2.index('\n  },', i)
    blk = d2[i:j]
    ki = blk.index("'XNC-ZZ-PLT': {")
    ke = blk.index('\n    },', ki)
    ln = blk[ki:ke]
    if '"status": "客户转租出"' in ln:
        ln2 = ln
        ln2 = ln2.replace('"name": "塑料托盘 1200×1000（安吉智行·转租终端用户）"', '"name": "塑料托盘 1200×1000（安吉智行·客户虚拟仓）"')
        ln2 = ln2.replace('"area": "转租终端仓", "loc": "—", "status": "客户转租出"', '"area": "客户虚拟仓", "loc": "XNC-AJZX", "status": "客户端(租出)"')
        # cells 首格名称+末格仓库名
        ln2 = ln2.replace('["塑料托盘 1200×1000（安吉智行·转租终端用户）"', '["塑料托盘 1200×1000（安吉智行·客户虚拟仓）"')
        ln2 = ln2.replace('"张", "转租终端仓"]', '"张", "客户虚拟仓"]')
        assert ln2 != ln, 'PLT 行替换无变化'
        blk = blk[:ki] + ln2 + blk[ke:]
        d2 = d2[:i] + blk + d2[j:]
        wr(pd, d2)
        print('2b XNC-ZZ-PLT 行回退：客户端(租出)·客户虚拟仓（ZY-004 已终止）')
    else:
        print('2b PLT 行：已是租出态（跳过）')

# ============ 3. 统计卡 ============
pk = os.path.join('仓储作业', '库存查询.html')
s = rd(pk)
if '<div class="st-num">720<span class="unit">只</span></div>' in s:
    assert s.count('<div class="st-num">720<span class="unit">只</span></div>') == 1
    s = s.replace('<div class="st-num">720<span class="unit">只</span></div>', '<div class="st-num">680<span class="unit">只</span></div>')
    assert s.count('<div class="st-num">12,480<span class="unit">只/套</span></div>') == 1
    s = s.replace('<div class="st-num">12,480<span class="unit">只/套</span></div>', '<div class="st-num">12,600<span class="unit">只/套</span></div>')
    wr(pk, s)
    print('3 统计卡：客户转租出 720→680·在客户 12,480→12,600')
else:
    print('3 统计卡：已改（跳过）')

# ============ 4. detail-generic STATUS_CLS ============
pg = os.path.join('_data', 'detail-generic.js')
g = rd(pg)
if "'待转移'" not in g:
    anchor = "'已终止': 'tag-gray',"
    assert g.count(anchor) == 1
    g = g.replace(anchor, anchor + "\n    '待转移': 'tag-orange', '已转移': 'tag-green',")
    wr(pg, g)
    print('4 detail-generic STATUS_CLS +待转移/已转移')
else:
    print('4 detail-generic：已含（跳过）')

# ============ 5a. 列表页 ZY-002 物料名/单位 ============
pl = os.path.join('租赁管理', '转移出库列表.html')
sl = rd(pl)
if '电池包周转箱 1400×1000×680' in sl:
    sl = sl.replace('电池包周转箱 1400×1000×680', '塑料托盘 1200×1000')
    sl = sl.replace('<span class="td-num">80 只</span>', '<span class="td-num">80 张</span>')
    wr(pl, sl)
    print('5a 列表页 ZY-002：物料=塑料托盘 1200×1000·80 张')
else:
    print('5a 列表页：已改（跳过）')

# ============ 5b. 新建页物料下拉动态取 products ============
pf = os.path.join('租赁管理', '转移出库新建.html')
sf = rd(pf)
if 'zyFillMat' not in sf:
    old_sel = '<select id="zyMat"><option selected>围板箱 1200×1000×970</option><option>塑料托盘 1200×1000</option><option>料箱 600×400×340</option><option>电池包周转箱 1400×1000×680</option></select>'
    assert sf.count(old_sel) == 1
    new_sel = '<select id="zyMat"><option selected>围板箱 1200×1000×970</option><option>塑料托盘 1200×1000</option></select>'
    sf = sf.replace(old_sel, new_sel)
    # 动态填充脚本（URL 参数块前插）
    anchor_fn = '(function () {\n  /* 库存查询行内「转移出库」跳转带参'
    af = sf.index(anchor_fn) if anchor_fn in sf else sf.index('/* 库存查询行内')
    fill = ('/* 物料下拉动态取产品档案 */\n'
            'function zyFillMat() {\n'
            '  var P = (window.DEMO_DATA || {}).products || {};\n'
            '  var names = [];\n'
            '  Object.keys(P).forEach(function (k) { var f = (P[k].row || {}).fields || {}; if (f.name && f.status !== \'停用\') names.push(f.name); });\n'
            '  var m = document.getElementById(\'zyMat\');\n'
            '  if (!m || !names.length) return;\n'
            '  var cur = m.value;\n'
            '  m.innerHTML = names.sort().map(function (n) { return \'<option>\' + n + \'</option>\'; }).join(\'\');\n'
            '  if (names.indexOf(cur) > -1) m.value = cur;\n'
            '}\n'
            'zyFillMat();\n')
    nl = '\r\n' if '\r\n' in sf[af-50:af] else '\n'
    sf = sf[:af] + fill.replace('\n', nl) + sf[af:]
    wr(pf, sf)
    print('5b 新建页物料下拉动态取 products')
else:
    print('5b 新建页：已改（跳过）')
print('T4 DONE')
