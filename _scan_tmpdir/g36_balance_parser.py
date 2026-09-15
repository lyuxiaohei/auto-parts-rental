# -*- coding: utf-8 -*-
"""HTML 解析器权威复核：全站（+与 G36 前备份对照）"""
import io, os
from html.parser import HTMLParser

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.problems = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.problems.append(('未闭合', [t for t, _ in self.stack[i + 1:]], self.getpos()[0]))
                del self.stack[i:]
                return
        self.problems.append(('多余闭合', tag, self.getpos()[0]))


def check(path):
    s = io.open(path, encoding='utf-8', errors='ignore').read()
    c = Checker()
    c.feed(s)
    return c.problems, c.stack


rows = []
for dp, dn, fns in os.walk(ROOT):
    if '.git' in dp:
        continue
    for f in sorted(fns):
        if not f.endswith('.html'):
            continue
        fp = os.path.join(dp, f)
        pr, st = check(fp)
        if pr or st:
            rows.append((os.path.relpath(fp, ROOT).replace(os.sep, '/'),
                         [p[0] + ':' + (p[1] if isinstance(p[1], str) else ','.join(p[1])) + '@L' + str(p[2]) for p in pr][:3],
                         ['%s@L%d' % (t, l) for t, l in st][:3]))
print('解析器复核：全站问题页 %d' % len(rows))
for r, pr, st in rows:
    print('  %-42s 问题=%s 未闭合栈=%s' % (r, pr, st))
