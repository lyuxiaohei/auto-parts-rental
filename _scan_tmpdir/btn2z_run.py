# -*- coding: utf-8 -*-
"""#7 按钮两字化：上传附件→上传（4 页按钮＋demo-data ops）＋全站 ops 字长聚类报告。"""
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
BK = ROOT / 'backup-btn2z-20260919'

for f in ['采购管理/采购订单列表.html', '采购管理/采购订单新建.html',
          '销售管理/销售订单列表.html', '销售管理/销售订单新建.html']:
    p = PROTO / f
    b = p.read_bytes()
    c = b.count('上传附件'.encode('utf-8'))
    d = BK / f
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, d)
    p.write_bytes(b.replace('>上传附件<'.encode('utf-8'), '>上传<'.encode('utf-8')))
    print(f, c, '处')

p = PROTO / '_data/demo-data.js'
b = p.read_bytes()
d = BK / '_data/demo-data.js'
d.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(p, d)
c = b.count('"t": "上传附件"'.encode('utf-8'))
p.write_bytes(b.replace('"t": "上传附件"'.encode('utf-8'), '"t": "上传"'.encode('utf-8')))
print('demo-data ops', c, '处')
subprocess.run(['node', '--check', str(p)], check=True)
print('node --check 0')

t = p.read_text(encoding='utf-8')
ops = re.findall(r'"t": "([^"]+)"', t)
c = Counter(ops)
print()
print('demo-data ops >2 字候选（两字化后续批）:')
for k, v in sorted(c.items(), key=lambda x: -x[1]):
    if len(k) > 2:
        print('  %4d  %s（%d字）' % (v, k, len(k)))
print('两字及以内: %d 处 / 总 %d 处' % (sum(v for k, v in c.items() if len(k) <= 2), sum(c.values())))
