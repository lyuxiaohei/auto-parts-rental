# -*- coding: utf-8 -*-
"""G34 勘察：dictItems 结构 / 组数 / 项数 / productTaxes 税率值 / KW-ZQ 组"""
import io, re, json, sys

P = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\_data\demo-data.js'
with io.open(P, encoding='utf-8') as f:
    t = f.read()

# dictItems 段提取：花括号配对（含字符串跳过）
m = re.search(r'dictItems\s*:\s*\{', t)
i = t.index('{', m.start())
depth = 0; k = i; in_str = False; q = None
while k < len(t):
    c = t[k]
    if in_str:
        if c == '\\':
            k += 2; continue
        if c == q:
            in_str = False
    else:
        if c in ('"', "'"):
            in_str = True; q = c
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                break
    k += 1
seg = t[i:k+1]

# 每项形如 'WL-01': {...'cat': '物料类型'...}
items = re.findall(r"'([A-Z]+-\d+)':\s*\{", seg)
cats = re.findall(r"'([A-Z]+-\d+)':\s*\{.*?'cat':\s*'([^']+)'", seg)
print('dictItems 总项数:', len(items), '带cat匹配:', len(cats))
groups = {}
for code, cat in cats:
    groups.setdefault(cat, []).append(code)
print('组数:', len(groups))
for cat, codes in sorted(groups.items()):
    print('  %-14s %d 项: %s' % (cat, len(codes), ','.join(sorted(codes))))

# 看 WL 组一项完整样例（了解字段结构）
mm = re.search(r"'WL-01':\s*\{[^{}]*\}", seg)
print('\nWL-01 样例:', mm.group(0) if mm else 'N/A')

# productTaxes 税率值域
mt = re.search(r'productTaxes\s*:\s*\{', t)
j = t.index('{', mt.start())
depth = 0; k = j; in_str = False; q = None
while k < len(t):
    c = t[k]
    if in_str:
        if c == '\\':
            k += 2; continue
        if c == q:
            in_str = False
    else:
        if c in ('"', "'"):
            in_str = True; q = c
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                break
    k += 1
tseg = t[j:k+1]
rates = re.findall(r"'taxRate':\s*'([^']+)'", tseg)
cycles = re.findall(r"'settleCycle':\s*'([^']+)'", tseg)
print('\nproductTaxes 条数:', len(re.findall(r"'TAX-\d+'", tseg)))
print('taxRate 值:', rates)
print('settleCycle 值:', cycles)

# KW / ZQ 组现值
for g in ('KW', 'ZQ', 'DJ'):
    vals = re.findall(r"'" + g + r"-\d+':\s*\{.*?'val':\s*'([^']+)'", seg)
    print(g, '组值:', vals)
