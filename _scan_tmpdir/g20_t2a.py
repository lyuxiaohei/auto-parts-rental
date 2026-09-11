# -*- coding: utf-8 -*-
"""G20 T2a：退租入库录入入口（弹窗形态）——新模板+宿主页按钮+页内 createModal。
范本=租入归还新建.html（完整页面形态）。宿主页无 showToast→提交版仅 closeModal（任务书预案·记偏差）。"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL_SRC = ROOT/'P3-R01-包装租赁管理后台原型'/'租赁管理'/'弹窗'/'租入归还新建.html'
TPL_NEW = ROOT/'P3-R01-包装租赁管理后台原型'/'租赁管理'/'弹窗'/'退租入库新建.html'
PAGE = ROOT/'P3-R01-包装租赁管理后台原型'/'租赁管理'/'退租入库列表.html'

tpl = TPL_SRC.read_text(encoding='utf-8')

# ---------- ① 新模板 ----------
# 1a. 头注释+title
old_note = '<!-- 注入标记：租赁管理/租入归还列表.html -->'
assert tpl.count(old_note) == 1
tpl2 = tpl.replace(old_note, '<!-- 弹窗模板：退租入库新建（createModal）· 注入标记：租赁管理/退租入库列表.html -->')
old_title = '<title>租入归还新建 - 包装租赁管理后台</title>'
assert tpl2.count(old_title) == 1
tpl2 = tpl2.replace(old_title, '<title>退租入库新建 - 包装租赁管理后台</title>')

# 1b. modal 区整体替换（modal-overlay 到 </div> 闭合，不含其后 script）
k = tpl2.find('<div class="modal-overlay" id="createModal">')
j = tpl2.find('</div>\n<script>', k)
assert 0 < k < j, 'modal 块定位失败'
NEW_MODAL = '''<div class="modal-overlay" id="createModal">
  <div class="modal modal-lg">
    <div class="modal-header">
      <h3 class="modal-title">新建退租入库单</h3>
      <span class="modal-close" onclick="closeModal('createModal')">×</span>
    </div>
    <div class="modal-body">
      <div class="form-row">
        <span class="form-label"><span class="req">*</span>关联租赁单</span>
        <div class="select-box input-box"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>ZL-20260823-033（驾驶室围板箱 · 客户退回中）</option><option>ZL-20260901-032（围板箱组合 · 客户退回中）</option><option>ZL-20260828-031（整箱套件 · 客户退回中）</option></select><span class="caret">▾</span></div>
      </div>
      <div class="form-row">
        <span class="form-label"><span class="req">*</span>退回日期</span>
        <div class="input-box"><input type="date" value="2026-09-11"></div>
      </div>
      <div class="form-row">
        <span class="form-label"><span class="req">*</span>退回明细</span>
        <div style="flex:1;min-width:0;">
          <div class="table-wrap" style="border:1px solid var(--border);border-radius:6px;">
            <table class="edit-tbl">
              <thead><tr><th>物料</th><th>退回数量</th><th>缺损数量</th></tr></thead>
              <tbody>
                <tr><td>WBX-1210L 围板箱 1200×1000×970</td><td><input value="86"></td><td><input value="3"></td></tr>
                <tr><td>GB-800 隔板</td><td><input value="40"></td><td><input value="0"></td></tr>
                <tr><td>锁扣组件</td><td><input value="80"></td><td><input value="0"></td></tr>
              </tbody>
            </table>
          </div>
          <div class="pn-hint">按单一物料/拆后零件逐行记录；缺损行生成丢损应收（对客户）或应付（对供应商）。</div>
        </div>
      </div>
      <div class="form-row">
        <span class="form-label">验收备注</span>
        <div class="input-box" style="height:auto;padding:6px 11px;"><textarea placeholder="缺损情况、照片张数等" style="width:100%;border:none;outline:none;background:transparent;font:inherit;color:inherit;resize:vertical;min-height:44px;"></textarea></div>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-default" onclick="closeModal('createModal')">取消</button>
      <button class="btn" onclick="closeModal('createModal')">提交审核</button>
    </div>
  </div>
</div>'''
tpl2 = tpl2[:k] + NEW_MODAL + tpl2[j+len('</div>'):]
assert tpl2.count('id="createModal"') == 1 and '新建退租入库单' in tpl2
TPL_NEW.write_text(tpl2, encoding='utf-8')
print('new template written:', len(tpl2))

# ---------- ② 宿主页 ----------
s = PAGE.read_text(encoding='utf-8')
old_btn = '<div class="head-btns"><button class="btn btn-default btn-sm">批量导出</button></div>'
assert s.count(old_btn) == 1, '按钮锚'
new_btn = '<div class="head-btns"><button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新建退租入库单</button></div>'
s = s.replace(old_btn, new_btn)
# 内嵌 createModal（与模板 markup 逐字一致，不含 script；插在 openModal 定义行前）
anchor_js = 'function openModal(id)'
assert s.count(anchor_js) == 1, 'openModal 函数锚'
s = s.replace(anchor_js, NEW_MODAL + '\n\n' + anchor_js)
assert s.count('id="createModal"') == 1
assert s.count('function openModal') == 1 and s.count('function closeModal') == 1, 'open/close 唯一'
assert 'showToast' not in s  # 页内无 showToast（任务书预案：仅 closeModal·记偏差）
PAGE.write_text(s, encoding='utf-8')
print('host page updated:', len(s))
