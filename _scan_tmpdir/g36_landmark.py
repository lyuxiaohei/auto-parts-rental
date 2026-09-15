# -*- coding: utf-8 -*-
"""标志点深度分布：找出缺闭合标签的页及其缺失层级"""
import io, os
from collections import Counter
from html.parser import HTMLParser

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'}
MARKS = ('body', 'main-col', 'content', 'content submit-pad', 'sidebar')


class D(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.d = 0
        self.m = {}

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.d += 1
        if tag == 'div':
            cls = dict(attrs).get('class', '')
            if cls in MARKS and cls not in self.m:
                self.m[cls] = self.d

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        self.d -= 1


info = {}
for dp, dn, fns in os.walk(ROOT):
    if '.git' in dp:
        continue
    for f in fns:
        if not f.endswith('.html'):
            continue
        fp = os.path.join(dp, f)
        s = io.open(fp, encoding='utf-8', errors='ignore').read()
        c = D(); c.feed(s)
        info[os.path.relpath(fp, ROOT).replace(os.sep, '/')] = (dict(c.m), c.d)

# 众数
for key in ('body', 'main-col', 'content', 'content submit-pad'):
    vals = Counter(v[0].get(key) for v in info.values() if key in v[0])
    print('%-20s 深度分布: %s' % (key, dict(vals)))
print()
print('末尾残留深度分布:', dict(Counter(v[1] for v in info.values())))
print()
print('==== 末尾残留深度 != 0 的页 ====')
for p, (m, d) in sorted(info.items()):
    if d != 0:
        print('  %-42s 残留=%d  content深度=%s main-col=%s' % (p, d, m.get('content'), m.get('main-col')))
