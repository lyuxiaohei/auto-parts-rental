/* G19b PC 默认登录态守卫与顶栏账户下拉（38 业务页统一挂载）
 * 键域：localStorage['pc-logout']——无键或≠'1'=已登录（默认态·清缓存也直达）；='1'=已退出。
 * mobile m-auth 键域独立，本文件不读不写。登录页自身不注入本文件（防死循环）。 */
(function () {
  'use strict';

  // ---- 登录页地址解析（按本文件被引用的相对层级，不硬编码每页路径）----
  var loginUrl = (function () {
    try {
      var src = document.currentScript && document.currentScript.src;
      if (src && /_data\/pc-auth\.js/.test(src)) {
        return src.replace(/_data\/pc-auth\.js.*$/, '') + encodeURIComponent('登录.html');
      }
    } catch (e) {}
    // fallback：pathname 去文件名后按深度回溯到原型根
    var dir = location.pathname.replace(/[^/]*$/, '');
    var depth = dir.split('/').filter(function (s) { return s !== ''; }).length;
    // 本文件仅在「原型根/」或「原型根/子目录/」两层出现：根级页 depth 即原型根，子目录页需 -1
    var up = Math.max(0, depth - (window.__PC_AUTH_DEPTH__ || 0));
    return '../'.repeat(Math.min(1, up)) + encodeURIComponent('登录.html');
  })();

  var isLoginPage = /%E7%99%BB%E5%BD%95\.html$|\/登录\.html$/.test(location.pathname) ||
                    /登录\.html$/.test(decodeURIComponent(location.pathname));

  // ---- 守卫：已退出态访问业务页 → 跳登录页 ----
  try {
    if (localStorage.getItem('pc-logout') === '1' && !isLoginPage) {
      location.href = loginUrl;
      return; // 跳转中不再注入下拉
    }
  } catch (e) {}

  // ---- 顶栏账户下拉（JS click 切换——触屏 hover 不可靠）----
  function injectAvatarMenu() {
    var avatar = document.querySelector('.topbar .avatar') || document.querySelector('.tools .avatar');
    if (!avatar) return false; // D6：无头像页只挂守卫，下拉跳过
    var userName = 'liu.dy（演示）';
    avatar.style.cursor = 'pointer';
    var menu = document.createElement('div');
    menu.style.cssText = 'position:absolute;z-index:999;background:#fff;border:1px solid #e5e6eb;border-radius:6px;box-shadow:0 4px 14px rgba(0,0,0,.1);min-width:132px;padding:4px 0;display:none;font-size:13px;color:#262626;';
    var nameRow = document.createElement('div');
    nameRow.textContent = userName;
    nameRow.style.cssText = 'padding:7px 14px;color:#8c8c8c;border-bottom:1px solid #f0f1f3;';
    var logoutRow = document.createElement('div');
    logoutRow.textContent = '退出登录';
    logoutRow.style.cssText = 'padding:7px 14px;cursor:pointer;';
    logoutRow.addEventListener('mouseenter', function () { logoutRow.style.background = '#f5f6f8'; });
    logoutRow.addEventListener('mouseleave', function () { logoutRow.style.background = ''; });
    logoutRow.addEventListener('click', function () {
      try { localStorage.setItem('pc-logout', '1'); } catch (e) {}
      location.href = loginUrl;
    });
    menu.appendChild(nameRow);
    menu.appendChild(logoutRow);
    // 挂到 tools（相对定位容器），贴头像下方
    var host = avatar.parentElement || document.body;
    if (getComputedStyle(host).position === 'static') host.style.position = 'relative';
    host.appendChild(menu);
    function place() {
      var r = avatar.getBoundingClientRect(), h = host.getBoundingClientRect();
      menu.style.top = (r.bottom - h.top + host.scrollTop + 6) + 'px';
      menu.style.left = (r.right - h.left + host.scrollLeft - menu.offsetWidth) + 'px';
    }
    avatar.addEventListener('click', function (ev) {
      ev.stopPropagation();
      var show = menu.style.display !== 'block';
      place();
      menu.style.display = show ? 'block' : 'none'; // DOM 副作用：就地开合
    });
    document.addEventListener('click', function () { menu.style.display = 'none'; });
    return true;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectAvatarMenu);
  } else {
    injectAvatarMenu();
  }
})();
