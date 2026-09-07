# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃（弹窗提取，已完成使命）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""弹窗架构改造-第1步：从页面提取 43 个页内弹窗为独立模板（模块/弹窗/），原位置留注入标记"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2lib import PROTO, read_page, write_page
from modal_lib import audit_modal

def extract_modal(html, mid):
    """按 div 深度平衡提取 modal-overlay 整块，返回 (块文本, 起, 止)"""
    m = re.search(r'<div class="modal-overlay" id="' + re.escape(mid) + r'"[^>]*>', html)
    if not m:
        return None
    depth = 1
    for mm in re.finditer(r'<div|</div>', html[m.end():]):
        if mm.group(0) == '<div':
            depth += 1
        else:
            depth -= 1
        if depth == 0:
            end = m.end() + mm.end()
            return html[m.start():end], m.start(), end
    return None

# page → [(modal_id, 模板文件名, 标题覆盖(None=用页内原标题))]
MAP = {
    '项目管理/项目档案.html': [('createModal', '新建项目.html', None), ('ruleModal', '编码规则.html', None), ('bindModal', '上下游绑定.html', None)],
    '项目管理/项目详情.html': [('bindModal', '上下游绑定.html', None)],  # 共享模板
    '采购管理/采购订单列表.html': [('createModal', '新建采购订单.html', None), ('auditModal', '采购订单审核.html', None)],
    '销售管理/销售订单列表.html': [('createModal', '新建销售订单.html', None), ('auditModal', '销售订单审核.html', None)],
    '仓储作业/销售出库列表.html': [('createModal', '销售出库新建.html', None), ('auditModal', '销售出库审核.html', None)],
    '仓储作业/退租入库列表.html': [('auditModal', '退租入库审核.html', None)],
    '仓储作业/其他入库列表.html': [('createModal', '其他入库新建.html', None), ('auditModal', '其他入库审核.html', None)],
    '仓储作业/其他出库列表.html': [('createModal', '其他出库新建.html', None), ('auditModal', '其他出库审核.html', None)],
    '仓储作业/拆卸管理列表.html': [('createModal', '拆卸新建.html', None), ('auditModal', '拆卸审核.html', None)],
    '仓储作业/库存调拨列表.html': [('createModal', '调拨新建.html', None), ('auditModal', '调拨审核.html', None)],
    '仓储作业/组合出库列表.html': [('auditModal', '组合出库确认.html', '出库确认')],
    '仓储作业/盘点列表.html': [('auditModal', '盘点审核.html', None)],
    '包装管理/租赁单列表.html': [('createModal', '租赁单新建.html', None), ('auditModal', '租赁单审核.html', None)],
    '包装管理/退租申请列表.html': [('createModal', '退租申请新建.html', None), ('auditModal', '退租申请审核.html', None)],
    '包装管理/丢损赔偿单.html': [('auditModal', '丢损赔偿审核.html', None)],
    '订单协同/客户订单.html': [('auditModal', '订单审核.html', None)],
    '订单协同/结算导出.html': [('createModal', '结算批次新建.html', None)],
    '订单协同/路凯下发.html': [('createModal', '下发批次生成.html', None), ('confirmModal', '下发确认.html', None)],
    '财务协同/应付账单.html': [('createModal', '应付账单新建.html', None)],
    '财务协同/付款登记.html': [('createModal', '付款登记新建.html', None), ('auditModal', '付款确认.html', '确认付款')],
    '财务协同/回款登记.html': [('createModal', '收款登记新建.html', None)],
    '财务协同/应收账单.html': [('createModal', '应收账单生成.html', None)],
    '财务协同/开票登记.html': [('createModal', '开票登记新建.html', None)],
    '基础数据/客商管理.html': [('createModal', '新建客商.html', None)],
    '基础数据/器具档案.html': [('createModal', '新建器具.html', None)],
    '基础数据/零部件档案.html': [('createModal', '新建零部件.html', None)],
    '基础数据/库位档案.html': [('createModal', '新建库位.html', None)],
    '系统管理/用户权限.html': [('createModal', '新增用户.html', None), ('roleModal', '角色管理.html', None)],
    '系统管理/数据字典.html': [('createModal', '新增字典项.html', None)],
}

MARKER = '<!-- 弹窗已提取到 弹窗/{fname}，构建时注入 -->'
written_templates = {}  # 模板路径 → 内容（共享模板只写一次）

for rel, modals in MAP.items():
    h = read_page(rel)
    module = rel.split('/')[0]
    for mid, fname, title_override in modals:
        r = extract_modal(h, mid)
        if not r:
            print(f'⚠️ {rel}: 未找到 {mid}（跳过）')
            continue
        block, s, e = r
        # 标题覆盖（组合出库确认/付款确认）
        if title_override:
            block = re.sub(r'(<h3 class="modal-title">)[^<]*(</h3>)', r'\g<1>' + title_override + r'\g<2>', block)
        title = re.search(r'<h3 class="modal-title">([^<]*)</h3>', block).group(1)
        # 从页面移除，留标记
        h = h[:s] + MARKER.format(fname=fname) + h[e:]
        # 写模板（共享模板首次写，注入标记含所有引用页）
        tpath = os.path.join(PROTO, module, '弹窗', fname)
        if tpath not in written_templates:
            pages_of_tpl = [p for p, ms in MAP.items() for i2, f2, _ in ms if f2 == fname and p.split('/')[0] == module]
            marker_pages = '、'.join(pages_of_tpl)
            tpl = f'<!-- 弹窗模板：{title}（{mid}） -->\n<!-- 注入标记：{marker_pages} -->\n{block}\n'
            written_templates[tpath] = tpl
    write_page(rel, h)
    print(f'提取 ✅ {rel}（{len(modals)} 个）')

# 采购入库列表：新增「验收」审核弹窗模板 + 接线 + 标记
rel = '仓储作业/采购入库列表.html'
h = read_page(rel)
block = audit_modal('CGRK-20260827-009', '采购入库单', '到货数量', '12 托（零部件）', '李国栋 / 2026-08-27 09:20', '验收通过后库存入账，并可生成应付账单')
block = block.rstrip('\n')
tpath = os.path.join(PROTO, '仓储作业', '弹窗', '采购入库审核.html')
tpl = f'<!-- 弹窗模板：审核确认（auditModal） -->\n<!-- 注入标记：{rel} -->\n{block}\n'
written_templates[tpath] = tpl
h = h.replace('<a>验收</a>', '<a onclick="openModal(\'auditModal\')">验收</a>')
# 在页面尾部脚本前留注入标记
h = h.replace('<script>\n/* ===== 菜单折叠', MARKER.format(fname='采购入库审核.html') + '\n<script>\n/* ===== 菜单折叠', 1)
write_page(rel, h)
print(f'新增模板+接线 ✅ {rel}（验收 → 采购入库审核）')

# 落盘所有模板
for tpath, tpl in written_templates.items():
    os.makedirs(os.path.dirname(tpath), exist_ok=True)
    with open(tpath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(tpl)
print(f'\n共写出 {len(written_templates)} 个弹窗模板')
