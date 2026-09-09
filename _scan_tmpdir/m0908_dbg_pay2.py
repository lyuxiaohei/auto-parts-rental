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
    pg.on('console', lambda m: errs.append('CONSOLE-' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
    pg.goto(BASE + '财务协同/应付账单.html')
    pg.wait_for_selector('tbody tr')
    pg.wait_for_timeout(600)
    print('locator count:', pg.locator('tbody a[data-detail-key]').count())
    print('eval count:', pg.eval_on_selector_all('tbody a[data-detail-key]', 'els=>els.length'))
    print('main-col HTML len:', pg.evaluate("document.querySelector('.main-col').innerHTML.length"))
    print('instCard present:', pg.evaluate("!!document.getElementById('instCard')"))
    print('errs:', errs[:5])
    # 编程点击测试
    r = pg.evaluate("""() => {
      const a = document.querySelector('tbody a[data-detail-key]');
      if (!a) return 'no anchor';
      a.click();
      const m = document.getElementById('detailModal');
      return m && m.classList.contains('show') ? (document.getElementById('detailTitle').textContent.slice(0,30)) : 'modal not shown';
    }""")
    print('编程点击:', r)
    b.close()
