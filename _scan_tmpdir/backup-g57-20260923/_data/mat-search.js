/* ==========================================================================
 * mat-search.js —— 物料搜索下拉共享件（2026-09-17 · 道远指示：物料下拉换搜索组件）
 * --------------------------------------------------------------------------
 * 用法（页面尾挂在 demo-data.js / select-source.js 之后）：
 *   <script src="../_data/mat-search.js"></script>
 *   <script>
 *     MSEL.attachAll('.edit-tbl select.g39mat');                    // 明细表内（自带边框形态）
 *     MSEL.attach(SSEL.byFormLabel('物料'));                        // 表单头部 input-box（无框形态·保箭头）
 *   </script>
 * 说明：
 *   - 原生 select 隐藏保留为取值载体：选中后派发 change（冒泡），既有联动照常触发
 *   - 输入即过滤（option 文本与值双向包含匹配）；浮层 fixed 定位防表格容器裁剪
 *   - Esc 恢复 / 点外部关闭 / 滚动与缩放关闭 / 无匹配提示
 *   - 自动兼容「添加一行」克隆与页面重建：attachAll 幂等（克隆不带事件与标记·自动重绑），
 *     并自动包装 window.addDetailRow / window.renderRows（存在时）在重建后重挂
 * ========================================================================== */
