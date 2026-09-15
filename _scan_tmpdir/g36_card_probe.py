# -*- coding: utf-8 -*-
"""提取待改页的卡内分段标题原始标记与上下文"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
PAGES = {
    '采购管理/采购退货新建.html': ['退货明细'],
    '销售管理/销售订单新建.html': ['订单明细', '订单附件'],
    '销售管理/销售出库新建.html': ['出库明细'],
    '销售管理/销售退货新建.html': ['退货明细'],
    '租赁管理/租赁单新建.html': ['租赁器具明细'],
    '租入管理/租入单新建.html': ['租入明细'],
    '财务协同/付款新建.html': ['分期付款计划'],
    '财务协同/应付新建.html': ['分期付款计划'],
    '财务协同/应收生成.html': ['分期收款计划'],
    '仓储作业/盘点录入.html': ['盈亏处理'],
    '基础数据/BOM维护.html': ['版本记录'],
}

for p, keys in PAGES.items():
    fp = os.path.join(ROOT, p.replace('/', os.sep))
    if not os.path.exists(fp):
        print('== MISSING', p); continue
    s = io.open(fp, encoding='utf-8', newline='').read()
    print('=' * 76)
    print(p)
    # 卡片边界
    for m in re.finditer(r'<div class="card">|<div class="card-head">|<h3 class="card-title"[^>]*>([^<]*)</h3>', s):
        ln = s[:m.start()].count('\n') + 1
        print('   L%-5d %s' % (ln, re.sub(r'\s+', ' ', m.group(0))[:80]))
    for k in keys:
        for m in re.finditer(re.escape(k), s):
            a = s.rfind('\n', 0, m.start()) + 1
            b = s.find('\n', m.end())
            ln = s[:m.start()].count('\n') + 1
            line = s[a:b].replace('\r', '')
            if '<div' in line and 'card-title' not in line:
                print('   >>> L%-5d %s' % (ln, repr(line.strip())[:150]))
                break
