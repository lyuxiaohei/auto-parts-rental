/* ============================================================================
 * 演示数据集（金种子数据）· 包装租赁管理后台原型
 * ----------------------------------------------------------------------------
 * 用途：不起后端、双击 HTML 即可演示。file:// 协议下 fetch(json) 会被浏览器
 *       拦截，所以数据一律写成 JS（window.DEMO_DATA），用 <script src> 引入。
 *
 * 建模约定：
 *   1. 单号即外键：实体间用单号互相引用（如应付账单 refs → 采购订单/租入单），
 *      不复制对方数据。跨页面"互溯链"因此永远一致——详情弹窗里的 PO-xxx 和
 *      采购订单列表页里那一条是同一个号。
 *   2. url 一律相对原型根目录（不含前导 ./），页面渲染时加各自的前缀：
 *      模块列表页（模块/x.html）前缀 '../'，弹窗模板预览（模块/弹窗/x.html）
 *      前缀 '../../'。
 *   3. 金额存数字，展示时格式化为千分位两位小数；口径要求：账单金额 =
 *      费用明细合计，已付 + 未付 = 账单金额，演示不露馅。
 *   4. scenario 标注该条数据支撑的演示故事线（对应 P3-R01-A04 流程链标注）。
 *
 * 扩展方式：新增实体（如 purchaseOrders / rentInOrders / receivableBills）时
 *   在 DEMO_DATA 下加同级 keyed-map，键=单号。
 * ========================================================================== */
window.DEMO_DATA = {
  _meta: {
    version: '2026-09-08',
    desc: '全局演示数据集 · 详情弹窗全站数据驱动（财务协同 6 + 租赁主线 8 + 买卖仓储 8 + 库存档案 10 页）'
  },

  /* --------------------------------------------------------------------------
   * 应付账单 payableBills：键 = 账单号
   *   billType: 采购应付 / 租金应付 / 赔付应付
   *   status:   未付款 / 部分付款 / 已付款
   *   refs[]:   关联来源单据（类型不同则单据不同：采购订单 vs 租入单 vs 赔偿单）
   *   fees[]:   费用明细行（src=来源单据号，无来源用 '—' 且不给 url）
   *   chain[]:  关联单据互溯链节点（self:true 表示本单高亮）
   *   timeline[]: 流转时间线（off:true 表示尚未发生的后续节点）
   * ------------------------------------------------------------------------ */
  payableBills: {

    /* ===== 预付（路凯 · 预付供应商大箱租金 9 月度 · 已付款） ===== */
     'AP-20260905-013': {
      'row': {"fields": {"supplier": "一汽解放汽车有限公司", "btype": "对客户应付", "project": "PRJ-2601", "period": "2026-09", "ref": "—", "inbound": "—", "date": "2026-09-05", "status": "未付款"}, "cells": ["一汽解放汽车有限公司", "<span class=\"tag tag-purple\" style=\"background:#f9f0ff;border-color:#d3adf7;color:#722ed1\">对客户应付</span><div style=\"color:#8c8c8c;font-size:11px;\">交付延误 · 断产赔偿（赔付客户）</div>", "PRJ-2601", "2026-09", "—", "—", "<span class=\"td-num\">68,400.00</span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\" style=\"color:var(--danger)\">68,400.00</span>", "2026-09-05", "2026-09-20", "<span class=\"tag tag-red\">未付款</span>"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "分期付款", "act": "go('../财务协同/付款登记.html')"}, {"t": "详情", "detail": true}]},
      'title': '应付账单详情',
      'billNo': 'AP-20260905-013',
      'billType': '对客户应付',
      'status': '未付款',
      'supplier': '一汽解放汽车有限公司（客户）',
      'project': 'PRJ-2601',
      'period': '2026-09',
      'amount': 68400,
      'paid': 0,
      'genMode': '直接生成（我方赔付客户 · 交付延误/断产/回款违约金，无赔偿单，2026-09-08 会议 4v4）',
      'scenario': 'F2 · 对客户应付（4 来源）',
      'refs': [],
      'fees': [
        { src: '—', desc: '断产赔偿 · 交付延误 12 天（合同条款）', amount: 68400 }
      ],
      'chain': [
        { role: '对客户应付（本单）', name: 'AP-20260905-013 · 赔付客户', self: true },
        { role: '付款登记', name: '分期计划 · 3 期', url: '财务协同/付款登记.html' }
      ],
      'timeline': [
        { t: '09-05', text: '断产赔偿认定 · 直接生成对客户应付（费用分类=违约金/断产赔偿）', who: '商务-王强' },
        { t: '—', text: '分期付款 3 期（40%/30%/30%）· 付款登记执行', who: '系统', off: true }
      ]
    },

   'AP-20260905-012': {
      'row': {"fields": {"supplier": "路凯包装运营", "btype": "预付预付供应商大箱租金（9 月度）", "project": "PRJ-2604", "period": "2026-09", "ref": "RZD-20260815-005", "inbound": "—", "date": "2026-09-05", "status": "已付款"}, "cells": ["路凯包装运营", "<span class=\"tag tag-blue\">预付</span><div style=\"color:#8c8c8c;font-size:11px;\">预付供应商大箱租金（9 月度）</div>", "PRJ-2604", "2026-09", "<span class=\"lk\">RZD-20260815-005</span>", "—", "<span class=\"td-num\">30,000.00</span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\">30,000.00</span>", "2026-09-05", "2026-09-30", "<span class=\"tag tag-green\">已付款</span>"], "ops": [{"t": "详情", "detail": true}]},
      billNo: 'AP-20260905-012',
      billType: '预付',
      status: '已付款',
      supplier: '路凯包装运营（上海）有限公司',
      project: 'PRJ-2604',
      period: '2026-09',
      amount: 30000,
      paid: 30000,
      genMode: '手动创建（预付）',
      scenario: '预付冲抵 · 供应商租金',
      refs: [
        { label: '关联租入单', no: 'RZD-20260815-005', url: '租赁管理/租入单列表.html' }
      ],
      fees: [
        { src: 'RZD-20260815-005', desc: '预付供应商大箱租金 · 2026-09 月度', amount: 30000, url: '租赁管理/租入单列表.html' }
      ],
      chain: [
        { role: '租入单', name: 'RZD-20260815-005', url: '租赁管理/租入单列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260905-012 · 预付', self: true },
        { role: '付款登记', name: '已付清', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '09-05', text: '预付款支付 · 记预付（路凯 ¥30,000）', who: '财务' },
        { t: '—', text: '每月 预付冲抵 · 租金应付生成后自预付冲抵', who: '系统', off: true }
      ]
    },

    /* ===== 采购应付（宁波华塑 · 未付款 · 财务通道主场景） ===== */
    'AP-20260901-008': {
      'row': {"fields": {"supplier": "宁波华塑包装制品有限公司", "btype": "采购应付", "project": "PRJ-2601", "period": "2026-09", "ref": "PO-20260825-014", "inbound": "CGRK-20260828-012", "date": "2026-09-01", "status": "未付款"}, "note": "3", "cells": ["宁波华塑包装制品有限公司", "<span class=\"tag tag-blue\">采购应付</span>", "PRJ-2601", "2026-09", "<span class=\"lk\">PO-20260825-014</span>", "<span class=\"lk\">CGRK-20260828-012</span>", "<span class=\"td-num\">84,000.00</span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\" style=\"color:var(--danger)\">84,000.00</span>", "2026-09-01", "2026-09-30", "<span class=\"tag tag-red\">未付款</span>"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}, {"t": "详情", "detail": true}]},
      billNo: 'AP-20260901-008',
      billType: '采购应付',
      status: '未付款',
      supplier: '宁波华塑包装制品有限公司',
      project: 'PRJ-2601',
      period: '2026-09',
      amount: 84000,
      paid: 0,
      genMode: '验收通过自动生成',
      scenario: '财务通道 · 采购应付',
      refs: [
        { label: '关联采购订单', no: 'PO-20260825-014', url: '采购管理/采购订单列表.html' },
        { label: '关联采购入库', no: 'CGRK-20260828-012', url: '采购管理/采购入库列表.html' }
      ],
      fees: [
        { src: 'CGRK-20260828-012', desc: '采购入库验收 · 采购应付', amount: 84000, url: '采购管理/采购入库列表.html' }
      ],
      chain: [
        { role: '采购订单', name: 'PO-20260825-014', url: '采购管理/采购订单列表.html' },
        { role: '采购入库', name: 'CGRK-20260828-012', url: '采购管理/采购入库列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260901-008 · 采购应付', self: true },
        { role: '付款登记', name: '待付款', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '08-28', text: '采购入库验收通过 · CGRK-20260828-012', who: '张伟' },
        { t: '09-01', text: '应付账单自动生成', who: '系统' },
        { t: '—', text: '待付款 → 付款登记确认', off: true }
      ]
    },

    /* ===== 采购应付（苏州联恒 · 部分付款） ===== */
    'AP-20260830-007': {
      'row': {"fields": {"supplier": "苏州联恒五金制品有限公司", "btype": "采购应付", "project": "PRJ-2602", "period": "2026-08", "ref": "PO-20260820-013", "inbound": "CGRK-20260825-011", "date": "2026-08-30", "status": "部分付款"}, "cells": ["苏州联恒五金制品有限公司", "<span class=\"tag tag-blue\">采购应付</span>", "PRJ-2602", "2026-08", "<span class=\"lk\">PO-20260820-013</span>", "<span class=\"lk\">CGRK-20260825-011</span>", "<span class=\"td-num\">12,700.00</span>", "<span class=\"td-num\">6,000.00</span>", "<span class=\"td-num\">6,700.00</span>", "2026-08-30", "2026-09-29", "<span class=\"tag tag-orange\">部分付款</span>"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}, {"t": "详情", "detail": true}]},
      billNo: 'AP-20260830-007',
      billType: '采购应付',
      status: '部分付款',
      supplier: '苏州联恒五金制品有限公司',
      project: 'PRJ-2602',
      period: '2026-08',
      amount: 12700,
      paid: 6000,
      genMode: '验收通过自动生成',
      refs: [
        { label: '关联采购订单', no: 'PO-20260820-013', url: '采购管理/采购订单列表.html' },
        { label: '关联采购入库', no: 'CGRK-20260825-011', url: '采购管理/采购入库列表.html' }
      ],
      fees: [
        { src: 'CGRK-20260825-011', desc: '采购入库验收 · 采购应付', amount: 12700, url: '采购管理/采购入库列表.html' }
      ],
      chain: [
        { role: '采购订单', name: 'PO-20260820-013', url: '采购管理/采购订单列表.html' },
        { role: '采购入库', name: 'CGRK-20260825-011', url: '采购管理/采购入库列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260830-007 · 采购应付', self: true },
        { role: '付款登记', name: '已付 6,000.00', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '08-25', text: '采购入库验收通过 · CGRK-20260825-011', who: '张伟' },
        { t: '08-30', text: '应付账单自动生成', who: '系统' },
        { t: '09-05', text: '付款登记 6,000.00 元', who: '王芳' },
        { t: '—', text: '待付尾款 6,700.00 元', off: true }
      ]
    },

    /* ===== 采购应付（常州正大 · 已付款） ===== */
    'AP-20260828-006': {
      'row': {"fields": {"supplier": "常州正大塑料托盘厂", "btype": "采购应付", "project": "PRJ-2603", "period": "2026-08", "ref": "PO-20260815-011", "inbound": "CGRK-20260820-009", "date": "2026-08-28", "status": "已付款"}, "cells": ["常州正大塑料托盘厂", "<span class=\"tag tag-blue\">采购应付</span>", "PRJ-2603", "2026-08", "<span class=\"lk\">PO-20260815-011</span>", "<span class=\"lk\">CGRK-20260820-009</span>", "<span class=\"td-num\">42,500.00</span>", "<span class=\"td-num\">42,500.00</span>", "<span class=\"td-num\">0.00</span>", "2026-08-28", "2026-09-27", "<span class=\"tag tag-green\">已付款</span>"], "ops": [{"t": "详情", "detail": true}]},
      billNo: 'AP-20260828-006',
      billType: '采购应付',
      status: '已付款',
      supplier: '常州正大塑料托盘厂',
      project: 'PRJ-2603',
      period: '2026-08',
      amount: 42500,
      paid: 42500,
      genMode: '验收通过自动生成',
      refs: [
        { label: '关联采购订单', no: 'PO-20260815-011', url: '采购管理/采购订单列表.html' },
        { label: '关联采购入库', no: 'CGRK-20260820-009', url: '采购管理/采购入库列表.html' }
      ],
      fees: [
        { src: 'CGRK-20260820-009', desc: '采购入库验收 · 采购应付', amount: 42500, url: '采购管理/采购入库列表.html' }
      ],
      chain: [
        { role: '采购订单', name: 'PO-20260815-011', url: '采购管理/采购订单列表.html' },
        { role: '采购入库', name: 'CGRK-20260820-009', url: '采购管理/采购入库列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260828-006 · 采购应付', self: true },
        { role: '付款登记', name: '已付清', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '08-20', text: '采购入库验收通过 · CGRK-20260820-009', who: '张伟' },
        { t: '08-28', text: '应付账单自动生成', who: '系统' },
        { t: '09-05', text: '付款登记确认 42,500.00 元', who: '王芳' }
      ]
    },

    /* ===== 采购应付（路凯 · 租入运营费 · 手动创建，无来源单据） ===== */
    'AP-20260825-005': {
      'row': {"fields": {"supplier": "路凯包装运营（上海）有限公司", "btype": "采购应付", "project": "—", "period": "2026-08", "ref": "—（租入运营费）", "inbound": "—", "date": "2026-08-25", "status": "未付款"}, "cells": ["路凯包装运营（上海）有限公司", "<span class=\"tag tag-blue\">采购应付</span>", "—", "2026-08", "—（租入运营费）", "—", "<span class=\"td-num\">126,000.00</span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\" style=\"color:var(--danger)\">126,000.00</span>", "2026-08-25", "2026-09-24", "<span class=\"tag tag-red\">未付款</span>"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}, {"t": "详情", "detail": true}]},
      billNo: 'AP-20260825-005',
      billType: '采购应付',
      status: '未付款',
      supplier: '路凯包装运营（上海）有限公司',
      project: '—',
      period: '2026-08',
      amount: 126000,
      paid: 0,
      genMode: '手动创建',
      refs: [],
      fees: [
        { src: '—', desc: '租入运营费 · 2026-08 账期', amount: 126000 }
      ],
      chain: [
        { role: '应付账单（本单）', name: 'AP-20260825-005 · 采购应付（手动创建）', self: true },
        { role: '付款登记', name: '待付款', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '08-25', text: '手动创建应付账单（租入运营费）', who: '王芳' },
        { t: '—', text: '待付款 → 付款登记确认', off: true }
      ]
    },

    /* ===== 采购应付（苏州联恒 · 已付款） ===== */
    'AP-20260820-004': {
      'row': {"fields": {"supplier": "苏州联恒五金制品有限公司", "btype": "采购应付", "project": "PRJ-2601", "period": "2026-08", "ref": "PO-20260810-009", "inbound": "CGRK-20260815-007", "date": "2026-08-20", "status": "已付款"}, "cells": ["苏州联恒五金制品有限公司", "<span class=\"tag tag-blue\">采购应付</span>", "PRJ-2601", "2026-08", "<span class=\"lk\">PO-20260810-009</span>", "<span class=\"lk\">CGRK-20260815-007</span>", "<span class=\"td-num\">6,300.00</span>", "<span class=\"td-num\">6,300.00</span>", "<span class=\"td-num\">0.00</span>", "2026-08-20", "2026-09-19", "<span class=\"tag tag-green\">已付款</span>"], "ops": [{"t": "详情", "detail": true}]},
      billNo: 'AP-20260820-004',
      billType: '采购应付',
      status: '已付款',
      supplier: '苏州联恒五金制品有限公司',
      project: 'PRJ-2601',
      period: '2026-08',
      amount: 6300,
      paid: 6300,
      genMode: '验收通过自动生成',
      refs: [
        { label: '关联采购订单', no: 'PO-20260810-009', url: '采购管理/采购订单列表.html' },
        { label: '关联采购入库', no: 'CGRK-20260815-007', url: '采购管理/采购入库列表.html' }
      ],
      fees: [
        { src: 'CGRK-20260815-007', desc: '采购入库验收 · 采购应付', amount: 6300, url: '采购管理/采购入库列表.html' }
      ],
      chain: [
        { role: '采购订单', name: 'PO-20260810-009', url: '采购管理/采购订单列表.html' },
        { role: '采购入库', name: 'CGRK-20260815-007', url: '采购管理/采购入库列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260820-004 · 采购应付', self: true },
        { role: '付款登记', name: '已付清', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '08-15', text: '采购入库验收通过 · CGRK-20260815-007', who: '张伟' },
        { t: '08-20', text: '应付账单自动生成', who: '系统' },
        { t: '09-02', text: '付款登记确认 6,300.00 元', who: '王芳' }
      ]
    },

    /* ===== 采购应付（宁波华塑 · 已付款） ===== */
    'AP-20260815-003': {
      'row': {"fields": {"supplier": "宁波华塑包装制品有限公司", "btype": "采购应付", "project": "PRJ-2602", "period": "2026-08", "ref": "PO-20260808-008", "inbound": "CGRK-20260812-006", "date": "2026-08-15", "status": "已付款"}, "cells": ["宁波华塑包装制品有限公司", "<span class=\"tag tag-blue\">采购应付</span>", "PRJ-2602", "2026-08", "<span class=\"lk\">PO-20260808-008</span>", "<span class=\"lk\">CGRK-20260812-006</span>", "<span class=\"td-num\">35,200.00</span>", "<span class=\"td-num\">35,200.00</span>", "<span class=\"td-num\">0.00</span>", "2026-08-15", "2026-09-14", "<span class=\"tag tag-green\">已付款</span>"], "ops": [{"t": "详情", "detail": true}]},
      billNo: 'AP-20260815-003',
      billType: '采购应付',
      status: '已付款',
      supplier: '宁波华塑包装制品有限公司',
      project: 'PRJ-2602',
      period: '2026-08',
      amount: 35200,
      paid: 35200,
      genMode: '验收通过自动生成',
      refs: [
        { label: '关联采购订单', no: 'PO-20260808-008', url: '采购管理/采购订单列表.html' },
        { label: '关联采购入库', no: 'CGRK-20260812-006', url: '采购管理/采购入库列表.html' }
      ],
      fees: [
        { src: 'CGRK-20260812-006', desc: '采购入库验收 · 采购应付', amount: 35200, url: '采购管理/采购入库列表.html' }
      ],
      chain: [
        { role: '采购订单', name: 'PO-20260808-008', url: '采购管理/采购订单列表.html' },
        { role: '采购入库', name: 'CGRK-20260812-006', url: '采购管理/采购入库列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260815-003 · 采购应付', self: true },
        { role: '付款登记', name: '已付清', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '08-12', text: '采购入库验收通过 · CGRK-20260812-006', who: '张伟' },
        { t: '08-15', text: '应付账单自动生成', who: '系统' },
        { t: '08-30', text: '付款登记确认 35,200.00 元', who: '王芳' }
      ]
    },

    /* ===== 租金应付（路凯 · 未付款 · L4 多线应付场景） ===== */
    'AP-20260903-010': {
      'row': {"fields": {"supplier": "路凯包装运营（上海）有限公司", "btype": "租金应付", "project": "PRJ-2604", "period": "2026-09", "ref": "RZD-20260815-005（租入单）", "inbound": "RZRK-20260816-022", "date": "2026-09-03", "status": "未付款"}, "note": "2", "cells": ["路凯包装运营（上海）有限公司", "<span class=\"tag tag-orange\">租金应付</span>", "PRJ-2604", "2026-09", "<span class=\"lk\" onclick=\"go('../租赁管理/租入单列表.html')\">RZD-20260815-005（租入单）</span>", "RZRK-20260816-022", "12,000.00", "0.00", "12,000.00", "2026-09-03", "2026-10-02", "<span class=\"tag tag-orange\">未付款</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}]},
      billNo: 'AP-20260903-010',
      billType: '租金应付',
      status: '未付款',
      supplier: '路凯包装运营（上海）有限公司',
      project: 'PRJ-2604',
      period: '2026-09',
      amount: 12000,
      paid: 0,
      genMode: '按周期自动生成（月结）',
      scenario: 'L4 · 多线应付（租金线）',
      refs: [
        { label: '关联租入单', no: 'RZD-20260815-005', url: '租赁管理/租入单列表.html' },
        { label: '关联租入入库', no: 'RZRK-20260816-022', url: '租赁管理/租入入库列表.html' }
      ],
      fees: [
        { src: 'RZD-20260815-005', desc: '租入租金 · 2026-09 账期', amount: 12000, url: '租赁管理/租入单列表.html' }
      ],
      chain: [
        { role: '租入单', name: 'RZD-20260815-005', url: '租赁管理/租入单列表.html' },
        { role: '租入入库', name: 'RZRK-20260816-022', url: '租赁管理/租入入库列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260903-010 · 租金应付', self: true },
        { role: '付款登记', name: '待付款', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '08-16', text: '租入入库确认 · RZRK-20260816-022', who: '张伟' },
        { t: '09-03', text: '按周期生成租金应付（月结）', who: '系统' },
        { t: '—', text: '待付款 → 付款登记确认', off: true }
      ]
    },

    /* ===== 租金应付（路凯 · 未付款 · L3 租金应付场景，36,000） ===== */
    'AP-20260903-009': {
      'row': {"fields": {"supplier": "路凯包装运营（上海）有限公司", "btype": "租金应付", "project": "PRJ-2603", "period": "2026-09", "ref": "RZD-20260815-003（租入单）", "inbound": "RZRK-20260816-021", "date": "2026-09-03", "status": "未付款"}, "note": "1", "cells": ["路凯包装运营（上海）有限公司", "<span class=\"tag tag-orange\">租金应付</span>", "PRJ-2603", "2026-09", "<span class=\"lk\" onclick=\"go('../租赁管理/租入单列表.html')\">RZD-20260815-003（租入单）</span>", "RZRK-20260816-021", "36,000.00", "0.00", "36,000.00", "2026-09-03", "2026-10-02", "<span class=\"tag tag-orange\">未付款</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}]},
      billNo: 'AP-20260903-009',
      billType: '租金应付',
      status: '未付款',
      supplier: '路凯包装运营（上海）有限公司',
      project: 'PRJ-2603',
      period: '2026-09',
      amount: 36000,
      paid: 0,
      genMode: '按周期自动生成（月结）',
      scenario: 'L3 · 步骤 8/8 租金应付',
      refs: [
        { label: '关联租入单', no: 'RZD-20260815-003', url: '租赁管理/租入单列表.html' },
        { label: '关联租入入库', no: 'RZRK-20260816-021', url: '租赁管理/租入入库列表.html' }
      ],
      fees: [
        { src: 'RZD-20260815-003', desc: '租入租金 · 2026-09 账期', amount: 36000, url: '租赁管理/租入单列表.html' }
      ],
      chain: [
        { role: '租入单', name: 'RZD-20260815-003', url: '租赁管理/租入单列表.html' },
        { role: '租入入库', name: 'RZRK-20260816-021', url: '租赁管理/租入入库列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260903-009 · 租金应付', self: true },
        { role: '付款登记', name: '待付款', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '08-16', text: '租入入库确认 · RZRK-20260816-021', who: '张伟' },
        { t: '09-03', text: '按周期生成租金应付（月结）', who: '系统' },
        { t: '—', text: '待付款 → 付款登记确认', off: true }
      ]
    },

    /* ===== 赔付应付（路凯 · 未付款 · 丢损赔偿场景） ===== */
    'AP-20260903-011': {
      'row': {"fields": {"supplier": "路凯包装运营（上海）有限公司", "btype": "赔付应付", "project": "PRJ-2603", "period": "2026-09", "ref": "BS-20260902-010（丢损赔偿单）", "inbound": "—", "date": "2026-09-03", "status": "未付款"}, "cells": ["路凯包装运营（上海）有限公司", "<span class=\"tag tag-orange\">赔付应付</span>", "PRJ-2603", "2026-09", "BS-20260902-010（丢损赔偿单）", "—", "930.00", "0.00", "930.00", "2026-09-03", "2026-09-18", "<span class=\"tag tag-orange\">未付款</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}]},
      billNo: 'AP-20260903-011',
      billType: '赔付应付',
      status: '未付款',
      supplier: '路凯包装运营（上海）有限公司',
      project: 'PRJ-2603',
      period: '2026-09',
      amount: 930,
      paid: 0,
      genMode: '直接生成（丢损赔付 · 无赔偿单，2026-09-08 会议）',
      scenario: 'L4 · 多线应付（赔付线）',
      refs: [
        { label: '关联丢损赔偿单', no: 'BS-20260902-010' }
      ],
      fees: [
        { src: 'BS-20260902-010', desc: '退租丢损赔偿 · 赔付应付', amount: 930 }
      ],
      chain: [
        { role: '丢损赔偿单', name: 'BS-20260902-010' },
        { role: '应付账单（本单）', name: 'AP-20260903-011 · 赔付应付', self: true },
        { role: '付款登记', name: '待付款', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '09-02', text: '丢损赔偿审核通过 · BS-20260902-010', who: '王芳' },
        { t: '09-03', text: '赔付应付自动生成', who: '系统' },
        { t: '—', text: '待付款 → 付款登记确认', off: true }
      ]
    }
  },

  /* --------------------------------------------------------------------------
   * 应收账单 receivableBills：键 = 账单号（赔偿联动行键 = 赔偿单号）
   *   billType: 销售费 / 租赁费 / 预收 / 丢损赔偿
   *   status:   未开票 / 部分收款 / 已结清 / 已收（预收）
   *   fees[]:   qty/price 为展示字符串（汇总行用 '—'），amount 为数字
   *   下游链统一为：本单 → 开票登记 → 回款/水单核销
   * ------------------------------------------------------------------------ */
  receivableBills: {

    /* ===== 预收（安吉智行 · 预付 9-10 月租金 · 已收） ===== */
     'AR-20260904-015': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2603", "customer": "路凯包装运营（上海）有限公司", "btype": "供应商应收", "docs": "租入单 RZD-20260815-005 · 赔付我方", "gen": "直接生成", "date": "2026-09-04", "status": "未开票"}, "cells": ["2026-09", "PRJ-2603", "路凯包装运营（上海）有限公司", "<span class=\"tag tag-blue\">供应商应收</span><div style=\"color:#8c8c8c;font-size:11px;\">供应商赔付我方 · 租入围板箱缺损 6 只</div>", "租入单 RZD-20260815-005 · 赔付我方", "<span class=\"td-num\"><b>2,850.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-red\">未开票</span>", "<span class=\"tag tag-orange\">直接生成</span>", "2026-09-04 10:12"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}]},
      'title': '应收账单详情',
      'billNo': 'AR-20260904-015',
      'billType': '供应商应收',
      'status': '未开票',
      'customer': '路凯包装运营（上海）有限公司',
      'project': 'PRJ-2603',
      'period': '2026-09',
      'amount': 2850,
      'paid': 0,
      'genMode': '直接生成（供应商赔付我方 · 无赔偿单，2026-09-08 会议 4v4）',
      'scenario': 'F1 · 供应商应收（4 来源）',
      'refs': [
        { label: '关联租入单', no: 'RZD-20260815-005', url: '租赁管理/租入单列表.html' }
      ],
      'fees': [
        { src: 'RZD-20260815-005', desc: '租入围板箱缺损赔付 · 供应商赔付我方', qty: '6 只', price: '475.00', amount: 2850, url: '租赁管理/租入单列表.html' }
      ],
      'chain': [
        { role: '租入单', name: 'RZD-20260815-005', url: '租赁管理/租入单列表.html' },
        { role: '应收账单（本单）', name: 'AR-20260904-015 · 供应商应收', self: true }
      ],
      'timeline': [
        { t: '09-04', text: '退租验收缺损 6 只 · 直接生成供应商应收（不走赔偿单）', who: '张伟' },
        { t: '—', text: '对方确认 → 开票 → 回款核销', who: '系统', off: true }
      ]
    },

    'AR-20260906-016': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "btype": "预付款（保证金）", "docs": "客户保证金（N3 · 直接建单承载）", "gen": "直接生成", "date": "2026-09-06", "status": "已结清"}, "cells": ["2026-09", "PRJ-2601", "一汽解放汽车有限公司", "<span class=\"tag tag-purple\" style=\"background:#f9f0ff;border-color:#d3adf7;color:#722ed1\">预付款（保证金）</span><div style=\"color:#8c8c8c;font-size:11px;\">客户保证金 · 无订单 · 直接建单承载</div>", "客户保证金（N3 · 直接建单承载）", "<span class=\"td-num\"><b>50,000.00</b></span>", "<span class=\"td-num\">50,000.00</span>", "<span class=\"tag tag-green\">已结清</span>", "<span class=\"tag tag-orange\">直接生成</span>", "2026-09-06 09:30"], "ops": [{"t": "详情", "detail": true}]},
      'title': '应收账单详情',
      'billNo': 'AR-20260906-016',
      'billType': '预付款（保证金）',
      'status': '已结清',
      'customer': '一汽解放汽车有限公司',
      'project': 'PRJ-2601',
      'period': '2026-09',
      'amount': 50000,
      'paid': 50000,
      'genMode': '直接生成（无订单保证金/预付款 · 直接建单承载，挂应收侧 · T2 待财务确认）',
      'scenario': 'N3 · 预付款（保证金）',
      'refs': [],
      'fees': [
        { src: '—', desc: '客户保证金（无订单 · 退款场景待议）', qty: '—', price: '—', amount: 50000 }
      ],
      'chain': [
        { role: '预付款（保证金）', name: '客户直接建单 · 无订单', self: true }
      ],
      'timeline': [
        { t: '09-06', text: '客户保证金到账 50,000 · 直接建单承载（不做独立预付款模块/虚拟项目）', who: '财务-周敏' },
        { t: '—', text: '合同结束按约退还或冲抵后续应收', who: '系统', off: true }
      ]
    },

   'AR-2026-09-PRJ2601-YS': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2601", "customer": "安吉智行物流", "btype": "预收客户预付 9-10 月租金，后续按月冲抵", "docs": "—", "gen": "手动登记", "date": "2026-09-05", "status": "已收"}, "cells": ["2026-09", "PRJ-2601", "安吉智行物流", "<span class=\"tag tag-blue\">预收</span><div style=\"color:#8c8c8c;font-size:11px;\">客户预付 9-10 月租金，后续按月冲抵</div>", "—", "<span class=\"td-num\"><b>50,000.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-green\">已收</span>", "<span class=\"tag tag-blue\">手动登记</span>", "2026-09-05 10:20"], "ops": [{"t": "详情", "detail": true}]},
      billNo: 'AR-2026-09-PRJ2601-YS',
      billType: '预收',
      status: '已收',
      customer: '安吉智行物流',
      project: 'PRJ-2601',
      period: '2026-09',
      amount: 50000,
      verified: 0,
      genMode: '手动登记',
      genDate: '2026-09-05',
      feeType: '预收（客户预付 9-10 月租金，后续按月冲抵）',
      scenario: '预收冲抵 · 客户预付租金',
      fees: [
        { src: '—', desc: '预收客户预付 9-10 月租金，后续按月冲抵', qty: '—', price: '—', amount: 50000 }
      ],
      chain: [
        { role: '应收账单（本单）', name: 'AR-2026-09-PRJ2601-YS · 预收', self: true },
        { role: '月度账单冲抵', name: '后续租金账单生成后自动冲抵' }
      ],
      timeline: [
        { t: '09-05', text: '预收款到账 · 记预收（安吉智行 ¥50,000）', who: '财务' },
        { t: '每月', text: '租金自预收冲抵 · 月度账单生成后自动冲抵', who: '系统', off: true }
      ]
    },

    /* ===== 销售费（一汽解放 · 未开票 · B1 销售线） ===== */
    'AR-2026-09-PRJ2601-S1': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "btype": "销售费（按销售出库自动汇总）关联 XSCK-20260902-015 等 2 单", "docs": "销售出库 XSCK-20260902-015 等", "gen": "自动生成", "date": "2026-09-03", "status": "未开票"}, "note": "1", "cells": ["2026-09", "PRJ-2601", "一汽解放汽车有限公司", "销售费（按销售出库自动汇总）<div style=\"color:#8c8c8c;font-size:11px;\">关联 XSCK-20260902-015 等 2 单</div>", "销售出库 XSCK-20260902-015 等", "<span class=\"td-num\"><b>10,200.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-red\">未开票</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-09-03 00:06"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      billNo: 'AR-2026-09-PRJ2601-S1',
      billType: '销售费',
      status: '未开票',
      customer: '一汽解放汽车有限公司',
      project: 'PRJ-2601',
      period: '2026-09',
      amount: 10200,
      verified: 0,
      genMode: '自动生成',
      genDate: '2026-09-03',
      feeType: '销售费（按销售出库自动汇总）',
      scenario: '财务通道 · 销售费应收',
      fees: [
        { src: 'XSCK-20260902-015', desc: '销售费 · 箱盖 ABS 吸塑', qty: '1,500 件', price: '6.80', amount: 10200, url: '销售管理/销售出库列表.html' }
      ],
      chain: [
        { role: '销售出库', name: 'XSCK-20260902-015', url: '销售管理/销售出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-09-PRJ2601-S1 · 销售费', self: true },
        { role: '开票登记', name: '待开票', url: '财务协同/开票登记.html' },
        { role: '回款 / 核销', name: '回款登记 → 银行水单核销', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '09-02', text: '销售出库 · XSCK-20260902-015（1,500 件）', who: '张伟' },
        { t: '09-03', text: '账单自动生成 · 销售费汇总', who: '系统' },
        { t: '—', text: '待开票 → 回款 → 水单核销', off: true }
      ]
    },

    /* ===== 销售费（东风本田 · 未开票） ===== */
    'AR-2026-09-PRJ2604-S1': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2604", "customer": "东风本田汽车有限公司", "btype": "销售费（按销售出库自动汇总）关联 XSCK-20260901-014", "docs": "销售出库 XSCK-20260901-014 等", "gen": "自动生成", "date": "2026-09-02", "status": "未开票"}, "cells": ["2026-09", "PRJ-2604", "东风本田汽车有限公司", "销售费（按销售出库自动汇总）<div style=\"color:#8c8c8c;font-size:11px;\">关联 XSCK-20260901-014</div>", "销售出库 XSCK-20260901-014 等", "<span class=\"td-num\"><b>1,280.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-red\">未开票</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-09-02 00:06"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      billNo: 'AR-2026-09-PRJ2604-S1',
      billType: '销售费',
      status: '未开票',
      customer: '东风本田汽车有限公司',
      project: 'PRJ-2604',
      period: '2026-09',
      amount: 1280,
      verified: 0,
      genMode: '自动生成',
      genDate: '2026-09-02',
      feeType: '销售费（按销售出库自动汇总）',
      fees: [
        { src: 'XSCK-20260901-014', desc: '销售费 · 零部件销售', qty: '160 件', price: '8.00', amount: 1280, url: '销售管理/销售出库列表.html' }
      ],
      chain: [
        { role: '销售出库', name: 'XSCK-20260901-014', url: '销售管理/销售出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-09-PRJ2604-S1 · 销售费', self: true },
        { role: '开票登记', name: '待开票', url: '财务协同/开票登记.html' },
        { role: '回款 / 核销', name: '回款登记 → 银行水单核销', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '09-01', text: '销售出库 · XSCK-20260901-014（160 件）', who: '张伟' },
        { t: '09-02', text: '账单自动生成 · 销售费汇总', who: '系统' },
        { t: '—', text: '待开票 → 回款 → 水单核销', off: true }
      ]
    },

    /* ===== 销售费（上汽大众宁波 · 已结清） ===== */
    'AR-2026-08-PRJ2602-S1': {
      'row': {"fields": {"period": "2026-08", "project": "PRJ-2602", "customer": "上汽大众宁波分公司", "btype": "销售费（按销售出库自动汇总）关联 XSCK-20260826-012", "docs": "销售出库 XSCK-20260826-012 等", "gen": "自动生成", "date": "2026-08-31", "status": "已结清"}, "cells": ["2026-08", "PRJ-2602", "上汽大众宁波分公司", "销售费（按销售出库自动汇总）<div style=\"color:#8c8c8c;font-size:11px;\">关联 XSCK-20260826-012</div>", "销售出库 XSCK-20260826-012 等", "<span class=\"td-num\"><b>6,050.00</b></span>", "<span class=\"td-num\">6,050.00</span>", "<span class=\"tag tag-green\">已结清</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-08-31 00:06"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      billNo: 'AR-2026-08-PRJ2602-S1',
      billType: '销售费',
      status: '已结清',
      customer: '上汽大众宁波分公司',
      project: 'PRJ-2602',
      period: '2026-08',
      amount: 6050,
      verified: 6050,
      genMode: '自动生成',
      genDate: '2026-08-31',
      feeType: '销售费（按销售出库自动汇总）',
      fees: [
        { src: 'XSCK-20260826-012', desc: '销售费 · 零部件销售', qty: '605 件', price: '10.00', amount: 6050, url: '销售管理/销售出库列表.html' }
      ],
      chain: [
        { role: '销售出库', name: 'XSCK-20260826-012', url: '销售管理/销售出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-08-PRJ2602-S1 · 销售费', self: true },
        { role: '开票登记', name: '已开票', url: '财务协同/开票登记.html' },
        { role: '回款 / 核销', name: '已核销结清', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '08-26', text: '销售出库 · XSCK-20260826-012（605 件）', who: '张伟' },
        { t: '08-31', text: '账单自动生成 · 销售费汇总', who: '系统' },
        { t: '09-02', text: '开票登记', who: '王芳' },
        { t: '09-05', text: '回款核销 6,050.00 元 · 结清', who: '财务' }
      ]
    },

    /* ===== 租赁费（一汽解放 · 部分收款） ===== */
    'AR-2026-08-PRJ2601': {
      'row': {"fields": {"period": "2026-08", "project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "btype": "租赁费（按组合出库自动汇总）", "docs": "租赁出库 26 张", "gen": "自动生成", "date": "2026-08-31", "status": "部分收款"}, "note": "2", "cells": ["2026-08", "PRJ-2601", "一汽解放汽车有限公司", "租赁费（按组合出库自动汇总）", "租赁出库 26 张", "<span class=\"td-num\"><b>486,200.00</b></span>", "<span class=\"td-num\">186,200.00</span>", "<span class=\"tag tag-orange\">部分收款</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-08-31 00:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      billNo: 'AR-2026-08-PRJ2601',
      billType: '租赁费',
      status: '部分收款',
      customer: '一汽解放汽车有限公司',
      project: 'PRJ-2601',
      period: '2026-08',
      amount: 486200,
      verified: 186200,
      genMode: '自动生成',
      genDate: '2026-08-31',
      feeType: '租赁费（按组合出库自动汇总）',
      fees: [
        { src: '组合出库单 ×26', desc: '租赁费 · 2026-08 账期（按组合出库自动汇总）', qty: '—', price: '—', amount: 486200, url: '租赁管理/组合出库列表.html' }
      ],
      chain: [
        { role: '组合出库', name: '组合出库 ×26 张', url: '租赁管理/组合出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-08-PRJ2601 · 租赁费', self: true },
        { role: '开票登记', name: '已开票', url: '财务协同/开票登记.html' },
        { role: '回款 / 核销', name: '部分核销 186,200.00', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '08-31', text: '账单自动生成 · 组合出库汇总 26 张', who: '系统' },
        { t: '09-02', text: '开票登记', who: '王芳' },
        { t: '09-05', text: '回款 186,200.00 元 · 水单核销', who: '财务' },
        { t: '—', text: '待收尾款 300,000.00 元', off: true }
      ]
    },

    /* ===== 租赁费（上汽大众宁波 · 未开票） ===== */
    'AR-2026-08-PRJ2602': {
      'row': {"fields": {"period": "2026-08", "project": "PRJ-2602", "customer": "上汽大众宁波分公司", "btype": "租赁费（按组合出库自动汇总）", "docs": "租赁出库 26 张", "gen": "自动生成", "date": "2026-08-31", "status": "未开票"}, "cells": ["2026-08", "PRJ-2602", "上汽大众宁波分公司", "租赁费（按组合出库自动汇总）", "租赁出库 26 张", "<span class=\"td-num\"><b>358,900.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-orange\">未开票</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-08-31 00:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      billNo: 'AR-2026-08-PRJ2602',
      billType: '租赁费',
      status: '未开票',
      customer: '上汽大众宁波分公司',
      project: 'PRJ-2602',
      period: '2026-08',
      amount: 358900,
      verified: 0,
      genMode: '自动生成',
      genDate: '2026-08-31',
      feeType: '租赁费（按组合出库自动汇总）',
      fees: [
        { src: '组合出库单 ×26', desc: '租赁费 · 2026-08 账期（按组合出库自动汇总）', qty: '—', price: '—', amount: 358900, url: '租赁管理/组合出库列表.html' }
      ],
      chain: [
        { role: '组合出库', name: '组合出库 ×26 张', url: '租赁管理/组合出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-08-PRJ2602 · 租赁费', self: true },
        { role: '开票登记', name: '待开票', url: '财务协同/开票登记.html' },
        { role: '回款 / 核销', name: '回款登记 → 银行水单核销', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '08-31', text: '账单自动生成 · 组合出库汇总 26 张', who: '系统' },
        { t: '—', text: '待开票 → 回款 → 水单核销', off: true }
      ]
    },

    /* ===== 租赁费（小鹏汽车 · 未开票） ===== */
    'AR-2026-08-PRJ2603': {
      'row': {"fields": {"period": "2026-08", "project": "PRJ-2603", "customer": "小鹏汽车科技有限公司", "btype": "租赁费（按组合出库自动汇总）", "docs": "租赁出库 26 张", "gen": "自动生成", "date": "2026-08-31", "status": "未开票"}, "cells": ["2026-08", "PRJ-2603", "小鹏汽车科技有限公司", "租赁费（按组合出库自动汇总）", "租赁出库 26 张", "<span class=\"td-num\"><b>241,500.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-orange\">未开票</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-08-31 00:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      billNo: 'AR-2026-08-PRJ2603',
      billType: '租赁费',
      status: '未开票',
      customer: '小鹏汽车科技有限公司',
      project: 'PRJ-2603',
      period: '2026-08',
      amount: 241500,
      verified: 0,
      genMode: '自动生成',
      genDate: '2026-08-31',
      feeType: '租赁费（按组合出库自动汇总）',
      fees: [
        { src: '组合出库单 ×26', desc: '租赁费 · 2026-08 账期（按组合出库自动汇总）', qty: '—', price: '—', amount: 241500, url: '租赁管理/组合出库列表.html' }
      ],
      chain: [
        { role: '组合出库', name: '组合出库 ×26 张', url: '租赁管理/组合出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-08-PRJ2603 · 租赁费', self: true },
        { role: '开票登记', name: '待开票', url: '财务协同/开票登记.html' },
        { role: '回款 / 核销', name: '回款登记 → 银行水单核销', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '08-31', text: '账单自动生成 · 组合出库汇总 26 张', who: '系统' },
        { t: '—', text: '待开票 → 回款 → 水单核销', off: true }
      ]
    },

    /* ===== 租赁费（一汽解放 · 已结清） ===== */
    'AR-2026-07-PRJ2601': {
      'row': {"fields": {"period": "2026-07", "project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "btype": "租赁费（按组合出库自动汇总）", "docs": "租赁出库 26 张", "gen": "自动生成", "date": "2026-07-31", "status": "已结清"}, "cells": ["2026-07", "PRJ-2601", "一汽解放汽车有限公司", "租赁费（按组合出库自动汇总）", "租赁出库 26 张", "<span class=\"td-num\"><b>442,800.00</b></span>", "<span class=\"td-num\">442,800.00</span>", "<span class=\"tag tag-green\">已结清</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-07-31 00:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      billNo: 'AR-2026-07-PRJ2601',
      billType: '租赁费',
      status: '已结清',
      customer: '一汽解放汽车有限公司',
      project: 'PRJ-2601',
      period: '2026-07',
      amount: 442800,
      verified: 442800,
      genMode: '自动生成',
      genDate: '2026-07-31',
      feeType: '租赁费（按组合出库自动汇总）',
      fees: [
        { src: '组合出库单 ×26', desc: '租赁费 · 2026-07 账期（按组合出库自动汇总）', qty: '—', price: '—', amount: 442800, url: '租赁管理/组合出库列表.html' }
      ],
      chain: [
        { role: '组合出库', name: '组合出库 ×26 张', url: '租赁管理/组合出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-07-PRJ2601 · 租赁费', self: true },
        { role: '开票登记', name: '已开票', url: '财务协同/开票登记.html' },
        { role: '回款 / 核销', name: '已核销结清', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '07-31', text: '账单自动生成 · 组合出库汇总 26 张', who: '系统' },
        { t: '08-05', text: '开票登记', who: '王芳' },
        { t: '08-20', text: '回款核销 442,800.00 元 · 结清', who: '财务' }
      ]
    },

    /* ===== 丢损赔偿（一汽解放 · 未开票 · 退租联动转应收） ===== */
    'BS-20260828-004': {
      'row': {"fields": {"period": "2026-08", "project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "btype": "丢损赔偿单（退租联动）", "docs": "丢损赔偿单 BS-20260828-004", "gen": "赔偿联动", "date": "2026-08-28", "status": "未开票"}, "note": "3", "cells": ["2026-08", "PRJ-2601", "一汽解放汽车有限公司", "丢损赔偿单（退租联动）", "丢损赔偿单 BS-20260828-004", "<span class=\"td-num\"><b>3,690.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-orange\">未开票</span>", "<span class=\"tag tag-blue\">赔偿联动</span>", "2026-08-28 11:30"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      billNo: 'BS-20260828-004',
      billType: '丢损赔偿',
      status: '未开票',
      customer: '一汽解放汽车有限公司',
      project: 'PRJ-2601',
      period: '2026-08',
      amount: 3690,
      verified: 0,
      genMode: '直接生成（丢损赔付联动核销 · 无赔偿单）',
      genDate: '2026-08-28',
      feeType: '丢损赔偿（退租联动转应收）',
      scenario: 'S5 · 丢损赔偿转应收',
      fees: [
        { src: 'BS-20260828-004', desc: '退租丢损赔偿 · 客户承担', qty: '—', price: '—', amount: 3690 }
      ],
      chain: [
        { role: '丢损赔偿单', name: 'BS-20260828-004' },
        { role: '应收账单（本单）', name: 'BS-20260828-004 · 丢损赔偿', self: true },
        { role: '开票登记', name: '待开票', url: '财务协同/开票登记.html' },
        { role: '回款 / 核销', name: '回款登记 → 银行水单核销', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '08-28', text: '丢损赔偿审核通过 · BS-20260828-004 转应收', who: '王芳' },
        { t: '08-28', text: '应收账单自动生成', who: '系统' },
        { t: '—', text: '待开票 → 回款 → 水单核销', off: true }
      ]
    },

    /* ===== 租赁费（上汽大众宁波 · 部分收款） ===== */
    'AR-2026-07-PRJ2602': {
      'row': {"fields": {"period": "2026-07", "project": "PRJ-2602", "customer": "上汽大众宁波分公司", "btype": "租赁费（按组合出库自动汇总）", "docs": "租赁出库 26 张", "gen": "自动生成", "date": "2026-07-31", "status": "部分收款"}, "cells": ["2026-07", "PRJ-2602", "上汽大众宁波分公司", "租赁费（按组合出库自动汇总）", "租赁出库 26 张", "<span class=\"td-num\"><b>366,200.00</b></span>", "<span class=\"td-num\">186,200.00</span>", "<span class=\"tag tag-orange\">部分收款</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-07-31 00:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      billNo: 'AR-2026-07-PRJ2602',
      billType: '租赁费',
      status: '部分收款',
      customer: '上汽大众宁波分公司',
      project: 'PRJ-2602',
      period: '2026-07',
      amount: 366200,
      verified: 186200,
      genMode: '自动生成',
      genDate: '2026-07-31',
      feeType: '租赁费（按组合出库自动汇总）',
      fees: [
        { src: '组合出库单 ×26', desc: '租赁费 · 2026-07 账期（按组合出库自动汇总）', qty: '—', price: '—', amount: 366200, url: '租赁管理/组合出库列表.html' }
      ],
      chain: [
        { role: '组合出库', name: '组合出库 ×26 张', url: '租赁管理/组合出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-07-PRJ2602 · 租赁费', self: true },
        { role: '开票登记', name: '已开票', url: '财务协同/开票登记.html' },
        { role: '回款 / 核销', name: '部分核销 186,200.00', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '07-31', text: '账单自动生成 · 组合出库汇总 26 张', who: '系统' },
        { t: '08-05', text: '开票登记', who: '王芳' },
        { t: '08-25', text: '回款 186,200.00 元 · 水单核销', who: '财务' },
        { t: '—', text: '待收尾款 180,000.00 元', off: true }
      ]
    },

    /* ===== 租赁费（上汽大众宁波 · 已结清） ===== */
    'AR-2026-06-PRJ2602': {
      'row': {"fields": {"period": "2026-06", "project": "PRJ-2602", "customer": "上汽大众宁波分公司", "btype": "租赁费（按组合出库自动汇总）", "docs": "租赁出库 26 张", "gen": "自动生成", "date": "2026-06-30", "status": "已结清"}, "cells": ["2026-06", "PRJ-2602", "上汽大众宁波分公司", "租赁费（按组合出库自动汇总）", "租赁出库 26 张", "<span class=\"td-num\"><b>358,900.00</b></span>", "<span class=\"td-num\">358,900.00</span>", "<span class=\"tag tag-green\">已结清</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-06-30 00:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      billNo: 'AR-2026-06-PRJ2602',
      billType: '租赁费',
      status: '已结清',
      customer: '上汽大众宁波分公司',
      project: 'PRJ-2602',
      period: '2026-06',
      amount: 358900,
      verified: 358900,
      genMode: '自动生成',
      genDate: '2026-06-30',
      feeType: '租赁费（按组合出库自动汇总）',
      fees: [
        { src: '组合出库单 ×26', desc: '租赁费 · 2026-06 账期（按组合出库自动汇总）', qty: '—', price: '—', amount: 358900, url: '租赁管理/组合出库列表.html' }
      ],
      chain: [
        { role: '组合出库', name: '组合出库 ×26 张', url: '租赁管理/组合出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-06-PRJ2602 · 租赁费', self: true },
        { role: '开票登记', name: '已开票', url: '财务协同/开票登记.html' },
        { role: '回款 / 核销', name: '已核销结清', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '06-30', text: '账单自动生成 · 组合出库汇总 26 张', who: '系统' },
        { t: '07-05', text: '开票登记', who: '王芳' },
        { t: '07-18', text: '回款核销 358,900.00 元 · 结清', who: '财务' }
      ]
    }
  },

  /* --------------------------------------------------------------------------
   * 财务协同下游单据（通用四段式，渲染器 _data/detail-generic.js）
   *   记录结构：title 弹窗标题前缀 / titleNo 标题显示单号（缺省用键）
   *     info: [{label, text, full?, url?, tag?}]  tag 走统一状态色
   *     feeCols + fees: [{cells:[...], links:{列号:url}}]
   *     chain / timeline 同账单实体
   *   金额/数量一律存展示字符串（通用渲染器不做语义格式化）
   * ------------------------------------------------------------------------ */

  /* 付款登记（键 = PAY 付款单号） */
  payments: {
    'PAY-20260902-005': {
      'row': {"fields": {"supplier": "苏州联恒五金制品有限公司", "ref": "AP-20260830-007", "bank": "招商银行苏州分行 1109××××8821", "date": "2026-09-02", "status": "待确认"}, "note": "1", "cells": ["苏州联恒五金制品有限公司", "<span class=\"lk\">AP-20260830-007</span>", "<span class=\"td-num\">6,000.00</span>", "2026-09-02", "招商银行苏州分行 1109××××8821", "<span class=\"tag tag-orange\">待确认</span>"], "ops": [{"t": "确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}]},
      title: '付款登记详情',
      info: [
        { label: '付款单号', text: 'PAY-20260902-005', full: true },
        { label: '状态', tag: '待确认' },
        { label: '付款日期', text: '2026-09-02' },
        { label: '供应商', text: '苏州联恒五金制品有限公司', full: true },
        { label: '关联应付', text: 'AP-20260830-007', url: '财务协同/应付账单.html' },
        { label: '付款金额', text: '6,000.00 元' },
        { label: '付款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务-周敏' },
        { label: '付款方式', text: '银行转账' },
        { label: '凭证', text: '已上传' }
      ],
      feeCols: ['关联账单', '账单类型', '本次付款(元)'],
      fees: [
        { cells: ['AP-20260830-007', '采购应付', '6,000.00'], links: { 0: '财务协同/应付账单.html' } }
      ],
      chain: [
        { role: '应付账单', name: 'AP-20260830-007', url: '财务协同/应付账单.html' },
        { role: '付款登记（本单）', name: 'PAY-20260902-005', self: true },
        { role: '付款确认', name: '待确认（审核流）' }
      ],
      timeline: [
        { t: '09-02 16:05', text: '付款登记 · 上传付款凭证', who: '财务-周敏' },
        { t: '—', text: '待确认 · 通过后账单转已付款', off: true }
      ]
    },
    'PAY-20260831-004': {
      'row': {"fields": {"supplier": "常州正大塑料托盘厂", "ref": "AP-20260828-006", "bank": "中国银行常州分行 3325××××0067", "date": "2026-08-31", "status": "已确认"}, "cells": ["常州正大塑料托盘厂", "<span class=\"lk\">AP-20260828-006</span>", "<span class=\"td-num\">42,500.00</span>", "2026-08-31", "中国银行常州分行 3325××××0067", "<span class=\"tag tag-green\">已确认</span>"], "ops": [{"t": "详情", "detail": true}]},
      title: '付款登记详情',
      info: [
        { label: '付款单号', text: 'PAY-20260831-004', full: true },
        { label: '状态', tag: '已确认' },
        { label: '付款日期', text: '2026-08-31' },
        { label: '供应商', text: '常州正大塑料托盘厂', full: true },
        { label: '关联应付', text: 'AP-20260828-006', url: '财务协同/应付账单.html' },
        { label: '付款金额', text: '42,500.00 元' },
        { label: '付款账户', text: '中国银行常州分行 3325××××0067' },
        { label: '登记人', text: '财务-周敏' },
        { label: '付款方式', text: '银行转账' },
        { label: '凭证', text: '已上传' }
      ],
      feeCols: ['关联账单', '账单类型', '本次付款(元)'],
      fees: [
        { cells: ['AP-20260828-006', '采购应付', '42,500.00'], links: { 0: '财务协同/应付账单.html' } }
      ],
      chain: [
        { role: '应付账单', name: 'AP-20260828-006', url: '财务协同/应付账单.html' },
        { role: '付款登记（本单）', name: 'PAY-20260831-004', self: true },
        { role: '付款确认', name: '已确认 · 账单转已付款' }
      ],
      timeline: [
        { t: '08-31 14:20', text: '付款登记 · 上传付款凭证', who: '财务-周敏' },
        { t: '09-01 09:15', text: '付款确认通过 · 账单转已付款', who: '王芳' }
      ]
    },
    'PAY-20260828-003': {
      'row': {"fields": {"supplier": "宁波华塑包装制品有限公司", "ref": "AP-20260815-003", "bank": "工商银行宁波分行 4402××××5531", "date": "2026-08-28", "status": "已确认"}, "cells": ["宁波华塑包装制品有限公司", "<span class=\"lk\">AP-20260815-003</span>", "<span class=\"td-num\">35,200.00</span>", "2026-08-28", "工商银行宁波分行 4402××××5531", "<span class=\"tag tag-green\">已确认</span>"], "ops": [{"t": "详情", "detail": true}]},
      title: '付款登记详情',
      info: [
        { label: '付款单号', text: 'PAY-20260828-003', full: true },
        { label: '状态', tag: '已确认' },
        { label: '付款日期', text: '2026-08-28' },
        { label: '供应商', text: '宁波华塑包装制品有限公司', full: true },
        { label: '关联应付', text: 'AP-20260815-003', url: '财务协同/应付账单.html' },
        { label: '付款金额', text: '35,200.00 元' },
        { label: '付款账户', text: '工商银行宁波分行 4402××××5531' },
        { label: '登记人', text: '财务-周敏' },
        { label: '付款方式', text: '银行转账' },
        { label: '凭证', text: '已上传' }
      ],
      feeCols: ['关联账单', '账单类型', '本次付款(元)'],
      fees: [
        { cells: ['AP-20260815-003', '采购应付', '35,200.00'], links: { 0: '财务协同/应付账单.html' } }
      ],
      chain: [
        { role: '应付账单', name: 'AP-20260815-003', url: '财务协同/应付账单.html' },
        { role: '付款登记（本单）', name: 'PAY-20260828-003', self: true },
        { role: '付款确认', name: '已确认 · 账单转已付款' }
      ],
      timeline: [
        { t: '08-28 11:40', text: '付款登记 · 上传付款凭证', who: '财务-周敏' },
        { t: '08-29 10:05', text: '付款确认通过 · 账单转已付款', who: '王芳' }
      ]
    },
    'PAY-20260825-002': {
      'row': {"fields": {"supplier": "苏州联恒五金制品有限公司", "ref": "AP-20260820-004", "bank": "招商银行苏州分行 1109××××8821", "date": "2026-08-25", "status": "已确认"}, "cells": ["苏州联恒五金制品有限公司", "<span class=\"lk\">AP-20260820-004</span>", "<span class=\"td-num\">6,300.00</span>", "2026-08-25", "招商银行苏州分行 1109××××8821", "<span class=\"tag tag-green\">已确认</span>"], "ops": [{"t": "详情", "detail": true}]},
      title: '付款登记详情',
      info: [
        { label: '付款单号', text: 'PAY-20260825-002', full: true },
        { label: '状态', tag: '已确认' },
        { label: '付款日期', text: '2026-08-25' },
        { label: '供应商', text: '苏州联恒五金制品有限公司', full: true },
        { label: '关联应付', text: 'AP-20260820-004', url: '财务协同/应付账单.html' },
        { label: '付款金额', text: '6,300.00 元' },
        { label: '付款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务-周敏' },
        { label: '付款方式', text: '银行转账' },
        { label: '凭证', text: '已上传' }
      ],
      feeCols: ['关联账单', '账单类型', '本次付款(元)'],
      fees: [
        { cells: ['AP-20260820-004', '采购应付', '6,300.00'], links: { 0: '财务协同/应付账单.html' } }
      ],
      chain: [
        { role: '应付账单', name: 'AP-20260820-004', url: '财务协同/应付账单.html' },
        { role: '付款登记（本单）', name: 'PAY-20260825-002', self: true },
        { role: '付款确认', name: '已确认 · 账单转已付款' }
      ],
      timeline: [
        { t: '08-25 15:30', text: '付款登记 · 上传付款凭证', who: '财务-周敏' },
        { t: '08-26 09:10', text: '付款确认通过 · 账单转已付款', who: '王芳' }
      ]
    },
    'PAY-20260818-001': {
      'row': {"fields": {"supplier": "路凯包装运营（上海）有限公司", "ref": "AP-20260810-002", "bank": "建设银行上海分行 6217××××9045", "date": "2026-08-18", "status": "已确认"}, "cells": ["路凯包装运营（上海）有限公司", "<span class=\"lk\">AP-20260810-002</span>", "<span class=\"td-num\">58,000.00</span>", "2026-08-18", "建设银行上海分行 6217××××9045", "<span class=\"tag tag-green\">已确认</span>"], "ops": [{"t": "详情", "detail": true}]},
      title: '付款登记详情',
      info: [
        { label: '付款单号', text: 'PAY-20260818-001', full: true },
        { label: '状态', tag: '已确认' },
        { label: '付款日期', text: '2026-08-18' },
        { label: '供应商', text: '路凯包装运营（上海）有限公司', full: true },
        { label: '关联应付', text: 'AP-20260810-002', url: '财务协同/应付账单.html' },
        { label: '付款金额', text: '58,000.00 元' },
        { label: '付款账户', text: '建设银行上海分行 6217××××9045' },
        { label: '登记人', text: '财务-周敏' },
        { label: '付款方式', text: '银行转账' },
        { label: '凭证', text: '已上传' }
      ],
      feeCols: ['关联账单', '账单类型', '本次付款(元)'],
      fees: [
        { cells: ['AP-20260810-002', '租金应付', '58,000.00'], links: { 0: '财务协同/应付账单.html' } }
      ],
      chain: [
        { role: '应付账单', name: 'AP-20260810-002', url: '财务协同/应付账单.html' },
        { role: '付款登记（本单）', name: 'PAY-20260818-001', self: true },
        { role: '付款确认', name: '已确认 · 账单转已付款' }
      ],
      timeline: [
        { t: '08-18 10:12', text: '付款登记 · 上传付款凭证', who: '财务-周敏' },
        { t: '08-19 09:40', text: '付款确认通过 · 账单转已付款', who: '王芳' }
      ]
    }
  },

  /* 回款登记（键 = HK 回款单号） */
  receipts: {
    'HK-20260830-014': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "ref": "AR-2026-08-PRJ2601", "bank": "招行基本户 1209****8866", "receipt": "已上传", "date": "2026-08-30", "status": "待核销"}, "note": "1", "cells": ["一汽解放汽车有限公司", "AR-2026-08-PRJ2601", "<span class=\"td-num\"><b>286,500.00</b></span>", "2026-08-30", "招行基本户 1209****8866", "<span class=\"tag tag-green\">已上传</span>", "<span class=\"tag tag-orange\">待核销</span>"], "ops": [{"t": "确认收款", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "去核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      title: '回款登记详情',
      info: [
        { label: '回款单号', text: 'HK-20260830-014', full: true },
        { label: '水单状态', tag: '已上传' },
        { label: '核销状态', tag: '待核销' },
        { label: '客户', text: '一汽解放汽车有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-08-PRJ2601', url: '财务协同/应收账单.html' },
        { label: '发票关联', text: 'INV-20260830-012', url: '财务协同/开票登记.html' },
        { label: '回款金额', text: '286,500.00 元' },
        { label: '回款日期', text: '2026-08-30' },
        { label: '收款账户', text: '招行基本户 1209****8866' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['关联账单', '费用项', '本次回款(元)', '核销去向'],
      fees: [
        { cells: ['AR-2026-08-PRJ2601', '租赁费 · 部分回款', '286,500.00', '银行水单核销（待执行）'], links: { 0: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-08-PRJ2601', url: '财务协同/应收账单.html' },
        { role: '开票登记', name: 'INV-20260830-012', url: '财务协同/开票登记.html' },
        { role: '回款登记（本单）', name: 'HK-20260830-014', self: true },
        { role: '银行水单核销', name: 'SD-20260830-011', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '08-30 10:20', text: '收款到账 · 招行基本户', who: '财务-周敏' },
        { t: '08-30 10:35', text: '水单上传 · 与应收账单关联', who: '财务-周敏' },
        { t: '—', text: '待核销 → 银行水单核销勾对', off: true }
      ]
    },
    'HK-20260828-013': {
      'row': {"fields": {"customer": "上汽大众宁波分公司", "ref": "AR-2026-07-PRJ2602", "bank": "建行一般户 3321****0417", "receipt": "已上传", "date": "2026-08-28", "status": "待核销"}, "cells": ["上汽大众宁波分公司", "AR-2026-07-PRJ2602", "<span class=\"td-num\"><b>158,420.50</b></span>", "2026-08-28", "建行一般户 3321****0417", "<span class=\"tag tag-green\">已上传</span>", "<span class=\"tag tag-orange\">待核销</span>"], "ops": [{"t": "确认收款", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "去核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      title: '回款登记详情',
      info: [
        { label: '回款单号', text: 'HK-20260828-013', full: true },
        { label: '水单状态', tag: '已上传' },
        { label: '核销状态', tag: '待核销' },
        { label: '客户', text: '上汽大众宁波分公司', full: true },
        { label: '关联应收', text: 'AR-2026-07-PRJ2602', url: '财务协同/应收账单.html' },
        { label: '发票关联', text: 'INV-20260826-011', url: '财务协同/开票登记.html' },
        { label: '回款金额', text: '158,420.50 元' },
        { label: '回款日期', text: '2026-08-28' },
        { label: '收款账户', text: '建行一般户 3321****0417' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['关联账单', '费用项', '本次回款(元)', '核销去向'],
      fees: [
        { cells: ['AR-2026-07-PRJ2602', '租赁费 · 部分回款', '158,420.50', '银行水单核销（待执行）'], links: { 0: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-07-PRJ2602', url: '财务协同/应收账单.html' },
        { role: '开票登记', name: 'INV-20260826-011', url: '财务协同/开票登记.html' },
        { role: '回款登记（本单）', name: 'HK-20260828-013', self: true },
        { role: '银行水单核销', name: 'SD-20260828-010', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '08-28 09:50', text: '收款到账 · 建行一般户', who: '财务-周敏' },
        { t: '08-28 10:10', text: '水单上传 · 与应收账单关联', who: '财务-周敏' },
        { t: '—', text: '待核销 → 银行水单核销勾对', off: true }
      ]
    },
    'HK-20260825-012': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "ref": "AR-2026-07-PRJ2601", "bank": "招行基本户 1209****8866", "receipt": "已上传", "date": "2026-08-25", "status": "部分核销"}, "cells": ["一汽解放汽车有限公司", "AR-2026-07-PRJ2601", "<span class=\"td-num\"><b>98,000.00</b></span>", "2026-08-25", "招行基本户 1209****8866", "<span class=\"tag tag-green\">已上传</span>", "<span class=\"tag tag-blue\">部分核销</span>"], "ops": [{"t": "确认收款", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "去核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      title: '回款登记详情',
      info: [
        { label: '回款单号', text: 'HK-20260825-012', full: true },
        { label: '水单状态', tag: '已上传' },
        { label: '核销状态', tag: '部分核销' },
        { label: '客户', text: '一汽解放汽车有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-07-PRJ2601', url: '财务协同/应收账单.html' },
        { label: '发票关联', text: 'INV-20260820-010', url: '财务协同/开票登记.html' },
        { label: '回款金额', text: '98,000.00 元' },
        { label: '回款日期', text: '2026-08-25' },
        { label: '收款账户', text: '招行基本户 1209****8866' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['关联账单', '费用项', '本次回款(元)', '核销去向'],
      fees: [
        { cells: ['AR-2026-07-PRJ2601', '租赁费 · 部分回款', '98,000.00', '已核销 60,000.00 · 余 38,000.00'], links: { 0: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-07-PRJ2601', url: '财务协同/应收账单.html' },
        { role: '开票登记', name: 'INV-20260820-010', url: '财务协同/开票登记.html' },
        { role: '回款登记（本单）', name: 'HK-20260825-012', self: true },
        { role: '银行水单核销', name: 'SD-20260825-009 · 部分核销', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '08-25 14:05', text: '收款到账 · 招行基本户', who: '财务-周敏' },
        { t: '08-25 14:20', text: '水单上传 · 与应收账单关联', who: '财务-周敏' },
        { t: '08-30 14:22', text: '水单核销 60,000.00 元 · 部分核销', who: '李静' },
        { t: '—', text: '余 38,000.00 待后续核销', off: true }
      ]
    },
    'HK-20260822-011': {
      'row': {"fields": {"customer": "小鹏汽车科技有限公司", "ref": "AR-2026-07-PRJ2603", "bank": "工行一般户 0200****5533", "receipt": "补传回单", "date": "2026-08-22", "status": "已核销"}, "cells": ["小鹏汽车科技有限公司", "AR-2026-07-PRJ2603", "<span class=\"td-num\"><b>65,320.00</b></span>", "2026-08-22", "工行一般户 0200****5533", "<span class=\"ops\"><a>补传回单</a></span>", "<span class=\"tag tag-green\">已核销</span>"], "ops": [{"t": "确认收款", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "去核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      title: '回款登记详情',
      info: [
        { label: '回款单号', text: 'HK-20260822-011', full: true },
        { label: '水单状态', tag: '补传回单' },
        { label: '核销状态', tag: '已核销' },
        { label: '客户', text: '小鹏汽车科技有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-07-PRJ2603', url: '财务协同/应收账单.html' },
        { label: '发票关联', text: 'INV-20260815-009', url: '财务协同/开票登记.html' },
        { label: '回款金额', text: '65,320.00 元' },
        { label: '回款日期', text: '2026-08-22' },
        { label: '收款账户', text: '工行一般户 0200****5533' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['关联账单', '费用项', '本次回款(元)', '核销去向'],
      fees: [
        { cells: ['AR-2026-07-PRJ2603', '租赁费 · 部分回款', '65,320.00', '已核销（全额）'], links: { 0: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-07-PRJ2603', url: '财务协同/应收账单.html' },
        { role: '开票登记', name: 'INV-20260815-009', url: '财务协同/开票登记.html' },
        { role: '回款登记（本单）', name: 'HK-20260822-011', self: true },
        { role: '银行水单核销', name: 'SD-20260822-008 · 已核销', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '08-22 11:30', text: '收款到账 · 工行一般户', who: '财务-周敏' },
        { t: '08-26 09:15', text: '补传回款单', who: '财务-周敏' },
        { t: '08-28 10:05', text: '水单核销 65,320.00 元 · 全额核销', who: '李静' }
      ]
    },
    'HK-20260818-010': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "ref": "BS-20260802-001", "bank": "招行基本户 1209****8866", "receipt": "已上传", "date": "2026-08-18", "status": "已核销"}, "cells": ["一汽解放汽车有限公司", "BS-20260802-001", "<span class=\"td-num\"><b>860.00</b></span>", "2026-08-18", "招行基本户 1209****8866", "<span class=\"tag tag-green\">已上传</span>", "<span class=\"tag tag-green\">已核销</span>"], "ops": [{"t": "确认收款", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "去核销", "act": "go('../财务协同/银行水单核销.html')"}]},
      title: '回款登记详情',
      info: [
        { label: '回款单号', text: 'HK-20260818-010', full: true },
        { label: '水单状态', tag: '已上传' },
        { label: '核销状态', tag: '已核销' },
        { label: '客户', text: '一汽解放汽车有限公司', full: true },
        { label: '关联应收', text: 'BS-20260802-001（丢损赔偿）' },
        { label: '发票关联', text: '—' },
        { label: '回款金额', text: '860.00 元' },
        { label: '回款日期', text: '2026-08-18' },
        { label: '收款账户', text: '招行基本户 1209****8866' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['关联账单', '费用项', '本次回款(元)', '核销去向'],
      fees: [
        { cells: ['BS-20260802-001', '丢损赔偿款', '860.00', '已核销（全额）'] }
      ],
      chain: [
        { role: '丢损赔偿单', name: 'BS-20260802-001' },
        { role: '回款登记（本单）', name: 'HK-20260818-010', self: true },
        { role: '银行水单核销', name: 'SD-20260818-006 · 已核销', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '08-18 15:40', text: '收款到账 · 招行基本户', who: '财务-周敏' },
        { t: '08-18 15:55', text: '水单上传 · 关联丢损赔偿单', who: '财务-周敏' },
        { t: '08-26 16:40', text: '水单核销 860.00 元 · 全额核销', who: '李静' }
      ]
    }
  },

  /* 开票登记（键 = INV 登记单号） */
  invoices: {
    'INV-20260902-013': {
      'row': {"fields": {"no": "26119800421390", "itype": "专票", "buyer": "上汽大众汽车有限公司宁波分公司", "ref": "AR-2026-08-PRJ2603", "date": "2026-09-02", "status": "已红冲"}, "cells": ["26119800421390", "<span class=\"tag tag-blue\">专票</span>", "上汽大众汽车有限公司宁波分公司", "AR-2026-08-PRJ2603", "<span class=\"td-num\"><b>-46,800.00</b></span>", "13%", "2026-09-02", "<span class=\"tag tag-red\">已红冲</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "查看账单", "act": "go('../财务协同/应收账单.html')"}]},
      title: '开票登记详情',
      info: [
        { label: '登记单号', text: 'INV-20260902-013', full: true },
        { label: '状态', tag: '已红冲' },
        { label: '开票日期', text: '2026-09-02' },
        { label: '发票号码', text: '26119800421390' },
        { label: '发票类型', text: '增值税专用发票' },
        { label: '购方', text: '上汽大众汽车有限公司宁波分公司', full: true },
        { label: '关联应收', text: 'AR-2026-08-PRJ2603', url: '财务协同/应收账单.html' },
        { label: '价税合计', text: '-46,800.00 元' },
        { label: '税率', text: '13%' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['费用项', '关联账单', '税率', '金额(元)'],
      fees: [
        { cells: ['租赁费 · 2026-08（红冲）', 'AR-2026-08-PRJ2603', '13%', '-46,800.00'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-08-PRJ2603', url: '财务协同/应收账单.html' },
        { role: '开票登记（本单）', name: 'INV-20260902-013 · 已红冲', self: true },
        { role: '红字发票', name: '冲减应收 46,800.00' }
      ],
      timeline: [
        { t: '08-31', text: '应收账单汇总 · AR-2026-08-PRJ2603', who: '系统' },
        { t: '09-02 10:20', text: '开票登记 · 发票号码 26119800421390', who: '财务-周敏' },
        { t: '09-02 17:05', text: '红冲 · 价税合计 -46,800.00（开票信息有误作废重开）', who: '财务-周敏' }
      ]
    },
    'INV-20260830-012': {
      'row': {"fields": {"no": "26119800421376", "itype": "专票", "buyer": "一汽解放汽车有限公司", "ref": "AR-2026-08-PRJ2601", "date": "2026-08-30", "status": "已登记"}, "note": "1", "cells": ["26119800421376", "<span class=\"tag tag-blue\">专票</span>", "一汽解放汽车有限公司", "AR-2026-08-PRJ2601", "<span class=\"td-num\"><b>186,200.00</b></span>", "13%", "2026-08-30", "<span class=\"tag tag-green\">已登记</span>"], "ops": [{"t": "开票确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "查看账单", "act": "go('../财务协同/应收账单.html')"}, {"t": "回款", "act": "go('../财务协同/回款登记.html')"}]},
      title: '开票登记详情',
      info: [
        { label: '登记单号', text: 'INV-20260830-012', full: true },
        { label: '状态', tag: '已登记' },
        { label: '开票日期', text: '2026-08-30' },
        { label: '发票号码', text: '26119800421376' },
        { label: '发票类型', text: '增值税专用发票' },
        { label: '购方', text: '一汽解放汽车有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-08-PRJ2601', url: '财务协同/应收账单.html' },
        { label: '价税合计', text: '186,200.00 元' },
        { label: '税率', text: '13%' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['费用项', '关联账单', '税率', '金额(元)'],
      fees: [
        { cells: ['租赁费 · 2026-08', 'AR-2026-08-PRJ2601', '13%', '186,200.00'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-08-PRJ2601', url: '财务协同/应收账单.html' },
        { role: '开票登记（本单）', name: 'INV-20260830-012', self: true },
        { role: '回款登记', name: 'HK-20260830-014', url: '财务协同/回款登记.html' },
        { role: '银行水单核销', name: 'SD-20260830-011', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '08-30', text: '应收账单汇总 · AR-2026-08-PRJ2601', who: '系统' },
        { t: '08-30 16:40', text: '开票登记 · 发票号码 26119800421376', who: '财务-周敏' },
        { t: '—', text: '待回款 → 水单核销', off: true }
      ]
    },
    'INV-20260826-011': {
      'row': {"fields": {"no": "26119800420988", "itype": "专票", "buyer": "上汽大众宁波分公司", "ref": "AR-2026-07-PRJ2602", "date": "2026-08-26", "status": "已登记"}, "cells": ["26119800420988", "<span class=\"tag tag-blue\">专票</span>", "上汽大众宁波分公司", "AR-2026-07-PRJ2602", "<span class=\"td-num\"><b>186,200.00</b></span>", "13%", "2026-08-26", "<span class=\"tag tag-green\">已登记</span>"], "ops": [{"t": "开票确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "查看账单", "act": "go('../财务协同/应收账单.html')"}, {"t": "回款", "act": "go('../财务协同/回款登记.html')"}]},
      title: '开票登记详情',
      info: [
        { label: '登记单号', text: 'INV-20260826-011', full: true },
        { label: '状态', tag: '已登记' },
        { label: '开票日期', text: '2026-08-26' },
        { label: '发票号码', text: '26119800420988' },
        { label: '发票类型', text: '增值税专用发票' },
        { label: '购方', text: '上汽大众宁波分公司', full: true },
        { label: '关联应收', text: 'AR-2026-07-PRJ2602', url: '财务协同/应收账单.html' },
        { label: '价税合计', text: '186,200.00 元' },
        { label: '税率', text: '13%' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['费用项', '关联账单', '税率', '金额(元)'],
      fees: [
        { cells: ['租赁费 · 2026-07', 'AR-2026-07-PRJ2602', '13%', '186,200.00'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-07-PRJ2602', url: '财务协同/应收账单.html' },
        { role: '开票登记（本单）', name: 'INV-20260826-011', self: true },
        { role: '回款登记', name: 'HK-20260828-013', url: '财务协同/回款登记.html' },
        { role: '银行水单核销', name: 'SD-20260828-010', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '07-31', text: '应收账单汇总 · AR-2026-07-PRJ2602', who: '系统' },
        { t: '08-26 15:10', text: '开票登记 · 发票号码 26119800420988', who: '财务-周敏' },
        { t: '—', text: '待回款 → 水单核销', off: true }
      ]
    },
    'INV-20260820-010': {
      'row': {"fields": {"no": "26119800419501", "itype": "专票", "buyer": "一汽解放汽车有限公司", "ref": "AR-2026-07-PRJ2601", "date": "2026-08-20", "status": "已登记"}, "cells": ["26119800419501", "<span class=\"tag tag-blue\">专票</span>", "一汽解放汽车有限公司", "AR-2026-07-PRJ2601", "<span class=\"td-num\"><b>256,600.00</b></span>", "13%", "2026-08-20", "<span class=\"tag tag-green\">已登记</span>"], "ops": [{"t": "开票确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "查看账单", "act": "go('../财务协同/应收账单.html')"}, {"t": "回款", "act": "go('../财务协同/回款登记.html')"}]},
      title: '开票登记详情',
      info: [
        { label: '登记单号', text: 'INV-20260820-010', full: true },
        { label: '状态', tag: '已登记' },
        { label: '开票日期', text: '2026-08-20' },
        { label: '发票号码', text: '26119800419501' },
        { label: '发票类型', text: '增值税专用发票' },
        { label: '购方', text: '一汽解放汽车有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-07-PRJ2601', url: '财务协同/应收账单.html' },
        { label: '价税合计', text: '256,600.00 元' },
        { label: '税率', text: '13%' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['费用项', '关联账单', '税率', '金额(元)'],
      fees: [
        { cells: ['租赁费 · 2026-07', 'AR-2026-07-PRJ2601', '13%', '256,600.00'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-07-PRJ2601', url: '财务协同/应收账单.html' },
        { role: '开票登记（本单）', name: 'INV-20260820-010', self: true },
        { role: '回款登记', name: 'HK-20260825-012', url: '财务协同/回款登记.html' },
        { role: '银行水单核销', name: 'SD-20260825-009 · 部分核销', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '07-31', text: '应收账单汇总 · AR-2026-07-PRJ2601', who: '系统' },
        { t: '08-20 11:25', text: '开票登记 · 发票号码 26119800419501', who: '财务-周敏' },
        { t: '—', text: '待回款 → 水单核销', off: true }
      ]
    },
    'INV-20260815-009': {
      'row': {"fields": {"no": "26119800418233", "itype": "普票", "buyer": "小鹏汽车科技有限公司", "ref": "AR-2026-07-PRJ2603", "date": "2026-08-15", "status": "已登记"}, "cells": ["26119800418233", "<span class=\"tag tag-gray\">普票</span>", "小鹏汽车科技有限公司", "AR-2026-07-PRJ2603", "<span class=\"td-num\"><b>98,000.00</b></span>", "13%", "2026-08-15", "<span class=\"tag tag-green\">已登记</span>"], "ops": [{"t": "开票确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "查看账单", "act": "go('../财务协同/应收账单.html')"}, {"t": "回款", "act": "go('../财务协同/回款登记.html')"}]},
      title: '开票登记详情',
      info: [
        { label: '登记单号', text: 'INV-20260815-009', full: true },
        { label: '状态', tag: '已登记' },
        { label: '开票日期', text: '2026-08-15' },
        { label: '发票号码', text: '26119800418233' },
        { label: '发票类型', text: '增值税普通发票' },
        { label: '购方', text: '小鹏汽车科技有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-07-PRJ2603', url: '财务协同/应收账单.html' },
        { label: '价税合计', text: '98,000.00 元' },
        { label: '税率', text: '13%' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['费用项', '关联账单', '税率', '金额(元)'],
      fees: [
        { cells: ['租赁费 · 2026-07', 'AR-2026-07-PRJ2603', '13%', '98,000.00'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-07-PRJ2603', url: '财务协同/应收账单.html' },
        { role: '开票登记（本单）', name: 'INV-20260815-009', self: true },
        { role: '回款登记', name: 'HK-20260822-011', url: '财务协同/回款登记.html' },
        { role: '银行水单核销', name: 'SD-20260822-008 · 已核销', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '07-31', text: '应收账单汇总 · AR-2026-07-PRJ2603', who: '系统' },
        { t: '08-15 10:05', text: '开票登记 · 发票号码 26119800418233', who: '财务-周敏' },
        { t: '08-28 10:05', text: '回款 65,320.00 已核销 · 余款待收', who: '李静' }
      ]
    },
    'INV-20260802-008': {
      'row': {"fields": {"no": "26119800417077", "itype": "专票", "buyer": "一汽解放汽车有限公司", "ref": "AR-2026-06-PRJ2601", "date": "2026-08-02", "status": "停用"}, "cells": ["26119800417077", "<span class=\"tag tag-blue\">专票</span>", "一汽解放汽车有限公司", "AR-2026-06-PRJ2601", "<span class=\"td-num\"><b>442,800.00</b></span>", "13%", "2026-08-02", "<span class=\"tag tag-gray\">停用</span>"], "ops": [{"t": "开票确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "查看账单", "act": "go('../财务协同/应收账单.html')"}, {"t": "回款", "act": "go('../财务协同/回款登记.html')"}]},
      title: '开票登记详情',
      info: [
        { label: '登记单号', text: 'INV-20260802-008', full: true },
        { label: '状态', tag: '停用' },
        { label: '开票日期', text: '2026-08-02' },
        { label: '发票号码', text: '26119800417077' },
        { label: '发票类型', text: '增值税专用发票' },
        { label: '购方', text: '一汽解放汽车有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-06-PRJ2601', url: '财务协同/应收账单.html' },
        { label: '价税合计', text: '442,800.00 元' },
        { label: '税率', text: '13%' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['费用项', '关联账单', '税率', '金额(元)'],
      fees: [
        { cells: ['租赁费 · 2026-06', 'AR-2026-06-PRJ2601', '13%', '442,800.00'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-06-PRJ2601', url: '财务协同/应收账单.html' },
        { role: '开票登记（本单）', name: 'INV-20260802-008 · 已停用', self: true },
        { role: '回款 / 核销', name: '已于 08 月核销结清', url: '财务协同/银行水单核销.html' }
      ],
      timeline: [
        { t: '06-30', text: '应收账单汇总 · AR-2026-06-PRJ2601', who: '系统' },
        { t: '08-02 09:50', text: '开票登记 · 发票号码 26119800417077', who: '财务-周敏' },
        { t: '08-22 09:30', text: '回款核销 358,900.00 元', who: '李静' },
        { t: '09-01 14:00', text: '登记停用 · 重复登记作废（保留痕迹）', who: '财务-周敏' }
      ]
    }
  },

  /* 水单核销记录（键 = HX 核销单号；弹窗按水单维度展示，titleNo = SD 水单号） */
  writeoffs: {
    'HX-20260830-012': {
      'row': {"fields": {"sd": "SD-20260825-009", "ref": "AR-2026-07-PRJ2601", "status": "部分核销", "time": "2026-08-30 14:22", "who": "李静"}, "cells": ["SD-20260825-009", "AR-2026-07-PRJ2601", "<span class=\"td-num\"><b>60,000.00</b></span>", "<span class=\"tag tag-blue\">部分核销</span>", "2026-08-30 14:22", "李静"], "ops": [{"t": "详情", "detail": true}, {"t": "撤销核销", "act": "openModal('undoModal')"}]},
      title: '水单核销详情', titleNo: 'SD-20260825-009',
      info: [
        { label: '水单号', text: 'SD-20260825-009', full: true },
        { label: '状态', tag: '部分核销' },
        { label: '到账日期', text: '2026-08-25' },
        { label: '付款方', text: '一汽解放汽车有限公司', full: true },
        { label: '到账金额', text: '98,000.00 元' },
        { label: '已核销', text: '60,000.00 元' },
        { label: '未核销', text: '38,000.00 元' },
        { label: '关联回款', text: 'HK-20260825-012', url: '财务协同/回款登记.html' },
        { label: '收款账户', text: '招行基本户 1209****8866' },
        { label: '经办', text: '李静' }
      ],
      feeCols: ['勾对', '应收账单', '账单金额(元)', '本次核销(元)'],
      fees: [
        { cells: ['☑', 'AR-2026-07-PRJ2601', '442,800.00', '60,000.00（部分核销）'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '回款登记', name: 'HK-20260825-012', url: '财务协同/回款登记.html' },
        { role: '水单核销（本单）', name: 'SD-20260825-009', self: true },
        { role: '应收账单', name: 'AR-2026-07-PRJ2601 · 核销冲抵', url: '财务协同/应收账单.html' }
      ],
      timeline: [
        { t: '08-25', text: '水单接收 · 与回款登记匹配', who: '系统' },
        { t: '08-30 14:22', text: '勾对核销 60,000.00 元 · 部分核销', who: '李静' },
        { t: '—', text: '余 38,000.00 待后续核销 / 可撤销核销', off: true }
      ]
    },
    'HX-20260828-011': {
      'row': {"fields": {"sd": "SD-20260822-008", "ref": "AR-2026-07-PRJ2603", "status": "已核销", "time": "2026-08-28 10:05", "who": "李静"}, "cells": ["SD-20260822-008", "AR-2026-07-PRJ2603", "<span class=\"td-num\"><b>65,320.00</b></span>", "<span class=\"tag tag-green\">已核销</span>", "2026-08-28 10:05", "李静"], "ops": [{"t": "详情", "detail": true}, {"t": "撤销核销", "act": "openModal('undoModal')"}]},
      title: '水单核销详情', titleNo: 'SD-20260822-008',
      info: [
        { label: '水单号', text: 'SD-20260822-008', full: true },
        { label: '状态', tag: '已核销' },
        { label: '到账日期', text: '2026-08-22' },
        { label: '付款方', text: '小鹏汽车科技有限公司', full: true },
        { label: '到账金额', text: '65,320.00 元' },
        { label: '已核销', text: '65,320.00 元' },
        { label: '未核销', text: '0.00 元' },
        { label: '关联回款', text: 'HK-20260822-011', url: '财务协同/回款登记.html' },
        { label: '收款账户', text: '工行一般户 0200****5533' },
        { label: '经办', text: '李静' }
      ],
      feeCols: ['勾对', '应收账单', '账单金额(元)', '本次核销(元)'],
      fees: [
        { cells: ['☑', 'AR-2026-07-PRJ2603', '241,500.00', '65,320.00（全额核销）'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '回款登记', name: 'HK-20260822-011', url: '财务协同/回款登记.html' },
        { role: '水单核销（本单）', name: 'SD-20260822-008', self: true },
        { role: '应收账单', name: 'AR-2026-07-PRJ2603 · 核销冲抵', url: '财务协同/应收账单.html' }
      ],
      timeline: [
        { t: '08-22', text: '水单接收 · 与回款登记匹配', who: '系统' },
        { t: '08-28 10:05', text: '勾对核销 65,320.00 元 · 全额核销', who: '李静' }
      ]
    },
    'HX-20260826-010': {
      'row': {"fields": {"sd": "SD-20260818-006", "ref": "BS-20260802-001", "status": "已核销", "time": "2026-08-26 16:40", "who": "李静"}, "cells": ["SD-20260818-006", "BS-20260802-001", "<span class=\"td-num\"><b>860.00</b></span>", "<span class=\"tag tag-green\">已核销</span>", "2026-08-26 16:40", "李静"], "ops": [{"t": "详情", "detail": true}, {"t": "撤销核销", "act": "openModal('undoModal')"}]},
      title: '水单核销详情', titleNo: 'SD-20260818-006',
      info: [
        { label: '水单号', text: 'SD-20260818-006', full: true },
        { label: '状态', tag: '已核销' },
        { label: '到账日期', text: '2026-08-18' },
        { label: '付款方', text: '一汽解放汽车有限公司', full: true },
        { label: '到账金额', text: '860.00 元' },
        { label: '已核销', text: '860.00 元' },
        { label: '未核销', text: '0.00 元' },
        { label: '关联回款', text: 'HK-20260818-010', url: '财务协同/回款登记.html' },
        { label: '收款账户', text: '招行基本户 1209****8866' },
        { label: '经办', text: '李静' }
      ],
      feeCols: ['勾对', '来源单据', '单据金额(元)', '本次核销(元)'],
      fees: [
        { cells: ['☑', 'BS-20260802-001（丢损赔偿）', '860.00', '860.00（全额核销）'] }
      ],
      chain: [
        { role: '回款登记', name: 'HK-20260818-010', url: '财务协同/回款登记.html' },
        { role: '水单核销（本单）', name: 'SD-20260818-006', self: true },
        { role: '丢损赔偿单', name: 'BS-20260802-001 · 核销冲抵' }
      ],
      timeline: [
        { t: '08-18', text: '水单接收 · 与回款登记匹配', who: '系统' },
        { t: '08-26 16:40', text: '勾对核销 860.00 元 · 全额核销', who: '李静' }
      ]
    },
    'HX-20260822-009': {
      'row': {"fields": {"sd": "SD-20260815-005", "ref": "AR-2026-06-PRJ2602", "status": "已核销", "time": "2026-08-22 09:30", "who": "李静"}, "cells": ["SD-20260815-005", "AR-2026-06-PRJ2602", "<span class=\"td-num\"><b>358,900.00</b></span>", "<span class=\"tag tag-green\">已核销</span>", "2026-08-22 09:30", "李静"], "ops": [{"t": "详情", "detail": true}, {"t": "撤销核销", "act": "openModal('undoModal')"}]},
      title: '水单核销详情', titleNo: 'SD-20260815-005',
      info: [
        { label: '水单号', text: 'SD-20260815-005', full: true },
        { label: '状态', tag: '已核销' },
        { label: '到账日期', text: '2026-08-15' },
        { label: '付款方', text: '上汽大众宁波分公司', full: true },
        { label: '到账金额', text: '358,900.00 元' },
        { label: '已核销', text: '358,900.00 元' },
        { label: '未核销', text: '0.00 元' },
        { label: '关联回款', text: '—' },
        { label: '收款账户', text: '建行一般户 3321****0417' },
        { label: '经办', text: '李静' }
      ],
      feeCols: ['勾对', '应收账单', '账单金额(元)', '本次核销(元)'],
      fees: [
        { cells: ['☑', 'AR-2026-06-PRJ2602', '358,900.00', '358,900.00（全额核销）'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '水单核销（本单）', name: 'SD-20260815-005', self: true },
        { role: '应收账单', name: 'AR-2026-06-PRJ2602 · 核销冲抵结清', url: '财务协同/应收账单.html' }
      ],
      timeline: [
        { t: '08-15', text: '水单接收 · 到账 358,900.00 元', who: '系统' },
        { t: '08-22 09:30', text: '勾对核销 358,900.00 元 · 全额核销结清', who: '李静' }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 租赁单 leaseOrders：键 = ZL 租赁单号（租赁管理/租赁单列表.html 9 行全量） */
  /* 租金标准 8.00 元/套/日为默认决策待确认；押金口径待客户 */
  leaseOrders: {
    'ZL-20260823-033': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "project": "PRJ-2604", "status": "已退租", "start": "2026-08-23"}, "note": "1", "cells": ["一汽解放汽车有限公司", "PRJ-2604", "ZH-2604-D 混合组合套件", "<span class=\"tag tag-orange\">混合（自购 + 租入-路凯）</span> <span class=\"lk\" onclick=\"go('../租赁管理/租入单列表.html')\">RZD-20260815-005</span>", "<span class=\"td-num\">40 套</span>", "2026-08-23", "<span class=\"td-num\">40/40 套</span>", "<span class=\"tag tag-green\">已退租</span>"], "ops": [{"t": "编辑", "act": "openModal('createModal')"}, {"t": "审核", "act": "openModal('auditModal')"}, {"t": "关闭"}]},
      'title': '租赁单详情',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260823-033',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已退租'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2604'
        },
        {
          'label': '数量',
          'text': '40 套'
        },
        {
          'label': '业务员',
          'text': '王琳'
        },
        {
          'label': '租赁内容',
          'text': 'ZH-2604-D 混合组合套件 × 40 套',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '混合（自购 + 租入-路凯  · RZD-20260815-005',
          'full': true,
          'url': '租赁管理/租入单列表.html'
        },
        {
          'label': '退回进度',
          'text': '40/40 套',
          'full': true
        },
        {
          'label': '计租天数',
          'text': '92 天'
        },
        {
          'label': '租金标准',
          'text': '8.00 元 / 套 / 日（默认决策待确认）',
          'full': true
        },
        {
          'label': '押金',
          'text': '—（商务口径待客户确认）',
          'full': true
        }
      ],
      'feeSecTitle': '租赁明细（未税为基准 · 含税自动换算 · 总价=逐行加总）',
      'feeCols': ['产品', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['ZH-2604-D 混合组合套件', '40', '8.00', '13%', '9.04', '361.60']
        },
        {
          'cells': ['合计', '—', '—', '—', '—', '361.60']
        }
      ],
      'chain': [
        {
          'role': '组装',
          'name': 'ZZ-20260822-006 · 混合配方',
        },
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260823-033',
          'self': true
        },
        {
          'role': '组合出库',
          'name': 'CK-20260824-009',
          'url': '租赁管理/组合出库列表.html'
        },
        {
          'role': '退租入库',
          'name': 'TZRK-20260902-010',
          'url': '租赁管理/退租入库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-22',
          'text': '组装完成 · ZZ-20260822-006（40 套待租）',
          'who': '刘志强'
        },
        {
          't': '08-23',
          'text': '起租 · 租赁单签订',
          'who': '王琳'
        },
        {
          't': '08-24',
          'text': '组合出库 · CK-20260824-009（40 套）',
          'who': '张伟'
        },
        {
          't': '09-02',
          'text': '客户退租 · TZRK-20260902-010（直接入库·提前退租）',
          'who': '客户提交'
        },
        {
          't': '09-02',
          'text': '退租入库 · TZRK-20260902-010（按 BOM 拆散分流）',
          'who': '张伟'
        }
      ]
    },
    'ZL-20260901-032': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "project": "PRJ-2601", "status": "待审核", "start": "2026-09-05"}, "cells": ["一汽解放汽车有限公司", "PRJ-2601", "ZH-2601-A 驾驶室围板箱整箱套件", "<span class=\"tag tag-gray\">自有</span>", "<span class=\"td-num\">180 套</span>", "2026-09-05", "<span class=\"td-num\">—</span>", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "编辑", "act": "openModal('createModal')"}, {"t": "审核", "act": "openModal('auditModal')"}, {"t": "关闭"}]},
      'title': '租赁单详情',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260901-032',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '数量',
          'text': '180 套'
        },
        {
          'label': '业务员',
          'text': '王琳'
        },
        {
          'label': '租赁内容',
          'text': 'ZH-2601-A 驾驶室围板箱整箱套件 × 180 套',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有',
          'full': true
        },
        {
          'label': '退回进度',
          'text': '—',
          'full': true
        },
        {
          'label': '计租天数',
          'text': '91 天'
        },
        {
          'label': '租金标准',
          'text': '8.00 元 / 套 / 日（默认决策待确认）',
          'full': true
        },
        {
          'label': '押金',
          'text': '—（商务口径待客户确认）',
          'full': true
        }
      ],
      'feeSecTitle': '租赁明细（未税为基准 · 含税自动换算 · 总价=逐行加总）',
      'feeCols': ['产品', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['ZH-2601-A 驾驶室围板箱整箱套件', '180', '8.00', '13%', '9.04', '1,627.20']
        },
        {
          'cells': ['合计', '—', '—', '—', '—', '1,627.20']
        }
      ],
      'chain': [
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260901-032 · 待审核',
          'self': true
        },
        {
          'role': '组合出库',
          'name': '审核通过后出库',
          'url': '租赁管理/组合出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-01',
          'text': '租赁单提交 · 待审核',
          'who': '王琳'
        },
        {
          't': '—',
          'text': '审核通过 → 组合出库 · 09-05 起租',
          'who': '系统',
          'off': true
        }
      ]
    },
    'ZL-20260828-031': {
      'row': {"fields": {"customer": "上汽大众汽车有限公司宁波分公司", "project": "PRJ-2602", "status": "已审核", "start": "2026-09-01"}, "note": "3", "cells": ["上汽大众汽车有限公司宁波分公司", "PRJ-2602", "ZH-2602-B 冲压件料箱组套", "<span class=\"tag tag-gray\">自有</span>", "<span class=\"td-num\">120 套</span>", "2026-09-01", "<span class=\"td-num\">0/120 套</span>", "<span class=\"tag tag-blue\">已审核</span>"], "ops": [{"t": "出库", "act": "go('../租赁管理/组合出库列表.html')"}, {"t": "详情", "detail": true}, {"t": "关闭"}]},
      'title': '租赁单详情',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260828-031',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已审核'
        },
        {
          'label': '客户',
          'text': '上汽大众汽车有限公司宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '数量',
          'text': '120 套'
        },
        {
          'label': '业务员',
          'text': '王琳'
        },
        {
          'label': '租赁内容',
          'text': 'ZH-2602-B 冲压件料箱组套 × 120 套',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有',
          'full': true
        },
        {
          'label': '退回进度',
          'text': '0/120 套',
          'full': true
        },
        {
          'label': '计租天数',
          'text': '90 天'
        },
        {
          'label': '租金标准',
          'text': '8.00 元 / 套 / 日（默认决策待确认）',
          'full': true
        },
        {
          'label': '押金',
          'text': '—（商务口径待客户确认）',
          'full': true
        }
      ],
      'feeSecTitle': '租赁明细（未税为基准 · 含税自动换算 · 总价=逐行加总）',
      'feeCols': ['产品', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['ZH-2602-B 冲压件料箱组套', '120', '8.00', '13%', '9.04', '1,084.80']
        },
        {
          'cells': ['合计', '—', '—', '—', '—', '1,084.80']
        }
      ],
      'chain': [
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260828-031 · 已审核',
          'self': true
        },
        {
          'role': '组合出库',
          'name': 'CK-20260830-014 · 拣货中',
          'url': '租赁管理/组合出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-28',
          'text': '租赁单签订',
          'who': '王琳'
        },
        {
          't': '08-29',
          'text': '审核通过',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '拣货中 · CK-20260830-014 出库确认后起租',
          'who': '张伟',
          'off': true
        }
      ]
    },
    'ZL-20260816-029': {
      'row': {"fields": {"customer": "上汽大众汽车有限公司宁波分公司", "project": "PRJ-2603", "status": "已退租", "start": "2026-08-16"}, "note": "2", "cells": ["上汽大众汽车有限公司宁波分公司", "PRJ-2603", "WBX-1210L 围板箱 1200×1000×970", "<span class=\"tag tag-orange\">租入-路凯</span> <span class=\"lk\" onclick=\"go('../租赁管理/租入单列表.html')\">RZD-20260815-003</span>", "<span class=\"td-num\">30 只</span>", "2026-08-16", "<span class=\"td-num\">30/30 只</span>", "<span class=\"tag tag-green\">已退租</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "退租入库", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '租赁单详情',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260816-029',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已退租'
        },
        {
          'label': '客户',
          'text': '上汽大众汽车有限公司宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2603'
        },
        {
          'label': '数量',
          'text': '30 只'
        },
        {
          'label': '业务员',
          'text': '王琳'
        },
        {
          'label': '租赁内容',
          'text': 'WBX-1210L 围板箱 1200×1000×970 × 30 只',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '租入-路凯  · RZD-20260815-003',
          'full': true,
          'url': '租赁管理/租入单列表.html'
        },
        {
          'label': '退回进度',
          'text': '30/30 只',
          'full': true
        },
        {
          'label': '计租天数',
          'text': '92 天'
        },
        {
          'label': '租金标准',
          'text': '8.00 元 / 套 / 日（默认决策待确认）',
          'full': true
        },
        {
          'label': '押金',
          'text': '—（商务口径待客户确认）',
          'full': true
        }
      ],
      'feeSecTitle': '租赁明细（未税为基准 · 含税自动换算 · 总价=逐行加总）',
      'feeCols': ['产品', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['WBX-1210L 围板箱 1200×1000×970', '30', '8.00', '13%', '9.04', '271.20']
        },
        {
          'cells': ['合计', '—', '—', '—', '—', '271.20']
        }
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260815-003',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260816-029',
          'self': true
        },
        {
          'role': '退租入库',
          'name': 'TZRK-20260903-009',
          'url': '租赁管理/退租入库列表.html'
        },
        {
          'role': '租入归还',
          'name': 'GHCK-20260903-001',
          'url': '租赁管理/租入归还列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-15',
          'text': '租入单签订 · RZD-20260815-003 计租开始',
          'who': '王志远'
        },
        {
          't': '08-16',
          'text': '转租客户 · 起租',
          'who': '王琳'
        },
        {
          't': '09-03',
          'text': '客户退租 · TZRK-20260903-009（直接入库·整箱退回）',
          'who': '客户提交'
        },
        {
          't': '09-03',
          'text': '退租入库 · TZRK-20260903-009 · 租入件转归还',
          'who': '张伟'
        },
        {
          't': '09-03',
          'text': '整退归还路凯 · GHCK-20260903-001',
          'who': '李国栋'
        }
      ]
    },
    'ZL-20260815-028': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "project": "PRJ-2601", "status": "在租", "start": "2026-08-20"}, "note": "5", "cells": ["一汽解放汽车有限公司", "PRJ-2601", "WBX-1210L 围板箱 1200×1000×970", "<span class=\"tag tag-orange\">租入-路凯</span> <span class=\"lk\" onclick=\"go('../租赁管理/租入单列表.html')\">RZD-20260815-003</span>", "<span class=\"td-num\">300 只</span>", "2026-08-20", "<span class=\"td-num\">0/300 只</span>", "<span class=\"tag tag-blue\">在租</span>"], "ops": [{"t": "出库", "act": "go('../租赁管理/组合出库列表.html')"}, {"t": "详情", "detail": true}, {"t": "退租入库", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '租赁单详情',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260815-028',
          'full': true
        },
        {
          'label': '状态',
          'tag': '在租'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '数量',
          'text': '300 只'
        },
        {
          'label': '业务员',
          'text': '王琳'
        },
        {
          'label': '租赁内容',
          'text': 'WBX-1210L 围板箱 1200×1000×970 × 300 只',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '租入-路凯  · RZD-20260815-003',
          'full': true,
          'url': '租赁管理/租入单列表.html'
        },
        {
          'label': '退回进度',
          'text': '0/300 只',
          'full': true
        },
        {
          'label': '计租天数',
          'text': '92 天'
        },
        {
          'label': '租金标准',
          'text': '8.00 元 / 套 / 日（默认决策待确认）',
          'full': true
        },
        {
          'label': '押金',
          'text': '—（商务口径待客户确认）',
          'full': true
        }
      ],
      'feeSecTitle': '租赁明细（未税为基准 · 含税自动换算 · 总价=逐行加总）',
      'feeCols': ['产品', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['WBX-1210L 围板箱 1200×1000×970', '300', '8.00', '13%', '9.04', '2,712.00']
        },
        {
          'cells': ['合计', '—', '—', '—', '—', '2,712.00']
        }
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260815-003',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260815-028',
          'self': true
        },
        {
          'role': '组合出库',
          'name': 'CK-20260828-010',
          'url': '租赁管理/组合出库列表.html'
        },
        {
          'role': '库存查询·客户在租',
          'name': '客户占用 · 租赁费应收',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-15',
          'text': '租入单签订 · RZD-20260815-003',
          'who': '王志远'
        },
        {
          't': '08-20',
          'text': '起租 · 租赁单签订',
          'who': '王琳'
        },
        {
          't': '08-28',
          'text': '组合出库 · CK-20260828-010（200 套）',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '在租中 · 退租后回库循环再出租',
          'who': '系统',
          'off': true
        }
      ]
    },
    'ZL-20260720-022': {
      'row': {"fields": {"customer": "小鹏汽车科技有限公司", "project": "PRJ-2603", "status": "在租", "start": "2026-07-25"}, "cells": ["小鹏汽车科技有限公司", "PRJ-2603", "ZH-2603-C 电池托盘护角套件", "<span class=\"tag tag-gray\">自有</span>", "<span class=\"td-num\">60 套</span>", "2026-07-25", "<span class=\"td-num\">20/60 套</span>", "<span class=\"tag tag-blue\">在租</span>"], "ops": [{"t": "出库", "act": "go('../租赁管理/组合出库列表.html')"}, {"t": "详情", "detail": true}, {"t": "退租入库", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '租赁单详情',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260720-022',
          'full': true
        },
        {
          'label': '状态',
          'tag': '在租'
        },
        {
          'label': '客户',
          'text': '小鹏汽车科技有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2603'
        },
        {
          'label': '数量',
          'text': '60 套'
        },
        {
          'label': '业务员',
          'text': '王琳'
        },
        {
          'label': '租赁内容',
          'text': 'ZH-2603-C 电池托盘护角套件 × 60 套',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有',
          'full': true
        },
        {
          'label': '退回进度',
          'text': '20/60 套',
          'full': true
        },
        {
          'label': '计租天数',
          'text': '92 天'
        },
        {
          'label': '租金标准',
          'text': '8.00 元 / 套 / 日（默认决策待确认）',
          'full': true
        },
        {
          'label': '押金',
          'text': '—（商务口径待客户确认）',
          'full': true
        }
      ],
      'feeSecTitle': '租赁明细（未税为基准 · 含税自动换算 · 总价=逐行加总）',
      'feeCols': ['产品', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['ZH-2603-C 电池托盘护角套件', '60', '8.00', '13%', '9.04', '542.40']
        },
        {
          'cells': ['合计', '—', '—', '—', '—', '542.40']
        }
      ],
      'chain': [
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260720-022',
          'self': true
        },
        {
          'role': '退租入库',
          'name': 'TZRK-20260831-006 · 退 20 套',
          'url': '租赁管理/退租入库列表.html'
        }
      ],
      'timeline': [
        {
          't': '07-25',
          'text': '起租 · 租赁单签订',
          'who': '王琳'
        },
        {
          't': '08-29',
          'text': '客户退租 · TZRK-20260831-006（直接入库·退 20 套，部分退租）',
          'who': '客户提交'
        },
        {
          't': '—',
          'text': '在租中 · 余量继续计租',
          'who': '系统',
          'off': true
        }
      ]
    },
    'ZL-20260610-015': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "project": "PRJ-2601", "status": "在租", "start": "2026-06-15"}, "cells": ["一汽解放汽车有限公司", "PRJ-2601", "BTC-6040 料箱 600×400×340", "<span class=\"tag tag-gray\">自有</span>", "<span class=\"td-num\">500 只</span>", "2026-06-15", "<span class=\"td-num\">0/500 只</span>", "<span class=\"tag tag-blue\">在租</span>"], "ops": [{"t": "出库", "act": "go('../租赁管理/组合出库列表.html')"}, {"t": "详情", "detail": true}, {"t": "退租入库", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '租赁单详情',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260610-015',
          'full': true
        },
        {
          'label': '状态',
          'tag': '在租'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '数量',
          'text': '500 只'
        },
        {
          'label': '业务员',
          'text': '王琳'
        },
        {
          'label': '租赁内容',
          'text': 'BTC-6040 料箱 600×400×340 × 500 只',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有',
          'full': true
        },
        {
          'label': '退回进度',
          'text': '0/500 只',
          'full': true
        },
        {
          'label': '计租天数',
          'text': '92 天'
        },
        {
          'label': '租金标准',
          'text': '8.00 元 / 套 / 日（默认决策待确认）',
          'full': true
        },
        {
          'label': '押金',
          'text': '—（商务口径待客户确认）',
          'full': true
        }
      ],
      'feeSecTitle': '租赁明细（未税为基准 · 含税自动换算 · 总价=逐行加总）',
      'feeCols': ['产品', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['BTC-6040 料箱 600×400×340', '500', '8.00', '13%', '9.04', '4,520.00']
        },
        {
          'cells': ['合计', '—', '—', '—', '—', '4,520.00']
        }
      ],
      'chain': [
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260610-015',
          'self': true
        },
        {
          'role': '组合出库',
          'name': 'CK-20260830-015（180 套）',
          'url': '租赁管理/组合出库列表.html'
        },
        {
          'role': '退租入库',
          'name': 'TZRK-20260828-005 · 退 200 只',
          'url': '租赁管理/退租入库列表.html'
        }
      ],
      'timeline': [
        {
          't': '06-15',
          'text': '起租 · 租赁单签订',
          'who': '王琳'
        },
        {
          't': '08-26',
          'text': '客户退租 · TZRK-20260828-005（直接入库·退 200 只，部分退租）',
          'who': '客户提交'
        },
        {
          't': '08-28',
          'text': '退租入库 · TZRK-20260828-005（散件直接入库）',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '在租中 · 余量继续计租',
          'who': '系统',
          'off': true
        }
      ]
    },
    'ZL-20260301-006': {
      'row': {"fields": {"customer": "上汽大众汽车有限公司宁波分公司", "project": "PRJ-2602", "status": "已退租", "start": "2026-03-05"}, "note": "4", "cells": ["上汽大众汽车有限公司宁波分公司", "PRJ-2602", "PLT-1210P 塑料托盘 1200×1000", "<span class=\"tag tag-gray\">自有（单一器具直接出租）</span>", "<span class=\"td-num\">400 块</span>", "2026-03-05", "<span class=\"td-num\">400/400 块</span>", "<span class=\"tag tag-green\">已退租</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '租赁单详情',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260301-006',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已退租'
        },
        {
          'label': '客户',
          'text': '上汽大众汽车有限公司宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '数量',
          'text': '400 块'
        },
        {
          'label': '业务员',
          'text': '王琳'
        },
        {
          'label': '租赁内容',
          'text': 'PLT-1210P 塑料托盘 1200×1000 × 400 块',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有（单一器具直接出租）',
          'full': true
        },
        {
          'label': '退回进度',
          'text': '400/400 块',
          'full': true
        },
        {
          'label': '计租天数',
          'text': '92 天'
        },
        {
          'label': '租金标准',
          'text': '8.00 元 / 套 / 日（默认决策待确认）',
          'full': true
        },
        {
          'label': '押金',
          'text': '—（商务口径待客户确认）',
          'full': true
        }
      ],
      'feeSecTitle': '租赁明细（未税为基准 · 含税自动换算 · 总价=逐行加总）',
      'feeCols': ['产品', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['PLT-1210P 塑料托盘 1200×1000', '400', '8.00', '13%', '9.04', '3,616.00']
        },
        {
          'cells': ['合计', '—', '—', '—', '—', '3,616.00']
        }
      ],
      'chain': [
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260301-006',
          'self': true
        },
        {
          'role': '退租入库',
          'name': 'TZRK-20260825-004',
          'url': '租赁管理/退租入库列表.html'
        },
        {
          'role': '退租入库',
          'name': 'TZRK-20260825-004',
          'url': '租赁管理/退租入库列表.html'
        }
      ],
      'timeline': [
        {
          't': '03-05',
          'text': '起租 · 租赁单签订（单一器具直接出租）',
          'who': '王琳'
        },
        {
          't': '08-23',
          'text': '客户退租 · TZRK-20260825-004（直接入库）',
          'who': '客户提交'
        },
        {
          't': '08-25',
          'text': '退租入库 · TZRK-20260825-004（散件直接入库）',
          'who': '张伟'
        }
      ]
    },
    'ZL-20260115-002': {
      'row': {"fields": {"customer": "东风本田汽车有限公司", "project": "PRJ-2604", "status": "已关闭", "start": "2026-01-20"}, "cells": ["东风本田汽车有限公司", "PRJ-2604", "WBX-1210M 围板箱 1200×1000×590", "<span class=\"tag tag-gray\">自有</span>", "<span class=\"td-num\">150 只</span>", "2026-01-20", "<span class=\"td-num\">150/150 只</span>", "<span class=\"tag tag-gray\">已关闭</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '租赁单详情',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260115-002',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已关闭'
        },
        {
          'label': '客户',
          'text': '东风本田汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2604'
        },
        {
          'label': '数量',
          'text': '150 只'
        },
        {
          'label': '业务员',
          'text': '王琳'
        },
        {
          'label': '租赁内容',
          'text': 'WBX-1210M 围板箱 1200×1000×590 × 150 只',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有',
          'full': true
        },
        {
          'label': '退回进度',
          'text': '150/150 只',
          'full': true
        },
        {
          'label': '计租天数',
          'text': '90 天'
        },
        {
          'label': '租金标准',
          'text': '8.00 元 / 套 / 日（默认决策待确认）',
          'full': true
        },
        {
          'label': '押金',
          'text': '—（商务口径待客户确认）',
          'full': true
        }
      ],
      'feeSecTitle': '租赁明细（未税为基准 · 含税自动换算 · 总价=逐行加总）',
      'feeCols': ['产品', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['WBX-1210M 围板箱 1200×1000×590', '150', '8.00', '13%', '9.04', '1,356.00']
        },
        {
          'cells': ['合计', '—', '—', '—', '—', '1,356.00']
        }
      ],
      'chain': [
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260115-002 · 已关闭',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '01-20',
          'text': '租赁单签订',
          'who': '王琳'
        },
        {
          't': '02-02',
          'text': '单据关闭（客户取消）',
          'who': '王琳'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 租入单 rentInOrders：键 = RZD 租入单号（租赁管理/租入单列表.html 5 行全量） */
  /* 租金条款按月生成应付，已建应付实体单号贯通 */
  rentInOrders: {
    'RZD-20260815-003': {
      'row': {"fields": {"operator": "路凯包装运营（上海）有限公司", "appliance": "围板箱 1200×1000×970", "period": "2026-08-15 ~ 2027-08-14", "status": "履行中", "agent": "王志远", "date": "2026-08-15"}, "note": "1", "cells": ["路凯包装运营（上海）有限公司", "围板箱 1200×1000×970", "30 只", "400.00", "2026-08-15 ~ 2027-08-14", "36,000.00", "84,000.00", "<span class=\"tag tag-blue\">履行中</span>", "王志远", "2026-08-15 10:22"], "ops": [{"t": "详情", "detail": true}, {"t": "生成租金应付", "act": "go('../财务协同/应付账单.html')"}, {"t": "发起归还", "act": "go('../租赁管理/租入归还列表.html')"}]},
      'title': '租入单详情',
      'info': [
        {
          'label': '租入单号',
          'text': 'RZD-20260815-003',
          'full': true
        },
        {
          'label': '状态',
          'tag': '履行中'
        },
        {
          'label': '供应商',
          'text': '路凯包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '器具',
          'text': '围板箱 1200×1000×970',
          'full': true
        },
        {
          'label': '数量',
          'text': '30 只'
        },
        {
          'label': '日租金',
          'text': '400.00 元 / 日（按单）',
          'full': true
        },
        {
          'label': '租期',
          'text': '2026-08-15 ~ 2027-08-14',
          'full': true
        },
        {
          'label': '押金',
          'text': '84,000.00 元（商务口径待确认）',
          'full': true
        },
        {
          'label': '经办人',
          'text': '王志远'
        },
        {
          'label': '创建时间',
          'text': '2026-08-15 10:22'
        },
        {
          'label': '已生成租金应付',
          'text': 'AP-20260903-009 · 36,000.00 元',
          'url': '财务协同/应付账单.html',
          'full': true
        }
      ],
      'feeSecTitle': '租入明细（多货品 · 月租/按套 · 无日租金）',
      'feeCols': ['产品', '数量', '计费方式', '未税单价(元)', '税率', '含税单价(元)', '首期应付(元)'],
      'fees': [
        {
          'cells': ['WBX-1210L 围板箱 1200×1000×970（租入）', '30 只', '月租', '400.00', '13%', '452.00', '36,000.00']
        }
      ],
      'chain': [
        {
          'role': '租入单（本单）',
          'name': 'RZD-20260815-003',
          'self': true
        },
        {
          'role': '租入入库',
          'name': 'RZRK-20260816-021',
          'url': '租赁管理/租入入库列表.html'
        },
        {
          'role': '租赁单（转租）',
          'name': 'ZL-20260816-029',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '租入归还',
          'name': 'GHCK-20260903-001',
          'url': '租赁管理/租入归还列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-15',
          'text': '签订租入单 · 计租开始',
          'who': '王志远'
        },
        {
          't': '08-16',
          'text': '租入入库 · RZRK-20260816-021（30 只）',
          'who': '李国栋'
        },
        {
          't': '08-16',
          'text': '转租客户 · ZL-20260816-029',
          'who': '王琳'
        },
        {
          't': '09-03',
          'text': '整退归还 · GHCK-20260903-001',
          'who': '李国栋'
        },
        {
          't': '09-03',
          'text': '生成租金应付 · AP-20260903-009（36,000 元）',
          'who': '系统'
        }
      ]
    },
    'RZD-20260815-005': {
      'row': {"fields": {"operator": "路凯包装运营（上海）有限公司", "appliance": "围板箱 1200×1000×970", "period": "2026-08-15 ~ 2027-08-14", "status": "部分归还", "agent": "王志远", "date": "2026-08-15"}, "note": "2", "cells": ["路凯包装运营（上海）有限公司", "围板箱 1200×1000×970", "10 只", "400.00", "2026-08-15 ~ 2027-08-14", "12,000.00", "12,000.00", "<span class=\"tag tag-orange\">部分归还</span>", "王志远", "2026-08-15 11:05"], "ops": [{"t": "详情", "detail": true}, {"t": "生成租金应付", "act": "go('../财务协同/应付账单.html')"}, {"t": "发起归还", "act": "go('../租赁管理/租入归还列表.html')"}]},
      'title': '租入单详情',
      'info': [
        {
          'label': '租入单号',
          'text': 'RZD-20260815-005',
          'full': true
        },
        {
          'label': '状态',
          'tag': '部分归还'
        },
        {
          'label': '供应商',
          'text': '路凯包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '器具',
          'text': '围板箱 1200×1000×970',
          'full': true
        },
        {
          'label': '数量',
          'text': '10 只'
        },
        {
          'label': '日租金',
          'text': '400.00 元 / 日（按单）',
          'full': true
        },
        {
          'label': '租期',
          'text': '2026-08-15 ~ 2027-08-14',
          'full': true
        },
        {
          'label': '押金',
          'text': '12,000.00 元（商务口径待确认）',
          'full': true
        },
        {
          'label': '经办人',
          'text': '王志远'
        },
        {
          'label': '创建时间',
          'text': '2026-08-15 11:05'
        },
        {
          'label': '已生成租金应付',
          'text': 'AP-20260903-010 · 12,000.00 元',
          'url': '财务协同/应付账单.html',
          'full': true
        }
      ],
      'feeSecTitle': '租入明细（多货品 · 月租/按套 · 无日租金）',
      'feeCols': ['产品', '数量', '计费方式', '未税单价(元)', '税率', '含税单价(元)', '首期应付(元)'],
      'fees': [
        {
          'cells': ['WBX-1210L 围板箱 1200×1000×970（租入）', '10 只', '月租', '400.00', '13%', '452.00', '12,000.00']
        }
      ],
      'chain': [
        {
          'role': '租入单（本单）',
          'name': 'RZD-20260815-005',
          'self': true
        },
        {
          'role': '租入入库',
          'name': 'RZRK-20260816-022',
          'url': '租赁管理/租入入库列表.html'
        },
        {
          'role': '组装（混合配方）',
          'name': 'ZZ-20260822-006',
        },
        {
          'role': '租入归还（分流）',
          'name': 'GHCK-20260903-002 · 4 只缺损',
          'url': '租赁管理/租入归还列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-15',
          'text': '签订租入单 · 计租开始',
          'who': '王志远'
        },
        {
          't': '08-16',
          'text': '租入入库 · RZRK-20260816-022（10 只）',
          'who': '李国栋'
        },
        {
          't': '08-22',
          'text': '混合组装 · ZZ-20260822-006（ZH-2604-D）',
          'who': '刘志强'
        },
        {
          't': '09-03',
          'text': '分流归还 · GHCK-20260903-002（10 只中 4 只缺损赔付）',
          'who': '李国栋'
        },
        {
          't': '09-03',
          'text': '生成租金应付 · AP-20260903-010（12,000 元）',
          'who': '系统'
        }
      ]
    },
    'RZD-20260902-008': {
      'row': {"fields": {"operator": "路凯包装运营（上海）有限公司", "appliance": "塑料托盘 1200×1000", "period": "2026-09-02 ~ 2026-12-31", "status": "待审核", "agent": "陈金", "date": "2026-09-02"}, "cells": ["路凯包装运营（上海）有限公司", "塑料托盘 1200×1000", "50 只", "1.20", "2026-09-02 ~ 2026-12-31", "5,000.00", "—", "<span class=\"tag tag-orange\">待审核</span>", "陈金", "2026-09-02 16:40"], "ops": [{"t": "详情", "detail": true}, {"t": "审核", "act": "openModal('auditModal')"}]},
      'title': '租入单详情',
      'info': [
        {
          'label': '租入单号',
          'text': 'RZD-20260902-008',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '供应商',
          'text': '路凯包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '器具',
          'text': '塑料托盘 1200×1000',
          'full': true
        },
        {
          'label': '数量',
          'text': '50 只'
        },
        {
          'label': '日租金',
          'text': '1.20 元 / 日（按单）',
          'full': true
        },
        {
          'label': '租期',
          'text': '2026-09-02 ~ 2026-12-31',
          'full': true
        },
        {
          'label': '押金',
          'text': '—',
          'full': true
        },
        {
          'label': '经办人',
          'text': '陈金'
        },
        {
          'label': '创建时间',
          'text': '2026-09-02 16:40'
        },
        {
          'label': '已生成租金应付',
          'text': '—',
          'full': true
        }
      ],
      'feeSecTitle': '租入明细（多货品 · 月租/按套 · 无日租金）',
      'feeCols': ['产品', '数量', '计费方式', '未税单价(元)', '税率', '含税单价(元)', '首期应付(元)'],
      'fees': [
        {
          'cells': ['WBX-1210L 围板箱 1200×1000×970（租入）', '30 只', '月租', '1210', '13%', '1367.30', '5,000.00']
        }
      ],
      'chain': [
        {
          'role': '租入单（本单）',
          'name': 'RZD-20260902-008 · 待审核',
          'self': true
        },
        {
          'role': '租入入库',
          'name': 'RZRK-20260903-023 · 待入库',
          'url': '租赁管理/租入入库列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-02',
          'text': '租入单提交 · 待审核',
          'who': '陈金'
        },
        {
          't': '—',
          'text': '审核通过 → 租入入库 · 按月生成租金应付',
          'who': '系统',
          'off': true
        }
      ]
    },
    'RZD-20260701-001': {
      'row': {"fields": {"operator": "路凯包装运营（上海）有限公司", "appliance": "金属料箱 800×600", "period": "2026-07-01 ~ 2026-08-31", "status": "已归还", "agent": "王志远", "date": "2026-07-01"}, "cells": ["路凯包装运营（上海）有限公司", "金属料箱 800×600", "20 只", "3.00", "2026-07-01 ~ 2026-08-31", "—", "10,800.00", "<span class=\"tag tag-green\">已归还</span>", "王志远", "2026-07-01 09:30"], "ops": [{"t": "详情", "detail": true}, {"t": "归还记录", "act": "go('../租赁管理/租入归还列表.html')"}]},
      'title': '租入单详情',
      'info': [
        {
          'label': '租入单号',
          'text': 'RZD-20260701-001',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已归还'
        },
        {
          'label': '供应商',
          'text': '路凯包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '器具',
          'text': '金属料箱 800×600',
          'full': true
        },
        {
          'label': '数量',
          'text': '20 只'
        },
        {
          'label': '日租金',
          'text': '3.00 元 / 日（按单）',
          'full': true
        },
        {
          'label': '租期',
          'text': '2026-07-01 ~ 2026-08-31',
          'full': true
        },
        {
          'label': '押金',
          'text': '10,800.00 元（商务口径待确认）',
          'full': true
        },
        {
          'label': '经办人',
          'text': '王志远'
        },
        {
          'label': '创建时间',
          'text': '2026-07-01 09:30'
        },
        {
          'label': '已生成租金应付',
          'text': '—',
          'full': true
        }
      ],
      'feeSecTitle': '租入明细（多货品 · 月租/按套 · 无日租金）',
      'feeCols': ['产品', '数量', '计费方式', '未税单价(元)', '税率', '含税单价(元)', '首期应付(元)'],
      'fees': [
        {
          'cells': ['WBX-1210L 围板箱 1200×1000×970（租入）', '20 只', '月租', '3.00', '13%', '3.39', '36,000.00']
        }
      ],
      'chain': [
        {
          'role': '租入单（本单）',
          'name': 'RZD-20260701-001',
          'self': true
        },
        {
          'role': '租入归还',
          'name': 'GHCK-20260831-003 · 整退归还',
          'url': '租赁管理/租入归还列表.html'
        }
      ],
      'timeline': [
        {
          't': '07-01',
          'text': '签订租入单 · 计租开始',
          'who': '王志远'
        },
        {
          't': '08-31',
          'text': '整退归还 · GHCK-20260831-003（20 只）',
          'who': '王志远'
        },
        {
          't': '08-31',
          'text': '租金结清 · 单据完结',
          'who': '系统'
        }
      ]
    },
    'RZD-20260615-002': {
      'row': {"fields": {"operator": "路凯包装运营（上海）有限公司", "appliance": "塑料围板箱 800×600", "period": "2026-06-15 ~ 2026-08-14", "status": "已终止", "agent": "王志远", "date": "2026-06-15"}, "cells": ["路凯包装运营（上海）有限公司", "塑料围板箱 800×600", "15 只", "2.50", "2026-06-15 ~ 2026-08-14", "—", "4,500.00", "<span class=\"tag tag-gray\">已终止</span>", "王志远", "2026-06-15 14:12"], "ops": [{"t": "详情", "detail": true}]},
      'title': '租入单详情',
      'info': [
        {
          'label': '租入单号',
          'text': 'RZD-20260615-002',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已终止'
        },
        {
          'label': '供应商',
          'text': '路凯包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '器具',
          'text': '塑料围板箱 800×600',
          'full': true
        },
        {
          'label': '数量',
          'text': '15 只'
        },
        {
          'label': '日租金',
          'text': '2.50 元 / 日（按单）',
          'full': true
        },
        {
          'label': '租期',
          'text': '2026-06-15 ~ 2026-08-14',
          'full': true
        },
        {
          'label': '押金',
          'text': '4,500.00 元（商务口径待确认）',
          'full': true
        },
        {
          'label': '经办人',
          'text': '王志远'
        },
        {
          'label': '创建时间',
          'text': '2026-06-15 14:12'
        },
        {
          'label': '已生成租金应付',
          'text': '—',
          'full': true
        }
      ],
      'feeSecTitle': '租入明细（多货品 · 月租/按套 · 无日租金）',
      'feeCols': ['产品', '数量', '计费方式', '未税单价(元)', '税率', '含税单价(元)', '首期应付(元)'],
      'fees': [
        {
          'cells': ['WBX-1210L 围板箱 1200×1000×970（租入）', '15 只', '月租', '2.50', '13%', '2.82', '36,000.00']
        }
      ],
      'chain': [
        {
          'role': '租入单（本单）',
          'name': 'RZD-20260615-002 · 已终止',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '06-15',
          'text': '签订租入单 · 计租开始',
          'who': '王志远'
        },
        {
          't': '07-20',
          'text': '提前终止 · 按违约条款结算',
          'who': '王志远'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 组合出库单 comboOutbounds：键 = CK 出库单号（租赁管理/组合出库列表.html 8 行全量） */
  /* 关联租赁单/销售订单双关联；租入件无 SO 用 —（租赁出库） */
  comboOutbounds: {
    'CK-20260903-016': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "zl": "ZL-20260903-034", "combo": "ZH-2601-A × 60 套（退租回库件循环出库）", "so": "—（租赁出库）", "addr": "长春基地一号门", "status": "已出库", "date": "2026-09-03"}, "cells": ["PRJ-2601", "一汽解放汽车有限公司", "<span class=\"lk\">ZL-20260903-034</span>", "ZH-2601-A × 60 套（退租回库件循环出库）", "—（租赁出库）", "长春基地一号门", "<span class=\"tag tag-green\">已出库</span>", "2026-09-03 09:15"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}, {"t": "出库确认", "act": "openModal('exitConfirmModal')"}]},
      'title': '组合出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'CK-20260903-016',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已出库'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260903-034',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '关联销售订单',
          'text': '—（租赁出库）',
          'full': true
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '出库内容',
          'text': 'ZH-2601-A × 60 套(退租回库件循环出库)',
          'full': true
        },
        {
          'label': '出库库区',
          'text': '成品区 RB'
        },
        {
          'label': '送达地点',
          'text': '长春基地一号门'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '出库时间',
          'text': '2026-09-03 09:15'
        },
        {
          'label': '出库方式',
          'text': '一箱一件 · 逐件核对（扫码口预留）',
          'full': true
        }
      ],
      'feeSecTitle': '器具 / 组合件清单',
      'feeCols': ['序号', '组合件编码', '名称', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'ZH-2601-A', '驾驶室围板箱整箱套件', '套', '60', '1.00', '13%', '1.13', '67.80', 'RB-A-01-01']
        }
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260903-034',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '组合出库（本单）',
          'name': 'CK-20260903-016',
          'self': true
        },
        {
          'role': '库存查询·客户在租 / 应收',
          'name': '客户占用起租 · 租赁费应收',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-30 14:25',
          'text': '拣货备货 · 成品区 RB（ZH-2601-A 60 套）',
          'who': '张伟'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 长春基地一号门',
          'who': '张伟'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张伟'
        }
      ]
    },
    'CK-20260830-015': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "zl": "ZL-20260610-015", "combo": "ZH-2601-A × 180 套", "so": "SO-20260830-0041", "addr": "长春基地一号门", "status": "已出库", "date": "2026-08-30"}, "note": "2", "cells": ["PRJ-2601", "一汽解放汽车有限公司", "<span class=\"lk\">ZL-20260610-015</span>", "ZH-2601-A × 180 套", "SO-20260830-0041", "长春基地一号门", "<span class=\"tag tag-green\">已出库</span>", "2026-08-30 17:20"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}, {"t": "出库确认", "act": "openModal('exitConfirmModal')"}]},
      'title': '组合出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'CK-20260830-015',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已出库'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260610-015',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '关联销售订单',
          'text': 'SO-20260830-0041（双关联）',
          'url': '销售管理/销售订单列表.html',
          'full': true
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '出库内容',
          'text': 'ZH-2601-A × 180 套',
          'full': true
        },
        {
          'label': '出库库区',
          'text': '成品区 RB'
        },
        {
          'label': '送达地点',
          'text': '长春基地一号门'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '出库时间',
          'text': '2026-08-30 17:20'
        },
        {
          'label': '出库方式',
          'text': '一箱一件 · 逐件核对（扫码口预留）',
          'full': true
        }
      ],
      'feeSecTitle': '器具 / 组合件清单',
      'feeCols': ['序号', '组合件编码', '名称', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'ZH-2601-A', '驾驶室围板箱整箱套件', '套', '180', '1.00', '13%', '1.13', '203.40', 'RB-A-01-01']
        }
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260610-015',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '销售订单（双关联）',
          'name': 'SO-20260830-0041',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '组合出库（本单）',
          'name': 'CK-20260830-015',
          'self': true
        },
        {
          'role': '库存查询·客户在租 / 应收',
          'name': '客户占用起租 · 租赁费应收',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-30 14:25',
          'text': '拣货备货 · 成品区 RB（ZH-2601-A 180 套）',
          'who': '张伟'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 长春基地一号门',
          'who': '张伟'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张伟'
        }
      ]
    },
    'CK-20260830-014': {
      'row': {"fields": {"project": "PRJ-2602", "customer": "上汽大众宁波分公司", "zl": "ZL-20260828-031", "combo": "ZH-2602-B × 120 套", "so": "SO-20260829-0038", "addr": "宁波工厂 C 门", "status": "拣货中", "date": "—"}, "cells": ["PRJ-2602", "上汽大众宁波分公司", "<span class=\"lk\">ZL-20260828-031</span>", "ZH-2602-B × 120 套", "SO-20260829-0038", "宁波工厂 C 门", "<span class=\"tag tag-blue\">拣货中</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}, {"t": "出库确认", "act": "openModal('exitConfirmModal')"}]},
      'title': '组合出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'CK-20260830-014',
          'full': true
        },
        {
          'label': '状态',
          'tag': '拣货中'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260828-031',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '关联销售订单',
          'text': 'SO-20260829-0038（双关联）',
          'url': '销售管理/销售订单列表.html',
          'full': true
        },
        {
          'label': '客户',
          'text': '上汽大众宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '出库内容',
          'text': 'ZH-2602-B × 120 套',
          'full': true
        },
        {
          'label': '出库库区',
          'text': '成品区 RB'
        },
        {
          'label': '送达地点',
          'text': '宁波工厂 C 门'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '出库时间',
          'text': '—'
        },
        {
          'label': '出库方式',
          'text': '一箱一件 · 逐件核对（扫码口预留）',
          'full': true
        }
      ],
      'feeSecTitle': '器具 / 组合件清单',
      'feeCols': ['序号', '组合件编码', '名称', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'ZH-2602-B', '冲压件料箱组套', '套', '120', '1.00', '13%', '1.13', '135.60', 'RB-B-02-01']
        }
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260828-031',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '销售订单（双关联）',
          'name': 'SO-20260829-0038',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '组合出库（本单）',
          'name': 'CK-20260830-014',
          'self': true
        },
        {
          'role': '库存查询·客户在租 / 应收',
          'name': '出库确认后起租',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-30 15:00',
          'text': '拣货备货中 · 成品区 RB（ZH-2602-B 120 套）',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '出库确认后已出库 · 起租计费',
          'who': '系统',
          'off': true
        }
      ]
    },
    'CK-20260829-013': {
      'row': {"fields": {"project": "PRJ-2603", "customer": "小鹏汽车科技有限公司", "zl": "ZL-20260610-015", "combo": "ZH-2603-C × 60 套", "so": "SO-20260828-0035", "addr": "广州工厂收货口", "status": "已出库", "date": "2026-08-29"}, "cells": ["PRJ-2603", "小鹏汽车科技有限公司", "<span class=\"lk\">ZL-20260610-015</span>", "ZH-2603-C × 60 套", "SO-20260828-0035", "广州工厂收货口", "<span class=\"tag tag-green\">已出库</span>", "2026-08-29 16:05"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}, {"t": "出库确认", "act": "openModal('exitConfirmModal')"}]},
      'title': '组合出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'CK-20260829-013',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已出库'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260610-015',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '关联销售订单',
          'text': 'SO-20260828-0035（双关联）',
          'url': '销售管理/销售订单列表.html',
          'full': true
        },
        {
          'label': '客户',
          'text': '小鹏汽车科技有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2603'
        },
        {
          'label': '出库内容',
          'text': 'ZH-2603-C × 60 套',
          'full': true
        },
        {
          'label': '出库库区',
          'text': '成品区 RB'
        },
        {
          'label': '送达地点',
          'text': '广州工厂收货口'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '出库时间',
          'text': '2026-08-29 16:05'
        },
        {
          'label': '出库方式',
          'text': '一箱一件 · 逐件核对（扫码口预留）',
          'full': true
        }
      ],
      'feeSecTitle': '器具 / 组合件清单',
      'feeCols': ['序号', '组合件编码', '名称', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'ZH-2603-C', '电池托盘护角套件', '套', '60', '1.00', '13%', '1.13', '67.80', 'RB-C-01-02']
        }
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260610-015',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '销售订单（双关联）',
          'name': 'SO-20260828-0035',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '组合出库（本单）',
          'name': 'CK-20260829-013',
          'self': true
        },
        {
          'role': '库存查询·客户在租 / 应收',
          'name': '客户占用起租 · 租赁费应收',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-30 14:25',
          'text': '拣货备货 · 成品区 RB（ZH-2603-C 60 套）',
          'who': '张伟'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 广州工厂收货口',
          'who': '张伟'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张伟'
        }
      ]
    },
    'CK-20260829-012': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "zl": "ZL-20260301-006", "combo": "ZH-2601-A × 120 套", "so": "SO-20260827-0036", "addr": "长春基地一号门", "status": "已出库", "date": "2026-08-29"}, "cells": ["PRJ-2601", "一汽解放汽车有限公司", "<span class=\"lk\">ZL-20260301-006</span>", "ZH-2601-A × 120 套", "SO-20260827-0036", "长春基地一号门", "<span class=\"tag tag-green\">已出库</span>", "2026-08-29 10:42"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}, {"t": "出库确认", "act": "openModal('exitConfirmModal')"}]},
      'title': '组合出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'CK-20260829-012',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已出库'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260301-006',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '关联销售订单',
          'text': 'SO-20260827-0036（双关联）',
          'url': '销售管理/销售订单列表.html',
          'full': true
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '出库内容',
          'text': 'ZH-2601-A × 120 套',
          'full': true
        },
        {
          'label': '出库库区',
          'text': '成品区 RB'
        },
        {
          'label': '送达地点',
          'text': '长春基地一号门'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '出库时间',
          'text': '2026-08-29 10:42'
        },
        {
          'label': '出库方式',
          'text': '一箱一件 · 逐件核对（扫码口预留）',
          'full': true
        }
      ],
      'feeSecTitle': '器具 / 组合件清单',
      'feeCols': ['序号', '组合件编码', '名称', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'ZH-2601-A', '驾驶室围板箱整箱套件', '套', '120', '1.00', '13%', '1.13', '135.60', 'RB-A-01-01']
        }
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260301-006',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '销售订单（双关联）',
          'name': 'SO-20260827-0036',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '组合出库（本单）',
          'name': 'CK-20260829-012',
          'self': true
        },
        {
          'role': '库存查询·客户在租 / 应收',
          'name': '客户占用起租 · 租赁费应收',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-30 14:25',
          'text': '拣货备货 · 成品区 RB（ZH-2601-A 120 套）',
          'who': '张伟'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 长春基地一号门',
          'who': '张伟'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张伟'
        }
      ]
    },
    'CK-20260828-011': {
      'row': {"fields": {"project": "PRJ-2604", "customer": "东风本田汽车有限公司", "zl": "ZL-20260828-031", "combo": "ZH-2601-A × 96 套", "so": "SO-20260826-0033", "addr": "武汉工厂 2 号门", "status": "已出库", "date": "2026-08-28"}, "cells": ["PRJ-2604", "东风本田汽车有限公司", "<span class=\"lk\">ZL-20260828-031</span>", "ZH-2601-A × 96 套", "SO-20260826-0033", "武汉工厂 2 号门", "<span class=\"tag tag-green\">已出库</span>", "2026-08-28 14:55"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}, {"t": "出库确认", "act": "openModal('exitConfirmModal')"}]},
      'title': '组合出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'CK-20260828-011',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已出库'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260828-031',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '关联销售订单',
          'text': 'SO-20260826-0033（双关联）',
          'url': '销售管理/销售订单列表.html',
          'full': true
        },
        {
          'label': '客户',
          'text': '东风本田汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2604'
        },
        {
          'label': '出库内容',
          'text': 'ZH-2601-A × 96 套',
          'full': true
        },
        {
          'label': '出库库区',
          'text': '成品区 RB'
        },
        {
          'label': '送达地点',
          'text': '武汉工厂 2 号门'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '出库时间',
          'text': '2026-08-28 14:55'
        },
        {
          'label': '出库方式',
          'text': '一箱一件 · 逐件核对（扫码口预留）',
          'full': true
        }
      ],
      'feeSecTitle': '器具 / 组合件清单',
      'feeCols': ['序号', '组合件编码', '名称', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'ZH-2601-A', '驾驶室围板箱整箱套件', '套', '96', '1.00', '13%', '1.13', '108.48', 'RB-A-01-01']
        }
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260828-031',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '销售订单（双关联）',
          'name': 'SO-20260826-0033',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '组合出库（本单）',
          'name': 'CK-20260828-011',
          'self': true
        },
        {
          'role': '库存查询·客户在租 / 应收',
          'name': '客户占用起租 · 租赁费应收',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-30 14:25',
          'text': '拣货备货 · 成品区 RB（ZH-2601-A 96 套）',
          'who': '张伟'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 武汉工厂 2 号门',
          'who': '张伟'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张伟'
        }
      ]
    },
    'CK-20260824-009': {
      'row': {"fields": {"project": "PRJ-2604", "customer": "一汽解放汽车有限公司", "zl": "ZL-20260823-033", "combo": "ZH-2604-D 混合组合套件 × 40 套", "so": "—", "addr": "长春基地一号门", "status": "已出库", "date": "2026-08-24"}, "note": "1", "cells": ["PRJ-2604", "一汽解放汽车有限公司", "<span class=\"lk\">ZL-20260823-033</span>", "ZH-2604-D 混合组合套件 × 40 套", "—", "长春基地一号门", "<span class=\"tag tag-green\">已出库</span>", "2026-08-24 16:40"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}, {"t": "出库确认", "act": "openModal('exitConfirmModal')"}]},
      'title': '组合出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'CK-20260824-009',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已出库'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260823-033',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '关联销售订单',
          'text': '—（租赁出库）',
          'full': true
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2604'
        },
        {
          'label': '出库内容',
          'text': 'ZH-2604-D × 40 套(混合组合套件)',
          'full': true
        },
        {
          'label': '出库库区',
          'text': '成品区 RB'
        },
        {
          'label': '送达地点',
          'text': '长春基地一号门'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '出库时间',
          'text': '2026-08-24 16:40'
        },
        {
          'label': '出库方式',
          'text': '一箱一件 · 逐件核对（扫码口预留）',
          'full': true
        }
      ],
      'feeSecTitle': '器具 / 组合件清单',
      'feeCols': ['序号', '组合件编码', '名称', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'ZH-2604-D', '混合组合套件', '套', '40', '1.00', '13%', '1.13', '45.20', 'RB-D-01-01']
        }
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260823-033',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '组合出库（本单）',
          'name': 'CK-20260824-009',
          'self': true
        },
        {
          'role': '库存查询·客户在租 / 应收',
          'name': '客户占用起租 · 租赁费应收',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-30 14:25',
          'text': '拣货备货 · 成品区 RB（ZH-2604-D 40 套）',
          'who': '张伟'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 长春基地一号门',
          'who': '张伟'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张伟'
        }
      ]
    },
    'CK-20260828-010': {
      'row': {"fields": {"project": "PRJ-2602", "customer": "上汽大众宁波分公司", "zl": "ZL-20260815-028", "combo": "ZH-2602-B × 200 套", "so": "SO-20260826-0032", "addr": "宁波工厂 C 门", "status": "已出库", "date": "2026-08-28"}, "cells": ["PRJ-2602", "上汽大众宁波分公司", "<span class=\"lk\">ZL-20260815-028</span>", "ZH-2602-B × 200 套", "SO-20260826-0032", "宁波工厂 C 门", "<span class=\"tag tag-green\">已出库</span>", "2026-08-28 09:30"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}, {"t": "出库确认", "act": "openModal('exitConfirmModal')"}]},
      'title': '组合出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'CK-20260828-010',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已出库'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260815-028',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '关联销售订单',
          'text': 'SO-20260826-0032（双关联）',
          'url': '销售管理/销售订单列表.html',
          'full': true
        },
        {
          'label': '客户',
          'text': '上汽大众宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '出库内容',
          'text': 'ZH-2602-B × 200 套',
          'full': true
        },
        {
          'label': '出库库区',
          'text': '成品区 RB'
        },
        {
          'label': '送达地点',
          'text': '宁波工厂 C 门'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '出库时间',
          'text': '2026-08-28 09:30'
        },
        {
          'label': '出库方式',
          'text': '一箱一件 · 逐件核对（扫码口预留）',
          'full': true
        }
      ],
      'feeSecTitle': '器具 / 组合件清单',
      'feeCols': ['序号', '组合件编码', '名称', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'ZH-2602-B', '冲压件料箱组套', '套', '200', '1.00', '13%', '1.13', '226.00', 'RB-B-02-01']
        }
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260815-028',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '销售订单（双关联）',
          'name': 'SO-20260826-0032',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '组合出库（本单）',
          'name': 'CK-20260828-010',
          'self': true
        },
        {
          'role': '库存查询·客户在租 / 应收',
          'name': '客户占用起租 · 租赁费应收',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-30 14:25',
          'text': '拣货备货 · 成品区 RB（ZH-2602-B 200 套）',
          'who': '张伟'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 宁波工厂 C 门',
          'who': '张伟'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张伟'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 退租入库单 returnInbounds：键 = TZRK 入库单号（租赁管理/退租入库列表.html 8 行全量） */
  /* 拆散去向：自有回库 / 租入件转归还；缺损/丢失联动丢损赔偿 */
  returnInbounds: {
    'TZRK-20260902-010': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "project": "PRJ-2604", "appliance": "ZH-2604-D 混合组合套件（自购隔板 + 租入大箱）", "dest": "自有回库 租入件转归还", "warehouse": "成品区 RB", "date": "2026-09-02", "result": "缺损", "status": "待审核"}, "note": "1", "cells": ["一汽解放汽车有限公司", "PRJ-2604", "ZH-2604-D 混合组合套件（自购隔板 + 租入大箱）", "<span class=\"td-num\">40 套</span>", "隔板×80（自购）/ 大箱×10（租入-路凯，其中 4 只缺损）", "<span class=\"tag tag-gray\">自有回库</span> <span class=\"tag tag-orange\" onclick=\"go('../租赁管理/租入归还列表.html')\" style=\"cursor:pointer\">租入件转归还</span>", "成品区 RB", "2026-09-02", "<span class=\"tag tag-orange\">缺损</span>", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "审核", "act": "openModal('auditModal')"}]},
      'title': '退租入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'TZRK-20260902-010',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260823-033',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2604'
        },
        {
          'label': '退租内容',
          'text': 'ZH-2604-D 混合组合套件（自购隔板 + 租入大箱） × 40 套',
          'full': true
        },
        {
          'label': '拆散方式',
          'text': '按 BOM 拆散'
        },
        {
          'label': '拆散去向',
          'text': '自有回库 + 租入件转归还',
          'full': true
        },
        {
          'label': '入库库区',
          'text': '成品区 RB'
        },
        {
          'label': '入库时间',
          'text': '2026-09-02'
        },
        {
          'label': '缺损情况',
          'text': '验收发现缺损 · 转丢损赔偿',
          'full': true
        }
      ],
      'feeSecTitle': '拆散明细',
      'feeCols': ['物料', '来源', '单位', '数量', '去向'],
      'fees': [
        {
          'cells': ['折叠隔板', '自购', '件', '80', '自有回库 · 成品区 RB']
        },
        {
          'cells': ['围板箱大箱 1200×1000×970', '租入 · 路凯', '只', '10', '租入件转归还（其中 4 只缺损 → 赔付）']
        }
      ],
      'chain': [
        {
          'role': '退租入库（本单）',
          'name': 'TZRK-20260902-010 · BOM 拆散',
          'self': true
        },
        {
          'role': '租入归还（分流）',
          'name': 'GHCK-20260903-002',
          'url': '租赁管理/租入归还列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-02 09:40',
          'text': '客户退回 · 直接入库登记（无申请单）',
          'who': '张伟'
        },
        {
          't': '09-02 14:20',
          'text': '到货验收 · 发现大箱 4 只缺损',
          'who': '张伟'
        },
        {
          't': '09-02 16:10',
          'text': '按 BOM 拆散 · 隔板 × 80 自有回库',
          'who': '张伟'
        },
        {
          't': '09-03 14:05',
          'text': '大箱分流归还 · GHCK-20260903-002（4 只缺损赔付）',
          'who': '李国栋'
        }
      ]
    },
    'TZRK-20260903-009': {
      'row': {"fields": {"customer": "上汽大众汽车有限公司宁波分公司", "project": "PRJ-2603", "appliance": "WBX-1210L 围板箱 1200×1000×970（租入-路凯）", "dest": "租入件转归还", "warehouse": "外购区 RW", "date": "2026-09-03", "result": "完好", "status": "待审核"}, "note": "2", "cells": ["上汽大众汽车有限公司宁波分公司", "PRJ-2603", "WBX-1210L 围板箱 1200×1000×970（租入-路凯）", "<span class=\"td-num\">30 只</span>", "整箱退回（租入资产，不拆散）", "<span class=\"tag tag-orange\" onclick=\"go('../租赁管理/租入归还列表.html')\" style=\"cursor:pointer\">租入件转归还</span>", "外购区 RW", "2026-09-03", "<span class=\"tag tag-green\">完好</span>", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "审核", "act": "openModal('auditModal')"}]},
      'title': '退租入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'TZRK-20260903-009',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260816-029',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '客户',
          'text': '上汽大众汽车有限公司宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2603'
        },
        {
          'label': '退租内容',
          'text': 'WBX-1210L 围板箱 1200×1000×970（租入-路凯） × 30 只',
          'full': true
        },
        {
          'label': '拆散方式',
          'text': '整箱退回（不拆散）'
        },
        {
          'label': '拆散去向',
          'text': '租入件转归还',
          'full': true
        },
        {
          'label': '入库库区',
          'text': '外购区 RW'
        },
        {
          'label': '入库时间',
          'text': '2026-09-03'
        },
        {
          'label': '缺损情况',
          'text': '验收完好',
          'full': true
        }
      ],
      'feeSecTitle': '拆散明细',
      'feeCols': ['物料', '来源', '单位', '数量', '去向'],
      'fees': [
        {
          'cells': ['WBX-1210L 围板箱 1200×1000×970', '租入 · 路凯', '只', '30', '整箱退回 · 租入件转归还']
        }
      ],
      'chain': [
        {
          'role': '退租入库（本单）',
          'name': 'TZRK-20260903-009',
          'self': true
        },
        {
          'role': '租入归还',
          'name': 'GHCK-20260903-001',
          'url': '租赁管理/租入归还列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-03 09:20',
          'text': '客户整箱退回 · 到货验收',
          'who': '张伟'
        },
        {
          't': '09-03 11:00',
          'text': '验收完好 · 不拆散直接转归还',
          'who': '张伟'
        },
        {
          't': '09-03 11:30',
          'text': '整退归还路凯 · GHCK-20260903-001',
          'who': '李国栋'
        },
        {
          't': '—',
          'text': '待审核 · 审核通过转已入库',
          'who': '系统',
          'off': true
        }
      ]
    },
    'TZRK-20260902-008': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "project": "PRJ-2601", "appliance": "ZH-2601-A 驾驶室围板箱整箱套件", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-09-02", "result": "缺损", "status": "待审核"}, "note": "3", "cells": ["一汽解放汽车有限公司", "PRJ-2601", "ZH-2601-A 驾驶室围板箱整箱套件", "<span class=\"td-num\">60 套</span>", "围板×120 / 箱体×60 / 锁扣组件×240", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-09-02", "<span class=\"tag tag-orange\">缺损</span>", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "审核", "act": "openModal('auditModal')"}]},
      'title': '退租入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'TZRK-20260902-008',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260610-015',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '退租内容',
          'text': 'ZH-2601-A 驾驶室围板箱整箱套件 × 60 套',
          'full': true
        },
        {
          'label': '拆散方式',
          'text': '按 BOM 拆散'
        },
        {
          'label': '拆散去向',
          'text': '自有回库',
          'full': true
        },
        {
          'label': '入库库区',
          'text': '成品区 RB'
        },
        {
          'label': '入库时间',
          'text': '2026-09-02'
        },
        {
          'label': '缺损情况',
          'text': '验收发现缺损 · 转丢损赔偿',
          'full': true
        }
      ],
      'feeSecTitle': '拆散明细',
      'feeCols': ['物料', '来源', '单位', '数量', '去向'],
      'fees': [
        {
          'cells': ['围板', '自购', '件', '120', '自有回库 · 成品区 RB']
        },
        {
          'cells': ['箱体', '自购', '只', '60', '自有回库 · 成品区 RB']
        },
        {
          'cells': ['锁扣组件', '自购', '件', '240', '自有回库 · 成品区 RB']
        }
      ],
      'chain': [
        {
          'role': '退租入库（本单）',
          'name': 'TZRK-20260902-008 · BOM 拆散',
          'self': true
        },
        {
          'role': '丢损赔偿',
          'name': '缺损件转赔偿',
        },
        {
          'role': '拆卸 · 再组装',
          'name': '拆散件回散件库',
        }
      ],
      'timeline': [
        {
          't': '09-01',
          'text': '客户退回 · 直接入库登记',
          'who': '张伟'
        },
        {
          't': '09-02 10:30',
          'text': '到货验收 · 发现缺损',
          'who': '张伟'
        },
        {
          't': '09-02 15:40',
          'text': '按 BOM 拆散入库 · 自有回库',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '待审核 · 缺损件转丢损赔偿',
          'who': '系统',
          'off': true
        }
      ]
    },
    'TZRK-20260901-007': {
      'row': {"fields": {"customer": "上汽大众汽车有限公司宁波分公司", "project": "PRJ-2602", "appliance": "ZH-2602-B 冲压件料箱组套", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-09-01", "result": "完好", "status": "已入库"}, "cells": ["上汽大众汽车有限公司宁波分公司", "PRJ-2602", "ZH-2602-B 冲压件料箱组套", "<span class=\"td-num\">45 套</span>", "料箱×45 / 隔板×90", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-09-01", "<span class=\"tag tag-green\">完好</span>", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '退租入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'TZRK-20260901-007',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260301-006',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '客户',
          'text': '上汽大众汽车有限公司宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '退租内容',
          'text': 'ZH-2602-B 冲压件料箱组套 × 45 套',
          'full': true
        },
        {
          'label': '拆散方式',
          'text': '按 BOM 拆散'
        },
        {
          'label': '拆散去向',
          'text': '自有回库',
          'full': true
        },
        {
          'label': '入库库区',
          'text': '成品区 RB'
        },
        {
          'label': '入库时间',
          'text': '2026-09-01'
        },
        {
          'label': '缺损情况',
          'text': '验收完好',
          'full': true
        }
      ],
      'feeSecTitle': '拆散明细',
      'feeCols': ['物料', '来源', '单位', '数量', '去向'],
      'fees': [
        {
          'cells': ['料箱', '自购', '只', '45', '自有回库 · 成品区 RB']
        },
        {
          'cells': ['隔板', '自购', '件', '90', '自有回库 · 成品区 RB']
        }
      ],
      'chain': [
        {
          'role': '退租入库（本单）',
          'name': 'TZRK-20260901-007 · BOM 拆散',
          'self': true
        },
        {
          'role': '拆卸 · 再组装',
          'name': '拆散件回散件库',
        }
      ],
      'timeline': [
        {
          't': '08-30',
          'text': '客户退回 · 直接入库登记',
          'who': '张伟'
        },
        {
          't': '09-01 09:50',
          'text': '到货验收 · 完好',
          'who': '张伟'
        },
        {
          't': '09-01 14:20',
          'text': '按 BOM 拆散入库 · 自有回库',
          'who': '张伟'
        }
      ]
    },
    'TZRK-20260831-006': {
      'row': {"fields": {"customer": "小鹏汽车科技有限公司", "project": "PRJ-2603", "appliance": "ZH-2603-C 电池托盘护角套件", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-08-31", "result": "丢失", "status": "已入库"}, "cells": ["小鹏汽车科技有限公司", "PRJ-2603", "ZH-2603-C 电池托盘护角套件", "<span class=\"td-num\">20 套</span>", "托盘×20 / 护角×80", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-08-31", "<span class=\"tag tag-red\">丢失</span>", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '退租入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'TZRK-20260831-006',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260720-022',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '客户',
          'text': '小鹏汽车科技有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2603'
        },
        {
          'label': '退租内容',
          'text': 'ZH-2603-C 电池托盘护角套件 × 20 套',
          'full': true
        },
        {
          'label': '拆散方式',
          'text': '按 BOM 拆散'
        },
        {
          'label': '拆散去向',
          'text': '自有回库',
          'full': true
        },
        {
          'label': '入库库区',
          'text': '成品区 RB'
        },
        {
          'label': '入库时间',
          'text': '2026-08-31'
        },
        {
          'label': '缺损情况',
          'text': '验收发现丢失 · 自客户态直接出账（赔偿核销）',
          'full': true
        }
      ],
      'feeSecTitle': '拆散明细',
      'feeCols': ['物料', '来源', '单位', '数量', '去向'],
      'fees': [
        {
          'cells': ['托盘', '自购', '件', '20', '自有回库 · 成品区 RB（4 件丢失 → 赔偿）']
        },
        {
          'cells': ['护角', '自购', '件', '80', '自有回库 · 成品区 RB']
        }
      ],
      'chain': [
        {
          'role': '退租入库（本单）',
          'name': 'TZRK-20260831-006 · BOM 拆散',
          'self': true
        },
        {
          'role': '丢损赔偿',
          'name': 'BS-20260902-010 · 丢失件出账',
        },
        {
          'role': '库存核销',
          'name': '其他出库 · 赔偿核销',
          'url': '仓储作业/其他出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-29',
          'text': '客户退回 · 直接入库登记',
          'who': '张伟'
        },
        {
          't': '08-31 10:15',
          'text': '到货验收 · 托盘 4 件丢失',
          'who': '张伟'
        },
        {
          't': '08-31 16:20',
          'text': '拆散入库 · 丢失件生成赔偿 BS-20260902-010',
          'who': '系统'
        },
        {
          't': '—',
          'text': '丢失件自客户态直接出账 · 其他出库赔偿核销',
          'who': '系统',
          'off': true
        }
      ]
    },
    'TZRK-20260828-005': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "project": "PRJ-2601", "appliance": "BTC-6040 料箱", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-08-28", "result": "完好", "status": "已入库"}, "cells": ["一汽解放汽车有限公司", "PRJ-2601", "BTC-6040 料箱", "<span class=\"td-num\">200 只</span>", "—（散件直接入库）", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-08-28", "<span class=\"tag tag-green\">完好</span>", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '退租入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'TZRK-20260828-005',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260610-015',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '退租内容',
          'text': 'BTC-6040 料箱 × 200 只',
          'full': true
        },
        {
          'label': '拆散方式',
          'text': '散件直接入库'
        },
        {
          'label': '拆散去向',
          'text': '自有回库',
          'full': true
        },
        {
          'label': '入库库区',
          'text': '成品区 RB'
        },
        {
          'label': '入库时间',
          'text': '2026-08-28'
        },
        {
          'label': '缺损情况',
          'text': '验收完好',
          'full': true
        }
      ],
      'feeSecTitle': '拆散明细',
      'feeCols': ['物料', '来源', '单位', '数量', '去向'],
      'fees': [
        {
          'cells': ['BTC-6040 料箱', '自购', '只', '200', '自有回库 · 成品区 RB']
        }
      ],
      'chain': [
        {
          'role': '退租入库（本单）',
          'name': 'TZRK-20260828-005',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '08-26',
          'text': '客户退回 · 直接入库登记',
          'who': '张伟'
        },
        {
          't': '08-28 09:30',
          'text': '到货验收 · 完好',
          'who': '张伟'
        },
        {
          't': '08-28 11:00',
          'text': '散件直接入库 · 自有回库',
          'who': '张伟'
        }
      ]
    },
    'TZRK-20260825-004': {
      'row': {"fields": {"customer": "上汽大众汽车有限公司宁波分公司", "project": "PRJ-2602", "appliance": "PLT-1210P 塑料托盘", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-08-25", "result": "完好", "status": "已入库"}, "cells": ["上汽大众汽车有限公司宁波分公司", "PRJ-2602", "PLT-1210P 塑料托盘", "<span class=\"td-num\">150 块</span>", "—（散件直接入库）", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-08-25", "<span class=\"tag tag-green\">完好</span>", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '退租入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'TZRK-20260825-004',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260301-006',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '客户',
          'text': '上汽大众汽车有限公司宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '退租内容',
          'text': 'PLT-1210P 塑料托盘 × 150 块',
          'full': true
        },
        {
          'label': '拆散方式',
          'text': '散件直接入库'
        },
        {
          'label': '拆散去向',
          'text': '自有回库',
          'full': true
        },
        {
          'label': '入库库区',
          'text': '成品区 RB'
        },
        {
          'label': '入库时间',
          'text': '2026-08-25'
        },
        {
          'label': '缺损情况',
          'text': '验收完好',
          'full': true
        }
      ],
      'feeSecTitle': '拆散明细',
      'feeCols': ['物料', '来源', '单位', '数量', '去向'],
      'fees': [
        {
          'cells': ['PLT-1210P 塑料托盘', '自购', '块', '150', '自有回库 · 成品区 RB']
        }
      ],
      'chain': [
        {
          'role': '退租入库（本单）',
          'name': 'TZRK-20260825-004',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '08-23',
          'text': '客户退回 · 直接入库登记',
          'who': '张伟'
        },
        {
          't': '08-25 10:20',
          'text': '到货验收 · 完好',
          'who': '张伟'
        },
        {
          't': '08-25 15:10',
          'text': '散件直接入库 · 自有回库',
          'who': '张伟'
        }
      ]
    },
    'TZRK-20260820-003': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "project": "PRJ-2601", "appliance": "ZH-2601-A 驾驶室围板箱整箱套件", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-08-20", "result": "缺损", "status": "已入库"}, "cells": ["一汽解放汽车有限公司", "PRJ-2601", "ZH-2601-A 驾驶室围板箱整箱套件", "<span class=\"td-num\">30 套</span>", "围板×60 / 箱体×30 / 锁扣组件×120", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-08-20", "<span class=\"tag tag-orange\">缺损</span>", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '退租入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'TZRK-20260820-003',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '关联租赁单',
          'text': 'ZL-20260815-028',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '退租内容',
          'text': 'ZH-2601-A 驾驶室围板箱整箱套件 × 30 套',
          'full': true
        },
        {
          'label': '拆散方式',
          'text': '按 BOM 拆散'
        },
        {
          'label': '拆散去向',
          'text': '自有回库',
          'full': true
        },
        {
          'label': '入库库区',
          'text': '成品区 RB'
        },
        {
          'label': '入库时间',
          'text': '2026-08-20'
        },
        {
          'label': '缺损情况',
          'text': '验收发现缺损 · 转丢损赔偿',
          'full': true
        }
      ],
      'feeSecTitle': '拆散明细',
      'feeCols': ['物料', '来源', '单位', '数量', '去向'],
      'fees': [
        {
          'cells': ['围板', '自购', '件', '60', '自有回库 · 成品区 RB']
        },
        {
          'cells': ['箱体', '自购', '只', '30', '自有回库 · 成品区 RB（缺损 → 赔偿）']
        },
        {
          'cells': ['锁扣组件', '自购', '件', '120', '自有回库 · 成品区 RB']
        }
      ],
      'chain': [
        {
          'role': '退租入库（本单）',
          'name': 'TZRK-20260820-003 · BOM 拆散',
          'self': true
        },
        {
          'role': '丢损赔偿',
          'name': 'BS-20260901-009 · 缺损件转赔偿',
        },
        {
          'role': '拆卸 · 再组装',
          'name': '拆散件回散件库',
        }
      ],
      'timeline': [
        {
          't': '08-18',
          'text': '客户退回 · 直接入库登记',
          'who': '张伟'
        },
        {
          't': '08-20 09:40',
          'text': '到货验收 · 发现缺损',
          'who': '张伟'
        },
        {
          't': '08-20 15:30',
          'text': '按 BOM 拆散入库 · 缺损件生成赔偿 BS-20260901-009',
          'who': '系统'
        }
      ]
    }
  },  /* -------------------------------------------------------------------------- */
  /* 租入归还单 rentInReturns：键 = GHCK 归还单号（租赁管理/租入归还列表.html 3 行全量） */
  /* 归还类型：整退归还(L3) / 分流归还(L4) */
  rentInReturns: {
    'GHCK-20260903-001': {
      'row': {"fields": {"ref": "RZD-20260815-003", "operator": "路凯包装运营（上海）有限公司", "rtype": "整退归还", "appliance": "围板箱 1200×1000×970", "status": "已归还", "maker": "李国栋", "date": "2026-09-03"}, "note": "1", "cells": ["<span class=\"lk\" onclick=\"go('../租赁管理/租入单列表.html')\">RZD-20260815-003</span>", "路凯包装运营（上海）有限公司", "<span class=\"tag tag-blue\">整退归还</span>", "围板箱 1200×1000×970", "30 只", "<span class=\"tag tag-green\">已归还</span>", "李国栋", "2026-09-03 11:30"], "ops": [{"t": "详情", "detail": true}, {"t": "租金应付", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '租入归还单详情',
      'info': [
        {
          'label': '归还单号',
          'text': 'GHCK-20260903-001',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已归还'
        },
        {
          'label': '关联租入单',
          'text': 'RZD-20260815-003',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'label': '供应商',
          'text': '路凯包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '归还类型',
          'text': '整退归还（L3）'
        },
        {
          'label': '器具',
          'text': '围板箱 1200×1000×970',
          'full': true
        },
        {
          'label': '归还数量',
          'text': '30 只'
        },
        {
          'label': '器具状况',
          'text': '验收完好'
        },
        {
          'label': '经办人',
          'text': '李国栋'
        },
        {
          'label': '归还日期',
          'text': '2026-09-03'
        },
        {
          'label': '租金结算',
          'text': '已生成租金应付 AP-20260903-009（36,000.00 元）',
          'url': '财务协同/应付账单.html',
          'full': true
        }
      ],
      'feeSecTitle': '归还明细',
      'feeCols': ['序号', '器具', '归还类型', '单位', '数量', '状况'],
      'fees': [
        {
          'cells': ['1', '围板箱 1200×1000×970', '整退归还', '只', '30', '完好']
        }
      ],
      'chain': [
        {
          'role': '退租入库',
          'name': 'TZRK-20260903-009 · 整箱退回',
          'url': '租赁管理/退租入库列表.html'
        },
        {
          'role': '租入归还（本单）',
          'name': 'GHCK-20260903-001',
          'self': true
        },
        {
          'role': '租金应付',
          'name': 'AP-20260903-009 · 36,000 元',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '09-03 09:10',
          'text': '客户整箱退回 · 退租入库核对（TZRK-20260903-009）',
          'who': '李国栋'
        },
        {
          't': '09-03 11:30',
          'text': '整退归还路凯 · 出库确认',
          'who': '李国栋'
        },
        {
          't': '09-03',
          'text': '按周期生成租金应付 AP-20260903-009',
          'who': '系统'
        }
      ]
    },
    'GHCK-20260903-002': {
      'row': {"fields": {"ref": "RZD-20260815-005", "operator": "路凯包装运营（上海）有限公司", "rtype": "分流归还", "appliance": "围板箱 1200×1000×970（退租拆散后归还）", "status": "待审核", "maker": "李国栋", "date": "2026-09-03"}, "note": "2", "cells": ["<span class=\"lk\" onclick=\"go('../租赁管理/租入单列表.html')\">RZD-20260815-005</span>", "路凯包装运营（上海）有限公司", "<span class=\"tag tag-orange\">分流归还</span>", "围板箱 1200×1000×970（退租拆散后归还）", "4 只", "<span class=\"tag tag-orange\">待审核</span>", "李国栋", "2026-09-03 14:05"], "ops": [{"t": "详情", "detail": true}, {"t": "审核", "act": "openModal('auditModal')"}]},
      'title': '租入归还单详情',
      'info': [
        {
          'label': '归还单号',
          'text': 'GHCK-20260903-002',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '关联租入单',
          'text': 'RZD-20260815-005',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'label': '供应商',
          'text': '路凯包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '归还类型',
          'text': '分流归还（L4）'
        },
        {
          'label': '器具',
          'text': '围板箱 1200×1000×970（退租拆散后归还）',
          'full': true
        },
        {
          'label': '归还数量',
          'text': '4 只'
        },
        {
          'label': '器具状况',
          'text': '验收完好（4 只缺损已转赔付）'
        },
        {
          'label': '经办人',
          'text': '李国栋'
        },
        {
          'label': '归还日期',
          'text': '2026-09-03'
        },
        {
          'label': '租金结算',
          'text': '按周期生成租金应付 · AP-20260903-010（12,000.00 元）',
          'url': '财务协同/应付账单.html',
          'full': true
        }
      ],
      'feeSecTitle': '归还明细',
      'feeCols': ['序号', '器具', '归还类型', '单位', '数量', '状况'],
      'fees': [
        {
          'cells': ['1', '围板箱 1200×1000×970', '分流归还', '只', '4', '完好（4 只缺损已转赔付）']
        }
      ],
      'chain': [
        {
          'role': '退租入库',
          'name': 'TZRK-20260902-010 · 分流',
          'url': '租赁管理/退租入库列表.html'
        },
        {
          'role': '租入归还（本单）',
          'name': 'GHCK-20260903-002',
          'self': true
        },
        {
          'role': '租金应付',
          'name': 'AP-20260903-010 · 12,000 元',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '09-02',
          'text': '退租拆散 · TZRK-20260902-010（大箱 10 只分流）',
          'who': '张伟'
        },
        {
          't': '09-03 14:05',
          'text': '分流归还路凯 · 其中 4 只缺损转赔付',
          'who': '李国栋'
        },
        {
          't': '—',
          'text': '待审核 · 审核通过后完成归还',
          'who': '系统',
          'off': true
        }
      ]
    },
    'GHCK-20260831-003': {
      'row': {"fields": {"ref": "RZD-20260701-001", "operator": "路凯包装运营（上海）有限公司", "rtype": "整退归还", "appliance": "金属料箱 800×600", "status": "已归还", "maker": "王志远", "date": "2026-08-31"}, "cells": ["<span class=\"lk\" onclick=\"go('../租赁管理/租入单列表.html')\">RZD-20260701-001</span>", "路凯包装运营（上海）有限公司", "<span class=\"tag tag-blue\">整退归还</span>", "金属料箱 800×600", "20 只", "<span class=\"tag tag-green\">已归还</span>", "王志远", "2026-08-31 10:15"], "ops": [{"t": "详情", "detail": true}]},
      'title': '租入归还单详情',
      'info': [
        {
          'label': '归还单号',
          'text': 'GHCK-20260831-003',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已归还'
        },
        {
          'label': '关联租入单',
          'text': 'RZD-20260701-001',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'label': '供应商',
          'text': '路凯包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '归还类型',
          'text': '整退归还'
        },
        {
          'label': '器具',
          'text': '金属料箱 800×600',
          'full': true
        },
        {
          'label': '归还数量',
          'text': '20 只'
        },
        {
          'label': '器具状况',
          'text': '验收完好'
        },
        {
          'label': '经办人',
          'text': '王志远'
        },
        {
          'label': '归还日期',
          'text': '2026-08-31'
        },
        {
          'label': '租金结算',
          'text': '租金已结清 · 单据完结',
          'full': true
        }
      ],
      'feeSecTitle': '归还明细',
      'feeCols': ['序号', '器具', '归还类型', '单位', '数量', '状况'],
      'fees': [
        {
          'cells': ['1', '金属料箱 800×600', '整退归还', '只', '20', '完好']
        }
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260701-001',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'role': '租入归还（本单）',
          'name': 'GHCK-20260831-003',
          'self': true
        },
        {
          'role': '租金结算',
          'name': '已结清',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-31 09:30',
          'text': '整退出库 · 归还路凯',
          'who': '王志远'
        },
        {
          't': '08-31 10:15',
          'text': '归还确认 · 验收完好',
          'who': '王志远'
        },
        {
          't': '08-31',
          'text': '租金结清 · 单据完结',
          'who': '系统'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 租入入库单 rentInbounds：键 = RZRK 入库单号（租赁管理/租入入库列表.html 3 行全量） */
  /* 计租起点按租入单起算；入库后转租/组装去向贯通 */
  rentInbounds: {
    'RZRK-20260816-021': {
      'row': {"fields": {"ref": "RZD-20260815-003", "operator": "路凯包装运营（上海）有限公司", "appliance": "围板箱 1200×1000×970", "area": "外购区 RW", "status": "已入库", "maker": "李国栋", "date": "2026-08-16"}, "note": "1", "cells": ["<span class=\"lk\" onclick=\"go('../租赁管理/租入单列表.html')\">RZD-20260815-003</span>", "路凯包装运营（上海）有限公司", "围板箱 1200×1000×970", "30 只", "外购区 RW", "<span class=\"tag tag-green\">已入库</span>", "李国栋", "2026-08-16 14:20"], "ops": [{"t": "详情", "detail": true}, {"t": "租金应付", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '租入入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'RZRK-20260816-021',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '关联租入单',
          'text': 'RZD-20260815-003',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'label': '供应商',
          'text': '路凯包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '器具',
          'text': '围板箱 1200×1000×970',
          'full': true
        },
        {
          'label': '入库数量',
          'text': '30 只'
        },
        {
          'label': '入库库区',
          'text': '外购区 RW（租入在库）',
          'full': true
        },
        {
          'label': '计租起点',
          'text': '2026-08-15（按租入单起算）',
          'full': true
        },
        {
          'label': '经办人',
          'text': '李国栋'
        },
        {
          'label': '入库时间',
          'text': '2026-08-16 14:20'
        },
        {
          'label': '转租去向',
          'text': 'ZL-20260816-029',
          'url': '租赁管理/租赁单列表.html',
          'full': true
        }
      ],
      'feeSecTitle': '入库明细',
      'feeCols': ['序号', '器具', '资产来源', '单位', '数量', '库位'],
      'fees': [
        {
          'cells': ['1', '围板箱 1200×1000×970', '租入 · 路凯', '只', '30', '外购区 RW']
        }
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260815-003',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'role': '租入入库（本单）',
          'name': 'RZRK-20260816-021',
          'self': true
        },
        {
          'role': '租赁单（转租）',
          'name': 'ZL-20260816-029',
          'url': '租赁管理/租赁单列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-15',
          'text': '租入单签订 · 计租开始',
          'who': '王志远'
        },
        {
          't': '08-16 10:00',
          'text': '路凯到货 · 围板箱 30 只',
          'who': '李国栋'
        },
        {
          't': '08-16 14:20',
          'text': '验收入库 · 计入租入在库（外购区 RW）',
          'who': '李国栋'
        },
        {
          't': '08-16',
          'text': '转租客户 · ZL-20260816-029',
          'who': '王琳'
        }
      ]
    },
    'RZRK-20260816-022': {
      'row': {"fields": {"ref": "RZD-20260815-005", "operator": "路凯包装运营（上海）有限公司", "appliance": "围板箱 1200×1000×970", "area": "外购区 RW", "status": "已入库", "maker": "李国栋", "date": "2026-08-16"}, "note": "2", "cells": ["<span class=\"lk\" onclick=\"go('../租赁管理/租入单列表.html')\">RZD-20260815-005</span>", "路凯包装运营（上海）有限公司", "围板箱 1200×1000×970", "10 只", "外购区 RW", "<span class=\"tag tag-green\">已入库</span>", "李国栋", "2026-08-16 15:02"], "ops": [{"t": "详情", "detail": true}, {"t": "租金应付", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '租入入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'RZRK-20260816-022',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '关联租入单',
          'text': 'RZD-20260815-005',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'label': '供应商',
          'text': '路凯包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '器具',
          'text': '围板箱 1200×1000×970',
          'full': true
        },
        {
          'label': '入库数量',
          'text': '10 只'
        },
        {
          'label': '入库库区',
          'text': '外购区 RW（租入在库）',
          'full': true
        },
        {
          'label': '计租起点',
          'text': '2026-08-15（按租入单起算）',
          'full': true
        },
        {
          'label': '经办人',
          'text': '李国栋'
        },
        {
          'label': '入库时间',
          'text': '2026-08-16 15:02'
        },
        {
          'label': '转租去向',
          'text': 'ZZ-20260822-006',
          'full': true
        }
      ],
      'feeSecTitle': '入库明细',
      'feeCols': ['序号', '器具', '资产来源', '单位', '数量', '库位'],
      'fees': [
        {
          'cells': ['1', '围板箱 1200×1000×970', '租入 · 路凯', '只', '10', '外购区 RW']
        }
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260815-005',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'role': '租入入库（本单）',
          'name': 'RZRK-20260816-022',
          'self': true
        },
        {
          'role': '组装（混合配方）',
          'name': 'ZZ-20260822-006',
        },
        {
          'role': '租赁单',
          'name': 'ZL-20260823-033',
          'url': '租赁管理/租赁单列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-15',
          'text': '租入单签订 · 计租开始',
          'who': '王志远'
        },
        {
          't': '08-16 14:30',
          'text': '路凯到货 · 围板箱 10 只',
          'who': '李国栋'
        },
        {
          't': '08-16 15:02',
          'text': '验收入库 · 计入租入在库（外购区 RW）',
          'who': '李国栋'
        },
        {
          't': '08-22',
          'text': '混合组装 · ZZ-20260822-006（ZH-2604-D）',
          'who': '刘志强'
        }
      ]
    },
    'RZRK-20260903-023': {
      'row': {"fields": {"ref": "RZD-20260902-008", "operator": "路凯包装运营（上海）有限公司", "appliance": "塑料托盘 1200×1000", "area": "外购区 RW", "status": "待入库", "maker": "陈金", "date": "2026-09-03"}, "cells": ["<span class=\"lk\" onclick=\"go('../租赁管理/租入单列表.html')\">RZD-20260902-008</span>", "路凯包装运营（上海）有限公司", "塑料托盘 1200×1000", "50 只", "外购区 RW", "<span class=\"tag tag-orange\">待入库</span>", "陈金", "2026-09-03 09:45"], "ops": [{"t": "详情", "detail": true}, {"t": "入库确认", "act": "openModal('auditModal')"}]},
      'title': '租入入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'RZRK-20260903-023',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待入库'
        },
        {
          'label': '关联租入单',
          'text': 'RZD-20260902-008',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'label': '供应商',
          'text': '路凯包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '器具',
          'text': '塑料托盘 1200×1000',
          'full': true
        },
        {
          'label': '入库数量',
          'text': '50 只'
        },
        {
          'label': '入库库区',
          'text': '外购区 RW',
          'full': true
        },
        {
          'label': '计租起点',
          'text': '2026-09-02（按租入单起算）',
          'full': true
        },
        {
          'label': '经办人',
          'text': '陈金'
        },
        {
          'label': '入库时间',
          'text': '2026-09-03 09:45'
        },
        {
          'label': '转租去向',
          'text': '—（待入库确认）',
          'full': true
        }
      ],
      'feeSecTitle': '入库明细',
      'feeCols': ['序号', '器具', '资产来源', '单位', '数量', '库位'],
      'fees': [
        {
          'cells': ['1', '塑料托盘 1200×1000', '租入 · 路凯', '只', '50', '外购区 RW']
        }
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260902-008',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'role': '租入入库（本单）',
          'name': 'RZRK-20260903-023 · 待入库',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '09-03 09:45',
          'text': '租入单审核通过 · 待到货入库',
          'who': '陈金'
        },
        {
          't': '—',
          'text': '待入库确认 · 入库后计入租入在库并转租',
          'who': '系统',
          'off': true
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 采购订单 purchaseOrders：键 = PO 订单号（采购管理/采购订单列表.html 7 行全量） */
  /* B1 独立采购线 · 不以销定采；SO 号仅参考关联 */
  purchaseOrders: {
    'PO-20260902-018': {
      'row': {"fields": {"supplier": "苏州联恒五金制品有限公司", "mtype": "零部件", "summary": "锁扣组件×5,000 / 铰链×2,000", "date": "2026-09-10", "so": "SO-20260831-0042", "status": "待审核"}, "note": "1", "cells": ["苏州联恒五金制品有限公司", "<span class=\"tag tag-blue\">零部件</span>", "锁扣组件×5,000 / 铰链×2,000", "<span class=\"td-num\">7,000</span>", "<span class=\"td-num\">12,700.00</span>", "CNY", "2026-09-10", "<span class=\"lk\">SO-20260831-0042</span>", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "编辑", "act": "openModal('createModal')"}, {"t": "审核", "act": "openModal('auditModal')"}, {"t": "关闭"}]},
      'title': '采购订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'PO-20260902-018',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '供应商',
          'text': '苏州联恒五金制品有限公司',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '零部件'
        },
        {
          'label': '采购内容',
          'text': '锁扣组件× 5,000 / 铰链× 2,000',
          'full': true
        },
        {
          'label': '数量合计',
          'text': '7,000 件'
        },
        {
          'label': '订单金额',
          'text': '12,700.00 CNY'
        },
        {
          'label': '交货日期',
          'text': '2026-09-10'
        },
        {
          'label': '参考关联销售订单',
          'text': 'SO-20260831-0042（参考 · 不以销定采）',
          'url': '销售管理/销售订单列表.html',
          'full': true
        },
        {
          'label': '制单人',
          'text': '李国栋'
        },
        {
          'label': '审核人',
          'text': '—'
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['零件号', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['LJ-A100', '锁扣组件 不锈钢 304', '件', '5,000', '1.90', '13%', '2.15', '10,750.00']
        },
        {
          'cells': ['LJ-B200', '铰链 锌合金 65mm', '件', '2,000', '1.60', '13%', '1.81', '3,620.00']
        },
        {
          'cells': ['', '合计', '', '7,000', '', '', '', '12,700.00']
        }
      ],
      'chain': [
        {
          'role': '销售订单（参考）',
          'name': 'SO-20260831-0042',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '采购订单（本单）',
          'name': 'PO-20260902-018 · 独立采购线',
          'self': true
        },
        {
          'role': '采购入库',
          'name': '凭单到货验收',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '应付账单',
          'name': '采购应付',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '09-02 14:20',
          'text': '制单 · 零部件采购（锁扣 / 铰链）',
          'who': '李国栋'
        },
        {
          't': '—',
          'text': '待审核 · 通过后按交期 09-10 到货验收',
          'off': true
        }
      ]
    },
    'PO-20260901-017': {
      'row': {"fields": {"supplier": "宁波华塑包装制品有限公司", "mtype": "器具", "summary": "围板箱 1200×1000×970×300", "date": "2026-09-15", "so": "—", "status": "待审核"}, "cells": ["宁波华塑包装制品有限公司", "<span class=\"tag tag-green\">器具</span>", "围板箱 1200×1000×970×300", "<span class=\"td-num\">300</span>", "<span class=\"td-num\">84,000.00</span>", "CNY", "2026-09-15", "—", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "编辑", "act": "openModal('createModal')"}, {"t": "审核", "act": "openModal('auditModal')"}, {"t": "关闭"}]},
      'title': '采购订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'PO-20260901-017',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '供应商',
          'text': '宁波华塑包装制品有限公司',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '器具'
        },
        {
          'label': '采购内容',
          'text': '围板箱 1200× 1000× 970× 300',
          'full': true
        },
        {
          'label': '数量合计',
          'text': '300'
        },
        {
          'label': '订单金额',
          'text': '84,000.00 CNY'
        },
        {
          'label': '交货日期',
          'text': '2026-09-15'
        },
        {
          'label': '参考关联销售订单',
          'text': '——',
          'full': true
        },
        {
          'label': '制单人',
          'text': '李国栋'
        },
        {
          'label': '审核人',
          'text': '—'
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['零件号', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['WBX-1210L', '围板箱 1200×1000×970', '只', '300', '280.00', '13%', '316.40', '94,920.00']
        },
        {
          'cells': ['', '合计', '', '300', '', '', '', '84,000.00']
        }
      ],
      'chain': [
        {
          'role': '采购订单（本单）',
          'name': 'PO-20260901-017 · 独立采购线',
          'self': true
        },
        {
          'role': '采购入库',
          'name': '凭单到货验收',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '应付账单',
          'name': '采购应付',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '09-01 10:40',
          'text': '制单 · 器具采购（围板箱 300 只）',
          'who': '李国栋'
        },
        {
          't': '—',
          'text': '待审核 · 通过后按交期 09-15 到货验收',
          'off': true
        }
      ]
    },
    'PO-20260830-016': {
      'row': {"fields": {"supplier": "常州正大塑料托盘厂", "mtype": "器具", "summary": "塑料托盘 1200×1000×500", "date": "2026-09-08", "so": "—", "status": "已审核"}, "cells": ["常州正大塑料托盘厂", "<span class=\"tag tag-green\">器具</span>", "塑料托盘 1200×1000×500", "<span class=\"td-num\">500</span>", "<span class=\"td-num\">42,500.00</span>", "CNY", "2026-09-08", "—", "<span class=\"tag tag-blue\">已审核</span>"], "ops": [{"t": "生成入库单", "act": "go('../采购管理/采购入库列表.html')"}, {"t": "关闭"}]},
      'title': '采购订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'PO-20260830-016',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已审核'
        },
        {
          'label': '供应商',
          'text': '常州正大塑料托盘厂',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '器具'
        },
        {
          'label': '采购内容',
          'text': '塑料托盘 1200× 1000× 500',
          'full': true
        },
        {
          'label': '数量合计',
          'text': '500'
        },
        {
          'label': '订单金额',
          'text': '42,500.00 CNY'
        },
        {
          'label': '交货日期',
          'text': '2026-09-08'
        },
        {
          'label': '参考关联销售订单',
          'text': '——',
          'full': true
        },
        {
          'label': '制单人',
          'text': '李国栋'
        },
        {
          'label': '审核人',
          'text': '张伟'
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['零件号', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['PLT-1210P', '塑料托盘 1200×1000×500', '块', '500', '85.00', '13%', '96.05', '48,025.00']
        },
        {
          'cells': ['', '合计', '', '500', '', '', '', '42,500.00']
        }
      ],
      'chain': [
        {
          'role': '采购订单（本单）',
          'name': 'PO-20260830-016',
          'self': true
        },
        {
          'role': '采购入库',
          'name': 'CGRK-20260825-006 · 已入库',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '应付账单',
          'name': '采购应付',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-30 09:20',
          'text': '制单 · 器具采购（塑料托盘 500 块）',
          'who': '李国栋'
        },
        {
          't': '08-31 14:10',
          'text': '审核通过',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '在途 · 按交期 09-08 到货验收',
          'off': true
        }
      ]
    },
    'PO-20260828-015': {
      'row': {"fields": {"supplier": "苏州联恒五金制品有限公司", "mtype": "零部件", "summary": "箱盖 ABS 吸塑×2,000", "date": "2026-09-05", "so": "SO-20260827-0039", "status": "已审核"}, "cells": ["苏州联恒五金制品有限公司", "<span class=\"tag tag-blue\">零部件</span>", "箱盖 ABS 吸塑×2,000", "<span class=\"td-num\">2,000</span>", "<span class=\"td-num\">6,300.00</span>", "CNY", "2026-09-05", "<span class=\"lk\">SO-20260827-0039</span>", "<span class=\"tag tag-blue\">已审核</span>"], "ops": [{"t": "生成入库单", "act": "go('../采购管理/采购入库列表.html')"}, {"t": "关闭"}]},
      'title': '采购订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'PO-20260828-015',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已审核'
        },
        {
          'label': '供应商',
          'text': '苏州联恒五金制品有限公司',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '零部件'
        },
        {
          'label': '采购内容',
          'text': '箱盖 ABS 吸塑× 2,000',
          'full': true
        },
        {
          'label': '数量合计',
          'text': '2,000 件'
        },
        {
          'label': '订单金额',
          'text': '6,300.00 CNY'
        },
        {
          'label': '交货日期',
          'text': '2026-09-05'
        },
        {
          'label': '参考关联销售订单',
          'text': 'SO-20260827-0039（参考 · 不以销定采）',
          'url': '销售管理/销售订单列表.html',
          'full': true
        },
        {
          'label': '制单人',
          'text': '李国栋'
        },
        {
          'label': '审核人',
          'text': '张伟'
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['零件号', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['LJ-D400', '箱盖 ABS 吸塑', '件', '2,000', '3.15', '13%', '3.56', '7,120.00']
        },
        {
          'cells': ['', '合计', '', '2,000', '', '', '', '6,300.00']
        }
      ],
      'chain': [
        {
          'role': '销售订单（参考）',
          'name': 'SO-20260827-0039',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '采购订单（本单）',
          'name': 'PO-20260828-015 · 独立采购线',
          'self': true
        },
        {
          'role': '采购入库',
          'name': 'CGRK-20260828-012 · 已入库',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '应付账单',
          'name': 'AP-20260901-008 · 采购应付',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-28 11:05',
          'text': '制单 · 零部件采购（箱盖 2,000 件）',
          'who': '李国栋'
        },
        {
          't': '08-29 09:30',
          'text': '审核通过',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '在途 · 按交期 09-05 到货验收',
          'off': true
        }
      ]
    },
    'PO-20260825-014': {
      'row': {"fields": {"supplier": "宁波华塑包装制品有限公司", "mtype": "器具", "summary": "料箱 600×400×340×800", "date": "2026-09-02", "so": "—", "status": "已完成"}, "cells": ["宁波华塑包装制品有限公司", "<span class=\"tag tag-green\">器具</span>", "料箱 600×400×340×800", "<span class=\"td-num\">800</span>", "<span class=\"td-num\">35,200.00</span>", "CNY", "2026-09-02", "—", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "入库记录", "act": "go('../采购管理/采购入库列表.html')"}]},
      'title': '采购订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'PO-20260825-014',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '供应商',
          'text': '宁波华塑包装制品有限公司',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '器具'
        },
        {
          'label': '采购内容',
          'text': '料箱 600× 400× 340× 800',
          'full': true
        },
        {
          'label': '数量合计',
          'text': '800'
        },
        {
          'label': '订单金额',
          'text': '35,200.00 CNY'
        },
        {
          'label': '交货日期',
          'text': '2026-09-02'
        },
        {
          'label': '参考关联销售订单',
          'text': '——',
          'full': true
        },
        {
          'label': '制单人',
          'text': '李国栋'
        },
        {
          'label': '审核人',
          'text': '张伟'
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['零件号', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['BTC-6040', '料箱 600×400×340', '只', '800', '44.00', '13%', '49.72', '39,776.00']
        },
        {
          'cells': ['', '合计', '', '800', '', '', '', '35,200.00']
        }
      ],
      'chain': [
        {
          'role': '采购订单（本单）',
          'name': 'PO-20260825-014',
          'self': true
        },
        {
          'role': '采购入库',
          'name': 'CGRK-20260826-008',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '应付账单',
          'name': 'AP-20260901-008 · 采购应付',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-25 10:15',
          'text': '制单 · 器具采购（料箱 800 只）',
          'who': '李国栋'
        },
        {
          't': '08-26 09:00',
          'text': '审核通过',
          'who': '张伟'
        },
        {
          't': '08-26',
          'text': '采购入库 · CGRK-20260826-008 验收通过',
          'who': '张伟'
        },
        {
          't': '09-01',
          'text': '应付账单自动生成 · AP-20260901-008',
          'who': '系统'
        }
      ]
    },
    'PO-20260820-013': {
      'row': {"fields": {"supplier": "常州正大塑料托盘厂", "mtype": "器具", "summary": "木托盘 1200×1000×400", "date": "2026-08-30", "so": "—", "status": "已完成"}, "cells": ["常州正大塑料托盘厂", "<span class=\"tag tag-green\">器具</span>", "木托盘 1200×1000×400", "<span class=\"td-num\">400</span>", "<span class=\"td-num\">19,600.00</span>", "CNY", "2026-08-30", "—", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "入库记录", "act": "go('../采购管理/采购入库列表.html')"}]},
      'title': '采购订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'PO-20260820-013',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '供应商',
          'text': '常州正大塑料托盘厂',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '器具'
        },
        {
          'label': '采购内容',
          'text': '木托盘 1200× 1000× 400',
          'full': true
        },
        {
          'label': '数量合计',
          'text': '400'
        },
        {
          'label': '订单金额',
          'text': '19,600.00 CNY'
        },
        {
          'label': '交货日期',
          'text': '2026-08-30'
        },
        {
          'label': '参考关联销售订单',
          'text': '——',
          'full': true
        },
        {
          'label': '制单人',
          'text': '李国栋'
        },
        {
          'label': '审核人',
          'text': '张伟'
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['零件号', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['PLT-1210W', '木托盘 1200×1000×400', '块', '400', '49.00', '13%', '55.37', '22,148.00']
        },
        {
          'cells': ['', '合计', '', '400', '', '', '', '19,600.00']
        }
      ],
      'chain': [
        {
          'role': '采购订单（本单）',
          'name': 'PO-20260820-013',
          'self': true
        },
        {
          'role': '采购入库',
          'name': 'CGRK-20260827-010',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '应付账单',
          'name': 'AP-20260830-007 · 采购应付',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-20 13:30',
          'text': '制单 · 器具采购（木托盘 400 块）',
          'who': '李国栋'
        },
        {
          't': '08-21 10:20',
          'text': '审核通过',
          'who': '张伟'
        },
        {
          't': '08-27',
          'text': '采购入库 · CGRK-20260827-010 验收通过',
          'who': '李国栋'
        },
        {
          't': '08-30',
          'text': '应付账单自动生成 · AP-20260830-007',
          'who': '系统'
        }
      ]
    },
    'PO-20260815-012': {
      'row': {"fields": {"supplier": "苏州联恒五金制品有限公司", "mtype": "零部件", "summary": "内衬 EPE 珍珠棉×3,000", "date": "2026-08-25", "so": "—", "status": "已关闭"}, "cells": ["苏州联恒五金制品有限公司", "<span class=\"tag tag-blue\">零部件</span>", "内衬 EPE 珍珠棉×3,000", "<span class=\"td-num\">3,000</span>", "<span class=\"td-num\">4,500.00</span>", "CNY", "2026-08-25", "—", "<span class=\"tag tag-gray\">已关闭</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '采购订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'PO-20260815-012',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已关闭'
        },
        {
          'label': '供应商',
          'text': '苏州联恒五金制品有限公司',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '零部件'
        },
        {
          'label': '采购内容',
          'text': '内衬 EPE 珍珠棉× 3,000',
          'full': true
        },
        {
          'label': '数量合计',
          'text': '3,000 件'
        },
        {
          'label': '订单金额',
          'text': '4,500.00 CNY'
        },
        {
          'label': '交货日期',
          'text': '2026-08-25'
        },
        {
          'label': '参考关联销售订单',
          'text': '——',
          'full': true
        },
        {
          'label': '制单人',
          'text': '李国栋'
        },
        {
          'label': '审核人',
          'text': '—'
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['零件号', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['LJ-F600', '内衬 EPE 珍珠棉', '件', '3,000', '1.50', '13%', '1.69', '5,070.00']
        },
        {
          'cells': ['', '合计', '', '3,000', '', '', '', '4,500.00']
        }
      ],
      'chain': [
        {
          'role': '采购订单（本单）',
          'name': 'PO-20260815-012 · 已关闭',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '08-15 15:10',
          'text': '制单 · 零部件采购（内衬 3,000 件）',
          'who': '李国栋'
        },
        {
          't': '08-18 09:40',
          'text': '审核通过',
          'who': '张伟'
        },
        {
          't': '08-24',
          'text': '部分到货 · CGRK-20260824-005',
          'who': '李国栋'
        },
        {
          't': '09-01',
          'text': '订单关闭 · 需求变更终止后续到货',
          'who': '李国栋'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 销售订单 salesOrders：键 = SO 订单号（销售管理/销售订单列表.html 8 行全量） */
  /* 订单唯一来源=项目经理代下；客户自助为演示例外 */
  salesOrders: {
    'SO-20260903-0047': {
      'row': {"fields": {"customer": "上汽大众汽车有限公司宁波分公司", "project": "PRJ-2602", "summary": "冲压件隔板×2,400（先采后销 · 采购在途）", "mode": "项目经理代下", "status": "待发货", "agent": "王强", "date": "2026-09-03"}, "note": "1", "cells": ["上汽大众汽车有限公司宁波分公司", "PRJ-2602", "冲压件隔板×2,400（先采后销 · 采购在途）", "<span class=\"td-num\">2,400</span>", "<span class=\"td-num\">28,800.00</span>", "<span class=\"tag tag-blue\">项目经理代下</span>", "<span class=\"tag tag-blue\">待发货</span>", "王强", "2026-09-03 11:20"], "ops": [{"t": "编辑", "act": "openModal('createModal')"}, {"t": "审核", "act": "openModal('auditModal')"}, {"t": "关闭"}]},
      'title': '销售订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'SO-20260903-0047',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待发货'
        },
        {
          'label': '客户',
          'text': '上汽大众汽车有限公司宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '订单内容',
          'text': '冲压件隔板× 2,400',
          'full': true
        },
        {
          'label': '数量',
          'text': '2,400 件'
        },
        {
          'label': '订单金额',
          'text': '28,800.00 元'
        },
        {
          'label': '下单方式',
          'text': '项目经理代下（订单唯一来源）',
          'full': true
        },
        {
          'label': '业务员',
          'text': '王强'
        },
        {
          'label': '下单时间',
          'text': '2026-09-03 11:20'
        },
        {
          'label': '备注',
          'text': '先采后销 · 采购在途，库存到位后发货',
          'full': true
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['物料', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['GB-2602', '冲压件隔板', '件', '2,400', '12.00', '13%', '13.56', '32,544.00']
        },
        {
          'cells': ['', '合计', '', '2,400', '', '', '', '28,800.00']
        }
      ],
      'chain': [
        {
          'role': '客户 PO',
          'name': '项目经理代下（唯一来源）'
        },
        {
          'role': '销售订单（本单）',
          'name': 'SO-20260903-0047',
          'self': true
        },
        {
          'role': '采购订单（先采后销）',
          'name': 'PO-20260903-019 · 在途',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '销售出库',
          'name': '按库存可用量发货',
          'url': '销售管理/销售出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-03 11:20',
          'text': '项目经理代下订单 · 先采后销',
          'who': '王强'
        },
        {
          't': '09-03 11:30',
          'text': '审核通过 · 待采购入库到位',
          'who': '王强'
        },
        {
          't': '—',
          'text': '待发货 · 库存可用量满足后转销售出库',
          'off': true
        }
      ]
    },
    'SO-20260902-0046': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "project": "PRJ-2601", "summary": "锁扣组件×3,000", "mode": "项目经理代下", "status": "待审核", "agent": "王强", "date": "2026-09-02"}, "cells": ["一汽解放汽车有限公司", "PRJ-2601", "锁扣组件×3,000", "<span class=\"td-num\">3,000</span>", "<span class=\"td-num\">4,800.00</span>", "<span class=\"tag tag-blue\">项目经理代下</span>", "<span class=\"tag tag-orange\">待审核</span>", "王强", "2026-09-02 10:24"], "ops": [{"t": "编辑", "act": "openModal('createModal')"}, {"t": "审核", "act": "openModal('auditModal')"}, {"t": "关闭"}]},
      'title': '销售订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'SO-20260902-0046',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '订单内容',
          'text': '锁扣组件× 3,000',
          'full': true
        },
        {
          'label': '数量',
          'text': '3,000 件'
        },
        {
          'label': '订单金额',
          'text': '4,800.00 元'
        },
        {
          'label': '下单方式',
          'text': '项目经理代下（订单唯一来源）',
          'full': true
        },
        {
          'label': '业务员',
          'text': '王强'
        },
        {
          'label': '下单时间',
          'text': '2026-09-02 10:24'
        },
        {
          'label': '备注',
          'text': '关联采购订单在途',
          'full': true
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['物料', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['LJ-A100', '锁扣组件 不锈钢 304', '件', '3,000', '1.60', '13%', '1.81', '5,430.00']
        },
        {
          'cells': ['', '合计', '', '3,000', '', '', '', '4,800.00']
        }
      ],
      'chain': [
        {
          'role': '客户 PO',
          'name': '项目经理代下（唯一来源）'
        },
        {
          'role': '销售订单（本单）',
          'name': 'SO-20260902-0046',
          'self': true
        },
        {
          'role': '采购订单（参考）',
          'name': 'PO-20260902-018 · 在途',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '销售出库',
          'name': '审核通过后发货',
          'url': '销售管理/销售出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-02 10:24',
          'text': '项目经理代下订单',
          'who': '王强'
        },
        {
          't': '—',
          'text': '待审核 · 通过后按库存可用量发货',
          'off': true
        }
      ]
    },
    'SO-20260901-0045': {
      'row': {"fields": {"customer": "上汽大众汽车有限公司宁波分公司", "project": "PRJ-2602", "summary": "铰链×1,200 / 箱盖×800", "mode": "客户自助", "status": "待审核", "agent": "何静", "date": "2026-09-01", "po": "—"}, "cells": ["上汽大众汽车有限公司宁波分公司", "PRJ-2602", "铰链×1,200 / 箱盖×800", "<span class=\"td-num\">2,000</span>", "<span class=\"td-num\">6,050.00</span>", "<span class=\"tag tag-gray\">客户自助</span>", "<span class=\"tag tag-orange\">待审核</span>", "何静", "2026-09-01 16:40"], "ops": [{"t": "编辑", "act": "openModal('createModal')"}, {"t": "审核", "act": "openModal('auditModal')"}, {"t": "关闭"}]},
      'title': '销售订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'SO-20260901-0045',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '客户',
          'text': '上汽大众汽车有限公司宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '订单内容',
          'text': '铰链× 1,200 / 箱盖 ABS 吸塑× 800',
          'full': true
        },
        {
          'label': '数量',
          'text': '2,000 件'
        },
        {
          'label': '订单金额',
          'text': '6,050.00 元'
        },
        {
          'label': '下单方式',
          'text': '客户自助（例外 · 演示保留）',
          'full': true
        },
        {
          'label': '业务员',
          'text': '何静'
        },
        {
          'label': '下单时间',
          'text': '2026-09-01 16:40'
        },
        {
          'label': '备注',
          'text': '库存销售 · 原料区现货可发',
          'full': true
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['物料', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['LJ-B200', '铰链 锌合金 65mm', '件', '1,200', '1.60', '13%', '1.81', '2,172.00']
        },
        {
          'cells': ['LJ-D400', '箱盖 ABS 吸塑', '件', '800', '—', '13%', '—', '4,130.00']
        },
        {
          'cells': ['', '合计', '', '2,000', '', '', '', '6,050.00']
        }
      ],
      'chain': [
        {
          'role': '客户 PO',
          'name': '客户自助（例外）'
        },
        {
          'role': '销售订单（本单）',
          'name': 'SO-20260901-0045',
          'self': true
        },
        {
          'role': '销售出库',
          'name': '审核通过后发货',
          'url': '销售管理/销售出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-01 16:40',
          'text': '客户下单 · 铰链 / 箱盖',
          'who': '何静'
        },
        {
          't': '—',
          'text': '待审核 · 通过后按库存可用量发货',
          'off': true
        }
      ]
    },
    'SO-20260831-0044': {
      'row': {"fields": {"customer": "小鹏汽车科技有限公司", "project": "PRJ-2603", "summary": "内衬 EPE 珍珠棉×5,000", "mode": "项目经理代下", "status": "已审核", "agent": "陈金", "date": "2026-08-31", "po": "—"}, "cells": ["小鹏汽车科技有限公司", "PRJ-2603", "内衬 EPE 珍珠棉×5,000", "<span class=\"td-num\">5,000</span>", "<span class=\"td-num\">9,000.00</span>", "<span class=\"tag tag-blue\">项目经理代下</span>", "<span class=\"tag tag-blue\">已审核</span>", "陈金", "2026-08-31 11:05"], "ops": [{"t": "发货", "act": "go('../销售管理/销售出库列表.html')"}, {"t": "关闭"}]},
      'title': '销售订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'SO-20260831-0044',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已审核'
        },
        {
          'label': '客户',
          'text': '小鹏汽车科技有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2603'
        },
        {
          'label': '订单内容',
          'text': '内衬 EPE 珍珠棉× 5,000',
          'full': true
        },
        {
          'label': '数量',
          'text': '5,000 件'
        },
        {
          'label': '订单金额',
          'text': '9,000.00 元'
        },
        {
          'label': '下单方式',
          'text': '项目经理代下（订单唯一来源）',
          'full': true
        },
        {
          'label': '业务员',
          'text': '陈金'
        },
        {
          'label': '下单时间',
          'text': '2026-08-31 11:05'
        },
        {
          'label': '备注',
          'text': '库存销售 · 按可用量排期发货',
          'full': true
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['物料', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['LJ-F600', '内衬 EPE 珍珠棉', '件', '5,000', '1.80', '13%', '2.03', '10,150.00']
        },
        {
          'cells': ['', '合计', '', '5,000', '', '', '', '9,000.00']
        }
      ],
      'chain': [
        {
          'role': '客户 PO',
          'name': '项目经理代下（唯一来源）'
        },
        {
          'role': '销售订单（本单）',
          'name': 'SO-20260831-0044',
          'self': true
        },
        {
          'role': '销售出库',
          'name': '待发货',
          'url': '销售管理/销售出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-31 11:05',
          'text': '项目经理代下订单',
          'who': '陈金'
        },
        {
          't': '08-31 15:20',
          'text': '审核通过',
          'who': '王强'
        },
        {
          't': '—',
          'text': '待发货 · 按库存可用量排期',
          'off': true
        }
      ]
    },
    'SO-20260830-0043': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "project": "PRJ-2601", "summary": "箱盖 ABS 吸塑×1,500", "mode": "客户自助", "status": "待发货", "agent": "袁明", "date": "2026-08-30", "po": "—"}, "cells": ["一汽解放汽车有限公司", "PRJ-2601", "箱盖 ABS 吸塑×1,500", "<span class=\"td-num\">1,500</span>", "<span class=\"td-num\">5,400.00</span>", "<span class=\"tag tag-gray\">客户自助</span>", "<span class=\"tag tag-blue\">待发货</span>", "袁明", "2026-08-30 09:18"], "ops": [{"t": "发货", "act": "go('../销售管理/销售出库列表.html')"}, {"t": "关闭"}]},
      'title': '销售订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'SO-20260830-0043',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待发货'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '订单内容',
          'text': '箱盖 ABS 吸塑× 1,500',
          'full': true
        },
        {
          'label': '数量',
          'text': '1,500 件'
        },
        {
          'label': '订单金额',
          'text': '5,400.00 元'
        },
        {
          'label': '下单方式',
          'text': '客户自助（例外 · 演示保留）',
          'full': true
        },
        {
          'label': '业务员',
          'text': '袁明'
        },
        {
          'label': '下单时间',
          'text': '2026-08-30 09:18'
        },
        {
          'label': '备注',
          'text': '库存销售 · 已排产备货',
          'full': true
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['物料', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['LJ-D400', '箱盖 ABS 吸塑', '件', '1,500', '3.60', '13%', '4.07', '6,105.00']
        },
        {
          'cells': ['', '合计', '', '1,500', '', '', '', '5,400.00']
        }
      ],
      'chain': [
        {
          'role': '客户 PO',
          'name': '客户自助（例外）'
        },
        {
          'role': '销售订单（本单）',
          'name': 'SO-20260830-0043',
          'self': true
        },
        {
          'role': '销售出库',
          'name': 'XSCK-20260902-015 · 待审核',
          'url': '销售管理/销售出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-30 09:18',
          'text': '客户下单 · 箱盖 1,500 件',
          'who': '袁明'
        },
        {
          't': '08-30 14:40',
          'text': '审核通过',
          'who': '王强'
        },
        {
          't': '09-02',
          'text': '销售出库制单 · XSCK-20260902-015（在库 980 + 在途补充）',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '待出库审核 · 通过后生成销售费应收',
          'off': true
        }
      ]
    },
    'SO-20260828-0041': {
      'row': {"fields": {"customer": "东风本田汽车有限公司", "project": "PRJ-2604", "summary": "锁扣组件×800", "mode": "项目经理代下", "status": "已完成", "agent": "王强", "date": "2026-08-28"}, "cells": ["东风本田汽车有限公司", "PRJ-2604", "锁扣组件×800", "<span class=\"td-num\">800</span>", "<span class=\"td-num\">1,280.00</span>", "<span class=\"tag tag-blue\">项目经理代下</span>", "<span class=\"tag tag-green\">已完成</span>", "王强", "2026-08-28 15:52"], "ops": [{"t": "详情", "detail": true}]},
      'title': '销售订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'SO-20260828-0041',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '客户',
          'text': '东风本田汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2604'
        },
        {
          'label': '订单内容',
          'text': '锁扣组件× 800',
          'full': true
        },
        {
          'label': '数量',
          'text': '800 件'
        },
        {
          'label': '订单金额',
          'text': '1,280.00 元'
        },
        {
          'label': '下单方式',
          'text': '项目经理代下（订单唯一来源）',
          'full': true
        },
        {
          'label': '业务员',
          'text': '王强'
        },
        {
          'label': '下单时间',
          'text': '2026-08-28 15:52'
        },
        {
          'label': '备注',
          'text': '已完成发货与应收结转',
          'full': true
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['物料', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['LJ-A100', '锁扣组件 不锈钢 304', '件', '800', '1.60', '13%', '1.81', '1,448.00']
        },
        {
          'cells': ['', '合计', '', '800', '', '', '', '1,280.00']
        }
      ],
      'chain': [
        {
          'role': '客户 PO',
          'name': '项目经理代下（唯一来源）'
        },
        {
          'role': '销售订单（本单）',
          'name': 'SO-20260828-0041',
          'self': true
        },
        {
          'role': '销售出库',
          'name': 'XSCK-20260901-014',
          'url': '销售管理/销售出库列表.html'
        },
        {
          'role': '应收账单',
          'name': '销售费 · 已汇总',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-28 15:52',
          'text': '项目经理代下订单',
          'who': '王强'
        },
        {
          't': '08-29 09:00',
          'text': '审核通过',
          'who': '王强'
        },
        {
          't': '09-01',
          'text': '销售出库 · XSCK-20260901-014（800 件）',
          'who': '张伟'
        },
        {
          't': '09-02',
          'text': '销售费应收生成 · AR-2026-09-PRJ2604-S1',
          'who': '系统'
        }
      ]
    },
    'SO-20260827-0039': {
      'row': {"fields": {"customer": "一汽解放汽车有限公司", "project": "PRJ-2601", "summary": "箱盖 ABS 吸塑×2,000", "mode": "客户自助", "status": "已完成", "agent": "袁明", "date": "2026-08-27"}, "cells": ["一汽解放汽车有限公司", "PRJ-2601", "箱盖 ABS 吸塑×2,000", "<span class=\"td-num\">2,000</span>", "<span class=\"td-num\">7,200.00</span>", "<span class=\"tag tag-gray\">客户自助</span>", "<span class=\"tag tag-green\">已完成</span>", "袁明", "2026-08-27 14:03"], "ops": [{"t": "详情", "detail": true}]},
      'title': '销售订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'SO-20260827-0039',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '订单内容',
          'text': '箱盖 ABS 吸塑× 2,000',
          'full': true
        },
        {
          'label': '数量',
          'text': '2,000 件'
        },
        {
          'label': '订单金额',
          'text': '7,200.00 元'
        },
        {
          'label': '下单方式',
          'text': '客户自助（例外 · 演示保留）',
          'full': true
        },
        {
          'label': '业务员',
          'text': '袁明'
        },
        {
          'label': '下单时间',
          'text': '2026-08-27 14:03'
        },
        {
          'label': '备注',
          'text': '已完成发货与应收结转',
          'full': true
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['物料', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['LJ-D400', '箱盖 ABS 吸塑', '件', '2,000', '3.60', '13%', '4.07', '8,140.00']
        },
        {
          'cells': ['', '合计', '', '2,000', '', '', '', '7,200.00']
        }
      ],
      'chain': [
        {
          'role': '客户 PO',
          'name': '客户自助（例外）'
        },
        {
          'role': '销售订单（本单）',
          'name': 'SO-20260827-0039',
          'self': true
        },
        {
          'role': '销售出库',
          'name': 'XSCK-20260829-013',
          'url': '销售管理/销售出库列表.html'
        },
        {
          'role': '应收账单',
          'name': '销售费 · 已汇总',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-27 14:03',
          'text': '客户下单 · 箱盖 2,000 件',
          'who': '袁明'
        },
        {
          't': '08-28 09:20',
          'text': '审核通过',
          'who': '王强'
        },
        {
          't': '08-29',
          'text': '销售出库 · XSCK-20260829-013（2,000 件）',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '销售费应收按出库汇总',
          'off': true
        }
      ]
    },
    'SO-20260820-0036': {
      'row': {"fields": {"customer": "上汽大众汽车有限公司宁波分公司", "project": "PRJ-2602", "summary": "铰链×600", "mode": "项目经理代下", "status": "已关闭", "agent": "王强", "date": "2026-08-20", "po": "—"}, "cells": ["上汽大众汽车有限公司宁波分公司", "PRJ-2602", "铰链×600", "<span class=\"td-num\">600</span>", "<span class=\"td-num\">1,890.00</span>", "<span class=\"tag tag-blue\">项目经理代下</span>", "<span class=\"tag tag-gray\">已关闭</span>", "王强", "2026-08-20 10:44"], "ops": [{"t": "详情", "detail": true}]},
      'title': '销售订单详情',
      'info': [
        {
          'label': '订单号',
          'text': 'SO-20260820-0036',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已关闭'
        },
        {
          'label': '客户',
          'text': '上汽大众汽车有限公司宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '订单内容',
          'text': '铰链× 600',
          'full': true
        },
        {
          'label': '数量',
          'text': '600 件'
        },
        {
          'label': '订单金额',
          'text': '1,890.00 元'
        },
        {
          'label': '下单方式',
          'text': '项目经理代下（订单唯一来源）',
          'full': true
        },
        {
          'label': '业务员',
          'text': '王强'
        },
        {
          'label': '下单时间',
          'text': '2026-08-20 10:44'
        },
        {
          'label': '备注',
          'text': '客户取消 · 单据关闭',
          'full': true
        }
      ],
      'feeSecTitle': '物料行',
      'feeCols': ['物料', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'fees': [
        {
          'cells': ['LJ-B200', '铰链 锌合金 65mm', '件', '600', '1.60', '13%', '1.81', '1,086.00']
        },
        {
          'cells': ['', '合计', '', '600', '', '', '', '1,890.00']
        }
      ],
      'chain': [
        {
          'role': '销售订单（本单）',
          'name': 'SO-20260820-0036 · 已关闭',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '08-20 10:44',
          'text': '项目经理代下订单 · 铰链 600 件',
          'who': '王强'
        },
        {
          't': '08-22 09:15',
          'text': '客户取消 · 单据关闭',
          'who': '王强'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 采购入库单 purchaseInbounds：键 = CGRK 入库单号（采购管理/采购入库列表.html 8 行全量） */
  /* 凭采购订单到货验收；验收通过生成采购应付 */
  purchaseInbounds: {
    'CGRK-20260828-012': {
      'row': {"fields": {"supplier": "苏州联恒五金制品有限公司", "project": "PRJ-2601", "bizType": "零部件采购", "status": "已入库", "inTime": "2026-08-28 14:32"}, "cells": ["苏州联恒五金制品有限公司", "<span class=\"lk\">PO-20260828-015</span>", "PRJ-2601", "零部件采购", "<span class=\"td-num\">40 托</span>", "原料区 RA", "<span class=\"tag tag-green\">已入库</span>", "张伟", "2026-08-28 14:32"], "ops": [{"t": "详情", "detail": true}, {"t": "验收", "act": "openModal('auditModal')"}, {"t": "打印", "act": "window.print();this.classList.toggle('printed')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'CGRK-20260828-012',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '采购入库单 · 零部件采购',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '供应商',
          'text': '苏州联恒五金制品有限公司',
          'full': true
        },
        {
          'label': '关联采购订单',
          'text': 'PO-20260828-015',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '到货数量',
          'text': '40 托 / 3,400 件'
        },
        {
          'label': '入库库区',
          'text': '原料区 RA'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '入库时间',
          'text': '2026-08-28 14:32'
        },
        {
          'label': '验收方式',
          'text': '凭采购订单到货验收',
          'full': true
        },
        {
          'label': '备注',
          'text': '验收通过后库存入账，并可生成应付账单',
          'full': true
        }
      ],
      'feeSecTitle': '到货明细',
      'feeCols': ['序号', '零件号', '名称规格', '单位', '托数 × 件数', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次', '库位'],
      'fees': [
        {
          'cells': ['1', 'LJ-A100', '锁扣组件 不锈钢 304', '件', '24 托 × 100', '4.80', '13%', '5.42', '13,008.00', 'B20260828-01', 'RA-A-01-02']
        },
        {
          'cells': ['2', 'LJ-B200', '铰链 锌合金 65mm', '件', '16 托 × 125', '1.60', '13%', '1.81', '3.62', 'B20260828-02', 'RA-A-01-03']
        }
      ],
      'chain': [
        {
          'role': '采购订单',
          'name': 'PO-20260828-015',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '采购入库（本单）',
          'name': 'CGRK-20260828-012',
          'self': true
        },
        {
          'role': '库存台账',
          'name': '原料区 RA · LJ-A100 / LJ-B200',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '应付账单',
          'name': '验收通过后生成（采购应付）',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-28 09:40',
          'text': '到货登记 · 苏州联恒送货到达原料区 RA（40 托）',
          'who': '张伟'
        },
        {
          't': '08-28 11:20',
          'text': '数量清点 · 40 托 / 3,400 件，与采购订单一致',
          'who': '张伟'
        },
        {
          't': '08-28 14:10',
          'text': '质检验收 · 抽检合格，验收通过',
          'who': '张伟'
        },
        {
          't': '08-28 14:32',
          'text': '入库完成 · 库存入账（原料区 RA）',
          'who': '系统'
        },
        {
          't': '—',
          'text': '应付账单 · 待按验收结果生成',
          'who': '系统',
          'off': true
        }
      ]
    },
    'CGRK-20260828-011': {
      'row': {"fields": {"supplier": "宁波华塑包装制品有限公司", "project": "PRJ-2601", "bizType": "器具采购", "status": "已入库", "inTime": "2026-08-28 10:05"}, "note": "2", "cells": ["宁波华塑包装制品有限公司", "<span class=\"lk\">PO-20260901-017</span>", "PRJ-2601", "器具采购", "<span class=\"td-num\">25 托</span>", "原料区 RA", "<span class=\"tag tag-green\">已入库</span>", "张伟", "2026-08-28 10:05"], "ops": [{"t": "详情", "detail": true}, {"t": "验收", "act": "openModal('auditModal')"}, {"t": "打印", "act": "window.print();this.classList.toggle('printed')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'CGRK-20260828-011',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '采购入库单 · 器具采购',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '供应商',
          'text': '宁波华塑包装制品有限公司',
          'full': true
        },
        {
          'label': '关联采购订单',
          'text': 'PO-20260901-017',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '到货数量',
          'text': '25 托'
        },
        {
          'label': '入库库区',
          'text': '原料区 RA'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '入库时间',
          'text': '2026-08-28 10:05'
        },
        {
          'label': '验收方式',
          'text': '凭采购订单到货验收',
          'full': true
        },
        {
          'label': '备注',
          'text': '验收通过后库存入账，并可生成应付账单',
          'full': true
        }
      ],
      'feeSecTitle': '到货明细',
      'feeCols': ['序号', '零件号', '名称规格', '单位', '托数 × 件数', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次', '库位'],
      'fees': [
        {
          'cells': ['1', 'WBX-1210L', '围板箱 1200×1000×970', '只', '25 托 × 12', '280.00', '13%', '316.40', '94,920.00', 'B20260828-11', 'RA-A-01-05']
        }
      ],
      'chain': [
        {
          'role': '采购订单',
          'name': 'PO-20260901-017',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '采购入库（本单）',
          'name': 'CGRK-20260828-011',
          'self': true
        },
        {
          'role': '库存台账',
          'name': '原料区 RA · WBX-1210L',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '应付账单',
          'name': '验收通过后生成（采购应付）',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-28 09:10',
          'text': '到货登记 · 宁波华塑围板箱 300 只',
          'who': '张伟'
        },
        {
          't': '08-28 09:50',
          'text': '数量清点 · 与采购订单一致',
          'who': '张伟'
        },
        {
          't': '08-28 10:05',
          'text': '验收通过 · 库存入账（原料区 RA）',
          'who': '系统'
        },
        {
          't': '—',
          'text': '应付账单 · 待按验收结果生成',
          'who': '系统',
          'off': true
        }
      ]
    },
    'CGRK-20260827-010': {
      'row': {"fields": {"supplier": "常州正大塑料托盘厂", "project": "PRJ-2602", "bizType": "器具采购", "status": "已入库", "inTime": "2026-08-27 16:44"}, "cells": ["常州正大塑料托盘厂", "<span class=\"lk\">PO-20260820-013</span>", "PRJ-2602", "器具采购", "<span class=\"td-num\">18 托</span>", "成品区 RB", "<span class=\"tag tag-green\">已入库</span>", "李国栋", "2026-08-27 16:44"], "ops": [{"t": "详情", "detail": true}, {"t": "验收", "act": "openModal('auditModal')"}, {"t": "打印", "act": "window.print();this.classList.toggle('printed')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'CGRK-20260827-010',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '采购入库单 · 器具采购',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '供应商',
          'text': '常州正大塑料托盘厂',
          'full': true
        },
        {
          'label': '关联采购订单',
          'text': 'PO-20260820-013',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '到货数量',
          'text': '18 托'
        },
        {
          'label': '入库库区',
          'text': '成品区 RB'
        },
        {
          'label': '制单人',
          'text': '李国栋'
        },
        {
          'label': '入库时间',
          'text': '2026-08-27 16:44'
        },
        {
          'label': '验收方式',
          'text': '凭采购订单到货验收',
          'full': true
        },
        {
          'label': '备注',
          'text': '验收通过后库存入账，并可生成应付账单',
          'full': true
        }
      ],
      'feeSecTitle': '到货明细',
      'feeCols': ['序号', '零件号', '名称规格', '单位', '托数 × 件数', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次', '库位'],
      'fees': [
        {
          'cells': ['1', 'PLT-1210W', '木托盘 1200×1000×400', '块', '18 托 · 400 块', '49.00', '13%', '55.37', '22,148.00', 'B20260827-10', 'RB-B-01-02']
        }
      ],
      'chain': [
        {
          'role': '采购订单',
          'name': 'PO-20260820-013',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '采购入库（本单）',
          'name': 'CGRK-20260827-010',
          'self': true
        },
        {
          'role': '库存台账',
          'name': '成品区 RB · PLT-1210W',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '应付账单',
          'name': 'AP-20260830-007 · 已生成',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-27 14:30',
          'text': '到货登记 · 常州正大木托盘 400 块',
          'who': '李国栋'
        },
        {
          't': '08-27 16:20',
          'text': '数量清点 · 与采购订单一致',
          'who': '李国栋'
        },
        {
          't': '08-27 16:44',
          'text': '验收通过 · 库存入账（成品区 RB）',
          'who': '系统'
        },
        {
          't': '08-30',
          'text': '应付账单自动生成 · AP-20260830-007',
          'who': '系统'
        }
      ]
    },
    'CGRK-20260827-009': {
      'row': {"fields": {"supplier": "苏州联恒五金制品有限公司", "project": "PRJ-2602", "bizType": "零部件采购", "status": "待验收", "inTime": "2026-08-27 09:20"}, "cells": ["苏州联恒五金制品有限公司", "<span class=\"lk\">PO-20260902-018</span>", "PRJ-2602", "零部件采购", "<span class=\"td-num\">12 托</span>", "原料区 RA", "<span class=\"tag tag-orange\">待验收</span>", "李国栋", "2026-08-27 09:20"], "ops": [{"t": "详情", "detail": true}, {"t": "验收", "act": "openModal('auditModal')"}, {"t": "打印", "act": "window.print();this.classList.toggle('printed')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'CGRK-20260827-009',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '采购入库单 · 零部件采购',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待验收'
        },
        {
          'label': '供应商',
          'text': '苏州联恒五金制品有限公司',
          'full': true
        },
        {
          'label': '关联采购订单',
          'text': 'PO-20260902-018',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '到货数量',
          'text': '12 托'
        },
        {
          'label': '入库库区',
          'text': '原料区 RA'
        },
        {
          'label': '制单人',
          'text': '李国栋'
        },
        {
          'label': '入库时间',
          'text': '2026-08-27 09:20'
        },
        {
          'label': '验收方式',
          'text': '凭采购订单到货验收',
          'full': true
        },
        {
          'label': '备注',
          'text': '验收通过后库存入账，并可生成应付账单',
          'full': true
        }
      ],
      'feeSecTitle': '到货明细',
      'feeCols': ['序号', '零件号', '名称规格', '单位', '托数 × 件数', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次', '库位'],
      'fees': [
        {
          'cells': ['1', 'LJ-A100', '锁扣组件 不锈钢 304', '件', '8 托 × 100', '1.90', '13%', '2.15', '1,720.00', 'B20260827-09', 'RA-A-01-01']
        },
        {
          'cells': ['2', 'LJ-B200', '铰链 锌合金 65mm', '件', '4 托 × 125', '1.60', '13%', '1.81', '3.62', 'B20260827-09', 'RA-A-01-01']
        }
      ],
      'chain': [
        {
          'role': '采购订单',
          'name': 'PO-20260902-018',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '采购入库（本单）',
          'name': 'CGRK-20260827-009 · 待验收',
          'self': true
        },
        {
          'role': '库存台账',
          'name': '验收通过后入账',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-27 09:20',
          'text': '到货登记 · 苏州联恒零部件 12 托',
          'who': '李国栋'
        },
        {
          't': '—',
          'text': '待验收 · 验收通过后库存入账并生成应付',
          'off': true
        }
      ]
    },
    'CGRK-20260826-008': {
      'row': {"fields": {"supplier": "宁波华塑包装制品有限公司", "project": "PRJ-2603", "bizType": "器具采购", "status": "已入库", "inTime": "2026-08-26 15:10"}, "cells": ["宁波华塑包装制品有限公司", "<span class=\"lk\">PO-20260825-014</span>", "PRJ-2603", "器具采购", "<span class=\"td-num\">9 托</span>", "原料区 RA", "<span class=\"tag tag-green\">已入库</span>", "张伟", "2026-08-26 15:10"], "ops": [{"t": "详情", "detail": true}, {"t": "验收", "act": "openModal('auditModal')"}, {"t": "打印", "act": "window.print();this.classList.toggle('printed')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'CGRK-20260826-008',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '采购入库单 · 器具采购',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '供应商',
          'text': '宁波华塑包装制品有限公司',
          'full': true
        },
        {
          'label': '关联采购订单',
          'text': 'PO-20260825-014',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2603'
        },
        {
          'label': '到货数量',
          'text': '9 托'
        },
        {
          'label': '入库库区',
          'text': '原料区 RA'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '入库时间',
          'text': '2026-08-26 15:10'
        },
        {
          'label': '验收方式',
          'text': '凭采购订单到货验收',
          'full': true
        },
        {
          'label': '备注',
          'text': '验收通过后库存入账，并可生成应付账单',
          'full': true
        }
      ],
      'feeSecTitle': '到货明细',
      'feeCols': ['序号', '零件号', '名称规格', '单位', '托数 × 件数', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次', '库位'],
      'fees': [
        {
          'cells': ['1', 'BTC-6040', '料箱 600×400×340', '只', '9 托 · 800 只', '44.00', '13%', '49.72', '39,776.00', 'B20260826-08', 'RA-A-02-01']
        }
      ],
      'chain': [
        {
          'role': '采购订单',
          'name': 'PO-20260825-014',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '采购入库（本单）',
          'name': 'CGRK-20260826-008',
          'self': true
        },
        {
          'role': '库存台账',
          'name': '原料区 RA · BTC-6040',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '应付账单',
          'name': 'AP-20260901-008 · 已生成',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-26 13:40',
          'text': '到货登记 · 宁波华塑料箱 800 只',
          'who': '张伟'
        },
        {
          't': '08-26 14:50',
          'text': '数量清点 · 与采购订单一致',
          'who': '张伟'
        },
        {
          't': '08-26 15:10',
          'text': '验收通过 · 库存入账（原料区 RA）',
          'who': '系统'
        },
        {
          't': '09-01',
          'text': '应付账单自动生成 · AP-20260901-008',
          'who': '系统'
        }
      ]
    },
    'CGRK-20260825-006': {
      'row': {"fields": {"supplier": "常州正大塑料托盘厂", "project": "PRJ-2603", "bizType": "器具采购", "status": "已入库", "inTime": "2026-08-25 11:02"}, "cells": ["常州正大塑料托盘厂", "<span class=\"lk\">PO-20260830-016</span>", "PRJ-2603", "器具采购", "<span class=\"td-num\">22 托</span>", "成品区 RB", "<span class=\"tag tag-green\">已入库</span>", "张伟", "2026-08-25 11:02"], "ops": [{"t": "详情", "detail": true}, {"t": "验收", "act": "openModal('auditModal')"}, {"t": "打印", "act": "window.print();this.classList.toggle('printed')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'CGRK-20260825-006',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '采购入库单 · 器具采购',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '供应商',
          'text': '常州正大塑料托盘厂',
          'full': true
        },
        {
          'label': '关联采购订单',
          'text': 'PO-20260830-016',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2603'
        },
        {
          'label': '到货数量',
          'text': '22 托'
        },
        {
          'label': '入库库区',
          'text': '成品区 RB'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '入库时间',
          'text': '2026-08-25 11:02'
        },
        {
          'label': '验收方式',
          'text': '凭采购订单到货验收',
          'full': true
        },
        {
          'label': '备注',
          'text': '验收通过后库存入账，并可生成应付账单',
          'full': true
        }
      ],
      'feeSecTitle': '到货明细',
      'feeCols': ['序号', '零件号', '名称规格', '单位', '托数 × 件数', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次', '库位'],
      'fees': [
        {
          'cells': ['1', 'PLT-1210P', '塑料托盘 1200×1000', '块', '22 托 · 500 块', '85.00', '13%', '96.05', '48,025.00', 'B20260825-06', 'RB-B-02-01']
        }
      ],
      'chain': [
        {
          'role': '采购订单',
          'name': 'PO-20260830-016',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '采购入库（本单）',
          'name': 'CGRK-20260825-006',
          'self': true
        },
        {
          'role': '库存台账',
          'name': '成品区 RB · PLT-1210P',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '应付账单',
          'name': '验收通过后生成（采购应付）',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-25 09:30',
          'text': '到货登记 · 常州正大塑料托盘 500 块',
          'who': '张伟'
        },
        {
          't': '08-25 10:40',
          'text': '数量清点 · 与采购订单一致',
          'who': '张伟'
        },
        {
          't': '08-25 11:02',
          'text': '验收通过 · 库存入账（成品区 RB）',
          'who': '系统'
        },
        {
          't': '—',
          'text': '应付账单 · 待按验收结果生成',
          'who': '系统',
          'off': true
        }
      ]
    },
    'CGRK-20260824-005': {
      'row': {"fields": {"supplier": "苏州联恒五金制品有限公司", "project": "PRJ-2604", "bizType": "零部件采购", "status": "已入库", "inTime": "2026-08-24 14:18"}, "note": "1", "cells": ["苏州联恒五金制品有限公司", "<span class=\"lk\">PO-20260815-012</span>", "PRJ-2604", "零部件采购", "<span class=\"td-num\">6 托</span>", "原料区 RA", "<span class=\"tag tag-green\">已入库</span>", "李国栋", "2026-08-24 14:18"], "ops": [{"t": "详情", "detail": true}, {"t": "验收", "act": "openModal('auditModal')"}, {"t": "打印", "act": "window.print();this.classList.toggle('printed')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'CGRK-20260824-005',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '采购入库单 · 零部件采购',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '供应商',
          'text': '苏州联恒五金制品有限公司',
          'full': true
        },
        {
          'label': '关联采购订单',
          'text': 'PO-20260815-012',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2604'
        },
        {
          'label': '到货数量',
          'text': '6 托'
        },
        {
          'label': '入库库区',
          'text': '原料区 RA'
        },
        {
          'label': '制单人',
          'text': '李国栋'
        },
        {
          'label': '入库时间',
          'text': '2026-08-24 14:18'
        },
        {
          'label': '验收方式',
          'text': '凭采购订单到货验收',
          'full': true
        },
        {
          'label': '备注',
          'text': '验收通过后库存入账，并可生成应付账单',
          'full': true
        }
      ],
      'feeSecTitle': '到货明细',
      'feeCols': ['序号', '零件号', '名称规格', '单位', '托数 × 件数', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次', '库位'],
      'fees': [
        {
          'cells': ['1', 'LJ-F600', '内衬 EPE 珍珠棉', '件', '6 托 × 500', '1.50', '13%', '1.69', '5,070.00', 'B20260824-05', 'RA-A-03-01']
        }
      ],
      'chain': [
        {
          'role': '采购订单',
          'name': 'PO-20260815-012',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '采购入库（本单）',
          'name': 'CGRK-20260824-005',
          'self': true
        },
        {
          'role': '库存台账',
          'name': '原料区 RA · LJ-F600',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-24 13:20',
          'text': '到货登记 · 苏州联恒内衬 3,000 件',
          'who': '李国栋'
        },
        {
          't': '08-24 14:00',
          'text': '数量清点 · 与采购订单一致',
          'who': '李国栋'
        },
        {
          't': '08-24 14:18',
          'text': '验收通过 · 库存入账（原料区 RA）',
          'who': '系统'
        }
      ]
    },
    'CGRK-20260820-006': {
      'row': {"fields": {"supplier": "苏州联恒五金制品有限公司", "project": "PRJ-2604", "bizType": "器具采购", "status": "已入库", "inTime": "2026-08-20 14:30"}, "note": "3", "cells": ["苏州联恒五金制品有限公司", "<span class=\"lk\">PO-20260815-012</span>", "PRJ-2604", "器具采购", "<span class=\"td-num\">80 件（折叠隔板）</span>", "原料区 RA", "<span class=\"tag tag-green\">已入库</span>", "张伟", "2026-08-20 14:30"], "ops": [{"t": "详情", "detail": true}, {"t": "验收", "act": "openModal('auditModal')"}, {"t": "打印", "act": "window.print();this.classList.toggle('printed')"}]},
      'title': '采购入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'CGRK-20260820-006',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '采购入库单 · 器具采购',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '供应商',
          'text': '苏州联恒五金制品有限公司',
          'full': true
        },
        {
          'label': '关联采购订单',
          'text': 'PO-20260815-012',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2604'
        },
        {
          'label': '到货数量',
          'text': '80 件（折叠隔板）'
        },
        {
          'label': '入库库区',
          'text': '原料区 RA'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '入库时间',
          'text': '2026-08-20 14:30'
        },
        {
          'label': '验收方式',
          'text': '凭采购订单到货验收',
          'full': true
        },
        {
          'label': '备注',
          'text': '验收通过后库存入账，并可生成应付账单',
          'full': true
        }
      ],
      'feeSecTitle': '到货明细',
      'feeCols': ['序号', '零件号', '名称规格', '单位', '托数 × 件数', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次', '库位'],
      'fees': [
        {
          'cells': ['1', 'GB-800', '折叠隔板', '件', '80 件（折叠隔板）', '—', '13%', '—', '—', 'B20260820-06', 'RA-A-03-02']
        }
      ],
      'chain': [
        {
          'role': '采购订单',
          'name': 'PO-20260815-012',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '采购入库（本单）',
          'name': 'CGRK-20260820-006 · L4 自购侧',
          'self': true
        },
        {
          'role': '组装（混合配方）',
          'name': 'ZZ-20260822-006 · 隔板 × 80',
        }
      ],
      'timeline': [
        {
          't': '08-20 13:50',
          'text': '到货登记 · 折叠隔板 80 件（L4 混合线自购侧）',
          'who': '张伟'
        },
        {
          't': '08-20 14:30',
          'text': '验收通过 · 库存入账（原料区 RA）',
          'who': '系统'
        },
        {
          't': '08-22',
          'text': '混合组装领用 · ZZ-20260822-006',
          'who': '刘志强'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 销售出库单 salesOutbounds：键 = XSCK 出库单号（销售管理/销售出库列表.html 6 行全量） */
  /* 按库存可用量发货；销售费应收按出库自动汇总 */
  salesOutbounds: {
    'XSCK-20260902-015': {
      'row': {"fields": {"so": "SO-20260830-0043", "customer": "一汽解放汽车有限公司", "project": "PRJ-2601", "summary": "箱盖 ABS 吸塑×1,500", "warehouse": "原料区 RA", "date": "2026-09-02", "status": "待审核"}, "note": "1", "cells": ["<span class=\"lk\">SO-20260830-0043</span>", "一汽解放汽车有限公司", "PRJ-2601", "箱盖 ABS 吸塑×1,500", "<span class=\"td-num\">1,500</span>", "原料区 RA", "2026-09-02", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "审核", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}]},
      'title': '销售出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'XSCK-20260902-015',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '关联销售订单',
          'text': 'SO-20260830-0043',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '出库物料',
          'text': '箱盖 ABS 吸塑（LJ-D400）',
          'full': true
        },
        {
          'label': '数量',
          'text': '1,500 件'
        },
        {
          'label': '出库库区',
          'text': '原料区 RA'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '制单时间',
          'text': '2026-09-02 11:30'
        },
        {
          'label': '计价方式',
          'text': '销售价随订单（一进一出）',
          'full': true
        }
      ],
      'feeSecTitle': '出库明细',
      'feeCols': ['序号', '物料编码', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'LJ-D400', '箱盖 ABS 吸塑', '件', '1,500', '36.00', '13%', '40.68', '61,020.00', 'RA-A-02-01']
        }
      ],
      'chain': [
        {
          'role': '销售订单',
          'name': 'SO-20260830-0043',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '销售出库（本单）',
          'name': 'XSCK-20260902-015',
          'self': true
        },
        {
          'role': '应收账单',
          'name': '销售费 · 按出库自动汇总',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '09-02 11:30',
          'text': '制单 · 按订单可用量备货（LJ-D400 在库 980 + 在途补充）',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '待审核 · 通过后出库并生成销售费应收',
          'off': true
        }
      ]
    },
    'XSCK-20260901-014': {
      'row': {"fields": {"so": "SO-20260828-0041", "customer": "东风本田汽车有限公司", "project": "PRJ-2604", "summary": "锁扣组件×800", "warehouse": "原料区 RA", "date": "2026-09-01", "status": "已完成"}, "cells": ["<span class=\"lk\">SO-20260828-0041</span>", "东风本田汽车有限公司", "PRJ-2604", "锁扣组件×800", "<span class=\"td-num\">800</span>", "原料区 RA", "2026-09-01", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}]},
      'title': '销售出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'XSCK-20260901-014',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '关联销售订单',
          'text': 'SO-20260828-0041',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'label': '客户',
          'text': '东风本田汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2604'
        },
        {
          'label': '出库物料',
          'text': '锁扣组件（LJ-A100）',
          'full': true
        },
        {
          'label': '数量',
          'text': '800 件'
        },
        {
          'label': '出库库区',
          'text': '原料区 RA'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '制单时间',
          'text': '2026-09-01'
        },
        {
          'label': '计价方式',
          'text': '销售价随订单（一进一出）',
          'full': true
        }
      ],
      'feeSecTitle': '出库明细',
      'feeCols': ['序号', '物料编码', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'LJ-A100', '锁扣组件 不锈钢 304', '件', '800', '6.80', '13%', '7.68', '6,144.00', 'RA-A-02-01']
        }
      ],
      'chain': [
        {
          'role': '销售订单',
          'name': 'SO-20260828-0041',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '销售出库（本单）',
          'name': 'XSCK-20260901-014',
          'self': true
        },
        {
          'role': '应收账单',
          'name': 'AR-2026-09-PRJ2604-S1 · 销售费',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '09-01 10:20',
          'text': '备货 · 原料区 RA 锁扣 800 件',
          'who': '张伟'
        },
        {
          't': '09-01 15:40',
          'text': '出库确认 · 客户签收',
          'who': '张伟'
        },
        {
          't': '09-02',
          'text': '销售费应收生成 · AR-2026-09-PRJ2604-S1（1,280 元）',
          'who': '系统'
        }
      ]
    },
    'XSCK-20260829-013': {
      'row': {"fields": {"so": "SO-20260827-0039", "customer": "一汽解放汽车有限公司", "project": "PRJ-2601", "summary": "箱盖 ABS 吸塑×2,000", "warehouse": "原料区 RA", "date": "2026-08-29", "status": "已完成"}, "cells": ["<span class=\"lk\">SO-20260827-0039</span>", "一汽解放汽车有限公司", "PRJ-2601", "箱盖 ABS 吸塑×2,000", "<span class=\"td-num\">2,000</span>", "原料区 RA", "2026-08-29", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}]},
      'title': '销售出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'XSCK-20260829-013',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '关联销售订单',
          'text': 'SO-20260827-0039',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '出库物料',
          'text': '箱盖 ABS 吸塑（LJ-D400）',
          'full': true
        },
        {
          'label': '数量',
          'text': '2,000 件'
        },
        {
          'label': '出库库区',
          'text': '原料区 RA'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '制单时间',
          'text': '2026-08-29'
        },
        {
          'label': '计价方式',
          'text': '销售价随订单（一进一出）',
          'full': true
        }
      ],
      'feeSecTitle': '出库明细',
      'feeCols': ['序号', '物料编码', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'LJ-D400', '箱盖 ABS 吸塑', '件', '2,000', '36.00', '13%', '40.68', '81,360.00', 'RA-A-02-01']
        }
      ],
      'chain': [
        {
          'role': '销售订单',
          'name': 'SO-20260827-0039',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '销售出库（本单）',
          'name': 'XSCK-20260829-013',
          'self': true
        },
        {
          'role': '应收账单',
          'name': '销售费 · 按出库自动汇总',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-29 09:40',
          'text': '备货 · 原料区 RA 箱盖 2,000 件',
          'who': '张伟'
        },
        {
          't': '08-29 16:05',
          'text': '出库确认 · 客户签收',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '销售费应收按出库汇总',
          'off': true
        }
      ]
    },
    'XSCK-20260826-012': {
      'row': {"fields": {"so": "SO-20260822-0038", "customer": "上汽大众汽车有限公司宁波分公司", "project": "PRJ-2602", "summary": "铰链×900 / 内衬×400", "warehouse": "原料区 RA", "date": "2026-08-26", "status": "已完成"}, "cells": ["<span class=\"lk\">SO-20260822-0038</span>", "上汽大众汽车有限公司宁波分公司", "PRJ-2602", "铰链×900 / 内衬×400", "<span class=\"td-num\">1,300</span>", "原料区 RA", "2026-08-26", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}]},
      'title': '销售出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'XSCK-20260826-012',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '关联销售订单',
          'text': 'SO-20260822-0038',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'label': '客户',
          'text': '上汽大众汽车有限公司宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '出库物料',
          'text': '铰链（LJ-B200）× 900 / 内衬（LJ-F600）× 400',
          'full': true
        },
        {
          'label': '数量',
          'text': '1,300 件'
        },
        {
          'label': '出库库区',
          'text': '原料区 RA'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '制单时间',
          'text': '2026-08-26'
        },
        {
          'label': '计价方式',
          'text': '销售价随订单（一进一出）',
          'full': true
        }
      ],
      'feeSecTitle': '出库明细',
      'feeCols': ['序号', '物料编码', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'LJ-B200', '铰链 锌合金 65mm', '件', '1,300', '4.20', '13%', '4.75', '6,175.00', 'RA-A-02-01']
        },
        {
          'cells': ['2', 'LJ-F600', '内衬 EPE 珍珠棉', '件', '400', '15.50', '13%', '17.51', '7,004.00', 'RA-A-03-01']
        }
      ],
      'chain': [
        {
          'role': '销售订单',
          'name': 'SO-20260822-0038',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '销售出库（本单）',
          'name': 'XSCK-20260826-012',
          'self': true
        },
        {
          'role': '应收账单',
          'name': 'AR-2026-08-PRJ2602-S1 · 销售费',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-26 10:10',
          'text': '备货 · 原料区 RA 铰链 900 / 内衬 400',
          'who': '张伟'
        },
        {
          't': '08-26 15:30',
          'text': '出库确认 · 客户签收',
          'who': '张伟'
        },
        {
          't': '08-31',
          'text': '销售费应收生成 · AR-2026-08-PRJ2602-S1（6,050 元）',
          'who': '系统'
        }
      ]
    },
    'XSCK-20260822-011': {
      'row': {"fields": {"so": "SO-20260819-0035", "customer": "小鹏汽车科技有限公司", "project": "PRJ-2603", "summary": "锁扣组件×1,200", "warehouse": "原料区 RA", "date": "2026-08-22", "status": "已完成"}, "cells": ["<span class=\"lk\">SO-20260819-0035</span>", "小鹏汽车科技有限公司", "PRJ-2603", "锁扣组件×1,200", "<span class=\"td-num\">1,200</span>", "原料区 RA", "2026-08-22", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}]},
      'title': '销售出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'XSCK-20260822-011',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '关联销售订单',
          'text': 'SO-20260819-0035',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'label': '客户',
          'text': '小鹏汽车科技有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2603'
        },
        {
          'label': '出库物料',
          'text': '锁扣组件（LJ-A100）',
          'full': true
        },
        {
          'label': '数量',
          'text': '1,200 件'
        },
        {
          'label': '出库库区',
          'text': '原料区 RA'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '制单时间',
          'text': '2026-08-22'
        },
        {
          'label': '计价方式',
          'text': '销售价随订单（一进一出）',
          'full': true
        }
      ],
      'feeSecTitle': '出库明细',
      'feeCols': ['序号', '物料编码', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'LJ-A100', '锁扣组件 不锈钢 304', '件', '1,200', '6.80', '13%', '7.68', '9,216.00', 'RA-A-02-01']
        }
      ],
      'chain': [
        {
          'role': '销售订单',
          'name': 'SO-20260819-0035',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '销售出库（本单）',
          'name': 'XSCK-20260822-011',
          'self': true
        },
        {
          'role': '应收账单',
          'name': '销售费 · 按出库自动汇总',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-22 09:30',
          'text': '备货 · 原料区 RA 锁扣 1,200 件',
          'who': '张伟'
        },
        {
          't': '08-22 14:20',
          'text': '出库确认 · 客户签收',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '销售费应收按出库汇总',
          'off': true
        }
      ]
    },
    'XSCK-20260818-010': {
      'row': {"fields": {"so": "SO-20260815-0032", "customer": "一汽解放汽车有限公司", "project": "PRJ-2601", "summary": "箱盖 ABS 吸塑×600", "warehouse": "原料区 RA", "date": "2026-08-18", "status": "已完成"}, "cells": ["<span class=\"lk\">SO-20260815-0032</span>", "一汽解放汽车有限公司", "PRJ-2601", "箱盖 ABS 吸塑×600", "<span class=\"td-num\">600</span>", "原料区 RA", "2026-08-18", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "打印出货单", "act": "window.print();this.classList.toggle('printed')"}]},
      'title': '销售出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'XSCK-20260818-010',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '关联销售订单',
          'text': 'SO-20260815-0032',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '出库物料',
          'text': '箱盖 ABS 吸塑（LJ-D400）',
          'full': true
        },
        {
          'label': '数量',
          'text': '600 件'
        },
        {
          'label': '出库库区',
          'text': '原料区 RA'
        },
        {
          'label': '制单人',
          'text': '张伟'
        },
        {
          'label': '制单时间',
          'text': '2026-08-18'
        },
        {
          'label': '计价方式',
          'text': '销售价随订单（一进一出）',
          'full': true
        }
      ],
      'feeSecTitle': '出库明细',
      'feeCols': ['序号', '物料编码', '名称规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'],
      'fees': [
        {
          'cells': ['1', 'LJ-D400', '箱盖 ABS 吸塑', '件', '600', '36.00', '13%', '40.68', '24,408.00', 'RA-A-02-01']
        }
      ],
      'chain': [
        {
          'role': '销售订单',
          'name': 'SO-20260815-0032',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '销售出库（本单）',
          'name': 'XSCK-20260818-010',
          'self': true
        },
        {
          'role': '应收账单',
          'name': '销售费 · 按出库自动汇总',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-18 10:00',
          'text': '备货 · 原料区 RA 箱盖 600 件',
          'who': '张伟'
        },
        {
          't': '08-18 16:10',
          'text': '出库确认 · 客户签收',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '销售费应收按出库汇总',
          'off': true
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 其他入库单 otherInbounds：键 = QTRK 入库单号（仓储作业/其他入库列表.html 3 行全量） */
  /* 期初/盘盈/退货/手工例外；盘盈联动盘点差异 */
  otherInbounds: {
    'QTRK-20260901-003': {
      'row': {"fields": {"type": "盘盈", "material": "LJ-B200 铰链 锌合金 65mm", "warehouse": "原料区 RA", "date": "2026-09-01", "status": "待审核"}, "cells": ["<span class=\"tag tag-blue\">盘盈</span>", "LJ-B200 铰链 锌合金 65mm", "<span class=\"td-num\">120 件</span>", "原料区 RA", "2026-09-01", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "审核", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}]},
      'title': '其他入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'QTRK-20260901-003',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '其他入库单 · 盘盈',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '物料',
          'text': 'LJ-B200 铰链 锌合金 65mm',
          'full': true
        },
        {
          'label': '数量',
          'text': '120 件'
        },
        {
          'label': '入库库区',
          'text': '原料区 RA'
        },
        {
          'label': '入库类型',
          'text': '盘盈入库（盘点差异处理）',
          'full': true
        },
        {
          'label': '关联盘点单',
          'text': 'PD-202608-02',
          'url': '仓储作业/盘点列表.html'
        },
        {
          'label': '入库日期',
          'text': '2026-09-01'
        },
        {
          'label': '制单人',
          'text': '赵芳'
        },
        {
          'label': '审核人',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '账外实物，盘点确认后补录库存',
          'full': true
        }
      ],
      'feeSecTitle': '入库明细',
      'feeCols': ['序号', '物料编码', '名称规格', '单位', '数量', '处理方式'],
      'fees': [
        {
          'cells': ['1', 'LJ-B200', '铰链 锌合金 65mm', '件', '120', '盘盈补录 · 原料区 RA']
        }
      ],
      'chain': [
        {
          'role': '库存盘点',
          'name': 'PD-202608-02 · 差异 12 项',
          'url': '仓储作业/盘点列表.html'
        },
        {
          'role': '其他入库（本单）',
          'name': 'QTRK-20260901-003',
          'self': true
        },
        {
          'role': '库存台账',
          'name': 'LJ-B200 在库 +120',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-31 18:00',
          'text': '盘点完成 · 发现 LJ-B200 账实差异（盘盈 120 件）',
          'who': '陈金'
        },
        {
          't': '09-01 14:30',
          'text': '制单 · 盘盈入库申请',
          'who': '赵芳'
        },
        {
          't': '—',
          'text': '待审核 · 通过后库存入账',
          'off': true
        }
      ]
    },
    'QTRK-20260828-002': {
      'row': {"fields": {"type": "退货", "material": "LJ-D400 箱盖 ABS 吸塑", "warehouse": "原料区 RA", "date": "2026-08-28", "status": "已入库"}, "cells": ["<span class=\"tag tag-orange\">退货</span>", "LJ-D400 箱盖 ABS 吸塑", "<span class=\"td-num\">300 件</span>", "原料区 RA", "2026-08-28", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '其他入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'QTRK-20260828-002',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '其他入库单 · 退货',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '物料',
          'text': 'LJ-D400 箱盖 ABS 吸塑',
          'full': true
        },
        {
          'label': '数量',
          'text': '300 件'
        },
        {
          'label': '入库库区',
          'text': '原料区 RA'
        },
        {
          'label': '入库类型',
          'text': '客户退货入库（质量换货退回）',
          'full': true
        },
        {
          'label': '关联盘点单',
          'text': '—'
        },
        {
          'label': '入库日期',
          'text': '2026-08-28'
        },
        {
          'label': '制单人',
          'text': '赵芳'
        },
        {
          'label': '审核人',
          'text': '张伟'
        },
        {
          'label': '备注',
          'text': '客户换货退回，质检合格后回库',
          'full': true
        }
      ],
      'feeSecTitle': '入库明细',
      'feeCols': ['序号', '物料编码', '名称规格', '单位', '数量', '处理方式'],
      'fees': [
        {
          'cells': ['1', 'LJ-D400', '箱盖 ABS 吸塑', '件', '300', '退货回库 · 原料区 RA']
        }
      ],
      'chain': [
        {
          'role': '其他入库（本单）',
          'name': 'QTRK-20260828-002',
          'self': true
        },
        {
          'role': '库存台账',
          'name': 'LJ-D400 在库 +300',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-27 16:20',
          'text': '客户退货到货 · 箱盖 300 件',
          'who': '张伟'
        },
        {
          't': '08-28 10:40',
          'text': '质检验收 · 合格回库',
          'who': '张伟'
        },
        {
          't': '08-28 14:00',
          'text': '入库完成 · 库存入账',
          'who': '系统'
        }
      ]
    },
    'QTRK-20260820-001': {
      'row': {"fields": {"type": "其他", "material": "WBX-1210M 围板箱 1200×1000×590", "warehouse": "成品区 RB", "date": "2026-08-20", "status": "已入库"}, "cells": ["<span class=\"tag tag-gray\">其他</span>", "WBX-1210M 围板箱 1200×1000×590", "<span class=\"td-num\">15 只</span>", "成品区 RB", "2026-08-20", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '其他入库单详情',
      'info': [
        {
          'label': '入库单号',
          'text': 'QTRK-20260820-001',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '其他入库单 · 其他',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已入库'
        },
        {
          'label': '物料',
          'text': 'WBX-1210M 围板箱 1200×1000×590',
          'full': true
        },
        {
          'label': '数量',
          'text': '15 只'
        },
        {
          'label': '入库库区',
          'text': '成品区 RB'
        },
        {
          'label': '入库类型',
          'text': '期初导入 / 手工例外入库',
          'full': true
        },
        {
          'label': '关联盘点单',
          'text': '—'
        },
        {
          'label': '入库日期',
          'text': '2026-08-20'
        },
        {
          'label': '制单人',
          'text': '赵芳'
        },
        {
          'label': '审核人',
          'text': '张伟'
        },
        {
          'label': '备注',
          'text': '期初建账补录（历史遗留批次）',
          'full': true
        }
      ],
      'feeSecTitle': '入库明细',
      'feeCols': ['序号', '物料编码', '名称规格', '单位', '数量', '处理方式'],
      'fees': [
        {
          'cells': ['1', 'WBX-1210M', '围板箱 1200×1000×590', '只', '15', '期初补录 · 成品区 RB']
        }
      ],
      'chain': [
        {
          'role': '其他入库（本单）',
          'name': 'QTRK-20260820-001',
          'self': true
        },
        {
          'role': '库存台账',
          'name': 'WBX-1210M 在库 +15',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-20 09:30',
          'text': '制单 · 期初补录申请',
          'who': '赵芳'
        },
        {
          't': '08-20 11:00',
          'text': '审核通过 · 库存入账',
          'who': '张伟'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 其他出库单 otherOutbounds：键 = QTCK 出库单号（仓储作业/其他出库列表.html 5 行全量） */
  /* 报废/盘亏/赔偿核销/手工例外；赔偿核销=丢损赔偿联动（09-05 口径） */
  otherOutbounds: {
    'QTCK-20260905-005': {
      'row': {"fields": {"type": "赔偿核销", "material": "GB-800 隔板 · 关联赔偿单 BS-20260902-010（丢失 1 套自客户态出账）", "warehouse": "—", "date": "2026-09-05", "status": "已出库"}, "cells": ["<span class=\"tag tag-blue\">赔偿核销</span>", "GB-800 隔板 · 关联赔偿单 <span class=\"lk\">BS-20260902-010</span>（丢失 1 套自客户态出账）", "<span class=\"td-num\">1 套</span>", "—", "2026-09-05", "<span class=\"tag tag-green\">已出库</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '其他出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'QTCK-20260905-005',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '其他出库单 · 赔偿核销',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已出库'
        },
        {
          'label': '器具',
          'text': 'GB-800 隔板',
          'full': true
        },
        {
          'label': '数量',
          'text': '1 套'
        },
        {
          'label': '出库库区',
          'text': '—（自客户态出账）'
        },
        {
          'label': '出库类型',
          'text': '赔偿核销出库（丢损赔偿联动）',
          'full': true
        },
        {
          'label': '关联赔偿单',
          'text': 'BS-20260902-010',
          'full': true
        },
        {
          'label': '出库日期',
          'text': '2026-09-05'
        },
        {
          'label': '制单人',
          'text': '系统'
        },
        {
          'label': '审核人',
          'text': '王芳'
        },
        {
          'label': '备注',
          'text': '丢失 1 套自客户态直接出账（赔偿审核即核销）',
          'full': true
        }
      ],
      'feeSecTitle': '出库明细',
      'feeCols': ['序号', '器具编码', '名称规格', '单位', '数量', '处置去向'],
      'fees': [
        {
          'cells': ['1', 'GB-800', '隔板', '套', '1', '丢失件自客户态出账 · 赔偿核销']
        }
      ],
      'chain': [
        {
          'role': '丢损赔偿单',
          'name': 'BS-20260902-010 · 审核即核销',
        },
        {
          'role': '其他出库（本单）',
          'name': 'QTCK-20260905-005 · 赔偿核销',
          'self': true
        },
        {
          'role': '库存台账',
          'name': '客户态 -1 · 出账',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '09-02 17:20',
          'text': '退租验收发现丢失 · BS-20260902-010',
          'who': '张伟'
        },
        {
          't': '09-05 10:00',
          'text': '赔偿审核通过 · 自动生成赔偿核销出库',
          'who': '王芳'
        },
        {
          't': '09-05 10:01',
          'text': '丢失件自客户态直接出账 · 核销完成',
          'who': '系统'
        }
      ]
    },
    'QTCK-20260901-004': {
      'row': {"fields": {"type": "报废", "material": "WBX-1210L", "warehouse": "成品区 RB", "date": "2026-09-01", "status": "待审核"}, "cells": ["<span class=\"tag tag-red\">报废</span>", "WBX-1210L(旧) 围板箱 旧箱体批次", "<span class=\"td-num\">35 只</span>", "成品区 RB", "2026-09-01", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "审核", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}]},
      'title': '其他出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'QTCK-20260901-004',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '其他出库单 · 报废',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '器具',
          'text': 'WBX-1210L（旧） 围板箱 1200×1000×970',
          'full': true
        },
        {
          'label': '数量',
          'text': '35 只'
        },
        {
          'label': '出库库区',
          'text': '成品区 RB'
        },
        {
          'label': '出库类型',
          'text': '报废出库（手工例外）',
          'full': true
        },
        {
          'label': '报废原因',
          'text': '破损不可维修（字典：破损 PS）',
          'full': true
        },
        {
          'label': '处置方式',
          'text': '资产出库 · 不可再出租',
          'full': true
        },
        {
          'label': '出库日期',
          'text': '2026-09-01'
        },
        {
          'label': '制单人',
          'text': '赵芳'
        },
        {
          'label': '审核人',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '旧箱体批次，维修判定不可修复',
          'full': true
        }
      ],
      'feeSecTitle': '出库明细',
      'feeCols': ['序号', '器具编码', '名称规格', '单位', '数量', '处置去向'],
      'fees': [
        {
          'cells': ['1', 'WBX-1210L（旧）', '围板箱 1200×1000×970 · 旧箱体批次', '只', '35', '资产报废出库']
        }
      ],
      'chain': [
        {
          'role': '库存台账',
          'name': '成品区 RB · 旧箱体批次',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '其他出库（本单）',
          'name': 'QTCK-20260901-004',
          'self': true
        },
        {
          'role': '资产处置',
          'name': '报废出库 · 账面核减'
        }
      ],
      'timeline': [
        {
          't': '08-30 16:20',
          'text': '维修判定 · 旧批次围板箱不可修复',
          'who': '张伟'
        },
        {
          't': '09-01 15:50',
          'text': '制单 · 报废出库申请',
          'who': '赵芳'
        },
        {
          't': '—',
          'text': '待审核 · 通过后资产出库核减',
          'off': true
        }
      ]
    },
    'QTCK-20260829-003': {
      'row': {"fields": {"type": "盘亏", "material": "LJ-F600 内衬 EPE 珍珠棉", "warehouse": "原料区 RA", "date": "2026-08-29", "status": "已完成"}, "cells": ["<span class=\"tag tag-orange\">盘亏</span>", "LJ-F600 内衬 EPE 珍珠棉", "<span class=\"td-num\">80 件</span>", "原料区 RA", "2026-08-29", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '其他出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'QTCK-20260829-003',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '其他出库单 · 盘亏',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '器具',
          'text': 'LJ-F600 内衬 EPE 珍珠棉',
          'full': true
        },
        {
          'label': '数量',
          'text': '80 件'
        },
        {
          'label': '出库库区',
          'text': '原料区 RA'
        },
        {
          'label': '出库类型',
          'text': '盘亏出库（盘点差异处理）',
          'full': true
        },
        {
          'label': '关联盘点单',
          'text': 'PD-202608-02',
          'url': '仓储作业/盘点列表.html',
          'full': true
        },
        {
          'label': '出库日期',
          'text': '2026-08-29'
        },
        {
          'label': '制单人',
          'text': '赵芳'
        },
        {
          'label': '审核人',
          'text': '张伟'
        },
        {
          'label': '备注',
          'text': '盘点盘亏核减（账面大于实物）',
          'full': true
        }
      ],
      'feeSecTitle': '出库明细',
      'feeCols': ['序号', '器具编码', '名称规格', '单位', '数量', '处置去向'],
      'fees': [
        {
          'cells': ['1', 'LJ-F600', '内衬 EPE 珍珠棉', '件', '80', '盘亏核减 · 账面调减']
        }
      ],
      'chain': [
        {
          'role': '库存盘点',
          'name': 'PD-202608-02 · 差异 12 项',
          'url': '仓储作业/盘点列表.html'
        },
        {
          'role': '其他出库（本单）',
          'name': 'QTCK-20260829-003',
          'self': true
        },
        {
          'role': '库存台账',
          'name': 'LJ-F600 在库 -80',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-31 18:00',
          'text': '盘点完成 · LJ-F600 盘亏 80 件',
          'who': '陈金'
        },
        {
          't': '08-29 09:10',
          'text': '制单 · 盘亏出库（按盘点差异）',
          'who': '赵芳'
        },
        {
          't': '08-29 15:30',
          'text': '审核通过 · 账面核减',
          'who': '张伟'
        }
      ]
    },
    'QTCK-20260825-002': {
      'row': {"fields": {"type": "报废", "material": "PLT-1210W 木托盘 1200×1000", "warehouse": "成品区 RB", "date": "2026-08-25", "status": "已完成"}, "cells": ["<span class=\"tag tag-red\">报废</span>", "PLT-1210W 木托盘 1200×1000", "<span class=\"td-num\">22 块</span>", "成品区 RB", "2026-08-25", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '其他出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'QTCK-20260825-002',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '其他出库单 · 报废',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '器具',
          'text': 'PLT-1210W 木托盘 1200×1000',
          'full': true
        },
        {
          'label': '数量',
          'text': '22 块'
        },
        {
          'label': '出库库区',
          'text': '成品区 RB'
        },
        {
          'label': '出库类型',
          'text': '报废出库（手工例外）',
          'full': true
        },
        {
          'label': '报废原因',
          'text': '破损不可维修（字典：破损 PS）',
          'full': true
        },
        {
          'label': '处置方式',
          'text': '资产出库 · 不可再出租',
          'full': true
        },
        {
          'label': '出库日期',
          'text': '2026-08-25'
        },
        {
          'label': '制单人',
          'text': '赵芳'
        },
        {
          'label': '审核人',
          'text': '张伟'
        },
        {
          'label': '备注',
          'text': '木托盘断裂批次报废',
          'full': true
        }
      ],
      'feeSecTitle': '出库明细',
      'feeCols': ['序号', '器具编码', '名称规格', '单位', '数量', '处置去向'],
      'fees': [
        {
          'cells': ['1', 'PLT-1210W', '木托盘 1200×1000', '块', '22', '资产报废出库']
        }
      ],
      'chain': [
        {
          'role': '库存台账',
          'name': '成品区 RB · PLT-1210W',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '其他出库（本单）',
          'name': 'QTCK-20260825-002',
          'self': true
        },
        {
          'role': '资产处置',
          'name': '报废出库 · 账面核减'
        }
      ],
      'timeline': [
        {
          't': '08-24 15:00',
          'text': '维修判定 · 断裂不可修复',
          'who': '张伟'
        },
        {
          't': '08-25 10:20',
          'text': '制单 · 报废出库申请',
          'who': '赵芳'
        },
        {
          't': '08-25 16:40',
          'text': '审核通过 · 资产出库核减',
          'who': '张伟'
        }
      ]
    },
    'QTCK-20260815-001': {
      'row': {"fields": {"type": "其他", "material": "LJ-A100 锁扣组件 不锈钢 304", "warehouse": "原料区 RA", "date": "2026-08-15", "status": "已完成"}, "cells": ["<span class=\"tag tag-gray\">其他</span>", "LJ-A100 锁扣组件 不锈钢 304", "<span class=\"td-num\">50 件</span>", "原料区 RA", "2026-08-15", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '其他出库单详情',
      'info': [
        {
          'label': '出库单号',
          'text': 'QTCK-20260815-001',
          'full': true
        },
        {
          'label': '单据类型',
          'text': '其他出库单 · 其他',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '器具',
          'text': 'LJ-A100 锁扣组件 不锈钢 304',
          'full': true
        },
        {
          'label': '数量',
          'text': '50 件'
        },
        {
          'label': '出库库区',
          'text': '原料区 RA'
        },
        {
          'label': '出库类型',
          'text': '其他出库（手工例外）',
          'full': true
        },
        {
          'label': '出库日期',
          'text': '2026-08-15'
        },
        {
          'label': '制单人',
          'text': '赵芳'
        },
        {
          'label': '审核人',
          'text': '张伟'
        },
        {
          'label': '备注',
          'text': '样品领用出库（研发试用）',
          'full': true
        }
      ],
      'feeSecTitle': '出库明细',
      'feeCols': ['序号', '器具编码', '名称规格', '单位', '数量', '处置去向'],
      'fees': [
        {
          'cells': ['1', 'LJ-A100', '锁扣组件 不锈钢 304', '件', '50', '样品领用 · 手工例外']
        }
      ],
      'chain': [
        {
          'role': '库存台账',
          'name': '原料区 RA · LJ-A100',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '其他出库（本单）',
          'name': 'QTCK-20260815-001',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '08-15 10:30',
          'text': '制单 · 样品领用出库',
          'who': '赵芳'
        },
        {
          't': '08-15 14:20',
          'text': '审核通过 · 出库',
          'who': '张伟'
        }
      ]
    }
  },  /* -------------------------------------------------------------------------- */
  /* 盘点单 stocktakes：键 = PD 盘点单号（仓储作业/盘点列表.html 5 行全量） */
  /* 差异处理：盘盈→其他入库 / 盘亏报废→其他出库（S1 支线） */
  stocktakes: {
    'PD-202608-03': {
      'row': {"fields": {"scope": "华东中心仓 / 全库区", "caliber": "正常", "status": "盘点中", "checker": "张伟", "date": "2026-08-30"}, "cells": ["华东中心仓 / 全库区", "<span class=\"tag tag-green\">正常</span>", "<span class=\"td-num\">1,286</span>", "—", "<span class=\"tag tag-blue\">盘点中</span>", "张伟", "2026-08-30"], "ops": [{"t": "详情", "detail": true}, {"t": "录入", "act": "go('../仓储作业/盘点录入.html')"}, {"t": "审核", "act": "openModal('auditModal')"}]},
      'title': '盘点单详情',
      'info': [
        {
          'label': '盘点单号',
          'text': 'PD-202608-03',
          'full': true
        },
        {
          'label': '状态',
          'tag': '盘点中'
        },
        {
          'label': '盘点范围',
          'text': '华东中心仓 · 全库区',
          'full': true
        },
        {
          'label': '盘点方式',
          'text': '全面盘点（静态盘点）',
          'full': true
        },
        {
          'label': '盘点基准',
          'text': '2026-08-30 账面库存',
          'full': true
        },
        {
          'label': '账面项数',
          'text': '1,286 项'
        },
        {
          'label': '差异项数',
          'text': '—（盘点中）'
        },
        {
          'label': '盘点人',
          'text': '张伟'
        },
        {
          'label': '创建日期',
          'text': '2026-08-30'
        },
        {
          'label': '上期盘点',
          'text': 'PD-202608-02 · 差异 12 项已处理',
          'url': '仓储作业/盘点列表.html',
          'full': true
        }
      ],
      'feeSecTitle': '差异明细（上期 PD-202608-02 示例 · 本单待生成）',
      'feeCols': ['物料', '账面', '实盘', '差异', '处理单据'],
      'fees': [
        {
          'cells': ['LJ-B200 铰链 锌合金 65mm', '2,520', '2,640', '+120', 'QTRK-20260901-003 盘盈入库'],
          'links': {
            4: '仓储作业/其他入库列表.html'
          }
        },
        {
          'cells': ['WBX-1210L（旧）围板箱 · 旧箱体批次', '35', '0', '-35', 'QTCK-20260901-004 报废出库'],
          'links': {
            4: '仓储作业/其他出库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '库存台账',
          'name': '账面 1,286 项',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '库存盘点（本单）',
          'name': 'PD-202608-03 · 盘点中',
          'self': true
        },
        {
          'role': '差异处理',
          'name': '盘盈 → 其他入库 / 盘亏报废 → 其他出库',
          'url': '仓储作业/其他入库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-30 09:00',
          'text': '创建盘点任务 · 全库区静态盘点',
          'who': '张伟'
        },
        {
          't': '08-30 至今',
          'text': '库区实物清点 · 录入中',
          'who': '张伟'
        },
        {
          't': '—',
          'text': '待录入完成 → 提交审核 → 差异转处理单据',
          'off': true
        }
      ]
    },
    'PD-202608-02': {
      'row': {"fields": {"scope": "华东中心仓 / 组装区 RD", "caliber": "正常", "status": "待审核", "checker": "李国栋", "date": "2026-08-15"}, "cells": ["华东中心仓 / 组装区 RD", "<span class=\"tag tag-green\">正常</span>", "<span class=\"td-num\">36</span>", "<span class=\"td-num\" style=\"color:var(--primary)\">+18</span>", "<span class=\"tag tag-orange\">待审核</span>", "李国栋", "2026-08-15"], "ops": [{"t": "详情", "detail": true}, {"t": "录入", "act": "go('../仓储作业/盘点录入.html')"}, {"t": "审核", "act": "openModal('auditModal')"}]},
      'title': '盘点单详情',
      'info': [
        {
          'label': '盘点单号',
          'text': 'PD-202608-02',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '盘点范围',
          'text': '华东中心仓 · 组装区 RD',
          'full': true
        },
        {
          'label': '盘点方式',
          'text': '全面盘点（静态盘点）',
          'full': true
        },
        {
          'label': '盘点基准',
          'text': '2026-08-15 账面库存',
          'full': true
        },
        {
          'label': '账面项数',
          'text': '36 项'
        },
        {
          'label': '差异项数',
          'text': '+18'
        },
        {
          'label': '盘点人',
          'text': '李国栋'
        },
        {
          'label': '创建日期',
          'text': '2026-08-15'
        },
        {
          'label': '上期盘点',
          'text': 'PD-202607-02 · 差异 2 项已处理',
          'url': '仓储作业/盘点列表.html',
          'full': true
        }
      ],
      'feeSecTitle': '差异明细',
      'feeCols': ['物料', '账面', '实盘', '差异', '处理单据'],
      'fees': [
        {
          'cells': ['LJ-B200 铰链 锌合金 65mm', '2,520', '2,640', '+120', 'QTRK-20260901-003 盘盈入库'],
          'links': {
            4: '仓储作业/其他入库列表.html'
          }
        },
        {
          'cells': ['WBX-1210L（旧）围板箱 · 旧箱体批次', '35', '0', '-35', 'QTCK-20260901-004 报废出库'],
          'links': {
            4: '仓储作业/其他出库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '库存台账',
          'name': '组装区 RD 账面',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '库存盘点（本单）',
          'name': 'PD-202608-02 · 待审核',
          'self': true
        },
        {
          'role': '差异处理',
          'name': '盘盈 → 其他入库 / 盘亏报废 → 其他出库',
          'url': '仓储作业/其他入库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-15 10:20',
          'text': '创建盘点任务 · 组装区 RD',
          'who': '李国栋'
        },
        {
          't': '08-31 18:00',
          'text': '盘点完成 · 差异 2 项（+120 / -35）',
          'who': '李国栋'
        },
        {
          't': '—',
          'text': '待审核 · 差异已转处理单据（QTRK/QTCK）',
          'off': true
        }
      ]
    },
    'PD-202607-02': {
      'row': {"fields": {"scope": "华东中心仓 / 成品区 RB", "caliber": "在租", "status": "已完成", "checker": "李国栋", "date": "2026-07-31"}, "cells": ["华东中心仓 / 成品区 RB", "<span class=\"tag tag-blue\">在租</span>", "<span class=\"td-num\">86</span>", "<span class=\"td-num\" style=\"color:var(--danger)\">-2</span>", "<span class=\"tag tag-green\">已完成</span>", "李国栋", "2026-07-31"], "ops": [{"t": "详情", "detail": true}, {"t": "录入", "act": "go('../仓储作业/盘点录入.html')"}, {"t": "审核", "act": "openModal('auditModal')"}]},
      'title': '盘点单详情',
      'info': [
        {
          'label': '盘点单号',
          'text': 'PD-202607-02',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '盘点范围',
          'text': '华东中心仓 · 成品区 RB',
          'full': true
        },
        {
          'label': '盘点方式',
          'text': '全面盘点（静态盘点）',
          'full': true
        },
        {
          'label': '盘点基准',
          'text': '2026-07-31 账面库存',
          'full': true
        },
        {
          'label': '账面项数',
          'text': '86 项'
        },
        {
          'label': '差异项数',
          'text': '-2'
        },
        {
          'label': '盘点人',
          'text': '李国栋'
        },
        {
          'label': '创建日期',
          'text': '2026-07-31'
        },
        {
          'label': '上期盘点',
          'text': 'PD-202607-01',
          'url': '仓储作业/盘点列表.html',
          'full': true
        }
      ],
      'feeSecTitle': '差异明细',
      'feeCols': ['物料', '账面', '实盘', '差异', '处理单据'],
      'fees': [
        {
          'cells': ['ZH-2602-B 冲压件料箱组套', '4,122', '4,120', '-2', '盘亏核减（历史处理）']
        }
      ],
      'chain': [
        {
          'role': '库存台账',
          'name': '成品区 RB 账面',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '库存盘点（本单）',
          'name': 'PD-202607-02 · 已完成',
          'self': true
        },
        {
          'role': '差异处理',
          'name': '差异已处理完结',
          'url': '仓储作业/其他出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '07-31 09:00',
          'text': '创建盘点任务 · 成品区 RB',
          'who': '李国栋'
        },
        {
          't': '08-01 16:40',
          'text': '盘点完成 · 差异 -2 已核减',
          'who': '李国栋'
        }
      ]
    },
    'PD-202607-01': {
      'row': {"fields": {"scope": "华东中心仓 / 原料区 RA", "caliber": "正常", "status": "已完成", "checker": "张伟", "date": "2026-07-31"}, "cells": ["华东中心仓 / 原料区 RA", "<span class=\"tag tag-green\">正常</span>", "<span class=\"td-num\">642</span>", "<span class=\"td-num\">0</span>", "<span class=\"tag tag-green\">已完成</span>", "张伟", "2026-07-31"], "ops": [{"t": "详情", "detail": true}, {"t": "录入", "act": "go('../仓储作业/盘点录入.html')"}, {"t": "审核", "act": "openModal('auditModal')"}]},
      'title': '盘点单详情',
      'info': [
        {
          'label': '盘点单号',
          'text': 'PD-202607-01',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '盘点范围',
          'text': '华东中心仓 · 原料区 RA',
          'full': true
        },
        {
          'label': '盘点方式',
          'text': '全面盘点（静态盘点）',
          'full': true
        },
        {
          'label': '盘点基准',
          'text': '2026-07-31 账面库存',
          'full': true
        },
        {
          'label': '账面项数',
          'text': '642 项'
        },
        {
          'label': '差异项数',
          'text': '0'
        },
        {
          'label': '盘点人',
          'text': '张伟'
        },
        {
          'label': '创建日期',
          'text': '2026-07-31'
        },
        {
          'label': '上期盘点',
          'text': 'PD-202606-01',
          'url': '仓储作业/盘点列表.html',
          'full': true
        }
      ],
      'feeSecTitle': '差异明细',
      'feeCols': ['物料', '账面', '实盘', '差异', '处理单据'],
      'fees': [
        {
          'cells': ['—', '—', '—', '0', '— 无差异']
        }
      ],
      'chain': [
        {
          'role': '库存台账',
          'name': '原料区 RA 账面',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '库存盘点（本单）',
          'name': 'PD-202607-01 · 已完成',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '07-31 08:30',
          'text': '创建盘点任务 · 原料区 RA',
          'who': '张伟'
        },
        {
          't': '08-01 10:20',
          'text': '盘点完成 · 无差异',
          'who': '张伟'
        }
      ]
    },
    'PD-202606-01': {
      'row': {"fields": {"scope": "华东中心仓 / 退货区 RC", "caliber": "正常", "status": "已完成", "checker": "张伟", "date": "2026-06-30"}, "cells": ["华东中心仓 / 退货区 RC", "<span class=\"tag tag-green\">正常</span>", "<span class=\"td-num\">128</span>", "<span class=\"td-num\" style=\"color:var(--primary)\">+3</span>", "<span class=\"tag tag-green\">已完成</span>", "张伟", "2026-06-30"], "ops": [{"t": "详情", "detail": true}, {"t": "录入", "act": "go('../仓储作业/盘点录入.html')"}, {"t": "审核", "act": "openModal('auditModal')"}]},
      'title': '盘点单详情',
      'info': [
        {
          'label': '盘点单号',
          'text': 'PD-202606-01',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '盘点范围',
          'text': '华东中心仓 · 退货区 RC',
          'full': true
        },
        {
          'label': '盘点方式',
          'text': '全面盘点（静态盘点）',
          'full': true
        },
        {
          'label': '盘点基准',
          'text': '2026-06-30 账面库存',
          'full': true
        },
        {
          'label': '账面项数',
          'text': '128 项'
        },
        {
          'label': '差异项数',
          'text': '+3'
        },
        {
          'label': '盘点人',
          'text': '张伟'
        },
        {
          'label': '创建日期',
          'text': '2026-06-30'
        },
        {
          'label': '上期盘点',
          'text': 'PD-202607-01',
          'url': '仓储作业/盘点列表.html',
          'full': true
        }
      ],
      'feeSecTitle': '差异明细',
      'feeCols': ['物料', '账面', '实盘', '差异', '处理单据'],
      'fees': [
        {
          'cells': ['LJ-D400 箱盖 ABS 吸塑', '297', '300', '+3', '盘盈补录（历史处理）']
        }
      ],
      'chain': [
        {
          'role': '库存台账',
          'name': '退货区 RC 账面',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '库存盘点（本单）',
          'name': 'PD-202606-01 · 已完成',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '06-30 09:00',
          'text': '创建盘点任务 · 退货区 RC',
          'who': '张伟'
        },
        {
          't': '07-01 15:10',
          'text': '盘点完成 · 盘盈 +3 已补录',
          'who': '张伟'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 库存调拨 transfers：键 = DB 调拨单号（仓储作业/库存调拨列表.html 3 行全量） */
  /* 调拨不变总量 · 仅变动库区分布 */
  transfers: {
    'DB-20260901-003': {
      'row': {"fields": {"material": "LJ-A100 锁扣组件 不锈钢 304", "frm": "原料区 RA", "to": "成品区 RB", "date": "2026-09-01", "status": "待审核"}, "cells": ["LJ-A100 锁扣组件 不锈钢 304", "<span class=\"td-num\">1,000 件</span>", "原料区 RA", "成品区 RB", "2026-09-01", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "审核", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}]},
      'title': '调拨单详情',
      'info': [
        {
          'label': '调拨单号',
          'text': 'DB-20260901-003',
          'full': true
        },
        {
          'label': '状态',
          'tag': '待审核'
        },
        {
          'label': '物料',
          'text': 'LJ-A100 锁扣组件 不锈钢 304',
          'full': true
        },
        {
          'label': '数量',
          'text': '1,000 件'
        },
        {
          'label': '调出库区',
          'text': '原料区 RA'
        },
        {
          'label': '调入库区',
          'text': '成品区 RB'
        },
        {
          'label': '调拨类型',
          'text': '库区内调拨'
        },
        {
          'label': '调拨原因',
          'text': '组装备料（ZH-2601-A 组装线需求）',
          'full': true
        },
        {
          'label': '调拨日期',
          'text': '2026-09-01'
        },
        {
          'label': '制单人',
          'text': '赵芳'
        },
        {
          'label': '审核人',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '调拨不影响库存总量，仅变动库区分布',
          'full': true
        }
      ],
      'feeSecTitle': '调拨明细',
      'feeCols': ['序号', '物料编码', '名称规格', '单位', '数量', '调出 → 调入'],
      'fees': [
        {
          'cells': ['1', 'LJ-A100', '锁扣组件 不锈钢 304', '件', '1000', '原料区 RA → 成品区 RB']
        }
      ],
      'chain': [
        {
          'role': '原料区 RA 库存',
          'name': 'LJ-A100 · 调出 1,000',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '库存调拨（本单）',
          'name': 'DB-20260901-003',
          'self': true
        },
        {
          'role': '成品区 RB 库存',
          'name': '组装线备料',
        }
      ],
      'timeline': [
        {
          't': '09-01 10:50',
          'text': '组装线提出备料需求 · ZH-2601-A',
          'who': '刘志强'
        },
        {
          't': '09-01 11:00',
          'text': '制单 · 调拨申请',
          'who': '赵芳'
        },
        {
          't': '—',
          'text': '待审核 · 通过后两库区库存同步变动',
          'off': true
        }
      ]
    },
    'DB-20260826-002': {
      'row': {"fields": {"material": "WBX-1210L 围板箱 1200×1000×970", "frm": "成品区 RB", "to": "外协周转区 RC", "date": "2026-08-26", "status": "已完成"}, "cells": ["WBX-1210L 围板箱 1200×1000×970", "<span class=\"td-num\">200 只</span>", "成品区 RB", "外协周转区 RC", "2026-08-26", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '调拨单详情',
      'info': [
        {
          'label': '调拨单号',
          'text': 'DB-20260826-002',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '物料',
          'text': 'WBX-1210L 围板箱 1200×1000×970',
          'full': true
        },
        {
          'label': '数量',
          'text': '200 只'
        },
        {
          'label': '调出库区',
          'text': '成品区 RB'
        },
        {
          'label': '调入库区',
          'text': '外协周转区 RC'
        },
        {
          'label': '调拨类型',
          'text': '库区间调拨'
        },
        {
          'label': '调拨原因',
          'text': '外协周转备货（客户产线周边仓）',
          'full': true
        },
        {
          'label': '调拨日期',
          'text': '2026-08-26'
        },
        {
          'label': '制单人',
          'text': '赵芳'
        },
        {
          'label': '审核人',
          'text': '张伟'
        },
        {
          'label': '备注',
          'text': '调拨不影响库存总量，仅变动库区分布',
          'full': true
        }
      ],
      'feeSecTitle': '调拨明细',
      'feeCols': ['序号', '物料编码', '名称规格', '单位', '数量', '调出 → 调入'],
      'fees': [
        {
          'cells': ['1', 'WBX-1210L', '围板箱 1200×1000×970', '只', '200', '成品区 RB → 外协周转区 RC']
        }
      ],
      'chain': [
        {
          'role': '成品区 RB 库存',
          'name': 'WBX-1210L · 调出 200',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '库存调拨（本单）',
          'name': 'DB-20260826-002',
          'self': true
        },
        {
          'role': '外协周转区 RC',
          'name': '客户产线周边备货',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-26 09:30',
          'text': '制单 · 外协周转备货调拨',
          'who': '赵芳'
        },
        {
          't': '08-26 14:20',
          'text': '审核通过 · 两库区库存同步变动',
          'who': '张伟'
        }
      ]
    },
    'DB-20260812-001': {
      'row': {"fields": {"material": "PLT-1210P 塑料托盘 1200×1000", "frm": "成品区 RB", "to": "原料区 RA", "date": "2026-08-12", "status": "已完成"}, "cells": ["PLT-1210P 塑料托盘 1200×1000", "<span class=\"td-num\">300 块</span>", "成品区 RB", "原料区 RA", "2026-08-12", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "detail": true}]},
      'title': '调拨单详情',
      'info': [
        {
          'label': '调拨单号',
          'text': 'DB-20260812-001',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已完成'
        },
        {
          'label': '物料',
          'text': 'PLT-1210P 塑料托盘 1200×1000',
          'full': true
        },
        {
          'label': '数量',
          'text': '300 块'
        },
        {
          'label': '调出库区',
          'text': '成品区 RB'
        },
        {
          'label': '调入库区',
          'text': '原料区 RA'
        },
        {
          'label': '调拨类型',
          'text': '库区间调拨'
        },
        {
          'label': '调拨原因',
          'text': '零部件区辅料补库（托盘周转）',
          'full': true
        },
        {
          'label': '调拨日期',
          'text': '2026-08-12'
        },
        {
          'label': '制单人',
          'text': '赵芳'
        },
        {
          'label': '审核人',
          'text': '张伟'
        },
        {
          'label': '备注',
          'text': '调拨不影响库存总量，仅变动库区分布',
          'full': true
        }
      ],
      'feeSecTitle': '调拨明细',
      'feeCols': ['序号', '物料编码', '名称规格', '单位', '数量', '调出 → 调入'],
      'fees': [
        {
          'cells': ['1', 'PLT-1210P', '塑料托盘 1200×1000', '块', '300', '成品区 RB → 原料区 RA']
        }
      ],
      'chain': [
        {
          'role': '成品区 RB 库存',
          'name': 'PLT-1210P · 调出 300',
          'url': '仓储作业/库存查询.html'
        },
        {
          'role': '库存调拨（本单）',
          'name': 'DB-20260812-001',
          'self': true
        },
        {
          'role': '原料区 RA 库存',
          'name': '托盘周转补库',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-12 10:10',
          'text': '制单 · 托盘周转调拨',
          'who': '赵芳'
        },
        {
          't': '08-12 16:00',
          'text': '审核通过 · 两库区库存同步变动',
          'who': '张伟'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 库存流水 stockFlows：键 = 物料编码（仓储作业/库存查询.html 散件 9 + 组合件 3） */
  /* 弹窗 flowModal · 触发锚「库存流水」；四态口径 + 进出流水时间倒序 */
  stockFlows: {
     'XNC-AJZX-WBX': {
      'row': {"fields": {"name": "围板箱 1200×1000×970（安吉智行·客户虚拟仓）", "cls": "租赁器具", "project": "PRJ-2605", "area": "安吉智行·客户虚拟仓"}, "cells": ["围板箱 1200×1000×970（安吉智行·客户虚拟仓）", "<span class=\"tag tag-blue\">租赁器具</span>", "PRJ-2605", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">640</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>640</b></span>", "只", "安吉智行·客户虚拟仓"], "ops": [{"t": "库存流水", "detail": true}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
      'title': '库存流水',
      'titleNo': 'XNC-AJZX-WBX 围板箱（安吉智行·客户虚拟仓）',
      'info': [
        {
          'label': '物料编码',
          'text': 'XNC-AJZX-WBX'
        },
        {
          'label': '名称规格',
          'text': '围板箱 1200×1000×970（安吉智行·客户虚拟仓）',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '租赁器具'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2605',
          'full': true
        },
        {
          'label': '在库',
          'text': '0（虚拟仓不占实体库）'
        },
        {
          'label': '客户端（on-hire）',
          'text': '640 只'
        },
        {
          'label': '口径',
          'text': '客户虚拟仓＝在客户处的租赁资产按客户归集（on-hire）；客户转租为其子状态',
          'full': true
        },
        {
          'label': '库区',
          'text': '安吉智行·客户虚拟仓'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['09-02', '组合出库', 'CK-20260824-009', '+640', '640'],
          'links': {
            2: '租赁管理/组合出库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260823-033',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '组合出库',
          'name': 'CK-20260824-009 · 出库至客户',
          'url': '租赁管理/组合出库列表.html'
        },
        {
          'role': '客户虚拟仓（本仓）',
          'name': 'XNC-AJZX · on-hire 640 只',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '09-02',
          'text': '组合出库 640 只至安吉智行 · 按客户归集记客户虚拟仓（on-hire）',
          'who': '张伟'
        }
      ]
    },
   'LJ-A100': {
      'row': {"fields": {"name": "锁扣组件 不锈钢 304", "cls": "零部件", "project": "PRJ-2601/02/04", "area": "原料区 RA"}, "cells": ["锁扣组件 不锈钢 304", "<span class=\"tag tag-blue\">零部件</span>", "PRJ-2601/02/04", "<span class=\"td-num\">5,260</span>", "<span class=\"td-num\">1,200</span>", "<span class=\"td-num\">800</span>", "<span class=\"td-num\">2,400</span>", "<span class=\"td-num\"><b>7,260</b></span>", "件", "原料区 RA"], "ops": [{"t": "库存流水", "detail": true}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
      'title': '库存流水',
      'titleNo': 'LJ-A100 锁扣组件 不锈钢 304',
      'info': [
        {
          'label': '物料编码',
          'text': 'LJ-A100'
        },
        {
          'label': '名称规格',
          'text': '锁扣组件 不锈钢 304',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '零部件'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2601 / 2602 / 2604',
          'full': true
        },
        {
          'label': '在库',
          'text': '5,260 件'
        },
        {
          'label': '在途（退租未审核）',
          'text': '1,200 件'
        },
        {
          'label': '客户端（租出）',
          'text': '800 件'
        },
        {
          'label': '退租待入库',
          'text': '2,400 件'
        },
        {
          'label': '库区',
          'text': '原料区 RA'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['09-02', '退租入库', 'TZRK-20260902-008', '+60', '5,260'],
          'links': {
            2: '租赁管理/退租入库列表.html'
          }
        },
        {
          'cells': ['09-01', '调拨出库', 'DB-20260901-003', '-1,000', '4,260'],
          'links': {
            2: '仓储作业/库存调拨列表.html'
          }
        },
        {
          'cells': ['08-28', '采购入库', 'CGRK-20260828-012', '+2,400', '5,260'],
          'links': {
            2: '采购管理/采购入库列表.html'
          }
        },
        {
          'cells': ['08-24', '采购入库', 'CGRK-20260824-005', '+1,600', '2,860'],
          'links': {
            2: '采购管理/采购入库列表.html'
          }
        },
        {
          'cells': ['08-22', '组装领料', 'ZZ-20260822-006', '-640', '1,260']
        }
      ],
      'chain': [
        {
          'role': '采购入库',
          'name': '来源 · 两单 +4,000',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '库存台账（本物料）',
          'name': 'LJ-A100 · 原料区 RA',
          'self': true
        },
        {
          'role': '组装 / 调拨',
          'name': '去向 · 领料与备料',
        }
      ],
      'timeline': [
        {
          't': '08-24',
          'text': '最近大批入库 · CGRK-20260824-005（+1,600）',
          'who': '张伟'
        },
        {
          't': '08-22',
          'text': '组装领料 · ZZ-20260822-006（-640，V2.1 配比 4 只/套 × 160 套）',
          'who': '刘志强'
        },
        {
          't': '09-01',
          'text': '调拨出库 · DB-20260901-003（-1,000 → 成品区 RB 备料）',
          'who': '赵芳'
        }
      ]
    },
    'LJ-B200': {
      'row': {"fields": {"name": "铰链 锌合金 65mm", "cls": "零部件", "project": "PRJ-2601/02", "area": "原料区 RA"}, "cells": ["铰链 锌合金 65mm", "<span class=\"tag tag-blue\">零部件</span>", "PRJ-2601/02", "<span class=\"td-num\">2,640</span>", "<span class=\"td-num\">400</span>", "<span class=\"td-num\">1,600</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>4,640</b></span>", "件", "原料区 RA"], "ops": [{"t": "库存流水", "detail": true}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
      'title': '库存流水',
      'titleNo': 'LJ-B200 铰链 锌合金 65mm',
      'info': [
        {
          'label': '物料编码',
          'text': 'LJ-B200'
        },
        {
          'label': '名称规格',
          'text': '铰链 锌合金 65mm',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '零部件'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2601 / 2602',
          'full': true
        },
        {
          'label': '在库',
          'text': '2,640 件'
        },
        {
          'label': '在途（退租未审核）',
          'text': '400 件'
        },
        {
          'label': '客户端（租出）',
          'text': '1,600 件'
        },
        {
          'label': '退租待入库',
          'text': '0 件'
        },
        {
          'label': '库区',
          'text': '原料区 RA'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['09-01', '盘盈入库', 'QTRK-20260901-003', '+120', '2,640'],
          'links': {
            2: '仓储作业/其他入库列表.html'
          }
        },
        {
          'cells': ['08-28', '采购入库', 'CGRK-20260828-012', '+2,000', '2,520'],
          'links': {
            2: '采购管理/采购入库列表.html'
          }
        },
        {
          'cells': ['08-27', '采购入库', 'CGRK-20260827-009', '+500', '520'],
          'links': {
            2: '采购管理/采购入库列表.html'
          }
        },
        {
          'cells': ['08-20', '期初建账', '—', '+20', '20']
        }
      ],
      'chain': [
        {
          'role': '采购入库',
          'name': '来源 · CGRK 两单',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '库存台账（本物料）',
          'name': 'LJ-B200 · 原料区 RA',
          'self': true
        },
        {
          'role': 'B1 销售',
          'name': '去向 · 销售出库随单',
          'url': '销售管理/销售出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-01',
          'text': '盘盈入库 +120 · QTRK-20260901-003（盘点差异处理）',
          'who': '赵芳'
        },
        {
          't': '08-28',
          'text': '采购入库 +2,000 · CGRK-20260828-012',
          'who': '张伟'
        }
      ]
    },
    'LJ-C300': {
      'row': {"fields": {"name": "围板 HDPE 波纹板", "cls": "零部件", "project": "PRJ-2601", "area": "原料区 RA"}, "cells": ["围板 HDPE 波纹板", "<span class=\"tag tag-blue\">零部件</span>", "PRJ-2601", "<span class=\"td-num\">1,860</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">1,600</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>3,460</b></span>", "件", "原料区 RA"], "ops": [{"t": "库存流水", "detail": true}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
      'title': '库存流水',
      'titleNo': 'LJ-C300 围板 HDPE 波纹板',
      'info': [
        {
          'label': '物料编码',
          'text': 'LJ-C300'
        },
        {
          'label': '名称规格',
          'text': '围板 HDPE 波纹板',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '零部件'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2601',
          'full': true
        },
        {
          'label': '在库',
          'text': '1,860 件'
        },
        {
          'label': '在途（退租未审核）',
          'text': '0 件'
        },
        {
          'label': '客户端（租出）',
          'text': '1,600 件'
        },
        {
          'label': '退租待入库',
          'text': '0 件'
        },
        {
          'label': '库区',
          'text': '原料区 RA'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['09-02', '拆卸产出', 'CX-20260902-006', '+100', '1,860']
        },
        {
          'cells': ['08-30', '组装领料', 'ZZ-20260830-004', '-600', '1,760']
        },
        {
          'cells': ['08-29', '组装领料', 'ZZ-20260829-003', '-400', '2,360']
        },
        {
          'cells': ['08-18', '拆卸产出', 'CX-20260818-003', '+60', '2,760']
        }
      ],
      'chain': [
        {
          'role': '拆卸产出',
          'name': '来源 · BOM 反拆回库',
        },
        {
          'role': '库存台账（本物料）',
          'name': 'LJ-C300 · 原料区 RA',
          'self': true
        },
        {
          'role': '组装领料',
          'name': '去向 · ZH-2601-A 配方（4 件/套）',
        }
      ],
      'timeline': [
        {
          't': '09-02',
          'text': '拆卸产出 +100 · CX-20260902-006',
          'who': '张伟'
        },
        {
          't': '08-30',
          'text': '组装领料 -600 · ZZ-20260830-004（300 套 × 2）',
          'who': '刘志强'
        }
      ]
    },
    'LJ-D400': {
      'row': {"fields": {"name": "箱盖 ABS 吸塑", "cls": "零部件", "project": "PRJ-2601/04", "area": "原料区 RA"}, "cells": ["箱盖 ABS 吸塑", "<span class=\"tag tag-blue\">零部件</span>", "PRJ-2601/04", "<span class=\"td-num\">980</span>", "<span class=\"td-num\">480</span>", "<span class=\"td-num\">400</span>", "<span class=\"td-num\">1,000</span>", "<span class=\"td-num\"><b>1,860</b></span>", "件", "原料区 RA"], "ops": [{"t": "库存流水", "detail": true}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
      'title': '库存流水',
      'titleNo': 'LJ-D400 箱盖 ABS 吸塑',
      'info': [
        {
          'label': '物料编码',
          'text': 'LJ-D400'
        },
        {
          'label': '名称规格',
          'text': '箱盖 ABS 吸塑',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '零部件'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2601 / 2604',
          'full': true
        },
        {
          'label': '在库',
          'text': '980 件'
        },
        {
          'label': '在途（退租未审核）',
          'text': '480 件'
        },
        {
          'label': '客户端（租出）',
          'text': '400 件'
        },
        {
          'label': '退租待入库',
          'text': '1,000 件'
        },
        {
          'label': '库区',
          'text': '原料区 RA'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['09-02', '销售出库', 'XSCK-20260902-015', '-1,500', '980'],
          'links': {
            2: '销售管理/销售出库列表.html'
          }
        },
        {
          'cells': ['08-29', '销售出库', 'XSCK-20260829-013', '-2,000', '2,480'],
          'links': {
            2: '销售管理/销售出库列表.html'
          }
        },
        {
          'cells': ['08-28', '退货入库', 'QTRK-20260828-002', '+300', '4,480'],
          'links': {
            2: '仓储作业/其他入库列表.html'
          }
        },
        {
          'cells': ['08-26', '销售出库', 'XSCK-20260826-012', '-400', '4,180'],
          'links': {
            2: '销售管理/销售出库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '采购入库',
          'name': '来源 · 宁波华塑',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '库存台账（本物料）',
          'name': 'LJ-D400 · 原料区 RA',
          'self': true
        },
        {
          'role': 'B1 销售',
          'name': '去向 · 销售出库',
          'url': '销售管理/销售出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-02',
          'text': '销售出库 -1,500 · XSCK-20260902-015（在库 980 + 在途补充）',
          'who': '张伟'
        },
        {
          't': '08-28',
          'text': '退货入库 +300 · QTRK-20260828-002',
          'who': '张伟'
        }
      ]
    },
    'LJ-F600': {
      'row': {"fields": {"name": "内衬 EPE 珍珠棉", "cls": "零部件", "project": "PRJ-2603/05", "area": "原料区 RA"}, "cells": ["内衬 EPE 珍珠棉", "<span class=\"tag tag-blue\">零部件</span>", "PRJ-2603/05", "<span class=\"td-num\">1,520</span>", "<span class=\"td-num\">120</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>1,640</b></span>", "件", "原料区 RA"], "ops": [{"t": "库存流水", "detail": true}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
      'title': '库存流水',
      'titleNo': 'LJ-F600 内衬 EPE 珍珠棉',
      'info': [
        {
          'label': '物料编码',
          'text': 'LJ-F600'
        },
        {
          'label': '名称规格',
          'text': '内衬 EPE 珍珠棉',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '零部件'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2603 / 2605',
          'full': true
        },
        {
          'label': '在库',
          'text': '1,520 件'
        },
        {
          'label': '在途（退租未审核）',
          'text': '120 件'
        },
        {
          'label': '客户端（租出）',
          'text': '0 件'
        },
        {
          'label': '退租待入库',
          'text': '0 件'
        },
        {
          'label': '库区',
          'text': '原料区 RA'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['08-29', '盘亏出库', 'QTCK-20260829-003', '-80', '1,520'],
          'links': {
            2: '仓储作业/其他出库列表.html'
          }
        },
        {
          'cells': ['08-26', '销售出库', 'XSCK-20260826-012', '-400', '1,600'],
          'links': {
            2: '销售管理/销售出库列表.html'
          }
        },
        {
          'cells': ['08-24', '采购入库', 'CGRK-20260824-005', '+3,000', '2,000'],
          'links': {
            2: '采购管理/采购入库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '采购入库',
          'name': '来源 · CGRK-20260824-005',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '库存台账（本物料）',
          'name': 'LJ-F600 · 原料区 RA',
          'self': true
        },
        {
          'role': 'B1 销售 / BOM 可选配',
          'name': '去向',
          'url': '销售管理/销售出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-29',
          'text': '盘亏出库 -80 · QTCK-20260829-003（盘点差异）',
          'who': '赵芳'
        },
        {
          't': '08-24',
          'text': '采购入库 +3,000 · CGRK-20260824-005',
          'who': '李国栋'
        }
      ]
    },
    'WBX-1210L': {
      'row': {"fields": {"name": "围板箱 1200×1000×970", "cls": "租赁器具", "project": "PRJ-2601/04", "area": "成品区 RB"}, "cells": ["围板箱 1200×1000×970", "<span class=\"tag tag-green\">租赁器具</span>", "PRJ-2601/04", "<span class=\"td-num\">2,120</span>", "<span class=\"td-num\">160</span>", "<span class=\"td-num\">3,120</span>", "<span class=\"td-num\">80</span>", "<span class=\"td-num\"><b>2,480</b></span>", "只", "成品区 RB"], "ops": [{"t": "库存流水", "detail": true}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
      'title': '库存流水',
      'titleNo': 'WBX-1210L 围板箱 1200×1000×970',
      'info': [
        {
          'label': '物料编码',
          'text': 'WBX-1210L'
        },
        {
          'label': '名称规格',
          'text': '围板箱 1200×1000×970',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '租赁器具'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2601 / 2604',
          'full': true
        },
        {
          'label': '在库',
          'text': '2,120 只'
        },
        {
          'label': '在途（退租未审核）',
          'text': '160 只'
        },
        {
          'label': '客户端（租出）',
          'text': '3,120 只'
        },
        {
          'label': '退租待入库',
          'text': '80 只'
        },
        {
          'label': '库区',
          'text': '成品区 RB'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['09-02', '拆卸产出', 'CX-20260902-006', '+50', '2,120']
        },
        {
          'cells': ['09-01', '采购入库', 'CGRK-20260828-011', '+300', '2,070'],
          'links': {
            2: '采购管理/采购入库列表.html'
          }
        },
        {
          'cells': ['08-18', '拆卸产出', 'CX-20260818-003', '+30', '1,770']
        }
      ],
      'chain': [
        {
          'role': '采购入库 / 拆卸产出',
          'name': '来源',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '库存台账（本物料）',
          'name': 'WBX-1210L · 成品区 RB',
          'self': true
        },
        {
          'role': '组合出库 / 租出',
          'name': '去向 · ZH-2601-A 组装与出租',
          'url': '租赁管理/组合出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-01',
          'text': '采购入库 +300 · CGRK-20260828-011（宁波华塑）',
          'who': '张伟'
        },
        {
          't': '09-02',
          'text': '拆卸产出 +50 · CX-20260902-006',
          'who': '张伟'
        }
      ]
    },
    'WBX-1210M': {
      'row': {"fields": {"name": "围板箱 1200×1000×590", "cls": "租赁器具", "project": "PRJ-2602", "area": "成品区 RB"}, "cells": ["围板箱 1200×1000×590", "<span class=\"tag tag-green\">租赁器具</span>", "PRJ-2602", "<span class=\"td-num\">860</span>", "<span class=\"td-num\">40</span>", "<span class=\"td-num\">1,020</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>1,000</b></span>", "只", "成品区 RB"], "ops": [{"t": "库存流水", "detail": true}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
      'title': '库存流水',
      'titleNo': 'WBX-1210M 围板箱 1200×1000×590',
      'info': [
        {
          'label': '物料编码',
          'text': 'WBX-1210M'
        },
        {
          'label': '名称规格',
          'text': '围板箱 1200×1000×590',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '租赁器具'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2602',
          'full': true
        },
        {
          'label': '在库',
          'text': '860 只'
        },
        {
          'label': '在途（退租未审核）',
          'text': '40 只'
        },
        {
          'label': '客户端（租出）',
          'text': '1,020 只'
        },
        {
          'label': '退租待入库',
          'text': '0 只'
        },
        {
          'label': '库区',
          'text': '成品区 RB'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['08-20', '其他入库（期初）', 'QTRK-20260820-001', '+15', '860'],
          'links': {
            2: '仓储作业/其他入库列表.html'
          }
        },
        {
          'cells': ['01-06', '期初建账', '—', '+845', '845']
        }
      ],
      'chain': [
        {
          'role': '期初 / 例外入库',
          'name': '来源',
          'url': '仓储作业/其他入库列表.html'
        },
        {
          'role': '库存台账（本物料）',
          'name': 'WBX-1210M · 成品区 RB',
          'self': true
        },
        {
          'role': '租出',
          'name': '去向 · 客户在租（库存查询）',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-20',
          'text': '期初补录 +15 · QTRK-20260820-001',
          'who': '赵芳'
        },
        {
          't': '持续',
          'text': '循环出租 · 在租 1,020 只',
          'who': '—'
        }
      ]
    },
    'PLT-1210P': {
      'row': {"fields": {"name": "塑料托盘 1200×1000", "cls": "租赁器具", "project": "PRJ-2602/03", "area": "成品区 RB"}, "cells": ["塑料托盘 1200×1000", "<span class=\"tag tag-green\">租赁器具</span>", "PRJ-2602/03", "<span class=\"td-num\">1,410</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">1,860</span>", "<span class=\"td-num\">60</span>", "<span class=\"td-num\"><b>1,700</b></span>", "块", "成品区 RB"], "ops": [{"t": "库存流水", "detail": true}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
      'title': '库存流水',
      'titleNo': 'PLT-1210P 塑料托盘 1200×1000',
      'info': [
        {
          'label': '物料编码',
          'text': 'PLT-1210P'
        },
        {
          'label': '名称规格',
          'text': '塑料托盘 1200×1000',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '租赁器具'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2602 / 2603',
          'full': true
        },
        {
          'label': '在库',
          'text': '1,410 块'
        },
        {
          'label': '在途（退租未审核）',
          'text': '0 块'
        },
        {
          'label': '客户端（租出）',
          'text': '1,860 块'
        },
        {
          'label': '退租待入库',
          'text': '60 块'
        },
        {
          'label': '库区',
          'text': '成品区 RB'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['08-26', '拆卸产出', 'CX-20260826-004', '+30', '1,410']
        },
        {
          'cells': ['08-25', '采购入库', 'CGRK-20260825-006', '+500', '1,380'],
          'links': {
            2: '采购管理/采购入库列表.html'
          }
        },
        {
          'cells': ['02-22', '期初建账', '—', '+880', '880']
        }
      ],
      'chain': [
        {
          'role': '采购入库',
          'name': '来源 · CGRK-20260825-006',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '库存台账（本物料）',
          'name': 'PLT-1210P · 成品区 RB',
          'self': true
        },
        {
          'role': '租出 / 组装',
          'name': '去向',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-25',
          'text': '采购入库 +500 · CGRK-20260825-006（常州正大）',
          'who': '张伟'
        },
        {
          't': '08-26',
          'text': '拆卸产出 +30 · CX-20260826-004',
          'who': '张伟'
        }
      ]
    },
    'BTC-6040': {
      'row': {"fields": {"name": "料箱 600×400×340", "cls": "租赁器具", "project": "PRJ-2602", "area": "成品区 RB"}, "cells": ["料箱 600×400×340", "<span class=\"tag tag-green\">租赁器具</span>", "PRJ-2602", "<span class=\"td-num\">3,300</span>", "<span class=\"td-num\">40</span>", "<span class=\"td-num\">2,480</span>", "<span class=\"td-num\">120</span>", "<span class=\"td-num\"><b>3,940</b></span>", "只", "成品区 RB"], "ops": [{"t": "库存流水", "detail": true}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
      'title': '库存流水',
      'titleNo': 'BTC-6040 料箱 600×400×340',
      'info': [
        {
          'label': '物料编码',
          'text': 'BTC-6040'
        },
        {
          'label': '名称规格',
          'text': '料箱 600×400×340',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '租赁器具'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2602',
          'full': true
        },
        {
          'label': '在库',
          'text': '3,300 只'
        },
        {
          'label': '在途（退租未审核）',
          'text': '40 只'
        },
        {
          'label': '客户端（租出）',
          'text': '2,480 只'
        },
        {
          'label': '退租待入库',
          'text': '120 只'
        },
        {
          'label': '库区',
          'text': '成品区 RB'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['08-30', '拆卸产出', 'CX-20260830-005', '+40', '3,300']
        },
        {
          'cells': ['08-26', '采购入库', 'CGRK-20260826-008', '+800', '3,260'],
          'links': {
            2: '采购管理/采购入库列表.html'
          }
        },
        {
          'cells': ['08-18', '拆卸产出', 'CX-20260818-003', '+30', '2,460']
        }
      ],
      'chain': [
        {
          'role': '采购入库',
          'name': '来源 · CGRK-20260826-008',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '库存台账（本物料）',
          'name': 'BTC-6040 · 成品区 RB',
          'self': true
        },
        {
          'role': '组装 / 租出',
          'name': '去向 · ZH-2602-B 配方',
        }
      ],
      'timeline': [
        {
          't': '08-26',
          'text': '采购入库 +800 · CGRK-20260826-008（宁波华塑）',
          'who': '张伟'
        },
        {
          't': '08-30',
          'text': '拆卸产出 +40 · CX-20260830-005',
          'who': '张伟'
        }
      ]
    },
    'ZH-2601-A': {
      'title': '库存流水',
      'titleNo': 'ZH-2601-A 驾驶室围板箱整箱套件',
      'info': [
        {
          'label': '物料编码',
          'text': 'ZH-2601-A'
        },
        {
          'label': '名称规格',
          'text': '驾驶室围板箱整箱套件',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '组合件'
        },
        {
          'label': 'BOM 版本',
          'text': 'V2.1'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2601',
          'full': true
        },
        {
          'label': '在库',
          'text': '640 套'
        },
        {
          'label': '在途（退租未审核）',
          'text': '60 套'
        },
        {
          'label': '客户端（租出）',
          'text': '3,120 套'
        },
        {
          'label': '退租待入库',
          'text': '80 套'
        },
        {
          'label': '库区',
          'text': '成品区 RB'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['09-04', '组装入库', 'ZZ-20260904-007', '+32', '640']
        },
        {
          'cells': ['09-03', '组合出库', 'CK-20260903-016', '-60', '608'],
          'links': {
            2: '租赁管理/组合出库列表.html'
          }
        },
        {
          'cells': ['09-02', '拆卸出库', 'CX-20260902-006', '-50', '668']
        },
        {
          'cells': ['08-30', '组合出库', 'CK-20260830-015', '-180', '718'],
          'links': {
            2: '租赁管理/组合出库列表.html'
          }
        },
        {
          'cells': ['08-29', '组装入库', 'ZZ-20260829-003', '+200', '898']
        }
      ],
      'chain': [
        {
          'role': '组装',
          'name': '产出 · ZZ 系列入库',
        },
        {
          'role': '库存台账（本物料）',
          'name': 'ZH-2601-A · 成品区 RB',
          'self': true
        },
        {
          'role': '组合出库',
          'name': '租出 · CK 系列出库',
          'url': '租赁管理/组合出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-04',
          'text': '组装入库 +32 · ZZ-20260904-007（拆散件再组装 · 组装中）',
          'who': '刘志强'
        },
        {
          't': '09-03',
          'text': '循环再出租 -60 · CK-20260903-016（退租回库件）',
          'who': '张伟'
        }
      ]
    },
    'ZH-2602-B': {
      'title': '库存流水',
      'titleNo': 'ZH-2602-B 冲压件料箱组套',
      'info': [
        {
          'label': '物料编码',
          'text': 'ZH-2602-B'
        },
        {
          'label': '名称规格',
          'text': '冲压件料箱组套',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '组合件'
        },
        {
          'label': 'BOM 版本',
          'text': 'V1.3'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2602',
          'full': true
        },
        {
          'label': '在库',
          'text': '820 套'
        },
        {
          'label': '在途（退租未审核）',
          'text': '45 套'
        },
        {
          'label': '客户端（租出）',
          'text': '4,120 套'
        },
        {
          'label': '退租待入库',
          'text': '0 套'
        },
        {
          'label': '库区',
          'text': '成品区 RB'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['08-30', '拆卸出库', 'CX-20260830-005', '-40', '820']
        },
        {
          'cells': ['08-28', '组合出库', 'CK-20260828-010', '-200', '860'],
          'links': {
            2: '租赁管理/组合出库列表.html'
          }
        },
        {
          'cells': ['08-22', '期初建账', '—', '+1,060', '1,060']
        }
      ],
      'chain': [
        {
          'role': '组装',
          'name': '产出 · BOM 配方入库',
        },
        {
          'role': '库存台账（本物料）',
          'name': 'ZH-2602-B · 成品区 RB',
          'self': true
        },
        {
          'role': '组合出库',
          'name': '租出 · CK 系列出库',
          'url': '租赁管理/组合出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-28',
          'text': '组合出库 -200 · CK-20260828-010',
          'who': '张伟'
        },
        {
          't': '08-30',
          'text': '拆卸出库 -40 · CX-20260830-005（散件需求）',
          'who': '张伟'
        }
      ]
    },
    'ZH-2603-C': {
      'title': '库存流水',
      'titleNo': 'ZH-2603-C 电池托盘护角套件',
      'info': [
        {
          'label': '物料编码',
          'text': 'ZH-2603-C'
        },
        {
          'label': '名称规格',
          'text': '电池托盘护角套件',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '组合件'
        },
        {
          'label': 'BOM 版本',
          'text': 'V1.0'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2603',
          'full': true
        },
        {
          'label': '在库',
          'text': '150 套'
        },
        {
          'label': '在途（退租未审核）',
          'text': '0 套'
        },
        {
          'label': '客户端（租出）',
          'text': '1,020 套'
        },
        {
          'label': '退租待入库',
          'text': '20 套'
        },
        {
          'label': '库区',
          'text': '成品区 RB'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['08-29', '组合出库', 'CK-20260829-013', '-60', '150'],
          'links': {
            2: '租赁管理/组合出库列表.html'
          }
        },
        {
          'cells': ['08-27', '组装入库', 'ZZ-20260827-001', '+150', '210']
        },
        {
          'cells': ['08-26', '拆卸出库', 'CX-20260826-004', '-30', '60']
        }
      ],
      'chain': [
        {
          'role': '组装',
          'name': '产出 · ZZ-20260827-001',
        },
        {
          'role': '库存台账（本物料）',
          'name': 'ZH-2603-C · 成品区 RB',
          'self': true
        },
        {
          'role': '组合出库',
          'name': '租出 · CK-20260829-013',
          'url': '租赁管理/组合出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-27',
          'text': '组装入库 +150 · ZZ-20260827-001',
          'who': '王海生'
        },
        {
          't': '08-29',
          'text': '组合出库 -60 · CK-20260829-013',
          'who': '张伟'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 器具出租履历 rentTracks：键 = ZL 租赁单号（原宿主 租出台账 2026-09-10 并入租赁单列表；现供 弹窗/器具出租履历.html 独立模板 10 行全量） */
  /* 弹窗 trackModal · 触发锚「详情」；含循环再出租/部分退租/超期场景 */
  rentTracks: {
    'ZL-20260903-034': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "combo": "ZH-2601-A × 60 套（退租回库件再出租）", "src": "自有", "date": "2026-09-03", "back": "2026-12-03", "status": "在租"}, "cells": ["PRJ-2601", "一汽解放汽车有限公司", "ZH-2601-A × 60 套（退租回库件再出租）", "自有", "<span class=\"td-num\">2026-09-03</span>", "2026-12-03", "<span class=\"td-num\">0 套</span>", "<span class=\"tag tag-blue\">在租</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '器具出租履历',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260903-034',
          'full': true
        },
        {
          'label': '状态',
          'tag': '在租'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '器具 / 组合件',
          'text': 'ZH-2601-A × 60 套（退租回库件再出租）',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有'
        },
        {
          'label': '起租日期',
          'text': '2026-09-03'
        },
        {
          'label': '租期止',
          'text': '2026-12-03'
        },
        {
          'label': '累计退回',
          'text': '0 套'
        },
        {
          'label': '退回日期',
          'text': '—'
        }
      ],
      'feeSecTitle': '出租记录',
      'feeCols': ['#', '租赁单号', '客户', '起租', '退租', '数量', '状态'],
      'fees': [
        {
          'cells': ['1', 'ZL-20260903-034', '一汽解放汽车有限公司', '09-03', '—', '60 套', '在租'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        },
        {
          'cells': ['2', 'ZL-20260610-015', '一汽解放汽车有限公司', '06-15', '09-02', '60 套', '已退租（前手 · 回库件循环）'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '退租入库',
          'name': 'TZRK-20260902-008 · 回库件',
          'url': '租赁管理/退租入库列表.html'
        },
        {
          'role': '出租履历（本单）',
          'name': 'ZL-20260903-034 · 循环再出租',
          'self': true
        },
        {
          'role': '库存查询·客户在租',
          'name': '客户占用 · 计租',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '09-02',
          'text': '退租入库 · TZRK-20260902-008（60 套回库）',
          'who': '张伟'
        },
        {
          't': '09-03',
          'text': '循环再出租 · ZL-20260903-034',
          'who': '王琳'
        }
      ]
    },
    'ZL-20260823-033': {
      'row': {"fields": {"project": "PRJ-2604", "customer": "一汽解放汽车有限公司", "combo": "ZH-2604-D × 40 套", "src": "混合（自购 + 租入）", "date": "2026-08-23", "back": "2026-11-23", "status": "已退租"}, "note": "1", "cells": ["PRJ-2604", "一汽解放汽车有限公司", "ZH-2604-D × 40 套", "<span class=\"tag tag-orange\">混合（自购 + 租入）</span>", "<span class=\"td-num\">2026-08-23</span>", "2026-11-23", "<span class=\"td-num\">40 套</span>", "<span class=\"tag tag-green\">已退租</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '器具出租履历',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260823-033',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已退租'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2604'
        },
        {
          'label': '器具 / 组合件',
          'text': 'ZH-2604-D × 40 套',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '混合（自购 + 租入）'
        },
        {
          'label': '起租日期',
          'text': '2026-08-23'
        },
        {
          'label': '租期止',
          'text': '2026-11-23'
        },
        {
          'label': '累计退回',
          'text': '40 套'
        },
        {
          'label': '退回日期',
          'text': '—'
        }
      ],
      'feeSecTitle': '出租记录',
      'feeCols': ['#', '租赁单号', '客户', '起租', '退租', '数量', '状态'],
      'fees': [
        {
          'cells': ['1', 'ZL-20260823-033', '一汽解放汽车有限公司', '08-23', '09-02', '40 套', '已退租'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '组装',
          'name': 'ZZ-20260822-006 · 混合配方产出',
        },
        {
          'role': '出租履历（本单）',
          'name': 'ZL-20260823-033',
          'self': true
        },
        {
          'role': '退租入库',
          'name': 'TZRK-20260902-010 · 拆散分流',
          'url': '租赁管理/退租入库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-23',
          'text': '起租 · 混合套件 40 套',
          'who': '王琳'
        },
        {
          't': '09-02',
          'text': '退租入库 · 按 BOM 拆散分流（自有回库 + 租入转归还）',
          'who': '张伟'
        }
      ]
    },
    'ZL-20260312-0088': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "combo": "ZH-2601-A × 620 套", "src": "自有", "date": "2026-03-12", "back": "长期循环", "status": "在租"}, "cells": ["PRJ-2601", "一汽解放汽车有限公司", "ZH-2601-A × 620 套", "自有", "<span class=\"td-num\">2026-03-12</span>", "长期循环", "<span class=\"td-num\">126 套</span>", "<span class=\"tag tag-blue\">在租</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '器具出租履历',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260312-0088',
          'full': true
        },
        {
          'label': '状态',
          'tag': '在租'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '器具 / 组合件',
          'text': 'ZH-2601-A × 620 套',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有'
        },
        {
          'label': '起租日期',
          'text': '2026-03-12'
        },
        {
          'label': '租期止',
          'text': '长期循环'
        },
        {
          'label': '累计退回',
          'text': '126 套'
        },
        {
          'label': '退回日期',
          'text': '—'
        }
      ],
      'feeSecTitle': '出租记录',
      'feeCols': ['#', '租赁单号', '客户', '起租', '退租', '数量', '状态'],
      'fees': [
        {
          'cells': ['1', 'ZL-20260312-0088', '一汽解放汽车有限公司', '03-12', '长期循环', '620 套', '在租'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        },
        {
          'cells': ['2', 'ZL-20260312-0088 · 部分退租', '一汽解放汽车有限公司', '—', '09-04', '200 套', '退租中']
        }
      ],
      'chain': [
        {
          'role': '出租履历（本单）',
          'name': 'ZL-20260312-0088 · 长期循环',
          'self': true
        },
        {
          'role': '退租入库',
          'name': '退 200 / 留 294 · 直接入库',
          'url': '租赁管理/退租入库列表.html'
        },
        {
          'role': '库存查询·客户在租',
          'name': '余量继续计租',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '03-12',
          'text': '起租 · 长期循环协议',
          'who': '王琳'
        },
        {
          't': '09-04',
          'text': '部分退租 · 退 200 套（直接入库）',
          'who': '客户提交'
        }
      ]
    },
    'ZL-20260402-0102': {
      'row': {"fields": {"project": "PRJ-2602", "customer": "上汽大众宁波分公司", "combo": "ZH-2602-B × 840 套", "src": "自有", "date": "2026-04-02", "back": "长期循环", "status": "在租"}, "cells": ["PRJ-2602", "上汽大众宁波分公司", "ZH-2602-B × 840 套", "自有", "<span class=\"td-num\">2026-04-02</span>", "长期循环", "<span class=\"td-num\">212 套</span>", "<span class=\"tag tag-blue\">在租</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '器具出租履历',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260402-0102',
          'full': true
        },
        {
          'label': '状态',
          'tag': '在租'
        },
        {
          'label': '客户',
          'text': '上汽大众宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '器具 / 组合件',
          'text': 'ZH-2602-B × 840 套',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有'
        },
        {
          'label': '起租日期',
          'text': '2026-04-02'
        },
        {
          'label': '租期止',
          'text': '长期循环'
        },
        {
          'label': '累计退回',
          'text': '212 套'
        },
        {
          'label': '退回日期',
          'text': '—'
        }
      ],
      'feeSecTitle': '出租记录',
      'feeCols': ['#', '租赁单号', '客户', '起租', '退租', '数量', '状态'],
      'fees': [
        {
          'cells': ['1', 'ZL-20260402-0102', '上汽大众宁波分公司', '04-02', '长期循环', '840 套', '在租'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '出租履历（本单）',
          'name': 'ZL-20260402-0102 · 长期循环',
          'self': true
        },
        {
          'role': '库存查询·客户在租',
          'name': '客户占用 · 计租',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '04-02',
          'text': '起租 · 长期循环协议',
          'who': '王琳'
        },
        {
          't': '持续',
          'text': '循环出租 · 累计退回 212 套后再投放'
        }
      ]
    },
    'ZL-20260518-0145': {
      'row': {"fields": {"project": "PRJ-2603", "customer": "小鹏汽车科技有限公司", "combo": "ZH-2603-C × 420 套", "src": "自有", "date": "2026-05-18", "back": "长期循环", "status": "在租"}, "cells": ["PRJ-2603", "小鹏汽车科技有限公司", "ZH-2603-C × 420 套", "自有", "<span class=\"td-num\">2026-05-18</span>", "长期循环", "<span class=\"td-num\">96 套</span>", "<span class=\"tag tag-blue\">在租</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '器具出租履历',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260518-0145',
          'full': true
        },
        {
          'label': '状态',
          'tag': '在租'
        },
        {
          'label': '客户',
          'text': '小鹏汽车科技有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2603'
        },
        {
          'label': '器具 / 组合件',
          'text': 'ZH-2603-C × 420 套',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有'
        },
        {
          'label': '起租日期',
          'text': '2026-05-18'
        },
        {
          'label': '租期止',
          'text': '长期循环'
        },
        {
          'label': '累计退回',
          'text': '96 套'
        },
        {
          'label': '退回日期',
          'text': '—'
        }
      ],
      'feeSecTitle': '出租记录',
      'feeCols': ['#', '租赁单号', '客户', '起租', '退租', '数量', '状态'],
      'fees': [
        {
          'cells': ['1', 'ZL-20260518-0145', '小鹏汽车科技有限公司', '05-18', '长期循环', '420 套', '在租'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '出租履历（本单）',
          'name': 'ZL-20260518-0145 · 长期循环',
          'self': true
        },
        {
          'role': '库存查询·客户在租',
          'name': '客户占用 · 计租',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '05-18',
          'text': '起租 · 长期循环协议',
          'who': '王琳'
        },
        {
          't': '持续',
          'text': '循环出租 · 累计退回 96 套后再投放'
        }
      ]
    },
    'ZL-20260610-0167': {
      'row': {"fields": {"project": "PRJ-2604", "customer": "东风本田汽车有限公司", "combo": "ZH-2601-A × 380 套", "src": "自有", "date": "2026-06-10", "back": "长期循环", "status": "已退回"}, "cells": ["PRJ-2604", "东风本田汽车有限公司", "ZH-2601-A × 380 套", "自有", "<span class=\"td-num\">2026-06-10</span>", "长期循环", "<span class=\"td-num\">380 套</span>", "<span class=\"tag tag-green\">已退回</span>", "2026-08-20"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '器具出租履历',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260610-0167',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已退回'
        },
        {
          'label': '客户',
          'text': '东风本田汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2604'
        },
        {
          'label': '器具 / 组合件',
          'text': 'ZH-2601-A × 380 套',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有'
        },
        {
          'label': '起租日期',
          'text': '2026-06-10'
        },
        {
          'label': '租期止',
          'text': '长期循环'
        },
        {
          'label': '累计退回',
          'text': '380 套'
        },
        {
          'label': '退回日期',
          'text': '2026-08-20'
        }
      ],
      'feeSecTitle': '出租记录',
      'feeCols': ['#', '租赁单号', '客户', '起租', '退租', '数量', '状态'],
      'fees': [
        {
          'cells': ['1', 'ZL-20260610-0167', '东风本田汽车有限公司', '06-10', '08-20', '380 套', '已退回'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '出租履历（本单）',
          'name': 'ZL-20260610-0167',
          'self': true
        },
        {
          'role': '退租入库',
          'name': '08-20 全量退回',
          'url': '租赁管理/退租入库列表.html'
        }
      ],
      'timeline': [
        {
          't': '06-10',
          'text': '起租 · 380 套',
          'who': '王琳'
        },
        {
          't': '08-20',
          'text': '全量退回 · 退租入库',
          'who': '张伟'
        }
      ]
    },
    'ZL-20260108-0031': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "combo": "WBX-1210L × 300 只", "src": "租入-路凯", "date": "2026-01-08", "back": "2026-08-31", "status": "超期未还"}, "cells": ["PRJ-2601", "一汽解放汽车有限公司", "WBX-1210L × 300 只", "<span class=\"tag tag-orange\">租入-路凯</span>", "<span class=\"td-num\">2026-01-08</span>", "2026-08-31", "<span class=\"td-num\">0 只</span>", "<span class=\"tag tag-red\">超期未还</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '器具出租履历',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260108-0031',
          'full': true
        },
        {
          'label': '状态',
          'tag': '超期未还'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '器具 / 组合件',
          'text': 'WBX-1210L × 300 只',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '租入-路凯'
        },
        {
          'label': '起租日期',
          'text': '2026-01-08'
        },
        {
          'label': '租期止',
          'text': '2026-08-31'
        },
        {
          'label': '累计退回',
          'text': '0 只'
        },
        {
          'label': '退回日期',
          'text': '—'
        }
      ],
      'feeSecTitle': '出租记录',
      'feeCols': ['#', '租赁单号', '客户', '起租', '退租', '数量', '状态'],
      'fees': [
        {
          'cells': ['1', 'ZL-20260108-0031', '一汽解放汽车有限公司', '01-08', '—', '300 只', '超期未还'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '租入单',
          'name': '路凯资产 · 转租',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'role': '出租履历（本单）',
          'name': 'ZL-20260108-0031 · 超期',
          'self': true
        },
        {
          'role': '库存查询·客户在租',
          'name': '超期 240 只待催收',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '01-08',
          'text': '起租 · 租入转租（路凯资产）',
          'who': '王琳'
        },
        {
          't': '08-31',
          'text': '租期止 · 超期未还（催收中）',
          'who': '王琳'
        }
      ]
    },
    'ZL-20260222-0056': {
      'row': {"fields": {"project": "PRJ-2602", "customer": "上汽大众宁波分公司", "combo": "PLT-1210P × 260 块", "src": "自有", "date": "2026-02-22", "back": "长期循环", "status": "已退回"}, "cells": ["PRJ-2602", "上汽大众宁波分公司", "PLT-1210P × 260 块", "自有", "<span class=\"td-num\">2026-02-22</span>", "长期循环", "<span class=\"td-num\">260 块</span>", "<span class=\"tag tag-green\">已退回</span>", "2026-07-15"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '器具出租履历',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260222-0056',
          'full': true
        },
        {
          'label': '状态',
          'tag': '已退回'
        },
        {
          'label': '客户',
          'text': '上汽大众宁波分公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '器具 / 组合件',
          'text': 'PLT-1210P × 260 块',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有'
        },
        {
          'label': '起租日期',
          'text': '2026-02-22'
        },
        {
          'label': '租期止',
          'text': '长期循环'
        },
        {
          'label': '累计退回',
          'text': '260 块'
        },
        {
          'label': '退回日期',
          'text': '2026-07-15'
        }
      ],
      'feeSecTitle': '出租记录',
      'feeCols': ['#', '租赁单号', '客户', '起租', '退租', '数量', '状态'],
      'fees': [
        {
          'cells': ['1', 'ZL-20260222-0056', '上汽大众宁波分公司', '02-22', '07-15', '260 块', '已退回'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '出租履历（本单）',
          'name': 'ZL-20260222-0056',
          'self': true
        },
        {
          'role': '退租入库',
          'name': '07-15 全量退回',
          'url': '租赁管理/退租入库列表.html'
        }
      ],
      'timeline': [
        {
          't': '02-22',
          'text': '起租 · 260 块',
          'who': '王琳'
        },
        {
          't': '07-15',
          'text': '全量退回 · 退租入库',
          'who': '张伟'
        }
      ]
    },
    'ZL-20260701-0188': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "combo": "ZH-2601-A × 150 套", "src": "自有", "date": "2026-07-01", "back": "2026-09-30", "status": "在租"}, "cells": ["PRJ-2601", "一汽解放汽车有限公司", "ZH-2601-A × 150 套", "自有", "<span class=\"td-num\">2026-07-01</span>", "2026-09-30", "<span class=\"td-num\">0 套</span>", "<span class=\"tag tag-blue\">在租</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '器具出租履历',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260701-0188',
          'full': true
        },
        {
          'label': '状态',
          'tag': '在租'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '器具 / 组合件',
          'text': 'ZH-2601-A × 150 套',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有'
        },
        {
          'label': '起租日期',
          'text': '2026-07-01'
        },
        {
          'label': '租期止',
          'text': '2026-09-30'
        },
        {
          'label': '累计退回',
          'text': '150 套'
        },
        {
          'label': '退回日期',
          'text': '—'
        }
      ],
      'feeSecTitle': '出租记录',
      'feeCols': ['#', '租赁单号', '客户', '起租', '退租', '数量', '状态'],
      'fees': [
        {
          'cells': ['1', 'ZL-20260701-0188', '一汽解放汽车有限公司', '07-01', '—', '150 套', '在租'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '出租履历（本单）',
          'name': 'ZL-20260701-0188',
          'self': true
        },
        {
          'role': '库存查询·客户在租',
          'name': '即将到期（09-30 止）',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '07-01',
          'text': '起租 · 150 套',
          'who': '王琳'
        },
        {
          't': '—',
          'text': '在租中 · 租期止 09-30（即将到期页签跟踪）',
          'off': true
        }
      ]
    },
    'ZL-20260506-0121': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "combo": "ZH-2601-A × 96 套", "src": "自有", "date": "2026-05-06", "back": "长期循环", "status": "缺损待赔"}, "cells": ["PRJ-2601", "一汽解放汽车有限公司", "ZH-2601-A × 96 套", "自有", "<span class=\"td-num\">2026-05-06</span>", "长期循环", "<span class=\"td-num\">7 套</span>", "<span class=\"tag tag-red\">缺损待赔</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '器具出租履历',
      'info': [
        {
          'label': '租赁单号',
          'text': 'ZL-20260506-0121',
          'full': true
        },
        {
          'label': '状态',
          'tag': '缺损待赔'
        },
        {
          'label': '客户',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '器具 / 组合件',
          'text': 'ZH-2601-A × 96 套',
          'full': true
        },
        {
          'label': '资产来源',
          'text': '自有'
        },
        {
          'label': '起租日期',
          'text': '2026-05-06'
        },
        {
          'label': '租期止',
          'text': '长期循环'
        },
        {
          'label': '累计退回',
          'text': '7 套'
        },
        {
          'label': '退回日期',
          'text': '—'
        }
      ],
      'feeSecTitle': '出租记录',
      'feeCols': ['#', '租赁单号', '客户', '起租', '退租', '数量', '状态'],
      'fees': [
        {
          'cells': ['1', 'ZL-20260506-0121', '一汽解放汽车有限公司', '05-06', '—', '96 套', '缺损待赔'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '出租履历（本单）',
          'name': 'ZL-20260506-0121',
          'self': true
        },
        {
          'role': '丢损赔偿',
          'name': '退租验收发现缺损 · 转赔偿',
        }
      ],
      'timeline': [
        {
          't': '05-06',
          'text': '起租 · 96 套',
          'who': '王琳'
        },
        {
          't': '09-05',
          'text': '退租验收发现 7 套缺损 · 待赔偿处理',
          'who': '张伟'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 资产轨迹 assetTracks：键 = 器具编码（原宿主 租赁管理/在租台账.html 已删·9 行留档；现供库存查询 openTrack） */
  /* 弹窗 trackModal · 触发锚「资产轨迹」；履历模板=弹窗/器具出租履历.html（原租出台账共用） */
  /* 注意：WBX-1210L(旧) 键须排在 WBX-1210L 前（前缀包含防误匹配） */
  
  /* 宿主变更注记（2026-09-10 台账合并）：原列表宿主 租赁管理/在租台账.html 已删（row.cells/ops 留档不再渲染）；本实体 info/timeline 由 仓储作业/库存查询.html「客户在租」下钻 openTrack 渲染 */assetTracks: {
    'WBX-1210L(旧)': {
      'row': {"fields": {"name": "围板箱 旧箱体批次", "project": "—", "status": "已报废"}, "cells": ["围板箱 旧箱体批次", "—", "<span class=\"td-num\"><b>0</b></span>", "48.0", "—", "<span class=\"td-num\">0</span>", "<span class=\"tag tag-gray\">已报废</span>"], "ops": [{"t": "资产轨迹", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}, {"t": "报废", "act": "openModal('scrapModal')"}]},
      'title': '资产轨迹',
      'info': [
        {
          'label': '器具编码',
          'text': 'WBX-1210L(旧)'
        },
        {
          'label': '名称',
          'text': '围板箱 旧箱体批次',
          'full': true
        },
        {
          'label': '所属项目',
          'text': '—'
        },
        {
          'label': '在租数量',
          'text': '0'
        },
        {
          'label': '平均循环次数',
          'text': '48.0'
        },
        {
          'label': '平均租期',
          'text': '—'
        },
        {
          'label': '超期数量',
          'text': '0'
        },
        {
          'label': '循环状态',
          'tag': '已报废'
        },
        {
          'label': '资产构成',
          'text': '自有（旧批次 · 已报废核销）',
          'full': true
        }
      ],
      'feeSecTitle': '最近流转',
      'feeCols': ['日期', '单据', '事项', '数量'],
      'fees': [
        {
          'cells': ['09-01', 'QTCK-20260901-004', '报废出库 · 旧箱体批次 35 只', '-35 只'],
          'links': {
            1: '仓储作业/其他出库列表.html'
          }
        },
        {
          'cells': ['08-31', 'PD-202608-02', '盘点确认 · 批内待报废 35 只', '-35 只'],
          'links': {
            1: '仓储作业/盘点列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '库存盘点',
          'name': 'PD-202608-02 · 确认待报废',
          'url': '仓储作业/盘点列表.html'
        },
        {
          'role': '资产轨迹（本器具）',
          'name': 'WBX-1210L(旧) · 已报废',
          'self': true
        },
        {
          'role': '其他出库',
          'name': 'QTCK-20260901-004 · 报废核销',
          'url': '仓储作业/其他出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-31',
          'text': '盘点确认旧批次待报废',
          'who': '李国栋'
        },
        {
          't': '09-01',
          'text': '报废出库 · 资产核销（不可再出租）',
          'who': '赵芳'
        }
      ]
    },
    'WBX-1210L': {
      'row': {"fields": {"name": "围板箱 1200×1000×970", "project": "PRJ-2601/2604", "status": "在租"}, "note": "1", "cells": ["围板箱 1200×1000×970", "PRJ-2601/2604", "<span class=\"td-num\"><b>3,120</b></span>", "21.6", "86", "<span class=\"td-num\" style=\"color:var(--danger)\">128</span>", "<span class=\"tag tag-blue\">在租</span>"], "ops": [{"t": "资产轨迹", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}, {"t": "报废", "act": "openModal('scrapModal')"}]},
      'title': '资产轨迹',
      'info': [
        {
          'label': '器具编码',
          'text': 'WBX-1210L'
        },
        {
          'label': '名称',
          'text': '围板箱 1200×1000×970',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601/2604'
        },
        {
          'label': '在租数量',
          'text': '3,120'
        },
        {
          'label': '平均循环次数',
          'text': '21.6'
        },
        {
          'label': '平均租期',
          'text': '86'
        },
        {
          'label': '超期数量',
          'text': '128'
        },
        {
          'label': '循环状态',
          'tag': '在租'
        },
        {
          'label': '资产构成',
          'text': '自有 2,120 + 租入-路凯 1,000',
          'full': true
        }
      ],
      'feeSecTitle': '最近流转',
      'feeCols': ['日期', '单据', '事项', '数量'],
      'fees': [
        {
          'cells': ['09-03', 'GHCK-20260903-002', '分流归还 · 租入侧大箱 4 只缺损归还路凯', '-4 只'],
          'links': {
            1: '租赁管理/租入归还列表.html'
          }
        },
        {
          'cells': ['09-02', 'TZRK-20260902-010', '退租入库 · ZH-2604-D 拆散（含围板箱大箱 × 10）', '-10 只'],
          'links': {
            1: '租赁管理/退租入库列表.html'
          }
        },
        {
          'cells': ['08-24', 'CK-20260824-009', '组合出库 · ZH-2604-D × 40 套（配比含围板箱）', '租出 40 套'],
          'links': {
            1: '租赁管理/组合出库列表.html'
          }
        },
        {
          'cells': ['08-16', 'RZRK-20260816-021', '租入入库 · 路凯围板箱 30 只（转租）', '+30 只'],
          'links': {
            1: '租赁管理/租入入库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '租入入库 / 采购入库',
          'name': '来源',
          'url': '租赁管理/租入入库列表.html'
        },
        {
          'role': '资产轨迹（本器具）',
          'name': 'WBX-1210L',
          'self': true
        },
        {
          'role': '租赁单列表·退回进度',
          'name': '租出与退回统计（租赁单列表）',
          'url': '租赁管理/租赁单列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-16',
          'text': '租入入库 +30（路凯 · L3 转租链）',
          'who': '李国栋'
        },
        {
          't': '09-02',
          'text': 'L4 退租拆散 · 大箱 10 只分流归还',
          'who': '张伟'
        },
        {
          't': '当前',
          'text': '在租 3,120 · 超期 128 只待催还'
        }
      ]
    },
    'WBX-1210M': {
      'row': {"fields": {"name": "围板箱 1200×1000×590", "project": "PRJ-2602", "status": "在租"}, "cells": ["围板箱 1200×1000×590", "PRJ-2602", "<span class=\"td-num\"><b>1,020</b></span>", "14.2", "64", "<span class=\"td-num\">0</span>", "<span class=\"tag tag-blue\">在租</span>"], "ops": [{"t": "资产轨迹", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}, {"t": "报废", "act": "openModal('scrapModal')"}]},
      'title': '资产轨迹',
      'info': [
        {
          'label': '器具编码',
          'text': 'WBX-1210M'
        },
        {
          'label': '名称',
          'text': '围板箱 1200×1000×590',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '在租数量',
          'text': '1,020'
        },
        {
          'label': '平均循环次数',
          'text': '14.2'
        },
        {
          'label': '平均租期',
          'text': '64'
        },
        {
          'label': '超期数量',
          'text': '0'
        },
        {
          'label': '循环状态',
          'tag': '在租'
        },
        {
          'label': '资产构成',
          'text': '自有 1,020',
          'full': true
        }
      ],
      'feeSecTitle': '最近流转',
      'feeCols': ['日期', '单据', '事项', '数量'],
      'fees': [
        {
          'cells': ['06-30', '—', '租出在租 1,020 只（多租赁单累计）', '—']
        },
        {
          'cells': ['01-06', '—', '器具建档 · 启用', '—']
        }
      ],
      'chain': [
        {
          'role': '资产轨迹（本器具）',
          'name': 'WBX-1210M',
          'self': true
        },
        {
          'role': '库存查询·客户在租',
          'name': '四态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '01-06',
          'text': '建档启用',
          'who': '系统'
        },
        {
          't': '当前',
          'text': '在租 1,020 · 无超期'
        }
      ]
    },
    'PLT-1210P': {
      'row': {"fields": {"name": "塑料托盘 1200×1000", "project": "PRJ-2602/2603", "status": "在租"}, "cells": ["塑料托盘 1200×1000", "PRJ-2602/2603", "<span class=\"td-num\"><b>1,860</b></span>", "26.4", "102", "<span class=\"td-num\" style=\"color:var(--danger)\">36</span>", "<span class=\"tag tag-blue\">在租</span>"], "ops": [{"t": "资产轨迹", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}, {"t": "报废", "act": "openModal('scrapModal')"}]},
      'title': '资产轨迹',
      'info': [
        {
          'label': '器具编码',
          'text': 'PLT-1210P'
        },
        {
          'label': '名称',
          'text': '塑料托盘 1200×1000',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602/2603'
        },
        {
          'label': '在租数量',
          'text': '1,860'
        },
        {
          'label': '平均循环次数',
          'text': '26.4'
        },
        {
          'label': '平均租期',
          'text': '102'
        },
        {
          'label': '超期数量',
          'text': '36'
        },
        {
          'label': '循环状态',
          'tag': '在租'
        },
        {
          'label': '资产构成',
          'text': '自有 1,860',
          'full': true
        }
      ],
      'feeSecTitle': '最近流转',
      'feeCols': ['日期', '单据', '事项', '数量'],
      'fees': [
        {
          'cells': ['08-26', 'CX-20260826-004', '拆卸产出 · ZH-2603-C 反拆', '+30 块']
        },
        {
          'cells': ['08-25', 'CGRK-20260825-006', '采购入库 · 常州正大', '+500 块'],
          'links': {
            1: '采购管理/采购入库列表.html'
          }
        },
        {
          'cells': ['02-22', 'ZL-20260222-0056', '租出 260 块（07-15 已退回）', '租出 260 块'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '资产轨迹（本器具）',
          'name': 'PLT-1210P',
          'self': true
        },
        {
          'role': '库存查询·客户在租',
          'name': '四态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-25',
          'text': '采购入库 +500',
          'who': '张伟'
        },
        {
          't': '当前',
          'text': '在租 1,860 · 超期 36 块待催还'
        }
      ]
    },
    'PLT-1210W': {
      'row': {"fields": {"name": "木托盘 1200×1000", "project": "PRJ-2605", "status": "已退回"}, "cells": ["木托盘 1200×1000", "PRJ-2605", "<span class=\"td-num\"><b>0</b></span>", "—", "—", "<span class=\"td-num\">0</span>", "<span class=\"tag tag-green\">已退回</span>"], "ops": [{"t": "资产轨迹", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}, {"t": "报废", "act": "openModal('scrapModal')"}]},
      'title': '资产轨迹',
      'info': [
        {
          'label': '器具编码',
          'text': 'PLT-1210W'
        },
        {
          'label': '名称',
          'text': '木托盘 1200×1000',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2605'
        },
        {
          'label': '在租数量',
          'text': '0'
        },
        {
          'label': '平均循环次数',
          'text': '—'
        },
        {
          'label': '平均租期',
          'text': '—'
        },
        {
          'label': '超期数量',
          'text': '0'
        },
        {
          'label': '循环状态',
          'tag': '已退回'
        },
        {
          'label': '资产构成',
          'text': '自有（已全量报废核销 22 块）',
          'full': true
        }
      ],
      'feeSecTitle': '最近流转',
      'feeCols': ['日期', '单据', '事项', '数量'],
      'fees': [
        {
          'cells': ['08-25', 'QTCK-20260825-002', '报废出库 · 断裂批次', '-22 块'],
          'links': {
            1: '仓储作业/其他出库列表.html'
          }
        },
        {
          'cells': ['07-15', '—', '全量退回 · 暂无在租', '—']
        }
      ],
      'chain': [
        {
          'role': '其他出库',
          'name': 'QTCK-20260825-002 · 报废核销',
          'url': '仓储作业/其他出库列表.html'
        },
        {
          'role': '资产轨迹（本器具）',
          'name': 'PLT-1210W · 已退回',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '07-15',
          'text': '全量退回',
          'who': '张伟'
        },
        {
          't': '08-25',
          'text': '断裂批次报废 -22 块',
          'who': '赵芳'
        }
      ]
    },
    'BTC-6040': {
      'row': {"fields": {"name": "料箱 600×400×340", "project": "PRJ-2602", "status": "在租"}, "cells": ["料箱 600×400×340", "PRJ-2602", "<span class=\"td-num\"><b>2,480</b></span>", "31.8", "118", "<span class=\"td-num\">0</span>", "<span class=\"tag tag-blue\">在租</span>"], "ops": [{"t": "资产轨迹", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}, {"t": "报废", "act": "openModal('scrapModal')"}]},
      'title': '资产轨迹',
      'info': [
        {
          'label': '器具编码',
          'text': 'BTC-6040'
        },
        {
          'label': '名称',
          'text': '料箱 600×400×340',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '在租数量',
          'text': '2,480'
        },
        {
          'label': '平均循环次数',
          'text': '31.8'
        },
        {
          'label': '平均租期',
          'text': '118'
        },
        {
          'label': '超期数量',
          'text': '0'
        },
        {
          'label': '循环状态',
          'tag': '在租'
        },
        {
          'label': '资产构成',
          'text': '自有 2,480',
          'full': true
        }
      ],
      'feeSecTitle': '最近流转',
      'feeCols': ['日期', '单据', '事项', '数量'],
      'fees': [
        {
          'cells': ['08-30', 'CX-20260830-005', '拆卸产出 · ZH-2602-B 反拆', '+40 只']
        },
        {
          'cells': ['08-26', 'CGRK-20260826-008', '采购入库 · 宁波华塑', '+800 只'],
          'links': {
            1: '采购管理/采购入库列表.html'
          }
        },
        {
          'cells': ['04-02', 'ZL-20260402-0102', '租出 · ZH-2602-B 组套 840 套（含料箱）', '租出 840 套'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '资产轨迹（本器具）',
          'name': 'BTC-6040',
          'self': true
        },
        {
          'role': '库存查询·客户在租',
          'name': '四态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-26',
          'text': '采购入库 +800',
          'who': '张伟'
        },
        {
          't': '当前',
          'text': '在租 2,480 · 无超期'
        }
      ]
    },
    'ZH-2601-A': {
      'row': {"fields": {"name": "驾驶室围板箱整箱套件", "project": "PRJ-2601", "status": "在租"}, "cells": ["驾驶室围板箱整箱套件", "PRJ-2601", "<span class=\"td-num\"><b>3,120</b></span>", "18.9", "92", "<span class=\"td-num\" style=\"color:var(--danger)\">64</span>", "<span class=\"tag tag-blue\">在租</span>"], "ops": [{"t": "资产轨迹", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}, {"t": "报废", "act": "openModal('scrapModal')"}]},
      'title': '资产轨迹',
      'info': [
        {
          'label': '器具编码',
          'text': 'ZH-2601-A'
        },
        {
          'label': '名称',
          'text': '驾驶室围板箱整箱套件',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2601'
        },
        {
          'label': '在租数量',
          'text': '3,120'
        },
        {
          'label': '平均循环次数',
          'text': '18.9'
        },
        {
          'label': '平均租期',
          'text': '92'
        },
        {
          'label': '超期数量',
          'text': '64'
        },
        {
          'label': '循环状态',
          'tag': '在租'
        },
        {
          'label': '资产构成',
          'text': '自有（BOM V2.1 组合件）',
          'full': true
        }
      ],
      'feeSecTitle': '最近流转',
      'feeCols': ['日期', '单据', '事项', '数量'],
      'fees': [
        {
          'cells': ['09-03', 'CK-20260903-016', '循环再出租 · 退租回库件', '-60 套'],
          'links': {
            1: '租赁管理/组合出库列表.html'
          }
        },
        {
          'cells': ['09-02', 'TZRK-20260902-008', '退租入库 · 回库待检', '+60 套'],
          'links': {
            1: '租赁管理/退租入库列表.html'
          }
        },
        {
          'cells': ['08-30', 'CK-20260830-015', '组合出库 · 租出 180 套', '-180 套'],
          'links': {
            1: '租赁管理/组合出库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '组装',
          'name': 'BOM V2.1 产出',
        },
        {
          'role': '资产轨迹（本器具）',
          'name': 'ZH-2601-A',
          'self': true
        },
        {
          'role': '库存查询·客户在租',
          'name': '四态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-30',
          'text': '组合出库 -180',
          'who': '张伟'
        },
        {
          't': '09-03',
          'text': '回库件循环再出租 -60（CK-20260903-016）',
          'who': '张伟'
        }
      ]
    },
    'ZH-2602-B': {
      'row': {"fields": {"name": "冲压件料箱组套", "project": "PRJ-2602", "status": "在租"}, "cells": ["冲压件料箱组套", "PRJ-2602", "<span class=\"td-num\"><b>4,120</b></span>", "22.7", "110", "<span class=\"td-num\">0</span>", "<span class=\"tag tag-blue\">在租</span>"], "ops": [{"t": "资产轨迹", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}, {"t": "报废", "act": "openModal('scrapModal')"}]},
      'title': '资产轨迹',
      'info': [
        {
          'label': '器具编码',
          'text': 'ZH-2602-B'
        },
        {
          'label': '名称',
          'text': '冲压件料箱组套',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2602'
        },
        {
          'label': '在租数量',
          'text': '4,120'
        },
        {
          'label': '平均循环次数',
          'text': '22.7'
        },
        {
          'label': '平均租期',
          'text': '110'
        },
        {
          'label': '超期数量',
          'text': '0'
        },
        {
          'label': '循环状态',
          'tag': '在租'
        },
        {
          'label': '资产构成',
          'text': '自有（BOM V1.3 组合件）',
          'full': true
        }
      ],
      'feeSecTitle': '最近流转',
      'feeCols': ['日期', '单据', '事项', '数量'],
      'fees': [
        {
          'cells': ['08-30', 'CX-20260830-005', '拆卸出库 · 散件需求', '-40 套']
        },
        {
          'cells': ['08-28', 'CK-20260828-010', '组合出库 · 租出 200 套', '-200 套'],
          'links': {
            1: '租赁管理/组合出库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '组装',
          'name': 'BOM V1.3 产出',
        },
        {
          'role': '资产轨迹（本器具）',
          'name': 'ZH-2602-B',
          'self': true
        },
        {
          'role': '库存查询·客户在租',
          'name': '四态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-28',
          'text': '组合出库 -200',
          'who': '张伟'
        },
        {
          't': '当前',
          'text': '在租 4,120 · 无超期'
        }
      ]
    },
    'ZH-2603-C': {
      'row': {"fields": {"name": "电池托盘护角套件", "project": "PRJ-2603", "status": "缺损待赔"}, "cells": ["电池托盘护角套件", "PRJ-2603", "<span class=\"td-num\"><b>1,020</b></span>", "9.6", "58", "<span class=\"td-num\" style=\"color:var(--danger)\">12</span>", "<span class=\"tag tag-red\">缺损待赔</span>"], "ops": [{"t": "资产轨迹", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}, {"t": "报废", "act": "openModal('scrapModal')"}]},
      'title': '资产轨迹',
      'info': [
        {
          'label': '器具编码',
          'text': 'ZH-2603-C'
        },
        {
          'label': '名称',
          'text': '电池托盘护角套件',
          'full': true
        },
        {
          'label': '所属项目',
          'text': 'PRJ-2603'
        },
        {
          'label': '在租数量',
          'text': '1,020'
        },
        {
          'label': '平均循环次数',
          'text': '9.6'
        },
        {
          'label': '平均租期',
          'text': '58'
        },
        {
          'label': '超期数量',
          'text': '12'
        },
        {
          'label': '循环状态',
          'tag': '缺损待赔'
        },
        {
          'label': '资产构成',
          'text': '自有（BOM V1.0 组合件）',
          'full': true
        }
      ],
      'feeSecTitle': '最近流转',
      'feeCols': ['日期', '单据', '事项', '数量'],
      'fees': [
        {
          'cells': ['08-29', 'CK-20260829-013', '组合出库 · 租出 60 套', '-60 套'],
          'links': {
            1: '租赁管理/组合出库列表.html'
          }
        },
        {
          'cells': ['08-27', 'ZZ-20260827-001', '组装入库 +150 套', '+150 套']
        },
        {
          'cells': ['08-26', 'CX-20260826-004', '拆卸出库 · 散件需求', '-30 套']
        }
      ],
      'chain': [
        {
          'role': '组装',
          'name': 'BOM V1.0 产出',
        },
        {
          'role': '资产轨迹（本器具）',
          'name': 'ZH-2603-C',
          'self': true
        },
        {
          'role': '丢损赔偿',
          'name': '缺损待赔 · 转赔偿处理',
        }
      ],
      'timeline': [
        {
          't': '08-27',
          'text': '组装入库 +150',
          'who': '王海生'
        },
        {
          't': '当前',
          'text': '在租 1,020 · 缺损待赔 12 套'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 客商 partners：键 = DW 客商编码（基础数据/客商管理.html 8 行全量） */
  /* 四段语义映射：档案信息/往来统计/关联链/操作记录；统计数取既有实体真实单号 */
  partners: {
    'DW-0001': {
      'row': {"fields": {"name": "一汽解放汽车有限公司", "type": "客户", "contact": "袁明", "status": "正常", "date": "2026-08-12"}, "cells": ["一汽解放汽车有限公司", "<span class=\"tag tag-blue\">客户</span>", "袁明", "138****6621", "增值税专票 13%", "<span class=\"tag tag-green\">正常</span>", "2026-08-12"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "开票资料", "act": "openModal('createModal')"}]},
      'title': '客商详情',
      'titleNo': '一汽解放汽车有限公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0001'
        },
        {
          'label': '客商名称',
          'text': '一汽解放汽车有限公司',
          'full': true
        },
        {
          'label': '客商类型',
          'text': '客户'
        },
        {
          'label': '状态',
          'tag': '正常'
        },
        {
          'label': '联系人',
          'text': '袁明 138****6621'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新时间',
          'text': '2026-08-12'
        },
        {
          'label': '关联项目',
          'text': 'PRJ-2601 长春基地围板箱租赁',
          'url': '项目管理/项目档案.html',
          'full': true
        }
      ],
      'feeSecTitle': '联系人 / 往来统计',
      'feeCols': ['统计项', '数值', '说明'],
      'fees': [
        {
          'cells': ['本月营收（PRJ-2601）', '486,200 元', '租赁 + 销售费']
        },
        {
          'cells': ['累计开票', '312,000 元', 'INV-20260830-012 等']
        },
        {
          'cells': ['在租器具', '3,860 只', '围板箱 3,120 / 托盘 740']
        },
        {
          'cells': ['联系人', '袁明 · 业务对接', '138****6621']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0001 一汽解放',
          'self': true
        },
        {
          'role': '关联项目',
          'name': 'PRJ-2601',
          'url': '项目管理/项目档案.html'
        },
        {
          'role': '销售订单',
          'name': 'SO-20260827-0039 等',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '应收账单',
          'name': '租赁费 / 销售费',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '2026-01',
          'text': '建档 · 客户',
          'who': '系统'
        },
        {
          't': '2026-08-12',
          'text': '资质与开票信息更新',
          'who': '财务-周敏'
        },
        {
          't': '至今',
          'text': '持续合作 · PRJ-2601 在租 3,860 只'
        }
      ]
    },
    'DW-0002': {
      'row': {"fields": {"name": "上汽大众汽车有限公司宁波分公司", "type": "客户", "contact": "何静", "status": "正常", "date": "2026-08-05"}, "cells": ["上汽大众汽车有限公司宁波分公司", "<span class=\"tag tag-blue\">客户</span>", "何静", "139****0233", "增值税专票 13%", "<span class=\"tag tag-green\">正常</span>", "2026-08-05"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "开票资料", "act": "openModal('createModal')"}]},
      'title': '客商详情',
      'titleNo': '上汽大众汽车有限公司宁波分公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0002'
        },
        {
          'label': '客商名称',
          'text': '上汽大众汽车有限公司宁波分公司',
          'full': true
        },
        {
          'label': '客商类型',
          'text': '客户'
        },
        {
          'label': '状态',
          'tag': '正常'
        },
        {
          'label': '联系人',
          'text': '何静 139****0233'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新时间',
          'text': '2026-08-05'
        },
        {
          'label': '关联项目',
          'text': 'PRJ-2602 宁波工厂料箱组套租赁',
          'url': '项目管理/项目档案.html',
          'full': true
        }
      ],
      'feeSecTitle': '联系人 / 往来统计',
      'feeCols': ['统计项', '数值', '说明'],
      'fees': [
        {
          'cells': ['本月营收（PRJ-2602）', '358,900 元', '租赁费']
        },
        {
          'cells': ['累计开票', '186,200 元', 'INV-20260826-011 等']
        },
        {
          'cells': ['在租器具', '4,120 只', 'ZH-2602-B 组套']
        },
        {
          'cells': ['联系人', '何静 · 业务对接', '139****0233']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0002 上汽大众宁波',
          'self': true
        },
        {
          'role': '关联项目',
          'name': 'PRJ-2602',
          'url': '项目管理/项目档案.html'
        },
        {
          'role': '租赁单',
          'name': 'ZL-20260828-031 等',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '应收账单',
          'name': '租赁费',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '2026-02',
          'text': '建档 · 客户',
          'who': '系统'
        },
        {
          't': '2026-08-05',
          'text': '开票信息更新',
          'who': '财务-周敏'
        },
        {
          't': '至今',
          'text': '持续合作 · PRJ-2602 在租 4,120 只'
        }
      ]
    },
    'DW-0003': {
      'row': {"fields": {"name": "小鹏汽车科技有限公司", "type": "客户", "contact": "林芳", "status": "正常", "date": "2026-07-28"}, "cells": ["小鹏汽车科技有限公司", "<span class=\"tag tag-blue\">客户</span>", "林芳", "137****8845", "增值税专票 13%", "<span class=\"tag tag-green\">正常</span>", "2026-07-28"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "开票资料", "act": "openModal('createModal')"}]},
      'title': '客商详情',
      'titleNo': '小鹏汽车科技有限公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0003'
        },
        {
          'label': '客商名称',
          'text': '小鹏汽车科技有限公司',
          'full': true
        },
        {
          'label': '客商类型',
          'text': '客户'
        },
        {
          'label': '状态',
          'tag': '正常'
        },
        {
          'label': '联系人',
          'text': '林芳 137****8845'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新时间',
          'text': '2026-07-28'
        },
        {
          'label': '关联项目',
          'text': 'PRJ-2603 广州工厂护角套件租赁',
          'url': '项目管理/项目档案.html',
          'full': true
        }
      ],
      'feeSecTitle': '联系人 / 往来统计',
      'feeCols': ['统计项', '数值', '说明'],
      'fees': [
        {
          'cells': ['本月营收（PRJ-2603）', '241,500 元', '租赁费']
        },
        {
          'cells': ['累计开票', '98,000 元', 'INV-20260815-009']
        },
        {
          'cells': ['在租器具', '1,020 只', 'ZH-2603-C 组套']
        },
        {
          'cells': ['联系人', '林芳 · 业务对接', '137****8845']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0003 小鹏汽车',
          'self': true
        },
        {
          'role': '关联项目',
          'name': 'PRJ-2603',
          'url': '项目管理/项目档案.html'
        },
        {
          'role': '租赁单',
          'name': 'ZL-20260720-022',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '应收账单',
          'name': '租赁费',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '2026-03',
          'text': '建档 · 客户',
          'who': '系统'
        },
        {
          't': '2026-07-28',
          'text': '开票信息更新',
          'who': '财务-周敏'
        },
        {
          't': '至今',
          'text': '持续合作 · PRJ-2603 在租 1,020 只'
        }
      ]
    },
    'DW-0004': {
      'row': {"fields": {"name": "东风本田汽车有限公司", "type": "客户", "contact": "赵磊", "status": "停用", "date": "2026-06-30"}, "cells": ["东风本田汽车有限公司", "<span class=\"tag tag-blue\">客户</span>", "赵磊", "136****3312", "增值税专票 13%", "<span class=\"tag tag-gray\">停用</span>", "2026-06-30"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "开票资料", "act": "openModal('createModal')"}]},
      'title': '客商详情',
      'titleNo': '东风本田汽车有限公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0004'
        },
        {
          'label': '客商名称',
          'text': '东风本田汽车有限公司',
          'full': true
        },
        {
          'label': '客商类型',
          'text': '客户'
        },
        {
          'label': '状态',
          'tag': '停用'
        },
        {
          'label': '联系人',
          'text': '赵磊 136****3312'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新时间',
          'text': '2026-06-30'
        },
        {
          'label': '关联项目',
          'text': 'PRJ-2604 武汉工厂器具租赁（合作暂停）',
          'url': '项目管理/项目档案.html',
          'full': true
        }
      ],
      'feeSecTitle': '联系人 / 往来统计',
      'feeCols': ['统计项', '数值', '说明'],
      'fees': [
        {
          'cells': ['本月营收（PRJ-2604）', '1,280 元', '销售费（尾单）']
        },
        {
          'cells': ['在租器具', '96 套', 'ZH-2601-A（清理退租中）']
        },
        {
          'cells': ['联系人', '赵磊 · 业务对接', '136****3312']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0004 东风本田 · 停用',
          'self': true
        },
        {
          'role': '关联项目',
          'name': 'PRJ-2604',
          'url': '项目管理/项目档案.html'
        },
        {
          'role': '销售订单',
          'name': 'SO-20260828-0041',
          'url': '销售管理/销售订单列表.html'
        }
      ],
      'timeline': [
        {
          't': '2026-01',
          'text': '建档 · 客户',
          'who': '系统'
        },
        {
          't': '2026-06-30',
          'text': '合作暂停 · 档案停用（历史单据保留）',
          'who': '王琳'
        }
      ]
    },
    'DW-0101': {
      'row': {"fields": {"name": "宁波华塑包装制品有限公司", "type": "供应商", "contact": "孙建军", "status": "正常", "date": "2026-08-18"}, "cells": ["宁波华塑包装制品有限公司", "<span class=\"tag tag-green\">供应商</span>", "孙建军", "135****7790", "增值税专票 13%", "<span class=\"tag tag-green\">正常</span>", "2026-08-18"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "开票资料", "act": "openModal('createModal')"}]},
      'title': '客商详情',
      'titleNo': '宁波华塑包装制品有限公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0101'
        },
        {
          'label': '客商名称',
          'text': '宁波华塑包装制品有限公司',
          'full': true
        },
        {
          'label': '客商类型',
          'text': '供应商'
        },
        {
          'label': '状态',
          'tag': '正常'
        },
        {
          'label': '联系人',
          'text': '孙建军 135****7790'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新时间',
          'text': '2026-08-18'
        },
        {
          'label': '关联项目',
          'text': '— 围板箱 / 料箱 / 零部件供应',
          'url': '项目管理/项目档案.html',
          'full': true
        }
      ],
      'feeSecTitle': '联系人 / 往来统计',
      'feeCols': ['统计项', '数值', '说明'],
      'fees': [
        {
          'cells': ['本月采购额', '119,200 元', 'PO-20260901-017 / PO-20260825-014']
        },
        {
          'cells': ['累计付款', '35,200 元', 'PAY-20260828-003']
        },
        {
          'cells': ['主要供货', 'WBX-1210L / BTC-6040', '器具 + 零部件']
        },
        {
          'cells': ['联系人', '孙建军 · 供应对接', '135****7790']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0101 宁波华塑',
          'self': true
        },
        {
          'role': '采购订单',
          'name': 'PO-20260901-017 等',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '采购入库',
          'name': 'CGRK-20260826-008 等',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '应付账单',
          'name': 'AP-20260901-008',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '2026-01',
          'text': '建档 · 供应商',
          'who': '系统'
        },
        {
          't': '2026-08-18',
          'text': '供货品类扩充（料箱）',
          'who': '李国栋'
        }
      ]
    },
    'DW-0102': {
      'row': {"fields": {"name": "苏州联恒五金制品有限公司", "type": "供应商", "contact": "吴海涛", "status": "正常", "date": "2026-08-18"}, "cells": ["苏州联恒五金制品有限公司", "<span class=\"tag tag-green\">供应商</span>", "吴海涛", "133****5567", "增值税专票 13%", "<span class=\"tag tag-green\">正常</span>", "2026-08-18"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "开票资料", "act": "openModal('createModal')"}]},
      'title': '客商详情',
      'titleNo': '苏州联恒五金制品有限公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0102'
        },
        {
          'label': '客商名称',
          'text': '苏州联恒五金制品有限公司',
          'full': true
        },
        {
          'label': '客商类型',
          'text': '供应商'
        },
        {
          'label': '状态',
          'tag': '正常'
        },
        {
          'label': '联系人',
          'text': '吴海涛 133****5567'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新时间',
          'text': '2026-08-18'
        },
        {
          'label': '关联项目',
          'text': '— 锁扣 / 铰链 / 隔板等零部件供应',
          'url': '项目管理/项目档案.html',
          'full': true
        }
      ],
      'feeSecTitle': '联系人 / 往来统计',
      'feeCols': ['统计项', '数值', '说明'],
      'fees': [
        {
          'cells': ['本月采购额', '23,500 元', 'PO-20260902-018 / PO-20260828-015']
        },
        {
          'cells': ['累计付款', '12,300 元', 'PAY-20260902-005 等']
        },
        {
          'cells': ['在途到货', '3,400 件', 'CGRK-20260828-012 40 托']
        },
        {
          'cells': ['联系人', '吴海涛 · 供应对接', '133****5567']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0102 苏州联恒',
          'self': true
        },
        {
          'role': '采购订单',
          'name': 'PO-20260902-018 等',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '采购入库',
          'name': 'CGRK-20260828-012 等',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '应付账单',
          'name': 'AP-20260830-007',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '2026-01',
          'text': '建档 · 供应商',
          'who': '系统'
        },
        {
          't': '2026-08-18',
          'text': '月度对账完成',
          'who': '财务-周敏'
        }
      ]
    },
    'DW-0103': {
      'row': {"fields": {"name": "常州正大塑料托盘厂", "type": "供应商", "contact": "郑卫东", "status": "正常", "date": "2026-07-15"}, "cells": ["常州正大塑料托盘厂", "<span class=\"tag tag-green\">供应商</span>", "郑卫东", "138****2245", "增值税专票 13%", "<span class=\"tag tag-green\">正常</span>", "2026-07-15"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "开票资料", "act": "openModal('createModal')"}]},
      'title': '客商详情',
      'titleNo': '常州正大塑料托盘厂',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0103'
        },
        {
          'label': '客商名称',
          'text': '常州正大塑料托盘厂',
          'full': true
        },
        {
          'label': '客商类型',
          'text': '供应商'
        },
        {
          'label': '状态',
          'tag': '正常'
        },
        {
          'label': '联系人',
          'text': '郑卫东 138****2245'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新时间',
          'text': '2026-07-15'
        },
        {
          'label': '关联项目',
          'text': '— 塑料托盘 / 木托盘供应',
          'url': '项目管理/项目档案.html',
          'full': true
        }
      ],
      'feeSecTitle': '联系人 / 往来统计',
      'feeCols': ['统计项', '数值', '说明'],
      'fees': [
        {
          'cells': ['本月采购额', '62,100 元', 'PO-20260830-016 / PO-20260820-013']
        },
        {
          'cells': ['累计付款', '62,100 元', 'PAY-20260831-004 等（已结清）']
        },
        {
          'cells': ['主要供货', 'PLT-1210P / PLT-1210W', '托盘类']
        },
        {
          'cells': ['联系人', '郑卫东 · 供应对接', '138****2245']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0103 常州正大',
          'self': true
        },
        {
          'role': '采购订单',
          'name': 'PO-20260830-016 等',
          'url': '采购管理/采购订单列表.html'
        },
        {
          'role': '采购入库',
          'name': 'CGRK-20260827-010 等',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '应付账单',
          'name': '已结清',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '2026-02',
          'text': '建档 · 供应商',
          'who': '系统'
        },
        {
          't': '2026-07-15',
          'text': '供货验收合格率 100%',
          'who': '李国栋'
        }
      ]
    },
    'DW-0201': {
      'row': {"fields": {"name": "路凯包装运营（上海）有限公司", "type": "供应商", "contact": "路凯对接组", "status": "正常", "date": "2026-08-30"}, "cells": ["路凯包装运营（上海）有限公司", "<span class=\"tag tag-blue\">供应商</span>", "路凯对接组", "021-66****", "结算对账专用", "<span class=\"tag tag-green\">正常</span>", "2026-08-30"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "开票资料", "act": "openModal('createModal')"}]},
      'title': '客商详情',
      'titleNo': '路凯包装运营（上海）有限公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0201'
        },
        {
          'label': '客商名称',
          'text': '路凯包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '客商类型',
          'text': '供应商'
        },
        {
          'label': '状态',
          'tag': '正常'
        },
        {
          'label': '联系人',
          'text': '路凯对接组 021-66****'
        },
        {
          'label': '开票要求',
          'text': '结算对账专用'
        },
        {
          'label': '更新时间',
          'text': '2026-08-30'
        },
        {
          'label': '关联项目',
          'text': '— 围板箱租入运营（L3/L4 链）',
          'url': '项目管理/项目档案.html',
          'full': true
        }
      ],
      'feeSecTitle': '联系人 / 往来统计',
      'feeCols': ['统计项', '数值', '说明'],
      'fees': [
        {
          'cells': ['本月租金应付', '48,000 元', 'AP-20260903-009 / AP-20260903-010']
        },
        {
          'cells': ['预付款', '30,000 元', 'AP-20260905-012（预付冲抵）']
        },
        {
          'cells': ['赔付应付', '930 元', 'AP-20260903-011']
        },
        {
          'cells': ['联系人', '路凯对接组', '021-66****']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0201 路凯包装运营',
          'self': true
        },
        {
          'role': '租入单',
          'name': 'RZD-20260815-003 / -005',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'role': '租入归还',
          'name': 'GHCK-20260903-001 / -002',
          'url': '租赁管理/租入归还列表.html'
        },
        {
          'role': '应付账单',
          'name': '租金 / 预付 / 赔付',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '2026-08',
          'text': '租入合作建立（L3/L4 链）',
          'who': '王志远'
        },
        {
          't': '2026-09-05',
          'text': '预付 9 月度大箱租金 30,000 元',
          'who': '财务'
        },
        {
          't': '至今',
          'text': '月结租金 · 按周期自动生成应付'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 器具档案 appliances：键 = 器具编码（基础数据/器具档案.html 6 行全量） */
  /* BTC-6040S 键先于 BTC-6040（前缀包含防误匹配）；在租状态对齐库存查询客户态 */  products: {
    'WBX-1210L': {
      'row': {"fields": {"name": "围板箱 1200×1000×970", "cls": "围板箱", "spec": "1200×1000×970 mm", "src": "自有", "status": "启用", "date": "2026-01-06"}, "cells": ["围板箱 1200×1000×970", "<span class=\"tag tag-blue\">围板箱</span>", "1200×1000×970 mm", "只", "<span class=\"tag tag-green\">自有</span>", "<span class=\"td-num\">38.00</span>", "<span class=\"td-num\">38.00</span>", "<span class=\"tag tag-green\">启用</span>", "2026-01-06"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '产品详情',
      'info': [
        {
          'label': '产品编码',
          'text': 'WBX-1210L'
        },
        {
          'label': '名称',
          'text': '围板箱 1200×1000×970',
          'full': true
        },
        {
          'label': '分类',
          'text': '围板箱'
        },
        {
          'label': '规格',
          'text': '1200×1000×970 mm',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '只'
        },
        {
          'label': '归属权',
          'text': '自有（另有租入-路凯在库 · 见租入台账）',
          'full': true
        },
        {
          'label': '日租金',
          'text': '38.00 元 / 只 / 日'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-01-06'
        }
      ],
      'feeSecTitle': '在租状态（库存四态口径）',
      'feeCols': ['在租', '待归还（超期）', '平均循环', '平均租期', '台账'],
      'fees': [
        {
          'cells': ['3,120 只', '128 只', '21.6 次', '86 天', '客户在租'],
          'links': {
            4: '仓储作业/库存查询.html'
          }
        }
      ],
      'chain': [
        {
          'role': '产品档案（本档）',
          'name': 'WBX-1210L',
          'self': true
        },
        {
          'role': '租赁单列表·退回进度',
          'name': '租出记录 · 按来源统计（退回进度列）',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '库存查询·客户在租',
          'name': '四态统计 + 资产轨迹',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '2026-01-06',
          'text': '建档 · 启用（器具采购入库）',
          'who': '张伟'
        },
        {
          't': '持续',
          'text': '循环出租 · 平均循环 21.6 次 / 平均租期 86 天'
        },
        {
          't': '当前',
          'text': '在租 3,120 只 · 超期 128 只待催还'
        }
      ]
    },
    'WBX-1210M': {
      'row': {"fields": {"name": "围板箱 1200×1000×590", "cls": "围板箱", "spec": "1200×1000×590 mm", "src": "自有", "status": "启用", "date": "2026-01-06"}, "cells": ["围板箱 1200×1000×590", "<span class=\"tag tag-blue\">围板箱</span>", "1200×1000×590 mm", "只", "<span class=\"tag tag-green\">自有</span>", "<span class=\"td-num\">32.00</span>", "<span class=\"td-num\">32.00</span>", "<span class=\"tag tag-green\">启用</span>", "2026-01-06"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '产品详情',
      'info': [
        {
          'label': '产品编码',
          'text': 'WBX-1210M'
        },
        {
          'label': '名称',
          'text': '围板箱 1200×1000×590',
          'full': true
        },
        {
          'label': '分类',
          'text': '围板箱'
        },
        {
          'label': '规格',
          'text': '1200×1000×590 mm',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '只'
        },
        {
          'label': '归属权',
          'text': '自有',
          'full': true
        },
        {
          'label': '日租金',
          'text': '32.00 元 / 只 / 日'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-01-06'
        }
      ],
      'feeSecTitle': '在租状态（库存四态口径）',
      'feeCols': ['在租', '待归还（超期）', '平均循环', '平均租期', '台账'],
      'fees': [
        {
          'cells': ['1,020 只', '0 只', '14.2 次', '64 天', '客户在租'],
          'links': {
            4: '仓储作业/库存查询.html'
          }
        }
      ],
      'chain': [
        {
          'role': '产品档案（本档）',
          'name': 'WBX-1210M',
          'self': true
        },
        {
          'role': '租赁单列表·退回进度',
          'name': '租出记录（退回进度列）',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '库存查询·客户在租',
          'name': '四态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '2026-01-06',
          'text': '建档 · 启用',
          'who': '张伟'
        },
        {
          't': '当前',
          'text': '在租 1,020 只 · 无超期'
        }
      ]
    },
    'PLT-1210W': {
      'row': {"fields": {"name": "木托盘 1200×1000", "cls": "托盘", "spec": "1200×1000×144 mm", "src": "自有", "status": "启用", "date": "2026-02-11"}, "cells": ["木托盘 1200×1000", "<span class=\"tag tag-green\">托盘</span>", "1200×1000×144 mm", "块", "<span class=\"tag tag-green\">自有</span>", "<span class=\"td-num\">12.00</span>", "<span class=\"td-num\">12.00</span>", "<span class=\"tag tag-green\">启用</span>", "2026-02-11"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '产品详情',
      'info': [
        {
          'label': '产品编码',
          'text': 'PLT-1210W'
        },
        {
          'label': '名称',
          'text': '木托盘 1200×1000',
          'full': true
        },
        {
          'label': '分类',
          'text': '托盘'
        },
        {
          'label': '规格',
          'text': '1200×1000×144 mm',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '块'
        },
        {
          'label': '归属权',
          'text': '自有',
          'full': true
        },
        {
          'label': '日租金',
          'text': '12.00 元 / 块 / 日'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-02-11'
        }
      ],
      'feeSecTitle': '在租状态（库存四态口径）',
      'feeCols': ['在租', '待归还（超期）', '平均循环', '平均租期', '台账'],
      'fees': [
        {
          'cells': ['0 块', '0 块', '—', '—', '客户在租（已退回）'],
          'links': {
            4: '仓储作业/库存查询.html'
          }
        }
      ],
      'chain': [
        {
          'role': '产品档案（本档）',
          'name': 'PLT-1210W',
          'self': true
        },
        {
          'role': '其他出库',
          'name': '报废核销 22 块',
          'url': '仓储作业/其他出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '2026-02-11',
          'text': '建档 · 启用',
          'who': '张伟'
        },
        {
          't': '08-25',
          'text': '断裂批次报废 -22 块 · 全量退回后暂无在租',
          'who': '赵芳'
        }
      ]
    },
    'PLT-1210P': {
      'row': {"fields": {"name": "塑料托盘 1200×1000", "cls": "托盘", "spec": "1200×1000×150 mm", "src": "租入-路凯", "status": "启用", "date": "2026-02-11"}, "cells": ["塑料托盘 1200×1000", "<span class=\"tag tag-green\">托盘</span>", "1200×1000×150 mm", "块", "<span class=\"tag tag-orange\">租入-路凯</span>", "<span class=\"td-num\">18.00</span>", "<span class=\"td-num\">18.00</span>", "<span class=\"tag tag-green\">启用</span>", "2026-02-11"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '产品详情',
      'info': [
        {
          'label': '产品编码',
          'text': 'PLT-1210P'
        },
        {
          'label': '名称',
          'text': '塑料托盘 1200×1000',
          'full': true
        },
        {
          'label': '分类',
          'text': '托盘'
        },
        {
          'label': '规格',
          'text': '1200×1000×150 mm',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '块'
        },
        {
          'label': '归属权',
          'text': '租入-路凯（供应商资产 · 计租见租入单）',
          'full': true
        },
        {
          'label': '日租金',
          'text': '18.00 元 / 块 / 日'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-02-11'
        }
      ],
      'feeSecTitle': '在租状态（库存四态口径）',
      'feeCols': ['在租', '待归还（超期）', '平均循环', '平均租期', '台账'],
      'fees': [
        {
          'cells': ['1,860 块', '36 块', '26.4 次', '102 天', '客户在租'],
          'links': {
            4: '仓储作业/库存查询.html'
          }
        }
      ],
      'chain': [
        {
          'role': '产品档案（本档）',
          'name': 'PLT-1210P',
          'self': true
        },
        {
          'role': '租入单',
          'name': '路凯资产',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'role': '库存查询·客户在租',
          'name': '四态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '2026-02-11',
          'text': '建档 · 启用',
          'who': '张伟'
        },
        {
          't': '当前',
          'text': '在租 1,860 块 · 超期 36 块待催还'
        }
      ]
    },
    'BTC-6040S': {
      'row': {"fields": {"name": "料箱 600×400×220（带盖）", "cls": "料箱", "spec": "600×400×220 mm", "src": "自有", "status": "停用", "date": "2026-03-02"}, "cells": ["料箱 600×400×220（带盖）", "<span class=\"tag tag-orange\">料箱</span>", "600×400×220 mm", "只", "<span class=\"tag tag-green\">自有</span>", "<span class=\"td-num\">7.80</span>", "<span class=\"td-num\">7.80</span>", "<span class=\"tag tag-gray\">停用</span>", "2026-03-02"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '产品详情',
      'info': [
        {
          'label': '产品编码',
          'text': 'BTC-6040S'
        },
        {
          'label': '名称',
          'text': '料箱 600×400×220（带盖）',
          'full': true
        },
        {
          'label': '分类',
          'text': '料箱'
        },
        {
          'label': '规格',
          'text': '600×400×220 mm',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '只'
        },
        {
          'label': '归属权',
          'text': '否（停用 · 不可再出租）',
          'full': true
        },
        {
          'label': '日租金',
          'text': '7.80 元 / 只 / 日'
        },
        {
          'label': '状态',
          'tag': '停用'
        },
        {
          'label': '建档日期',
          'text': '2026-03-02'
        }
      ],
      'feeSecTitle': '在租状态（库存四态口径）',
      'feeCols': ['在租', '待归还（超期）', '平均循环', '平均租期', '台账'],
      'fees': [
        {
          'cells': ['0 只', '0 只', '—', '—', '客户在租（无在租）'],
          'links': {
            4: '仓储作业/库存查询.html'
          }
        }
      ],
      'chain': [
        {
          'role': '产品档案（本档）',
          'name': 'BTC-6040S · 停用',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '2026-03-02',
          'text': '建档',
          'who': '张伟'
        },
        {
          't': '2026-08-01',
          'text': '档案停用（供应商停产 · 停止新租）',
          'who': '张伟'
        }
      ]
    },
    'BTC-6040': {
      'row': {"fields": {"name": "料箱 600×400×340", "cls": "料箱", "spec": "600×400×340 mm", "src": "租入-路凯", "status": "启用", "date": "2026-03-02"}, "cells": ["料箱 600×400×340", "<span class=\"tag tag-orange\">料箱</span>", "600×400×340 mm", "只", "<span class=\"tag tag-orange\">租入-路凯</span>", "<span class=\"td-num\">8.50</span>", "<span class=\"td-num\">8.50</span>", "<span class=\"tag tag-green\">启用</span>", "2026-03-02"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '产品详情',
      'info': [
        {
          'label': '产品编码',
          'text': 'BTC-6040'
        },
        {
          'label': '名称',
          'text': '料箱 600×400×340',
          'full': true
        },
        {
          'label': '分类',
          'text': '料箱'
        },
        {
          'label': '规格',
          'text': '600×400×340 mm',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '只'
        },
        {
          'label': '归属权',
          'text': '租入-路凯（供应商资产 · 计租见租入单）',
          'full': true
        },
        {
          'label': '日租金',
          'text': '8.50 元 / 只 / 日'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-03-02'
        }
      ],
      'feeSecTitle': '在租状态（库存四态口径）',
      'feeCols': ['在租', '待归还（超期）', '平均循环', '平均租期', '台账'],
      'fees': [
        {
          'cells': ['2,480 只', '0 只', '31.8 次', '118 天', '客户在租'],
          'links': {
            4: '仓储作业/库存查询.html'
          }
        }
      ],
      'chain': [
        {
          'role': '产品档案（本档）',
          'name': 'BTC-6040',
          'self': true
        },
        {
          'role': '租入单',
          'name': '路凯资产',
          'url': '租赁管理/租入单列表.html'
        },
        {
          'role': '库存查询·客户在租',
          'name': '四态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '2026-03-02',
          'text': '建档 · 启用',
          'who': '张伟'
        },
        {
          't': '当前',
          'text': '在租 2,480 只 · 无超期'
        }
      ]
    },

    /* ===== 组件（原零部件档案并入 · N4 合并） ===== */
    'LJ-A100': {
      'row': {"fields": {"name": "锁扣组件", "cls": "组件", "spec": "不锈钢 304 · M8", "src": "自有", "status": "启用", "date": "2026-01-06", "supplier": "苏州联恒五金制品有限公司"}, "cells": ["锁扣组件", "<span class=\"tag tag-blue\">组件</span>", "不锈钢 304 · M8", "件", "<span class=\"tag tag-green\">自有</span>", "<span class=\"td-num\">6.80</span>", "—", "<span class=\"tag tag-green\">启用</span>", "2026-01-06"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
'title': '产品详情',
      'info': [
        {
          'label': '产品编码',
          'text': 'LJ-A100'
        },
        {
          'label': '名称',
          'text': '锁扣组件',
          'full': true
        },
        {
          'label': '分类',
          'text': '组件'
        },
        {
          'label': '规格',
          'text': '不锈钢 304 · M8',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '件'
        },
        {
          'label': '归属权',
          'text': '自有'
        },
        {
          'label': '参考单价',
          'text': '6.80 元'
        },
        {
          'label': '租金单价',
          'text': '—（采购件不计租金）'
        },
        {
          'label': '供应商（带出）',
          'text': '苏州联恒五金制品有限公司',
          'full': true
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-01-06'
        }
      ],
      'feeSecTitle': '库存与用途',
      'feeCols': ['在库', '在途', '客户端', '用途'],
      'fees': [
        {
          'cells': ['5,260 件（原料区 RA）', '1,200 件', '800 件', 'BOM 子件 · ZH-2601-A（V2.1 配比 4 只/套）']
        }
      ],
      'chain': [
        {
          'role': '供应商',
          'name': '苏州联恒'
        },
        {
          'role': '产品档案（本档）',
          'name': 'LJ-A100 锁扣组件',
          'self': true
        },
        {
          'role': '采购入库',
          'name': 'CGRK-20260828-012 · +2,400',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '组装',
          'name': 'ZH-2601-A 配方子件',
        }
      ],
      'timeline': [
        {
          't': '2026-01',
          'text': '建档 · 启用',
          'who': '系统'
        },
        {
          't': '08-28',
          'text': '最近入库 · CGRK-20260828-012（+2,400 件）',
          'who': '张伟'
        },
        {
          't': '09-01',
          'text': '调拨备料 · DB-20260901-003（-1,000 件 → 成品区 RB）',
          'who': '赵芳'
        }
      ]
    },
    'LJ-B200': {
      'row': {"fields": {"name": "铰链", "cls": "组件", "spec": "锌合金 · 65mm", "src": "自有", "status": "启用", "date": "2026-01-06", "supplier": "苏州联恒五金制品有限公司"}, "cells": ["铰链", "<span class=\"tag tag-blue\">组件</span>", "锌合金 · 65mm", "件", "<span class=\"tag tag-green\">自有</span>", "<span class=\"td-num\">4.20</span>", "—", "<span class=\"tag tag-green\">启用</span>", "2026-01-06"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
'title': '产品详情',
      'info': [
        {
          'label': '产品编码',
          'text': 'LJ-B200'
        },
        {
          'label': '名称',
          'text': '铰链',
          'full': true
        },
        {
          'label': '分类',
          'text': '组件'
        },
        {
          'label': '规格',
          'text': '锌合金 · 65mm',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '件'
        },
        {
          'label': '归属权',
          'text': '自有'
        },
        {
          'label': '参考单价',
          'text': '4.20 元'
        },
        {
          'label': '租金单价',
          'text': '—（采购件不计租金）'
        },
        {
          'label': '供应商（带出）',
          'text': '苏州联恒五金制品有限公司',
          'full': true
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-01-06'
        }
      ],
      'feeSecTitle': '库存与用途',
      'feeCols': ['在库', '在途', '客户端', '用途'],
      'fees': [
        {
          'cells': ['2,640 件（原料区 RA）', '400 件', '1,600 件', '采购件 · B1 直接销售（销售订单行）+ 组装辅材']
        }
      ],
      'chain': [
        {
          'role': '供应商',
          'name': '苏州联恒'
        },
        {
          'role': '产品档案（本档）',
          'name': 'LJ-B200 铰链',
          'self': true
        },
        {
          'role': '采购入库',
          'name': 'CGRK-20260828-012 · +2,000',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '销售出库',
          'name': 'B1 线随单出库',
          'url': '销售管理/销售出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '2026-01',
          'text': '建档 · 启用',
          'who': '系统'
        },
        {
          't': '09-01',
          'text': '盘盈补录 +120 · QTRK-20260901-003',
          'who': '赵芳'
        }
      ]
    },
    'LJ-C300': {
      'row': {"fields": {"name": "围板", "cls": "组件", "spec": "HDPE 波纹板 · 970 高", "src": "自有", "status": "启用", "date": "2026-02-02", "supplier": "宁波华塑包装制品有限公司"}, "cells": ["围板", "<span class=\"tag tag-blue\">组件</span>", "HDPE 波纹板 · 970 高", "件", "<span class=\"tag tag-green\">自有</span>", "<span class=\"td-num\">52.00</span>", "—", "<span class=\"tag tag-green\">启用</span>", "2026-02-02"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
'title': '产品详情',
      'info': [
        {
          'label': '产品编码',
          'text': 'LJ-C300'
        },
        {
          'label': '名称',
          'text': '围板',
          'full': true
        },
        {
          'label': '分类',
          'text': '组件'
        },
        {
          'label': '规格',
          'text': 'HDPE 波纹板 · 970 高',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '件'
        },
        {
          'label': '归属权',
          'text': '自有'
        },
        {
          'label': '参考单价',
          'text': '52.00 元'
        },
        {
          'label': '租金单价',
          'text': '—（采购件不计租金）'
        },
        {
          'label': '供应商（带出）',
          'text': '宁波华塑包装制品有限公司',
          'full': true
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-02-02'
        }
      ],
      'feeSecTitle': '库存与用途',
      'feeCols': ['在库', '在途', '客户端', '用途'],
      'fees': [
        {
          'cells': ['1,860 件（原料区 RA）', '0 件', '1,600 件', 'BOM 子件 · ZH-2601-A（V2.1 配比 4 件/套）']
        }
      ],
      'chain': [
        {
          'role': '供应商',
          'name': '宁波华塑'
        },
        {
          'role': '产品档案（本档）',
          'name': 'LJ-C300 围板',
          'self': true
        },
        {
          'role': '拆卸产出',
          'name': 'CX 系列 · BOM 反拆回库',
        },
        {
          'role': '组装',
          'name': 'ZH-2601-A 配方子件',
        }
      ],
      'timeline': [
        {
          't': '2026-01',
          'text': '建档',
          'who': '系统'
        },
        {
          't': '09-02',
          'text': '拆卸产出 +100 · CX-20260902-006',
          'who': '张伟'
        }
      ]
    },
    'LJ-D400': {
      'row': {"fields": {"name": "箱盖", "cls": "组件", "spec": "ABS 吸塑 · 1200×1000", "src": "自有", "status": "启用", "date": "2026-02-02", "supplier": "宁波华塑包装制品有限公司"}, "cells": ["箱盖", "<span class=\"tag tag-blue\">组件</span>", "ABS 吸塑 · 1200×1000", "件", "<span class=\"tag tag-green\">自有</span>", "<span class=\"td-num\">36.00</span>", "—", "<span class=\"tag tag-green\">启用</span>", "2026-02-02"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
'title': '产品详情',
      'info': [
        {
          'label': '产品编码',
          'text': 'LJ-D400'
        },
        {
          'label': '名称',
          'text': '箱盖',
          'full': true
        },
        {
          'label': '分类',
          'text': '组件'
        },
        {
          'label': '规格',
          'text': 'ABS 吸塑 · 1200×1000',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '件'
        },
        {
          'label': '归属权',
          'text': '自有'
        },
        {
          'label': '参考单价',
          'text': '36.00 元'
        },
        {
          'label': '租金单价',
          'text': '—（采购件不计租金）'
        },
        {
          'label': '供应商（带出）',
          'text': '宁波华塑包装制品有限公司',
          'full': true
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-02-02'
        }
      ],
      'feeSecTitle': '库存与用途',
      'feeCols': ['在库', '在途', '客户端', '用途'],
      'fees': [
        {
          'cells': ['980 件（原料区 RA）', '480 件', '400 件', 'BOM 子件 · ZH-2601-A（配比 1 件/套）+ B1 直接销售']
        }
      ],
      'chain': [
        {
          'role': '供应商',
          'name': '宁波华塑'
        },
        {
          'role': '产品档案（本档）',
          'name': 'LJ-D400 箱盖',
          'self': true
        },
        {
          'role': '销售出库',
          'name': 'XSCK-20260902-015 · -1,500',
          'url': '销售管理/销售出库列表.html'
        },
        {
          'role': '组装',
          'name': 'ZH-2601-A 配方子件',
        }
      ],
      'timeline': [
        {
          't': '2026-01',
          'text': '建档 · 启用',
          'who': '系统'
        },
        {
          't': '09-02',
          'text': '销售出库 -1,500 · XSCK-20260902-015（在库 980 + 在途补充）',
          'who': '张伟'
        }
      ]
    },
    'LJ-E500': {
      'row': {"fields": {"name": "底托架", "cls": "组件", "spec": "钢制喷塑 · 1200×1000", "src": "自有", "status": "启用", "date": "2026-03-06", "supplier": "常州正大塑料托盘厂"}, "cells": ["底托架", "<span class=\"tag tag-blue\">组件</span>", "钢制喷塑 · 1200×1000", "件", "<span class=\"tag tag-green\">自有</span>", "<span class=\"td-num\">78.00</span>", "—", "<span class=\"tag tag-green\">启用</span>", "2026-03-06"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
'title': '产品详情',
      'info': [
        {
          'label': '产品编码',
          'text': 'LJ-E500'
        },
        {
          'label': '名称',
          'text': '底托架',
          'full': true
        },
        {
          'label': '分类',
          'text': '组件'
        },
        {
          'label': '规格',
          'text': '钢制喷塑 · 1200×1000',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '件'
        },
        {
          'label': '归属权',
          'text': '自有'
        },
        {
          'label': '参考单价',
          'text': '78.00 元'
        },
        {
          'label': '租金单价',
          'text': '—（采购件不计租金）'
        },
        {
          'label': '供应商（带出）',
          'text': '常州正大塑料托盘厂',
          'full': true
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-03-06'
        }
      ],
      'feeSecTitle': '库存与用途',
      'feeCols': ['在库', '在途', '客户端', '用途'],
      'fees': [
        {
          'cells': ['0 件（暂无入库）', '0 件', '0 件', '项目备选件 · PRJ-2603 护角套件升级方案（未启用）']
        }
      ],
      'chain': [
        {
          'role': '供应商',
          'name': '常州正大'
        },
        {
          'role': '产品档案（本档）',
          'name': 'LJ-E500 底托架',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '2026-03',
          'text': '建档（备选）',
          'who': '系统'
        },
        {
          't': '—',
          'text': '未启用 · 无库存流水',
          'off': true
        }
      ]
    },
    'LJ-F600': {
      'row': {"fields": {"name": "内衬", "cls": "组件", "spec": "EPE 珍珠棉 · 定制", "src": "自有", "status": "启用", "date": "2026-03-06", "supplier": "宁波华塑包装制品有限公司"}, "cells": ["内衬", "<span class=\"tag tag-blue\">组件</span>", "EPE 珍珠棉 · 定制", "件", "<span class=\"tag tag-green\">自有</span>", "<span class=\"td-num\">15.50</span>", "—", "<span class=\"tag tag-green\">启用</span>", "2026-03-06"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
'title': '产品详情',
      'info': [
        {
          'label': '产品编码',
          'text': 'LJ-F600'
        },
        {
          'label': '名称',
          'text': '内衬',
          'full': true
        },
        {
          'label': '分类',
          'text': '组件'
        },
        {
          'label': '规格',
          'text': 'EPE 珍珠棉 · 定制',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '件'
        },
        {
          'label': '归属权',
          'text': '自有'
        },
        {
          'label': '参考单价',
          'text': '15.50 元'
        },
        {
          'label': '租金单价',
          'text': '—（采购件不计租金）'
        },
        {
          'label': '供应商（带出）',
          'text': '宁波华塑包装制品有限公司',
          'full': true
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-03-06'
        }
      ],
      'feeSecTitle': '库存与用途',
      'feeCols': ['在库', '在途', '客户端', '用途'],
      'fees': [
        {
          'cells': ['1,520 件（原料区 RA）', '120 件', '0 件', 'BOM 可选配（V2.0 起）+ B1 直接销售']
        }
      ],
      'chain': [
        {
          'role': '供应商',
          'name': '宁波华塑'
        },
        {
          'role': '产品档案（本档）',
          'name': 'LJ-F600 内衬',
          'self': true
        },
        {
          'role': '采购入库',
          'name': 'CGRK-20260824-005 · +3,000',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '销售出库',
          'name': 'B1 线随单出库',
          'url': '销售管理/销售出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '2026-01',
          'text': '建档 · 启用',
          'who': '系统'
        },
        {
          't': '08-24',
          'text': '最近入库 · CGRK-20260824-005（+3,000 件）',
          'who': '李国栋'
        }
      ]
    }
  },  /* -------------------------------------------------------------------------- */
  /* 库位档案 locations：键 = 库位编码（基础数据/库位档案.html 10 行全量） */
  /* 存放物料按库区真实分布 */
  locations: {
     'XNC-AJZX': {
      'row': {"fields": {"wh": "华东中心仓（WH-01）", "area": "客户虚拟仓", "ltype": "虚拟仓", "spec": "按客户归集", "usage": "on-hire 640 只", "status": "启用"}, "cells": ["客户虚拟仓（安吉智行）", "<span class=\"lk\">XNC-AJZX</span>", "虚拟仓", "按客户归集", "on-hire 640 只", "<span class=\"tag tag-blue\">启用</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}]},
      'title': '库位详情',
      'info': [
        {
          'label': '仓库',
          'text': '华东中心仓（WH-01）· 虚拟',
          'full': true
        },
        {
          'label': '库区',
          'text': '客户虚拟仓'
        },
        {
          'label': '库位编码',
          'text': 'XNC-AJZX'
        },
        {
          'label': '库位类型',
          'text': '虚拟仓'
        },
        {
          'label': '归集口径',
          'text': '在客户处的租赁资产按客户归集（on-hire）；客户转租为其子状态',
          'full': true
        },
        {
          'label': '容量占用',
          'text': 'on-hire 640 只（围板箱）'
        },
        {
          'label': '状态',
          'tag': '启用'
        }
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260823-033',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '组合出库',
          'name': 'CK-20260824-009',
          'url': '租赁管理/组合出库列表.html'
        },
        {
          'role': '客户虚拟仓（本仓）',
          'name': 'XNC-AJZX · 安吉智行',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '09-02',
          'text': '组合出库 640 只至安吉智行 · 记客户虚拟仓（on-hire）',
          'who': '张伟'
        },
        {
          't': '当前',
          'text': '虚拟仓在库 640 只 · 支撑按客户对账/盘点核对'
        }
      ]
    },
   'RA-A-01-01': {
      'row': {"fields": {"wh": "华东中心仓（WH-01）", "area": "原料区 RA", "ltype": "存储位", "spec": "1.2m×1.0m / 2t", "usage": "68%", "status": "启用"}, "cells": ["原料区 RA", "<span class=\"lk\">RA-A-01-01</span>", "存储位", "1.2m×1.0m / 2t", "68%", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '库位详情',
      'info': [
        {
          'label': '仓库',
          'text': '华东中心仓（WH-01）',
          'full': true
        },
        {
          'label': '库区',
          'text': '原料区 RA'
        },
        {
          'label': '库位编码',
          'text': 'RA-A-01-01'
        },
        {
          'label': '库位类型',
          'text': '存储位'
        },
        {
          'label': '规格 / 承重',
          'text': '1.2m×1.0m / 2t'
        },
        {
          'label': '容量占用',
          'text': '68%'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '库存容量',
          'text': '以库存四态口径管理',
          'full': true
        }
      ],
      'feeSecTitle': '存放物料',
      'feeCols': ['物料', '类别', '在库', '库区'],
      'fees': [
        {
          'cells': ['LJ-A100 锁扣组件 不锈钢 304', '零部件', '5,260 件', '原料区 RA']
        },
        {
          'cells': ['LJ-B200 铰链 锌合金 65mm', '零部件', '2,640 件', '原料区 RA']
        }
      ],
      'chain': [
        {
          'role': '库区',
          'name': '原料区 RA'
        },
        {
          'role': '库位（本档）',
          'name': 'RA-A-01-01 · 68%',
          'self': true
        },
        {
          'role': '存放物料',
          'name': 'LJ-A100 / LJ-B200',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '建档',
          'text': '库位启用 · 存储位',
          'who': '系统'
        },
        {
          't': '08-28',
          'text': '最近入库 · CGRK-20260828-012（LJ-A100 +2,400）',
          'who': '张伟'
        },
        {
          't': '当前',
          'text': '容量占用 68% · 正常'
        }
      ]
    },
    'RA-A-01-02': {
      'row': {"fields": {"wh": "华东中心仓（WH-01）", "area": "原料区 RA", "ltype": "存储位", "spec": "1.2m×1.0m / 2t", "usage": "45%", "status": "启用"}, "cells": ["原料区 RA", "<span class=\"lk\">RA-A-01-02</span>", "存储位", "1.2m×1.0m / 2t", "45%", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '库位详情',
      'info': [
        {
          'label': '仓库',
          'text': '华东中心仓（WH-01）',
          'full': true
        },
        {
          'label': '库区',
          'text': '原料区 RA'
        },
        {
          'label': '库位编码',
          'text': 'RA-A-01-02'
        },
        {
          'label': '库位类型',
          'text': '存储位'
        },
        {
          'label': '规格 / 承重',
          'text': '1.2m×1.0m / 2t'
        },
        {
          'label': '容量占用',
          'text': '45%'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '库存容量',
          'text': '以库存四态口径管理',
          'full': true
        }
      ],
      'feeSecTitle': '存放物料',
      'feeCols': ['物料', '类别', '在库', '库区'],
      'fees': [
        {
          'cells': ['LJ-A100 锁扣组件 不锈钢 304', '零部件', '2,400 件（批次 B20260828-01）', '原料区 RA']
        }
      ],
      'chain': [
        {
          'role': '库区',
          'name': '原料区 RA'
        },
        {
          'role': '库位（本档）',
          'name': 'RA-A-01-02 · 45%',
          'self': true
        },
        {
          'role': '存放物料',
          'name': 'LJ-A100 · 批次位',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '建档',
          'text': '库位启用 · 存储位',
          'who': '系统'
        },
        {
          't': '08-28',
          'text': '批次入库 · B20260828-01（LJ-A100 2,400 件）',
          'who': '张伟'
        }
      ]
    },
    'RA-B-02-01': {
      'row': {"fields": {"wh": "华东中心仓（WH-01）", "area": "原料区 RA", "ltype": "存储位", "spec": "1.2m×1.0m / 2t", "usage": "0%", "status": "启用"}, "cells": ["原料区 RA", "<span class=\"lk\">RA-B-02-01</span>", "存储位", "1.2m×1.0m / 2t", "0%", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '库位详情',
      'info': [
        {
          'label': '仓库',
          'text': '华东中心仓（WH-01）',
          'full': true
        },
        {
          'label': '库区',
          'text': '原料区 RA'
        },
        {
          'label': '库位编码',
          'text': 'RA-B-02-01'
        },
        {
          'label': '库位类型',
          'text': '存储位'
        },
        {
          'label': '规格 / 承重',
          'text': '1.2m×1.0m / 2t'
        },
        {
          'label': '容量占用',
          'text': '0%'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '库存容量',
          'text': '以库存四态口径管理',
          'full': true
        }
      ],
      'feeSecTitle': '存放物料',
      'feeCols': ['物料', '类别', '在库', '库区'],
      'fees': [
        {
          'cells': ['—', '—', '0（空置）', '原料区 RA']
        }
      ],
      'chain': [
        {
          'role': '库区',
          'name': '原料区 RA'
        },
        {
          'role': '库位（本档）',
          'name': 'RA-B-02-01 · 空置',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '建档',
          'text': '库位启用 · 存储位',
          'who': '系统'
        },
        {
          't': '当前',
          'text': '空置 · 待分配'
        }
      ]
    },
    'RB-A-01-01': {
      'row': {"fields": {"wh": "华东中心仓（WH-01）", "area": "成品区 RB", "ltype": "存储位", "spec": "1.2m×1.0m / 2t", "usage": "82%", "status": "启用"}, "cells": ["成品区 RB", "<span class=\"lk\">RB-A-01-01</span>", "存储位", "1.2m×1.0m / 2t", "82%", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '库位详情',
      'info': [
        {
          'label': '仓库',
          'text': '华东中心仓（WH-01）',
          'full': true
        },
        {
          'label': '库区',
          'text': '成品区 RB'
        },
        {
          'label': '库位编码',
          'text': 'RB-A-01-01'
        },
        {
          'label': '库位类型',
          'text': '存储位'
        },
        {
          'label': '规格 / 承重',
          'text': '1.2m×1.0m / 2t'
        },
        {
          'label': '容量占用',
          'text': '82%'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '库存容量',
          'text': '以库存四态口径管理',
          'full': true
        }
      ],
      'feeSecTitle': '存放物料',
      'feeCols': ['物料', '类别', '在库', '库区'],
      'fees': [
        {
          'cells': ['ZH-2601-A 驾驶室围板箱整箱套件', '组合件', '640 套', '成品区 RB']
        }
      ],
      'chain': [
        {
          'role': '库区',
          'name': '成品区 RB'
        },
        {
          'role': '库位（本档）',
          'name': 'RB-A-01-01 · 82%',
          'self': true
        },
        {
          'role': '存放物料',
          'name': 'ZH-2601-A 组合件',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '建档',
          'text': '库位启用 · 存储位',
          'who': '系统'
        },
        {
          't': '09-04',
          'text': '组装入库 · ZZ-20260904-007（+32 套）',
          'who': '刘志强'
        },
        {
          't': '当前',
          'text': '容量占用 82% · 接近满容'
        }
      ]
    },
    'RB-A-01-02': {
      'row': {"fields": {"wh": "华东中心仓（WH-01）", "area": "成品区 RB", "ltype": "存储位", "spec": "1.2m×1.0m / 2t", "usage": "74%", "status": "启用"}, "cells": ["成品区 RB", "<span class=\"lk\">RB-A-01-02</span>", "存储位", "1.2m×1.0m / 2t", "74%", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '库位详情',
      'info': [
        {
          'label': '仓库',
          'text': '华东中心仓（WH-01）',
          'full': true
        },
        {
          'label': '库区',
          'text': '成品区 RB'
        },
        {
          'label': '库位编码',
          'text': 'RB-A-01-02'
        },
        {
          'label': '库位类型',
          'text': '存储位'
        },
        {
          'label': '规格 / 承重',
          'text': '1.2m×1.0m / 2t'
        },
        {
          'label': '容量占用',
          'text': '74%'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '库存容量',
          'text': '以库存四态口径管理',
          'full': true
        }
      ],
      'feeSecTitle': '存放物料',
      'feeCols': ['物料', '类别', '在库', '库区'],
      'fees': [
        {
          'cells': ['LJ-A100 锁扣组件 不锈钢 304', '零部件', '1,000 件（调拨备料）', '成品区 RB']
        }
      ],
      'chain': [
        {
          'role': '库区',
          'name': '成品区 RB'
        },
        {
          'role': '库位（本档）',
          'name': 'RB-A-01-02 · 74%',
          'self': true
        },
        {
          'role': '存放物料',
          'name': 'LJ-A100 · 组装线备料',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '建档',
          'text': '库位启用 · 存储位',
          'who': '系统'
        },
        {
          't': '09-01',
          'text': '调拨入库 · DB-20260901-003（LJ-A100 +1,000 待审核）',
          'who': '赵芳'
        }
      ]
    },
    'RB-B-01-01': {
      'row': {"fields": {"wh": "华东中心仓（WH-01）", "area": "成品区 RB", "ltype": "拣选位", "spec": "1.2m×1.0m / 1.5t", "usage": "60%", "status": "启用"}, "cells": ["成品区 RB", "<span class=\"lk\">RB-B-01-01</span>", "拣选位", "1.2m×1.0m / 1.5t", "60%", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '库位详情',
      'info': [
        {
          'label': '仓库',
          'text': '华东中心仓（WH-01）',
          'full': true
        },
        {
          'label': '库区',
          'text': '成品区 RB'
        },
        {
          'label': '库位编码',
          'text': 'RB-B-01-01'
        },
        {
          'label': '库位类型',
          'text': '拣选位'
        },
        {
          'label': '规格 / 承重',
          'text': '1.2m×1.0m / 1.5t'
        },
        {
          'label': '容量占用',
          'text': '60%'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '库存容量',
          'text': '以库存四态口径管理',
          'full': true
        }
      ],
      'feeSecTitle': '存放物料',
      'feeCols': ['物料', '类别', '在库', '库区'],
      'fees': [
        {
          'cells': ['WBX-1210L 围板箱 1200×1000×970', '租赁器具', '2,120 只', '成品区 RB']
        }
      ],
      'chain': [
        {
          'role': '库区',
          'name': '成品区 RB'
        },
        {
          'role': '库位（本档）',
          'name': 'RB-B-01-01 · 拣选位',
          'self': true
        },
        {
          'role': '存放物料',
          'name': 'WBX-1210L',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '建档',
          'text': '库位启用 · 拣选位',
          'who': '系统'
        },
        {
          't': '当前',
          'text': '拣选备货 · 容量 60%'
        }
      ]
    },
    'RD-01': {
      'row': {"fields": {"wh": "华东中心仓（WH-01）", "area": "组装区 RD", "ltype": "组装暂存", "spec": "工位 1", "usage": "组装中", "status": "启用"}, "cells": ["组装区 RD", "<span class=\"lk\">RD-01</span>", "组装暂存", "工位 1", "组装中", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '库位详情',
      'info': [
        {
          'label': '仓库',
          'text': '华东中心仓（WH-01）',
          'full': true
        },
        {
          'label': '库区',
          'text': '组装区 RD'
        },
        {
          'label': '库位编码',
          'text': 'RD-01'
        },
        {
          'label': '库位类型',
          'text': '组装暂存'
        },
        {
          'label': '规格 / 承重',
          'text': '工位 1'
        },
        {
          'label': '容量占用',
          'text': '组装中'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '库存容量',
          'text': '以库存四态口径管理',
          'full': true
        }
      ],
      'feeSecTitle': '存放物料',
      'feeCols': ['物料', '类别', '在库', '库区'],
      'fees': [
        {
          'cells': ['ZH-2601-A 驾驶室围板箱整箱套件', '组合件', '32 套（组装中 32/50）', '组装区 RD']
        }
      ],
      'chain': [
        {
          'role': '库区',
          'name': '组装区 RD'
        },
        {
          'role': '库位（本档）',
          'name': 'RD-01 · 工位 1 组装中',
          'self': true
        },
        {
          'role': '组装单',
          'name': 'ZZ-20260904-007 · 拆散件再组装',
        }
      ],
      'timeline': [
        {
          't': '09-04',
          'text': '开工 · ZZ-20260904-007（承接 CX-20260902-006 散件）',
          'who': '刘志强'
        },
        {
          't': '当前',
          'text': '组装中 · 进度 32/50'
        }
      ]
    },
    'RD-02': {
      'row': {"fields": {"wh": "华东中心仓（WH-01）", "area": "组装区 RD", "ltype": "组装暂存", "spec": "工位 2", "usage": "空闲", "status": "启用"}, "cells": ["组装区 RD", "<span class=\"lk\">RD-02</span>", "组装暂存", "工位 2", "空闲", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '库位详情',
      'info': [
        {
          'label': '仓库',
          'text': '华东中心仓（WH-01）',
          'full': true
        },
        {
          'label': '库区',
          'text': '组装区 RD'
        },
        {
          'label': '库位编码',
          'text': 'RD-02'
        },
        {
          'label': '库位类型',
          'text': '组装暂存'
        },
        {
          'label': '规格 / 承重',
          'text': '工位 2'
        },
        {
          'label': '容量占用',
          'text': '空闲'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '库存容量',
          'text': '以库存四态口径管理',
          'full': true
        }
      ],
      'feeSecTitle': '存放物料',
      'feeCols': ['物料', '类别', '在库', '库区'],
      'fees': [
        {
          'cells': ['—', '—', '0（空闲）', '组装区 RD']
        }
      ],
      'chain': [
        {
          'role': '库区',
          'name': '组装区 RD'
        },
        {
          'role': '库位（本档）',
          'name': 'RD-02 · 工位 2 空闲',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '建档',
          'text': '库位启用 · 组装暂存',
          'who': '系统'
        },
        {
          't': '当前',
          'text': '空闲 · 待排产'
        }
      ]
    },
    'RC-01': {
      'row': {"fields": {"wh": "华东中心仓（WH-01）", "area": "退货区 RC", "ltype": "退货暂存", "spec": "1.2m×1.0m / 2t", "usage": "36%", "status": "启用"}, "cells": ["退货区 RC", "<span class=\"lk\">RC-01</span>", "退货暂存", "1.2m×1.0m / 2t", "36%", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '库位详情',
      'info': [
        {
          'label': '仓库',
          'text': '华东中心仓（WH-01）',
          'full': true
        },
        {
          'label': '库区',
          'text': '退货区 RC'
        },
        {
          'label': '库位编码',
          'text': 'RC-01'
        },
        {
          'label': '库位类型',
          'text': '退货暂存'
        },
        {
          'label': '规格 / 承重',
          'text': '1.2m×1.0m / 2t'
        },
        {
          'label': '容量占用',
          'text': '36%'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '库存容量',
          'text': '以库存四态口径管理',
          'full': true
        }
      ],
      'feeSecTitle': '存放物料',
      'feeCols': ['物料', '类别', '在库', '库区'],
      'fees': [
        {
          'cells': ['LJ-D400 箱盖 ABS 吸塑', '零部件', '300 件（退货待检）', '退货区 RC']
        }
      ],
      'chain': [
        {
          'role': '库区',
          'name': '退货区 RC'
        },
        {
          'role': '库位（本档）',
          'name': 'RC-01 · 退货暂存',
          'self': true
        },
        {
          'role': '其他入库',
          'name': 'QTRK-20260828-002 · 退货入库',
          'url': '仓储作业/其他入库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-28',
          'text': '退货到货 · 箱盖 300 件待检',
          'who': '张伟'
        },
        {
          't': '当前',
          'text': '容量占用 36%'
        }
      ]
    },
    'RC-02': {
      'row': {"fields": {"wh": "华东中心仓（WH-01）", "area": "退货区 RC", "ltype": "退货暂存", "spec": "1.2m×1.0m / 2t", "usage": "0%", "status": "停用"}, "cells": ["退货区 RC", "<span class=\"lk\">RC-02</span>", "退货暂存", "1.2m×1.0m / 2t", "0%", "<span class=\"tag tag-gray\">停用</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal('createModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '库位详情',
      'info': [
        {
          'label': '仓库',
          'text': '华东中心仓（WH-01）',
          'full': true
        },
        {
          'label': '库区',
          'text': '退货区 RC'
        },
        {
          'label': '库位编码',
          'text': 'RC-02'
        },
        {
          'label': '库位类型',
          'text': '退货暂存'
        },
        {
          'label': '规格 / 承重',
          'text': '1.2m×1.0m / 2t'
        },
        {
          'label': '容量占用',
          'text': '0%'
        },
        {
          'label': '状态',
          'tag': '停用'
        },
        {
          'label': '库存容量',
          'text': '以库存四态口径管理',
          'full': true
        }
      ],
      'feeSecTitle': '存放物料',
      'feeCols': ['物料', '类别', '在库', '库区'],
      'fees': [
        {
          'cells': ['—', '—', '0（停用）', '退货区 RC']
        }
      ],
      'chain': [
        {
          'role': '库区',
          'name': '退货区 RC'
        },
        {
          'role': '库位（本档）',
          'name': 'RC-02 · 停用',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '建档',
          'text': '库位启用',
          'who': '系统'
        },
        {
          't': '2026-07',
          'text': '库位停用（区域改造）',
          'who': '张伟'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* BOM 版本 bomVersions：键 = 版本号（基础数据/BOM维护.html 3 行全量） */
  /* 弹窗 bomViewModal · 触发锚「查看」；V2.1/V2.0/V1.0 配方演进 */
  bomVersions: {
    'V2.1': {
      'row': {"fields": {}, "keyHtml": "<span class=\"ver-tag\">V2.1<span class=\"tag tag-green\">已生效</span></span>", "cells": ["2026-08-20", "<span class=\"tag-green\">自购</span>", "陈金", "锁扣配比 6→4，按客户产线上线反馈调整"], "ops": [{"t": "查看", "detail": true}, {"t": "复制为新版本"}]},
      'title': 'BOM 版本查看',
      'titleNo': 'ZH-2601-A V2.1',
      'info': [
        {
          'label': '父项编码',
          'text': 'ZH-2601-A'
        },
        {
          'label': '父项名称',
          'text': '驾驶室围板箱整箱套件'
        },
        {
          'label': '版本',
          'text': 'V2.1'
        },
        {
          'label': '生效日期',
          'text': '2026-08-20'
        },
        {
          'label': '配方来源',
          'text': '自购'
        },
        {
          'label': '更新人',
          'text': '陈金'
        },
        {
          'label': '变更说明',
          'text': '锁扣配比 6→4，按客户产线上线反馈调整',
          'full': true
        }
      ],
      'feeSecTitle': '配方行（V2.1）',
      'feeCols': ['子项编码', '子项名称', '来源', '类型', '单位用量', '供应商（带出）'],
      'fees': [
        {
          'cells': ['WBX-1210L', '围板箱 1200×1000×970', '自购', '器具', '1', '宁波华塑包装制品有限公司']
        },
        {
          'cells': ['LJ-C300', '围板 HDPE 波纹板', '自购', '零件', '4', '宁波华塑包装制品有限公司']
        },
        {
          'cells': ['LJ-D400', '箱盖 ABS 吸塑', '自购', '器具', '1', '宁波华塑包装制品有限公司']
        },
        {
          'cells': ['LJ-A100', '锁扣组件 不锈钢', '自购', '零件', '4', '苏州联恒五金制品有限公司']
        }
      ],
      'chain': [
        {
          'role': 'BOM 版本（本版本）',
          'name': 'ZH-2601-A V2.1 · 生效中',
          'self': true
        },
        {
          'role': '组装',
          'name': 'ZZ 系列按 V2.1 投料',
        },
        {
          'role': '库存查询',
          'name': 'ZH-2601-A 组合件',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '2026-01-10',
          'text': 'V1.0 初版发布',
          'who': '王强'
        },
        {
          't': '2026-05-14',
          'text': 'V2.0 停用 · 新增内衬可选配、围板 5→4',
          'who': '陈金'
        },
        {
          't': '2026-08-20',
          'text': 'V2.1 生效 · 锁扣配比 6→4',
          'who': '陈金'
        }
      ]
    },
    'V2.0': {
      'row': {"fields": {}, "keyHtml": "<span class=\"ver-tag\">V2.0<span class=\"tag tag-gray\">停用</span></span>", "cells": ["2026-05-14", "<span class=\"tag-green\">自购</span>", "陈金", "新增内衬可选配；围板由 5 块改 4 块"], "ops": [{"t": "查看", "detail": true}, {"t": "复制为新版本"}]},
      'title': 'BOM 版本查看',
      'titleNo': 'ZH-2601-A V2.0',
      'info': [
        {
          'label': '父项编码',
          'text': 'ZH-2601-A'
        },
        {
          'label': '父项名称',
          'text': '驾驶室围板箱整箱套件'
        },
        {
          'label': '版本',
          'text': 'V2.0'
        },
        {
          'label': '生效日期',
          'text': '2026-05-14'
        },
        {
          'label': '配方来源',
          'text': '自购'
        },
        {
          'label': '更新人',
          'text': '陈金'
        },
        {
          'label': '变更说明',
          'text': '新增内衬可选配；围板由 5 块改 4 块',
          'full': true
        }
      ],
      'feeSecTitle': '配方行（V2.0）',
      'feeCols': ['子项编码', '子项名称', '来源', '类型', '单位用量', '供应商（带出）'],
      'fees': [
        {
          'cells': ['WBX-1210L', '围板箱 1200×1000×970', '自购', '器具', '1', '宁波华塑包装制品有限公司']
        },
        {
          'cells': ['LJ-C300', '围板 HDPE 波纹板', '自购', '零件', '4', '宁波华塑包装制品有限公司']
        },
        {
          'cells': ['LJ-D400', '箱盖 ABS 吸塑', '自购', '器具', '1', '宁波华塑包装制品有限公司']
        },
        {
          'cells': ['LJ-A100', '锁扣组件 不锈钢', '自购', '零件', '6', '苏州联恒五金制品有限公司']
        },
        {
          'cells': ['LJ-F600', '内衬 EPE 珍珠棉', '自购', '零件', '可选配 0-1', '宁波华塑包装制品有限公司']
        }
      ],
      'chain': [
        {
          'role': 'BOM 版本（本版本）',
          'name': 'ZH-2601-A V2.0 · 已停用',
          'self': true
        },
        {
          'role': '组装',
          'name': '历史组装按 V2.0 投料',
        }
      ],
      'timeline': [
        {
          't': '2026-05-14',
          'text': 'V2.0 生效 · 围板 5→4、新增内衬可选配',
          'who': '陈金'
        },
        {
          't': '2026-08-20',
          'text': 'V2.0 停用 · 由 V2.1 接替',
          'who': '陈金'
        }
      ]
    },
    'V1.0': {
      'row': {"fields": {}, "keyHtml": "<span class=\"ver-tag\">V1.0<span class=\"tag tag-gray\">停用</span></span>", "cells": ["2026-01-10", "<span class=\"tag-green\">自购</span>", "王强", "初版"], "ops": [{"t": "查看", "detail": true}, {"t": "复制为新版本"}]},
      'title': 'BOM 版本查看',
      'titleNo': 'ZH-2601-A V1.0',
      'info': [
        {
          'label': '父项编码',
          'text': 'ZH-2601-A'
        },
        {
          'label': '父项名称',
          'text': '驾驶室围板箱整箱套件'
        },
        {
          'label': '版本',
          'text': 'V1.0'
        },
        {
          'label': '生效日期',
          'text': '2026-01-10'
        },
        {
          'label': '配方来源',
          'text': '自购'
        },
        {
          'label': '更新人',
          'text': '王强'
        },
        {
          'label': '变更说明',
          'text': '初版',
          'full': true
        }
      ],
      'feeSecTitle': '配方行（V1.0）',
      'feeCols': ['子项编码', '子项名称', '来源', '类型', '单位用量', '供应商（带出）'],
      'fees': [
        {
          'cells': ['WBX-1210L', '围板箱 1200×1000×970', '自购', '器具', '1', '宁波华塑包装制品有限公司']
        },
        {
          'cells': ['LJ-C300', '围板 HDPE 波纹板', '自购', '零件', '5', '宁波华塑包装制品有限公司']
        },
        {
          'cells': ['LJ-D400', '箱盖 ABS 吸塑', '自购', '器具', '1', '宁波华塑包装制品有限公司']
        },
        {
          'cells': ['LJ-A100', '锁扣组件 不锈钢', '自购', '零件', '6', '苏州联恒五金制品有限公司']
        }
      ],
      'chain': [
        {
          'role': 'BOM 版本（本版本）',
          'name': 'ZH-2601-A V1.0 · 已停用',
          'self': true
        },
        {
          'role': '组装',
          'name': '历史组装按 V1.0 投料',
        }
      ],
      'timeline': [
        {
          't': '2026-01-10',
          'text': 'V1.0 初版生效',
          'who': '王强'
        },
        {
          't': '2026-05-14',
          'text': 'V1.0 停用 · 由 V2.0 接替',
          'who': '陈金'
        }
      ]
    }
  },
  /* --------------------------------------------------------------------------
   * 角色 roles：键 = RL-xx（角色管理页列表驱动，2026-09-09 G01）
   *   fields: name=角色名 desc=说明 scope=数据权限 accts=账号数；cells 不含外层 td
   * ------------------------------------------------------------------------ */
  roles: {
    'RL-01': { 'row': {"fields": {"name": "系统管理员", "desc": "全部功能 + 系统管理", "scope": "全部项目", "accts": "2"}, "keyHtml": "<b>系统管理员</b>", "cells": ["全部功能 + 系统管理", "全部项目", "<span class=\"td-num\">2</span>"], "ops": [{"t": "权限配置", "act": "openRolePerm('系统管理员')"}]} },
    'RL-02': { 'row': {"fields": {"name": "财务", "desc": "财务应收/应付/项目损益", "scope": "全部项目", "accts": "1"}, "keyHtml": "<b>财务</b>", "cells": ["财务应收/应付/项目损益", "全部项目", "<span class=\"td-num\">1</span>"], "ops": [{"t": "权限配置", "act": "openRolePerm('财务')"}]} },
    'RL-03': { 'row': {"fields": {"name": "财务主管", "desc": "财务全模块 + 付款/回款确认审核", "scope": "全部项目", "accts": "1"}, "keyHtml": "<b>财务主管</b>", "cells": ["财务全模块 + 付款/回款确认审核", "全部项目", "<span class=\"td-num\">1</span>"], "ops": [{"t": "权限配置", "act": "openRolePerm('财务主管')"}]} },
    'RL-04': { 'row': {"fields": {"name": "商务", "desc": "订单/租赁全流程", "scope": "全部项目", "accts": "2"}, "keyHtml": "<b>商务</b>", "cells": ["订单/租赁全流程", "全部项目", "<span class=\"td-num\">2</span>"], "ops": [{"t": "权限配置", "act": "openRolePerm('商务')"}]} },
    'RL-05': { 'row': {"fields": {"name": "商务主管", "desc": "订单/租赁全流程 + 单据审核", "scope": "全部项目", "accts": "1"}, "keyHtml": "<b>商务主管</b>", "cells": ["订单/租赁全流程 + 单据审核", "全部项目", "<span class=\"td-num\">1</span>"], "ops": [{"t": "权限配置", "act": "openRolePerm('商务主管')"}]} },
    'RL-06': { 'row': {"fields": {"name": "物流", "desc": "仓储作业 + 库存查询", "scope": "全部项目", "accts": "1"}, "keyHtml": "<b>物流</b>", "cells": ["仓储作业 + 库存查询", "全部项目", "<span class=\"td-num\">1</span>"], "ops": [{"t": "权限配置", "act": "openRolePerm('物流')"}]} },
    'RL-07': { 'row': {"fields": {"name": "物流主管", "desc": "仓储作业 + 库存查询 + 出/入库审核", "scope": "全部项目", "accts": "1"}, "keyHtml": "<b>物流主管</b>", "cells": ["仓储作业 + 库存查询 + 出/入库审核", "全部项目", "<span class=\"td-num\">1</span>"], "ops": [{"t": "权限配置", "act": "openRolePerm('物流主管')"}]} },
    'RL-08': { 'row': {"fields": {"name": "客户账号", "desc": "仅查看与下单申请", "scope": "所属客户", "accts": "7"}, "keyHtml": "<b>客户账号</b>", "cells": ["仅查看与下单申请", "所属客户", "<span class=\"td-num\">7</span>"], "ops": [{"t": "权限配置", "act": "openRolePerm('客户账号')"}]} },
    'RL-09': { 'row': {"fields": {"name": "供应商账号", "desc": "下发回执与对账", "scope": "所属供应商", "accts": "3"}, "keyHtml": "<b>供应商账号</b>", "cells": ["下发回执与对账", "所属供应商", "<span class=\"td-num\">3</span>"], "ops": [{"t": "权限配置", "act": "openRolePerm('供应商账号')"}]} }
  }
};