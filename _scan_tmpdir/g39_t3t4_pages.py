# -*- coding: utf-8 -*-
"""G39 T3+T4 · 页面与渲染器改造（精确替换＋断言＋幂等）
  1) 租入单新建：计费方式值域/列头联动/随料带出/参考价带出/起租+天数
  2) 租赁单新建：明细+计费方式列/联动/带出/起租日期行
  3) 租赁出库录单：+计费方式静态列（bomList 带出结果态）+价格列头
  4) 采购订单新建：参考未税采购价带出（change 监听扩展）
  5) 销售订单新建：参考未税销售价带出（新增监听）
  6) 应收/应付详情渲染器：segCols 期段化分支（历史账单走原 5 列·不回改）
"""
import io, re

ROOT = r'P3-R01-包装租赁管理后台原型'

def rd(p):
    return io.open(ROOT + '\\' + p, 'rb').read().decode('utf-8')

def wr(p, s):
    io.open(ROOT + '\\' + p, 'wb').write(s.encode('utf-8'))

def rep1(s, old, new, tag):
    assert s.count(old) == 1, '[%s] anchor=%d : %r' % (tag, s.count(old), old[:60])
    return s.replace(old, new)

# ============ 1) 租入管理/租入单新建.html ============
P = r'租入管理\租入单新建.html'
s = rd(P)
if 'g39PriceTh' not in s:
    s = rep1(s, '<div class="pn-hint">多物料 · 计费方式：按月 / 按次</div>',
             '<div class="pn-hint">多物料 · 计费方式：按时间周期 / 按次（按时间周期直录日租金 · 按次录次单价 · 列头联动）</div>', P+'-hint')
    s = rep1(s, '<option selected>按月</option><option>按次</option>',
             '<option selected>按时间周期</option><option>按次</option>', P+'-opt')
    s = rep1(s, '<th data-note="1">计费方式</th><th>未税单价(元)</th>',
             '<th data-note="1">计费方式</th><th id="g39PriceTh">日租金(元/天)</th>', P+'-th')
    # 计费方式 select 加 class
    s = rep1(s, '<select style="width:88px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;"><option selected>按时间周期</option>',
             '<select class="g39mode" style="width:104px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;"><option selected>按时间周期</option>', P+'-modeclass')
    # 物料 select 加 class（首个明细行）
    s = rep1(s, '<select style="width:100%;min-width:0;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;"><option selected>WBX-1210L',
             '<select class="g39mat" style="width:100%;min-width:0;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;"><option selected>WBX-1210L', P+'-matclass')
    # 参考价带出结果态（WBX-1210L 参考未税租入价 45.00·不换算直录）
    s = rep1(s, '<td><input data-tax="excl" value="400.00"></td>', '<td><input data-tax="excl" value="45.00"></td>', P+'-excl')
    s = rep1(s, '<td><input data-tax="incl" value="452.00"></td>', '<td><input data-tax="incl" value="50.85"></td>', P+'-incl')
    s = rep1(s, 'value="13,560.00"', 'value="1,525.50"', P+'-amt')
    # 起租日期行 → 起租+计租天数+止租自动
    s = rep1(s, '<div class="input-box" style="width:380px;"><input type="date" value="2026-09-03"></div><span style="font-size:12px;color:#8c8c8c;">单据起止只填开始时间，结束日期不填（D-117 两层租期）</span>',
             '<div class="input-box" style="width:170px;"><input type="date" id="g39Start" value="2026-09-03"></div><div class="form-label" style="width:auto;min-width:96px;"><span class="req">*</span>计租天数：</div><div class="input-box" style="width:104px;"><input id="g39Days" value="30"></div><span id="g39RentHint" style="font-size:12px;color:#8c8c8c;">止租日期 2026-10-02（自动＝起租＋天数−1 · 当天起当天退＝2 天）</span>', P+'-rentrow')
    JS = '''<script>
/* G39 · 计费方式随料带出＋列头联动＋参考价带出＋起租天数（D-148） */
(function () {
  function pf(code) { try { return ((window.DEMO_DATA.products || {})[code] || {}).row.fields || null; } catch (e) { return null; } }
  function syncHead(v) { var t = document.getElementById('g39PriceTh'); if (t) t.textContent = v === '按次' ? '次单价(元/次)' : '日租金(元/天)'; }
  function recalc(tr) {
    var ex = tr.querySelector('input[data-tax="excl"]'), rt = tr.querySelector('input[data-tax="rate"]'), inc = tr.querySelector('input[data-tax="incl"]'), amt = tr.querySelector('input[data-tax="amt"]'), q = tr.querySelector('input[data-tax="qty"]');
    if (!ex) return;
    var r = parseFloat(String(rt && rt.value).replace('%', '')) / 100 || 0;
    var iv = parseFloat(ex.value) * (1 + r);
    if (inc) inc.value = iv.toFixed(2);
    if (amt && q) amt.value = (parseFloat(String(q.value).replace(/,/g, '')) * iv).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  document.querySelectorAll('.edit-tbl tr').forEach(function (tr) {
    var mat = tr.querySelector('select.g39mat'), mode = tr.querySelector('select.g39mode');
    if (!mat || !mode) return;
    mode.addEventListener('change', function () { syncHead(mode.value); });
    mat.addEventListener('change', function () {
      var f = pf(String(mat.value).split(' ')[0]);
      if (!f) return;
      if (f.rentInMode === '按次') mode.value = '按次'; else if (f.rentInMode) mode.value = '按时间周期';
      syncHead(mode.value);
      if (f.rentInPrice && f.rentInPrice !== '—') { ex = tr.querySelector('input[data-tax="excl"]'); if (ex) { ex.value = f.rentInPrice; recalc(tr); } }
    });
  });
  var m0 = document.querySelector('select.g39mode'); if (m0) syncHead(m0.value);
  var sd = document.getElementById('g39Start'), dd = document.getElementById('g39Days'), hint = document.getElementById('g39RentHint');
  function syncRent() {
    if (!sd || !dd || !hint || !sd.value) return;
    var d = Math.max(2, parseInt(dd.value, 10) || 2); dd.value = d;
    var t = new Date(sd.value + 'T00:00:00'); t.setDate(t.getDate() + d - 1);
    var p = function (x) { return (x < 10 ? '0' : '') + x; };
    hint.textContent = '止租日期 ' + t.getFullYear() + '-' + p(t.getMonth() + 1) + '-' + p(t.getDate()) + '（自动＝起租＋天数−1 · 当天起当天退＝2 天）';
  }
  if (sd) { sd.addEventListener('change', syncRent); dd.addEventListener('input', syncRent); syncRent(); }
})();
</script>
'''
    assert s.count('</body>') == 1
    s = s.replace('</body>', JS + '</body>')
    wr(P, s)
    print('[1] 租入单新建 OK')

