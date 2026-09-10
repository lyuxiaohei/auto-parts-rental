# -*- coding: utf-8 -*-
"""G12 助手6：dump 用户权限/项目档案/项目详情/BOM/盈亏报表/项目看板 内容区"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def content(path, name, span=1500):
    txt = open(ROOT + path, encoding='utf-8').read()
    i = txt.find('<div class="content">')
    print('=' * 70); print('##', name)
    print('--- content 起始段 ---')
    print(txt[i:i+span])
    tb = re.search(r'<tbody[^>]*>([\s\S]*?</tr>)', txt)
    if tb:
        print('--- tbody 首行 ---')
        print(re.sub(r'\n\s*', '\n', tb.group(1))[:900])

content(r'\系统管理\用户权限.html', '用户权限')
content(r'\项目管理\项目档案.html', '项目档案')
content(r'\项目管理\项目详情.html', '项目详情', 2200)
