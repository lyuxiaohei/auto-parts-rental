# -*- coding: utf-8 -*-
"""G36 C2（D-130）：库存查询页——项目筛选后五数量列按 qtyByProject 实时重算＋客户在租下钻同步"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
FP = os.path.join(ROOT, '仓储作业', '库存查询.html')
s = io.open(FP, encoding='utf-8', newline='').read()

SCRIPT = '''<script>
/* G36 C2（D-130）：项目筛选后五个数量列按库存实例项目归属（qtyByProject）实时重算；
   各状态列之和=该项目总量；全项目之和=不筛选总数（演示数据已按分摊对平）；客户在租下钻同步按项目口径 */
(function () {
  var drillCache = null;
  function fmt(n) { return Number(n).toLocaleString('zh-CN'); }
  function projVal() {
    var ffs = document.querySelectorAll('.ff');
    for (var i = 0; i < ffs.length; i++) {
      var lb = ffs[i].querySelector('.ff-label');
      if (lb && lb.textContent.indexOf('项目') === 0) {
        var sel = ffs[i].querySelector('select');
        if (sel) return (sel.value === '全部' || !sel.value) ? '' : sel.value;
      }
    }
    return '';
  }
  function shares(key) {
    var r = (((window.DEMO_DATA || {}).stockFlows || {})[key] || {}).row || {};
    return (r.fields || {}).qtyByProject || null;
  }
  function drillTbody() {
    var out = null;
    document.querySelectorAll('table').forEach(function (t) {
      var th = t.querySelector('thead');
      if (th && th.textContent.indexOf('所属项目') > -1 && th.textContent.indexOf('在租数量') > -1) out = t.querySelector('tbody');
    });
    return out;
  }
  function recalcDrill(P) {
    var tb = drillTbody();
    if (!tb) return;
    if (drillCache === null) drillCache = tb.innerHTML;
    if (!P) { tb.innerHTML = drillCache; return; }
    var keep = [];
    Array.prototype.forEach.call(tb.rows, function (tr) {
      var pj = tr.cells[3] ? tr.cells[3].textContent : '';
      if (pj.indexOf(P) === -1) return;
      var key = tr.cells[0] ? tr.cells[0].textContent.trim() : '';
      var sh = shares(key);
      if (sh && sh[P] && tr.cells[4]) {
        var m = tr.cells[4].textContent.match(/[\\u4e00-\\u9fa5]+\\s*$/);
        var unit = m ? m[0].trim() : '只';
        tr.cells[4].innerHTML = '<span class="td-num"><b>' + fmt(sh[P][2]) + '</b> ' + unit + '</span>';
      }
      keep.push(tr.outerHTML);
    });
    tb.innerHTML = keep.join('') || drillCache;
  }
  function recalc() {
    var P = projVal();
    var main = null;
    document.querySelectorAll('table').forEach(function (t) {
      var th = t.querySelector('thead');
      if (th && th.textContent.indexOf('适用项目') > -1 && th.textContent.indexOf('总量') > -1) main = t;
    });
    if (!main) return;
    if (!P) { recalcDrill(''); return; } /* 全部：renderListPage 已按原始 cells 重渲染，仅还原下钻 */
    var tb = main.querySelector('tbody');
    Array.prototype.forEach.call(tb.rows, function (tr) {
      var key = tr.cells[0] ? tr.cells[0].textContent.trim() : '';
      var sh = shares(key);
      if (!sh) return;
      var q = sh[P];
      if (!q) return;
      var nums = [q[0], q[1], q[2], q[3], q[0] + q[1] + q[2] + q[3]];
      for (var c = 4; c <= 8; c++) {
        if (tr.cells[c]) tr.cells[c].innerHTML = '<span class="td-num">' + fmt(nums[c - 4]) + '</span>';
      }
      if (tr.cells[3]) tr.cells[3].textContent = P;
    });
    recalcDrill(P);
  }
  /* 触发：筛选卡 查询/重置 点击后（renderListPage 重渲染完成再算）；下钻弹窗打开时同步 */
  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('button') : null;
    if (el) {
      var txt = (el.textContent || '').trim();
      if (txt === '查询' || txt === '重置') setTimeout(recalc, 0);
    }
  });
  var _om = window.openModal;
  if (typeof _om === 'function') {
    window.openModal = function (id) { _om(id); setTimeout(function () { recalcDrill(projVal()); }, 0); };
  }
})();
</script>'''

m = re.search(r"modalId: 'flowModal'\r?\n\}\);", s)
assert m, 'flowModal cfg anchor not found'
ins = m.end()
s = s[:ins] + '\n' + SCRIPT + s[ins:]
io.open(FP, 'w', encoding='utf-8', newline='').write(s)
print('C2 page script injected after renderListPage cfg (', len(SCRIPT), 'chars )')
