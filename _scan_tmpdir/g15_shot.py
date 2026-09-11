# -*- coding: utf-8 -*-
"""G15 T7 · F01 全页截图（PW · full_page）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁')
F = ROOT / 'P3-R01-包装租赁管理后台原型' / 'P3-R01-F01-业务流程导航图.html'
OUT = ROOT / '_scan_tmpdir' / 'g15-f01-after.png'
url = F.as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1000, 'height': 1200})
    pg.goto(url, wait_until='domcontentloaded', timeout=60000)
    pg.wait_for_timeout(1500)
    t = pg.evaluate("document.title")
    h1 = pg.evaluate("document.querySelector('h1').textContent")
    svgs = pg.evaluate("[...document.querySelectorAll('svg')].map(s => s.getAttribute('viewBox'))")
    print('title:', t)
    print('h1:', h1)
    print('viewBoxes:', svgs)
    pg.screenshot(full_page=True, path=str(OUT))
    b.close()
print('截图:', OUT, OUT.stat().st_size, '字节')
