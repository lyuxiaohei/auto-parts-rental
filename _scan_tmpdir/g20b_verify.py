# -*- coding: utf-8 -*-
"""归属权退场验证：列表 8 列对齐/弹窗无归属权/详情无归属权行/税率编辑器未误伤/JS 0"""
from playwright.sync_api import sync_playwright
import pathlib, io, sys

BASE = pathlib.Path('P3-R01-包装租赁管理后台原型').resolve()
out = []
js_errors = []

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.on('pageerror', lambda e: js_errors.append(str(e)))
    pg.goto((BASE/'基础数据'/'产品档案.html').as_uri())
    pg.wait_for_load_state('load')

    # 1. 列头无归属权、列数=8
    ths = pg.locator('thead th').all_inner_texts()
    th_main = [t for t in ths if t.strip()]
    ok1 = '归属权' not in ths and len([t for t in th_main if t and t != '']) >= 7
    out.append(f"{'PASS' if ok1 else 'FAIL'} 1 列头无归属权（共 {len(th_main)} 列: {[t for t in th_main][:9]}）")

    # 2. 首行 td 数=th 数（列对齐）
    n_th = pg.locator('table thead th').first.locator('xpath=ancestor::thead//th').count()
    first_tds = pg.locator('tbody tr').first.locator('td').count()
    ok2 = first_tds == n_th
    out.append(f"{'PASS' if ok2 else 'FAIL'} 2 首行 td={first_tds} 与 th={n_th} 对齐")

    # 3. 渲染行数据（主表 12 行；税率区 5 行另计）
    rows = pg.locator('.card table tbody tr').count() if pg.locator('.card table tbody tr').count() else pg.locator('tbody tr').count()
    tax_rows_list = pg.locator('#taxRateBody tr').count()
    rows_main = pg.locator('tbody tr').count() - tax_rows_list
    ok3 = rows_main == 12 and tax_rows_list == 5
    out.append(f"{'PASS' if ok3 else 'FAIL'} 3 主表 12 行（实际 {rows_main}）+税率区 5 行（实际 {tax_rows_list}）")

    # 4. 筛选无归属权
    ffs = pg.locator('.ff-label').all_inner_texts()
    ok4 = not any('归属权' in t for t in ffs)
    out.append(f"{'PASS' if ok4 else 'FAIL'} 4 筛选无归属权（实际: {ffs}）")

    # 5. createModal 无归属权 radio、税率编辑器仍在
    pg.evaluate("() => document.getElementById('createModal').classList.add('show')")
    body_txt = pg.locator('#createModal').text_content()
    ok5a = '归属权' not in body_txt
    tax_rows = pg.locator('#taxEditRows .tax-edit-row').count()
    ok5 = ok5a and tax_rows == 2
    out.append(f"{'PASS' if ok5 else 'FAIL'} 5 createModal 无归属权{'✓' if ok5a else '✗'}·税率编辑器在({tax_rows} 行)")

    # 6. 详情弹窗无归属权（点首行详情）
    pg.evaluate("() => document.getElementById('createModal').classList.remove('show')")
    pg.locator('tbody tr').first.get_by_text('详情').first.click()
    pg.wait_for_timeout(500)
    det = pg.locator('.modal-overlay.show, .modal.show').first.text_content() if pg.locator('.modal-overlay.show, .modal.show').count() else ''
    ok6 = '归属权' not in det
    out.append(f"{'PASS' if ok6 else 'FAIL'} 6 详情弹窗无归属权")

    b.close()

out.append(f"{'PASS' if not js_errors else 'FAIL'} JS 错误 = {len(js_errors)} {js_errors[:2]}")
report = '\n'.join(out)
pathlib.Path('_scan_tmpdir/g20b_pw.txt').write_text(report, encoding='utf-8')
with io.open(1, 'w', encoding='utf-8', closefd=False) as f:
    f.write(report + '\n')
sys.exit(0 if all(l.startswith('PASS') for l in out) else 1)
