# -*- coding: utf-8 -*-
"""B4 冒烟：12 新页 + 5 宿主 + 待办 B4 域残留 + C2 回归"""
import asyncio, os, re
from playwright.async_api import async_playwright

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def url(rel):
    return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')

def num(t):
    d = re.findall(r'[\d,]+', t or '')
    return int(d[0].replace(',', '')) if d else 0

PAGES = ['仓储作业/其他入库详情.html', '仓储作业/其他入库审核.html', '仓储作业/其他入库新建.html',
         '仓储作业/其他出库详情.html', '仓储作业/其他出库审核.html', '仓储作业/其他出库新建.html',
         '仓储作业/库存流水.html', '仓储作业/盘点详情.html', '仓储作业/盘点审核.html',
         '仓储作业/调拨详情.html', '仓储作业/调拨审核.html', '仓储作业/调拨新建.html']
HOSTS = ['仓储作业/其他入库列表.html', '仓储作业/其他出库列表.html', '仓储作业/盘点列表.html', '仓储作业/库存调拨列表.html', '仓储作业/库存查询.html']

async def main():
    fails = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        for p in PAGES:
            await pg.goto(url(p))
            await pg.wait_for_timeout(320)
            js0 = not errs; errs.clear()
            isform = '新建' in p
            segs = await pg.evaluate("() => document.querySelectorAll('.dt-sec').length")
            bar = await pg.evaluate("() => !!document.querySelector('.submit-bar') || !!document.querySelector('.card')")
            okk = js0 and (segs >= 3 if not isform else bar)
            print('[%s] %-30s JS=%s %s' % ('PASS' if okk else 'FAIL', p.split('/')[-1], js0, ('dt-sec=%d' % segs) if not isform else ''))
            if not okk: fails += 1
            if errs: print('    err:', errs[:2]); errs.clear()
        for h in HOSTS:
            await pg.goto(url(h))
            await pg.wait_for_timeout(420)
            rows = await pg.eval_on_selector_all('tbody tr', 'els=>els.length')
            dangling = await pg.evaluate("""() => {
                var bad = [];
                document.querySelectorAll("a[onclick*='openModal']").forEach(function (e) {
                    var rest = (e.getAttribute('onclick') || '').split("openModal('")[1];
                    if (rest) { var id = rest.split("'")[0]; if (!document.getElementById(id)) bad.push(id); }
                });
                return bad;
            }""")
            okk = (not errs) and not dangling and rows > 0
            errs.clear()
            print('[%s] %-24s rows=%d dangling=%s' % ('PASS' if okk else 'FAIL', h.split('/')[-1], rows, dangling))
            if not okk: fails += 1
        # 待办 B4 域
        await pg.goto(url('我的待办.html'))
        await pg.wait_for_timeout(400)
        left = await pg.evaluate("() => Array.from(document.querySelectorAll('[onclick]')).map(e=>e.getAttribute('onclick')).filter(x => x && x.indexOf('audit=1') > -1 && x.indexOf('仓储') > -1).length")
        print('[%s] 待办 仓储 audit=1 残留 = %d' % ('PASS' if left == 0 else 'FAIL', left))
        if left: fails += 1
        # C2 回归：库存查询 flowModal 删除后项目闭环仍工作
        await pg.goto(url('仓储作业/库存查询.html'))
        await pg.wait_for_timeout(500)
        rows = await pg.evaluate("""() => {
            var main = null;
            document.querySelectorAll('table').forEach(function (t) {
                var th = t.querySelector('thead');
                if (th && th.textContent.indexOf('适用项目') > -1 && th.textContent.indexOf('总量') > -1) main = t;
            });
            return main ? main.querySelector('tbody').rows.length : -1;
        }""")
        lk = await pg.evaluate("() => { var a = document.querySelector('tbody tr .ops a'); return a ? a.getAttribute('onclick') : ''; }")
        print('[%s] C2 回归: 主表 %d 行；首操作=%s' % ('PASS' if rows == 14 and lk and '库存流水' in lk else 'FAIL', rows, lk))
        if not (rows == 14 and lk and '库存流水' in lk): fails += 1
        await b.close()
    print('B4 冒烟总判定：%s' % ('ALL PASS' if fails == 0 else '%d FAIL' % fails))

asyncio.run(main())
