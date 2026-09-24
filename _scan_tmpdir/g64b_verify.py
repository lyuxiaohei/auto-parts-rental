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
        pg.on('console', lambda m: errs.append('console.error: ' + m.text) if m.type == 'error' else None)

        # ① 采购退货单列表
        await pg.goto(B + '/采购管理/采购退货单列表.html')
        await pg.wait_for_timeout(500)
        rows = pg.locator('table tbody tr')
        out.append('[1] 行数(期望4): %s' % await rows.count())
        r1 = await pg.evaluate(
            "(() => { const tr = document.querySelector('table tbody tr'); const tds = tr.querySelectorAll('td');"
            " return { key: tds[1].innerText.trim(), status: tds[8].innerText.trim(), ops: [...tr.querySelectorAll('.ops a')].map(a=>a.textContent) }; })()")
        out.append('[2] 首行: %s' % r1)
        stabs = await pg.evaluate("[...document.querySelectorAll('.stabs .stab')].map(s=>s.textContent.trim())")
        out.append('[3] 页签统计: %s' % stabs)
        await pg.screenshot(path='_scan_tmpdir/g64b_return_list.png')

        # ② 行内审核 → 审核页
        await rows.first.locator('.ops a', has_text='审核').click()
        await pg.wait_for_timeout(600)
        out.append('[4] 审核页URL尾: %s' % pg.url.split('/')[-1])
        out.append('[5] 审核页标题: %s' % await pg.locator('#dtTitle').inner_text())
        body = await pg.evaluate('document.body.innerText')
        out.append('[6] 审核页含[审核决策]=%s [6,328.00]=%s [待审核]=%s [单号]=%s' % ('审核决策' in body, '6,328.00' in body, '待审核' in body, 'CGTH-20260915-004' in body))
        await pg.screenshot(path='_scan_tmpdir/g64b_return_audit.png', full_page=True)

        # ③ 无参默认落待审核单
        await pg.goto(B + '/采购管理/采购退货审核.html')
        await pg.wait_for_timeout(500)
        out.append('[7] 无参默认标题: %s' % await pg.locator('#dtTitle').inner_text())

        # ④ 我的待办：计数与行
        await pg.goto(B + '/我的待办.html')
        await pg.wait_for_timeout(500)
        out.append('[8] 待办总数: %s · 行数: %s' % (await pg.locator('#todoCount').inner_text(), await pg.locator('#todoBody tr').count()))
        cgth = pg.locator('#todoBody tr', has_text='CGTH-20260915-004')
        out.append('[9] 待办含采购退货单行: %s · 动作=%s' % (await cgth.count(), await cgth.first.inner_text() if await cgth.count() else '—'))
        await cgth.first.locator('a', has_text='去审核').click()
        await pg.wait_for_timeout(600)
        out.append('[10] 待办跳转URL尾: %s' % pg.url.split('/')[-1])

        # ⑤ 退款新建（消费实体）无 JS 错
        await pg.goto(B + '/财务协同/退款新建.html')
        await pg.wait_for_timeout(400)
        out.append('[11] JS错总数: %s %s' % (len(errs), errs[:3]))
        await b.close()
    print('\n'.join(out))

asyncio.run(main())
