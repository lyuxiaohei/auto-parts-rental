# -*- coding: utf-8 -*-
"""C2 修复2：①stockFlows 项目码缩写展开为全码（fields.project + cells 第3列）②下钻点击钩子（不依赖 openModal 包装时序）"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

# ---- ① demo-data 项目码展开 ----
FP = os.path.join(ROOT, '_data', 'demo-data.js')
s = io.open(FP, encoding='utf-8', newline='').read()

EXPAND = {
    'PRJ-2601/02/04': 'PRJ-2601/PRJ-2602/PRJ-2604',
    'PRJ-2601/02': 'PRJ-2601/PRJ-2602',
    'PRJ-2601/04': 'PRJ-2601/PRJ-2604',
    'PRJ-2603/05': 'PRJ-2603/PRJ-2605',
    'PRJ-2602/03': 'PRJ-2602/PRJ-2603',
}
cnt = 0
for old, new in EXPAND.items():
    # fields.project 值
    cnt += s.count('"project": "%s"' % old)
    s = s.replace('"project": "%s"' % old, '"project": "%s"' % new)
    # cells 中的适用项目列（裸字符串单元格）
    cnt += s.count(', "%s", ' % old)
    s = s.replace(', "%s", ' % old, ', "%s", ' % new)
print('demo-data 项目码展开：替换 %d 处' % cnt)
assert 'PRJ-2601/02' not in s.replace('PRJ-2601/0200', '')  # 无残留缩写（粗校）
io.open(FP, 'w', encoding='utf-8', newline='').write(s)

# ---- ② 库存查询 下钻点击钩子 ----
FP2 = os.path.join(ROOT, '仓储作业', '库存查询.html')
t = io.open(FP2, encoding='utf-8', newline='').read()
old_hook = "  var _om = window.openModal;\n  if (typeof _om === 'function') {\n    window.openModal = function (id) { _om(id); setTimeout(function () { recalcDrill(projVal()); }, 0); };\n  }"
new_hook = old_hook + """
  /* 兜底：点击「客户在租」打开下钻弹窗时同步（捕获相，先于 onclick 执行，setTimeout 0 延后渲染后） */
  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[onclick*="rentDrillModal"]') : null;
    if (el) setTimeout(function () { recalcDrill(projVal()); }, 0);
  }, true);"""
assert t.count(old_hook) == 1, 'openModal wrapper anchor x%d' % t.count(old_hook)
t = t.replace(old_hook, new_hook)
io.open(FP2, 'w', encoding='utf-8', newline='').write(t)
print('下钻点击钩子已加 ✓')
