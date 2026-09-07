# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃（弹窗库，随工具链归档）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""补齐缺口弹窗：12 页审核确认弹窗 + 6 页新建/配置弹窗；缺 openModal JS 的页面一并注入"""
import os, re, sys, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2lib import PROTO, read_page, write_page  # noqa

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

