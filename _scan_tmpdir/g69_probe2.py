import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        for url in ['/租赁管理/租赁单新建.html', '/租入管理/租入单新建.html']:
            await pg.goto(B + url)
            await pg.wait_for_timeout(450)
            info = await pg.evaluate("(() => { const s = document.querySelector('tbody tr select'); return s ? [...s.options].slice(0,3).map(o=>o.textContent) : null; })()")
            ths = await pg.evaluate("[...document.querySelectorAll('thead th')].map(t=>t.innerText.trim())")
            print('=====', url)
            print('  THS:', ths)
            print('  首列选项:', info)
            # 第二列内容（租赁单新建 auto-cell）
            cell2 = await pg.evaluate("(() => { const tds=[...document.querySelectorAll('tbody tr td')]; return tds.slice(0,3).map(td=>td.innerHTML.slice(0,80)); })()")
            print('  前3td innerHTML:', cell2)
        await b.close()

asyncio.run(main())
