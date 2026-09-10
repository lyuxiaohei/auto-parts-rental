# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
raw = open(P + r'\_data\demo-data.js', encoding='utf-8', newline='').read()
i = raw.index('assetTracks: {')
seg = raw[i:i+900]
print('==== assetTracks 头 900 字符 ===='); print(seg[:900])
v = open(P + r'\租赁管理\租入单列表.html', encoding='utf-8', newline='').read()
m = re.search(r'renderListPage\(\{[\s\S]{0,600}?\}\);', v)
print('==== 租入单列表 cfg ===='); print(m.group(0) if m else 'NONE')
d = open(P + r'\销售管理\弹窗\销售订单详情.html', encoding='utf-8', newline='').read()
print('==== 销售订单详情：detailBody?', 'detailBody' in d, '| form-row 数:', d.count('form-row'), '| dgrid:', d.count('dgrid'), '| len:', len(d))
k = d.index('<body')
print(d[k:k+1500])
