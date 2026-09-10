# -*- coding: utf-8 -*-
"""G12 助手3：A 页筛选区标签 + bomVersions 结构 + BOM维护接线 + 角色管理调用 + 数据字典布局"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def sect(name, path, fn):
    print('=' * 70); print('##', name)
    txt = open(ROOT + path, encoding='utf-8').read()
    fn(txt)

def filters_of(txt):
    m = re.search(r'<div class="filter-card"[\s\S]*?(?=<div class="table-wrap|<table|<section|<div class="card)</div>\s*</div>', txt)
    # 更稳：抓 filter-card 起至 </div> 三层闭合的片段（截 3000 字符）
    i = txt.find('filter-card')
    if i < 0:
        print('  无 filter-card'); return
    seg = txt[i-20:i+3000]
    labels = re.findall(r'<label class="ff-label">([^<]+)</label>', seg)
    selects = re.findall(r'<select[\s\S]*?</select>', seg)
    print('  [ff-labels]', labels)
    for s in selects[:6]:
        opts = re.findall(r'<option[^>]*>([^<]*)</option>', s)
        print('  [select]', opts[:10])
    btns = re.findall(r'<button[^>]*>([^<]{1,6})</button>', seg)
    print('  [buttons]', btns[:8])

sect('我的待办 筛选', r'\我的待办.html', filters_of)
sect('操作日志 筛选', r'\系统管理\操作日志.html', filters_of)
sect('数据字典 筛选+布局', r'\系统管理\数据字典.html', lambda t: (filters_of(t), print('  [段落标题]', re.findall(r'<h[23][^>]*>([^<]{2,20})</h[23]>', t))))
sect('用户权限 筛选+表格分布', r'\系统管理\用户权限.html', lambda t: (filters_of(t), print('  [h3]', re.findall(r'<h[23][^>]*>([^<]{2,20})</h[23]>', t)), print('  [table class]', re.findall(r'<table[^>]*class="([^"]*)"', t))))
sect('项目档案 筛选', r'\项目管理\项目档案.html', filters_of)
sect('项目详情 筛选+布局', r'\项目管理\项目详情.html', lambda t: (filters_of(t), print('  [h3]', re.findall(r'<h[23][^>]*>([^<]{2,20})</h[23]>', t))))
sect('BOM 筛选', r'\基础数据\BOM.html', filters_of)
sect('盈亏报表 筛选', r'\财务协同\盈亏报表.html', filters_of)
sect('项目看板 筛选', r'\首页\项目看板.html', filters_of)

def bominfo(txt):
    m = re.search(r'renderListPage\(\{[\s\S]{0,400}?\}\);', txt)
    print('  [renderListPage]', re.sub(r'\s+', ' ', m.group(0)) if m else 'NOT FOUND')
sect('BOM维护 接线', r'\基础数据\BOM维护.html', bominfo)
sect('角色管理 接线', r'\系统管理\角色管理.html', bominfo)

dd = open(ROOT + r'\_data\demo-data.js', encoding='utf-8').read()
i = dd.find('  bomVersions: {')
print('=' * 70); print('## bomVersions 实体头')
print(dd[i:i+1200])
