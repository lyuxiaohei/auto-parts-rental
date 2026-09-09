# -*- coding: utf-8 -*-
"""批3 Script C2：list-generic contains 支持 + 分期计划块（应付账单卡 + 付款登记新建双层）"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"
LOG = []

# 1. list-generic.js select 支持 match:'contains'
lg = PROTO / '_data' / 'list-generic.js'
txt = lg.read_bytes().decode('utf-8')
old_sel = """          if (v && v !== '全部') preds.push(function (r) { return String(r.fields[f.field]) === v; });"""
new_sel = """          if (v && v !== '全部') preds.push(function (r) {
            var fv = String(r.fields[f.field] || '');
            return f.match === 'contains' ? fv.indexOf(v) > -1 : fv === v;
          });"""
c = txt.count(old_sel)
assert c == 1, c
lg.write_bytes(txt.replace(old_sel, new_sel).encode('utf-8'))
LOG.append('list-generic.js select 支持 match:contains')

INST_HTML = '''<div class="card" id="instCard">
  <div class="card-head">
    <h3 class="card-title">分期计划（C-C/D · 比例⇄金额互算）</h3>
    <div class="head-btns">
      <select id="instN" style="border:1px solid #d9d9d9;border-radius:4px;padding:2px 6px;font:inherit;">
        <option value="1">分 1 期</option><option value="2" selected>分 2 期</option><option value="3">分 3 期</option>
      </select>
      <input id="instBase" value="68,400.00" style="border:1px solid #d9d9d9;border-radius:4px;padding:2px 8px;font:inherit;width:120px;text-align:right;" title="账单金额">
    </div>
  </div>
  <div class="table-wrap">
    <table>
      <thead><tr><th>期次</th><th>比例(%)</th><th>金额(元)</th><th>计划日期</th><th>状态</th></tr></thead>
      <tbody id="instBody"></tbody>
    </table>
  </div>
  <div class="pn-hint">分期互算：填比例自动算金额、填金额自动算比例，末期自动补差；账单头部展示「账单金额 / 已付 / 剩余」，付款时选金额，超出账单金额拦截（2026-09-08 会议 M2/C-C）。</div>
</div>
<script>/*C-C/D 分期比例⇄金额互算 · meeting0908 批3*/
(function () {
  function num(v){ var x = parseFloat(String(v).replace(/,/g,'')); return isNaN(x)?0:x; }
  function fmt(x){ return x.toLocaleString('zh-CN', {minimumFractionDigits:2, maximumFractionDigits:2}); }
  function base(){ var el = document.getElementById('INSTBASE'); return el ? num(el.value) : 0; }
  function n(){ var el = document.getElementById('INSTN'); return el ? parseInt(el.value,10) : 2; }
  function render() {
    var tb = document.getElementById('INSTBODY'); if (!tb) return;
    var rows = '', plans = ['2026-09-20', '2026-10-20', '2026-11-20'], N = n();
    var defs = N === 1 ? [100] : N === 2 ? [60, 40] : [40, 30, 30];
    for (var i = 0; i < N; i++) {
      var last = i === N - 1;
      rows += '<tr><td>第 ' + (i+1) + ' 期' + (last && N > 1 ? '（末期 · 自动补差）' : '') + '</td>'
        + '<td><input data-i="' + i + '" data-k="rate" value="' + defs[i].toFixed(2) + '" style="width:76px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 6px;"></td>'
        + '<td><input data-i="' + i + '" data-k="amt" value="' + fmt(base() * defs[i] / 100) + '" style="width:110px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 6px;text-align:right;"></td>'
        + '<td>' + plans[i] + '</td><td>' + (i === 0 ? '<span class="tag tag-orange">待付款</span>' : '<span class="tag tag-gray">未开始</span>') + '</td></tr>';
    }
    rows += '<tr><td style="font-weight:700;text-align:right;" colspan="2">合计（不得超账单金额，超出拦截）</td><td class="td-num" style="font-weight:700;" colspan="3">' + fmt(base()) + '</td></tr>';
    tb.innerHTML = rows;
  }
  document.addEventListener('input', function (e) {
    var i = e.target;
    if (!i.matches || !i.matches('#INSTCARD input[data-i]')) return;
    var idx = parseInt(i.getAttribute('data-i'), 10), kind = i.getAttribute('data-k');
    var tb = document.getElementById('INSTBODY'); if (!tb) return;
    var N = n(), b = base();
    var rates = [], amts = [], k, el;
    for (k = 0; k < N; k++) {
      var r = tb.querySelector('input[data-i="' + k + '"][data-k="rate"]');
      var a = tb.querySelector('input[data-i="' + k + '"][data-k="amt"]');
      rates.push(num(r.value)); amts.push(num(a.value));
    }
    if (kind === 'rate') { rates[idx] = num(i.value); amts[idx] = b * rates[idx] / 100; }
    else { amts[idx] = num(i.value); rates[idx] = b > 0 ? amts[idx] / b * 100 : 0; }
    if (N > 1) { /* 末期补差 */
      var rest = 0;
      for (k = 0; k < N - 1; k++) { rest += amts[k]; }
      amts[N-1] = Math.max(0, b - rest); rates[N-1] = b > 0 ? amts[N-1] / b * 100 : 0;
    }
    for (k = 0; k < N; k++) {
      el = tb.querySelector('input[data-i="' + k + '"][data-k="rate"]'); if (el) el.value = rates[k].toFixed(2);
      el = tb.querySelector('input[data-i="' + k + '"][data-k="amt"]'); if (el) el.value = fmt(amts[k]);
    }
    var sum = 0; for (k = 0; k < N; k++) sum += amts[k];
    i.style.borderColor = (sum > b + 0.005) ? '#ff4d4f' : '#d9d9d9';
  });
  document.addEventListener('change', function (e) { if (e.target && e.target.id === 'INSTN') render(); });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render); else render();
})();
</script>'''

# 2. 应付账单页：列表后插分期卡（脚本占位 INST* 替换为正式 id）
f = PROTO / '财务协同' / '应付账单.html'
txt = f.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'
assert '分期计划' not in txt
anchor = '<script src="../_data/demo-data.js"></script>'
assert txt.count(anchor) == 1
inst = INST_HTML
txt = txt.replace(anchor, inst + nl + anchor)
f.write_bytes(txt.encode('utf-8'))
LOG.append('应付账单 分期计划卡+互算JS')

# 3. 付款登记新建（模板 + 内嵌）：createModal body 尾插分期块（modal 版，INST* → INSTM*）
for rel in ['财务协同/弹窗/付款登记新建.html', '财务协同/付款登记.html']:
    f = PROTO / rel
    txt = f.read_bytes().decode('utf-8')
    nl = '\r\n' if '\r\n' in txt else '\n'
    m = re.search(r'(<div class="modal-overlay" id="createModal">.*?)(\n    <div class="modal-footer">)', txt, re.S)
    assert m, rel + ' createModal footer 未找到'
    im = INST_HTML.replace('id="instCard"', 'id="instCardM"').replace('INSTBASE', 'instBaseM').replace('INSTN', 'instNM').replace('INSTBODY', 'instBodyM').replace('INSTCARD', 'instCardM')
    tbl_part = im[im.find('<div class="card-head">'):im.find('<div class="pn-hint">')]
    js_part = im[im.find('<script>'):]
    hint = '<div style="font-size:12px;color:#8c8c8c;margin-top:4px;">填比例算金额 / 填金额算比例；末期自动补差；付款金额超出账单金额拦截（账单金额/已付/剩余 头部展示）。</div>'
    block = ('<div style="margin:12px 0 4px;font-size:13px;font-weight:600;">分期计划（比例⇄金额互算 · 末期补差）</div>' + nl +
             '<div style="display:flex;gap:8px;align-items:center;margin-bottom:6px;">' + tbl_part.replace('<div class="card-head">', '').replace('<h3 class="card-title">分期计划（C-C/D · 比例⇄金额互算）</h3>', '').strip() + '</div>' + nl + hint + nl + js_part + nl)
    txt = txt[:m.end(1)] + nl + block + txt[m.end(1):]
    f.write_bytes(txt.encode('utf-8'))
    LOG.append(f'{rel} 分期块（弹窗内）')

print('== 批3 Script C2 ==')
for l in LOG:
    print(' ✓', l)
