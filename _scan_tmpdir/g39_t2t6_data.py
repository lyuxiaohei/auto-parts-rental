# -*- coding: utf-8 -*-
"""G39 T2+T6 · stockEvents 事件流水 + 演示数据（多次出库+部分退租·两计费方式）+ bomList/products/dictItems 增量
精确替换＋实体域锚定＋断言＋幂等"""
import io, re

P = r'P3-R01-包装租赁管理后台原型\_data\demo-data.js'
raw = io.open(P, 'rb').read().decode('utf-8')
orig = raw

def ent_span(s, name):
    m = re.search(r'^ {2}(?:/\*.*?\*/[ \t]*)?%s: \{' % name, s, re.M)
    assert m, 'entity not found: ' + name
    nxt = re.search(r'^ {2}(?:/\*.*?\*/[ \t]*)?[A-Za-z_][A-Za-z0-9_]*: \{', s[m.end():], re.M)
    return m.start(), (m.end() + nxt.start()) if nxt else len(s)

def insert_before_close(s, entity, block):
    """在实体收尾 `  },` 前插入 block（幂等：block 首键已存在则跳过）"""
    a, b = ent_span(s, entity)
    seg = s[a:b]
    first_key = re.search(r"'([A-Za-z0-9\-]+)':", block).group(1)
    if ("'" + first_key + "'") in seg:
        print('  [skip] %s 已有 %s' % (entity, first_key))
        return s
    idx = seg.rfind('\r\n  },')
    assert idx > 0, entity + ' close not found'
    seg2 = seg[:idx] + '\r\n' + block + '\r\n  },' + seg[idx + len('\r\n  },'):]
    return s[:a] + seg2 + s[b:]

# ============ A) products +buyPrice/salePrice（参考价带出数据源） ============
BUY = {
 '围板箱 1200×1000×970': ('380.00', '—'), '围板箱 1200×1000×590': ('340.00', '—'),
 '木托盘 1200×1000': ('95.00', '—'), '塑料托盘 1200×1000': ('110.00', '—'),
 '料箱 600×400×220（带盖）': ('78.00', '—'), '料箱 600×400×340': ('85.00', '—'),
 '锁扣组件': ('6.80', '9.80'), '铰链': ('4.20', '6.50'), '围板': ('52.00', '68.00'),
 '箱盖': ('36.00', '48.00'), '底托架': ('78.00', '98.00'), '内衬': ('15.50', '22.00'),
 '卡板箱 1040×800×590': ('120.00', '—'), '金属托盘 1200×1000': ('165.00', '—'), '料架 1850×1000×1200': ('420.00', '—'),
}
if '"buyPrice":' not in raw:
    a, b = ent_span(raw, 'products')
    seg = raw[a:b]
    n = 0
    for name, (bp, sp) in BUY.items():
        anchor = '"name": "%s"' % name
        assert seg.count(anchor) == 1, 'products name anchor: ' + name
        i = seg.find(anchor)
        j = seg.find(', "cells": [', i)
        assert j > 0
        seg = seg[:j] + ', "buyPrice": "%s", "salePrice": "%s"' % (bp, sp) + seg[j:]
        n += 1
    assert n == 15
    raw = raw[:a] + seg + raw[b:]
    print('[A] products +buyPrice/salePrice ×15')

# ============ B) bomList +billing（计费方式随料带出·组合件闭环） ============
BL = {'ZH-2601-A': '按时间周期', 'ZH-2602-B': '按时间周期', 'ZH-2603-C': '按次',
      'ZT-2201': '按次', 'JP-3105': '按时间周期', 'WBX-1210L': '按时间周期'}
_a, _b = ent_span(raw, 'bomList')
if '"billing":' not in raw[_a:_b]:
    a, b = _a, _b
    seg = raw[a:b]
    for key, val in BL.items():
        m = re.search(r"^    '%s': \{ 'row': \{\"fields\": \{\"name\": \"[^\"]+\", \"ver\": \"[^\"]+\", \"status\"" % key, seg, re.M)
        assert m, 'bomList anchor: ' + key
        line_end = seg.find('"status"', m.start())
        seg = seg[:line_end] + '"billing": "%s", ' % val + seg[line_end:]
    raw = raw[:a] + seg + raw[b:]
    print('[B] bomList +billing ×6')

