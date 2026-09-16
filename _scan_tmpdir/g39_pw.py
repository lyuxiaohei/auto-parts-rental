# -*- coding: utf-8 -*-
"""G39 PW 交互断言（D-148）——验证门 5/6/7 ＋ 期段化渲染（T4）
  门5 列头联动：按时间周期→日租金(元/天)；按次→次单价(元/次)
  门6 计费方式随料带出：单件取 products.rentalMode/rentInMode·组合件取 bomList.billing
  门7 参考价带出且可改：四类单据各一例（采购/销售/租入/租赁）
  T4 期段化：应收/应付详情 segCols 表渲染"""
import os
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

PROTO = Path(__file__).resolve().parent.parent / 'P3-R01-包装租赁管理后台原型'
results = []

def check(name, cond, detail=''):
    results.append((name, bool(cond), detail))
    print('  [%s] %s %s' % ('PASS' if cond else 'FAIL', name, detail))

def url(rel):
    return (PROTO / rel).as_uri()

def set_select(page, sel, value):
    """编程选择（IAB 管道缺陷→evaluate 派发 change·bubbles）"""
    page.evaluate("""([sel, val]) => {
      const el = document.querySelector(sel);
      el.value = val;
      el.dispatchEvent(new Event('change', { bubbles: true }));
    }""", [sel, value])

