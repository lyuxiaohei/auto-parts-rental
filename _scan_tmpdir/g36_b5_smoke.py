# -*- coding: utf-8 -*-
"""B5 冒烟：18 新页 + 11 宿主 + 权限配置参数化 + 待办终态"""
import asyncio, os
from playwright.async_api import async_playwright

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def url(rel):
    return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')

PAGES = ['财务协同/付款新建.html', '财务协同/付款详情.html', '财务协同/付款确认.html',
         '财务协同/回款详情.html', '财务协同/应付新建.html', '财务协同/应付详情.html?id=AP-20260905-013',
         '财务协同/应收生成.html', '财务协同/应收详情.html', '财务协同/开票新建.html',
         '财务协同/开票详情.html', '财务协同/收款新建.html', '财务协同/水单核销详情.html',
         '财务协同/退款新建.html', '财务协同/退款详情.html',
         '系统管理/字典项新建.html', '系统管理/用户新建.html', '系统管理/角色新建.html',
         '系统管理/权限配置.html?role=财务主管']
HOSTS = ['财务协同/付款登记.html', '财务协同/回款登记.html', '财务协同/应付账单.html', '财务协同/应收账单.html',
         '财务协同/开票登记.html', '财务协同/银行水单核销.html', '财务协同/退款登记.html',
         '系统管理/数据字典.html', '系统管理/用户权限.html', '系统管理/角色管理.html']

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
            isform = ('新建' in p) or ('生成' in p)
            segs = await pg.evaluate("() => document.querySelectorAll('.dt-sec').length")
            drows = await pg.evaluate("() => document.querySelectorAll('.drow').length + document.querySelectorAll('.dgrid .drow').length")
            bar = await pg.evaluate("() => !!document.querySelector('.submit-bar') || !!document.querySelector('.card')")
            okk = js0 and ((segs >= 3 or drows >= 6) if not isform else bar)
            print('[%s] %-30s JS=%s %s' % ('PASS' if okk else 'FAIL', p.split('/')[-1].split('?')[0], js0, ('dt-sec=%d drow=%d' % (segs, drows)) if not isform else ''))
            if not okk and errs:
                print('    err:', errs[:2]); errs.clear()
            if not okk: fails += 1
            errs.clear()
        # 权限配置参数化：?role=财务主管
        await pg.goto(url('系统管理/权限配置.html?role=财务主管'))
        await pg.wait_for_timeout(350)
        t = await pg.evaluate("() => (document.getElementById('rolePermTitle')||{}).textContent || ''")
        ck = await pg.evaluate("() => { var c = document.querySelector('.checkbox.checked'); return c ? c.getAttribute('data-perm') : null; }")
        print('[%s] 权限配置 ?role=财务主管 → %s（首勾选=%s）' % ('PASS' if '财务主管' in (t or '') else 'FAIL', t, ck))
        if '财务主管' not in (t or ''): fails += 1
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
            print('[%s] %-22s rows=%d dangling=%s' % ('PASS' if okk else 'FAIL', h.split('/')[-1], rows, dangling))
            if not okk: fails += 1
        # 待办终态：全站仅剩 回款/退款 audit=1（其审核弹窗保留）
        await pg.goto(url('我的待办.html'))
        await pg.wait_for_timeout(400)
        left = await pg.evaluate("() => Array.from(document.querySelectorAll('[onclick]')).map(e=>e.getAttribute('onclick')).filter(x => x && x.indexOf('audit=1') > -1)")
        want = ["go('财务协同/回款登记.html?audit=1')", "go('财务协同/退款登记.html?audit=1')"]
        okleft = sorted(left) == sorted(want)
        print('[%s] 待办 audit=1 终态 = %s' % ('PASS' if okleft else 'FAIL', left))
        if not okleft: fails += 1
        await b.close()
    print('B5 冒烟总判定：%s' % ('ALL PASS' if fails == 0 else '%d FAIL' % fails))

asyncio.run(main())
