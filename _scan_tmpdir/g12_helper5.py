# -*- coding: utf-8 -*-
"""G12 助手5：dump 操作日志/我的待办/用户权限 内容区（sidebar 之后到第一表）+ tbody 首行"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def content(path, name, tail=0):
    txt = open(ROOT + path, encoding='utf-8').read()
    i = txt.find('<div class="content">')
    j = txt.find('<table', i)
    print('=' * 70); print('##', name, ' content→table 段:')
    print(txt[i:j][:1800])
    # tbody 首2行
    tb = re.search(r'<tbody[^>]*>([\s\S]*?</tr>[\s\S]*?</tr>)', txt)
    if tb:
        print('  --- tbody 前2行 ---')
        print(re.sub(r'\n\s*', '\n', tb.group(1))[:1200])

content(r'\系统管理\操作日志.html', '操作日志')
content(r'\我的待办.html', '我的待办')
