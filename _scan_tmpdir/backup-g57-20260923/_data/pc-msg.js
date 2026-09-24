/* pc-msg.js · 站内信中心（2026-09-14 拍板：站内信+到期提醒）
 * 挂载点：顶栏既有「通知」铃铛（.ico-btn[title="通知"]）——加未读角标+点击开右侧抽屉
 * （0922 道远反馈：原 top:52 下拉面板遮表格/条目换行错乱——改 notes-drawer 同款抽屉：右滑入+遮罩+×/Esc/点遮罩关闭）
 * 消息四类（演示态·单号均为 demo-data 真实行）：账单到期 / 分期付款 / 押金应退 / 续租跟进
 * 已读状态：localStorage 键 pc-msg-read（JSON 数组存已读 id）——与 pc-logout / m-auth 键域独立
 */
(function () {
  var MSGS = [
    { id: 'm1', t: '09-14 09:05', tag: '账单到期', unread: true,  link: '财务协同/应收账单.html',
      txt: '应收账单 AR-2026-09-PRJ2601（¥486,200 · 账期 2026-09）2026-09-30 到期，尚未结清，请跟进收款' },
    { id: 'm2', t: '09-14 08:40', tag: '分期付款', unread: true,  link: '财务协同/应付账单.html',
      txt: '应付账单 AP-20260905-013（对客户应付 ¥68,400 · 分期）付款到期日 2026-09-20，请安排付款登记' },
    { id: 'm3', t: '09-13 17:22', tag: '押金应退', unread: false, link: '财务协同/应付账单.html',
      txt: '租赁单 ZL-20260901-032 已退租结清，押金 ¥30,000 待退（对客户应付 AP-20260912-PRJ2601-YJT）' },
    { id: 'm4', t: '09-13 16:00', tag: '续租跟进', unread: false, link: '租赁管理/租赁单列表.html',
      txt: '租赁单 ZL-20260816-029（按月计费 · 在租）本月账期将满，请跟进客户续租意向' }
  ];
  var KEY = 'pc-msg-read';
function tagSource() {
  var D = window.DEMO_DATA && window.DEMO_DATA.dictItems;
  if (D) {
    var ks = Object.keys(D).filter(function (k) { return D[k].row && D[k].row.fields.category === '消息类型'; });
    var arr = ks.map(function (k) { return D[k].row.fields.abbr; }).filter(Boolean);
    if (arr.length) return arr;
  }
  return ['账单到期', '分期付款', '押金应退', '续租跟进'];
}
var curTag = '全部';

  function readSet() {
    try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; }
  }
  function isRead(m) { return m.unread === false || readSet().indexOf(m.id) > -1; }
  function unreadCount() { var n = 0; for (var i = 0; i < MSGS.length; i++) if (!isRead(MSGS[i])) n++; return n; }
  function prefix() { /* 按本脚本 src 写法判层级：目录页 ../_data/…（回根一级）；根级页 _data/…（直连） */
    var s = document.querySelector('script[src$="pc-msg.js"]');
    if (s) return s.getAttribute('src').indexOf('../') === 0 ? '../' : '';
    return '../';
  }
  function jump(link) {
    var url = prefix() + link;
    if (typeof go === 'function') { go(url); } else { location.href = url; }
  }

  function injectMsgCenter() {
    var bell = document.querySelector('.ico-btn[title="通知"]');
    if (!bell || bell.getAttribute('data-msg') === 'on') return true;
    bell.setAttribute('data-msg', 'on');
    bell.style.position = 'relative';
    bell.style.cursor = 'pointer';

    var style = document.createElement('style');
    style.textContent = [
      '.pc-msg-badge{position:absolute;top:-4px;right:-6px;min-width:14px;height:14px;line-height:14px;',
      'border-radius:7px;background:#ff4d4f;color:#fff;font-size:9px;text-align:center;padding:0 3px;font-weight:600}',
      '.pc-msg-mask{position:fixed;inset:0;background:rgba(0,0,0,.25);z-index:2999;opacity:0;pointer-events:none;transition:opacity .2s}',
      '.pc-msg-mask.pc-msg-show{opacity:1;pointer-events:auto}',
      '.pc-msg-panel{position:fixed;top:0;right:0;bottom:0;width:360px;max-width:92vw;background:#fff;',
      'box-shadow:-4px 0 16px rgba(0,0,0,.12);z-index:3000;transform:translateX(100%);transition:transform .22s ease;',
      'display:flex;flex-direction:column;font-size:12px;color:#333}',
      '.pc-msg-panel.pc-msg-show{transform:none}',
      '.pc-msg-hd{flex:none;display:flex;justify-content:space-between;align-items:center;padding:14px 16px;',
      'border-bottom:1px solid #f0f0f0;font-weight:600;font-size:14px;color:#262626}',
      '.pc-msg-hd-r{display:flex;align-items:center;gap:10px;font-weight:400}',
      '.pc-msg-all{color:#1677ff;font-weight:400;cursor:pointer;font-size:12px}',
      '.pc-msg-all:hover{color:#4096ff}',
      '.pc-msg-close{cursor:pointer;font-size:18px;color:#8c8c8c;line-height:1;padding:2px 4px}',
      '.pc-msg-close:hover{color:#262626}',
      '.pc-msg-flt{flex:none;display:flex;align-items:center;gap:6px;padding:10px 16px;',
      'border-bottom:1px solid #f0f0f0;font-size:12px;color:#595959}',
      '.pc-msg-flt select{height:26px;padding:0 6px;border:1px solid #d9d9d9;border-radius:4px;background:#fff;',
      'font-size:12px;color:#333;cursor:pointer;outline:none}',
      '.pc-msg-list{flex:1;overflow-y:auto;padding:12px 14px}',
      '.pc-msg-item{border:1px solid #f0f0f0;border-radius:6px;padding:10px 12px;margin-bottom:10px;cursor:pointer;',
      'transition:border-color .15s,background .15s}',
      '.pc-msg-item:hover{background:#f5f8ff;border-color:#91caff}',
      '.pc-msg-item-h{display:flex;align-items:center;gap:6px}',
      '.pc-msg-dot{width:6px;height:6px;border-radius:50%;background:#ff4d4f;flex:none}',
      '.pc-msg-dot.read{background:#d9d9d9}',
      '.pc-msg-tag{display:inline-block;padding:0 6px;height:18px;line-height:18px;border-radius:9px;',
      'background:#e6f4ff;color:#1677ff;font-size:11px;flex:none}',
      '.pc-msg-time{margin-left:auto;color:#8c8c8c;font-size:11px;flex:none}',
      '.pc-msg-body{margin-top:5px;line-height:1.6;color:#595959}',
      '.pc-msg-empty{padding:24px;text-align:center;color:#8c8c8c}'
    ].join('');
    document.head.appendChild(style);

    var badge = document.createElement('span');
    badge.className = 'pc-msg-badge';
    bell.appendChild(badge);

    var mask = document.createElement('div');
    mask.className = 'pc-msg-mask';
    var panel = document.createElement('div');
    panel.className = 'pc-msg-panel';
    document.body.appendChild(mask);
    document.body.appendChild(panel);

    function isOpen() { return panel.classList.contains('pc-msg-show'); }
    function openDrawer() { renderPanel(); panel.classList.add('pc-msg-show'); mask.classList.add('pc-msg-show'); }
    function closeDrawer() { panel.classList.remove('pc-msg-show'); mask.classList.remove('pc-msg-show'); }

    function renderBadge() {
      var n = unreadCount();
      badge.textContent = n;
      badge.style.display = n > 0 ? 'block' : 'none';
    }
    function renderPanel() {
      var rows = [];
      for (var i = 0; i < MSGS.length; i++) {
        var m = MSGS[i];
        if (curTag !== '全部' && m.tag !== curTag) continue;
        rows.push('<div class="pc-msg-item" data-id="' + m.id + '">'
          + '<div class="pc-msg-item-h"><span class="pc-msg-dot' + (isRead(m) ? ' read' : '') + '"></span>'
          + '<span class="pc-msg-tag">' + m.tag + '</span>'
          + '<span class="pc-msg-time">' + m.t + '</span></div>'
          + '<div class="pc-msg-body">' + m.txt + '</div></div>');
      }
      if (!rows.length) rows.push('<div class="pc-msg-empty">' + (curTag === '全部' ? '暂无消息' : '该类型暂无消息') + '</div>');
      panel.innerHTML = '<div class="pc-msg-hd">站内信<span class="pc-msg-hd-r">'
        + '<span class="pc-msg-all" data-act="all">全部标为已读</span><span class="pc-msg-close">×</span></span></div>'
        + '<div class="pc-msg-flt"><span>类型：</span><select id="pcMsgTag">'
        + ['全部'].concat(tagSource()).map(function (t) { return '<option' + (t === curTag ? ' selected' : '') + '>' + t + '</option>'; }).join('')
        + '</select></div><div class="pc-msg-list">' + rows.join('') + '</div>';
    }
    function markRead(id) {
      var s = readSet();
      if (s.indexOf(id) === -1) { s.push(id); localStorage.setItem(KEY, JSON.stringify(s)); }
    }

    bell.addEventListener('click', function (ev) {
      ev.stopPropagation();
      isOpen() ? closeDrawer() : openDrawer(); /* DOM 副作用：抽屉开合 class 切换 */
    });
    mask.addEventListener('click', closeDrawer);
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') closeDrawer();
    });
    panel.addEventListener('change', function (ev) {
      if (ev.target && ev.target.id === 'pcMsgTag') { curTag = ev.target.value; renderPanel(); }
    });
    panel.addEventListener('click', function (ev) {
      ev.stopPropagation();
      var el = ev.target;
      if (el.getAttribute && el.getAttribute('data-act') === 'all') {
        for (var i = 0; i < MSGS.length; i++) markRead(MSGS[i].id);
        renderPanel(); renderBadge();
        return;
      }
      if (el.classList && el.classList.contains('pc-msg-close')) { closeDrawer(); return; }
      while (el && el !== panel && !el.getAttribute('data-id')) el = el.parentElement;
      if (el && el.getAttribute && el.getAttribute('data-id')) {
        var id = el.getAttribute('data-id');
        markRead(id); renderBadge();
        for (var j = 0; j < MSGS.length; j++) if (MSGS[j].id === id) { jump(MSGS[j].link); break; }
        closeDrawer();
      }
    });
    renderBadge();
    return true;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectMsgCenter);
  } else {
    injectMsgCenter();
  }
})();
