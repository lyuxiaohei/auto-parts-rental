/* ============================================================================
 * 通用列表页 · 数据驱动渲染（2026-09-08 列表试点：租赁单列表/采购入库列表）
 * ----------------------------------------------------------------------------
 * 用法（列表页脚本一段）：
 *   <script src="../_data/demo-data.js"></script>
 *   <script src="../_data/detail-generic.js"></script>
 *   <script src="../_data/list-generic.js"></script>
 *   <script>renderListPage({ entity:'leaseOrders', stabs:true, filters:[
 *     { label:'租赁单号', field:'_key', match:'contains' },
 *     { label:'客户名称', field:'customer' },
 *     { label:'起租日期', field:'start', range:true }
 *   ]});</script>
 *
 * 数据约定：demo-data.js 实体记录带 row 字段——
 *   row: {
 *     note?: '1'          A04 标注角标号（挂到单号列 td）
 *     fields: {...}       供筛选/stab 统计的语义字段（status/customer/...）
 *     cells: [...]        业务列 innerHTML（单号列与 ops 列由渲染器生成）
 *     ops: [{t:'编辑', act:"openModal('createModal')"} | {t:'关闭'} | {t:'详情', detail:true}]
 *   }
 *
 * 行为（与静态版一致）：
 *   - 详情钮直接按行单号 openGenericDetail 渲染（取代 wireDetailModal 接线）
 *   - stab-count 由实体计数填充（全部=全量，其余按 fields.status 匹配）
 *   - 查询=按筛选控件值真过滤（label→.ff 定位，字段映射见 cfg.filters）；
 *     重置=ia-fix 清空控件（捕获相先行）+ 本脚本恢复全量（冒泡相）
 *   - 渲染后 pinsRefresh()：A04 pin 按数据重挂 + 标注 FAB 计数刷新
 *   - 批量按钮（[data-batch]）状态用事件委托维持，兼容行重渲染
 * ========================================================================== */
