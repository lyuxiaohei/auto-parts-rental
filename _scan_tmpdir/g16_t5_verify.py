# -*- coding: utf-8 -*-
"""G16 T5 验证门 5：Playwright——数据字典新大类 + 物料档案弹窗「物料类型」+ JS 错误"""
from playwright.sync_api import sync_playwright
import pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent / 'P3-R01-包装租赁管理后台原型'
out, fails, js_errs = [], [], []

with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page()
    pg.on('pageerror', lambda e: js_errs.append(str(e)))
    pg.on('console', lambda m: js_errs.append(m.text) if m.type == 'error' else None)

    # ---- 页1 数据字典：新大类可见 + 点击后明细含 器具/零部件 ----
    pg.goto((BASE / '系统管理/数据字典.html').as_uri())
    pg.wait_for_load_state('networkidle')
    item = pg.locator('.dic-item', has_text='物料类型')
    out.append(f'[1] 数据字典·物料类型分类项可见: {item.count() == 1}')
    if item.count() == 1:
        cnt = item.locator('.cnt').inner_text()
        out.append(f'[1b] 分类计数: {cnt} (期望 2)')
        item.first.click()
        pg.wait_for_timeout(300)
        title = pg.locator('.dic-wrap .card-head .card-title').inner_text()
        rows = pg.locator('.dic-wrap tbody tr').all_inner_texts()
        has_qj = any('器具' in r for r in rows)
        has_lbj = any('零部件' in r for r in rows)
        out.append(f'[1c] 切换后标题: {title!r}')
        out.append(f'[1d] 明细含器具: {has_qj} / 含零部件: {has_lbj} / 行数: {len(rows)}')
        if not (has_qj and has_lbj and '物料类型' in title): fails.append('数据字典明细缺器具/零部件')
    else:
        fails.append('数据字典无物料类型分类项')

    # ---- 页2 物料档案：createModal「物料类型」在「分类」之前 + 2 选项 ----
    pg.goto((BASE / '基础数据/产品档案.html').as_uri())
    pg.wait_for_load_state('networkidle')
    pg.evaluate("openModal('createModal')")
    pg.wait_for_timeout(300)
    modal = pg.locator('#createModal')
    labels = [t.strip() for t in modal.locator('.form-label').all_inner_texts()]
    labels_clean = [l.lstrip('*').strip() for l in labels]
    out.append(f'[2] createModal 标签序: {labels_clean}')
    def idx(name):
        for i, l in enumerate(labels_clean):
            if l == name: return i
        return -1
    i_mt, i_cls = idx('物料类型'), idx('分类')
    out.append(f'[2b] 物料类型 idx={i_mt} < 分类 idx={i_cls}: {0 <= i_mt < i_cls}')
    if not (0 <= i_mt < i_cls): fails.append('物料类型不在分类之前')
    sel = modal.locator('.form-row', has_text='物料类型').locator('select')
    opts = sel.locator('option').all_inner_texts()
    out.append(f'[2c] 物料类型下拉选项: {opts} (期望 器具/零部件, 器具 selected)')
    if opts != ['器具', '零部件']: fails.append(f'物料类型选项异常: {opts}')
    first_sel = sel.locator('option').first.get_attribute('selected')
    out.append(f'[2d] 器具默认选中: {first_sel is not None or sel.evaluate("el=>el.value") == "器具"}')

    # ---- 页3 预览副本 弹窗/新建产品.html ----
    pg.goto((BASE / '基础数据/弹窗/新建产品.html').as_uri())
    pg.wait_for_load_state('networkidle')
    body = pg.locator('.form-row', has_text='物料类型')
    out.append(f'[3] 预览页物料类型行存在: {body.count() == 1}，选项: {body.locator("option").all_inner_texts() if body.count() else []}')
    if body.count() != 1: fails.append('预览页缺物料类型行')

    br.close()

out.append(f'[JS] 页面错误数: {len(js_errs)}' + (f' -> {js_errs[:3]}' if js_errs else ''))
if js_errs: fails.append(f'JS 错误 {len(js_errs)}')
out.append(f'== 判定: {"ALL PASS" if not fails else "FAIL: " + "; ".join(fails)} ==')
pathlib.Path(__file__).parent.joinpath('g16_t5_result.txt').write_text('\n'.join(out), encoding='utf-8')
print('\n'.join(out))
