# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
src = open(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\_data\demo-data.js', encoding='utf-8').read()
for grp in ['RKU', 'CKU']:
    pat = re.compile("'" + grp + r"[^']*': \{ 'row': \{.*?\"name\": \"([^\"]+)\"", re.S)
    vals = [m.group(1) for m in pat.finditer(src)]
    print(grp, vals)
# QTRK-004 的 type 值
i = src.find('QTRK-20260912-004')
print('QTRK-004 段:', re.sub(r'\s+', ' ', src[i:i+300])[:260])
