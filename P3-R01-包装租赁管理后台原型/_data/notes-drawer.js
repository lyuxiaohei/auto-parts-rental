/* 原型标注抽屉（notes-drawer）——0918 拍板：角标只保留数字，说明文案集中右侧抽屉
 * 依赖：_data/notes-data.js（NOTES_META.codes / NOTES_DATA[页面键]）
 * 页面只需要：data-note="N" 数字标记 ＋ 本件与 notes-data 两行引用，文案改动不碰页面
 * 开关：右下角「标注 N」按钮 / 点击紫色数字角标（开抽屉并定位对应条目）/ 点击 ? 圆标（素材图·业务提示小弹窗·0920）/ Alt+N / ?notes=1 初始开
 * 初始态：默认不展示（0918 道远「默认不要展示抽屉弹窗」·不跨页记忆）；?notes=1 仅当页初始开，不锁死开关 */
(function () {
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
    + '.pn-drawer-foot{flex:none;padding:8px 16px;border-top:1px solid #f0f0f0;font-size:11px;color:#8c8c8c}'
    /* 双轨（0919 道远拍板 #9·0920 修正）：业务提示＝锚点文字后内联「?」圆标（素材图 项目原型素材/问号.png 内嵌 base64）·点击弹小弹窗——**? 圆标及内容属正式功能需求·需开发到前端页面**（面向最终用户·标题后水平对齐/按钮内并入文本·问号插入最深层文本元素后·间隔 10px——flex 容器不甩尾）；PRD 注释＝紫色数字角标悬浮右上·点击开抽屉——**仅开发过程内部查看·正式版不出现** */
    + '[data-note].pn-biz{position:relative}'
    + 'body.proto-notes-on [data-note].pn-biz::after{display:none}'
    + '.pn-q{display:inline-flex;width:14px;height:14px;background:url(data:image/png;base64,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) center/contain no-repeat;cursor:pointer;vertical-align:middle;margin-left:10px;position:relative;opacity:.85;transition:opacity .15s}'
    + '.pn-q:hover{opacity:1}'
    + '.pn-tip{position:fixed;z-index:895;width:280px;max-width:300px;background:#fff;color:#262626;border:1px solid #262626;border-radius:8px;font-size:12px;line-height:1.7;font-family:-apple-system,\'Segoe UI\',\'Microsoft YaHei\',sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.22);pointer-events:auto;opacity:0;transform:translateY(4px);transition:opacity .15s,transform .15s}'
    + '.pn-tip.pn-show{opacity:1;transform:none}'
    + '.pn-tip .pn-tip-h{display:flex;align-items:center;justify-content:space-between;padding:9px 12px;border-bottom:1px solid #e8e8e8;font-weight:600;font-size:13px;color:#000}'
    + '.pn-tip .pn-tip-x{cursor:pointer;color:#8c8c8c;font-size:16px;line-height:1;padding:0 2px;font-weight:400}'
    + '.pn-tip .pn-tip-x:hover{color:#000}'
    + '.pn-tip .pn-tip-b{padding:9px 12px;color:#404040;max-height:220px;overflow-y:auto}'
    + '.pn-aud{flex:none;border-radius:3px;padding:0 5px;font-size:10px;line-height:16px;font-weight:600;margin-left:2px}'
    + '.pn-aud-dev{background:#722ed1;color:#fff}'
    + '.pn-aud-biz{background:#e6f4ff;color:#1677ff;border:1px solid #91caff}';
  var st = document.createElement('style');
  st.id = 'notes-drawer-style';
  st.textContent = css;
  document.head.appendChild(st);

  /* ---------- 抽屉 DOM ---------- */
  var mask = document.createElement('div');
  mask.className = 'pn-mask';
  var drawer = document.createElement('div');
  drawer.className = 'pn-drawer';
  var html = '<div class="pn-drawer-head"><div class="pn-drawer-title">原型标注 <span class="pn-fab-n"></span></div><span class="pn-close">×</span></div><div class="pn-drawer-body"></div><div class="pn-drawer-foot">? 圆标＝业务说明（点击弹小窗）；紫色数字＝PRD 注释（点击开抽屉）；Alt+N 或右下角按钮开关抽屉</div>';
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
      var aud = it.aud === 'dev' ? '<span class="pn-aud pn-aud-dev">开发</span>' : '<span class="pn-aud pn-aud-biz">业务</span>';
      [it.fp, it.req].forEach(function (t) { if (t) tags.push('<span class="pn-tag">' + esc(tagText(t)) + '</span>'); });
      h.push('<div class="pn-item" data-id="' + it.id + '"><div class="pn-item-t"><span class="pn-item-n">' + it.id + '</span>' + esc(it.title) + aud + '</div>'
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
    if (e.key === 'Escape') { hideTip(); if (drawerOpen()) closeDrawer(); }
  });

  /* ---------- 双轨（0919 道远拍板 #9）：业务条目＝锚点旁「?」圆标常显＋悬停小提示；开发条目＝数字角标开抽屉 ---------- */
  var tip = document.createElement('div');
  tip.className = 'pn-tip';
  document.body.appendChild(tip);
  function idMap() {
    var m = {};
    (items || []).forEach(function (it) { m[String(it.id)] = it; });
    return m;
  }
  var IMAP = idMap();
  function showTip(q, it) {
    tip.innerHTML = '<div class="pn-tip-h"><span>' + esc(it.title) + '</span><span class="pn-tip-x">×</span></div>'
      + (it.note ? '<div class="pn-tip-b">' + esc(it.note) + '</div>' : '');
    var x = tip.querySelector('.pn-tip-x');
    if (x) x.addEventListener('click', function (e) { e.stopPropagation(); hideTip(); });
    tip.classList.add('pn-show');
    var r = q.getBoundingClientRect();
    var top = r.bottom + 6;
    tip.style.left = Math.max(8, Math.min(r.left - 4, window.innerWidth - 296)) + 'px';
    tip.style.top = (top + tip.offsetHeight > window.innerHeight - 8 ? r.top - tip.offsetHeight - 6 : top) + 'px';
  }
  function hideTip() { tip.classList.remove('pn-show'); }
  document.querySelectorAll('[data-note]').forEach(function (el) {
    var it = IMAP[el.getAttribute('data-note')];
    if (!it) return;
    if (it.aud === 'dev') return; /* PRD 注释：维持紫色数字角标+抽屉 */
    el.classList.add('pn-biz');
    var q = document.createElement('span');
    q.className = 'pn-q';
    q.title = '';
    /* 0920 道远：? 放文本右侧·间隔 10px——须插进最深层含文本的子元素内，
       直接 appendChild 到锚点尾会被 flex/space-between 容器甩到行尾（如我的待办统计卡标签） */
    var host = el, n = el, guard = 0, SKIP = { SELECT: 1, INPUT: 1, TEXTAREA: 1, IMG: 1, SVG: 1 };
    while (guard++ < 6) {
      var deep = null;
      for (var i = 0; i < n.children.length; i++) {
        var c = n.children[i];
        if ((c.classList && c.classList.contains('pn-q')) || SKIP[c.tagName]) continue;
        if ((c.textContent || '').trim()) { deep = c; break; }
      }
      if (!deep) break;
      host = deep; n = deep;
    }
    host.appendChild(q);
    q.addEventListener('click', function (e) { e.stopPropagation(); tip.classList.contains('pn-show') ? hideTip() : showTip(q, it); });
  });

  /* ---------- 点击角标：开抽屉并定位对应条目（0918 拍板：抽屉含全部标注） ---------- */
  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('.pn-tip')) return; /* 业务小弹窗内部点击：既不关窗也不开抽屉（× 自关） */
    if (e.target.closest && e.target.closest('.pn-q')) return; /* ? 圆标＝点击弹小弹窗（自身 handler），不开抽屉 */
    hideTip(); /* 点外关闭业务小弹窗 */
    var t = e.target.closest ? e.target.closest('[data-note]') : null;
    if (!t) return;
    /* 0920 双轨收口：biz 元素本体点击＝元素自身功能（如按钮跳页），不得劫持——劫持仅限 dev
       （dev 紫数字为 ::after 伪元素，点击命中宿主，须由宿主承接开抽屉）。此前 biz 按钮点击
       被 preventDefault+stopPropagation 吞掉，新建客商/新建项目/自动匹配等全部只弹抽屉不执行 */
    if (t.classList.contains('pn-biz')) return;
    e.preventDefault();
    e.stopPropagation();
    openDrawer(t.getAttribute('data-note'));
  }, true);

  /* ---------- 初始态：默认不展示，仅 ?notes=1 显式初始开（不跨页记忆） ---------- */
  var initOn = location.search.indexOf('notes=1') > -1;
  notesOn(initOn);
  if (initOn && items && items.length) openDrawer();
})();
