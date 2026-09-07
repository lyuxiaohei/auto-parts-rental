# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃（弹窗注入旧版，已被后续流程取代）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""补齐缺口弹窗 第二批（容错版）：按按钮文本注入 onclick，保留 data-note 等属性"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2lib import read_page, write_page
from modal_lib import m_select, m_input, m_radio, audit_modal, create_modal, inject, wire

def wire_btn(html, btn_text, modal_id, page_rel):
    """给 <button ...>btn_text</button> 注入 onclick（幂等：已有 onclick 则跳过）"""
    pat = re.compile(r'<button((?:(?!onclick)[^>])*)>' + re.escape(btn_text) + r'</button>')
    m = pat.search(html)
    if not m:
        if f'openModal(\'{modal_id}\')' in html and f'>{btn_text}</button>' in html:
            print(f'  （已接线，跳过 {page_rel} / {btn_text}）')
            return html
        raise RuntimeError(f'{page_rel}: 未找到按钮 {btn_text}')
    return html[:m.start()] + f'<button{m.group(1)} onclick="openModal(\'{modal_id}\')">{btn_text}</button>' + html[m.end():]

def wire_op(html, op_text, modal_id, page_rel):
    """把无 onclick 的行内 <a>op</a> 接到弹窗"""
    pat = re.compile(r'<a>' + re.escape(op_text) + r'</a>')
    if not pat.search(html):
        print(f'  （无 {op_text} 链接或已接线 {page_rel}）')
        return html
    return pat.sub(f'<a onclick="openModal(\'{modal_id}\')">{op_text}</a>', html)

JOBS = [
    ('财务协同/回款登记.html', '新增收款', '新建收款登记', lambda: (
        m_select('客户', '一汽解放汽车有限公司', req=True) +
        m_select('关联应收账单', 'AR-202608-001（未核销 126,800.00）', req=True) +
        m_input('收款金额(元)', '60,000.00', req=True) +
        m_input('收款日期', '2026-09-03') +
        m_select('收款银行', '工商银行长春分行 6222××××3308') +
        m_input('银行回单', ph='上传回单附件（原型占位）'))),
    ('财务协同/开票登记.html', '新增开票登记', '新增开票登记', lambda: (
        m_select('购方名称（客户）', '一汽解放汽车有限公司', req=True) +
        m_select('关联应收账单', 'AR-202608-001（126,800.00）', req=True) +
        m_select('发票类型', '增值税专票 13%') +
        m_input('开票金额(元)', '126,800.00', req=True) +
        m_input('开票日期', '2026-09-03') +
        m_input('备注', ph='选填'))),
    ('财务协同/应收账单.html', '手动生成账单', '手动生成账单', lambda: (
        m_select('客户', '一汽解放汽车有限公司', req=True) +
        m_select('所属项目', 'PRJ-2601 一汽解放·长春基地', req=True) +
        m_input('账期', '2026-09') +
        m_select('账单类型', '租赁费') +
        m_input('账单金额(元)', '126,800.00', req=True) +
        m_input('备注', ph='选填'))),
    ('订单协同/结算导出.html', '新建结算批次', '新建结算批次', lambda: (
        m_select('运营方', '路凯包装运营（上海）有限公司', req=True) +
        m_input('账期', '2026-08', req=True) +
        m_select('所属项目', '全部项目') +
        m_input('备注', ph='选填'))),
]

for rel, btn_text, title, fields_fn in JOBS:
    h = read_page(rel)
    if f'id="createModal"' in h:
        print(f'  （已有 createModal，仅补接线 {rel}）')
        h = wire_btn(h, btn_text, 'createModal', rel)
    else:
        h = wire_btn(h, btn_text, 'createModal', rel)
        h = inject(h, create_modal('createModal', title, fields_fn()), rel, 'function openModal' not in h)
    write_page(rel, h)
    print(f'✅ {rel}（{title}）')

# ---- 路凯下发 ----
rel = '订单协同/路凯下发.html'
h = read_page(rel)
if 'id="createModal"' not in h:
    batch_modal = create_modal('createModal', '生成下发批次',
        m_select('来源订单范围', '已审核未下发订单（6 张）', req=True) +
        m_select('下发方式', 'API 自动下发路凯') +
        m_input('备注', ph='选填'))
    confirm_modal = create_modal('confirmModal', '下发确认',
        '''<div class="dgrid" style="margin-bottom:16px;">
        <div class="drow"><div class="dlabel">下发批次号</div><div class="dval">XF-20260902-003</div></div>
        <div class="drow"><div class="dlabel">覆盖数量</div><div class="dval">6 张订单 / 1,240 件套</div></div>
        <div class="drow"><div class="dlabel">下发方式</div><div class="dval">API 自动下发路凯</div></div>
        <div class="drow"><div class="dlabel">回执</div><div class="dval">下发后等待路凯回执（状态自动更新）</div></div>
      </div>''')
    h = inject(h, batch_modal + confirm_modal, rel, True)
h = wire_btn(h, '生成下发批次', 'createModal', rel)
h = wire_op(h, '下发', 'confirmModal', rel)
write_page(rel, h)
print(f'✅ {rel}（生成下发批次 + 下发确认）')

# ---- 盘点列表 ----
rel = '仓储作业/盘点列表.html'
h = read_page(rel)
if 'id="auditModal"' not in h:
    h = inject(h, audit_modal('PD-20260830-004', '库存盘点单', '盘点项数 / 盈亏', '86 项 / 盘盈 320 元', '李国栋 / 2026-08-30 17:20', '审核通过后按盈亏生成其他出入库单'), rel, True)
h = wire_op(h, '审核', 'auditModal', rel)
write_page(rel, h)
print(f'✅ {rel}（盘点审核）')

# ---- 组合出库列表 ----
rel = '仓储作业/组合出库列表.html'
h = read_page(rel)
if 'id="auditModal"' not in h:
    h = inject(h, audit_modal('ZHCK-20260901-006', '组合出库单', '出库数量', '180 套', '张伟 / 2026-09-01 10:32', '确认后库存扣减、对应租赁单进入在租状态'), rel, True)
h = wire_op(h, '出库确认', 'auditModal', rel)
write_page(rel, h)
print(f'✅ {rel}（出库确认）')

# ---- 租出台账：新建台账 → 新建租赁单（跳转） ----
rel = '包装管理/租出台账.html'
h = read_page(rel)
if '>新建台账</button>' in h:
    h = re.sub(r'<button([^>]*)>新建台账</button>',
               '<button\\1 onclick="go(\'../包装管理/租赁单列表.html\')">新建租赁单</button>', h)
    write_page(rel, h)
    print(f'✅ {rel}（新建台账 → 新建租赁单跳转）')
else:
    print(f'  （{rel} 已是跳转态，跳过）')

print('\n第二批完成')
