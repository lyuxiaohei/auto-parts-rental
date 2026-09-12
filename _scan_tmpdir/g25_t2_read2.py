# -*- coding: utf-8 -*-
"""定位 rentInOrders 实体段+路凯行摘要；RZRK-20260816 单据归属（只读）"""
import io, re

t = io.open(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\_data\demo-data.js", encoding="utf-8").read()
m = re.search(r"^  rentInOrders: \{", t, re.M)
print("rentInOrders 实体 @", m.start() if m else None)
if m:
    seg = t[m.start():t.find("\n  /* ----", m.start())]
    print("段长:", len(seg))
    for km in re.finditer(r"^    '([^']+)': \{", seg, re.M):
        key = km.group(1)
        rs = seg.find("'row'", km.start())
        print("KEY", key, "→", seg[rs:seg.find("\n", rs)][:360] if rs > 0 else "(无 row)")
    print()
    print("段头 300:", seg[:300])
j = t.find("RZRK-20260816-021")
print("\nRZRK-20260816-021 上下文:", t[max(0, j - 300):j + 150].replace("\n", " "))
