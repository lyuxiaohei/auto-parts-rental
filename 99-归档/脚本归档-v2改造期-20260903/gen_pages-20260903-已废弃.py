# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃·禁止运行（内嵌12页旧快照，重跑覆盖手工修改）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""步骤5：12 个 v2 新页面的页面配置与生成主程序"""
import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfw import *

PAGES = []

# ============================================================
# 5.1 采购管理/采购订单列表.html
# ============================================================
cg_modal = modal('createModal', '新建采购订单',
    m_select('供应商', '苏州联恒五金制品有限公司', req=True) +
    m_select('物料类型', '零部件', req=True) +
    m_input('关联销售订单号', ph='选填，先销后采时自动带出') +
    m_input('预计到货日期', '2026-09-15') +
    m_table('采购明细', ['物料编码', '物料名称', '规格', '单位', '数量', '单价(元)', '金额(元)'], [
        ['<input value="LJ-A100">', '<input value="锁扣组件">', '<input value="不锈钢 304">', '<input value="件">', '<input value="5,000">', '<input value="1.28">', '<input class="auto" value="6,400.00" readonly>'],
        ['<input value="LJ-B200">', '<input value="铰链">', '<input value="锌合金 65mm">', '<input value="件">', '<input value="2,000">', '<input value="1.65">', '<input class="auto" value="3,300.00" readonly>'],
    ]) +
    m_input('备注', ph='选填'))

cg_rows = [
    [CB, '<span class="lk">PO-20260902-018</span>', '苏州联恒五金制品有限公司', tag('零部件', 'blue'), '锁扣组件×5,000 / 铰链×2,000', num('7,000'), num('12,700.00'), 'CNY', '2026-09-10', '<span class="lk">SO-20260831-0042</span>', st('待审核'), ops(('编辑', None, 'createModal'), ('审核', None, None), ('关闭', None, None))],
    [CB, '<span class="lk">PO-20260901-017</span>', '宁波华塑包装制品有限公司', tag('器具', 'green'), '围板箱 1200×1000×970×300', num('300'), num('84,000.00'), 'CNY', '2026-09-15', '—', st('待审核'), ops(('编辑', None, 'createModal'), ('审核', None, None), ('关闭', None, None))],
    [CB, '<span class="lk">PO-20260830-016</span>', '常州正大塑料托盘厂', tag('器具', 'green'), '塑料托盘 1200×1000×500', num('500'), num('42,500.00'), 'CNY', '2026-09-08', '—', st('已审核'), ops(('生成入库单', '../仓储作业/采购入库列表.html', None), ('关闭', None, None))],
    [CB, '<span class="lk">PO-20260828-015</span>', '苏州联恒五金制品有限公司', tag('零部件', 'blue'), '箱盖 ABS 吸塑×2,000', num('2,000'), num('6,300.00'), 'CNY', '2026-09-05', '<span class="lk">SO-20260827-0039</span>', st('已审核'), ops(('生成入库单', '../仓储作业/采购入库列表.html', None), ('关闭', None, None))],
    [CB, '<span class="lk">PO-20260825-014</span>', '宁波华塑包装制品有限公司', tag('器具', 'green'), '料箱 600×400×340×800', num('800'), num('35,200.00'), 'CNY', '2026-09-02', '—', st('已完成'), ops(('详情', None, None), ('入库记录', '../仓储作业/采购入库列表.html', None))],
    [CB, '<span class="lk">PO-20260820-013</span>', '常州正大塑料托盘厂', tag('器具', 'green'), '木托盘 1200×1000×400', num('400'), num('19,600.00'), 'CNY', '2026-08-30', '—', st('已完成'), ops(('详情', None, None), ('入库记录', '../仓储作业/采购入库列表.html', None))],
    [CB, '<span class="lk">PO-20260815-012</span>', '苏州联恒五金制品有限公司', tag('零部件', 'blue'), '内衬 EPE 珍珠棉×3,000', num('3,000'), num('4,500.00'), 'CNY', '2026-08-25', '—', st('已关闭'), ops(('详情', None, None))],
]
PAGES.append(dict(
    rel='采购管理/采购订单列表.html', title='采购订单', selected='采购订单',
    tab_names=['采购订单', '采购入库', '应付账单'],
    content=filter_card([fi_input('采购订单号'), fi_sel('供应商'), fi_sel('物料类型')],
                        [fi_sel('订单状态'), fi_range('下单日期'), fi_sel('所属项目')]) +
            list_card('采购订单', '<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新建采购订单</button>',
                      stabs_bar([('全部', 18), ('待审核', 3), ('已审核', 6), ('已完成', 7), ('已关闭', 2)]),
                      table(['', '采购订单号', '供应商名称', '物料类型', '采购明细摘要', '数量', '金额(元)', '币种', '预计到货日期', '关联销售订单号', '订单状态', '操作'], cg_rows),
                      pager(18)),
    modals=cg_modal))

# ============================================================
# 5.2 销售管理/销售订单列表.html
# ============================================================
xs_modal = modal('createModal', '新建销售订单',
    m_select('客户', '一汽解放汽车有限公司', req=True) +
    m_select('所属项目', 'PRJ-2601 一汽解放·长春基地', req=True) +
    m_radio('下单方式', ['客户自助下单', '项目经理代下单'], checked=1) +
    m_input('要求交货日期', '2026-09-12') +
    m_table('订单明细', ['物料编码', '物料名称', '规格', '单位', '数量', '单价(元)', '金额(元)'], [
        ['<input value="LJ-A100">', '<input value="锁扣组件">', '<input value="不锈钢 304">', '<input value="件">', '<input value="3,000">', '<input value="1.60">', '<input class="auto" value="4,800.00" readonly>'],
        ['<input value="LJ-D400">', '<input value="箱盖">', '<input value="ABS 吸塑">', '<input value="件">', '<input value="1,500">', '<input value="3.60">', '<input class="auto" value="5,400.00" readonly>'],
    ]) +
    m_input('备注', ph='选填'))

