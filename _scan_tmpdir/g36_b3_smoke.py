# -*- coding: utf-8 -*-
"""B3 冒烟：17 新页 + 7 宿主 + C1 复验（确认页勾选）+ 待办 B3 域残留"""
import asyncio, os
from playwright.async_api import async_playwright

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def url(rel):
    return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')

PAGES = ['租赁管理/租赁单详情.html', '租赁管理/租赁单审核.html', '租赁管理/租赁单新建.html',
         '租赁管理/租赁出库详情.html', '租赁管理/租赁出库确认.html', '租赁管理/退租入库详情.html',
         '租赁管理/退租入库审核.html', '租赁管理/退租入库新建.html', '租赁管理/器具出租履历.html?key=WBX-1210L',
         '租入管理/租入单详情.html', '租入管理/租入单审核.html', '租入管理/租入单新建.html',
         '租入管理/租入入库详情.html', '租入管理/租入入库确认.html', '租入管理/租入归还详情.html',
         '租入管理/租入归还审核.html', '租入管理/租入归还新建.html']
HOSTS = ['租赁管理/租赁单列表.html', '租赁管理/租赁出库列表.html', '租赁管理/退租入库列表.html',
         '租入管理/租入单列表.html', '租入管理/租入入库列表.html', '租入管理/租入归还列表.html', '仓储作业/库存查询.html']

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
            await pg.wait_for_timeout(350)
            js0 = not errs; errs.clear()
            segs = await pg.evaluate("() => document.querySelectorAll('.dt-sec').length")
            isform = '新建' in p
            bar = await pg.evaluate("() => !!document.querySelector('.submit-bar') || !!document.querySelector('.card')")
            title = await pg.evaluate("() => (document.getElementById('dtTitle')||{}).textContent || document.title")
            okk = js0 and (segs >= 3 if not isform else bar)
            print('[%s] %-38s JS=%s dt-sec=%d | %s' % ('PASS' if okk else 'FAIL', p.split('/')[-1][:36], js0, segs, (title or '')[:26]))
            if not okk and errs: print('     err:', errs[:2])
            if not okk: fails += 1
            errs.clear()
        # 租入入库确认：立即转租默认勾选
        await pg.goto(url('租入管理/租入入库确认.html'))
        await pg.wait_for_timeout(300)
        chk = await pg.evaluate("() => { var c = document.querySelector('.cb'); return c ? c.checked : null; }")
        print('[%s] 租入入库确认 立即转租勾选=%s' % ('PASS' if chk is True else 'FAIL', chk))
        if chk is not True: fails += 1
        # pins 迁移验证
        for p, exp in [('租赁管理/租赁单新建.html', 2), ('租入管理/租入单新建.html', 1), ('租入管理/租入归还新建.html', 1)]:
            await pg.goto(url(p))
            await pg.wait_for_timeout(300)
            n = await pg.evaluate("() => document.querySelectorAll('#proto-pins .proto-pin').length")
            okk = n >= exp and not errs
            errs.clear()
            print('[%s] %s pins=%d(≥%d)' % ('PASS' if okk else 'FAIL', p.split('/')[-1], n, exp))
            if not okk: fails += 1
        for h in HOSTS:
            await pg.goto(url(h))
            await pg.wait_for_timeout(450)
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
            print('[%s] %-26s rows=%d dangling=%s' % ('PASS' if okk else 'FAIL', h.split('/')[-1], rows, dangling))
            if not okk: fails += 1
        # 待办 B3 域残留
        await pg.goto(url('我的待办.html'))
        await pg.wait_for_timeout(400)
        left = await pg.evaluate("""() => Array.from(document.querySelectorAll('[onclick]')).map(e=>e.getAttribute('onclick')).filter(x => x && x.indexOf('audit=1') > -1 && (x.indexOf('租赁') > -1 || x.indexOf('租入') > -1)).length""")
        print('[%s] 待办 租赁/租入 audit=1 残留 = %d' % ('PASS' if left == 0 else 'FAIL', left))
        if left: fails += 1
        # 库存查询 资产轨迹跳转
        await pg.goto(url('仓储作业/库存查询.html'))
        await pg.wait_for_timeout(400)
        lk = await pg.evaluate("() => (window.openTrack || Function.prototype).toString().indexOf('器具出租履历') > -1")
        print('[%s] 库存查询 openTrack 指向器具出租履历页 = %s' % ('PASS' if lk else 'FAIL', lk))
        if not lk: fails += 1
        await b.close()
    print('B3 冒烟总判定：%s' % ('ALL PASS' if fails == 0 else '%d FAIL' % fails))

asyncio.run(main())
