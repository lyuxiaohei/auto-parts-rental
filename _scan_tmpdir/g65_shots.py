import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})

        # ① 列表页（物料档案）
        await pg.goto(B + '/基础数据/产品档案.html')
        await pg.wait_for_timeout(500)
        await pg.screenshot(path='_scan_tmpdir/g65_1_列表-物料档案.png')

        # ② 新建页（点右上「新建」）
        await pg.locator('.head-btns button', has_text='新建').click()
        await pg.wait_for_timeout(600)
        await pg.screenshot(path='_scan_tmpdir/g65_2_新建物料.png')

        # ③ 详情页（列表点行内「详情」）
        await pg.goto(B + '/基础数据/产品档案.html')
        await pg.wait_for_timeout(500)
        await pg.locator('table tbody tr').first.locator('.ops a', has_text='详情').click()
        await pg.wait_for_timeout(600)
        await pg.screenshot(path='_scan_tmpdir/g65_3_物料详情.png')

        # ④ 编辑（列表点行内「编辑」→看打开的是什么页）
        await pg.goto(B + '/基础数据/产品档案.html')
        await pg.wait_for_timeout(500)
        await pg.locator('table tbody tr').first.locator('.ops a', has_text='编辑').click()
        await pg.wait_for_timeout(600)
        url = pg.url
        tab = await pg.locator('.tabs .tab.active').inner_text()
        vals = await pg.evaluate("[...document.querySelectorAll('.card input')].slice(0,6).map(i=>i.value)")
        await pg.screenshot(path='_scan_tmpdir/g65_4_编辑-打开的是新建页.png')
        print('编辑跳转URL:', url.split('/')[-1])
        print('当前页签:', tab)
        print('表单前几个值:', vals)

        await b.close()

asyncio.run(main())
