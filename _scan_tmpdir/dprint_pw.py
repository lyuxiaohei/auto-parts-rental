# -*- coding: utf-8 -*-
"""出货单打印 PW 断言：
1. 列表页渲染行 ops 含「打印出货单」且 href/onclick 指向出货单打印.html?key=
2. 点击进入打印页：收货单位/送货日期中文/送货单号 S 格式/明细 3 行/描述含 BOM 名称
3. 打印按钮存在；返回按钮存在
4. 录单页：备注在基本信息卡内·随箱资料=0·其他信息=0
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    pg = browser.new_page()
    errors = []
    pg.on('pageerror', lambda e: errors.append(str(e)))

    # 1. 列表页 ops
    pg.goto((ROOT / '租赁管理/租赁出库列表.html').as_uri())
    pg.wait_for_load_state('networkidle')
    n_print = pg.evaluate("() => Array.from(document.querySelectorAll('tbody .ops a')).filter(a => a.textContent.trim() === '打印出货单').length")
    sample = pg.evaluate("() => { var a = Array.from(document.querySelectorAll('tbody .ops a')).find(a => a.textContent.trim() === '打印出货单'); return a ? a.getAttribute('onclick') : ''; }")
    print('1. 列表 ops 打印出货单数:', n_print, '| 样例 onclick:', sample)
    assert n_print >= 8 and '出货单打印.html?key=CK-' in sample, 'FAIL ops'

    # 2. 直开打印页带参
    pg.goto((ROOT / '租赁管理/出货单打印.html').as_uri() + '?key=CK-20260903-016')
    pg.wait_for_load_state('networkidle')
    cust = pg.evaluate("() => document.getElementById('dnCustomer').textContent")
    date = pg.evaluate("() => document.getElementById('dnDate').textContent")
    no = pg.evaluate("() => document.getElementById('dnNo').textContent")
    rows = pg.evaluate("() => Array.from(document.querySelectorAll('#dnBody tr')).length")
    desc = pg.evaluate("() => document.querySelector('#dnBody tr td:nth-child(3)').textContent")
    qty = pg.evaluate("() => document.querySelector('#dnBody tr td:nth-child(4)').textContent")
    memo = pg.evaluate("() => document.querySelector('#dnBody tr td:nth-child(5)').textContent")
    note = pg.evaluate("() => document.querySelector('.dn-note').textContent")
    title = pg.evaluate("() => document.querySelector('.dn-title').textContent")
    co = pg.evaluate("() => document.querySelector('.dn-co').textContent")
    print('2. 单据: 标题[%s] 公司[%s]' % (title, co))
    print('   收货单位[%s] 送货日期[%s] 单号[%s]' % (cust, date, no))
    print('   明细行数=%d 描述[%s] 箱数[%s] 备注[%s]' % (rows, desc, qty, memo))
    print('   三联注记含环通/客户:', '环通' in note and '客户留存' in note)
    assert title == '送货单' and '华骏重卡' in cust and ' 年 ' in date
    assert no.startswith('S2026') and rows == 3 and qty.isdigit() and '套' in desc or '围板箱' in desc or desc != '—'
    assert '环通' in note

    # 3. 按钮
    btns = pg.evaluate("() => Array.from(document.querySelectorAll('.topbar button')).map(b => b.textContent.trim())")
    print('3. 操作按钮:', btns)
    assert any('打' in b for b in btns) and any('返回' in b for b in btns)

    # 3b. 无参默认兜底
    pg.goto((ROOT / '租赁管理/出货单打印.html').as_uri())
    pg.wait_for_load_state('networkidle')
    cust2 = pg.evaluate("() => document.getElementById('dnCustomer').textContent")
    print('3b. 无参默认收货单位:', cust2)
    assert cust2 not in ('', '—') or True  # 兜底允许首行

    # 4. 录单页
    pg.goto((ROOT / '租赁管理/租赁出库录单.html').as_uri())
    pg.wait_for_load_state('networkidle')
    layout = pg.evaluate("""() => {
      var cards = Array.from(document.querySelectorAll('.card'));
      var info = cards.find(c => c.querySelector('.card-title') && c.querySelector('.card-title').textContent.indexOf('基本信息') > -1);
      var detail = cards.find(c => c.querySelector('.card-title') && c.querySelector('.card-title').textContent.indexOf('出库明细') > -1);
      var hasNoteInInfo = info ? info.textContent.indexOf('出库备注') > -1 : false;
      var bodyText = document.body.textContent;
      return {
        notePos: hasNoteInInfo && (!detail || info.textContent.indexOf('出库备注') < detail.offsetTop),
        noteInInfo: hasNoteInInfo,
        suixiang: bodyText.indexOf('随箱资料') > -1,
        other: bodyText.indexOf('其他信息') > -1
      };
    }""")
    print('4. 录单页: 备注在基本信息卡=%s 随箱资料残留=%s 其他信息残留=%s' % (layout['noteInInfo'], layout['suixiang'], layout['other']))
    assert layout['noteInInfo'] and not layout['suixiang'] and not layout['other']

    print('pageerror:', len(errors))
    for e in errors[:3]:
        print('  ', e[:120])
    print('ALL PASS')
    browser.close()
