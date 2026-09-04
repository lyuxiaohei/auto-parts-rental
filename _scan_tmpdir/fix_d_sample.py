# -*- coding: utf-8 -*-
"""样板：采购入库单详情弹窗（四段式）· 采购入库列表 8 个「详情」按钮。"""
import sys
sys.path.insert(0, r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir")
from detail_modal_lib import *

PAGE = '仓储作业/采购入库列表.html'

header = (
    drow('入库单号', 'CGRK-20260828-012')
    + drow('单据类型', '采购入库单 · 零部件采购')
    + drow('状态', '<span class="tag tag-green">已入库</span>')
    + drow('供应商', '苏州联恒五金制品有限公司')
    + drow('关联采购订单', '<span class="lk" onclick="go(\'../采购管理/采购订单列表.html\')">PO-20260828-015</span>')
    + drow('所属项目', 'PRJ-2601')
    + drow('到货数量', '40 托 / 3,400 件')
    + drow('入库库区', '原料区 RA')
    + drow('制单人', '张伟')
    + drow('入库时间', '2026-08-28 14:32')
    + drow('验收方式', '凭采购订单到货验收')
    + drow('备注', '验收通过后库存入账，并可生成应付账单')
)

mat = mat_table(
    ['序号', '零件号', '名称规格', '单位', '~托数 × 件数', '~单价(元)', '~金额(元)', '批次', '库位'],
    [
        ['1', 'LJ-A100', '锁扣组件 不锈钢 304', '件', '~24 托 × 100', '~4.80', '~11,520.00', 'B20260828-01', 'RA-A-01-02'],
        ['2', 'LJ-B200', '铰链 锌合金 65mm', '件', '~16 托 × 125', '~1.60', '~3,200.00', 'B20260828-02', 'RA-A-01-03'],
    ])

chain = (
    node('采购订单', 'PO-20260828-015', '../采购管理/采购订单列表.html')
    + ARROW
    + node('采购入库（本单）', 'CGRK-20260828-012', cur=True)
    + ARROW
    + node('库存台账', '原料区 RA · LJ-A100 / LJ-B200', '../仓储作业/库存查询.html')
    + ARROW
    + node('应付账单', '验收通过后生成（采购应付）', '../财务协同/应付账单.html')
)

timeline = (
    tl('08-28 09:40', '到货登记 · 苏州联恒送货到达原料区 RA（40 托）', '张伟')
    + tl('08-28 11:20', '数量清点 · 40 托 / 3,400 件，与采购订单一致', '张伟')
    + tl('08-28 14:10', '质检验收 · 抽检合格，验收通过', '张伟')
    + tl('08-28 14:32', '入库完成 · 库存入账（原料区 RA）', '系统')
    + tl_off('08-28 14:33', '应付账单 · 待按验收结果生成', '系统')
)

modal = detail_modal('detailModal', '采购入库单详情 · CGRK-20260828-012', header, '到货明细', mat, chain, timeline)

t, t2 = inject_block(PAGE, modal, with_js=False)  # 页内已有 auditModal + 弹窗开关脚本
t2 = bind_buttons(t2, '<a>详情</a>', '<a onclick="openModal(\'detailModal\')">详情</a>', 8)
assert_unique_id(t2, 'detailModal')
write_page(PAGE, t2)
print('OK 业务页注入:', PAGE)

out = standalone('仓储作业/弹窗/采购入库单详情.html', '采购入库单详情', PAGE, modal)
print('OK 独立模板:', out)
