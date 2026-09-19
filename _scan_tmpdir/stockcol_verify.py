# -*- coding: utf-8 -*-
"""待办#3 扩项验证：三页明细「可用库存」列改造（列序/JS 填值/红绿/警告条/审计）。"""
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

    # 1) 租赁单新建
    pg.goto((PROTO / '租赁管理/租赁单新建.html').as_uri(), wait_until='networkidle')
    r = pg.evaluate("""() => {
        const ths = [...document.querySelectorAll('.edit-tbl thead th')].map(t => t.textContent.trim());
        const i = ths.indexOf('数量'), j = ths.indexOf('可用库存');
        const cells = [...document.querySelectorAll('.edit-tbl tbody tr')].map(tr => tr.querySelector('.stock-cell')?.textContent);
        const hints = document.querySelectorAll('.stock-hint').length;
        return {cols: ths, qtyIdx: i, stockIdx: j, cells, hints};
    }""")
    print('租赁单新建: 列序=数量@%d 可用库存@%d 相邻=%s 值=%s 物料下残留提示=%d' % (
        r['qtyIdx'], r['stockIdx'], r['stockIdx'] == r['qtyIdx'] + 1, r['cells'], r['hints']))
    # 改数量超库存 → 红 + stockWarn
    r2 = pg.evaluate("""() => {
        const inp = document.querySelector('.edit-tbl input[data-tax="qty"]');
        inp.value = '9999'; inp.dispatchEvent(new Event('input', {bubbles: true}));
        const tr = inp.closest('tr');
        const cell = tr.querySelector('.stock-cell');
        return {cellText: cell.textContent, color: cell.style.color, warn: document.getElementById('stockWarn').style.display};
    }""")
    print('  超量联动: cell=%s color=%s 警告条=%s' % (r2['cellText'], r2['color'], r2['warn']))

    # 2) 销售订单新建
    pg.goto((PROTO / '销售管理/销售订单新建.html').as_uri(), wait_until='networkidle')
    r = pg.evaluate("""() => {
        const ths = [...document.querySelectorAll('.edit-tbl thead th')].map(t => t.textContent.trim());
        const i = ths.indexOf('数量'), j = ths.indexOf('可用库存');
        const cells = [...document.querySelectorAll('.edit-tbl tbody tr')].map(tr => tr.querySelector('.stock-cell')?.textContent);
        return {i, j, cells, hints: document.querySelectorAll('.stock-hint').length};
    }""")
    print('销售订单新建: 相邻=%s 值=%s 物料下残留提示=%d' % (r['j'] == r['i'] + 1, r['cells'], r['hints']))

    # 3) 租赁出库录单：列序
    pg.goto((PROTO / '租赁管理/租赁出库录单.html').as_uri(), wait_until='networkidle')
    r = pg.evaluate("""() => {
        const ths = [...document.querySelectorAll('.edit-tbl thead th')].map(t => t.textContent.trim());
        const row1 = [...document.querySelectorAll('.edit-tbl tbody tr')][0];
        const vals = [...row1.querySelectorAll('td')].map(td => td.textContent.trim().slice(0, 8));
        return {ths, vals};
    }""")
    i, j, k = r['ths'].index('出库数量 *'), r['ths'].index('可用组合库存'), r['ths'].index('可用量校验')
    print('租赁出库录单: 数量@%d 库存@%d 校验@%d 顺序正确=%s' % (i, j, k, j == i + 1 and k == j + 1))
    print('  行1 单元格序:', [v for v in r['vals'] if v][:9])
    print('JS 错误累计:', len(errs), errs[:2] if errs else '')

    from _run_filter_audit3 import audit_page
    ok = 0
    for rel in ['租赁管理/租赁单新建.html', '销售管理/销售订单新建.html', '租赁管理/租赁出库录单.html']:
        res = audit_page(b, PROTO / rel)
        good = not res['problems'] and not res['dead_links']
        ok += good
        print('%s %s problems=%d dead=%d' % ('PASS' if good else 'FAIL', rel, len(res['problems']), len(res['dead_links'])))
    print('定向审计: %d/3 PASS' % ok)
    b.close()