# ============ 2) 租赁管理/租赁单新建.html ============
P = r'租赁管理\租赁单新建.html'
s = rd(P)
if 'g39PriceTh' not in s:
    s = rep1(s, '<th>数量</th><th style="font-size:13.5px;font-weight:700;">未税单价(元)</th>',
             '<th>数量</th><th>计费方式</th><th style="font-size:13.5px;font-weight:700;" id="g39PriceTh">日租金(元/天)</th>', P+'-th')
    MODE_TD1 = '<td><select class="g39mode" style="width:104px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;"><option selected>按时间周期</option><option>按次</option></select></td>'
    s = rep1(s, '<td><input data-tax="qty" value="180"></td><td><input data-tax="excl" value="2.40"></td>',
             '<td><input data-tax="qty" value="180"></td>' + MODE_TD1 + '<td><input data-tax="excl" value="2.40"></td>', P+'-r1')
    s = rep1(s, '<td><input data-tax="qty" value="180"></td><td><input data-tax="excl" value="0.15"></td>',
             '<td><input data-tax="qty" value="180"></td>' + MODE_TD1 + '<td><input data-tax="excl" value="0.15"></td>', P+'-r2')
    s = rep1(s, '<td colspan="7" style="text-align:right;font-weight:700;">租赁总价', '<td colspan="8" style="text-align:right;font-weight:700;">租赁总价', P+'-foot')
    # 两个物料 select 加 class（计数=2）
    OLDMAT = '<select style="width:100%;min-width:0;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;">'
    assert s.count(OLDMAT) == 2, s.count(OLDMAT)
    s = s.replace(OLDMAT, '<select class="g39mat" style="width:100%;min-width:0;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;">')
    # 起租日期行（计费方式行前插·CRLF 混合行尾页面）
    ANCH = '  </div>\r\n  <div class="form-row">\r\n    <div class="form-label"><span class="req" data-note="2">*</span>计费方式：</div>'
    NEWROW = '''  </div>
  <div class="form-row">
    <div class="form-label">起租日期：</div>
    <div class="input-box" style="width:380px;"><input type="date" value="2026-09-06"><span style="font-size:12px;color:#8c8c8c;">　＝首笔租赁出库「发货审核完成日」；止租＝退租入库「验收完成日」·当日仍计租·最低 2 天（D-148）</span></div>
  </div>
  <div class="form-row">
    <div class="form-label"><span class="req" data-note="2">*</span>计费方式：</div>'''.replace('\n', '\r\n')
    s = rep1(s, ANCH, NEWROW, P+'-rentrow')
    JS = '''<script>
/* G39 · 租赁明细：计费方式随料带出（组合件取 bomList）＋列头联动＋参考价带出（单件·组合件租价手填）（D-148） */
(function () {
  function pf(code) { try { return ((window.DEMO_DATA.products || {})[code] || {}).row.fields || null; } catch (e) { return null; } }
  function bf(code) { try { return ((window.DEMO_DATA.bomList || {})[code] || {}).row.fields || null; } catch (e) { return null; } }
  function syncHead(v) { var t = document.getElementById('g39PriceTh'); if (t) t.textContent = v === '按次' ? '次单价(元/次)' : '日租金(元/天)'; }
  function recalc(tr) {
    var ex = tr.querySelector('input[data-tax="excl"]'), rt = tr.querySelector('input[data-tax="rate"]'), inc = tr.querySelector('input[data-tax="incl"]'), amt = tr.querySelector('input[data-tax="amt"]'), q = tr.querySelector('input[data-tax="qty"]');
    if (!ex) return;
    var r = parseFloat(String(rt && rt.value).replace('%', '')) / 100 || 0;
    var iv = parseFloat(ex.value) * (1 + r);
    if (inc) inc.value = iv.toFixed(2);
    if (amt && q) amt.value = (parseFloat(String(q.value).replace(/,/g, '')) * iv).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  document.querySelectorAll('.edit-tbl tr').forEach(function (tr) {
    var mat = tr.querySelector('select.g39mat'), mode = tr.querySelector('select.g39mode');
    if (!mat || !mode) return;
    mode.addEventListener('change', function () { syncHead(mode.value); });
    mat.addEventListener('change', function () {
      var code = String(mat.value).split(' ')[0], f = pf(code);
      if (f) {
        if (f.rentalMode === '按次') mode.value = '按次'; else if (f.rentalMode) mode.value = '按时间周期';
        syncHead(mode.value);
        if (f.rentalPrice && f.rentalPrice !== '—') { var ex = tr.querySelector('input[data-tax="excl"]'); if (ex) { ex.value = f.rentalPrice; recalc(tr); } }
      } else {
        var b = bf(code);
        if (b && b.billing) { mode.value = b.billing; syncHead(mode.value); }
      }
    });
  });
  var m0 = document.querySelector('select.g39mode'); if (m0) syncHead(m0.value);
})();
</script>
'''
    assert s.count('</body>') == 1
    s = s.replace('</body>', JS + '</body>')
    wr(P, s)
    print('[2] 租赁单新建 OK')

