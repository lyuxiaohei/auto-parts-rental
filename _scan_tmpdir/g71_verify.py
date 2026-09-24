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
        await pg.goto(B + '/仓储作业/库存查询.html')
        await pg.wait_for_timeout(700)
        body = await pg.evaluate('document.body.innerText')
        out.append('%s 页面无「终止转移」: %s' % ('PASS' if '终止转移' not in body else 'FAIL', '终止转移' not in body))
        ffs = await pg.evaluate("[...document.querySelectorAll('.ff-label')].map(x=>x.innerText.trim())")
        out.append('%s 筛选标签: %s' % ('PASS' if '库位：' in ffs and '库房：' not in ffs else 'FAIL', ffs))
        ops = await pg.evaluate("[...document.querySelectorAll('td.sticky-op')].map(c=>c.innerText.replace(/\\n/g,'|').trim()).slice(0,6)")
        out.append('前6行操作: %s' % ops)
        try:
            n1 = await pg.evaluate("document.querySelectorAll('tbody tr').length")
            opts = await pg.evaluate("(() => { const ff=[...document.querySelectorAll('.ff')].find(x=>x.innerText.indexOf('库位：')>-1); const s=ff.querySelector('select'); s.value='RA-A-01-01'; return [...s.options].map(o=>o.value).includes('RA-A-01-01'); })()")
            await pg.locator('.filter-actions button', has_text='查询').click()
            await pg.wait_for_timeout(400)
            n2 = await pg.evaluate("document.querySelectorAll('tbody tr').length")
            rowtxt = await pg.evaluate("[...document.querySelectorAll('tbody tr')].map(r=>r.innerText.replace(/\\n/g,' ').slice(0,50)).slice(0,2)")
            out.append('%s 库位筛选(选项有RA-A-01-01=%s): 前=%d 后=%d 样例=%s' % ('PASS' if opts and 0 < n2 <= n1 else 'FAIL', opts, n1, n2, rowtxt))
        except Exception as e:
            out.append('库位筛选测试异常: %s' % e)
        out.append('JS 错: %s %s' % (len(errs), errs[:3]))
        await pg.goto(B + '/仓储作业/库存查询.html'); await pg.wait_for_timeout(500)
        await pg.screenshot(path='_scan_tmpdir/g71_stock_query.png')
        await b.close()
    print('\n'.join(out))

asyncio.run(main())
