# -*- coding: utf-8 -*-
"""G36 B2-B5 全量勘察：各模块弹窗清单/宿主页 openModal/demo-data ops/实体↔宿主映射"""
import io, os, re, time, json
from collections import Counter

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
MODS = ['采购管理', '销售管理', '租赁管理', '租入管理', '仓储作业', '财务协同', '系统管理']

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='', errors='ignore').read()

now = time.time()
print('==== 模块 mtime（单写者校验）====')
for m in MODS:
    p = os.path.join(ROOT, m)
    newest = 0
    for dp, dn, fns in os.walk(p):
        for f in fns:
            newest = max(newest, os.path.getmtime(os.path.join(dp, f)))
    print('%s: newest %.0f min ago %s' % (m, (now - newest) / 60, 'OK' if (now - newest) / 60 >= 30 else '*** RECENT ***'))

print()
print('==== 各模块弹窗模板 ====')
for m in MODS:
    d = os.path.join(ROOT, m, '弹窗')
    if not os.path.isdir(d):
        print(m, ': 无弹窗目录')
        continue
    for f in sorted(os.listdir(d)):
        s = rd(os.path.join(m, '弹窗', f))
        ids = re.findall(r'<div class="modal-overlay" id="([^"]+)"', s)
        pins = '有标注pin' if 'proto-pin' in s else ''
        title = re.search(r'modal-title[^>]*>([^<]*)', s)
        print('%s/弹窗/%s | ids=%s | %s %s | %dB' % (m, f, ids, title.group(1).strip() if title else '?', pins, len(s)))

print()
print('==== 宿主页 openModal 分布（模块内业务页）====')
for m in MODS:
    d = os.path.join(ROOT, m)
    for f in sorted(os.listdir(d)):
        if not f.endswith('.html'):
            continue
        s = rd(os.path.join(m, f))
        ovs = re.findall(r'<div class="modal-overlay" id="([^"]+)"', s)
        acts = Counter(re.findall(r"openModal\('([a-zA-Z]+Modal)'\)", s))
        if ovs or acts:
            print('%s/%s | overlays=%s | openModal 调用=%s' % (m, f, ovs, dict(acts)))

print()
print('==== demo-data 各实体 ops 形态 ====')
s = rd('_data/demo-data.js')
ents = ['purchaseOrders', 'purchaseInbounds', 'purchaseReturns', 'salesOrders', 'salesOutbounds', 'salesReturns',
        'leaseOrders', 'comboOutbounds', 'returnInbounds', 'rentInOrders', 'rentInbounds', 'rentInReturns',
        'otherInbounds', 'otherOutbounds', 'stocktakes', 'transfers', 'stockFlows',
        'payableBills', 'receivableBills', 'payments', 'receipts', 'invoices', 'writeoffs', 'refunds',
        'roles', 'users', 'dictItems', 'todoItems']
def span(ent):
    a = s.index(ent + ': {')
    a = s.rfind('\n', 0, a) + 1
    b = s.index('\n  },', a)
    return a, b
for ent in ents:
    try:
        a, b = span(ent)
    except ValueError:
        print(ent, ': NOT FOUND')
        continue
    blk = s[a:b]
    acts = Counter(re.findall(r'"act": "([^"]+)"', blk))
    dets = blk.count('"detail": true')
    print('%-18s rows~%d detail:%d acts=%s' % (ent, len(re.findall(r"^\s*'[A-Za-z0-9\-\.]+': \{", blk, re.M)), dets, dict(acts)))

print()
print('==== 我的待办 审核跳转口径 ====')
t = rd('我的待办.html')
print('audit=1 refs:', len(re.findall(r'audit=1', t)), '| go 列表跳转样例:', re.findall(r"go\('([^']*(?:列表|登记|账单)[^']*)'\)", t)[:6])
dd = s
i = dd.index('todoItems: {')
a = dd.rfind('\n', 0, i) + 1
b = dd.index('\n  },', a)
blk = dd[a:b]
print('todoItems 链接样例:', re.findall(r'"url": "([^"]+)"', blk)[:4], '| audit 参数:', len(re.findall(r'audit=1', blk)))
print()
print('==== 全站 ?audit=1 auto-open 机制 ====')
cnt = 0
for m in MODS + ['']:
    d = os.path.join(ROOT, m)
    for f in os.listdir(d):
        if f.endswith('.html'):
            x = rd(os.path.join(m, f)) if m else rd(f)
            if 'audit=1' in x:
                cnt += 1
                print('  ', (m + '/' if m else '') + f)
print('共', cnt, '页含 audit=1')