(function () {
  var REG = [];
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }

  function bind(sel, wrap, inp, opts) {
    if (sel.__drop && sel.__drop.parentElement) sel.__drop.remove();
    var drop = document.createElement('div');
    drop.className = 'ms-drop';
    drop.style.cssText = 'display:none;position:fixed;background:#fff;border:1px solid #d9d9d9;border-radius:6px;box-shadow:0 6px 16px rgba(0,0,0,.12);z-index:9990;max-height:224px;overflow:auto;font-size:12.5px;min-width:230px;';
    drop.__wrap = wrap;
    document.body.appendChild(drop);
    sel.__ms = 1; sel.__inp = inp; sel.__drop = drop;
    if (opts && opts.placeholder) inp.placeholder = opts.placeholder;
    function sync() { var o = sel.options[sel.selectedIndex]; inp.value = o ? o.text : ''; }
    function place() {
      var r = inp.getBoundingClientRect();
      drop.style.left = r.left + 'px';
      drop.style.width = Math.max(r.width, 230) + 'px';
      drop.style.top = (window.innerHeight - r.bottom > 250 ? r.bottom + 4 : r.top - Math.min(drop.offsetHeight || 224, 224) - 4) + 'px';
    }
    function open() {
      var q = (inp.value || '').trim().toLowerCase(), h = '';
      for (var i = 0; i < sel.options.length; i++) {
        var o = sel.options[i];
        if (!q || o.text.toLowerCase().indexOf(q) > -1 || String(o.value || o.text).toLowerCase().indexOf(q) > -1)
          h += '<div class="ms-item" data-v="' + esc(o.value || o.text) + '" style="padding:6px 10px;cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;' + ((o.value || o.text) === sel.value ? 'color:#1677ff;font-weight:600;' : '') + '">' + esc(o.text) + (o.value && o.value !== o.text ? ' <span style="color:#8c8c8c;">' + esc(o.value) + '</span>' : '') + '</div>';
      }
      drop.innerHTML = h || '<div style="padding:8px 10px;color:#8c8c8c;">无匹配选项</div>';
      drop.style.display = 'block';
      place();
    }
    inp.addEventListener('focus', open);
    inp.addEventListener('input', open);
    inp.addEventListener('keydown', function (e) { if (e.key === 'Escape') { drop.style.display = 'none'; sync(); } });
    drop.addEventListener('mousedown', function (e) {
      var it = e.target.closest ? e.target.closest('.ms-item') : null;
      if (!it) return;
      e.preventDefault();
      sel.value = it.getAttribute('data-v');
      for (var i = 0; i < sel.options.length; i++) { if ((sel.options[i].value || sel.options[i].text) === sel.value) sel.options[i].setAttribute('selected', 'selected'); else sel.options[i].removeAttribute('selected'); }
      sync(); drop.style.display = 'none';
      sel.dispatchEvent(new Event('change', { bubbles: true }));
    });
    sel.addEventListener('change', sync);
    sync();
  }

  function attach(target, opts) {
    var sel = target && target.tagName === 'SELECT' ? target : document.querySelector(target);
    if (!sel) return;
    opts = opts || {};
    if (sel.__ms && sel.__inp) return;
    var wrap = sel.parentElement;
    /* 克隆重绑：wrap 已是组件容器但 select 丢了标记（cloneNode 不复制扩展属性与监听） */
    if (wrap && wrap.classList && wrap.classList.contains('ms-wrap')) { bind(sel, wrap, wrap.querySelector('input'), opts); return; }
    var box = sel.closest ? sel.closest('.input-box') : null;
    if (box && box.classList.contains('select-box')) {
      /* 表单头部：input-box.select-box 内保框保箭头，插无框输入框 */
      sel.style.display = 'none';
      var inp = document.createElement('input');
      inp.setAttribute('autocomplete', 'off');
      inp.placeholder = opts.placeholder || '输入搜索';
      inp.style.cssText = 'flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;padding:0;';
      box.insertBefore(inp, sel);
      bind(sel, box, inp, opts);
      return;
    }
    /* 明细表格单元格：自建带边框包裹 */
    wrap = document.createElement('div');
    wrap.className = 'ms-wrap';
    wrap.style.cssText = 'position:relative;width:100%;min-width:110px;';
    var inp2 = document.createElement('input');
    inp2.setAttribute('autocomplete', 'off');
    inp2.placeholder = opts.placeholder || '输入编码/名称搜索';
    inp2.style.cssText = 'width:100%;border:1px solid #d9d9d9;border-radius:4px;padding:2px 6px;font:inherit;background:#fff;';
    sel.style.display = 'none';
    sel.parentNode.insertBefore(wrap, sel);
    wrap.appendChild(inp2); wrap.appendChild(sel);
    bind(sel, wrap, inp2, opts);
  }

  function reattachAll() {
    REG.forEach(function (r) { document.querySelectorAll(r[0]).forEach(function (el) { attach(el, r[1]); }); });
  }
  function syncAll() {
    document.querySelectorAll('select').forEach(function (s) {
      if (s.__ms && s.__inp) { var o = s.options[s.selectedIndex]; s.__inp.value = o ? o.text : ''; }
    });
  }
  function hook(name) {
    var fn = window[name];
    if (typeof fn !== 'function' || fn.__msHooked) return;
    var wrapped = function () { var r = fn.apply(this, arguments); reattachAll(); syncAll(); return r; };
    wrapped.__msHooked = 1;
    window[name] = wrapped;
  }

  function attachAll(selector, opts) {
    REG.push([selector, opts]);
    document.querySelectorAll(selector).forEach(function (el) { attach(el, opts); });
    hook('addDetailRow'); hook('renderRows');
  }

  /* 全局关闭句柄（一次） */
  if (!window.__msGlobal) {
    window.__msGlobal = 1;
    window.addEventListener('scroll', function () { document.querySelectorAll('.ms-drop').forEach(function (d) { d.style.display = 'none'; }); }, true);
    window.addEventListener('resize', function () { document.querySelectorAll('.ms-drop').forEach(function (d) { d.style.display = 'none'; }); });
    document.addEventListener('click', function (e) {
      document.querySelectorAll('.ms-drop').forEach(function (d) {
        if (d.style.display === 'none') return;
        if (!d.__wrap || (!d.__wrap.contains(e.target) && !d.contains(e.target))) d.style.display = 'none';
      });
    });
  }

  window.MSEL = { attach: attach, attachAll: attachAll, syncAll: syncAll };
})();