xs_rows = [
    [CB, '<span class="lk">SO-20260902-0046</span>', '一汽解放汽车有限公司', 'PRJ-2601', '锁扣组件×3,000', num('3,000'), num('4,800.00'), tag('项目经理代下', 'blue'), '王强', '2026-09-02 10:24', '<span class="lk">PO-20260902-018</span>', st('待审核'), ops(('编辑', None, 'createModal'), ('审核', None, None), ('关闭', None, None))],
    [CB, '<span class="lk">SO-20260901-0045</span>', '上汽大众汽车有限公司宁波分公司', 'PRJ-2602', '铰链×1,200 / 箱盖×800', num('2,000'), num('6,050.00'), tag('客户自助', 'gray'), '何静', '2026-09-01 16:40', '—', st('待审核'), ops(('编辑', None, 'createModal'), ('审核', None, None), ('关闭', None, None))],
    [CB, '<span class="lk">SO-20260831-0044</span>', '小鹏汽车科技有限公司', 'PRJ-2603', '内衬 EPE 珍珠棉×5,000', num('5,000'), num('9,000.00'), tag('项目经理代下', 'blue'), '陈金', '2026-08-31 11:05', '—', st('已审核'), ops(('发货', '../仓储作业/销售出库列表.html', None), ('关闭', None, None))],
    [CB, '<span class="lk">SO-20260830-0043</span>', '一汽解放汽车有限公司', 'PRJ-2601', '箱盖 ABS 吸塑×1,500', num('1,500'), num('5,400.00'), tag('客户自助', 'gray'), '袁明', '2026-08-30 09:18', '—', st('待发货'), ops(('发货', '../仓储作业/销售出库列表.html', None), ('关闭', None, None))],
    [CB, '<span class="lk">SO-20260828-0041</span>', '东风本田汽车有限公司', 'PRJ-2604', '锁扣组件×800', num('800'), num('1,280.00'), tag('项目经理代下', 'blue'), '王强', '2026-08-28 15:52', '<span class="lk">PO-20260828-015</span>', st('已完成'), ops(('详情', None, None))],
    [CB, '<span class="lk">SO-20260827-0039</span>', '一汽解放汽车有限公司', 'PRJ-2601', '箱盖 ABS 吸塑×2,000', num('2,000'), num('7,200.00'), tag('客户自助', 'gray'), '袁明', '2026-08-27 14:03', '<span class="lk">PO-20260828-015</span>', st('已完成'), ops(('详情', None, None))],
    [CB, '<span class="lk">SO-20260820-0036</span>', '上汽大众汽车有限公司宁波分公司', 'PRJ-2602', '铰链×600', num('600'), num('1,890.00'), tag('项目经理代下', 'blue'), '王强', '2026-08-20 10:44', '—', st('已关闭'), ops(('详情', None, None))],
]
PAGES.append(dict(
    rel='销售管理/销售订单列表.html', title='销售订单', selected='销售订单',
    tab_names=['销售订单', '销售出库', '订单审核'],
    content=filter_card([fi_input('销售订单号'), fi_sel('客户名称'), fi_sel('所属项目')],
                        [fi_sel('订单状态'), fi_range('下单日期'), fi_sel('下单方式')]) +
            list_card('销售订单', '<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新建销售订单</button>',
                      stabs_bar([('全部', 26), ('待审核', 4), ('已审核', 8), ('待发货', 5), ('已完成', 7), ('已关闭', 2)]),
                      table(['', '销售订单号', '客户名称', '所属项目', '订单明细摘要', '数量', '金额(元)', '是否代下单', '下单人', '下单时间', '关联采购订单号', '订单状态', '操作'], xs_rows),
                      pager(26)),
    modals=xs_modal))

# ============================================================
# 5.3 仓储作业/销售出库列表.html
# ============================================================
xck_modal = modal('createModal', '新增销售出库单',
    m_select('关联销售订单', 'SO-20260831-0044 小鹏汽车科技有限公司', req=True) +
    m_select('出库仓库', '原料区 RA', req=True) +
    m_input('出库日期', '2026-09-03') +
    m_table('出库明细', ['物料编码', '物料名称', '单位', '出库数量', '备注'], [
        ['<input value="LJ-F600">', '<input value="内衬 EPE 珍珠棉">', '<input value="件">', '<input value="5,000">', '<input value="">'],
    ]) +
    m_input('备注', ph='选填'))

