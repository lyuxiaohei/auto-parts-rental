#!/usr/bin/env python3
# G42 T11: 退款类型 2→4（TKL 组改写+追加·勿动 THC）＋旧方向词迁移＋refunds +2 行＋AP-012 timeline＋两页 4 值＋数据字典 cnt
import io

ROOT = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型'
DD = ROOT + '/_data/demo-data.js'
s = io.open(DD, encoding='utf-8').read()

# ---------- 1) dictItems TKL 组 ----------
tkl01_old = """    'TKL-01': { 'row': {"fields": {"category": "退款类型", "abbr": "应付退款", "name": "应付退款", "status": "启用"}, "cells": ["应付退款", "应付退款", "<span class=\\"td-num\\">1</span>", "对供应商·源自采购退货·资金方向=收款", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },"""
tkl01_new = """    'TKL-01': { 'row': {"fields": {"category": "退款类型", "abbr": "采购退货退款", "name": "采购退货退款", "status": "启用"}, "cells": ["采购退货退款", "采购退货退款", "<span class=\\"td-num\\">1</span>", "供应商·我方收款（应付侧）·源自采购退货", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'TKL-02': { 'row': {"fields": {"category": "退款类型", "abbr": "销售退货退款", "name": "销售退货退款", "status": "启用"}, "cells": ["销售退货退款", "销售退货退款", "<span class=\\"td-num\\">2</span>", "客户·我方付款（应收侧）·源自销售退货", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'TKL-03': { 'row': {"fields": {"category": "退款类型", "abbr": "预收退回", "name": "预收退回", "status": "启用"}, "cells": ["预收退回", "预收退回", "<span class=\\"td-num\\">3</span>", "客户·我方付款（应收侧）·预收冲抵后余额退回", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'TKL-04': { 'row': {"fields": {"category": "退款类型", "abbr": "多付退回", "name": "多付退回", "status": "启用"}, "cells": ["多付退回", "多付退回", "<span class=\\"td-num\\">4</span>", "供应商·我方收款（应付侧）·多付款项退回", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },"""
tkl02_old = """    'TKL-02': { 'row': {"fields": {"category": "退款类型", "abbr": "应收退款", "name": "应收退款", "status": "启用"}, "cells": ["应收退款", "应收退款", "<span class=\\"td-num\\">2</span>", "对客户·源自销售退货·资金方向=付款", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },"""
assert s.count(tkl01_old) == 1 and s.count(tkl02_old) == 1
s = s.replace(tkl01_old, tkl01_new).replace(tkl02_old + '\n', '')
# THC 组不受扰断言（改写前后行数）
thc = s.count('"category": "退货类型"')
assert thc == 2, thc

# ---------- 2) refunds 旧方向词迁移（fields.type / cells / info / timeline） ----------
pairs = [
    ('应付退款（对供应商）', '采购退货退款（供应商·我方收款）'),
    ('应收退款（对客户）', '销售退货退款（客户·我方付款）'),
]
for old, new in pairs:
    c = s.count(old)
    assert c in (4, 3), (old, c)  # 实测：应付=4（cells2+info2）·应收=3
    s = s.replace(old, new)
# fields.type 与 timeline 措辞（裸词·仅 refunds 实体域内）
i0 = s.index('  refunds: {')
i1 = s.index('\n  },', i0)
blk = s[i0:i1]
blk = blk.replace('"type": "应付退款"', '"type": "采购退货退款"')
blk = blk.replace('"type": "应收退款"', '"type": "销售退货退款"')
blk = blk.replace('应付退款登记提交', '采购退货退款登记提交')
blk = blk.replace('应收退款登记提交', '销售退货退款登记提交')
s = s[:i0] + blk + s[i1:]

