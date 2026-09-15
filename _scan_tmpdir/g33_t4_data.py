# -*- coding: utf-8 -*-
"""G33 T4: demo-data.js 增量
- 三新实体 purchaseReturns/salesReturns/refunds（各 3 行·前缀 CGTH-/XSTH-/TKD-）
- dictItems +7 项（DJ-17~19 + THC-01~02 + TKL-01~02）119→126 项 24→26 组
- todoItems +3 行（采购退货单/销售退货单/退款登记·插「租赁出库」行之后）
销售退货关联原单键 = salesOutbounds 实读键（XSCK-*，按 fields.so 反查）
"""
import io, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DD = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型', '_data', 'demo-data.js')
src = io.open(DD, encoding='utf-8', newline='').read()

# ---- 反查 salesOutbounds 键（fields.so → 实体键）----
seg = src[src.index('salesOutbounds: {'):src.index('otherInbounds: {')]
xs_keys = re.findall(r"'(XSCK-[0-9-]+)':", seg)
so2key = {}
for idx, xk in enumerate(xs_keys):
    start = seg.index("'" + xk + "':")
    end = seg.index("'" + xs_keys[idx + 1] + "':", start) if idx + 1 < len(xs_keys) else len(seg)
    m = re.search(r'"so": "([^"]+)"', seg[start:end])
    if m:
        so2key[m.group(1)] = xk
for need in ('SO-20260830-0043', 'SO-20260828-0041', 'SO-20260822-0038'):
    assert need in so2key, 'salesOutbounds 未找到 ' + need
K1, K2, K3 = so2key['SO-20260830-0043'], so2key['SO-20260828-0041'], so2key['SO-20260822-0038']

