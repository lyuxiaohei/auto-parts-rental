# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃（弹窗注入旧版，已被后续流程取代）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""补齐缺口弹窗：12 页审核确认弹窗 + 6 页新建/配置弹窗；缺 openModal JS 的页面一并注入"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2lib import PROTO, read_page, write_page

MODAL_JS = '''<script>
function openModal(id) { document.getElementById(id).classList.add('show'); }
function closeModal(id) { document.getElementById(id).classList.remove('show'); }
document.querySelectorAll('.modal-overlay').forEach(function (ov) {
  ov.addEventListener('click', function (e) { if (e.target === ov) ov.classList.remove('show'); });
});
</script>
'''

SEL_CARET = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>'

def m_select(label, val, req=False):
    reqh = '<span class="req">*</span>' if req else ''
    return f'''<div class="form-row">
    <span class="form-label">{reqh}{label}</span>
    <div class="input-box select-box"><span>{val}</span><span class="caret">{SEL_CARET}</span></div>
  </div>'''

def m_input(label, val='', req=False, ph='请输入'):
    reqh = '<span class="req">*</span>' if req else ''
    v = f' value="{val}"' if val else ''
    return f'''<div class="form-row">
    <span class="form-label">{reqh}{label}</span>
    <div class="input-box"><input{v} placeholder="{ph}"></div>
  </div>'''

def m_radio(label, options, checked=0):
    radios = ''.join(f'<span class="radio{" checked" if i == checked else ""}"><span class="dot"></span>{o}</span>' for i, o in enumerate(options))
    return f'''<div class="form-row">
    <span class="form-label">{label}</span>
    <div>{radios}</div>
  </div>'''

def audit_modal(doc_no, doc_type, qty_label, qty_val, submitter, extra_note=''):
    """通用审核确认弹窗"""
    note_row = f'<div class="drow"><div class="dlabel">备注</div><div class="dval">{extra_note}</div></div>' if extra_note else ''
    return f'''<div class="modal-overlay" id="auditModal">
  <div class="modal">
    <div class="modal-header">
      <h3 class="modal-title">审核确认</h3>
      <span class="modal-close" onclick="closeModal('auditModal')">×</span>
    </div>
    <div class="modal-body">
      <div class="dgrid" style="margin-bottom:16px;">
        <div class="drow"><div class="dlabel">单据编号</div><div class="dval">{doc_no}</div></div>
        <div class="drow"><div class="dlabel">单据类型</div><div class="dval">{doc_type}</div></div>
        <div class="drow"><div class="dlabel">{qty_label}</div><div class="dval">{qty_val}</div></div>
        <div class="drow"><div class="dlabel">提交人 / 时间</div><div class="dval">{submitter}</div></div>
        {note_row}
      </div>
      <div class="form-row">
        <span class="form-label"><span class="req">*</span>审核结论</span>
        <div><span class="radio checked"><span class="dot"></span>通过</span><span class="radio"><span class="dot"></span>驳回</span></div>
      </div>
      <div class="form-row">
        <span class="form-label">审核意见</span>
        <div class="input-box"><input placeholder="选填，驳回时建议填写原因"></div>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-default" onclick="closeModal('auditModal')">取消</button>
      <button class="btn" onclick="closeModal('auditModal')">确认提交</button>
    </div>
  </div>
</div>
'''

def create_modal(mid, title, fields_html, wide=False):
    return f'''<div class="modal-overlay" id="{mid}">
  <div class="modal{' modal-lg' if wide else ''}">
    <div class="modal-header">
      <h3 class="modal-title">{title}</h3>
      <span class="modal-close" onclick="closeModal('{mid}')">×</span>
    </div>
    <div class="modal-body">
{fields_html}
    </div>
    <div class="modal-footer">
      <button class="btn btn-default" onclick="closeModal('{mid}')">取消</button>
      <button class="btn" onclick="closeModal('{mid}')">保存</button>
    </div>
  </div>
</div>
'''

def inject(html, modal_html, page_rel, need_js):
    """在 proto-notes 样式块前（或 </body> 前）注入弹窗 HTML 和 JS"""
    payload = ''
    if need_js:
        payload += MODAL_JS
    payload += modal_html
    for anchor in ['<style id="proto-notes-style">', '</body>']:
        if anchor in html:
            return html.replace(anchor, payload + '\n' + anchor, 1)
    raise RuntimeError(f'{page_rel}: 找不到注入锚点')

def wire(html, pairs, page_rel):
    """把无交互的按钮/链接接上 openModal"""
    for old, new in pairs:
        if old not in html:
            raise RuntimeError(f'{page_rel}: 未找到 {old[:60]}')
        html = html.replace(old, new)
    return html