xck_rows = [
    [CB, '<span class="lk">XSCK-20260902-015</span>', '<span class="lk">SO-20260830-0043</span>', '一汽解放汽车有限公司', 'PRJ-2601', '箱盖 ABS 吸塑×1,500', num('1,500'), '原料区 RA', '2026-09-02', st('待审核'), ops(('审核', None, None), ('详情', None, None))],
    [CB, '<span class="lk">XSCK-20260901-014</span>', '<span class="lk">SO-20260828-0041</span>', '东风本田汽车有限公司', 'PRJ-2604', '锁扣组件×800', num('800'), '原料区 RA', '2026-09-01', st('已完成'), ops(('详情', None, None))],
    [CB, '<span class="lk">XSCK-20260829-013</span>', '<span class="lk">SO-20260827-0039</span>', '一汽解放汽车有限公司', 'PRJ-2601', '箱盖 ABS 吸塑×2,000', num('2,000'), '原料区 RA', '2026-08-29', st('已完成'), ops(('详情', None, None))],
    [CB, '<span class="lk">XSCK-20260826-012</span>', '<span class="lk">SO-20260822-0038</span>', '上汽大众汽车有限公司宁波分公司', 'PRJ-2602', '铰链×900 / 内衬×400', num('1,300'), '原料区 RA', '2026-08-26', st('已完成'), ops(('详情', None, None))],
    [CB, '<span class="lk">XSCK-20260822-011</span>', '<span class="lk">SO-20260819-0035</span>', '小鹏汽车科技有限公司', 'PRJ-2603', '锁扣组件×1,200', num('1,200'), '原料区 RA', '2026-08-22', st('已完成'), ops(('详情', None, None))],
    [CB, '<span class="lk">XSCK-20260818-010</span>', '<span class="lk">SO-20260815-0032</span>', '一汽解放汽车有限公司', 'PRJ-2601', '箱盖 ABS 吸塑×600', num('600'), '原料区 RA', '2026-08-18', st('已完成'), ops(('详情', None, None))],
]
PAGES.append(dict(
    rel='仓储作业/销售出库列表.html', title='销售出库', selected='销售出库',
    tab_names=['销售出库', '销售订单', '组合出库'],
    content=filter_card([fi_input('出库单号'), fi_input('关联销售订单号'), fi_sel('客户名称')],
                        [fi_sel('状态'), fi_range('出库日期'), fi_sel('所属项目')]) +
            list_card('销售出库单', '<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新增出库单</button>',
                      stabs_bar([('全部', 42), ('待审核', 5), ('已完成', 37)]),
                      table(['', '出库单号', '关联销售订单号', '客户名称', '所属项目', '出库明细摘要', '数量', '出库仓库', '出库日期', '状态', '操作'], xck_rows),
                      pager(42)),
    modals=xck_modal))

# ============================================================
# 5.4 仓储作业/退租入库列表.html
# ============================================================
tzrk_rows = [
    [CB, '<span class="lk">TZRK-20260902-008</span>', '<span class="lk">TZSQ-20260901-006</span>', '一汽解放汽车有限公司', 'PRJ-2601', 'ZH-2601-A 驾驶室围板箱整箱套件', num('60 套'), '围板×120 / 箱体×60 / 锁扣组件×240', '成品区 RB', '2026-09-02', tag('缺损', 'orange'), st('待审核'), ops(('审核', None, None), ('生成赔偿单', '../包装管理/丢损赔偿单.html', None), ('创建拆卸单', '../仓储作业/拆卸管理列表.html', None))],
    [CB, '<span class="lk">TZRK-20260901-007</span>', '<span class="lk">TZSQ-20260830-005</span>', '上汽大众汽车有限公司宁波分公司', 'PRJ-2602', 'ZH-2602-B 冲压件料箱组套', num('45 套'), '料箱×45 / 隔板×90', '成品区 RB', '2026-09-01', tag('完好', 'green'), st('已入库'), ops(('详情', None, None), ('创建拆卸单', '../仓储作业/拆卸管理列表.html', None))],
    [CB, '<span class="lk">TZRK-20260831-006</span>', '<span class="lk">TZSQ-20260829-004</span>', '小鹏汽车科技有限公司', 'PRJ-2603', 'ZH-2603-C 电池托盘护角套件', num('20 套'), '托盘×20 / 护角×80', '成品区 RB', '2026-08-31', tag('丢失', 'red'), st('已入库'), ops(('详情', None, None), ('生成赔偿单', '../包装管理/丢损赔偿单.html', None))],
    [CB, '<span class="lk">TZRK-20260828-005</span>', '<span class="lk">TZSQ-20260826-003</span>', '一汽解放汽车有限公司', 'PRJ-2601', 'BTC-6040 料箱', num('200 只'), '—（散件直接入库）', '成品区 RB', '2026-08-28', tag('完好', 'green'), st('已入库'), ops(('详情', None, None))],
    [CB, '<span class="lk">TZRK-20260825-004</span>', '<span class="lk">TZSQ-20260823-002</span>', '上汽大众汽车有限公司宁波分公司', 'PRJ-2602', 'PLT-1210P 塑料托盘', num('150 块'), '—（散件直接入库）', '成品区 RB', '2026-08-25', tag('完好', 'green'), st('已入库'), ops(('详情', None, None))],
    [CB, '<span class="lk">TZRK-20260820-003</span>', '<span class="lk">TZSQ-20260818-001</span>', '一汽解放汽车有限公司', 'PRJ-2601', 'ZH-2601-A 驾驶室围板箱整箱套件', num('30 套'), '围板×60 / 箱体×30 / 锁扣组件×120', '成品区 RB', '2026-08-20', tag('缺损', 'orange'), st('已入库'), ops(('详情', None, None), ('生成赔偿单', '../包装管理/丢损赔偿单.html', None), ('创建拆卸单', '../仓储作业/拆卸管理列表.html', None))],
]
PAGES.append(dict(
    rel='仓储作业/退租入库列表.html', title='退租入库', selected='退租入库',
    tab_names=['退租入库', '退租申请', '拆卸管理'],
    content=filter_card([fi_input('退租入库单号'), fi_input('关联退租申请单号'), fi_sel('客户名称')],
                        [fi_sel('验收结果'), fi_range('入库日期'), fi_sel('所属项目')]) +
            list_card('退租入库单', '<button class="btn btn-default btn-sm">批量导出</button>',
                      stabs_bar([('全部', 31), ('待审核', 4), ('已入库', 27)]),
                      table(['', '退租入库单号', '关联退租申请单号', '客户名称', '所属项目', '退租器具名称', '退租数量', '按BOM拆解后散件明细摘要', '入库仓库', '入库日期', '验收结果', '状态', '操作'], tzrk_rows),
                      pager(31)) +
            '<div class="pn-hint" style="padding:0 4px;">退租入库单由包装管理模块的「退租申请」审核通过后自动生成，按 BOM 配方将组合单元拆回散件入库；本页面不支持手工新建。</div>',
    modals=''))

