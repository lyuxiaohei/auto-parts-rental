# -*- coding: utf-8 -*-
"""C1 回归（页面化后口径）：三页互见＋确认页勾选＋链接跳转"""
import asyncio, os
from urllib.parse import unquote
from playwright.async_api import async_playwright

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def url(rel):
    return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')

async def main():
    ok = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(url('租入管理/租入单详情.html?id=RZD-20260902-008'))
        await pg.wait_for_timeout(400)
        t = await pg.eval_on_selector('#detailBody', 'el=>el.textContent')
        ok.append(('C1-1 租入单详情链含 RZRK+CK', ('RZRK-20260903-023' in t) and ('CK-20260914-023' in t), ''))
        lk = pg.locator('#detailBody .chain .lk', has_text='CK-20260914-023').first
        async with pg.expect_navigation():
            await lk.click()
        u = unquote(await pg.evaluate('()=>location.pathname'))
        ok.append(('C1-2 链路点击跳租赁出库列表', '租赁出库列表' in u, u.split('/')[-1]))
        await pg.goto(url('租赁管理/租赁出库详情.html?id=CK-20260914-023'))
        await pg.wait_for_timeout(400)
        t2 = await pg.eval_on_selector('#detailBody', 'el=>el.textContent')
        ok.append(('C1-3 CK详情回链 RZRK+RZD', ('RZRK-20260903-023' in t2) and ('RZD-20260902-008' in t2), ''))
        await pg.goto(url('租入管理/租入入库详情.html?id=RZRK-20260903-023'))
        await pg.wait_for_timeout(400)
        t3 = await pg.eval_on_selector('#detailBody', 'el=>el.textContent')
        ok.append(('C1-4 租入入库详情链含 RZD+CK', ('RZD-20260902-008' in t3) and ('CK-20260914-023' in t3), ''))
        await pg.goto(url('租入管理/租入入库确认.html?id=RZRK-20260903-023'))
        await pg.wait_for_timeout(400)
        chk = await pg.evaluate("() => { var c = document.querySelector('input.cb'); return c ? c.checked : null; }")
        ok.append(('C1-5 确认页立即转租默认勾选', chk is True, str(chk)))
        ok.append(('C1 全程 JS 0', not errs, '; '.join(errs[:2])))
        await b.close()
    fails = 0
    for name, p, ev in ok:
        print('[%s] %s %s' % ('PASS' if p else 'FAIL', name, ev))
        if not p: fails += 1
    print('C1 回归：%d PASS / %d FAIL' % (len(ok) - fails, fails))

asyncio.run(main())