# ============================================================
# A. 审核确认弹窗 ×12
# ============================================================
AUDIT_PAGES = {
    '采购管理/采购订单列表.html': ('PO-20260902-018', '采购订单', '采购金额', '12,700.00 元', '王强 / 2026-09-02 10:24'),
    '销售管理/销售订单列表.html': ('SO-20260902-0046', '销售订单', '销售金额', '4,800.00 元', '王强 / 2026-09-02 10:24'),
    '仓储作业/销售出库列表.html': ('XSCK-20260902-015', '销售出库单', '出库数量', '1,500 件', '张伟 / 2026-09-02 14:10'),
    '仓储作业/其他入库列表.html': ('QTRK-20260901-003', '其他入库单（盘盈）', '入库数量', '120 件', '李国栋 / 2026-09-01 09:30'),
    '仓储作业/其他出库列表.html': ('QTCK-20260901-004', '其他出库单（报废）', '出库数量', '35 只', '李国栋 / 2026-09-01 15:20'),
    '仓储作业/拆卸管理列表.html': ('CX-20260902-006', '拆卸单', '拆卸数量', '50 套', '张伟 / 2026-09-02 11:05'),
    '仓储作业/库存调拨列表.html': ('DB-20260901-003', '库存调拨单', '调拨数量', '1,000 件', '李国栋 / 2026-09-01 10:12'),
    '仓储作业/退租入库列表.html': ('TZRK-20260902-008', '退租入库单', '退租数量', '60 套', '张伟 / 2026-09-02 16:40', '验收结果：缺损，审核通过后将生成丢损赔偿单'),
    '包装管理/租赁单列表.html': ('ZL-20260901-032', '租赁单', '租赁数量', '180 套 · 租期 91 天', '王强 / 2026-09-01 09:18'),
    '包装管理/退租申请列表.html': ('TZSQ-20260902-007', '退租申请', '退租数量', '100 只', '袁明（客户）/ 2026-09-02 08:55', '审核通过后自动生成退租入库单'),
    '包装管理/丢损赔偿单.html': ('BS-20260902-010', '丢损赔偿单', '赔偿金额', '930.00 元', '系统自动生成 / 2026-09-02 17:02'),
    '财务协同/付款登记.html': ('PAY-20260902-005', '付款登记', '付款金额', '6,000.00 元', '财务·周敏 / 2026-09-02 13:26'),
}

for rel, args in AUDIT_PAGES.items():
    h = read_page(rel)
    modal = audit_modal(*args)
    need_js = 'function openModal' not in h
    # 接线：审核/驳回/确认
    pairs = []
    for word in ['审核', '驳回', '确认']:
        pairs.append((f'<a>{word}</a>', f'<a onclick="openModal(\'auditModal\')">{word}</a>'))
    h = wire(h, [(o, n) for o, n in pairs if o in h], rel)
    h = inject(h, modal, rel, need_js)
    write_page(rel, h)
    print(f'审核弹窗 ✅ {rel} (注入JS={need_js})')

# ============================================================
# B1. 基础数据 4 页新建弹窗
# ============================================================
CREATE_PAGES = {
    '基础数据/客商管理.html': (
        '新建客商',
        m_input('客商名称', req=True, ph='企业全称') +
        m_select('客商类型', '客户', req=True) +
        m_input('联系人', '张三') +
        m_input('联系电话', '138****0000') +
        m_select('开票资料', '增值税专票 13%') +
        m_input('备注', ph='选填'),
        '<button class="btn btn-sm" data-note="1">新建客商</button>'),
    '基础数据/器具档案.html': (
        '新建器具',
        m_input('器具编码', req=True, ph='如 WBX-1210L') +
        m_input('器具名称', req=True, ph='如 围板箱 1200×1000×970') +
        m_select('类别', '围板箱') +
        m_input('规格', '1200×1000×970mm') +
        m_select('单位', '只') +
        m_input('租金单价(元/天)', '2.40') +
        m_input('备注', ph='选填'),
        '<button class="btn btn-sm">新建器具</button>'),
    '基础数据/零部件档案.html': (
        '新建零部件',
        m_input('零件号', req=True, ph='如 LJ-A100') +
        m_input('零件名称', req=True, ph='如 锁扣组件') +
        m_input('规格 / 材质', '不锈钢 304') +
        m_select('供应商', '苏州联恒五金制品有限公司') +
        m_input('采购单价(元)', '1.28') +
        m_select('适用项目', '多项目共用') +
        m_input('备注', ph='选填'),
        '<button class="btn btn-sm">新建零部件</button>'),
    '基础数据/库位档案.html': (
        '新建库位',
        m_select('仓库', '一号仓', req=True) +
        m_select('库区', '原料区 RA') +
        m_input('库位编码', req=True, ph='如 RA-A01') +
        m_select('库位类型', '平面库位') +
        m_input('规格 / 承载', '1200×1000 · ≤800kg') +
        m_input('备注', ph='选填'),
        '<button class="btn btn-sm">新建库位</button>'),
}

