import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        for url, sel in [
            ('/租赁管理/租赁单新建.html', 'tbody tr'),
            ('/租入管理/租入单新建.html', 'tbody tr'),
            ('/仓储作业/收发存.html', 'tbody tr'),
            ('/仓储作业/盘点录入.html', 'tbody tr'),
        ]:
            await pg.goto(B + url)
            await pg.wait_for_timeout(500)
            rows = await pg.evaluate("(() => { const tr = document.querySelector('tbody tr'); if (!tr) return null; return [...tr.querySelectorAll('td')].map(td => (td.innerText || '').trim().slice(0, 40)); })()")
            ths = await pg.evaluate("[...document.querySelectorAll('thead th')].map(t => t.innerText.trim())")
            print('=====', url)
            print('  THS:', ths)
            print('  ROW1:', rows)
        await b.close()

asyncio.run(main())
