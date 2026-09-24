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

        # 盘点录入
        await pg.goto(B + '/仓储作业/盘点录入.html')
        await pg.wait_for_timeout(500)
        lab = await pg.evaluate("[...document.querySelectorAll('.form-label')].map(x=>x.innerText.trim())")
        opts = await pg.evaluate("(() => { const ls=[...document.querySelectorAll('.form-label')].filter(x=>x.innerText.indexOf('盘点库位')>-1); if(!ls.length) return null; const s=ls[0].closest('.form-row').querySelector('select'); return [...s.options].map(o=>o.textContent); })()")
        out.append('%s 录入·字段名: %s' % ('PASS' if '盘点库位：' in lab and '盘点范围：' not in lab else 'FAIL', [x for x in lab if '盘点' in x]))
        out.append('%s 录入·选项(%d): %s' % ('PASS' if opts and len(opts) == 5 else 'FAIL', len(opts) if opts else 0, opts))

        # 盘点列表
        await pg.goto(B + '/仓储作业/盘点列表.html')
        await pg.wait_for_timeout(500)
        ths = await pg.evaluate("[...document.querySelectorAll('thead th')].map(x=>x.innerText.trim())")
        out.append('%s 列表·表头: %s' % ('PASS' if '盘点库位' in ths and '盘点范围' not in ths else 'FAIL', ths))
        fopts = await pg.evaluate("(() => { const ff=[...document.querySelectorAll('.ff')].find(x=>x.innerText.indexOf('盘点库位')>-1); return ff ? [...ff.querySelector('select').options].map(o=>o.textContent) : null; })()")
        out.append('%s 列表·筛选选项(%d): %s' % ('PASS' if fopts and len(fopts) == 6 else 'FAIL', len(fopts) if fopts else 0, fopts))
        row1 = await pg.evaluate("(() => { const td = document.querySelector('tbody tr td'); return td ? td.innerText.trim() : null; })()")
        out.append('%s 列表·首行值: %s' % ('PASS' if row1 and '全部库位' in row1 else 'FAIL', row1))

        # 详情 PD-202608-02 / PD-202606-01
        await pg.goto(B + '/仓储作业/盘点详情.html?id=PD-202608-02')
        await pg.wait_for_timeout(500)
        body = await pg.evaluate('document.body.innerText')
        out.append('%s 详情02: 盘点库位行=%s · 明细库位RD=%s' % ('PASS' if '成品区 RB · 组装暂存（RD-01 / RD-02）' in body and 'RD-01' in body and 'RD-02' in body else 'FAIL', '盘点库位' in body, 'RD-01' in body and 'RD-02' in body))
        await pg.goto(B + '/仓储作业/盘点详情.html?id=PD-202606-01')
        await pg.wait_for_timeout(500)
        body = await pg.evaluate('document.body.innerText')
        out.append('%s 详情06: 次品区 RC（RC-01）=%s · RC-01明细=%s' % ('PASS' if '次品区 RC（RC-01）' in body and 'RC-01' in body else 'FAIL', '次品区 RC（RC-01）' in body, 'RC-01' in body))
        out.append('JS 错: %s %s' % (len(errs), errs[:3]))

        await pg.goto(B + '/仓储作业/盘点列表.html'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='_scan_tmpdir/g70_checklist.png')
        await pg.goto(B + '/仓储作业/盘点录入.html'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='_scan_tmpdir/g70_entry.png')
        await b.close()
    print('\n'.join(out))

asyncio.run(main())
