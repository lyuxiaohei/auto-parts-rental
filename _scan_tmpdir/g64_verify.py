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

        # ① 列表页基础
        await pg.goto(B + '/采购管理/采购订单列表.html')
        await pg.wait_for_timeout(500)
        btn = pg.locator('.head-btns button', has_text='批量审核')
        out.append('[1] 批量审核按钮数(期望1): %s' % await btn.count())
        out.append('[2] 初始禁用: opacity=%s cursor=%s' % (await btn.evaluate('el=>el.style.opacity'), await btn.evaluate('el=>el.style.cursor')))
        rows = pg.locator('table.aln-a tbody tr')
        out.append('[3] 行数(期望8): %s' % await rows.count())
        r1 = await pg.evaluate(
            "(() => { const tr = document.querySelector('table.aln-a tbody tr'); const tds = tr.querySelectorAll('td');"
            " return { key: tds[1].innerText.trim(), status: tds[10].innerText.trim(), ops: [...tr.querySelectorAll('.ops a')].map(a=>a.textContent) }; })()")
        out.append('[4] 首行: %s' % r1)

        # ② 勾选 → 启用 → 弹窗
        await rows.first.locator('input.cb').check()
        out.append('[5] 勾选后启用: opacity=%s' % await btn.evaluate('el=>el.style.opacity'))
        await btn.click()
        out.append('[6] 弹窗显示: %s' % await pg.locator('#poBatchModal').evaluate('el=>el.classList.contains("show")'))
        out.append('[7] 计数=%s · 明细行=%s · 单号=%s' % (
            await pg.locator('#poBatchCount').inner_text(),
            await pg.locator('#poBatchList tr').count(),
            await pg.locator('#poBatchList tr td').first.inner_text()))
        out.append('[8] 默认结论: %s' % await pg.locator('#poBatchModal .radio.checked').inner_text())
        await pg.screenshot(path='_scan_tmpdir/g64_batch_modal.png')

        # ③ 结论切换 + 取消关闭 + 遮罩关闭
        await pg.locator('#poBatchModal .radio', has_text='驳回').click()
        out.append('[9] 切换驳回: %s' % await pg.locator('#poBatchModal .radio.checked').inner_text())
        await pg.locator('#poBatchModal .modal-footer button', has_text='取消').click()
        out.append('[10] 取消关闭: %s' % (not await pg.locator('#poBatchModal').evaluate('el=>el.classList.contains("show")')))
        await btn.click()
        await pg.mouse.click(20, 400)  # 点遮罩空白处
        await pg.wait_for_timeout(150)
        out.append('[10b] 遮罩点击关闭: %s' % (not await pg.locator('#poBatchModal').evaluate('el=>el.classList.contains("show")')))

        # ④ 重开 → 确认提交 → toast
        await btn.click()
        await pg.locator('#poBatchNote').fill('价格与框架协议一致，集中通过')
        await pg.locator('#poBatchModal .modal-footer button', has_text='确认提交').click()
        await pg.wait_for_timeout(250)
        out.append('[11] 提交toast: %s' % await pg.locator('#g64Toast').inner_text())
        out.append('[12] 提交后弹窗关闭: %s' % (not await pg.locator('#poBatchModal').evaluate('el=>el.classList.contains("show")')))

        # ⑤ 非待审核行拦截
        await rows.first.locator('input.cb').uncheck()
        await rows.nth(1).locator('input.cb').check()
        await btn.click()
        await pg.wait_for_timeout(250)
        out.append('[13] 非待审核拦截toast: %s' % await pg.locator('#g64Toast').inner_text())

        # ⑥ 行内审核 op → 审核页（两种交互之二·整页）
        await rows.first.locator('.ops a', has_text='审核').click()
        await pg.wait_for_timeout(600)
        out.append('[14] 审核页URL尾: %s' % pg.url.split('/')[-1])
        out.append('[15] 审核页标题: %s' % await pg.locator('#dtTitle').inner_text())
        body = await pg.evaluate('document.body.innerText')
        out.append('[16] 审核页含[审核决策]=%s [37,968.00]=%s [待审核]=%s' % ('审核决策' in body, '37,968.00' in body, '待审核' in body))
        await pg.screenshot(path='_scan_tmpdir/g64_audit_page.png', full_page=True)

        # ⑦ 无 ?id 默认选中待审核单
        await pg.goto(B + '/采购管理/采购订单审核.html')
        await pg.wait_for_timeout(500)
        out.append('[17] 无参默认标题: %s' % await pg.locator('#dtTitle').inner_text())

        # ⑧ 其他消费页无 JS 错
        for p in ['/采购管理/采购入库录单.html', '/财务协同/应付新建.html', '/我的待办.html']:
            await pg.goto(B + p)
            await pg.wait_for_timeout(400)
        out.append('[18] JS错总数: %s %s' % (len(errs), errs[:3]))
        await b.close()
    print('\n'.join(out))

asyncio.run(main())
