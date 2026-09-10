# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
raw = open(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\_data\demo-data.js', encoding='utf-8', newline='').read()
i = raw.index('  leaseOrders: {'); j = raw.index('  rentInOrders: {')
sec = raw[i:j]
NL = '\r\n' if '\r\n' in sec else '\n'
lines = sec.split(NL)
for idx, ln in enumerate(lines):
    m = re.search(r"'(ZL-[\d-]+)': \{", ln)
    if m and lines[idx+1].lstrip().startswith("'row':"):
        rowline = lines[idx+1]
        mm = re.search(r'"ops": \[.*?\]', rowline)
        print(m.group(1), '=>', (mm.group(0)[:200] if mm else 'NO-OPS: ' + rowline[-200:]))
