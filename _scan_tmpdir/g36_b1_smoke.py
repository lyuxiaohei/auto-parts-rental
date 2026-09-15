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
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pages = ['基础数据/物料新建.html', '基础数据/客商新建.html', '基础数据/库位新建.html',
                 '基础数据/客商开票资料.html', '基础数据/客商收货信息.html', '基础数据/物料详情.html',
                 '基础数据/客商详情.html?id=DW-0002', '基础数据/库位详情.html', '基础数据/BOM版本查看.html',
                 '项目管理/上下游绑定.html', '项目管理/项目新建.html', '项目管理/编码规则.html']
        for p in pages:
            await pg.goto(url(p))
            await pg.wait_for_timeout(400)
            print('%-42s JS errors: %s' % (p, errs if errs else 0))
            errs.clear()
        # spot assertions
        await pg.goto(url('基础数据/物料新建.html'))
        await pg.wait_for_timeout(400)
        n = await pg.eval_on_selector_all('#taxEditRows .tax-edit-row', 'els=>els.length')
        w = await pg.eval_on_selector('.form-row .input-box', 'el=>el.getBoundingClientRect().width')
        opt = await pg.eval_on_selector('#wlTypeSel', 'el=>el.options.length')
        print('物料新建: tax rows =', n, '| first input-box width =', round(w), '| 物料类型 options =', opt)
        await pg.goto(url('基础数据/客商详情.html?id=DW-0002'))
        await pg.wait_for_timeout(400)
        t = await pg.eval_on_selector('#dtTitle', 'el=>el.textContent')
        seg = await pg.eval_on_selector_all('#detailBody .dt-sec', 'els=>els.length')
        print('客商详情: title =', t, '| dt-sec =', seg)
        await pg.goto(url('基础数据/BOM版本查看.html'))
        await pg.wait_for_timeout(400)
        t2 = await pg.eval_on_selector('#dtTitle', 'el=>el.textContent')
        print('BOM版本查看: title =', t2)
        await pg.goto(url('项目管理/上下游绑定.html'))
        await pg.wait_for_timeout(400)
        sp = await pg.eval_on_selector_all('#bindSups label', 'els=>els.length')
        pr = await pg.eval_on_selector('#bindPrj', 'el=>el.options.length')
        print('上下游绑定: 供应商 checkbox =', sp, '| 项目 options =', pr)
        await b.close()

asyncio.run(main())
