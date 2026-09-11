/* ============================================================================
 * P3-R01 移动端 H5 共享脚本（G14 · 2026-09-11）
 * 依赖：../_data/demo-data.js（window.DEMO_DATA，37 实体只读复用）
 * 机制：
 *   - go(u)        全局跳转函数（审计 harness 会接管 window.go 记录导航意图）
 *   - mGuard()     免二次登录守卫：未登录(无 m-auth)访问受护页 → 跳 登录.html
 *                  （600ms 延迟发起，避免页面 load 事件被打断）
 *   - m-auth       localStorage 登录标记：登录页写入 / 我的页清除 / 受护页校验
 *   - m-done       审批结果暂存 { 单号: 已通过|已驳回 }，待办列表回显状态
 * ========================================================================== */

/* ---- 全局跳转（勿改名：全站按钮 onclick 均经此函数） ---- */
function go(u) { location.href = u; }

/* ---- 免二次登录守卫（受护页调用；delay 毫秒后校验） ---- */
function mGuard(delay) {
  setTimeout(function () {
    if (!localStorage.getItem('m-auth')) location.replace('登录.html');
  }, delay || 600);
}

/* ---- 登录页反向守卫：已登录访问登录页 → 直达待办 ---- */
function mGuardAuthed(delay) {
  setTimeout(function () {
    if (localStorage.getItem('m-auth')) location.replace('待办审批.html');
  }, delay || 600);
}

/* ---- 登录标记读写 ---- */
function mUser() {
  try { return JSON.parse(localStorage.getItem('m-auth') || 'null'); }
  catch (e) { return null; }
}
function mLogin(name, role) {
  localStorage.setItem('m-auth', JSON.stringify({ name: name, role: role, ts: Date.now() }));
}
function mLogout() {
  localStorage.removeItem('m-auth');
  localStorage.removeItem('m-done');
}

/* ---- 审批结果暂存 ---- */
function mDoneMap() {
  try { return JSON.parse(localStorage.getItem('m-done') || '{}'); }
  catch (e) { return {}; }
}
function mDoneSet(docNo, action) {
  var m = mDoneMap(); m[docNo] = action;
  localStorage.setItem('m-done', JSON.stringify(m));
}

/* ---- 数据助手：实体 → 行数组（过滤 _header 等无 row 条目） ---- */
function mRows(entity) {
  var box = (window.DEMO_DATA || {})[entity] || {};
  return Object.keys(box).map(function (k) {
    var r = box[k] && box[k].row ? box[k].row : null;
    return r ? { id: k, row: r } : null;
  }).filter(Boolean);
}

/* ---- HTML 转义 ---- */
function mEsc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

/* ---- 从 cells HTML 里取含 <b> 的合计数量文本，无则取首个纯数字 ---- */
function mQtyFromCells(cells) {
  if (!cells || !cells.length) return '—';
  var hit = null;
  for (var i = 0; i < cells.length; i++) {
    if (String(cells[i]).indexOf('<b>') >= 0) { hit = cells[i]; break; }
  }
  var txt = String(hit == null ? '' : hit).replace(/<[^>]+>/g, '').trim();
  return txt || '—';
}

/* ---- 状态徽标配色 ---- */
function mBadgeCls(status) {
  var s = String(status || '');
  if (s === '已通过' || s === '在库' || s === '已提交') return 'm-badge-green';
  if (s === '已驳回') return 'm-badge-red';
  if (s === '客户端(转租)') return 'm-badge-purple';
  if (s === '客户端(租出)') return 'm-badge-blue';
  if (s.indexOf('待') === 0) return 'm-badge-orange';
  return 'm-badge-gray';
}

/* ---- 单据类型徽标配色 ---- */
function mTypeCls(type) {
  var t = String(type || '');
  if (t === '销售订单' || t === '销售出库') return 'm-badge-blue';
  if (t === '采购订单' || t === '采购入库') return 'm-badge-purple';
  if (t === '租赁单' || t === '租入库' || t === '租入归还') return 'm-badge-green';
  if (t === '退租入库' || t === '盘点' || t === '其他入库') return 'm-badge-orange';
  if (t === '付款登记' || t === '收款确认') return 'm-badge-red';
  return 'm-badge-gray';
}

/* ---- toast ---- */
var mToastTimer = null;
function mToast(msg) {
  var el = document.getElementById('m-toast');
  if (!el) {
    el = document.createElement('div'); el.id = 'm-toast'; el.className = 'm-toast';
    document.body.appendChild(el);
  }
  el.textContent = msg;
  el.classList.add('show');
  if (mToastTimer) clearTimeout(mToastTimer);
  mToastTimer = setTimeout(function () { el.classList.remove('show'); }, 1800);
}
