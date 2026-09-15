# -*- coding: utf-8 -*-
import io, re, os
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
for p in ['仓储作业/盘点录入.html', '租赁管理/租赁出库录单.html', '基础数据/BOM维护.html']:
    fp = os.path.join(ROOT, p.replace('/', os.sep))
    s = io.open(fp, encoding='utf-8', newline='').read()
    m = re.search(r'<div class="submit-bar">.*?</div>\s*\r?\n', s, re.S)
    fab = ('f01-fab' in s) or ('pn-fab' in s)
    just = re.search(r'\.submit-bar \{[^}]*justify-content:(\w+)', s)
    print('== %-26s justify=%-9s fab=%s' % (p.split('/')[-1], just.group(1) if just else '?', fab))
    print('   按钮:', re.findall(r'<button[^>]*>([^<]+)</button>', m.group(0)) if m else '无 submit-bar')
    # 提交条在内容区内还是外
    if m:
        pos = m.start()
        cpos = s.find('class="content')
        print('   提交条位置: 内容区之后=%s' % (cpos > 0 and pos > cpos))
