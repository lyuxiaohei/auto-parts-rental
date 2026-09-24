import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        await pg.goto(B + '/仓储作业/盘点录入.html')
        await pg.wait_for_timeout(500)
        lab = await pg.evaluate("[...document.querySelectorAll('.form-label')].map(x=>x.innerText.trim())")
        print('录入字段名含盘点库位:', any('盘点库位' in x for x in lab), '| 含盘点范围:', any('盘点范围' in x for x in lab))
        await pg.goto(B + '/仓储作业/盘点列表.html')
        await pg.wait_for_timeout(600)
        cells = await pg.evaluate("(() => { const tr = document.querySelector('tbody tr'); return tr ? [...tr.querySelectorAll('td')].map(td => td.innerText.trim()).slice(0,4) : null; })()")
        print('列表首行前四格:', cells)
        await b.close()

asyncio.run(main())
