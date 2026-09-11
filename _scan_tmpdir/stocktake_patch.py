# -*- coding: utf-8 -*-
"""盘点列表改造：关联单据列(+N 气泡) + 盘盈亏生成出入库按钮(无蒙层小弹窗) · 2026-09-11"""
import pathlib, re

f = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\仓储作业\盘点列表.html")
s = f.read_text(encoding='utf-8')

# 1) 列头加「关联单据」（盈亏合计后）
s = s.replace('          <th>盈亏合计</th>\n', '          <th>盈亏合计</th>\n          <th>关联单据</th>\n', 1)

def docs_td(first, n):
    if n == 0:
        return '          <td><span class="lk">' + first + '</span></td>\n'
    return ('          <td><span class="lk">' + first + '</span> '
            '<a class="docs-plus">' + str(n) + '</a></td>\n')

# 2) 每行插 td + 操作列加生成按钮
rows = {
 'PD-202608-02': ('QTRK-20260816-023', 1, 'in'),   # 盘盈 2 条入库 → +1
 'PD-202607-02': ('QTCK-20260731-005', 2, 'out'),  # 盘亏 3 条出库 → +2
 'PD-202606-01': ('QTRK-20260630-011', 0, 'in'),   # 盘盈 1 条 → 无 +N
}
for pd, (first, n, typ) in rows.items():
    i = s.find(pd)
    assert i > 0, pd
    seg_end = s.find('</tr>', i)
    seg = s[i:seg_end]
    m = re.search(r'(<td class="sticky-op">)', seg)
    seg = seg[:m.start(1)] + docs_td(first, n).rstrip('\n') + '\n          ' + seg[m.start(1):]
    det = seg.find('详情</a>')
    btn = '<a onclick="showGen(\'in\', event)">生成入库</a>' if typ == 'in' else '<a onclick="showGen(\'out\', event)">生成出库</a>'
    seg = seg[:det+4] + btn + seg[det+4:]
    s = s[:i] + seg + s[seg_end:]

# 3) 无盈亏两行补空 td
for pd in ['PD-202608-03', 'PD-202607-01']:
    i = s.find(pd); seg_end = s.find('</tr>', i)
    seg = s[i:seg_end]
    m = re.search(r'(<td class="sticky-op">)', seg)
    seg = seg[:m.start(1)] + '          <td>—</td>\n          ' + seg[m.start(1):]
    s = s[:i] + seg + s[seg_end:]

INJ = '''
<style id="docs-pop-css">
.docs-plus{display:inline-flex;align-items:center;justify-content:center;min-width:20px;height:18px;padding:0 5px;margin-left:4px;border:1px solid #d9d9d9;border-radius:9px;background:#fafafa;color:#8c8c8c;font-size:11px;cursor:pointer;user-select:none}
.docs-plus:hover{border-color:#1677ff;color:#1677ff}
.docs-pop{position:absolute;z-index:1200;min-width:230px;max-width:320px;background:#fff;border:1px solid #e5e6eb;border-radius:8px;box-shadow:0 6px 20px rgba(0,0,0,.14);padding:10px 12px;font-size:12px;color:#262626;display:none}
.docs-pop .dp-t{font-weight:600;margin-bottom:6px;padding-bottom:6px;border-bottom:1px solid #f0f0f0;display:flex;justify-content:space-between;align-items:center}
.docs-pop .dp-x{cursor:pointer;color:#8c8c8c;font-weight:400;padding:0 4px}
.docs-pop .dp-x:hover{color:#262626}
.docs-pop .dp-row{display:flex;justify-content:space-between;align-items:center;padding:5px 0;gap:12px}
.docs-pop .dp-row .lk{font-size:12px}
.docs-pop .dp-tag{flex:none;font-size:11px;color:#8c8c8c}
.docs-pop .dp-go{margin-top:8px;padding-top:8px;border-top:1px dashed #f0f0f0;display:flex;gap:10px;align-items:center}
.docs-pop .dp-ok{color:#52c41a;font-weight:600}
</style>
<div class="docs-pop" id="docsPop"></div>
<script id="docs-pop-js">/* 盘点关联单据 +N 气泡 & 盘盈亏生成出入库 · 2026-09-11 · 无蒙层小弹窗 */
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

  document.querySelectorAll('.docs-plus').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.stopPropagation();
      var tr = a.closest('tr'); var pd = tr ? (tr.querySelector('.lk') ? tr.querySelector('.lk').textContent.trim() : '') : '';
      var d = DOCS[pd] || { list: [] };
      var rows = d.list.map(function (it) {
        return '<div class="dp-row"><span class="lk" onclick="go(\\'' + TARGET[d.dir] + '\\')">' + it.no + '</span><span class="dp-tag">' + it.tag + '</span></div>';
      }).join('');
      pop.innerHTML = '<div class="dp-t">' + pd + ' · 关联' + NAME[d.dir] + '<span class="dp-x">×</span></div>' + rows;
      pop.querySelector('.dp-x').addEventListener('click', close);
      var rc = a.getBoundingClientRect();
      place(rc.left + window.scrollX - 60, rc.bottom + window.scrollY);
    });
  });

  window.showGen = function (dir, ev) {
    ev && ev.stopPropagation && ev.stopPropagation();
    var tr = ev.target.closest('tr'); var pd = tr ? tr.querySelector('.lk').textContent.trim() : '';
    pop.innerHTML = '<div class="dp-t">生成' + NAME[dir] + '<span class="dp-x">×</span></div>'
      + '<div style="line-height:1.8">将按 ' + pd + ' 的盘' + (dir === 'in' ? '盈' : '亏') + '明细自动生成' + NAME[dir] + '草稿，入库/出库后库存即时调整。</div>'
      + '<div class="dp-go"><button class="btn btn-sm" id="dpGen">生成草稿</button><span class="dp-ok" id="dpDone" style="display:none"></span></div>';
    pop.querySelector('.dp-x').addEventListener('click', close);
    pop.querySelector('#dpGen').addEventListener('click', function () {
      var no = (dir === 'in' ? 'QTRK-' : 'QTCK-') + '20260911-0' + Math.ceil(Math.random() * 9);
      this.style.display = 'none';
      var done = pop.querySelector('#dpDone');
      done.style.display = 'inline';
      done.innerHTML = '已生成 <span class="lk" onclick="go(\\'' + TARGET[dir] + '\\')">' + no + '</span> · 点击单号前往查看';
    });
    var rc = ev.target.getBoundingClientRect();
    place(rc.left + window.scrollX - 80, rc.bottom + window.scrollY);
  };
})();
</script>
'''
s = s.replace('</body>', INJ + '</body>', 1)
f.write_text(s, encoding='utf-8', newline='')
print('盘点列表改造完成')