# ================= 三新实体 =================
ENTITIES = r'''
  /* --------------------------------------------------------------------------
 * 采购退货单 purchaseReturns：键 = 退货单号（G33 · 退货退款闭环方案 B·道远 09-15 拍板）
 *   fields: type(退货类型 THC)/ref(关联采购入库单)/supplier/material/qty/amount/status/date 供筛选与 stab
 *   状态流 待审核→已审核→已退款；收货拒收=未入库直接退（不产生库存流水）/入库后退货=已入库再退（D-109 不改原入库单）
 * ------------------------------------------------------------------------ */
  purchaseReturns: {
    'CGTH-20260914-001': {
      'row': {"fields": {"type": "入库后退货", "ref": "CGRK-20260828-012", "supplier": "苏州联恒五金制品有限公司", "material": "围板箱 1200×1000×970", "qty": "10 只", "amount": "4,800.00", "status": "已退款", "date": "2026-09-14"}, "cells": ["入库后退货", "<span class=\"lk\">CGRK-20260828-012</span>", "苏州联恒五金制品有限公司", "围板箱 1200×1000×970", "<span class=\"td-num\">10 只</span>", "<span class=\"td-num\">4,800.00</span>", "<span class=\"tag tag-green\">已退款</span>", "2026-09-14"], "ops": [{"t": "详情", "detail": true}, {"t": "退款登记", "act": "go('../财务协同/退款登记.html')"}]},
      title: '采购退货单详情',
      info: [
        { label: '退货单号', text: 'CGTH-20260914-001', full: true },
        { label: '状态', tag: '已退款' },
        { label: '退货类型', text: '入库后退货（已入库再退）' },
        { label: '退货日期', text: '2026-09-14' },
        { label: '供应商', text: '苏州联恒五金制品有限公司', full: true },
        { label: '关联采购入库', text: 'CGRK-20260828-012', url: '采购管理/采购入库列表.html' },
        { label: '关联退款单', text: 'TKD-20260912-003', url: '财务协同/退款登记.html' },
        { label: '制单人', text: '李国栋' },
        { label: '退货原因', text: '规格不符（尺寸下差），供应商确认后退货' }
      ],
      feeCols: ['物料', '数量', '单价(元)', '金额(元)'],
      fees: [ { cells: ['围板箱 1200×1000×970', '10 只', '480.00', '4,800.00'] } ],
      chain: [
        { role: '采购入库单', name: 'CGRK-20260828-012', url: '采购管理/采购入库列表.html' },
        { role: '采购退货单（本单）', name: 'CGTH-20260914-001', self: true },
        { role: '退款登记', name: 'TKD-20260912-003', url: '财务协同/退款登记.html' }
      ],
      timeline: [
        { t: '09-14 09:30', text: '采购退货登记 · 提交审核', who: '李国栋' },
        { t: '09-14 14:20', text: '审核通过 · 冲减库存与应付', who: '徐蔚' },
        { t: '09-15 10:05', text: '退款到账确认 · 单据转已退款', who: '财务·周敏' }
      ]
    },
    'CGTH-20260912-002': {
      'row': {"fields": {"type": "收货拒收", "ref": "CGRK-20260828-011", "supplier": "宁波华塑包装制品有限公司", "material": "锁扣组件", "qty": "500 套", "amount": "2,000.00", "status": "已审核", "date": "2026-09-12"}, "cells": ["收货拒收", "<span class=\"lk\">CGRK-20260828-011</span>", "宁波华塑包装制品有限公司", "锁扣组件", "<span class=\"td-num\">500 套</span>", "<span class=\"td-num\">2,000.00</span>", "<span class=\"tag tag-blue\">已审核</span>", "2026-09-12"], "ops": [{"t": "详情", "detail": true}, {"t": "退款登记", "act": "go('../财务协同/退款登记.html')"}]},
      title: '采购退货单详情',
      info: [
        { label: '退货单号', text: 'CGTH-20260912-002', full: true },
        { label: '状态', tag: '已审核' },
        { label: '退货类型', text: '收货拒收（未入库直接退·不产生库存流水）' },
        { label: '退货日期', text: '2026-09-12' },
        { label: '供应商', text: '宁波华塑包装制品有限公司', full: true },
        { label: '关联采购入库', text: 'CGRK-20260828-011', url: '采购管理/采购入库列表.html' },
        { label: '制单人', text: '李国栋' },
        { label: '退货原因', text: '到货验收不合格（镀层脱落），整批拒收' }
      ],
      feeCols: ['物料', '数量', '单价(元)', '金额(元)'],
      fees: [ { cells: ['锁扣组件', '500 套', '4.00', '2,000.00'] } ],
      chain: [
        { role: '采购入库单', name: 'CGRK-20260828-011', url: '采购管理/采购入库列表.html' },
        { role: '采购退货单（本单）', name: 'CGTH-20260912-002', self: true },
        { role: '退款登记', name: '待退款（应付退款·对供应商）' }
      ],
      timeline: [
        { t: '09-12 08:40', text: '采购退货登记 · 收货拒收', who: '李国栋' },
        { t: '09-12 16:10', text: '审核通过 · 不动原入库单（未入库）', who: '徐蔚' },
        { t: '—', text: '待退款 · 供应商退款后转已退款', off: true }
      ]
    },
    'CGTH-20260910-003': {
      'row': {"fields": {"type": "入库后退货", "ref": "CGRK-20260827-010", "supplier": "常州正大塑料托盘厂", "material": "塑料托盘 1200×1000×150", "qty": "40 张", "amount": "2,400.00", "status": "待审核", "date": "2026-09-10"}, "cells": ["入库后退货", "<span class=\"lk\">CGRK-20260827-010</span>", "常州正大塑料托盘厂", "塑料托盘 1200×1000×150", "<span class=\"td-num\">40 张</span>", "<span class=\"td-num\">2,400.00</span>", "<span class=\"tag tag-orange\">待审核</span>", "2026-09-10"], "ops": [{"t": "审核", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}]},
      title: '采购退货单详情',
      info: [
        { label: '退货单号', text: 'CGTH-20260910-003', full: true },
        { label: '状态', tag: '待审核' },
        { label: '退货类型', text: '入库后退货（已入库再退）' },
        { label: '退货日期', text: '2026-09-10' },
        { label: '供应商', text: '常州正大塑料托盘厂', full: true },
        { label: '关联采购入库', text: 'CGRK-20260827-010', url: '采购管理/采购入库列表.html' },
        { label: '制单人', text: '李国栋' },
        { label: '退货原因', text: '项目减量，多余托盘退回供应商' }
      ],
      feeCols: ['物料', '数量', '单价(元)', '金额(元)'],
      fees: [ { cells: ['塑料托盘 1200×1000×150', '40 张', '60.00', '2,400.00'] } ],
      chain: [
        { role: '采购入库单', name: 'CGRK-20260827-010', url: '采购管理/采购入库列表.html' },
        { role: '采购退货单（本单）', name: 'CGTH-20260910-003', self: true },
        { role: '退款登记', name: '待审核通过后生成' }
      ],
      timeline: [
        { t: '09-10 11:05', text: '采购退货登记 · 提交审核', who: '李国栋' },
        { t: '—', text: '待审核 · 通过后冲减库存并登记应付退款', off: true }
      ]
    },
  },

  /* --------------------------------------------------------------------------
 * 销售退货单 salesReturns：键 = 退货单号（G33 · 退货退款闭环方案 B）
 *   fields: type/ref(关联销售出库单 XSCK-)/customer/material/qty/amount/status/date
 *   方向映射（道远 09-15 拍板·固定）：销售退货 → 应收退款（对客户）
 * ------------------------------------------------------------------------ */
  salesReturns: {
    'XSTH-20260913-001': {
      'row': {"fields": {"type": "收货拒收", "ref": "__K1__", "customer": "一汽解放汽车有限公司", "material": "箱盖 ABS 吸塑", "qty": "200 件", "amount": "3,600.00", "status": "已退款", "date": "2026-09-13"}, "cells": ["收货拒收", "<span class=\"lk\">__K1__</span>", "一汽解放汽车有限公司", "箱盖 ABS 吸塑", "<span class=\"td-num\">200 件</span>", "<span class=\"td-num\">3,600.00</span>", "<span class=\"tag tag-green\">已退款</span>", "2026-09-13"], "ops": [{"t": "详情", "detail": true}, {"t": "退款登记", "act": "go('../财务协同/退款登记.html')"}]},
      title: '销售退货单详情',
      info: [
        { label: '退货单号', text: 'XSTH-20260913-001', full: true },
        { label: '状态', tag: '已退款' },
        { label: '退货类型', text: '收货拒收（客户未收货直接退回）' },
        { label: '退货日期', text: '2026-09-13' },
        { label: '客户', text: '一汽解放汽车有限公司', full: true },
        { label: '关联销售出库', text: '__K1__', url: '销售管理/销售出库列表.html' },
        { label: '关联退款单', text: 'TKD-20260913-002', url: '财务协同/退款登记.html' },
        { label: '制单人', text: '王琳' },
        { label: '退货原因', text: '客户产线暂停，出库后整批拒收退回' }
      ],
      feeCols: ['物料', '数量', '单价(元)', '金额(元)'],
      fees: [ { cells: ['箱盖 ABS 吸塑', '200 件', '18.00', '3,600.00'] } ],
      chain: [
        { role: '销售出库单', name: '__K1__', url: '销售管理/销售出库列表.html' },
        { role: '销售退货单（本单）', name: 'XSTH-20260913-001', self: true },
        { role: '退款登记', name: 'TKD-20260913-002', url: '财务协同/退款登记.html' }
      ],
      timeline: [
        { t: '09-13 09:15', text: '销售退货登记 · 提交审核', who: '王琳' },
        { t: '09-13 15:40', text: '审核通过 · 货物回仓', who: '陈金' },
        { t: '09-14 09:50', text: '应收退款付讫 · 单据转已退款', who: '财务·周敏' }
      ]
    },
    'XSTH-20260912-002': {
      'row': {"fields": {"type": "入库后退货", "ref": "__K2__", "customer": "东风本田汽车有限公司", "material": "锁扣组件", "qty": "100 套", "amount": "800.00", "status": "已审核", "date": "2026-09-12"}, "cells": ["入库后退货", "<span class=\"lk\">__K2__</span>", "东风本田汽车有限公司", "锁扣组件", "<span class=\"td-num\">100 套</span>", "<span class=\"td-num\">800.00</span>", "<span class=\"tag tag-blue\">已审核</span>", "2026-09-12"], "ops": [{"t": "详情", "detail": true}, {"t": "退款登记", "act": "go('../财务协同/退款登记.html')"}]},
      title: '销售退货单详情',
      info: [
        { label: '退货单号', text: 'XSTH-20260912-002', full: true },
        { label: '状态', tag: '已审核' },
        { label: '退货类型', text: '入库后退货（客户收货使用后退货回仓）' },
        { label: '退货日期', text: '2026-09-12' },
        { label: '客户', text: '东风本田汽车有限公司', full: true },
        { label: '关联销售出库', text: '__K2__', url: '销售管理/销售出库列表.html' },
        { label: '制单人', text: '王琳' },
        { label: '退货原因', text: '多发数量退回（开票前冲减）' }
      ],
      feeCols: ['物料', '数量', '单价(元)', '金额(元)'],
      fees: [ { cells: ['锁扣组件', '100 套', '8.00', '800.00'] } ],
      chain: [
        { role: '销售出库单', name: '__K2__', url: '销售管理/销售出库列表.html' },
        { role: '销售退货单（本单）', name: 'XSTH-20260912-002', self: true },
        { role: '退款登记', name: '待退款（应收退款·对客户）' }
      ],
      timeline: [
        { t: '09-12 10:20', text: '销售退货登记 · 提交审核', who: '王琳' },
        { t: '09-12 17:35', text: '审核通过 · 验收回仓', who: '陈金' },
        { t: '—', text: '待退款 · 退款付讫后转已退款', off: true }
      ]
    },
    'XSTH-20260911-003': {
      'row': {"fields": {"type": "收货拒收", "ref": "__K3__", "customer": "上汽大众汽车有限公司宁波分公司", "material": "内衬", "qty": "300 件", "amount": "1,500.00", "status": "待审核", "date": "2026-09-11"}, "cells": ["收货拒收", "<span class=\"lk\">__K3__</span>", "上汽大众汽车有限公司宁波分公司", "内衬", "<span class=\"td-num\">300 件</span>", "<span class=\"td-num\">1,500.00</span>", "<span class=\"tag tag-orange\">待审核</span>", "2026-09-11"], "ops": [{"t": "审核", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}]},
      title: '销售退货单详情',
      info: [
        { label: '退货单号', text: 'XSTH-20260911-003', full: true },
        { label: '状态', tag: '待审核' },
        { label: '退货类型', text: '收货拒收（客户未收货直接退回）' },
        { label: '退货日期', text: '2026-09-11' },
        { label: '客户', text: '上汽大众汽车有限公司宁波分公司', full: true },
        { label: '关联销售出库', text: '__K3__', url: '销售管理/销售出库列表.html' },
        { label: '制单人', text: '王琳' },
        { label: '退货原因', text: '质量异议（划伤），产线拒收整批退回' }
      ],
      feeCols: ['物料', '数量', '单价(元)', '金额(元)'],
      fees: [ { cells: ['内衬', '300 件', '5.00', '1,500.00'] } ],
      chain: [
        { role: '销售出库单', name: '__K3__', url: '销售管理/销售出库列表.html' },
        { role: '销售退货单（本单）', name: 'XSTH-20260911-003', self: true },
        { role: '退款登记', name: '待审核通过后生成' }
      ],
      timeline: [
        { t: '09-11 14:30', text: '销售退货登记 · 提交审核', who: '王琳' },
        { t: '—', text: '待审核 · 通过后回仓并登记应收退款', off: true }
      ]
    },
  },

  /* --------------------------------------------------------------------------
 * 退款登记 refunds：键 = 退款单号 TKD-（G33 · 一页双向）
 *   fields: type(退款类型 TKL)/ref(关联退货单)/partner(往来单位)/amount/direction/status/date
 *   方向映射（固定）：采购退货→应付退款（对供应商·收款）；销售退货→应收退款（对客户·付款）
 *   「供应商应收」既有行 AR-20260904-015 不动（赔付用途·不承载退货退款）
 * ------------------------------------------------------------------------ */
  refunds: {
    'TKD-20260914-001': {
      'row': {"fields": {"type": "应付退款", "ref": "CGTH-20260912-002", "partner": "宁波华塑包装制品有限公司", "amount": "2,000.00", "direction": "收款（供应商退回）", "status": "待审核", "date": "2026-09-14"}, "cells": ["应付退款（对供应商）", "<span class=\"lk\">CGTH-20260912-002</span>", "宁波华塑包装制品有限公司", "<span class=\"td-num\">2,000.00</span>", "收款（供应商退回）", "<span class=\"tag tag-orange\">待审核</span>", "2026-09-14"], "ops": [{"t": "确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}]},
      title: '退款登记详情',
      info: [
        { label: '退款单号', text: 'TKD-20260914-001', full: true },
        { label: '状态', tag: '待审核' },
        { label: '退款类型', text: '应付退款（对供应商）' },
        { label: '资金方向', text: '收款 · 供应商退回我方' },
        { label: '登记日期', text: '2026-09-14' },
        { label: '往来单位', text: '宁波华塑包装制品有限公司', full: true },
        { label: '关联退货单', text: 'CGTH-20260912-002', url: '采购管理/采购退货单列表.html' },
        { label: '退款金额', text: '2,000.00 元' },
        { label: '收退款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务·周敏' }
      ],
      feeCols: ['关联退货单', '退货类型', '退款金额(元)'],
      fees: [ { cells: ['CGTH-20260912-002', '收货拒收', '2,000.00'], links: { 0: '采购管理/采购退货单列表.html' } } ],
      chain: [
        { role: '采购退货单', name: 'CGTH-20260912-002', url: '采购管理/采购退货单列表.html' },
        { role: '退款登记（本单）', name: 'TKD-20260914-001', self: true },
        { role: '退款确认', name: '待审核（到账后转已确认）' }
      ],
      timeline: [
        { t: '09-14 10:15', text: '退款登记 · 应付退款登记提交', who: '财务·周敏' },
        { t: '—', text: '待审核 · 到账确认后转已确认', off: true }
      ]
    },
    'TKD-20260913-002': {
      'row': {"fields": {"type": "应收退款", "ref": "XSTH-20260913-001", "partner": "一汽解放汽车有限公司", "amount": "3,600.00", "direction": "付款（退回客户）", "status": "已确认", "date": "2026-09-13"}, "cells": ["应收退款（对客户）", "<span class=\"lk\">XSTH-20260913-001</span>", "一汽解放汽车有限公司", "<span class=\"td-num\">3,600.00</span>", "付款（退回客户）", "<span class=\"tag tag-green\">已确认</span>", "2026-09-13"], "ops": [{"t": "详情", "detail": true}]},
      title: '退款登记详情',
      info: [
        { label: '退款单号', text: 'TKD-20260913-002', full: true },
        { label: '状态', tag: '已确认' },
        { label: '退款类型', text: '应收退款（对客户）' },
        { label: '资金方向', text: '付款 · 我方退回客户' },
        { label: '登记日期', text: '2026-09-13' },
        { label: '往来单位', text: '一汽解放汽车有限公司', full: true },
        { label: '关联退货单', text: 'XSTH-20260913-001', url: '销售管理/销售退货单列表.html' },
        { label: '退款金额', text: '3,600.00 元' },
        { label: '收退款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务·周敏' }
      ],
      feeCols: ['关联退货单', '退货类型', '退款金额(元)'],
      fees: [ { cells: ['XSTH-20260913-001', '收货拒收', '3,600.00'], links: { 0: '销售管理/销售退货单列表.html' } } ],
      chain: [
        { role: '销售退货单', name: 'XSTH-20260913-001', url: '销售管理/销售退货单列表.html' },
        { role: '退款登记（本单）', name: 'TKD-20260913-002', self: true },
        { role: '退款确认', name: '已确认 · 退款付讫' }
      ],
      timeline: [
        { t: '09-13 16:20', text: '退款登记 · 应收退款登记提交', who: '财务·周敏' },
        { t: '09-14 09:50', text: '退款确认通过 · 付款退回客户', who: '王芳' }
      ]
    },
    'TKD-20260912-003': {
      'row': {"fields": {"type": "应付退款", "ref": "CGTH-20260914-001", "partner": "苏州联恒五金制品有限公司", "amount": "4,800.00", "direction": "收款（供应商退回）", "status": "已确认", "date": "2026-09-12"}, "cells": ["应付退款（对供应商）", "<span class=\"lk\">CGTH-20260914-001</span>", "苏州联恒五金制品有限公司", "<span class=\"td-num\">4,800.00</span>", "收款（供应商退回）", "<span class=\"tag tag-green\">已确认</span>", "2026-09-12"], "ops": [{"t": "详情", "detail": true}]},
      title: '退款登记详情',
      info: [
        { label: '退款单号', text: 'TKD-20260912-003', full: true },
        { label: '状态', tag: '已确认' },
        { label: '退款类型', text: '应付退款（对供应商）' },
        { label: '资金方向', text: '收款 · 供应商退回我方' },
        { label: '登记日期', text: '2026-09-12' },
        { label: '往来单位', text: '苏州联恒五金制品有限公司', full: true },
        { label: '关联退货单', text: 'CGTH-20260914-001', url: '采购管理/采购退货单列表.html' },
        { label: '退款金额', text: '4,800.00 元' },
        { label: '收退款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务·周敏' }
      ],
      feeCols: ['关联退货单', '退货类型', '退款金额(元)'],
      fees: [ { cells: ['CGTH-20260914-001', '入库后退货', '4,800.00'], links: { 0: '采购管理/采购退货单列表.html' } } ],
      chain: [
        { role: '采购退货单', name: 'CGTH-20260914-001', url: '采购管理/采购退货单列表.html' },
        { role: '退款登记（本单）', name: 'TKD-20260912-003', self: true },
        { role: '退款确认', name: '已确认 · 退款到账' }
      ],
      timeline: [
        { t: '09-12 11:00', text: '退款登记 · 应付退款登记提交', who: '财务·周敏' },
        { t: '09-15 10:05', text: '退款确认通过 · 供应商退款到账', who: '王芳' }
      ]
    },
  },
'''
ENTITIES = ENTITIES.replace('__K1__', K1).replace('__K2__', K2).replace('__K3__', K3)

