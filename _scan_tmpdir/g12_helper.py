# -*- coding: utf-8 -*-
"""G12 助手：查看已驱动页接线样例 + 实体 row 结构"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

txt = open(ROOT + r'\租赁管理\租赁单列表.html', encoding='utf-8').read()
print('=== 租赁单列表.html script 引用 ===')
for m in re.finditer(r'<script[^>]*src="[^"]*"[^>]*></script>', txt):
    print(' ', m.group(0))
m = re.search(r'<script>\s*renderListPage[\s\S]*?</script>', txt)
print('--- renderListPage 调用 ---')
print(m.group(0)[:1600] if m else 'NOT FOUND')

print()
print('=== roles 实体头 45 行 ===')
dd = open(ROOT + r'\_data\demo-data.js', encoding='utf-8').read().split('\n')
print('\n'.join(dd[15332:15378]))
