# -*- coding: utf-8 -*-
"""G17 T3 门5 Playwright 抽验：库存查询/租入单列表/物料档案弹窗/BOM维护 + JS 0"""
from playwright.sync_api import sync_playwright
import pathlib, io, sys

BASE = pathlib.Path('P3-R01-包装租赁管理后台原型').resolve()
out = []
js_errors = []

def url(rel):
    return (BASE / rel).as_uri()

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.on('pageerror', lambda e: js_errors.append(str(e)))

    # 1. 库存查询：列头「物料类型」+ 值含「租赁器具」
    pg.goto(url('仓储作业/库存查询.html')); pg.wait_for_load_state('networkidle')
    ths = pg.locator('th').all_inner_texts()
    tds = pg.locator('td').all_inner_texts()
    ok1a = '物料类型' in ths
    ok1b = any('租赁器具' in t for t in tds)
    out.append(f"{'PASS' if ok1a else 'FAIL'} 1a 库存查询列头含「物料类型」（实际 th：{[t for t in ths if '物料' in t or '类型' in t or '类别' in t]}）")
    out.append(f"{'PASS' if ok1b else 'FAIL'} 1b 库存查询值含「租赁器具」（白名单保留）")

    # 2. 租入单列表：列头「物料」（A 类数据驱动页，渲染后列头来自 cfg）
    pg.goto(url('租赁管理/租入单列表.html')); pg.wait_for_load_state('networkidle')
    ths2 = pg.locator('th').all_inner_texts()
    ok2 = '物料' in ths2 and '器具' not in ths2
    out.append(f"{'PASS' if ok2 else 'FAIL'} 2 租入单列表列头含「物料」且无「器具」（实际：{[t for t in ths2 if '物料' in t or '器具' in t]}）")

    # 3. 物料档案：新建弹窗「物料分类」标签 + 筛选「物料分类：」
    pg.goto(url('基础数据/产品档案.html')); pg.wait_for_load_state('networkidle')
    ok3a = '物料分类：' in pg.locator('.ff-label').all_inner_texts() or any('物料分类' in t for t in pg.locator('.ff-label').all_inner_texts())
    ths3 = pg.locator('th').all_inner_texts()
    ok3b = '物料分类' in ths3
    pg.evaluate("document.querySelector('.modal') ? document.querySelectorAll('.modal').forEach(m=>m.style.display='flex') : 0")
    labels3 = pg.locator('.form-label').all_inner_texts()
    ok3c = any('物料分类' in t for t in labels3)
    out.append(f"{'PASS' if ok3a else 'FAIL'} 3a 物料档案筛选含「物料分类：」")
    out.append(f"{'PASS' if ok3b else 'FAIL'} 3b 物料档案列头含「物料分类」")
    out.append(f"{'PASS' if ok3c else 'FAIL'} 3c 新建产品弹窗表单标签含「物料分类」（实际 form-label：{[t for t in labels3 if '分类' in t]}）")

    # 4. BOM维护：列头「物料类型」+ 值「零部件」
    pg.goto(url('基础数据/BOM维护.html')); pg.wait_for_load_state('networkidle')
    ths4 = pg.locator('th').all_inner_texts()
    tds4 = pg.locator('td').all_inner_texts()
    ok4a = '物料类型' in ths4
    ok4b = any('零部件' in t for t in tds4) and not any(t.strip() == '零件' for t in tds4)
    out.append(f"{'PASS' if ok4a else 'FAIL'} 4a BOM维护列头含「物料类型」")
    out.append(f"{'PASS' if ok4b else 'FAIL'} 4b BOM维护值含「零部件」且无裸「零件」值")

    # 5. 其他入库：列头「单据编号」+「入库库房」
    pg.goto(url('仓储作业/其他入库列表.html')); pg.wait_for_load_state('networkidle')
    ths5 = pg.locator('th').all_inner_texts()
    ok5 = '单据编号' in ths5 and '入库库房' in ths5 and '单号' not in ths5 and '入库仓库' not in ths5
    out.append(f"{'PASS' if ok5 else 'FAIL'} 5 其他入库列头「单据编号」+「入库库房」（实际：{[t for t in ths5 if '单' in t or '库' in t]}）")

    b.close()

out.append(f"{'PASS' if not js_errors else 'FAIL'} JS 错误 = {len(js_errors)} {js_errors[:3]}")
report = '\n'.join(out)
pathlib.Path('_scan_tmpdir/g17_t3_pw.txt').write_text(report, encoding='utf-8')
with io.open(1, 'w', encoding='utf-8', closefd=False) as f:
    f.write(report + '\n')
sys.exit(0 if all(l.startswith('PASS') for l in out) else 1)
