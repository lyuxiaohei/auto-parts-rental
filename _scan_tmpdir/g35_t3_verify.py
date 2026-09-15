# -*- coding: utf-8 -*-
"""G35 T3 收尾自检：终态核验 + div 配平 + label 落位"""
import io, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
PAGES = ['财务协同/应付账单', '仓储作业/库存查询', '基础数据/BOM', '租入管理/租入入库列表', '租入管理/租入归还列表',
         '租赁管理/退租入库列表', '采购管理/采购入库列表', '销售管理/销售出库列表', '销售管理/销售订单列表',
         '系统管理/操作日志', '系统管理/用户权限', '我的待办',
         '租赁管理/租赁单列表', '财务协同/付款登记', '基础数据/客商管理', '项目管理/项目档案']
print('%-24s %-6s %-6s %-6s %s' % ('page', 'fill', 'g35id', 'div配平', '备注'))
allok = True
for p in PAGES:
    t = io.open(ROOT + '/' + p + '.html', encoding='utf-8', newline='').read()
    fills = t.count('G35 筛选值域动态渲染')
    ids = t.count('id="g35')
    opens = len(re.findall(r'<div\b', t))
    closes = len(re.findall(r'</div>', t))
    bal = 'OK' if opens == closes else 'BAD(%d/%d)' % (opens, closes)
    if opens != closes or fills > 1:
        allok = False
    print('%-24s %-6d %-6d %-6s' % (p.split('/')[-1], fills, ids, bal))
print('div 配平全部 OK:', allok)
# label 落位（Batch A 8 处）
checks = [
    ('租赁管理/租赁单列表.html', "{ label: '客户名称', field: 'customer' }"),
    ('租赁管理/退租入库列表.html', "{ label: '客户名称', field: 'customer' }"),
    ('财务协同/付款登记.html', "{ label: '供应商名称', field: 'supplier' }"),
    ('财务协同/应付账单.html', "{ label: '供应商名称', field: 'supplier' }"),
    ('销售管理/销售出库列表.html', "{ label: '客户名称', field: 'customer' }"),
    ('销售管理/销售订单列表.html', "{ label: '客户名称', field: 'customer' }"),
    ('基础数据/客商管理.html', "{ label: '客商名称', field: 'name' }"),
    ('项目管理/项目档案.html', "{ label: '客户名称', field: 'customer' }"),
]
for p, s in checks:
    t = io.open(ROOT + '/' + p, encoding='utf-8', newline='').read()
    ok = s in t
    allok = allok and ok
    print('label', 'OK ' if ok else 'MISS', p)
# cfg ↔ HTML label 对齐核验（读 filters cfg labels vs .ff labels，对所有 renderListPage 页）
print('--- cfg/HTML label 对齐（33 页内 renderListPage 页） ---')
import json
raw = json.load(io.open(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g35_t1_raw.json', encoding='utf-8'))
mis = 0
for name, e in raw.items():
    if not e['cfg']:
        continue
    t = io.open(ROOT + '/' + e['path'], encoding='utf-8', newline='').read()
    m = re.search(r'renderListPage\(\{[\s\S]*?\}\);', t)
    cfg_labels = re.findall(r"label:\s*'([^']+)'", m.group(0))
    i = t.find('<div class="filter-card')
    if i < 0:
        continue
    d = 0; j = i
    for mm in re.finditer(r'<div\b|</div>', t[i:]):
        d += 1 if mm.group(0).startswith('<div') else -1
        if d == 0:
            j = i + mm.end(); break
    html_labels = [re.sub(r'[:：]\s*$', '', x) for x in re.findall(r'<span class="ff-label"[^>]*>(.*?)</span>', t[i:j], re.S)]
    html_labels = [re.sub(r'<[^>]+>', '', x).strip() for x in html_labels]
    missing = [c for c in cfg_labels if c not in html_labels]
    if missing:
        mis += 1
        print('  MISMATCH', name, 'cfg 有而 HTML 无:', missing)
print('cfg/HTML label 不齐页数:', mis)
print('ALL OK' if allok and mis == 0 else 'HAS ISSUES')
