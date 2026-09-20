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
    /* 仅渲染带 row 字段的记录（详情-only 键/多表共用实体的次表键不参与列表渲染，2026-09-08 全量推广） */
    var keysAll = Object.keys(DATA).filter(function (k) { return DATA[k].row; });

    /* ---- 操作列按钮池（0920 道远三点菜单）：全行 ops 并集·首现序；cfg.opsTop 可钉常用前缀 ---- */
    var POOL = [];
    keysAll.forEach(function (k) {
      ((DATA[k].row.ops || []).forEach(function (o) {
        if (POOL.indexOf(o.t) < 0) POOL.push(o.t);
      }));
    });
    (cfg.opsTop || []).forEach(function (t) {
      var i = POOL.indexOf(t);
      if (i > 0) { POOL.splice(i, 1); POOL.unshift(t); }
    });
    var opLink = function (o) {
      if (o.detail) return '<a data-detail-key="' + o.key + '">' + o.t + '</a>';
      else if (o.act) return '<a onclick="' + o.act + '">' + o.t + '</a>';
      else return '<a>' + o.t + '</a>';
    };

    /* ---- 行渲染 ---- */
    function rowHTML(key) {
      var r = DATA[key].row;
      var h = '<tr>\n';
      if (!cfg.noCheckbox) h += '          <td><input type="checkbox" class="cb"></td>\n';
      h += '          <td' +
        (r.note ? ' data-note="' + r.note + '"' : '') + '>' +
        (r.keyHtml || '<span class="lk">' + key + '</span>') + '</td>\n';
      r.cells.forEach(function (c) { h += '          <td>' + c + '</td>\n'; });
      /* G12（2026-09-10）：noOps=表格无操作列（操作日志/损益报表类）；顺带防御 ops 缺失
         0920 道远三点菜单：池前 3 直显+⋮ 收纳第 4+；每行按池展示全量——该行 ops 没有的置灰 */
      if (!cfg.noOps) {
        var rowOps = r.ops || [];
        var byT = {};
        rowOps.forEach(function (o) { if (!byT[o.t]) byT[o.t] = { t: o.t, act: o.act, detail: o.detail, key: key }; });
        h += '          <td class="sticky-op"><span class="ops">';
        POOL.slice(0, 3).forEach(function (t) {
          h += byT[t] ? opLink(byT[t]) : '<a class="op-dis">' + t + '</a>';
        });
        if (POOL.length > 3) {
          h += '<a class="op-more" title="更多操作">⋮</a>';
          h += '<div class="op-menu">';
          POOL.slice(3).forEach(function (t) {
            h += byT[t] ? opLink(byT[t]) : '<a class="op-dis">' + t + '</a>';
          });
          h += '</div>';
        }
        h += '</span></td>\n';
      }
      h += '        </tr>';
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

    /* ---- stab 自动统计（cfg.stabField 默认 'status'；客商等类型语义页签可指定，2026-09-08 全量推广） ---- */
    function stabsRefresh() {
      if (!cfg.stabs) return;
      var fld = cfg.stabField || 'status';
      document.querySelectorAll('.stabs .stab').forEach(function (st) {
        var cntEl = st.querySelector('.stab-count');
        if (!cntEl) return;
        var label = st.childNodes[0] ? st.childNodes[0].textContent.trim() : st.textContent.trim();
        var n;
        if (label === '全部') n = keysAll.length;
        else {
          n = keysAll.filter(function (k) { return DATA[k].row.fields && DATA[k].row.fields[fld] === label; }).length;
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
          if (v && v !== '全部') preds.push(function (r) {
            var fv = String(r.fields[f.field] || '');
            return f.match === 'contains' ? fv.indexOf(v) > -1 : fv === v;
          });
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

    /* 详情点击（委托，兼容重渲染）；cfg.detailFn 供专用渲染器页面使用（应付/应收账单，2026-09-08 全量推广） */
    tbody.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a[data-detail-key]') : null;
      if (!a) return;
      if (cfg.detailFn) cfg.detailFn(cfg.entity, a.getAttribute('data-detail-key'));
      else openGenericDetail(cfg.entity, a.getAttribute('data-detail-key'), cfg.base, cfg.modalId);
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

    /* 0920 道远三点菜单：⋮ 开合（document 委托·同页单开·点外/Esc/选项点击后关） */
    if (!window.__opMenuReady) {
      window.__opMenuReady = true;
      var opMenuStyle = document.createElement('style');
      opMenuStyle.textContent =
        '.ops{position:relative;}' +
        '.op-dis{color:#c0c4cc!important;pointer-events:none;}' +
        '.op-more{display:inline-block;width:18px;text-align:center;font-size:14px;font-weight:700;color:#1677ff;letter-spacing:-1px;cursor:pointer;user-select:none;padding:0 2px;}' +
        '.op-more:hover{background:#e6f4ff;border-radius:3px;}' +
        '.op-menu{display:none;position:absolute;right:0;top:100%;z-index:960;min-width:96px;padding:4px 0;background:#fff;border:1px solid #e5e6eb;border-radius:6px;box-shadow:0 6px 16px rgba(0,0,0,.12);white-space:nowrap;}' +
        '.op-menu.open{display:block;}' +
        '.op-menu a{display:block;padding:6px 14px;color:#262626;cursor:pointer;}' +
        '.op-menu a:hover{background:#f5f7fa;color:#1677ff;}' +
        '.op-menu a.op-dis{color:#c0c4cc;background:none;cursor:default;}';
      document.head.appendChild(opMenuStyle);
      document.addEventListener('click', function (e) {
        var more = e.target.closest ? e.target.closest('.op-more') : null;
        document.querySelectorAll('.op-menu.open').forEach(function (m) {
          if (!more || m !== more.parentElement.querySelector('.op-menu')) m.classList.remove('open');
        });
        if (more) {
          var menu = more.parentElement.querySelector('.op-menu');
          if (menu) menu.classList.toggle('open');
          e.stopPropagation();
        }
      }, true);
      document.addEventListener('click', function (e) {
        var menu = e.target.closest ? e.target.closest('.op-menu') : null;
        if (menu) setTimeout(function () { menu.classList.remove('open'); }, 0);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') document.querySelectorAll('.op-menu.open').forEach(function (m) { m.classList.remove('open'); });
      });
    }

    stabsRefresh();
    render([]);
  };
})();
