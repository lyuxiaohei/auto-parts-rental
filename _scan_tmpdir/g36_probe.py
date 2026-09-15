# -*- coding: utf-8 -*-
import asyncio, os
from playwright.async_api import async_playwright
BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
def url(rel): return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(url('租入管理/租入单列表.html'))
        await pg.wait_for_timeout(600)
        row = pg.locator('tbody tr', has_text='RZD-20260902-008').first
        print('row count:', await pg.locator('tbody tr', has_text='RZD-20260902-008').count())
        await row.locator('.ops a', has_text='详情').click()
        await pg.wait_for_timeout(400)
        shown = await pg.eval_on_selector_all('.modal-overlay.show', 'els=>els.map(e=>e.id)')
        print('shown modals:', shown, '| JS:', errs)
        body = await pg.evaluate("""() => {
            var m = document.querySelector('.modal-overlay.show');
            if (!m) return 'NO MODAL';
            var c = m.querySelector('.chain');
            return c ? c.textContent : 'NO CHAIN; body=' + m.querySelector('.modal-body').textContent.slice(0, 200);
        }""")
        print('chain:', body)
        lks = await pg.eval_on_selector_all('.modal-overlay.show .chain .lk', 'els=>els.map(e=>e.textContent)')
        print('chain links:', lks)
        await b.close()
asyncio.run(main())
