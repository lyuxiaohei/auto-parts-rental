import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(B + '/仓储作业/库存流水.html?id=XNC-AJZX-WBX')
        await pg.wait_for_timeout(500)
        body = await pg.evaluate('document.body.innerText')
        print('库存流水: 物料类型=%s 客户端（租出）=%s 物料类别=%s on-hire=%s' % ('物料类型' in body, '客户端（租出）' in body, '物料类别' in body, 'on-hire' in body))
        await pg.goto(B + '/租入管理/租入单详情.html?id=RZD-20260910-009')
        await pg.wait_for_timeout(500)
        body = await pg.evaluate('document.body.innerText')
        print('租入单详情: 租金行=%s' % ('租金' in body))
        idx = body.find('月租')
        print('月租上下文:', repr(body[max(0, idx - 30):idx + 30]) if idx > -1 else '无')
        print('JS错:', len(errs), errs[:2])
        await b.close()

asyncio.run(main())
