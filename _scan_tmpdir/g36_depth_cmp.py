# -*- coding: utf-8 -*-
"""标志点 div 深度对比，定位多余闭合起点"""
import io
from html.parser import HTMLParser

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'}
MARKS = ('body', 'main-col', 'content submit-pad', 'card', 'submit-bar', 'card-head')


class Depth(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.d = 0
        self.marks = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.d += 1
        cls = dict(attrs).get('class', '')
        if tag == 'div' and cls in MARKS:
            self.marks.append((cls, self.d, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        self.d -= 1


for name in ('应付新建.html', '付款新建.html', '退款新建.html'):
    p = ROOT + '\\财务协同\\' + name
    s = io.open(p, encoding='utf-8', newline='').read()
    c = Depth()
    c.feed(s)
    print('===', name, '| 末深度 =', c.d)
    for cls, d, ln in c.marks:
        print('    %-20s depth=%d  line=%d' % (cls, d, ln))
