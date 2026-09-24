import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        await pg.goto(B + '/采购管理/采购订单列表.html')
        await pg.wait_for_timeout(500)
        await pg.screenshot(path='_scan_tmpdir/g64_list.png')
        await b.close()

asyncio.run(main())
