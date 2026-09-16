# -*- coding: utf-8 -*-
"""G38 T4/T5：HTML 页面字段名口径收敛（精确替换＋计数断言）"""
import io, sys

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

# (相对路径, [(旧, 新, 期望次数)])
PLAN = [
    # —— 裸「金额(元)／单价(元)」清零（th 精确替换） ——
    (r'\采购管理\采购退货单列表.html', [('<th>金额(元)</th>', '<th>含税金额(元)</th>', 1)]),
    (r'\采购管理\采购退货新建.html', [('<th>单价(元)</th>', '<th>未税单价(元)</th>', 1), ('<th>金额(元)</th>', '<th>含税金额(元)</th>', 1)]),
    (r'\销售管理\销售退货单列表.html', [('<th>金额(元)</th>', '<th>含税金额(元)</th>', 1)]),
    (r'\销售管理\销售退货新建.html', [('<th>单价(元)</th>', '<th>未税单价(元)</th>', 1), ('<th>金额(元)</th>', '<th>含税金额(元)</th>', 1)]),
    (r'\采购管理\采购订单列表.html', [('<th>金额(元)</th>', '<th>含税金额(元)</th>', 1)]),
    (r'\销售管理\销售订单列表.html', [('<th>金额(元)</th>', '<th>含税金额(元)</th>', 1)]),
    # —— 分期表裸金额 → 分期金额(元) ——
    (r'\财务协同\付款新建.html', [('<th>金额(元)</th>', '<th>分期金额(元)</th>', 1)]),
    (r'\财务协同\应付新建.html', [('<th>金额(元)</th>', '<th>分期金额(元)</th>', 1)]),
    (r'\财务协同\应付账单.html', [('<th>金额(元)</th>', '<th>分期金额(元)</th>', 1)]),
    (r'\财务协同\应收生成.html', [('<th>金额(元)</th>', '<th>分期金额(元)</th>', 1)]),
    # —— 物料列（货品→物料） ——
    (r'\租入管理\租入归还新建.html', [('<th>货品</th>', '<th>物料</th>', 1)]),
    (r'\租赁管理\租赁单列表.html', [('<th>货品</th>', '<th>物料</th>', 1)]),
    (r'\租入管理\租入单新建.html', [('多货品 · 计费方式', '多物料 · 计费方式', 1)]),
    # —— 时间粒度（值纯日期→「日期」） ——
    (r'\基础数据\BOM.html', [('更新时间', '更新日期', 3)]),
    (r'\基础数据\产品档案.html', [('建档时间', '建档日期', 2), ('更新时间', '更新日期', 1)]),
    (r'\基础数据\客商管理.html', [('创建时间', '创建日期', 2), ('更新时间', '更新日期', 1)]),
    (r'\项目管理\项目档案.html', [('立项时间', '立项日期', 2)]),
    (r'\租入管理\租入归还列表.html', [('归还时间', '归还日期', 3)]),
]

fail = []
for rel, rules in PLAN:
    p = BASE + rel
    t = io.open(p, encoding='utf-8', newline='').read()
    ok = True
    for old, new, exp in rules:
        n = t.count(old)
        if n != exp:
            print('[MISS] %s 「%s」出现 %d 次（期望 %d）——跳过该文件' % (rel, old, n, exp))
            ok = False
            fail.append((rel, old, n, exp))
            break
    if not ok:
        continue
    for old, new, exp in rules:
        t = t.replace(old, new)
    io.open(p, 'w', encoding='utf-8', newline='').write(t)
    print('[OK] %s（%d 条规则）' % (rel, len(rules)))

print('FAILURES:', len(fail))
sys.exit(0)