# ============================================================
# 5.5 仓储作业/其他入库列表.html
# ============================================================
qtrk_modal = modal('createModal', '新增其他入库单',
    m_radio('入库类型', ['盘盈', '退货', '其他'], checked=0) +
    m_select('物料', 'LJ-B200 铰链 锌合金 65mm', req=True) +
    m_input('数量', '120') +
    m_select('入库仓库', '原料区 RA', req=True) +
    m_input('入库日期', '2026-09-03') +
    m_input('备注', ph='选填'), wide=False)

qtrk_rows = [
    [CB, '<span class="lk">QTRK-20260901-003</span>', tag('盘盈', 'blue'), 'LJ-B200 铰链 锌合金 65mm', num('120 件'), '原料区 RA', '2026-09-01', st('待审核'), ops(('审核', None, None), ('详情', None, None))],
    [CB, '<span class="lk">QTRK-20260828-002</span>', tag('退货', 'orange'), 'LJ-D400 箱盖 ABS 吸塑', num('300 件'), '原料区 RA', '2026-08-28', st('已入库'), ops(('详情', None, None))],
    [CB, '<span class="lk">QTRK-20260820-001</span>', tag('其他', 'gray'), 'WBX-1210M 围板箱 1200×1000×590', num('15 只'), '成品区 RB', '2026-08-20', st('已入库'), ops(('详情', None, None))],
]
PAGES.append(dict(
    rel='仓储作业/其他入库列表.html', title='其他入库', selected='其他入库',
    tab_names=['其他入库', '采购入库', '退租入库'],
    content=filter_card([fi_input('单号'), fi_sel('入库类型'), fi_input('物料名称')],
                        [fi_sel('状态'), fi_range('入库日期'), fi_sel('入库仓库')]) +
            list_card('其他入库单', '<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新增入库单</button>',
                      stabs_bar([('全部', 12), ('待审核', 2), ('已入库', 10)]),
                      table(['', '单号', '入库类型', '物料名称', '数量', '入库仓库', '入库日期', '状态', '操作'], qtrk_rows),
                      pager(12)),
    modals=qtrk_modal))

# ============================================================
# 5.6 仓储作业/其他出库列表.html
# ============================================================
qtck_modal = modal('createModal', '新增其他出库单',
    m_radio('出库类型', ['报废', '盘亏', '其他'], checked=0) +
    m_select('物料', 'WBX-1210L(旧) 围板箱 旧箱体批次', req=True) +
    m_input('数量', '35') +
    m_select('出库仓库', '成品区 RB', req=True) +
    m_input('出库日期', '2026-09-03') +
    m_input('备注', ph='选填'), wide=False)

qtck_rows = [
    [CB, '<span class="lk">QTCK-20260901-004</span>', tag('报废', 'red'), 'WBX-1210L(旧) 围板箱 旧箱体批次', num('35 只'), '成品区 RB', '2026-09-01', st('待审核'), ops(('审核', None, None), ('详情', None, None))],
    [CB, '<span class="lk">QTCK-20260829-003</span>', tag('盘亏', 'orange'), 'LJ-F600 内衬 EPE 珍珠棉', num('80 件'), '原料区 RA', '2026-08-29', st('已完成'), ops(('详情', None, None))],
    [CB, '<span class="lk">QTCK-20260825-002</span>', tag('报废', 'red'), 'PLT-1210W 木托盘 1200×1000', num('22 块'), '成品区 RB', '2026-08-25', st('已完成'), ops(('详情', None, None))],
    [CB, '<span class="lk">QTCK-20260815-001</span>', tag('其他', 'gray'), 'LJ-A100 锁扣组件 不锈钢 304', num('50 件'), '原料区 RA', '2026-08-15', st('已完成'), ops(('详情', None, None))],
]
PAGES.append(dict(
    rel='仓储作业/其他出库列表.html', title='其他出库', selected='其他出库',
    tab_names=['其他出库', '销售出库', '组合出库'],
    content=filter_card([fi_input('单号'), fi_sel('出库类型'), fi_input('物料名称')],
                        [fi_sel('状态'), fi_range('出库日期'), fi_sel('出库仓库')]) +
            list_card('其他出库单', '<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新增出库单</button>',
                      stabs_bar([('全部', 9), ('待审核', 2), ('已完成', 7)]),
                      table(['', '单号', '出库类型', '物料名称', '数量', '出库仓库', '出库日期', '状态', '操作'], qtck_rows),
                      pager(9)),
    modals=qtck_modal))

