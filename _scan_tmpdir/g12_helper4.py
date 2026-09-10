# -*- coding: utf-8 -*-
"""G12 助手4：dump 三页筛选区/工具条原文"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def dump_toolbar(path, name):
    txt = open(ROOT + path, encoding='utf-8').read()
    body = txt[txt.find('<body'):]
    print('=' * 70); print('##', name)
    # toolbar/filter 相关片段
    for kw in ['filter', 'toolbar', '筛选', 'tabs']:
        for m in re.finditer(r'<div class="[^"]*' + kw + r'[^"]*"[\s\S]{0,900}?</div>\s*<', body[:body.find('<table')] if kw != 'tabs' else []):
            pass
    # 简化：抓 content 起始到第一个 table 之间的全部标记
    i_tb = body.find('<table')
    pre = body[:i_tb]
    # 只留标签行
    tags = re.findall(r'<(div|label|input|select|option|button|span)[^>]*>[^<]{0,24}', pre)
    print('  [table 前的标签流]')
    depth = 0
    for line in re.findall(r'<[^>]+>|[^<>{2,}]+', pre):
        s = line.strip()
        if s.startswith('<'):
            print('   ', s[:150])

dump_toolbar(r'\系统管理\数据字典.html', '数据字典 table 前结构')
