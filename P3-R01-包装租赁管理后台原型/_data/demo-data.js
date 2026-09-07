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
    version: '2026-09-07',
    desc: '全局演示数据集 · 试点范围：应付账单（财务协同）'
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

    /* ===== 预付（路凯 · 预付运营方大箱租金 9 月度 · 已付款） ===== */
    'AP-20260905-012': {
      billNo: 'AP-20260905-012',
      billType: '预付',
      status: '已付款',
      supplier: '路凯包装运营（上海）有限公司',
      project: 'PRJ-2604',
      period: '2026-09',
      amount: 30000,
      paid: 30000,
      genMode: '手动创建（预付）',
      scenario: '预付冲抵 · 运营方租金',
      refs: [
        { label: '关联租入单', no: 'RZD-20260815-005', url: '采购管理/租入单列表.html' }
      ],
      fees: [
        { src: 'RZD-20260815-005', desc: '预付运营方大箱租金 · 2026-09 月度', amount: 30000, url: '采购管理/租入单列表.html' }
      ],
      chain: [
        { role: '租入单', name: 'RZD-20260815-005', url: '采购管理/租入单列表.html' },
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
        { label: '关联采购入库', no: 'CGRK-20260828-012', url: '仓储作业/采购入库列表.html' }
      ],
      fees: [
        { src: 'CGRK-20260828-012', desc: '采购入库验收 · 采购应付', amount: 84000, url: '仓储作业/采购入库列表.html' }
      ],
      chain: [
        { role: '采购订单', name: 'PO-20260825-014', url: '采购管理/采购订单列表.html' },
        { role: '采购入库', name: 'CGRK-20260828-012', url: '仓储作业/采购入库列表.html' },
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
        { label: '关联采购入库', no: 'CGRK-20260825-011', url: '仓储作业/采购入库列表.html' }
      ],
      fees: [
        { src: 'CGRK-20260825-011', desc: '采购入库验收 · 采购应付', amount: 12700, url: '仓储作业/采购入库列表.html' }
      ],
      chain: [
        { role: '采购订单', name: 'PO-20260820-013', url: '采购管理/采购订单列表.html' },
        { role: '采购入库', name: 'CGRK-20260825-011', url: '仓储作业/采购入库列表.html' },
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
        { label: '关联采购入库', no: 'CGRK-20260820-009', url: '仓储作业/采购入库列表.html' }
      ],
      fees: [
        { src: 'CGRK-20260820-009', desc: '采购入库验收 · 采购应付', amount: 42500, url: '仓储作业/采购入库列表.html' }
      ],
      chain: [
        { role: '采购订单', name: 'PO-20260815-011', url: '采购管理/采购订单列表.html' },
        { role: '采购入库', name: 'CGRK-20260820-009', url: '仓储作业/采购入库列表.html' },
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
        { label: '关联采购入库', no: 'CGRK-20260815-007', url: '仓储作业/采购入库列表.html' }
      ],
      fees: [
        { src: 'CGRK-20260815-007', desc: '采购入库验收 · 采购应付', amount: 6300, url: '仓储作业/采购入库列表.html' }
      ],
      chain: [
        { role: '采购订单', name: 'PO-20260810-009', url: '采购管理/采购订单列表.html' },
        { role: '采购入库', name: 'CGRK-20260815-007', url: '仓储作业/采购入库列表.html' },
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
        { label: '关联采购入库', no: 'CGRK-20260812-006', url: '仓储作业/采购入库列表.html' }
      ],
      fees: [
        { src: 'CGRK-20260812-006', desc: '采购入库验收 · 采购应付', amount: 35200, url: '仓储作业/采购入库列表.html' }
      ],
      chain: [
        { role: '采购订单', name: 'PO-20260808-008', url: '采购管理/采购订单列表.html' },
        { role: '采购入库', name: 'CGRK-20260812-006', url: '仓储作业/采购入库列表.html' },
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
        { label: '关联租入单', no: 'RZD-20260815-005', url: '采购管理/租入单列表.html' },
        { label: '关联租入入库', no: 'RZRK-20260816-022', url: '仓储作业/租入入库列表.html' }
      ],
      fees: [
        { src: 'RZD-20260815-005', desc: '租入租金 · 2026-09 账期', amount: 12000, url: '采购管理/租入单列表.html' }
      ],
      chain: [
        { role: '租入单', name: 'RZD-20260815-005', url: '采购管理/租入单列表.html' },
        { role: '租入入库', name: 'RZRK-20260816-022', url: '仓储作业/租入入库列表.html' },
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
        { label: '关联租入单', no: 'RZD-20260815-003', url: '采购管理/租入单列表.html' },
        { label: '关联租入入库', no: 'RZRK-20260816-021', url: '仓储作业/租入入库列表.html' }
      ],
      fees: [
        { src: 'RZD-20260815-003', desc: '租入租金 · 2026-09 账期', amount: 36000, url: '采购管理/租入单列表.html' }
      ],
      chain: [
        { role: '租入单', name: 'RZD-20260815-003', url: '采购管理/租入单列表.html' },
        { role: '租入入库', name: 'RZRK-20260816-021', url: '仓储作业/租入入库列表.html' },
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
      billNo: 'AP-20260903-011',
      billType: '赔付应付',
      status: '未付款',
      supplier: '路凯包装运营（上海）有限公司',
      project: 'PRJ-2603',
      period: '2026-09',
      amount: 930,
      paid: 0,
      genMode: '赔偿审核通过自动生成',
      scenario: 'L4 · 多线应付（赔付线）',
      refs: [
        { label: '关联丢损赔偿单', no: 'BS-20260902-010', url: '租赁管理/丢损赔偿单.html' }
      ],
      fees: [
        { src: 'BS-20260902-010', desc: '退租丢损赔偿 · 赔付应付', amount: 930, url: '租赁管理/丢损赔偿单.html' }
      ],
      chain: [
        { role: '丢损赔偿单', name: 'BS-20260902-010', url: '租赁管理/丢损赔偿单.html' },
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
    'AR-2026-09-PRJ2601-YS': {
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
        { src: 'XSCK-20260902-015', desc: '销售费 · 箱盖 ABS 吸塑', qty: '1,500 件', price: '6.80', amount: 10200, url: '仓储作业/销售出库列表.html' }
      ],
      chain: [
        { role: '销售出库', name: 'XSCK-20260902-015', url: '仓储作业/销售出库列表.html' },
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
        { src: 'XSCK-20260901-014', desc: '销售费 · 零部件销售', qty: '160 件', price: '8.00', amount: 1280, url: '仓储作业/销售出库列表.html' }
      ],
      chain: [
        { role: '销售出库', name: 'XSCK-20260901-014', url: '仓储作业/销售出库列表.html' },
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
        { src: 'XSCK-20260826-012', desc: '销售费 · 零部件销售', qty: '605 件', price: '10.00', amount: 6050, url: '仓储作业/销售出库列表.html' }
      ],
      chain: [
        { role: '销售出库', name: 'XSCK-20260826-012', url: '仓储作业/销售出库列表.html' },
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
        { src: '组合出库单 ×26', desc: '租赁费 · 2026-08 账期（按组合出库自动汇总）', qty: '—', price: '—', amount: 486200, url: '仓储作业/组合出库列表.html' }
      ],
      chain: [
        { role: '组合出库', name: '组合出库 ×26 张', url: '仓储作业/组合出库列表.html' },
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
        { src: '组合出库单 ×26', desc: '租赁费 · 2026-08 账期（按组合出库自动汇总）', qty: '—', price: '—', amount: 358900, url: '仓储作业/组合出库列表.html' }
      ],
      chain: [
        { role: '组合出库', name: '组合出库 ×26 张', url: '仓储作业/组合出库列表.html' },
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
        { src: '组合出库单 ×26', desc: '租赁费 · 2026-08 账期（按组合出库自动汇总）', qty: '—', price: '—', amount: 241500, url: '仓储作业/组合出库列表.html' }
      ],
      chain: [
        { role: '组合出库', name: '组合出库 ×26 张', url: '仓储作业/组合出库列表.html' },
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
        { src: '组合出库单 ×26', desc: '租赁费 · 2026-07 账期（按组合出库自动汇总）', qty: '—', price: '—', amount: 442800, url: '仓储作业/组合出库列表.html' }
      ],
      chain: [
        { role: '组合出库', name: '组合出库 ×26 张', url: '仓储作业/组合出库列表.html' },
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
      billNo: 'BS-20260828-004',
      billType: '丢损赔偿',
      status: '未开票',
      customer: '一汽解放汽车有限公司',
      project: 'PRJ-2601',
      period: '2026-08',
      amount: 3690,
      verified: 0,
      genMode: '赔偿联动',
      genDate: '2026-08-28',
      feeType: '丢损赔偿（退租联动转应收）',
      scenario: 'S5 · 丢损赔偿转应收',
      fees: [
        { src: 'BS-20260828-004', desc: '退租丢损赔偿 · 客户承担', qty: '—', price: '—', amount: 3690, url: '租赁管理/丢损赔偿单.html' }
      ],
      chain: [
        { role: '丢损赔偿单', name: 'BS-20260828-004', url: '租赁管理/丢损赔偿单.html' },
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
        { src: '组合出库单 ×26', desc: '租赁费 · 2026-07 账期（按组合出库自动汇总）', qty: '—', price: '—', amount: 366200, url: '仓储作业/组合出库列表.html' }
      ],
      chain: [
        { role: '组合出库', name: '组合出库 ×26 张', url: '仓储作业/组合出库列表.html' },
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
        { src: '组合出库单 ×26', desc: '租赁费 · 2026-06 账期（按组合出库自动汇总）', qty: '—', price: '—', amount: 358900, url: '仓储作业/组合出库列表.html' }
      ],
      chain: [
        { role: '组合出库', name: '组合出库 ×26 张', url: '仓储作业/组合出库列表.html' },
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
  }
};