# ---------- 3) refunds +2 行（TKD-003 块尾后插） ----------
tkd3_tail = "{ t: '09-12 11:05', text: '退款确认通过 · 供应商原路退回', who: '王芳' }"
# 找 TKD-20260912-003 的 timeline 尾与其条目闭合
i3 = s.index("    'TKD-20260912-003': {")
ient = s.index('\n    },', i3)
new_rows = """
    'TKD-20260916-004': {
      'row': {"fields": {"type": "预收退回", "ref": "AR-2026-09-PRJ2601-YS", "partner": "华骏重卡汽车有限公司", "amount": "20,000.00", "direction": "付款（退回客户）", "status": "待审核", "date": "2026-09-16"}, "cells": ["预收退回（客户·我方付款）", "<span class=\\"lk\\" onclick=\\"go('../财务协同/应收账单.html')\\">AR-2026-09-PRJ2601-YS</span>", "华骏重卡汽车有限公司", "<span class=\\"td-num\\">20,000.00</span>", "付款（退回客户）", "<span class=\\"tag tag-orange\\">待审核</span>", "2026-09-16"], "ops": [{"t": "确认", "act": "openModal('auditModal')"}, {"t": "详情", "act": "go('../财务协同/退款详情.html?id=TKD-20260916-004')"}]},
      title: '退款登记详情',
      info: [
        { label: '退款单号', text: 'TKD-20260916-004', full: true },
        { label: '状态', tag: '待审核' },
        { label: '退款类型', text: '预收退回（客户·我方付款）' },
        { label: '资金方向', text: '付款 · 我方退回客户' },
        { label: '登记日期', text: '2026-09-16' },
        { label: '往来单位', text: '华骏重卡汽车有限公司', full: true },
        { label: '关联账单', text: 'AR-2026-09-PRJ2601-YS', url: '财务协同/应收账单.html' },
        { label: '退款金额', text: '20,000.00 元（预收 50,000 部分退回）', full: true },
        { label: '收退款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务·周敏' }
      ],
      feeCols: ['关联账单', '费用项', '退款金额(元)'],
      fees: [ { cells: ['AR-2026-09-PRJ2601-YS', '预收冲抵后余额退回', '20,000.00'], links: { 0: '财务协同/应收账单.html' } } ],
      chain: [
        { role: '应收账单（预收）', name: 'AR-2026-09-PRJ2601-YS', url: '财务协同/应收账单.html' },
        { role: '退款登记（本单）', name: 'TKD-20260916-004', self: true },
        { role: '退款确认', name: '待审核（到账后转已确认）' }
      ],
      timeline: [
        { t: '09-16 10:30', text: '退款登记 · 预收 50,000 中 20,000 申请退回', who: '财务·周敏' },
        { t: '—', text: '待审核 · 付款退回客户后转已确认', off: true }
      ]
    },
    'TKD-20260916-005': {
      'row': {"fields": {"type": "多付退回", "ref": "AP-20260905-012", "partner": "环通包装运营", "amount": "10,000.00", "direction": "收款（供应商退回）", "status": "已确认", "date": "2026-09-16"}, "cells": ["多付退回（供应商·我方收款）", "<span class=\\"lk\\" onclick=\\"go('../财务协同/应付账单.html')\\">AP-20260905-012</span>", "环通包装运营", "<span class=\\"td-num\\">10,000.00</span>", "收款（供应商退回）", "<span class=\\"tag tag-green\\">已确认</span>", "2026-09-16"], "ops": [{"t": "详情", "act": "go('../财务协同/退款详情.html?id=TKD-20260916-005')"}]},
      title: '退款登记详情',
      info: [
        { label: '退款单号', text: 'TKD-20260916-005', full: true },
        { label: '状态', tag: '已确认' },
        { label: '退款类型', text: '多付退回（供应商·我方收款）' },
        { label: '资金方向', text: '收款 · 供应商退回我方' },
        { label: '登记日期', text: '2026-09-16' },
        { label: '往来单位', text: '环通包装运营', full: true },
        { label: '关联账单', text: 'AP-20260905-012', url: '财务协同/应付账单.html' },
        { label: '退款金额', text: '10,000.00 元（预付多付款项退回）', full: true },
        { label: '收退款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务·周敏' }
      ],
      feeCols: ['关联账单', '费用项', '退款金额(元)'],
      fees: [ { cells: ['AP-20260905-012', '预付多付退回', '10,000.00'], links: { 0: '财务协同/应付账单.html' } } ],
      chain: [
        { role: '应付账单（预付）', name: 'AP-20260905-012', url: '财务协同/应付账单.html' },
        { role: '退款登记（本单）', name: 'TKD-20260916-005', self: true },
        { role: '退款确认', name: '已确认 · 款项收讫' }
      ],
      timeline: [
        { t: '09-16 10:00', text: '退款登记 · 多付 ¥10,000 退回申请（与 09-12 预付冲减呼应）', who: '财务·周敏' },
        { t: '09-16 15:00', text: '退款确认通过 · 供应商原路退回', who: '王芳' }
      ]
    },"""
