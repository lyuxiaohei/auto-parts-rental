# -*- coding: utf-8 -*-
"""供应商税率维护验证：渲染/预填/下拉源/加删行/JS 0（产品档案页+弹窗模板页）"""
from playwright.sync_api import sync_playwright
from urllib.parse import unquote
import pathlib, io, sys

BASE = pathlib.Path('P3-R01-包装租赁管理后台原型').resolve()
out = []
js_errors = []

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.on('pageerror', lambda e: js_errors.append(str(e)))

    # ===== 产品档案页 =====
    pg.goto((BASE/'基础数据'/'产品档案.html').as_uri())
    pg.wait_for_load_state('load')
    # 1. 税率区数据驱动渲染 5 行
    rows = pg.locator('#taxRateBody tr').count()
    ok1 = rows == 5
    first = pg.locator('#taxRateBody tr').first.inner_text().replace('\t', ' ') if rows else ''
    out.append(f"{'PASS' if ok1 else 'FAIL'} 1 税率区按 productTaxes 渲染 {rows} 行（首行: {first[:70]}）")

    # 2. 打开 createModal：行编辑器预填 WBX-1210L 两行
    pg.evaluate("() => document.getElementById('createModal').classList.add('show')")
    er = pg.locator('#taxEditRows .tax-edit-row').count()
    ok2 = er == 2
    out.append(f"{'PASS' if ok2 else 'FAIL'} 2 createModal 预填 WBX-1210L 税率 {er} 行（期望 2）")

    # 3. 供应商下拉源=partners 4 家
    opts = pg.locator('#taxEditRows .tax-edit-row').first.locator('select.tax-sel option').all_inner_texts()
    ok3 = len(opts) == 4 and '路凯包装运营（上海）有限公司' in opts
    out.append(f"{'PASS' if ok3 else 'FAIL'} 3 下拉源=partners 供应商 {len(opts)} 家: {opts[:2]}…")

    # 4. + 添加一行 → 3 行；删除 → 2 行
    pg.click('button:has-text("+ 添加一行")')
    n_after_add = pg.locator('#taxEditRows .tax-edit-row').count()
    pg.locator('#taxEditRows .tax-del').first.click()
    n_after_del = pg.locator('#taxEditRows .tax-edit-row').count()
    ok4 = n_after_add == 3 and n_after_del == 2
    out.append(f"{'PASS' if ok4 else 'FAIL'} 4 加行→{n_after_add}（期望3）·删行→{n_after_del}（期望2）")

    # ===== 弹窗模板页 =====
    pg2 = b.new_page()
    pg2.on('pageerror', lambda e: js_errors.append(str(e)))
    pg2.goto((BASE/'基础数据'/'弹窗'/'新建产品.html').as_uri())
    pg2.wait_for_load_state('load')
    er2 = pg2.locator('#taxEditRows .tax-edit-row').count()
    opts2 = pg2.locator('#taxEditRows .tax-edit-row').first.locator('select.tax-sel option').count() if er2 else 0
    ok5 = er2 == 2 and opts2 == 4
    out.append(f"{'PASS' if ok5 else 'FAIL'} 5 模板页同款：预填 {er2} 行·下拉(首行) {opts2} 家（demo-data 引用生效）")

    b.close()

out.append(f"{'PASS' if not js_errors else 'FAIL'} JS 错误 = {len(js_errors)} {js_errors[:2]}")
report = '\n'.join(out)
pathlib.Path('_scan_tmpdir/g20_pw.txt').write_text(report, encoding='utf-8')
with io.open(1, 'w', encoding='utf-8', closefd=False) as f:
    f.write(report + '\n')
sys.exit(0 if all(l.startswith('PASS') for l in out) else 1)
