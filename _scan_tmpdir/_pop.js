/* 盘点关联单据 +N 气泡 & 盘盈亏生成出入库 · 2026-09-11 · 无蒙层小弹窗（数据驱动版） */
(function () {
  var DOCS = {
    'PD-202608-02': { dir: 'in',  list: [
      { no: 'QTRK-20260816-023', tag: '围板箱 +12 · 已入库' },
      { no: 'QTRK-20260816-024', tag: '托盘 +6 · 已入库' } ] },
    'PD-202607-02': { dir: 'out', list: [
      { no: 'QTCK-20260731-005', tag: '锁扣组件 -1 · 已出库' },
      { no: 'QTCK-20260731-006', tag: '内衬 -1 · 已出库' },
      { no: 'QTCK-20260801-007', tag: '围板 补录 · 已出库' } ] },
    'PD-202606-01': { dir: 'in',  list: [
      { no: 'QTRK-20260630-011', tag: '料箱 +3 · 已入库' } ] }
  };
  var TARGET = { in: '../仓储作业/其他入库列表.html', out: '../仓储作业/其他出库列表.html' };
  var NAME = { in: '其他入库单', out: '其他出库单' };
  var pop = document.getElementById('docsPop');
  function place(x, y) {
    pop.style.display = 'block';
    var r = pop.getBoundingClientRect();
    pop.style.left = Math.min(x, window.scrollX + document.documentElement.clientWidth - r.width - 12) + 'px';
    pop.style.top = (y + 18) + 'px';
  }
  function close() { pop.style.display = 'none'; pop.innerHTML = ''; }
  window.addEventListener('click', function (e) { if (!pop.contains(e.target)) close(); }, true);

  function bindPlus() {
    document.querySelectorAll('.docs-plus').forEach(function (a) {
      if (a._bound) return; a._bound = true;
      a.addEventListener('click', function (e) {
        e.stopPropagation();
        var tr = a.closest('tr');
        var pd = tr ? (tr.querySelector('.lk') ? tr.querySelector('.lk').textContent.trim() : '') : '';
        var d = DOCS[pd] || { list: [] };
        var rows = d.list.map(function (it) {
          return '<div class="dp-row"><span class="lk" onclick="go(\'' + TARGET[d.dir] + '\')">' + it.no + '</span><span class="dp-tag">' + it.tag + '</span></div>';
        }).join('');
        pop.innerHTML = '<div class="dp-t">' + pd + ' · 关联' + NAME[d.dir] + '<span class="dp-x">×</span></div>' + rows;
        pop.querySelector('.dp-x').addEventListener('click', close);
        var rc = a.getBoundingClientRect();
        place(rc.left + window.scrollX - 60, rc.bottom + window.scrollY);
      });
    });
  }
  /* renderListPage 渲染完后绑定（渲染是同步的，DOMContentLoaded 后跑一次+轮询兜底） */
  function boot() { bindPlus(); setTimeout(bindPlus, 400); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();

  window.showGen = function (dir, ev) {
    ev && ev.stopPropagation && ev.stopPropagation();
    var tr = ev.target.closest('tr'); var pd = tr ? (tr.querySelector('.lk').textContent.trim()) : '';
    pop.innerHTML = '<div class="dp-t">生成' + NAME[dir] + '<span class="dp-x">×</span></div>'
      + '<div style="line-height:1.8">将按 ' + pd + ' 的盘' + (dir === 'in' ? '盈' : '亏') + '明细自动生成' + NAME[dir] + '草稿，入库/出库后库存即时调整。</div>'
      + '<div class="dp-go"><button class="btn btn-sm" id="dpGen">生成草稿</button><span class="dp-ok" id="dpDone" style="display:none"></span></div>';
    pop.querySelector('.dp-x').addEventListener('click', close);
    pop.querySelector('#dpGen').addEventListener('click', function () {
      var no = (dir === 'in' ? 'QTRK-' : 'QTCK-') + '20260911-0' + Math.ceil(Math.random() * 9);
      this.style.display = 'none';
      var done = pop.querySelector('#dpDone');
      done.style.display = 'inline';
      done.innerHTML = '已生成 <span class="lk" onclick="go(\'' + TARGET[dir] + '\')">' + no + '</span> · 点击单号前往查看';
    });
    var rc = ev.target.getBoundingClientRect();
    place(rc.left + window.scrollX - 80, rc.bottom + window.scrollY);
  };
})();