# ============================================================
# 5.7 仓储作业/拆卸管理列表.html
# ============================================================
cx_modal = modal('createModal', '新建拆卸单',
    m_select('组合单元', 'ZH-2601-A 驾驶室围板箱整箱套件', req=True) +
    m_input('拆卸数量', '50', req=True) +
    m_select('拆卸仓库', '成品区 RB', req=True) +
    m_hint('按 BOM V2.1 自动拆出以下散件，确认后散件库存增加、组合件库存减少：') +
    m_table('拆出散件明细（按 BOM 自动带出）', ['散件编码', '散件名称', '单位', '单套用量', '拆出数量'], [
        ['<span class="auto-cell">LJ-C300</span>', '<span class="auto-cell">围板 HDPE 波纹板</span>', '<span class="auto-cell">件</span>', '<span class="auto-cell">2</span>', '<input class="auto" value="100" readonly>'],
        ['<span class="auto-cell">LJ-E500</span>', '<span class="auto-cell">箱体 PP 中空板</span>', '<span class="auto-cell">件</span>', '<span class="auto-cell">1</span>', '<input class="auto" value="50" readonly>'],
        ['<span class="auto-cell">LJ-A100</span>', '<span class="auto-cell">锁扣组件 不锈钢 304</span>', '<span class="auto-cell">件</span>', '<span class="auto-cell">4</span>', '<input class="auto" value="200" readonly>'],
    ]) +
    m_input('备注', ph='选填'))

cx_rows = [
    [CB, '<span class="lk">CX-20260902-006</span>', '<span class="lk">ZH-2601-A</span>', '驾驶室围板箱整箱套件', '围板×100 / 箱体×50 / 锁扣组件×200', num('50 套'), '成品区 RB', '2026-09-02', st('待审核'), ops(('审核', None, None), ('详情', None, None))],
    [CB, '<span class="lk">CX-20260830-005</span>', '<span class="lk">ZH-2602-B</span>', '冲压件料箱组套', '料箱×40 / 隔板×80', num('40 套'), '成品区 RB', '2026-08-30', st('已完成'), ops(('详情', None, None))],
    [CB, '<span class="lk">CX-20260826-004</span>', '<span class="lk">ZH-2603-C</span>', '电池托盘护角套件', '托盘×30 / 护角×120', num('30 套'), '成品区 RB', '2026-08-26', st('已完成'), ops(('详情', None, None))],
    [CB, '<span class="lk">CX-20260818-003</span>', '<span class="lk">ZH-2601-A</span>', '驾驶室围板箱整箱套件', '围板×60 / 箱体×30 / 锁扣组件×120', num('30 套'), '成品区 RB', '2026-08-18', st('已完成'), ops(('详情', None, None))],
]
PAGES.append(dict(
    rel='仓储作业/拆卸管理列表.html', title='拆卸管理', selected='拆卸管理',
    tab_names=['拆卸管理', '组装', '退租入库'],
    content=filter_card([fi_input('拆卸单号'), fi_input('组合单元编码'), fi_sel('拆卸仓库')],
                        [fi_sel('状态'), fi_range('拆卸日期')]) +
            list_card('拆卸单', '<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新建拆卸单</button>',
                      stabs_bar([('全部', 15), ('待审核', 3), ('已完成', 12)]),
                      table(['', '拆卸单号', '组合单元编码', '组合单元名称', '按BOM拆出散件明细摘要', '拆卸数量', '拆卸仓库', '拆卸日期', '状态', '操作'], cx_rows),
                      pager(15)),
    modals=cx_modal))

# ============================================================
# 5.8 仓储作业/库存调拨列表.html
# ============================================================
db_modal = modal('createModal', '新建调拨单',
    m_select('物料', 'LJ-A100 锁扣组件 不锈钢 304', req=True) +
    m_input('调拨数量', '1,000', req=True) +
    m_select('调出仓库', '原料区 RA', req=True) +
    m_select('调入仓库', '成品区 RB', req=True) +
    m_input('调拨日期', '2026-09-03') +
    m_input('备注', ph='选填'), wide=False)

db_rows = [
    [CB, '<span class="lk">DB-20260901-003</span>', 'LJ-A100 锁扣组件 不锈钢 304', num('1,000 件'), '原料区 RA', '成品区 RB', '2026-09-01', st('待审核'), ops(('审核', None, None), ('详情', None, None))],
    [CB, '<span class="lk">DB-20260826-002</span>', 'WBX-1210L 围板箱 1200×1000×970', num('200 只'), '成品区 RB', '外协周转区 RC', '2026-08-26', st('已完成'), ops(('详情', None, None))],
    [CB, '<span class="lk">DB-20260812-001</span>', 'PLT-1210P 塑料托盘 1200×1000', num('300 块'), '成品区 RB', '原料区 RA', '2026-08-12', st('已完成'), ops(('详情', None, None))],
]
PAGES.append(dict(
    rel='仓储作业/库存调拨列表.html', title='库存调拨', selected='库存调拨',
    tab_names=['库存调拨', '库存查询', '库存盘点'],
    content=filter_card([fi_input('调拨单号'), fi_input('物料名称'), fi_sel('调出仓库')],
                        [fi_sel('调入仓库'), fi_range('调拨日期'), fi_sel('状态')]) +
            list_card('库存调拨单', '<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新建调拨单</button>',
                      stabs_bar([('全部', 8), ('待审核', 1), ('已完成', 7)]),
                      table(['', '调拨单号', '物料名称', '数量', '调出仓库', '调入仓库', '调拨日期', '状态', '操作'], db_rows),
                      pager(8)) +
            '<div class="pn-hint" style="padding:0 4px;">第一期仅支持同仓群内的库位调拨，不做调拨在途管理；调拨审核通过后即时完成库存转移。</div>',
    modals=db_modal))

