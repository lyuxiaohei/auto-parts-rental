# -*- coding: utf-8 -*-
"""列表数据驱动试点验证门（2026-09-08）· 租赁单列表 + 采购入库列表 各 7 项断言"""
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'

PAGES = [
    dict(name='租赁单列表', file=PROTO / '销售管理' / '租赁单列表.html', entity='leaseOrders',
         n=9, pins=5, filter=dict(kind='select', label='客户名称', value='一汽解放汽车有限公司', expect=4),
         filter2=dict(kind='input', label='租赁单号', value='032', expect=1),
         stabs={'全部': 9, '待审核': 1, '已审核': 1, '在租': 3, '已退租': 3, '已关闭': 1}),
    dict(name='采购入库列表', file=PROTO / '仓储作业' / '采购入库列表.html', entity='purchaseInbounds',
         n=8, pins=3, filter=dict(kind='select', label='供应商', value='苏州联恒五金制品有限公司', expect=4),
         filter2=dict(kind='input', label='入库单号', value='009', expect=1),
         stabs={'全部': 8, '待验收': 1, '已入库': 7}),
]

results = []

def check(page_name, item, ok, detail=''):
    results.append((page_name, item, ok, detail))
    print(('✅' if ok else '❌'), page_name, '|', item, '|', detail)

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for P in PAGES:
        page = browser.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:150]))
        page.goto(P['file'].as_uri(), wait_until='load')
        page.wait_for_selector('tbody tr', timeout=5000)
        page.wait_for_timeout(300)

        # 1 行数=实体条数
        rows = page.locator('tbody').first.locator('tr')
        n_rows = rows.count()
        check(P['name'], '1 行数=实体条数', n_rows == P['n'], f'{n_rows}=={P["n"]}')

        # 2 行单号=实体键
        keys = page.evaluate("Object.keys(window.DEMO_DATA['%s'])" % P['entity'])
        row_keys = [rows.nth(i).locator('td').nth(1).text_content().strip() for i in range(n_rows)]
        check(P['name'], '2 行单号=实体键', row_keys == keys, f'{row_keys == keys}')

        # 3 详情弹窗标题=行单号（逐行实点有详情钮的行）
        ok3, tried = True, 0
        for i in range(n_rows):
            a = rows.nth(i).locator('a[data-detail-key]')
            if a.count() == 0:
                continue
            tried += 1
            key = a.first.get_attribute('data-detail-key')
            a.first.click()
            page.wait_for_timeout(80)
            title = page.locator('#detailTitle').text_content()
            shown = page.locator('#detailModal').evaluate("el => el.classList.contains('show')")
            if key not in title or not shown:
                ok3 = False
                check(P['name'], f'3 详情标题·{key}', False, f'title={title!r} shown={shown}')
            page.evaluate("closeModal('detailModal')")
        check(P['name'], '3 详情弹窗标题=行单号', ok3, f'逐行实点 {tried} 行全过' if ok3 else '见上')

        # 4 真过滤（select + input 各一组）
        for F in (P['filter'], P['filter2']):
            ff = page.locator('.filter-card .ff', has=page.locator('.ff-label', has_text=F['label'])).first
            if F['kind'] == 'select':
                ff.locator('select').select_option(label=F['value'])
            else:
                ff.locator('input').first.fill(F['value'])
            page.locator('.filter-actions button', has_text='查询').click()
            page.wait_for_timeout(80)
            got = page.locator('tbody').first.locator('tr').count()
            check(P['name'], f'4 真过滤 {F["label"]}={F["value"]}', got == F['expect'], f'{got}=={F["expect"]}（全量 {P["n"]}）')
            page.locator('.filter-actions button', has_text='重置').click()
            page.wait_for_timeout(120)

        # 5 重置恢复全量
        got = page.locator('tbody').first.locator('tr').count()
        check(P['name'], '5 重置恢复全量', got == P['n'], f'{got}=={P["n"]}')

        # 6 stab 计数=统计值
        stab_ok, detail = True, []
        for label, want in P['stabs'].items():
            st = page.locator('.stabs .stab', has_text=label).first
            got = int(st.locator('.stab-count').text_content())
            if got != want:
                stab_ok = False
            detail.append(f'{label}:{got}')
        check(P['name'], '6 stab 计数=统计值', stab_ok, ' '.join(detail))

        # 7 ?notes=1 pin 全在
        page2 = browser.new_page()
        page2.goto(P['file'].as_uri() + '?notes=1', wait_until='load')
        page2.wait_for_selector('tbody tr', timeout=5000)
        page2.wait_for_timeout(300)
        notes = page2.locator('[data-note]')
        pin_divs = page2.locator('.proto-pin').count()
        layer_on = page2.evaluate("document.body.classList.contains('proto-notes-on')")
        # 实点第一个 pin 角标（右上角 24x22 热区）
        first = notes.first
        box = first.bounding_box()
        page2.mouse.click(box['x'] + box['width'] - 4, box['y'] + 4)
        page2.wait_for_timeout(120)
        opened = page2.locator('.proto-pin.pn-open').count()
        check(P['name'], '7 ?notes=1 pin 全在',
              notes.count() == P['pins'] and layer_on and opened >= 1,
              f"data-note={notes.count()}/{P['pins']} pin层={'开' if layer_on else '关'} pin弹层={pin_divs} 实点打开={opened}")
        page2.close()

        check(P['name'], '0 JS 错误', len(errs) == 0, str(errs[:2]) if errs else '0')
        page.close()
    browser.close()

fails = [r for r in results if not r[2]]
print('\n==== 试点验证门汇总：', f'断言 {len(results)} 项，失败 {len(fails)} 项', '====')
sys.exit(1 if fails else 0)
