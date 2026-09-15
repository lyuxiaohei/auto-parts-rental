# -*- coding: utf-8 -*-
"""G37 T1：菜单 v5→v6 全站同步——租赁管理组插「转移出库」（退租入库之前）
变体：../ 前缀 115 页 / 无前缀 1 页 / selected 4 页（退租入库自家页）。已含新行页跳过。"""
import io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
ZY = '转移出库列表.html'

changed, skipped, nomenu = [], [], 0
for dp, dn, fn in os.walk(ROOT):
    if 'backup' in dp or os.sep + 'mobile' in dp:
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        s = io.open(p, encoding='utf-8', newline='').read()
        if '转移出库列表.html' in s:
            skipped.append(os.path.relpath(p, ROOT))
            continue
        # 退租入库菜单行（onclick 或 selected）
        m = re.search(r'([ \t]*)<li><div class="sm-link(?: selected)?"(?: onclick="go\(\'([^\']*)退租入库列表\.html\'\)")?>退租入库</div></li>\r?\n?', s)
        if not m:
            nomenu += 1
            continue
        indent, prefix = m.group(1), m.group(2) or ''
        newline = '\r\n' if '\r\n' in m.group(0) else '\n'
        newli = '%s<li><div class="sm-link" onclick="go(\'%s租赁管理/%s\')">转移出库</div></li>%s' % (indent, prefix, ZY, newline)
        s = s[:m.start()] + newli + s[m.start():]
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
        changed.append(os.path.relpath(p, ROOT))

print('插入 %d 页 / 跳过(已含) %d 页 / 无菜单页 %d' % (len(changed), len(skipped), nomenu))
print('已含（跳过）:', skipped)
# 校验：全站「转移出库」菜单行计数 = 含菜单页总数
n_zy = 0
for dp, dn, fn in os.walk(ROOT):
    if 'backup' in dp or os.sep + 'mobile' in dp:
        continue
    for f in fn:
        if f.endswith('.html'):
            s2 = io.open(os.path.join(dp, f), encoding='utf-8', errors='replace').read()
            n_zy += s2.count('>转移出库</div></li>')
print('全站转移出库菜单行计数:', n_zy)
