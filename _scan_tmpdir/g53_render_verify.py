# -*- coding: utf-8 -*-
"""G53 T3-2 渲染门：20 实体详情页三卡版式断言（只读验证脚本）。
断言：a) 无 pageerror/console.error；b) #detailBody > .fm-card ≥2 且首卡标题=formTitle；
c) 明细卡首三列；d) chain/timeline 渲染（流转信息卡）；e) .dgrid 旧四段式 0 残留。"""
import asyncio, sys, json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')

# (实体, 详情页, 默认记录键, formTitle, 明细首三列)
CASES = [
    ('purchaseOrders',   '采购管理/采购订单详情.html',   'PO-20260902-018',  '订单信息',   ['序号', '物料编码', '物料名称']),
    ('purchaseInbounds', '采购管理/采购入库详情.html',   'CGRK-20260828-012','基本信息',   ['序号', '物料编码', '物料名称']),
    ('purchaseReturns',  '采购管理/采购退货详情.html',   'CGTH-20260914-001','退货信息',   ['序号', '物料编码', '物料名称']),
    ('rentInOrders',     '租入管理/租入单详情.html',     'RZD-20260815-003', '租入信息',   ['序号', '物料编码', '物料名称']),
    ('rentInbounds',     '租入管理/租入入库详情.html',   'RZRK-20260816-021','入库信息',   ['序号', '物料编码', '物料名称']),
    ('rentInReturns',    '租入管理/租入归还详情.html',   'GHCK-20260903-001','归还信息',   ['序号', '物料编码', '物料名称']),
    ('leaseOrders',      '租赁管理/租赁单详情.html',     'ZL-20260823-033',  '租赁信息',   ['序号', '物料编码', '物料名称']),
    ('comboOutbounds',   '租赁管理/租赁出库详情.html',   'CK-20260910-022',  '基本信息',   ['序号', '组合件编码', '组合件名称']),
    ('returnInbounds',   '租赁管理/退租入库详情.html',   'TZRK-20260902-010','退租入库信息', ['序号', '物料编码', '物料名称']),
    ('transferOutbounds','租赁管理/转移出库单详情.html', 'ZY-20260915-005',  '转移信息',   ['序号', '物料编码', '物料名称']),
    ('stocktakes',       '仓储作业/盘点详情.html',       'PD-202608-03',     '基本信息',   ['序号', '物料编码', '物料名称']),
    ('otherInbounds',    '仓储作业/其他入库详情.html',   'QTRK-20260901-003','入库信息',   ['序号', '物料编码', '物料名称']),
    ('otherOutbounds',   '仓储作业/其他出库详情.html',   'QTCK-20260905-005','出库信息',   ['序号', '物料编码', '物料名称']),
    ('salesOrders',      '销售管理/销售订单详情.html',   'SO-20260903-0047', '订单信息',   ['序号', '物料编码', '物料名称']),
    ('salesOutbounds',   '销售管理/销售出库详情.html',   'XSCK-20260910-016','出库信息',   ['序号', '物料编码', '物料名称']),
    ('salesReturns',     '销售管理/销售退货详情.html',   'XSTH-20260913-001','退货信息',   ['序号', '物料编码', '物料名称']),
    ('receipts',         '财务协同/收款详情.html',       'HK-20260830-014',  '收款信息',   ['关联账单', '费用项', '本次收款(元)']),
    ('payments',         '财务协同/付款详情.html',       'PAY-20260902-005', '付款信息',   ['笔次', '比例(%)', '分期金额(元)']),
    ('invoices',         '财务协同/开票详情.html',       'INV-20260902-013', '开票信息',   ['费用项', '关联账单', '税率']),
    ('refunds',          '财务协同/退款详情.html',       'TKD-20260913-002', '退款信息',   ['关联退货单', '退货类型', '退款金额(元)']),
]

async def main():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for ent, page_rel, key, form_title, first3 in CASES:
            errs = []
            ctx = await browser.new_context()
            pg = await ctx.new_page()
            page_errors, console_errors = [], []
            pg.on('pageerror', lambda e: page_errors.append(str(e)))
            pg.on('console', lambda m: console_errors.append(m.text) if m.type == 'error' else None)
            url = (ROOT / page_rel).as_uri() + '?id=' + key
            try:
                await pg.goto(url, wait_until='networkidle', timeout=20000)
                await pg.wait_for_timeout(300)
                # a) 无 JS 错误
                if page_errors or console_errors:
                    errs.append('JS错误: ' + '; '.join((page_errors + console_errors)[:2]))
                # b) fm-card ≥2 且首卡标题
                n_cards = await pg.locator('#detailBody > .fm-card').count()
                if n_cards < 2:
                    errs.append('fm-card=' + str(n_cards) + ' <2')
                t1 = await pg.locator('#detailBody > .fm-card .card-title').first.inner_text() if n_cards else ''
                if t1.strip() != form_title:
                    errs.append('首卡标题=' + t1.strip() + ' 期望=' + form_title)
                # c) 明细卡存在 + 首三列
                n_tab = await pg.locator('#detailBody > .fm-card table thead th').count()
                if n_tab == 0:
                    errs.append('明细表缺失')
                else:
                    got3 = []
                    for i in range(min(3, n_tab)):
                        got3.append((await pg.locator('#detailBody > .fm-card table thead th').nth(i).inner_text()).strip())
                    if got3 != first3:
                        errs.append('明细首三列=' + '|'.join(got3) + ' 期望=' + '|'.join(first3))
                # d) 流转信息卡（chain/timeline）
                flow = await pg.locator('#detailBody > .fm-card .card-title', has_text='流转信息').count()
                chain_n = await pg.locator('#detailBody .chain').count()
                tl_n = await pg.locator('#detailBody .tl').count()
                if flow < 1 or (chain_n < 1 and tl_n < 1):
                    errs.append('流转卡缺失(flow=%d chain=%d tl=%d)' % (flow, chain_n, tl_n))
                # e) .dgrid 旧四段式 0 残留
                dgrid = await pg.locator('#detailBody .dgrid').count()
                if dgrid > 0:
                    errs.append('dgrid 残留=' + str(dgrid))
            except Exception as ex:
                errs.append('异常: ' + str(ex)[:120])
            await ctx.close()
            ok = not errs
            results.append((ent, ok, errs))
            print(('PASS ' if ok else 'FAIL ') + ent + ('' if ok else '  <- ' + ' ; '.join(errs)), flush=True)
        await browser.close()
    npass = sum(1 for r in results if r[1])
    print('RENDER GATE: %d PASS / %d FAIL' % (npass, len(results) - npass))
    sys.exit(0 if npass == len(results) else 1)

asyncio.run(main())
