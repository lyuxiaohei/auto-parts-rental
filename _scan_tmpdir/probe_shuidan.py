# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
s = io.open(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\财务协同\银行水单核销.html', encoding='utf-8', newline='').read()
print('modal id:', re.findall(r'class="modal-overlay[^"]*" id="([a-zA-Z]+)"', s))
KEYS = ['function openModal', 'function closeModal', ".radio').forEach", ".modal-overlay').forEach", 'ia-fix']
for m in re.finditer(r'<script[^>]*>(.*?)</script>', s, re.S):
    keys = [k for k in KEYS if k in m.group(1)]
    head = m.group(1)[:80].replace('\r', '').replace('\n', ' ')
    print(f'@{m.start()}-{m.end()}', keys, '|', head)
