/* ==========================================================================
 * select-source.js —— 下拉数据源化共享件（G43 · 2026-09-17 · D-93/D-153 延续）
 * --------------------------------------------------------------------------
 * 用法（页面尾挂在 demo-data.js 之后·静态 option 不动作运行时兜底）：
 *   <script src="../_data/demo-data.js"></script>
 *   <script src="../_data/select-source.js"></script>
 *   <script>
 *     SSEL.fillDict(SSEL.byLabel('入库类型'), '入库类型', true);          // B 类：字典渲染
 *     SSEL.fillEntity(SSEL.byLabel('客户'), 'partners', {               // A 类：实体渲染
 *       field: 'name', filter: function (k, f) { return f.type === '客户'; },
 *       keepFirst: true
 *     });
 *   </script>
 * API：
 *   dictOpts(cat)                          字典组名 -> [name]（status!=停用·按键序）
 *   fillDict(sel, cat, keepFirst, opts)    字典渲染；opts.value={name:匹配值}（筛选保匹配），
 *                                          opts.title={name:悬浮注记}（措辞统一·括号说明入 title），
 *                                          opts.only=[name...]（表单子集）
 *   fillEntity(sel, entity, opts)          实体渲染；两种模式：
 *     · 字段去重：opts.field='wh'（值=字段实值·筛选用）+ opts.filterV(v) 值过滤
 *     · 行键列表：opts.label=key/fields->文本（缺省=键）+ opts.filter(k,f) 行过滤
 *       + opts.desc（键倒序）+ opts.limit（前 N 条·配 desc 用）
 *   通用：opts.keepFirst=保留「全部」首项；opts.append=[追加演示 option]
 *        （如「其他（演示）」）；opts.emptyKeep=空实体守卫保留原 option
 *   byLabel(text)  按 .ff-label 文本定位筛选区 select（list-generic 同口径）
 *   periods(n)     近 n 期账期（执行月倒推 YYYY-MM）
 * fill 后若原选中值仍在新集合则保持选中，否则回落首项。
 * 样板：G34 dictOpts（客商开票资料）·G35 fill/ent（库存查询）·差集矩阵 g43_接线差集_v2.md
 * ========================================================================== */
