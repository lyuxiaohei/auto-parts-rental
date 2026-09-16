# -*- coding: utf-8 -*-
import os
from playwright.sync_api import sync_playwright
ROOT='/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型'
CHECKS=[
 ('基础数据/客商详情.html?id=DW-0001', ['开票资料','纳税人识别号','91131015MA1FA00014','结算周期']),
 ('租赁管理/租赁单新建.html', ['PRJ-2606 长丰锂电·二期 电池包周转箱扩容']),
 ('财务协同/应收账单.html', ['预收']),
 ('财务协同/退款登记.html', ['采购退货退款（供应商·我方收款）','销售退货退款（客户·我方付款）']),
 ('财务协同/退款新建.html', ['预收退回','多付退回']),
 ('财务协同/损益报表.html', ['AR-2026-08-PRJ2601','AP-20260901-008']),
 ('首页/项目看板.html', ['AR-2026-08-PRJ2601']),
 ('基础数据/BOM维护.html', ['暂 存']),
 ('租入管理/租入归还审核.html', ['押金随归还审核原路退还']),
 ('租赁管理/退租入库详情.html?id=TZRK-20260915-012', ['转租物经直接客户退回','博世汽车部件（苏州）']),
 ('租入管理/租入归还详情.html?id=GHCK-20260903-002', ['押金退还','¥12,000.00']),
 ('财务协同/应收详情.html', ['账单类型','备注']),
 ('财务协同/应付详情.html', ['账单日期','到期日']),
 ('财务协同/退款详情.html?id=TKD-20260916-004', ['预收退回','20,000.00']),
 ('财务协同/退款详情.html?id=TKD-20260916-005', ['多付退回','AP-20260905-012']),
]
fails=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    for page,tokens in CHECKS:
        pg.goto('file://'+os.path.join(ROOT,page), wait_until='networkidle'); pg.wait_for_timeout(300)
        body=pg.evaluate('() => document.body.innerText')
        for t in tokens:
            if t not in body:
                fails.append(page+' 缺: '+t)
                print('[FAIL]', page, '缺:', t)
        else:
            pass
    b.close()
print('DOM 内容断言：', len(CHECKS), '页', 'FAIL', len(fails))
