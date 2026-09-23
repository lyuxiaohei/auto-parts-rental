# -*- coding: utf-8 -*-
"""G56 第二轮遗漏扫描：开发规则/S1 副标值域/F02 完整性/页面覆盖（只读）"""
import io, sys, re, os
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P3 = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

# 1) 开发规则过期串
dr = open(os.path.join(P3, 'P3-R01-F01-业务流程导航图-开发规则.md'), encoding='utf-8').read()
for kw in ['38 页', '2484', '2584', 'Geist', '回程三节点', 'v3.9']:
    print('开发规则[%s]:' % kw, dr.count(kw))

# 2) 其他入库/其他出库 实测类型（demo + 新建页 radio）
src = open(os.path.join(P3, '_data', 'demo-data.js'), encoding='utf-8').read()
for ent, nxt in [('otherInbounds', 'returnInbounds'), ('otherOutbounds', 'salesOutbounds')]:
    i = src.find(ent + ':'); j = src.find(nxt + ':', i)
    seg = src[i:j if j > 0 else i + 9000]
    types = Counter(re.findall(r'"type": "([^"]+)"', seg))
    print(ent, '类型值域:', dict(types))
for pg in ['仓储作业/其他入库新建.html', '仓储作业/其他出库新建.html']:
    o = open(os.path.join(P3, pg), encoding='utf-8').read()
    radios = re.findall(r'value="([^"]+)"[^>]*>', o)
    lab = re.findall(r'<label class="radio"[^>]*>\s*<input[^>]*value="([^"]+)"', o) or re.findall(r'radio[^>]*value="([^"]+)"', o)
    print(pg, 'radio 值:', lab[:8])

# 3) F01 S1 两副标现行文本
f01 = open(os.path.join(P3, 'P3-R01-F01-业务流程导航图.html'), encoding='utf-8').read()
for kw in ['期初 / 盘盈 / 手工例外', '报废/盘亏/其他', '赔偿核销', '报数调整单', '客户报数调整']:
    print('F01[%s]:' % kw, f01.count(kw))

# 4) F02 未转录项检查
f02 = open(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P1-R03\P1-R03-F02-业务流程导航图绘图信息.md', encoding='utf-8').read()
for kw in ['决策变更 · 09-04 道远拍板第一期闭环', '决策升级 · 09-04 拍板', '采购应付 → 应付账单（验收立）', '决策框']:
    print('F02 含[%s]:' % kw, kw in f02)

# 5) 未入图页面存在性（系统管理/站内信 等）
for dp, dn, fn in os.walk(P3):
    if '.git' in dp or '_data' in dp: continue
    for f in fn:
        if f.endswith('.html') and ('站内信' in f or '消息' in f):
            print('站内信类页面:', os.path.relpath(os.path.join(dp, f), P3))
# F01 是否提及站内信
print('F01 提及站内信:', f01.count('站内信'))
