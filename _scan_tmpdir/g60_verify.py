import asyncio
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    out = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))

        # ① 详情页（华骏 DW-0001）：多组 sec 渲染
        await pg.goto(B + '/基础数据/客商详情.html?id=DW-0001')
        await pg.wait_for_timeout(400)
        secs = await pg.evaluate("[...document.querySelectorAll('.dgrid,.form-sec,section,h4,[class*=sec]')].length")
        txt = await pg.evaluate("document.body.innerText")
        for kw in ['开票资料 ①（默认）', '开票资料 ②', '沈阳分公司', '收货信息 ①（默认）', '收货信息 ②', '2 号收货口（冲压车间）']:
            out.append(f"详情含[{kw}]: {kw in txt}")
        # 东海：单组开票+双地址
        await pg.goto(B + '/基础数据/客商详情.html?id=DW-0002')
        await pg.wait_for_timeout(400)
        txt2 = await pg.evaluate("document.body.innerText")
        out.append(f"东海含[开票资料 ①（默认）]: {'开票资料 ①（默认）' in txt2}")
        out.append(f"东海含[收货信息 ②·梅山码头]: {'梅山码头' in txt2}")

        # ② 新建页：添加组/标号/删除联动
        await pg.goto(B + '/基础数据/客商新建.html')
        await pg.wait_for_timeout(400)
        out.append(f"初始: 开票组{await pg.evaluate("document.querySelectorAll('.ks-inv-group').length")} 地址组{await pg.evaluate("document.querySelectorAll('.ks-addr-group').length")}")
        await pg.evaluate("ksAddInvGroup()")
        await pg.evaluate("ksAddAddrGroup()")
        await pg.wait_for_timeout(200)
        heads = await pg.evaluate("[...document.querySelectorAll('.ks-group-head')].map(x=>x.firstChild.textContent)")
        dels_visible = await pg.evaluate("[...document.querySelectorAll('.ks-group-del')].map(x=>getComputedStyle(x).display!=='none')")
        out.append(f"添加后组头: {heads}")
        out.append(f"删除链接可见: {dels_visible}")
        # 新组输入应为空且无 id 冲突
        ids = await pg.evaluate("[...document.querySelectorAll('.ks-inv-group input[id]')].length")
        out.append(f"开票组内带id的input数(应仅第一组3个): {ids}")
        # 删除第二组→回落①
        await pg.evaluate("[...document.querySelectorAll('.ks-inv-group')][1].querySelector('.ks-group-del').click()")
        await pg.wait_for_timeout(150)
        out.append(f"删组后: 开票组{await pg.evaluate("document.querySelectorAll('.ks-inv-group').length")} 组头{await pg.evaluate("[...document.querySelectorAll('.ks-inv-group .ks-group-head')].map(x=>x.firstChild.textContent)")}")
        await pg.screenshot(path='_scan_tmpdir/g60_partner_multi.png', full_page=True)

        out.append(f"JS错: {len(errs)} {errs[:2]}")
        await b.close()
    print('\n'.join(out))

asyncio.run(main())
