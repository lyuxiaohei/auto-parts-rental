# -*- coding: utf-8 -*-
"""四参考价验证：列头 12 列/首行 td=th/四价渲染/弹窗四价表单+税率编辑器/详情四价/JS 0"""
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

    # 1. 列头四价在、旧两价无、列数 12（含选择框列+操作列）
    ths = pg.locator('.table-wrap table thead th').all_inner_texts()
    ok1 = all(t in ths for t in ['参考未税采购价(元)', '参考未税销售价(元)', '参考未税租入价', '参考未税租赁价']) \
          and '参考单价(元)' not in ths and '租金单价(元/天)' not in ths
    out.append(f"{'PASS' if ok1 else 'FAIL'} 1 列头四价在/旧两价无（{len(ths)} 列: {[t for t in ths if '价' in t or '租' in t]}）")

    # 2. 首行 td=th 对齐（只取主表=第一个 .table-wrap 首个 table）
    main_tbl = pg.locator('.table-wrap table').first
    n_th = main_tbl.locator('thead th').count()
    n_td = main_tbl.locator('tbody tr').first.locator('td').count()
    ok2 = n_th == n_td
    out.append(f"{'PASS' if ok2 else 'FAIL'} 2 主表首行 td={n_td} = th={n_th}")

    # 3. 首行（WBX-1210L）四价值
    row_txt = pg.locator('.table-wrap table tbody tr').first.inner_text()
    ok3 = '380.00' in row_txt and '45.00' in row_txt and '60.00' in row_txt
    out.append(f"{'PASS' if ok3 else 'FAIL'} 3 首行四价值（380 采购/45 租入·月/60 租赁·月）: {[x for x in row_txt.replace(chr(10),'|').split('|') if '价' in x or '.' in x][:6]}")

    # 4. 弹窗四价表单+税率编辑器
    pg.evaluate("() => document.getElementById('createModal').classList.add('show')")
    labels = pg.locator('#createModal .form-label').all_inner_texts()
    ok4a = sum(1 for t in labels if '参考未税' in t) == 4 and not any('租金单价' in t for t in labels)
    tax_n = pg.locator('#taxEditRows .tax-edit-row').count()
    ok4 = ok4a and tax_n == 2
    out.append(f"{'PASS' if ok4 else 'FAIL'} 4 弹窗四价表单×{sum(1 for t in labels if '参考未税' in t)}+税率编辑器 {tax_n} 行")

    # 5. 详情弹窗四价（点首行详情）
    pg.evaluate("() => document.getElementById('createModal').classList.remove('show')")
    pg.locator('.table-wrap table tbody tr').first.get_by_text('详情').first.click()
    pg.wait_for_timeout(600)
    modal = pg.locator('.modal.show, .modal-overlay.show').first
    det_txt = modal.text_content() if modal.count() else ''
    ok5 = all(t in det_txt for t in ['参考未税采购价', '参考未税销售价', '参考未税租入价', '参考未税租赁价']) and '日租金' not in det_txt
    out.append(f"{'PASS' if ok5 else 'FAIL'} 5 详情四价块在·日租金无")

    # 6. 模板页四价表单
    pg2 = b.new_page()
    pg2.on('pageerror', lambda e: js_errors.append(str(e)))
    pg2.goto((BASE/'基础数据'/'弹窗'/'新建产品.html').as_uri())
    pg2.wait_for_load_state('load')
    lab2 = pg2.locator('.form-label').all_inner_texts()
    ok6 = sum(1 for t in lab2 if '参考未税' in t) == 4
    out.append(f"{'PASS' if ok6 else 'FAIL'} 6 模板页四价表单×{sum(1 for t in lab2 if '参考未税' in t)}")

    b.close()

out.append(f"{'PASS' if not js_errors else 'FAIL'} JS 错误 = {len(js_errors)} {js_errors[:2]}")
report = '\n'.join(out)
pathlib.Path('_scan_tmpdir/g21_pw.txt').write_text(report, encoding='utf-8')
with io.open(1, 'w', encoding='utf-8', closefd=False) as f:
    f.write(report + '\n')
sys.exit(0 if all(l.startswith('PASS') for l in out) else 1)
