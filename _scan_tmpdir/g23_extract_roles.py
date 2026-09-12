# -*- coding: utf-8 -*-
"""G23 材料：提取 roles/users/todoItems 概要与若干实体字段键"""
import io, sys, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
txt = open(r"P3-R01-包装租赁管理后台原型\_data\demo-data.js", encoding="utf-8").read()

def block(name):
    m = re.search(r"^\s{2}(?:/\*.*?\*/\s*)?" + name + r"\s*:\s*[\[{](.*?)^\s{2}\}", txt, re.M | re.S)
    return m.group(1) if m else ""

print("== roles 9 键 ==")
b = block("roles")
for mm in re.finditer(r'"name": "([^"]+)", "desc": "([^"]+)"', b):
    print(" -", mm.group(1), "|", mm.group(2))

print()
print("== users 结构（前 2 行） ==")
b2 = block("users")
rows = re.findall(r"'(U-\d+)': \{ 'row': \{(.*?)\} \}", b2, re.S)
print("users 行数 =", len(rows))
for k, r in rows[:2]:
    print(" ", k, "->", r[:200])

print()
print("== 各业务实体 fields 键（首行） ==")
ents = ["projects","salesOrders","salesOutbounds","leaseOrders","comboOutbounds","returnInbounds",
        "rentInOrders","rentInbounds","rentInReturns","purchaseOrders","purchaseInbounds",
        "otherInbounds","otherOutbounds","stocktakes","transfers","stockFlows",
        "payableBills","receivableBills","payments","receipts","invoices","writeoffs",
        "profitRows","partners","locations","bomList","bomVersions","dictItems","productTaxes",
        "rentTracks","assetTracks","projectDocs","boardRows","opLogs","todoItems","users"]
for name in ents:
    blk = block(name)
    m = re.search(r"\{\\\\?\"fields\\\\?\": \{(.*?)\}", blk.replace('\\"', '"'), re.S)
    # demo-data 用单引号内嵌双引号转义，直接找 "fields": {
    m2 = re.search(r'\"fields\": \{(.*?)\}', blk, re.S)
    if m2:
        keys = re.findall(r'"(\w+)":', m2.group(1))
        print(f"{name}: {keys}")
    else:
        print(f"{name}: <无 fields 结构>")
