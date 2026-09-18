/* 原型标注抽屉（notes-drawer）——0918 拍板：角标只保留数字，说明文案集中右侧抽屉
 * 依赖：_data/notes-data.js（NOTES_META.codes / NOTES_DATA[页面键]）
 * 页面只需要：data-note="N" 数字标记 ＋ 本件与 notes-data 两行引用，文案改动不碰页面
 * 开关：右下角「标注 N」按钮 / 点击任意角标（开抽屉并定位对应条目）/ Alt+N / ?notes=1 初始开
 * 记忆：localStorage 'proto-notes-on'；?notes=1 仅作初始态，不锁死开关 */
(function () {
  var KEY = 'proto-notes-on';
  var META = window.NOTES_META || { codes: {} };
  var CODES = META.codes || {};

  function pageKey() {
    var p = decodeURIComponent(location.pathname);
    var d = window.NOTES_DATA || {};
    var m = p.match(/([^\/]+\/[^\/]+\.html)$/);
    if (m && d[m[1]]) return m[1];
    var m2 = p.match(/([^\/]+\.html)$/); /* T1.2b：根级页（如 我的待办.html）末两段带目录前缀匹配不上，回退末段（0918） */
    return m2 ? m2[1] : null;
  }
  var items = (window.NOTES_DATA || {})[pageKey()] || null;

  /* ---------- 样式（组件自带，页面零依赖） ---------- */
  var css = ''
    + 'body.proto-notes-on [data-note]{position:relative}'
    + 'body.proto-notes-on [data-note]::after{content:attr(data-note);position:absolute;top:1px;right:1px;min-width:16px;height:16px;padding:0 3px;border-radius:3px;background:#722ed1;color:#fff;font-size:10px;line-height:16px;text-align:center;font-weight:600;box-shadow:0 0 0 1.5px #fff;cursor:pointer;opacity:.75;transition:opacity .15s;z-index:5}'
    + 'body.proto-notes-on [data-note]:hover::after{opacity:1}'
    + '.pn-fab{position:fixed;right:12px;bottom:12px;z-index:880;display:flex;align-items:center;gap:5px;height:24px;padding:0 10px;border-radius:4px;background:#fff;border:1px solid #ddd0ec;color:#722ed1;font-size:11px;font-family:-apple-system,\'Segoe UI\',\'Microsoft YaHei\',sans-serif;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.06);opacity:.6;transition:opacity .15s}'
    + '.pn-fab:hover{opacity:1;border-color:#722ed1}'
    + 'body.proto-notes-on .pn-fab{background:#f9f0ff;border-color:#722ed1;opacity:.95}'
    + '.pn-fab .pn-fab-n{font-family:Consolas,monospace;font-weight:600}'
    + '.fab-row .pn-fab{position:static}'
    + '.pn-mask{position:fixed;inset:0;background:rgba(0,0,0,.25);z-index:890;opacity:0;pointer-events:none;transition:opacity .2s}'
    + '.pn-mask.pn-show{opacity:1;pointer-events:auto}'
    + '.pn-drawer{position:fixed;top:0;right:0;bottom:0;width:360px;max-width:92vw;background:#fff;box-shadow:-4px 0 16px rgba(0,0,0,.12);z-index:891;transform:translateX(100%);transition:transform .22s ease;display:flex;flex-direction:column;font-family:-apple-system,\'Segoe UI\',\'Microsoft YaHei\',sans-serif}'
    + '.pn-drawer.pn-show{transform:none}'
    + '.pn-drawer-head{flex:none;display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid #f0f0f0}'
    + '.pn-drawer-title{font-size:14px;font-weight:600;color:#262626;display:flex;align-items:center;gap:8px}'
    + '.pn-drawer-title .pn-fab-n{color:#722ed1}'
    + '.pn-close{cursor:pointer;font-size:18px;color:#8c8c8c;line-height:1;padding:2px 4px}'
    + '.pn-close:hover{color:#262626}'
    + '.pn-drawer-body{flex:1;overflow-y:auto;padding:12px 14px}'
    + '.pn-empty{font-size:12px;color:#8c8c8c;padding:8px 2px}'
    + '.pn-item{border:1px solid #f0f0f0;border-radius:6px;padding:10px 12px;margin-bottom:10px;font-size:12px;color:#262626;transition:border-color .15s,box-shadow .15s}'
    + '.pn-item.pn-hl{border-color:#722ed1;box-shadow:0 0 0 2px rgba(114,46,209,.25)}'
    + '.pn-item-t{display:flex;align-items:center;gap:6px;font-weight:600;font-size:13px;padding-right:14px}'
    + '.pn-item-n{flex:none;min-width:16px;height:16px;padding:0 3px;border-radius:3px;background:#722ed1;color:#fff;font-size:10px;line-height:16px;text-align:center;font-weight:600}'
    + '.pn-item-d{margin-top:5px;color:#595959;line-height:1.6}'
    + '.pn-item-b{margin-top:6px;display:flex;gap:4px;flex-wrap:wrap}'
    + '.pn-tag{background:#f9f0ff;color:#722ed1;border-radius:3px;padding:0 6px;font-size:11px;line-height:20px}'
    + '.pn-src{margin-top:8px;padding-top:7px;border-top:1px dashed #e5dff0;font-size:11px;color:#595959;line-height:1.65}'
    + '.pn-src b{color:#722ed1;font-weight:600}'
    + '.pn-drawer-foot{flex:none;padding:8px 16px;border-top:1px solid #f0f0f0;font-size:11px;color:#8c8c8c}';
  var st = document.createElement('style');
  st.id = 'notes-drawer-style';
  st.textContent = css;
  document.head.appendChild(st);

  /* ---------- 抽屉 DOM ---------- */
  var mask = document.createElement('div');
  mask.className = 'pn-mask';
  var drawer = document.createElement('div');
  drawer.className = 'pn-drawer';
  var html = '<div class="pn-drawer-head"><div class="pn-drawer-title">原型标注 <span class="pn-fab-n"></span></div><span class="pn-close">×</span></div><div class="pn-drawer-body"></div><div class="pn-drawer-foot">编号与页面紫色角标一一对应；Alt+N 或右下角按钮开关</div>';
  drawer.innerHTML = html;
  document.body.appendChild(mask);
  document.body.appendChild(drawer);
  var body = drawer.querySelector('.pn-drawer-body');
  var cnt = drawer.querySelector('.pn-drawer-title .pn-fab-n');

  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : String(s); return d.innerHTML; }
  function tagText(t) {
    var c = CODES[t];
    return c ? t + ' · ' + c.name : t;
  }
  function srcHtml(it) {
    var out = [];
    [it.fp, it.req].forEach(function (t) {
      if (!t) return;
      var c = CODES[t];
      out.push(c ? '<b>' + t + ' ' + esc(c.name) + '</b>：' + esc(c.desc || '') : '<b>' + esc(t) + '</b>');
    });
    return out.join('<br>');
  }
  function render() {
    if (!items || !items.length) {
      body.innerHTML = '<div class="pn-empty">本页暂无标注（数据见 _data/notes-data.js）。</div>';
      cnt.textContent = '0';
      return;
    }
    var h = [];
    items.forEach(function (it) {
      var tags = [];
      [it.fp, it.req].forEach(function (t) { if (t) tags.push('<span class="pn-tag">' + esc(tagText(t)) + '</span>'); });
      h.push('<div class="pn-item" data-id="' + it.id + '"><div class="pn-item-t"><span class="pn-item-n">' + it.id + '</span>' + esc(it.title) + '</div>'
        + (it.note ? '<div class="pn-item-d">' + esc(it.note) + '</div>' : '')
        + (tags.length ? '<div class="pn-item-b">' + tags.join('') + '</div>' : '')
        + (srcHtml(it) ? '<div class="pn-src">' + srcHtml(it) + '</div>' : '')
        + '</div>');
    });
    body.innerHTML = h.join('');
    cnt.textContent = items.length;
  }
  render();

  /* ---------- 开关 ---------- */
  function isOn() { return document.body.classList.contains('proto-notes-on'); }
  function drawerOpen() { return drawer.classList.contains('pn-show'); }
  function notesOn(v) {
    document.body.classList.toggle('proto-notes-on', v);
    localStorage.setItem(KEY, v ? '1' : '0');
    fab.textContent = '';
    fab.innerHTML = (v ? '收起' : '标注 <span class="pn-fab-n">' + cnt.textContent + '</span>');
    fab.title = v ? '收起标注（Alt+N）' : '显示标注（Alt+N）';
  }
  function openDrawer(focusId) {
    drawer.classList.add('pn-show');
    mask.classList.add('pn-show');
    notesOn(true);
    if (focusId != null) {
      var el = body.querySelector('.pn-item[data-id="' + focusId + '"]');
      if (el) {
        body.querySelectorAll('.pn-item.pn-hl').forEach(function (x) { x.classList.remove('pn-hl'); });
        el.classList.add('pn-hl');
        el.scrollIntoView({ block: 'nearest' });
        setTimeout(function () { el.classList.remove('pn-hl'); }, 2400);
      }
    }
  }
  function closeDrawer() {
    drawer.classList.remove('pn-show');
    mask.classList.remove('pn-show');
  }

  /* ---------- 右下角按钮（有 fab-row 则并入，与流程图按钮同行） ---------- */
  var fab = document.createElement('div');
  fab.className = 'pn-fab';
  fab.id = 'protoNotesFab';
  var row = document.querySelector('.fab-row');
  if (row) { row.appendChild(fab); } else { document.body.appendChild(fab); }
  if (!items || !items.length) { fab.style.display = 'none'; } /* T1.2：本页无标注数据则隐藏入口（0918） */
  fab.addEventListener('click', function () {
    if (drawerOpen()) { closeDrawer(); } else { openDrawer(); }
  });
  drawer.querySelector('.pn-close').addEventListener('click', closeDrawer);
  mask.addEventListener('click', closeDrawer);
  document.addEventListener('keydown', function (e) {
    if (e.altKey && (e.key === 'n' || e.key === 'N')) {
      if (drawerOpen()) { closeDrawer(); notesOn(false); } else { openDrawer(); }
    }
    if (e.key === 'Escape' && drawerOpen()) closeDrawer();
  });

  /* ---------- 点击角标：开抽屉并定位对应条目（0918 拍板：抽屉含全部标注） ---------- */
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-note]') : null;
    if (!t) return;
    e.preventDefault();
    e.stopPropagation();
    openDrawer(t.getAttribute('data-note'));
  }, true);

  /* ---------- 初始态 ---------- */
  var initOn = location.search.indexOf('notes=1') > -1 || localStorage.getItem(KEY) === '1';
  notesOn(initOn);
  if (initOn && items && items.length) openDrawer();
})();
