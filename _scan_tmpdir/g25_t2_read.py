# -*- coding: utf-8 -*-
"""读 rentInOrders 行摘要与 RZRK 单号上下文（只读）"""
import io, re

t = io.open(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\_data\demo-data.js", encoding="utf-8").read()
i = t.find('rentInOrders')
print('rentInOrders @', i)
for m in list(re.finditer(r"'row': \{\"fields\":[^\n]+", t[i:i + 30000]))[:8]:
    print(m.group(0)[:400])
    print()
j = t.find('RZRK-20260903-023')
print('RZRK-20260903-023 上下文:', t[max(0, j - 260):j + 120].replace("\n", " "))
