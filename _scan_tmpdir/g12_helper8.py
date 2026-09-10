# -*- coding: utf-8 -*-
"""G12 助手8：最后确认——filterTodo 实现/项目详情 stabs/盈亏 ff 全表/用户权限 roles 表"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

# 1. 我的待办 filterTodo
txt = open(ROOT + r'\我的待办.html', encoding='utf-8').read()
i = txt.find('function filterTodo')
print('## 我的待办 filterTodo:')
print(txt[i-200:i+1400] if i > 0 else 'NOT FOUND')

# 2. 项目详情 stabs + filter + tbody 位置
txt2 = open(ROOT + r'\项目管理\项目详情.html', encoding='utf-8').read()
i = txt2.find('class="stabs"')
print('\n## 项目详情 stabs 段:')
print(txt2[i-300:i+500] if i > 0 else '无 stabs')
print('filter-card:', 'filter-card' in txt2)

# 3. 盈亏报表 ff 标签全集
txt3 = open(ROOT + r'\财务协同\盈亏报表.html', encoding='utf-8').read()
seg = txt3[txt3.find('filter-card'):txt3.find('<table')]
labels = re.findall(r'<span class="ff-label">([^<]*)</span>', seg)
print('\n## 盈亏报表 ff-labels:', labels)

# 4. 用户权限 roles 二表 tbody 前行
txt4 = open(ROOT + r'\系统管理\用户权限.html', encoding='utf-8').read()
tbs = re.findall(r'<tbody[^>]*>([\s\S]{0,300}?)</tr>', txt4)
print('\n## 用户权限 第2个 tbody 首行:', re.sub(r'\s+', ' ', tbs[1])[:280] if len(tbs) > 1 else 'MISSING')
print('openRolePerm 定义?', 'function openRolePerm' in txt4, '| 引用?', 'openRolePerm(' in txt4)
