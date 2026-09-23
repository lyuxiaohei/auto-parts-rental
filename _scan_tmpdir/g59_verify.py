import asyncio, json
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    r = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)

        # ① 4 出库列表：批量导入按钮 → 弹窗开 → 遮罩点击关 → 导出按钮存在
        for p in ['销售管理/销售出库列表', '租赁管理/租赁出库列表', '仓储作业/其他出库列表', '租入管理/归还出库列表']:
            await pg.goto(B + '/' + p + '.html')
            btn = pg.locator('button:has-text("批量导入")')
            ok1 = await btn.count() == 1
            await btn.click()
            await pg.wait_for_timeout(200)
            vis = await pg.evaluate("document.getElementById('importModal').classList.contains('show')")
            title = await pg.evaluate("(document.querySelector('#importModal .modal-title')||{}).textContent")
            await pg.evaluate("document.getElementById('importModal').click()")
            await pg.wait_for_timeout(150)
            closed = await pg.evaluate("!document.getElementById('importModal').classList.contains('show')")
            exp = await pg.locator('button:has-text("导出")').count()
            r.append(f"{p.split('/')[-1]}: 按钮{ok1}·弹窗开{vis}·标题[{title}]·遮罩关{closed}·导出钮{exp}")

        # ② 销售退货新建：库位列+SSEL 填充+添加行联动
        await pg.goto(B + '/销售管理/销售退货新建.html')
        th = await pg.evaluate("[...document.querySelector('#retItems').closest('table').querySelectorAll('th')].map(x=>x.textContent)")
        opts = await pg.evaluate("document.querySelectorAll('select.retLoc')[0]?.options.length")
        optv = await pg.evaluate("document.querySelectorAll('select.retLoc')[0]?.options[0]?.textContent")
        await pg.locator('button:has-text("添加")').click()
        await pg.wait_for_timeout(300)
        rows = await pg.evaluate("document.querySelectorAll('#retItems tr').length")
        opts2 = await pg.evaluate("document.querySelectorAll('select.retLoc').length")
        hint = await pg.evaluate("document.querySelector('.pn-hint')?.textContent")
        r.append(f"销售退货新建: 表头{th}·首行库位选项{opts}[{optv}]·添加后行{rows}·库位select总数{opts2}")
        r.append(f"pn-hint: {hint}")

        # ③ 截图
        await pg.goto(B + '/仓储作业/其他出库列表.html')
        await pg.locator('button:has-text("批量导入")').click()
        await pg.wait_for_timeout(250)
        await pg.screenshot(path='_scan_tmpdir/g59_import_modal.png')
        await pg.goto(B + '/销售管理/销售退货新建.html')
        await pg.wait_for_timeout(300)
        await pg.screenshot(path='_scan_tmpdir/g59_ret_loc.png', full_page=True)

        r.append(f"JS错: {len(errs)} {errs[:3]}")
        await b.close()
    print('\n'.join(r))

asyncio.run(main())
