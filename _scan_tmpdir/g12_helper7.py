# -*- coding: utf-8 -*-
"""G12 助手7：dump BOM/盈亏报表/项目看板 内容区 + 项目详情 content 定位"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def seg(path, name, start_kw='<div class="content', span=1400):
    txt = open(ROOT + path, encoding='utf-8').read()
    i = txt.find(start_kw)
    print('=' * 70); print('##', name, 'at', i)
    if i >= 0: print(txt[i:i+span])
    tb = re.search(r'<tbody[^>]*>([\s\S]*?</tr>)', txt)
    if tb:
        print('--- tbody 首行 ---')
        print(re.sub(r'\n\s*', '\n', tb.group(1))[:800])

seg(r'\基础数据\BOM.html', 'BOM')
seg(r'\财务协同\盈亏报表.html', '盈亏报表')
seg(r'\首页\项目看板.html', '项目看板')
seg(r'\项目管理\项目详情.html', '项目详情', '<div class="main-col">')