# ============ 3) 租赁管理/租赁出库录单.html ============
P = r'租赁管理\租赁出库录单.html'
s = rd(P)
if '<th>计费方式</th>' not in s:
    s = rep1(s, '<th>组合件名称</th><th style="width:110px;">出库数量 *</th>', '<th>组合件名称</th><th>计费方式</th><th style="width:110px;">出库数量 *</th>', P+'-th')
    CTL = '<td><div class="ctl sel" style="min-width:96px;"><span class="v">按时间周期</span><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></div></td>'
    s = rep1(s, '<td>驾驶室围板箱整箱套件</td>', '<td>驾驶室围板箱整箱套件</td>' + CTL, P+'-r1')
    s = rep1(s, '<td>冲压件料箱组套</td>', '<td>冲压件料箱组套</td>' + CTL, P+'-r2')
    s = rep1(s, '<th style="font-size:13.5px;font-weight:700;">未税单价(元)</th>', '<th style="font-size:13.5px;font-weight:700;">日租金(元/天)</th>', P+'-price-th')
    wr(P, s)
    print('[3] 租赁出库录单 OK')

# ============ 4) 采购管理/采购订单新建.html ============
P = r'采购管理\采购订单新建.html'
s = rd(P)
if 'G39' not in s:
    ANCH_LF = "  var sp = tr.querySelector('input[data-spec]');\n  if (sp) sp.value = prodFields(el.value).spec || '';"
    ANCH = ANCH_LF.replace('\n', '\r\n') if s.count(ANCH_LF) == 0 else ANCH_LF
    NEW = ANCH + """
  /* G39 · 参考价带出且可改（D-148）：按参考未税采购价预填 */
  var bp = prodFields(el.value).buyPrice;
  var ex = tr.querySelector('input[data-tax="excl"]');
  if (ex && bp && bp !== '—') {
    ex.value = bp;
    var rsel = tr.querySelector('select[data-tax="rate"]');
    var r = parseFloat(String(rsel && rsel.value).replace('%', '')) / 100 || 0.13;
    var inc = tr.querySelector('input[data-tax="incl"]');
    if (inc) inc.value = (parseFloat(bp) * (1 + r)).toFixed(2);
    var amt = tr.querySelector('input[data-tax="amt"]');
    var q = tr.querySelector('input[data-tax="qty"]');
    if (amt && q) amt.value = (parseFloat(String(q.value).replace(/,/g, '')) * parseFloat(bp) * (1 + r)).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }"""
    if s.count(ANCH) == 1:
        s = s.replace(ANCH, NEW)
        wr(P, s)
        print('[4] 采购订单新建 OK（change 监听扩展）')
    else:
        print('[4] 采购订单新建 ANCH count =', s.count(ANCH), '（跳过记失败）')

