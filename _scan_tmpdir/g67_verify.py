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

        async def check(url, contains, excludes=None, note=''):
            await pg.goto(B + url)
            await pg.wait_for_timeout(450)
            body = await pg.evaluate('document.body.innerText')
            ok1 = all(k in body for k in contains)
            ok2 = all(k not in body for k in (excludes or []))
            out.append('%s %s | 含%s=%s 排除%s=%s' % ('PASS' if ok1 and ok2 else 'FAIL', url, contains, ok1, excludes or '-', ok2))

        # 财务域
        await check('/财务协同/付款登记.html', ['付款单号'], ['付款编号'])
        await check('/财务协同/收款登记.html', ['收款单号'], ['收款编号'])
        await check('/财务协同/退款登记.html', ['退款单号'], ['退款编号'])
        await check('/财务协同/开票登记.html', ['开票登记单号', '发票类型'], ['发票登记号'])
        await check('/财务协同/应收账单.html', ['应收账单号'], ['账单编号'])
        await check('/财务协同/银行回单核销.html', ['银行回单号'], ['回单编号'])
        # 应收详情渲染器
        await check('/财务协同/应收详情.html', ['应收账单号'], [])
        # 新建表单 + 下拉填充
        await pg.goto(B + '/财务协同/付款新建.html'); await pg.wait_for_timeout(500)
        opts = await pg.evaluate("(() => { const sel = [...document.querySelectorAll('select')].find(s=>s.closest('.form-row') && s.closest('.form-row').innerText.indexOf('关联应付账单号')>-1); return sel ? sel.options.length : -1; })()")
        out.append('%s 付款新建·关联应付账单号下拉选项=%s' % ('PASS' if opts > 1 else 'FAIL', opts))
        await pg.goto(B + '/财务协同/收款新建.html'); await pg.wait_for_timeout(500)
        opts = await pg.evaluate("(() => { const sel = [...document.querySelectorAll('select')].find(s=>s.closest('.form-row') && s.closest('.form-row').innerText.indexOf('关联应收账单号')>-1); return sel ? sel.options.length : -1; })()")
        out.append('%s 收款新建·关联应收账单号下拉选项=%s' % ('PASS' if opts > 1 else 'FAIL', opts))
        # 采购/销售退货
        await check('/采购管理/采购退货单列表.html', ['关联采购入库单号', 'CGTH-20260915-004'], ['关联原单号'])
        await pg.goto(B + '/采购管理/采购退货新建.html'); await pg.wait_for_timeout(500)
        opts = await pg.evaluate("(() => { const sel = [...document.querySelectorAll('select')].find(s=>s.closest('.form-row') && s.closest('.form-row').innerText.indexOf('关联采购入库单号')>-1); return sel ? sel.options.length : -1; })()")
        out.append('%s 采购退货新建·下拉选项=%s' % ('PASS' if opts > 1 else 'FAIL', opts))
        await check('/销售管理/销售退货单列表.html', ['关联销售出库单号'], ['关联出库单号'])
        await check('/销售管理/销售退货新建.html', ['关联销售出库单号'], ['关联原单'])
        # 租赁域
        await check('/租赁管理/租赁出库录单.html', ['关联租赁单号', '关联销售订单号'], [])
        await check('/租赁管理/租赁出库列表.html', ['关联销售订单号'], [])
        await check('/租赁管理/租赁单新建.html', ['创建日期'], ['建单日期'])
        await check('/租赁管理/租赁单详情.html?id=ZL-20260910-036', ['创建日期'], ['建单日期'])
        await check('/租赁管理/退租入库列表.html', ['拆散去向'], ['拆解去向'])
        await check('/租赁管理/退租入库详情.html?id=TZRK-20260902-010', ['入库日期'], ['退回日期'])
        # 租入域
        await check('/租入管理/租入单详情.html?id=RZD-20260910-009', ['租金'], ['月租'])
        await check('/租入管理/租入入库列表.html', ['关联租入单号'], [])
        await check('/租入管理/归还出库列表.html', ['关联租入单号', '归还时间'], [])
        await check('/租入管理/归还出库详情.html?id=GHCK-20260903-001', ['归还时间', '2026-09-03 11:30', '供应商'], ['供应商（带出）'])
        # 采购/销售订单
        await check('/采购管理/采购订单详情.html?id=PO-20260910-019', ['采购订单号', '订单状态', '客户'], ['客户（带出）', '（带出）'])
        await check('/销售管理/销售订单详情.html?id=SO-20260903-0047', ['销售订单号', '订单状态'], [])
        await check('/销售管理/销售订单列表.html', ['业务员'], ['下单人'])
        # 仓储/基础
        await check('/仓储作业/库存查询.html', ['物料编码', '客户端（租出）'], ['>编码<'])
        await check('/仓储作业/库存流水.html?id=XNC-ZZ-WBX', ['物料类型', '客户端（租出）'], ['物料类别', 'on-hire'])
        await check('/仓储作业/盘点录入.html', ['复盘人'], ['复 盘 人'])
        await check('/基础数据/BOM.html', ['BOM物料名称'], ['（组合件）'])
        await check('/基础数据/BOM维护.html', ['供应商', '版本'], ['供应商（带出）', '版本号：'])
        await check('/租赁管理/器具出租履历.html?key=WBX-1210L', ['物料编码', '物料名称'], ['器具编码'])
        await pg.screenshot(path='_scan_tmpdir/g67_return_list.png')
        await pg.goto(B + '/财务协同/付款登记.html'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='_scan_tmpdir/g67_pay_list.png')
        out.append('JS 错总数: %s %s' % (len(errs), errs[:4]))
        await b.close()
    print('\n'.join(out))

asyncio.run(main())
