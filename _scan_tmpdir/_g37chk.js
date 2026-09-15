
(function () {
  var ENT = 'transferOutbounds', DEF = 'ZY-20260914-001';
  var k = null;
  try { k = new URLSearchParams(location.search).get("id"); } catch (e) {}
  var D = (window.DEMO_DATA || {})[ENT] || {};
  if (!D[k]) k = Object.keys(D).filter(function (x) { return D[x] && JSON.stringify(D[x]).replace(/\s/g, "").indexOf('"tag":"待') > -1; })[0]    || Object.keys(D).filter(function (x) { return D[x] && (D[x].info || D[x].title); })[0] || DEF;
  var rec = D[k] || {};
  var t = document.getElementById("dtTitle");
  if (t) t.textContent = (rec.title || '转移出库单详情') + " · " + (rec.titleNo || k);
  var el = document.getElementById("detailBody");
  if (el && window.renderGenericDetailHTML) el.innerHTML = window.renderGenericDetailHTML(rec, "../");
})();

;

/* ===== 菜单折叠 / 页签与表单视觉态（统一脚本） ===== */
function go(url) { location.href = url; }
document.querySelectorAll('.sm-item.has-sub > .sm-link').forEach(function (link) {
  link.addEventListener('click', function () { link.parentElement.classList.toggle('open'); });
});
/* 状态页签切换（视觉选中态） */
document.querySelectorAll('.stabs .stab').forEach(function (tab) {
  tab.addEventListener('click', function () {
    tab.parentElement.querySelectorAll('.stab').forEach(function (t) { t.classList.remove('active'); });
    tab.classList.add('active');
  });
});
/* 表单单选/复选视觉态切换 */
document.querySelectorAll('.radio').forEach(function (r) {
  r.addEventListener('click', function () {
    r.parentElement.querySelectorAll('.radio').forEach(function (x) { x.classList.remove('checked'); });
    r.classList.add('checked');
  });
});
document.querySelectorAll('.checkbox').forEach(function (c) {
  c.addEventListener('click', function () { c.classList.toggle('checked'); });
});

;
/*ia-fix: tab-switch + btn-feedback (2026-09-04)*/
/* R3 顶部页签切换（点击换 active；× 不做关闭跳转——原型不销毁页签） */
document.querySelectorAll('.tab').forEach(function (t) {
  t.addEventListener('click', function () {
    document.querySelectorAll('.tab').forEach(function (x) { x.classList.remove('active'); });
    t.classList.add('active');
  });
});
/* R1 死按钮全局反馈：无 onclick 的 button/a 给按压视觉态；「重置」清空所在筛选卡 */
(function () {
  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('button, a, .sm-link') : null;
    if (!el) return;
    if (el.getAttribute('onclick')) return;
    var h = el.getAttribute('href');
    if (el.tagName === 'A' && h && h !== '#' && !/^javascript:/i.test(h)) return;
    if (el.disabled) return;
    var txt = (el.textContent || '').trim();
    if (txt === '重置') {
      var card = el.closest('.filter-card') || el.closest('.card');
      if (card) {
        card.querySelectorAll('input:not([type=checkbox]):not([type=radio])').forEach(function (i) { if (!i.readOnly && !i.disabled) i.value = ''; });
        card.querySelectorAll('select').forEach(function (s) { if (!s.disabled) s.selectedIndex = 0; });
      }
    }
    el.style.transition = 'transform .08s';
    el.style.transform = 'scale(.96)';
    setTimeout(function () { el.style.transform = ''; }, 160);
  }, true);
})();

;

(function(){
  var KEY='proto-notes-on';
  function on(){return location.search.indexOf('notes=1')>-1||localStorage.getItem(KEY)==='1'}
  function apply(){
    document.body.classList.toggle('proto-notes-on',on());
    var fab=document.getElementById('protoNotesFab');
    if(fab){fab.innerHTML=on()?'收起':'标注 <span class="pn-fab-n">'+(document.querySelectorAll('[data-note]').length)+'</span>';fab.title=on()?'收起标注（Alt+N）':'显示标注（Alt+N）'}
  }
  function toggle(){var v=!on();localStorage.setItem(KEY,v?'1':'0');apply()}
  document.addEventListener('keydown',function(e){if(e.altKey&&(e.key==='n'||e.key==='N')){e.preventDefault();toggle()}});
  function place(el,pin){
    var r=el.getBoundingClientRect(),sx=window.scrollX||0,sy=window.scrollY||0;
    var w=pin.offsetWidth||248,h=pin.offsetHeight||90,vw=document.documentElement.clientWidth;
    var x=r.right+sx+12;
    if(x+w>sx+vw-8){var xl=r.left+sx-w-12;x=xl>=sx+8?xl:(sx+vw-w-8)}
    var y=r.top+sy;
    if(y+h>sy+document.documentElement.clientHeight-8)y=Math.max(sy+52,r.bottom+sy-h);
    pin.style.left=x+'px';pin.style.top=y+'px';
  }
  document.addEventListener('click',function(e){
    if(!on())return;
    var tgt=e.target.closest?e.target.closest('[data-note]'):null;
    if(tgt){
      var r=tgt.getBoundingClientRect();
      if(e.clientX>r.right-24&&e.clientY<r.top+22){
        e.stopPropagation();e.preventDefault();
        var pin=document.getElementById('proto-pin-'+tgt.getAttribute('data-note'));
        if(pin){
          if(pin.classList.contains('pn-open')){pin.classList.remove('pn-open')}
          else{pin.classList.add('pn-open');place(tgt,pin)}
        }
      }
    }
  },true);
  document.addEventListener('click',function(e){
    var t=e.target;
    var fab=t.closest?t.closest('.pn-fab'):null;
    if(fab){toggle();return}
    var pc=t.closest?t.closest('.proto-pin'):null;
    if(pc){
      if(t.classList&&t.classList.contains('pnp-close'))pc.classList.remove('pn-open');
      return;
    }
  });
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply);else apply();
})();