# ============ C) dictItems：BF-06 按时间周期 + BF-05 释义更新 ============
if "'BF-06'" not in raw:
    a, b = ent_span(raw, 'dictItems')
    seg = raw[a:b]
    m = re.search(r"^    'BF-05': \{ 'row': .*?\},\r\n", seg, re.M)
    assert m, 'BF-05 anchor'
    line = m.group(0)
    # BF-05 释义更新（G39 后「本期无日租金业务」口径作废）
    old_desc = '日租金 × 在租天数 · 短期备用口径（本期无日租金业务）'
    new_desc = '周期单位 · 三段式档案参考价用（G39 起单据侧直录日租金）'
    assert old_desc in line
    line2 = line.replace(old_desc, new_desc)
    bf06 = ("    'BF-06': { 'row': {\"fields\": {\"category\": \"计费方式\", \"abbr\": \"按时间周期\", \"name\": \"按时间周期计租（直录日租金）\", \"status\": \"启用\"}, "
            "\"cells\": [\"按时间周期\", \"按时间周期计租（直录日租金）\", \"<span class=\\\"td-num\\\">6</span>\", \"日租金 × 每日在租数量 × 天数 · 按持有量计租（D-148）\", \"<span class=\\\"tag tag-green\\\">启用</span>\"]} },\r\n")
    seg2 = seg[:m.start()] + line2 + bf06 + seg[m.end():]
    raw = raw[:a] + seg2 + raw[b:]
    print('[C] dictItems BF-06 + BF-05 释义更新')

# ============ D) returnInbounds +TZRK-20260908-011（T6 部分退租） ============
TZ_NEW = """    'TZRK-20260908-011': {
      'row': {"fields": {"customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "appliance": "ZH-2601-A 驾驶室围板箱整箱套件", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "120", "unit": "套", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-09-08", "result": "完好", "status": "已入库"}, "cells": ["华骏重卡汽车有限公司", "PRJ-2601", "ZH-2601-A 驾驶室围板箱整箱套件", "<span class=\\"td-num\\">120 套</span>", "整套退回 120 套 · 部分退租（在租 530 套中退 120）", "<span class=\\"tag tag-gray\\">自有回库</span>", "成品区 RB", "2026-09-08", "<span class=\\"tag tag-green\\">完好</span>", "<span class=\\"tag tag-green\\">已入库</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/退租入库详情.html?id=TZRK-20260908-011')"}]},
      'title': '退租入库单详情',
      'info': [
        {'label': '入库单号', 'text': 'TZRK-20260908-011', 'full': true},
        {'label': '状态', 'tag': '已入库'},
        {'label': '客户', 'text': '华骏重卡汽车有限公司', 'full': true},
        {'label': '所属项目', 'text': 'PRJ-2601'},
        {'label': '退租内容', 'text': 'ZH-2601-A 驾驶室围板箱整箱套件 × 120 套（部分退租）', 'full': true},
        {'label': '退租方式', 'text': '整套退回（不拆散）'},
        {'label': '拆散去向', 'text': '自有回库 · 循环再出租', 'full': true},
        {'label': '入库库房', 'text': '成品区 RB'},
        {'label': '入库日期', 'text': '2026-09-08'},
        {'label': '验收情况', 'text': '验收完好 · 止租日 2026-09-08（当日仍计租）', 'full': true}
      ],
      'feeSecTitle': '退回明细',
      'feeCols': ['物料编码', '物料名称', '来源', '单位', '数量', '去向'],
      'fees': [
        {'cells': ['ZH-2601-A', '驾驶室围板箱整箱套件', '自购', '套', '120', '自有回库 · 成品区 RB']}
      ],
      'chain': [
        {'role': '租赁出库（多次）', 'name': 'CK-20260829-012 / -015 / -016', 'url': '租赁管理/租赁出库列表.html'},
        {'role': '退租入库（本单）', 'name': 'TZRK-20260908-011 · 部分退租', 'self': true},
        {'role': '库存查询 · 客户在租', 'name': '止租后每日在租量由 stockEvents 派生', 'url': '仓储作业/库存查询.html'}
      ],
      'timeline': [
        {'t': '09-08 10:20', 'text': '客户退回 120 套 · 登记入库', 'who': '张帆'},
        {'t': '09-08 16:00', 'text': '验收完好 · 整套回库（不勾稽原租赁单 D-106）', 'who': '张帆'},
        {'t': '—', 'text': '剩余在租 410 套 · 继续按持有量计租', 'who': '系统', 'off': true}
      ]
    },"""
