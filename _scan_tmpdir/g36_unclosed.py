# -*- coding: utf-8 -*-
"""打印不平衡页在 </body> 处仍未闭合的元素（含开标签行号/class）"""
import io, os
from html.parser import HTMLParser

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'}
PAGES = ['我的待办.html', '仓储作业/其他入库列表.html', '仓储作业/其他出库列表.html', '仓储作业/库存调拨列表.html',
         '租入管理/租入入库列表.html', '租入管理/租入单列表.html', '租入管理/租入归还列表.html',
         '租赁管理/租赁单列表.html', '租赁管理/退租入库列表.html', '财务协同/应付账单.html',
         '财务协同/退款登记.html', '财务协同/银行水单核销.html', '采购管理/采购入库录单.html',
         '采购管理/采购订单列表.html', '销售管理/销售出库列表.html', '销售管理/销售订单列表.html',
         '销售管理/销售退货单列表.html', '项目管理/项目详情.html']


class T(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.events = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        d = dict(attrs)
        self.stack.append((tag, d.get('class', ''), d.get('id', ''), self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                lost = self.stack[i + 1:]
                self.events.append(('多余的 </%s>' % tag, 'L%d' % self.getpos()[0],
                                    ['%s.%s@L%d' % (t, c or i2 or '-', l) for t, c, i2, l in lost]))
                del self.stack[i:]
                return
        self.events.append(('无主的 </%s>' % tag, 'L%d' % self.getpos()[0], []))


for p in PAGES:
    fp = os.path.join(ROOT, p)
    s = io.open(fp, encoding='utf-8', errors='ignore').read()
    c = T(); c.feed(s)
    print('=' * 74)
    print(p, '| 末尾残留 %d' % len(c.stack))
    if c.stack:
        for t, cl, idv, ln in c.stack:
            print('   未闭合 <%s class="%s" id="%s"> 开于 L%d' % (t, cl, idv, ln))
    for e in c.events[:3]:
        print('   事件:', e[0], e[1], e[2])