# ============================================================
# 5.9 包装管理/租赁单列表.html
# ============================================================
zl_modal = modal('createModal', '新建租赁单',
    m_select('客户', '一汽解放汽车有限公司', req=True) +
    m_select('所属项目', 'PRJ-2601 一汽解放·长春基地', req=True) +
    m_input('起租日期', '2026-09-05', req=True) +
    m_input('约定归还日期', '2026-12-05', req=True) +
    m_input('押金(元)', '50,000.00') +
    m_table('租赁器具明细', ['器具编码', '器具名称', '类型', '单位', '数量', '日租金(元)'], [
        ['<input value="ZH-2601-A">', '<input value="驾驶室围板箱整箱套件">', '<input value="组合单元">', '<input value="套">', '<input value="180">', '<input value="2.40">'],
        ['<input value="PLT-1210P">', '<input value="塑料托盘 1200×1000">', '<input value="散件">', '<input value="块">', '<input value="180">', '<input value="0.15">'],
    ]) +
    m_input('备注', ph='选填'))

zl_rows = [
    [CB, '<span class="lk">ZL-20260901-032</span>', '一汽解放汽车有限公司', 'PRJ-2601', 'ZH-2601-A 驾驶室围板箱整箱套件', num('180 套'), '2026-09-05', '2026-12-05', num('91'), st('待审核'), ops(('编辑', None, 'createModal'), ('审核', None, None), ('关闭', None, None))],
    [CB, '<span class="lk">ZL-20260828-031</span>', '上汽大众汽车有限公司宁波分公司', 'PRJ-2602', 'ZH-2602-B 冲压件料箱组套', num('120 套'), '2026-09-01', '2026-11-30', num('90'), st('已审核'), ops(('详情', None, None), ('关闭', None, None))],
    [CB, '<span class="lk">ZL-20260815-028</span>', '一汽解放汽车有限公司', 'PRJ-2601', 'WBX-1210L 围板箱 1200×1000×970', num('300 只'), '2026-08-20', '2026-11-20', num('92'), st('在租'), ops(('详情', None, None), ('创建退租申请', '../包装管理/退租申请列表.html', None))],
    [CB, '<span class="lk">ZL-20260720-022</span>', '小鹏汽车科技有限公司', 'PRJ-2603', 'ZH-2603-C 电池托盘护角套件', num('60 套'), '2026-07-25', '2026-10-25', num('92'), st('在租'), ops(('详情', None, None), ('创建退租申请', '../包装管理/退租申请列表.html', None))],
    [CB, '<span class="lk">ZL-20260610-015</span>', '一汽解放汽车有限公司', 'PRJ-2601', 'BTC-6040 料箱 600×400×340', num('500 只'), '2026-06-15', '2026-09-15', num('92'), st('在租'), ops(('详情', None, None), ('创建退租申请', '../包装管理/退租申请列表.html', None))],
    [CB, '<span class="lk">ZL-20260301-006</span>', '上汽大众汽车有限公司宁波分公司', 'PRJ-2602', 'PLT-1210P 塑料托盘 1200×1000', num('400 块'), '2026-03-05', '2026-06-05', num('92'), st('已退租'), ops(('详情', None, None))],
    [CB, '<span class="lk">ZL-20260115-002</span>', '东风本田汽车有限公司', 'PRJ-2604', 'WBX-1210M 围板箱 1200×1000×590', num('150 只'), '2026-01-20', '2026-04-20', num('90'), st('已关闭'), ops(('详情', None, None))],
]
PAGES.append(dict(
    rel='包装管理/租赁单列表.html', title='租赁单', selected='租赁单',
    tab_names=['租赁单', '退租申请', '在租台账'],
    content=filter_card([fi_input('租赁单号'), fi_sel('客户名称'), fi_sel('所属项目')],
                        [fi_sel('状态'), fi_range('起租日期')]) +
            list_card('租赁单', '<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新建租赁单</button>',
                      stabs_bar([('全部', 56), ('待审核', 3), ('已审核', 8), ('在租', 40), ('已退租', 4), ('已关闭', 1)]),
                      table(['', '租赁单号', '客户名称', '所属项目', '租赁器具', '数量', '起租日期', '约定归还日期', '租赁天数', '状态', '操作'], zl_rows),
                      pager(56)),
    modals=zl_modal))

# ============================================================
# 5.10 包装管理/退租申请列表.html
# ============================================================
tz_modal = modal('createModal', '新建退租申请',
    m_select('客户', '一汽解放汽车有限公司', req=True) +
    m_select('所属项目', 'PRJ-2601 一汽解放·长春基地', req=True) +
    m_select('关联租赁单', 'ZL-20260815-028（在租 · 围板箱×300）', req=True) +
    m_input('申请日期', '2026-09-03') +
    m_input('预计入库日期', '2026-09-06') +
    m_table('退租器具明细', ['器具编码', '器具名称', '单位', '退租数量', '备注'], [
        ['<input value="WBX-1210L">', '<input value="围板箱 1200×1000×970">', '<input value="只">', '<input value="100">', '<input value="">'],
    ]) +
    m_input('备注', ph='选填'))

