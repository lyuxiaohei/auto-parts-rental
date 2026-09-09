# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
BASE = 'file:///' + str(PROTO).replace('\\', '/').replace(' ', '%20') + '/'
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(BASE + '财务协同/应付账单.html')
    pg.wait_for_selector('tbody tr')
    keys = pg.eval_on_selector_all('tbody a[data-detail-key]', 'els=>els.map(e=>e.getAttribute("data-detail-key"))')
    print('详情锚点数:', len(keys))
    print('JS errors:', errs[:3])
    for i, k in enumerate(keys):
        try:
            pg.click(f'tbody a[data-detail-key="{k}"]', timeout=3000)
            ttl = pg.eval_on_selector('#detailTitle', 'e=>e.textContent')
            print(i, k, '->', ttl[:40])
            pg.eval_on_selector('#detailModal .modal-close', 'e=>e.click()')
            pg.wait_for_timeout(150)
        except Exception as ex:
            print(i, k, 'CLICK FAIL:', str(ex)[:120])
    b.close()
