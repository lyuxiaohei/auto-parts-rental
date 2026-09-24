import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        await pg.goto(B + '/基础数据/客商新建.html')
        await pg.wait_for_timeout(600)
        r = await pg.evaluate("(() => { const t = document.body.innerText; const i = t.indexOf('协议税点'); const n = t.split('协议税点').length - 1; return {i, n, ctx: i > -1 ? t.slice(Math.max(0, i - 60), i + 40) : ''}; })()")
        print('innerText 次数=%s 上下文=%r' % (r['n'], r['ctx']))
        html = await pg.evaluate('document.documentElement.outerHTML')
        print('outerHTML 次数:', html.split('协议税点').length - 1)
        idx = html.find('协议税点')
        while idx > -1:
            print('HTML ctx:', html[max(0, idx - 70):idx + 30].replace('\n', '|'))
            idx = html.find('协议税点', idx + 1)
        await b.close()

asyncio.run(main())
