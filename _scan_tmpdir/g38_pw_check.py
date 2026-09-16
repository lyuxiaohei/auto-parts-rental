# -*- coding: utf-8 -*-
"""G38 PW 抽验：两录单页四价格列有值＋两列表页列对齐（file:// + DOM 断言）"""
import sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

BASE = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')
results = []

def check(name, cond, detail=''):
    results.append((name, bool(cond), detail))
    print(('[PASS] ' if cond else '[FAIL] ') + name + (' | ' + detail if detail else ''))

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()

    # 1. 采购入库录单：12 列×3 行·四价格格有值
    pg.goto((BASE / '采购管理' / '采购入库录单.html').as_uri())
    ths = pg.eval_on_selector_all('thead th', 'els => els.length')
    rows = pg.eval_on_selector_all('tbody tr', 'els => els.length')
    check('采购入库录单 表头列数=12', ths == 12, '实际 %d' % ths)
    tds = pg.eval_on_selector_all('tbody tr', 'els => els.map(e=>e.querySelectorAll("td").length)')
    check('采购入库录单 3 行格数均=12', all(t == 12 for t in tds), str(tds))
    prices = pg.eval_on_selector_all('tbody tr', '''els => els.map(e => {
        const tds = e.querySelectorAll('td');
        const v = td => { const i = td.querySelector('input'); return i ? i.value : td.innerText.trim(); };
        return [v(tds[5]), v(tds[6]), v(tds[7]), v(tds[8])];
    })''')
    ok = all(all(p for p in r) for r in prices) and prices[0] == ['6.80', '13%', '7.68', '36,864.00']
    check('采购入库录单 四价格列逐格有值（行1=6.80/13%/7.68/36,864.00）', ok, str(prices))

    # 2. 租赁出库录单：12 列×2 行·四价格格有值
    pg.goto((BASE / '租赁管理' / '租赁出库录单.html').as_uri())
    ths = pg.eval_on_selector_all('thead th', 'els => els.length')
    check('租赁出库录单 表头列数=12', ths == 12, '实际 %d' % ths)
    tds = pg.eval_on_selector_all('tbody tr', 'els => els.map(e=>e.querySelectorAll("td").length)')
    check('租赁出库录单 2 行格数均=12', all(t == 12 for t in tds), str(tds))
    prices = pg.eval_on_selector_all('tbody tr', '''els => els.map(e => {
        const tds = e.querySelectorAll('td');
        const v = td => { const i = td.querySelector('input'); return i ? i.value : td.innerText.trim(); };
        return [v(tds[4]), v(tds[5]), v(tds[6]), v(tds[7])];
    })''')
    ok = all(all(p for p in r) for r in prices) and prices[0] == ['2.40', '13%', '2.71', '487.80']
    check('租赁出库录单 四价格列逐格有值（行1=2.40/13%/2.71/487.80）', ok, str(prices))

    # 3. 采购入库列表：数据驱动渲染后 表头=行格数·入库库房列在位
    pg.goto((BASE / '采购管理' / '采购入库列表.html').as_uri())
    pg.wait_for_timeout(600)
    ths = pg.eval_on_selector_all('thead th', 'els => els.length')
    first_cells = pg.eval_on_selector_all('tbody tr:first-child td', 'els => els.length')
    check('采购入库列表 表头 10=行格 10', ths == 10 and first_cells == 10, 'thead %d / td %d' % (ths, first_cells))
    th_txt = pg.eval_on_selector_all('thead th', 'els => els.map(e=>e.innerText.trim())')
    check('采购入库列表 无「到货托数/入库库区」', '到货托数' not in th_txt and '入库库区' not in th_txt and '入库库房' in th_txt, str(th_txt))

    # 4. 租入入库列表：数据驱动渲染后 表头=行格数·入库库房/入库时间在位
    pg.goto((BASE / '租入管理' / '租入入库列表.html').as_uri())
    pg.wait_for_timeout(600)
    ths = pg.eval_on_selector_all('thead th', 'els => els.length')
    first_cells = pg.eval_on_selector_all('tbody tr:first-child td', 'els => els.length')
    check('租入入库列表 表头=行格数', ths == first_cells and ths > 0, 'thead %d / td %d' % (ths, first_cells))
    th_txt = pg.eval_on_selector_all('thead th', 'els => els.map(e=>e.innerText.trim())')
    check('租入入库列表 入库库房在位/无入库库区', '入库库房' in th_txt and '入库库区' not in th_txt, str(th_txt))

    b.close()

fails = [r for r in results if not r[1]]
print('PW 抽验合计 %d 项 / PASS %d / FAIL %d' % (len(results), len(results) - len(fails), len(fails)))
sys.exit(1 if fails else 0)