s = s[:ient] + new_rows + s[ient:]

# ---------- 4) AP-20260905-012 timeline 增退款单引用 ----------
tl_old = "        { t: '09-12', text: '预付款部分退款 · 供应商退回 ¥10,000（啥都没买·原路退回，冲减预付）', who: '财务' },"
assert s.count(tl_old) == 1
tl_new = tl_old + "\n        { t: '09-16', text: '多付退回落单 · 退款登记 TKD-20260916-005（¥10,000 原路退回）', who: '财务' },"
s = s.replace(tl_old, tl_new)

io.open(DD, 'w', encoding='utf-8').write(s)
print('demo-data T11 done')

# ---------- 5) 退款新建.html：4 值 + form-tip ----------
P = ROOT + '/财务协同/退款新建.html'
t = io.open(P, encoding='utf-8').read()
o1 = '<option selected>应付退款（对供应商）</option><option>应收退款（对客户）</option>'
n1 = '<option selected>采购退货退款</option><option>销售退货退款</option><option>预收退回</option><option>多付退回</option>'
assert t.count(o1) == 1
t = t.replace(o1, n1)
o2 = '采购退货→应付退款；销售退货→应收退款（D-123）'
n2 = '采购退货→采购退货退款（应付·我方收款）；销售退货→销售退货退款（应收·我方付款）；预收退回（应收·我方付款）；多付退回（应付·我方收款）（D-123 扩展）'
assert t.count(o2) == 1
t = t.replace(o2, n2)
o3 = '应付退款=收款；应收退款=付款（随类型自动带出）'
n3 = '应付侧（采购退货退款/多付退回）=我方收款；应收侧（销售退货退款/预收退回）=我方付款（随类型自动带出）'
assert t.count(o3) == 1
t = t.replace(o3, n3)
io.open(P, 'w', encoding='utf-8').write(t)
print('退款新建 done')

# ---------- 6) 退款登记.html：筛选 4 值 + 静态行迁移 ----------
P = ROOT + '/财务协同/退款登记.html'
t = io.open(P, encoding='utf-8').read()
o4 = '<select><option value="">全部</option><option>应付退款</option><option>应收退款</option></select>'
n4 = '<select><option value="">全部</option><option>采购退货退款</option><option>销售退货退款</option><option>预收退回</option><option>多付退回</option></select>'
assert t.count(o4) == 1
t = t.replace(o4, n4)
for old, new in pairs:
    c = t.count(old)
    assert c in (1, 2), (old, c)  # 实测：应付静态行 2·应收 1
    t = t.replace(old, new)
o5 = '2,000.00 元（应付退款 · 收款）'
n5 = '2,000.00 元（采购退货退款 · 收款）'
assert t.count(o5) == 1
t = t.replace(o5, n5)
io.open(P, 'w', encoding='utf-8').write(t)
print('退款登记 done')

# ---------- 7) 数据字典 cnt 2→4 ----------
P = ROOT + '/系统管理/数据字典.html'
t = io.open(P, encoding='utf-8').read()
o6 = '<div class="dic-item"><span>退款类型</span><span class="cnt">2</span></div>'
n6 = '<div class="dic-item"><span>退款类型</span><span class="cnt">4</span></div>'
assert t.count(o6) == 1
t = t.replace(o6, n6)
io.open(P, 'w', encoding='utf-8').write(t)
print('数据字典 done')
