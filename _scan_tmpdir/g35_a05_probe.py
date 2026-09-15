# -*- coding: utf-8 -*-
import io
t = io.open(r'P3-R01-包装租赁管理后台原型\P3-R01-A05-字段字典.md', encoding='utf-8', newline='').read()
i = t.find('G34 增补')
j = t.find('\n## ', 200)  # skip header
# print the tail (G34 登记节)
print('len:', len(t))
print('=== tail 1500 ===')
print(t[-1500:])
