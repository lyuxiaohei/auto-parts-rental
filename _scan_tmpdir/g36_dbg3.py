# -*- coding: utf-8 -*-
import asyncio, os
from playwright.async_api import async_playwright
BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
def url(rel): return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append('PAGE:' + str(e)))
        await pg.goto(url('仓储作业/库存查询.html'))
        await pg.wait_for_timeout(700)
        main = await pg.evaluate("""() => {
            var main = null;
            document.querySelectorAll('table').forEach(function (t) {
                var th = t.querySelector('thead');
                if (th && th.textContent.indexOf('适用项目') > -1 && th.textContent.indexOf('总量') > -1) main = t;
            });
            if (!main) return 'NOT FOUND';
            var ths = Array.prototype.map.call(main.querySelectorAll('thead th'), function (th) { return th.textContent.trim(); });
            var rows = Array.prototype.map.call(main.querySelector('tbody').rows, function (tr) {
                return Array.prototype.map.call(tr.cells, function (c) { return c.textContent.trim(); });
            });
            return {ths: ths, nrows: rows.length, first: rows[0], third: rows[2]};
        }""")
        print('main table:', main)
        print('JS:', errs if errs else 0)
        # 设置项目并点查询
        await pg.evaluate("""() => {
            document.querySelectorAll('.ff').forEach(function (f) {
                var lb = f.querySelector('.ff-label');
                if (lb && lb.textContent.indexOf('项目') === 0) {
                    var sel = f.querySelector('select');
                    if (sel) { sel.value = 'PRJ-2601'; sel.dispatchEvent(new Event('change', {bubbles: true})); }
                }
            });
        }""")
        await pg.click('button:has-text("查询")')
        await pg.wait_for_timeout(400)
        n = await pg.evaluate("""() => {
            var main = null;
            document.querySelectorAll('table').forEach(function (t) {
                var th = t.querySelector('thead');
                if (th && th.textContent.indexOf('适用项目') > -1 && th.textContent.indexOf('总量') > -1) main = t;
            });
            var rows = Array.prototype.map.call(main.querySelector('tbody').rows, function (tr) {
                return Array.prototype.map.call(tr.cells, function (c) { return c.textContent.trim(); }).slice(0, 9);
            });
            return rows;
        }""")
        print('after PRJ-2601 + 查询: rows=%d' % len(n))
        for r in n:
            print('  ', r)
        await b.close()
asyncio.run(main())