raw = insert_before_close(raw, 'returnInbounds', TZ_NEW)
print('[D] returnInbounds +TZRK-20260908-011')

# ============ E) receivableBills +D1 +D2 ============
D1 = """    'AR-2026-09-PRJ2601-D1': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "btype": "租赁费（按持有量×天数）", "docs": "stockEvents 事件流水 ×3", "gen": "按持有量×天数", "date": "2026-09-11", "status": "未开票"}, "cells": ["2026-09", "PRJ-2601", "华骏重卡汽车有限公司", "租赁费（按持有量×天数）", "期段 09-01 ~ 09-10 · 每日在租量合计 4,940 套天", "<span class=\\"td-num\\"><b>9,880.00</b></span>", "<span class=\\"td-num\\">0.00</span>", "<span class=\\"tag tag-red\\">未开票</span>", "<span class=\\"tag tag-blue\\">按持有量×天数</span>", "2026-09-11 09:00"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-09-PRJ2601-D1',
      billType: '租赁费',
      status: '未开票',
      customer: '华骏重卡汽车有限公司',
      project: 'PRJ-2601',
      period: '2026-09',
      amount: 9880,
      verified: 0,
      genMode: '按持有量×天数',
      genDate: '2026-09-11',
      feeType: '租赁费（按持有量×天数）',
      segCols: ['物料编码', '物料名称', '单位', '起租日期', '止租日期', '天数', '在租量·套天', '日租金(元/天)', '小计(元)'],
      fees: [
        {src: 'stockEvents · 华骏 × ZH-2601-A', desc: '按持有量计租 · 期段 2026-09-01 ~ 2026-09-10（09-03 增 60 套 · 09-08 退租 120 套当日仍计）', qty: '4,940 套天', price: '2.00', amount: 9880, url: '租赁管理/租赁出库列表.html', cells: ['ZH-2601-A', '驾驶室围板箱整箱套件', '套', '2026-09-01', '2026-09-10', '10', '4,940', '2.00', '9,880.00']}
      ],
      chain: [
        {role: '租赁出库（多次）', name: 'CK-20260829-012 / -015 / -016', url: '租赁管理/租赁出库列表.html'},
        {role: '退租入库（部分）', name: 'TZRK-20260908-011 · 120 套', url: '租赁管理/退租入库列表.html'},
        {role: '应收账单（本单）', name: 'AR-2026-09-PRJ2601-D1 · 按持有量×天数', self: true},
        {role: '开票登记', name: '待开票', url: '财务协同/开票登记.html'}
      ],
      timeline: [
        {t: '09-01', text: '期段起 · 每日在租 470 套', who: '系统'},
        {t: '09-03', text: '循环出库 +60 套 · 每日在租 530 套', who: '系统'},
        {t: '09-08', text: '部分退租 120 套 · 当日仍计 530 套', who: '系统'},
        {t: '09-09', text: '起每日在租 410 套', who: '系统'},
        {t: '09-11', text: '账单生成 · 4,940 套天 × 2.00 元 = 9,880.00 元', who: '系统'}
      ]
    },"""
