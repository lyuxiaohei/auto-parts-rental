# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
BASE = 'file:///' + str(PROTO).replace('\\', '/').replace(' ', '%20') + '/'
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page()
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(BASE + '仓储作业/库存查询.html')
    pg.wait_for_timeout(800)
    info = pg.evaluate("""() => {
      const tbs=[...document.querySelectorAll('tbody')];
      return tbs.map(t=>({rows:t.querySelectorAll('tr').length,
        first:(t.querySelector('tr')?t.querySelector('tr').textContent.slice(0,30):''),
        xnc:t.textContent.indexOf('XNC-AJZX-WBX')>-1}));
    }""")
    for i, t in enumerate(info):
        print(i, t)
    print('errs:', errs)
    b.close()
