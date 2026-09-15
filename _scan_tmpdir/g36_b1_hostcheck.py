# -*- coding: utf-8 -*-
import asyncio, os
from playwright.async_api import async_playwright

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def url(rel):
    return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        for p in ['基础数据/产品档案.html', '基础数据/客商管理.html', '基础数据/库位档案.html', '基础数据/BOM维护.html', '项目管理/项目档案.html', '项目管理/项目详情.html']:
            await pg.goto(url(p))
            await pg.wait_for_timeout(500)
            rows = await pg.eval_on_selector_all('tbody tr', 'els=>els.length')
            dangling = await pg.evaluate("""() => {
                var bad = [];
                document.querySelectorAll("a[onclick*='openModal']").forEach(function (e) {
                    var oc = e.getAttribute('onclick') || '';
                    var rest = oc.split("openModal('")[1];
                    if (rest) {
                        var id = rest.split("'")[0];
                        if (!document.getElementById(id)) bad.push(id);
                    }
                });
                return bad;
            }""")
            print('%-24s rows=%-3d dangling-openModal=%s JS=%s' % (p.split('/')[-1], rows, dangling if dangling else 0, errs if errs else 0))
            errs.clear()
        await pg.goto(url('基础数据/产品档案.html')); await pg.wait_for_timeout(500)
        a1 = await pg.eval_on_selector('tbody tr:first-child .ops a:first-child', 'el=>el.getAttribute("onclick")')
        a2 = await pg.eval_on_selector('tbody tr:first-child .ops a:nth-child(2)', 'el=>el.getAttribute("onclick")')
        print('产品档案 运行时 ops[0]/[1]:', a1, '|', a2)
        await pg.goto(url('基础数据/客商管理.html')); await pg.wait_for_timeout(500)
        acts = await pg.eval_on_selector_all('tbody tr:first-child .ops a', 'els=>els.map(e=>e.getAttribute("onclick"))')
        print('客商管理 运行时 ops:', acts)
        await pg.goto(url('基础数据/库位档案.html')); await pg.wait_for_timeout(500)
        acts = await pg.eval_on_selector_all('tbody tr:first-child .ops a', 'els=>els.map(e=>e.getAttribute("onclick"))')
        print('库位档案 运行时 ops:', acts)
        await b.close()

asyncio.run(main())