D2 = """    'AR-2026-09-PRJ2603-D1': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2603", "customer": "星途新能源汽车科技有限公司", "btype": "租赁费（按次套数）", "docs": "CK-20260829-013 ×1 次", "gen": "按次套数", "date": "2026-09-11", "status": "未开票"}, "cells": ["2026-09", "PRJ-2603", "星途新能源汽车科技有限公司", "租赁费（按次套数）", "出库 1 次 × 60 套 × 4.50 元/次", "<span class=\\"td-num\\"><b>270.00</b></span>", "<span class=\\"td-num\\">0.00</span>", "<span class=\\"tag tag-red\\">未开票</span>", "<span class=\\"tag tag-blue\\">按次套数</span>", "2026-09-11 09:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-09-PRJ2603-D1',
      billType: '租赁费',
      status: '未开票',
      customer: '星途新能源汽车科技有限公司',
      project: 'PRJ-2603',
      period: '2026-09',
      amount: 270,
      verified: 0,
      genMode: '按次套数',
      genDate: '2026-09-11',
      feeType: '租赁费（按次套数）',
      segCols: ['物料编码', '物料名称', '单位', '数量', '次数', '次单价(元/次)', '小计(元)'],
      fees: [
        {src: 'CK-20260829-013', desc: '按次计费 · 出库 1 次 × 60 套 × 4.50 元/次（部分退租 20 套不影响按次计费口径）', qty: '60 套', price: '4.50', amount: 270, url: '租赁管理/租赁出库列表.html', cells: ['ZH-2603-C', '电池托盘护角套件', '套', '60', '1', '4.50', '270.00']}
      ],
      chain: [
        {role: '租赁出库', name: 'CK-20260829-013 · 60 套', url: '租赁管理/租赁出库列表.html'},
        {role: '应收账单（本单）', name: 'AR-2026-09-PRJ2603-D1 · 按次套数', self: true},
        {role: '开票登记', name: '待开票', url: '财务协同/开票登记.html'}
      ],
      timeline: [
        {t: '08-29', text: '租赁出库 60 套 · 按次计费第 1 次', who: '物流·赵磊'},
        {t: '08-31', text: '部分退租 20 套（按次已计·不冲减）', who: '张帆'},
        {t: '09-11', text: '账单生成 · 1 次 × 60 套 × 4.50 = 270.00 元', who: '系统'}
      ]
    },"""
raw = insert_before_close(raw, 'receivableBills', D1)
raw = insert_before_close(raw, 'receivableBills', D2)
print('[E] receivableBills +D1 +D2')

# ============ F) payableBills +AP（租入侧按持有量×天数） ============
AP = """    'AP-20260911-013': {
      'row': {"fields": {"supplier": "环通循环包装运营（上海）有限公司", "btype": "租金应付（按持有量×天数）", "project": "PRJ-2603", "period": "2026-09", "ref": "RZD-20260815-003 / RZD-20260815-005", "inbound": "RZRK-20260816-021 / -022", "date": "2026-09-11", "status": "未付款"}, "cells": ["环通循环包装运营（上海）有限公司", "<span class=\\"tag tag-orange\\">租金应付（按持有量×天数）</span>", "PRJ-2603", "2026-09", "RZD-20260815-003 / RZD-20260815-005", "RZRK-20260816-021 / -022", "1,080.00", "0.00", "1,080.00", "2026-09-11", "2026-10-13", "<span class=\\"tag tag-orange\\">未付款</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}]},
      billNo: 'AP-20260911-013',
      billType: '租金应付（按持有量×天数）',
      status: '未付款',
      supplier: '环通循环包装运营（上海）有限公司',
      project: 'PRJ-2603',
      period: '2026-09',
      amount: 1080,
      paid: 0,
      genMode: '按持有量×天数',
      genDate: '2026-09-11',
      refs: [
        {label: '关联租入单', no: 'RZD-20260815-003 / RZD-20260815-005', url: '租入管理/租入单列表.html'},
        {label: '关联租入入库', no: 'RZRK-20260816-021 / RZRK-20260816-022', url: '租入管理/租入入库列表.html'}
      ],
      segCols: ['物料编码', '物料名称', '单位', '起租日期', '止租日期', '天数', '持有量·只天', '日租金(元/天)', '小计(元)'],
      fees: [
        {src: 'stockEvents · 环通 × WBX-1210L', desc: '按持有量计租 · 期段 2026-08-16 ~ 2026-09-03（每日持有 40 只 · 09-03 归还当日仍计）', qty: '720 只天', price: '1.50', amount: 1080, url: '租入管理/租入入库列表.html', cells: ['WBX-1210L', '围板箱 1200×1000×970', '只', '2026-08-16', '2026-09-03', '18', '720', '1.50', '1,080.00']}
      ],
      chain: [
        {role: '租入入库', name: 'RZRK-20260816-021 / -022 · 40 只', url: '租入管理/租入入库列表.html'},
        {role: '应付账单（本单）', name: 'AP-20260911-013 · 按持有量×天数', self: true},
        {role: '付款登记', name: '待付款', url: '财务协同/付款登记.html'}
      ],
      timeline: [
        {t: '08-16', text: '租入入库 30+10 只 · 期段起', who: '张帆'},
        {t: '09-03', text: '整退 30 / 分流 4 只 · 当日仍计 40 只', who: '林国栋'},
        {t: '09-11', text: '账单生成 · 720 只天 × 1.50 元 = 1,080.00 元', who: '系统'}
      ]
    },"""