tz_rows = [
    [CB, '<span class="lk">TZSQ-20260902-007</span>', '<span class="lk">ZL-20260815-028</span>', '一汽解放汽车有限公司', 'PRJ-2601', 'WBX-1210L 围板箱', num('100 只'), '2026-09-02', '2026-09-05', '—', st('待审核'), ops(('审核', None, None), ('驳回', None, None))],
    [CB, '<span class="lk">TZSQ-20260901-006</span>', '<span class="lk">ZL-20260610-015</span>', '一汽解放汽车有限公司', 'PRJ-2601', 'ZH-2601-A 驾驶室围板箱整箱套件', num('60 套'), '2026-09-01', '2026-09-03', '—', st('已审核'), ops(('查看入库单', '../仓储作业/退租入库列表.html', None))],
    [CB, '<span class="lk">TZSQ-20260830-005</span>', '<span class="lk">ZL-20260301-006</span>', '上汽大众汽车有限公司宁波分公司', 'PRJ-2602', 'ZH-2602-B 冲压件料箱组套', num('45 套'), '2026-08-30', '2026-09-01', tag('完好', 'green'), st('待入库'), ops(('查看入库单', '../仓储作业/退租入库列表.html', None))],
    [CB, '<span class="lk">TZSQ-20260829-004</span>', '<span class="lk">ZL-20260720-022</span>', '小鹏汽车科技有限公司', 'PRJ-2603', 'ZH-2603-C 电池托盘护角套件', num('20 套'), '2026-08-29', '2026-08-31', tag('丢失', 'red'), st('已入库'), ops(('查看入库单', '../仓储作业/退租入库列表.html', None))],
    [CB, '<span class="lk">TZSQ-20260826-003</span>', '<span class="lk">ZL-20260610-015</span>', '一汽解放汽车有限公司', 'PRJ-2601', 'BTC-6040 料箱', num('200 只'), '2026-08-26', '2026-08-28', tag('完好', 'green'), st('已入库'), ops(('查看入库单', '../仓储作业/退租入库列表.html', None))],
    [CB, '<span class="lk">TZSQ-20260823-002</span>', '<span class="lk">ZL-20260301-006</span>', '上汽大众汽车有限公司宁波分公司', 'PRJ-2602', 'PLT-1210P 塑料托盘', num('150 块'), '2026-08-23', '2026-08-25', tag('完好', 'green'), st('已入库'), ops(('查看入库单', '../仓储作业/退租入库列表.html', None))],
    [CB, '<span class="lk">TZSQ-20260818-001</span>', '<span class="lk">ZL-20260815-028</span>', '一汽解放汽车有限公司', 'PRJ-2601', 'ZH-2601-A 驾驶室围板箱整箱套件', num('30 套'), '2026-08-18', '2026-08-20', tag('缺损', 'orange'), st('已入库'), ops(('查看入库单', '../仓储作业/退租入库列表.html', None))],
]
PAGES.append(dict(
    rel='包装管理/退租申请列表.html', title='退租申请', selected='退租申请',
    tab_names=['退租申请', '租赁单', '退租入库'],
    content=filter_card([fi_input('退租申请单号'), fi_input('关联租赁单号'), fi_sel('客户名称')],
                        [fi_sel('状态'), fi_range('申请日期'), fi_sel('所属项目')]) +
            list_card('退租申请', '<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新建退租申请</button>',
                      stabs_bar([('全部', 24), ('待审核', 3), ('已审核', 5), ('待入库', 4), ('已入库', 12)]),
                      table(['', '退租申请单号', '关联租赁单号', '客户名称', '所属项目', '退租器具', '数量', '申请日期', '预计入库日期', '验收结果', '状态', '操作'], tz_rows),
                      pager(24)) +
            '<div class="pn-hint" style="padding:0 4px;">退租申请审核通过后自动生成「退租入库单」，由仓储作业模块完成验收与按 BOM 拆解入库。</div>',
    modals=tz_modal))

# ============================================================
# 5.12 财务协同/应付账单.html
# ============================================================
ap_modal = modal('createModal', '新建应付账单',
    m_select('供应商', '宁波华塑包装制品有限公司', req=True) +
    m_input('关联采购订单号', 'PO-20260901-017') +
    m_input('账单金额(元)', '84,000.00', req=True) +
    m_input('账单日期', '2026-09-03') +
    m_input('到期日', '2026-10-03') +
    m_input('备注', ph='选填'), wide=False)

