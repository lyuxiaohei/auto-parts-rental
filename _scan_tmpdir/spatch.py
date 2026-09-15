# -*- coding: utf-8 -*-
"""销售出库接入出货单打印页：打印页双实体 + demo-data 6 行 + 静态行 6 处"""
import io, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
FAILS = []
def rd(p):
    return io.open(ROOT + '\\' + p, encoding='utf-8', newline='').read()
def wr(p, t):
    io.open(ROOT + '\\' + p, 'w', encoding='utf-8', newline='').write(t)

PLACE_JS = "window.print();this.classList.toggle('printed')"

# ---------- 1. 打印页双实体 ----------
p = r'租赁管理\出货单打印.html'
t = rd(p)
OLD_BLOCK = """(function () {
  var D = (window.DEMO_DATA || {}).comboOutbounds || {};
  var BOM = (window.DEMO_DATA || {}).bomList || {};
  var key = decodeURIComponent((location.search.match(/[?&]key=([^&]+)/) || [])[1] || '');
  var rec = D[key] || {};
  var f = rec.row ? (rec.row.fields || {}) : {};
  var first = Object.keys(D)[0];
  if (!rec.row && first) { key = first; rec = D[key] || {}; f = rec.row ? rec.row.fields : {}; }"""
NEW_BLOCK = """(function () {
  /* D-144 扩展：租赁出库（comboOutbounds·key=CK-）与销售出库（salesOutbounds·key=XSCK-）双实体自动识别 */
  var D = (window.DEMO_DATA || {}).comboOutbounds || {};
  var D2 = (window.DEMO_DATA || {}).salesOutbounds || {};
  var BOM = (window.DEMO_DATA || {}).bomList || {};
  var key = decodeURIComponent((location.search.match(/[?&]key=([^&]+)/) || [])[1] || '');
  var rec = D[key] || {};
  var isSales = false;
  if (!(rec.row || {}).fields && (D2[key] || {}).row) { rec = D2[key]; isSales = true; }
  var f = rec.row ? (rec.row.fields || {}) : {};
  var first = Object.keys(D)[0];
  if (!rec.row && first) { key = first; rec = D[key] || {}; f = rec.row ? rec.row.fields : {}; }"""
if 'isSales' in t:
    print('打印页已是双实体，跳过')
else:
    assert t.count(OLD_BLOCK) == 1, '打印页头锚=%d' % t.count(OLD_BLOCK)
    t = t.replace(OLD_BLOCK, NEW_BLOCK)
    OLD_DETAIL = """  /* 明细行：组合件「ZH-xxx × N 套」→ 编码/名称/数量；固定 3 行（不足补空行） */
  var combo = String(f.combo || '');
  var parts = combo.split('×');
  var code = (parts[0] || '').trim();
  var qty = ((parts[1] || '').match(/\\d+/) || [''])[0];
  var brec = BOM[code] || {};
  var name = (brec.row && brec.row.fields && brec.row.fields.name) ? brec.row.fields.name : code;
  var desc = code ? (name + (qty ? ('（' + qty + ' 套）') : '')) : '—';
  var so = String(f.so || '');
  var rows = [];
  if (code) {
    rows.push({ no: 1, so: so.indexOf('—') === 0 ? '—' : so, desc: desc, qty: qty || '—', memo: '1托' });
  }"""
    NEW_DETAIL = """  /* 明细行：租赁=组合件「ZH-xxx × N 套」→ BOM 名称+套数；销售=summary 摘要+cells 数量列；固定 3 行（不足补空行） */
  var rows = [];
  if (isSales) {
    var scells = (rec.row.cells || []).map(function (c) { return String(c).replace(/<[^>]+>/g, ''); });
    var sqty = (scells[4] || '').replace(/,/g, '').trim();
    var sso = String(f.so || '');
    rows.push({ no: 1, so: sso, desc: String(f.summary || '—'), qty: sqty || '—', memo: '1托' });
  } else {
    var combo = String(f.combo || '');
    var parts = combo.split('×');
    var code = (parts[0] || '').trim();
    var qty = ((parts[1] || '').match(/\\d+/) || [''])[0];
    var brec = BOM[code] || {};
    var name = (brec.row && brec.row.fields && brec.row.fields.name) ? brec.row.fields.name : code;
    var desc = code ? (name + (qty ? ('（' + qty + ' 套）') : '')) : '—';
    var so = String(f.so || '');
    if (code) {
      rows.push({ no: 1, so: so.indexOf('—') === 0 ? '—' : so, desc: desc, qty: qty || '—', memo: '1托' });
    }
  }"""
    assert t.count(OLD_DETAIL) == 1, '打印页明细锚=%d' % t.count(OLD_DETAIL)
    t = t.replace(OLD_DETAIL, NEW_DETAIL)
    wr(p, t)
    print('打印页双实体改造完成')

# ---------- 2. demo-data salesOutbounds 6 行 ----------
p = r'_data\demo-data.js'
t = rd(p)
eol = '\r\n' if '\r\n' in t else '\n'
lines = t.split(eol)
i0 = next(i for i, l in enumerate(lines) if l.startswith('  salesOutbounds: {'))
i1 = next(i for i, l in enumerate(lines) if i > i0 and l == '  },')
cur_key = None
rep = 0
for idx in range(i0, i1 + 1):
    l = lines[idx]
    km = re.match(r"    '([A-Z][A-Z0-9-]+)': \{", l)
    if km:
        cur_key = km.group(1)
        continue
    if not cur_key:
        continue
    if PLACE_JS in l and 'XSCK' not in l:
        lines[idx] = l.replace(PLACE_JS, "go('../租赁管理/出货单打印.html?key=%s')" % cur_key, 1)
        rep += 1
print('demo-data salesOutbounds 替换:', rep)
if rep != 6:
    FAILS.append(('demo', p, 'rep=%d expect 6' % rep))
else:
    wr(p, eol.join(lines))

# ---------- 3. 销售出库列表静态行 ----------
p = r'销售管理\销售出库列表.html'
t = rd(p)
eol = '\r\n' if '\r\n' in t else '\n'
lines = t.split(eol)
cur_ck = None
rep2 = 0
for idx, l in enumerate(lines):
    km = re.search(r'<span class="lk">(XSCK-[0-9-]+)</span>', l)
    if km:
        cur_ck = km.group(1)
    if 'printed' in l and '打印出货单' in l and cur_ck:
        old = "<a onclick=\"window.print();this.classList.toggle('printed')\">打印出货单</a>"
        new = "<a onclick=\"go('../租赁管理/出货单打印.html?key=%s')\">打印出货单</a>" % cur_ck
        if old in l:
            lines[idx] = l.replace(old, new, 1)
            rep2 += 1
print('销售出库静态行替换:', rep2)
residual = eol.join(lines).count(PLACE_JS)
if rep2 != 6 or residual:
    FAILS.append(('static', p, 'rep=%d residual=%d' % (rep2, residual)))
else:
    wr(p, eol.join(lines))

for f in FAILS:
    print('FAIL:', f)
print('DONE' if not FAILS else 'HAS FAILS')
