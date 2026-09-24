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
    + '.pn-q{display:inline-flex;width:14px;height:14px;background-color:#8c8c8c;-webkit-mask:url(data:image/png;base64,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) center/contain no-repeat;mask:url(data:image/png;base64,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) center/contain no-repeat;cursor:pointer;vertical-align:middle;margin-left:10px;position:relative;opacity:.85;transition:opacity .15s}'
    + '.pn-q:hover{opacity:1}'
    + '.btn:not(.btn-default) .pn-q{background-color:#fff}'
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