# ============ 5) 销售管理/销售订单新建.html ============
P = r'销售管理\销售订单新建.html'
s = rd(P)
if 'g39SaleRef' not in s:
    JS = '''<script>
/* G39 · 参考价带出且可改（D-148）：销售明细按参考未税销售价预填 */
(function () {
  function pf(code) { try { return ((window.DEMO_DATA.products || {})[code] || {}).row.fields || null; } catch (e) { return null; } }
  function g39SaleRef(e) {
    var el = e.target;
    if (!el.matches || !el.matches('select[data-tax="prod"]')) return;
    var tr = el.closest('tr'); if (!tr) return;
    var f = pf(String(el.value).split(' ')[0]);
    if (!f || !f.salePrice || f.salePrice === '—') return;
    var ex = tr.querySelector('input[data-tax="excl"]');
    if (!ex) return;
    ex.value = f.salePrice;
    var rt = tr.querySelector('input[data-tax="rate"]') || tr.querySelector('select[data-tax="rate"]');
    var r = parseFloat(String(rt && rt.value).replace('%', '')) / 100 || 0.13;
    var inc = tr.querySelector('input[data-tax="incl"]');
    if (inc) inc.value = (parseFloat(f.salePrice) * (1 + r)).toFixed(2);
    var amt = tr.querySelector('input[data-tax="amt"]'), q = tr.querySelector('input[data-tax="qty"]');
    if (amt && q) amt.value = (parseFloat(String(q.value).replace(/,/g, '')) * parseFloat(f.salePrice) * (1 + r)).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  document.addEventListener('change', g39SaleRef);
})();
</script>
'''
    assert s.count('</body>') == 1
    s = s.replace('</body>', JS + '</body>')
    wr(P, s)
    print('[5] 销售订单新建 OK')

