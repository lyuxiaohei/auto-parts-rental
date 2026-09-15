# -*- coding: utf-8 -*-
"""B3 收尾：引用清理＋comboOutbounds exitConfirm 逐键修正＋删 17 模板"""
import sys, io, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g36_factory import rd, wr, ROOT

# 1) comboOutbounds exitConfirm 逐键修正（先前固定键误写）
s = rd('_data/demo-data.js')
a = s.index('comboOutbounds: {')
a0 = s.rfind('\n', 0, a) + 1
b = s.index('\n  },', a)
lines = s[a0:b].split('\n')
key = None; nfix = 0
BAD = "go('../租赁管理/租赁出库确认.html?id=CK-20260910-022')"
for i, ln in enumerate(lines):
    mk = re.search(r"^\s*'([A-Za-z0-9\-\.]+)': \{", ln)
    if mk and mk.group(1) != 'row':
        key = mk.group(1)
    if BAD in ln:
        assert key
        ln = ln.replace(BAD, "go('../租赁管理/租赁出库确认.html?id=%s')" % key)
        nfix += 1
    lines[i] = ln
s = s[:a0] + '\n'.join(lines) + s[b:]
print('exitConfirm 逐键修正 ×%d' % nfix)
assert nfix == 10, nfix

# 2) demo-data 注释两处
s = s.replace('现供 弹窗/器具出租履历.html 独立模板 10 行全量', '现供 租赁管理/器具出租履历.html 页面渲染（G36 B3 页面化）')
s = s.replace('履历模板=弹窗/器具出租履历.html（原租出台账共用）', '履历页=租赁管理/器具出租履历.html（G36 B3 页面化·原租出台账共用）')
assert '弹窗/器具出租履历' not in s
wr('_data/demo-data.js', s)
print('demo-data 注释 ✓')

# 3) F01 两链改指新页
s = rd('P3-R01-F01-业务流程导航图.html')
n1 = s.count('href="租赁管理/弹窗/退租入库新建.html"')
s = s.replace('href="租赁管理/弹窗/退租入库新建.html"', 'href="租赁管理/退租入库新建.html"')
s = s.replace('⟷ 退租入库列表 · 弹窗', '⟷ 退租入库列表 · 页面')
n2 = s.count('href="租入管理/弹窗/租入归还新建.html"')
s = s.replace('href="租入管理/弹窗/租入归还新建.html"', 'href="租入管理/租入归还新建.html"')
s = s.replace('弹窗 · ⟷ 租入归还列表', '页面 · ⟷ 租入归还列表')
wr('P3-R01-F01-业务流程导航图.html', s)
print('F01: %d+%d 链接改指新页' % (n1, n2))

# 4) 4 宿主注释
for hp, old, new in [
    ('租赁管理/退租入库列表.html', '<!-- 弹窗已提取到 弹窗/退租入库审核.html，构建时注入 -->', '<!-- 退租入库审核已页面化（G36 B3） -->'),
    ('租赁管理/租赁出库列表.html', '<!-- 弹窗已提取到 弹窗/租赁出库确认.html，构建时注入 -->', '<!-- 租赁出库确认已页面化（G36 B3） -->'),
    ('租赁管理/租赁单列表.html', '<!-- 弹窗已提取到 弹窗/租赁单新建.html，构建时注入 -->', '<!-- 租赁单新建已页面化（G36 B3） -->'),
    ('租赁管理/租赁单列表.html', '<!-- 弹窗已提取到 弹窗/租赁单审核.html，构建时注入 -->', '<!-- 租赁单审核已页面化（G36 B3） -->'),
]:
    t = rd(hp)
    if old in t:
        t = t.replace(old, new)
        wr(hp, t)
        print('注释 ✓', hp.split('/')[-1])

# 5) 删 17 模板（引用复核 0 后）
names = ['器具出租履历', '租赁出库单详情', '租赁出库确认', '租赁单审核', '租赁单新建', '租赁单详情', '退租入库单详情', '退租入库审核', '退租入库新建',
         '租入入库单详情', '租入入库确认', '租入单审核', '租入单新建', '租入单详情', '租入归还单详情', '租入归还审核', '租入归还新建']
total = 0
for dp, dn, fns in os.walk('.'):
    if '.git' in dp:
        continue
    for fn in fns:
        if fn.endswith(('.html', '.js', '.txt')):
            fp = os.path.join(dp, fn)
            txt = io.open(fp, encoding='utf-8', errors='ignore').read()
            for n2 in names:
                if ('弹窗/%s.html' % n2) in txt:
                    total += 1
                    print('REF:', fp.replace(os.sep, '/'), '::', n2)
print('删前引用数:', total)
assert total == 0
for n2 in names:
    for mod in ('租赁管理', '租入管理'):
        fp = os.path.join(ROOT, mod, '弹窗', n2 + '.html')
        if os.path.exists(fp):
            os.remove(fp)
print('deleted 17 templates ✓')