for rel, (title, fields, btn_old) in CREATE_PAGES.items():
    h = read_page(rel)
    modal = create_modal('createModal', title, fields)
    btn_new = btn_old.replace('<button class="btn btn-sm"', '<button class="btn btn-sm" onclick="openModal(\'createModal\')"', 1)
    h = wire(h, [(btn_old, btn_new)], rel)
    h = inject(h, modal, rel, 'function openModal' not in h)
    write_page(rel, h)
    print(f'新建弹窗 ✅ {rel}')

# ============================================================
# B2. 系统管理 2 页
# ============================================================
rel = '系统管理/用户权限.html'
h = read_page(rel)
user_modal = create_modal('createModal', '新增用户',
    m_input('姓名', req=True, ph='真实姓名') +
    m_input('手机号', req=True, ph='登录账号') +
    m_select('角色', '项目经理', req=True) +
    m_select('所属方', '我方（系统运营）') +
    m_select('数据权限范围', '全部项目'))
role_modal = '''<div class="modal-overlay" id="roleModal">
  <div class="modal modal-lg">
    <div class="modal-header">
      <h3 class="modal-title">角色管理</h3>
      <span class="modal-close" onclick="closeModal('roleModal')">×</span>
    </div>
    <div class="modal-body">
      <div class="table-wrap" style="border:1px solid var(--border);border-radius:6px;">
        <table>
          <thead><tr><th>角色</th><th>说明</th><th>数据权限</th><th>账号数</th><th>操作</th></tr></thead>
          <tbody>
            <tr><td><b>系统管理员</b></td><td>全部功能 + 系统管理</td><td>全部项目</td><td><span class="td-num">2</span></td><td><span class="ops"><a>权限配置</a></span></td></tr>
            <tr><td><b>项目经理</b></td><td>项目/订单/租赁全流程</td><td>负责的项目</td><td><span class="td-num">5</span></td><td><span class="ops"><a>权限配置</a></span></td></tr>
            <tr><td><b>仓储主管</b></td><td>仓储作业 + 库存查询</td><td>全部项目</td><td><span class="td-num">4</span></td><td><span class="ops"><a>权限配置</a></span></td></tr>
            <tr><td><b>财务</b></td><td>财务应收/应付/项目损益</td><td>全部项目</td><td><span class="td-num">3</span></td><td><span class="ops"><a>权限配置</a></span></td></tr>
            <tr><td><b>客户账号</b></td><td>仅查看与下单申请</td><td>所属客户</td><td><span class="td-num">12</span></td><td><span class="ops"><a>权限配置</a></span></td></tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-default" onclick="closeModal('roleModal')">关闭</button>
      <button class="btn" onclick="closeModal('roleModal')">新增角色</button>
    </div>
  </div>
</div>
'''
h = wire(h, [
    ('<button class="btn btn-sm">新增用户</button>', '<button class="btn btn-sm" onclick="openModal(\'createModal\')">新增用户</button>'),
    ('<button class="btn btn-default btn-sm">角色管理</button>', '<button class="btn btn-default btn-sm" onclick="openModal(\'roleModal\')">角色管理</button>'),
], rel)
h = inject(h, user_modal + role_modal, rel, True)
write_page(rel, h)
print(f'弹窗 ✅ {rel}（新增用户 + 角色管理）')

rel = '系统管理/数据字典.html'
h = read_page(rel)
dict_modal = create_modal('createModal', '新增字典项',
    m_select('字典分类', '缺损类型', req=True) +
    m_input('字典项编码', req=True, ph='如 DAMAGE-05') +
    m_input('简码', 'QS') +
    m_input('名称', req=True, ph='如 箱体划痕') +
    m_input('排序', '5') +
    m_input('备注', ph='选填'))
h = wire(h, [
    ('<button class="btn btn-sm">新增字典项</button>', '<button class="btn btn-sm" onclick="openModal(\'createModal\')">新增字典项</button>'),
], rel)
h = inject(h, dict_modal, rel, True)
write_page(rel, h)
print(f'弹窗 ✅ {rel}（新增字典项）')

print('\n全部弹窗注入完成')
