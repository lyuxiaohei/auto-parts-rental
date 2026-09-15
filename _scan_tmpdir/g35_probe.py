# -*- coding: utf-8 -*-
import io, re
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
txt = io.open(ROOT + r'\我的待办.html', encoding='utf-8').read()
i = txt.find('<div class="filter-card')
depth = 0; j = i
for m in re.finditer(r'<div\b|</div>', txt[i:]):
    depth += 1 if m.group(0).startswith('<div') else -1
    if depth == 0:
        j = i + m.end(); break
print('=== 我的待办 filter-card ===')
print(txt[i:j].replace('\r\n', '\n'))
print()
t2 = io.open(ROOT + r'\基础数据\BOM.html', encoding='utf-8').read()
k = t2.find('renderListPage(')
k2 = t2.find('</script>', k)
print('=== BOM cfg script tail (repr) ===')
print(repr(t2[k2-40:k2+15]))
print()
pages = ['仓储作业/库存查询', '租入管理/租入入库列表', '采购管理/采购入库列表', '系统管理/操作日志',
         '销售管理/销售订单列表', '销售管理/销售出库列表', '租赁管理/退租入库列表', '租入管理/租入归还列表',
         '财务协同/付款登记', '财务协同/应付账单', '系统管理/用户权限', '基础数据/客商管理',
         '租赁管理/租赁单列表', '项目管理/项目档案', '我的待办', '基础数据/BOM']
for p in pages:
    t = io.open(ROOT + '\\' + p + '.html', encoding='utf-8').read()
    print('%s: %s' % (p, 'CRLF' if '\r\n' in t else 'LF'))
