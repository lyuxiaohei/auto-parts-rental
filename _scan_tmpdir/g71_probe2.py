import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        await pg.goto(B + '/仓储作业/库存查询.html')
        await pg.wait_for_timeout(700)
        r = await pg.evaluate("(() => { const t=document.body.innerText; const i=t.indexOf('终止转移'); const n=t.split('终止转移').length-1; return { n, ctx: i>-1 ? t.slice(Math.max(0,i-70), i+50) : '' }; })()")
        print('innerText 次数=%s' % r['n'])
        print('上下文:', r['ctx'])
        # 是否在卡片/表格区（非抽屉）
        inCard = await pg.evaluate("[...document.querySelectorAll('.card')].map(c=>c.innerText).join('').indexOf('终止转移')>-1")
        inDrawer = await pg.evaluate("(document.querySelector('#pnDrawer, .pn-drawer, #notesDrawer')||{}).innerText ? true : document.body.innerText.indexOf('终止转移')>-1")
        print('卡片区含终止转移:', inCard)
        await b.close()

asyncio.run(main())