# ---- 插入点：productTaxes 结束（TAX-005 行后的 `  },\n};`）----
anchor = "'TAX-005': {'row': "
i = src.index(anchor)
EOL = '\r\n' if '\r\n' in src else '\n'
j = src.index(EOL + '  },' + EOL + '};', i)
assert j > i, 'T4 尾部锚点异常'
# src[:j] = 至 TAX-005 行尾；插入 productTaxes 收尾 "  }," + 三实体（统一 EOL）；再接原尾
ENT_CRLF = ENTITIES.rstrip().replace('\n', EOL)
out = src[:j] + EOL + '  },' + EOL + ENT_CRLF + src[j + len(EOL + '  },'):]

# ================= dictItems +7 =================
DICT_ADD = """    'DJ-17': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-17", "name": "采购退货单", "status": "启用"}, "cells": ["DJ-17", "采购退货单", "<span class=\\"td-num\\">17</span>", "采购退货单据（G33）", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-18': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-18", "name": "销售退货单", "status": "启用"}, "cells": ["DJ-18", "销售退货单", "<span class=\\"td-num\\">18</span>", "销售退货单据（G33）", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-19': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-19", "name": "退款登记", "status": "启用"}, "cells": ["DJ-19", "退款登记", "<span class=\\"td-num\\">19</span>", "退款单据（G33）", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'THC-01': { 'row': {"fields": {"category": "退货类型", "abbr": "收货拒收", "name": "收货拒收", "status": "启用"}, "cells": ["收货拒收", "收货拒收", "<span class=\\"td-num\\">1</span>", "未入库直接退·不产生库存流水（G33·方案 B）", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'THC-02': { 'row': {"fields": {"category": "退货类型", "abbr": "入库后退货", "name": "入库后退货", "status": "启用"}, "cells": ["入库后退货", "入库后退货", "<span class=\\"td-num\\">2</span>", "已入库再退·退货单自身为凭不改原单（D-109）", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'TKL-01': { 'row': {"fields": {"category": "退款类型", "abbr": "应付退款", "name": "应付退款", "status": "启用"}, "cells": ["应付退款", "应付退款", "<span class=\\"td-num\\">1</span>", "对供应商·源自采购退货·资金方向=收款", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'TKL-02': { 'row': {"fields": {"category": "退款类型", "abbr": "应收退款", "name": "应收退款", "status": "启用"}, "cells": ["应收退款", "应收退款", "<span class=\\"td-num\\">2</span>", "对客户·源自销售退货·资金方向=付款", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
"""
DJ16 = "'DJ-16': { 'row':"
assert out.count(DJ16) == 1, 'DJ-16 锚点异常'
k = out.index(DJ16)
k_end = out.index(EOL, k)
out = out[:k_end + len(EOL)] + DICT_ADD.replace('\n', EOL) + out[k_end + len(EOL):]

