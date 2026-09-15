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
        pg.on('console', lambda m: errs.append('CONSOLE:' + m.text) if m.type == 'error' else None)
        await pg.goto(url('仓储作业/库存查询.html'))
        await pg.wait_for_timeout(700)
        print('JS errors:', errs if errs else 0); errs.clear()
        info = await pg.evaluate("""() => {
            var tables = [];
            document.querySelectorAll('table').forEach(function (t) {
                var th = t.querySelector('thead');
                tables.push({head: th ? th.textContent.slice(0, 40) : '', rows: t.querySelectorAll('tbody tr').length,
                             hasApply: th ? th.textContent.indexOf('适用项目') > -1 : false,
                             hasTotal: th ? th.textContent.indexOf('总量') > -1 : false});
            });
            var ffs = [];
            document.querySelectorAll('.ff').forEach(function (f) {
                var lb = f.querySelector('.ff-label');
                ffs.push({label: lb ? lb.textContent : '', hasSel: !!f.querySelector('select'),
                          selVal: f.querySelector('select') ? f.querySelector('select').value : null});
            });
            return {tables: tables, ffs: ffs};
        }""")
        for t in info['tables']:
            print('TABLE rows=%d apply=%s total=%s | %s' % (t['rows'], t['hasApply'], t['hasTotal'], t['head']))
        for f in info['ffs']:
            print('FF', f)
        # 点查询按钮实验
        btn = await pg.evaluate("""() => {
            var btns = [];
            document.querySelectorAll('button').forEach(function (b) { btns.push(b.textContent.trim()); });
            return btns;
        }""")
        print('buttons:', btn)
        await b.close()
asyncio.run(main())
