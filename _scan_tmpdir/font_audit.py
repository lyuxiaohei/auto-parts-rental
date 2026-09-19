# -*- coding: utf-8 -*-
"""#8 字体样式审计：全站 CSS font-family / font-size 声明值聚类，找体系外值与独立风格页。"""
import re
from collections import Counter, defaultdict
from pathlib import Path

PROTO = Path(__file__).resolve().parent.parent / 'P3-R01-包装租赁管理后台原型'

fams = Counter()
sizes = Counter()
fam_pages = defaultdict(set)
size_pages = defaultdict(set)

for p in PROTO.rglob('*.html'):
    if 'mobile' in str(p) or 'backup' in str(p).lower():
        continue
    t = p.read_text(encoding='utf-8', errors='ignore')
    rel = str(p.relative_to(PROTO))
    for m in re.finditer(r'font-family\s*:\s*([^;}]+)', t):
        v = m.group(1).strip()
        fams[v] += 1
        fam_pages[v].add(rel)
    for m in re.finditer(r'font-size\s*:\s*([\d.]+)px', t):
        v = m.group(1)
        sizes[v] += 1
        size_pages[v].add(rel)

print('== font-family 声明值聚类（按处数） ==')
for v, n in fams.most_common():
    pages = fam_pages[v]
    tag = ' [体系外]' if n <= 8 or 'Geist' in v or 'Inter' in v else ''
    print('%5d 处 %3d 页  %s%s' % (n, len(pages), v[:90], tag))
    if tag and len(pages) <= 8:
        for pg in sorted(pages)[:8]:
            print('        -', pg)

print()
print('== font-size 声明值聚类（px） ==')
for v, n in sizes.most_common():
    pages = size_pages[v]
    print('%5d 处 %3d 页  %spx' % (n, len(pages), v))
