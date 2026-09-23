# -*- coding: utf-8 -*-
"""G56 追加审计：F01 其余流程 vs demo-data 实据（只读取证）"""
import io, sys, re, os
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P3 = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
src = open(os.path.join(P3, '_data', 'demo-data.js'), encoding='utf-8').read()

# 1) 待办类型数
i, j = src.find('todoItems:'), src.find('opLogs:')
seg = src[i:j]
types = re.findall(r'"type":\s*"([^"]+)"', seg)
c = Counter(types)
print('== 1) todoItems 类型 %d 种 ==' % len(c))
for k, v in c.items(): print('   ', k, 'x%d' % v)

# 2) DJ 字典
dj = re.findall(r"'(DJ-\d+)': \{ 'row': \{[^\}]*?\"name\": \"([^\"]+)\"", src)
print('== 2) DJ 字典 %d 条 ==' % len(dj), [n for _, n in dj][:25])

# 3) WL 字典（物料类型现行值）
wl = re.findall(r"'(WL-\d+)': \{ 'row': \{[^\}]*?\"name\": \"([^\"]+)\"", src)
print('== 3) WL 字典 ==', wl)

# 4) 资产来源残留
i2, j2 = src.find('products:'), src.find('productTaxes:')
pseg = src[i2:j2]
print('== 4) products 段：资产来源 %d · 归属 %d · src字段 %d ==' % (pseg.count('资产来源'), pseg.count('归属'), len(re.findall(r'"src":', pseg))))
kccx = open(os.path.join(P3, '仓储作业', '库存查询.html'), encoding='utf-8').read()
print('   库存查询页 资产来源出现 %d 次' % kccx.count('资产来源'))

# 5) D-158 租赁出库录单主关联
o = open(os.path.join(P3, '租赁管理', '租赁出库录单.html'), encoding='utf-8').read()
print('== 5) 租赁出库录单：关联租赁单 %d · 关联销售订单 %d ==' % (o.count('关联租赁单'), o.count('关联销售订单')))

# 6) L2 顺序实据：组合租赁的 租赁单 与 出库 谁先（leaseOrders 组合行的 chain/timeline）
i3, j3 = src.find('leaseOrders:'), src.find('salesOrders:')
lseg = src[i3:j3]
for m in re.finditer(r"'(ZD-[^']+)': \{ 'row': \{.*?'chain': (\[.*?\])", lseg):
    chain_roles = re.findall(r"'role': '([^']+)'", m.group(2))
    print('== 6)', m.group(1), 'chain:', ' → '.join(chain_roles))

# 7) L4 同型（对照）
for m in re.finditer(r"'(ZH-[^']+)': \{ 'row': \{.*?'chain': (\[.*?\])", lseg):
    chain_roles = re.findall(r"'role': '([^']+)'", m.group(2))
    print('   ', m.group(1), 'chain:', ' → '.join(chain_roles))

# 8) 器具 在 F01 出现位置（除 SRC_DATA 段）
f01 = open(os.path.join(P3, 'P3-R01-F01-业务流程导航图.html'), encoding='utf-8').read()
i4 = f01.index('var SRC_DATA')
pre_sd = f01[:i4]
print('== 8) F01 SRC_DATA 前「器具」出现 %d 处 ==' % pre_sd.count('器具'))
for m in re.finditer(r'器具', pre_sd):
    print('   ...', re.sub(r'\s+', ' ', pre_sd[max(0,m.start()-60):m.start()+40])[-90:])

# 9) 15 类 在 F01（除 SRC_DATA）
print('== 9) F01 SRC_DATA 前「15 类」出现 %d 处 ==' % pre_sd.count('15 类'))

# 10) 组合出库 comboOutbounds 首键 chain（谁关联租赁单）
i5, j5 = src.find('comboOutbounds:'), src.find('salesOutbounds:')
cseg = src[i5:j5]
for m in re.finditer(r"'(CK-[^']+)': \{ 'row': \{.*?'chain': (\[.*?\])", cseg):
    roles = re.findall(r"'role': '([^']+)'", m.group(2))
    print('== 10)', m.group(1), 'chain:', ' → '.join(roles))
