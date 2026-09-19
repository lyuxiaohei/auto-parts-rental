# -*- coding: utf-8 -*-
"""四单据库存校验统一验证（D-161）：四页同构行为——库存列红绿/数量标红/红条/双按钮。"""
import sys
from pathlib import Path

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁')
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
sys.path.insert(0, str(ROOT / '_scan_tmpdir'))

from playwright.sync_api import sync_playwright

JS_ROW = """() => {
  const tr = document.querySelector('.edit-tbl tbody tr');
  const cells = [...document.querySelectorAll('.edit-tbl tbody tr')].map(r => r.querySelector('.stock-cell')?.textContent);
  const qi = tr.querySelector('input[data-tax="qty"]');
  const chk = tr.querySelector('.chk-cell span');
  const w = document.getElementById('stockWarn');
  return {cells, qty: qi.value, qtyColor: qi.style.color,
          chk: chk ? chk.textContent + '/' + chk.style.color : null,
          warn: w ? w.style.display : 'NOBAR',
          btns: w ? w.querySelectorAll('button').length : 0};
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)

    # 销售出库新建：默认场景 5,000 > 1,520 → 全链红
    pg.goto((PROTO / '销售管理/销售出库新建.html').as_uri(), wait_until='networkidle')
    r = pg.evaluate(JS_ROW)
    print('销售出库[默认缺] 库存=%s 数量色=%s 红条=%s 按钮=%d' % (r['cells'], r['qtyColor'], r['warn'], r['btns']))

    # 租赁出库录单：默认满足 + 超量联动 + 校验列动态
    pg.goto((PROTO / '租赁管理/租赁出库录单.html').as_uri(), wait_until='networkidle')
    r = pg.evaluate(JS_ROW)
    print('租赁出库录单[默认] 库存=%s 校验=%s 红条=%s' % (r['cells'], r['chk'], r['warn']))
    r2 = pg.evaluate("""() => {
      const inp = document.querySelector('.edit-tbl input[data-tax="qty"]');
      inp.value = '9999'; inp.dispatchEvent(new Event('input', {bubbles: true}));
      const tr = inp.closest('tr');
      return {stock: tr.querySelector('.stock-cell').textContent, stockColor: tr.querySelector('.stock-cell').style.color,
              qtyColor: inp.style.color, chk: tr.querySelector('.chk-cell span').textContent,
              warn: document.getElementById('stockWarn').style.display, btns: document.getElementById('stockWarn').querySelectorAll('button').length};
    }""")
    print('  [改9999] 库存=%s(%s) 数量色=%s 校验=%s 红条=%s 按钮=%d' % (r2['stock'], r2['stockColor'], r2['qtyColor'], r2['chk'], r2['warn'], r2['btns']))

    # 租赁单新建 / 销售订单新建：数量标红回归
    for rel in ['租赁管理/租赁单新建.html', '销售管理/销售订单新建.html']:
        pg.goto((PROTO / rel).as_uri(), wait_until='networkidle')
        r = pg.evaluate(JS_ROW)
        print('%s[默认] 库存=%s 数量色=%s 红条=%s' % (rel.split('/')[-1], r['cells'], r['qtyColor'] or '(默认)', r['warn']))
        r2 = pg.evaluate("""() => {
          const inp = document.querySelector('.edit-tbl input[data-tax="qty"]');
          inp.value = '9999'; inp.dispatchEvent(new Event('input', {bubbles: true}));
          return {qtyColor: inp.style.color, warn: document.getElementById('stockWarn').style.display,
                  btns: document.getElementById('stockWarn').querySelectorAll('button').length};
        }""")
        print('  [改9999] 数量色=%s 红条=%s 按钮=%d' % (r2['qtyColor'], r2['warn'], r2['btns']))

    print('JS 错误累计:', len(errs), errs[:2] if errs else '')

    from _run_filter_audit3 import audit_page
    ok = 0
    PAGES = ['销售管理/销售出库新建.html', '租赁管理/租赁出库录单.html', '租赁管理/租赁单新建.html', '销售管理/销售订单新建.html']
    for rel in PAGES:
        res = audit_page(b, PROTO / rel)
        good = not res['problems'] and not res['dead_links']
        ok += good
        print('%s %s problems=%d dead=%d' % ('PASS' if good else 'FAIL', rel, len(res['problems']), len(res['dead_links'])))
    print('定向审计: %d/4 PASS' % ok)
    b.close()
