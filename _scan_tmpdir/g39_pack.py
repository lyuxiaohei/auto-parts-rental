# -*- coding: utf-8 -*-
"""G39 打包 · 包装租赁管理后台原型-20260916.zip
口径＝沿 20260911-3（完整原型目录快照）：
  含 132 HTML（PC 127＋mobile 5）＋ _data/ 7 件（铁律：demo-data 必在）＋ mobile/ 7 件 ＋ 根级交付文档 6 件
  排除：目录内 4 个旧 zip、全部 .prompts/ 工具日志（上次误卷 1 件·本次剔除）
"""
import os, zipfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'P3-R01-包装租赁管理后台原型')
ROOT = os.path.abspath(ROOT)
OUT = os.path.join(ROOT, '包装租赁管理后台原型-20260916.zip')
assert not os.path.exists(OUT), 'zip 已存在'

SEP = chr(92)
files = []
for dp, ds, fs in os.walk(ROOT):
    ds[:] = [d for d in ds if d != '.prompts']
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(SEP, '/')
        if f.endswith('.zip') or '/.prompts/' in rel:
            continue
        files.append(rel)

htmls = [f for f in files if f.endswith('.html')]
assert len(htmls) == 132, 'html=%d != 132' % len(htmls)
assert '_data/demo-data.js' in files and '_data/pc-msg.js' in files
assert not any('.prompts' in f or f.endswith('.zip') for f in files)

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for rel in files:
        z.write(os.path.join(ROOT, rel), rel)

z = zipfile.ZipFile(OUT)
names = [n for n in z.namelist() if not n.endswith('/')]
htmls = [n for n in names if n.endswith('.html')]
data = [n for n in names if n.startswith('_data/')]
mob = [n for n in names if n.startswith('mobile/')]
docs = [n for n in names if n.endswith(('.md', '.json')) and '/' not in n]
print('=== 包装租赁管理后台原型-20260916.zip ===')
print('文件总数: %d（HTML %d = PC %d + mobile %d | _data %d 件 | mobile 共 %d 件 | 交付文档 %d 件）' % (
    len(names), len(htmls), len(htmls) - 5, 5, len(data), len(mob), len(docs)))
print('交付文档:', sorted(docs))
print('嵌套 zip: %d | .prompts: %d' % (
    sum(1 for n in names if n.endswith('.zip')), sum(1 for n in names if '.prompts' in n)))
spot = ['转移出库列表', '退租入库新建', '应收详情', 'mobile/待办审批']
print('新文件抽检:', {k: any(k in n for n in names) for k in spot})
print('大小: %.1f MB' % (os.path.getsize(OUT) / 1048576))
print('完整性 testzip:', 'OK' if z.testzip() is None else z.testzip())
