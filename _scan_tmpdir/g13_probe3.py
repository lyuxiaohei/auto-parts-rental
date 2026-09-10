# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
raw = open(P + r'\_data\demo-data.js', encoding='utf-8', newline='').read()
i = raw.index('salesOrders: {'); j = raw.index('purchaseInbounds: {', i)
sec = raw[i:j]
NL = '\r\n' if '\r\n' in sec else '\n'
lines = sec.split(NL)
# 找第一条记录的 detail 结构（跳过 row 行）
shown = 0
for k, ln in enumerate(lines):
    if "'label'" in ln and shown < 8:
        print(k, ln.strip()[:90]); shown += 1
print('--- 状态锚计数:', sec.count("'label': '状态'"), '| tag 锚:', sec.count("'label': '状态',"))
print('--- 首条记录头 40 行:')
st = sec.index("'row'")
print(NL.join(lines[:40])[:2000])
# 销售订单审核 soft 结果
for f in [r'\销售管理\弹窗\销售订单审核.html', r'\销售管理\销售订单列表.html']:
    t = open(P + f, encoding='utf-8', newline='').read()
    print(f, '→ 按角色匹配:', t.count('审核人（按角色匹配）'), '| 按角色配置:', t.count('审核人（按角色配置）'))
