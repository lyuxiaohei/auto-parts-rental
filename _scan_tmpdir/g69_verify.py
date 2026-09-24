import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    out = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console: ' + m.text) if m.type == 'error' else None)

        async def ths(url):
            await pg.goto(B + url)
            await pg.wait_for_timeout(450)
            return await pg.evaluate("[...document.querySelectorAll('thead th')].map(t=>t.innerText.trim())")

        t = await ths('/采购管理/采购退货单列表.html')
        out.append('%s 采购退货列表: %s' % ('PASS' if '物料名称' in t and '物料' not in t else 'FAIL', t))
        t = await ths('/销售管理/销售退货单列表.html')
        out.append('%s 销售退货列表: %s' % ('PASS' if '物料名称' in t and '物料' not in t else 'FAIL', t))
        t = await ths('/租赁管理/租赁单列表.html')
        out.append('%s 租赁单列表: %s' % ('PASS' if '物料名称' in t and '物料' not in t else 'FAIL', t))
        t = await ths('/租入管理/租入单列表.html')
        out.append('%s 租入单列表: %s' % ('PASS' if '物料名称' in t and '物料' not in t else 'FAIL', t))
        ff = await pg.evaluate("[...document.querySelectorAll('.ff-label')].map(x=>x.innerText.trim())")
        out.append('%s 租入单筛选标签: %s' % ('PASS' if '物料名称：' in ff else 'FAIL', ff))
        t = await ths('/仓储作业/收发存.html')
        out.append('%s 库存台账(收发存): %s' % ('PASS' if '物料名称' in t and '物料' not in t else 'FAIL', t))
        ff = await pg.evaluate("[...document.querySelectorAll('.ff-label')].map(x=>x.innerText.trim())")
        out.append('%s 收发存筛选标签: %s' % ('PASS' if '物料名称：' in ff else 'FAIL', ff))

        # 盘点录入
        await pg.goto(B + '/仓储作业/盘点录入.html')
        await pg.wait_for_timeout(450)
        t = await pg.evaluate("[...document.querySelectorAll('thead th')].map(x=>x.innerText.trim())")
        out.append('%s 盘点录入表头: %s' % ('PASS' if '物料编码' in t and '物料名称' in t and '编码' not in t and '名称' not in t else 'FAIL', t))
        ops = await pg.evaluate("[...document.querySelectorAll('tbody tr')].map(tr => { const last = tr.querySelector('td.sticky-op'); return last ? last.innerText.trim() : ''; })")
        out.append('%s 盘点行操作: %s' % ('PASS' if '生成其他入库' in ops and '生成其他出库' in ops else 'FAIL', ops))
        # 点击盘盈行 生成其他入库 → 应跳 其他入库列表.html?create=1
        idx = ops.index('生成其他入库')
        await pg.locator('tbody tr').nth(idx).locator('a', has_text='生成其他入库').click()
        await pg.wait_for_timeout(500)
        out.append('%s 盘盈跳转: %s' % ('PASS' if 'create=1&item=ZH-260' in pg.url else 'FAIL', pg.url.split('/')[-1][:100]))
        out.append('JS 错: %s %s' % (len(errs), errs[:3]))
        await pg.goto(B + '/仓储作业/盘点录入.html'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='_scan_tmpdir/g69_inventory.png')
        await pg.goto(B + '/租赁管理/租赁单列表.html'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='_scan_tmpdir/g69_lease_list.png')
        await b.close()
    print('\n'.join(out))

asyncio.run(main())
