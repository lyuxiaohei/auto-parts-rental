# -*- coding: utf-8 -*-
"""销售出库→出货单打印 PW 断言"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    pg = browser.new_page()
    errors = []
    pg.on('pageerror', lambda e: errors.append(str(e)))

    # 1. 销售出库列表 ops
    pg.goto((ROOT / '销售管理/销售出库列表.html').as_uri())
    pg.wait_for_load_state('networkidle')
    n = pg.evaluate("() => Array.from(document.querySelectorAll('tbody .ops a')).filter(a => a.textContent.trim() === '打印出货单').length")
    sample = pg.evaluate("() => { var a = Array.from(document.querySelectorAll('tbody .ops a')).find(a => a.textContent.trim() === '打印出货单'); return a ? a.getAttribute('onclick') : ''; }")
    print('1. 销售 ops 打印出货单数:', n, '| 样例:', sample)
    assert n >= 6 and "go('../租赁管理/出货单打印.html?key=XSCK-" in sample

    # 2. 打印页销售行渲染
    pg.goto((ROOT / '租赁管理/出货单打印.html').as_uri() + '?key=XSCK-20260826-012')
    pg.wait_for_load_state('networkidle')
    cust = pg.evaluate("() => document.getElementById('dnCustomer').textContent")
    date = pg.evaluate("() => document.getElementById('dnDate').textContent")
    no = pg.evaluate("() => document.getElementById('dnNo').textContent")
    desc = pg.evaluate("() => document.querySelector('#dnBody tr td:nth-child(3)').textContent")
    qty = pg.evaluate("() => document.querySelector('#dnBody tr td:nth-child(4)').textContent")
    so = pg.evaluate("() => document.querySelector('#dnBody tr td:nth-child(2)').textContent")
    addr = pg.evaluate("() => document.getElementById('dnAddr').textContent")
    print('2. 销售单据: 收货单位[%s] 日期[%s] 单号[%s] 订单[%s]' % (cust, date, no, so))
    print('   描述[%s] 箱数[%s] 收货地址[%s]' % (desc, qty, addr))
    assert '东海商用' in cust and desc == '铰链×900 / 内衬×400' and qty == '1300' and so == 'SO-20260822-0038' and no.startswith('S20260826')

    # 3. 租赁侧回归（CK 仍走组合件逻辑）
    pg.goto((ROOT / '租赁管理/出货单打印.html').as_uri() + '?key=CK-20260903-016')
    pg.wait_for_load_state('networkidle')
    desc2 = pg.evaluate("() => document.querySelector('#dnBody tr td:nth-child(3)').textContent")
    print('3. 租赁侧回归 描述[%s]' % desc2)
    assert '驾驶室围板箱' in desc2

    print('pageerror:', len(errors))
    assert not errors
    print('ALL PASS')
    browser.close()
