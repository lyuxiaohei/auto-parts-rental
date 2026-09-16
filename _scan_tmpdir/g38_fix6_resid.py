# -*- coding: utf-8 -*-
"""G38 fix6：src 引文/租赁器具 残留清零＋field_gate 禁用词补录"""
import io, os, re

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

# 1. 全站注入块 src 引文（A03 数据源已新·HTML 陈旧副本）
n_files = 0
for root, ds, fs in os.walk(BASE):
    if 'backup' in root:
        continue
    for f in fs:
        if not f.endswith('.html'):
            continue
        p = os.path.join(root, f)
        t = io.open(p, encoding='utf-8', newline='').read()
        if '按零配件、以托为单位入库' in t:
            t = t.replace('按零配件、以托为单位入库', '按物料基本单位入库（D-145）')
            io.open(p, 'w', encoding='utf-8', newline='').write(t)
            n_files += 1
print('[OK] src 引文同步 %d 文件' % n_files)

# 2. 租赁单列表 下钻 th 租赁器具→物料
p = BASE + r'\租赁管理\租赁单列表.html'
t = io.open(p, encoding='utf-8', newline='').read()
assert t.count('<th>租赁器具</th>') == 1, t.count('<th>租赁器具</th>')
t = t.replace('<th>租赁器具</th>', '<th>物料</th>')
assert t.count('租赁器具') == 0
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('[OK] 租赁单列表 下钻 th 租赁器具→物料')

# 3. 租赁单新建 节标题 租赁器具明细→租赁明细
p = BASE + r'\租赁管理\租赁单新建.html'
t = io.open(p, encoding='utf-8', newline='').read()
assert t.count('租赁器具明细') == 1, t.count('租赁器具明细')
t = t.replace('租赁器具明细', '租赁明细')
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('[OK] 租赁单新建 节标题 租赁器具明细→租赁明细')

# 4. field_gate 禁用词补录「租赁器具」（字段名位置）
gp = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\field_gate.py'
g = io.open(gp, encoding='utf-8', newline='').read()
old = "FORBIDDEN_SUBSTR = ['货品', '库区', '零件号', '托数', '每托数量', '入库总数']"
new = "FORBIDDEN_SUBSTR = ['货品', '库区', '零件号', '托数', '每托数量', '入库总数', '租赁器具']"
assert g.count(old) == 1
io.open(gp, 'w', encoding='utf-8', newline='').write(g.replace(old, new))
print('[OK] field_gate 禁用词 +租赁器具')
