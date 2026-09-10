# -*- coding: utf-8 -*-
"""G12 助手2：提取 A 类页面关键结构（thead/筛选/stabs/script/tbody 首行）"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
PAGES = [
    r'\系统管理\角色管理.html',      # 已驱动参照
    r'\我的待办.html',
    r'\系统管理\操作日志.html',
    r'\系统管理\数据字典.html',
    r'\系统管理\用户权限.html',
    r'\项目管理\项目档案.html',
    r'\项目管理\项目详情.html',
    r'\基础数据\BOM.html',
    r'\财务协同\盈亏报表.html',
    r'\首页\项目看板.html',
]
for p in PAGES:
    txt = open(ROOT + p, encoding='utf-8').read()
    print('=' * 70)
    print('PAGE:', p, ' len=', len(txt))
    for m in re.finditer(r'<script[^>]*src="([^"]+)"[^>]*></script>', txt):
        print('  [src]', m.group(1))
    for m in re.finditer(r'<script>\s*\n?(/\*[^\n]*)?\n?(renderListPage[\s\S]{0,500}?)</script>', txt):
        print('  [renderListPage]', re.sub(r'\s+', ' ', m.group(2))[:400])
    # stabs
    st = re.search(r'class="stabs"[^>]*>([\s\S]*?)</div>', txt)
    if st:
        print('  [stabs]', re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', st.group(1)))[:220])
    # filter-bar 标签
    fb = re.search(r'class="filter-bar"([\s\S]{0,2000}?)</div>\s*(<div|<div class="table|<table|<section)', txt)
    if fb:
        labels = re.findall(r'<label[^>]*>([^<]{1,14})</label>|\bplaceholder="([^"]{1,16})"', fb.group(1))
        print('  [filter labels]', [a or b for a, b in labels][:12])
    # 所有表头
    for tm in re.finditer(r'<table[^>]*>([\s\S]*?)</table>', txt):
        t = tm.group(1)
        head = re.search(r'<thead[^>]*>([\s\S]*?)</thead>', t)
        rows = len(re.findall(r'<tr', t))
        if head:
            cols = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', head.group(1)))
            print(f'  [table rows={rows}] {cols[:260]}')
    # tbody 首行样例
    tb = re.search(r'<tbody[^>]*>\s*(<tr>[\s\S]{0,400}?)</tr>', txt)
    if tb:
        print('  [tbody r1]', re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', tb.group(1)))[:260])