# ================= todoItems +3（插「租赁出库」行 CK-20260910-022 之后）=================
TODO_ADD = """    'CGTH-20260910-003': { 'row': {"fields": {"auditor": "徐蔚", "type": "采购退货单", "docNo": "CGTH-20260910-003", "summary": "常州正大 · 塑料托盘退货 40 张（入库后）", "project": "PRJ-2602", "submitter": "李国栋", "time": "09-10 11:05", "action": "待审核"}}, 'link': '采购管理/采购退货单列表.html?audit=1' },
    'XSTH-20260911-003': { 'row': {"fields": {"auditor": "王琳", "type": "销售退货单", "docNo": "XSTH-20260911-003", "summary": "上汽大众宁波 · 内衬退货 300 件（拒收）", "project": "PRJ-2602", "submitter": "王琳", "time": "09-11 14:30", "action": "待审核"}}, 'link': '销售管理/销售退货单列表.html?audit=1' },
    'TKD-20260914-001': { 'row': {"fields": {"auditor": "袁丽晶", "type": "退款登记", "docNo": "TKD-20260914-001", "summary": "宁波华塑 · 采购退货应付退款 2,000.00", "project": "PRJ-2601", "submitter": "李静", "time": "09-14 10:15", "action": "待审核"}}, 'link': '财务协同/退款登记.html?audit=1' },
"""
CK22 = "'CK-20260910-022': { 'row':"
assert out.count(CK22) == 1, 'todo 租赁出库行锚点异常'
t = out.index(CK22)
t_end = out.index(EOL, t)
out = out[:t_end + len(EOL)] + TODO_ADD.replace('\n', EOL) + out[t_end + len(EOL):]

io.open(DD, 'w', encoding='utf-8', newline='').write(out)
print('=== G33 T4 demo-data 写入完成 ===')
print('purchaseReturns 行数:', out.count("purchaseReturns: {") and len(re.findall(r"'CGTH-", out)))
print('salesReturns 行数:', len(re.findall(r"'XSTH-", out)))
print('refunds 行数:', len(re.findall(r"'TKD-", out)))
print('dictItems 新增: DJ-17/18/19 THC-01/02 TKL-01/02 =', len(re.findall(r"'(?:DJ-1[789]|THC-0[12]|TKL-0[12])': \{ 'row'", out)))
print('todoItems 新增 3 行:', len(re.findall(r"(?:CGTH-20260910-003|XSTH-20260911-003|TKD-20260914-001)': \{ 'row'", out)))