# ============ 6) 应收详情渲染器 segCols 期段化分支 ============
P = r'_data\receivable-bill-detail.js'
s = rd(P)
if 'segCols' not in s:
    OLD = """    h += '<div class="dt-sec">费用明细</div>' +
      '<div class="table-wrap"><table><thead><tr><th>来源单据</th><th>费用说明</th><th class="td-num">数量</th><th class="td-num">单价(元)</th><th class="td-num">金额(元)</th></tr></thead><tbody>';
    b.fees.forEach(function (f) {
      h += '<tr><td>' + (f.url ? lk(f.src, f.url, base) : f.src) + '</td><td>' + f.desc +
        '</td><td class="td-num">' + f.qty + '</td><td class="td-num">' + f.price +
        '</td><td class="td-num">' + fmt(f.amount) + '</td></tr>';
    });
    h += '</tbody></table></div>';"""
    NEW = """    h += '<div class="dt-sec">费用明细</div>';
    if (b.segCols) {
      /* G39 期段化明细（D-148）：起租日期|止租日期|天数|日单价|小计（按持有量×天数） */
      h += '<div class="table-wrap"><table><thead><tr>' +
        b.segCols.map(function (c) { return '<th>' + c + '</th>'; }).join('') + '</tr></thead><tbody>';
      b.fees.forEach(function (f) {
        h += '<tr>' + (f.cells || []).map(function (c, i) {
          return '<td' + (i >= b.segCols.length - 2 ? ' class="td-num"' : '') + '>' + c + '</td>';
        }).join('') + '</tr>';
      });
      h += '</tbody></table></div>';
    } else {
      h += '<div class="table-wrap"><table><thead><tr><th>来源单据</th><th>费用说明</th><th class="td-num">数量</th><th class="td-num">单价(元)</th><th class="td-num">金额(元)</th></tr></thead><tbody>';
      b.fees.forEach(function (f) {
        h += '<tr><td>' + (f.url ? lk(f.src, f.url, base) : f.src) + '</td><td>' + f.desc +
          '</td><td class="td-num">' + f.qty + '</td><td class="td-num">' + f.price +
          '</td><td class="td-num">' + fmt(f.amount) + '</td></tr>';
      });
      h += '</tbody></table></div>';
    }"""
    assert s.count(OLD) == 1, 'receivable fees block=%d' % s.count(OLD)
    s = s.replace(OLD, NEW)
    wr(P, s)
    print('[6a] 应收渲染器 segCols OK')

# ============ 7) 应付详情渲染器 segCols 分支 ============
P = r'_data\payable-bill-detail.js'
s = rd(P)
if 'segCols' not in s:
    # 读出旧块（金额三列版）
    m = re.search(r"    h \+= '<div class=\"dt-sec\">费用明细</div>' \+\r?\n.*?h \+= '</tbody></table></div>';", s, re.S)
    assert m, 'payable fees block not found'
    OLD = m.group(0)
    OLD_BODY = OLD
    # 提取 legacy forEach 内核（保持不变），包进 else
    NEW = """    h += '<div class="dt-sec">费用明细</div>';
    if (b.segCols) {
      /* G39 期段化明细（D-148）：起租日期|止租日期|天数|日单价|小计（按持有量×天数） */
      h += '<div class="table-wrap"><table><thead><tr>' +
        b.segCols.map(function (c) { return '<th>' + c + '</th>'; }).join('') + '</tr></thead><tbody>';
      b.fees.forEach(function (f) {
        h += '<tr>' + (f.cells || []).map(function (c, i) {
          return '<td' + (i >= b.segCols.length - 2 ? ' class="td-num"' : '') + '>' + c + '</td>';
        }).join('') + '</tr>';
      });
      h += '</tbody></table></div>';
    } else {
""" + '\n'.join('  ' + ln if ln.strip() else ln for ln in OLD_BODY.split('\n')[1:]) + """
    }"""
    s = s.replace(OLD, NEW)
    wr(P, s)
    print('[7] 应付渲染器 segCols OK')

print('=== T3+T4 页面/渲染器改造完成 ===')
