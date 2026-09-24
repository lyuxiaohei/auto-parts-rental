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
        await pg.goto(B + '/基础数据/客商新建.html')
        await pg.wait_for_timeout(600)
        gap = await pg.evaluate("""(() => {
            const grp = document.querySelector('.ks-inv-group');
            const last = grp.querySelector('.form-row:last-child');
            const rows = [...document.querySelectorAll('.card')].find(c=>c.innerText.indexOf('开票资料')>-1).querySelectorAll('.form-row');
            const remark = [...rows].find(r=>r.innerText.indexOf('备注')>-1);
            const a = last.getBoundingClientRect().bottom;
            const c = remark.getBoundingClientRect().top;
            return { gap: Math.round(c - a), lastH: Math.round(last.getBoundingClientRect().height), remarkH: Math.round(remark.getBoundingClientRect().height) };
        })()""")
        out.append('收款账号→备注 间距: %spx（期望≈20）' % gap['gap'])
        # 加第二组后的组间距
        await pg.evaluate('ksAddInvGroup()')
        await pg.wait_for_timeout(250)
        g = await pg.evaluate("""(() => {
            const gs=[...document.querySelectorAll('.ks-inv-group')];
            const last1 = gs[0].querySelector('.form-row:last-child').getBoundingClientRect().bottom;
            const head2 = gs[1].querySelector('.ks-group-head').getBoundingClientRect().top;
            return Math.round(head2 - last1);
        })()""")
        out.append('第1组末行→第2组组头 间距: %spx（期望≈20+2）' % g)
        await pg.screenshot(path='_scan_tmpdir/g68_spacing.png')
        out.append('JS 错: %s' % len(errs))
        await b.close()
    print('\n'.join(out))

asyncio.run(main())