ap_rows = [
    [CB, '<span class="lk">AP-20260901-008</span>', '宁波华塑包装制品有限公司', '<span class="lk">PO-20260825-014</span>', '<span class="lk">CGRK-20260828-012</span>', num('84,000.00'), num('0.00'), num('84,000.00', danger=True), '2026-09-01', '2026-09-30', st('未付款'), ops(('付款', '../财务协同/付款登记.html', None), ('详情', None, None))],
    [CB, '<span class="lk">AP-20260830-007</span>', '苏州联恒五金制品有限公司', '<span class="lk">PO-20260820-013</span>', '<span class="lk">CGRK-20260825-011</span>', num('12,700.00'), num('6,000.00'), num('6,700.00'), '2026-08-30', '2026-09-29', st('部分付款'), ops(('付款', '../财务协同/付款登记.html', None), ('详情', None, None))],
    [CB, '<span class="lk">AP-20260828-006</span>', '常州正大塑料托盘厂', '<span class="lk">PO-20260815-011</span>', '<span class="lk">CGRK-20260820-009</span>', num('42,500.00'), num('42,500.00'), num('0.00'), '2026-08-28', '2026-09-27', st('已付款'), ops(('详情', None, None))],
    [CB, '<span class="lk">AP-20260825-005</span>', '路凯包装运营（上海）有限公司', '—（租入运营费）', '—', num('126,000.00'), num('0.00'), num('126,000.00', danger=True), '2026-08-25', '2026-09-24', st('未付款'), ops(('付款', '../财务协同/付款登记.html', None), ('详情', None, None))],
    [CB, '<span class="lk">AP-20260820-004</span>', '苏州联恒五金制品有限公司', '<span class="lk">PO-20260810-009</span>', '<span class="lk">CGRK-20260815-007</span>', num('6,300.00'), num('6,300.00'), num('0.00'), '2026-08-20', '2026-09-19', st('已付款'), ops(('详情', None, None))],
    [CB, '<span class="lk">AP-20260815-003</span>', '宁波华塑包装制品有限公司', '<span class="lk">PO-20260808-008</span>', '<span class="lk">CGRK-20260812-006</span>', num('35,200.00'), num('35,200.00'), num('0.00'), '2026-08-15', '2026-09-14', st('已付款'), ops(('详情', None, None))],
]
PAGES.append(dict(
    rel='财务协同/应付账单.html', title='应付账单', selected='应付账单',
    tab_names=['应付账单', '付款登记', '应收账单'],
    content=filter_card([fi_input('应付账单号'), fi_sel('供应商名称'), fi_input('关联采购订单号')],
                        [fi_sel('状态'), fi_range('账单日期')]) +
            list_card('应付账单', '<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新建应付账单</button>',
                      stabs_bar([('全部', 19), ('未付款', 6), ('部分付款', 4), ('已付款', 9)]),
                      table(['', '应付账单号', '供应商名称', '关联采购订单号', '关联采购入库单号', '账单金额(元)', '已付金额(元)', '未付金额(元)', '账单日期', '到期日', '状态', '操作'], ap_rows),
                      pager(19)) +
            '<div class="pn-hint" style="padding:0 4px;">应付账单可由采购入库单审核后自动生成（第一期支持手动创建）；租入业务（路凯）按周期生成应付账单。</div>',
    modals=ap_modal))

# ============================================================
# 5.13 财务协同/付款登记.html
# ============================================================
pay_modal = modal('createModal', '新建付款登记',
    m_select('供应商', '苏州联恒五金制品有限公司', req=True) +
    m_select('关联应付账单', 'AP-20260830-007（未付 6,700.00）', req=True) +
    m_input('付款金额(元)', '6,700.00', req=True) +
    m_input('付款日期', '2026-09-03') +
    m_select('付款银行', '招商银行苏州分行 1109××××8821') +
    m_input('备注', ph='选填'), wide=False)

pay_rows = [
    [CB, '<span class="lk">PAY-20260902-005</span>', '苏州联恒五金制品有限公司', '<span class="lk">AP-20260830-007</span>', num('6,000.00'), '2026-09-02', '招商银行苏州分行 1109××××8821', st('待确认'), ops(('确认', None, None), ('详情', None, None))],
    [CB, '<span class="lk">PAY-20260831-004</span>', '常州正大塑料托盘厂', '<span class="lk">AP-20260828-006</span>', num('42,500.00'), '2026-08-31', '中国银行常州分行 3325××××0067', st('已确认'), ops(('详情', None, None))],
    [CB, '<span class="lk">PAY-20260828-003</span>', '宁波华塑包装制品有限公司', '<span class="lk">AP-20260815-003</span>', num('35,200.00'), '2026-08-28', '工商银行宁波分行 4402××××5531', st('已确认'), ops(('详情', None, None))],
    [CB, '<span class="lk">PAY-20260825-002</span>', '苏州联恒五金制品有限公司', '<span class="lk">AP-20260820-004</span>', num('6,300.00'), '2026-08-25', '招商银行苏州分行 1109××××8821', st('已确认'), ops(('详情', None, None))],
    [CB, '<span class="lk">PAY-20260818-001</span>', '路凯包装运营（上海）有限公司', '<span class="lk">AP-20260810-002</span>', num('58,000.00'), '2026-08-18', '建设银行上海分行 6217××××9045', st('已确认'), ops(('详情', None, None))],
]
PAGES.append(dict(
    rel='财务协同/付款登记.html', title='付款登记', selected='付款登记',
    tab_names=['付款登记', '应付账单', '收款登记'],
    content=filter_card([fi_input('付款编号'), fi_sel('供应商名称'), fi_input('关联应付账单号')],
                        [fi_sel('状态'), fi_range('付款日期')]) +
            list_card('付款登记', '<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新建付款登记</button>',
                      stabs_bar([('全部', 11), ('待确认', 3), ('已确认', 8)]),
                      table(['', '付款编号', '供应商名称', '关联应付账单号', '付款金额(元)', '付款日期', '付款银行', '状态', '操作'], pay_rows),
                      pager(11)),
    modals=pay_modal))

# ============================================================
# 主程序
# ============================================================
if __name__ == '__main__':
    for cfg in PAGES:
        html = build_page(cfg['rel'], cfg['title'], cfg['selected'], cfg['tab_names'], cfg['content'], cfg.get('modals', ''))
        write_page(cfg['rel'], html)
        print(f"已生成: {cfg['rel']} ({len(html)} 字节)")
    print(f'共生成 {len(PAGES)} 个新页面')
