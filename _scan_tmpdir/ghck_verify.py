# -*- coding: utf-8 -*-
"""#14 改名后验证：菜单链接/列表渲染/F01/我的待办 + 定向审计 10 页。"""
import sys
from pathlib import Path

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁')
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
sys.path.insert(0, str(ROOT / '_scan_tmpdir'))

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)

    pg.goto((PROTO / '租入管理/归还出库列表.html').as_uri(), wait_until='networkidle')
    r = pg.evaluate("""() => {
        const links = [...document.querySelectorAll('[href],[onclick]')].filter(el =>
            (el.getAttribute('href')||'') .includes('归还出库列表.html') ||
            (el.getAttribute('onclick')||'').includes('归还出库列表.html'));
        return {rows: document.querySelectorAll('tbody tr').length,
                menuHits: links.length, menuText: links[0] ? links[0].textContent.trim() : ''};
    }""")
    print('列表页:', r)

    pg.goto((PROTO / 'P3-R01-F01-业务流程导航图.html').as_uri(), wait_until='networkidle')
    has = pg.evaluate("() => document.body.innerHTML.includes('归还出库')")
    print('F01 含归还出库:', has)

    pg.goto((PROTO / '我的待办.html').as_uri(), wait_until='networkidle')
    r = pg.evaluate("""() => {
        const opts = [...document.querySelectorAll('select option')].map(o => o.textContent);
        return {hasNew: opts.some(t => t.includes('归还出库')), hasOld: opts.some(t => t.includes('租入归还'))};
    }""")
    print('我的待办 option:', r)
    print('JS 错误累计:', len(errs))

    from _run_filter_audit3 import audit_page
    PAGES = ['租入管理/归还出库列表.html', '租入管理/归还出库新建.html', '租入管理/归还出库详情.html',
             '租入管理/归还出库审核.html', '租入管理/租入单列表.html', '租入管理/租入单详情.html',
             '我的待办.html', 'P3-R01-F01-业务流程导航图.html', '租赁管理/租赁出库录单.html',
             '租赁管理/退租入库列表.html']
    ok = 0
    for rel in PAGES:
        res = audit_page(b, PROTO / rel)
        good = not res['problems'] and not res['dead_links']
        ok += good
        print('%s %s problems=%d dead=%d js=%d' % ('PASS' if good else 'FAIL', rel,
              len(res['problems']), len(res['dead_links']), len(res['js_errors'])),
              res['problems'][:1] if res['problems'] else '')
    print('定向审计: %d/%d PASS' % (ok, len(PAGES)))
    b.close()
