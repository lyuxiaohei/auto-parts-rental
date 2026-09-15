# -*- coding: utf-8 -*-
"""G34 试点迭代 2：按道远 09-15 四条意见改造 采购订单新建.html

1. 删除「返回列表」按钮（与「取消」重复）
2. 「类别」→「物料类型」，取值改自数据字典（物料类型组·6 值）
3. 明细表「单位」「税率」改下拉，取值自数据字典（计量单位组 / 供应商税率组）
4. 明细表「物料编码」↔「物料名称」双向联动（取值自物料档案 products）
"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
N_P = os.path.join(ROOT, r'P3-R01-包装租赁管理后台原型\采购管理\采购订单新建.html')

N = io.open(N_P, encoding='utf-8', newline='').read().replace('\r\n', '\n')
SEL = 'flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;'
CELL = 'width:100%;min-width:110px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;'

# ============ 1. 删「返回列表」按钮 ============
old1 = """    <div class="head-btns"><button class="btn btn-default btn-sm" onclick="go('../采购管理/采购订单列表.html')">返回列表</button></div>
"""
assert N.count(old1) == 1, '返回列表按钮锚点异常'
N = N.replace(old1, '')
print('[1] 已删「返回列表」按钮（与提交条「取消」重复）')

# ============ 2. 类别 → 物料类型（字典驱动） ============
old2 = '<div class="form-label"><span class="req">*</span>类别：</div>'
assert N.count(old2) == 1, '类别 label 锚点异常'
N = N.replace(old2, '<div class="form-label"><span class="req">*</span>物料类型：</div>')
m2 = re.search(r'<select onchange="poToggleQj\(this\)"[^>]*>.*?</select>', N, re.S)
assert m2, '类别 select 锚点异常'
N = N[:m2.start()] + f'<select id="cmMtype" style="{SEL}"></select>' + N[m2.end():]
print('[2] 「类别」→「物料类型」，select 改字典驱动（选项由 JS 渲染）')

# ============ 3. 删「物料档案」行（物料类型已细分，该联动行不再需要） ============
lines = N.split('\n')
i3 = next((k for k, l in enumerate(lines) if 'id="poQjRow"' in l), -1)
assert i3 > 0 and 'form-row' in lines[i3], 'poQjRow 定位失败'
assert lines[i3 + 5].strip() == '</div>', f'poQjRow 结构异常: {lines[i3+5]!r}'
del lines[i3:i3 + 6]
N = '\n'.join(lines)
print('[3] 已删「物料档案」行（6 行）')

# ============ 4. 重写明细表 tbody：单位/税率下拉 + 物料编码↔名称联动位 ============
def tr(idx, spec, qty, excl, incl, amt, pick=False):
    spec_attr = 'value=""' if pick else f'value="{spec}"'
    return f'''        <tr>
          <td>{idx}</td>
          <td><select data-prod-key style="{CELL}"></select></td>
          <td><select data-prod-name style="{CELL}"></select></td>
          <td><input data-spec {spec_attr}></td>
          <td><select data-unit style="{CELL}"></select></td>
          <td class="td-num"><input data-tax="qty" value="{qty}"></td>
          <td class="td-num"><input data-tax="excl" value="{excl}"></td>
          <td><select data-tax="rate" style="width:80px;"></select></td>
          <td class="td-num"><input data-tax="incl" value="{incl}"></td>
          <td class="td-num auto-cell" data-tax="amt">{amt}</td>
          <td class="ops sticky-op"><a>删除</a></td>
        </tr>'''

tbody_new = '\n' + tr(1, '不锈钢 304', '5,000', '1.28', '1.45', '7,250.00') + '\n' + tr(2, '锌合金 65mm', '2,000', '1.65', '1.86', '3,720.00') + '\n      '
m4 = re.search(r'(<div class="table-wrap edit-tbl">\s*<table>\s*<thead>.*?</thead>\s*<tbody>)(.*?)(</tbody>)', N, re.S)
assert m4, 'tbody 锚点异常'
N = N[:m4.start(2)] + tbody_new + N[m4.end(2):]
print('[4] 明细表 tbody 重写：物料编码/名称/单位/税率 四列为下拉')

# ============ 5. poSoPick 模板同步（生成行也用下拉） ============
old5 = re.search(r"      return '<tr><td>' \+ \(idx \+ 1\) \+ '</td>'.*?\+ '<td class=\"ops sticky-op\"><a>删除</a></td></tr>';", N, re.S)
assert old5, 'poSoPick 模板锚点异常'
new5 = ("""      return '<tr><td>' + (idx + 1) + '</td>'
        + '<td><select data-prod-key style="%s"></select></td>'
        + '<td><select data-prod-name style="%s"></select></td>'
        + '<td><input data-spec value=""></td>'
        + '<td><select data-unit style="%s"></select></td>'
        + '<td class="td-num"><input data-tax="qty" value="' + String(mth[2]).replace(/,/g, '') + '"></td>'
        + '<td class="td-num"><input data-tax="excl" value=""></td>'
        + '<td><select data-tax="rate" style="width:80px;"></select></td>'
        + '<td class="td-num"><input data-tax="incl" value=""></td>'
        + '<td class="td-num auto-cell" data-tax="amt"></td>'
        + '<td class="ops sticky-op"><a>删除</a></td></tr>';""" % (CELL, CELL, CELL))
N = N[:old5.start()] + new5 + N[old5.end():]
# 生成后渲染新行
old5b = """    }).join('') || poSoDefaultRows;
  }"""
assert N.count(old5b) == 1
N = N.replace(old5b, """    }).join('') || poSoDefaultRows;
    renderRows();
  }""")
print('[5] poSoPick 模板同步 + 生成后调用 renderRows()')

# ============ 6. 替换 poToggleQj 脚本为字典/联动脚本 ============
old6 = re.search(r'<script>\s*function poToggleQj\(sel\) \{.*?\}\s*</script>', N, re.S)
assert old6, 'poToggleQj 脚本锚点异常'
new6 = '''<script src="../_data/demo-data.js"></script>
<script>
/* ===== 数据字典与物料档案取值（D-127：选项一律取自字典，不写死） ===== */
function dictOpts(cat) {
  var D = (window.DEMO_DATA || {}).dictItems || {};
  return Object.keys(D).filter(function (k) {
    var f = (D[k].row || {}).fields || {};
    return f.category === cat && f.status !== '停用';
  }).sort().map(function (k) { return ((D[k].row || {}).fields || {}).name; }).filter(Boolean);
}
function prodKeys() { return Object.keys((window.DEMO_DATA || {}).products || {}); }
function prodFields(k) { var P = (window.DEMO_DATA || {}).products || {}; return ((P[k] || {}).row || {}).fields || {}; }

/* 明细行：填充四个下拉并按 key 选中 + 带出规格 */
function renderRow(tr, key) {
  var keys = prodKeys();
  var kk = key || (tr.getAttribute('data-key') || (keys[0] || ''));
  tr.setAttribute('data-key', kk);
  var sk = tr.querySelector('select[data-prod-key]');
  var sn = tr.querySelector('select[data-prod-name]');
  var su = tr.querySelector('select[data-unit]');
  var sr = tr.querySelector('select[data-tax="rate"]');
  if (sk) sk.innerHTML = keys.map(function (k) { return '<option value="' + k + '"' + (k === kk ? ' selected' : '') + '>' + k + '</option>'; }).join('');
  if (sn) sn.innerHTML = keys.map(function (k) { return '<option value="' + k + '"' + (k === kk ? ' selected' : '') + '>' + (prodFields(k).name || k) + '</option>'; }).join('');
  if (su) { var us = dictOpts('计量单位'); var u0 = prodFields(kk).unit || us[2] || us[0]; su.innerHTML = us.map(function (u) { return '<option' + (u === u0 ? ' selected' : '') + '>' + u + '</option>'; }).join(''); }
  if (sr) sr.innerHTML = dictOpts('供应商税率').map(function (r) { return '<option' + (r === '13%' ? ' selected' : '') + '>' + r + '</option>'; }).join('');
}
function renderRows() {
  document.querySelectorAll('.edit-tbl tbody tr').forEach(function (tr) { renderRow(tr); });
}
/* 表头「物料类型」下拉（字典驱动） */
(function () {
  var mt = document.getElementById('cmMtype');
  if (mt) mt.innerHTML = dictOpts('物料类型').map(function (n) { return '<option>' + n + '</option>'; }).join('');
})();
/* 物料编码 ↔ 物料名称 双向联动 + 带出规格（任一变化，另一字段自动变更） */
document.addEventListener('change', function (e) {
  var el = e.target;
  if (!el.matches || !el.matches('select[data-prod-key], select[data-prod-name]')) return;
  var tr = el.closest('tr'); if (!tr) return;
  renderRow(tr, el.value);
  var sp = tr.querySelector('input[data-spec]');
  if (sp) sp.value = prodFields(el.value).spec || '';
});
window.addEventListener('load', renderRows);
renderRows();
</script>'''
N = N[:old6.start()] + new6 + N[old6.end():]
print('[6] 新增字典/联动脚本，删除 poToggleQj')

# ============ 7. 税率三件套脚本适配（select 触发 change，且不再限定 input） ============
old7a = "    if (!i.matches || !i.matches('input[data-tax]')) return;"
assert N.count(old7a) == 1, '税率脚本 matches 锚点异常'
N = N.replace(old7a, "    if (!i.matches || !i.matches('[data-tax]')) return;")
old7b = """    function q(r){ var el = tr.querySelector('input[data-tax="'+r+'"]'); return el ? String(el.value).replace(/,/g,'') : '0'; }"""
assert N.count(old7b) == 1, 'q() 锚点异常'
N = N.replace(old7b, """    function q(r){ var el = tr.querySelector('[data-tax="'+r+'"]'); return el ? String(el.value).replace(/,/g,'') : '0'; }""")
old7c = """  document.addEventListener('input', function (e) {
    var i = e.target;"""
assert N.count(old7c) == 1, '监听锚点异常'
N = N.replace(old7c, """  function taxRecalc(e) {
    var i = e.target;""")
old7d = """    if (amt) { var v = (num(q('qty')) * num(q('incl'))).toLocaleString('zh-CN', {minimumFractionDigits: 2, maximumFractionDigits: 2}); if (amt.tagName === 'INPUT') amt.value = v; else amt.textContent = v; }
  });
})();"""
assert N.count(old7d) == 1, '税额计算锚点异常'
N = N.replace(old7d, """    if (amt) { var v = (num(q('qty')) * num(q('incl'))).toLocaleString('zh-CN', {minimumFractionDigits: 2, maximumFractionDigits: 2}); if (amt.tagName === 'INPUT') amt.value = v; else amt.textContent = v; }
  }
  document.addEventListener('input', taxRecalc);
  document.addEventListener('change', taxRecalc);
})();""")
print('[7] 税率三件套适配：select 触发 change + 选择器放开到 [data-tax]')

# ============ 写出 ============
io.open(N_P, 'w', encoding='utf-8', newline='').write(N.replace('\r\n', '\n').replace('\n', '\r\n'))
print(f'[写出] {N_P} —— {len(N)} 字符')
