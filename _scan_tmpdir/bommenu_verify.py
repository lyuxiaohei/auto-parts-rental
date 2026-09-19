# -*- coding: utf-8 -*-
"""菜单 BOM→BOM组合 改后验证：菜单渲染/选中态/F01/审计 4 页。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
sys.path.insert(0, str(ROOT / '_scan_tmpdir'))

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))

    for rel in ['基础数据/产品档案.html', '基础数据/BOM.html']:
        pg.goto((PROTO / rel).as_uri(), wait_until='networkidle')
        r = pg.evaluate("""() => {
          const items = [...document.querySelectorAll('.sm-link')].map(a => a.textContent.trim());
          return {newCount: items.filter(t => t === 'BOM组合').length,
                  oldCount: items.filter(t => t === 'BOM').length,
                  selected: (document.querySelector('.sm-link.selected') || {}).textContent};
        }""")
        print(rel, '->', r)

    pg.goto((PROTO / 'P3-R01-F01-业务流程导航图.html').as_uri(), wait_until='networkidle')
    has = pg.evaluate("() => document.body.innerHTML.includes('BOM组合')")
    print('F01 含 BOM组合:', has, '| JS 错误:', len(errs))

    from _run_filter_audit3 import audit_page
    for rel in ['基础数据/BOM.html', '基础数据/BOM维护.html', '我的待办.html', 'P3-R01-F01-业务流程导航图.html']:
        res = audit_page(b, PROTO / rel)
        print('%s problems=%d dead=%d js=%d' % (rel, len(res['problems']), len(res['dead_links']), len(res['js_errors'])))
    b.close()
