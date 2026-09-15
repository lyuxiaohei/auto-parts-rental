# -*- coding: utf-8 -*-
import io
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
txt = io.open(ROOT + r'\_data\demo-data.js', encoding='utf-8').read()
i = txt.find('  opLogs: {')
print('=== opLogs head 900 ===')
print(txt[i:i+900])
print()
i2 = txt.find('  purchaseInbounds: {')
print('=== purchaseInbounds head 1100 ===')
print(txt[i2:i2+1100])
