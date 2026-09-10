# -*- coding: utf-8 -*-
"""G12 T3b：我的待办（实体重建行）+ 数据字典（分类切换渲染器）接线"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
ANCHOR = '/* ===== 菜单折叠 / 页签与表单视觉态（统一脚本） ===== */'

def insert_before_menu(path, block):
    txt = open(path, encoding='utf-8').read()
    assert txt.count(ANCHOR) == 1, 'anchor !=1: ' + path
    assert 'demo-data.js' not in txt, 'already wired: ' + path
    eol = '\r\n' if '\r\n' in txt else '\n'
    ci = txt.find(ANCHOR)
    si = txt.rfind('<script>', 0, ci)
    assert si > 0
    new = txt[:si] + block.replace('\n', eol) + txt[si:]
    new = new.replace('\r\n', '\n')
    open(path, 'w', encoding='utf-8', newline='\n').write(new)
    chk = open(path, encoding='utf-8').read()
    assert 'demo-data.js' in chk and ANCHOR in chk and chk.count('<html') == 1
    print('WIRED:', path)

# ---------- 我的待办（页面在原型根目录，src 无 ../） ----------
TODO_JS = r"""<script src="_data/demo-data.js"></script>
<script>
/* G12 数据驱动接线（2026-09-10）：#todoBody 由 todoItems 实体重建，filterTodo()/pickType() 原逻辑不变 */
(function () {
  var DATA = window.DEMO_DATA && window.DEMO_DATA.todoItems;
  if (!DATA) return;
  var tbody = document.getElementById('todoBody');
  if (!tbody) return;
  var keys = Object.keys(DATA);
  var html = '';
  keys.forEach(function (k) {
    var rec = DATA[k], f = rec.row.fields;
    html += '<tr data-type="' + f.type + '"><td><span class="tag tag-blue">' + f.type + '</span></td>' +
      '<td><span class="lk">' + k + '</span></td><td>' + f.summary + '</td><td>' + f.project + '</td>' +
      '<td>' + f.submitter + '</td><td>' + f.time + '</td><td><span class="tag tag-orange">' + f.action + '</span></td>' +
      '<td class="sticky-op"><span class="ops"><a onclick="go(\'' + rec.link + '\')">去审核</a></span></td></tr>' + '\n';
  });
  tbody.innerHTML = html;
  /* 统计卡计数联动（首卡 todoCount 由 filterTodo 维护） */
  var acts = {}, types = {};
  keys.forEach(function (k) { var f = DATA[k].row.fields; acts[f.action] = (acts[f.action] || 0) + 1; types[f.type] = 1; });
  var nums = document.querySelectorAll('.stat-grid .stat .st-num');
  if (nums.length >= 5) {
    nums[1].innerHTML = (acts['待审核'] || 0) + '<span class="unit">单</span>';
    nums[2].innerHTML = (acts['待验收'] || 0) + '<span class="unit">单</span>';
    nums[3].innerHTML = (acts['待确认'] || 0) + '<span class="unit">单</span>';
    nums[4].innerHTML = (acts['待入库'] || 0) + '<span class="unit">单</span>';
  }
  var foot0 = document.querySelector('.stat-grid .stat .st-foot');
  if (foot0) foot0.textContent = '覆盖 ' + Object.keys(types).length + ' 类单据 · 点击"去审核"直达审核弹窗';
  var pg = document.querySelector('.pg-info');
  if (pg) pg.textContent = '第 1-' + keys.length + ' 条 / 总共 ' + keys.length + ' 条待办';
  if (typeof filterTodo === 'function') filterTodo();
})();
</script>

"""
insert_before_menu(ROOT + r'\我的待办.html', TODO_JS)

# ---------- 数据字典（分类切换 + 计数联动；计费方式卡片保持静态） ----------
DICT_JS = r"""<script src="../_data/demo-data.js"></script>
<script>
/* G12 数据驱动接线（2026-09-10）：字典分类点击切换主表（道远点名交互）+ dictItems 实体渲染 + 分类计数联动 */
(function () {
  var DATA = window.DEMO_DATA && window.DEMO_DATA.dictItems;
  if (!DATA) return;
  var keysAll = Object.keys(DATA).filter(function (k) { return DATA[k].row; });
  var tbody = document.querySelector('.dic-wrap table tbody');
  var title = document.querySelector('.dic-wrap .card-head .card-title');
  var pg = document.querySelector('.dic-wrap .pg-info');
  var items = document.querySelectorAll('.dic-list .dic-item');
  if (!tbody) return;
  function byCat(cat) {
    return keysAll.filter(function (k) { return DATA[k].row.fields.category === cat; });
  }
  function render(cat) {
    var keys = byCat(cat);
    tbody.innerHTML = keys.length ? keys.map(function (k) {
      var r = DATA[k].row;
      var ops = r.ops.map(function (o) { return o.act ? '<a onclick="' + o.act + '">' + o.t + '</a>' : '<a>' + o.t + '</a>'; }).join('');
      return '<tr><td>' + k + '</td>' + r.cells.map(function (c) { return '<td>' + c + '</td>'; }).join('') +
        '<td class="sticky-op"><span class="ops">' + ops + '</span></td></tr>';
    }).join('\n') : '<tr><td colspan="7" style="text-align:center;color:#8c8c8c;padding:24px 0;">该分类暂无字典项</td></tr>';
    if (title) title.textContent = '字典项 · ' + cat;
    if (pg) pg.textContent = '第 1-' + keys.length + ' 条/总共 ' + keys.length + ' 条';
  }
  function refreshCounts(activeCat) {
    items.forEach(function (it) {
      var name = it.querySelector('span').textContent.trim();
      var cnt = it.querySelector('.cnt');
      if (cnt) { cnt.textContent = byCat(name).length; cnt.classList.toggle('hot', name === activeCat); }
      it.classList.toggle('active', name === activeCat);
    });
  }
  items.forEach(function (it) {
    it.addEventListener('click', function () {
      var cat = it.querySelector('span').textContent.trim();
      render(cat); refreshCounts(cat);
    });
  });
  var init = document.querySelector('.dic-list .dic-item.active span');
  var cat0 = init ? init.textContent.trim() : '缺损类型';
  render(cat0); refreshCounts(cat0);
})();
</script>

"""
insert_before_menu(ROOT + r'\系统管理\数据字典.html', DICT_JS)
print('自写渲染器 2 页接线完成')