raw = insert_before_close(raw, 'payableBills', AP)
print('[F] payableBills +AP-20260911-013')

# ============ G) stockEvents 新实体（文件尾追加） ============
def ev(key, date, cust, proj, mat, matName, unit, qty, dr, doc, side, note=None):
    cells_doc = doc
    f = '{"date": "%s", "customer": "%s", "project": "%s", "mat": "%s", "matName": "%s", "qty": "%s", "unit": "%s", "dir": "%s", "doc": "%s", "side": "%s"%s}' % (
        date, cust, proj, mat, matName, qty, unit, dr, doc, side, (', "note": "%s"' % note) if note else '')
    c = '["%s", "%s", "%s", "%s", "%s", "%s", "<span class=\\"td-num\\">%s</span>", "<span class=\\"tag tag-%s\\">%s</span>", "%s", "%s"]' % (
        date, cust, proj, mat, matName, unit, qty, {'出库':'blue','退租':'green','归还':'gray','调拨':'purple','其他出入库':'gray'}[dr], dr, doc, side)
    return "    '%s': { 'row': {\"fields\": %s, \"cells\": %s} }," % (key, f, c)

HJ = '华骏重卡汽车有限公司'; DH = '东海商用汽车有限公司宁波分公司'; XT = '星途新能源汽车科技有限公司'; CF = '长风汽车制造有限公司'; HT = '环通循环包装运营（上海）有限公司'
EVROWS = [
 ev('EV-20260814-001', '2026-08-14', HJ, 'PRJ-2601', 'ZH-2601-A', '驾驶室围板箱整箱套件', '套', '200', '其他出入库', '期初结转', '客户在租', '期初在租结转（历史出库未入流水·不做历史迁移）'),
 ev('EV-20260818-002', '2026-08-18', DH, 'PRJ-2602', 'PLT-1210P', '塑料托盘', '块', '150', '其他出入库', '期初结转', '客户在租', '期初在租结转'),
 ev('EV-20260820-003', '2026-08-20', HJ, 'PRJ-2601', 'ZH-2601-A', '驾驶室围板箱整箱套件', '套', '30', '退租', 'TZRK-20260820-003', '客户在租', 'BOM 拆散退回'),
 ev('EV-20260824-004', '2026-08-24', HJ, 'PRJ-2604', 'ZH-2604-D', '混合组合套件', '套', '40', '出库', 'CK-20260824-009', '客户在租', None),
 ev('EV-20260825-005', '2026-08-25', DH, 'PRJ-2602', 'PLT-1210P', '塑料托盘', '块', '150', '退租', 'TZRK-20260825-004', '客户在租', None),
 ev('EV-20260826-006', '2026-08-26', HJ, 'PRJ-2601', 'BTC-6040', '料箱', '只', '200', '其他出入库', '期初结转', '客户在租', '期初在租结转'),
 ev('EV-20260828-007', '2026-08-28', HJ, 'PRJ-2601', 'BTC-6040', '料箱', '只', '200', '退租', 'TZRK-20260828-005', '客户在租', None),
 ev('EV-20260828-008', '2026-08-28', CF, 'PRJ-2604', 'ZH-2601-A', '驾驶室围板箱整箱套件', '套', '96', '出库', 'CK-20260828-011', '客户在租', None),
 ev('EV-20260828-009', '2026-08-28', DH, 'PRJ-2602', 'ZH-2602-B', '冲压件料箱组套', '套', '200', '出库', 'CK-20260828-010', '客户在租', None),
 ev('EV-20260829-010', '2026-08-29', HJ, 'PRJ-2601', 'ZH-2601-A', '驾驶室围板箱整箱套件', '套', '120', '出库', 'CK-20260829-012', '客户在租', None),
 ev('EV-20260829-011', '2026-08-29', XT, 'PRJ-2603', 'ZH-2603-C', '电池托盘护角套件', '套', '60', '出库', 'CK-20260829-013', '客户在租', '按次计费链（bomList.billing=按次）'),
 ev('EV-20260830-012', '2026-08-30', HJ, 'PRJ-2601', 'ZH-2601-A', '驾驶室围板箱整箱套件', '套', '180', '出库', 'CK-20260830-015', '客户在租', None),
 ev('EV-20260831-013', '2026-08-31', XT, 'PRJ-2603', 'ZH-2603-C', '电池托盘护角套件', '套', '20', '退租', 'TZRK-20260831-006', '客户在租', '部分退租'),
 ev('EV-20260901-014', '2026-09-01', DH, 'PRJ-2602', 'ZH-2602-B', '冲压件料箱组套', '套', '45', '退租', 'TZRK-20260901-007', '客户在租', '部分退租'),
 ev('EV-20260903-015', '2026-09-03', HJ, 'PRJ-2601', 'ZH-2601-A', '驾驶室围板箱整箱套件', '套', '60', '出库', 'CK-20260903-016', '客户在租', '退租回库件循环出库'),
 ev('EV-20260908-016', '2026-09-08', HJ, 'PRJ-2601', 'ZH-2601-A', '驾驶室围板箱整箱套件', '套', '120', '退租', 'TZRK-20260908-011', '客户在租', '部分退租（T6 演示·当日仍计租）'),
 ev('EV-20260731-017', '2026-07-31', HT, '—', 'BTC-6040', '金属料箱 800×600', '只', '20', '其他出入库', '期初结转', '租入持有', '期初租入持有结转'),
 ev('EV-20260816-018', '2026-08-16', HT, '—', 'WBX-1210L', '围板箱 1200×1000×970', '只', '30', '其他出入库', 'RZRK-20260816-021', '租入持有', '租入入库'),
 ev('EV-20260816-019', '2026-08-16', HT, '—', 'WBX-1210L', '围板箱 1200×1000×970', '只', '10', '其他出入库', 'RZRK-20260816-022', '租入持有', '租入入库'),
 ev('EV-20260831-020', '2026-08-31', HT, '—', 'BTC-6040', '金属料箱 800×600', '只', '20', '归还', 'GHCK-20260831-003', '租入持有', '整退归还'),
 ev('EV-20260903-021', '2026-09-03', HT, '—', 'WBX-1210L', '围板箱 1200×1000×970', '只', '30', '归还', 'GHCK-20260903-001', '租入持有', '整退归还'),
 ev('EV-20260903-022', '2026-09-03', HT, '—', 'WBX-1210L', '围板箱 1200×1000×970', '只', '4', '归还', 'GHCK-20260903-002', '租入持有', '分流归还'),
]
if '  stockEvents:' not in raw:
    tail_anchor = '\r\n  },\r\n};'
    idx = raw.rfind(tail_anchor)
    assert idx > 0, 'file tail anchor'
    block = '\r\n  /* G39 T2 · 在租量事件流水（D-148）：每条＝日期+客户+项目+物料+数量+方向；\r\n     每日在租量由事件派生——出库/入库当日计入，退租/归还当日仍计、次日起减（天数=max(2,止-起+1)） */\r\n  stockEvents: {\r\n' + '\r\n'.join(EVROWS) + '\r\n  },'
    raw = raw[:idx] + block + raw[idx + len('\r\n  },'):]
    print('[G] stockEvents 实体 +%d 行' % len(EVROWS))

# ============ 校验 ============
assert raw.count("'BF-06'") == 1
assert raw.count("'TZRK-20260908-011'") == 2  # 记录键 + info text
assert raw.count("'AR-2026-09-PRJ2601-D1'") >= 1 and raw.count("'AR-2026-09-PRJ2603-D1'") >= 1
assert raw.count("'AP-20260911-013'") >= 1
assert raw.count('  stockEvents:') == 1
assert raw != orig
io.open(P, 'wb').write(raw.encode('utf-8'))
print('[T2+T6] OK 写盘')