(function () {
  function fmtPager(n) { return '第 1-' + n + ' 条/总共 ' + n + ' 条'; }

  window.renderListPage = function (cfg) {
    var DATA = window.DEMO_DATA && window.DEMO_DATA[cfg.entity];
    if (!DATA) { console.warn('[list-generic] 无实体: ' + cfg.entity); return; }
    var tbody = document.querySelector(cfg.tbodySel || 'tbody');
    if (!tbody) { console.warn('[list-generic] 无 tbody'); return; }
    var keysAll = Object.keys(DATA);

    /* ---- 行渲染 ---- */
    function rowHTML(key) {
      var r = DATA[key].row;
      var h = '<tr>\n          <td><input type="checkbox" class="cb"></td>\n          <td' +
        (r.note ? ' data-note="' + r.note + '"' : '') + '><span class="lk">' + key + '</span></td>\n';
      r.cells.forEach(function (c) { h += '          <td>' + c + '</td>\n'; });
      h += '          <td class="sticky-op"><span class="ops">';
      r.ops.forEach(function (o) {
        if (o.detail) h += '<a data-detail-key="' + key + '">' + o.t + '</a>';
        else if (o.act) h += '<a onclick="' + o.act + '">' + o.t + '</a>';
        else h += '<a>' + o.t + '</a>';
      });
      h += '</span></td>\n        </tr>';
      return h;
    }

    /* ---- A04 pin 重挂钩子 ---- */
    function pinsRefresh() {
      var fab = document.getElementById('protoNotesFab');
      if (fab) {
        var n = document.querySelectorAll('[data-note]').length;
        var cnt = fab.querySelector('.pn-fab-n');
        if (cnt) cnt.textContent = n;
        else if (fab.textContent.indexOf('标注') > -1) { /* 未展开态 FAB 带计数时由标注层自理 */ }
      }
      document.querySelectorAll('.proto-pin.pn-open').forEach(function (p) { p.classList.remove('pn-open'); });
    }

    /* ---- stab 自动统计 ---- */
    function stabsRefresh() {
      if (!cfg.stabs) return;
      document.querySelectorAll('.stabs .stab').forEach(function (st) {
        var cntEl = st.querySelector('.stab-count');
        if (!cntEl) return;
        var label = st.childNodes[0] ? st.childNodes[0].textContent.trim() : st.textContent.trim();
        var n;
        if (label === '全部') n = keysAll.length;
        else {
          n = keysAll.filter(function (k) { return DATA[k].row.fields && DATA[k].row.fields.status === label; }).length;
          if (n === 0) { n = keysAll.length; console.warn('[list-generic] stab「' + label + '」无状态匹配，按全量计数'); }
        }
        cntEl.textContent = n;
      });
    }

    /* ---- 筛选 ---- */
    function readFilters() {
      var preds = [];
      (cfg.filters || []).forEach(function (f) {
        var ff = null;
        document.querySelectorAll('.filter-card .ff').forEach(function (el) {
          var lb = el.querySelector('.ff-label');
          if (!ff && lb && lb.textContent.replace(/[:：]\s*$/, '') === f.label) ff = el;
        });
        if (!ff) { console.warn('[list-generic] 筛控件未找到: ' + f.label); return; }
        if (f.range) {
          var ins = ff.querySelectorAll('input');
          var lo = ins[0] && ins[0].value.trim(), hi = ins[1] && ins[1].value.trim();
          if (lo || hi) preds.push(function (r) {
            var d = String(r.fields[f.field] || '').slice(0, 10);
            return (!lo || d >= lo) && (!hi || d <= hi);
          });
          return;
        }
        var sel = ff.querySelector('select');
        if (sel) {
          var v = sel.value || (sel.options[sel.selectedIndex] || {}).text || '';
          v = v.trim();
          if (v && v !== '全部') preds.push(function (r) { return String(r.fields[f.field]) === v; });
          return;
        }
        var inp = ff.querySelector('input');
        if (inp) {
          var t = inp.value.trim();
          if (t) preds.push(function (r) {
            var fv = f.field === '_key' ? r._key : String(r.fields[f.field] || '');
            return fv.indexOf(t) > -1;
          });
        }
      });
      return preds;
    }

    function render(preds) {
      var keys = keysAll.filter(function (k) {
        var r = DATA[k].row; r._key = k;
        return (preds || []).every(function (p) { return p(r); });
      });
      tbody.innerHTML = keys.map(rowHTML).join('\n');
      var pg = document.querySelector('.pg-info');
      if (pg) pg.textContent = fmtPager(keys.length);
      document.querySelectorAll('[data-batch]').forEach(function (btn) {
        btn.style.opacity = '.45'; btn.style.cursor = 'not-allowed';
      });
      pinsRefresh();
      return keys.length;
    }

    /* 详情点击（委托，兼容重渲染） */
    tbody.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a[data-detail-key]') : null;
      if (!a) return;
      openGenericDetail(cfg.entity, a.getAttribute('data-detail-key'), cfg.base, cfg.modalId);
    });

    /* 批量复选状态（委托） */
    document.addEventListener('change', function (e) {
      if (!(e.target.matches && e.target.matches('tbody input[type="checkbox"].cb'))) return;
      var any = document.querySelectorAll('tbody input[type="checkbox"].cb:checked').length > 0;
      document.querySelectorAll('[data-batch]').forEach(function (btn) {
        btn.style.opacity = any ? '1' : '.45';
        btn.style.cursor = any ? 'pointer' : 'not-allowed';
      });
    });

    /* 查询 / 重置 */
    document.querySelectorAll('.filter-card button, .filter-actions button').forEach(function (btn) {
      var t = btn.textContent.trim();
      if (t === '查询') btn.addEventListener('click', function () { render(readFilters()); });
      if (t === '重置') btn.addEventListener('click', function () {
        /* ia-fix 捕获相已清空控件，此处恢复全量 */
        setTimeout(function () { render([]); }, 0);
      });
    });

    stabsRefresh();
    render([]);
  };
})();
