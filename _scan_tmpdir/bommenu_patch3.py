# -*- coding: utf-8 -*-
"""BOM 菜单更名·收尾：三张 selected 页补替换 + 全库残留终检 + 渲染复验。"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
BACKUP = ROOT / 'backup-bommenu-20260919'
OLD, NEW = 'class="sm-link selected">BOM<', 'class="sm-link selected">BOM组合<'

for f in ['基础数据/BOM.html', '基础数据/BOM维护.html', '基础数据/BOM版本查看.html']:
    p = PROTO / f
    b = p.read_bytes()
    n = b.count(OLD.encode('utf-8'))
    dst = BACKUP / f
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copy2(p, dst)
    p.write_bytes(b.replace(OLD.encode('utf-8'), NEW.encode('utf-8')))
    print(f, n, '处已补')

r1 = r2 = 0
for p in PROTO.rglob('*.html'):
    if 'mobile' in str(p) or 'backup' in str(p).lower():
        continue
    b = p.read_bytes()
    r1 += b.count(b'\')">BOM<')
    r2 += b.count(b'selected">BOM<')
print('菜单残留终检: onclick形态=%d selected形态=%d' % (r1, r2))

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    for rel in ['基础数据/BOM.html', '基础数据/BOM维护.html', '基础数据/BOM版本查看.html']:
        pg.goto((PROTO / rel).as_uri(), wait_until='networkidle')
        r = pg.evaluate("""() => {
          const items = [...document.querySelectorAll('.sm-link')].map(a => a.textContent.trim());
          return {newCount: items.filter(t => t === 'BOM组合').length,
                  oldCount: items.filter(t => t === 'BOM').length,
                  sel: (document.querySelector('.sm-link.selected') || {}).textContent};
        }""")
        print(rel.split('/')[-1], r)
    print('JS 错误:', len(errs))
    b.close()