with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))

    # ============ 门5+6+7 · 租入单新建 ============
    print('== 租入管理/租入单新建.html ==')
    pg.goto(url('租入管理/租入单新建.html'))
    th0 = pg.text_content('#g39PriceTh')
    check('门5 初始列头（按时间周期→日租金(元/天)）', th0 == '日租金(元/天)', '实测=' + th0)
    set_select(pg, 'select.g39mode', '按次')
    th1 = pg.text_content('#g39PriceTh')
    check('门5 切按次→次单价(元/次)', th1 == '次单价(元/次)', '实测=' + th1)
    set_select(pg, 'select.g39mode', '按时间周期')
    th2 = pg.text_content('#g39PriceTh')
    check('门5 切回按时间周期→日租金(元/天)', th2 == '日租金(元/天)', '实测=' + th2)
    # 门6：BTC-6040 rentInMode=按次 → 随料带出
    set_select(pg, 'select.g39mat', 'PLT-1210W 木托盘 1200×1000')
    mv = pg.eval_on_selector('select.g39mode', 'el => el.value')
    thv = pg.text_content('#g39PriceTh')
    check('门6 租入·PLT-1210W（档案租入按次）→计费方式带出=按次', mv == '按次', 'mode=' + mv)
    check('门6 列头随带出联动→次单价(元/次)', thv == '次单价(元/次)', 'th=' + thv)
    # 门7 租入：WBX-1210L 参考租入价 45.00 带出＋可改
    set_select(pg, 'select.g39mat', 'WBX-1210L 围板箱 1200×1000×970')
    ex0 = pg.eval_on_selector('input[data-tax="excl"]', 'el => el.value')
    check('门7 租入·参考租入价带出 45.00（不换算直录）', ex0 == '45.00', 'excl=' + ex0)
    pg.evaluate("document.querySelector('input[data-tax=\"excl\"]').value = '1.50'")
    ex1 = pg.eval_on_selector('input[data-tax="excl"]', 'el => el.value')
    ro = pg.eval_on_selector('input[data-tax="excl"]', 'el => el.readOnly')
    check('门7 租入·可改（非只读·值可编辑）', ex1 == '1.50' and not ro, '改后=' + ex1 + ' readonly=' + str(ro))
    # 天数联动
    pg.fill('#g39Days', '2')
    pg.eval_on_selector('#g39Days', "el => el.dispatchEvent(new Event('input',{bubbles:true}))")
    hint = pg.text_content('#g39RentHint')
    check('起租 09-03＋计租 2 天→止租 2026-09-04（当天起当天退=2 天）', '2026-09-04' in hint, hint.strip()[:60])

    # ============ 门5+6+7 · 租赁单新建（第 2 行 PLT-1210W 按次 15.00） ============
    print('== 租赁管理/租赁单新建.html ==')
    pg.goto(url('租赁管理/租赁单新建.html'))
    rows = pg.eval_on_selector_all('.edit-tbl tbody tr', 'els => els.length')
    th0 = pg.text_content('#g39PriceTh')
    check('门5 租赁·初始列头 日租金(元/天)', th0 == '日租金(元/天)', '实测=' + th0 + ' 行数=' + str(rows))
    # 第 2 行物料切 PLT-1210W（rentalMode=按次 15.00）
    pg.evaluate("""() => {
      const tr = document.querySelectorAll('.edit-tbl tbody tr')[1];
      const sel = tr.querySelector('select.g39mat');
      sel.value = 'PLT-1210W 木托盘 1200×1000';
      sel.dispatchEvent(new Event('change', { bubbles: true }));
    }""")
    mv2 = pg.evaluate("() => document.querySelectorAll('.edit-tbl tbody tr')[1].querySelector('select.g39mode').value")
    ex2 = pg.evaluate("() => document.querySelectorAll('.edit-tbl tbody tr')[1].querySelector('input[data-tax=\"excl\"]').value")
    thv2 = pg.text_content('#g39PriceTh')
    check('门6 租赁·PLT-1210W（档案按次）→计费方式带出=按次', mv2 == '按次', 'mode=' + mv2)
    check('门7 租赁·参考租赁价带出 15.00', ex2 == '15.00', 'excl=' + ex2)
    check('门5 租赁·列头联动→次单价(元/次)', thv2 == '次单价(元/次)', 'th=' + thv2)
    # 组合件：第 1 行切 ZH-2603-C（bomList 按次）·租价不预填（手填）
    ex1_before = pg.evaluate("() => document.querySelectorAll('.edit-tbl tbody tr')[0].querySelector('input[data-tax=\"excl\"]').value")
    pg.evaluate("""() => {
      const tr = document.querySelectorAll('.edit-tbl tbody tr')[0];
      const sel = tr.querySelector('select.g39mat');
      sel.value = 'ZH-2603-C 电池托盘护角套件';
      sel.dispatchEvent(new Event('change', { bubbles: true }));
    }""")
    mvz = pg.evaluate("() => document.querySelectorAll('.edit-tbl tbody tr')[0].querySelector('select.g39mode').value")
    exz = pg.evaluate("() => document.querySelectorAll('.edit-tbl tbody tr')[0].querySelector('input[data-tax=\"excl\"]').value")
    check('门6 组合件·ZH-2603-C 取 bomList.billing=按次', mvz == '按次', 'mode=' + mvz)
    check('门7 组合件租价手填（不预填·原值保留）', exz == ex1_before, '组合件 excl=' + exz)

    # ============ 门7 采购 · 采购订单新建 ============
    print('== 采购管理/采购订单新建.html ==')
    pg.goto(url('采购管理/采购订单新建.html'))
    pg.wait_for_timeout(400)
    set_select(pg, '.edit-tbl tbody tr:first-child select[data-prod-key]', 'LJ-A100')
    ex_p = pg.eval_on_selector('.edit-tbl tbody tr:first-child input[data-tax="excl"]', 'el => el.value')
    check('门7 采购·LJ-A100 参考未税采购价带出 6.80', ex_p == '6.80', 'excl=' + ex_p)

    # ============ 门7 销售 · 销售订单新建 ============
    print('== 销售管理/销售订单新建.html ==')
    pg.goto(url('销售管理/销售订单新建.html'))
    pg.wait_for_timeout(300)
    set_select(pg, '.edit-tbl tbody tr:first-child select[data-tax="prod"]', 'LJ-D400 箱盖')
    ex_s = pg.eval_on_selector('.edit-tbl tbody tr:first-child input[data-tax="excl"]', 'el => el.value')
    check('门7 销售·LJ-D400 参考未税销售价带出 48.00', ex_s == '48.00', 'excl=' + ex_s)

    # ============ T4 期段化 · 应收详情 D1 ============
    print('== 财务协同/应收详情.html?id=AR-2026-09-PRJ2601-D1 ==')
    pg.goto(url('财务协同/应收详情.html') + '?id=' + quote('AR-2026-09-PRJ2601-D1'))
    pg.wait_for_timeout(400)
    seg_head = pg.eval_on_selector_all('#detailBody table thead th', 'els => els.map(e=>e.textContent.trim())')
    seg_row = pg.eval_on_selector_all('#detailBody table tbody tr:first-child td', 'els => els.map(e=>e.textContent.trim())')
    check('T4 应收期段化表头（起租日期|止租日期|天数|日租金|小计）',
          seg_head[:2] == ['物料编码', '物料名称'] and '起租日期' in seg_head and '止租日期' in seg_head and '天数' in seg_head and '日租金(元/天)' in seg_head and '小计(元)' in seg_head,
          '|'.join(seg_head))
    check('T4 应收期段化行值（09-01|09-10|10|4,940|2.00|9,880.00）',
          seg_row[3:9] == ['2026-09-01', '2026-09-10', '10', '4,940', '2.00', '9,880.00'], '|'.join(seg_row))

    # ============ T4 期段化 · 应付详情 AP ============
    print('== 财务协同/应付详情.html?id=AP-20260911-013 ==')
    pg.goto(url('财务协同/应付详情.html') + '?id=' + quote('AP-20260911-013'))
    pg.wait_for_timeout(400)
    seg_head2 = pg.eval_on_selector_all('#detailBody table thead th', 'els => els.map(e=>e.textContent.trim())')
    seg_row2 = pg.eval_on_selector_all('#detailBody table tbody tr:first-child td', 'els => els.map(e=>e.textContent.trim())')
    check('T4 应付期段化表头', '起租日期' in seg_head2 and '天数' in seg_head2 and '日租金(元/天)' in seg_head2, '|'.join(seg_head2))
    check('T4 应付期段化行值（08-16|09-03|19|760|1.50|1,140.00）',
          seg_row2[3:9] == ['2026-08-16', '2026-09-03', '19', '760', '1.50', '1,140.00'], '|'.join(seg_row2))

    # ============ 退租入库新建（勾稽行已删） ============
    print('== 租赁管理/退租入库新建.html ==')
    pg.goto(url('租赁管理/退租入库新建.html'))
    body_txt = pg.eval_on_selector('body', 'el => el.textContent')
    check('门7 退租入库新建页无「关联租赁单」', '关联租赁单' not in body_txt)
    ths = pg.eval_on_selector_all('.edit-tbl thead th', 'els => els.map(e=>e.textContent.trim())')
    check('T1 退租入库新建明细编码化', ths[:5] == ['物料编码', '物料名称', '单位', '退回数量', '缺损数量'], '|'.join(ths))

    # ============ 租入归还新建明细 ============
    print('== 租入管理/租入归还新建.html ==')
    pg.goto(url('租入管理/租入归还新建.html'))
    pg.wait_for_timeout(300)
    ths2 = pg.eval_on_selector_all('.edit-tbl thead th', 'els => els.map(e=>e.textContent.trim())')
    tds2 = pg.eval_on_selector_all('#riItemsBody tr:first-child td', 'els => els.map(e=>e.textContent.trim())')
    check('T1 租入归还新建明细编码化（表头）', ths2[:3] == ['物料编码', '物料名称', '单位'], '|'.join(ths2))
    check('T1 租入归还新建明细编码化（行）', tds2[0] == 'WBX-1210L' and tds2[2] == '只', '|'.join(tds2[:4]))

    # ============ 租赁出库录单 计费方式列 ============
    print('== 租赁管理/租赁出库录单.html ==')
    pg.goto(url('租赁管理/租赁出库录单.html'))
    ths3 = pg.eval_on_selector_all('.edit-tbl thead th, table thead th', 'els => els.map(e=>e.textContent.trim())')
    check('T3 租赁出库录单+计费方式列+日租金列头', '计费方式' in ths3 and '日租金(元/天)' in ths3, '|'.join(ths3[:8]))

    if errs:
        print('JS 页面错误：', errs[:5])
    check('全程无页面 JS 错误', not errs, '; '.join(errs[:2]))
    br.close()

n_pass = sum(1 for _, ok, _ in results if ok)
print('=' * 60)
print('PW 断言：%d/%d PASS' % (n_pass, len(results)))
exit(0 if n_pass == len(results) else 1)
