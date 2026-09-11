# -*- coding: utf-8 -*-
"""盘点记录改造 v2（数据驱动版）：demo-data stocktakes 实体 + 页面 th/popover · 2026-09-11
- 列表加「关联单据」列（盈亏合计后）：第一条单号 + (+N 气囊，点开无蒙层小弹窗)
- 盘盈行操作加「生成入库」、盘亏行加「生成出库」（详情后）
"""
import pathlib, re

ROOT = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")

# ---------- 1) demo-data.js：stocktakes 三行加关联单据 cell + ops ----------
dd = ROOT / '_data' / 'demo-data.js'
s = dd.read_text(encoding='utf-8')
i0 = s.find('stocktakes:')
i1 = s.find('\n  },', i0)
seg = s[i0:i1]

def esc(t): return t.replace('\\', '\\\\').replace('"', '\\"')

# 关联单据 cell（HTML）——注意 JS 双引号串内转义
CELL = {
 'PD-202608-02': '<span class=\\"lk\\">QTRK-20260816-023</span> <a class=\\"docs-plus\\">1</a>',
 'PD-202607-02': '<span class=\\"lk\\">QTCK-20260731-005</span> <a class=\\"docs-plus\\">2</a>',
 'PD-202606-01': '<span class=\\"lk\\">QTRK-20260630-011</span>',
}
EMPTY = '—'
BTN_IN = '{\\"t\\": \\"生成入库\\", \\"act\\": \\"showGen(' + "'in'" + ', event)\\"}'
BTN_OUT = '{\\"t\\": \\"生成出库\\", \\"act\\": \\"showGen(' + "'out'" + ', event)\\"}'

for key in ['PD-202608-03', 'PD-202607-01']:
    seg = re.sub(r"('%s': \{.*?\"ops\": \[)(.*?)(\] \})" % key,
                 lambda m: m.group(1) + m.group(2) + m.group(3), seg)  # 保持原 ops

def patch_row(seg, key, cell_html, extra_op):
    # cells 末尾插入关联单据（在 ops 前的 cells 数组闭合处插）——cells 结构：[..., 最后一个cell"]，ops 在 cells 后
    # 安全法：在 "ops": [ 前插入 cell 到 cells 末尾 + ops 头插按钮
    pat = re.compile(r"('%s': \{.*?)(\"ops\": \[)(.*?)(\] \})" % key, re.S)
    def rep(m):
        head, opk, ops, tail = m.group(1), m.group(2), m.group(3), m.group(4)
        # cells 末尾插 cell：head 里最后一个 "]," 是 cells 结束
        ci = head.rfind('"], "ops"')
        if ci < 0:
            ci = head.rfind('"], ')
        head2 = head[:ci] + '", "' + cell_html + head[ci+1:]
        return head2 + opk + ' ' + extra_op + ', ' + ops + tail
    return pat.sub(rep, seg, count=1)

seg = patch_row(seg, 'PD-202608-02', CELL['PD-202608-02'], BTN_IN)
seg = patch_row(seg, 'PD-202607-02', CELL['PD-202607-02'], BTN_OUT)
seg = patch_row(seg, 'PD-202606-01', CELL['PD-202606-01'], BTN_IN)
# 两行正常单补空 cell（无按钮）
for key in ['PD-202608-03', 'PD-202607-01']:
    pat = re.compile(r"('%s': \{.*?)(\"ops\": \[)" % key, re.S)
    seg = pat.sub(lambda m: m.group(1)[:-2] + ', "' + EMPTY + '"], ' + m.group(2), seg, count=1)

s = s[:i0] + seg + s[i1:]
dd.write_text(s, encoding='utf-8', newline='')
print('demo-data stocktakes 改造完成')

# ---------- 2) 盘点列表.html：th 加列 + 尾部注入 popover ----------
pg = ROOT / '仓储作业' / '盘点列表.html'
h = pg.read_text(encoding='utf-8')
h = h.replace('          <th>盈亏合计</th>\n', '          <th>盈亏合计</th>\n          <th>关联单据</th>\n', 1)
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
<script id="docs-pop-js">/* 盘点关联单据 +N 气泡 & 盘盈亏生成出入库 · 2026-09-11 · 无蒙层小弹窗（数据驱动版） */
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
          return '<div class="dp-row"><span class="lk" onclick="go(\\'' + TARGET[d.dir] + '\\')">' + it.no + '</span><span class="dp-tag">' + it.tag + '</span></div>';
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
      done.innerHTML = '已生成 <span class="lk" onclick="go(\\'' + TARGET[dir] + '\\')">' + no + '</span> · 点击单号前往查看';
    });
    var rc = ev.target.getBoundingClientRect();
    place(rc.left + window.scrollX - 80, rc.bottom + window.scrollY);
  };
})();
</script>
'''
h = h.replace('</body>', INJ + '</body>', 1)
pg.write_text(h, encoding='utf-8', newline='')
print('盘点列表.html 注入完成')
