# -*- coding: utf-8 -*-
import io, re
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
t = io.open(ROOT + r'\租赁管理\租赁出库列表.html', encoding='utf-8', newline='').read()
lines = t.split('\r\n' if '\r\n' in t else '\n')
for i, l in enumerate(lines):
    if 'printed' in l:
        ck = None
        for j in range(i, max(0, i - 20) - 1, -1):
            m = re.search(r'CK-[0-9-]+', lines[j])
            if m:
                ck = m.group(0)
                break
        print('line', i + 1, 'ck=', ck)
print('static CK order:', [m.group(1) for m in re.finditer(r'<span class="lk">(CK-[0-9-]+)</span>', t)])
