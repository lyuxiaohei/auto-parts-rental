# -*- coding: utf-8 -*-
"""标签配平修复：按 HTML 解析器结果补齐未闭合 div / 删除无主 </div>（渲染零变化口径）"""
import io, os, re
from html.parser import HTMLParser

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'}


class T(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.strays = []
        self.lost = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        d = dict(attrs)
        self.stack.append((tag, d.get('class', ''), self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.lost.append(([t for t, _, _ in self.stack[i + 1:]], self.getpos()[0]))
                del self.stack[i:]
                return
        self.strays.append((tag, self.getpos()[0]))


def analyze(path):
    c = T()
    c.feed(io.open(path, encoding='utf-8', errors='ignore').read())
    return c


def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)


PAGES = []
for dp, dn, fns in os.walk(ROOT):
    if '.git' in dp:
        continue
    for f in sorted(fns):
        if f.endswith('.html'):
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, '/')
            c = analyze(os.path.join(dp, f))
            if len(c.stack) or c.strays or c.lost:
                PAGES.append((rel, c))

print('待修页 %d' % len(PAGES))
for rel, c in PAGES:
    s = rd(rel)
    log = []
    # 1) 删无主 </div>（按行号，行内只含该闭合）
    for tag, ln in reversed(c.strays):
        lines = s.split('\n')
        raw = lines[ln - 1]
        if raw.replace('\r', '').strip() == '</%s>' % tag:
            lines[ln - 1] = None
            s = '\n'.join(l for l in lines if l is not None)
            log.append('删无主 </%s> L%d' % (tag, ln))
        else:
            log.append('!! 无主 </%s> L%d 行内非单一标签·跳过' % (tag, ln))
    # 2) 补未闭合（插在 </body> 前，与浏览器隐式闭合等价）
    #    未闭合元素体现为匹配 </body> 时被丢弃的下层元素（c.lost）
    n = sum(len(dropped) for dropped, _ in c.lost) + len(c.stack)
    if n:
        assert s.count('\r\n</body>') == 1 or s.count('\n</body>') == 1, rel + ' </body> 锚点异常'
        ins = ('\r\n' if '\r\n' in s else '\n').join(['</div>'] * n)
        if '\r\n' in s:
            s = s.replace('\r\n</body>', '\r\n' + ins + '\r\n</body>')
        else:
            s = s.replace('\n</body>', '\n' + ins + '\n</body>')
        log.append('补齐未闭合 ×%d' % n)
    # 3) 同时存在 lost（下层元素被误闭）时提示
    if c.lost:
        log.append('!! 存在被误闭元素 %s' % c.lost[:2])
    wr(rel, s)
    print('  %-42s %s' % (rel, ' | '.join(log)))
