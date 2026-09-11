# -*- coding: utf-8 -*-
"""供应商税率维护（道远拍板方案 A+数据驱动）：
① 页内 createModal+弹窗模板 双层内嵌行编辑器（供应商下拉=partners·税率·结算周期·+添加一行·删除）
② 产品档案页税率区 tbody 静态 5 行→按 DEMO_DATA.productTaxes 渲染
③ 弹窗模板补 demo-data.js 引用。精确替换+assert。"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT/'P3-R01-包装租赁管理后台原型'/'基础数据'/'产品档案.html'
TPL = ROOT/'P3-R01-包装租赁管理后台原型'/'基础数据'/'弹窗'/'新建产品.html'

TAX_HTML = '''  </div>
  <style>
  .tax-sec{margin:2px 0 6px;}
  .tax-sec-title{font-size:13px;font-weight:600;color:#1a1a1a;margin:4px 0 8px;}
  .tax-sec-sub{font-weight:400;color:#8c8c8c;font-size:12px;margin-left:6px;}
  .tax-edit{border:1px solid #e5e6eb;border-radius:6px;padding:8px 10px;}
  .tax-edit-hd{display:flex;gap:8px;font-size:12px;color:#8c8c8c;padding:2px 0 6px;}
  .tax-edit-hd span{flex:1;}
  .tax-edit-row{display:flex;gap:8px;margin-bottom:6px;align-items:center;}
  .tax-cell{flex:1;display:flex;}
  .tax-sel,.tax-in{width:100%;height:28px;border:1px solid #d9d9d9;border-radius:4px;font-size:12px;padding:0 6px;outline:none;box-sizing:border-box;}
  .tax-sel:focus,.tax-in:focus{border-color:#1677ff;}
  .tax-del{color:#1677ff;font-size:12px;text-decoration:none;white-space:nowrap;}
  </style>
  <div class="tax-sec">
    <div class="tax-sec-title">供应商税率<span class="tax-sec-sub">同一物料可按供应商维护不同税率；单据明细税率默认带出、可手动覆盖</span></div>
    <div class="tax-edit">
      <div class="tax-edit-hd"><span>供应商</span><span>默认税率</span><span>结算周期</span><span style="flex:0 0 44px;">操作</span></div>
      <div id="taxEditRows"></div>
      <button class="btn btn-default btn-sm" type="button" onclick="addTaxRow()">+ 添加一行</button>
    </div>
  </div>
'''

TAX_JS = '''<script>
/* 供应商税率行编辑器（数据驱动：下拉源=DEMO_DATA.partners 类型=供应商；预填=DEMO_DATA.productTaxes） */
(function () {
  var SUPS = [];
  try {
    var P = (window.DEMO_DATA || {}).partners || {};
    Object.keys(P).forEach(function (k) {
      var f = (P[k].row || {}).fields || {};
      if (f.type === '供应商') SUPS.push(f.name);
    });
  } catch (e) {}
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  window.addTaxRow = function (sup, rate, cyc) {
    var box = document.getElementById('taxEditRows');
    if (!box) return;
    var opts = SUPS.map(function (n) {
      return '<option value="' + esc(n) + '"' + (n === sup ? ' selected' : '') + '>' + esc(n) + '</option>';
    }).join('');
    box.insertAdjacentHTML('beforeend',
      '<div class="tax-edit-row">'
      + '<span class="tax-cell"><select class="tax-sel">' + opts + '</select></span>'
      + '<span class="tax-cell"><input class="tax-in" value="' + esc(rate || '13%') + '"></span>'
      + '<span class="tax-cell"><input class="tax-in" value="' + esc(cyc || '月结 30 天') + '"></span>'
      + '<span class="tax-cell" style="flex:0 0 44px;"><a href="javascript:void(0)" class="tax-del" onclick="removeTaxRow(this)">删除</a></span>'
      + '</div>');
  };
  window.removeTaxRow = function (el) {
    var row = el.closest('.tax-edit-row');
    if (row && row.parentNode) row.parentNode.removeChild(row);
  };
  window.initTaxEdit = function (productKey) {
    var box = document.getElementById('taxEditRows');
    if (!box) return;
    box.innerHTML = '';
    var n = 0;
    try {
      var T = (window.DEMO_DATA || {}).productTaxes || {};
      Object.keys(T).forEach(function (k) {
        var f = (T[k].row || {}).fields || {};
        if (!productKey || f.product === productKey) { window.addTaxRow(f.supplier, f.taxRate, f.settleCycle); n++; }
      });
    } catch (e) {}
    if (n === 0) window.addTaxRow();
  };
  if (document.getElementById('taxEditRows')) initTaxEdit('WBX-1210L');
  /* 供应商税率维护区列表（仅产品档案页有此节点）：按 productTaxes 渲染 */
  var listBody = document.getElementById('taxRateBody');
  if (listBody) {
    var html = '';
    try {
      var T2 = (window.DEMO_DATA || {}).productTaxes || {};
      Object.keys(T2).forEach(function (k) {
        var f = (T2[k].row || {}).fields || {};
        html += '<tr><td>' + esc(f.product) + '</td><td>' + esc(f.productName) + '</td><td>' + esc(f.cls) + '</td><td>' + esc(f.supplier) + '</td><td><span class="td-num">' + esc(f.taxRate) + '</span></td><td>' + esc(f.settleCycle) + '</td></tr>';
      });
    } catch (e) {}
    listBody.innerHTML = html || '<tr><td colspan="6">—</td></tr>';
  }
})();
</script>
'''

# ---------- ① 产品档案.html ----------
s = PAGE.read_text(encoding='utf-8')
# 1a. createModal 备注锚后插行编辑器（双层同锚）
anchor_remark = '''<div class="input-box"><input placeholder="选填"></div>
  </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-default" onclick="closeModal('createModal')">取消</button>
      <button class="btn" onclick="closeModal('createModal')">保存</button>'''
assert s.count(anchor_remark) == 1, f'页内备注锚 {s.count(anchor_remark)}'
new_remark = '''<div class="input-box"><input placeholder="选填"></div>
''' + TAX_HTML + '''    </div>
    <div class="modal-footer">
      <button class="btn btn-default" onclick="closeModal('createModal')">取消</button>
      <button class="btn" onclick="closeModal('createModal')">保存</button>'''
s = s.replace(anchor_remark, new_remark)

# 1b. 税率区 tbody 静态 5 行 → 数据驱动容器（tbody 置空+id，行由 JS 渲染）
import re
m = re.search(r'(供应商税率维护</h3>.*?<tbody>)(.*?)(</tbody>)', s, re.S)
assert m, '税率区锚缺失'
old_rows = m.group(2)
assert old_rows.count('<tr>') == 5, f'税率区静态行 {old_rows.count("<tr>")}≠5'
head_with_id = m.group(1).replace('<tbody>', '<tbody id="taxRateBody">')
s = s[:m.start()] + head_with_id + '\n      ' + m.group(3) + s[m.end():]

# 1c. </body> 前插 JS（pc-auth 引用之前）
pc = '<script src="../_data/pc-auth.js"></script>'
assert s.count(pc) == 1, 'pc-auth 引用锚'
s = s.replace(pc, TAX_JS + '\n' + pc)
PAGE.write_text(s, encoding='utf-8')
print('产品档案.html 改造完成')

# ---------- ② 弹窗模板 ----------
s2 = TPL.read_text(encoding='utf-8')
assert s2.count(anchor_remark) == 1, f'模板备注锚 {s2.count(anchor_remark)}'
s2 = s2.replace(anchor_remark, new_remark)
# 模板补 demo-data 引用 + JS（</body> 前）
tail_anchor = '</body>'
assert s2.count(tail_anchor) == 1
s2 = s2.replace(tail_anchor, '<script src="../../_data/demo-data.js"></script>\n' + TAX_JS + '</body>')
TPL.write_text(s2, encoding='utf-8')
print('新建产品.html 改造完成')
