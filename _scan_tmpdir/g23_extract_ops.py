# -*- coding: utf-8 -*-
"""G23 材料：各实体 ops 按钮面 + 页面 stabs/筛选概要（UC 动作真值源）"""
import io, sys, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
txt = open(r"P3-R01-包装租赁管理后台原型\_data\demo-data.js", encoding="utf-8").read()

def block(name):
    m = re.search(r"^\s{2}(?:/\*.*?\*/\s*)?" + name + r"\s*:\s*[\[{](.*?)^\s{2}\}", txt, re.M | re.S)
    return m.group(1) if m else ""

ents = ["projects","salesOrders","salesOutbounds","leaseOrders","comboOutbounds","returnInbounds",
        "rentInOrders","rentInbounds","rentInReturns","purchaseOrders","purchaseInbounds",
        "otherInbounds","otherOutbounds","stocktakes","transfers","stockFlows",
        "payableBills","receivableBills","payments","receipts","invoices","writeoffs",
        "profitRows","partners","locations","bomList","bomVersions","dictItems",
        "rentTracks","assetTracks","opLogs","todoItems","productTaxes"]

for name in ents:
    blk = block(name)
    if not blk:
        print(f"{name}: <块未找到>")
        continue
    ops_sets = {}
    for mm in re.finditer(r'"t": "([^"]+)"', blk):
        ops_sets[mm.group(1)] = ops_sets.get(mm.group(1), 0) + 1
    print(f"{name}: ops={dict(ops_sets)}")

print()
print("== 各列表页 stabs（从 demo-data stab/stabs 键） ==")
for mm in re.finditer(r'"stabs": \[([^\]]*)\]', txt):
    vals = re.findall(r'"([^"]+)"', mm.group(1))
    # 找出宿主实体：向前找最近的实体名
    pre = txt[:mm.start()]
    m2 = re.findall(r"^\s{2}(\w+): \{", pre, re.M)
    host = m2[-1] if m2 else "?"
    print(f" - {host}: {vals}")