(function () {
  function D() { return window.DEMO_DATA || {}; }
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function resolve(sel) {
    if (sel && sel.tagName === 'SELECT') return sel;
    return document.getElementById(sel);
  }
  function dictOpts(cat) {
    var it = D().dictItems || {}, out = [];
    Object.keys(it).filter(function (k) {
      var f = (it[k].row || {}).fields || {};
      return f.category === cat && f.status !== '停用';
    }).sort().forEach(function (k) {
      var n = ((it[k].row || {}).fields || {}).name;
      if (n) out.push(n);
    });
    return out;
  }
  function render(s, items, keepFirst) {
    if (!s || !items || !items.length) return false;
    var prev = s.value;
    var html = keepFirst ? '<option>全部</option>' : '';
    html += items.map(function (it) {
      var v = it.value != null ? ' value="' + esc(it.value) + '"' : '';
      var t = it.title ? ' title="' + esc(it.title) + '"' : '';
      var dk = it.dataKey ? ' data-key="' + esc(it.dataKey) + '"' : '';
      return '<option' + v + t + dk + '>' + esc(it.text) + '</option>';
    }).join('');
    s.innerHTML = html;
    if (prev) {
      for (var i = 0; i < s.options.length; i++) {
        if (s.options[i].value === prev || s.options[i].textContent === prev) { s.selectedIndex = i; break; }
      }
    }
    return true;
  }
  function fillDict(sel, cat, keepFirst, opts) {
    opts = opts || {};
    var s = resolve(sel);
    if (!s) return false;
    var names = dictOpts(cat);
    if (opts.only) names = names.filter(function (n) { return opts.only.indexOf(n) > -1; });
    if (!names.length) return false; /* 空守卫：保留静态兜底 */
    return render(s, names.map(function (n) {
      return { text: n, value: opts.value && opts.value[n], title: opts.title && opts.title[n] };
    }), keepFirst);
  }
  function fillEntity(sel, entity, o) {
    o = o || {};
    var s = resolve(sel);
    if (!s) return false;
    var ents = Array.isArray(entity) ? entity : [entity];
    ents = ents.map(function (e) { return D()[e]; }).filter(Boolean);
    if (!ents.length) return false;
    var items = [];
    if (o.field) {
      var seen = {};
      ents.forEach(function (ent) {
        Object.keys(ent).forEach(function (k) {
          var f = (ent[k].row || {}).fields || {};
          var v = f[o.field];
          if (v == null || v === '' || v === '—' || seen[v]) return;
          if (o.filterV && !o.filterV(v)) return;
          seen[v] = 1;
          items.push({ text: v, value: v });
        });
      });
    } else {
      var keys = [];
      ents.forEach(function (ent) { Object.keys(ent).forEach(function (k) { keys.push([k, ent]); }); });
      if (o.filter) keys = keys.filter(function (p) { var f = (p[1][p[0]].row || {}).fields || {}; return o.filter(p[0], f); });
      keys.sort(function (a, b) { return a[0] < b[0] ? -1 : (a[0] > b[0] ? 1 : 0); });
      if (o.desc) keys.reverse();
      if (o.limit) keys = keys.slice(0, o.limit);
      keys.forEach(function (p) {
        var k = p[0], f = (p[1][k].row || {}).fields || {};
        var text = typeof o.label === 'function' ? o.label(k, f) : (o.label ? String(f[o.label] || '') : k);
        if (!text) return;
        items.push({ text: text, value: k, dataKey: k });
      });
    }
    if (!items.length) return o.emptyKeep ? true : false; /* 空守卫 */
    if (o.append) o.append.forEach(function (a) { items.push(typeof a === 'string' ? { text: a, value: a } : a); });
    return render(s, items, o.keepFirst);
  }
  function byLabel(text) {
    var els = document.querySelectorAll('.ff');
    for (var i = 0; i < els.length; i++) {
      var lb = els[i].querySelector('.ff-label');
      if (lb && lb.textContent.replace(/[:：]\s*$/, '') === text) return els[i].querySelector('select');
    }
    return null;
  }
  function norm(t) { return String(t).replace(/[\s\*]/g, '').replace(/[:：]$/, ''); }
  function byFormLabel(text) {
    var els = document.querySelectorAll('.form-label');
    for (var i = 0; i < els.length; i++) {
      if (norm(els[i].textContent) !== norm(text)) continue;
      var row = els[i].closest('.form-row') || els[i].parentElement;
      if (row) return row.querySelector('select');
    }
    return null;
  }
  function periods(n) {
    var out = [], d = new Date(), y = d.getFullYear(), m = d.getMonth() + 1;
    for (var i = 0; i < n; i++) {
      out.push(y + '-' + ('0' + m).slice(-2));
      m--; if (m === 0) { m = 12; y--; }
    }
    return out;
  }
  function fillPeriods(sel, n, keepFirst) {
    var s = resolve(sel);
    if (!s) return false;
    var prev = s.value;
    var html = keepFirst ? '<option>全部</option>' : '';
    html += periods(n).map(function (p) { return '<option>' + p + '</option>'; }).join('');
    s.innerHTML = html;
    if (prev) {
      for (var i = 0; i < s.options.length; i++) {
        if (s.options[i].textContent === prev) { s.selectedIndex = i; break; }
      }
    }
    return true;
  }
  window.SSEL = { dictOpts: dictOpts, fillDict: fillDict, fillEntity: fillEntity, fillPeriods: fillPeriods, byLabel: byLabel, byFormLabel: byFormLabel, periods: periods };
})();
