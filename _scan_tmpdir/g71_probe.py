import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        await pg.goto(B + '/仓储作业/库存查询.html')
        await pg.wait_for_timeout(700)
        ops = await pg.evaluate("[...document.querySelectorAll('tbody tr')].map(tr => { const c=tr.querySelector('td.sticky-op'); return c ? c.innerText.replace(/\\n/g,'|') : ''; })")
        print('首5行操作列:')
        for x in ops[:8]:
            print('  ', x)
        allops = await pg.evaluate("[...new Set([...document.querySelectorAll('td.sticky-op a, td.sticky-op .op-dis')].map(a=>a.textContent.trim()))]")
        print('全表操作项去重:', allops)
        await b.close()

asyncio.run(main())
