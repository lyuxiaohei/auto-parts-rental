# -*- coding: utf-8 -*-
"""查 rentInOrders 各键 returnItems 行数（只读）"""
import io, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
t = io.open(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\_data\demo-data.js",
            encoding="utf-8", newline="").read()
i = t.find("rentInOrders")
print("rentInOrders @", i)
seg = t[i:i + 20000]
for m in re.finditer(r"'(RZD-[^']+)': \{", seg):
    key = m.group(1)
    nxt = seg.find("'RZD-", m.start() + 10)
    sub = seg[m.start():nxt if nxt > 0 else m.start() + 4000]
    ri = sub.find("returnItems")
    if ri < 0:
        print(key, "| 无 returnItems")
        continue
    sub_ri = sub[ri:]
    n = sub_ri.count("item:")
    items = re.findall(r"item: '([^']{0,34})", sub_ri)
    print(key, "| returnItems", n, "行:", items)
