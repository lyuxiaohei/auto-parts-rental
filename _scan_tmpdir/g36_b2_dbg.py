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
        pg.on('pageerror', lambda e: errs.append('PAGE:' + str(e)))
        pg.on('console', lambda m: errs.append('CON:' + m.text) if m.type == 'error' else None)
        await pg.goto(url('采购管理/采购订单详情.html'))
        await pg.wait_for_timeout(500)
        for e in errs[:6]:
            print(e[:220])
        t = await pg.eval_on_selector('#dtTitle', 'el=>el.textContent') if await pg.eval_on_selector_all('#dtTitle', 'els=>els.length') else '?'
        print('title:', t)
        await pg.goto(url('我的待办.html'))
        await pg.wait_for_timeout(400)
        left = await pg.evaluate("""() => Array.from(document.querySelectorAll('[onclick]')).map(e=>e.getAttribute('onclick')).filter(x => x && x.indexOf('audit=1') > -1)""")
        print('待办 audit=1 全部残留 onclick:', left)
        await b.close()
asyncio.run(main())
