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
    version: '2026-09-10',
    desc: '全局演示数据集 · 详情弹窗全站数据驱动 + G12 漏网收口（新增 opLogs/users/dictItems/todoItems/projects/projectDocs/boardRows/profitRows/bomList 9 实体 · 26→35）'
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

    /* ===== 预付（环通 · 预付供应商大箱租金 9 月度 · 已付款） ===== */
     'AP-20260905-013': {
      'row': {"fields": {"supplier": "华骏重卡汽车有限公司", "btype": "对客户应付", "project": "PRJ-2601", "period": "2026-09", "ref": "—", "inbound": "—", "date": "2026-09-05", "status": "未付款"}, "cells": ["华骏重卡汽车有限公司", "<span class=\"tag tag-purple\" style=\"background:#f9f0ff;border-color:#d3adf7;color:#722ed1\">对客户应付</span><div style=\"color:#8c8c8c;font-size:11px;\">交付延误 · 断产赔偿（赔付客户）</div>", "PRJ-2601", "2026-09", "—", "—", "<span class=\"td-num\">68,400.00</span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\" style=\"color:var(--danger)\">68,400.00</span>", "2026-09-05", "2026-09-20", "<span class=\"tag tag-red\">未付款</span>"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "分期付款", "act": "openModal('instModal')"}, {"t": "详情", "detail": true}]},
      'title': '应付账单详情',
      'billNo': 'AP-20260905-013',
      'billType': '对客户应付',
      'status': '未付款',
      'supplier': '华骏重卡汽车有限公司（客户）',
      'project': 'PRJ-2601',
      'period': '2026-09',
      'amount': 68400,
      'paid': 0,
      'genMode': '直接生成（我方赔付客户 · 交付延误/断产/收款违约金，无赔偿单，2026-09-08 会议 4v4）',
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
        { t: '09-05', text: '断产赔偿认定 · 直接生成对客户应付（费用分类=违约金/断产赔偿）', who: '商务-江强' },
        { t: '—', text: '分期付款 3 期（40%/30%/30%）· 付款登记执行', who: '系统', off: true }
      ]
    },

   'AP-20260905-012': {
      'row': {"fields": {"supplier": "环通包装运营", "btype": "预付预付供应商大箱租金（9 月度）", "project": "PRJ-2604", "period": "2026-09", "ref": "RZD-20260815-005", "inbound": "—", "date": "2026-09-05", "status": "已付款"}, "cells": ["环通包装运营", "<span class=\"tag tag-blue\">预付</span><div style=\"color:#8c8c8c;font-size:11px;\">预付供应商大箱租金（9 月度）</div>", "PRJ-2604", "2026-09", "<span class=\"lk\">RZD-20260815-005</span>", "—", "<span class=\"td-num\">30,000.00</span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\">30,000.00</span>", "2026-09-05", "2026-09-30", "<span class=\"tag tag-green\">已付款</span>"], "ops": [{"t": "详情", "detail": true}]},
      billNo: 'AP-20260905-012',
      billType: '预付',
      status: '已付款',
      supplier: '环通循环包装运营（上海）有限公司',
      project: 'PRJ-2604',
      period: '2026-09',
      amount: 30000,
      paid: 30000,
      genMode: '手动创建（预付）',
      scenario: '预付冲抵 · 供应商租金',
      refs: [
        { label: '关联租入单', no: 'RZD-20260815-005', url: '租入管理/租入单列表.html' }
      ],
      fees: [
        { src: 'RZD-20260815-005', desc: '预付供应商大箱租金 · 2026-09 月度', amount: 30000, url: '租入管理/租入单列表.html' }
      ],
      chain: [
        { role: '租入单', name: 'RZD-20260815-005', url: '租入管理/租入单列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260905-012 · 预付', self: true },
        { role: '付款登记', name: '已付清', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '09-05', text: '预付款支付 · 记预付（环通 ¥30,000）', who: '财务' },
        { t: '09-12', text: '预付款部分退款 · 供应商退回 ¥10,000（啥都没买·原路退回，冲减预付）', who: '财务' },
        { t: '09-16', text: '多付退回落单 · 退款登记 TKD-20260916-005（¥10,000 原路退回）', who: '财务' },
        { t: '—', text: '每月 预付冲抵 · 租金应付生成后自预付冲抵', who: '系统', off: true }
      ]
    },
   'AP-20260912-PRJ2601-YJT': {
      'row': {"fields": {"supplier": "安吉智行物流", "btype": "对客户应付押金退还（ZL-20260901-032 结清·关联押金应收）", "project": "PRJ-2601", "period": "2026-09", "ref": "AR-20260910-PRJ2601-YJ", "inbound": "—", "date": "2026-09-12", "status": "未付款"}, "cells": ["安吉智行物流", "<span class=\"tag tag-purple\">对客户应付</span><div style=\"color:#8c8c8c;font-size:11px;\">押金退还（退客户·押金应收结清转来）</div>", "PRJ-2601", "2026-09", "<span class=\"lk\">AR-20260910-PRJ2601-YJ</span>", "—", "<span class=\"td-num\">30,000.00</span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\" style=\"color:var(--danger)\">30,000.00</span>", "2026-09-12", "2026-09-30", "<span class=\"tag tag-red\">未付款</span>"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}]},
      billNo: 'AP-20260912-PRJ2601-YJT',
      billType: '对客户应付',
      status: '未付款',
      supplier: '安吉智行物流',
      project: 'PRJ-2601',
      period: '2026-09',
      amount: 30000,
      paid: 0,
      genMode: '押金退还联动',
      scenario: '押金收退 · 应收应付承载（2026-09-14 拍板）',
      refs: [
        { label: '关联押金应收', no: 'AR-20260910-PRJ2601-YJ', url: '财务协同/应收账单.html' }
      ],
      fees: [
        { src: 'AR-20260910-PRJ2601-YJ', desc: '租赁押金退还（ZL-20260901-032 退租结清）', amount: 30000, url: '财务协同/应收账单.html' }
      ],
      chain: [
        { role: '押金应收', name: 'AR-20260910-PRJ2601-YJ · 押金', url: '财务协同/应收账单.html' },
        { role: '应付账单（本单）', name: 'AP-20260912-PRJ2601-YJT · 押金退还', self: true },
        { role: '付款登记', name: '待付款', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '09-10', text: '押金收取 · 记应收押金（AR-20260910-PRJ2601-YJ ¥30,000）', who: '财务' },
        { t: '09-12', text: '退租结清 · 押金全额退还 → 生成对客户应付（本单）', who: '系统' },
        { t: '—', text: '付款登记 · 确认后押金退清', who: '财务', off: true }
      ]
    },

    /* ===== 采购应付（甬城塑业 · 未付款 · 财务通道主场景） ===== */
    'AP-20260901-008': {
      'row': {"fields": {"supplier": "甬城塑业包装制品有限公司", "btype": "采购应付", "project": "PRJ-2601", "period": "2026-09", "ref": "PO-20260901-017", "inbound": "CGRK-20260828-011", "date": "2026-09-01", "status": "未付款"}, "note": "3", "cells": ["甬城塑业包装制品有限公司", "<span class=\"tag tag-blue\">采购应付</span>", "PRJ-2601", "2026-09", "<span class=\"lk\">PO-20260901-017</span>", "<span class=\"lk\">CGRK-20260828-011</span>", "<span class=\"td-num\">84,000.00</span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\" style=\"color:var(--danger)\">84,000.00</span>", "2026-09-01", "2026-09-30", "<span class=\"tag tag-red\">未付款</span>"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}, {"t": "详情", "detail": true}]},
      billNo: 'AP-20260901-008',
      billType: '采购应付',
      status: '未付款',
      supplier: '甬城塑业包装制品有限公司',
      project: 'PRJ-2601',
      period: '2026-09',
      amount: 84000,
      paid: 0,
      genMode: '验收通过自动生成',
      scenario: '财务通道 · 采购应付',
      refs: [
        { label: '关联采购订单', no: 'PO-20260901-017', url: '采购管理/采购订单列表.html' },
        { label: '关联采购入库', no: 'CGRK-20260828-011', url: '采购管理/采购入库列表.html' }
      ],
      fees: [
        { src: 'CGRK-20260828-011', desc: '采购入库验收 · 采购应付', amount: 84000, url: '采购管理/采购入库列表.html' }
      ],
      chain: [
        { role: '采购订单', name: 'PO-20260901-017', url: '采购管理/采购订单列表.html' },
        { role: '采购入库', name: 'CGRK-20260828-011', url: '采购管理/采购入库列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260901-008 · 采购应付', self: true },
        { role: '付款登记', name: '待付款', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '08-28', text: '采购入库验收通过 · CGRK-20260828-011', who: '张帆' },
        { t: '09-01', text: '应付账单自动生成', who: '系统' },
        { t: '—', text: '待付款 → 付款登记确认', off: true }
      ]
    },

    /* ===== 采购应付（吴越联合 · 部分付款） ===== */
    'AP-20260830-007': {
      'row': {"fields": {"supplier": "延陵塑料托盘厂", "btype": "采购应付", "project": "PRJ-2602", "period": "2026-08", "ref": "PO-20260820-013", "inbound": "CGRK-20260827-010", "date": "2026-08-30", "status": "部分付款"}, "cells": ["延陵塑料托盘厂", "<span class=\"tag tag-blue\">采购应付</span>", "PRJ-2602", "2026-08", "<span class=\"lk\">PO-20260820-013</span>", "<span class=\"lk\">CGRK-20260827-010</span>", "<span class=\"td-num\">19,600.00</span>", "<span class=\"td-num\">6,000.00</span>", "<span class=\"td-num\">13,600.00</span>", "2026-08-30", "2026-09-29", "<span class=\"tag tag-orange\">部分付款</span>"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}, {"t": "详情", "detail": true}]},
      billNo: 'AP-20260830-007',
      billType: '采购应付',
      status: '部分付款',
      supplier: '延陵塑料托盘厂',
      project: 'PRJ-2602',
      period: '2026-08',
      amount: 19600,
      paid: 6000,
      genMode: '验收通过自动生成',
      refs: [
        { label: '关联采购订单', no: 'PO-20260820-013', url: '采购管理/采购订单列表.html' },
        { label: '关联采购入库', no: 'CGRK-20260827-010', url: '采购管理/采购入库列表.html' }
      ],
      fees: [
        { src: 'CGRK-20260827-010', desc: '采购入库验收 · 采购应付', amount: 19600, url: '采购管理/采购入库列表.html' }
      ],
      chain: [
        { role: '采购订单', name: 'PO-20260820-013', url: '采购管理/采购订单列表.html' },
        { role: '采购入库', name: 'CGRK-20260827-010', url: '采购管理/采购入库列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260830-007 · 采购应付', self: true },
        { role: '付款登记', name: '已付 6,000.00', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '08-25', text: '采购入库验收通过 · CGRK-20260827-010', who: '张帆' },
        { t: '08-30', text: '应付账单自动生成', who: '系统' },
        { t: '09-05', text: '付款登记 6,000.00 元', who: '王芳' },
        { t: '—', text: '待付尾款 13,600.00 元', off: true }
      ]
    },

    /* ===== 采购应付（延陵托盘 · 已付款） ===== */
    'AP-20260828-006': {
      'row': {"fields": {"supplier": "延陵塑料托盘厂", "btype": "采购应付", "project": "PRJ-2603", "period": "2026-08", "ref": "PO-20260815-011", "inbound": "CGRK-20260820-009", "date": "2026-08-28", "status": "已付款"}, "cells": ["延陵塑料托盘厂", "<span class=\"tag tag-blue\">采购应付</span>", "PRJ-2603", "2026-08", "<span class=\"lk\">PO-20260815-011</span>", "<span class=\"lk\">CGRK-20260820-009</span>", "<span class=\"td-num\">42,500.00</span>", "<span class=\"td-num\">42,500.00</span>", "<span class=\"td-num\">0.00</span>", "2026-08-28", "2026-09-27", "<span class=\"tag tag-green\">已付款</span>"], "ops": [{"t": "详情", "detail": true}]},
      billNo: 'AP-20260828-006',
      billType: '采购应付',
      status: '已付款',
      supplier: '延陵塑料托盘厂',
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
        { t: '08-20', text: '采购入库验收通过 · CGRK-20260820-009', who: '张帆' },
        { t: '08-28', text: '应付账单自动生成', who: '系统' },
        { t: '09-05', text: '付款登记确认 42,500.00 元', who: '王芳' }
      ]
    },

    /* ===== 采购应付（环通 · 租入运营费 · 手动创建，无来源单据） ===== */
    'AP-20260825-005': {
      'row': {"fields": {"supplier": "环通循环包装运营（上海）有限公司", "btype": "采购应付", "project": "—", "period": "2026-08", "ref": "—（租入运营费）", "inbound": "—", "date": "2026-08-25", "status": "未付款"}, "cells": ["环通循环包装运营（上海）有限公司", "<span class=\"tag tag-blue\">采购应付</span>", "—", "2026-08", "—（租入运营费）", "—", "<span class=\"td-num\">126,000.00</span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\" style=\"color:var(--danger)\">126,000.00</span>", "2026-08-25", "2026-09-24", "<span class=\"tag tag-red\">未付款</span>"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}, {"t": "详情", "detail": true}]},
      billNo: 'AP-20260825-005',
      billType: '采购应付',
      status: '未付款',
      supplier: '环通循环包装运营（上海）有限公司',
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

    /* ===== 采购应付（吴越联合 · 已付款） ===== */
    'AP-20260820-004': {
      'row': {"fields": {"supplier": "吴越联合五金制品有限公司", "btype": "采购应付", "project": "PRJ-2601", "period": "2026-08", "ref": "PO-20260810-009", "inbound": "CGRK-20260815-007", "date": "2026-08-20", "status": "已付款"}, "cells": ["吴越联合五金制品有限公司", "<span class=\"tag tag-blue\">采购应付</span>", "PRJ-2601", "2026-08", "<span class=\"lk\">PO-20260810-009</span>", "<span class=\"lk\">CGRK-20260815-007</span>", "<span class=\"td-num\">6,300.00</span>", "<span class=\"td-num\">6,300.00</span>", "<span class=\"td-num\">0.00</span>", "2026-08-20", "2026-09-19", "<span class=\"tag tag-green\">已付款</span>"], "ops": [{"t": "详情", "detail": true}]},
      billNo: 'AP-20260820-004',
      billType: '采购应付',
      status: '已付款',
      supplier: '吴越联合五金制品有限公司',
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
        { t: '08-15', text: '采购入库验收通过 · CGRK-20260815-007', who: '张帆' },
        { t: '08-20', text: '应付账单自动生成', who: '系统' },
        { t: '09-02', text: '付款登记确认 6,300.00 元', who: '王芳' }
      ]
    },

    /* ===== 采购应付（甬城塑业 · 已付款） ===== */
    'AP-20260815-003': {
      'row': {"fields": {"supplier": "甬城塑业包装制品有限公司", "btype": "采购应付", "project": "PRJ-2602", "period": "2026-08", "ref": "PO-20260808-008", "inbound": "CGRK-20260812-006", "date": "2026-08-15", "status": "已付款"}, "cells": ["甬城塑业包装制品有限公司", "<span class=\"tag tag-blue\">采购应付</span>", "PRJ-2602", "2026-08", "<span class=\"lk\">PO-20260808-008</span>", "<span class=\"lk\">CGRK-20260812-006</span>", "<span class=\"td-num\">35,200.00</span>", "<span class=\"td-num\">35,200.00</span>", "<span class=\"td-num\">0.00</span>", "2026-08-15", "2026-09-14", "<span class=\"tag tag-green\">已付款</span>"], "ops": [{"t": "详情", "detail": true}]},
      billNo: 'AP-20260815-003',
      billType: '采购应付',
      status: '已付款',
      supplier: '甬城塑业包装制品有限公司',
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
        { t: '08-12', text: '采购入库验收通过 · CGRK-20260812-006', who: '张帆' },
        { t: '08-15', text: '应付账单自动生成', who: '系统' },
        { t: '08-30', text: '付款登记确认 35,200.00 元', who: '王芳' }
      ]
    },

    /* ===== 租金应付（环通 · 未付款 · L4 多线应付场景） ===== */
    'AP-20260903-010': {
      'row': {"fields": {"supplier": "环通循环包装运营（上海）有限公司", "btype": "租金应付", "project": "PRJ-2604", "period": "2026-09", "ref": "RZD-20260815-005（租入单）", "inbound": "RZRK-20260816-022", "date": "2026-09-03", "status": "未付款"}, "note": "2", "cells": ["环通循环包装运营（上海）有限公司", "<span class=\"tag tag-orange\">租金应付</span>", "PRJ-2604", "2026-09", "<span class=\"lk\" onclick=\"go('../租入管理/租入单列表.html')\">RZD-20260815-005（租入单）</span>", "RZRK-20260816-022", "12,000.00", "0.00", "12,000.00", "2026-09-03", "2026-10-02", "<span class=\"tag tag-orange\">未付款</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}]},
      billNo: 'AP-20260903-010',
      billType: '租金应付',
      status: '未付款',
      supplier: '环通循环包装运营（上海）有限公司',
      project: 'PRJ-2604',
      period: '2026-09',
      amount: 12000,
      paid: 0,
      genMode: '按周期自动生成（月结）',
      scenario: 'L4 · 多线应付（租金线）',
      refs: [
        { label: '关联租入单', no: 'RZD-20260815-005', url: '租入管理/租入单列表.html' },
        { label: '关联租入入库', no: 'RZRK-20260816-022', url: '租入管理/租入入库列表.html' }
      ],
      fees: [
        { src: 'RZD-20260815-005', desc: '租入租金 · 2026-09 账期', amount: 12000, url: '租入管理/租入单列表.html' }
      ],
      chain: [
        { role: '租入单', name: 'RZD-20260815-005', url: '租入管理/租入单列表.html' },
        { role: '租入入库', name: 'RZRK-20260816-022', url: '租入管理/租入入库列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260903-010 · 租金应付', self: true },
        { role: '付款登记', name: '待付款', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '08-16', text: '租入入库确认 · RZRK-20260816-022', who: '张帆' },
        { t: '09-03', text: '按周期生成租金应付（月结）', who: '系统' },
        { t: '—', text: '待付款 → 付款登记确认', off: true }
      ]
    },

    /* ===== 租金应付（环通 · 未付款 · L3 租金应付场景，36,000） ===== */
    'AP-20260903-009': {
      'row': {"fields": {"supplier": "环通循环包装运营（上海）有限公司", "btype": "租金应付", "project": "PRJ-2603", "period": "2026-09", "ref": "RZD-20260815-003（租入单）", "inbound": "RZRK-20260816-021", "date": "2026-09-03", "status": "未付款"}, "note": "1", "cells": ["环通循环包装运营（上海）有限公司", "<span class=\"tag tag-orange\">租金应付</span>", "PRJ-2603", "2026-09", "<span class=\"lk\" onclick=\"go('../租入管理/租入单列表.html')\">RZD-20260815-003（租入单）</span>", "RZRK-20260816-021", "36,000.00", "0.00", "36,000.00", "2026-09-03", "2026-10-02", "<span class=\"tag tag-orange\">未付款</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}]},
      billNo: 'AP-20260903-009',
      billType: '租金应付',
      status: '未付款',
      supplier: '环通循环包装运营（上海）有限公司',
      project: 'PRJ-2603',
      period: '2026-09',
      amount: 36000,
      paid: 0,
      genMode: '按周期自动生成（月结）',
      scenario: 'L3 · 步骤 8/8 租金应付',
      refs: [
        { label: '关联租入单', no: 'RZD-20260815-003', url: '租入管理/租入单列表.html' },
        { label: '关联租入入库', no: 'RZRK-20260816-021', url: '租入管理/租入入库列表.html' }
      ],
      fees: [
        { src: 'RZD-20260815-003', desc: '租入租金 · 2026-09 账期', amount: 36000, url: '租入管理/租入单列表.html' }
      ],
      chain: [
        { role: '租入单', name: 'RZD-20260815-003', url: '租入管理/租入单列表.html' },
        { role: '租入入库', name: 'RZRK-20260816-021', url: '租入管理/租入入库列表.html' },
        { role: '应付账单（本单）', name: 'AP-20260903-009 · 租金应付', self: true },
        { role: '付款登记', name: '待付款', url: '财务协同/付款登记.html' }
      ],
      timeline: [
        { t: '08-16', text: '租入入库确认 · RZRK-20260816-021', who: '张帆' },
        { t: '09-03', text: '按周期生成租金应付（月结）', who: '系统' },
        { t: '—', text: '待付款 → 付款登记确认', off: true }
      ]
    },

    /* ===== 赔付应付（环通 · 未付款 · 丢损赔偿场景） ===== */
    'AP-20260903-011': {
      'row': {"fields": {"supplier": "环通循环包装运营（上海）有限公司", "btype": "赔付应付", "project": "PRJ-2603", "period": "2026-09", "ref": "BS-20260902-010（丢损赔偿单）", "inbound": "—", "date": "2026-09-03", "status": "未付款"}, "cells": ["环通循环包装运营（上海）有限公司", "<span class=\"tag tag-orange\">赔付应付</span>", "PRJ-2603", "2026-09", "BS-20260902-010（丢损赔偿单）", "—", "930.00", "0.00", "930.00", "2026-09-03", "2026-09-18", "<span class=\"tag tag-orange\">未付款</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}]},
      billNo: 'AP-20260903-011',
      billType: '赔付应付',
      status: '未付款',
      supplier: '环通循环包装运营（上海）有限公司',
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
    },
    'AP-20260911-013': {
      'row': {"fields": {"supplier": "环通循环包装运营（上海）有限公司", "btype": "租金应付（按持有量×天数）", "project": "PRJ-2603", "period": "2026-09", "ref": "RZD-20260815-003 / RZD-20260815-005", "inbound": "RZRK-20260816-021 / -022", "date": "2026-09-11", "status": "未付款"}, "cells": ["环通循环包装运营（上海）有限公司", "<span class=\"tag tag-orange\">租金应付（按持有量×天数）</span>", "PRJ-2603", "2026-09", "RZD-20260815-003 / RZD-20260815-005", "RZRK-20260816-021 / -022", "1,140.00", "0.00", "1,140.00", "2026-09-11", "2026-10-13", "<span class=\"tag tag-orange\">未付款</span>"], "ops": [{"t": "详情", "detail": true}, {"t": "付款", "act": "go('../财务协同/付款登记.html')"}]},
      billNo: 'AP-20260911-013',
      billType: '租金应付（按持有量×天数）',
      status: '未付款',
      supplier: '环通循环包装运营（上海）有限公司',
      project: 'PRJ-2603',
      period: '2026-09',
      amount: 1140,
      paid: 0,
      genMode: '按持有量×天数',
      genDate: '2026-09-11',
      refs: [
        {label: '关联租入单', no: 'RZD-20260815-003 / RZD-20260815-005', url: '租入管理/租入单列表.html'},
        {label: '关联租入入库', no: 'RZRK-20260816-021 / RZRK-20260816-022', url: '租入管理/租入入库列表.html'}
      ],
      segCols: ['物料编码', '物料名称', '单位', '起租日期', '止租日期', '天数', '持有量·只天', '日租金(元/天)', '小计(元)'],
      fees: [
        {src: 'stockEvents · 环通 × WBX-1210L', desc: '按持有量计租 · 期段 2026-08-16 ~ 2026-09-03（每日持有 40 只 · 09-03 归还当日仍计）', qty: '760 只天', price: '1.50', amount: 1140, url: '租入管理/租入入库列表.html', cells: ['WBX-1210L', '围板箱 1200×1000×970', '只', '2026-08-16', '2026-09-03', '19', '760', '1.50', '1,140.00']}
      ],
      chain: [
        {role: '租入入库', name: 'RZRK-20260816-021 / -022 · 40 只', url: '租入管理/租入入库列表.html'},
        {role: '应付账单（本单）', name: 'AP-20260911-013 · 按持有量×天数', self: true},
        {role: '付款登记', name: '待付款', url: '财务协同/付款登记.html'}
      ],
      timeline: [
        {t: '08-16', text: '租入入库 30+10 只 · 期段起', who: '张帆'},
        {t: '09-03', text: '整退 30 / 分流 4 只 · 当日仍计 40 只', who: '林国栋'},
        {t: '09-11', text: '账单生成 · 760 只天 × 1.50 元 = 1,140.00 元', who: '系统'}
      ]
    },
  },

  /* --------------------------------------------------------------------------
   * 应收账单 receivableBills：键 = 账单号（赔偿联动行键 = 赔偿单号）
   *   billType: 销售费 / 租赁费 / 预收 / 丢损赔偿
   *   status:   未开票 / 部分收款 / 已结清 / 已收（预收）
   *   fees[]:   qty/price 为展示字符串（汇总行用 '—'），amount 为数字
   *   下游链统一为：本单 → 开票登记 → 收款/银行回单核销
   * ------------------------------------------------------------------------ */
  receivableBills: {

    /* ===== 预收（安吉智行 · 预付 9-10 月租金 · 已收） ===== */
     'AR-20260904-015': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2603", "customer": "环通循环包装运营（上海）有限公司", "btype": "供应商应收", "docs": "租入单 RZD-20260815-005 · 赔付我方", "gen": "直接生成", "date": "2026-09-04", "status": "未开票"}, "cells": ["2026-09", "PRJ-2603", "环通循环包装运营（上海）有限公司", "<span class=\"tag tag-blue\">供应商应收</span><div style=\"color:#8c8c8c;font-size:11px;\">供应商赔付我方 · 租入围板箱缺损 6 只</div>", "租入单 RZD-20260815-005 · 赔付我方", "<span class=\"td-num\"><b>2,850.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-red\">未开票</span>", "<span class=\"tag tag-orange\">直接生成</span>", "2026-09-04 10:12"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}]},
      'title': '应收账单详情',
      'billNo': 'AR-20260904-015',
      'billType': '供应商应收',
      'status': '未开票',
      'customer': '环通循环包装运营（上海）有限公司',
      'project': 'PRJ-2603',
      'period': '2026-09',
      'amount': 2850,
      'paid': 0,
      'genMode': '直接生成（供应商赔付我方 · 无赔偿单，2026-09-08 会议 4v4）',
      'scenario': 'F1 · 供应商应收（4 来源）',
      'refs': [
        { label: '关联租入单', no: 'RZD-20260815-005', url: '租入管理/租入单列表.html' }
      ],
      'fees': [
        { src: 'RZD-20260815-005', desc: '租入围板箱缺损赔付 · 供应商赔付我方', qty: '6 只', price: '475.00', amount: 2850, url: '租入管理/租入单列表.html' }
      ],
      'chain': [
        { role: '租入单', name: 'RZD-20260815-005', url: '租入管理/租入单列表.html' },
        { role: '应收账单（本单）', name: 'AR-20260904-015 · 供应商应收', self: true }
      ],
      'timeline': [
        { t: '09-04', text: '退租验收缺损 6 只 · 直接生成供应商应收（不走赔偿单）', who: '张帆' },
        { t: '—', text: '对方确认 → 开票 → 收款核销', who: '系统', off: true }
      ]
    },

    'AR-20260906-016': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "btype": "预付款（保证金）", "docs": "客户保证金（N3 · 直接建单承载）", "gen": "直接生成", "date": "2026-09-06", "status": "已结清"}, "cells": ["2026-09", "PRJ-2601", "华骏重卡汽车有限公司", "<span class=\"tag tag-purple\" style=\"background:#f9f0ff;border-color:#d3adf7;color:#722ed1\">预付款（保证金）</span><div style=\"color:#8c8c8c;font-size:11px;\">客户保证金 · 无订单 · 直接建单承载</div>", "客户保证金（N3 · 直接建单承载）", "<span class=\"td-num\"><b>50,000.00</b></span>", "<span class=\"td-num\">50,000.00</span>", "<span class=\"tag tag-green\">已结清</span>", "<span class=\"tag tag-orange\">直接生成</span>", "2026-09-06 09:30"], "ops": [{"t": "详情", "detail": true}]},
      'title': '应收账单详情',
      'billNo': 'AR-20260906-016',
      'billType': '预付款（保证金）',
      'status': '已结清',
      'customer': '华骏重卡汽车有限公司',
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
   'AR-20260910-PRJ2601-YJ': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2601", "customer": "安吉智行物流", "btype": "押金客户交付租赁押金（ZL-20260901-032），退租结清后全额退还", "docs": "ZL-20260901-032", "gen": "手动登记", "date": "2026-09-10", "status": "已收"}, "cells": ["2026-09", "PRJ-2601", "安吉智行物流", "<span class=\"tag tag-orange\">押金</span><div style=\"color:#8c8c8c;font-size:11px;\">租赁押金 · 退时转对客户应付</div>", "ZL-20260901-032", "<span class=\"td-num\"><b>30,000.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-green\">已收</span>", "<span class=\"tag tag-blue\">手动登记</span>", "2026-09-10 14:30"], "ops": [{"t": "详情", "detail": true}]},
      billNo: 'AR-20260910-PRJ2601-YJ',
      billType: '押金',
      status: '已收',
      customer: '安吉智行物流',
      project: 'PRJ-2601',
      period: '2026-09',
      amount: 30000,
      verified: 0,
      genMode: '手动登记',
      genDate: '2026-09-10',
      feeType: '押金（客户交付租赁押金 · ZL-20260901-032）',
      scenario: '押金收退 · 应收应付承载（2026-09-14 拍板）',
      fees: [
        { src: 'ZL-20260901-032', desc: '租赁押金收取（退租结清后全额退还）', qty: '—', price: '—', amount: 30000 }
      ],
      chain: [
        { role: '租赁单', name: 'ZL-20260901-032', url: '租赁管理/租赁单列表.html' },
        { role: '应收账单（本单）', name: 'AR-20260910-PRJ2601-YJ · 押金', self: true },
        { role: '对客户应付（退还）', name: 'AP-20260912-PRJ2601-YJT · 押金退还', url: '财务协同/应付账单.html' }
      ],
      timeline: [
        { t: '09-10', text: '押金收取 · 记应收押金（安吉智行 ¥30,000）', who: '财务' },
        { t: '09-12', text: '退租结清 · 押金全额退还 → 转对客户应付 AP-20260912-PRJ2601-YJT（待付款）', who: '系统' }
      ]
    },

    /* ===== 销售费（华骏重卡 · 未开票 · B1 销售线） ===== */
    'AR-2026-09-PRJ2601-S1': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "btype": "销售费（按销售出库自动汇总）关联 XSCK-20260902-015 等 2 单", "docs": "销售出库 XSCK-20260902-015 等", "gen": "自动生成", "date": "2026-09-03", "status": "未开票"}, "note": "1", "cells": ["2026-09", "PRJ-2601", "华骏重卡汽车有限公司", "销售费（按销售出库自动汇总）<div style=\"color:#8c8c8c;font-size:11px;\">关联 XSCK-20260902-015 等 2 单</div>", "销售出库 XSCK-20260902-015 等", "<span class=\"td-num\"><b>10,200.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-red\">未开票</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-09-03 00:06"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-09-PRJ2601-S1',
      billType: '销售费',
      status: '未开票',
      customer: '华骏重卡汽车有限公司',
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
        { role: '收款 / 核销', name: '收款登记 → 银行回单核销', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '09-02', text: '销售出库 · XSCK-20260902-015（1,500 件）', who: '张帆' },
        { t: '09-03', text: '账单自动生成 · 销售费汇总', who: '系统' },
        { t: '—', text: '待开票 → 收款 → 银行回单核销', off: true }
      ]
    },

    /* ===== 销售费（华骏 · SO-0039 第二批按次） ===== */
    'AR-2026-09-PRJ2601-S2': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "btype": "销售费（按次生成）关联 XSCK-20260910-016", "docs": "销售出库 XSCK-20260910-016", "gen": "自动生成", "date": "2026-09-11", "status": "未开票"}, "cells": ["2026-09", "PRJ-2601", "华骏重卡汽车有限公司", "销售费（按次生成）<div style=\"color:#8c8c8c;font-size:11px;\">关联 XSCK-20260910-016 · SO-20260827-0039 第二批</div>", "销售出库 XSCK-20260910-016", "<span class=\"td-num\"><b>1,800.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-red\">未开票</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-09-11 00:06"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-09-PRJ2601-S2',
      billType: '销售费',
      status: '未开票',
      customer: '华骏重卡汽车有限公司',
      project: 'PRJ-2601',
      period: '2026-09',
      amount: 1800,
      verified: 0,
      genMode: '自动生成',
      genDate: '2026-09-11',
      feeType: '销售费（按次生成）',
      scenario: '财务通道 · 销售费应收（按次）',
      fees: [
        { src: 'XSCK-20260910-016', desc: '销售费 · 箱盖 ABS 吸塑（SO-20260827-0039 第二批）', qty: '500 件', price: '3.60', amount: 1800, url: '销售管理/销售出库列表.html' }
      ],
      chain: [
        { role: '销售订单', name: 'SO-20260827-0039（第二批）', url: '销售管理/销售订单列表.html' },
        { role: '销售出库', name: 'XSCK-20260910-016', url: '销售管理/销售出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-09-PRJ2601-S2 · 销售费（按次）', self: true },
        { role: '开票登记', name: '待开票', url: '财务协同/开票登记.html' },
        { role: '收款 / 核销', name: '收款登记 → 银行回单核销', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '09-10', text: '销售出库 · XSCK-20260910-016（500 件）', who: '张帆' },
        { t: '09-11', text: '按次账单自动生成 · 1,800.00 元', who: '系统' },
        { t: '—', text: '待开票 → 收款 → 银行回单核销', off: true }
      ]
    },

    /* ===== 销售费（长风汽制 · 未开票） ===== */
    'AR-2026-09-PRJ2604-S1': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2604", "customer": "长风汽车制造有限公司", "btype": "销售费（按销售出库自动汇总）关联 XSCK-20260901-014", "docs": "销售出库 XSCK-20260901-014 等", "gen": "自动生成", "date": "2026-09-02", "status": "未开票"}, "cells": ["2026-09", "PRJ-2604", "长风汽车制造有限公司", "销售费（按销售出库自动汇总）<div style=\"color:#8c8c8c;font-size:11px;\">关联 XSCK-20260901-014</div>", "销售出库 XSCK-20260901-014 等", "<span class=\"td-num\"><b>1,280.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-red\">未开票</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-09-02 00:06"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-09-PRJ2604-S1',
      billType: '销售费',
      status: '未开票',
      customer: '长风汽车制造有限公司',
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
        { role: '收款 / 核销', name: '收款登记 → 银行回单核销', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '09-01', text: '销售出库 · XSCK-20260901-014（160 件）', who: '张帆' },
        { t: '09-02', text: '账单自动生成 · 销售费汇总', who: '系统' },
        { t: '—', text: '待开票 → 收款 → 银行回单核销', off: true }
      ]
    },

    /* ===== 销售费（东海商用宁波 · 已结清） ===== */
    'AR-2026-08-PRJ2602-S1': {
      'row': {"fields": {"period": "2026-08", "project": "PRJ-2602", "customer": "东海商用宁波分公司", "btype": "销售费（按销售出库自动汇总）关联 XSCK-20260826-012", "docs": "销售出库 XSCK-20260826-012 等", "gen": "自动生成", "date": "2026-08-31", "status": "已结清"}, "cells": ["2026-08", "PRJ-2602", "东海商用宁波分公司", "销售费（按销售出库自动汇总）<div style=\"color:#8c8c8c;font-size:11px;\">关联 XSCK-20260826-012</div>", "销售出库 XSCK-20260826-012 等", "<span class=\"td-num\"><b>6,050.00</b></span>", "<span class=\"td-num\">6,050.00</span>", "<span class=\"tag tag-green\">已结清</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-08-31 00:06"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-08-PRJ2602-S1',
      billType: '销售费',
      status: '已结清',
      customer: '东海商用宁波分公司',
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
        { role: '收款 / 核销', name: '已核销结清', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '08-26', text: '销售出库 · XSCK-20260826-012（605 件）', who: '张帆' },
        { t: '08-31', text: '账单自动生成 · 销售费汇总', who: '系统' },
        { t: '09-02', text: '开票登记', who: '王芳' },
        { t: '09-05', text: '收款核销 6,050.00 元 · 结清', who: '财务' }
      ]
    },

    /* ===== 租赁费（华骏重卡 · 部分收款） ===== */
    'AR-2026-08-PRJ2601': {
      'row': {"fields": {"period": "2026-08", "project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "btype": "租赁费（按租赁出库自动汇总）", "docs": "租赁出库 26 张", "gen": "自动生成", "date": "2026-08-31", "status": "部分收款"}, "note": "2", "cells": ["2026-08", "PRJ-2601", "华骏重卡汽车有限公司", "租赁费（按租赁出库自动汇总）", "租赁出库 26 张", "<span class=\"td-num\"><b>486,200.00</b></span>", "<span class=\"td-num\">186,200.00</span>", "<span class=\"tag tag-orange\">部分收款</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-08-31 00:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-08-PRJ2601',
      billType: '租赁费',
      status: '部分收款',
      customer: '华骏重卡汽车有限公司',
      project: 'PRJ-2601',
      period: '2026-08',
      amount: 486200,
      verified: 186200,
      genMode: '自动生成',
      genDate: '2026-08-31',
      feeType: '租赁费（按租赁出库自动汇总）',
      fees: [
        { src: '租赁出库单 ×26', desc: '租赁费 · 2026-08 账期（按租赁出库自动汇总）', qty: '—', price: '—', amount: 486200, url: '租赁管理/租赁出库列表.html' }
      ],
      chain: [
        { role: '租赁出库', name: '租赁出库 ×26 张', url: '租赁管理/租赁出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-08-PRJ2601 · 租赁费', self: true },
        { role: '开票登记', name: '已开票', url: '财务协同/开票登记.html' },
        { role: '收款 / 核销', name: '部分核销 186,200.00', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '08-31', text: '账单自动生成 · 租赁出库汇总 26 张', who: '系统' },
        { t: '09-02', text: '开票登记', who: '王芳' },
        { t: '09-05', text: '收款 186,200.00 元 · 银行回单核销', who: '财务' },
        { t: '—', text: '待收尾款 300,000.00 元', off: true }
      ]
    },

    /* ===== 租赁费（东海商用宁波 · 未开票） ===== */
    'AR-2026-08-PRJ2602': {
      'row': {"fields": {"period": "2026-08", "project": "PRJ-2602", "customer": "东海商用宁波分公司", "btype": "租赁费（按租赁出库自动汇总）", "docs": "租赁出库 26 张", "gen": "自动生成", "date": "2026-08-31", "status": "未开票"}, "cells": ["2026-08", "PRJ-2602", "东海商用宁波分公司", "租赁费（按租赁出库自动汇总）", "租赁出库 26 张", "<span class=\"td-num\"><b>358,900.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-orange\">未开票</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-08-31 00:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-08-PRJ2602',
      billType: '租赁费',
      status: '未开票',
      customer: '东海商用宁波分公司',
      project: 'PRJ-2602',
      period: '2026-08',
      amount: 358900,
      verified: 0,
      genMode: '自动生成',
      genDate: '2026-08-31',
      feeType: '租赁费（按租赁出库自动汇总）',
      fees: [
        { src: '租赁出库单 ×26', desc: '租赁费 · 2026-08 账期（按租赁出库自动汇总）', qty: '—', price: '—', amount: 358900, url: '租赁管理/租赁出库列表.html' }
      ],
      chain: [
        { role: '租赁出库', name: '租赁出库 ×26 张', url: '租赁管理/租赁出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-08-PRJ2602 · 租赁费', self: true },
        { role: '开票登记', name: '待开票', url: '财务协同/开票登记.html' },
        { role: '收款 / 核销', name: '收款登记 → 银行回单核销', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '08-31', text: '账单自动生成 · 租赁出库汇总 26 张', who: '系统' },
        { t: '—', text: '待开票 → 收款 → 银行回单核销', off: true }
      ]
    },

    /* ===== 租赁费（星途新能源 · 未开票） ===== */
    'AR-2026-08-PRJ2603': {
      'row': {"fields": {"period": "2026-08", "project": "PRJ-2603", "customer": "星途新能源汽车科技有限公司", "btype": "租赁费（按租赁出库自动汇总）", "docs": "租赁出库 26 张", "gen": "自动生成", "date": "2026-08-31", "status": "未开票"}, "cells": ["2026-08", "PRJ-2603", "星途新能源汽车科技有限公司", "租赁费（按租赁出库自动汇总）", "租赁出库 26 张", "<span class=\"td-num\"><b>241,500.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-orange\">未开票</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-08-31 00:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-08-PRJ2603',
      billType: '租赁费',
      status: '未开票',
      customer: '星途新能源汽车科技有限公司',
      project: 'PRJ-2603',
      period: '2026-08',
      amount: 241500,
      verified: 0,
      genMode: '自动生成',
      genDate: '2026-08-31',
      feeType: '租赁费（按租赁出库自动汇总）',
      fees: [
        { src: '租赁出库单 ×26', desc: '租赁费 · 2026-08 账期（按租赁出库自动汇总）', qty: '—', price: '—', amount: 241500, url: '租赁管理/租赁出库列表.html' }
      ],
      chain: [
        { role: '租赁出库', name: '租赁出库 ×26 张', url: '租赁管理/租赁出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-08-PRJ2603 · 租赁费', self: true },
        { role: '开票登记', name: '待开票', url: '财务协同/开票登记.html' },
        { role: '收款 / 核销', name: '收款登记 → 银行回单核销', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '08-31', text: '账单自动生成 · 租赁出库汇总 26 张', who: '系统' },
        { t: '—', text: '待开票 → 收款 → 银行回单核销', off: true }
      ]
    },

    /* ===== 租赁费（华骏重卡 · 已结清） ===== */
    'AR-2026-07-PRJ2601': {
      'row': {"fields": {"period": "2026-07", "project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "btype": "租赁费（按租赁出库自动汇总）", "docs": "租赁出库 26 张", "gen": "自动生成", "date": "2026-07-31", "status": "已结清"}, "cells": ["2026-07", "PRJ-2601", "华骏重卡汽车有限公司", "租赁费（按租赁出库自动汇总）", "租赁出库 26 张", "<span class=\"td-num\"><b>442,800.00</b></span>", "<span class=\"td-num\">442,800.00</span>", "<span class=\"tag tag-green\">已结清</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-07-31 00:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-07-PRJ2601',
      billType: '租赁费',
      status: '已结清',
      customer: '华骏重卡汽车有限公司',
      project: 'PRJ-2601',
      period: '2026-07',
      amount: 442800,
      verified: 442800,
      genMode: '自动生成',
      genDate: '2026-07-31',
      feeType: '租赁费（按租赁出库自动汇总）',
      fees: [
        { src: '租赁出库单 ×26', desc: '租赁费 · 2026-07 账期（按租赁出库自动汇总）', qty: '—', price: '—', amount: 442800, url: '租赁管理/租赁出库列表.html' }
      ],
      chain: [
        { role: '租赁出库', name: '租赁出库 ×26 张', url: '租赁管理/租赁出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-07-PRJ2601 · 租赁费', self: true },
        { role: '开票登记', name: '已开票', url: '财务协同/开票登记.html' },
        { role: '收款 / 核销', name: '已核销结清', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '07-31', text: '账单自动生成 · 租赁出库汇总 26 张', who: '系统' },
        { t: '08-05', text: '开票登记', who: '王芳' },
        { t: '08-20', text: '收款核销 442,800.00 元 · 结清', who: '财务' }
      ]
    },

    /* ===== 丢损赔偿（华骏重卡 · 未开票 · 退租联动转应收） ===== */
    'BS-20260828-004': {
      'row': {"fields": {"period": "2026-08", "project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "btype": "丢损赔偿单（退租联动）", "docs": "丢损赔偿单 BS-20260828-004", "gen": "赔偿联动", "date": "2026-08-28", "status": "未开票"}, "note": "3", "cells": ["2026-08", "PRJ-2601", "华骏重卡汽车有限公司", "丢损赔偿单（退租联动）", "丢损赔偿单 BS-20260828-004", "<span class=\"td-num\"><b>3,690.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-orange\">未开票</span>", "<span class=\"tag tag-blue\">赔偿联动</span>", "2026-08-28 11:30"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'BS-20260828-004',
      billType: '丢损赔偿',
      status: '未开票',
      customer: '华骏重卡汽车有限公司',
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
        { role: '收款 / 核销', name: '收款登记 → 银行回单核销', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '08-28', text: '丢损赔偿审核通过 · BS-20260828-004 转应收', who: '王芳' },
        { t: '08-28', text: '应收账单自动生成', who: '系统' },
        { t: '—', text: '待开票 → 收款 → 银行回单核销', off: true }
      ]
    },

    /* ===== 租赁费（东海商用宁波 · 部分收款） ===== */
    'AR-2026-07-PRJ2602': {
      'row': {"fields": {"period": "2026-07", "project": "PRJ-2602", "customer": "东海商用宁波分公司", "btype": "租赁费（按租赁出库自动汇总）", "docs": "租赁出库 26 张", "gen": "自动生成", "date": "2026-07-31", "status": "部分收款"}, "cells": ["2026-07", "PRJ-2602", "东海商用宁波分公司", "租赁费（按租赁出库自动汇总）", "租赁出库 26 张", "<span class=\"td-num\"><b>366,200.00</b></span>", "<span class=\"td-num\">186,200.00</span>", "<span class=\"tag tag-orange\">部分收款</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-07-31 00:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-07-PRJ2602',
      billType: '租赁费',
      status: '部分收款',
      customer: '东海商用宁波分公司',
      project: 'PRJ-2602',
      period: '2026-07',
      amount: 366200,
      verified: 186200,
      genMode: '自动生成',
      genDate: '2026-07-31',
      feeType: '租赁费（按租赁出库自动汇总）',
      fees: [
        { src: '租赁出库单 ×26', desc: '租赁费 · 2026-07 账期（按租赁出库自动汇总）', qty: '—', price: '—', amount: 366200, url: '租赁管理/租赁出库列表.html' }
      ],
      chain: [
        { role: '租赁出库', name: '租赁出库 ×26 张', url: '租赁管理/租赁出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-07-PRJ2602 · 租赁费', self: true },
        { role: '开票登记', name: '已开票', url: '财务协同/开票登记.html' },
        { role: '收款 / 核销', name: '部分核销 186,200.00', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '07-31', text: '账单自动生成 · 租赁出库汇总 26 张', who: '系统' },
        { t: '08-05', text: '开票登记', who: '王芳' },
        { t: '08-25', text: '收款 186,200.00 元 · 银行回单核销', who: '财务' },
        { t: '—', text: '待收尾款 180,000.00 元', off: true }
      ]
    },

    /* ===== 租赁费（东海商用宁波 · 已结清） ===== */
    'AR-2026-06-PRJ2602': {
      'row': {"fields": {"period": "2026-06", "project": "PRJ-2602", "customer": "东海商用宁波分公司", "btype": "租赁费（按租赁出库自动汇总）", "docs": "租赁出库 26 张", "gen": "自动生成", "date": "2026-06-30", "status": "已结清"}, "cells": ["2026-06", "PRJ-2602", "东海商用宁波分公司", "租赁费（按租赁出库自动汇总）", "租赁出库 26 张", "<span class=\"td-num\"><b>358,900.00</b></span>", "<span class=\"td-num\">358,900.00</span>", "<span class=\"tag tag-green\">已结清</span>", "<span class=\"tag tag-blue\">自动生成</span>", "2026-06-30 00:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-06-PRJ2602',
      billType: '租赁费',
      status: '已结清',
      customer: '东海商用宁波分公司',
      project: 'PRJ-2602',
      period: '2026-06',
      amount: 358900,
      verified: 358900,
      genMode: '自动生成',
      genDate: '2026-06-30',
      feeType: '租赁费（按租赁出库自动汇总）',
      fees: [
        { src: '租赁出库单 ×26', desc: '租赁费 · 2026-06 账期（按租赁出库自动汇总）', qty: '—', price: '—', amount: 358900, url: '租赁管理/租赁出库列表.html' }
      ],
      chain: [
        { role: '租赁出库', name: '租赁出库 ×26 张', url: '租赁管理/租赁出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-06-PRJ2602 · 租赁费', self: true },
        { role: '开票登记', name: '已开票', url: '财务协同/开票登记.html' },
        { role: '收款 / 核销', name: '已核销结清', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '06-30', text: '账单自动生成 · 租赁出库汇总 26 张', who: '系统' },
        { t: '07-05', text: '开票登记', who: '王芳' },
        { t: '07-18', text: '收款核销 358,900.00 元 · 结清', who: '财务' }
      ]
    },
    'AR-2026-09-PRJ2603-U1': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2603", "customer": "星途新能源汽车科技有限公司", "btype": "租赁费（按实际使用量生成）", "docs": "按客户对账量录入 · 数量×单价", "gen": "按实际使用量", "date": "2026-09-08", "status": "未开票"}, "cells": ["2026-09", "PRJ-2603", "星途新能源汽车科技有限公司", "租赁费（按实际使用量生成）", "按客户对账量录入 · 数量×单价", "<span class=\"td-num\"><b>186,400.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-orange\">未开票</span>", "<span class=\"tag tag-blue\">按实际使用量</span>", "2026-09-08 14:20"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      billNo: 'AR-2026-09-PRJ2603-U1',
      billType: '租赁费',
      status: '未开票',
      customer: '星途新能源汽车科技有限公司',
      project: 'PRJ-2603',
      period: '2026-09',
      amount: 186400,
      verified: 0,
      genMode: '按实际使用量',
      genDate: '2026-09-08',
      feeType: '租赁费（按实际使用量生成 · 按客户对账量录入）',
      fees: [
        { src: '客户对账量 ×26 张', desc: '租赁费 · 2026-09（按实际使用量：46,600 套·日 × 4.00 元）', qty: '46,600', price: '4.00', amount: 186400, url: '租赁管理/租赁出库列表.html' }
      ],
      chain: [
        { role: '租赁出库', name: '实际使用量 ×26 张', url: '租赁管理/租赁出库列表.html' },
        { role: '应收账单（本单）', name: 'AR-2026-09-PRJ2603-U1 · 按实际使用量', self: true },
        { role: '开票登记', name: '待开票', url: '财务协同/开票登记.html' },
        { role: '收款 / 核销', name: '收款登记 → 银行回单核销', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '09-08', text: '按客户对账量录入生成 · 数量×单价（46,600 × 4.00）', who: '王芳' },
        { t: '—', text: '待开票 → 收款 → 银行回单核销', off: true }
      ]
    },

    'AR-2026-09-PRJ2601-D1': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "btype": "租赁费（按持有量×天数）", "docs": "stockEvents 事件流水 ×3", "gen": "按持有量×天数", "date": "2026-09-11", "status": "未开票"}, "cells": ["2026-09", "PRJ-2601", "华骏重卡汽车有限公司", "租赁费（按持有量×天数）", "期段 09-01 ~ 09-10 · 每日在租量合计 4,940 套天", "<span class=\"td-num\"><b>9,880.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-red\">未开票</span>", "<span class=\"tag tag-blue\">按持有量×天数</span>", "2026-09-11 09:00"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
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
    },
    'AR-2026-09-PRJ2603-D1': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2603", "customer": "星途新能源汽车科技有限公司", "btype": "租赁费（按次套数）", "docs": "CK-20260829-013 ×1 次", "gen": "按次套数", "date": "2026-09-11", "status": "未开票"}, "cells": ["2026-09", "PRJ-2603", "星途新能源汽车科技有限公司", "租赁费（按次套数）", "出库 1 次 × 60 套 × 4.50 元/次", "<span class=\"td-num\"><b>270.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"tag tag-red\">未开票</span>", "<span class=\"tag tag-blue\">按次套数</span>", "2026-09-11 09:05"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}, {"t": "核销", "act": "go('../财务协同/银行回单核销.html')"}]},
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
    },
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
      'row': {"fields": {"supplier": "延陵塑料托盘厂", "ref": "AP-20260830-007", "bank": "招商银行苏州分行 1109××××8821", "date": "2026-09-02", "status": "待确认"}, "note": "1", "cells": ["延陵塑料托盘厂", "<span class=\"lk\">AP-20260830-007</span>", "<span class=\"td-num\">6,000.00</span>", "2026-09-02", "招商银行苏州分行 1109××××8821", "<span class=\"tag tag-orange\">待确认</span>"], "ops": [{"t": "确认", "act": "go('../财务协同/付款确认.html?id=PAY-20260902-005')"}, {"t": "详情", "act": "go('../财务协同/付款详情.html?id=PAY-20260902-005')"}]},
      title: '付款登记详情',
      info: [
        { label: '付款单号', text: 'PAY-20260902-005', full: true },
        { label: '状态', tag: '待确认' },
        { label: '付款日期', text: '2026-09-02' },
        { label: '供应商', text: '延陵塑料托盘厂', full: true },
        { label: '关联应付', text: 'AP-20260830-007', url: '财务协同/应付账单.html' },
        { label: '付款金额', text: '6,000.00 元' },
        { label: '付款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务-周敏' },
        { label: '付款方式', text: '银行转账' },
        { label: '凭证', text: '已上传' },
        { label: '备注', text: '—' }
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
      'row': {"fields": {"supplier": "延陵塑料托盘厂", "ref": "AP-20260828-006", "bank": "中国银行常州分行 3325××××0067", "date": "2026-08-31", "status": "已确认"}, "cells": ["延陵塑料托盘厂", "<span class=\"lk\">AP-20260828-006</span>", "<span class=\"td-num\">42,500.00</span>", "2026-08-31", "中国银行常州分行 3325××××0067", "<span class=\"tag tag-green\">已确认</span>"], "ops": [{"t": "详情", "act": "go('../财务协同/付款详情.html?id=PAY-20260831-004')"}]},
      title: '付款登记详情',
      info: [
        { label: '付款单号', text: 'PAY-20260831-004', full: true },
        { label: '状态', tag: '已确认' },
        { label: '付款日期', text: '2026-08-31' },
        { label: '供应商', text: '延陵塑料托盘厂', full: true },
        { label: '关联应付', text: 'AP-20260828-006', url: '财务协同/应付账单.html' },
        { label: '付款金额', text: '42,500.00 元' },
        { label: '付款账户', text: '中国银行常州分行 3325××××0067' },
        { label: '登记人', text: '财务-周敏' },
        { label: '付款方式', text: '银行转账' },
        { label: '凭证', text: '已上传' },
        { label: '备注', text: '—' }
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
      'row': {"fields": {"supplier": "甬城塑业包装制品有限公司", "ref": "AP-20260815-003", "bank": "工商银行宁波分行 4402××××5531", "date": "2026-08-28", "status": "已确认"}, "cells": ["甬城塑业包装制品有限公司", "<span class=\"lk\">AP-20260815-003</span>", "<span class=\"td-num\">35,200.00</span>", "2026-08-28", "工商银行宁波分行 4402××××5531", "<span class=\"tag tag-green\">已确认</span>"], "ops": [{"t": "详情", "act": "go('../财务协同/付款详情.html?id=PAY-20260828-003')"}]},
      title: '付款登记详情',
      info: [
        { label: '付款单号', text: 'PAY-20260828-003', full: true },
        { label: '状态', tag: '已确认' },
        { label: '付款日期', text: '2026-08-28' },
        { label: '供应商', text: '甬城塑业包装制品有限公司', full: true },
        { label: '关联应付', text: 'AP-20260815-003', url: '财务协同/应付账单.html' },
        { label: '付款金额', text: '35,200.00 元' },
        { label: '付款账户', text: '工商银行宁波分行 4402××××5531' },
        { label: '登记人', text: '财务-周敏' },
        { label: '付款方式', text: '银行转账' },
        { label: '凭证', text: '已上传' },
        { label: '备注', text: '—' }
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
      'row': {"fields": {"supplier": "吴越联合五金制品有限公司", "ref": "AP-20260820-004", "bank": "招商银行苏州分行 1109××××8821", "date": "2026-08-25", "status": "已确认"}, "cells": ["吴越联合五金制品有限公司", "<span class=\"lk\">AP-20260820-004</span>", "<span class=\"td-num\">6,300.00</span>", "2026-08-25", "招商银行苏州分行 1109××××8821", "<span class=\"tag tag-green\">已确认</span>"], "ops": [{"t": "详情", "act": "go('../财务协同/付款详情.html?id=PAY-20260825-002')"}]},
      title: '付款登记详情',
      info: [
        { label: '付款单号', text: 'PAY-20260825-002', full: true },
        { label: '状态', tag: '已确认' },
        { label: '付款日期', text: '2026-08-25' },
        { label: '供应商', text: '吴越联合五金制品有限公司', full: true },
        { label: '关联应付', text: 'AP-20260820-004', url: '财务协同/应付账单.html' },
        { label: '付款金额', text: '6,300.00 元' },
        { label: '付款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务-周敏' },
        { label: '付款方式', text: '银行转账' },
        { label: '凭证', text: '已上传' },
        { label: '备注', text: '—' }
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
      'row': {"fields": {"supplier": "环通循环包装运营（上海）有限公司", "ref": "AP-20260815-003", "bank": "建设银行上海分行 6217××××9045", "date": "2026-08-18", "status": "已确认"}, "cells": ["环通循环包装运营（上海）有限公司", "<span class=\"lk\">AP-20260815-003</span>", "<span class=\"td-num\">58,000.00</span>", "2026-08-18", "建设银行上海分行 6217××××9045", "<span class=\"tag tag-green\">已确认</span>"], "ops": [{"t": "详情", "act": "go('../财务协同/付款详情.html?id=PAY-20260818-001')"}]},
      title: '付款登记详情',
      info: [
        { label: '付款单号', text: 'PAY-20260818-001', full: true },
        { label: '状态', tag: '已确认' },
        { label: '付款日期', text: '2026-08-18' },
        { label: '供应商', text: '环通循环包装运营（上海）有限公司', full: true },
        { label: '关联应付', text: 'AP-20260815-003', url: '财务协同/应付账单.html' },
        { label: '付款金额', text: '58,000.00 元' },
        { label: '付款账户', text: '建设银行上海分行 6217××××9045' },
        { label: '登记人', text: '财务-周敏' },
        { label: '付款方式', text: '银行转账' },
        { label: '凭证', text: '已上传' },
        { label: '备注', text: '—' }
      ],
      feeCols: ['关联账单', '账单类型', '本次付款(元)'],
      fees: [
        { cells: ['AP-20260815-003', '采购应付', '58,000.00'], links: { 0: '财务协同/应付账单.html' } }
      ],
      chain: [
        { role: '应付账单', name: 'AP-20260815-003', url: '财务协同/应付账单.html' },
        { role: '付款登记（本单）', name: 'PAY-20260818-001', self: true },
        { role: '付款确认', name: '已确认 · 账单转已付款' }
      ],
      timeline: [
        { t: '08-18 10:12', text: '付款登记 · 上传付款凭证', who: '财务-周敏' },
        { t: '08-19 09:40', text: '付款确认通过 · 账单转已付款', who: '王芳' }
      ]
    }
  },

  /* 收款登记（键 = HK 收款单号） */
  receipts: {
    'HK-20260830-014': {
      'row': {"fields": {"customer": "华骏重卡汽车有限公司", "ref": "AR-2026-08-PRJ2601", "bank": "招行基本户 1209****8866", "receipt": "已上传", "date": "2026-08-30", "status": "待核销"}, "note": "1", "cells": ["华骏重卡汽车有限公司", "AR-2026-08-PRJ2601", "<span class=\"td-num\"><b>286,500.00</b></span>", "2026-08-30", "招行基本户 1209****8866", "<span class=\"tag tag-green\">已上传</span>", "<span class=\"tag tag-orange\">待核销</span>"], "ops": [{"t": "确认收款", "act": "openModal('auditModal')"}, {"t": "详情", "act": "go('../财务协同/收款详情.html?id=HK-20260830-014')"}, {"t": "去核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      title: '收款登记详情',
      info: [
        { label: '收款单号', text: 'HK-20260830-014', full: true },
        { label: '银行回单状态', tag: '已上传' },
        { label: '核销状态', tag: '待核销' },
        { label: '客户', text: '华骏重卡汽车有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-08-PRJ2601', url: '财务协同/应收账单.html' },
        { label: '发票关联', text: 'INV-20260830-012', url: '财务协同/开票登记.html' },
        { label: '收款金额', text: '286,500.00 元' },
        { label: '收款日期', text: '2026-08-30' },
        { label: '收款账户', text: '招行基本户 1209****8866' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['关联账单', '费用项', '本次收款(元)', '核销去向'],
      fees: [
        { cells: ['AR-2026-08-PRJ2601', '租赁费 · 部分收款', '286,500.00', '银行回单核销（待执行）'], links: { 0: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-08-PRJ2601', url: '财务协同/应收账单.html' },
        { role: '开票登记', name: 'INV-20260830-012', url: '财务协同/开票登记.html' },
        { role: '收款登记（本单）', name: 'HK-20260830-014', self: true },
        { role: '银行回单核销', name: 'SD-20260830-011', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '08-30 10:20', text: '收款到账 · 招行基本户', who: '财务-周敏' },
        { t: '08-30 10:35', text: '银行回单上传 · 与应收账单关联', who: '财务-周敏' },
        { t: '—', text: '待核销 → 银行回单核销勾对', off: true }
      ]
    },
    'HK-20260828-013': {
      'row': {"fields": {"customer": "东海商用宁波分公司", "ref": "AR-2026-07-PRJ2602", "bank": "建行一般户 3321****0417", "receipt": "已上传", "date": "2026-08-28", "status": "待核销"}, "cells": ["东海商用宁波分公司", "AR-2026-07-PRJ2602", "<span class=\"td-num\"><b>158,420.50</b></span>", "2026-08-28", "建行一般户 3321****0417", "<span class=\"tag tag-green\">已上传</span>", "<span class=\"tag tag-orange\">待核销</span>"], "ops": [{"t": "确认收款", "act": "openModal('auditModal')"}, {"t": "详情", "act": "go('../财务协同/收款详情.html?id=HK-20260828-013')"}, {"t": "去核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      title: '收款登记详情',
      info: [
        { label: '收款单号', text: 'HK-20260828-013', full: true },
        { label: '银行回单状态', tag: '已上传' },
        { label: '核销状态', tag: '待核销' },
        { label: '客户', text: '东海商用宁波分公司', full: true },
        { label: '关联应收', text: 'AR-2026-07-PRJ2602', url: '财务协同/应收账单.html' },
        { label: '发票关联', text: 'INV-20260826-011', url: '财务协同/开票登记.html' },
        { label: '收款金额', text: '158,420.50 元' },
        { label: '收款日期', text: '2026-08-28' },
        { label: '收款账户', text: '建行一般户 3321****0417' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['关联账单', '费用项', '本次收款(元)', '核销去向'],
      fees: [
        { cells: ['AR-2026-07-PRJ2602', '租赁费 · 部分收款', '158,420.50', '银行回单核销（待执行）'], links: { 0: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-07-PRJ2602', url: '财务协同/应收账单.html' },
        { role: '开票登记', name: 'INV-20260826-011', url: '财务协同/开票登记.html' },
        { role: '收款登记（本单）', name: 'HK-20260828-013', self: true },
        { role: '银行回单核销', name: 'SD-20260828-010', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '08-28 09:50', text: '收款到账 · 建行一般户', who: '财务-周敏' },
        { t: '08-28 10:10', text: '银行回单上传 · 与应收账单关联', who: '财务-周敏' },
        { t: '—', text: '待核销 → 银行回单核销勾对', off: true }
      ]
    },
    'HK-20260825-012': {
      'row': {"fields": {"customer": "华骏重卡汽车有限公司", "ref": "AR-2026-07-PRJ2601", "bank": "招行基本户 1209****8866", "receipt": "已上传", "date": "2026-08-25", "status": "部分核销"}, "cells": ["华骏重卡汽车有限公司", "AR-2026-07-PRJ2601", "<span class=\"td-num\"><b>98,000.00</b></span>", "2026-08-25", "招行基本户 1209****8866", "<span class=\"tag tag-green\">已上传</span>", "<span class=\"tag tag-blue\">部分核销</span>"], "ops": [{"t": "确认收款", "act": "openModal('auditModal')"}, {"t": "详情", "act": "go('../财务协同/收款详情.html?id=HK-20260825-012')"}, {"t": "去核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      title: '收款登记详情',
      info: [
        { label: '收款单号', text: 'HK-20260825-012', full: true },
        { label: '银行回单状态', tag: '已上传' },
        { label: '核销状态', tag: '部分核销' },
        { label: '客户', text: '华骏重卡汽车有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-07-PRJ2601', url: '财务协同/应收账单.html' },
        { label: '发票关联', text: 'INV-20260820-010', url: '财务协同/开票登记.html' },
        { label: '收款金额', text: '98,000.00 元' },
        { label: '收款日期', text: '2026-08-25' },
        { label: '收款账户', text: '招行基本户 1209****8866' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['关联账单', '费用项', '本次收款(元)', '核销去向'],
      fees: [
        { cells: ['AR-2026-07-PRJ2601', '租赁费 · 部分收款', '98,000.00', '已核销 60,000.00 · 余 38,000.00'], links: { 0: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-07-PRJ2601', url: '财务协同/应收账单.html' },
        { role: '开票登记', name: 'INV-20260820-010', url: '财务协同/开票登记.html' },
        { role: '收款登记（本单）', name: 'HK-20260825-012', self: true },
        { role: '银行回单核销', name: 'SD-20260825-009 · 部分核销', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '08-25 14:05', text: '收款到账 · 招行基本户', who: '财务-周敏' },
        { t: '08-25 14:20', text: '银行回单上传 · 与应收账单关联', who: '财务-周敏' },
        { t: '08-30 14:22', text: '银行回单核销 60,000.00 元 · 部分核销', who: '李婧' },
        { t: '—', text: '余 38,000.00 待后续核销', off: true }
      ]
    },
    'HK-20260822-011': {
      'row': {"fields": {"customer": "星途新能源汽车科技有限公司", "ref": "AR-2026-07-PRJ2603", "bank": "工行一般户 0200****5533", "receipt": "补传回单", "date": "2026-08-22", "status": "已核销"}, "cells": ["星途新能源汽车科技有限公司", "AR-2026-07-PRJ2603", "<span class=\"td-num\"><b>65,320.00</b></span>", "2026-08-22", "工行一般户 0200****5533", "<span class=\"ops\"><a>补传回单</a></span>", "<span class=\"tag tag-green\">已核销</span>"], "ops": [{"t": "确认收款", "act": "openModal('auditModal')"}, {"t": "详情", "act": "go('../财务协同/收款详情.html?id=HK-20260822-011')"}, {"t": "去核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      title: '收款登记详情',
      info: [
        { label: '收款单号', text: 'HK-20260822-011', full: true },
        { label: '银行回单状态', tag: '补传回单' },
        { label: '核销状态', tag: '已核销' },
        { label: '客户', text: '星途新能源汽车科技有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-07-PRJ2603', url: '财务协同/应收账单.html' },
        { label: '发票关联', text: 'INV-20260815-009', url: '财务协同/开票登记.html' },
        { label: '收款金额', text: '65,320.00 元' },
        { label: '收款日期', text: '2026-08-22' },
        { label: '收款账户', text: '工行一般户 0200****5533' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['关联账单', '费用项', '本次收款(元)', '核销去向'],
      fees: [
        { cells: ['AR-2026-07-PRJ2603', '租赁费 · 部分收款', '65,320.00', '已核销（全额）'], links: { 0: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-07-PRJ2603', url: '财务协同/应收账单.html' },
        { role: '开票登记', name: 'INV-20260815-009', url: '财务协同/开票登记.html' },
        { role: '收款登记（本单）', name: 'HK-20260822-011', self: true },
        { role: '银行回单核销', name: 'SD-20260822-008 · 已核销', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '08-22 11:30', text: '收款到账 · 工行一般户', who: '财务-周敏' },
        { t: '08-26 09:15', text: '补传收款单', who: '财务-周敏' },
        { t: '08-28 10:05', text: '银行回单核销 65,320.00 元 · 全额核销', who: '李婧' }
      ]
    },
    'HK-20260818-010': {
      'row': {"fields": {"customer": "华骏重卡汽车有限公司", "ref": "BS-20260802-001", "bank": "招行基本户 1209****8866", "receipt": "已上传", "date": "2026-08-18", "status": "已核销"}, "cells": ["华骏重卡汽车有限公司", "BS-20260802-001", "<span class=\"td-num\"><b>860.00</b></span>", "2026-08-18", "招行基本户 1209****8866", "<span class=\"tag tag-green\">已上传</span>", "<span class=\"tag tag-green\">已核销</span>"], "ops": [{"t": "确认收款", "act": "openModal('auditModal')"}, {"t": "详情", "act": "go('../财务协同/收款详情.html?id=HK-20260818-010')"}, {"t": "去核销", "act": "go('../财务协同/银行回单核销.html')"}]},
      title: '收款登记详情',
      info: [
        { label: '收款单号', text: 'HK-20260818-010', full: true },
        { label: '银行回单状态', tag: '已上传' },
        { label: '核销状态', tag: '已核销' },
        { label: '客户', text: '华骏重卡汽车有限公司', full: true },
        { label: '关联应收', text: 'BS-20260802-001（丢损赔偿）' },
        { label: '发票关联', text: '—' },
        { label: '收款金额', text: '860.00 元' },
        { label: '收款日期', text: '2026-08-18' },
        { label: '收款账户', text: '招行基本户 1209****8866' },
        { label: '登记人', text: '财务-周敏' }
      ],
      feeCols: ['关联账单', '费用项', '本次收款(元)', '核销去向'],
      fees: [
        { cells: ['BS-20260802-001', '丢损赔偿款', '860.00', '已核销（全额）'] }
      ],
      chain: [
        { role: '丢损赔偿单', name: 'BS-20260802-001' },
        { role: '收款登记（本单）', name: 'HK-20260818-010', self: true },
        { role: '银行回单核销', name: 'SD-20260818-006 · 已核销', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '08-18 15:40', text: '收款到账 · 招行基本户', who: '财务-周敏' },
        { t: '08-18 15:55', text: '银行回单上传 · 关联丢损赔偿单', who: '财务-周敏' },
        { t: '08-26 16:40', text: '银行回单核销 860.00 元 · 全额核销', who: '李婧' }
      ]
    }
  },

  /* 开票登记（键 = INV 登记单号） */
  invoices: {
    'INV-20260902-013': {
      'row': {"fields": {"no": "26119800421390", "itype": "专票", "buyer": "东海商用汽车有限公司宁波分公司", "ref": "AR-2026-08-PRJ2603", "date": "2026-09-02", "status": "已红冲"}, "cells": ["26119800421390", "<span class=\"tag tag-blue\">专票</span>", "东海商用汽车有限公司宁波分公司", "AR-2026-08-PRJ2603", "<span class=\"td-num\"><b>-46,800.00</b></span>", "13%", "2026-09-02", "<span class=\"tag tag-red\">已红冲</span>"], "ops": [{"t": "详情", "act": "go('../财务协同/开票详情.html?id=INV-20260902-013')"}, {"t": "查看账单", "act": "go('../财务协同/应收账单.html')"}]},
      title: '开票登记详情',
      info: [
        { label: '登记单号', text: 'INV-20260902-013', full: true },
        { label: '状态', tag: '已红冲' },
        { label: '开票日期', text: '2026-09-02' },
        { label: '发票号码', text: '26119800421390' },
        { label: '发票类型', text: '增值税专用发票' },
        { label: '购方', text: '东海商用汽车有限公司宁波分公司', full: true },
        { label: '关联应收', text: 'AR-2026-08-PRJ2603', url: '财务协同/应收账单.html' },
        { label: '价税合计', text: '-46,800.00 元' },
        { label: '税率', text: '13%' },
        { label: '登记人', text: '财务-周敏' },
        { label: '备注', text: '—' }
      ],
      feeCols: ['费用项', '关联账单', '税率', '开票金额(元)'],
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
      'row': {"fields": {"no": "26119800421376", "itype": "专票", "buyer": "华骏重卡汽车有限公司", "ref": "AR-2026-08-PRJ2601", "date": "2026-08-30", "status": "已登记"}, "note": "1", "cells": ["26119800421376", "<span class=\"tag tag-blue\">专票</span>", "华骏重卡汽车有限公司", "AR-2026-08-PRJ2601", "<span class=\"td-num\"><b>186,200.00</b></span>", "13%", "2026-08-30", "<span class=\"tag tag-green\">已登记</span>"], "ops": [{"t": "开票确认", "act": "openModal('auditModal')"}, {"t": "详情", "act": "go('../财务协同/开票详情.html?id=INV-20260830-012')"}, {"t": "查看账单", "act": "go('../财务协同/应收账单.html')"}, {"t": "收款", "act": "go('../财务协同/收款登记.html')"}]},
      title: '开票登记详情',
      info: [
        { label: '登记单号', text: 'INV-20260830-012', full: true },
        { label: '状态', tag: '已登记' },
        { label: '开票日期', text: '2026-08-30' },
        { label: '发票号码', text: '26119800421376' },
        { label: '发票类型', text: '增值税专用发票' },
        { label: '购方', text: '华骏重卡汽车有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-08-PRJ2601', url: '财务协同/应收账单.html' },
        { label: '价税合计', text: '186,200.00 元' },
        { label: '税率', text: '13%' },
        { label: '登记人', text: '财务-周敏' },
        { label: '备注', text: '—' }
      ],
      feeCols: ['费用项', '关联账单', '税率', '开票金额(元)'],
      fees: [
        { cells: ['租赁费 · 2026-08', 'AR-2026-08-PRJ2601', '13%', '186,200.00'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-08-PRJ2601', url: '财务协同/应收账单.html' },
        { role: '开票登记（本单）', name: 'INV-20260830-012', self: true },
        { role: '收款登记', name: 'HK-20260830-014', url: '财务协同/收款登记.html' },
        { role: '银行回单核销', name: 'SD-20260830-011', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '08-30', text: '应收账单汇总 · AR-2026-08-PRJ2601', who: '系统' },
        { t: '08-30 16:40', text: '开票登记 · 发票号码 26119800421376', who: '财务-周敏' },
        { t: '—', text: '待收款 → 银行回单核销', off: true }
      ]
    },
    'INV-20260826-011': {
      'row': {"fields": {"no": "26119800420988", "itype": "专票", "buyer": "东海商用宁波分公司", "ref": "AR-2026-07-PRJ2602", "date": "2026-08-26", "status": "已登记"}, "cells": ["26119800420988", "<span class=\"tag tag-blue\">专票</span>", "东海商用宁波分公司", "AR-2026-07-PRJ2602", "<span class=\"td-num\"><b>186,200.00</b></span>", "13%", "2026-08-26", "<span class=\"tag tag-green\">已登记</span>"], "ops": [{"t": "开票确认", "act": "openModal('auditModal')"}, {"t": "详情", "act": "go('../财务协同/开票详情.html?id=INV-20260826-011')"}, {"t": "查看账单", "act": "go('../财务协同/应收账单.html')"}, {"t": "收款", "act": "go('../财务协同/收款登记.html')"}]},
      title: '开票登记详情',
      info: [
        { label: '登记单号', text: 'INV-20260826-011', full: true },
        { label: '状态', tag: '已登记' },
        { label: '开票日期', text: '2026-08-26' },
        { label: '发票号码', text: '26119800420988' },
        { label: '发票类型', text: '增值税专用发票' },
        { label: '购方', text: '东海商用宁波分公司', full: true },
        { label: '关联应收', text: 'AR-2026-07-PRJ2602', url: '财务协同/应收账单.html' },
        { label: '价税合计', text: '186,200.00 元' },
        { label: '税率', text: '13%' },
        { label: '登记人', text: '财务-周敏' },
        { label: '备注', text: '—' }
      ],
      feeCols: ['费用项', '关联账单', '税率', '开票金额(元)'],
      fees: [
        { cells: ['租赁费 · 2026-07', 'AR-2026-07-PRJ2602', '13%', '186,200.00'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-07-PRJ2602', url: '财务协同/应收账单.html' },
        { role: '开票登记（本单）', name: 'INV-20260826-011', self: true },
        { role: '收款登记', name: 'HK-20260828-013', url: '财务协同/收款登记.html' },
        { role: '银行回单核销', name: 'SD-20260828-010', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '07-31', text: '应收账单汇总 · AR-2026-07-PRJ2602', who: '系统' },
        { t: '08-26 15:10', text: '开票登记 · 发票号码 26119800420988', who: '财务-周敏' },
        { t: '—', text: '待收款 → 银行回单核销', off: true }
      ]
    },
    'INV-20260820-010': {
      'row': {"fields": {"no": "26119800419501", "itype": "专票", "buyer": "华骏重卡汽车有限公司", "ref": "AR-2026-07-PRJ2601", "date": "2026-08-20", "status": "已登记"}, "cells": ["26119800419501", "<span class=\"tag tag-blue\">专票</span>", "华骏重卡汽车有限公司", "AR-2026-07-PRJ2601", "<span class=\"td-num\"><b>256,600.00</b></span>", "13%", "2026-08-20", "<span class=\"tag tag-green\">已登记</span>"], "ops": [{"t": "开票确认", "act": "openModal('auditModal')"}, {"t": "详情", "act": "go('../财务协同/开票详情.html?id=INV-20260820-010')"}, {"t": "查看账单", "act": "go('../财务协同/应收账单.html')"}, {"t": "收款", "act": "go('../财务协同/收款登记.html')"}]},
      title: '开票登记详情',
      info: [
        { label: '登记单号', text: 'INV-20260820-010', full: true },
        { label: '状态', tag: '已登记' },
        { label: '开票日期', text: '2026-08-20' },
        { label: '发票号码', text: '26119800419501' },
        { label: '发票类型', text: '增值税专用发票' },
        { label: '购方', text: '华骏重卡汽车有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-07-PRJ2601', url: '财务协同/应收账单.html' },
        { label: '价税合计', text: '256,600.00 元' },
        { label: '税率', text: '13%' },
        { label: '登记人', text: '财务-周敏' },
        { label: '备注', text: '—' }
      ],
      feeCols: ['费用项', '关联账单', '税率', '开票金额(元)'],
      fees: [
        { cells: ['租赁费 · 2026-07', 'AR-2026-07-PRJ2601', '13%', '256,600.00'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-07-PRJ2601', url: '财务协同/应收账单.html' },
        { role: '开票登记（本单）', name: 'INV-20260820-010', self: true },
        { role: '收款登记', name: 'HK-20260825-012', url: '财务协同/收款登记.html' },
        { role: '银行回单核销', name: 'SD-20260825-009 · 部分核销', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '07-31', text: '应收账单汇总 · AR-2026-07-PRJ2601', who: '系统' },
        { t: '08-20 11:25', text: '开票登记 · 发票号码 26119800419501', who: '财务-周敏' },
        { t: '—', text: '待收款 → 银行回单核销', off: true }
      ]
    },
    'INV-20260815-009': {
      'row': {"fields": {"no": "26119800418233", "itype": "普票", "buyer": "星途新能源汽车科技有限公司", "ref": "AR-2026-07-PRJ2603", "date": "2026-08-15", "status": "已登记"}, "cells": ["26119800418233", "<span class=\"tag tag-gray\">普票</span>", "星途新能源汽车科技有限公司", "AR-2026-07-PRJ2603", "<span class=\"td-num\"><b>98,000.00</b></span>", "13%", "2026-08-15", "<span class=\"tag tag-green\">已登记</span>"], "ops": [{"t": "开票确认", "act": "openModal('auditModal')"}, {"t": "详情", "act": "go('../财务协同/开票详情.html?id=INV-20260815-009')"}, {"t": "查看账单", "act": "go('../财务协同/应收账单.html')"}, {"t": "收款", "act": "go('../财务协同/收款登记.html')"}]},
      title: '开票登记详情',
      info: [
        { label: '登记单号', text: 'INV-20260815-009', full: true },
        { label: '状态', tag: '已登记' },
        { label: '开票日期', text: '2026-08-15' },
        { label: '发票号码', text: '26119800418233' },
        { label: '发票类型', text: '增值税普通发票' },
        { label: '购方', text: '星途新能源汽车科技有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-07-PRJ2603', url: '财务协同/应收账单.html' },
        { label: '价税合计', text: '98,000.00 元' },
        { label: '税率', text: '13%' },
        { label: '登记人', text: '财务-周敏' },
        { label: '备注', text: '—' }
      ],
      feeCols: ['费用项', '关联账单', '税率', '开票金额(元)'],
      fees: [
        { cells: ['租赁费 · 2026-07', 'AR-2026-07-PRJ2603', '13%', '98,000.00'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-07-PRJ2603', url: '财务协同/应收账单.html' },
        { role: '开票登记（本单）', name: 'INV-20260815-009', self: true },
        { role: '收款登记', name: 'HK-20260822-011', url: '财务协同/收款登记.html' },
        { role: '银行回单核销', name: 'SD-20260822-008 · 已核销', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '07-31', text: '应收账单汇总 · AR-2026-07-PRJ2603', who: '系统' },
        { t: '08-15 10:05', text: '开票登记 · 发票号码 26119800418233', who: '财务-周敏' },
        { t: '08-28 10:05', text: '收款 65,320.00 已核销 · 余款待收', who: '李婧' }
      ]
    },
    'INV-20260802-008': {
      'row': {"fields": {"no": "26119800417077", "itype": "专票", "buyer": "华骏重卡汽车有限公司", "ref": "AR-2026-06-PRJ2601", "date": "2026-08-02", "status": "停用"}, "cells": ["26119800417077", "<span class=\"tag tag-blue\">专票</span>", "华骏重卡汽车有限公司", "AR-2026-06-PRJ2601", "<span class=\"td-num\"><b>442,800.00</b></span>", "13%", "2026-08-02", "<span class=\"tag tag-gray\">停用</span>"], "ops": [{"t": "开票确认", "act": "openModal('auditModal')"}, {"t": "详情", "act": "go('../财务协同/开票详情.html?id=INV-20260802-008')"}, {"t": "查看账单", "act": "go('../财务协同/应收账单.html')"}, {"t": "收款", "act": "go('../财务协同/收款登记.html')"}]},
      title: '开票登记详情',
      info: [
        { label: '登记单号', text: 'INV-20260802-008', full: true },
        { label: '状态', tag: '停用' },
        { label: '开票日期', text: '2026-08-02' },
        { label: '发票号码', text: '26119800417077' },
        { label: '发票类型', text: '增值税专用发票' },
        { label: '购方', text: '华骏重卡汽车有限公司', full: true },
        { label: '关联应收', text: 'AR-2026-06-PRJ2601', url: '财务协同/应收账单.html' },
        { label: '价税合计', text: '442,800.00 元' },
        { label: '税率', text: '13%' },
        { label: '登记人', text: '财务-周敏' },
        { label: '备注', text: '—' }
      ],
      feeCols: ['费用项', '关联账单', '税率', '开票金额(元)'],
      fees: [
        { cells: ['租赁费 · 2026-06', 'AR-2026-06-PRJ2601', '13%', '442,800.00'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '应收账单', name: 'AR-2026-06-PRJ2601', url: '财务协同/应收账单.html' },
        { role: '开票登记（本单）', name: 'INV-20260802-008 · 已停用', self: true },
        { role: '收款 / 核销', name: '已于 08 月核销结清', url: '财务协同/银行回单核销.html' }
      ],
      timeline: [
        { t: '06-30', text: '应收账单汇总 · AR-2026-06-PRJ2601', who: '系统' },
        { t: '08-02 09:50', text: '开票登记 · 发票号码 26119800417077', who: '财务-周敏' },
        { t: '08-22 09:30', text: '收款核销 358,900.00 元', who: '李婧' },
        { t: '09-01 14:00', text: '登记停用 · 重复登记作废（保留痕迹）', who: '财务-周敏' }
      ]
    }
  },

  /* 银行回单核销记录（键 = HX 核销单号；弹窗按银行回单维度展示，titleNo = SD 银行回单号） */
  writeoffs: {
    'HX-20260830-012': {
      'row': {"fields": {"sd": "SD-20260825-009", "ref": "AR-2026-07-PRJ2601", "status": "部分核销", "time": "2026-08-30 14:22", "who": "李婧"}, "cells": ["SD-20260825-009", "AR-2026-07-PRJ2601", "<span class=\"td-num\"><b>60,000.00</b></span>", "<span class=\"tag tag-blue\">部分核销</span>", "2026-08-30 14:22", "李婧"], "ops": [{"t": "详情", "act": "go('../财务协同/银行回单核销详情.html?id=HX-20260830-012')"}, {"t": "撤销核销", "act": "openModal('undoModal')"}]},
      title: '银行回单核销详情', titleNo: 'SD-20260825-009',
      info: [
        { label: '银行回单号', text: 'SD-20260825-009', full: true },
        { label: '状态', tag: '部分核销' },
        { label: '到账日期', text: '2026-08-25' },
        { label: '付款方', text: '华骏重卡汽车有限公司', full: true },
        { label: '到账金额', text: '98,000.00 元' },
        { label: '已核销', text: '60,000.00 元' },
        { label: '未核销', text: '38,000.00 元' },
        { label: '关联收款', text: 'HK-20260825-012', url: '财务协同/收款登记.html' },
        { label: '收款账户', text: '招行基本户 1209****8866' },
        { label: '经办', text: '李婧' }
      ],
      feeCols: ['勾对', '应收账单', '账单金额(元)', '本次核销(元)'],
      fees: [
        { cells: ['☑', 'AR-2026-07-PRJ2601', '442,800.00', '60,000.00（部分核销）'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '收款登记', name: 'HK-20260825-012', url: '财务协同/收款登记.html' },
        { role: '银行回单核销（本单）', name: 'SD-20260825-009', self: true },
        { role: '应收账单', name: 'AR-2026-07-PRJ2601 · 核销冲抵', url: '财务协同/应收账单.html' }
      ],
      timeline: [
        { t: '08-25', text: '银行回单接收 · 与收款登记匹配', who: '系统' },
        { t: '08-30 14:22', text: '勾对核销 60,000.00 元 · 部分核销', who: '李婧' },
        { t: '—', text: '余 38,000.00 待后续核销 / 可撤销核销', off: true }
      ]
    },
    'HX-20260828-011': {
      'row': {"fields": {"sd": "SD-20260822-008", "ref": "AR-2026-07-PRJ2603", "status": "已核销", "time": "2026-08-28 10:05", "who": "李婧"}, "cells": ["SD-20260822-008", "AR-2026-07-PRJ2603", "<span class=\"td-num\"><b>65,320.00</b></span>", "<span class=\"tag tag-green\">已核销</span>", "2026-08-28 10:05", "李婧"], "ops": [{"t": "详情", "act": "go('../财务协同/银行回单核销详情.html?id=HX-20260828-011')"}, {"t": "撤销核销", "act": "openModal('undoModal')"}]},
      title: '银行回单核销详情', titleNo: 'SD-20260822-008',
      info: [
        { label: '银行回单号', text: 'SD-20260822-008', full: true },
        { label: '状态', tag: '已核销' },
        { label: '到账日期', text: '2026-08-22' },
        { label: '付款方', text: '星途新能源汽车科技有限公司', full: true },
        { label: '到账金额', text: '65,320.00 元' },
        { label: '已核销', text: '65,320.00 元' },
        { label: '未核销', text: '0.00 元' },
        { label: '关联收款', text: 'HK-20260822-011', url: '财务协同/收款登记.html' },
        { label: '收款账户', text: '工行一般户 0200****5533' },
        { label: '经办', text: '李婧' }
      ],
      feeCols: ['勾对', '应收账单', '账单金额(元)', '本次核销(元)'],
      fees: [
        { cells: ['☑', 'AR-2026-07-PRJ2603', '241,500.00', '65,320.00（全额核销）'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '收款登记', name: 'HK-20260822-011', url: '财务协同/收款登记.html' },
        { role: '银行回单核销（本单）', name: 'SD-20260822-008', self: true },
        { role: '应收账单', name: 'AR-2026-07-PRJ2603 · 核销冲抵', url: '财务协同/应收账单.html' }
      ],
      timeline: [
        { t: '08-22', text: '银行回单接收 · 与收款登记匹配', who: '系统' },
        { t: '08-28 10:05', text: '勾对核销 65,320.00 元 · 全额核销', who: '李婧' }
      ]
    },
    'HX-20260826-010': {
      'row': {"fields": {"sd": "SD-20260818-006", "ref": "BS-20260802-001", "status": "已核销", "time": "2026-08-26 16:40", "who": "李婧"}, "cells": ["SD-20260818-006", "BS-20260802-001", "<span class=\"td-num\"><b>860.00</b></span>", "<span class=\"tag tag-green\">已核销</span>", "2026-08-26 16:40", "李婧"], "ops": [{"t": "详情", "act": "go('../财务协同/银行回单核销详情.html?id=HX-20260826-010')"}, {"t": "撤销核销", "act": "openModal('undoModal')"}]},
      title: '银行回单核销详情', titleNo: 'SD-20260818-006',
      info: [
        { label: '银行回单号', text: 'SD-20260818-006', full: true },
        { label: '状态', tag: '已核销' },
        { label: '到账日期', text: '2026-08-18' },
        { label: '付款方', text: '华骏重卡汽车有限公司', full: true },
        { label: '到账金额', text: '860.00 元' },
        { label: '已核销', text: '860.00 元' },
        { label: '未核销', text: '0.00 元' },
        { label: '关联收款', text: 'HK-20260818-010', url: '财务协同/收款登记.html' },
        { label: '收款账户', text: '招行基本户 1209****8866' },
        { label: '经办', text: '李婧' }
      ],
      feeCols: ['勾对', '来源单据', '单据金额(元)', '本次核销(元)'],
      fees: [
        { cells: ['☑', 'BS-20260802-001（丢损赔偿）', '860.00', '860.00（全额核销）'] }
      ],
      chain: [
        { role: '收款登记', name: 'HK-20260818-010', url: '财务协同/收款登记.html' },
        { role: '银行回单核销（本单）', name: 'SD-20260818-006', self: true },
        { role: '丢损赔偿单', name: 'BS-20260802-001 · 核销冲抵' }
      ],
      timeline: [
        { t: '08-18', text: '银行回单接收 · 与收款登记匹配', who: '系统' },
        { t: '08-26 16:40', text: '勾对核销 860.00 元 · 全额核销', who: '李婧' }
      ]
    },
    'HX-20260822-009': {
      'row': {"fields": {"sd": "SD-20260815-005", "ref": "AR-2026-06-PRJ2602", "status": "已核销", "time": "2026-08-22 09:30", "who": "李婧"}, "cells": ["SD-20260815-005", "AR-2026-06-PRJ2602", "<span class=\"td-num\"><b>358,900.00</b></span>", "<span class=\"tag tag-green\">已核销</span>", "2026-08-22 09:30", "李婧"], "ops": [{"t": "详情", "act": "go('../财务协同/银行回单核销详情.html?id=HX-20260822-009')"}, {"t": "撤销核销", "act": "openModal('undoModal')"}]},
      title: '银行回单核销详情', titleNo: 'SD-20260815-005',
      info: [
        { label: '银行回单号', text: 'SD-20260815-005', full: true },
        { label: '状态', tag: '已核销' },
        { label: '到账日期', text: '2026-08-15' },
        { label: '付款方', text: '东海商用宁波分公司', full: true },
        { label: '到账金额', text: '358,900.00 元' },
        { label: '已核销', text: '358,900.00 元' },
        { label: '未核销', text: '0.00 元' },
        { label: '关联收款', text: '—' },
        { label: '收款账户', text: '建行一般户 3321****0417' },
        { label: '经办', text: '李婧' }
      ],
      feeCols: ['勾对', '应收账单', '账单金额(元)', '本次核销(元)'],
      fees: [
        { cells: ['☑', 'AR-2026-06-PRJ2602', '358,900.00', '358,900.00（全额核销）'], links: { 1: '财务协同/应收账单.html' } }
      ],
      chain: [
        { role: '银行回单核销（本单）', name: 'SD-20260815-005', self: true },
        { role: '应收账单', name: 'AR-2026-06-PRJ2602 · 核销冲抵结清', url: '财务协同/应收账单.html' }
      ],
      timeline: [
        { t: '08-15', text: '银行回单接收 · 到账 358,900.00 元', who: '系统' },
        { t: '08-22 09:30', text: '勾对核销 358,900.00 元 · 全额核销结清', who: '李婧' }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 租赁单 leaseOrders：键 = ZL 租赁单号（租赁管理/租赁单列表.html 9 行全量） */
  /* 租金标准 8.00 元/套/日为默认决策待确认；押金口径待客户 */
  leaseOrders: {
    'ZL-20260823-033': {
      'row': {"fields": {"billing": "按月定期", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2604", "status": "已退租", "start": "2026-08-23"}, "note": "1", "cells": ["华骏重卡汽车有限公司", "PRJ-2604", "ZH-2604-D 混合组合套件", "<span class=\"tag tag-orange\">混合（自购 + 租入）</span> <span class=\"lk\" onclick=\"go('../租入管理/租入单列表.html')\">RZD-20260815-005</span>", "<span class=\"td-num\">40 套</span>", "2026-08-23", "<span class=\"td-num\">40/40 套</span>", "<span class=\"tag tag-green\">已退租</span>"], "ops": [{"t": "退回对比", "act": "openModal('cmpModal')"}, {"t": "编辑", "act": "go('../租赁管理/租赁单新建.html')"}, {"t": "审核", "act": "go('../租赁管理/租赁单审核.html?id=ZL-20260823-033')"}, {"t": "关闭"}]},
      'title': '租赁单详情',
      'formTitle': '租赁信息',
      'formRows': [
        { 'label': '租赁单号', 'text': 'ZL-20260823-033' },
        { 'label': '状态', 'tag': '已退租' },
        { 'label': '客户', 'text': '华骏重卡汽车有限公司' },
        { 'label': '单据类型', 'text': '—' },
        { 'label': '所属项目', 'text': 'PRJ-2604' },
        { 'label': '建单日期', 'text': '—' },
        { 'label': '押金', 'text': '—（商务口径待客户确认）', 'full': true },
        { 'label': '起租日期', 'text': '2026-08-23' },
        { 'label': '计费方式', 'text': '按月定期生成应收（默认）' },
        { 'label': '备注', 'text': '—' },
        { 'label': '资产来源', 'text': '混合（自购 + 租入）· RZD-20260815-005', 'url': '租入管理/租入单列表.html', 'full': true },
        { 'label': '退回进度', 'text': '40/40 套' },
        { 'label': '计租天数', 'text': '92 天' },
        { 'label': '租金标准', 'text': '8.00 元 / 套 / 日（默认决策待确认）', 'full': true },
        { 'label': '业务员', 'text': '沈婷' }
      ],
      'itemTitle': '租赁明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'ZH-2604-D', '混合组合套件', '—', '套', '40', '按月定期', '8.00', '13%', '9.04', '361.60']
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
          'role': '租赁出库',
          'name': 'CK-20260824-009',
          'url': '租赁管理/租赁出库列表.html'
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
          'who': '沈婷'
        },
        {
          't': '08-24',
          'text': '租赁出库 · CK-20260824-009（40 套）',
          'who': '张帆'
        },
        {
          't': '09-02',
          'text': '客户退租 · TZRK-20260902-010（直接入库·提前退租）',
          'who': '客户提交'
        },
        {
          't': '09-02',
          'text': '退租入库 · TZRK-20260902-010（按 BOM 拆散分流）',
          'who': '张帆'
        }
      ]
    },
    'ZL-20260901-032': {
      'row': {"fields": {"billing": "按月定期", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "status": "待审核", "start": "2026-09-05"}, "cells": ["华骏重卡汽车有限公司", "PRJ-2601", "ZH-2601-A 驾驶室围板箱整箱套件", "<span class=\"tag tag-gray\">自有</span>", "<span class=\"td-num\">180 套</span>", "2026-09-05", "<span class=\"td-num\">—</span>", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "退回对比", "act": "openModal('cmpModal')"}, {"t": "编辑", "act": "go('../租赁管理/租赁单新建.html')"}, {"t": "审核", "act": "go('../租赁管理/租赁单审核.html?id=ZL-20260901-032')"}, {"t": "关闭"}]},
      'title': '租赁单详情',
      'formTitle': '租赁信息',
      'formRows': [
        { 'label': '租赁单号', 'text': 'ZL-20260901-032' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '客户', 'text': '华骏重卡汽车有限公司' },
        { 'label': '单据类型', 'text': '—' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '建单日期', 'text': '—' },
        { 'label': '押金', 'text': '—（商务口径待客户确认）', 'full': true },
        { 'label': '起租日期', 'text': '2026-09-05' },
        { 'label': '计费方式', 'text': '按月定期生成应收（默认）' },
        { 'label': '备注', 'text': '—' },
        { 'label': '资产来源', 'text': '自有' },
        { 'label': '退回进度', 'text': '—' },
        { 'label': '计租天数', 'text': '91 天' },
        { 'label': '租金标准', 'text': '8.00 元 / 套 / 日（默认决策待确认）', 'full': true },
        { 'label': '业务员', 'text': '沈婷' }
      ],
      'itemTitle': '租赁明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'ZH-2601-A', '驾驶室围板箱整箱套件', '—', '套', '180', '按月定期', '8.00', '13%', '9.04', '1,627.20']
      ],
      'chain': [
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260901-032 · 待审核',
          'self': true
        },
        {
          'role': '租赁出库',
          'name': '审核通过后出库',
          'url': '租赁管理/租赁出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-01',
          'text': '租赁单提交 · 待审核',
          'who': '沈婷'
        },
        {
          't': '—',
          'text': '审核通过 → 租赁出库 · 09-05 起租',
          'who': '系统',
          'off': true
        }
      ]
    },
    'ZL-20260828-031': {
      'row': {"fields": {"billing": "按月定期", "customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2602", "status": "已审核", "start": "2026-09-01"}, "note": "3", "cells": ["东海商用汽车有限公司宁波分公司", "PRJ-2602", "ZH-2602-B 冲压件料箱组套", "<span class=\"tag tag-gray\">自有</span>", "<span class=\"td-num\">120 套</span>", "2026-09-01", "<span class=\"td-num\">0/120 套</span>", "<span class=\"tag tag-blue\">已审核</span>"], "ops": [{"t": "退回对比", "act": "openModal('cmpModal')"}, {"t": "出库", "act": "go('../租赁管理/租赁出库列表.html')"}, {"t": "详情", "act": "go('../租赁管理/租赁单详情.html?id=ZL-20260828-031')"}, {"t": "关闭"}]},
      'title': '租赁单详情',
      'formTitle': '租赁信息',
      'formRows': [
        { 'label': '租赁单号', 'text': 'ZL-20260828-031' },
        { 'label': '状态', 'tag': '已审核' },
        { 'label': '客户', 'text': '东海商用汽车有限公司宁波分公司' },
        { 'label': '单据类型', 'text': '—' },
        { 'label': '所属项目', 'text': 'PRJ-2602' },
        { 'label': '建单日期', 'text': '—' },
        { 'label': '押金', 'text': '—（商务口径待客户确认）', 'full': true },
        { 'label': '起租日期', 'text': '2026-09-01' },
        { 'label': '计费方式', 'text': '按月定期生成应收（默认）' },
        { 'label': '备注', 'text': '—' },
        { 'label': '资产来源', 'text': '自有' },
        { 'label': '退回进度', 'text': '0/120 套' },
        { 'label': '计租天数', 'text': '90 天' },
        { 'label': '租金标准', 'text': '8.00 元 / 套 / 日（默认决策待确认）', 'full': true },
        { 'label': '业务员', 'text': '沈婷' }
      ],
      'itemTitle': '租赁明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'ZH-2602-B', '冲压件料箱组套', '—', '套', '120', '按月定期', '8.00', '13%', '9.04', '1,084.80']
      ],
      'chain': [
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260828-031 · 已审核',
          'self': true
        },
        {
          'role': '租赁出库',
          'name': 'CK-20260830-014 · 拣货中',
          'url': '租赁管理/租赁出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-28',
          'text': '租赁单签订',
          'who': '沈婷'
        },
        {
          't': '08-29',
          'text': '审核通过',
          'who': '张帆'
        },
        {
          't': '—',
          'text': '拣货中 · CK-20260830-014 出库确认后起租',
          'who': '张帆',
          'off': true
        }
      ]
    },
    'ZL-20260816-029': {
      'row': {"fields": {"billing": "按次套数", "customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2603", "status": "已退租", "start": "2026-08-16"}, "note": "2", "cells": ["东海商用汽车有限公司宁波分公司", "PRJ-2603", "WBX-1210L 围板箱 1200×1000×970", "<span class=\"tag tag-orange\">租入</span> <span class=\"lk\" onclick=\"go('../租入管理/租入单列表.html')\">RZD-20260815-003</span>", "<span class=\"td-num\">30 只</span>", "2026-08-16", "<span class=\"td-num\">30/30 只</span>", "<span class=\"tag tag-green\">已退租</span>"], "ops": [{"t": "退回对比", "act": "openModal('cmpModal')"}, {"t": "详情", "act": "go('../租赁管理/租赁单详情.html?id=ZL-20260816-029')"}, {"t": "退租入库", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '租赁单详情',
      'formTitle': '租赁信息',
      'formRows': [
        { 'label': '租赁单号', 'text': 'ZL-20260816-029' },
        { 'label': '状态', 'tag': '已退租' },
        { 'label': '客户', 'text': '东海商用汽车有限公司宁波分公司' },
        { 'label': '单据类型', 'text': '—' },
        { 'label': '所属项目', 'text': 'PRJ-2603' },
        { 'label': '建单日期', 'text': '—' },
        { 'label': '押金', 'text': '—（商务口径待客户确认）', 'full': true },
        { 'label': '起租日期', 'text': '2026-08-16' },
        { 'label': '计费方式', 'text': '按次套数对账（验收后按套数生成应收）' },
        { 'label': '备注', 'text': '—' },
        { 'label': '资产来源', 'text': '租入 · RZD-20260815-003', 'url': '租入管理/租入单列表.html', 'full': true },
        { 'label': '退回进度', 'text': '30/30 只' },
        { 'label': '计租天数', 'text': '92 天' },
        { 'label': '租金标准', 'text': '8.00 元 / 套 / 日（默认决策待确认）', 'full': true },
        { 'label': '业务员', 'text': '沈婷' }
      ],
      'itemTitle': '租赁明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '30', '按次套数', '8.00', '13%', '9.04', '271.20']
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260815-003',
          'url': '租入管理/租入单列表.html'
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
          'url': '租入管理/租入归还列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-15',
          'text': '租入单签订 · RZD-20260815-003 计租开始',
          'who': '周志远'
        },
        {
          't': '08-16',
          'text': '转租客户 · 起租',
          'who': '沈婷'
        },
        {
          't': '09-03',
          'text': '客户退租 · TZRK-20260903-009（直接入库·整箱退回）',
          'who': '客户提交'
        },
        {
          't': '09-03',
          'text': '退租入库 · TZRK-20260903-009 · 租入件转归还',
          'who': '张帆'
        },
        {
          't': '09-03',
          'text': '整退归还环通 · GHCK-20260903-001',
          'who': '林国栋'
        }
      ]
    },
    'ZL-20260815-028': {
      'row': {"fields": {"billing": "按月定期", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "status": "在租", "start": "2026-08-20"}, "note": "5", "cells": ["华骏重卡汽车有限公司", "PRJ-2601", "WBX-1210L 围板箱 1200×1000×970", "<span class=\"tag tag-orange\">租入</span> <span class=\"lk\" onclick=\"go('../租入管理/租入单列表.html')\">RZD-20260815-003</span>", "<span class=\"td-num\">300 只</span>", "2026-08-20", "<span class=\"td-num\">0/300 只</span>", "<span class=\"tag tag-blue\">在租</span>"], "ops": [{"t": "退回对比", "act": "openModal('cmpModal')"}, {"t": "出库", "act": "go('../租赁管理/租赁出库列表.html')"}, {"t": "详情", "act": "go('../租赁管理/租赁单详情.html?id=ZL-20260815-028')"}, {"t": "退租入库", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '租赁单详情',
      'formTitle': '租赁信息',
      'formRows': [
        { 'label': '租赁单号', 'text': 'ZL-20260815-028' },
        { 'label': '状态', 'tag': '在租' },
        { 'label': '客户', 'text': '华骏重卡汽车有限公司' },
        { 'label': '单据类型', 'text': '—' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '建单日期', 'text': '—' },
        { 'label': '押金', 'text': '—（商务口径待客户确认）', 'full': true },
        { 'label': '起租日期', 'text': '2026-08-20' },
        { 'label': '计费方式', 'text': '按月定期生成应收（默认）' },
        { 'label': '备注', 'text': '—' },
        { 'label': '资产来源', 'text': '租入 · RZD-20260815-003', 'url': '租入管理/租入单列表.html', 'full': true },
        { 'label': '退回进度', 'text': '0/300 只' },
        { 'label': '计租天数', 'text': '92 天' },
        { 'label': '租金标准', 'text': '8.00 元 / 套 / 日（默认决策待确认）', 'full': true },
        { 'label': '业务员', 'text': '沈婷' }
      ],
      'itemTitle': '租赁明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '300', '按月定期', '8.00', '13%', '9.04', '2,712.00']
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260815-003',
          'url': '租入管理/租入单列表.html'
        },
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260815-028',
          'self': true
        },
        {
          'role': '租赁出库',
          'name': 'CK-20260828-010',
          'url': '租赁管理/租赁出库列表.html'
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
          'who': '周志远'
        },
        {
          't': '08-20',
          'text': '起租 · 租赁单签订',
          'who': '沈婷'
        },
        {
          't': '08-28',
          'text': '租赁出库 · CK-20260828-010（200 套）',
          'who': '张帆'
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
      'row': {"fields": {"billing": "按月定期", "customer": "星途新能源汽车科技有限公司", "project": "PRJ-2603", "status": "在租", "start": "2026-07-25"}, "cells": ["星途新能源汽车科技有限公司", "PRJ-2603", "ZH-2603-C 电池托盘护角套件", "<span class=\"tag tag-gray\">自有</span>", "<span class=\"td-num\">60 套</span>", "2026-07-25", "<span class=\"td-num\">20/60 套</span>", "<span class=\"tag tag-blue\">在租</span>"], "ops": [{"t": "退回对比", "act": "openModal('cmpModal')"}, {"t": "出库", "act": "go('../租赁管理/租赁出库列表.html')"}, {"t": "详情", "act": "go('../租赁管理/租赁单详情.html?id=ZL-20260720-022')"}, {"t": "退租入库", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '租赁单详情',
      'formTitle': '租赁信息',
      'formRows': [
        { 'label': '租赁单号', 'text': 'ZL-20260720-022' },
        { 'label': '状态', 'tag': '在租' },
        { 'label': '客户', 'text': '星途新能源汽车科技有限公司' },
        { 'label': '单据类型', 'text': '—' },
        { 'label': '所属项目', 'text': 'PRJ-2603' },
        { 'label': '建单日期', 'text': '—' },
        { 'label': '押金', 'text': '—（商务口径待客户确认）', 'full': true },
        { 'label': '起租日期', 'text': '2026-07-25' },
        { 'label': '计费方式', 'text': '按月定期生成应收（默认）' },
        { 'label': '备注', 'text': '—' },
        { 'label': '资产来源', 'text': '自有' },
        { 'label': '退回进度', 'text': '20/60 套' },
        { 'label': '计租天数', 'text': '92 天' },
        { 'label': '租金标准', 'text': '8.00 元 / 套 / 日（默认决策待确认）', 'full': true },
        { 'label': '业务员', 'text': '沈婷' }
      ],
      'itemTitle': '租赁明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'ZH-2603-C', '电池托盘护角套件', '—', '套', '60', '按月定期', '8.00', '13%', '9.04', '542.40']
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
          'who': '沈婷'
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
      'row': {"fields": {"billing": "按次套数", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "status": "在租", "start": "2026-06-15"}, "cells": ["华骏重卡汽车有限公司", "PRJ-2601", "BTC-6040 料箱 600×400×340", "<span class=\"tag tag-gray\">自有</span>", "<span class=\"td-num\">500 只</span>", "2026-06-15", "<span class=\"td-num\">0/500 只</span>", "<span class=\"tag tag-blue\">在租</span>"], "ops": [{"t": "退回对比", "act": "openModal('cmpModal')"}, {"t": "出库", "act": "go('../租赁管理/租赁出库列表.html')"}, {"t": "详情", "act": "go('../租赁管理/租赁单详情.html?id=ZL-20260610-015')"}, {"t": "退租入库", "act": "go('../租赁管理/退租入库列表.html')"}]},
      'title': '租赁单详情',
      'formTitle': '租赁信息',
      'formRows': [
        { 'label': '租赁单号', 'text': 'ZL-20260610-015' },
        { 'label': '状态', 'tag': '在租' },
        { 'label': '客户', 'text': '华骏重卡汽车有限公司' },
        { 'label': '单据类型', 'text': '—' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '建单日期', 'text': '—' },
        { 'label': '押金', 'text': '—（商务口径待客户确认）', 'full': true },
        { 'label': '起租日期', 'text': '2026-06-15' },
        { 'label': '计费方式', 'text': '按次套数对账（验收后按套数生成应收）' },
        { 'label': '备注', 'text': '—' },
        { 'label': '资产来源', 'text': '自有' },
        { 'label': '退回进度', 'text': '0/500 只' },
        { 'label': '计租天数', 'text': '92 天' },
        { 'label': '租金标准', 'text': '8.00 元 / 套 / 日（默认决策待确认）', 'full': true },
        { 'label': '业务员', 'text': '沈婷' }
      ],
      'itemTitle': '租赁明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'BTC-6040', '料箱 600×400×340', '600×400×340 mm', '只', '500', '按次套数', '8.00', '13%', '9.04', '4,520.00']
      ],
      'chain': [
        {
          'role': '租赁单（本单）',
          'name': 'ZL-20260610-015',
          'self': true
        },
        {
          'role': '租赁出库',
          'name': 'CK-20260830-015（180 套）',
          'url': '租赁管理/租赁出库列表.html'
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
          'who': '沈婷'
        },
        {
          't': '08-26',
          'text': '客户退租 · TZRK-20260828-005（直接入库·退 200 只，部分退租）',
          'who': '客户提交'
        },
        {
          't': '08-28',
          'text': '退租入库 · TZRK-20260828-005（散件直接入库）',
          'who': '张帆'
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
      'row': {"fields": {"billing": "按月定期", "customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2602", "status": "已退租", "start": "2026-03-05"}, "note": "4", "cells": ["东海商用汽车有限公司宁波分公司", "PRJ-2602", "PLT-1210P 塑料托盘 1200×1000", "<span class=\"tag tag-gray\">自有（单一器具直接出租）</span>", "<span class=\"td-num\">400 块</span>", "2026-03-05", "<span class=\"td-num\">400/400 块</span>", "<span class=\"tag tag-green\">已退租</span>"], "ops": [{"t": "退回对比", "act": "openModal('cmpModal')"}, {"t": "详情", "act": "go('../租赁管理/租赁单详情.html?id=ZL-20260301-006')"}]},
      'title': '租赁单详情',
      'formTitle': '租赁信息',
      'formRows': [
        { 'label': '租赁单号', 'text': 'ZL-20260301-006' },
        { 'label': '状态', 'tag': '已退租' },
        { 'label': '客户', 'text': '东海商用汽车有限公司宁波分公司' },
        { 'label': '单据类型', 'text': '—' },
        { 'label': '所属项目', 'text': 'PRJ-2602' },
        { 'label': '建单日期', 'text': '—' },
        { 'label': '押金', 'text': '—（商务口径待客户确认）', 'full': true },
        { 'label': '起租日期', 'text': '2026-03-05' },
        { 'label': '计费方式', 'text': '按月定期生成应收（默认）' },
        { 'label': '备注', 'text': '—' },
        { 'label': '资产来源', 'text': '自有（单一器具直接出租）' },
        { 'label': '退回进度', 'text': '400/400 块' },
        { 'label': '计租天数', 'text': '92 天' },
        { 'label': '租金标准', 'text': '8.00 元 / 套 / 日（默认决策待确认）', 'full': true },
        { 'label': '业务员', 'text': '沈婷' }
      ],
      'itemTitle': '租赁明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'PLT-1210P', '塑料托盘 1200×1000', '1200×1000×150 mm', '块', '400', '按月定期', '8.00', '13%', '9.04', '3,616.00']
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
          'who': '沈婷'
        },
        {
          't': '08-23',
          'text': '客户退租 · TZRK-20260825-004（直接入库）',
          'who': '客户提交'
        },
        {
          't': '08-25',
          'text': '退租入库 · TZRK-20260825-004（散件直接入库）',
          'who': '张帆'
        }
      ]
    },
    'ZL-20260115-002': {
      'row': {"fields": {"billing": "按月定期", "customer": "长风汽车制造有限公司", "project": "PRJ-2604", "status": "已关闭", "start": "2026-01-20"}, "cells": ["长风汽车制造有限公司", "PRJ-2604", "WBX-1210M 围板箱 1200×1000×590", "<span class=\"tag tag-gray\">自有</span>", "<span class=\"td-num\">150 只</span>", "2026-01-20", "<span class=\"td-num\">150/150 只</span>", "<span class=\"tag tag-gray\">已关闭</span>"], "ops": [{"t": "退回对比", "act": "openModal('cmpModal')"}, {"t": "详情", "act": "go('../租赁管理/租赁单详情.html?id=ZL-20260115-002')"}]},
      'title': '租赁单详情',
      'formTitle': '租赁信息',
      'formRows': [
        { 'label': '租赁单号', 'text': 'ZL-20260115-002' },
        { 'label': '状态', 'tag': '已关闭' },
        { 'label': '客户', 'text': '长风汽车制造有限公司' },
        { 'label': '单据类型', 'text': '—' },
        { 'label': '所属项目', 'text': 'PRJ-2604' },
        { 'label': '建单日期', 'text': '—' },
        { 'label': '押金', 'text': '—（商务口径待客户确认）', 'full': true },
        { 'label': '起租日期', 'text': '2026-01-20' },
        { 'label': '计费方式', 'text': '按月定期生成应收（默认）' },
        { 'label': '备注', 'text': '—' },
        { 'label': '资产来源', 'text': '自有' },
        { 'label': '退回进度', 'text': '150/150 只' },
        { 'label': '计租天数', 'text': '90 天' },
        { 'label': '租金标准', 'text': '8.00 元 / 套 / 日（默认决策待确认）', 'full': true },
        { 'label': '业务员', 'text': '沈婷' }
      ],
      'itemTitle': '租赁明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'WBX-1210M', '围板箱 1200×1000×590', '1200×1000×590 mm', '只', '150', '按月定期', '8.00', '13%', '9.04', '1,356.00']
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
          'who': '沈婷'
        },
        {
          't': '02-02',
          'text': '单据关闭（客户取消）',
          'who': '沈婷'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 租入单 rentInOrders：键 = RZD 租入单号（租入管理/租入单列表.html 5 行全量） */
  /* 租金条款按月生成应付，已建应付实体单号贯通 */
  rentInOrders: {
    'RZD-20260815-003': {
      'row': {"fields": {"operator": "环通循环包装运营（上海）有限公司", "appliance": "围板箱 1200×1000×970", "period": "2026-08-15 ~ 2027-08-14", "status": "履行中", "agent": "周志远", "date": "2026-08-15"}, "note": "1", "cells": ["环通循环包装运营（上海）有限公司", "围板箱 1200×1000×970", "30 只", "400.00", "2026-08-15 ~ 2027-08-14", "36,000.00", "84,000.00", "<span class=\"tag tag-blue\">履行中</span>", "周志远", "2026-08-15 10:22"], "ops": [{"t": "详情", "act": "go('../租入管理/租入单详情.html?id=RZD-20260815-003')"}, {"t": "生成租金应付", "act": "go('../财务协同/应付账单.html')"}, {"t": "发起归还", "act": "go('../租入管理/租入归还列表.html')"}]},
      'returnItems': [{'item': 'WBX-1210L 围板箱 1200×1000×970', 'rentQty': 30, 'returned': 0, 'unit': '只'}],
      'title': '租入单详情',
      'formTitle': '租入信息',
      'formRows': [
        { 'label': '租入单号', 'text': 'RZD-20260815-003' },
        { 'label': '状态', 'tag': '履行中' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '环通循环包装运营（上海）有限公司' },
        { 'label': '起租日期', 'text': '2026-08-15' },
        { 'label': '止租日期', 'text': '2027-08-14' },
        { 'label': '计租天数', 'text': '365 天（合同期整期·止租当日仍计）' },
        { 'label': '押金', 'text': '84,000.00 元（商务口径待确认）', 'full': true },
        { 'label': '备注', 'text': '—' },
        { 'label': '月租', 'text': '1,350.00 元 / 月（按单 · 45.00 元/只×30）', 'full': true },
        { 'label': '已生成租金应付', 'text': 'AP-20260903-009 · 36,000.00 元', 'url': '财务协同/应付账单.html', 'full': true },
        { 'label': '经办人', 'text': '周志远' },
        { 'label': '创建时间', 'text': '2026-08-15 10:22' }
      ],
      'itemTitle': '租入明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '30', '月租', '400.00', '13%', '452.00', '36,000.00']
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
          'url': '租入管理/租入入库列表.html'
        },
        {
          'role': '租赁单（转租）',
          'name': 'ZL-20260816-029',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '租入归还',
          'name': 'GHCK-20260903-001',
          'url': '租入管理/租入归还列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-15',
          'text': '签订租入单 · 计租开始',
          'who': '周志远'
        },
        {
          't': '08-16',
          'text': '租入入库 · RZRK-20260816-021（30 只）',
          'who': '林国栋'
        },
        {
          't': '08-16',
          'text': '转租客户 · ZL-20260816-029',
          'who': '沈婷'
        },
        {
          't': '09-03',
          'text': '整退归还 · GHCK-20260903-001',
          'who': '林国栋'
        },
        {
          't': '09-03',
          'text': '生成租金应付 · AP-20260903-009（36,000 元）',
          'who': '系统'
        }
      ]
    },
    'RZD-20260815-005': {
      'row': {"fields": {"operator": "环通循环包装运营（上海）有限公司", "appliance": "围板箱 1200×1000×970", "period": "2026-08-15 ~ 2027-08-14", "status": "部分归还", "agent": "周志远", "date": "2026-08-15"}, "note": "2", "cells": ["环通循环包装运营（上海）有限公司", "围板箱 1200×1000×970", "10 只", "400.00", "2026-08-15 ~ 2027-08-14", "12,000.00", "12,000.00", "<span class=\"tag tag-orange\">部分归还</span>", "周志远", "2026-08-15 11:05"], "ops": [{"t": "详情", "act": "go('../租入管理/租入单详情.html?id=RZD-20260815-005')"}, {"t": "生成租金应付", "act": "go('../财务协同/应付账单.html')"}, {"t": "发起归还", "act": "go('../租入管理/租入归还列表.html')"}]},
      'returnItems': [{'item': 'WBX-1210L 围板箱 1200×1000×970', 'rentQty': 10, 'returned': 4, 'unit': '只'}],
      'title': '租入单详情',
      'formTitle': '租入信息',
      'formRows': [
        { 'label': '租入单号', 'text': 'RZD-20260815-005' },
        { 'label': '状态', 'tag': '部分归还' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '环通循环包装运营（上海）有限公司' },
        { 'label': '起租日期', 'text': '2026-08-15' },
        { 'label': '止租日期', 'text': '2027-08-14' },
        { 'label': '计租天数', 'text': '365 天（合同期整期·止租当日仍计）' },
        { 'label': '押金', 'text': '12,000.00 元（商务口径待确认）', 'full': true },
        { 'label': '备注', 'text': '—' },
        { 'label': '月租', 'text': '450.00 元 / 月（按单 · 45.00 元/只×10）', 'full': true },
        { 'label': '已生成租金应付', 'text': 'AP-20260903-010 · 12,000.00 元', 'url': '财务协同/应付账单.html', 'full': true },
        { 'label': '经办人', 'text': '周志远' },
        { 'label': '创建时间', 'text': '2026-08-15 11:05' }
      ],
      'itemTitle': '租入明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '10', '月租', '400.00', '13%', '452.00', '12,000.00']
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
          'url': '租入管理/租入入库列表.html'
        },
        {
          'role': '组装（混合配方）',
          'name': 'ZZ-20260822-006',
        },
        {
          'role': '租入归还（分流）',
          'name': 'GHCK-20260903-002 · 4 只缺损',
          'url': '租入管理/租入归还列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-15',
          'text': '签订租入单 · 计租开始',
          'who': '周志远'
        },
        {
          't': '08-16',
          'text': '租入入库 · RZRK-20260816-022（10 只）',
          'who': '林国栋'
        },
        {
          't': '08-22',
          'text': '混合组装 · ZZ-20260822-006（ZH-2604-D）',
          'who': '刘志强'
        },
        {
          't': '09-03',
          'text': '分流归还 · GHCK-20260903-002（10 只中 4 只缺损赔付）',
          'who': '林国栋'
        },
        {
          't': '09-03',
          'text': '生成租金应付 · AP-20260903-010（12,000 元）',
          'who': '系统'
        }
      ]
    },
    'RZD-20260902-008': {
      'row': {"fields": {"operator": "环通循环包装运营（上海）有限公司", "appliance": "塑料托盘 1200×1000", "period": "2026-09-02 ~ 2026-12-31", "status": "待审核", "agent": "陈锋", "date": "2026-09-02"}, "cells": ["环通循环包装运营（上海）有限公司", "塑料托盘 1200×1000", "50 只", "1.20", "2026-09-02 ~ 2026-12-31", "5,000.00", "—", "<span class=\"tag tag-orange\">待审核</span>", "陈锋", "2026-09-02 16:40"], "ops": [{"t": "详情", "act": "go('../租入管理/租入单详情.html?id=RZD-20260902-008')"}, {"t": "审核", "act": "go('../租入管理/租入单审核.html?id=RZD-20260902-008')"}]},
      'returnItems': [{'item': 'PLT-1210P 塑料托盘 1200×1000', 'rentQty': 60, 'returned': 0, 'unit': '块'}],
      'title': '租入单详情',
      'formTitle': '租入信息',
      'formRows': [
        { 'label': '租入单号', 'text': 'RZD-20260902-008' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '环通循环包装运营（上海）有限公司' },
        { 'label': '起租日期', 'text': '2026-09-02' },
        { 'label': '止租日期', 'text': '2026-12-31' },
        { 'label': '计租天数', 'text': '121 天（合同期整期·止租当日仍计）' },
        { 'label': '押金', 'text': '—' },
        { 'label': '备注', 'text': '—' },
        { 'label': '月租', 'text': '600.00 元 / 月（按单 · 12.00 元/块×50）', 'full': true },
        { 'label': '已生成租金应付', 'text': '—' },
        { 'label': '经办人', 'text': '陈锋' },
        { 'label': '创建时间', 'text': '2026-09-02 16:40' }
      ],
      'itemTitle': '租入明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'PLT-1210P', '塑料托盘 1200×1000', '1200×1000×150 mm', '块', '50', '月租', '12.00', '13%', '13.56', '678.00']
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
          'url': '租入管理/租入入库列表.html'
        },
        {
          'role': '租赁出库（立即转租·供应商直发）',
          'name': 'CK-20260914-023 · 待审核',
          'url': '租赁管理/租赁出库列表.html'
        },
      ],
      'timeline': [
        {
          't': '09-02',
          'text': '租入单提交 · 待审核',
          'who': '陈锋'
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
      'row': {"fields": {"operator": "环通循环包装运营（上海）有限公司", "appliance": "金属料箱 800×600", "period": "2026-07-01 ~ 2026-08-31", "status": "已归还", "agent": "周志远", "date": "2026-07-01"}, "cells": ["环通循环包装运营（上海）有限公司", "金属料箱 800×600", "20 只", "3.00", "2026-07-01 ~ 2026-08-31", "—", "10,800.00", "<span class=\"tag tag-green\">已归还</span>", "周志远", "2026-07-01 09:30"], "ops": [{"t": "详情", "act": "go('../租入管理/租入单详情.html?id=RZD-20260701-001')"}, {"t": "归还记录", "act": "go('../租入管理/租入归还列表.html')"}]},
      'title': '租入单详情',
      'formTitle': '租入信息',
      'formRows': [
        { 'label': '租入单号', 'text': 'RZD-20260701-001' },
        { 'label': '状态', 'tag': '已归还' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '环通循环包装运营（上海）有限公司' },
        { 'label': '起租日期', 'text': '2026-07-01' },
        { 'label': '止租日期', 'text': '2026-08-31' },
        { 'label': '计租天数', 'text': '62 天（合同期整期·止租当日仍计）' },
        { 'label': '押金', 'text': '10,800.00 元（商务口径待确认）', 'full': true },
        { 'label': '备注', 'text': '—' },
        { 'label': '月租', 'text': '200.00 元 / 月（按单 · 10.00 元/只×20）', 'full': true },
        { 'label': '已生成租金应付', 'text': '—' },
        { 'label': '经办人', 'text': '周志远' },
        { 'label': '创建时间', 'text': '2026-07-01 09:30' }
      ],
      'itemTitle': '租入明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', '—', '金属料箱 800×600', '800×600 mm', '只', '20', '月租', '10.00', '13%', '11.30', '226.00']
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
          'url': '租入管理/租入归还列表.html'
        }
      ],
      'timeline': [
        {
          't': '07-01',
          'text': '签订租入单 · 计租开始',
          'who': '周志远'
        },
        {
          't': '08-31',
          'text': '整退归还 · GHCK-20260831-003（20 只）',
          'who': '周志远'
        },
        {
          't': '08-31',
          'text': '租金结清 · 单据完结',
          'who': '系统'
        }
      ]
    },
    'RZD-20260615-002': {
      'row': {"fields": {"operator": "环通循环包装运营（上海）有限公司", "appliance": "塑料围板箱 800×600", "period": "2026-06-15 ~ 2026-08-14", "status": "已终止", "agent": "周志远", "date": "2026-06-15"}, "cells": ["环通循环包装运营（上海）有限公司", "塑料围板箱 800×600", "15 只", "2.50", "2026-06-15 ~ 2026-08-14", "—", "4,500.00", "<span class=\"tag tag-gray\">已终止</span>", "周志远", "2026-06-15 14:12"], "ops": [{"t": "详情", "act": "go('../租入管理/租入单详情.html?id=RZD-20260615-002')"}]},
      'title': '租入单详情',
      'formTitle': '租入信息',
      'formRows': [
        { 'label': '租入单号', 'text': 'RZD-20260615-002' },
        { 'label': '状态', 'tag': '已终止' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '环通循环包装运营（上海）有限公司' },
        { 'label': '起租日期', 'text': '2026-06-15' },
        { 'label': '止租日期', 'text': '2026-08-14' },
        { 'label': '计租天数', 'text': '61 天（合同期整期·止租当日仍计）' },
        { 'label': '押金', 'text': '4,500.00 元（商务口径待确认）', 'full': true },
        { 'label': '备注', 'text': '—' },
        { 'label': '月租', 'text': '150.00 元 / 月（按单 · 10.00 元/只×15）', 'full': true },
        { 'label': '已生成租金应付', 'text': '—' },
        { 'label': '经办人', 'text': '周志远' },
        { 'label': '创建时间', 'text': '2026-06-15 14:12' }
      ],
      'itemTitle': '租入明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', '—', '塑料围板箱 800×600', '800×600 mm', '只', '15', '月租', '10.00', '13%', '11.30', '169.50']
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
          'who': '周志远'
        },
        {
          't': '07-20',
          'text': '提前终止 · 按违约条款结算',
          'who': '周志远'
        }
      ]
    },
   'RZD-20260910-009': {
      'row': {"fields": {"operator": "供应商待选（背靠背自动生成）", "appliance": "WBX-1210L 围板箱 1200×1000×970", "period": "—", "status": "新建(草稿)", "agent": "系统", "date": "2026-09-10"}, "cells": ["供应商待选（背靠背自动生成）", "WBX-1210L 围板箱 1200×1000×970", "200 只", "—", "—", "0.00", "0.00", "<span class=\"tag tag-gray\">新建(草稿)</span>", "系统", "2026-09-10 20:30"], "ops": [{"t": "选供应商", "act": "showToast('已选供应商：环通循环包装运营（上海）有限公司 · 草稿待修改后提交')"}, {"t": "修改", "act": "showToast('草稿修改：器具/数量/租期可改，改后点提交进入待审核')"}, {"t": "提交", "act": "showToast('已提交审核 · RZD-20260910-009 → 待审核')"}]},
      'title': '租入单详情',
      'formTitle': '租入信息',
      'formRows': [
        { 'label': '租入单号', 'text': 'RZD-20260910-009' },
        { 'label': '状态', 'tag': '新建(草稿)' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '待选（来源：租赁单 ZL-20260910-036 审核确认背靠背自动生成）', 'full': true },
        { 'label': '起租日期', 'text': '—' },
        { 'label': '止租日期', 'text': '—' },
        { 'label': '计租天数', 'text': '—' },
        { 'label': '押金', 'text': '—' },
        { 'label': '备注', 'text': '—' },
        { 'label': '月租', 'text': '—' },
        { 'label': '已生成租金应付', 'text': '—' },
        { 'label': '经办人', 'text': '系统（自动生成）' },
        { 'label': '创建时间', 'text': '2026-09-10 20:30' }
      ],
      'itemTitle': '租入明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '计费方式', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '200', '月租', '—', '13%', '—', '—']
      ],
      'chain': [
        {'role': '租赁单（来源）', 'name': 'ZL-20260910-036 · 背靠背', 'url': '租赁管理/租赁单列表.html'},
        {'role': '租入单（本单·草稿）', 'name': 'RZD-20260910-009', 'self': true},
        {'role': '下一步', 'name': '选供应商 → 修改 → 提交审核'}
      ],
      'timeline': [
        {'t': '09-10', 'text': '租赁单审核确认 · 背靠背自动生成租入单草稿（供应商待选）', 'who': '系统'}
      ]
    },

  },

  /* -------------------------------------------------------------------------- */
  /* 租赁出库单 comboOutbounds：键 = CK 出库单号（租赁管理/租赁出库列表.html 8 行全量） */
  /* 关联租赁单/销售订单双关联；租入件无 SO 用 —（租赁出库） */
  comboOutbounds: {
    'CK-20260910-022': {
      'row': {"fields": {"project": "PRJ-2603", "customer": "东海商用宁波分公司", "zl": "ZL-20260910-040", "combo": "ZH-2603-B × 30 套", "mat": "ZH-2603-B", "matName": "冲压件料箱组套", "qty": "30", "unit": "套", "so": "—（租赁出库）", "addr": "宁波杭州湾基地", "status": "待审核", "date": "2026-09-10"}, "cells": ["PRJ-2603", "东海商用宁波分公司", "<span class=\"lk\">ZL-20260910-040</span>", "ZH-2603-B × 30 套", "—（租赁出库）", "宁波杭州湾基地", "<span class=\"tag tag-orange\">待审核</span>", "2026-09-10 15:20"], "ops": [{"t": "打印出货单", "act": "go('出货单打印.html?key=CK-20260910-022')"}, {"t": "详情", "act": "go('../租赁管理/租赁出库详情.html?id=CK-20260910-022')"}, {"t": "审核", "act": "go('../租赁管理/租赁出库确认.html?id=CK-20260910-022')"}]},
      'title': '租赁出库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'CK-20260910-022' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '所属项目', 'text': 'PRJ-2603' },
        { 'label': '关联租赁单', 'text': 'ZL-20260910-040', 'url': '租赁管理/租赁单列表.html' },
        { 'label': '关联销售订单', 'text': '—（租赁出库）' },
        { 'label': '客户（带出）', 'text': '东海商用宁波分公司' },
        { 'label': '出库类型', 'text': '一箱一件 · 逐件核对（扫码口预留）', 'full': true },
        { 'label': '出库库位', 'text': '成品区 RB' },
        { 'label': '收货地点', 'text': '宁波杭州湾基地' },
        { 'label': '要货日期', 'text': '—' },
        { 'label': '出库备注', 'text': '—' },
        { 'label': '制单人', 'text': '邵磊' },
        { 'label': '出库时间', 'text': '2026-09-10 15:20' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '组合件编码', '组合件名称', '计费方式', '出库数量', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)', '出库库位'],
      'items': [
        ['1', 'ZH-2603-B', '冲压件料箱组套', '按月定期', '30', '1.00', '13%', '1.13', '33.90', '成品区 RB']
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260910-040',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '租赁出库（本单）',
          'name': 'CK-20260910-022',
          'self': true
        },
        {
          'role': '库存查询·客户在租 / 应收',
          'name': '审核通过出库后起租',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '09-10 15:20',
          'text': '录单提交 · 待审核',
          'who': '邵磊'
        },
        {
          't': '—',
          'text': '审核通过后出库 · 起租计费',
          'who': '系统',
          'off': true
        }
      ]
    },

    'CK-20260914-023': {  /* G31 T6 立即转租溯源行（D-105·供应商直发） */
      'row': {"fields": {"project": "PRJ-2603", "customer": "东海商用宁波分公司", "zl": "—（立即转租生成）", "combo": "塑料托盘 1200×1000 × 50 只", "mat": "PLT-1210P", "matName": "塑料托盘 1200×1000", "qty": "50", "unit": "只", "so": "—（租赁出库·租入直发）", "addr": "宁波杭州湾基地", "status": "待审核", "date": "2026-09-14"}, "cells": ["PRJ-2603", "东海商用宁波分公司", "<span class=\"tag tag-orange\">租入直发（立即转租）</span>", "塑料托盘 1200×1000 × 50 只", "—（租赁出库·租入直发）", "宁波杭州湾基地", "<span class=\"tag tag-orange\">待审核</span>", "2026-09-14 10:05"], "ops": [{"t": "打印出货单", "act": "go('出货单打印.html?key=CK-20260914-023')"}, {"t": "详情", "act": "go('../租赁管理/租赁出库详情.html?id=CK-20260914-023')"}, {"t": "审核", "act": "go('../租赁管理/租赁出库确认.html?id=CK-20260914-023')"}]},
      'title': '租赁出库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'CK-20260914-023' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '所属项目', 'text': 'PRJ-2603' },
        { 'label': '关联租赁单', 'text': '—（立即转租生成）' },
        { 'label': '来源', 'text': '立即转租（租入入库登记时勾选·自动生成）', 'full': true },
        { 'label': '关联租入库', 'text': 'RZRK-20260903-023', 'url': '租入管理/租入入库列表.html' },
        { 'label': '关联租入单', 'text': 'RZD-20260902-008', 'url': '租入管理/租入单列表.html' },
        { 'label': '关联销售订单', 'text': '—（租赁出库·租入直发）' },
        { 'label': '客户（带出）', 'text': '东海商用宁波分公司' },
        { 'label': '出库库位', 'text': '—（供应商直发·不经实物入库）' },
        { 'label': '收货地点', 'text': '宁波杭州湾基地' },
        { 'label': '出库日期', 'text': '2026-09-14' },
        { 'label': '要货日期', 'text': '—' },
        { 'label': '出库备注', 'text': '—' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '组合件编码', '组合件名称', '计费方式', '出库数量', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)', '出库库位'],
      'items': [
        ['1', 'PLT-1210P', '塑料托盘 1200×1000', '按月定期', '50', '—', '13%', '—', '—', '—']
      ],
    },
    'CK-20260903-016': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "zl": "ZL-20260903-034", "combo": "ZH-2601-A × 60 套（退租回库件循环出库）", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "60", "unit": "套", "so": "—（租赁出库）", "addr": "长春基地一号门", "status": "已出库", "date": "2026-09-03"}, "cells": ["PRJ-2601", "华骏重卡汽车有限公司", "<span class=\"lk\">ZL-20260903-034</span>", "ZH-2601-A × 60 套（退租回库件循环出库）", "—（租赁出库）", "长春基地一号门", "<span class=\"tag tag-green\">已出库</span>", "2026-09-03 09:15"], "ops": [{"t": "详情", "act": "go('../租赁管理/租赁出库详情.html?id=CK-20260903-016')"}, {"t": "打印出货单", "act": "go('出货单打印.html?key=CK-20260903-016')"}, {"t": "审核", "act": "go('../租赁管理/租赁出库确认.html?id=CK-20260903-016')"}]},
      'title': '租赁出库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'CK-20260903-016' },
        { 'label': '状态', 'tag': '已出库' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '关联租赁单', 'text': 'ZL-20260903-034', 'url': '租赁管理/租赁单列表.html' },
        { 'label': '关联销售订单', 'text': '—（租赁出库）' },
        { 'label': '客户（带出）', 'text': '华骏重卡汽车有限公司' },
        { 'label': '出库类型', 'text': '一箱一件 · 逐件核对（扫码口预留）', 'full': true },
        { 'label': '出库库位', 'text': '成品区 RB' },
        { 'label': '收货地点', 'text': '长春基地一号门' },
        { 'label': '要货日期', 'text': '—' },
        { 'label': '出库备注', 'text': '—' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '出库时间', 'text': '2026-09-03 09:15' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '组合件编码', '组合件名称', '计费方式', '出库数量', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)', '出库库位'],
      'items': [
        ['1', 'ZH-2601-A', '驾驶室围板箱整箱套件', '按月定期', '60', '1.00', '13%', '1.13', '67.80', '成品区 RB']
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260903-034',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '租赁出库（本单）',
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
          'who': '张帆'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 长春基地一号门',
          'who': '张帆'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张帆'
        }
      ]
    },
    'CK-20260830-015': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "zl": "ZL-20260610-015", "combo": "ZH-2601-A × 180 套", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "180", "unit": "套", "so": "SO-20260830-0041", "addr": "长春基地一号门", "status": "已出库", "date": "2026-08-30"}, "note": "2", "cells": ["PRJ-2601", "华骏重卡汽车有限公司", "<span class=\"lk\">ZL-20260610-015</span>", "ZH-2601-A × 180 套", "SO-20260830-0041", "长春基地一号门", "<span class=\"tag tag-green\">已出库</span>", "2026-08-30 17:20"], "ops": [{"t": "详情", "act": "go('../租赁管理/租赁出库详情.html?id=CK-20260830-015')"}, {"t": "打印出货单", "act": "go('出货单打印.html?key=CK-20260830-015')"}, {"t": "审核", "act": "go('../租赁管理/租赁出库确认.html?id=CK-20260830-015')"}]},
      'title': '租赁出库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'CK-20260830-015' },
        { 'label': '状态', 'tag': '已出库' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '关联租赁单', 'text': 'ZL-20260610-015', 'url': '租赁管理/租赁单列表.html' },
        { 'label': '关联销售订单', 'text': 'SO-20260830-0041（双关联）', 'url': '销售管理/销售订单列表.html' },
        { 'label': '客户（带出）', 'text': '华骏重卡汽车有限公司' },
        { 'label': '出库类型', 'text': '一箱一件 · 逐件核对（扫码口预留）', 'full': true },
        { 'label': '出库库位', 'text': '成品区 RB' },
        { 'label': '收货地点', 'text': '长春基地一号门' },
        { 'label': '要货日期', 'text': '—' },
        { 'label': '出库备注', 'text': '—' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '出库时间', 'text': '2026-08-30 17:20' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '组合件编码', '组合件名称', '计费方式', '出库数量', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)', '出库库位'],
      'items': [
        ['1', 'ZH-2601-A', '驾驶室围板箱整箱套件', '按次套数', '180', '1.00', '13%', '1.13', '203.40', '成品区 RB']
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
          'role': '租赁出库（本单）',
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
          'who': '张帆'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 长春基地一号门',
          'who': '张帆'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张帆'
        }
      ]
    },
    'CK-20260830-014': {
      'row': {"fields": {"project": "PRJ-2602", "customer": "东海商用宁波分公司", "zl": "ZL-20260828-031", "combo": "ZH-2602-B × 120 套", "mat": "ZH-2602-B", "matName": "冲压件料箱组套", "qty": "120", "unit": "套", "so": "SO-20260829-0038", "addr": "宁波工厂 C 门", "status": "拣货中", "date": "—"}, "cells": ["PRJ-2602", "东海商用宁波分公司", "<span class=\"lk\">ZL-20260828-031</span>", "ZH-2602-B × 120 套", "SO-20260829-0038", "宁波工厂 C 门", "<span class=\"tag tag-blue\">拣货中</span>", "—"], "ops": [{"t": "详情", "act": "go('../租赁管理/租赁出库详情.html?id=CK-20260830-014')"}, {"t": "打印出货单", "act": "go('出货单打印.html?key=CK-20260830-014')"}, {"t": "审核", "act": "go('../租赁管理/租赁出库确认.html?id=CK-20260830-014')"}]},
      'title': '租赁出库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'CK-20260830-014' },
        { 'label': '状态', 'tag': '拣货中' },
        { 'label': '所属项目', 'text': 'PRJ-2602' },
        { 'label': '关联租赁单', 'text': 'ZL-20260828-031', 'url': '租赁管理/租赁单列表.html' },
        { 'label': '关联销售订单', 'text': 'SO-20260829-0038（双关联）', 'url': '销售管理/销售订单列表.html' },
        { 'label': '客户（带出）', 'text': '东海商用宁波分公司' },
        { 'label': '出库类型', 'text': '一箱一件 · 逐件核对（扫码口预留）', 'full': true },
        { 'label': '出库库位', 'text': '成品区 RB' },
        { 'label': '收货地点', 'text': '宁波工厂 C 门' },
        { 'label': '要货日期', 'text': '—' },
        { 'label': '出库备注', 'text': '—' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '出库时间', 'text': '—' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '组合件编码', '组合件名称', '计费方式', '出库数量', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)', '出库库位'],
      'items': [
        ['1', 'ZH-2602-B', '冲压件料箱组套', '按月定期', '120', '1.00', '13%', '1.13', '135.60', '成品区 RB']
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
          'role': '租赁出库（本单）',
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
          'who': '张帆'
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
      'row': {"fields": {"project": "PRJ-2603", "customer": "星途新能源汽车科技有限公司", "zl": "ZL-20260610-015", "combo": "ZH-2603-C × 60 套", "mat": "ZH-2603-C", "matName": "电池托盘护角套件", "qty": "60", "unit": "套", "so": "SO-20260828-0035", "addr": "广州工厂收货口", "status": "已出库", "date": "2026-08-29"}, "cells": ["PRJ-2603", "星途新能源汽车科技有限公司", "<span class=\"lk\">ZL-20260610-015</span>", "ZH-2603-C × 60 套", "SO-20260828-0035", "广州工厂收货口", "<span class=\"tag tag-green\">已出库</span>", "2026-08-29 16:05"], "ops": [{"t": "详情", "act": "go('../租赁管理/租赁出库详情.html?id=CK-20260829-013')"}, {"t": "打印出货单", "act": "go('出货单打印.html?key=CK-20260829-013')"}, {"t": "审核", "act": "go('../租赁管理/租赁出库确认.html?id=CK-20260829-013')"}]},
      'title': '租赁出库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'CK-20260829-013' },
        { 'label': '状态', 'tag': '已出库' },
        { 'label': '所属项目', 'text': 'PRJ-2603' },
        { 'label': '关联租赁单', 'text': 'ZL-20260610-015', 'url': '租赁管理/租赁单列表.html' },
        { 'label': '关联销售订单', 'text': 'SO-20260828-0035（双关联）', 'url': '销售管理/销售订单列表.html' },
        { 'label': '客户（带出）', 'text': '星途新能源汽车科技有限公司' },
        { 'label': '出库类型', 'text': '一箱一件 · 逐件核对（扫码口预留）', 'full': true },
        { 'label': '出库库位', 'text': '成品区 RB' },
        { 'label': '收货地点', 'text': '广州工厂收货口' },
        { 'label': '要货日期', 'text': '—' },
        { 'label': '出库备注', 'text': '—' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '出库时间', 'text': '2026-08-29 16:05' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '组合件编码', '组合件名称', '计费方式', '出库数量', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)', '出库库位'],
      'items': [
        ['1', 'ZH-2603-C', '电池托盘护角套件', '按月定期', '60', '1.00', '13%', '1.13', '67.80', '成品区 RB']
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
          'role': '租赁出库（本单）',
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
          'who': '张帆'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 广州工厂收货口',
          'who': '张帆'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张帆'
        }
      ]
    },
    'CK-20260829-012': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "zl": "ZL-20260301-006", "combo": "ZH-2601-A × 120 套", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "120", "unit": "套", "so": "SO-20260827-0036", "addr": "长春基地一号门", "status": "已出库", "date": "2026-08-29"}, "cells": ["PRJ-2601", "华骏重卡汽车有限公司", "<span class=\"lk\">ZL-20260301-006</span>", "ZH-2601-A × 120 套", "SO-20260827-0036", "长春基地一号门", "<span class=\"tag tag-green\">已出库</span>", "2026-08-29 10:42"], "ops": [{"t": "详情", "act": "go('../租赁管理/租赁出库详情.html?id=CK-20260829-012')"}, {"t": "打印出货单", "act": "go('出货单打印.html?key=CK-20260829-012')"}, {"t": "审核", "act": "go('../租赁管理/租赁出库确认.html?id=CK-20260829-012')"}]},
      'title': '租赁出库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'CK-20260829-012' },
        { 'label': '状态', 'tag': '已出库' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '关联租赁单', 'text': 'ZL-20260301-006', 'url': '租赁管理/租赁单列表.html' },
        { 'label': '关联销售订单', 'text': 'SO-20260827-0036（双关联）', 'url': '销售管理/销售订单列表.html' },
        { 'label': '客户（带出）', 'text': '华骏重卡汽车有限公司' },
        { 'label': '出库类型', 'text': '一箱一件 · 逐件核对（扫码口预留）', 'full': true },
        { 'label': '出库库位', 'text': '成品区 RB' },
        { 'label': '收货地点', 'text': '长春基地一号门' },
        { 'label': '要货日期', 'text': '—' },
        { 'label': '出库备注', 'text': '—' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '出库时间', 'text': '2026-08-29 10:42' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '组合件编码', '组合件名称', '计费方式', '出库数量', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)', '出库库位'],
      'items': [
        ['1', 'ZH-2601-A', '驾驶室围板箱整箱套件', '按月定期', '120', '1.00', '13%', '1.13', '135.60', '成品区 RB']
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
          'role': '租赁出库（本单）',
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
          'who': '张帆'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 长春基地一号门',
          'who': '张帆'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张帆'
        }
      ]
    },
    'CK-20260828-011': {
      'row': {"fields": {"project": "PRJ-2604", "customer": "长风汽车制造有限公司", "zl": "ZL-20260828-031", "combo": "ZH-2601-A × 96 套", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "96", "unit": "套", "so": "SO-20260826-0033", "addr": "武汉工厂 2 号门", "status": "已出库", "date": "2026-08-28"}, "cells": ["PRJ-2604", "长风汽车制造有限公司", "<span class=\"lk\">ZL-20260828-031</span>", "ZH-2601-A × 96 套", "SO-20260826-0033", "武汉工厂 2 号门", "<span class=\"tag tag-green\">已出库</span>", "2026-08-28 14:55"], "ops": [{"t": "详情", "act": "go('../租赁管理/租赁出库详情.html?id=CK-20260828-011')"}, {"t": "打印出货单", "act": "go('出货单打印.html?key=CK-20260828-011')"}, {"t": "审核", "act": "go('../租赁管理/租赁出库确认.html?id=CK-20260828-011')"}]},
      'title': '租赁出库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'CK-20260828-011' },
        { 'label': '状态', 'tag': '已出库' },
        { 'label': '所属项目', 'text': 'PRJ-2604' },
        { 'label': '关联租赁单', 'text': 'ZL-20260828-031', 'url': '租赁管理/租赁单列表.html' },
        { 'label': '关联销售订单', 'text': 'SO-20260826-0033（双关联）', 'url': '销售管理/销售订单列表.html' },
        { 'label': '客户（带出）', 'text': '长风汽车制造有限公司' },
        { 'label': '出库类型', 'text': '一箱一件 · 逐件核对（扫码口预留）', 'full': true },
        { 'label': '出库库位', 'text': '成品区 RB' },
        { 'label': '收货地点', 'text': '武汉工厂 2 号门' },
        { 'label': '要货日期', 'text': '—' },
        { 'label': '出库备注', 'text': '—' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '出库时间', 'text': '2026-08-28 14:55' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '组合件编码', '组合件名称', '计费方式', '出库数量', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)', '出库库位'],
      'items': [
        ['1', 'ZH-2601-A', '驾驶室围板箱整箱套件', '按月定期', '96', '1.00', '13%', '1.13', '108.48', '成品区 RB']
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
          'role': '租赁出库（本单）',
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
          'who': '张帆'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 武汉工厂 2 号门',
          'who': '张帆'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张帆'
        }
      ]
    },
    'CK-20260824-009': {
      'row': {"fields": {"project": "PRJ-2604", "customer": "华骏重卡汽车有限公司", "zl": "ZL-20260823-033", "combo": "ZH-2604-D 混合组合套件 × 40 套", "mat": "ZH-2604-D", "matName": "混合组合套件", "qty": "40", "unit": "套", "so": "—", "addr": "长春基地一号门", "status": "已出库", "date": "2026-08-24"}, "note": "1", "cells": ["PRJ-2604", "华骏重卡汽车有限公司", "<span class=\"lk\">ZL-20260823-033</span>", "ZH-2604-D 混合组合套件 × 40 套", "—", "长春基地一号门", "<span class=\"tag tag-green\">已出库</span>", "2026-08-24 16:40"], "ops": [{"t": "详情", "act": "go('../租赁管理/租赁出库详情.html?id=CK-20260824-009')"}, {"t": "打印出货单", "act": "go('出货单打印.html?key=CK-20260824-009')"}, {"t": "审核", "act": "go('../租赁管理/租赁出库确认.html?id=CK-20260824-009')"}]},
      'title': '租赁出库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'CK-20260824-009' },
        { 'label': '状态', 'tag': '已出库' },
        { 'label': '所属项目', 'text': 'PRJ-2604' },
        { 'label': '关联租赁单', 'text': 'ZL-20260823-033', 'url': '租赁管理/租赁单列表.html' },
        { 'label': '关联销售订单', 'text': '—（租赁出库）' },
        { 'label': '客户（带出）', 'text': '华骏重卡汽车有限公司' },
        { 'label': '出库类型', 'text': '一箱一件 · 逐件核对（扫码口预留）', 'full': true },
        { 'label': '出库库位', 'text': '成品区 RB' },
        { 'label': '收货地点', 'text': '长春基地一号门' },
        { 'label': '要货日期', 'text': '—' },
        { 'label': '出库备注', 'text': '—' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '出库时间', 'text': '2026-08-24 16:40' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '组合件编码', '组合件名称', '计费方式', '出库数量', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)', '出库库位'],
      'items': [
        ['1', 'ZH-2604-D', '混合组合套件', '按月定期', '40', '1.00', '13%', '1.13', '45.20', '成品区 RB']
      ],
      'chain': [
        {
          'role': '租赁单',
          'name': 'ZL-20260823-033',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '租赁出库（本单）',
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
          'who': '张帆'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 长春基地一号门',
          'who': '张帆'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张帆'
        }
      ]
    },
    'CK-20260828-010': {
      'row': {"fields": {"project": "PRJ-2602", "customer": "东海商用宁波分公司", "zl": "ZL-20260815-028", "combo": "ZH-2602-B × 200 套", "mat": "ZH-2602-B", "matName": "冲压件料箱组套", "qty": "200", "unit": "套", "so": "SO-20260826-0032", "addr": "宁波工厂 C 门", "status": "已出库", "date": "2026-08-28"}, "cells": ["PRJ-2602", "东海商用宁波分公司", "<span class=\"lk\">ZL-20260815-028</span>", "ZH-2602-B × 200 套", "SO-20260826-0032", "宁波工厂 C 门", "<span class=\"tag tag-green\">已出库</span>", "2026-08-28 09:30"], "ops": [{"t": "详情", "act": "go('../租赁管理/租赁出库详情.html?id=CK-20260828-010')"}, {"t": "打印出货单", "act": "go('出货单打印.html?key=CK-20260828-010')"}, {"t": "审核", "act": "go('../租赁管理/租赁出库确认.html?id=CK-20260828-010')"}]},
      'title': '租赁出库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'CK-20260828-010' },
        { 'label': '状态', 'tag': '已出库' },
        { 'label': '所属项目', 'text': 'PRJ-2602' },
        { 'label': '关联租赁单', 'text': 'ZL-20260815-028', 'url': '租赁管理/租赁单列表.html' },
        { 'label': '关联销售订单', 'text': 'SO-20260826-0032（双关联）', 'url': '销售管理/销售订单列表.html' },
        { 'label': '客户（带出）', 'text': '东海商用宁波分公司' },
        { 'label': '出库类型', 'text': '一箱一件 · 逐件核对（扫码口预留）', 'full': true },
        { 'label': '出库库位', 'text': '成品区 RB' },
        { 'label': '收货地点', 'text': '宁波工厂 C 门' },
        { 'label': '要货日期', 'text': '—' },
        { 'label': '出库备注', 'text': '—' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '出库时间', 'text': '2026-08-28 09:30' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '组合件编码', '组合件名称', '计费方式', '出库数量', '日租金(元/天)', '税率', '含税单价(元)', '含税金额(元)', '出库库位'],
      'items': [
        ['1', 'ZH-2602-B', '冲压件料箱组套', '按月定期', '200', '1.00', '13%', '1.13', '226.00', '成品区 RB']
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
          'role': '租赁出库（本单）',
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
          'who': '张帆'
        },
        {
          't': '08-30 15:25',
          'text': '装车发运 · 宁波工厂 C 门',
          'who': '张帆'
        },
        {
          't': '08-30 16:00',
          'text': '客户签收 · 出库确认',
          'who': '张帆'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 退租入库单 returnInbounds：键 = TZRK 入库单号（租赁管理/退租入库列表.html 8 行全量） */
  /* 拆散去向：自有回库 / 租入件转归还；缺损/丢失联动丢损赔偿 */
  returnInbounds: {
    'TZRK-20260902-010': {
      'row': {"fields": {"customer": "华骏重卡汽车有限公司", "project": "PRJ-2604", "appliance": "ZH-2604-D 混合组合套件（自购隔板 + 租入大箱）", "mat": "ZH-2604-D", "matName": "混合组合套件（自购隔板 + 租入大箱）", "qty": "40", "unit": "套", "dest": "自有回库 租入件转归还", "warehouse": "成品区 RB", "date": "2026-09-02", "result": "缺损", "status": "待审核"}, "note": "1", "cells": ["华骏重卡汽车有限公司", "PRJ-2604", "ZH-2604-D 混合组合套件（自购隔板 + 租入大箱）", "<span class=\"td-num\">40 套</span>", "隔板×80（自购）/ 大箱×10（租入，其中 4 只缺损）", "<span class=\"tag tag-gray\">自有回库</span> <span class=\"tag tag-orange\" onclick=\"go('../租入管理/租入归还列表.html')\" style=\"cursor:pointer\">租入件转归还</span>", "成品区 RB", "2026-09-02", "<span class=\"tag tag-orange\">缺损</span>", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/退租入库详情.html?id=TZRK-20260902-010')"}, {"t": "审核", "act": "go('../租赁管理/退租入库审核.html?id=TZRK-20260902-010')"}]},
      'title': '退租入库单详情',
      'formTitle': '退租入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'TZRK-20260902-010' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '客户', 'text': '华骏重卡汽车有限公司' },
        { 'label': '所属项目', 'text': 'PRJ-2604' },
        { 'label': '入库库位', 'text': '成品区 RB' },
        { 'label': '拆散方式', 'text': '按 BOM 拆散' },
        { 'label': '退回日期', 'text': '2026-09-02' },
        { 'label': '验收备注', 'text': '—' },
        { 'label': '缺损情况', 'text': '验收发现缺损 · 转丢损赔偿', 'full': true },
        { 'label': '拆散去向', 'text': '自有回库 + 租入件转归还', 'full': true }
      ],
      'itemTitle': '退回明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '退回数量', '缺损数量', '去向'],
      'items': [
        ['1', 'LJ-F600', '折叠隔板', '—', '件', '80', '0', '自有回库 · 成品区 RB'],
        ['2', 'WBX-1210L', '围板箱大箱 1200×1000×970', '1200×1000×970 mm', '只', '10', '4', '租入件转归还（其中 4 只缺损 → 赔付）']
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
          'url': '租入管理/租入归还列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-02 09:40',
          'text': '客户退回 · 直接入库登记（无申请单）',
          'who': '张帆'
        },
        {
          't': '09-02 14:20',
          'text': '到货验收 · 发现大箱 4 只缺损',
          'who': '张帆'
        },
        {
          't': '09-02 16:10',
          'text': '按 BOM 拆散 · 隔板 × 80 自有回库',
          'who': '张帆'
        },
        {
          't': '09-03 14:05',
          'text': '大箱分流归还 · GHCK-20260903-002（4 只缺损赔付）',
          'who': '林国栋'
        }
      ]
    },
    'TZRK-20260903-009': {
      'row': {"fields": {"customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2603", "appliance": "WBX-1210L 围板箱 1200×1000×970（租入）", "mat": "WBX-1210L", "matName": "围板箱 1200×1000×970（租入）", "qty": "30", "unit": "只", "dest": "租入件转归还", "warehouse": "外购区 RW", "date": "2026-09-03", "result": "完好", "status": "待审核"}, "note": "2", "cells": ["东海商用汽车有限公司宁波分公司", "PRJ-2603", "WBX-1210L 围板箱 1200×1000×970（租入）", "<span class=\"td-num\">30 只</span>", "整箱退回（租入资产，不拆散）", "<span class=\"tag tag-orange\" onclick=\"go('../租入管理/租入归还列表.html')\" style=\"cursor:pointer\">租入件转归还</span>", "外购区 RW", "2026-09-03", "<span class=\"tag tag-green\">完好</span>", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/退租入库详情.html?id=TZRK-20260903-009')"}, {"t": "审核", "act": "go('../租赁管理/退租入库审核.html?id=TZRK-20260903-009')"}]},
      'title': '退租入库单详情',
      'formTitle': '退租入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'TZRK-20260903-009' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '客户', 'text': '东海商用汽车有限公司宁波分公司' },
        { 'label': '所属项目', 'text': 'PRJ-2603' },
        { 'label': '入库库位', 'text': '外购区 RW' },
        { 'label': '拆散方式', 'text': '整箱退回（不拆散）' },
        { 'label': '退回日期', 'text': '2026-09-03' },
        { 'label': '验收备注', 'text': '—' },
        { 'label': '缺损情况', 'text': '验收完好', 'full': true },
        { 'label': '拆散去向', 'text': '租入件转归还', 'full': true }
      ],
      'itemTitle': '退回明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '退回数量', '缺损数量', '去向'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '30', '0', '整箱退回 · 租入件转归还']
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
          'url': '租入管理/租入归还列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-03 09:20',
          'text': '客户整箱退回 · 到货验收',
          'who': '张帆'
        },
        {
          't': '09-03 11:00',
          'text': '验收完好 · 不拆散直接转归还',
          'who': '张帆'
        },
        {
          't': '09-03 11:30',
          'text': '整退归还环通 · GHCK-20260903-001',
          'who': '林国栋'
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
      'row': {"fields": {"customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "appliance": "ZH-2601-A 驾驶室围板箱整箱套件", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "60", "unit": "套", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-09-02", "result": "缺损", "status": "待审核"}, "note": "3", "cells": ["华骏重卡汽车有限公司", "PRJ-2601", "ZH-2601-A 驾驶室围板箱整箱套件", "<span class=\"td-num\">60 套</span>", "围板×120 / 箱体×60 / 锁扣组件×240", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-09-02", "<span class=\"tag tag-orange\">缺损</span>", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "审核", "act": "go('../租赁管理/退租入库审核.html?id=TZRK-20260902-008')"}]},
      'title': '退租入库单详情',
      'formTitle': '退租入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'TZRK-20260902-008' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '客户', 'text': '华骏重卡汽车有限公司' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '入库库位', 'text': '成品区 RB' },
        { 'label': '拆散方式', 'text': '按 BOM 拆散' },
        { 'label': '退回日期', 'text': '2026-09-02' },
        { 'label': '验收备注', 'text': '—' },
        { 'label': '缺损情况', 'text': '验收发现缺损 · 转丢损赔偿', 'full': true },
        { 'label': '拆散去向', 'text': '自有回库', 'full': true }
      ],
      'itemTitle': '退回明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '退回数量', '缺损数量', '去向'],
      'items': [
        ['1', 'LJ-C300', '围板', 'HDPE 波纹板 · 970 高', '件', '120', '0', '自有回库 · 成品区 RB'],
        ['2', 'WBX-1210L', '箱体', '1200×1000×970 mm', '只', '60', '0', '自有回库 · 成品区 RB'],
        ['3', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '240', '0', '自有回库 · 成品区 RB']
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
          'who': '张帆'
        },
        {
          't': '09-02 10:30',
          'text': '到货验收 · 发现缺损',
          'who': '张帆'
        },
        {
          't': '09-02 15:40',
          'text': '按 BOM 拆散入库 · 自有回库',
          'who': '张帆'
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
      'row': {"fields": {"customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2602", "appliance": "ZH-2602-B 冲压件料箱组套", "mat": "ZH-2602-B", "matName": "冲压件料箱组套", "qty": "45", "unit": "套", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-09-01", "result": "完好", "status": "已入库"}, "cells": ["东海商用汽车有限公司宁波分公司", "PRJ-2602", "ZH-2602-B 冲压件料箱组套", "<span class=\"td-num\">45 套</span>", "料箱×45 / 隔板×90", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-09-01", "<span class=\"tag tag-green\">完好</span>", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/退租入库详情.html?id=TZRK-20260901-007')"}]},
      'title': '退租入库单详情',
      'formTitle': '退租入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'TZRK-20260901-007' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '客户', 'text': '东海商用汽车有限公司宁波分公司' },
        { 'label': '所属项目', 'text': 'PRJ-2602' },
        { 'label': '入库库位', 'text': '成品区 RB' },
        { 'label': '拆散方式', 'text': '按 BOM 拆散' },
        { 'label': '退回日期', 'text': '2026-09-01' },
        { 'label': '验收备注', 'text': '—' },
        { 'label': '缺损情况', 'text': '验收完好', 'full': true },
        { 'label': '拆散去向', 'text': '自有回库', 'full': true }
      ],
      'itemTitle': '退回明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '退回数量', '缺损数量', '去向'],
      'items': [
        ['1', 'BTC-6040', '料箱 600×400×340', '600×400×340 mm', '只', '45', '0', '自有回库 · 成品区 RB'],
        ['2', 'LJ-F600', '隔板', '—', '件', '90', '0', '自有回库 · 成品区 RB']
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
          'who': '张帆'
        },
        {
          't': '09-01 09:50',
          'text': '到货验收 · 完好',
          'who': '张帆'
        },
        {
          't': '09-01 14:20',
          'text': '按 BOM 拆散入库 · 自有回库',
          'who': '张帆'
        }
      ]
    },
    'TZRK-20260831-006': {
      'row': {"fields": {"customer": "星途新能源汽车科技有限公司", "project": "PRJ-2603", "appliance": "ZH-2603-C 电池托盘护角套件", "mat": "ZH-2603-C", "matName": "电池托盘护角套件", "qty": "20", "unit": "套", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-08-31", "result": "丢失", "status": "已入库"}, "cells": ["星途新能源汽车科技有限公司", "PRJ-2603", "ZH-2603-C 电池托盘护角套件", "<span class=\"td-num\">20 套</span>", "托盘×20 / 护角×80", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-08-31", "<span class=\"tag tag-red\">丢失</span>", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/退租入库详情.html?id=TZRK-20260831-006')"}]},
      'title': '退租入库单详情',
      'formTitle': '退租入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'TZRK-20260831-006' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '客户', 'text': '星途新能源汽车科技有限公司' },
        { 'label': '所属项目', 'text': 'PRJ-2603' },
        { 'label': '入库库位', 'text': '成品区 RB' },
        { 'label': '拆散方式', 'text': '按 BOM 拆散' },
        { 'label': '退回日期', 'text': '2026-08-31' },
        { 'label': '验收备注', 'text': '—' },
        { 'label': '缺损情况', 'text': '验收发现丢失 · 自客户态直接出账（赔偿核销）', 'full': true },
        { 'label': '拆散去向', 'text': '自有回库', 'full': true }
      ],
      'itemTitle': '退回明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '退回数量', '缺损数量', '去向'],
      'items': [
        ['1', 'PLT-1210P', '托盘', '1200×1000×150 mm', '块', '20', '4', '自有回库 · 成品区 RB（4 件丢失 → 赔偿）'],
        ['2', 'LJ-F600', '护角', '—', '件', '80', '0', '自有回库 · 成品区 RB']
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
          'who': '张帆'
        },
        {
          't': '08-31 10:15',
          'text': '到货验收 · 托盘 4 件丢失',
          'who': '张帆'
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
      'row': {"fields": {"customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "appliance": "BTC-6040 料箱", "mat": "BTC-6040", "matName": "料箱", "qty": "200", "unit": "只", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-08-28", "result": "完好", "status": "已入库"}, "cells": ["华骏重卡汽车有限公司", "PRJ-2601", "BTC-6040 料箱", "<span class=\"td-num\">200 只</span>", "—（散件直接入库）", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-08-28", "<span class=\"tag tag-green\">完好</span>", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/退租入库详情.html?id=TZRK-20260828-005')"}]},
      'title': '退租入库单详情',
      'formTitle': '退租入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'TZRK-20260828-005' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '客户', 'text': '华骏重卡汽车有限公司' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '入库库位', 'text': '成品区 RB' },
        { 'label': '拆散方式', 'text': '散件直接入库' },
        { 'label': '退回日期', 'text': '2026-08-28' },
        { 'label': '验收备注', 'text': '—' },
        { 'label': '缺损情况', 'text': '验收完好', 'full': true },
        { 'label': '拆散去向', 'text': '自有回库', 'full': true }
      ],
      'itemTitle': '退回明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '退回数量', '缺损数量', '去向'],
      'items': [
        ['1', 'BTC-6040', '料箱 600×400×340', '600×400×340 mm', '只', '200', '0', '自有回库 · 成品区 RB']
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
          'who': '张帆'
        },
        {
          't': '08-28 09:30',
          'text': '到货验收 · 完好',
          'who': '张帆'
        },
        {
          't': '08-28 11:00',
          'text': '散件直接入库 · 自有回库',
          'who': '张帆'
        }
      ]
    },
    'TZRK-20260825-004': {
      'row': {"fields": {"customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2602", "appliance": "PLT-1210P 塑料托盘", "mat": "PLT-1210P", "matName": "塑料托盘", "qty": "150", "unit": "块", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-08-25", "result": "完好", "status": "已入库"}, "cells": ["东海商用汽车有限公司宁波分公司", "PRJ-2602", "PLT-1210P 塑料托盘", "<span class=\"td-num\">150 块</span>", "—（散件直接入库）", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-08-25", "<span class=\"tag tag-green\">完好</span>", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/退租入库详情.html?id=TZRK-20260825-004')"}]},
      'title': '退租入库单详情',
      'formTitle': '退租入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'TZRK-20260825-004' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '客户', 'text': '东海商用汽车有限公司宁波分公司' },
        { 'label': '所属项目', 'text': 'PRJ-2602' },
        { 'label': '入库库位', 'text': '成品区 RB' },
        { 'label': '拆散方式', 'text': '散件直接入库' },
        { 'label': '退回日期', 'text': '2026-08-25' },
        { 'label': '验收备注', 'text': '—' },
        { 'label': '缺损情况', 'text': '验收完好', 'full': true },
        { 'label': '拆散去向', 'text': '自有回库', 'full': true }
      ],
      'itemTitle': '退回明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '退回数量', '缺损数量', '去向'],
      'items': [
        ['1', 'PLT-1210P', '塑料托盘 1200×1000', '1200×1000×150 mm', '块', '150', '0', '自有回库 · 成品区 RB']
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
          'who': '张帆'
        },
        {
          't': '08-25 10:20',
          'text': '到货验收 · 完好',
          'who': '张帆'
        },
        {
          't': '08-25 15:10',
          'text': '散件直接入库 · 自有回库',
          'who': '张帆'
        }
      ]
    },
    'TZRK-20260820-003': {
      'row': {"fields": {"customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "appliance": "ZH-2601-A 驾驶室围板箱整箱套件", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "30", "unit": "套", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-08-20", "result": "缺损", "status": "已入库"}, "cells": ["华骏重卡汽车有限公司", "PRJ-2601", "ZH-2601-A 驾驶室围板箱整箱套件", "<span class=\"td-num\">30 套</span>", "围板×60 / 箱体×30 / 锁扣组件×120", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-08-20", "<span class=\"tag tag-orange\">缺损</span>", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/退租入库详情.html?id=TZRK-20260820-003')"}]},
      'title': '退租入库单详情',
      'formTitle': '退租入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'TZRK-20260820-003' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '客户', 'text': '华骏重卡汽车有限公司' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '入库库位', 'text': '成品区 RB' },
        { 'label': '拆散方式', 'text': '按 BOM 拆散' },
        { 'label': '退回日期', 'text': '2026-08-20' },
        { 'label': '验收备注', 'text': '—' },
        { 'label': '缺损情况', 'text': '验收发现缺损 · 转丢损赔偿', 'full': true },
        { 'label': '拆散去向', 'text': '自有回库', 'full': true }
      ],
      'itemTitle': '退回明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '退回数量', '缺损数量', '去向'],
      'items': [
        ['1', 'LJ-C300', '围板', 'HDPE 波纹板 · 970 高', '件', '60', '0', '自有回库 · 成品区 RB'],
        ['2', 'WBX-1210L', '箱体', '1200×1000×970 mm', '只', '30', '30', '自有回库 · 成品区 RB（缺损 → 赔偿）'],
        ['3', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '120', '0', '自有回库 · 成品区 RB']
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
          'who': '张帆'
        },
        {
          't': '08-20 09:40',
          'text': '到货验收 · 发现缺损',
          'who': '张帆'
        },
        {
          't': '08-20 15:30',
          'text': '按 BOM 拆散入库 · 缺损件生成赔偿 BS-20260901-009',
          'who': '系统'
        }
      ]
    },
    'TZRK-20260908-011': {
      'row': {"fields": {"customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "appliance": "ZH-2601-A 驾驶室围板箱整箱套件", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "120", "unit": "套", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-09-08", "result": "完好", "status": "已入库"}, "cells": ["华骏重卡汽车有限公司", "PRJ-2601", "ZH-2601-A 驾驶室围板箱整箱套件", "<span class=\"td-num\">120 套</span>", "整套退回 120 套 · 部分退租（在租 530 套中退 120）", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-09-08", "<span class=\"tag tag-green\">完好</span>", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/退租入库详情.html?id=TZRK-20260908-011')"}]},
      'title': '退租入库单详情',
      'formTitle': '退租入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'TZRK-20260908-011' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '客户', 'text': '华骏重卡汽车有限公司' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '入库库位', 'text': '成品区 RB' },
        { 'label': '拆散方式', 'text': '整套退回（不拆散）' },
        { 'label': '退回日期', 'text': '2026-09-08' },
        { 'label': '验收备注', 'text': '—' },
        { 'label': '缺损情况', 'text': '验收完好 · 止租日 2026-09-08（当日仍计租）', 'full': true },
        { 'label': '拆散去向', 'text': '自有回库 · 循环再出租', 'full': true }
      ],
      'itemTitle': '退回明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '退回数量', '缺损数量', '去向'],
      'items': [
        ['1', 'ZH-2601-A', '驾驶室围板箱整箱套件', '—', '套', '120', '0', '自有回库 · 成品区 RB']
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
    },
    'TZRK-20260915-012': {
      'row': {"fields": {"customer": "安吉智行物流", "project": "PRJ-2605", "appliance": "XNC-ZZ-WBX 围板箱 1200×1000×970", "mat": "XNC-ZZ-WBX", "matName": "围板箱 1200×1000×970", "qty": "100", "unit": "只", "dest": "自有回库", "warehouse": "成品区 RB", "date": "2026-09-15", "result": "完好", "status": "已入库"}, "cells": ["安吉智行物流", "PRJ-2605", "XNC-ZZ-WBX 围板箱 1200×1000×970", "<span class=\"td-num\">100 只</span>", "转租物部分退回（终端在租 240 只中退 100 · 余 140 只继续在租）", "<span class=\"tag tag-gray\">自有回库</span>", "成品区 RB", "2026-09-15", "<span class=\"tag tag-green\">完好</span>", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/退租入库详情.html?id=TZRK-20260915-012')"}]},
      'title': '退租入库单详情',
      'formTitle': '退租入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'TZRK-20260915-012' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '客户', 'text': '安吉智行物流' },
        { 'label': '所属项目', 'text': 'PRJ-2605' },
        { 'label': '入库库位', 'text': '成品区 RB' },
        { 'label': '拆散方式', 'text': '整套退回（不拆散）' },
        { 'label': '退回日期', 'text': '2026-09-15' },
        { 'label': '验收备注', 'text': '—' },
        { 'label': '缺损情况', 'text': '验收完好 · 止租日 2026-09-15（当日仍计租）', 'full': true },
        { 'label': '拆散去向', 'text': '转租物经直接客户退回（XNC-ZZ-WBX · 客户转租出 → 退租入库）', 'full': true }
      ],
      'itemTitle': '退回明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '退回数量', '缺损数量', '去向'],
      'items': [
        ['1', 'XNC-ZZ-WBX', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '100', '0', '自有回库 · 成品区 RB']
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
  },  /* -------------------------------------------------------------------------- */
  /* 租入归还单 rentInReturns：键 = GHCK 归还单号（租入管理/租入归还列表.html 3 行全量） */
  /* 归还类型：整退归还(L3) / 分流归还(L4) */
  rentInReturns: {
    'GHCK-20260903-001': {
      'row': {"fields": {"ref": "RZD-20260815-003", "operator": "环通循环包装运营（上海）有限公司", "rtype": "整退归还", "appliance": "围板箱 1200×1000×970", "mat": "WBX-1210L", "matName": "围板箱 1200×1000×970", "qty": "30", "unit": "只", "status": "已归还", "maker": "林国栋", "date": "2026-09-03"}, "note": "1", "cells": ["<span class=\"lk\" onclick=\"go('../租入管理/租入单列表.html')\">RZD-20260815-003</span>", "环通循环包装运营（上海）有限公司", "<span class=\"tag tag-blue\">整退归还</span>", "围板箱 1200×1000×970", "30 只", "<span class=\"tag tag-green\">已归还</span>", "林国栋", "2026-09-03 11:30"], "ops": [{"t": "详情", "act": "go('../租入管理/租入归还详情.html?id=GHCK-20260903-001')"}, {"t": "租金应付", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '租入归还单详情',
      'formTitle': '归还信息',
      'formRows': [
        { 'label': '归还单号', 'text': 'GHCK-20260903-001' },
        { 'label': '状态', 'tag': '已归还' },
        { 'label': '关联租入单', 'text': 'RZD-20260815-003', 'url': '租入管理/租入单列表.html' },
        { 'label': '归还类型', 'text': '整退归还（L3）' },
        { 'label': '归还日期', 'text': '2026-09-03' },
        { 'label': '备注', 'text': '—' },
        { 'label': '供应商（带出）', 'text': '环通循环包装运营（上海）有限公司' },
        { 'label': '器具状况', 'text': '验收完好' },
        { 'label': '租金结算', 'text': '已生成租金应付 AP-20260903-009（36,000.00 元）', 'url': '财务协同/应付账单.html', 'full': true },
        { 'label': '押金退还', 'text': '¥84,000.00 原路退回', 'full': true },
        { 'label': '经办人', 'text': '林国栋' }
      ],
      'itemTitle': '归还明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '租入数量', '已归还', '本次归还数量'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '30', '0', '30']
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
          'who': '林国栋'
        },
        {
          't': '09-03 11:30',
          'text': '整退归还环通 · 出库确认',
          'who': '林国栋'
        },
        {
          't': '09-03',
          'text': '按周期生成租金应付 AP-20260903-009',
          'who': '系统'
        }
      ]
    },
    'GHCK-20260903-002': {
      'row': {"fields": {"ref": "RZD-20260815-005", "operator": "环通循环包装运营（上海）有限公司", "rtype": "分流归还", "appliance": "围板箱 1200×1000×970（退租拆散后归还）", "mat": "WBX-1210L", "matName": "围板箱 1200×1000×970（退租拆散后归还）", "qty": "4", "unit": "只", "status": "待审核", "maker": "林国栋", "date": "2026-09-03"}, "note": "2", "cells": ["<span class=\"lk\" onclick=\"go('../租入管理/租入单列表.html')\">RZD-20260815-005</span>", "环通循环包装运营（上海）有限公司", "<span class=\"tag tag-orange\">分流归还</span>", "围板箱 1200×1000×970（退租拆散后归还）", "4 只", "<span class=\"tag tag-orange\">待审核</span>", "林国栋", "2026-09-03 14:05"], "ops": [{"t": "详情", "act": "go('../租入管理/租入归还详情.html?id=GHCK-20260903-002')"}, {"t": "审核", "act": "go('../租入管理/租入归还审核.html?id=GHCK-20260903-002')"}]},
      'title': '租入归还单详情',
      'formTitle': '归还信息',
      'formRows': [
        { 'label': '归还单号', 'text': 'GHCK-20260903-002' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '关联租入单', 'text': 'RZD-20260815-005', 'url': '租入管理/租入单列表.html' },
        { 'label': '归还类型', 'text': '分流归还（L4）' },
        { 'label': '归还日期', 'text': '2026-09-03' },
        { 'label': '备注', 'text': '—' },
        { 'label': '供应商（带出）', 'text': '环通循环包装运营（上海）有限公司' },
        { 'label': '器具状况', 'text': '验收完好（4 只缺损已转赔付）', 'full': true },
        { 'label': '租金结算', 'text': '按周期生成租金应付 · AP-20260903-010（12,000.00 元）', 'url': '财务协同/应付账单.html', 'full': true },
        { 'label': '押金退还', 'text': '¥12,000.00（归还审核通过后原路退回）', 'full': true },
        { 'label': '经办人', 'text': '林国栋' }
      ],
      'itemTitle': '归还明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '租入数量', '已归还', '本次归还数量'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '10', '0', '4']
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
          'who': '张帆'
        },
        {
          't': '09-03 14:05',
          'text': '分流归还环通 · 其中 4 只缺损转赔付',
          'who': '林国栋'
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
      'row': {"fields": {"ref": "RZD-20260701-001", "operator": "环通循环包装运营（上海）有限公司", "rtype": "整退归还", "appliance": "金属料箱 800×600", "mat": "BTC-6040", "matName": "金属料箱 800×600", "qty": "20", "unit": "只", "status": "已归还", "maker": "周志远", "date": "2026-08-31"}, "cells": ["<span class=\"lk\" onclick=\"go('../租入管理/租入单列表.html')\">RZD-20260701-001</span>", "环通循环包装运营（上海）有限公司", "<span class=\"tag tag-blue\">整退归还</span>", "金属料箱 800×600", "20 只", "<span class=\"tag tag-green\">已归还</span>", "周志远", "2026-08-31 10:15"], "ops": [{"t": "详情", "act": "go('../租入管理/租入归还详情.html?id=GHCK-20260831-003')"}]},
      'title': '租入归还单详情',
      'formTitle': '归还信息',
      'formRows': [
        { 'label': '归还单号', 'text': 'GHCK-20260831-003' },
        { 'label': '状态', 'tag': '已归还' },
        { 'label': '关联租入单', 'text': 'RZD-20260701-001', 'url': '租入管理/租入单列表.html' },
        { 'label': '归还类型', 'text': '整退归还' },
        { 'label': '归还日期', 'text': '2026-08-31' },
        { 'label': '备注', 'text': '—' },
        { 'label': '供应商（带出）', 'text': '环通循环包装运营（上海）有限公司' },
        { 'label': '器具状况', 'text': '验收完好' },
        { 'label': '租金结算', 'text': '租金已结清 · 单据完结', 'full': true },
        { 'label': '押金退还', 'text': '¥10,800.00 原路退回', 'full': true },
        { 'label': '经办人', 'text': '周志远' }
      ],
      'itemTitle': '归还明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '租入数量', '已归还', '本次归还数量'],
      'items': [
        ['1', 'BTC-6040', '金属料箱 800×600', '—', '只', '20', '0', '20']
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260701-001',
          'url': '租入管理/租入单列表.html'
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
          'text': '整退出库 · 归还环通',
          'who': '周志远'
        },
        {
          't': '08-31 10:15',
          'text': '归还确认 · 验收完好',
          'who': '周志远'
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
  /* 租入入库单 rentInbounds：键 = RZRK 入库单号（租入管理/租入入库列表.html 3 行全量） */
  /* 计租起点按租入单起算；入库后转租/组装去向贯通 */
  rentInbounds: {
    'RZRK-20260816-021': {
      'row': {"fields": {"ref": "RZD-20260815-003", "operator": "环通循环包装运营（上海）有限公司", "appliance": "围板箱 1200×1000×970", "area": "外购区 RW", "status": "已入库", "maker": "林国栋", "date": "2026-08-16"}, "note": "1", "cells": ["<span class=\"lk\" onclick=\"go('../租入管理/租入单列表.html')\">RZD-20260815-003</span>", "环通循环包装运营（上海）有限公司", "围板箱 1200×1000×970", "30 只", "外购区 RW", "<span class=\"tag tag-green\">已入库</span>", "林国栋", "2026-08-16 14:20"], "ops": [{"t": "详情", "act": "go('../租入管理/租入入库详情.html?id=RZRK-20260816-021')"}, {"t": "租金应付", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '租入入库单详情',
      'formTitle': '入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'RZRK-20260816-021' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '关联租入单', 'text': 'RZD-20260815-003', 'url': '租入管理/租入单列表.html' },
        { 'label': '供应商', 'text': '环通循环包装运营（上海）有限公司' },
        { 'label': '入库库位', 'text': '外购区 RW（租入在库）', 'full': true },
        { 'label': '计租起点', 'text': '2026-08-15（按租入单起算）', 'full': true },
        { 'label': '经办人', 'text': '林国栋' },
        { 'label': '入库时间', 'text': '2026-08-16 14:20' },
        { 'label': '转租去向', 'text': 'ZL-20260816-029', 'url': '租赁管理/租赁单列表.html', 'full': true }
      ],
      'itemTitle': '入库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '入库数量'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '30']
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260815-003',
          'url': '租入管理/租入单列表.html'
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
          'who': '周志远'
        },
        {
          't': '08-16 10:00',
          'text': '环通到货 · 围板箱 30 只',
          'who': '林国栋'
        },
        {
          't': '08-16 14:20',
          'text': '验收入库 · 计入租入在库（外购区 RW）',
          'who': '林国栋'
        },
        {
          't': '08-16',
          'text': '转租客户 · ZL-20260816-029',
          'who': '沈婷'
        }
      ]
    },
    'RZRK-20260816-022': {
      'row': {"fields": {"ref": "RZD-20260815-005", "operator": "环通循环包装运营（上海）有限公司", "appliance": "围板箱 1200×1000×970", "area": "外购区 RW", "status": "已入库", "maker": "林国栋", "date": "2026-08-16"}, "note": "2", "cells": ["<span class=\"lk\" onclick=\"go('../租入管理/租入单列表.html')\">RZD-20260815-005</span>", "环通循环包装运营（上海）有限公司", "围板箱 1200×1000×970", "10 只", "外购区 RW", "<span class=\"tag tag-green\">已入库</span>", "林国栋", "2026-08-16 15:02"], "ops": [{"t": "详情", "act": "go('../租入管理/租入入库详情.html?id=RZRK-20260816-022')"}, {"t": "租金应付", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '租入入库单详情',
      'formTitle': '入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'RZRK-20260816-022' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '关联租入单', 'text': 'RZD-20260815-005', 'url': '租入管理/租入单列表.html' },
        { 'label': '供应商', 'text': '环通循环包装运营（上海）有限公司' },
        { 'label': '入库库位', 'text': '外购区 RW（租入在库）', 'full': true },
        { 'label': '计租起点', 'text': '2026-08-15（按租入单起算）', 'full': true },
        { 'label': '经办人', 'text': '林国栋' },
        { 'label': '入库时间', 'text': '2026-08-16 15:02' },
        { 'label': '转租去向', 'text': 'ZZ-20260822-006', 'full': true }
      ],
      'itemTitle': '入库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '入库数量'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '10']
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260815-005',
          'url': '租入管理/租入单列表.html'
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
          'who': '周志远'
        },
        {
          't': '08-16 14:30',
          'text': '环通到货 · 围板箱 10 只',
          'who': '林国栋'
        },
        {
          't': '08-16 15:02',
          'text': '验收入库 · 计入租入在库（外购区 RW）',
          'who': '林国栋'
        },
        {
          't': '08-22',
          'text': '混合组装 · ZZ-20260822-006（ZH-2604-D）',
          'who': '刘志强'
        }
      ]
    },
    'RZRK-20260903-023': {
      'row': {"fields": {"ref": "RZD-20260902-008", "operator": "环通循环包装运营（上海）有限公司", "appliance": "塑料托盘 1200×1000", "area": "外购区 RW", "status": "待入库", "maker": "陈锋", "date": "2026-09-03"}, "cells": ["<span class=\"lk\" onclick=\"go('../租入管理/租入单列表.html')\">RZD-20260902-008</span>", "环通循环包装运营（上海）有限公司", "塑料托盘 1200×1000", "50 只", "外购区 RW", "<span class=\"tag tag-orange\">待入库</span>", "陈锋", "2026-09-03 09:45"], "ops": [{"t": "详情", "act": "go('../租入管理/租入入库详情.html?id=RZRK-20260903-023')"}, {"t": "入库确认", "act": "go('../租入管理/租入入库确认.html?id=RZRK-20260903-023')"}]},
      'title': '租入入库单详情',
      'formTitle': '入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'RZRK-20260903-023' },
        { 'label': '状态', 'tag': '待入库' },
        { 'label': '关联租入单', 'text': 'RZD-20260902-008', 'url': '租入管理/租入单列表.html' },
        { 'label': '供应商', 'text': '环通循环包装运营（上海）有限公司' },
        { 'label': '入库库位', 'text': '外购区 RW', 'full': true },
        { 'label': '计租起点', 'text': '2026-09-02（按租入单起算）', 'full': true },
        { 'label': '经办人', 'text': '陈锋' },
        { 'label': '入库时间', 'text': '2026-09-03 09:45' },
        { 'label': '转租去向', 'text': '—（待入库确认）', 'full': true }
      ],
      'itemTitle': '入库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '入库数量'],
      'items': [
        ['1', 'PLT-1210P', '塑料托盘 1200×1000', '1200×1000×150 mm', '块', '50']
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260902-008',
          'url': '租入管理/租入单列表.html'
        },
        {
          'role': '租入入库（本单）',
          'name': 'RZRK-20260903-023 · 待入库',
          'self': true
        },
        {
          'role': '立即转租生成 · 租赁出库',
          'name': 'CK-20260914-023 · 待审核',
          'url': '租赁管理/租赁出库列表.html'
        },
      ],
      'timeline': [
        {
          't': '09-03 09:45',
          'text': '租入单审核通过 · 待到货入库',
          'who': '陈锋'
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
      'row': {"fields": {"supplier": "吴越联合五金制品有限公司", "mtype": "零部件", "summary": "锁扣组件×5,000 / 铰链×2,500", "date": "2026-08-26", "so": "SO-20260831-0042", "status": "已审核"}, "note": "1", "cells": ["吴越联合五金制品有限公司", "<span class=\"tag tag-blue\">零部件</span>", "锁扣组件×5,000 / 铰链×2,500", "<span class=\"td-num\">7,500</span>", "<span class=\"td-num\">13,500.00</span>", "CNY", "2026-08-26", "<span class=\"lk\">SO-20260831-0042</span>", "<span class=\"tag tag-blue\">已审核</span>"], "ops": [{"t": "生成入库单", "act": "go('../采购管理/采购入库列表.html')"}, {"t": "关闭"}, {"t": "上传附件", "act": "openAttModal('PO-20260902-018')"}, {"t": "打印", "act": "orderPrint('PO-20260902-018')"}]},
      'title': '采购订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'PO-20260902-018' },
        { 'label': '状态', 'tag': '已审核' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '吴越联合五金制品有限公司' },
        { 'label': '物料类型', 'text': '零部件' },
        { 'label': '关联销售订单号', 'text': 'SO-20260831-0042（参考 · 不以销定采）', 'url': '销售管理/销售订单列表.html', 'full': true },
        { 'label': '客户（带出）', 'text': '—' },
        { 'label': '预计到货日期', 'text': '2026-08-26' },
        { 'label': '备注', 'text': '—' },
        { 'label': '订单金额', 'text': '13,500.00 CNY' },
        { 'label': '制单人', 'text': '林国栋' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'info2Title': '执行情况（订单·入库·退货数量勾稽）',
      'info2': [
        { 'label': '订购数量', 'text': '锁扣 5,000 / 铰链 2,500' },
        { 'label': '已入库（CGRK-012·08-28 验收通过）', 'text': '锁扣 2,400 / 铰链 2,000' },
        { 'label': '待验收（CGRK-009·08-27 到货）', 'text': '锁扣 800（含拒收 500）/ 铰链 500' },
        { 'label': '采购退货（CGTH-002 拒收）', 'text': '锁扣 500 · 未入库直接退' },
        { 'label': '在途未到', 'text': '锁扣 1,800 / 铰链 0' },
        { 'label': '勾稽对平', 'text': '2,400+800+1,800 = 5,000 ✓ 铰链 2,000+500 = 2,500 ✓' }
      ],
      'itemTitle': '采购明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '5,000', '1.90', '13%', '2.15', '10,750.00'],
        ['2', 'LJ-B200', '铰链', '锌合金 · 65mm', '件', '2,500', '1.60', '13%', '1.81', '4,525.00']
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
          'name': 'CGRK-20260827-009 · 待验收',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '采购入库',
          'name': 'CGRK-20260828-012 · 已入库',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '应付账单',
          'name': '验收通过后生成（采购应付）',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-24 14:20',
          'text': '制单 · 零部件采购（锁扣 / 铰链）',
          'who': '林国栋'
        },
        {
          't': '08-25 09:10',
          'text': '审核通过 · 分批到货',
          'who': '张帆'
        },
        {
          't': '08-27 09:20',
          'text': '第一批到货 · CGRK-20260827-009 待验收（锁扣 800 / 铰链 500）',
          'who': '林国栋'
        },
        {
          't': '08-28 14:32',
          'text': '第二批到货 · CGRK-20260828-012 验收通过（锁扣 2,400 / 铰链 2,000）',
          'who': '张帆'
        }
      ]
    },
    'PO-20260901-017': {
      'row': {"fields": {"supplier": "甬城塑业包装制品有限公司", "mtype": "器具", "summary": "围板箱 1200×1000×970×300", "date": "2026-08-25", "so": "—", "status": "已完成"}, "cells": ["甬城塑业包装制品有限公司", "<span class=\"tag tag-green\">器具</span>", "围板箱 1200×1000×970×300", "<span class=\"td-num\">300</span>", "<span class=\"td-num\">84,000.00</span>", "CNY", "2026-08-25", "—", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../采购管理/采购订单详情.html?id=PO-20260901-017')"}, {"t": "入库记录", "act": "go('../采购管理/采购入库列表.html')"}, {"t": "上传附件", "act": "openAttModal('PO-20260901-017')"}, {"t": "打印", "act": "orderPrint('PO-20260901-017')"}]},
      'title': '采购订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'PO-20260901-017' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '甬城塑业包装制品有限公司' },
        { 'label': '物料类型', 'text': '器具' },
        { 'label': '关联销售订单号', 'text': '——' },
        { 'label': '客户（带出）', 'text': '—' },
        { 'label': '预计到货日期', 'text': '2026-08-25' },
        { 'label': '备注', 'text': '—' },
        { 'label': '订单金额', 'text': '84,000.00 CNY' },
        { 'label': '制单人', 'text': '林国栋' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'itemTitle': '采购明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '300', '280.00', '13%', '316.40', '94,920.00']
      ],
      'chain': [
        {
          'role': '采购订单（本单）',
          'name': 'PO-20260901-017 · 独立采购线',
          'self': true
        },
        {
          'role': '采购入库',
          'name': 'CGRK-20260828-011 · 已入库',
          'url': '采购管理/采购入库列表.html'
        },
        {
          'role': '应付账单',
          'name': 'AP-20260901-008 · 采购应付 · 未付款',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-24 10:40',
          'text': '制单 · 器具采购（围板箱 300 只）',
          'who': '林国栋'
        },
        {
          't': '08-24 15:20',
          'text': '审核通过',
          'who': '张帆'
        },
        {
          't': '08-28 10:05',
          'text': '采购入库 · CGRK-20260828-011 到货 300 只 · 验收通过',
          'who': '张帆'
        },
        {
          't': '09-01',
          'text': '应付账单自动生成 · AP-20260901-008 · 84,000.00 元（未付款）',
          'who': '系统'
        }
      ]
    },
    'PO-20260830-016': {
      'row': {"fields": {"supplier": "延陵塑料托盘厂", "mtype": "器具", "summary": "塑料托盘 1200×1000×500", "date": "2026-09-08", "so": "—", "status": "已审核"}, "cells": ["延陵塑料托盘厂", "<span class=\"tag tag-green\">器具</span>", "塑料托盘 1200×1000×500", "<span class=\"td-num\">500</span>", "<span class=\"td-num\">42,500.00</span>", "CNY", "2026-09-08", "—", "<span class=\"tag tag-blue\">已审核</span>"], "ops": [{"t": "生成入库单", "act": "go('../采购管理/采购入库列表.html')"}, {"t": "关闭"}, {"t": "上传附件", "act": "openAttModal('PO-20260830-016')"}, {"t": "打印", "act": "orderPrint('PO-20260830-016')"}]},
      'title': '采购订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'PO-20260830-016' },
        { 'label': '状态', 'tag': '已审核' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '延陵塑料托盘厂' },
        { 'label': '物料类型', 'text': '器具' },
        { 'label': '关联销售订单号', 'text': '——' },
        { 'label': '客户（带出）', 'text': '—' },
        { 'label': '预计到货日期', 'text': '2026-09-08' },
        { 'label': '备注', 'text': '—' },
        { 'label': '订单金额', 'text': '42,500.00 CNY' },
        { 'label': '制单人', 'text': '林国栋' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'itemTitle': '采购明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'PLT-1210P', '塑料托盘 1200×1000', '1200×1000×150 mm', '块', '500', '85.00', '13%', '96.05', '48,025.00']
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
          'who': '林国栋'
        },
        {
          't': '08-31 14:10',
          'text': '审核通过',
          'who': '张帆'
        },
        {
          't': '—',
          'text': '在途 · 按交期 09-08 到货验收',
          'off': true
        }
      ]
    },
    'PO-20260828-015': {
      'row': {"fields": {"supplier": "吴越联合五金制品有限公司", "mtype": "零部件", "summary": "箱盖 ABS 吸塑×2,000", "date": "2026-09-25", "so": "SO-20260827-0039", "status": "已审核"}, "cells": ["吴越联合五金制品有限公司", "<span class=\"tag tag-blue\">零部件</span>", "箱盖 ABS 吸塑×2,000", "<span class=\"td-num\">2,000</span>", "<span class=\"td-num\">6,300.00</span>", "CNY", "2026-09-25", "<span class=\"lk\">SO-20260827-0039</span>", "<span class=\"tag tag-blue\">已审核</span>"], "ops": [{"t": "生成入库单", "act": "go('../采购管理/采购入库列表.html')"}, {"t": "关闭"}, {"t": "上传附件", "act": "openAttModal('PO-20260828-015')"}, {"t": "打印", "act": "orderPrint('PO-20260828-015')"}]},
      'title': '采购订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'PO-20260828-015' },
        { 'label': '状态', 'tag': '已审核' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '吴越联合五金制品有限公司' },
        { 'label': '物料类型', 'text': '零部件' },
        { 'label': '关联销售订单号', 'text': 'SO-20260827-0039（参考 · 不以销定采）', 'url': '销售管理/销售订单列表.html', 'full': true },
        { 'label': '客户（带出）', 'text': '—' },
        { 'label': '预计到货日期', 'text': '2026-09-25' },
        { 'label': '备注', 'text': '—' },
        { 'label': '订单金额', 'text': '6,300.00 CNY' },
        { 'label': '制单人', 'text': '林国栋' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'itemTitle': '采购明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'LJ-D400', '箱盖', 'ABS 吸塑 · 1200×1000', '件', '2,000', '3.15', '13%', '3.56', '7,120.00']
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
          'role': '应付账单',
          'name': '验收通过后生成（采购应付）',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-28 11:05',
          'text': '制单 · 零部件采购（箱盖 2,000 件）',
          'who': '林国栋'
        },
        {
          't': '08-29 09:30',
          'text': '审核通过',
          'who': '张帆'
        },
        {
          't': '—',
          'text': '在途 · 按交期 09-25 到货验收',
          'off': true
        }
      ]
    },
    'PO-20260825-014': {
      'row': {"fields": {"supplier": "甬城塑业包装制品有限公司", "mtype": "器具", "summary": "料箱 600×400×340×800", "date": "2026-09-02", "so": "—", "status": "已完成"}, "cells": ["甬城塑业包装制品有限公司", "<span class=\"tag tag-green\">器具</span>", "料箱 600×400×340×800", "<span class=\"td-num\">800</span>", "<span class=\"td-num\">35,200.00</span>", "CNY", "2026-09-02", "—", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../采购管理/采购订单详情.html?id=PO-20260825-014')"}, {"t": "入库记录", "act": "go('../采购管理/采购入库列表.html')"}, {"t": "上传附件", "act": "openAttModal('PO-20260825-014')"}, {"t": "打印", "act": "orderPrint('PO-20260825-014')"}]},
      'title': '采购订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'PO-20260825-014' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '甬城塑业包装制品有限公司' },
        { 'label': '物料类型', 'text': '器具' },
        { 'label': '关联销售订单号', 'text': '——' },
        { 'label': '客户（带出）', 'text': '—' },
        { 'label': '预计到货日期', 'text': '2026-09-02' },
        { 'label': '备注', 'text': '—' },
        { 'label': '订单金额', 'text': '35,200.00 CNY' },
        { 'label': '制单人', 'text': '林国栋' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'itemTitle': '采购明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'BTC-6040', '料箱 600×400×340', '600×400×340 mm', '只', '800', '44.00', '13%', '49.72', '39,776.00']
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
          'name': '应付已结清 · 货款两讫',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-25 10:15',
          'text': '制单 · 器具采购（料箱 800 只）',
          'who': '林国栋'
        },
        {
          't': '08-26 09:00',
          'text': '审核通过',
          'who': '张帆'
        },
        {
          't': '08-26',
          'text': '采购入库 · CGRK-20260826-008 验收通过',
          'who': '张帆'
        },
        {
          't': '09-01',
          'text': '应付结清 · 料箱采购货款两讫',
          'who': '财务'
        }
      ]
    },
    'PO-20260820-013': {
      'row': {"fields": {"supplier": "延陵塑料托盘厂", "mtype": "器具", "summary": "木托盘 1200×1000×400", "date": "2026-08-30", "so": "—", "status": "已完成"}, "cells": ["延陵塑料托盘厂", "<span class=\"tag tag-green\">器具</span>", "木托盘 1200×1000×400", "<span class=\"td-num\">400</span>", "<span class=\"td-num\">19,600.00</span>", "CNY", "2026-08-30", "—", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../采购管理/采购订单详情.html?id=PO-20260820-013')"}, {"t": "入库记录", "act": "go('../采购管理/采购入库列表.html')"}, {"t": "上传附件", "act": "openAttModal('PO-20260820-013')"}, {"t": "打印", "act": "orderPrint('PO-20260820-013')"}]},
      'title': '采购订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'PO-20260820-013' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '延陵塑料托盘厂' },
        { 'label': '物料类型', 'text': '器具' },
        { 'label': '关联销售订单号', 'text': '——' },
        { 'label': '客户（带出）', 'text': '—' },
        { 'label': '预计到货日期', 'text': '2026-08-30' },
        { 'label': '备注', 'text': '—' },
        { 'label': '订单金额', 'text': '19,600.00 CNY' },
        { 'label': '制单人', 'text': '林国栋' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'info2Title': '执行情况（订单·入库·应付数量勾稽）',
      'info2': [
        { 'label': '订购数量', 'text': '木托盘 400' },
        { 'label': '已入库（CGRK-010·08-27 验收通过）', 'text': '400 · 全部到货' },
        { 'label': '在途未到', 'text': '0' },
        { 'label': '采购退货', 'text': '无' },
        { 'label': '应付账单（AP-20260830-007）', 'text': '08-30 自动生成 · 未结清部分见应付列表' },
        { 'label': '勾稽对平', 'text': '已入库 400 = 订购 400 ✓ 订单已关闭收货' }
      ],
      'itemTitle': '采购明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'PLT-1210W', '木托盘 1200×1000', '1200×1000×144 mm', '块', '400', '49.00', '13%', '55.37', '22,148.00']
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
          'who': '林国栋'
        },
        {
          't': '08-21 10:20',
          'text': '审核通过',
          'who': '张帆'
        },
        {
          't': '08-27',
          'text': '采购入库 · CGRK-20260827-010 验收通过',
          'who': '林国栋'
        },
        {
          't': '08-30',
          'text': '应付账单自动生成 · AP-20260830-007',
          'who': '系统'
        }
      ]
    },
    'PO-20260815-012': {
      'row': {"fields": {"supplier": "吴越联合五金制品有限公司", "mtype": "零部件", "summary": "内衬 EPE 珍珠棉×3,000", "date": "2026-08-25", "so": "—", "status": "已关闭"}, "cells": ["吴越联合五金制品有限公司", "<span class=\"tag tag-blue\">零部件</span>", "内衬 EPE 珍珠棉×3,000", "<span class=\"td-num\">3,000</span>", "<span class=\"td-num\">4,500.00</span>", "CNY", "2026-08-25", "—", "<span class=\"tag tag-gray\">已关闭</span>"], "ops": [{"t": "详情", "act": "go('../采购管理/采购订单详情.html?id=PO-20260815-012')"}, {"t": "上传附件", "act": "openAttModal('PO-20260815-012')"}, {"t": "打印", "act": "orderPrint('PO-20260815-012')"}]},
      'title': '采购订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'PO-20260815-012' },
        { 'label': '状态', 'tag': '已关闭' },
        { 'label': '所属项目', 'text': '—' },
        { 'label': '供应商', 'text': '吴越联合五金制品有限公司' },
        { 'label': '物料类型', 'text': '零部件' },
        { 'label': '关联销售订单号', 'text': '——' },
        { 'label': '客户（带出）', 'text': '—' },
        { 'label': '预计到货日期', 'text': '2026-08-25' },
        { 'label': '备注', 'text': '—' },
        { 'label': '订单金额', 'text': '4,500.00 CNY' },
        { 'label': '制单人', 'text': '林国栋' },
        { 'label': '审核人', 'text': '—' }
      ],
      'itemTitle': '采购明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'LJ-F600', '内衬', 'EPE 珍珠棉 · 定制', '件', '3,000', '1.50', '13%', '1.69', '5,070.00']
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
          'who': '林国栋'
        },
        {
          't': '08-18 09:40',
          'text': '审核通过',
          'who': '张帆'
        },
        {
          't': '08-24',
          'text': '部分到货 · CGRK-20260824-005',
          'who': '林国栋'
        },
        {
          't': '09-01',
          'text': '订单关闭 · 需求变更终止后续到货',
          'who': '林国栋'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 销售订单 salesOrders：键 = SO 订单号（销售管理/销售订单列表.html 8 行全量） */
  /* 订单唯一来源=项目经理代下；客户自助为演示例外 */
  salesOrders: {
    'SO-20260903-0047': {
      'row': {"fields": {"customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2602", "summary": "冲压件隔板×2,400（先采后销 · 采购在途）", "status": "待发货", "agent": "江强", "date": "2026-09-03"}, "note": "1", "cells": ["东海商用汽车有限公司宁波分公司", "PRJ-2602", "冲压件隔板×2,400（先采后销 · 采购在途）", "<span class=\"td-num\">2,400</span>", "<span class=\"td-num\">28,800.00</span>", "<span class=\"tag tag-blue\">待发货</span>", "江强", "2026-09-03 11:20"], "ops": [{"t": "编辑", "act": "go('../销售管理/销售订单新建.html')"}, {"t": "审核", "act": "go('../销售管理/销售订单审核.html?id=SO-20260903-0047')"}, {"t": "关闭"}, {"t": "上传附件", "act": "openAttModal('SO-20260903-0047')"}, {"t": "打印", "act": "orderPrint('SO-20260903-0047')"}]},
      'title': '销售订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'SO-20260903-0047' },
        { 'label': '状态', 'tag': '待发货' },
        { 'label': '客户', 'text': '东海商用汽车有限公司宁波分公司' },
        { 'label': '所属项目', 'text': 'PRJ-2602' },
        { 'label': '要求交货日期', 'text': '—' },
        { 'label': '备注', 'text': '先采后销 · 采购在途，库存到位后发货', 'full': true },
        { 'label': '订单金额', 'text': '28,800.00 元' },
        { 'label': '下单方式', 'text': '项目经理代下（订单唯一来源）', 'full': true },
        { 'label': '业务员', 'text': '江强' },
        { 'label': '下单时间', 'text': '2026-09-03 11:20' },
        { 'label': '订单附件', 'text': 'PO-2601-围板箱采购合同.pdf · 客户下单确认邮件截图.png（新建可上传/删除，演示）', 'full': true }
      ],
      'itemTitle': '订单明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'GB-2602', '冲压件隔板', '—', '件', '2,400', '12.00', '13%', '13.56', '32,544.00']
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
          'who': '江强'
        },
        {
          't': '09-03 11:30',
          'text': '审核通过 · 待采购入库到位',
          'who': '江强'
        },
        {
          't': '—',
          'text': '待发货 · 库存可用量满足后转销售出库',
          'off': true
        }
      ]
    },
    'SO-20260902-0046': {
      'row': {"fields": {"customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "summary": "锁扣组件×3,000", "status": "待审核", "agent": "江强", "date": "2026-09-02"}, "cells": ["华骏重卡汽车有限公司", "PRJ-2601", "锁扣组件×3,000", "<span class=\"td-num\">3,000</span>", "<span class=\"td-num\">4,800.00</span>", "<span class=\"tag tag-orange\">待审核</span>", "江强", "2026-09-02 10:24"], "ops": [{"t": "编辑", "act": "go('../销售管理/销售订单新建.html')"}, {"t": "审核", "act": "go('../销售管理/销售订单审核.html?id=SO-20260902-0046')"}, {"t": "关闭"}, {"t": "上传附件", "act": "openAttModal('SO-20260902-0046')"}, {"t": "打印", "act": "orderPrint('SO-20260902-0046')"}]},
      'title': '销售订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'SO-20260902-0046' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '客户', 'text': '华骏重卡汽车有限公司' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '要求交货日期', 'text': '—' },
        { 'label': '备注', 'text': '关联采购订单在途', 'full': true },
        { 'label': '订单金额', 'text': '4,800.00 元' },
        { 'label': '下单方式', 'text': '项目经理代下（订单唯一来源）', 'full': true },
        { 'label': '业务员', 'text': '江强' },
        { 'label': '下单时间', 'text': '2026-09-02 10:24' },
        { 'label': '订单附件', 'text': 'PO-2601-围板箱采购合同.pdf · 客户下单确认邮件截图.png（新建可上传/删除，演示）', 'full': true }
      ],
      'itemTitle': '订单明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '3,000', '1.60', '13%', '1.81', '5,430.00']
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
          'who': '江强'
        },
        {
          't': '—',
          'text': '待审核 · 通过后按库存可用量发货',
          'off': true
        }
      ]
    },
    'SO-20260901-0045': {
      'row': {"fields": {"customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2602", "summary": "铰链×1,200 / 箱盖×800", "status": "待审核", "agent": "何雅", "date": "2026-09-01", "po": "—"}, "cells": ["东海商用汽车有限公司宁波分公司", "PRJ-2602", "铰链×1,200 / 箱盖×800", "<span class=\"td-num\">2,000</span>", "<span class=\"td-num\">6,050.00</span>", "<span class=\"tag tag-orange\">待审核</span>", "何雅", "2026-09-01 16:40"], "ops": [{"t": "编辑", "act": "go('../销售管理/销售订单新建.html')"}, {"t": "审核", "act": "go('../销售管理/销售订单审核.html?id=SO-20260901-0045')"}, {"t": "关闭"}, {"t": "上传附件", "act": "openAttModal('SO-20260901-0045')"}, {"t": "打印", "act": "orderPrint('SO-20260901-0045')"}]},
      'title': '销售订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'SO-20260901-0045' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '客户', 'text': '东海商用汽车有限公司宁波分公司' },
        { 'label': '所属项目', 'text': 'PRJ-2602' },
        { 'label': '要求交货日期', 'text': '—' },
        { 'label': '备注', 'text': '库存销售 · 原料区现货可发', 'full': true },
        { 'label': '订单金额', 'text': '6,050.00 元' },
        { 'label': '下单方式', 'text': '客户自助（例外 · 演示保留）', 'full': true },
        { 'label': '业务员', 'text': '何雅' },
        { 'label': '下单时间', 'text': '2026-09-01 16:40' },
        { 'label': '订单附件', 'text': 'PO-2601-围板箱采购合同.pdf · 客户下单确认邮件截图.png（新建可上传/删除，演示）', 'full': true }
      ],
      'itemTitle': '订单明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'LJ-B200', '铰链', '锌合金 · 65mm', '件', '1,200', '1.60', '13%', '1.81', '2,172.00'],
        ['2', 'LJ-D400', '箱盖', 'ABS 吸塑 · 1200×1000', '件', '800', '—', '13%', '—', '4,130.00']
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
          'who': '何雅'
        },
        {
          't': '—',
          'text': '待审核 · 通过后按库存可用量发货',
          'off': true
        }
      ]
    },
    'SO-20260831-0044': {
      'row': {"fields": {"customer": "星途新能源汽车科技有限公司", "project": "PRJ-2603", "summary": "内衬 EPE 珍珠棉×5,000", "status": "已审核", "agent": "陈锋", "date": "2026-08-31", "po": "—"}, "cells": ["星途新能源汽车科技有限公司", "PRJ-2603", "内衬 EPE 珍珠棉×5,000", "<span class=\"td-num\">5,000</span>", "<span class=\"td-num\">9,000.00</span>", "<span class=\"tag tag-blue\">已审核</span>", "陈锋", "2026-08-31 11:05"], "ops": [{"t": "发货", "act": "go('../销售管理/销售出库列表.html')"}, {"t": "关闭"}, {"t": "上传附件", "act": "openAttModal('SO-20260831-0044')"}, {"t": "打印", "act": "orderPrint('SO-20260831-0044')"}]},
      'title': '销售订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'SO-20260831-0044' },
        { 'label': '状态', 'tag': '已审核' },
        { 'label': '客户', 'text': '星途新能源汽车科技有限公司' },
        { 'label': '所属项目', 'text': 'PRJ-2603' },
        { 'label': '要求交货日期', 'text': '—' },
        { 'label': '备注', 'text': '库存销售 · 按可用量排期发货', 'full': true },
        { 'label': '订单金额', 'text': '9,000.00 元' },
        { 'label': '下单方式', 'text': '项目经理代下（订单唯一来源）', 'full': true },
        { 'label': '业务员', 'text': '陈锋' },
        { 'label': '下单时间', 'text': '2026-08-31 11:05' },
        { 'label': '订单附件', 'text': 'PO-2601-围板箱采购合同.pdf · 客户下单确认邮件截图.png（新建可上传/删除，演示）', 'full': true }
      ],
      'itemTitle': '订单明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'LJ-F600', '内衬', 'EPE 珍珠棉 · 定制', '件', '5,000', '1.80', '13%', '2.03', '10,150.00']
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
          'who': '陈锋'
        },
        {
          't': '08-31 15:20',
          'text': '审核通过',
          'who': '江强'
        },
        {
          't': '—',
          'text': '待发货 · 按库存可用量排期',
          'off': true
        }
      ]
    },
    'SO-20260830-0043': {
      'row': {"fields": {"customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "summary": "箱盖 ABS 吸塑×1,500", "status": "待发货", "agent": "严明", "date": "2026-08-30", "po": "—"}, "cells": ["华骏重卡汽车有限公司", "PRJ-2601", "箱盖 ABS 吸塑×1,500", "<span class=\"td-num\">1,500</span>", "<span class=\"td-num\">5,400.00</span>", "<span class=\"tag tag-blue\">待发货</span>", "严明", "2026-08-30 09:18"], "ops": [{"t": "发货", "act": "go('../销售管理/销售出库列表.html')"}, {"t": "关闭"}, {"t": "上传附件", "act": "openAttModal('SO-20260830-0043')"}, {"t": "打印", "act": "orderPrint('SO-20260830-0043')"}]},
      'title': '销售订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'SO-20260830-0043' },
        { 'label': '状态', 'tag': '待发货' },
        { 'label': '客户', 'text': '华骏重卡汽车有限公司' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '要求交货日期', 'text': '—' },
        { 'label': '备注', 'text': '库存销售 · 已排产备货', 'full': true },
        { 'label': '订单金额', 'text': '5,400.00 元' },
        { 'label': '下单方式', 'text': '客户自助（例外 · 演示保留）', 'full': true },
        { 'label': '业务员', 'text': '严明' },
        { 'label': '下单时间', 'text': '2026-08-30 09:18' },
        { 'label': '订单附件', 'text': 'PO-2601-围板箱采购合同.pdf · 客户下单确认邮件截图.png（新建可上传/删除，演示）', 'full': true }
      ],
      'itemTitle': '订单明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'LJ-D400', '箱盖', 'ABS 吸塑 · 1200×1000', '件', '1,500', '3.60', '13%', '4.07', '6,105.00']
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
          'who': '严明'
        },
        {
          't': '08-30 14:40',
          'text': '审核通过',
          'who': '江强'
        },
        {
          't': '09-02',
          'text': '销售出库制单 · XSCK-20260902-015（在库 980 + 在途补充）',
          'who': '张帆'
        },
        {
          't': '—',
          'text': '待出库审核 · 通过后生成销售费应收',
          'off': true
        }
      ]
    },
    'SO-20260828-0041': {
      'row': {"fields": {"customer": "长风汽车制造有限公司", "project": "PRJ-2604", "summary": "锁扣组件×800", "status": "已完成", "agent": "江强", "date": "2026-08-28"}, "cells": ["长风汽车制造有限公司", "PRJ-2604", "锁扣组件×800", "<span class=\"td-num\">800</span>", "<span class=\"td-num\">1,280.00</span>", "<span class=\"tag tag-green\">已完成</span>", "江强", "2026-08-28 15:52"], "ops": [{"t": "详情", "act": "go('../销售管理/销售订单详情.html?id=SO-20260828-0041')"}, {"t": "上传附件", "act": "openAttModal('SO-20260828-0041')"}, {"t": "打印", "act": "orderPrint('SO-20260828-0041')"}]},
      'title': '销售订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'SO-20260828-0041' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '客户', 'text': '长风汽车制造有限公司' },
        { 'label': '所属项目', 'text': 'PRJ-2604' },
        { 'label': '要求交货日期', 'text': '—' },
        { 'label': '备注', 'text': '已完成发货与应收结转', 'full': true },
        { 'label': '订单金额', 'text': '1,280.00 元' },
        { 'label': '下单方式', 'text': '项目经理代下（订单唯一来源）', 'full': true },
        { 'label': '业务员', 'text': '江强' },
        { 'label': '下单时间', 'text': '2026-08-28 15:52' },
        { 'label': '订单附件', 'text': 'PO-2601-围板箱采购合同.pdf · 客户下单确认邮件截图.png（新建可上传/删除，演示）', 'full': true }
      ],
      'itemTitle': '订单明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '800', '1.60', '13%', '1.81', '1,448.00']
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
          'who': '江强'
        },
        {
          't': '08-29 09:00',
          'text': '审核通过',
          'who': '江强'
        },
        {
          't': '09-01',
          'text': '销售出库 · XSCK-20260901-014（800 件）',
          'who': '张帆'
        },
        {
          't': '09-02',
          'text': '销售费应收生成 · AR-2026-09-PRJ2604-S1',
          'who': '系统'
        }
      ]
    },
    'SO-20260827-0039': {
      'row': {"fields": {"customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "summary": "箱盖 ABS 吸塑×2,500", "status": "已完成", "agent": "严明", "date": "2026-08-27"}, "cells": ["华骏重卡汽车有限公司", "PRJ-2601", "箱盖 ABS 吸塑×2,500", "<span class=\"td-num\">2,500</span>", "<span class=\"td-num\">9,000.00</span>", "<span class=\"tag tag-green\">已完成</span>", "严明", "2026-08-27 14:03"], "ops": [{"t": "详情", "act": "go('../销售管理/销售订单详情.html?id=SO-20260827-0039')"}, {"t": "上传附件", "act": "openAttModal('SO-20260827-0039')"}, {"t": "打印", "act": "orderPrint('SO-20260827-0039')"}]},
      'title': '销售订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'SO-20260827-0039' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '客户', 'text': '华骏重卡汽车有限公司' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '要求交货日期', 'text': '—' },
        { 'label': '备注', 'text': '已完成发货与应收结转', 'full': true },
        { 'label': '订单金额', 'text': '7,200.00 元' },
        { 'label': '下单方式', 'text': '客户自助（例外 · 演示保留）', 'full': true },
        { 'label': '业务员', 'text': '严明' },
        { 'label': '下单时间', 'text': '2026-08-27 14:03' },
        { 'label': '订单附件', 'text': 'PO-2601-围板箱采购合同.pdf · 客户下单确认邮件截图.png（新建可上传/删除，演示）', 'full': true }
      ],
      'itemTitle': '订单明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'LJ-D400', '箱盖', 'ABS 吸塑 · 1200×1000', '件', '2,000', '3.60', '13%', '4.07', '8,140.00']
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
          'name': 'XSCK-20260829-013（第一批 2,000）',
          'url': '销售管理/销售出库列表.html'
        },
        {
          'role': '销售出库',
          'name': 'XSCK-20260910-016（第二批 500）',
          'url': '销售管理/销售出库列表.html'
        },
        {
          'role': '应收账单',
          'name': 'AR-2026-08-PRJ2601 · 8 月汇总（含第一批）',
          'url': '财务协同/应收账单.html'
        },
        {
          'role': '应收账单',
          'name': 'AR-2026-09-PRJ2601-S2 · 按次（第二批）',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-27 14:03',
          'text': '客户下单 · 箱盖 2,500 件',
          'who': '严明'
        },
        {
          't': '08-28 09:20',
          'text': '审核通过 · 分批交付',
          'who': '江强'
        },
        {
          't': '08-29',
          'text': '第一批出库 · XSCK-20260829-013（2,000 件）',
          'who': '张帆'
        },
        {
          't': '08-31',
          'text': '应收汇总生成 · AR-2026-08-PRJ2601（含第一批）',
          'who': '系统'
        },
        {
          't': '09-10',
          'text': '第二批出库 · XSCK-20260910-016（500 件）',
          'who': '张帆'
        },
        {
          't': '09-11',
          'text': '按次应收生成 · AR-2026-09-PRJ2601-S2',
          'who': '系统'
        }
      ]
    },
    'SO-20260820-0036': {
      'row': {"fields": {"customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2602", "summary": "铰链×600", "status": "已关闭", "agent": "江强", "date": "2026-08-20", "po": "—"}, "cells": ["东海商用汽车有限公司宁波分公司", "PRJ-2602", "铰链×600", "<span class=\"td-num\">600</span>", "<span class=\"td-num\">1,890.00</span>", "<span class=\"tag tag-gray\">已关闭</span>", "江强", "2026-08-20 10:44"], "ops": [{"t": "详情", "act": "go('../销售管理/销售订单详情.html?id=SO-20260820-0036')"}, {"t": "上传附件", "act": "openAttModal('SO-20260820-0036')"}, {"t": "打印", "act": "orderPrint('SO-20260820-0036')"}]},
      'title': '销售订单详情',
      'formTitle': '订单信息',
      'formRows': [
        { 'label': '订单号', 'text': 'SO-20260820-0036' },
        { 'label': '状态', 'tag': '已关闭' },
        { 'label': '客户', 'text': '东海商用汽车有限公司宁波分公司' },
        { 'label': '所属项目', 'text': 'PRJ-2602' },
        { 'label': '要求交货日期', 'text': '—' },
        { 'label': '备注', 'text': '客户取消 · 单据关闭', 'full': true },
        { 'label': '订单金额', 'text': '1,890.00 元' },
        { 'label': '下单方式', 'text': '项目经理代下（订单唯一来源）', 'full': true },
        { 'label': '业务员', 'text': '江强' },
        { 'label': '下单时间', 'text': '2026-08-20 10:44' },
        { 'label': '订单附件', 'text': 'PO-2601-围板箱采购合同.pdf · 客户下单确认邮件截图.png（新建可上传/删除，演示）', 'full': true }
      ],
      'itemTitle': '订单明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'],
      'items': [
        ['1', 'LJ-B200', '铰链', '锌合金 · 65mm', '件', '600', '1.60', '13%', '1.81', '1,086.00']
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
          'who': '江强'
        },
        {
          't': '08-22 09:15',
          'text': '客户取消 · 单据关闭',
          'who': '江强'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 采购入库单 purchaseInbounds：键 = CGRK 入库单号（采购管理/采购入库列表.html 8 行全量） */
  /* 凭采购订单到货验收；验收通过生成采购应付 */
  purchaseInbounds: {
    'CGRK-20260828-012': {
      'row': {"fields": {"supplier": "吴越联合五金制品有限公司", "order": "PO-20260902-018", "project": "PRJ-2601", "status": "已入库", "inTime": "2026-08-28 14:32", "maker": "张帆", "area": "原料区 RA"}, "cells": ["吴越联合五金制品有限公司", "<span class=\"lk\">PO-20260902-018</span>", "PRJ-2601", "原料区 RA", "<span class=\"tag tag-green\">已入库</span>", "张帆", "2026-08-28 14:32"], "ops": [{"t": "详情", "act": "go('../采购管理/采购入库详情.html?id=CGRK-20260828-012')"}, {"t": "验收", "act": "go('../采购管理/采购入库审核.html?id=CGRK-20260828-012')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'CGRK-20260828-012' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '供应商', 'text': '吴越联合五金制品有限公司' },
        { 'label': '关联采购订单号', 'text': 'PO-20260902-018', 'url': '采购管理/采购订单列表.html' },
        { 'label': '到货日期', 'text': '—' },
        { 'label': '仓管员', 'text': '张帆' },
        { 'label': '质检要求', 'text': '凭采购订单到货验收', 'full': true },
        { 'label': '随货单据', 'text': '—' },
        { 'label': '备注', 'text': '验收通过后库存入账，并可生成应付账单', 'full': true },
        { 'label': '单据类型', 'text': '采购入库单 · 零部件采购' },
        { 'label': '到货数量', 'text': '40 托 / 3,400 件' },
        { 'label': '入库库位', 'text': '原料区 RA' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '入库时间', 'text': '2026-08-28 14:32' }
      ],
      'itemTitle': '到货明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次号', '入库库位'],
      'items': [
        ['1', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '2,400', '4.80', '13%', '5.42', '13,008.00', 'B20260828-01', '原料区 RA'],
        ['2', 'LJ-B200', '铰链', '锌合金 · 65mm', '件', '2,000', '1.60', '13%', '1.81', '3,620.00', 'B20260828-02', '原料区 RA']
      ],
      'chain': [
        {
          'role': '采购订单',
          'name': 'PO-20260902-018',
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
          'text': '到货登记 · 吴越联合送货到达原料区 RA（40 托）',
          'who': '张帆'
        },
        {
          't': '08-28 11:20',
          'text': '数量清点 · 40 托 / 3,400 件，与采购订单一致',
          'who': '张帆'
        },
        {
          't': '08-28 14:10',
          'text': '质检验收 · 抽检合格，验收通过',
          'who': '张帆'
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
      'row': {"fields": {"supplier": "甬城塑业包装制品有限公司", "order": "PO-20260901-017", "project": "PRJ-2601", "status": "已入库", "inTime": "2026-08-28 10:05", "maker": "张帆", "area": "原料区 RA"}, "note": "2", "cells": ["甬城塑业包装制品有限公司", "<span class=\"lk\">PO-20260901-017</span>", "PRJ-2601", "原料区 RA", "<span class=\"tag tag-green\">已入库</span>", "张帆", "2026-08-28 10:05"], "ops": [{"t": "详情", "act": "go('../采购管理/采购入库详情.html?id=CGRK-20260828-011')"}, {"t": "验收", "act": "go('../采购管理/采购入库审核.html?id=CGRK-20260828-011')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'CGRK-20260828-011' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '所属项目', 'text': 'PRJ-2601' },
        { 'label': '供应商', 'text': '甬城塑业包装制品有限公司' },
        { 'label': '关联采购订单号', 'text': 'PO-20260901-017', 'url': '采购管理/采购订单列表.html' },
        { 'label': '到货日期', 'text': '—' },
        { 'label': '仓管员', 'text': '张帆' },
        { 'label': '质检要求', 'text': '凭采购订单到货验收', 'full': true },
        { 'label': '随货单据', 'text': '—' },
        { 'label': '备注', 'text': '验收通过后库存入账，并可生成应付账单', 'full': true },
        { 'label': '单据类型', 'text': '采购入库单 · 器具采购' },
        { 'label': '到货数量', 'text': '25 托' },
        { 'label': '入库库位', 'text': '原料区 RA' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '入库时间', 'text': '2026-08-28 10:05' }
      ],
      'itemTitle': '到货明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次号', '入库库位'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '300', '280.00', '13%', '316.40', '94,920.00', 'B20260828-11', '原料区 RA']
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
          'name': 'AP-20260901-008 · 采购应付 · 未付款',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-28 09:10',
          'text': '到货登记 · 甬城塑业围板箱 300 只',
          'who': '张帆'
        },
        {
          't': '08-28 09:50',
          'text': '数量清点 · 与采购订单一致',
          'who': '张帆'
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
      'row': {"fields": {"supplier": "延陵塑料托盘厂", "order": "PO-20260820-013", "project": "PRJ-2602", "status": "已入库", "inTime": "2026-08-27 16:44", "maker": "林国栋", "area": "成品区 RB"}, "cells": ["延陵塑料托盘厂", "<span class=\"lk\">PO-20260820-013</span>", "PRJ-2602", "成品区 RB", "<span class=\"tag tag-green\">已入库</span>", "林国栋", "2026-08-27 16:44"], "ops": [{"t": "详情", "act": "go('../采购管理/采购入库详情.html?id=CGRK-20260827-010')"}, {"t": "验收", "act": "go('../采购管理/采购入库审核.html?id=CGRK-20260827-010')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'CGRK-20260827-010' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '所属项目', 'text': 'PRJ-2602' },
        { 'label': '供应商', 'text': '延陵塑料托盘厂' },
        { 'label': '关联采购订单号', 'text': 'PO-20260820-013', 'url': '采购管理/采购订单列表.html' },
        { 'label': '到货日期', 'text': '—' },
        { 'label': '仓管员', 'text': '林国栋' },
        { 'label': '质检要求', 'text': '凭采购订单到货验收', 'full': true },
        { 'label': '随货单据', 'text': '—' },
        { 'label': '备注', 'text': '验收通过后库存入账，并可生成应付账单', 'full': true },
        { 'label': '单据类型', 'text': '采购入库单 · 器具采购' },
        { 'label': '到货数量', 'text': '18 托' },
        { 'label': '入库库位', 'text': '成品区 RB' },
        { 'label': '制单人', 'text': '林国栋' },
        { 'label': '入库时间', 'text': '2026-08-27 16:44' }
      ],
      'itemTitle': '到货明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次号', '入库库位'],
      'items': [
        ['1', 'PLT-1210W', '木托盘 1200×1000', '1200×1000×144 mm', '块', '400', '49.00', '13%', '55.37', '22,148.00', 'B20260827-10', '成品区 RB']
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
          'text': '到货登记 · 延陵托盘木托盘 400 块',
          'who': '林国栋'
        },
        {
          't': '08-27 16:20',
          'text': '数量清点 · 与采购订单一致',
          'who': '林国栋'
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
      'row': {"fields": {"supplier": "吴越联合五金制品有限公司", "order": "PO-20260902-018", "project": "PRJ-2602", "status": "待验收", "inTime": "2026-08-27 09:20", "maker": "林国栋", "area": "原料区 RA"}, "cells": ["吴越联合五金制品有限公司", "<span class=\"lk\">PO-20260902-018</span>", "PRJ-2602", "原料区 RA", "<span class=\"tag tag-orange\">待验收</span>", "林国栋", "2026-08-27 09:20"], "ops": [{"t": "详情", "act": "go('../采购管理/采购入库详情.html?id=CGRK-20260827-009')"}, {"t": "验收", "act": "go('../采购管理/采购入库审核.html?id=CGRK-20260827-009')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'CGRK-20260827-009' },
        { 'label': '状态', 'tag': '待验收' },
        { 'label': '所属项目', 'text': 'PRJ-2602' },
        { 'label': '供应商', 'text': '吴越联合五金制品有限公司' },
        { 'label': '关联采购订单号', 'text': 'PO-20260902-018', 'url': '采购管理/采购订单列表.html' },
        { 'label': '到货日期', 'text': '—' },
        { 'label': '仓管员', 'text': '林国栋' },
        { 'label': '质检要求', 'text': '凭采购订单到货验收', 'full': true },
        { 'label': '随货单据', 'text': '—' },
        { 'label': '备注', 'text': '验收通过后库存入账，并可生成应付账单', 'full': true },
        { 'label': '单据类型', 'text': '采购入库单 · 零部件采购' },
        { 'label': '到货数量', 'text': '12 托' },
        { 'label': '入库库位', 'text': '原料区 RA' },
        { 'label': '制单人', 'text': '林国栋' },
        { 'label': '入库时间', 'text': '2026-08-27 09:20' }
      ],
      'itemTitle': '到货明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次号', '入库库位'],
      'items': [
        ['1', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '800', '1.90', '13%', '2.15', '1,720.00', 'B20260827-09', '原料区 RA'],
        ['2', 'LJ-B200', '铰链', '锌合金 · 65mm', '件', '500', '1.60', '13%', '1.81', '905.00', 'B20260827-09', '原料区 RA']
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
          'text': '到货登记 · 吴越联合零部件 12 托',
          'who': '林国栋'
        },
        {
          't': '—',
          'text': '待验收 · 验收通过后库存入账并生成应付',
          'off': true
        }
      ]
    },
    'CGRK-20260826-008': {
      'row': {"fields": {"supplier": "甬城塑业包装制品有限公司", "order": "PO-20260825-014", "project": "PRJ-2603", "status": "已入库", "inTime": "2026-08-26 15:10", "maker": "张帆", "area": "原料区 RA"}, "cells": ["甬城塑业包装制品有限公司", "<span class=\"lk\">PO-20260825-014</span>", "PRJ-2603", "原料区 RA", "<span class=\"tag tag-green\">已入库</span>", "张帆", "2026-08-26 15:10"], "ops": [{"t": "详情", "act": "go('../采购管理/采购入库详情.html?id=CGRK-20260826-008')"}, {"t": "验收", "act": "go('../采购管理/采购入库审核.html?id=CGRK-20260826-008')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'CGRK-20260826-008' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '所属项目', 'text': 'PRJ-2603' },
        { 'label': '供应商', 'text': '甬城塑业包装制品有限公司' },
        { 'label': '关联采购订单号', 'text': 'PO-20260825-014', 'url': '采购管理/采购订单列表.html' },
        { 'label': '到货日期', 'text': '—' },
        { 'label': '仓管员', 'text': '张帆' },
        { 'label': '质检要求', 'text': '凭采购订单到货验收', 'full': true },
        { 'label': '随货单据', 'text': '—' },
        { 'label': '备注', 'text': '验收通过后库存入账，并可生成应付账单', 'full': true },
        { 'label': '单据类型', 'text': '采购入库单 · 器具采购' },
        { 'label': '到货数量', 'text': '9 托' },
        { 'label': '入库库位', 'text': '原料区 RA' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '入库时间', 'text': '2026-08-26 15:10' }
      ],
      'itemTitle': '到货明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次号', '入库库位'],
      'items': [
        ['1', 'BTC-6040', '料箱 600×400×340', '600×400×340 mm', '只', '800', '44.00', '13%', '49.72', '39,776.00', 'B20260826-08', '原料区 RA']
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
          'name': '应付已结清 · 货款两讫',
          'url': '财务协同/应付账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-26 13:40',
          'text': '到货登记 · 甬城塑业料箱 800 只',
          'who': '张帆'
        },
        {
          't': '08-26 14:50',
          'text': '数量清点 · 与采购订单一致',
          'who': '张帆'
        },
        {
          't': '08-26 15:10',
          'text': '验收通过 · 库存入账（原料区 RA）',
          'who': '系统'
        },
        {
          't': '09-01',
          'text': '应付结清 · 料箱采购货款两讫',
          'who': '财务'
        }
      ]
    },
    'CGRK-20260825-006': {
      'row': {"fields": {"supplier": "延陵塑料托盘厂", "order": "PO-20260830-016", "project": "PRJ-2603", "status": "已入库", "inTime": "2026-08-25 11:02", "maker": "张帆", "area": "成品区 RB"}, "cells": ["延陵塑料托盘厂", "<span class=\"lk\">PO-20260830-016</span>", "PRJ-2603", "成品区 RB", "<span class=\"tag tag-green\">已入库</span>", "张帆", "2026-08-25 11:02"], "ops": [{"t": "详情", "act": "go('../采购管理/采购入库详情.html?id=CGRK-20260825-006')"}, {"t": "验收", "act": "go('../采购管理/采购入库审核.html?id=CGRK-20260825-006')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'CGRK-20260825-006' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '所属项目', 'text': 'PRJ-2603' },
        { 'label': '供应商', 'text': '延陵塑料托盘厂' },
        { 'label': '关联采购订单号', 'text': 'PO-20260830-016', 'url': '采购管理/采购订单列表.html' },
        { 'label': '到货日期', 'text': '—' },
        { 'label': '仓管员', 'text': '张帆' },
        { 'label': '质检要求', 'text': '凭采购订单到货验收', 'full': true },
        { 'label': '随货单据', 'text': '—' },
        { 'label': '备注', 'text': '验收通过后库存入账，并可生成应付账单', 'full': true },
        { 'label': '单据类型', 'text': '采购入库单 · 器具采购' },
        { 'label': '到货数量', 'text': '22 托' },
        { 'label': '入库库位', 'text': '成品区 RB' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '入库时间', 'text': '2026-08-25 11:02' }
      ],
      'itemTitle': '到货明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次号', '入库库位'],
      'items': [
        ['1', 'PLT-1210P', '塑料托盘 1200×1000', '1200×1000×150 mm', '块', '500', '85.00', '13%', '96.05', '48,025.00', 'B20260825-06', '成品区 RB']
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
          'text': '到货登记 · 延陵托盘塑料托盘 500 块',
          'who': '张帆'
        },
        {
          't': '08-25 10:40',
          'text': '数量清点 · 与采购订单一致',
          'who': '张帆'
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
      'row': {"fields": {"supplier": "吴越联合五金制品有限公司", "order": "PO-20260815-012", "project": "PRJ-2604", "status": "已入库", "inTime": "2026-08-24 14:18", "maker": "林国栋", "area": "原料区 RA"}, "note": "1", "cells": ["吴越联合五金制品有限公司", "<span class=\"lk\">PO-20260815-012</span>", "PRJ-2604", "原料区 RA", "<span class=\"tag tag-green\">已入库</span>", "林国栋", "2026-08-24 14:18"], "ops": [{"t": "详情", "act": "go('../采购管理/采购入库详情.html?id=CGRK-20260824-005')"}, {"t": "验收", "act": "go('../采购管理/采购入库审核.html?id=CGRK-20260824-005')"}, {"t": "应付账单", "act": "go('../财务协同/应付账单.html')"}]},
      'title': '采购入库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'CGRK-20260824-005' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '所属项目', 'text': 'PRJ-2604' },
        { 'label': '供应商', 'text': '吴越联合五金制品有限公司' },
        { 'label': '关联采购订单号', 'text': 'PO-20260815-012', 'url': '采购管理/采购订单列表.html' },
        { 'label': '到货日期', 'text': '—' },
        { 'label': '仓管员', 'text': '林国栋' },
        { 'label': '质检要求', 'text': '凭采购订单到货验收', 'full': true },
        { 'label': '随货单据', 'text': '—' },
        { 'label': '备注', 'text': '验收通过后库存入账，并可生成应付账单', 'full': true },
        { 'label': '单据类型', 'text': '采购入库单 · 零部件采购' },
        { 'label': '到货数量', 'text': '6 托' },
        { 'label': '入库库位', 'text': '原料区 RA' },
        { 'label': '制单人', 'text': '林国栋' },
        { 'label': '入库时间', 'text': '2026-08-24 14:18' }
      ],
      'itemTitle': '到货明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次号', '入库库位'],
      'items': [
        ['1', 'LJ-F600', '内衬', 'EPE 珍珠棉 · 定制', '件', '3,000', '1.50', '13%', '1.69', '5,070.00', 'B20260824-05', '原料区 RA']
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
          'text': '到货登记 · 吴越联合内衬 3,000 件',
          'who': '林国栋'
        },
        {
          't': '08-24 14:00',
          'text': '数量清点 · 与采购订单一致',
          'who': '林国栋'
        },
        {
          't': '08-24 14:18',
          'text': '验收通过 · 库存入账（原料区 RA）',
          'who': '系统'
        }
      ]
    },
    'CGRK-20260820-006': {
      'row': {"fields": {"supplier": "吴越联合五金制品有限公司", "order": "PO-20260815-012", "project": "PRJ-2604", "status": "已入库", "inTime": "2026-08-20 14:30", "maker": "张帆", "area": "原料区 RA"}, "note": "3", "cells": ["吴越联合五金制品有限公司", "<span class=\"lk\">PO-20260815-012</span>", "PRJ-2604", "原料区 RA", "<span class=\"tag tag-green\">已入库</span>", "张帆", "2026-08-20 14:30"], "ops": [{"t": "详情", "act": "go('../采购管理/采购入库详情.html?id=CGRK-20260820-006')"}, {"t": "验收", "act": "go('../采购管理/采购入库审核.html?id=CGRK-20260820-006')"}]},
      'title': '采购入库单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'CGRK-20260820-006' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '所属项目', 'text': 'PRJ-2604' },
        { 'label': '供应商', 'text': '吴越联合五金制品有限公司' },
        { 'label': '关联采购订单号', 'text': 'PO-20260815-012', 'url': '采购管理/采购订单列表.html' },
        { 'label': '到货日期', 'text': '—' },
        { 'label': '仓管员', 'text': '张帆' },
        { 'label': '质检要求', 'text': '凭采购订单到货验收', 'full': true },
        { 'label': '随货单据', 'text': '—' },
        { 'label': '备注', 'text': '验收通过后库存入账，并可生成应付账单', 'full': true },
        { 'label': '单据类型', 'text': '采购入库单 · 器具采购' },
        { 'label': '到货数量', 'text': '80 件（折叠隔板）' },
        { 'label': '入库库位', 'text': '原料区 RA' },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '入库时间', 'text': '2026-08-20 14:30' }
      ],
      'itemTitle': '到货明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '批次号', '入库库位'],
      'items': [
        ['1', 'GB-800', '折叠隔板', '—', '件', '80', '—', '13%', '—', '—', 'B20260820-06', '原料区 RA']
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
          'who': '张帆'
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
    'XSCK-20260910-016': {
      'row': {"fields": {"so": "SO-20260827-0039", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "summary": "箱盖 ABS 吸塑×500（第二批）", "warehouse": "原料区 RA", "date": "2026-09-10", "status": "已完成", "ar": "AR-2026-09-PRJ2601-S2"}, "cells": ["<span class=\"lk\">SO-20260827-0039</span>", "华骏重卡汽车有限公司", "PRJ-2601", "箱盖 ABS 吸塑×500（第二批）", "<span class=\"td-num\">500</span>", "原料区 RA", "2026-09-10", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../销售管理/销售出库详情.html?id=XSCK-20260910-016')"}, {"t": "打印出货单", "act": "go('../租赁管理/出货单打印.html?key=XSCK-20260910-016')"}, {"t": "应收账单", "act": "go('../财务协同/应收账单.html')"}]},
      'title': '销售出库单详情',
      'formTitle': '出库信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'XSCK-20260910-016' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '关联销售订单', 'text': 'SO-20260827-0039', 'url': '销售管理/销售订单列表.html' },
        { 'label': '出库库位', 'text': '原料区 RA' },
        { 'label': '出库日期', 'text': '2026-09-10' },
        { 'label': '备注', 'text': 'SO-20260827-0039 第二批交付（累计 2,500 件全部交付）', 'full': true },
        { 'label': '关联应收账单', 'text': 'AR-2026-09-PRJ2601-S2（销售费 · 按次生成）', 'url': '财务协同/应收账单.html', 'full': true },
        { 'label': '客户（带出）', 'text': '华骏重卡汽车有限公司' },
        { 'label': '所属项目（带出）', 'text': 'PRJ-2601' },
        { 'label': '计价方式', 'text': '销售价随订单（一进一出）', 'full': true },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '制单时间', 'text': '2026-09-10' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '出库数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '备注'],
      'items': [
        ['1', 'LJ-D400', '箱盖', 'ABS 吸塑 · 1200×1000', '件', '500', '3.60', '13%', '4.07', '2,034.00', '—']
      ],
      'chain': [
        {
          'role': '销售订单',
          'name': 'SO-20260827-0039（第二批）',
          'url': '销售管理/销售订单列表.html'
        },
        {
          'role': '销售出库（本单）',
          'name': 'XSCK-20260910-016',
          'self': true
        },
        {
          'role': '应收账单',
          'name': 'AR-2026-09-PRJ2601-S2 · 销售费（按次生成）',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '09-10 09:20',
          'text': '备货 · 原料区 RA 箱盖 500 件（第二批）',
          'who': '张帆'
        },
        {
          't': '09-10 15:40',
          'text': '出库确认 · 客户签收 · 订单全部交付',
          'who': '张帆'
        },
        {
          't': '09-11',
          'text': '按次应收生成 · AR-2026-09-PRJ2601-S2（1,800.00 元）',
          'who': '系统'
        }
      ]
    },
    'XSCK-20260902-015': {
      'row': {"fields": {"so": "SO-20260830-0043", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "summary": "箱盖 ABS 吸塑×1,500", "warehouse": "原料区 RA", "date": "2026-09-02", "status": "待审核"}, "note": "1", "cells": ["<span class=\"lk\">SO-20260830-0043</span>", "华骏重卡汽车有限公司", "PRJ-2601", "箱盖 ABS 吸塑×1,500", "<span class=\"td-num\">1,500</span>", "原料区 RA", "2026-09-02", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "审核", "act": "go('../销售管理/销售出库审核.html?id=XSCK-20260902-015')"}, {"t": "详情", "act": "go('../销售管理/销售出库详情.html?id=XSCK-20260902-015')"}, {"t": "打印出货单", "act": "go('../租赁管理/出货单打印.html?key=XSCK-20260902-015')"}]},
      'title': '销售出库单详情',
      'formTitle': '出库信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'XSCK-20260902-015' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '关联销售订单', 'text': 'SO-20260830-0043', 'url': '销售管理/销售订单列表.html' },
        { 'label': '出库库位', 'text': '原料区 RA' },
        { 'label': '出库日期', 'text': '2026-09-02' },
        { 'label': '备注', 'text': '—' },
        { 'label': '客户（带出）', 'text': '华骏重卡汽车有限公司' },
        { 'label': '所属项目（带出）', 'text': 'PRJ-2601' },
        { 'label': '计价方式', 'text': '销售价随订单（一进一出）', 'full': true },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '制单时间', 'text': '2026-09-02 11:30' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '出库数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '备注'],
      'items': [
        ['1', 'LJ-D400', '箱盖', 'ABS 吸塑 · 1200×1000', '件', '1,500', '36.00', '13%', '40.68', '61,020.00', '—']
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
          'who': '张帆'
        },
        {
          't': '—',
          'text': '待审核 · 通过后出库并生成销售费应收',
          'off': true
        }
      ]
    },
    'XSCK-20260901-014': {
      'row': {"fields": {"so": "SO-20260828-0041", "customer": "长风汽车制造有限公司", "project": "PRJ-2604", "summary": "锁扣组件×800", "warehouse": "原料区 RA", "date": "2026-09-01", "status": "已完成", "ar": "AR-2026-09-PRJ2604-S1"}, "cells": ["<span class=\"lk\">SO-20260828-0041</span>", "长风汽车制造有限公司", "PRJ-2604", "锁扣组件×800", "<span class=\"td-num\">800</span>", "原料区 RA", "2026-09-01", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../销售管理/销售出库详情.html?id=XSCK-20260901-014')"}, {"t": "打印出货单", "act": "go('../租赁管理/出货单打印.html?key=XSCK-20260901-014')"}, {"t": "应收账单", "act": "go('../财务协同/应收账单.html')"}]},
      'title': '销售出库单详情',
      'formTitle': '出库信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'XSCK-20260901-014' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '关联销售订单', 'text': 'SO-20260828-0041', 'url': '销售管理/销售订单列表.html' },
        { 'label': '出库库位', 'text': '原料区 RA' },
        { 'label': '出库日期', 'text': '2026-09-01' },
        { 'label': '备注', 'text': '—' },
        { 'label': '关联应收账单', 'text': 'AR-2026-09-PRJ2604-S1（销售费 · 按次生成）', 'url': '财务协同/应收账单.html', 'full': true },
        { 'label': '客户（带出）', 'text': '长风汽车制造有限公司' },
        { 'label': '所属项目（带出）', 'text': 'PRJ-2604' },
        { 'label': '计价方式', 'text': '销售价随订单（一进一出）', 'full': true },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '制单时间', 'text': '2026-09-01' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '出库数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '备注'],
      'items': [
        ['1', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '800', '6.80', '13%', '7.68', '6,144.00', '—']
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
          'who': '张帆'
        },
        {
          't': '09-01 15:40',
          'text': '出库确认 · 客户签收',
          'who': '张帆'
        },
        {
          't': '09-02',
          'text': '销售费应收生成 · AR-2026-09-PRJ2604-S1（1,280 元）',
          'who': '系统'
        }
      ]
    },
    'XSCK-20260829-013': {
      'row': {"fields": {"so": "SO-20260827-0039", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "summary": "箱盖 ABS 吸塑×2,000", "warehouse": "原料区 RA", "date": "2026-08-29", "status": "已完成", "ar": "AR-2026-08-PRJ2601"}, "cells": ["<span class=\"lk\">SO-20260827-0039</span>", "华骏重卡汽车有限公司", "PRJ-2601", "箱盖 ABS 吸塑×2,000", "<span class=\"td-num\">2,000</span>", "原料区 RA", "2026-08-29", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../销售管理/销售出库详情.html?id=XSCK-20260829-013')"}, {"t": "打印出货单", "act": "go('../租赁管理/出货单打印.html?key=XSCK-20260829-013')"}, {"t": "应收账单", "act": "go('../财务协同/应收账单.html')"}]},
      'title': '销售出库单详情',
      'formTitle': '出库信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'XSCK-20260829-013' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '关联销售订单', 'text': 'SO-20260827-0039', 'url': '销售管理/销售订单列表.html' },
        { 'label': '出库库位', 'text': '原料区 RA' },
        { 'label': '出库日期', 'text': '2026-08-29' },
        { 'label': '备注', 'text': '—' },
        { 'label': '关联应收账单', 'text': 'AR-2026-08-PRJ2601（销售费 · 8 月按出库汇总）', 'url': '财务协同/应收账单.html', 'full': true },
        { 'label': '客户（带出）', 'text': '华骏重卡汽车有限公司' },
        { 'label': '所属项目（带出）', 'text': 'PRJ-2601' },
        { 'label': '计价方式', 'text': '销售价随订单（一进一出）', 'full': true },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '制单时间', 'text': '2026-08-29' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '出库数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '备注'],
      'items': [
        ['1', 'LJ-D400', '箱盖', 'ABS 吸塑 · 1200×1000', '件', '2,000', '36.00', '13%', '40.68', '81,360.00', '—']
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
          'name': 'AR-2026-08-PRJ2601 · 销售费（8 月按出库汇总）',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-29 09:40',
          'text': '备货 · 原料区 RA 箱盖 2,000 件',
          'who': '张帆'
        },
        {
          't': '08-29 16:05',
          'text': '出库确认 · 客户签收',
          'who': '张帆'
        },
        {
          't': '08-31',
          'text': '应收账单汇总生成 · AR-2026-08-PRJ2601（销售费）',
          'who': '系统'
        }
      ]
    },
    'XSCK-20260826-012': {
      'row': {"fields": {"so": "SO-20260822-0038", "customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2602", "summary": "铰链×900 / 内衬×400", "warehouse": "原料区 RA", "date": "2026-08-26", "status": "已完成", "ar": "AR-2026-08-PRJ2602-S1"}, "cells": ["<span class=\"lk\">SO-20260822-0038</span>", "东海商用汽车有限公司宁波分公司", "PRJ-2602", "铰链×900 / 内衬×400", "<span class=\"td-num\">1,300</span>", "原料区 RA", "2026-08-26", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../销售管理/销售出库详情.html?id=XSCK-20260826-012')"}, {"t": "打印出货单", "act": "go('../租赁管理/出货单打印.html?key=XSCK-20260826-012')"}, {"t": "应收账单", "act": "go('../财务协同/应收账单.html')"}]},
      'title': '销售出库单详情',
      'formTitle': '出库信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'XSCK-20260826-012' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '关联销售订单', 'text': 'SO-20260822-0038', 'url': '销售管理/销售订单列表.html' },
        { 'label': '出库库位', 'text': '原料区 RA' },
        { 'label': '出库日期', 'text': '2026-08-26' },
        { 'label': '备注', 'text': '—' },
        { 'label': '关联应收账单', 'text': 'AR-2026-08-PRJ2602-S1（销售费 · 已结清）', 'url': '财务协同/应收账单.html', 'full': true },
        { 'label': '客户（带出）', 'text': '东海商用汽车有限公司宁波分公司' },
        { 'label': '所属项目（带出）', 'text': 'PRJ-2602' },
        { 'label': '计价方式', 'text': '销售价随订单（一进一出）', 'full': true },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '制单时间', 'text': '2026-08-26' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '出库数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '备注'],
      'items': [
        ['1', 'LJ-B200', '铰链', '锌合金 · 65mm', '件', '1,300', '4.20', '13%', '4.75', '6,175.00', '—'],
        ['2', 'LJ-F600', '内衬', 'EPE 珍珠棉 · 定制', '件', '400', '15.50', '13%', '17.51', '7,004.00', '—']
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
          'who': '张帆'
        },
        {
          't': '08-26 15:30',
          'text': '出库确认 · 客户签收',
          'who': '张帆'
        },
        {
          't': '08-31',
          'text': '销售费应收生成 · AR-2026-08-PRJ2602-S1（6,050 元）',
          'who': '系统'
        }
      ]
    },
    'XSCK-20260822-011': {
      'row': {"fields": {"so": "SO-20260819-0035", "customer": "星途新能源汽车科技有限公司", "project": "PRJ-2603", "summary": "锁扣组件×1,200", "warehouse": "原料区 RA", "date": "2026-08-22", "status": "已完成", "ar": "AR-2026-08-PRJ2603"}, "cells": ["<span class=\"lk\">SO-20260819-0035</span>", "星途新能源汽车科技有限公司", "PRJ-2603", "锁扣组件×1,200", "<span class=\"td-num\">1,200</span>", "原料区 RA", "2026-08-22", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../销售管理/销售出库详情.html?id=XSCK-20260822-011')"}, {"t": "打印出货单", "act": "go('../租赁管理/出货单打印.html?key=XSCK-20260822-011')"}, {"t": "应收账单", "act": "go('../财务协同/应收账单.html')"}]},
      'title': '销售出库单详情',
      'formTitle': '出库信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'XSCK-20260822-011' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '关联销售订单', 'text': 'SO-20260819-0035', 'url': '销售管理/销售订单列表.html' },
        { 'label': '出库库位', 'text': '原料区 RA' },
        { 'label': '出库日期', 'text': '2026-08-22' },
        { 'label': '备注', 'text': '—' },
        { 'label': '关联应收账单', 'text': 'AR-2026-08-PRJ2603（销售费 · 8 月按出库汇总）', 'url': '财务协同/应收账单.html', 'full': true },
        { 'label': '客户（带出）', 'text': '星途新能源汽车科技有限公司' },
        { 'label': '所属项目（带出）', 'text': 'PRJ-2603' },
        { 'label': '计价方式', 'text': '销售价随订单（一进一出）', 'full': true },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '制单时间', 'text': '2026-08-22' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '出库数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '备注'],
      'items': [
        ['1', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '1,200', '6.80', '13%', '7.68', '9,216.00', '—']
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
          'name': 'AR-2026-08-PRJ2603 · 销售费（8 月按出库汇总）',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-22 09:30',
          'text': '备货 · 原料区 RA 锁扣 1,200 件',
          'who': '张帆'
        },
        {
          't': '08-22 14:20',
          'text': '出库确认 · 客户签收',
          'who': '张帆'
        },
        {
          't': '08-31',
          'text': '应收账单汇总生成 · AR-2026-08-PRJ2603（销售费）',
          'who': '系统'
        }
      ]
    },
    'XSCK-20260818-010': {
      'row': {"fields": {"so": "SO-20260815-0032", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "summary": "箱盖 ABS 吸塑×600", "warehouse": "原料区 RA", "date": "2026-08-18", "status": "已完成", "ar": "AR-2026-08-PRJ2601"}, "cells": ["<span class=\"lk\">SO-20260815-0032</span>", "华骏重卡汽车有限公司", "PRJ-2601", "箱盖 ABS 吸塑×600", "<span class=\"td-num\">600</span>", "原料区 RA", "2026-08-18", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../销售管理/销售出库详情.html?id=XSCK-20260818-010')"}, {"t": "打印出货单", "act": "go('../租赁管理/出货单打印.html?key=XSCK-20260818-010')"}, {"t": "应收账单", "act": "go('../财务协同/应收账单.html')"}]},
      'title': '销售出库单详情',
      'formTitle': '出库信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'XSCK-20260818-010' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '关联销售订单', 'text': 'SO-20260815-0032', 'url': '销售管理/销售订单列表.html' },
        { 'label': '出库库位', 'text': '原料区 RA' },
        { 'label': '出库日期', 'text': '2026-08-18' },
        { 'label': '备注', 'text': '—' },
        { 'label': '关联应收账单', 'text': 'AR-2026-08-PRJ2601（销售费 · 8 月按出库汇总）', 'url': '财务协同/应收账单.html', 'full': true },
        { 'label': '客户（带出）', 'text': '华骏重卡汽车有限公司' },
        { 'label': '所属项目（带出）', 'text': 'PRJ-2601' },
        { 'label': '计价方式', 'text': '销售价随订单（一进一出）', 'full': true },
        { 'label': '制单人', 'text': '张帆' },
        { 'label': '制单时间', 'text': '2026-08-18' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '出库数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '备注'],
      'items': [
        ['1', 'LJ-D400', '箱盖', 'ABS 吸塑 · 1200×1000', '件', '600', '36.00', '13%', '40.68', '24,408.00', '—']
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
          'name': 'AR-2026-08-PRJ2601 · 销售费（8 月按出库汇总）',
          'url': '财务协同/应收账单.html'
        }
      ],
      'timeline': [
        {
          't': '08-18 10:00',
          'text': '备货 · 原料区 RA 箱盖 600 件',
          'who': '张帆'
        },
        {
          't': '08-18 16:10',
          'text': '出库确认 · 客户签收',
          'who': '张帆'
        },
        {
          't': '08-31',
          'text': '应收账单汇总生成 · AR-2026-08-PRJ2601（销售费）',
          'who': '系统'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 其他入库单 otherInbounds：键 = QTRK 入库单号（仓储作业/其他入库列表.html 3 行全量） */
  /* 期初/盘盈/退货/手工例外；盘盈联动盘点差异 */
  otherInbounds: {
    'QTRK-20260901-003': {
      'row': {"fields": {"type": "盘盈", "material": "LJ-B200 铰链 锌合金 65mm", "warehouse": "原料区 RA", "date": "2026-09-01", "status": "待审核"}, "cells": ["<span class=\"tag tag-blue\">盘盈</span>", "LJ-B200 铰链 锌合金 65mm", "<span class=\"td-num\">120 件</span>", "原料区 RA", "2026-09-01", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "审核", "act": "go('../仓储作业/其他入库审核.html?id=QTRK-20260901-003')"}, {"t": "详情", "act": "go('../仓储作业/其他入库详情.html?id=QTRK-20260901-003')"}]},
      'title': '其他入库单详情',
      'formTitle': '入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'QTRK-20260901-003' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '入库类型', 'text': '盘盈入库（盘点差异处理）', 'full': true },
        { 'label': '入库库位', 'text': '原料区 RA' },
        { 'label': '入库日期', 'text': '2026-09-01' },
        { 'label': '备注', 'text': '账外实物，盘点确认后补录库存', 'full': true },
        { 'label': '单据类型', 'text': '其他入库单 · 盘盈' },
        { 'label': '关联盘点单', 'text': 'PD-202608-02', 'url': '仓储作业/盘点列表.html' },
        { 'label': '制单人', 'text': '赵芳' },
        { 'label': '审核人', 'text': '—' }
      ],
      'itemTitle': '入库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '入库数量', '备注'],
      'items': [
        ['1', 'LJ-B200', '铰链', '锌合金 · 65mm', '件', '120', '盘盈补录 · 原料区 RA']
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
          'who': '陈锋'
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
      'row': {"fields": {"type": "退货", "material": "LJ-D400 箱盖 ABS 吸塑", "warehouse": "原料区 RA", "date": "2026-08-28", "status": "已入库"}, "cells": ["<span class=\"tag tag-orange\">退货</span>", "LJ-D400 箱盖 ABS 吸塑", "<span class=\"td-num\">300 件</span>", "原料区 RA", "2026-08-28", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "act": "go('../仓储作业/其他入库详情.html?id=QTRK-20260828-002')"}]},
      'title': '其他入库单详情',
      'formTitle': '入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'QTRK-20260828-002' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '入库类型', 'text': '客户退货入库（质量换货退回）', 'full': true },
        { 'label': '入库库位', 'text': '原料区 RA' },
        { 'label': '入库日期', 'text': '2026-08-28' },
        { 'label': '备注', 'text': '客户换货退回，质检合格后回库', 'full': true },
        { 'label': '单据类型', 'text': '其他入库单 · 退货' },
        { 'label': '关联盘点单', 'text': '—' },
        { 'label': '制单人', 'text': '赵芳' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'itemTitle': '入库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '入库数量', '备注'],
      'items': [
        ['1', 'LJ-D400', '箱盖', 'ABS 吸塑 · 1200×1000', '件', '300', '退货回库 · 原料区 RA']
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
          'who': '张帆'
        },
        {
          't': '08-28 10:40',
          'text': '质检验收 · 合格回库',
          'who': '张帆'
        },
        {
          't': '08-28 14:00',
          'text': '入库完成 · 库存入账',
          'who': '系统'
        }
      ]
    },
    'QTRK-20260820-001': {
      'row': {"fields": {"type": "其他", "material": "WBX-1210M 围板箱 1200×1000×590", "warehouse": "成品区 RB", "date": "2026-08-20", "status": "已入库"}, "cells": ["<span class=\"tag tag-gray\">其他</span>", "WBX-1210M 围板箱 1200×1000×590", "<span class=\"td-num\">15 只</span>", "成品区 RB", "2026-08-20", "<span class=\"tag tag-green\">已入库</span>"], "ops": [{"t": "详情", "act": "go('../仓储作业/其他入库详情.html?id=QTRK-20260820-001')"}]},
      'title': '其他入库单详情',
      'formTitle': '入库信息',
      'formRows': [
        { 'label': '入库单号', 'text': 'QTRK-20260820-001' },
        { 'label': '状态', 'tag': '已入库' },
        { 'label': '入库类型', 'text': '期初导入 / 手工例外入库', 'full': true },
        { 'label': '入库库位', 'text': '成品区 RB' },
        { 'label': '入库日期', 'text': '2026-08-20' },
        { 'label': '备注', 'text': '期初建账补录（历史遗留批次）', 'full': true },
        { 'label': '单据类型', 'text': '其他入库单 · 其他' },
        { 'label': '关联盘点单', 'text': '—' },
        { 'label': '制单人', 'text': '赵芳' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'itemTitle': '入库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '入库数量', '备注'],
      'items': [
        ['1', 'WBX-1210M', '围板箱 1200×1000×590', '1200×1000×590 mm', '只', '15', '期初补录 · 成品区 RB']
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
          'who': '张帆'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 其他出库单 otherOutbounds：键 = QTCK 出库单号（仓储作业/其他出库列表.html 5 行全量） */
  /* 报废/盘亏/赔偿核销/手工例外；赔偿核销=丢损赔偿联动（09-05 口径） */
  otherOutbounds: {
    'QTCK-20260905-005': {
      'row': {"fields": {"type": "赔偿核销", "material": "GB-800 隔板 · 关联赔偿单 BS-20260902-010（丢失 1 套自客户态出账）", "warehouse": "—", "date": "2026-09-05", "status": "已出库"}, "cells": ["<span class=\"tag tag-blue\">赔偿核销</span>", "GB-800 隔板 · 关联赔偿单 <span class=\"lk\">BS-20260902-010</span>（丢失 1 套自客户态出账）", "<span class=\"td-num\">1 套</span>", "—", "2026-09-05", "<span class=\"tag tag-green\">已出库</span>"], "ops": [{"t": "详情", "act": "go('../仓储作业/其他出库详情.html?id=QTCK-20260905-005')"}]},
      'title': '其他出库单详情',
      'formTitle': '出库信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'QTCK-20260905-005' },
        { 'label': '状态', 'tag': '已出库' },
        { 'label': '出库类型', 'text': '赔偿核销出库（丢损赔偿联动）', 'full': true },
        { 'label': '出库库位', 'text': '—（自客户态出账）' },
        { 'label': '出库日期', 'text': '2026-09-05' },
        { 'label': '备注', 'text': '丢失 1 套自客户态直接出账（赔偿审核即核销）', 'full': true },
        { 'label': '单据类型', 'text': '其他出库单 · 赔偿核销' },
        { 'label': '关联赔偿单', 'text': 'BS-20260902-010' },
        { 'label': '制单人', 'text': '系统' },
        { 'label': '审核人', 'text': '王芳' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '出库数量', '备注'],
      'items': [
        ['1', 'GB-800', '隔板', '—', '套', '1', '丢失件自客户态出账 · 赔偿核销']
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
          'who': '张帆'
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
      'row': {"fields": {"type": "报废", "material": "WBX-1210L", "warehouse": "成品区 RB", "date": "2026-09-01", "status": "待审核"}, "cells": ["<span class=\"tag tag-red\">报废</span>", "WBX-1210L(旧) 围板箱 旧箱体批次", "<span class=\"td-num\">35 只</span>", "成品区 RB", "2026-09-01", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "审核", "act": "go('../仓储作业/其他出库审核.html?id=QTCK-20260901-004')"}, {"t": "详情", "act": "go('../仓储作业/其他出库详情.html?id=QTCK-20260901-004')"}]},
      'title': '其他出库单详情',
      'formTitle': '出库信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'QTCK-20260901-004' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '出库类型', 'text': '报废出库（手工例外）', 'full': true },
        { 'label': '报废原因', 'text': '破损不可维修（字典：破损 PS）', 'full': true },
        { 'label': '处置方式', 'text': '资产出库 · 不可再出租', 'full': true },
        { 'label': '出库库位', 'text': '成品区 RB' },
        { 'label': '出库日期', 'text': '2026-09-01' },
        { 'label': '备注', 'text': '旧箱体批次，维修判定不可修复', 'full': true },
        { 'label': '单据类型', 'text': '其他出库单 · 报废' },
        { 'label': '制单人', 'text': '赵芳' },
        { 'label': '审核人', 'text': '—' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '出库数量', '备注'],
      'items': [
        ['1', 'WBX-1210L（旧）', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '35', '旧箱体批次 · 资产报废出库']
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
          'who': '张帆'
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
      'row': {"fields": {"type": "盘亏", "material": "LJ-F600 内衬 EPE 珍珠棉", "warehouse": "原料区 RA", "date": "2026-08-29", "status": "已完成"}, "cells": ["<span class=\"tag tag-orange\">盘亏</span>", "LJ-F600 内衬 EPE 珍珠棉", "<span class=\"td-num\">80 件</span>", "原料区 RA", "2026-08-29", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../仓储作业/其他出库详情.html?id=QTCK-20260829-003')"}]},
      'title': '其他出库单详情',
      'formTitle': '出库信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'QTCK-20260829-003' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '出库类型', 'text': '盘亏出库（盘点差异处理）', 'full': true },
        { 'label': '出库库位', 'text': '原料区 RA' },
        { 'label': '出库日期', 'text': '2026-08-29' },
        { 'label': '备注', 'text': '盘点盘亏核减（账面大于实物）', 'full': true },
        { 'label': '单据类型', 'text': '其他出库单 · 盘亏' },
        { 'label': '关联盘点单', 'text': 'PD-202608-02', 'url': '仓储作业/盘点列表.html' },
        { 'label': '制单人', 'text': '赵芳' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '出库数量', '备注'],
      'items': [
        ['1', 'LJ-F600', '内衬', 'EPE 珍珠棉 · 定制', '件', '80', '盘亏核减 · 账面调减']
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
          'who': '陈锋'
        },
        {
          't': '08-29 09:10',
          'text': '制单 · 盘亏出库（按盘点差异）',
          'who': '赵芳'
        },
        {
          't': '08-29 15:30',
          'text': '审核通过 · 账面核减',
          'who': '张帆'
        }
      ]
    },
    'QTCK-20260825-002': {
      'row': {"fields": {"type": "报废", "material": "PLT-1210W 木托盘 1200×1000", "warehouse": "成品区 RB", "date": "2026-08-25", "status": "已完成"}, "cells": ["<span class=\"tag tag-red\">报废</span>", "PLT-1210W 木托盘 1200×1000", "<span class=\"td-num\">22 块</span>", "成品区 RB", "2026-08-25", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../仓储作业/其他出库详情.html?id=QTCK-20260825-002')"}]},
      'title': '其他出库单详情',
      'formTitle': '出库信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'QTCK-20260825-002' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '出库类型', 'text': '报废出库（手工例外）', 'full': true },
        { 'label': '报废原因', 'text': '破损不可维修（字典：破损 PS）', 'full': true },
        { 'label': '处置方式', 'text': '资产出库 · 不可再出租', 'full': true },
        { 'label': '出库库位', 'text': '成品区 RB' },
        { 'label': '出库日期', 'text': '2026-08-25' },
        { 'label': '备注', 'text': '木托盘断裂批次报废', 'full': true },
        { 'label': '单据类型', 'text': '其他出库单 · 报废' },
        { 'label': '制单人', 'text': '赵芳' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '出库数量', '备注'],
      'items': [
        ['1', 'PLT-1210W', '木托盘 1200×1000', '1200×1000×144 mm', '块', '22', '资产报废出库']
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
          'who': '张帆'
        },
        {
          't': '08-25 10:20',
          'text': '制单 · 报废出库申请',
          'who': '赵芳'
        },
        {
          't': '08-25 16:40',
          'text': '审核通过 · 资产出库核减',
          'who': '张帆'
        }
      ]
    },
    'QTCK-20260815-001': {
      'row': {"fields": {"type": "其他", "material": "LJ-A100 锁扣组件 不锈钢 304", "warehouse": "原料区 RA", "date": "2026-08-15", "status": "已完成"}, "cells": ["<span class=\"tag tag-gray\">其他</span>", "LJ-A100 锁扣组件 不锈钢 304", "<span class=\"td-num\">50 件</span>", "原料区 RA", "2026-08-15", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../仓储作业/其他出库详情.html?id=QTCK-20260815-001')"}]},
      'title': '其他出库单详情',
      'formTitle': '出库信息',
      'formRows': [
        { 'label': '出库单号', 'text': 'QTCK-20260815-001' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '出库类型', 'text': '其他出库（手工例外）', 'full': true },
        { 'label': '出库库位', 'text': '原料区 RA' },
        { 'label': '出库日期', 'text': '2026-08-15' },
        { 'label': '备注', 'text': '样品领用出库（研发试用）', 'full': true },
        { 'label': '单据类型', 'text': '其他出库单 · 其他' },
        { 'label': '制单人', 'text': '赵芳' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'itemTitle': '出库明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '出库数量', '备注'],
      'items': [
        ['1', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '50', '样品领用 · 手工例外']
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
          'who': '张帆'
        }
      ]
    }
  },  /* -------------------------------------------------------------------------- */
  /* 盘点单 stocktakes：键 = PD 盘点单号（仓储作业/盘点列表.html 5 行全量） */
  /* 差异处理：盘盈→其他入库 / 盘亏报废→其他出库（S1 支线） */
  stocktakes: {
    'PD-202608-03': {
      'row': {"fields": {"scope": "华东中心仓 / 全库区", "caliber": "正常", "status": "盘点中", "checker": "张帆", "date": "2026-08-30"}, "cells": ["华东中心仓 / 全库区", "<span class=\"tag tag-green\">正常</span>", "<span class=\"td-num\">1,286</span>", "—", "<span class=\"tag tag-blue\">盘点中</span>", "张帆", "2026-08-30", "—"], "ops": [{"t": "详情", "act": "go('../仓储作业/盘点详情.html?id=PD-202608-03')"}, {"t": "录入", "act": "go('../仓储作业/盘点录入.html')"}, {"t": "审核", "act": "go('../仓储作业/盘点审核.html?id=PD-202608-03')"}]},
      'title': '盘点单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '盘点单号', 'text': 'PD-202608-03' },
        { 'label': '状态', 'tag': '盘点中' },
        { 'label': '盘点库房', 'text': '—' },
        { 'label': '盘点范围', 'text': '华东中心仓 · 全库区', 'full': true },
        { 'label': '盘点口径', 'text': '全面盘点（静态盘点）', 'full': true },
        { 'label': '盘点人', 'text': '张帆' },
        { 'label': '盘点日期', 'text': '2026-08-30' },
        { 'label': '处理方式', 'text': '—' },
        { 'label': '复盘人', 'text': '—' },
        { 'label': '备注', 'text': '—' },
        { 'label': '盘点基准', 'text': '2026-08-30 账面库存', 'full': true },
        { 'label': '账面项数', 'text': '1,286 项' },
        { 'label': '差异项数', 'text': '—（盘点中）' },
        { 'label': '上期盘点', 'text': 'PD-202608-02 · 差异 12 项已处理', 'url': '仓储作业/盘点列表.html', 'full': true }
      ],
      'itemTitle': '盘点明细（上期 PD-202608-02 示例 · 本单待生成）',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '库位', '账面数量', '实盘数量', '差异', '差异说明'],
      'items': [
        ['1', 'LJ-B200', '铰链', '锌合金 · 65mm', '件', '—', '2,520', '2,640', '+120', 'QTRK-20260901-003 盘盈入库'],
        ['2', 'WBX-1210L（旧）', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '—', '35', '0', '-35', 'QTCK-20260901-004 报废出库']
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
          'who': '张帆'
        },
        {
          't': '08-30 至今',
          'text': '库区实物清点 · 录入中',
          'who': '张帆'
        },
        {
          't': '—',
          'text': '待录入完成 → 提交审核 → 差异转处理单据',
          'off': true
        }
      ]
    },
    'PD-202608-02': {
      'row': {"fields": {"scope": "华东中心仓 / 组装区 RD", "caliber": "正常", "status": "待审核", "checker": "林国栋", "date": "2026-08-15"}, "cells": ["华东中心仓 / 组装区 RD", "<span class=\"tag tag-green\">正常</span>", "<span class=\"td-num\">36</span>", "<span class=\"td-num\" style=\"color:var(--primary)\">+18</span>", "<span class=\"tag tag-orange\">待审核</span>", "林国栋", "2026-08-15", "<span class=\"lk\">QTRK-20260816-023</span> <a class=\"docs-plus\">1</a>"], "ops": [ {"t": "生成入库", "act": "showGen('in', event)"},{"t": "详情", "act": "go('../仓储作业/盘点详情.html?id=PD-202608-02')"}, {"t": "录入", "act": "go('../仓储作业/盘点录入.html')"}, {"t": "审核", "act": "go('../仓储作业/盘点审核.html?id=PD-202608-02')"}]},
      'title': '盘点单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '盘点单号', 'text': 'PD-202608-02' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '盘点库房', 'text': '—' },
        { 'label': '盘点范围', 'text': '华东中心仓 · 组装区 RD', 'full': true },
        { 'label': '盘点口径', 'text': '全面盘点（静态盘点）', 'full': true },
        { 'label': '盘点人', 'text': '林国栋' },
        { 'label': '盘点日期', 'text': '2026-08-15' },
        { 'label': '处理方式', 'text': '—' },
        { 'label': '复盘人', 'text': '—' },
        { 'label': '备注', 'text': '—' },
        { 'label': '盘点基准', 'text': '2026-08-15 账面库存', 'full': true },
        { 'label': '账面项数', 'text': '36 项' },
        { 'label': '差异项数', 'text': '+18' },
        { 'label': '上期盘点', 'text': 'PD-202607-02 · 差异 2 项已处理', 'url': '仓储作业/盘点列表.html', 'full': true }
      ],
      'itemTitle': '盘点明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '库位', '账面数量', '实盘数量', '差异', '差异说明'],
      'items': [
        ['1', 'LJ-B200', '铰链', '锌合金 · 65mm', '件', '组装区 RD', '2,520', '2,640', '+120', 'QTRK-20260901-003 盘盈入库'],
        ['2', 'WBX-1210L（旧）', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '组装区 RD', '35', '0', '-35', 'QTCK-20260901-004 报废出库']
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
          'who': '林国栋'
        },
        {
          't': '08-31 18:00',
          'text': '盘点完成 · 差异 2 项（+120 / -35）',
          'who': '林国栋'
        },
        {
          't': '—',
          'text': '待审核 · 差异已转处理单据（QTRK/QTCK）',
          'off': true
        }
      ]
    },
    'PD-202607-02': {
      'row': {"fields": {"scope": "华东中心仓 / 成品区 RB", "caliber": "在租", "status": "已完成", "checker": "林国栋", "date": "2026-07-31"}, "cells": ["华东中心仓 / 成品区 RB", "<span class=\"tag tag-blue\">在租</span>", "<span class=\"td-num\">86</span>", "<span class=\"td-num\" style=\"color:var(--danger)\">-2</span>", "<span class=\"tag tag-green\">已完成</span>", "林国栋", "2026-07-31", "<span class=\"lk\">QTCK-20260731-005</span> <a class=\"docs-plus\">2</a>"], "ops": [ {"t": "生成出库", "act": "showGen('out', event)"},{"t": "详情", "act": "go('../仓储作业/盘点详情.html?id=PD-202607-02')"}, {"t": "录入", "act": "go('../仓储作业/盘点录入.html')"}, {"t": "审核", "act": "go('../仓储作业/盘点审核.html?id=PD-202607-02')"}]},
      'title': '盘点单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '盘点单号', 'text': 'PD-202607-02' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '盘点库房', 'text': '—' },
        { 'label': '盘点范围', 'text': '华东中心仓 · 成品区 RB', 'full': true },
        { 'label': '盘点口径', 'text': '全面盘点（静态盘点）', 'full': true },
        { 'label': '盘点人', 'text': '林国栋' },
        { 'label': '盘点日期', 'text': '2026-07-31' },
        { 'label': '处理方式', 'text': '—' },
        { 'label': '复盘人', 'text': '—' },
        { 'label': '备注', 'text': '—' },
        { 'label': '盘点基准', 'text': '2026-07-31 账面库存', 'full': true },
        { 'label': '账面项数', 'text': '86 项' },
        { 'label': '差异项数', 'text': '-2' },
        { 'label': '上期盘点', 'text': 'PD-202607-01', 'url': '仓储作业/盘点列表.html', 'full': true }
      ],
      'itemTitle': '盘点明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '库位', '账面数量', '实盘数量', '差异', '差异说明'],
      'items': [
        ['1', 'ZH-2602-B', '冲压件料箱组套', '—', '套', '成品区 RB', '4,122', '4,120', '-2', '盘亏核减（历史处理）']
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
          'who': '林国栋'
        },
        {
          't': '08-01 16:40',
          'text': '盘点完成 · 差异 -2 已核减',
          'who': '林国栋'
        }
      ]
    },
    'PD-202607-01': {
      'row': {"fields": {"scope": "华东中心仓 / 原料区 RA", "caliber": "正常", "status": "已完成", "checker": "张帆", "date": "2026-07-31"}, "cells": ["华东中心仓 / 原料区 RA", "<span class=\"tag tag-green\">正常</span>", "<span class=\"td-num\">642</span>", "<span class=\"td-num\">0</span>", "<span class=\"tag tag-green\">已完成</span>", "张帆", "2026-07-31", "—"], "ops": [{"t": "详情", "act": "go('../仓储作业/盘点详情.html?id=PD-202607-01')"}, {"t": "录入", "act": "go('../仓储作业/盘点录入.html')"}, {"t": "审核", "act": "go('../仓储作业/盘点审核.html?id=PD-202607-01')"}]},
      'title': '盘点单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '盘点单号', 'text': 'PD-202607-01' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '盘点库房', 'text': '—' },
        { 'label': '盘点范围', 'text': '华东中心仓 · 原料区 RA', 'full': true },
        { 'label': '盘点口径', 'text': '全面盘点（静态盘点）', 'full': true },
        { 'label': '盘点人', 'text': '张帆' },
        { 'label': '盘点日期', 'text': '2026-07-31' },
        { 'label': '处理方式', 'text': '—' },
        { 'label': '复盘人', 'text': '—' },
        { 'label': '备注', 'text': '—' },
        { 'label': '盘点基准', 'text': '2026-07-31 账面库存', 'full': true },
        { 'label': '账面项数', 'text': '642 项' },
        { 'label': '差异项数', 'text': '0' },
        { 'label': '上期盘点', 'text': 'PD-202606-01', 'url': '仓储作业/盘点列表.html', 'full': true }
      ],
      'itemTitle': '盘点明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '库位', '账面数量', '实盘数量', '差异', '差异说明'],
      'items': [
        ['1', '—', '—', '—', '—', '原料区 RA', '—', '—', '0', '无差异']
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
          'who': '张帆'
        },
        {
          't': '08-01 10:20',
          'text': '盘点完成 · 无差异',
          'who': '张帆'
        }
      ]
    },
    'PD-202606-01': {
      'row': {"fields": {"scope": "华东中心仓 / 退货区 RC", "caliber": "正常", "status": "已完成", "checker": "张帆", "date": "2026-06-30"}, "cells": ["华东中心仓 / 退货区 RC", "<span class=\"tag tag-green\">正常</span>", "<span class=\"td-num\">128</span>", "<span class=\"td-num\" style=\"color:var(--primary)\">+3</span>", "<span class=\"tag tag-green\">已完成</span>", "张帆", "2026-06-30", "<span class=\"lk\">QTRK-20260630-011</span>"], "ops": [ {"t": "生成入库", "act": "showGen('in', event)"},{"t": "详情", "act": "go('../仓储作业/盘点详情.html?id=PD-202606-01')"}, {"t": "录入", "act": "go('../仓储作业/盘点录入.html')"}, {"t": "审核", "act": "go('../仓储作业/盘点审核.html?id=PD-202606-01')"}]},
      'title': '盘点单详情',
      'formTitle': '基本信息',
      'formRows': [
        { 'label': '盘点单号', 'text': 'PD-202606-01' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '盘点库房', 'text': '—' },
        { 'label': '盘点范围', 'text': '华东中心仓 · 退货区 RC', 'full': true },
        { 'label': '盘点口径', 'text': '全面盘点（静态盘点）', 'full': true },
        { 'label': '盘点人', 'text': '张帆' },
        { 'label': '盘点日期', 'text': '2026-06-30' },
        { 'label': '处理方式', 'text': '—' },
        { 'label': '复盘人', 'text': '—' },
        { 'label': '备注', 'text': '—' },
        { 'label': '盘点基准', 'text': '2026-06-30 账面库存', 'full': true },
        { 'label': '账面项数', 'text': '128 项' },
        { 'label': '差异项数', 'text': '+3' },
        { 'label': '上期盘点', 'text': 'PD-202607-01', 'url': '仓储作业/盘点列表.html', 'full': true }
      ],
      'itemTitle': '盘点明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '库位', '账面数量', '实盘数量', '差异', '差异说明'],
      'items': [
        ['1', 'LJ-D400', '箱盖', 'ABS 吸塑 · 1200×1000', '件', '退货区 RC', '297', '300', '+3', '盘盈补录（历史处理）']
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
          'who': '张帆'
        },
        {
          't': '07-01 15:10',
          'text': '盘点完成 · 盘盈 +3 已补录',
          'who': '张帆'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 库存调拨 transfers：键 = DB 调拨单号（仓储作业/库存调拨列表.html 3 行全量） */
  /* 调拨不变总量 · 仅变动库区分布 */
  transfers: {
    'DB-20260901-003': {
      'row': {"fields": {"material": "LJ-A100 锁扣组件 不锈钢 304", "frm": "原料区 RA", "to": "成品区 RB", "date": "2026-09-01", "status": "待审核"}, "cells": ["LJ-A100 锁扣组件 不锈钢 304", "<span class=\"td-num\">1,000 件</span>", "原料区 RA", "成品区 RB", "2026-09-01", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "审核", "act": "go('../仓储作业/调拨审核.html?id=DB-20260901-003')"}, {"t": "详情", "act": "go('../仓储作业/调拨详情.html?id=DB-20260901-003')"}]},
      'title': '调拨单详情',
      'formTitle': '调拨信息',
      'formRows': [
        { 'label': '调拨单号', 'text': 'DB-20260901-003' },
        { 'label': '状态', 'tag': '待审核' },
        { 'label': '调出库位', 'text': '原料区 RA' },
        { 'label': '调入库位', 'text': '成品区 RB' },
        { 'label': '调拨类型', 'text': '库区内调拨' },
        { 'label': '调拨原因', 'text': '组装备料（ZH-2601-A 组装线需求）', 'full': true },
        { 'label': '调拨日期', 'text': '2026-09-01' },
        { 'label': '备注', 'text': '调拨不影响库存总量，仅变动库区分布', 'full': true },
        { 'label': '制单人', 'text': '赵芳' },
        { 'label': '审核人', 'text': '—' }
      ],
      'itemTitle': '调拨明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '调拨数量', '备注'],
      'items': [
        ['1', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '600', 'ZH-2601-A 组装线备料'],
        ['2', 'LJ-B200', '铰链', '锌合金 · 65mm', '件', '400', '—'],
        ['3', 'LJ-D400', '箱盖', 'ABS 吸塑 · 1200×1000', '件', '300', '—']
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
      'row': {"fields": {"material": "WBX-1210L 围板箱 1200×1000×970", "frm": "成品区 RB", "to": "外协周转区 RC", "date": "2026-08-26", "status": "已完成"}, "cells": ["WBX-1210L 围板箱 1200×1000×970", "<span class=\"td-num\">200 只</span>", "成品区 RB", "外协周转区 RC", "2026-08-26", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../仓储作业/调拨详情.html?id=DB-20260826-002')"}]},
      'title': '调拨单详情',
      'formTitle': '调拨信息',
      'formRows': [
        { 'label': '调拨单号', 'text': 'DB-20260826-002' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '调出库位', 'text': '成品区 RB' },
        { 'label': '调入库位', 'text': '外协周转区 RC' },
        { 'label': '调拨类型', 'text': '库区间调拨' },
        { 'label': '调拨原因', 'text': '外协周转备货（客户产线周边仓）', 'full': true },
        { 'label': '调拨日期', 'text': '2026-08-26' },
        { 'label': '备注', 'text': '调拨不影响库存总量，仅变动库区分布', 'full': true },
        { 'label': '制单人', 'text': '赵芳' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'itemTitle': '调拨明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '调拨数量', '备注'],
      'items': [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '200', '外协周转备货']
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
          'who': '张帆'
        }
      ]
    },
    'DB-20260812-001': {
      'row': {"fields": {"material": "PLT-1210P 塑料托盘 1200×1000", "frm": "成品区 RB", "to": "原料区 RA", "date": "2026-08-12", "status": "已完成"}, "cells": ["PLT-1210P 塑料托盘 1200×1000", "<span class=\"td-num\">300 块</span>", "成品区 RB", "原料区 RA", "2026-08-12", "<span class=\"tag tag-green\">已完成</span>"], "ops": [{"t": "详情", "act": "go('../仓储作业/调拨详情.html?id=DB-20260812-001')"}]},
      'title': '调拨单详情',
      'formTitle': '调拨信息',
      'formRows': [
        { 'label': '调拨单号', 'text': 'DB-20260812-001' },
        { 'label': '状态', 'tag': '已完成' },
        { 'label': '调出库位', 'text': '成品区 RB' },
        { 'label': '调入库位', 'text': '原料区 RA' },
        { 'label': '调拨类型', 'text': '库区间调拨' },
        { 'label': '调拨原因', 'text': '零部件区辅料补库（托盘周转）', 'full': true },
        { 'label': '调拨日期', 'text': '2026-08-12' },
        { 'label': '备注', 'text': '调拨不影响库存总量，仅变动库区分布', 'full': true },
        { 'label': '制单人', 'text': '赵芳' },
        { 'label': '审核人', 'text': '张帆' }
      ],
      'itemTitle': '调拨明细',
      'itemCols': ['序号', '物料编码', '物料名称', '规格', '单位', '调拨数量', '备注'],
      'items': [
        ['1', 'PLT-1210P', '塑料托盘 1200×1000', '1200×1000×150 mm', '块', '300', '托盘周转补库']
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
          'who': '张帆'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 库存流水 stockFlows：键 = 物料编码（仓储作业/库存查询.html 散件 9 + 组合件 3） */
  /* 弹窗 flowModal · 触发锚「库存流水」；状态口径 + 进出流水时间倒序 */
  stockFlows: {
     'XNC-AJZX-WBX': {
      'row': {"fields": {"status": "客户端(租出)", "name": "围板箱 1200×1000×970（安吉智行·客户虚拟仓）", "cls": "围板箱", "project": "PRJ-2605", "area": "客户虚拟仓", "loc": "XNC-AJZX", "loc": "XNC-AJZX", "qtyByProject": {"PRJ-2605": [0, 0, 640, 0]}}, "cells": ["围板箱 1200×1000×970（安吉智行·客户虚拟仓）", "<span class=\"tag tag-blue\">围板箱</span>", "PRJ-2605", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">640</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>640</b></span>", "<span class=\"td-num\">340.00</span>", "只", "客户虚拟仓"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=XNC-AJZX-WBX')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}, {"t": "转移出库", "act": "go('../租赁管理/转移出库新建.html?mat=围板箱 1200×1000×970&cust=安吉智行物流')"}]},
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
          'text': '围板箱'
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
          'label': '库房',
          'text': '安吉智行·客户虚拟仓'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['09-02', '租赁出库', 'CK-20260824-009', '+640', '640'],
          'links': {
            2: '租赁管理/租赁出库列表.html'
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
          'role': '租赁出库',
          'name': 'CK-20260824-009 · 出库至客户',
          'url': '租赁管理/租赁出库列表.html'
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
          'text': '租赁出库 640 只至安吉智行 · 按客户归集记客户虚拟仓（on-hire）',
          'who': '张帆'
        }
      ]
    },
   'LJ-A100': {
      'row': {"fields": {"status": "在库", "name": "锁扣组件 不锈钢 304", "cls": "零部件", "project": "PRJ-2601/PRJ-2602/PRJ-2604", "area": "原料区 RA", "loc": "RA-A-01-01", "loc": "RA-A-01-01", "qtyByProject": {"PRJ-2601": [2500, 700, 500, 1200], "PRJ-2602": [1600, 300, 200, 800], "PRJ-2604": [1160, 200, 100, 400]}}, "cells": ["锁扣组件 不锈钢 304", "<span class=\"tag tag-blue\">零部件</span>", "PRJ-2601/PRJ-2602/PRJ-2604", "<span class=\"td-num\">5,260</span>", "<span class=\"td-num\">1,200</span>", "<span class=\"td-num\">800</span>", "<span class=\"td-num\">2,400</span>", "<span class=\"td-num\"><b>9,660</b></span>", "<span class=\"td-num\">1.60</span>", "件", "原料区 RA"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=LJ-A100')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
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
          'label': '退租在途（待入库）',
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
          'label': '库房',
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
          'who': '张帆'
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
      'row': {"fields": {"status": "在库", "name": "铰链 锌合金 65mm", "cls": "零部件", "project": "PRJ-2601/PRJ-2602", "area": "原料区 RA", "loc": "RA-A-01-02", "loc": "RA-A-01-02", "qtyByProject": {"PRJ-2601": [1500, 250, 1000, 0], "PRJ-2602": [1140, 150, 600, 0]}}, "cells": ["铰链 锌合金 65mm", "<span class=\"tag tag-blue\">零部件</span>", "PRJ-2601/PRJ-2602", "<span class=\"td-num\">2,640</span>", "<span class=\"td-num\">400</span>", "<span class=\"td-num\">1,600</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>4,640</b></span>", "<span class=\"td-num\">1.10</span>", "件", "原料区 RA"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=LJ-B200')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
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
          'label': '退租在途（待入库）',
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
          'label': '库房',
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
          'who': '张帆'
        }
      ]
    },
    'LJ-C300': {
      'row': {"fields": {"status": "在库", "name": "围板 HDPE 波纹板", "cls": "零部件", "project": "PRJ-2601", "area": "成品区 RB", "loc": "RB-A-01-01", "loc": "RB-A-01-01", "qtyByProject": {"PRJ-2601": [1860, 0, 1600, 0]}}, "cells": ["围板 HDPE 波纹板", "<span class=\"tag tag-blue\">零部件</span>", "PRJ-2601", "<span class=\"td-num\">1,860</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">1,600</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>3,460</b></span>", "<span class=\"td-num\">8.20</span>", "件", "成品区 RB"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=LJ-C300')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
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
          'label': '退租在途（待入库）',
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
          'label': '库房',
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
          'who': '张帆'
        },
        {
          't': '08-30',
          'text': '组装领料 -600 · ZZ-20260830-004（300 套 × 2）',
          'who': '刘志强'
        }
      ]
    },
    'LJ-D400': {
      'row': {"fields": {"status": "退租待入库", "name": "箱盖 ABS 吸塑", "cls": "零部件", "project": "PRJ-2601/PRJ-2604", "area": "成品区 RB", "loc": "RB-A-01-02", "loc": "RB-A-01-02", "qtyByProject": {"PRJ-2601": [580, 280, 250, 600], "PRJ-2604": [400, 200, 150, 400]}}, "cells": ["箱盖 ABS 吸塑", "<span class=\"tag tag-blue\">零部件</span>", "PRJ-2601/PRJ-2604", "<span class=\"td-num\">980</span>", "<span class=\"td-num\">480</span>", "<span class=\"td-num\">400</span>", "<span class=\"td-num\">1,000</span>", "<span class=\"td-num\"><b>2,860</b></span>", "<span class=\"td-num\">3.60</span>", "件", "成品区 RB"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=LJ-D400')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
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
          'label': '退租在途（待入库）',
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
          'label': '库房',
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
          'name': '来源 · 甬城塑业',
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
          'who': '张帆'
        },
        {
          't': '08-28',
          'text': '退货入库 +300 · QTRK-20260828-002',
          'who': '张帆'
        }
      ]
    },
    'LJ-F600': {
      'row': {"fields": {"status": "在库", "name": "内衬 EPE 珍珠棉", "cls": "内衬", "project": "PRJ-2603/PRJ-2605", "area": "原料区 RA", "loc": "RA-A-01-01", "loc": "RA-A-01-01", "qtyByProject": {"PRJ-2603": [900, 70, 0, 0], "PRJ-2605": [620, 50, 0, 0]}}, "cells": ["内衬 EPE 珍珠棉", "<span class=\"tag tag-blue\">内衬</span>", "PRJ-2603/PRJ-2605", "<span class=\"td-num\">1,520</span>", "<span class=\"td-num\">120</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>1,640</b></span>", "<span class=\"td-num\">0.90</span>", "件", "原料区 RA"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=LJ-F600')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}]},
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
          'text': '内衬'
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
          'label': '退租在途（待入库）',
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
          'label': '库房',
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
          'who': '林国栋'
        }
      ]
    },
    'WBX-1210L': {
      'row': {"fields": {"status": "客户端(租出)", "name": "围板箱 1200×1000×970", "cls": "围板箱", "project": "PRJ-2601/PRJ-2604", "area": "原料区 RA", "loc": "RA-A-01-02", "loc": "RA-A-01-02", "qtyByProject": {"PRJ-2601": [1200, 100, 1800, 50], "PRJ-2604": [920, 60, 1320, 30]}}, "cells": ["围板箱 1200×1000×970", "<span class=\"tag tag-green\">围板箱</span>", "PRJ-2601/PRJ-2604", "<span class=\"td-num\">2,120</span>", "<span class=\"td-num\">160</span>", "<span class=\"td-num\">3,120</span>", "<span class=\"td-num\">80</span>", "<span class=\"td-num\"><b>5,480</b></span>", "<span class=\"td-num\">340.00</span>", "只", "原料区 RA"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=WBX-1210L')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}, {"t": "转移出库", "act": "go('../租赁管理/转移出库新建.html?mat=围板箱 1200×1000×970&cust=华骏重卡汽车有限公司')"}]},
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
          'text': '围板箱'
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
          'label': '退租在途（待入库）',
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
          'label': '库房',
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
          'role': '租赁出库 / 租出',
          'name': '去向 · ZH-2601-A 组装与出租',
          'url': '租赁管理/租赁出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '09-01',
          'text': '采购入库 +300 · CGRK-20260828-011（甬城塑业）',
          'who': '张帆'
        },
        {
          't': '09-02',
          'text': '拆卸产出 +50 · CX-20260902-006',
          'who': '张帆'
        }
      ]
    },
    'WBX-1210M': {
      'row': {"fields": {"status": "客户端(租出)", "name": "围板箱 1200×1000×590", "cls": "围板箱", "project": "PRJ-2602", "area": "成品区 RB", "loc": "RB-A-01-01", "loc": "RB-A-01-01", "qtyByProject": {"PRJ-2602": [860, 40, 1020, 0]}}, "cells": ["围板箱 1200×1000×590", "<span class=\"tag tag-green\">围板箱</span>", "PRJ-2602", "<span class=\"td-num\">860</span>", "<span class=\"td-num\">40</span>", "<span class=\"td-num\">1,020</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>1,920</b></span>", "<span class=\"td-num\">296.00</span>", "只", "成品区 RB"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=WBX-1210M')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}, {"t": "转移出库", "act": "go('../租赁管理/转移出库新建.html?mat=围板箱 1200×1000×590&cust=华骏重卡汽车有限公司')"}]},
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
          'text': '围板箱'
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
          'label': '退租在途（待入库）',
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
          'label': '库房',
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
      'row': {"fields": {"status": "客户端(租出)", "name": "塑料托盘 1200×1000", "cls": "塑料托盘", "project": "PRJ-2602/PRJ-2603", "area": "成品区 RB", "loc": "RB-A-01-02", "loc": "RB-A-01-02", "qtyByProject": {"PRJ-2602": [800, 0, 1100, 40], "PRJ-2603": [610, 0, 760, 20]}}, "cells": ["塑料托盘 1200×1000", "<span class=\"tag tag-green\">塑料托盘</span>", "PRJ-2602/PRJ-2603", "<span class=\"td-num\">1,410</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">1,860</span>", "<span class=\"td-num\">60</span>", "<span class=\"td-num\"><b>3,330</b></span>", "<span class=\"td-num\">98.00</span>", "块", "成品区 RB"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=PLT-1210P')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}, {"t": "转移出库", "act": "go('../租赁管理/转移出库新建.html?mat=塑料托盘 1200×1000&cust=华骏重卡汽车有限公司')"}]},
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
          'text': '塑料托盘'
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
          'label': '退租在途（待入库）',
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
          'label': '库房',
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
          'text': '采购入库 +500 · CGRK-20260825-006（延陵托盘）',
          'who': '张帆'
        },
        {
          't': '08-26',
          'text': '拆卸产出 +30 · CX-20260826-004',
          'who': '张帆'
        }
      ]
    },
    'BTC-6040': {
      'row': {"fields": {"status": "客户端(租出)", "name": "料箱 600×400×340", "cls": "料箱", "project": "PRJ-2602", "area": "原料区 RA", "loc": "RA-A-01-01", "loc": "RA-A-01-01", "qtyByProject": {"PRJ-2602": [3300, 40, 2480, 120]}}, "cells": ["料箱 600×400×340", "<span class=\"tag tag-green\">料箱</span>", "PRJ-2602", "<span class=\"td-num\">3,300</span>", "<span class=\"td-num\">40</span>", "<span class=\"td-num\">2,480</span>", "<span class=\"td-num\">120</span>", "<span class=\"td-num\"><b>5,940</b></span>", "<span class=\"td-num\">76.50</span>", "只", "原料区 RA"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=BTC-6040')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}, {"t": "转移出库", "act": "go('../租赁管理/转移出库新建.html?mat=料箱 600×400×340&cust=华骏重卡汽车有限公司')"}]},
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
          'text': '料箱'
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
          'label': '退租在途（待入库）',
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
          'label': '库房',
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
          'text': '采购入库 +800 · CGRK-20260826-008（甬城塑业）',
          'who': '张帆'
        },
        {
          't': '08-30',
          'text': '拆卸产出 +40 · CX-20260830-005',
          'who': '张帆'
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
          'label': '退租在途（待入库）',
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
          'label': '库房',
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
          'cells': ['09-03', '租赁出库', 'CK-20260903-016', '-60', '608'],
          'links': {
            2: '租赁管理/租赁出库列表.html'
          }
        },
        {
          'cells': ['09-02', '拆卸出库', 'CX-20260902-006', '-50', '668']
        },
        {
          'cells': ['08-30', '租赁出库', 'CK-20260830-015', '-180', '718'],
          'links': {
            2: '租赁管理/租赁出库列表.html'
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
          'role': '租赁出库',
          'name': '租出 · CK 系列出库',
          'url': '租赁管理/租赁出库列表.html'
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
          'who': '张帆'
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
          'label': '退租在途（待入库）',
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
          'label': '库房',
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
          'cells': ['08-28', '租赁出库', 'CK-20260828-010', '-200', '860'],
          'links': {
            2: '租赁管理/租赁出库列表.html'
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
          'role': '租赁出库',
          'name': '租出 · CK 系列出库',
          'url': '租赁管理/租赁出库列表.html'
        }
      ],
      'timeline': [
        {
          't': '08-28',
          'text': '租赁出库 -200 · CK-20260828-010',
          'who': '张帆'
        },
        {
          't': '08-30',
          'text': '拆卸出库 -40 · CX-20260830-005（散件需求）',
          'who': '张帆'
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
          'label': '退租在途（待入库）',
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
          'label': '库房',
          'text': '成品区 RB'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['08-29', '租赁出库', 'CK-20260829-013', '-60', '150'],
          'links': {
            2: '租赁管理/租赁出库列表.html'
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
          'role': '租赁出库',
          'name': '租出 · CK-20260829-013',
          'url': '租赁管理/租赁出库列表.html'
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
          'text': '租赁出库 -60 · CK-20260829-013',
          'who': '张帆'
        }
      ]
    },
   'XNC-ZZ-WBX': {
      'row': {"fields": {"name": "围板箱 1200×1000×970（安吉智行·转租终端用户）", "cls": "围板箱", "project": "PRJ-2605", "area": "转租终端仓", "loc": "—", "loc": "—", "status": "客户转租出", "qtyByProject": {"PRJ-2605": [0, 0, 240, 0]}}, "cells": ["围板箱 1200×1000×970（安吉智行·转租终端用户）", "<span class=\"tag tag-blue\">围板箱</span>", "PRJ-2605", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">240</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>240</b></span>", "<span class=\"td-num\">340.00</span>", "只", "转租终端仓"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=XNC-ZZ-WBX')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}, {"t": "终止转移", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260914-001')"}]},
      'title': '库存流水',
      'titleNo': 'XNC-ZZ-WBX 围板箱 1200×1000×970（转租终端用户）',
      'info': [
        {
          'label': '物料编码',
          'text': 'XNC-ZZ-WBX'
        },
        {
          'label': '名称规格',
          'text': '围板箱 1200×1000×970（安吉智行·转租终端用户）',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '围板箱'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2605',
          'full': true
        },
        {
          'label': '库存状态',
          'text': '客户转租出'
        },
        {
          'label': '在租数量',
          'text': '240 只（客户安吉智行转租给终端用户）',
          'full': true
        },
        {
          'label': '成本单价',
          'text': '340.00 元（未税 · 最近采购入库价）'
        },
        {
          'label': '库房',
          'text': '安吉智行·转租终端仓'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['09-06', '租赁出库·转租', 'CK-20260905-012', '+240', '240'],
          'links': {
            2: '租赁管理/租赁出库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260815-005 · 环通',
          'url': '租入管理/租入单列表.html'
        },
        {
          'role': '租赁单',
          'name': 'ZL-20260905-034 · 客户安吉智行',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '转租终端仓（本仓）',
          'name': 'XNC-ZZ-WBX · 转租 240 只',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '09-06',
          'text': '客户安吉智行转租终端用户 · 240 只（客户转租出＝在租子状态）',
          'who': '沈婷'
        }
      ]
    },
   'XNC-ZZ-PLT': {
      'row': {"fields": {"name": "塑料托盘 1200×1000（安吉智行·客户虚拟仓）", "cls": "塑料托盘", "project": "PRJ-2605", "area": "客户虚拟仓", "loc": "XNC-AJZX", "loc": "XNC-AJZX", "status": "客户端(租出)", "qtyByProject": {"PRJ-2605": [0, 0, 120, 0]}}, "cells": ["塑料托盘 1200×1000（安吉智行·客户虚拟仓）", "<span class=\"tag tag-blue\">塑料托盘</span>", "PRJ-2605", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">120</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>120</b></span>", "<span class=\"td-num\">98.00</span>", "块", "客户虚拟仓"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=XNC-ZZ-PLT')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}, {"t": "转移出库", "act": "go('../租赁管理/转移出库新建.html?mat=塑料托盘 1200×1000&cust=安吉智行物流')"}]},
      'title': '库存流水',
      'titleNo': 'XNC-ZZ-PLT 塑料托盘 1200×1000（转租终端用户）',
      'info': [
        {
          'label': '物料编码',
          'text': 'XNC-ZZ-PLT'
        },
        {
          'label': '名称规格',
          'text': '塑料托盘 1200×1000（安吉智行·转租终端用户）',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '塑料托盘'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2605',
          'full': true
        },
        {
          'label': '库存状态',
          'text': '客户转租出'
        },
        {
          'label': '在租数量',
          'text': '120 块（客户安吉智行转租给终端用户）',
          'full': true
        },
        {
          'label': '成本单价',
          'text': '98.00 元（未税 · 最近采购入库价）'
        },
        {
          'label': '库房',
          'text': '安吉智行·客户虚拟仓（转移已终止·回在租）'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['09-06', '租赁出库·转租', 'CK-20260905-012', '+120', '120'],
          'links': {
            2: '租赁管理/租赁出库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260815-005 · 环通',
          'url': '租入管理/租入单列表.html'
        },
        {
          'role': '租赁单',
          'name': 'ZL-20260905-034 · 客户安吉智行',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '客户虚拟仓（本仓·转移已终止）',
          'name': 'XNC-ZZ-PLT · 转租 120 块',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '09-06',
          'text': '客户安吉智行转租终端用户 · 120 块（客户转租出＝在租子状态）',
          'who': '沈婷'
        }
      ]
    },
   'XNC-ZZ-BTC': {
      'row': {"fields": {"name": "料箱 600×400×340（安吉智行·转租终端用户）", "cls": "料箱", "project": "PRJ-2605", "area": "转租终端仓", "loc": "—", "loc": "—", "status": "客户转租出", "qtyByProject": {"PRJ-2605": [0, 0, 360, 0]}}, "cells": ["料箱 600×400×340（安吉智行·转租终端用户）", "<span class=\"tag tag-blue\">料箱</span>", "PRJ-2605", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">360</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>360</b></span>", "<span class=\"td-num\">76.50</span>", "只", "转租终端仓"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=XNC-ZZ-BTC')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}, {"t": "终止转移", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260914-003')"}]},
      'title': '库存流水',
      'titleNo': 'XNC-ZZ-BTC 料箱 600×400×340（转租终端用户）',
      'info': [
        {
          'label': '物料编码',
          'text': 'XNC-ZZ-BTC'
        },
        {
          'label': '名称规格',
          'text': '料箱 600×400×340（安吉智行·转租终端用户）',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '料箱'
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2605',
          'full': true
        },
        {
          'label': '库存状态',
          'text': '客户转租出'
        },
        {
          'label': '在租数量',
          'text': '360 只（客户安吉智行转租给终端用户）',
          'full': true
        },
        {
          'label': '成本单价',
          'text': '76.50 元（未税 · 最近采购入库价）'
        },
        {
          'label': '库房',
          'text': '安吉智行·转租终端仓'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['09-06', '租赁出库·转租', 'CK-20260905-012', '+360', '360'],
          'links': {
            2: '租赁管理/租赁出库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260815-005 · 环通',
          'url': '租入管理/租入单列表.html'
        },
        {
          'role': '租赁单',
          'name': 'ZL-20260905-034 · 客户安吉智行',
          'url': '租赁管理/租赁单列表.html'
        },
        {
          'role': '转租终端仓（本仓）',
          'name': 'XNC-ZZ-BTC · 转租 360 只',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '09-06',
          'text': '客户安吉智行转租终端用户 · 360 只（客户转租出＝在租子状态）',
          'who': '沈婷'
        }
      ]
    },
    'XNC-ZZ-PLT2': {
      'row': {"fields": {"name": "塑料托盘 1200×1000（长丰锂电·转租终端用户）", "cls": "塑料托盘", "project": "PRJ-2603", "area": "转租终端仓", "loc": "—", "status": "客户转租出", "qtyByProject": {"PRJ-2603": [0, 0, 80, 0]}}, "cells": ["塑料托盘 1200×1000（长丰锂电·转租终端用户）", "<span class=\"tag tag-blue\">塑料托盘</span>", "PRJ-2603", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">80</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>80</b></span>", "<span class=\"td-num\">98.00</span>", "张", "转租终端仓"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=XNC-ZZ-PLT2')"}, {"t": "客户在租", "act": "openModal('rentDrillModal')"}, {"t": "终止转移", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260914-002')"}]},
    },

    'RZRK-20260910-024': {
      'row': {"fields": {"status": "租入", "name": "围板箱 1200×1000×970（环通租入 · 在库未转租）", "cls": "围板箱", "project": "PRJ-2603", "area": "上海一号库", "loc": "—", "loc": "—", "qtyByProject": {"PRJ-2603": [500, 0, 0, 0]}}, "cells": ["围板箱 1200×1000×970（环通租入）", "<span class=\"tag tag-blue\">围板箱</span>", "PRJ-2603", "<span class=\"td-num\">500</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\"><b>500</b></span>", "<span class=\"td-num\">340.00</span>", "只", "上海一号库"], "ops": [{"t": "库存流水", "act": "go('../仓储作业/库存流水.html?id=RZRK-20260910-024')"}]},
      'title': '库存流水',
      'titleNo': 'RZRK-20260910-024 围板箱（环通租入 · 在库未转租）',
      'info': [
        {
          'label': '物料编码',
          'text': 'WBX-1210L'
        },
        {
          'label': '名称规格',
          'text': '围板箱 1200×1000×970（环通租入）',
          'full': true
        },
        {
          'label': '物料类别',
          'text': '围板箱'
        },
        {
          'label': '资产来源',
          'tag': '租入'
        },
        {
          'label': '供应商',
          'text': '环通循环包装运营（上海）有限公司',
          'full': true
        },
        {
          'label': '适用项目',
          'text': 'PRJ-2603',
          'full': true
        },
        {
          'label': '在库（租入）',
          'text': '500 只'
        },
        {
          'label': '口径',
          'text': '租入＝租入在库未转租，转租后计入客户态（来源标记区分）',
          'full': true
        },
        {
          'label': '库房',
          'text': '上海一号库'
        }
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {
          'cells': ['09-10', '租入入库', 'RZRK-20260910-024', '+500', '500'],
          'links': {
            2: '租入管理/租入入库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '租入单',
          'name': 'RZD-20260815-003 · 环通',
          'url': '租入管理/租入单列表.html'
        },
        {
          'role': '租入库批次（本批）',
          'name': 'RZRK-20260910-024 · 上海一号库',
          'self': true
        },
        {
          'role': '转租客户（未发生）',
          'name': '转租后计入客户态 · 来源标记区分'
        }
      ],
      'timeline': [
        {
          't': '09-10',
          'text': '租入入库 +500 · 环通（在库未转租 · 计入租入态）',
          'who': '张帆'
        }
      ]
    },

  },

  /* -------------------------------------------------------------------------- */
  /* 器具出租履历 rentTracks：键 = ZL 租赁单号（原宿主 租出台账 2026-09-10 并入租赁单列表；现供 租赁管理/器具出租履历.html 页面渲染（G36 B3 页面化）） */
  /* 弹窗 trackModal · 触发锚「详情」；含循环再出租/部分退租/超期场景 */
  rentTracks: {
    'ZL-20260903-034': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "combo": "ZH-2601-A × 60 套（退租回库件再出租）", "src": "自有", "date": "2026-09-03", "back": "2026-12-03", "status": "在租"}, "cells": ["PRJ-2601", "华骏重卡汽车有限公司", "ZH-2601-A × 60 套（退租回库件再出租）", "自有", "<span class=\"td-num\">2026-09-03</span>", "2026-12-03", "<span class=\"td-num\">0 套</span>", "<span class=\"tag tag-blue\">在租</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
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
          'text': '华骏重卡汽车有限公司',
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
          'cells': ['1', 'ZL-20260903-034', '华骏重卡汽车有限公司', '09-03', '—', '60 套', '在租'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        },
        {
          'cells': ['2', 'ZL-20260610-015', '华骏重卡汽车有限公司', '06-15', '09-02', '60 套', '已退租（前手 · 回库件循环）'],
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
          'who': '张帆'
        },
        {
          't': '09-03',
          'text': '循环再出租 · ZL-20260903-034',
          'who': '沈婷'
        }
      ]
    },
    'ZL-20260823-033': {
      'row': {"fields": {"project": "PRJ-2604", "customer": "华骏重卡汽车有限公司", "combo": "ZH-2604-D × 40 套", "src": "混合（自购 + 租入）", "date": "2026-08-23", "back": "2026-11-23", "status": "已退租"}, "note": "1", "cells": ["PRJ-2604", "华骏重卡汽车有限公司", "ZH-2604-D × 40 套", "<span class=\"tag tag-orange\">混合（自购 + 租入）</span>", "<span class=\"td-num\">2026-08-23</span>", "2026-11-23", "<span class=\"td-num\">40 套</span>", "<span class=\"tag tag-green\">已退租</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
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
          'text': '华骏重卡汽车有限公司',
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
          'cells': ['1', 'ZL-20260823-033', '华骏重卡汽车有限公司', '08-23', '09-02', '40 套', '已退租'],
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
          'who': '沈婷'
        },
        {
          't': '09-02',
          'text': '退租入库 · 按 BOM 拆散分流（自有回库 + 租入转归还）',
          'who': '张帆'
        }
      ]
    },
    'ZL-20260312-0088': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "combo": "ZH-2601-A × 620 套", "src": "自有", "date": "2026-03-12", "back": "长期循环", "status": "在租"}, "cells": ["PRJ-2601", "华骏重卡汽车有限公司", "ZH-2601-A × 620 套", "自有", "<span class=\"td-num\">2026-03-12</span>", "长期循环", "<span class=\"td-num\">126 套</span>", "<span class=\"tag tag-blue\">在租</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
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
          'text': '华骏重卡汽车有限公司',
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
          'cells': ['1', 'ZL-20260312-0088', '华骏重卡汽车有限公司', '03-12', '长期循环', '620 套', '在租'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        },
        {
          'cells': ['2', 'ZL-20260312-0088 · 部分退租', '华骏重卡汽车有限公司', '—', '09-04', '200 套', '退租中']
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
          'who': '沈婷'
        },
        {
          't': '09-04',
          'text': '部分退租 · 退 200 套（直接入库）',
          'who': '客户提交'
        }
      ]
    },
    'ZL-20260402-0102': {
      'row': {"fields": {"project": "PRJ-2602", "customer": "东海商用宁波分公司", "combo": "ZH-2602-B × 840 套", "src": "自有", "date": "2026-04-02", "back": "长期循环", "status": "在租"}, "cells": ["PRJ-2602", "东海商用宁波分公司", "ZH-2602-B × 840 套", "自有", "<span class=\"td-num\">2026-04-02</span>", "长期循环", "<span class=\"td-num\">212 套</span>", "<span class=\"tag tag-blue\">在租</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
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
          'text': '东海商用宁波分公司',
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
          'cells': ['1', 'ZL-20260402-0102', '东海商用宁波分公司', '04-02', '长期循环', '840 套', '在租'],
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
          'who': '沈婷'
        },
        {
          't': '持续',
          'text': '循环出租 · 累计退回 212 套后再投放'
        }
      ]
    },
    'ZL-20260518-0145': {
      'row': {"fields": {"project": "PRJ-2603", "customer": "星途新能源汽车科技有限公司", "combo": "ZH-2603-C × 420 套", "src": "自有", "date": "2026-05-18", "back": "长期循环", "status": "在租"}, "cells": ["PRJ-2603", "星途新能源汽车科技有限公司", "ZH-2603-C × 420 套", "自有", "<span class=\"td-num\">2026-05-18</span>", "长期循环", "<span class=\"td-num\">96 套</span>", "<span class=\"tag tag-blue\">在租</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
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
          'text': '星途新能源汽车科技有限公司',
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
          'cells': ['1', 'ZL-20260518-0145', '星途新能源汽车科技有限公司', '05-18', '长期循环', '420 套', '在租'],
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
          'who': '沈婷'
        },
        {
          't': '持续',
          'text': '循环出租 · 累计退回 96 套后再投放'
        }
      ]
    },
    'ZL-20260610-0167': {
      'row': {"fields": {"project": "PRJ-2604", "customer": "长风汽车制造有限公司", "combo": "ZH-2601-A × 380 套", "src": "自有", "date": "2026-06-10", "back": "长期循环", "status": "已退回"}, "cells": ["PRJ-2604", "长风汽车制造有限公司", "ZH-2601-A × 380 套", "自有", "<span class=\"td-num\">2026-06-10</span>", "长期循环", "<span class=\"td-num\">380 套</span>", "<span class=\"tag tag-green\">已退回</span>", "2026-08-20"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
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
          'text': '长风汽车制造有限公司',
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
          'cells': ['1', 'ZL-20260610-0167', '长风汽车制造有限公司', '06-10', '08-20', '380 套', '已退回'],
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
          'who': '沈婷'
        },
        {
          't': '08-20',
          'text': '全量退回 · 退租入库',
          'who': '张帆'
        }
      ]
    },
    'ZL-20260108-0031': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "combo": "WBX-1210L × 300 只", "src": "租入", "date": "2026-01-08", "back": "2026-08-31", "status": "超期未还"}, "cells": ["PRJ-2601", "华骏重卡汽车有限公司", "WBX-1210L × 300 只", "<span class=\"tag tag-orange\">租入</span>", "<span class=\"td-num\">2026-01-08</span>", "2026-08-31", "<span class=\"td-num\">0 只</span>", "<span class=\"tag tag-red\">超期未还</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
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
          'text': '华骏重卡汽车有限公司',
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
          'text': '租入'
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
          'cells': ['1', 'ZL-20260108-0031', '华骏重卡汽车有限公司', '01-08', '—', '300 只', '超期未还'],
          'links': {
            1: '租赁管理/租赁单列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '租入单',
          'name': '环通资产 · 转租',
          'url': '租入管理/租入单列表.html'
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
          'text': '起租 · 租入转租（环通资产）',
          'who': '沈婷'
        },
        {
          't': '08-31',
          'text': '租期止 · 超期未还（催收中）',
          'who': '沈婷'
        }
      ]
    },
    'ZL-20260222-0056': {
      'row': {"fields": {"project": "PRJ-2602", "customer": "东海商用宁波分公司", "combo": "PLT-1210P × 260 块", "src": "自有", "date": "2026-02-22", "back": "长期循环", "status": "已退回"}, "cells": ["PRJ-2602", "东海商用宁波分公司", "PLT-1210P × 260 块", "自有", "<span class=\"td-num\">2026-02-22</span>", "长期循环", "<span class=\"td-num\">260 块</span>", "<span class=\"tag tag-green\">已退回</span>", "2026-07-15"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
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
          'text': '东海商用宁波分公司',
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
          'cells': ['1', 'ZL-20260222-0056', '东海商用宁波分公司', '02-22', '07-15', '260 块', '已退回'],
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
          'who': '沈婷'
        },
        {
          't': '07-15',
          'text': '全量退回 · 退租入库',
          'who': '张帆'
        }
      ]
    },
    'ZL-20260701-0188': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "combo": "ZH-2601-A × 150 套", "src": "自有", "date": "2026-07-01", "back": "2026-09-30", "status": "在租"}, "cells": ["PRJ-2601", "华骏重卡汽车有限公司", "ZH-2601-A × 150 套", "自有", "<span class=\"td-num\">2026-07-01</span>", "2026-09-30", "<span class=\"td-num\">0 套</span>", "<span class=\"tag tag-blue\">在租</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
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
          'text': '华骏重卡汽车有限公司',
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
          'cells': ['1', 'ZL-20260701-0188', '华骏重卡汽车有限公司', '07-01', '—', '150 套', '在租'],
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
          'who': '沈婷'
        },
        {
          't': '—',
          'text': '在租中 · 租期止 09-30（即将到期页签跟踪）',
          'off': true
        }
      ]
    },
    'ZL-20260506-0121': {
      'row': {"fields": {"project": "PRJ-2601", "customer": "华骏重卡汽车有限公司", "combo": "ZH-2601-A × 96 套", "src": "自有", "date": "2026-05-06", "back": "长期循环", "status": "缺损待赔"}, "cells": ["PRJ-2601", "华骏重卡汽车有限公司", "ZH-2601-A × 96 套", "自有", "<span class=\"td-num\">2026-05-06</span>", "长期循环", "<span class=\"td-num\">7 套</span>", "<span class=\"tag tag-red\">缺损待赔</span>", "—"], "ops": [{"t": "详情", "detail": true}, {"t": "退租", "act": "go('../租赁管理/退租入库列表.html')"}]},
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
          'text': '华骏重卡汽车有限公司',
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
          'cells': ['1', 'ZL-20260506-0121', '华骏重卡汽车有限公司', '05-06', '—', '96 套', '缺损待赔'],
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
          'who': '沈婷'
        },
        {
          't': '09-05',
          'text': '退租验收发现 7 套缺损 · 待赔偿处理',
          'who': '张帆'
        }
      ]
    }
  },

  /* -------------------------------------------------------------------------- */
  /* 资产轨迹 assetTracks：键 = 器具编码（原宿主 租赁管理/在租台账.html 已删·9 行留档；现供库存查询 openTrack） */
  /* 弹窗 trackModal · 触发锚「资产轨迹」；履历页=租赁管理/器具出租履历.html（G36 B3 页面化·原租出台账共用） */
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
          'who': '林国栋'
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
          'text': '自有 2,120 + 租入 1,000',
          'full': true
        }
      ],
      'feeSecTitle': '最近流转',
      'feeCols': ['日期', '单据', '事项', '数量'],
      'fees': [
        {
          'cells': ['09-03', 'GHCK-20260903-002', '分流归还 · 租入侧大箱 4 只缺损归还环通', '-4 只'],
          'links': {
            1: '租入管理/租入归还列表.html'
          }
        },
        {
          'cells': ['09-02', 'TZRK-20260902-010', '退租入库 · ZH-2604-D 拆散（含围板箱大箱 × 10）', '-10 只'],
          'links': {
            1: '租赁管理/退租入库列表.html'
          }
        },
        {
          'cells': ['08-24', 'CK-20260824-009', '租赁出库 · ZH-2604-D × 40 套（配比含围板箱）', '租出 40 套'],
          'links': {
            1: '租赁管理/租赁出库列表.html'
          }
        },
        {
          'cells': ['08-16', 'RZRK-20260816-021', '租入入库 · 环通围板箱 30 只（转租）', '+30 只'],
          'links': {
            1: '租入管理/租入入库列表.html'
          }
        }
      ],
      'chain': [
        {
          'role': '租入入库 / 采购入库',
          'name': '来源',
          'url': '租入管理/租入入库列表.html'
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
          'text': '租入入库 +30（环通 · L3 转租链）',
          'who': '林国栋'
        },
        {
          't': '09-02',
          'text': 'L4 退租拆散 · 大箱 10 只分流归还',
          'who': '张帆'
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
          'name': '状态统计',
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
          'cells': ['08-25', 'CGRK-20260825-006', '采购入库 · 延陵托盘', '+500 块'],
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
          'name': '状态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-25',
          'text': '采购入库 +500',
          'who': '张帆'
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
          'who': '张帆'
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
          'cells': ['08-26', 'CGRK-20260826-008', '采购入库 · 甬城塑业', '+800 只'],
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
          'name': '状态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-26',
          'text': '采购入库 +800',
          'who': '张帆'
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
            1: '租赁管理/租赁出库列表.html'
          }
        },
        {
          'cells': ['09-02', 'TZRK-20260902-008', '退租入库 · 回库待检', '+60 套'],
          'links': {
            1: '租赁管理/退租入库列表.html'
          }
        },
        {
          'cells': ['08-30', 'CK-20260830-015', '租赁出库 · 租出 180 套', '-180 套'],
          'links': {
            1: '租赁管理/租赁出库列表.html'
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
          'name': '状态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-30',
          'text': '租赁出库 -180',
          'who': '张帆'
        },
        {
          't': '09-03',
          'text': '回库件循环再出租 -60（CK-20260903-016）',
          'who': '张帆'
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
          'cells': ['08-28', 'CK-20260828-010', '租赁出库 · 租出 200 套', '-200 套'],
          'links': {
            1: '租赁管理/租赁出库列表.html'
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
          'name': '状态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '08-28',
          'text': '租赁出库 -200',
          'who': '张帆'
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
          'cells': ['08-29', 'CK-20260829-013', '租赁出库 · 租出 60 套', '-60 套'],
          'links': {
            1: '租赁管理/租赁出库列表.html'
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
    },
    'XNC-ZZ-WBX': {
      'title': '资产轨迹',
      'info': [
        {'label': '器具编码', 'text': 'XNC-ZZ-WBX'},
        {'label': '名称', 'text': '围板箱 1200×1000×970（安吉智行·转租终端用户）', 'full': true},
        {'label': '库存状态', 'text': '客户转租出＝在租子状态'},
        {'label': '当前持有人', 'text': '终端用户·延锋座椅厂（客户安吉智行转租）', 'full': true},
        {'label': '在租数量', 'text': '240 只'}
      ],
      'chain': [
        {'role': '租入单', 'name': 'RZD-20260815-005 · 环通', 'url': '租入管理/租入单列表.html'},
        {'role': '租赁单', 'name': '客户安吉智行 · 转租出库', 'url': '租赁管理/租赁单列表.html'},
        {'role': '转租终端仓（当前）', 'name': 'XNC-ZZ-WBX · 240 只', 'self': true}
      ],
      'timeline': [
        {'t': '08-15', 'text': '环通租入 240 只（RZD-20260815-005 关联批次）', 'who': '周志远'},
        {'t': '09-06', 'text': '客户安吉智行转租终端用户 · 240 只（转租＝在租子状态）', 'who': '沈婷'}
      ]
    },

  },

  /* -------------------------------------------------------------------------- */
  /* 客商 partners：键 = DW 客商编码（基础数据/客商管理.html 8 行全量） */
  /* 四段语义映射：档案信息/往来统计/关联链/操作记录；统计数取既有实体真实单号 */
  partners: {
    'DW-0001': {
      'row': {"fields": {"name": "华骏重卡汽车有限公司", "type": "客户", "contact": "严明", "invoiceTaxNo": "91131015MA1FA00014", "status": "正常", "date": "2026-08-12"}, "cells": ["华骏重卡汽车有限公司", "<span class=\"tag tag-blue\">客户</span>", "严明", "138****6621", "增值税专票 13%", "<span class=\"tag tag-green\">正常</span>", "2026-08-12"], "ops": [{"t": "详情", "act": "go('../基础数据/客商详情.html?id=DW-0001')"}, {"t": "编辑", "act": "go('../基础数据/客商新建.html')"}, {"t": "开票资料", "act": "go('../基础数据/客商开票资料.html')"}, {"t": "收货信息", "act": "go('../基础数据/客商收货信息.html')"}]},
      'title': '客商详情',
      'titleNo': '华骏重卡汽车有限公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0001'
        },
        {
          'label': '客商名称',
          'text': '华骏重卡汽车有限公司',
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
          'text': '严明 138****6621'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新日期',
          'text': '2026-08-12'
        },
        {
          'label': '关联项目',
          'text': 'PRJ-2601 长春基地围板箱租赁',
          'url': '项目管理/项目档案.html',
          'full': true
        },
        {
          'label': '联系电话',
          'text': '严明'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'info2Title': '开票资料',
      'info2': [
        {
          'label': '发票类型',
          'text': '增值税专票 13%'
        },
        {
          'label': '纳税人识别号',
          'text': '91131015MA1FA00014'
        },
        {
          'label': '开户行',
          'text': '工商银行长春汽车厂支行'
        },
        {
          'label': '账号',
          'text': '0800221109100123456'
        },
        {
          'label': '结算周期',
          'text': '月结'
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
          'cells': ['联系人', '严明 · 业务对接', '138****6621']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0001 华骏重卡',
          'self': true
        },
        {
          'role': '关联项目',
          'name': 'PRJ-2601',
          'url': '项目管理/项目档案.html'
        },
        {
          'role': '关联项目',
          'name': 'PRJ-2602',
          'url': '项目管理/项目档案.html'
        },
        {
          'role': '关联项目',
          'name': 'PRJ-2605',
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
      'row': {"fields": {"name": "东海商用汽车有限公司宁波分公司", "type": "客户", "contact": "何雅", "invoiceTaxNo": "91131015MA1FA00025", "status": "正常", "date": "2026-08-05"}, "cells": ["东海商用汽车有限公司宁波分公司", "<span class=\"tag tag-blue\">客户</span>", "何雅", "139****0233", "增值税专票 13%", "<span class=\"tag tag-green\">正常</span>", "2026-08-05"], "ops": [{"t": "详情", "act": "go('../基础数据/客商详情.html?id=DW-0002')"}, {"t": "编辑", "act": "go('../基础数据/客商新建.html')"}, {"t": "开票资料", "act": "go('../基础数据/客商开票资料.html')"}, {"t": "收货信息", "act": "go('../基础数据/客商收货信息.html')"}]},
      'title': '客商详情',
      'titleNo': '东海商用汽车有限公司宁波分公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0002'
        },
        {
          'label': '客商名称',
          'text': '东海商用汽车有限公司宁波分公司',
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
          'text': '何雅 139****0233'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新日期',
          'text': '2026-08-05'
        },
        {
          'label': '关联项目',
          'text': 'PRJ-2602 宁波工厂料箱组套租赁',
          'url': '项目管理/项目档案.html',
          'full': true
        },
        {
          'label': '联系电话',
          'text': '何雅'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'info2Title': '开票资料',
      'info2': [
        {
          'label': '发票类型',
          'text': '增值税专票 13%'
        },
        {
          'label': '纳税人识别号',
          'text': '91131015MA1FA00025'
        },
        {
          'label': '开户行',
          'text': '建设银行宁波分行'
        },
        {
          'label': '账号',
          'text': '6217001230056689'
        },
        {
          'label': '结算周期',
          'text': '月结'
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
          'cells': ['联系人', '何雅 · 业务对接', '139****0233']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0002 东海商用宁波',
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
      'row': {"fields": {"name": "星途新能源汽车科技有限公司", "type": "客户", "contact": "林岚", "invoiceTaxNo": "91131015MA1FA00036", "status": "正常", "date": "2026-07-28"}, "cells": ["星途新能源汽车科技有限公司", "<span class=\"tag tag-blue\">客户</span>", "林岚", "137****8845", "增值税专票 13%", "<span class=\"tag tag-green\">正常</span>", "2026-07-28"], "ops": [{"t": "详情", "act": "go('../基础数据/客商详情.html?id=DW-0003')"}, {"t": "编辑", "act": "go('../基础数据/客商新建.html')"}, {"t": "开票资料", "act": "go('../基础数据/客商开票资料.html')"}, {"t": "收货信息", "act": "go('../基础数据/客商收货信息.html')"}]},
      'title': '客商详情',
      'titleNo': '星途新能源汽车科技有限公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0003'
        },
        {
          'label': '客商名称',
          'text': '星途新能源汽车科技有限公司',
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
          'text': '林岚 137****8845'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新日期',
          'text': '2026-07-28'
        },
        {
          'label': '关联项目',
          'text': 'PRJ-2603 广州工厂护角套件租赁',
          'url': '项目管理/项目档案.html',
          'full': true
        },
        {
          'label': '联系电话',
          'text': '林岚'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'info2Title': '开票资料',
      'info2': [
        {
          'label': '发票类型',
          'text': '增值税专票 13%'
        },
        {
          'label': '纳税人识别号',
          'text': '91131015MA1FA00036'
        },
        {
          'label': '开户行',
          'text': '中国银行合肥滨湖支行'
        },
        {
          'label': '账号',
          'text': '3411222009887'
        },
        {
          'label': '结算周期',
          'text': '发票后 30 天'
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
          'cells': ['联系人', '林岚 · 业务对接', '137****8845']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0003 星途新能源',
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
      'row': {"fields": {"name": "长风汽车制造有限公司", "type": "客户", "contact": "邵磊", "invoiceTaxNo": "91131015MA1FA00047", "status": "停用", "date": "2026-06-30"}, "cells": ["长风汽车制造有限公司", "<span class=\"tag tag-blue\">客户</span>", "邵磊", "136****3312", "增值税专票 13%", "<span class=\"tag tag-gray\">停用</span>", "2026-06-30"], "ops": [{"t": "详情", "act": "go('../基础数据/客商详情.html?id=DW-0004')"}, {"t": "编辑", "act": "go('../基础数据/客商新建.html')"}, {"t": "开票资料", "act": "go('../基础数据/客商开票资料.html')"}, {"t": "收货信息", "act": "go('../基础数据/客商收货信息.html')"}]},
      'title': '客商详情',
      'titleNo': '长风汽车制造有限公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0004'
        },
        {
          'label': '客商名称',
          'text': '长风汽车制造有限公司',
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
          'text': '邵磊 136****3312'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新日期',
          'text': '2026-06-30'
        },
        {
          'label': '关联项目',
          'text': 'PRJ-2604 武汉工厂器具租赁（合作暂停）',
          'url': '项目管理/项目档案.html',
          'full': true
        },
        {
          'label': '联系电话',
          'text': '邵磊'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'info2Title': '开票资料',
      'info2': [
        {
          'label': '发票类型',
          'text': '增值税专票 13%'
        },
        {
          'label': '纳税人识别号',
          'text': '91131015MA1FA00047'
        },
        {
          'label': '开户行',
          'text': '农业银行西安经开区支行'
        },
        {
          'label': '账号',
          'text': '1020681209966'
        },
        {
          'label': '结算周期',
          'text': '月结'
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
          'cells': ['联系人', '邵磊 · 业务对接', '136****3312']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0004 长风汽制 · 停用',
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
          'who': '沈婷'
        }
      ]
    },
    'DW-0101': {
      'row': {"fields": {"name": "甬城塑业包装制品有限公司", "type": "供应商", "contact": "孙建平", "invoiceTaxNo": "91131015MA1FA00058", "status": "正常", "date": "2026-08-18"}, "cells": ["甬城塑业包装制品有限公司", "<span class=\"tag tag-green\">供应商</span>", "孙建平", "135****7790", "增值税专票 13%", "<span class=\"tag tag-green\">正常</span>", "2026-08-18"], "ops": [{"t": "详情", "act": "go('../基础数据/客商详情.html?id=DW-0101')"}, {"t": "编辑", "act": "go('../基础数据/客商新建.html')"}, {"t": "开票资料", "act": "go('../基础数据/客商开票资料.html')"}, {"t": "收货信息", "act": "go('../基础数据/客商收货信息.html')"}]},
      'title': '客商详情',
      'titleNo': '甬城塑业包装制品有限公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0101'
        },
        {
          'label': '客商名称',
          'text': '甬城塑业包装制品有限公司',
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
          'text': '孙建平 135****7790'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新日期',
          'text': '2026-08-18'
        },
        {
          'label': '关联项目',
          'text': '— 围板箱 / 料箱 / 零部件供应',
          'url': '项目管理/项目档案.html',
          'full': true
        },
        {
          'label': '联系电话',
          'text': '孙建平'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'info2Title': '开票资料',
      'info2': [
        {
          'label': '发票类型',
          'text': '增值税专票 13%'
        },
        {
          'label': '纳税人识别号',
          'text': '91131015MA1FA00058'
        },
        {
          'label': '开户行',
          'text': '宁波银行鄞州支行'
        },
        {
          'label': '账号',
          'text': '3102010099876'
        },
        {
          'label': '结算周期',
          'text': '月结'
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
          'cells': ['联系人', '孙建平 · 供应对接', '135****7790']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0101 甬城塑业',
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
          'who': '林国栋'
        }
      ]
    },
    'DW-0102': {
      'row': {"fields": {"name": "吴越联合五金制品有限公司", "type": "供应商", "contact": "吴海川", "invoiceTaxNo": "91131015MA1FA00069", "status": "正常", "date": "2026-08-18"}, "cells": ["吴越联合五金制品有限公司", "<span class=\"tag tag-green\">供应商</span>", "吴海川", "133****5567", "增值税专票 13%", "<span class=\"tag tag-green\">正常</span>", "2026-08-18"], "ops": [{"t": "详情", "act": "go('../基础数据/客商详情.html?id=DW-0102')"}, {"t": "编辑", "act": "go('../基础数据/客商新建.html')"}, {"t": "开票资料", "act": "go('../基础数据/客商开票资料.html')"}, {"t": "收货信息", "act": "go('../基础数据/客商收货信息.html')"}]},
      'title': '客商详情',
      'titleNo': '吴越联合五金制品有限公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0102'
        },
        {
          'label': '客商名称',
          'text': '吴越联合五金制品有限公司',
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
          'text': '吴海川 133****5567'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新日期',
          'text': '2026-08-18'
        },
        {
          'label': '关联项目',
          'text': '— 锁扣 / 铰链 / 隔板等零部件供应',
          'url': '项目管理/项目档案.html',
          'full': true
        },
        {
          'label': '联系电话',
          'text': '吴海川'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'info2Title': '开票资料',
      'info2': [
        {
          'label': '发票类型',
          'text': '增值税专票 13%'
        },
        {
          'label': '纳税人识别号',
          'text': '91131015MA1FA00069'
        },
        {
          'label': '开户行',
          'text': '招商银行苏州分行'
        },
        {
          'label': '账号',
          'text': '5129066012213'
        },
        {
          'label': '结算周期',
          'text': '发票后 30 天'
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
          'cells': ['联系人', '吴海川 · 供应对接', '133****5567']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0102 吴越联合',
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
      'row': {"fields": {"name": "延陵塑料托盘厂", "type": "供应商", "contact": "郑卫平", "invoiceTaxNo": "91131015MA1FA00070", "status": "正常", "date": "2026-07-15"}, "cells": ["延陵塑料托盘厂", "<span class=\"tag tag-green\">供应商</span>", "郑卫平", "138****2245", "增值税专票 13%", "<span class=\"tag tag-green\">正常</span>", "2026-07-15"], "ops": [{"t": "详情", "act": "go('../基础数据/客商详情.html?id=DW-0103')"}, {"t": "编辑", "act": "go('../基础数据/客商新建.html')"}, {"t": "开票资料", "act": "go('../基础数据/客商开票资料.html')"}, {"t": "收货信息", "act": "go('../基础数据/客商收货信息.html')"}]},
      'title': '客商详情',
      'titleNo': '延陵塑料托盘厂',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0103'
        },
        {
          'label': '客商名称',
          'text': '延陵塑料托盘厂',
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
          'text': '郑卫平 138****2245'
        },
        {
          'label': '开票要求',
          'text': '增值税专票 13%'
        },
        {
          'label': '更新日期',
          'text': '2026-07-15'
        },
        {
          'label': '关联项目',
          'text': '— 塑料托盘 / 木托盘供应',
          'url': '项目管理/项目档案.html',
          'full': true
        },
        {
          'label': '联系电话',
          'text': '郑卫平'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'info2Title': '开票资料',
      'info2': [
        {
          'label': '发票类型',
          'text': '增值税专票 13%'
        },
        {
          'label': '纳税人识别号',
          'text': '91131015MA1FA00070'
        },
        {
          'label': '开户行',
          'text': '江苏银行常州新北支行'
        },
        {
          'label': '账号',
          'text': '3204109001120'
        },
        {
          'label': '结算周期',
          'text': '货到付款'
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
          'cells': ['联系人', '郑卫平 · 供应对接', '138****2245']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0103 延陵托盘',
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
          'who': '林国栋'
        }
      ]
    },
    'DW-0201': {
      'row': {"fields": {"name": "环通循环包装运营（上海）有限公司", "type": "供应商", "contact": "环通对接组", "invoiceTaxNo": "91131015MA1FA00081", "status": "正常", "date": "2026-08-30"}, "cells": ["环通循环包装运营（上海）有限公司", "<span class=\"tag tag-blue\">供应商</span>", "环通对接组", "021-66****", "结算对账专用", "<span class=\"tag tag-green\">正常</span>", "2026-08-30"], "ops": [{"t": "详情", "act": "go('../基础数据/客商详情.html?id=DW-0201')"}, {"t": "编辑", "act": "go('../基础数据/客商新建.html')"}, {"t": "开票资料", "act": "go('../基础数据/客商开票资料.html')"}, {"t": "收货信息", "act": "go('../基础数据/客商收货信息.html')"}]},
      'title': '客商详情',
      'titleNo': '环通循环包装运营（上海）有限公司',
      'info': [
        {
          'label': '客商编码',
          'text': 'DW-0201'
        },
        {
          'label': '客商名称',
          'text': '环通循环包装运营（上海）有限公司',
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
          'text': '环通对接组 021-66****'
        },
        {
          'label': '开票要求',
          'text': '结算对账专用'
        },
        {
          'label': '更新日期',
          'text': '2026-08-30'
        },
        {
          'label': '关联项目',
          'text': '— 围板箱租入运营（L3/L4 链）',
          'url': '项目管理/项目档案.html',
          'full': true
        },
        {
          'label': '联系电话',
          'text': '环通对接组'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'info2Title': '开票资料',
      'info2': [
        {
          'label': '发票类型',
          'text': '增值税专票 13%'
        },
        {
          'label': '纳税人识别号',
          'text': '91131015MA1FA00081'
        },
        {
          'label': '开户行',
          'text': '建设银行上海分行'
        },
        {
          'label': '账号',
          'text': '3100156820005001234'
        },
        {
          'label': '结算周期',
          'text': '预付'
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
          'cells': ['联系人', '环通对接组', '021-66****']
        }
      ],
      'chain': [
        {
          'role': '客商（本档）',
          'name': 'DW-0201 环通包装运营',
          'self': true
        },
        {
          'role': '租入单',
          'name': 'RZD-20260815-003 / -005',
          'url': '租入管理/租入单列表.html'
        },
        {
          'role': '租入归还',
          'name': 'GHCK-20260903-001 / -002',
          'url': '租入管理/租入归还列表.html'
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
          'who': '周志远'
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
      'row': {"fields": {"name": "围板箱 1200×1000×970", "model": "WBX-1210L", "innerCode": "HJ-BX-0970", "cls": "围板箱", "spec": "1200×1000×970 mm", "status": "启用", "date": "2026-01-06", "rentInMode": "按月", "rentInPrice": "45.00", "rentalMode": "按月", "rentalPrice": "60.00", "buyPrice": "380.00", "salePrice": "—"}, "cells": ["围板箱 1200×1000×970", "<span class=\"tag tag-blue\">围板箱</span>", "1200×1000×970 mm", "只", "<span class=\"td-num\">380.00</span>", "—", "<span class=\"td-num\">45.00 元/只·月</span>", "<span class=\"td-num\">60.00 元/只·月</span>", "<span class=\"tag tag-green\">启用</span>", "2026-01-06"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=WBX-1210L')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'WBX-1210L'
        },
        {
          'label': '物料名称',
          'text': '围板箱 1200×1000×970',
          'full': true
        },
        {
          'label': '物料类型',
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
          'label': '参考未税采购价',
          'text': '380.00 元'
        },
        {
          'label': '参考未税销售价',
          'text': '—（租赁器具不零售）'
        },
        {
          'label': '参考未税租入价',
          'text': '45.00 元/只·月'
        },
        {
          'label': '参考未税租赁价',
          'text': '60.00 元/只·月'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-01-06'
        },
        {
          'label': '物料型号',
          'text': 'WBX-1210L'
        },
        {
          'label': '供应商内部编码',
          'text': 'HJ-BX-0970'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'feeSecTitle': '在租状态（库存状态口径）',
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
          'role': '物料档案（本档）',
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
          'name': '状态统计 + 资产轨迹',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '2026-01-06',
          'text': '建档 · 启用（器具采购入库）',
          'who': '张帆'
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
      'row': {"fields": {"name": "围板箱 1200×1000×590", "cls": "围板箱", "spec": "1200×1000×590 mm", "status": "启用", "date": "2026-01-06", "rentInMode": null, "rentInPrice": null, "rentalMode": "按月", "rentalPrice": "55.00", "buyPrice": "340.00", "salePrice": "—"}, "cells": ["围板箱 1200×1000×590", "<span class=\"tag tag-blue\">围板箱</span>", "1200×1000×590 mm", "只", "<span class=\"td-num\">340.00</span>", "—", "—", "<span class=\"td-num\">55.00 元/只·月</span>", "<span class=\"tag tag-green\">启用</span>", "2026-01-06"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=WBX-1210M')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'WBX-1210M'
        },
        {
          'label': '物料名称',
          'text': '围板箱 1200×1000×590',
          'full': true
        },
        {
          'label': '物料类型',
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
          'label': '参考未税采购价',
          'text': '340.00 元'
        },
        {
          'label': '参考未税销售价',
          'text': '—（租赁器具不零售）'
        },
        {
          'label': '参考未税租入价',
          'text': '—（无租入来源）'
        },
        {
          'label': '参考未税租赁价',
          'text': '55.00 元/只·月'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-01-06'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'feeSecTitle': '在租状态（库存状态口径）',
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
          'role': '物料档案（本档）',
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
          'name': '状态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '2026-01-06',
          'text': '建档 · 启用',
          'who': '张帆'
        },
        {
          't': '当前',
          'text': '在租 1,020 只 · 无超期'
        }
      ]
    },
    'PLT-1210W': {
      'row': {"fields": {"name": "木托盘 1200×1000", "cls": "木托盘", "spec": "1200×1000×144 mm", "status": "启用", "date": "2026-02-11", "rentInMode": null, "rentInPrice": null, "rentInMode": "按次", "rentInPrice": "6.00", "rentalMode": "按次", "rentalPrice": "15.00", "buyPrice": "95.00", "salePrice": "—"}, "cells": ["木托盘 1200×1000", "<span class=\"tag tag-green\">木托盘</span>", "1200×1000×144 mm", "块", "<span class=\"td-num\">95.00</span>", "—", "<span class=\"td-num\">6.00 元/块·次</span>", "<span class=\"td-num\">15.00 元/块·次</span>", "<span class=\"tag tag-green\">启用</span>", "2026-02-11"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=PLT-1210W')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'PLT-1210W'
        },
        {
          'label': '物料名称',
          'text': '木托盘 1200×1000',
          'full': true
        },
        {
          'label': '物料类型',
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
          'label': '参考未税采购价',
          'text': '95.00 元'
        },
        {
          'label': '参考未税销售价',
          'text': '—（租赁器具不零售）'
        },
        {
          'label': '参考未税租入价',
          'text': '6.00 元/块·次（按次·G39 演示）'
        },
        {
          'label': '参考未税租赁价',
          'text': '15.00 元/块·次'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-02-11'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'feeSecTitle': '在租状态（库存状态口径）',
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
          'role': '物料档案（本档）',
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
          'who': '张帆'
        },
        {
          't': '08-25',
          'text': '断裂批次报废 -22 块 · 全量退回后暂无在租',
          'who': '赵芳'
        }
      ]
    },
    'PLT-1210P': {
      'row': {"fields": {"name": "塑料托盘 1200×1000", "cls": "塑料托盘", "spec": "1200×1000×150 mm", "status": "启用", "date": "2026-02-11", "rentInMode": "按月", "rentInPrice": "12.00", "rentalMode": "按月", "rentalPrice": "18.00", "buyPrice": "110.00", "salePrice": "—"}, "cells": ["塑料托盘 1200×1000", "<span class=\"tag tag-green\">塑料托盘</span>", "1200×1000×150 mm", "块", "<span class=\"td-num\">110.00</span>", "—", "<span class=\"td-num\">12.00 元/块·月</span>", "<span class=\"td-num\">18.00 元/块·月</span>", "<span class=\"tag tag-green\">启用</span>", "2026-02-11"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=PLT-1210P')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'PLT-1210P'
        },
        {
          'label': '物料名称',
          'text': '塑料托盘 1200×1000',
          'full': true
        },
        {
          'label': '物料类型',
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
          'label': '参考未税采购价',
          'text': '110.00 元'
        },
        {
          'label': '参考未税销售价',
          'text': '—（租赁器具不零售）'
        },
        {
          'label': '参考未税租入价',
          'text': '12.00 元/块·月'
        },
        {
          'label': '参考未税租赁价',
          'text': '18.00 元/块·月'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-02-11'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'feeSecTitle': '在租状态（库存状态口径）',
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
          'role': '物料档案（本档）',
          'name': 'PLT-1210P',
          'self': true
        },
        {
          'role': '租入单',
          'name': '环通资产',
          'url': '租入管理/租入单列表.html'
        },
        {
          'role': '库存查询·客户在租',
          'name': '状态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '2026-02-11',
          'text': '建档 · 启用',
          'who': '张帆'
        },
        {
          't': '当前',
          'text': '在租 1,860 块 · 超期 36 块待催还'
        }
      ]
    },
    'BTC-6040S': {
      'row': {"fields": {"name": "料箱 600×400×220（带盖）", "cls": "料箱", "spec": "600×400×220 mm", "status": "停用", "date": "2026-03-02", "rentInMode": null, "rentInPrice": null, "rentalMode": null, "rentalPrice": null, "buyPrice": "78.00", "salePrice": "—"}, "cells": ["料箱 600×400×220（带盖）", "<span class=\"tag tag-orange\">料箱</span>", "600×400×220 mm", "只", "<span class=\"td-num\">78.00</span>", "—", "—", "—", "<span class=\"tag tag-gray\">停用</span>", "2026-03-02"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=BTC-6040S')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'BTC-6040S'
        },
        {
          'label': '物料名称',
          'text': '料箱 600×400×220（带盖）',
          'full': true
        },
        {
          'label': '物料类型',
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
          'label': '参考未税采购价',
          'text': '78.00 元'
        },
        {
          'label': '参考未税销售价',
          'text': '—（租赁器具不零售）'
        },
        {
          'label': '参考未税租入价',
          'text': '—（无租入来源）'
        },
        {
          'label': '参考未税租赁价',
          'text': '—（采购件 / 停用不计租）'
        },
        {
          'label': '状态',
          'tag': '停用'
        },
        {
          'label': '建档日期',
          'text': '2026-03-02'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'feeSecTitle': '在租状态（库存状态口径）',
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
          'role': '物料档案（本档）',
          'name': 'BTC-6040S · 停用',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '2026-03-02',
          'text': '建档',
          'who': '张帆'
        },
        {
          't': '2026-08-01',
          'text': '档案停用（供应商停产 · 停止新租）',
          'who': '张帆'
        }
      ]
    },
    'BTC-6040': {
      'row': {"fields": {"name": "料箱 600×400×340", "cls": "料箱", "spec": "600×400×340 mm", "status": "启用", "date": "2026-03-02", "rentInMode": "按月", "rentInPrice": "10.00", "rentalMode": "按次", "rentalPrice": "14.00", "buyPrice": "85.00", "salePrice": "—"}, "cells": ["料箱 600×400×340", "<span class=\"tag tag-orange\">料箱</span>", "600×400×340 mm", "只", "<span class=\"td-num\">85.00</span>", "—", "<span class=\"td-num\">10.00 元/只·月</span>", "<span class=\"td-num\">14.00 元/只·次</span>", "<span class=\"tag tag-green\">启用</span>", "2026-03-02"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=BTC-6040')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'BTC-6040'
        },
        {
          'label': '物料名称',
          'text': '料箱 600×400×340',
          'full': true
        },
        {
          'label': '物料类型',
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
          'label': '参考未税采购价',
          'text': '85.00 元'
        },
        {
          'label': '参考未税销售价',
          'text': '—（租赁器具不零售）'
        },
        {
          'label': '参考未税租入价',
          'text': '10.00 元/只·月'
        },
        {
          'label': '参考未税租赁价',
          'text': '14.00 元/只·次'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-03-02'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'feeSecTitle': '在租状态（库存状态口径）',
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
          'role': '物料档案（本档）',
          'name': 'BTC-6040',
          'self': true
        },
        {
          'role': '租入单',
          'name': '环通资产',
          'url': '租入管理/租入单列表.html'
        },
        {
          'role': '库存查询·客户在租',
          'name': '状态统计',
          'url': '仓储作业/库存查询.html'
        }
      ],
      'timeline': [
        {
          't': '2026-03-02',
          'text': '建档 · 启用',
          'who': '张帆'
        },
        {
          't': '当前',
          'text': '在租 2,480 只 · 无超期'
        }
      ]
    },

    /* ===== 组件（原零部件档案并入 · N4 合并） ===== */
    'LJ-A100': {
      'row': {"fields": {"name": "锁扣组件", "cls": "零部件", "spec": "不锈钢 304 · M8", "status": "启用", "date": "2026-01-06", "supplier": "吴越联合五金制品有限公司", "rentInMode": null, "rentInPrice": null, "rentalMode": null, "rentalPrice": null, "buyPrice": "6.80", "salePrice": "9.80"}, "cells": ["锁扣组件", "<span class=\"tag tag-blue\">零部件</span>", "不锈钢 304 · M8", "件", "<span class=\"td-num\">6.80</span>", "<span class=\"td-num\">9.80</span>", "—", "—", "<span class=\"tag tag-green\">启用</span>", "2026-01-06"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=LJ-A100')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'LJ-A100'
        },
        {
          'label': '物料名称',
          'text': '锁扣组件',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '零部件'
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
          'label': '参考未税采购价',
          'text': '6.80 元'
        },
        {
          'label': '参考未税销售价',
          'text': '9.80 元'
        },
        {
          'label': '参考未税租入价',
          'text': '—（无租入来源）'
        },
        {
          'label': '参考未税租赁价',
          'text': '—（采购件 / 停用不计租）'
        },
        {
          'label': '供应商（带出）',
          'text': '吴越联合五金制品有限公司',
          'full': true
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-01-06'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
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
          'name': '吴越联合'
        },
        {
          'role': '物料档案（本档）',
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
          'who': '张帆'
        },
        {
          't': '09-01',
          'text': '调拨备料 · DB-20260901-003（-1,000 件 → 成品区 RB）',
          'who': '赵芳'
        }
      ]
    },
    'LJ-B200': {
      'row': {"fields": {"name": "铰链", "cls": "零部件", "spec": "锌合金 · 65mm", "status": "启用", "date": "2026-01-06", "supplier": "吴越联合五金制品有限公司", "rentInMode": null, "rentInPrice": null, "rentalMode": null, "rentalPrice": null, "buyPrice": "4.20", "salePrice": "6.50"}, "cells": ["铰链", "<span class=\"tag tag-blue\">零部件</span>", "锌合金 · 65mm", "件", "<span class=\"td-num\">4.20</span>", "<span class=\"td-num\">6.50</span>", "—", "—", "<span class=\"tag tag-green\">启用</span>", "2026-01-06"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=LJ-B200')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'LJ-B200'
        },
        {
          'label': '物料名称',
          'text': '铰链',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '零部件'
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
          'label': '参考未税采购价',
          'text': '4.20 元'
        },
        {
          'label': '参考未税销售价',
          'text': '6.50 元'
        },
        {
          'label': '参考未税租入价',
          'text': '—（无租入来源）'
        },
        {
          'label': '参考未税租赁价',
          'text': '—（采购件 / 停用不计租）'
        },
        {
          'label': '供应商（带出）',
          'text': '吴越联合五金制品有限公司',
          'full': true
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-01-06'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
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
          'name': '吴越联合'
        },
        {
          'role': '物料档案（本档）',
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
      'row': {"fields": {"name": "围板", "cls": "零部件", "spec": "HDPE 波纹板 · 970 高", "status": "启用", "date": "2026-02-02", "supplier": "甬城塑业包装制品有限公司", "rentInMode": null, "rentInPrice": null, "rentalMode": null, "rentalPrice": null, "buyPrice": "52.00", "salePrice": "68.00"}, "cells": ["围板", "<span class=\"tag tag-blue\">零部件</span>", "HDPE 波纹板 · 970 高", "件", "<span class=\"td-num\">52.00</span>", "<span class=\"td-num\">68.00</span>", "—", "—", "<span class=\"tag tag-green\">启用</span>", "2026-02-02"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=LJ-C300')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'LJ-C300'
        },
        {
          'label': '物料名称',
          'text': '围板',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '零部件'
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
          'label': '参考未税采购价',
          'text': '52.00 元'
        },
        {
          'label': '参考未税销售价',
          'text': '68.00 元'
        },
        {
          'label': '参考未税租入价',
          'text': '—（无租入来源）'
        },
        {
          'label': '参考未税租赁价',
          'text': '—（采购件 / 停用不计租）'
        },
        {
          'label': '供应商（带出）',
          'text': '甬城塑业包装制品有限公司',
          'full': true
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-02-02'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
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
          'name': '甬城塑业'
        },
        {
          'role': '物料档案（本档）',
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
          'who': '张帆'
        }
      ]
    },
    'LJ-D400': {
      'row': {"fields": {"name": "箱盖", "cls": "零部件", "spec": "ABS 吸塑 · 1200×1000", "status": "启用", "date": "2026-02-02", "supplier": "甬城塑业包装制品有限公司", "rentInMode": null, "rentInPrice": null, "rentalMode": null, "rentalPrice": null, "buyPrice": "36.00", "salePrice": "48.00"}, "cells": ["箱盖", "<span class=\"tag tag-blue\">零部件</span>", "ABS 吸塑 · 1200×1000", "件", "<span class=\"td-num\">36.00</span>", "<span class=\"td-num\">48.00</span>", "—", "—", "<span class=\"tag tag-green\">启用</span>", "2026-02-02"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=LJ-D400')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'LJ-D400'
        },
        {
          'label': '物料名称',
          'text': '箱盖',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '零部件'
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
          'label': '参考未税采购价',
          'text': '36.00 元'
        },
        {
          'label': '参考未税销售价',
          'text': '48.00 元'
        },
        {
          'label': '参考未税租入价',
          'text': '—（无租入来源）'
        },
        {
          'label': '参考未税租赁价',
          'text': '—（采购件 / 停用不计租）'
        },
        {
          'label': '供应商（带出）',
          'text': '甬城塑业包装制品有限公司',
          'full': true
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-02-02'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
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
          'name': '甬城塑业'
        },
        {
          'role': '物料档案（本档）',
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
          'who': '张帆'
        }
      ]
    },
    'LJ-E500': {
      'row': {"fields": {"name": "底托架", "cls": "内衬", "spec": "钢制喷塑 · 1200×1000", "status": "启用", "date": "2026-03-06", "supplier": "延陵塑料托盘厂", "rentInMode": null, "rentInPrice": null, "rentalMode": null, "rentalPrice": null, "buyPrice": "78.00", "salePrice": "98.00"}, "cells": ["底托架", "<span class=\"tag tag-blue\">内衬</span>", "钢制喷塑 · 1200×1000", "件", "<span class=\"td-num\">78.00</span>", "<span class=\"td-num\">98.00</span>", "—", "—", "<span class=\"tag tag-green\">启用</span>", "2026-03-06"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=LJ-E500')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'LJ-E500'
        },
        {
          'label': '物料名称',
          'text': '底托架',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '内衬'
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
          'label': '参考未税采购价',
          'text': '78.00 元'
        },
        {
          'label': '参考未税销售价',
          'text': '98.00 元'
        },
        {
          'label': '参考未税租入价',
          'text': '—（无租入来源）'
        },
        {
          'label': '参考未税租赁价',
          'text': '—（采购件 / 停用不计租）'
        },
        {
          'label': '供应商（带出）',
          'text': '延陵塑料托盘厂',
          'full': true
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-03-06'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
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
          'name': '延陵托盘'
        },
        {
          'role': '物料档案（本档）',
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
      'row': {"fields": {"name": "内衬", "cls": "内衬", "spec": "EPE 珍珠棉 · 定制", "status": "启用", "date": "2026-03-06", "supplier": "甬城塑业包装制品有限公司", "rentInMode": null, "rentInPrice": null, "rentalMode": null, "rentalPrice": null, "buyPrice": "15.50", "salePrice": "22.00"}, "cells": ["内衬", "<span class=\"tag tag-blue\">内衬</span>", "EPE 珍珠棉 · 定制", "件", "<span class=\"td-num\">15.50</span>", "<span class=\"td-num\">22.00</span>", "—", "—", "<span class=\"tag tag-green\">启用</span>", "2026-03-06"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=LJ-F600')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'LJ-F600'
        },
        {
          'label': '物料名称',
          'text': '内衬',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '内衬'
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
          'label': '参考未税采购价',
          'text': '15.50 元'
        },
        {
          'label': '参考未税销售价',
          'text': '22.00 元'
        },
        {
          'label': '参考未税租入价',
          'text': '—（无租入来源）'
        },
        {
          'label': '参考未税租赁价',
          'text': '—（采购件 / 停用不计租）'
        },
        {
          'label': '供应商（带出）',
          'text': '甬城塑业包装制品有限公司',
          'full': true
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-03-06'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
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
          'name': '甬城塑业'
        },
        {
          'role': '物料档案（本档）',
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
          'who': '林国栋'
        }
      ]
    },
    'KBX-1040M': {
      'row': {"fields": {"name": "卡板箱 1040×800×590", "cls": "卡板箱", "spec": "1040×800×590 mm", "status": "启用", "date": "2026-06-18", "supplier": "甬城塑业包装制品有限公司", "rentInMode": "按月", "rentInPrice": 8.00, "rentalMode": "按月", "rentalPrice": 12.00, "buyPrice": "120.00", "salePrice": "—"}, "cells": ["卡板箱 1040×800×590", "<span class=\"tag tag-blue\">卡板箱</span>", "1040×800×590 mm", "只", "<span class=\"td-num\">120.00</span>", "—", "<span class=\"td-num\">8.00 元/只·月</span>", "<span class=\"td-num\">12.00 元/只·月</span>", "<span class=\"tag tag-green\">启用</span>", "2026-06-18"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=KBX-1040M')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'KBX-1040M'
        },
        {
          'label': '物料名称',
          'text': '卡板箱 1040×800×590',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '卡板箱'
        },
        {
          'label': '规格',
          'text': '1040×800×590 mm',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '只'
        },
        {
          'label': '参考未税采购价',
          'text': '120.00 元'
        },
        {
          'label': '参考未税销售价',
          'text': '—（租赁器具不零售）'
        },
        {
          'label': '参考未税租入价',
          'text': '8.00 元/只·月'
        },
        {
          'label': '参考未税租赁价',
          'text': '12.00 元/只·月'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-06-18'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'feeSecTitle': '在租状态（库存状态口径）',
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
          'role': '物料档案（本档）',
          'name': 'KBX-1040M · 启用',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '2026-06-18',
          'text': '建档 · 启用（G38 物料类型 10 值扩展示例）',
          'who': '张帆'
        }
      ]
    },
    'PLT-1210G': {
      'row': {"fields": {"name": "金属托盘 1200×1000", "cls": "金属托盘", "spec": "1200×1000×144 mm", "status": "启用", "date": "2026-02-10", "supplier": "吴越联合五金制品有限公司", "rentInMode": "按月", "rentInPrice": 10.00, "rentalMode": "按月", "rentalPrice": 15.00, "buyPrice": "165.00", "salePrice": "—"}, "cells": ["金属托盘 1200×1000", "<span class=\"tag tag-blue\">金属托盘</span>", "1200×1000×144 mm", "块", "<span class=\"td-num\">165.00</span>", "—", "<span class=\"td-num\">10.00 元/块·月</span>", "<span class=\"td-num\">15.00 元/块·月</span>", "<span class=\"tag tag-green\">启用</span>", "2026-02-10"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=PLT-1210G')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'PLT-1210G'
        },
        {
          'label': '物料名称',
          'text': '金属托盘 1200×1000',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '金属托盘'
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
          'label': '参考未税采购价',
          'text': '165.00 元'
        },
        {
          'label': '参考未税销售价',
          'text': '—（租赁器具不零售）'
        },
        {
          'label': '参考未税租入价',
          'text': '10.00 元/块·月'
        },
        {
          'label': '参考未税租赁价',
          'text': '15.00 元/块·月'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-02-10'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'feeSecTitle': '在租状态（库存状态口径）',
      'feeCols': ['在租', '待归还（超期）', '平均循环', '平均租期', '台账'],
      'fees': [
        {
          'cells': ['0 块', '0 块', '—', '—', '客户在租（无在租）'],
          'links': {
            4: '仓储作业/库存查询.html'
          }
        }
      ],
      'chain': [
        {
          'role': '物料档案（本档）',
          'name': 'PLT-1210G · 启用',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '2026-02-10',
          'text': '建档 · 启用（G38 物料类型 10 值扩展示例）',
          'who': '张帆'
        }
      ]
    },
    'KJ-2701': {
      'row': {"fields": {"name": "料架 1850×1000×1200", "cls": "料架", "spec": "1850×1000×1200 mm", "status": "启用", "date": "2026-04-22", "supplier": "吴越联合五金制品有限公司", "rentInMode": "按月", "rentInPrice": 25.00, "rentalMode": "按月", "rentalPrice": 38.00, "buyPrice": "420.00", "salePrice": "—"}, "cells": ["料架 1850×1000×1200", "<span class=\"tag tag-blue\">料架</span>", "1850×1000×1200 mm", "套", "<span class=\"td-num\">420.00</span>", "—", "<span class=\"td-num\">25.00 元/套·月</span>", "<span class=\"td-num\">38.00 元/套·月</span>", "<span class=\"tag tag-green\">启用</span>", "2026-04-22"], "ops": [{"t": "详情", "act": "go('../基础数据/物料详情.html?id=KJ-2701')"}, {"t": "编辑", "act": "go('../基础数据/物料新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
      'title': '物料详情',
      'info': [
        {
          'label': '物料编码',
          'text': 'KJ-2701'
        },
        {
          'label': '物料名称',
          'text': '料架 1850×1000×1200',
          'full': true
        },
        {
          'label': '物料类型',
          'text': '料架'
        },
        {
          'label': '规格',
          'text': '1850×1000×1200 mm',
          'full': true
        },
        {
          'label': '计量单位',
          'text': '套'
        },
        {
          'label': '参考未税采购价',
          'text': '420.00 元'
        },
        {
          'label': '参考未税销售价',
          'text': '—（租赁器具不零售）'
        },
        {
          'label': '参考未税租入价',
          'text': '25.00 元/套·月'
        },
        {
          'label': '参考未税租赁价',
          'text': '38.00 元/套·月'
        },
        {
          'label': '状态',
          'tag': '启用'
        },
        {
          'label': '建档日期',
          'text': '2026-04-22'
        },
        {
          'label': '物料型号',
          'text': '—'
        },
        {
          'label': '供应商内部编码',
          'text': '—'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'feeSecTitle': '在租状态（库存状态口径）',
      'feeCols': ['在租', '待归还（超期）', '平均循环', '平均租期', '台账'],
      'fees': [
        {
          'cells': ['0 套', '0 套', '—', '—', '客户在租（无在租）'],
          'links': {
            4: '仓储作业/库存查询.html'
          }
        }
      ],
      'chain': [
        {
          'role': '物料档案（本档）',
          'name': 'KJ-2701 · 启用',
          'self': true
        }
      ],
      'timeline': [
        {
          't': '2026-04-22',
          'text': '建档 · 启用（G38 物料类型 10 值扩展示例）',
          'who': '张帆'
        }
      ]
    }
  },  /* -------------------------------------------------------------------------- */
  /* 库位档案 locations：键 = 库位编码（基础数据/库位档案.html 10 行全量） */
  /* 存放物料按库区真实分布 */
  locations: {
'RA-A-01-01': {
      'row': {"fields": {"wh": "原料区 RA", "ltype": "存储位", "spec": "1.2m×1.0m / 2t", "usage": "68%", "status": "启用"}, "cells": ["原料区 RA", "存储位", "1.2m×1.0m / 2t", "68%", "<span class=\"tag-green\">启用</span>"], "ops": [{"t": "编辑", "act": "go('../基础数据/库位新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
    },
    'RA-A-01-02': {
      'row': {"fields": {"wh": "原料区 RA", "ltype": "存储位", "spec": "1.2m×1.0m / 2t", "usage": "45%", "status": "启用"}, "cells": ["原料区 RA", "存储位", "1.2m×1.0m / 2t", "45%", "<span class=\"tag-green\">启用</span>"], "ops": [{"t": "编辑", "act": "go('../基础数据/库位新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
    },
    'RA-B-02-01': {
      'row': {"fields": {"wh": "原料区 RA", "ltype": "存储位", "spec": "1.2m×1.0m / 2t", "usage": "0%", "status": "启用"}, "cells": ["原料区 RA", "存储位", "1.2m×1.0m / 2t", "0%", "<span class=\"tag-green\">启用</span>"], "ops": [{"t": "编辑", "act": "go('../基础数据/库位新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
    },
    'RB-A-01-01': {
      'row': {"fields": {"wh": "成品区 RB", "ltype": "存储位", "spec": "1.2m×1.0m / 2t", "usage": "82%", "status": "启用"}, "cells": ["成品区 RB", "存储位", "1.2m×1.0m / 2t", "82%", "<span class=\"tag-green\">启用</span>"], "ops": [{"t": "编辑", "act": "go('../基础数据/库位新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
    },
    'RB-A-01-02': {
      'row': {"fields": {"wh": "成品区 RB", "ltype": "存储位", "spec": "1.2m×1.0m / 2t", "usage": "74%", "status": "启用"}, "cells": ["成品区 RB", "存储位", "1.2m×1.0m / 2t", "74%", "<span class=\"tag-green\">启用</span>"], "ops": [{"t": "编辑", "act": "go('../基础数据/库位新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
    },
    'RB-B-01-01': {
      'row': {"fields": {"wh": "成品区 RB", "ltype": "拣选位", "spec": "1.2m×1.0m / 1.5t", "usage": "60%", "status": "启用"}, "cells": ["成品区 RB", "拣选位", "1.2m×1.0m / 1.5t", "60%", "<span class=\"tag-green\">启用</span>"], "ops": [{"t": "编辑", "act": "go('../基础数据/库位新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
    },
    'RD-01': {
      'row': {"fields": {"wh": "成品区 RB", "ltype": "组装暂存", "spec": "工位 1", "usage": "组装中", "status": "启用"}, "cells": ["成品区 RB", "组装暂存", "工位 1", "组装中", "<span class=\"tag-green\">启用</span>"], "ops": [{"t": "编辑", "act": "go('../基础数据/库位新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
    },
    'RD-02': {
      'row': {"fields": {"wh": "成品区 RB", "ltype": "组装暂存", "spec": "工位 2", "usage": "空闲", "status": "启用"}, "cells": ["成品区 RB", "组装暂存", "工位 2", "空闲", "<span class=\"tag-green\">启用</span>"], "ops": [{"t": "编辑", "act": "go('../基础数据/库位新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
    },
    'RC-01': {
      'row': {"fields": {"wh": "次品区 RC", "ltype": "退货暂存", "spec": "1.2m×1.0m / 2t", "usage": "36%", "status": "启用"}, "cells": ["次品区 RC", "退货暂存", "1.2m×1.0m / 2t", "36%", "<span class=\"tag-green\">启用</span>"], "ops": [{"t": "编辑", "act": "go('../基础数据/库位新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
    },
    'RC-02': {
      'row': {"fields": {"wh": "次品区 RC", "ltype": "退货暂存", "spec": "1.2m×1.0m / 2t", "usage": "0%", "status": "停用"}, "cells": ["次品区 RC", "退货暂存", "1.2m×1.0m / 2t", "0%", "<span class=\"tag-gray\">停用</span>"], "ops": [{"t": "编辑", "act": "go('../基础数据/库位新建.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]},
    }
  },

  /* -------------------------------------------------------------------------- */
  /* BOM 版本 bomVersions：键 = 版本号（基础数据/BOM维护.html 3 行全量） */
  /* 弹窗 bomViewModal · 触发锚「查看」；V2.1/V2.0/V1.0 配方演进 */
  bomVersions: {
    'V2.1': {
      'row': {"fields": {}, "keyHtml": "<span class=\"ver-tag\">V2.1<span class=\"tag tag-green\">已生效</span></span>", "cells": ["2026-08-20", "<span class=\"tag-green\">自购</span>", "陈锋", "锁扣配比 6→4，按客户产线上线反馈调整"], "ops": [{"t": "查看", "act": "go('../基础数据/BOM版本查看.html?id=V2.1')"}, {"t": "复制为新版本"}]},
      'title': 'BOM 版本查看',
      'titleNo': 'ZH-2601-A V2.1',
      'info': [
        {
          'label': 'BOM物料编码',
          'text': 'ZH-2601-A'
        },
        {
          'label': 'BOM物料名称',
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
          'text': '陈锋'
        },
        {
          'label': '变更说明',
          'text': '锁扣配比 6→4，按客户产线上线反馈调整',
          'full': true
        },
        {
          'label': '状态',
          'text': '已生效'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'feeSecTitle': '配方行（V2.1）',
      'feeCols': ['子项编码', '子项名称', '来源', '类型', '单位用量', '供应商（带出）'],
      'fees': [
        {
          'cells': ['WBX-1210L', '围板箱 1200×1000×970', '自购', '器具', '1', '甬城塑业包装制品有限公司']
        },
        {
          'cells': ['LJ-C300', '围板 HDPE 波纹板', '自购', '零件', '4', '甬城塑业包装制品有限公司']
        },
        {
          'cells': ['LJ-D400', '箱盖 ABS 吸塑', '自购', '器具', '1', '甬城塑业包装制品有限公司']
        },
        {
          'cells': ['LJ-A100', '锁扣组件 不锈钢', '自购', '零件', '4', '吴越联合五金制品有限公司']
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
          'who': '江强'
        },
        {
          't': '2026-05-14',
          'text': 'V2.0 停用 · 新增内衬可选配、围板 5→4',
          'who': '陈锋'
        },
        {
          't': '2026-08-20',
          'text': 'V2.1 生效 · 锁扣配比 6→4',
          'who': '陈锋'
        }
      ]
    },
    'V2.0': {
      'row': {"fields": {}, "keyHtml": "<span class=\"ver-tag\">V2.0<span class=\"tag tag-gray\">停用</span></span>", "cells": ["2026-05-14", "<span class=\"tag-green\">自购</span>", "陈锋", "新增内衬可选配；围板由 5 块改 4 块"], "ops": [{"t": "查看", "act": "go('../基础数据/BOM版本查看.html?id=V2.1')"}, {"t": "复制为新版本"}]},
      'title': 'BOM 版本查看',
      'titleNo': 'ZH-2601-A V2.0',
      'info': [
        {
          'label': 'BOM物料编码',
          'text': 'ZH-2601-A'
        },
        {
          'label': 'BOM物料名称',
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
          'text': '陈锋'
        },
        {
          'label': '变更说明',
          'text': '新增内衬可选配；围板由 5 块改 4 块',
          'full': true
        },
        {
          'label': '状态',
          'text': '停用'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'feeSecTitle': '配方行（V2.0）',
      'feeCols': ['子项编码', '子项名称', '来源', '类型', '单位用量', '供应商（带出）'],
      'fees': [
        {
          'cells': ['WBX-1210L', '围板箱 1200×1000×970', '自购', '器具', '1', '甬城塑业包装制品有限公司']
        },
        {
          'cells': ['LJ-C300', '围板 HDPE 波纹板', '自购', '零件', '4', '甬城塑业包装制品有限公司']
        },
        {
          'cells': ['LJ-D400', '箱盖 ABS 吸塑', '自购', '器具', '1', '甬城塑业包装制品有限公司']
        },
        {
          'cells': ['LJ-A100', '锁扣组件 不锈钢', '自购', '零件', '6', '吴越联合五金制品有限公司']
        },
        {
          'cells': ['LJ-F600', '内衬 EPE 珍珠棉', '自购', '零件', '可选配 0-1', '甬城塑业包装制品有限公司']
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
          'who': '陈锋'
        },
        {
          't': '2026-08-20',
          'text': 'V2.0 停用 · 由 V2.1 接替',
          'who': '陈锋'
        }
      ]
    },
    'V1.0': {
      'row': {"fields": {}, "keyHtml": "<span class=\"ver-tag\">V1.0<span class=\"tag tag-gray\">停用</span></span>", "cells": ["2026-01-10", "<span class=\"tag-green\">自购</span>", "江强", "初版"], "ops": [{"t": "查看", "act": "go('../基础数据/BOM版本查看.html?id=V2.1')"}, {"t": "复制为新版本"}]},
      'title': 'BOM 版本查看',
      'titleNo': 'ZH-2601-A V1.0',
      'info': [
        {
          'label': 'BOM物料编码',
          'text': 'ZH-2601-A'
        },
        {
          'label': 'BOM物料名称',
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
          'text': '江强'
        },
        {
          'label': '变更说明',
          'text': '初版',
          'full': true
        },
        {
          'label': '状态',
          'text': '停用'
        },
        {
          'label': '备注',
          'text': '—'
        }
      ],
      'feeSecTitle': '配方行（V1.0）',
      'feeCols': ['子项编码', '子项名称', '来源', '类型', '单位用量', '供应商（带出）'],
      'fees': [
        {
          'cells': ['WBX-1210L', '围板箱 1200×1000×970', '自购', '器具', '1', '甬城塑业包装制品有限公司']
        },
        {
          'cells': ['LJ-C300', '围板 HDPE 波纹板', '自购', '零件', '5', '甬城塑业包装制品有限公司']
        },
        {
          'cells': ['LJ-D400', '箱盖 ABS 吸塑', '自购', '器具', '1', '甬城塑业包装制品有限公司']
        },
        {
          'cells': ['LJ-A100', '锁扣组件 不锈钢', '自购', '零件', '6', '吴越联合五金制品有限公司']
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
          'who': '江强'
        },
        {
          't': '2026-05-14',
          'text': 'V1.0 停用 · 由 V2.0 接替',
          'who': '陈锋'
        }
      ]
    }
  },
  /* --------------------------------------------------------------------------
   * 角色 roles：键 = RL-xx（角色管理页列表驱动，2026-09-09 G01）
   *   fields: name=角色名 desc=说明 scope=数据权限 accts=账号数；cells 不含外层 td
   * ------------------------------------------------------------------------ */
  roles: {
    'RL-01': { 'row': {"fields": {"name": "系统管理员", "desc": "全部功能 + 系统管理", "scope": "全部项目", "accts": "2"}, "keyHtml": "<b>系统管理员</b>", "cells": ["全部功能 + 系统管理", "全部项目", "<span class=\"td-num\">2</span>"], "ops": [{"t": "权限配置", "act": "go('../系统管理/权限配置.html?role=系统管理员')"}]} },
    'RL-02': { 'row': {"fields": {"name": "财务", "desc": "财务全模块 + 付款/收款确认审核（主管职责并入）", "scope": "全部项目", "accts": "2"}, "keyHtml": "<b>财务</b>", "cells": ["财务全模块 + 付款/收款确认审核（主管职责并入）", "全部项目", "<span class=\"td-num\">2</span>"], "ops": [{"t": "权限配置", "act": "go('../系统管理/权限配置.html?role=财务')"}]} },
    'RL-03': { 'row': {"fields": {"name": "商务", "desc": "订单/租赁全流程 + 单据审核（主管职责并入）", "scope": "全部项目", "accts": "2"}, "keyHtml": "<b>商务</b>", "cells": ["订单/租赁全流程 + 单据审核（主管职责并入）", "全部项目", "<span class=\"td-num\">2</span>"], "ops": [{"t": "权限配置", "act": "go('../系统管理/权限配置.html?role=商务')"}]} },
    'RL-04': { 'row': {"fields": {"name": "物流", "desc": "仓储作业 + 库存查询 + 出/入库审核（主管职责并入）", "scope": "全部项目", "accts": "2"}, "keyHtml": "<b>物流</b>", "cells": ["仓储作业 + 库存查询 + 出/入库审核（主管职责并入）", "全部项目", "<span class=\"td-num\">2</span>"], "ops": [{"t": "权限配置", "act": "go('../系统管理/权限配置.html?role=物流')"}]} },
    'RL-05': { 'row': {"fields": {"name": "采购", "desc": "采购全流程（订单/入库/退货）+ 供应商税率维护", "scope": "全部项目", "accts": "1"}, "keyHtml": "<b>采购</b>", "cells": ["采购全流程（订单/入库/退货）+ 供应商税率维护", "全部项目", "<span class=\"td-num\">1</span>"], "ops": [{"t": "权限配置", "act": "go('../系统管理/权限配置.html?role=采购')"}]} },
    'RL-06': { 'row': {"fields": {"name": "项目经理", "desc": "项目管理 + 销售订单代下 + 转移出库", "scope": "所属项目", "accts": "1"}, "keyHtml": "<b>项目经理</b>", "cells": ["项目管理 + 销售订单代下 + 转移出库", "所属项目", "<span class=\"td-num\">1</span>"], "ops": [{"t": "权限配置", "act": "go('../系统管理/权限配置.html?role=项目经理')"}]} }
  },

  /* --------------------------------------------------------------------------
 * 操作日志 opLogs：键 = 日志编号（G12 · 系统管理/操作日志 列表驱动）
 *   fields: user/module/opType/time/summary 供筛选（操作人/所属模块/操作类型/时间范围/关键字）
 * ------------------------------------------------------------------------ */
  opLogs: {
    'LOG-20260910-0912': { 'row': {"fields": {"user": "admin", "module": "系统管理", "opType": "登录", "time": "2026-09-10 09:12:05", "summary": "用户 admin 登录系统", "result": "成功"}, "cells": ["2026-09-10 09:12:05", "admin", "系统管理", "<span class=\"tag tag-gray\">登录</span>", "用户 admin 登录系统", "10.8.*.*", "<span class=\"tag tag-green\">成功</span>"]} },
    'LOG-20260910-0910': { 'row': {"fields": {"user": "江强", "module": "项目管理", "opType": "新增", "time": "2026-09-10 09:02:41", "summary": "新增项目档案 PRJ-2605（华骏重卡·蔚山基地围板箱租赁扩建）", "result": "成功"}, "cells": ["2026-09-10 09:02:41", "江强", "项目管理", "<span class=\"tag tag-blue\">新增</span>", "新增项目档案 PRJ-2605（华骏重卡·蔚山基地围板箱租赁扩建）", "10.8.*.*", "<span class=\"tag tag-green\">成功</span>"]} },
    'LOG-20260910-0908': { 'row': {"fields": {"user": "陈锋", "module": "基础数据", "opType": "编辑", "time": "2026-09-10 08:47:19", "summary": "编辑 BOM ZH-2602-B 子项配比（锁扣 2→4）", "result": "成功"}, "cells": ["2026-09-10 08:47:19", "陈锋", "基础数据", "<span class=\"tag tag-blue\">编辑</span>", "编辑 BOM ZH-2602-B 子项配比（锁扣 2→4）", "192.168.*.*", "<span class=\"tag tag-green\">成功</span>"]} },
    'LOG-20260909-0906': { 'row': {"fields": {"user": "李婧", "module": "财务管理", "opType": "审核", "time": "2026-09-09 17:36:02", "summary": "审核通过应收账单 AR-20260907-0031（PRJ-2602 · 8 月租金）", "result": "成功"}, "cells": ["2026-09-09 17:36:02", "李婧", "财务管理", "<span class=\"tag tag-orange\">审核</span>", "审核通过应收账单 AR-20260907-0031（PRJ-2602 · 8 月租金）", "192.168.*.*", "<span class=\"tag tag-green\">成功</span>"]} },
    'LOG-20260909-0903': { 'row': {"fields": {"user": "林国栋", "module": "仓储管理", "opType": "新增", "time": "2026-09-09 16:20:44", "summary": "新建其他入库单 QT-20260909-002（华东中心仓 · 托盘余量回库 40 张）", "result": "成功"}, "cells": ["2026-09-09 16:20:44", "林国栋", "仓储管理", "<span class=\"tag tag-blue\">新增</span>", "新建其他入库单 QT-20260909-002（华东中心仓 · 托盘余量回库 40 张）", "10.8.*.*", "<span class=\"tag tag-green\">成功</span>"]} },
    'LOG-20260909-0895': { 'row': {"fields": {"user": "江强", "module": "租赁管理", "opType": "审核", "time": "2026-09-09 11:42:10", "summary": "审核通过租赁单 LZ-20260908-012（华骏重卡 · 围板箱续租 200 只）", "result": "成功"}, "cells": ["2026-09-09 11:42:10", "江强", "租赁管理", "<span class=\"tag tag-orange\">审核</span>", "审核通过租赁单 LZ-20260908-012（华骏重卡 · 围板箱续租 200 只）", "10.8.*.*", "<span class=\"tag tag-green\">成功</span>"]} },
    'LOG-20260908-0890': { 'row': {"fields": {"user": "李婧", "module": "财务管理", "opType": "删除", "time": "2026-09-08 16:55:23", "summary": "删除应收账单 AR-2026-07-PRJ2601 失败（该账单已核销，不可删除）", "result": "失败"}, "cells": ["2026-09-08 16:55:23", "李婧", "财务管理", "<span class=\"tag tag-red\">删除</span>", "删除应收账单 AR-2026-07-PRJ2601 失败（该账单已核销，不可删除）", "192.168.*.*", "<span class=\"tag tag-red\">失败</span>"]} },
    'LOG-20260908-0887': { 'row': {"fields": {"user": "陈锋", "module": "基础数据", "opType": "新增", "time": "2026-09-08 15:30:08", "summary": "新增客商档案（长丰锂电科技 · 客户）", "result": "成功"}, "cells": ["2026-09-08 15:30:08", "陈锋", "基础数据", "<span class=\"tag tag-blue\">新增</span>", "新增客商档案（长丰锂电科技 · 客户）", "10.8.*.*", "<span class=\"tag tag-green\">成功</span>"]} },
    'LOG-20260907-0876': { 'row': {"fields": {"user": "沈婷", "module": "项目管理", "opType": "新增", "time": "2026-09-07 09:50:31", "summary": "提交销售订单 SO-20260907-0044（ZH-2603-C × 80 套）", "result": "成功"}, "cells": ["2026-09-07 09:50:31", "沈婷", "项目管理", "<span class=\"tag tag-blue\">新增</span>", "提交销售订单 SO-20260907-0044（ZH-2603-C × 80 套）", "10.8.*.*", "<span class=\"tag tag-green\">成功</span>"]} },
    'LOG-20260906-0870': { 'row': {"fields": {"user": "admin", "module": "系统管理", "opType": "编辑", "time": "2026-09-06 17:22:15", "summary": "调整用户权限（邵磊 · 停用账号）", "result": "成功"}, "cells": ["2026-09-06 17:22:15", "admin", "系统管理", "<span class=\"tag tag-blue\">编辑</span>", "调整用户权限（邵磊 · 停用账号）", "10.8.*.*", "<span class=\"tag tag-green\">成功</span>"]} },
  },

  /* --------------------------------------------------------------------------
 * 用户权限 users：键 = 用户账号（G12 · 系统管理/用户权限 列表驱动；页面第二表「角色管理」复用 roles 实体页面静态展示）
 *   fields: search(账号+姓名 联合模糊)/role/scope/status（side/所属方 2026-09-14 拍板随客户/供应商账号移除）
 * ------------------------------------------------------------------------ */
  users: {
    'admin': { 'row': {"fields": {"search": "admin 系统管理员", "role": "系统管理员", "scope": "全部数据", "status": "启用"}, "cells": ["系统管理员", "<span class=\"tag tag-blue\">系统管理员</span>", "全部数据", "138****0001", "<span class=\"tag tag-green\">启用</span>", "2026-09-10 09:12"], "ops": [{"t": "编辑", "act": "go('../系统管理/用户新建.html')"}, {"t": "权限配置", "act": "go('../系统管理/权限配置.html')"}, {"t": "重置密码", "act": "openModal('resetModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'jiangqiang': { 'row': {"fields": {"search": "jiangqiang 江强", "role": "商务", "scope": "全部数据", "status": "启用"}, "cells": ["江强", "<span class=\"tag tag-blue\">商务</span>", "全部数据", "139****0102", "<span class=\"tag tag-green\">启用</span>", "2026-09-10 08:40"], "ops": [{"t": "编辑", "act": "go('../系统管理/用户新建.html')"}, {"t": "权限配置", "act": "go('../系统管理/权限配置.html')"}, {"t": "重置密码", "act": "openModal('resetModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'chenfeng': { 'row': {"fields": {"search": "chenfeng 陈锋", "role": "商务", "scope": "华东区", "status": "启用"}, "cells": ["陈锋", "<span class=\"tag tag-blue\">商务</span>", "华东区", "137****2031", "<span class=\"tag tag-green\">启用</span>", "2026-09-09 18:22"], "ops": [{"t": "编辑", "act": "go('../系统管理/用户新建.html')"}, {"t": "权限配置", "act": "go('../系统管理/权限配置.html')"}, {"t": "重置密码", "act": "openModal('resetModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'lijing': { 'row': {"fields": {"search": "lijing 李婧", "role": "财务", "scope": "全部数据", "status": "启用"}, "cells": ["李婧", "<span class=\"tag tag-blue\">财务</span>", "全部数据", "136****3345", "<span class=\"tag tag-green\">启用</span>", "2026-09-10 09:05"], "ops": [{"t": "编辑", "act": "go('../系统管理/用户新建.html')"}, {"t": "权限配置", "act": "go('../系统管理/权限配置.html')"}, {"t": "重置密码", "act": "openModal('resetModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'linguodong': { 'row': {"fields": {"search": "linguodong 林国栋", "role": "物流", "scope": "华东区", "status": "启用"}, "cells": ["林国栋", "<span class=\"tag tag-blue\">物流</span>", "华东区", "135****4567", "<span class=\"tag tag-green\">启用</span>", "2026-09-10 08:15"], "ops": [{"t": "编辑", "act": "go('../系统管理/用户新建.html')"}, {"t": "权限配置", "act": "go('../系统管理/权限配置.html')"}, {"t": "重置密码", "act": "openModal('resetModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'shaolei': { 'row': {"fields": {"search": "shaolei 邵磊", "role": "物流", "scope": "华东中心仓", "status": "停用"}, "cells": ["邵磊", "<span class=\"tag tag-blue\">物流</span>", "华东中心仓", "133****5689", "<span class=\"tag tag-gray\">停用</span>", "2026-08-30 17:44"], "ops": [{"t": "编辑", "act": "go('../系统管理/用户新建.html')"}, {"t": "权限配置", "act": "go('../系统管理/权限配置.html')"}, {"t": "重置密码", "act": "openModal('resetModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'xuwen': { 'row': {"fields": {"search": "xuwen 徐文", "role": "采购", "scope": "全部数据", "status": "启用"}, "cells": ["徐文", "<span class=\"tag tag-blue\">采购</span>", "全部数据", "132****7801", "<span class=\"tag tag-green\">启用</span>", "2026-09-14 10:20"], "ops": [{"t": "编辑", "act": "go('../系统管理/用户新建.html')"}, {"t": "权限配置", "act": "go('../系统管理/权限配置.html')"}, {"t": "重置密码", "act": "openModal('resetModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'shenting': { 'row': {"fields": {"search": "shenting 沈婷", "role": "项目经理", "scope": "所属项目", "status": "启用"}, "cells": ["沈婷", "<span class=\"tag tag-blue\">项目经理</span>", "所属项目", "131****9012", "<span class=\"tag tag-green\">启用</span>", "2026-09-14 10:22"], "ops": [{"t": "编辑", "act": "go('../系统管理/用户新建.html')"}, {"t": "权限配置", "act": "go('../系统管理/权限配置.html')"}, {"t": "重置密码", "act": "openModal('resetModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
  },

  /* --------------------------------------------------------------------------
 * 数据字典 dictItems：键 = 分类前缀-序号（G12 · 系统管理/数据字典 分类切换驱动；10 分类 × 2-6 行）
 *   fields: category/abbr/name/status；左部分类列表点击 → 按 category 过滤主表并联动计数（计费方式卡片保持静态展示）
 * ------------------------------------------------------------------------ */
  dictItems: {
    'MSG-01': { 'row': {"fields": {"category": "消息类型", "abbr": "账单到期", "name": "站内信·账单到期", "status": "启用"}, "cells": ["账单到期", "站内信·账单到期", "<span class=\"td-num\">1</span>", "pc-msg.js 消息面板类型筛选值源（D-126·双源同步）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]}},

    'MSG-02': { 'row': {"fields": {"category": "消息类型", "abbr": "分期付款", "name": "站内信·分期付款", "status": "启用"}, "cells": ["分期付款", "站内信·分期付款", "<span class=\"td-num\">2</span>", "pc-msg.js 消息面板类型筛选值源（D-126·双源同步）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]}},

    'MSG-03': { 'row': {"fields": {"category": "消息类型", "abbr": "押金应退", "name": "站内信·押金应退", "status": "启用"}, "cells": ["押金应退", "站内信·押金应退", "<span class=\"td-num\">3</span>", "pc-msg.js 消息面板类型筛选值源（D-126·双源同步）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]}},

    'MSG-04': { 'row': {"fields": {"category": "消息类型", "abbr": "续租跟进", "name": "站内信·续租跟进", "status": "启用"}, "cells": ["续租跟进", "站内信·续租跟进", "<span class=\"td-num\">4</span>", "pc-msg.js 消息面板类型筛选值源（D-126·双源同步）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]}},
    'DT-01': { 'row': {"fields": {"category": "缺损类型", "abbr": "PS", "name": "破损", "status": "启用"}, "cells": ["PS", "破损", "<span class=\"td-num\">1</span>", "外观或结构损坏，可维修", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DT-02': { 'row': {"fields": {"category": "缺损类型", "abbr": "QS", "name": "缺失", "status": "启用"}, "cells": ["QS", "缺失", "<span class=\"td-num\">2</span>", "回收时无法找到的部件", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DT-03': { 'row': {"fields": {"category": "缺损类型", "abbr": "BX", "name": "变形", "status": "启用"}, "cells": ["BX", "变形", "<span class=\"td-num\">3</span>", "超差变形影响使用", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DT-04': { 'row': {"fields": {"category": "缺损类型", "abbr": "WS", "name": "污损", "status": "停用"}, "cells": ["WS", "污损", "<span class=\"td-num\">4</span>", "严重污染无法清理", "<span class=\"tag tag-gray\">停用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DT-05': { 'row': {"fields": {"category": "缺损类型", "abbr": "LH", "name": "老化", "status": "启用"}, "cells": ["LH", "老化", "<span class=\"td-num\">5</span>", "达到设计寿命正常老化", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DT-06': { 'row': {"fields": {"category": "缺损类型", "abbr": "HJ", "name": "划痕", "status": "启用"}, "cells": ["HJ", "划痕", "<span class=\"td-num\">6</span>", "外表层划痕，影响外观不影响使用", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'BF-01': { 'row': {"fields": {"category": "计费方式", "abbr": "按月", "name": "按月计租", "status": "启用"}, "cells": ["按月", "按月计租", "<span class=\"td-num\">1</span>", "月租金 / 按套数单价 · 围板箱/托盘租赁", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'BF-02': { 'row': {"fields": {"category": "计费方式", "abbr": "按次", "name": "按次计费", "status": "启用"}, "cells": ["按次", "按次计费", "<span class=\"td-num\">2</span>", "出库/退租次数 × 次单价 · 组装服务费", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'BF-03': { 'row': {"fields": {"category": "计费方式", "abbr": "按张", "name": "按张计费", "status": "停用"}, "cells": ["按张", "按张计费", "<span class=\"td-num\">3</span>", "在租张数 × 张单价 · 托盘/料箱备用口径", "<span class=\"tag tag-gray\">停用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'BF-04': { 'row': {"fields": {"category": "计费方式", "abbr": "按年", "name": "按年计租", "status": "启用"}, "cells": ["按年", "按年计租", "<span class=\"td-num\">4</span>", "年租金 × 租期年数 · 长周期备用口径", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'BF-05': { 'row': {"fields": {"category": "计费方式", "abbr": "按日", "name": "按日计租", "status": "启用"}, "cells": ["按日", "按日计租", "<span class=\"td-num\">5</span>", "周期单位 · 三段式档案参考价用（G39 起单据侧直录日租金）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'BF-06': { 'row': {"fields": {"category": "计费方式", "abbr": "按时间周期", "name": "按时间周期计租（直录日租金）", "status": "启用"}, "cells": ["按时间周期", "按时间周期计租（直录日租金）", "<span class=\"td-num\">6</span>", "日租金 × 每日在租数量 × 天数 · 按持有量计租（D-148）", "<span class=\"tag tag-green\">启用</span>"]} },
    'ZT-01': { 'row': {"fields": {"category": "单据状态", "abbr": "CG", "name": "草稿", "status": "启用"}, "cells": ["CG", "草稿", "<span class=\"td-num\">1</span>", "保存未提交", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZT-02': { 'row': {"fields": {"category": "单据状态", "abbr": "DSH", "name": "待审核", "status": "启用"}, "cells": ["DSH", "待审核", "<span class=\"td-num\">2</span>", "已提交待审核", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZT-03': { 'row': {"fields": {"category": "单据状态", "abbr": "YSH", "name": "已审核", "status": "启用"}, "cells": ["YSH", "已审核", "<span class=\"td-num\">3</span>", "审核通过流转中", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZT-04': { 'row': {"fields": {"category": "单据状态", "abbr": "ZX", "name": "执行中", "status": "启用"}, "cells": ["ZX", "执行中", "<span class=\"td-num\">4</span>", "业务执行中", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZT-05': { 'row': {"fields": {"category": "单据状态", "abbr": "WC", "name": "已完成", "status": "启用"}, "cells": ["WC", "已完成", "<span class=\"td-num\">5</span>", "业务闭环", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZT-06': { 'row': {"fields": {"category": "单据状态", "abbr": "QX", "name": "已取消", "status": "启用"}, "cells": ["QX", "已取消", "<span class=\"td-num\">6</span>", "作废或取消", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DW-01': { 'row': {"fields": {"category": "计量单位", "abbr": "GE", "name": "个", "status": "启用"}, "cells": ["GE", "个", "<span class=\"td-num\">1</span>", "计数单位", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DW-02': { 'row': {"fields": {"category": "计量单位", "abbr": "TAO", "name": "套", "status": "启用"}, "cells": ["TAO", "套", "<span class=\"td-num\">2</span>", "组合件计量", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DW-03': { 'row': {"fields": {"category": "计量单位", "abbr": "ZHI", "name": "只", "status": "启用"}, "cells": ["ZHI", "只", "<span class=\"td-num\">3</span>", "器具常用计量", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DW-04': { 'row': {"fields": {"category": "计量单位", "abbr": "ZHANG", "name": "张", "status": "启用"}, "cells": ["ZHANG", "张", "<span class=\"td-num\">4</span>", "围板/托盘计量", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DW-05': { 'row': {"fields": {"category": "计量单位", "abbr": "JIAN", "name": "件", "status": "启用"}, "cells": ["JIAN", "件", "<span class=\"td-num\">5</span>", "出库/退租计量", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DW-06': { 'row': {"fields": {"category": "计量单位", "abbr": "TAI", "name": "台", "status": "启用"}, "cells": ["TAI", "台", "<span class=\"td-num\">6</span>", "设备计量", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DW-07': { 'row': {"fields": {"category": "计量单位", "abbr": "DW-07", "name": "托", "status": "启用"}, "cells": ["DW-07", "托", "<span class=\"td-num\">7</span>", "托盘计量", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'PJ-01': { 'row': {"fields": {"category": "项目状态", "abbr": "CB", "name": "筹备中", "status": "启用"}, "cells": ["CB", "筹备中", "<span class=\"td-num\">1</span>", "立项筹备未开工", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'PJ-02': { 'row': {"fields": {"category": "项目状态", "abbr": "ZX", "name": "执行中", "status": "启用"}, "cells": ["ZX", "执行中", "<span class=\"td-num\">2</span>", "业务执行中", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'PJ-03': { 'row': {"fields": {"category": "项目状态", "abbr": "JJ", "name": "已结项", "status": "启用"}, "cells": ["JJ", "已结项", "<span class=\"td-num\">3</span>", "正常完结", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'PJ-04': { 'row': {"fields": {"category": "项目状态", "abbr": "ZJ", "name": "已终止", "status": "启用"}, "cells": ["ZJ", "已终止", "<span class=\"td-num\">4</span>", "提前终止/暂停", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'LX-01': { 'row': {"fields": {"category": "单据类型", "abbr": "SO", "name": "销售订单", "status": "启用"}, "cells": ["SO", "销售订单", "<span class=\"td-num\">1</span>", "项目经理代下单", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'LX-02': { 'row': {"fields": {"category": "单据类型", "abbr": "PO", "name": "采购订单", "status": "启用"}, "cells": ["PO", "采购订单", "<span class=\"td-num\">2</span>", "自购器具采购", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'LX-03': { 'row': {"fields": {"category": "单据类型", "abbr": "LZ", "name": "租赁单", "status": "启用"}, "cells": ["LZ", "租赁单", "<span class=\"td-num\">3</span>", "客户租赁主单", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'LX-04': { 'row': {"fields": {"category": "单据类型", "abbr": "CK", "name": "租赁出库单", "status": "启用"}, "cells": ["CK", "租赁出库单", "<span class=\"td-num\">4</span>", "租赁租赁出库", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'LX-05': { 'row': {"fields": {"category": "单据类型", "abbr": "TK", "name": "退租入库单", "status": "启用"}, "cells": ["TK", "退租入库单", "<span class=\"td-num\">5</span>", "客户退租入库", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'LX-06': { 'row': {"fields": {"category": "单据类型", "abbr": "RZ", "name": "租入单", "status": "启用"}, "cells": ["RZ", "租入单", "<span class=\"td-num\">6</span>", "向供应商租入", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'XH-01': { 'row': {"fields": {"category": "循环状态", "abbr": "ZK", "name": "在库", "status": "启用"}, "cells": ["ZK", "在库", "<span class=\"td-num\">1</span>", "库存待租", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'XH-02': { 'row': {"fields": {"category": "循环状态", "abbr": "ZZ", "name": "在租", "status": "启用"}, "cells": ["ZZ", "在租", "<span class=\"td-num\">2</span>", "客户在租", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'XH-03': { 'row': {"fields": {"category": "循环状态", "abbr": "SD", "name": "锁定", "status": "启用"}, "cells": ["SD", "锁定", "<span class=\"td-num\">3</span>", "出库锁定/预留", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'XH-04': { 'row': {"fields": {"category": "循环状态", "abbr": "BF", "name": "报废", "status": "启用"}, "cells": ["BF", "报废", "<span class=\"td-num\">4</span>", "报废待处置", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'XH-05': { 'row': {"fields": {"category": "循环状态", "abbr": "DS", "name": "丢失", "status": "启用"}, "cells": ["DS", "丢失", "<span class=\"td-num\">5</span>", "丢失未找回", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'KW-01': { 'row': {"fields": {"category": "库位类型", "abbr": "CC", "name": "存储位", "status": "启用"}, "cells": ["CC", "存储位", "<span class=\"td-num\">1</span>", "常规存储", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'KW-02': { 'row': {"fields": {"category": "库位类型", "abbr": "JX", "name": "拣选位", "status": "启用"}, "cells": ["JX", "拣选位", "<span class=\"td-num\">2</span>", "出库拣选", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'KW-03': { 'row': {"fields": {"category": "库位类型", "abbr": "ZC", "name": "暂存位", "status": "启用"}, "cells": ["ZC", "暂存位", "<span class=\"td-num\">3</span>", "收发货暂存", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'KW-04': { 'row': {"fields": {"category": "库位类型", "abbr": "BH", "name": "不合格品位", "status": "启用"}, "cells": ["BH", "不合格品位", "<span class=\"td-num\">4</span>", "缺损隔离", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'YH-01': { 'row': {"fields": {"category": "银行账户", "abbr": "JB", "name": "对公基本户", "status": "启用"}, "cells": ["JB", "对公基本户", "<span class=\"td-num\">1</span>", "日常收付结算", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'YH-02': { 'row': {"fields": {"category": "银行账户", "abbr": "YB", "name": "对公一般户", "status": "启用"}, "cells": ["YB", "对公一般户", "<span class=\"td-num\">2</span>", "专项收支", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'YH-03': { 'row': {"fields": {"category": "银行账户", "abbr": "BX", "name": "保证金户", "status": "启用"}, "cells": ["BX", "保证金户", "<span class=\"td-num\">3</span>", "投标/履约保证金", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZF-01': { 'row': {"fields": {"category": "支付方式", "abbr": "ZZ", "name": "银行转账", "status": "启用"}, "cells": ["ZZ", "银行转账", "<span class=\"td-num\">1</span>", "主流收付方式", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZF-02': { 'row': {"fields": {"category": "支付方式", "abbr": "CD", "name": "承兑", "status": "启用"}, "cells": ["CD", "承兑", "<span class=\"td-num\">2</span>", "承兑汇票", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZF-03': { 'row': {"fields": {"category": "支付方式", "abbr": "ZF-03", "name": "现金", "status": "启用"}, "cells": ["ZF-03", "现金", "<span class=\"td-num\">3</span>", "现金收付", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZF-04': { 'row': {"fields": {"category": "支付方式", "abbr": "ZF-04", "name": "票据", "status": "启用"}, "cells": ["ZF-04", "票据", "<span class=\"td-num\">4</span>", "票据收付", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'WL-01': { 'row': {"fields": {"category": "物料类型", "abbr": "WL-01", "name": "围板箱", "status": "启用"}, "cells": ["WL-01", "围板箱", "<span class=\"td-num\">1</span>", "可折叠周转箱", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'WL-02': { 'row': {"fields": {"category": "物料类型", "abbr": "WL-02", "name": "塑料托盘", "status": "启用"}, "cells": ["WL-02", "塑料托盘", "<span class=\"td-num\">2</span>", "塑料栈板", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'WL-03': { 'row': {"fields": {"category": "物料类型", "abbr": "WL-03", "name": "木托盘", "status": "启用"}, "cells": ["WL-03", "木托盘", "<span class=\"td-num\">3</span>", "木质栈板", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'WL-04': { 'row': {"fields": {"category": "物料类型", "abbr": "WL-04", "name": "料箱", "status": "启用"}, "cells": ["WL-04", "料箱", "<span class=\"td-num\">4</span>", "小型周转箱", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'WL-05': { 'row': {"fields": {"category": "物料类型", "abbr": "WL-05", "name": "料架", "status": "启用"}, "cells": ["WL-05", "料架", "<span class=\"td-num\">5</span>", "金属料架", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'WL-06': { 'row': {"fields": {"category": "物料类型", "abbr": "WL-06", "name": "组件", "status": "启用"}, "cells": ["WL-06", "组件", "<span class=\"td-num\">6</span>", "BOM 组合件（ZH-* 母件）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'WL-07': { 'row': {"fields": {"category": "物料类型", "abbr": "WL-07", "name": "卡板箱", "status": "启用"}, "cells": ["WL-07", "卡板箱", "<span class=\"td-num\">7</span>", "钢制/塑钢卡板箱", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'WL-08': { 'row': {"fields": {"category": "物料类型", "abbr": "WL-08", "name": "金属托盘", "status": "启用"}, "cells": ["WL-08", "金属托盘", "<span class=\"td-num\">8</span>", "钢制金属托盘", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'WL-09': { 'row': {"fields": {"category": "物料类型", "abbr": "WL-09", "name": "内衬", "status": "启用"}, "cells": ["WL-09", "内衬", "<span class=\"td-num\">9</span>", "E500/F600 等隔衬件", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'WL-10': { 'row': {"fields": {"category": "物料类型", "abbr": "WL-10", "name": "零部件", "status": "启用"}, "cells": ["WL-10", "零部件", "<span class=\"td-num\">10</span>", "锁扣/铰链/围板/箱盖/底托架", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'KC-01': { 'row': {"fields": {"category": "库存状态", "abbr": "KC-01", "name": "在库", "status": "启用"}, "cells": ["KC-01", "在库", "<span class=\"td-num\">1</span>", "自有库存在仓", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'KC-02': { 'row': {"fields": {"category": "库存状态", "abbr": "KC-02", "name": "客户端(租出)", "status": "启用"}, "cells": ["KC-02", "客户端(租出)", "<span class=\"td-num\">2</span>", "租赁在客户处", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'KC-03': { 'row': {"fields": {"category": "库存状态", "abbr": "KC-03", "name": "客户转租出", "status": "启用"}, "cells": ["KC-03", "客户转租出", "<span class=\"td-num\">3</span>", "客户转租第三方", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'KC-04': { 'row': {"fields": {"category": "库存状态", "abbr": "KC-04", "name": "退租待入库", "status": "启用"}, "cells": ["KC-04", "退租待入库", "<span class=\"td-num\">4</span>", "退租验收待入库", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'KC-05': { 'row': {"fields": {"category": "库存状态", "abbr": "KC-05", "name": "租入", "status": "启用"}, "cells": ["KC-05", "租入", "<span class=\"td-num\">5</span>", "向供应商租入在仓", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'RKU-01': { 'row': {"fields": {"category": "入库类型", "abbr": "RKU-01", "name": "盘盈", "status": "启用"}, "cells": ["RKU-01", "盘盈", "<span class=\"td-num\">1</span>", "盘点盈余入账", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'RKU-02': { 'row': {"fields": {"category": "入库类型", "abbr": "RKU-02", "name": "退货", "status": "启用"}, "cells": ["RKU-02", "退货", "<span class=\"td-num\">2</span>", "销售退货入库", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'RKU-03': { 'row': {"fields": {"category": "入库类型", "abbr": "RKU-03", "name": "其他", "status": "启用"}, "cells": ["RKU-03", "其他", "<span class=\"td-num\">3</span>", "手工例外入库", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'CKU-01': { 'row': {"fields": {"category": "出库类型", "abbr": "CKU-01", "name": "报废", "status": "启用"}, "cells": ["CKU-01", "报废", "<span class=\"td-num\">1</span>", "损坏报废出库", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'CKU-02': { 'row': {"fields": {"category": "出库类型", "abbr": "CKU-02", "name": "盘亏", "status": "启用"}, "cells": ["CKU-02", "盘亏", "<span class=\"td-num\">2</span>", "盘点亏损出账", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'CKU-03': { 'row': {"fields": {"category": "出库类型", "abbr": "CKU-03", "name": "赔偿核销", "status": "启用"}, "cells": ["CKU-03", "赔偿核销", "<span class=\"td-num\">3</span>", "丢损赔偿核销", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'CKU-04': { 'row': {"fields": {"category": "出库类型", "abbr": "CKU-04", "name": "其他", "status": "启用"}, "cells": ["CKU-04", "其他", "<span class=\"td-num\">4</span>", "手工例外出库", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ARB-01': { 'row': {"fields": {"category": "应收账单类型", "abbr": "ARB-01", "name": "租赁费", "status": "启用"}, "cells": ["ARB-01", "租赁费", "<span class=\"td-num\">1</span>", "按租赁出库汇总", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ARB-02': { 'row': {"fields": {"category": "应收账单类型", "abbr": "ARB-02", "name": "销售费", "status": "启用"}, "cells": ["ARB-02", "销售费", "<span class=\"td-num\">2</span>", "按销售出库汇总", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ARB-03': { 'row': {"fields": {"category": "应收账单类型", "abbr": "ARB-03", "name": "丢损赔偿", "status": "启用"}, "cells": ["ARB-03", "丢损赔偿", "<span class=\"td-num\">3</span>", "客户赔付我方", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ARB-04': { 'row': {"fields": {"category": "应收账单类型", "abbr": "ARB-04", "name": "供应商应收", "status": "启用"}, "cells": ["ARB-04", "供应商应收", "<span class=\"td-num\">4</span>", "供应商赔付我方", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ARB-05': { 'row': {"fields": {"category": "应收账单类型", "abbr": "ARB-05", "name": "押金", "status": "启用"}, "cells": ["ARB-05", "押金", "<span class=\"td-num\">5</span>", "收客户租赁押金", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ARB-06': { 'row': {"fields": {"category": "应收账单类型", "abbr": "ARB-06", "name": "预付款（保证金）", "status": "启用"}, "cells": ["ARB-06", "预付款（保证金）", "<span class=\"td-num\">6</span>", "无订单直接建单", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ARB-07': { 'row': {"fields": {"category": "应收账单类型", "abbr": "ARB-07", "name": "预收", "status": "启用"}, "cells": ["ARB-07", "预收", "<span class=\"td-num\">7</span>", "客户预付租金冲抵后续应收", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'APB-01': { 'row': {"fields": {"category": "应付账单类型", "abbr": "APB-01", "name": "采购应付", "status": "启用"}, "cells": ["APB-01", "采购应付", "<span class=\"td-num\">1</span>", "按采购订单汇总", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'APB-02': { 'row': {"fields": {"category": "应付账单类型", "abbr": "APB-02", "name": "租金应付", "status": "启用"}, "cells": ["APB-02", "租金应付", "<span class=\"td-num\">2</span>", "按租入单汇总", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'APB-03': { 'row': {"fields": {"category": "应付账单类型", "abbr": "APB-03", "name": "丢损赔偿（赔付供应商）", "status": "启用"}, "cells": ["APB-03", "丢损赔偿（赔付供应商）", "<span class=\"td-num\">3</span>", "赔付供应商", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'APB-04': { 'row': {"fields": {"category": "应付账单类型", "abbr": "APB-04", "name": "对客户应付", "status": "启用"}, "cells": ["APB-04", "对客户应付", "<span class=\"td-num\">4</span>", "交付延误断产赔付", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'APB-05': { 'row': {"fields": {"category": "应付账单类型", "abbr": "APB-05", "name": "无订单预付款", "status": "启用"}, "cells": ["APB-05", "无订单预付款", "<span class=\"td-num\">5</span>", "付供应商保证金", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'FY-01': { 'row': {"fields": {"category": "费用分类", "abbr": "FY-01", "name": "丢损缺损赔偿", "status": "启用"}, "cells": ["FY-01", "丢损缺损赔偿", "<span class=\"td-num\">1</span>", "丢损缺损赔付", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'FY-02': { 'row': {"fields": {"category": "费用分类", "abbr": "FY-02", "name": "违约金", "status": "启用"}, "cells": ["FY-02", "违约金", "<span class=\"td-num\">2</span>", "合同违约计收", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'FY-03': { 'row': {"fields": {"category": "费用分类", "abbr": "FY-03", "name": "断产赔偿", "status": "启用"}, "cells": ["FY-03", "断产赔偿", "<span class=\"td-num\">3</span>", "断产损失赔付", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'FY-04': { 'row': {"fields": {"category": "费用分类", "abbr": "FY-04", "name": "交付延误", "status": "启用"}, "cells": ["FY-04", "交付延误", "<span class=\"td-num\">4</span>", "延误交付赔付", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'FY-05': { 'row': {"fields": {"category": "费用分类", "abbr": "FY-05", "name": "收款违约金", "status": "启用"}, "cells": ["FY-05", "收款违约金", "<span class=\"td-num\">5</span>", "收款逾期计收", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'FY-06': { 'row': {"fields": {"category": "费用分类", "abbr": "FY-06", "name": "保证金", "status": "启用"}, "cells": ["FY-06", "保证金", "<span class=\"td-num\">6</span>", "履约保证金", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'FY-07': { 'row': {"fields": {"category": "费用分类", "abbr": "FY-07", "name": "预付款", "status": "启用"}, "cells": ["FY-07", "预付款", "<span class=\"td-num\">7</span>", "预付租金类", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'FP-01': { 'row': {"fields": {"category": "发票类型", "abbr": "FP-01", "name": "增值税专票 13%", "status": "启用"}, "cells": ["FP-01", "增值税专票 13%", "<span class=\"td-num\">1</span>", "可抵扣进项", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'FP-02': { 'row': {"fields": {"category": "发票类型", "abbr": "FP-02", "name": "增值税普通发票", "status": "启用"}, "cells": ["FP-02", "增值税普通发票", "<span class=\"td-num\">2</span>", "不可抵扣", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'KST-01': { 'row': {"fields": {"category": "客商类型", "abbr": "KST-01", "name": "客户", "status": "启用"}, "cells": ["KST-01", "客户", "<span class=\"td-num\">1</span>", "承租购件客户", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'KST-02': { 'row': {"fields": {"category": "客商类型", "abbr": "KST-02", "name": "供应商", "status": "启用"}, "cells": ["KST-02", "供应商", "<span class=\"td-num\">2</span>", "租入采购供应商", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'KST-03': { 'row': {"fields": {"category": "客商类型", "abbr": "KST-03", "name": "客户兼供应商", "status": "启用"}, "cells": ["KST-03", "客户兼供应商", "<span class=\"td-num\">3</span>", "双向合作客商", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'SJQ-01': { 'row': {"fields": {"category": "数据权限范围", "abbr": "SJQ-01", "name": "全部项目", "status": "启用"}, "cells": ["SJQ-01", "全部项目", "<span class=\"td-num\">1</span>", "全局数据可见", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'SJQ-02': { 'row': {"fields": {"category": "数据权限范围", "abbr": "SJQ-02", "name": "所属客户", "status": "启用"}, "cells": ["SJQ-02", "所属客户", "<span class=\"td-num\">2</span>", "限客户相关数据", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'SJQ-03': { 'row': {"fields": {"category": "数据权限范围", "abbr": "SJQ-03", "name": "所属供应商", "status": "启用"}, "cells": ["SJQ-03", "所属供应商", "<span class=\"td-num\">3</span>", "限供应商相关数据", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'PDK-01': { 'row': {"fields": {"category": "盘点口径", "abbr": "PDK-01", "name": "按物料", "status": "启用"}, "cells": ["PDK-01", "按物料", "<span class=\"td-num\">1</span>", "按物料编码盘点", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'PDK-02': { 'row': {"fields": {"category": "盘点口径", "abbr": "PDK-02", "name": "按库位", "status": "启用"}, "cells": ["PDK-02", "按库位", "<span class=\"td-num\">2</span>", "按库位清点", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZQ-01': { 'row': {"fields": {"category": "周期单位", "abbr": "ZQ-01", "name": "月", "status": "启用"}, "cells": ["ZQ-01", "月", "<span class=\"td-num\">1</span>", "月度计费周期", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZQ-02': { 'row': {"fields": {"category": "周期单位", "abbr": "ZQ-02", "name": "年", "status": "启用"}, "cells": ["ZQ-02", "年", "<span class=\"td-num\">2</span>", "年度计费周期", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZQ-03': { 'row': {"fields": {"category": "周期单位", "abbr": "ZQ-03", "name": "日", "status": "启用"}, "cells": ["ZQ-03", "日", "<span class=\"td-num\">3</span>", "日计费周期", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-01': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-01", "name": "销售订单", "status": "启用"}, "cells": ["DJ-01", "销售订单", "<span class=\"td-num\">1</span>", "代下订单审核", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-02': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-02", "name": "采购订单", "status": "启用"}, "cells": ["DJ-02", "采购订单", "<span class=\"td-num\">2</span>", "采购单审核", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-03': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-03", "name": "租赁单", "status": "启用"}, "cells": ["DJ-03", "租赁单", "<span class=\"td-num\">3</span>", "租赁单审核", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-04': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-04", "name": "销售出库", "status": "启用"}, "cells": ["DJ-04", "销售出库", "<span class=\"td-num\">4</span>", "销售出库单据", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-05': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-05", "name": "退租入库", "status": "启用"}, "cells": ["DJ-05", "退租入库", "<span class=\"td-num\">5</span>", "退租验收单据", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-06': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-06", "name": "盘点", "status": "启用"}, "cells": ["DJ-06", "盘点", "<span class=\"td-num\">6</span>", "盘点单审核", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-07': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-07", "name": "采购入库", "status": "启用"}, "cells": ["DJ-07", "采购入库", "<span class=\"td-num\">7</span>", "采购验收单据", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-08': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-08", "name": "租入入库", "status": "启用"}, "cells": ["DJ-08", "租入入库", "<span class=\"td-num\">8</span>", "租入验收单据", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-09': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-09", "name": "租入归还", "status": "启用"}, "cells": ["DJ-09", "租入归还", "<span class=\"td-num\">9</span>", "归还供应商单据", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-10': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-10", "name": "其他入库", "status": "启用"}, "cells": ["DJ-10", "其他入库", "<span class=\"td-num\">10</span>", "手工入库单据", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-11': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-11", "name": "付款登记", "status": "启用"}, "cells": ["DJ-11", "付款登记", "<span class=\"td-num\">11</span>", "付款单据", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-12': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-12", "name": "收款确认", "status": "启用"}, "cells": ["DJ-12", "收款确认", "<span class=\"td-num\">12</span>", "收款单据", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-13': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-13", "name": "其他出库", "status": "启用"}, "cells": ["DJ-13", "其他出库", "<span class=\"td-num\">13</span>", "手工出库单据", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-14': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-14", "name": "库存调拨", "status": "启用"}, "cells": ["DJ-14", "库存调拨", "<span class=\"td-num\">14</span>", "调拨单据", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-15': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-15", "name": "租入单", "status": "启用"}, "cells": ["DJ-15", "租入单", "<span class=\"td-num\">15</span>", "租入单审核", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-16': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-16", "name": "租赁出库", "status": "启用"}, "cells": ["DJ-16", "租赁出库", "<span class=\"td-num\">16</span>", "租赁出库审核", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-17': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-17", "name": "采购退货单", "status": "启用"}, "cells": ["DJ-17", "采购退货单", "<span class=\"td-num\">17</span>", "采购退货单据（G33）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-18': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-18", "name": "销售退货单", "status": "启用"}, "cells": ["DJ-18", "销售退货单", "<span class=\"td-num\">18</span>", "销售退货单据（G33）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-19': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-19", "name": "退款登记", "status": "启用"}, "cells": ["DJ-19", "退款登记", "<span class=\"td-num\">19</span>", "退款单据（G33）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'DJ-20': { 'row': {"fields": {"category": "待办单据类型", "abbr": "DJ-20", "name": "转移出库", "status": "启用"}, "cells": ["DJ-20", "转移出库", "<span class=\"td-num\">20</span>", "转移单审核（09-16 拍板加审）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'THC-01': { 'row': {"fields": {"category": "退货类型", "abbr": "收货拒收", "name": "收货拒收", "status": "启用"}, "cells": ["收货拒收", "收货拒收", "<span class=\"td-num\">1</span>", "未入库直接退·不产生库存流水（G33·方案 B）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'THC-02': { 'row': {"fields": {"category": "退货类型", "abbr": "入库后退货", "name": "入库后退货", "status": "启用"}, "cells": ["入库后退货", "入库后退货", "<span class=\"td-num\">2</span>", "已入库再退·退货单自身为凭不改原单（D-109）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'TKL-01': { 'row': {"fields": {"category": "退款类型", "abbr": "采购退货退款", "name": "采购退货退款", "status": "启用"}, "cells": ["采购退货退款", "采购退货退款", "<span class=\"td-num\">1</span>", "供应商·我方收款（应付侧）·源自采购退货", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'TKL-02': { 'row': {"fields": {"category": "退款类型", "abbr": "销售退货退款", "name": "销售退货退款", "status": "启用"}, "cells": ["销售退货退款", "销售退货退款", "<span class=\"td-num\">2</span>", "客户·我方付款（应收侧）·源自销售退货", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'TKL-03': { 'row': {"fields": {"category": "退款类型", "abbr": "预收退回", "name": "预收退回", "status": "启用"}, "cells": ["预收退回", "预收退回", "<span class=\"td-num\">3</span>", "客户·我方付款（应收侧）·预收冲抵后余额退回", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'TKL-04': { 'row': {"fields": {"category": "退款类型", "abbr": "多付退回", "name": "多付退回", "status": "启用"}, "cells": ["多付退回", "多付退回", "<span class=\"td-num\">4</span>", "供应商·我方收款（应付侧）·多付款项退回", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },

    'SL-01': { 'row': {"fields": {"category": "供应商税率", "abbr": "SL-01", "name": "0%", "status": "启用"}, "cells": ["SL-01", "0%", "<span class=\"td-num\">1</span>", "供应商默认税率下拉值源（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'SL-02': { 'row': {"fields": {"category": "供应商税率", "abbr": "SL-02", "name": "1%", "status": "启用"}, "cells": ["SL-02", "1%", "<span class=\"td-num\">2</span>", "供应商默认税率下拉值源（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'SL-03': { 'row': {"fields": {"category": "供应商税率", "abbr": "SL-03", "name": "3%", "status": "启用"}, "cells": ["SL-03", "3%", "<span class=\"td-num\">3</span>", "供应商默认税率下拉值源（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'SL-04': { 'row': {"fields": {"category": "供应商税率", "abbr": "SL-04", "name": "6%", "status": "启用"}, "cells": ["SL-04", "6%", "<span class=\"td-num\">4</span>", "供应商默认税率下拉值源（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'SL-05': { 'row': {"fields": {"category": "供应商税率", "abbr": "SL-05", "name": "9%", "status": "启用"}, "cells": ["SL-05", "9%", "<span class=\"td-num\">5</span>", "供应商默认税率下拉值源（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'SL-06': { 'row': {"fields": {"category": "供应商税率", "abbr": "SL-06", "name": "13%", "status": "启用"}, "cells": ["SL-06", "13%", "<span class=\"td-num\">6</span>", "供应商默认税率下拉值源（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'JSQ-01': { 'row': {"fields": {"category": "结算周期", "abbr": "JSQ-01", "name": "预付", "status": "启用"}, "cells": ["JSQ-01", "预付", "<span class=\"td-num\">1</span>", "结算周期统一值源·客商开票资料+物料供应商税率区共用（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'JSQ-02': { 'row': {"fields": {"category": "结算周期", "abbr": "JSQ-02", "name": "货到付款", "status": "启用"}, "cells": ["JSQ-02", "货到付款", "<span class=\"td-num\">2</span>", "结算周期统一值源·客商开票资料+物料供应商税率区共用（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'JSQ-03': { 'row': {"fields": {"category": "结算周期", "abbr": "JSQ-03", "name": "周结", "status": "启用"}, "cells": ["JSQ-03", "周结", "<span class=\"td-num\">3</span>", "结算周期统一值源·客商开票资料+物料供应商税率区共用（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'JSQ-04': { 'row': {"fields": {"category": "结算周期", "abbr": "JSQ-04", "name": "半月结", "status": "启用"}, "cells": ["JSQ-04", "半月结", "<span class=\"td-num\">4</span>", "结算周期统一值源·客商开票资料+物料供应商税率区共用（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'JSQ-05': { 'row': {"fields": {"category": "结算周期", "abbr": "JSQ-05", "name": "月结", "status": "启用"}, "cells": ["JSQ-05", "月结", "<span class=\"td-num\">5</span>", "结算周期统一值源·客商开票资料+物料供应商税率区共用（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'JSQ-06': { 'row': {"fields": {"category": "结算周期", "abbr": "JSQ-06", "name": "发票后 30 天", "status": "启用"}, "cells": ["JSQ-06", "发票后 30 天", "<span class=\"td-num\">6</span>", "结算周期统一值源·客商开票资料+物料供应商税率区共用（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'JSQ-07': { 'row': {"fields": {"category": "结算周期", "abbr": "JSQ-07", "name": "发票后 60 天", "status": "启用"}, "cells": ["JSQ-07", "发票后 60 天", "<span class=\"td-num\">7</span>", "结算周期统一值源·客商开票资料+物料供应商税率区共用（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'JSQ-08': { 'row': {"fields": {"category": "结算周期", "abbr": "JSQ-08", "name": "发票后 90 天", "status": "启用"}, "cells": ["JSQ-08", "发票后 90 天", "<span class=\"td-num\">8</span>", "结算周期统一值源·客商开票资料+物料供应商税率区共用（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'JSQ-09': { 'row': {"fields": {"category": "结算周期", "abbr": "JSQ-09", "name": "发票后 120 天", "status": "启用"}, "cells": ["JSQ-09", "发票后 120 天", "<span class=\"td-num\">9</span>", "结算周期统一值源·客商开票资料+物料供应商税率区共用（D-127）", "<span class=\"tag tag-green\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
  },

  /* --------------------------------------------------------------------------
 * 我的待办 todoItems：键 = 单据号（G12 · 我的待办 实体渲染；type/action 供筛选与统计卡计数）
 *   渲染器：页面自带 filterTodo()（类型下拉+多字段关键词）不变，初始化脚本用本实体重建 #todoBody 行
 * ------------------------------------------------------------------------ */
  todoItems: {
    'SO-20260910-0047': { 'row': {"fields": {"auditor": "沈婷", "type": "销售订单", "docNo": "SO-20260910-0047", "summary": "华骏重卡 · 驾驶室围板箱 160 套", "project": "PRJ-2601", "submitter": "沈婷", "time": "09-10 09:20", "action": "待审核"}}, 'link': '销售管理/销售订单审核.html?id=SO-20260910-0047' },
    'PO-20260910-019': { 'row': {"fields": {"auditor": "徐文", "type": "采购订单", "docNo": "PO-20260910-019", "summary": "甬城塑业包装 · 围板箱 120 只", "project": "PRJ-2601", "submitter": "林国栋", "time": "09-10 08:55", "action": "待审核"}}, 'link': '采购管理/采购订单审核.html?id=PO-20260910-019' },
    'LZ-20260909-012': { 'row': {"fields": {"auditor": "沈婷", "type": "租赁单", "docNo": "LZ-20260909-012", "summary": "华骏重卡 · 围板箱续租 200 只", "project": "PRJ-2601", "submitter": "沈婷", "time": "09-09 15:40", "action": "待审核"}}, 'link': '租赁管理/租赁单审核.html?id=LZ-20260909-012' },
    'CK-20260909-021': { 'row': {"fields": {"auditor": "陈锋", "type": "销售出库", "docNo": "CK-20260909-021", "summary": "租赁出库 · 驾驶室围板箱 160 套", "project": "PRJ-2601", "submitter": "陈锋", "time": "09-09 14:05", "action": "待审核"}}, 'link': '销售管理/销售出库审核.html?id=CK-20260909-021' },
    'TK-20260908-006': { 'row': {"fields": {"auditor": "沈婷", "type": "退租入库", "docNo": "TK-20260908-006", "summary": "华骏重卡 · 退租围板箱 86 只（含缺损 3 只）", "project": "PRJ-2601", "submitter": "严明", "time": "09-08 16:30", "action": "待审核"}}, 'link': '租赁管理/退租入库审核.html?id=TK-20260908-006' },
    'PD-20260907-003': { 'row': {"fields": {"auditor": "林国栋", "type": "盘点", "docNo": "PD-20260907-003", "summary": "华东中心仓 9 月初盘点（差异 5 只）", "project": "华东中心仓", "submitter": "林国栋", "time": "09-07 10:12", "action": "待审核"}}, 'link': '仓储作业/盘点审核.html?id=PD-20260907-003' },
    'RK-20260906-014': { 'row': {"fields": {"auditor": "严丽", "type": "采购入库", "docNo": "RK-20260906-014", "summary": "甬城塑业包装 · 围板箱到货 200 只", "project": "PRJ-2601", "submitter": "林国栋", "time": "09-06 09:45", "action": "待验收"}}, 'link': '采购管理/采购入库审核.html?id=RK-20260906-014' },
    'RZ-20260905-004': { 'row': {"fields": {"auditor": "江强", "type": "租入入库", "docNo": "RZ-20260905-004", "summary": "环通 · 围板箱租入 300 只", "project": "PRJ-2603", "submitter": "江强", "time": "09-05 11:20", "action": "待入库"}}, 'link': '租入管理/租入入库确认.html?id=RZ-20260905-004' },
    'GH-20260904-002': { 'row': {"fields": {"auditor": "江强", "type": "租入归还", "docNo": "GH-20260904-002", "summary": "环通 · 归还围板箱 100 只", "project": "PRJ-2603", "submitter": "江强", "time": "09-04 15:08", "action": "待审核"}}, 'link': '租入管理/租入归还审核.html?id=GH-20260904-002' },
    'QT-20260903-001': { 'row': {"fields": {"auditor": "徐文", "type": "其他入库", "docNo": "QT-20260903-001", "summary": "调拨余量回库 · 托盘 40 张", "project": "华东中心仓", "submitter": "邵磊", "time": "09-03 14:22", "action": "待审核"}}, 'link': '仓储作业/其他入库审核.html?id=QT-20260903-001' },
    'FK-20260902-005': { 'row': {"fields": {"auditor": "严丽", "type": "付款登记", "docNo": "FK-20260902-005", "summary": "甬城塑业包装 · 8 月应付结算", "project": "PRJ-2601", "submitter": "李婧", "time": "09-02 10:30", "action": "待确认"}}, 'link': '财务协同/付款确认.html?id=FK-20260902-005' },
    'SK-20260901-003': { 'row': {"fields": {"auditor": "严丽", "type": "收款确认", "docNo": "SK-20260901-003", "summary": "华骏重卡 · 8 月租金收款", "project": "PRJ-2601", "submitter": "李婧", "time": "09-01 09:15", "action": "待确认"}}, 'link': '财务协同/收款登记.html?audit=1' },
    'QTCK-20260904-003': { 'row': {"fields": {"auditor": "林国栋", "type": "其他出库", "docNo": "QTCK-20260904-003", "summary": "华东中心仓 · 报废隔板 12 块", "project": "华东中心仓", "submitter": "邵磊", "time": "09-04 10:05", "action": "待审核"}}, 'link': '仓储作业/其他出库审核.html?id=QTCK-20260904-003' },
    'DB-20260906-008': { 'row': {"fields": {"auditor": "林国栋", "type": "库存调拨", "docNo": "DB-20260906-008", "summary": "华东中心仓→华南中心仓 · 围板箱 50 只", "project": "华东中心仓", "submitter": "邵磊", "time": "09-06 11:40", "action": "待审核"}}, 'link': '仓储作业/调拨审核.html?id=DB-20260906-008' },
    'RZD-20260909-010': { 'row': {"fields": {"auditor": "江强", "type": "租入单", "docNo": "RZD-20260909-010", "summary": "环通 · 大箱租入 40 只（月租）", "project": "PRJ-2603", "submitter": "江强", "time": "09-09 09:50", "action": "待审核"}}, 'link': '租入管理/租入单审核.html?id=RZD-20260909-010' },
    'CK-20260910-022': { 'row': {"fields": {"auditor": "林国栋", "type": "租赁出库", "docNo": "CK-20260910-022", "summary": "东海商用宁波 · 围板箱套件 30 套", "project": "PRJ-2603", "submitter": "邵磊", "time": "09-10 15:20", "action": "待审核"}}, 'link': '租赁管理/租赁出库确认.html?id=CK-20260910-022' },
    'XSTH-20260911-003': { 'row': {"fields": {"auditor": "沈婷", "type": "销售退货单", "docNo": "XSTH-20260911-003", "summary": "东海商用宁波 · 内衬退货 300 件（拒收）", "project": "PRJ-2602", "submitter": "沈婷", "time": "09-11 14:30", "action": "待审核"}}, 'link': '销售管理/销售退货审核.html?id=XSTH-20260911-003' },
    'ZY-20260915-005': { 'row': {"fields": {"auditor": "赵磊", "type": "转移出库", "docNo": "ZY-20260915-005", "summary": "安吉智行 · 围板箱转移博世苏州 200 只", "project": "PRJ-2605", "submitter": "沈婷", "time": "09-15 09:20", "action": "待审核"}}, 'link': '租赁管理/转移出库审核.html?id=ZY-20260915-005' },
  },

  /* --------------------------------------------------------------------------
 * 项目档案 projects：键 = 项目编码（G12 · 项目管理/项目档案 列表驱动；项目详情/项目看板/损益报表同键互溯）
 *   fields: name/customer/supplier/status/start/end/owner 供筛选（名称/客户/状态/立项时间区间/负责人）
 * ------------------------------------------------------------------------ */
  projects: {
    'PRJ-2601': { 'row': {"fields": {"name": "华骏重卡·长春基地 驾驶室围板箱租赁", "customer": "华骏重卡汽车有限公司", "suppliers": "环通包装运营（上海） · 甬城塑业", "settle": "按租出结算", "status": "进行中", "start": "2026-01-01", "end": "2027-12-31", "owner": "江强"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2601</span>", "cells": ["华骏重卡·长春基地 驾驶室围板箱租赁", "华骏重卡汽车有限公司", "<span class='tag tag-blue'>环通（租入）</span> <span class='tag tag-purple' style='background:#f9f0ff;border-color:#d3adf7;color:#722ed1;margin-left:2px'>甬城塑业（采购）</span>", "按租出结算", "<span class=\"tag tag-blue\">进行中</span>", "2026-01-01 ~ 2027-12-31", "江强"], "ops": [{"t": "详情", "act": "go('../项目管理/项目详情.html')"}, {"t": "上下游绑定", "act": "go('../项目管理/上下游绑定.html')"}]} },
    'PRJ-2602': { 'row': {"fields": {"name": "华骏重卡·青岛基地 保险杠料架租赁", "customer": "华骏重卡汽车有限公司（青岛）", "suppliers": "环通包装运营（上海） · 延陵托盘", "settle": "按租出结算", "status": "进行中", "start": "2026-03-15", "end": "2027-06-30", "owner": "陈锋"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2602</span>", "cells": ["华骏重卡·青岛基地 保险杠料架租赁", "华骏重卡汽车有限公司（青岛）", "<span class='tag tag-blue'>环通（租入）</span> <span class='tag tag-purple' style='background:#f9f0ff;border-color:#d3adf7;color:#722ed1;margin-left:2px'>延陵（采购）</span>", "按租出结算", "<span class=\"tag tag-blue\">进行中</span>", "2026-03-15 ~ 2027-06-30", "陈锋"], "ops": [{"t": "详情", "act": "go('../项目管理/项目详情.html')"}, {"t": "上下游绑定", "act": "go('../项目管理/上下游绑定.html')"}]} },
    'PRJ-2603': { 'row': {"fields": {"name": "长丰锂电·电池包周转箱租赁", "customer": "长丰锂电科技", "suppliers": "环通包装运营（上海）", "settle": "按终端结算", "status": "进行中", "start": "2026-05-01", "end": "2027-04-30", "owner": "江强"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2603</span>", "cells": ["长丰锂电·电池包周转箱租赁", "长丰锂电科技", "<span class='tag tag-blue'>环通（租入）</span>", "按终端结算", "<span class=\"tag tag-blue\">进行中</span>", "2026-05-01 ~ 2027-04-30", "江强"], "ops": [{"t": "详情", "act": "go('../项目管理/项目详情.html')"}, {"t": "上下游绑定", "act": "go('../项目管理/上下游绑定.html')"}]} },
    'PRJ-2604': { 'row': {"fields": {"name": "南方汽造·座椅周转箱租赁（试点）", "customer": "南方汽造", "suppliers": "甬城塑业包装制品", "settle": "按租出结算", "status": "已暂停", "start": "2026-06-10", "end": "2026-12-31", "owner": "陈锋"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2604</span>", "cells": ["南方汽造·座椅周转箱租赁（试点）", "南方汽造", "<span class='tag tag-blue'>甬城塑业（采购）</span>", "按租出结算", "<span class=\"tag tag-orange\">已暂停</span>", "2026-06-10 ~ 2026-12-31", "陈锋"], "ops": [{"t": "详情", "act": "go('../项目管理/项目详情.html')"}, {"t": "上下游绑定", "act": "go('../项目管理/上下游绑定.html')"}]} },
    'PRJ-2605': { 'row': {"fields": {"name": "华骏重卡·蔚山基地 围板箱租赁扩建", "customer": "华骏重卡汽车有限公司", "suppliers": "环通包装运营（上海）", "settle": "按租出结算", "status": "筹备中", "start": "2026-10-01", "end": "2028-03-31", "owner": "江强"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2605</span>", "cells": ["华骏重卡·蔚山基地 围板箱租赁扩建", "华骏重卡汽车有限公司", "<span class='tag tag-blue'>环通（租入）</span>", "按租出结算", "<span class=\"tag tag-gray\">筹备中</span>", "2026-10-01 ~ 2028-03-31", "江强"], "ops": [{"t": "详情", "act": "go('../项目管理/项目详情.html')"}, {"t": "上下游绑定", "act": "go('../项目管理/上下游绑定.html')"}]} },
    'PRJ-2606': { 'row': {"fields": {"name": "长丰锂电·二期 电池包周转箱扩容", "customer": "长丰锂电科技", "suppliers": "环通包装运营（上海） · 吴越联合", "settle": "按租出结算", "status": "筹备中", "start": "2026-11-01", "end": "2028-06-30", "owner": "沈婷"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2606</span>", "cells": ["长丰锂电·二期 电池包周转箱扩容", "长丰锂电科技", "<span class='tag tag-blue'>环通（租入）</span> <span class='tag tag-purple' style='background:#f9f0ff;border-color:#d3adf7;color:#722ed1;margin-left:2px'>吴越（采购）</span>", "按租出结算", "<span class=\"tag tag-gray\">筹备中</span>", "2026-11-01 ~ 2028-06-30", "沈婷"], "ops": [{"t": "详情", "act": "go('../项目管理/项目详情.html')"}, {"t": "上下游绑定", "act": "go('../项目管理/上下游绑定.html')"}]} },
    'PRJ-2599': { 'row': {"fields": {"name": "东海商用·南京工厂 托盘租赁（已完结）", "customer": "东海商用", "suppliers": "甬城塑业包装制品", "settle": "按租出结算", "status": "已完结", "start": "2025-06-01", "end": "2026-05-31", "owner": "陈锋"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2599</span>", "cells": ["东海商用·南京工厂 托盘租赁（已完结）", "东海商用", "<span class='tag tag-blue'>甬城塑业（采购）</span>", "按租出结算", "<span class=\"tag tag-green\">已完结</span>", "2025-06-01 ~ 2026-05-31", "陈锋"], "ops": [{"t": "详情", "act": "go('../项目管理/项目详情.html')"}, {"t": "上下游绑定", "act": "go('../项目管理/上下游绑定.html')"}]} },
    'PRJ-2598': { 'row': {"fields": {"name": "星河汽车·西安基地 料箱租赁（已完结）", "customer": "星河汽车", "suppliers": "甬城塑业包装制品", "settle": "按租出结算", "status": "已完结", "start": "2025-03-01", "end": "2026-02-28", "owner": "林国栋"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2598</span>", "cells": ["星河汽车·西安基地 料箱租赁（已完结）", "星河汽车", "<span class='tag tag-blue'>甬城塑业（采购）</span>", "按租出结算", "<span class=\"tag tag-green\">已完结</span>", "2025-03-01 ~ 2026-02-28", "林国栋"], "ops": [{"t": "详情", "act": "go('../项目管理/项目详情.html')"}, {"t": "上下游绑定", "act": "go('../项目管理/上下游绑定.html')"}]} },
  },

  /* --------------------------------------------------------------------------
 * 项目详情·单据查询 projectDocs：键 = 单据号（G12 · 项目管理/项目详情 主表驱动；单据号与各模块列表页实体同键互溯）
 *   fields: type/summary/qty/status/date/ref；stab=单据类型（全部单据/租赁出库单/退租入库单/采购入库单/销售订单/应收账单）
 * ------------------------------------------------------------------------ */
  projectDocs: {
    'CK-20260828-012': { 'row': {"fields": {"type": "租赁出库单", "summary": "ZH-2601-A 驾驶室围板箱整箱套件", "qty": "180 套", "status": "已出库", "date": "2026-08-28", "ref": "SO-20260827-0036"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../租赁管理/租赁出库列表.html')\">CK-20260828-012</span>", "cells": ["ZH-2601-A 驾驶室围板箱整箱套件", "<span class=\"td-num\">180 套</span>", "<span class=\"tag tag-green\">已出库</span>", "2026-08-28", "SO-20260827-0036"], "ops": [{"t": "查看单据", "act": "go('../租赁管理/租赁出库列表.html')"}]} },
    'CK-20260822-010': { 'row': {"fields": {"type": "租赁出库单", "summary": "ZH-2601-A 驾驶室围板箱整箱套件", "qty": "120 套", "status": "已出库", "date": "2026-08-22", "ref": "SO-20260820-0033"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../租赁管理/租赁出库列表.html')\">CK-20260822-010</span>", "cells": ["ZH-2601-A 驾驶室围板箱整箱套件", "<span class=\"td-num\">120 套</span>", "<span class=\"tag tag-green\">已出库</span>", "2026-08-22", "SO-20260820-0033"], "ops": [{"t": "查看单据", "act": "go('../租赁管理/租赁出库列表.html')"}]} },
    'CK-20260815-008': { 'row': {"fields": {"type": "租赁出库单", "summary": "ZH-2602-B 保险杠料架套件", "qty": "90 套", "status": "已出库", "date": "2026-08-15", "ref": "SO-20260813-0031"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../租赁管理/租赁出库列表.html')\">CK-20260815-008</span>", "cells": ["ZH-2602-B 保险杠料架套件", "<span class=\"td-num\">90 套</span>", "<span class=\"tag tag-green\">已出库</span>", "2026-08-15", "SO-20260813-0031"], "ops": [{"t": "查看单据", "act": "go('../租赁管理/租赁出库列表.html')"}]} },
    'TK-20260830-005': { 'row': {"fields": {"type": "退租入库单", "summary": "华骏重卡 · 退租围板箱 86 只（缺损 3 只）", "qty": "86 只", "status": "已入库", "date": "2026-08-30", "ref": "CK-20260828-012"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../租赁管理/退租入库列表.html')\">TK-20260830-005</span>", "cells": ["华骏重卡 · 退租围板箱 86 只（缺损 3 只）", "<span class=\"td-num\">86 只</span>", "<span class=\"tag tag-green\">已入库</span>", "2026-08-30", "CK-20260828-012"], "ops": [{"t": "查看单据", "act": "go('../租赁管理/退租入库列表.html')"}]} },
    'TK-20260818-003': { 'row': {"fields": {"type": "退租入库单", "summary": "华骏重卡 · 退租保险杠料架 54 套", "qty": "54 套", "status": "已入库", "date": "2026-08-18", "ref": "CK-20260815-008"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../租赁管理/退租入库列表.html')\">TK-20260818-003</span>", "cells": ["华骏重卡 · 退租保险杠料架 54 套", "<span class=\"td-num\">54 套</span>", "<span class=\"tag tag-green\">已入库</span>", "2026-08-18", "CK-20260815-008"], "ops": [{"t": "查看单据", "act": "go('../租赁管理/退租入库列表.html')"}]} },
    'RK-20260826-016': { 'row': {"fields": {"type": "采购入库单", "summary": "甬城塑业包装 · 围板箱到货", "qty": "200 只", "status": "已入库", "date": "2026-08-26", "ref": "PO-20260824-016"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../采购管理/采购入库列表.html')\">RK-20260826-016</span>", "cells": ["甬城塑业包装 · 围板箱到货", "<span class=\"td-num\">200 只</span>", "<span class=\"tag tag-green\">已入库</span>", "2026-08-26", "PO-20260824-016"], "ops": [{"t": "查看单据", "act": "go('../采购管理/采购入库列表.html')"}]} },
    'RK-20260812-011': { 'row': {"fields": {"type": "采购入库单", "summary": "甬城塑业包装 · 锁扣到货", "qty": "800 套", "status": "已入库", "date": "2026-08-12", "ref": "PO-20260810-013"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../采购管理/采购入库列表.html')\">RK-20260812-011</span>", "cells": ["甬城塑业包装 · 锁扣到货", "<span class=\"td-num\">800 套</span>", "<span class=\"tag tag-green\">已入库</span>", "2026-08-12", "PO-20260810-013"], "ops": [{"t": "查看单据", "act": "go('../采购管理/采购入库列表.html')"}]} },
    'SO-20260827-0036': { 'row': {"fields": {"type": "销售订单", "summary": "华骏重卡 · 驾驶室围板箱", "qty": "180 套", "status": "已审核", "date": "2026-08-27", "ref": "—"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../销售管理/销售订单列表.html')\">SO-20260827-0036</span>", "cells": ["华骏重卡 · 驾驶室围板箱", "<span class=\"td-num\">180 套</span>", "<span class=\"tag tag-blue\">已审核</span>", "2026-08-27", "—"], "ops": [{"t": "查看单据", "act": "go('../销售管理/销售订单列表.html')"}]} },
    'SO-20260820-0033': { 'row': {"fields": {"type": "销售订单", "summary": "华骏重卡 · 围板箱", "qty": "120 套", "status": "已审核", "date": "2026-08-20", "ref": "—"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../销售管理/销售订单列表.html')\">SO-20260820-0033</span>", "cells": ["华骏重卡 · 围板箱", "<span class=\"td-num\">120 套</span>", "<span class=\"tag tag-blue\">已审核</span>", "2026-08-20", "—"], "ops": [{"t": "查看单据", "act": "go('../销售管理/销售订单列表.html')"}]} },
    'AR-2026-08-PRJ2601': { 'row': {"fields": {"type": "应收账单", "summary": "PRJ-2601 · 8 月租金（按租赁出库汇总 486,200 元）", "qty": "—", "status": "部分收款", "date": "2026-08-31", "ref": "SO-20260827-0036"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../财务协同/应收账单.html')\">AR-2026-08-PRJ2601</span>", "cells": ["PRJ-2601 · 8 月租金（按租赁出库汇总 486,200 元）", "<span class=\"td-num\">—</span>", "<span class=\"tag tag-orange\">部分收款</span>", "2026-08-31", "SO-20260827-0036"], "ops": [{"t": "查看单据", "act": "go('../财务协同/应收账单.html')"}]} },
    'AR-2026-07-PRJ2601': { 'row': {"fields": {"type": "应收账单", "summary": "PRJ-2601 · 7 月租金（按租赁出库汇总 442,800 元 · 已结清）", "qty": "—", "status": "已结清", "date": "2026-07-31", "ref": "SO-20260820-0033"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../财务协同/应收账单.html')\">AR-2026-07-PRJ2601</span>", "cells": ["PRJ-2601 · 7 月租金（按租赁出库汇总 442,800 元 · 已结清）", "<span class=\"td-num\">—</span>", "<span class=\"tag tag-green\">已结清</span>", "2026-07-31", "SO-20260820-0033"], "ops": [{"t": "查看单据", "act": "go('../财务协同/应收账单.html')"}]} },
  },

  /* --------------------------------------------------------------------------
 * 项目看板·项目经营总览 boardRows：键 = 项目编码（G12 · 首页/项目看板 主表驱动；统计卡静态保留·混合页）
 *   fields: name/customer/status；列=出库/退租/在租/营收/累计毛利（演示口径）
 * ------------------------------------------------------------------------ */
  boardRows: {
    'PRJ-2601': { 'row': {"fields": {"name": "华骏重卡·长春基地 驾驶室围板箱租赁", "customer": "华骏重卡汽车有限公司", "status": "进行中"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2601</span>", "cells": ["华骏重卡·长春基地 驾驶室围板箱租赁", "华骏重卡汽车有限公司", "<span class=\"tag tag-blue\">进行中</span>", "<span class=\"td-num\">1,240</span>", "<span class=\"td-num\">986</span>", "<span class=\"td-num\">3,860</span>", "<span class=\"td-num\">486,200</span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('../财务协同/应收账单.html')\">AR-2026-08-PRJ2601</span></div>", "<span class=\"td-num\">212,400</span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('../财务协同/应付账单.html')\">AP-20260901-008</span></div>"], "ops": [{"t": "查看明细", "act": "go('../项目管理/项目详情.html')"}]} },
    'PRJ-2602': { 'row': {"fields": {"name": "华骏重卡·青岛基地 保险杠料架租赁", "customer": "华骏重卡汽车有限公司（青岛）", "status": "进行中"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2602</span>", "cells": ["华骏重卡·青岛基地 保险杠料架租赁", "华骏重卡汽车有限公司（青岛）", "<span class=\"tag tag-blue\">进行中</span>", "<span class=\"td-num\">620</span>", "<span class=\"td-num\">410</span>", "<span class=\"td-num\">1,530</span>", "<span class=\"td-num\">268,400</span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('../财务协同/应收账单.html')\">AR-2026-08-PRJ2602</span></div>", "<span class=\"td-num\">96,200</span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('../财务协同/应付账单.html')\">AP-20260830-007</span></div>"], "ops": [{"t": "查看明细", "act": "go('../项目管理/项目详情.html')"}]} },
    'PRJ-2603': { 'row': {"fields": {"name": "长丰锂电·电池包周转箱租赁", "customer": "长丰锂电科技", "status": "进行中"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2603</span>", "cells": ["长丰锂电·电池包周转箱租赁", "长丰锂电科技", "<span class=\"tag tag-blue\">进行中</span>", "<span class=\"td-num\">540</span>", "<span class=\"td-num\">286</span>", "<span class=\"td-num\">1,240</span>", "<span class=\"td-num\">186,300</span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('../财务协同/应收账单.html')\">AR-2026-08-PRJ2603</span></div>", "<span class=\"td-num\">58,900</span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('../财务协同/应付账单.html')\">AP-20260903-009</span></div>"], "ops": [{"t": "查看明细", "act": "go('../项目管理/项目详情.html')"}]} },
    'PRJ-2604': { 'row': {"fields": {"name": "南方汽造·座椅周转箱试点", "customer": "南方汽造", "status": "已暂停"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2604</span>", "cells": ["南方汽造·座椅周转箱试点", "南方汽造", "<span class=\"tag tag-orange\">已暂停</span>", "<span class=\"td-num\">86</span>", "<span class=\"td-num\">132</span>", "<span class=\"td-num\">96</span>", "<span class=\"td-num\">24,600</span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('../财务协同/应收账单.html')\">AR-2026-09-PRJ2604-S1</span></div>", "<span class=\"td-num\">-18,600</span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('../财务协同/应付账单.html')\">AP-20260903-010</span></div>"], "ops": [{"t": "查看明细", "act": "go('../项目管理/项目详情.html')"}]} },
    'PRJ-2605': { 'row': {"fields": {"name": "华骏重卡·蔚山基地 围板箱扩建", "customer": "华骏重卡汽车有限公司", "status": "筹备中"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2605</span>", "cells": ["华骏重卡·蔚山基地 围板箱扩建", "华骏重卡汽车有限公司", "<span class=\"tag tag-gray\">筹备中</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">0</span>"], "ops": [{"t": "查看明细", "act": "go('../项目管理/项目详情.html')"}]} },
    'PRJ-2599': { 'row': {"fields": {"name": "东海商用·南京工厂 托盘租赁（完结）", "customer": "东海商用", "status": "已完结"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2599</span>", "cells": ["东海商用·南京工厂 托盘租赁（完结）", "东海商用", "<span class=\"tag tag-green\">已完结</span>", "<span class=\"td-num\">320</span>", "<span class=\"td-num\">358</span>", "<span class=\"td-num\">0</span>", "<span class=\"td-num\">126,800</span>", "<span class=\"td-num\">41,300</span>"], "ops": [{"t": "查看明细", "act": "go('../项目管理/项目详情.html')"}]} },
  },

  /* --------------------------------------------------------------------------
 * 损益报表·按项目汇总 profitRows：键 = 项目编码（G12 · 财务协同/损益报表 主表驱动；统计卡静态保留·混合页；按月/按客户页签为视觉演示）
 *   fields: name/period 供筛选（账期/所属项目）；金额千分位两位小数口径与账单实体一致
 * ------------------------------------------------------------------------ */
  profitRows: {
    'PRJ-2601': { 'row': {"fields": {"code": "PRJ-2601", "name": "华骏重卡·长春基地 驾驶室围板箱租赁", "period": "2026-09"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2601</span>", "cells": ["华骏重卡·长春基地 驾驶室围板箱租赁", "<span class=\"td-num\">420,000.00</span>", "<span class=\"td-num\">48,000.00</span>", "<span class=\"td-num\">18,200.00</span>", "<span class=\"td-num\"><b>486,200.00</b></span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('应收账单.html')\">AR-2026-08-PRJ2601</span></div>", "<span class=\"td-num\">186,300.00</span>", "<span class=\"td-num\">75,600.00</span>", "<span class=\"td-num\"><b>261,900.00</b></span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('应付账单.html')\">AP-20260901-008</span></div>", "<span class=\"td-num\"><b>224,300.00</b></span>", "<span class=\"rate-bar\"><i style=\"width:46.1%;\"></i></span>46.1%"], "ops": []} },
    'PRJ-2602': { 'row': {"fields": {"code": "PRJ-2602", "name": "华骏重卡·青岛基地 保险杠料架租赁", "period": "2026-09"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2602</span>", "cells": ["华骏重卡·青岛基地 保险杠料架租赁", "<span class=\"td-num\">168,000.00</span>", "<span class=\"td-num\">12,000.00</span>", "<span class=\"td-num\">6,400.00</span>", "<span class=\"td-num\"><b>186,400.00</b></span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('应收账单.html')\">AR-2026-08-PRJ2602</span></div>", "<span class=\"td-num\">72,100.00</span>", "<span class=\"td-num\">31,800.00</span>", "<span class=\"td-num\"><b>103,900.00</b></span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('应付账单.html')\">AP-20260830-007</span></div>", "<span class=\"td-num\"><b>82,500.00</b></span>", "<span class=\"rate-bar\"><i style=\"width:44.3%;\"></i></span>44.3%"], "ops": []} },
    'PRJ-2603': { 'row': {"fields": {"code": "PRJ-2603", "name": "长丰锂电·电池包周转箱租赁", "period": "2026-09"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2603</span>", "cells": ["长丰锂电·电池包周转箱租赁", "<span class=\"td-num\">132,000.00</span>", "<span class=\"td-num\">18,000.00</span>", "<span class=\"td-num\">9,800.00</span>", "<span class=\"td-num\"><b>159,800.00</b></span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('应收账单.html')\">AR-2026-09-PRJ2603-U1</span></div>", "<span class=\"td-num\">68,400.00</span>", "<span class=\"td-num\">26,200.00</span>", "<span class=\"td-num\"><b>94,600.00</b></span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('应付账单.html')\">AP-20260903-009</span></div>", "<span class=\"td-num\"><b>65,200.00</b></span>", "<span class=\"rate-bar\"><i style=\"width:40.8%;\"></i></span>40.8%"], "ops": []} },
    'PRJ-2604': { 'row': {"fields": {"code": "PRJ-2604", "name": "南方汽造·座椅周转箱试点", "period": "2026-08"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2604</span>", "cells": ["南方汽造·座椅周转箱试点", "<span class=\"td-num\">24,600.00</span>", "<span class=\"td-num\">10,000.00</span>", "<span class=\"td-num\">2,400.00</span>", "<span class=\"td-num\"><b>37,000.00</b></span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('应收账单.html')\">AR-2026-09-PRJ2604-S1</span></div>", "<span class=\"td-num\">31,200.00</span>", "<span class=\"td-num\">24,400.00</span>", "<span class=\"td-num\"><b>55,600.00</b></span><div style=\"font-size:11px;color:#8c8c8c;margin-top:2px;white-space:nowrap;\"><span class=\"lk\" onclick=\"go('应付账单.html')\">AP-20260903-010</span></div>", "<span class=\"td-num\"><b>-18,600.00</b></span>", "<span class=\"rate-bar\"><i style=\"width:0%;\"></i></span>-50.3%"], "ops": []} },
    'PRJ-2605': { 'row': {"fields": {"code": "PRJ-2605", "name": "华骏重卡·蔚山基地 围板箱扩建", "period": "2026-09"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2605</span>", "cells": ["华骏重卡·蔚山基地 围板箱扩建", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\"><b>0.00</b></span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\">0.00</span>", "<span class=\"td-num\"><b>0.00</b></span>", "<span class=\"td-num\"><b>0.00</b></span>", "<span class=\"rate-bar\"><i style=\"width:0%;\"></i></span>0.0%"], "ops": []} },
    'PRJ-2599': { 'row': {"fields": {"code": "PRJ-2599", "name": "东海商用·南京工厂 托盘租赁（完结）", "period": "2026-08"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../项目管理/项目详情.html')\">PRJ-2599</span>", "cells": ["东海商用·南京工厂 托盘租赁（完结）", "<span class=\"td-num\">86,000.00</span>", "<span class=\"td-num\">6,000.00</span>", "<span class=\"td-num\">3,200.00</span>", "<span class=\"td-num\"><b>95,200.00</b></span>", "<span class=\"td-num\">38,400.00</span>", "<span class=\"td-num\">14,100.00</span>", "<span class=\"td-num\"><b>52,500.00</b></span>", "<span class=\"td-num\"><b>42,700.00</b></span>", "<span class=\"rate-bar\"><i style=\"width:44.9%;\"></i></span>44.9%"], "ops": []} },
  },

  /* --------------------------------------------------------------------------
 * BOM 列表 bomList：键 = BOM物料编码（G12 · 基础数据/BOM 列表驱动；版本明细复用 bomVersions 实体——BOM维护页已驱动）
 *   fields: name/ver/status/mix/updater/update 供筛选（BOM物料编码/名称/版本/状态/更新时间区间）
 * ------------------------------------------------------------------------ */
  bomList: {
    'ZH-2601-A': { 'row': {"fields": {"name": "驾驶室围板箱整箱套件", "ver": "V2.1", "billing": "按时间周期", "status": "启用", "mix": "围板箱×1（租入）+ 围板×4（自购）+ 箱盖×1（自购）+ 锁扣×4（自购）+ 铰链×2（自购）", "updater": "陈锋", "update": "2026-08-20"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../基础数据/BOM维护.html')\">ZH-2601-A</span>", "cells": ["驾驶室围板箱整箱套件", "<span class=\"tag tag-green\">启用</span>", "<span class=\"td-num\">5</span>", "围板箱×1（租入）+ 围板×4（自购）+ 箱盖×1（自购）+ 锁扣×4（自购）+ 铰链×2（自购）", "陈锋", "2026-08-20"], "ops": [{"t": "编辑", "act": "go('../基础数据/BOM维护.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZH-2602-B': { 'row': {"fields": {"name": "保险杠料架套件", "ver": "V1.3", "billing": "按时间周期", "status": "启用", "mix": "料架×1（租入）+ 支撑臂×2（自购）+ 锁扣×2（自购）", "updater": "陈锋", "update": "2026-07-14"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../基础数据/BOM维护.html')\">ZH-2602-B</span>", "cells": ["保险杠料架套件", "<span class=\"tag tag-green\">启用</span>", "<span class=\"td-num\">4</span>", "料架×1（租入）+ 支撑臂×2（自购）+ 锁扣×2（自购）", "陈锋", "2026-07-14"], "ops": [{"t": "编辑", "act": "go('../基础数据/BOM维护.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZH-2603-C': { 'row': {"fields": {"name": "电池包周转箱套件", "ver": "V1.0", "billing": "按次", "status": "启用", "mix": "周转箱×1（租入）+ 内衬×4（自购）+ 绑带×2（自购）+ 锁扣×4（自购）+ 铰链×2（自购）+ 标签×1（自购）", "updater": "沈婷", "update": "2026-06-30"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../基础数据/BOM维护.html')\">ZH-2603-C</span>", "cells": ["电池包周转箱套件", "<span class=\"tag tag-green\">启用</span>", "<span class=\"td-num\">6</span>", "周转箱×1（租入）+ 内衬×4（自购）+ 绑带×2（自购）+ 锁扣×4（自购）+ 铰链×2（自购）+ 标签×1（自购）", "沈婷", "2026-06-30"], "ops": [{"t": "编辑", "act": "go('../基础数据/BOM维护.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'ZT-2201': { 'row': {"fields": {"name": "座椅周转箱套件", "ver": "V1.0", "billing": "按次", "status": "启用", "mix": "周转箱×1（租入）+ 隔板×2（自购）", "updater": "陈锋", "update": "2026-05-18"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../基础数据/BOM维护.html')\">ZT-2201</span>", "cells": ["座椅周转箱套件", "<span class=\"tag tag-green\">启用</span>", "<span class=\"td-num\">3</span>", "周转箱×1（租入）+ 隔板×2（自购）", "陈锋", "2026-05-18"], "ops": [{"t": "编辑", "act": "go('../基础数据/BOM维护.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'JP-3105': { 'row': {"fields": {"name": "仪表板周转架套件", "ver": "V1.3", "billing": "按时间周期", "status": "启用", "mix": "周转架×1（自购）+ 支撑×2（自购）+ 锁扣×1（自购）", "updater": "陈锋", "update": "2026-04-22"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../基础数据/BOM维护.html')\">JP-3105</span>", "cells": ["仪表板周转架套件", "<span class=\"tag tag-green\">启用</span>", "<span class=\"td-num\">4</span>", "周转架×1（自购）+ 支撑×2（自购）+ 锁扣×1（自购）", "陈锋", "2026-04-22"], "ops": [{"t": "编辑", "act": "go('../基础数据/BOM维护.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'WBX-1210L': { 'row': {"fields": {"name": "围板箱 1200×1000×970（单件）", "ver": "V1.0", "billing": "按时间周期", "status": "停用", "mix": "—（单件器具，无子项组合）", "updater": "陈锋", "update": "2026-03-02"}, "keyHtml": "<span class=\"lk\" onclick=\"go('../基础数据/BOM维护.html')\">WBX-1210L</span>", "cells": ["围板箱 1200×1000×970（单件）", "<span class=\"tag tag-gray\">停用</span>", "<span class=\"td-num\">0</span>", "—（单件器具，无子项组合）", "陈锋", "2026-03-02"], "ops": [{"t": "编辑", "act": "go('../基础数据/BOM维护.html')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },  },
  productTaxes: {
    'TAX-001': {'row': {"fields": {"product": "WBX-1210L", "productName": "围板箱 1200×1000×970", "cls": "围板箱", "supplier": "甬城塑业包装制品有限公司", "taxRate": "13%", "settleCycle": "月结"}}},
    'TAX-002': {'row': {"fields": {"product": "WBX-1210L", "productName": "围板箱 1200×1000×970", "cls": "围板箱", "supplier": "环通循环包装运营（上海）有限公司", "taxRate": "13%", "settleCycle": "月结"}}},
    'TAX-003': {'row': {"fields": {"product": "BTC-6040", "productName": "料箱 600×400×340", "cls": "料箱", "supplier": "环通循环包装运营（上海）有限公司", "taxRate": "13%", "settleCycle": "月结"}}},
    'TAX-004': {'row': {"fields": {"product": "LJ-A100", "productName": "锁扣组件", "cls": "组件", "supplier": "吴越联合五金制品有限公司", "taxRate": "13%", "settleCycle": "发票后 60 天"}}},
    'TAX-005': {'row': {"fields": {"product": "LJ-F600", "productName": "内衬", "cls": "组件", "supplier": "甬城塑业包装制品有限公司", "taxRate": "13%", "settleCycle": "发票后 60 天"}}},
  },

  /* --------------------------------------------------------------------------
 * 采购退货单 purchaseReturns：键 = 退货单号（G33 · 退货退款闭环方案 B·陆鸣 09-15 拍板）
 *   fields: type(退货类型 THC)/ref(关联采购入库单)/supplier/material/qty/amount/status/date 供筛选与 stab
 *   状态流 待审核→已审核→已退款；收货拒收=未入库直接退（不产生库存流水）/入库后退货=已入库再退（D-109 不改原入库单）
 * ------------------------------------------------------------------------ */
  purchaseReturns: {
    'CGTH-20260914-001': {
      'row': {"fields": {"type": "入库后退货", "ref": "CGRK-20260828-012", "supplier": "吴越联合五金制品有限公司", "material": "锁扣组件 不锈钢 304", "qty": "1,000 件", "amount": "4,800.00", "status": "已审核", "payStatus": "未付款", "date": "2026-09-14"}, "cells": ["入库后退货", "<span class=\"lk\">CGRK-20260828-012</span>", "吴越联合五金制品有限公司", "锁扣组件 不锈钢 304", "<span class=\"td-num\">1,000 件</span>", "<span class=\"td-num\">4,800.00</span>", "<span class=\"tag tag-blue\">已审核</span>", "2026-09-14"], "ops": [{"t": "详情", "act": "go('../采购管理/采购退货详情.html?id=CGTH-20260914-001')"}]},
      title: '采购退货单详情',
      formTitle: '退货信息',
      formRows: [
        { label: '退货单号', text: 'CGTH-20260914-001' },
        { label: '状态', tag: '已审核' },
        { label: '退货类型', text: '入库后退货（已入库再退）' },
        { label: '供应商', text: '吴越联合五金制品有限公司' },
        { label: '关联采购入库', text: 'CGRK-20260828-012', url: '采购管理/采购入库列表.html' },
        { label: '退货日期', text: '2026-09-14' },
        { label: '退货原因', text: '规格不符（尺寸下差），供应商确认后退货', full: true },
        { label: '备注', text: '—' },
        { label: '货款支付状态', text: '未付款 · 退货冲减在途应付（不立退款单）', full: true },
        { label: '制单人', text: '林国栋' }
      ],
      itemTitle: '退货明细',
      itemCols: ['序号', '物料编码', '物料名称', '规格', '单位', '可退上限', '退货数量', '备注'],
      items: [
        ['1', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '1,000', '1,000', '—']
      ],
      chain: [
        { role: '采购入库单', name: 'CGRK-20260828-012', url: '采购管理/采购入库列表.html' },
        { role: '采购退货单（本单）', name: 'CGTH-20260914-001', self: true },
        { role: '应付账单', name: '货款未付 · 按净额挂账（验收后）', url: '财务协同/应付账单.html' }
      ],
      timeline: [
        { t: '09-14 09:30', text: '采购退货登记 · 提交审核', who: '林国栋' },
        { t: '09-14 14:20', text: '审核通过 · 冲减库存与在途应付（货款未付，不立退款单）', who: '徐文' }
      ]
    },
    'CGTH-20260912-002': {
      'row': {"fields": {"type": "收货拒收", "ref": "CGRK-20260827-009", "supplier": "吴越联合五金制品有限公司", "material": "锁扣组件", "qty": "500 套", "amount": "2,000.00", "status": "已审核", "payStatus": "未付款", "date": "2026-09-12"}, "cells": ["收货拒收", "<span class=\"lk\">CGRK-20260827-009</span>", "吴越联合五金制品有限公司", "锁扣组件", "<span class=\"td-num\">500 套</span>", "<span class=\"td-num\">2,000.00</span>", "<span class=\"tag tag-blue\">已审核</span>", "2026-09-12"], "ops": [{"t": "详情", "act": "go('../采购管理/采购退货详情.html?id=CGTH-20260912-002')"}]},
      title: '采购退货单详情',
      formTitle: '退货信息',
      formRows: [
        { label: '退货单号', text: 'CGTH-20260912-002' },
        { label: '状态', tag: '已审核' },
        { label: '退货类型', text: '收货拒收（未入库直接退·不产生库存流水）', full: true },
        { label: '供应商', text: '吴越联合五金制品有限公司' },
        { label: '关联采购入库', text: 'CGRK-20260827-009', url: '采购管理/采购入库列表.html' },
        { label: '退货日期', text: '2026-09-12' },
        { label: '退货原因', text: '到货验收不合格（镀层脱落），整批拒收', full: true },
        { label: '备注', text: '—' },
        { label: '货款支付状态', text: '未付款 · 拒收未入库，不产生应付与退款', full: true },
        { label: '制单人', text: '林国栋' }
      ],
      itemTitle: '退货明细',
      itemCols: ['序号', '物料编码', '物料名称', '规格', '单位', '可退上限', '退货数量', '备注'],
      items: [
        ['1', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '500', '500', '—']
      ],
      chain: [
        { role: '采购入库单', name: 'CGRK-20260827-009', url: '采购管理/采购入库列表.html' },
        { role: '采购退货单（本单）', name: 'CGTH-20260912-002', self: true },
        { role: '应付账单', name: '货款未付 · 拒收不挂账（单据终结）', url: '财务协同/应付账单.html' }
      ],
      timeline: [
        { t: '09-12 08:40', text: '采购退货登记 · 收货拒收', who: '林国栋' },
        { t: '09-12 16:10', text: '审核通过 · 不动原入库单（未入库）· 货款未付，无需退款', who: '徐文' }
      ]
    },
    'CGTH-20260910-003': {
      'row': {"fields": {"type": "入库后退货", "ref": "CGRK-20260827-010", "supplier": "延陵塑料托盘厂", "material": "木托盘 1200×1000×400", "qty": "40 块", "amount": "1,960.00", "status": "已退款", "payStatus": "部分付款", "date": "2026-09-10"}, "cells": ["入库后退货", "<span class=\"lk\">CGRK-20260827-010</span>", "延陵塑料托盘厂", "木托盘 1200×1000×400", "<span class=\"td-num\">40 块</span>", "<span class=\"td-num\">1,960.00</span>", "<span class=\"tag tag-green\">已退款</span>", "2026-09-10"], "ops": [{"t": "详情", "act": "go('../采购管理/采购退货详情.html?id=CGTH-20260910-003')"}, {"t": "退款登记", "act": "go('../财务协同/退款登记.html')"}]},
      title: '采购退货单详情',
      formTitle: '退货信息',
      formRows: [
        { label: '退货单号', text: 'CGTH-20260910-003' },
        { label: '状态', tag: '已退款' },
        { label: '退货类型', text: '入库后退货（已入库再退）' },
        { label: '供应商', text: '延陵塑料托盘厂' },
        { label: '关联采购入库', text: 'CGRK-20260827-010', url: '采购管理/采购入库列表.html' },
        { label: '退货日期', text: '2026-09-10' },
        { label: '退货原因', text: '项目减量，多余托盘退回供应商', full: true },
        { label: '备注', text: '—' },
        { label: '货款支付状态', text: '部分付款（应付已付 6,000 元）· 退货走退款', full: true },
        { label: '关联退款单', text: 'TKD-20260912-003', url: '财务协同/退款登记.html' },
        { label: '制单人', text: '林国栋' }
      ],
      itemTitle: '退货明细',
      itemCols: ['序号', '物料编码', '物料名称', '规格', '单位', '可退上限', '退货数量', '备注'],
      items: [
        ['1', 'PLT-1210W', '木托盘 1200×1000', '1200×1000×144 mm', '块', '40', '40', '—']
      ],
      chain: [
        { role: '采购入库单', name: 'CGRK-20260827-010', url: '采购管理/采购入库列表.html' },
        { role: '采购退货单（本单）', name: 'CGTH-20260910-003', self: true },
        { role: '退款登记', name: 'TKD-20260912-003 · 1,960.00 元', url: '财务协同/退款登记.html' }
      ],
      timeline: [
        { t: '09-10 11:05', text: '采购退货登记 · 提交审核', who: '林国栋' },
        { t: '09-11 09:40', text: '审核通过 · 冲减库存（货款已付部分，走退款）', who: '徐文' },
        { t: '09-12 11:00', text: '退款登记 · TKD-20260912-003', who: '财务·周敏' },
        { t: '09-13 10:05', text: '退款到账确认 · 单据转已退款', who: '王芳' }
      ]
    },
  },

  /* --------------------------------------------------------------------------
 * 销售退货单 salesReturns：键 = 退货单号（G33 · 退货退款闭环方案 B）
 *   fields: type/ref(关联销售出库单 XSCK-)/customer/material/qty/amount/status/date
 *   方向映射（陆鸣 09-15 拍板·固定）：销售退货 → 销售退货退款（客户·我方付款）
 * ------------------------------------------------------------------------ */
  salesReturns: {
    'XSTH-20260913-001': {
      'row': {"fields": {"type": "收货拒收", "ref": "XSCK-20260902-015", "customer": "华骏重卡汽车有限公司", "material": "箱盖 ABS 吸塑", "qty": "200 件", "amount": "3,600.00", "status": "已退款", "date": "2026-09-13"}, "cells": ["收货拒收", "<span class=\"lk\">XSCK-20260902-015</span>", "华骏重卡汽车有限公司", "箱盖 ABS 吸塑", "<span class=\"td-num\">200 件</span>", "<span class=\"td-num\">3,600.00</span>", "<span class=\"tag tag-green\">已退款</span>", "2026-09-13"], "ops": [{"t": "详情", "act": "go('../销售管理/销售退货详情.html?id=XSTH-20260913-001')"}, {"t": "退款登记", "act": "go('../财务协同/退款登记.html')"}]},
      title: '销售退货单详情',
      formTitle: '退货信息',
      formRows: [
        { label: '退货单号', text: 'XSTH-20260913-001' },
        { label: '状态', tag: '已退款' },
        { label: '退货类型', text: '收货拒收（客户未收货直接退回）' },
        { label: '客户', text: '华骏重卡汽车有限公司' },
        { label: '关联销售出库', text: 'XSCK-20260902-015', url: '销售管理/销售出库列表.html' },
        { label: '退货日期', text: '2026-09-13' },
        { label: '退货原因', text: '客户产线暂停，出库后整批拒收退回', full: true },
        { label: '备注', text: '—' },
        { label: '关联退款单', text: 'TKD-20260913-002', url: '财务协同/退款登记.html' },
        { label: '制单人', text: '沈婷' }
      ],
      itemTitle: '退货明细',
      itemCols: ['序号', '物料编码', '物料名称', '规格', '单位', '可退上限', '退货数量', '备注'],
      items: [
        ['1', 'LJ-D400', '箱盖', 'ABS 吸塑 · 1200×1000', '件', '200', '200', '—']
      ],
      chain: [
        { role: '销售出库单', name: 'XSCK-20260902-015', url: '销售管理/销售出库列表.html' },
        { role: '销售退货单（本单）', name: 'XSTH-20260913-001', self: true },
        { role: '退款登记', name: 'TKD-20260913-002', url: '财务协同/退款登记.html' }
      ],
      timeline: [
        { t: '09-13 09:15', text: '销售退货登记 · 提交审核', who: '沈婷' },
        { t: '09-13 15:40', text: '审核通过 · 货物回仓', who: '陈锋' },
        { t: '09-14 09:50', text: '应收退款付讫 · 单据转已退款', who: '财务·周敏' }
      ]
    },
    'XSTH-20260912-002': {
      'row': {"fields": {"type": "入库后退货", "ref": "XSCK-20260901-014", "customer": "长风汽车制造有限公司", "material": "锁扣组件", "qty": "100 套", "amount": "800.00", "status": "已审核", "date": "2026-09-12"}, "cells": ["入库后退货", "<span class=\"lk\">XSCK-20260901-014</span>", "长风汽车制造有限公司", "锁扣组件", "<span class=\"td-num\">100 套</span>", "<span class=\"td-num\">800.00</span>", "<span class=\"tag tag-blue\">已审核</span>", "2026-09-12"], "ops": [{"t": "详情", "act": "go('../销售管理/销售退货详情.html?id=XSTH-20260912-002')"}, {"t": "退款登记", "act": "go('../财务协同/退款登记.html')"}]},
      title: '销售退货单详情',
      formTitle: '退货信息',
      formRows: [
        { label: '退货单号', text: 'XSTH-20260912-002' },
        { label: '状态', tag: '已审核' },
        { label: '退货类型', text: '入库后退货（客户收货使用后退货回仓）', full: true },
        { label: '客户', text: '长风汽车制造有限公司' },
        { label: '关联销售出库', text: 'XSCK-20260901-014', url: '销售管理/销售出库列表.html' },
        { label: '退货日期', text: '2026-09-12' },
        { label: '退货原因', text: '多发数量退回（开票前冲减）', full: true },
        { label: '备注', text: '—' },
        { label: '制单人', text: '沈婷' }
      ],
      itemTitle: '退货明细',
      itemCols: ['序号', '物料编码', '物料名称', '规格', '单位', '可退上限', '退货数量', '备注'],
      items: [
        ['1', 'LJ-A100', '锁扣组件', '不锈钢 304 · M8', '件', '100', '100', '—']
      ],
      chain: [
        { role: '销售出库单', name: 'XSCK-20260901-014', url: '销售管理/销售出库列表.html' },
        { role: '销售退货单（本单）', name: 'XSTH-20260912-002', self: true },
        { role: '退款登记', name: '待退款（应收退款·对客户）' }
      ],
      timeline: [
        { t: '09-12 10:20', text: '销售退货登记 · 提交审核', who: '沈婷' },
        { t: '09-12 17:35', text: '审核通过 · 验收回仓', who: '陈锋' },
        { t: '—', text: '待退款 · 退款付讫后转已退款', off: true }
      ]
    },
    'XSTH-20260911-003': {
      'row': {"fields": {"type": "收货拒收", "ref": "XSCK-20260826-012", "customer": "东海商用汽车有限公司宁波分公司", "material": "内衬", "qty": "300 件", "amount": "1,500.00", "status": "待审核", "date": "2026-09-11"}, "cells": ["收货拒收", "<span class=\"lk\">XSCK-20260826-012</span>", "东海商用汽车有限公司宁波分公司", "内衬", "<span class=\"td-num\">300 件</span>", "<span class=\"td-num\">1,500.00</span>", "<span class=\"tag tag-orange\">待审核</span>", "2026-09-11"], "ops": [{"t": "审核", "act": "go('../销售管理/销售退货审核.html?id=XSTH-20260911-003')"}, {"t": "详情", "act": "go('../销售管理/销售退货详情.html?id=XSTH-20260911-003')"}]},
      title: '销售退货单详情',
      formTitle: '退货信息',
      formRows: [
        { label: '退货单号', text: 'XSTH-20260911-003' },
        { label: '状态', tag: '待审核' },
        { label: '退货类型', text: '收货拒收（客户未收货直接退回）' },
        { label: '客户', text: '东海商用汽车有限公司宁波分公司' },
        { label: '关联销售出库', text: 'XSCK-20260826-012', url: '销售管理/销售出库列表.html' },
        { label: '退货日期', text: '2026-09-11' },
        { label: '退货原因', text: '质量异议（划伤），产线拒收整批退回', full: true },
        { label: '备注', text: '—' },
        { label: '制单人', text: '沈婷' }
      ],
      itemTitle: '退货明细',
      itemCols: ['序号', '物料编码', '物料名称', '规格', '单位', '可退上限', '退货数量', '备注'],
      items: [
        ['1', 'LJ-F600', '内衬', 'EPE 珍珠棉 · 定制', '件', '300', '300', '—']
      ],
      chain: [
        { role: '销售出库单', name: 'XSCK-20260826-012', url: '销售管理/销售出库列表.html' },
        { role: '销售退货单（本单）', name: 'XSTH-20260911-003', self: true },
        { role: '退款登记', name: '待审核通过后生成' }
      ],
      timeline: [
        { t: '09-11 14:30', text: '销售退货登记 · 提交审核', who: '沈婷' },
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
    'TKD-20260913-002': {
      'row': {"fields": {"type": "销售退货退款", "ref": "XSTH-20260913-001", "partner": "华骏重卡汽车有限公司", "amount": "3,600.00", "direction": "付款（退回客户）", "status": "已确认", "date": "2026-09-13"}, "cells": ["销售退货退款（客户·我方付款）", "<span class=\"lk\">XSTH-20260913-001</span>", "华骏重卡汽车有限公司", "<span class=\"td-num\">3,600.00</span>", "付款（退回客户）", "<span class=\"tag tag-green\">已确认</span>", "2026-09-13"], "ops": [{"t": "详情", "act": "go('../财务协同/退款详情.html?id=TKD-20260913-002')"}]},
      title: '退款登记详情',
      formTitle: '退款信息',
      formRows: [
        { label: '退款单号', text: 'TKD-20260913-002' },
        { label: '状态', tag: '已确认' },
        { label: '退款类型', text: '销售退货退款（客户·我方付款）' },
        { label: '资金方向', text: '付款 · 我方退回客户' },
        { label: '退款日期', text: '2026-09-13' },
        { label: '往来单位', text: '华骏重卡汽车有限公司' },
        { label: '关联退货单', text: 'XSTH-20260913-001', url: '销售管理/销售退货单列表.html' },
        { label: '退款金额', text: '3,600.00 元' },
        { label: '收退款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务·周敏' },
        { label: '备注', text: '—' }
      ],
      itemTitle: '退款明细',
      itemCols: ['关联退货单', '退货类型', '退款金额(元)'],
      items: [
        ['XSTH-20260913-001', '收货拒收', '3,600.00']
      ],
      chain: [
        { role: '销售退货单', name: 'XSTH-20260913-001', url: '销售管理/销售退货单列表.html' },
        { role: '退款登记（本单）', name: 'TKD-20260913-002', self: true },
        { role: '退款确认', name: '已确认 · 退款付讫' }
      ],
      timeline: [
        { t: '09-13 16:20', text: '退款登记 · 销售退货退款登记提交', who: '财务·周敏' },
        { t: '09-14 09:50', text: '退款确认通过 · 付款退回客户', who: '王芳' }
      ]
    },
    'TKD-20260912-003': {
      'row': {"fields": {"type": "采购退货退款", "ref": "CGTH-20260910-003", "partner": "延陵塑料托盘厂", "amount": "1,960.00", "direction": "收款（供应商退回）", "status": "已确认", "date": "2026-09-12"}, "cells": ["采购退货退款（供应商·我方收款）", "<span class=\"lk\">CGTH-20260910-003</span>", "延陵塑料托盘厂", "<span class=\"td-num\">1,960.00</span>", "收款（供应商退回）", "<span class=\"tag tag-green\">已确认</span>", "2026-09-12"], "ops": [{"t": "详情", "act": "go('../财务协同/退款详情.html?id=TKD-20260912-003')"}]},
      title: '退款登记详情',
      formTitle: '退款信息',
      formRows: [
        { label: '退款单号', text: 'TKD-20260912-003' },
        { label: '状态', tag: '已确认' },
        { label: '退款类型', text: '采购退货退款（供应商·我方收款）' },
        { label: '资金方向', text: '收款 · 供应商退回我方' },
        { label: '退款日期', text: '2026-09-12' },
        { label: '往来单位', text: '延陵塑料托盘厂' },
        { label: '关联退货单', text: 'CGTH-20260910-003', url: '采购管理/采购退货单列表.html' },
        { label: '退款金额', text: '1,960.00 元' },
        { label: '收退款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务·周敏' },
        { label: '备注', text: '货款已付（部分付款 6,000 元 ≥ 退款额），退款成立' }
      ],
      itemTitle: '退款明细',
      itemCols: ['关联退货单', '退货类型', '退款金额(元)'],
      items: [
        ['CGTH-20260910-003', '入库后退货', '1,960.00']
      ],
      chain: [
        { role: '采购退货单', name: 'CGTH-20260910-003', url: '采购管理/采购退货单列表.html' },
        { role: '退款登记（本单）', name: 'TKD-20260912-003', self: true },
        { role: '退款确认', name: '已确认 · 退款到账' }
      ],
      timeline: [
        { t: '09-12 11:00', text: '退款登记 · 采购退货退款登记提交', who: '财务·周敏' },
        { t: '09-13 10:05', text: '退款确认通过 · 供应商退款到账', who: '王芳' }
      ]
    },

    'TKD-20260916-004': {
      'row': {"fields": {"type": "预收退回", "ref": "AR-2026-09-PRJ2601-YS", "partner": "华骏重卡汽车有限公司", "amount": "20,000.00", "direction": "付款（退回客户）", "status": "待审核", "date": "2026-09-16"}, "cells": ["预收退回（客户·我方付款）", "<span class=\"lk\" onclick=\"go('../财务协同/应收账单.html')\">AR-2026-09-PRJ2601-YS</span>", "华骏重卡汽车有限公司", "<span class=\"td-num\">20,000.00</span>", "付款（退回客户）", "<span class=\"tag tag-orange\">待审核</span>", "2026-09-16"], "ops": [{"t": "确认", "act": "openModal('auditModal')"}, {"t": "详情", "act": "go('../财务协同/退款详情.html?id=TKD-20260916-004')"}]},
      title: '退款登记详情',
      formTitle: '退款信息',
      formRows: [
        { label: '退款单号', text: 'TKD-20260916-004' },
        { label: '状态', tag: '待审核' },
        { label: '退款类型', text: '预收退回（客户·我方付款）' },
        { label: '资金方向', text: '付款 · 我方退回客户' },
        { label: '退款日期', text: '2026-09-16' },
        { label: '往来单位', text: '华骏重卡汽车有限公司' },
        { label: '关联账单', text: 'AR-2026-09-PRJ2601-YS', url: '财务协同/应收账单.html' },
        { label: '退款金额', text: '20,000.00 元（预收 50,000 部分退回）', full: true },
        { label: '收退款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务·周敏' },
        { label: '备注', text: '—' }
      ],
      itemTitle: '退款明细',
      itemCols: ['关联账单', '费用项', '退款金额(元)'],
      items: [
        ['AR-2026-09-PRJ2601-YS', '预收冲抵后余额退回', '20,000.00']
      ],
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
      'row': {"fields": {"type": "多付退回", "ref": "AP-20260905-012", "partner": "环通包装运营", "amount": "10,000.00", "direction": "收款（供应商退回）", "status": "已确认", "date": "2026-09-16"}, "cells": ["多付退回（供应商·我方收款）", "<span class=\"lk\" onclick=\"go('../财务协同/应付账单.html')\">AP-20260905-012</span>", "环通包装运营", "<span class=\"td-num\">10,000.00</span>", "收款（供应商退回）", "<span class=\"tag tag-green\">已确认</span>", "2026-09-16"], "ops": [{"t": "详情", "act": "go('../财务协同/退款详情.html?id=TKD-20260916-005')"}]},
      title: '退款登记详情',
      formTitle: '退款信息',
      formRows: [
        { label: '退款单号', text: 'TKD-20260916-005' },
        { label: '状态', tag: '已确认' },
        { label: '退款类型', text: '多付退回（供应商·我方收款）' },
        { label: '资金方向', text: '收款 · 供应商退回我方' },
        { label: '退款日期', text: '2026-09-16' },
        { label: '往来单位', text: '环通包装运营' },
        { label: '关联账单', text: 'AP-20260905-012', url: '财务协同/应付账单.html' },
        { label: '退款金额', text: '10,000.00 元（预付多付款项退回）', full: true },
        { label: '收退款账户', text: '招商银行苏州分行 1109××××8821' },
        { label: '登记人', text: '财务·周敏' },
        { label: '备注', text: '—' }
      ],
      itemTitle: '退款明细',
      itemCols: ['关联账单', '费用项', '退款金额(元)'],
      items: [
        ['AP-20260905-012', '预付多付退回', '10,000.00']
      ],
      chain: [
        { role: '应付账单（预付）', name: 'AP-20260905-012', url: '财务协同/应付账单.html' },
        { role: '退款登记（本单）', name: 'TKD-20260916-005', self: true },
        { role: '退款确认', name: '已确认 · 款项收讫' }
      ],
      timeline: [
        { t: '09-16 10:00', text: '退款登记 · 多付 ¥10,000 退回申请（与 09-12 预付冲减呼应）', who: '财务·周敏' },
        { t: '09-16 15:00', text: '退款确认通过 · 供应商原路退回', who: '王芳' }
      ]
    },
  },
  transferOutbounds: {
    'ZY-20260915-005': {
      'row': {"fields": {"from": "安吉智行物流", "to": "博世汽车部件（苏州）", "material": "围板箱 1200×1000×970", "qty": "200 只", "settle": "按租出结算", "date": "2026-09-15", "project": "PRJ-2605", "status": "待审核"}, "cells": ["安吉智行物流", "博世汽车部件（苏州）", "围板箱 1200×1000×970", "<span class=\"td-num\">200 只</span>", "按租出结算", "2026-09-15", "<span class=\"tag tag-orange\">待审核</span>"], "ops": [{"t": "审核", "act": "go('../租赁管理/转移出库审核.html?id=ZY-20260915-005')"}, {"t": "详情", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260915-005')"}]},
      title: '转移出库单详情',
      formTitle: '转移信息',
      formRows: [
        { label: '转移单号', text: 'ZY-20260915-005' },
        { label: '状态', tag: '待审核' },
        { label: '关联项目', text: 'PRJ-2605 华骏重卡·蔚山基地 围板箱租赁扩建' },
        { label: '转出方（直接客户）', text: '安吉智行物流' },
        { label: '接收方（终端客户）', text: '博世汽车部件（苏州）' },
        { label: '转移日期', text: '2026-09-15' },
        { label: '结算方式', text: '按租出结算（默认取项目档案，可按单覆盖）' },
        { label: '备注', text: '—' },
        { label: '财务口径', text: '不生成应收账单——租金仍向直接客户（安吉智行物流）计收，转移单不进财务链路', full: true },
        { label: '制单人', text: '沈婷' }
      ],
      itemTitle: '转移明细',
      itemCols: ['序号', '物料编码', '物料名称', '规格', '单位', '转移数量', '备注'],
      items: [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '200', '—']
      ],
      chain: [
        { role: '直接客户', name: '安吉智行物流（在租 640 只）' },
        { role: '转移出库单（本单）', name: 'ZY-20260915-005', self: true },
        { role: '终端客户', name: '博世汽车部件（苏州）·待审核生效' }
      ],
      timeline: [
        { t: '09-15 09:20', text: '转移出库登记 · 提交', who: '沈婷' },
        { t: '—', text: '待审核 · 审核通过后转移生效，库存状态转「客户转租出」', off: true }
      ]
    },
    'ZY-20260914-003': {
      'row': {"fields": {"from": "安吉智行物流", "to": "博世汽车部件（苏州）", "material": "料箱 600×400×340", "qty": "360 只", "settle": "按租出结算", "date": "2026-09-14", "project": "PRJ-2605", "status": "已转移"}, "cells": ["安吉智行物流", "博世汽车部件（苏州）", "料箱 600×400×340", "<span class=\"td-num\">360 只</span>", "按租出结算", "2026-09-14", "<span class=\"tag tag-green\">已转移</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260914-003')"}, {"t": "终止转移", "act": "zyStop(this)"}]},
      title: '转移出库单详情',
      formTitle: '转移信息',
      formRows: [
        { label: '转移单号', text: 'ZY-20260914-003' },
        { label: '状态', tag: '已转移' },
        { label: '关联项目', text: 'PRJ-2605 华骏重卡·蔚山基地 围板箱租赁扩建' },
        { label: '转出方（直接客户）', text: '安吉智行物流' },
        { label: '接收方（终端客户）', text: '博世汽车部件（苏州）' },
        { label: '转移日期', text: '2026-09-14' },
        { label: '结算方式', text: '按租出结算（默认取项目档案）' },
        { label: '备注', text: '—' },
        { label: '财务口径', text: '不生成应收账单——租金仍向直接客户（安吉智行物流）计收，转移单不进财务链路', full: true },
        { label: '库存状态', text: 'XNC-ZZ-BTC · 客户转租出（筛「客户转租出」可查）' },
        { label: '制单人', text: '沈婷' }
      ],
      itemTitle: '转移明细',
      itemCols: ['序号', '物料编码', '物料名称', '规格', '单位', '转移数量', '备注'],
      items: [
        ['1', 'BTC-6040', '料箱 600×400×340', '600×400×340 mm', '只', '360', '—']
      ],
      chain: [
        { role: '直接客户', name: '安吉智行物流' },
        { role: '转移出库单（本单）', name: 'ZY-20260914-003', self: true },
        { role: '终端客户', name: '博世汽车部件（苏州）' }
      ],
      timeline: [
        { t: '09-14 10:40', text: '转移出库登记 · 提交', who: '沈婷' },
        { t: '09-14 15:30', text: '审核通过 · 转移生效 · 库存状态转「客户转租出」', who: '物流·赵磊' }
      ]
    },
    'ZY-20260914-002': {
      'row': {"fields": {"from": "长丰锂电科技", "to": "星辉动力电池有限公司", "material": "塑料托盘 1200×1000", "qty": "80 张", "settle": "按终端结算", "date": "2026-09-14", "project": "PRJ-2603", "status": "已转移"}, "note": "1", "cells": ["长丰锂电科技", "星辉动力电池有限公司", "塑料托盘 1200×1000", "<span class=\"td-num\">80 张</span>", "按终端结算", "2026-09-14", "<span class=\"tag tag-green\">已转移</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260914-002')"}, {"t": "终止转移", "act": "zyStop(this)"}]},
      title: '转移出库单详情',
      formTitle: '转移信息',
      formRows: [
        { label: '转移单号', text: 'ZY-20260914-002' },
        { label: '状态', tag: '已转移' },
        { label: '关联项目', text: 'PRJ-2603 长丰锂电·电池包周转箱租赁' },
        { label: '转出方（直接客户）', text: '长丰锂电科技' },
        { label: '接收方（终端客户）', text: '星辉动力电池有限公司' },
        { label: '转移日期', text: '2026-09-14' },
        { label: '结算方式', text: '按终端结算（单据级覆盖·项目档案默认为按租出结算的特例项目）' },
        { label: '备注', text: '—' },
        { label: '财务口径', text: '转移生效后后续应收账单主体切换为终端客户（星辉动力电池有限公司）·历史账单不回改', full: true },
        { label: '库存状态', text: 'XNC-ZZ-PLT2 · 客户转租出（筛「客户转租出」可查）' },
        { label: '制单人', text: '江强' }
      ],
      itemTitle: '转移明细',
      itemCols: ['序号', '物料编码', '物料名称', '规格', '单位', '转移数量', '备注'],
      items: [
        ['1', 'PLT-1210P', '塑料托盘 1200×1000', '1200×1000×150 mm', '块', '80', '—']
      ],
      chain: [
        { role: '直接客户', name: '长丰锂电科技' },
        { role: '转移出库单（本单）', name: 'ZY-20260914-002', self: true },
        { role: '终端客户（账单主体）', name: '星辉动力电池有限公司' }
      ],
      timeline: [
        { t: '09-14 08:55', text: '转移出库登记 · 结算方式按终端（覆盖项目默认）', who: '江强' },
        { t: '09-14 14:10', text: '审核通过 · 转移生效 · 库存状态转「客户转租出」· 后续账单主体切终端', who: '物流·赵磊' }
      ]
    },
    'ZY-20260914-001': {
      'row': {"fields": {"from": "安吉智行物流", "to": "博世汽车部件（苏州）", "material": "围板箱 1200×1000×970", "qty": "240 只", "settle": "按租出结算", "date": "2026-09-14", "project": "PRJ-2605", "status": "已转移"}, "cells": ["安吉智行物流", "博世汽车部件（苏州）", "围板箱 1200×1000×970", "<span class=\"td-num\">240 只</span>", "按租出结算", "2026-09-14", "<span class=\"tag tag-green\">已转移</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260914-001')"}, {"t": "终止转移", "act": "zyStop(this)"}]},
      title: '转移出库单详情',
      formTitle: '转移信息',
      formRows: [
        { label: '转移单号', text: 'ZY-20260914-001' },
        { label: '状态', tag: '已转移' },
        { label: '关联项目', text: 'PRJ-2605 华骏重卡·蔚山基地 围板箱租赁扩建' },
        { label: '转出方（直接客户）', text: '安吉智行物流' },
        { label: '接收方（终端客户）', text: '博世汽车部件（苏州）' },
        { label: '转移日期', text: '2026-09-14' },
        { label: '结算方式', text: '按租出结算（默认取项目档案）' },
        { label: '备注', text: '—' },
        { label: '财务口径', text: '不生成应收账单——租金仍向直接客户（安吉智行物流）计收，转移单不进财务链路', full: true },
        { label: '库存状态', text: 'XNC-ZZ-WBX · 客户转租出（筛「客户转租出」可查）' },
        { label: '制单人', text: '沈婷' }
      ],
      itemTitle: '转移明细',
      itemCols: ['序号', '物料编码', '物料名称', '规格', '单位', '转移数量', '备注'],
      items: [
        ['1', 'WBX-1210L', '围板箱 1200×1000×970', '1200×1000×970 mm', '只', '240', '—']
      ],
      chain: [
        { role: '直接客户', name: '安吉智行物流' },
        { role: '转移出库单（本单）', name: 'ZY-20260914-001', self: true },
        { role: '终端客户', name: '博世汽车部件（苏州）' }
      ],
      timeline: [
        { t: '09-14 08:30', text: '转移出库登记 · 提交（库存查询「客户在租」行入口带出）', who: '沈婷' },
        { t: '09-14 11:20', text: '审核通过 · 转移生效 · 库存状态转「客户转租出」', who: '物流·赵磊' }
      ]
    },
    'ZY-20260912-004': {
      'row': {"fields": {"from": "安吉智行物流", "to": "延锋汽车饰件（苏州）", "material": "塑料托盘 1200×1000", "qty": "120 张", "settle": "按租出结算", "date": "2026-09-12", "project": "PRJ-2605", "status": "已终止"}, "cells": ["安吉智行物流", "延锋汽车饰件（苏州）", "塑料托盘 1200×1000", "<span class=\"td-num\">120 张</span>", "按租出结算", "2026-09-12", "<span class=\"tag tag-gray\">已终止</span>"], "ops": [{"t": "详情", "act": "go('../租赁管理/转移出库单详情.html?id=ZY-20260912-004')"}]},
      title: '转移出库单详情',
      formTitle: '转移信息',
      formRows: [
        { label: '转移单号', text: 'ZY-20260912-004' },
        { label: '状态', tag: '已终止' },
        { label: '关联项目', text: 'PRJ-2605 华骏重卡·蔚山基地 围板箱租赁扩建' },
        { label: '转出方（直接客户）', text: '安吉智行物流' },
        { label: '接收方（终端客户）', text: '延锋汽车饰件（苏州）' },
        { label: '转移日期', text: '2026-09-12' },
        { label: '终止日期', text: '2026-09-13' },
        { label: '结算方式', text: '按租出结算（默认取项目档案）' },
        { label: '备注', text: '—' },
        { label: '财务口径', text: '不生成应收账单——租金仍向直接客户（安吉智行物流）计收', full: true },
        { label: '库存状态', text: '已回「在客户（租出）」· 安吉智行客户虚拟仓（XNC-ZZ-PLT）' },
        { label: '制单人', text: '沈婷' }
      ],
      itemTitle: '转移明细',
      itemCols: ['序号', '物料编码', '物料名称', '规格', '单位', '转移数量', '备注'],
      items: [
        ['1', 'PLT-1210P', '塑料托盘 1200×1000', '1200×1000×150 mm', '块', '120', '—']
      ],
      chain: [
        { role: '直接客户', name: '安吉智行物流' },
        { role: '转移出库单（本单·已终止）', name: 'ZY-20260912-004', self: true },
        { role: '终端客户', name: '延锋汽车饰件（苏州）·已追回' }
      ],
      timeline: [
        { t: '09-12 14:00', text: '转移出库登记 · 提交', who: '沈婷' },
        { t: '09-12 17:45', text: '审核通过 · 转移生效 · 库存状态转「客户转租出」', who: '物流·赵磊' },
        { t: '09-13 09:30', text: '终止转移 · 库存状态回「在客户（租出）」', who: '物流·赵磊' }
      ]
    },
  },

  /* G39 T2 · 在租量事件流水（D-148）：每条＝日期+客户+项目+物料+数量+方向；
     每日在租量由事件派生——出库/入库当日计入，退租/归还当日仍计、次日起减（天数=max(2,止-起+1)） */
  stockEvents: {
    'EV-20260814-001': { 'row': {"fields": {"date": "2026-08-14", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "200", "unit": "套", "dir": "其他出入库", "doc": "期初结转", "side": "客户在租", "note": "期初在租结转（历史出库未入流水·不做历史迁移）"}, "cells": ["2026-08-14", "华骏重卡汽车有限公司", "PRJ-2601", "ZH-2601-A", "驾驶室围板箱整箱套件", "套", "<span class=\"td-num\">200</span>", "<span class=\"tag tag-gray\">其他出入库</span>", "期初结转", "客户在租"]} },
    'EV-20260818-002': { 'row': {"fields": {"date": "2026-08-18", "customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2602", "mat": "PLT-1210P", "matName": "塑料托盘", "qty": "150", "unit": "块", "dir": "其他出入库", "doc": "期初结转", "side": "客户在租", "note": "期初在租结转"}, "cells": ["2026-08-18", "东海商用汽车有限公司宁波分公司", "PRJ-2602", "PLT-1210P", "塑料托盘", "块", "<span class=\"td-num\">150</span>", "<span class=\"tag tag-gray\">其他出入库</span>", "期初结转", "客户在租"]} },
    'EV-20260820-003': { 'row': {"fields": {"date": "2026-08-20", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "30", "unit": "套", "dir": "退租", "doc": "TZRK-20260820-003", "side": "客户在租", "note": "BOM 拆散退回"}, "cells": ["2026-08-20", "华骏重卡汽车有限公司", "PRJ-2601", "ZH-2601-A", "驾驶室围板箱整箱套件", "套", "<span class=\"td-num\">30</span>", "<span class=\"tag tag-green\">退租</span>", "TZRK-20260820-003", "客户在租"]} },
    'EV-20260824-004': { 'row': {"fields": {"date": "2026-08-24", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2604", "mat": "ZH-2604-D", "matName": "混合组合套件", "qty": "40", "unit": "套", "dir": "出库", "doc": "CK-20260824-009", "side": "客户在租"}, "cells": ["2026-08-24", "华骏重卡汽车有限公司", "PRJ-2604", "ZH-2604-D", "混合组合套件", "套", "<span class=\"td-num\">40</span>", "<span class=\"tag tag-blue\">出库</span>", "CK-20260824-009", "客户在租"]} },
    'EV-20260825-005': { 'row': {"fields": {"date": "2026-08-25", "customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2602", "mat": "PLT-1210P", "matName": "塑料托盘", "qty": "150", "unit": "块", "dir": "退租", "doc": "TZRK-20260825-004", "side": "客户在租"}, "cells": ["2026-08-25", "东海商用汽车有限公司宁波分公司", "PRJ-2602", "PLT-1210P", "塑料托盘", "块", "<span class=\"td-num\">150</span>", "<span class=\"tag tag-green\">退租</span>", "TZRK-20260825-004", "客户在租"]} },
    'EV-20260826-006': { 'row': {"fields": {"date": "2026-08-26", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "mat": "BTC-6040", "matName": "料箱", "qty": "200", "unit": "只", "dir": "其他出入库", "doc": "期初结转", "side": "客户在租", "note": "期初在租结转"}, "cells": ["2026-08-26", "华骏重卡汽车有限公司", "PRJ-2601", "BTC-6040", "料箱", "只", "<span class=\"td-num\">200</span>", "<span class=\"tag tag-gray\">其他出入库</span>", "期初结转", "客户在租"]} },
    'EV-20260828-007': { 'row': {"fields": {"date": "2026-08-28", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "mat": "BTC-6040", "matName": "料箱", "qty": "200", "unit": "只", "dir": "退租", "doc": "TZRK-20260828-005", "side": "客户在租"}, "cells": ["2026-08-28", "华骏重卡汽车有限公司", "PRJ-2601", "BTC-6040", "料箱", "只", "<span class=\"td-num\">200</span>", "<span class=\"tag tag-green\">退租</span>", "TZRK-20260828-005", "客户在租"]} },
    'EV-20260828-008': { 'row': {"fields": {"date": "2026-08-28", "customer": "长风汽车制造有限公司", "project": "PRJ-2604", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "96", "unit": "套", "dir": "出库", "doc": "CK-20260828-011", "side": "客户在租"}, "cells": ["2026-08-28", "长风汽车制造有限公司", "PRJ-2604", "ZH-2601-A", "驾驶室围板箱整箱套件", "套", "<span class=\"td-num\">96</span>", "<span class=\"tag tag-blue\">出库</span>", "CK-20260828-011", "客户在租"]} },
    'EV-20260828-009': { 'row': {"fields": {"date": "2026-08-28", "customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2602", "mat": "ZH-2602-B", "matName": "冲压件料箱组套", "qty": "200", "unit": "套", "dir": "出库", "doc": "CK-20260828-010", "side": "客户在租"}, "cells": ["2026-08-28", "东海商用汽车有限公司宁波分公司", "PRJ-2602", "ZH-2602-B", "冲压件料箱组套", "套", "<span class=\"td-num\">200</span>", "<span class=\"tag tag-blue\">出库</span>", "CK-20260828-010", "客户在租"]} },
    'EV-20260829-010': { 'row': {"fields": {"date": "2026-08-29", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "120", "unit": "套", "dir": "出库", "doc": "CK-20260829-012", "side": "客户在租"}, "cells": ["2026-08-29", "华骏重卡汽车有限公司", "PRJ-2601", "ZH-2601-A", "驾驶室围板箱整箱套件", "套", "<span class=\"td-num\">120</span>", "<span class=\"tag tag-blue\">出库</span>", "CK-20260829-012", "客户在租"]} },
    'EV-20260829-011': { 'row': {"fields": {"date": "2026-08-29", "customer": "星途新能源汽车科技有限公司", "project": "PRJ-2603", "mat": "ZH-2603-C", "matName": "电池托盘护角套件", "qty": "60", "unit": "套", "dir": "出库", "doc": "CK-20260829-013", "side": "客户在租", "note": "按次计费链（bomList.billing=按次）"}, "cells": ["2026-08-29", "星途新能源汽车科技有限公司", "PRJ-2603", "ZH-2603-C", "电池托盘护角套件", "套", "<span class=\"td-num\">60</span>", "<span class=\"tag tag-blue\">出库</span>", "CK-20260829-013", "客户在租"]} },
    'EV-20260830-012': { 'row': {"fields": {"date": "2026-08-30", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "180", "unit": "套", "dir": "出库", "doc": "CK-20260830-015", "side": "客户在租"}, "cells": ["2026-08-30", "华骏重卡汽车有限公司", "PRJ-2601", "ZH-2601-A", "驾驶室围板箱整箱套件", "套", "<span class=\"td-num\">180</span>", "<span class=\"tag tag-blue\">出库</span>", "CK-20260830-015", "客户在租"]} },
    'EV-20260831-013': { 'row': {"fields": {"date": "2026-08-31", "customer": "星途新能源汽车科技有限公司", "project": "PRJ-2603", "mat": "ZH-2603-C", "matName": "电池托盘护角套件", "qty": "20", "unit": "套", "dir": "退租", "doc": "TZRK-20260831-006", "side": "客户在租", "note": "部分退租"}, "cells": ["2026-08-31", "星途新能源汽车科技有限公司", "PRJ-2603", "ZH-2603-C", "电池托盘护角套件", "套", "<span class=\"td-num\">20</span>", "<span class=\"tag tag-green\">退租</span>", "TZRK-20260831-006", "客户在租"]} },
    'EV-20260901-014': { 'row': {"fields": {"date": "2026-09-01", "customer": "东海商用汽车有限公司宁波分公司", "project": "PRJ-2602", "mat": "ZH-2602-B", "matName": "冲压件料箱组套", "qty": "45", "unit": "套", "dir": "退租", "doc": "TZRK-20260901-007", "side": "客户在租", "note": "部分退租"}, "cells": ["2026-09-01", "东海商用汽车有限公司宁波分公司", "PRJ-2602", "ZH-2602-B", "冲压件料箱组套", "套", "<span class=\"td-num\">45</span>", "<span class=\"tag tag-green\">退租</span>", "TZRK-20260901-007", "客户在租"]} },
    'EV-20260903-015': { 'row': {"fields": {"date": "2026-09-03", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "60", "unit": "套", "dir": "出库", "doc": "CK-20260903-016", "side": "客户在租", "note": "退租回库件循环出库"}, "cells": ["2026-09-03", "华骏重卡汽车有限公司", "PRJ-2601", "ZH-2601-A", "驾驶室围板箱整箱套件", "套", "<span class=\"td-num\">60</span>", "<span class=\"tag tag-blue\">出库</span>", "CK-20260903-016", "客户在租"]} },
    'EV-20260908-016': { 'row': {"fields": {"date": "2026-09-08", "customer": "华骏重卡汽车有限公司", "project": "PRJ-2601", "mat": "ZH-2601-A", "matName": "驾驶室围板箱整箱套件", "qty": "120", "unit": "套", "dir": "退租", "doc": "TZRK-20260908-011", "side": "客户在租", "note": "部分退租（T6 演示·当日仍计租）"}, "cells": ["2026-09-08", "华骏重卡汽车有限公司", "PRJ-2601", "ZH-2601-A", "驾驶室围板箱整箱套件", "套", "<span class=\"td-num\">120</span>", "<span class=\"tag tag-green\">退租</span>", "TZRK-20260908-011", "客户在租"]} },
    'EV-20260731-017': { 'row': {"fields": {"date": "2026-07-31", "customer": "环通循环包装运营（上海）有限公司", "project": "—", "mat": "BTC-6040", "matName": "金属料箱 800×600", "qty": "20", "unit": "只", "dir": "其他出入库", "doc": "期初结转", "side": "租入持有", "note": "期初租入持有结转"}, "cells": ["2026-07-31", "环通循环包装运营（上海）有限公司", "—", "BTC-6040", "金属料箱 800×600", "只", "<span class=\"td-num\">20</span>", "<span class=\"tag tag-gray\">其他出入库</span>", "期初结转", "租入持有"]} },
    'EV-20260816-018': { 'row': {"fields": {"date": "2026-08-16", "customer": "环通循环包装运营（上海）有限公司", "project": "—", "mat": "WBX-1210L", "matName": "围板箱 1200×1000×970", "qty": "30", "unit": "只", "dir": "其他出入库", "doc": "RZRK-20260816-021", "side": "租入持有", "note": "租入入库"}, "cells": ["2026-08-16", "环通循环包装运营（上海）有限公司", "—", "WBX-1210L", "围板箱 1200×1000×970", "只", "<span class=\"td-num\">30</span>", "<span class=\"tag tag-gray\">其他出入库</span>", "RZRK-20260816-021", "租入持有"]} },
    'EV-20260816-019': { 'row': {"fields": {"date": "2026-08-16", "customer": "环通循环包装运营（上海）有限公司", "project": "—", "mat": "WBX-1210L", "matName": "围板箱 1200×1000×970", "qty": "10", "unit": "只", "dir": "其他出入库", "doc": "RZRK-20260816-022", "side": "租入持有", "note": "租入入库"}, "cells": ["2026-08-16", "环通循环包装运营（上海）有限公司", "—", "WBX-1210L", "围板箱 1200×1000×970", "只", "<span class=\"td-num\">10</span>", "<span class=\"tag tag-gray\">其他出入库</span>", "RZRK-20260816-022", "租入持有"]} },
    'EV-20260831-020': { 'row': {"fields": {"date": "2026-08-31", "customer": "环通循环包装运营（上海）有限公司", "project": "—", "mat": "BTC-6040", "matName": "金属料箱 800×600", "qty": "20", "unit": "只", "dir": "归还", "doc": "GHCK-20260831-003", "side": "租入持有", "note": "整退归还"}, "cells": ["2026-08-31", "环通循环包装运营（上海）有限公司", "—", "BTC-6040", "金属料箱 800×600", "只", "<span class=\"td-num\">20</span>", "<span class=\"tag tag-gray\">归还</span>", "GHCK-20260831-003", "租入持有"]} },
    'EV-20260903-021': { 'row': {"fields": {"date": "2026-09-03", "customer": "环通循环包装运营（上海）有限公司", "project": "—", "mat": "WBX-1210L", "matName": "围板箱 1200×1000×970", "qty": "30", "unit": "只", "dir": "归还", "doc": "GHCK-20260903-001", "side": "租入持有", "note": "整退归还"}, "cells": ["2026-09-03", "环通循环包装运营（上海）有限公司", "—", "WBX-1210L", "围板箱 1200×1000×970", "只", "<span class=\"td-num\">30</span>", "<span class=\"tag tag-gray\">归还</span>", "GHCK-20260903-001", "租入持有"]} },
    'EV-20260903-022': { 'row': {"fields": {"date": "2026-09-03", "customer": "环通循环包装运营（上海）有限公司", "project": "—", "mat": "WBX-1210L", "matName": "围板箱 1200×1000×970", "qty": "4", "unit": "只", "dir": "归还", "doc": "GHCK-20260903-002", "side": "租入持有", "note": "分流归还"}, "cells": ["2026-09-03", "环通循环包装运营（上海）有限公司", "—", "WBX-1210L", "围板箱 1200×1000×970", "只", "<span class=\"td-num\">4</span>", "<span class=\"tag tag-gray\">归还</span>", "GHCK-20260903-002", "租入持有"]} },
    'EV-20260915-023': { 'row': {"fields": {"date": "2026-09-15", "customer": "安吉智行物流", "project": "PRJ-2605", "mat": "XNC-ZZ-WBX", "matName": "围板箱 1200×1000×970", "qty": "100", "unit": "只", "dir": "退租", "doc": "TZRK-20260915-012", "side": "客户在租", "note": "转租物部分退回（终端在租 240 只退 100 · 余 140 只继续在租）"}, "cells": ["2026-09-15", "安吉智行物流", "PRJ-2605", "XNC-ZZ-WBX", "围板箱 1200×1000×970", "只", "<span class=\"td-num\">100</span>", "<span class=\"tag tag-gray\">退租</span>", "TZRK-20260915-012", "客户在租"]} },
  },
};