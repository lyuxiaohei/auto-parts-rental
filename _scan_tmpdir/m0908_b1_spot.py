# -*- coding: utf-8 -*-
"""批1 Playwright 抽验：菜单五块结构+选中态+租赁单在租赁管理+待办一级直达+四模块菜单消失+打印出货单+待办15类"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
BASE = 'file:///' + str(PROTO).replace('\\', '/').replace(' ', '%20') + '/'
PASS, FAIL = [], []

def check(name, cond, detail=''):
    (PASS if cond else FAIL).append((name, detail))
    print(('✅' if cond else '❌'), name, detail)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))

    # 1. 租赁单列表（租赁管理组）：五块菜单结构+选中态+open组
    pg.goto(BASE + '租赁管理/租赁单列表.html')
    pg.wait_for_selector('tbody tr')
    groups = pg.eval_on_selector_all('.side-menu > .sm-item.has-sub', 'els=>els.map(e=>e.querySelector(".sm-link").textContent.trim())')
    singles = pg.eval_on_selector_all('.side-menu > .sm-item:not(.has-sub)', 'els=>els.map(e=>e.textContent.trim())')
    check('菜单组序列=采购/销售/租赁/仓储/基础资料/财务应收/财务应付/系统管理', groups == ['基础资料', '采购管理', '销售管理', '租赁管理', '仓储作业', '财务应收', '财务应付', '系统管理'], str(groups))
    check('一级单页=项目看板/我的待办/项目管理/项目损益', [s for s in singles if s] == ['项目看板', '我的待办', '项目管理', '项目损益'], str(singles))
    sel = pg.eval_on_selector_all('.sm-link.selected', 'els=>els.map(e=>e.textContent.trim())')
    check('租赁单列表 selected=租赁单', sel == ['租赁单'], str(sel))
    openg = pg.eval_on_selector_all('.sm-item.has-sub.open', 'els=>els.map(e=>e.querySelector(".sm-link").textContent.trim())')
    check('租赁单列表 open=租赁管理', openg == ['租赁管理'], str(openg))
    menu_txt = pg.eval_on_selector('.side-menu', 'e=>e.textContent')
    for gone in ['组装', '拆卸管理', '退租申请', '丢损赔偿单', '包装管理', '租入单列表旧位']:
        check(f'菜单已无「{gone}」', gone not in menu_txt)
    lease_items = pg.eval_on_selector_all('.sm-item.has-sub', 'els=>els.map(e=>[e.querySelector(".sm-link").textContent.trim(),[...e.querySelectorAll(".sm-sub .sm-link")].map(x=>x.textContent.trim())])')
    lm = dict(lease_items)['租赁管理']
    check('租赁管理组8项=租赁单/租入单/租入入库/组合出库/退租入库/租入归还/在租台账/租出台账',
          lm == ['租赁单', '租入单', '租入入库', '组合出库', '退租入库', '租入归还', '在租台账', '租出台账'], str(lm))
    wh = dict(lease_items)['仓储作业']
    check('仓储作业组6项=库存查询/盘点/盘点录入/库存调拨/其他入库/其他出库',
          wh == ['库存查询', '盘点', '盘点录入', '库存调拨', '其他入库', '其他出库'], str(wh))
    # 2. 我的待办一级直达（根级）
    pg.eval_on_selector('.side-menu .sm-link:text("我的待办")', 'e=>e.onclick()')
    pg.wait_for_timeout(300)
    check('我的待办一级菜单直达根级页面', unquote(pg.url).endswith('/我的待办.html'), unquote(pg.url))
    rows = pg.eval_on_selector_all('#todoBody tr', 'els=>els.length')
    check('我的待办 15 行', rows == 15, str(rows))
    cnt = pg.eval_on_selector('#todoCount', 'e=>e.textContent')
    check('待办计数=15', cnt == '15', cnt)
    chips = pg.eval_on_selector_all('.todo-chip', 'els=>els.map(e=>e.textContent.trim())')
    check('类型速滤无 退租申请/拆卸/丢损赔偿', all(x not in chips for x in ['退租申请', '拆卸', '丢损赔偿']), str(chips))
    sel2 = pg.eval_on_selector_all('.sm-link.selected', 'els=>els.map(e=>e.textContent.trim())')
    check('我的待办页 selected=我的待办', sel2 == ['我的待办'], str(sel2))
    check('待办页 JS 错 0', not errs, str(errs[:3]))

    # 3. 采购入库在采购管理组 + 销售出库在销售管理组（跳转）
    errs.clear()
    pg.goto(BASE + '租赁管理/组合出库列表.html')
    pg.wait_for_selector('tbody tr')
    pg.eval_on_selector('.sm-sub .sm-link:text("采购入库")', 'e=>e.onclick()')
    pg.wait_for_timeout(300)
    check('菜单跳转 采购入库→采购管理/采购入库列表.html', unquote(pg.url).endswith('采购管理/采购入库列表.html'), unquote(pg.url))
    sel3 = pg.eval_on_selector_all('.sm-link.selected', 'els=>els.map(e=>e.textContent.trim())')
    check('采购入库页 selected=采购入库', sel3 == ['采购入库'], str(sel3))
    # 4. 打印出货单文案
    pg.goto(BASE + '租赁管理/组合出库列表.html')
    pg.wait_for_selector('tbody tr')
    ops1 = pg.eval_on_selector_all('tbody tr:first-child .ops a', 'els=>els.map(e=>e.textContent.trim())')
    check('组合出库行含「打印出货单」', '打印出货单' in ops1, str(ops1))
    pg.goto(BASE + '销售管理/销售出库列表.html')
    pg.wait_for_selector('tbody tr')
    ops2 = pg.eval_on_selector_all('tbody tr:first-child .ops a', 'els=>els.map(e=>e.textContent.trim())')
    check('销售出库行含「打印出货单」', '打印出货单' in ops2, str(ops2))
    # 5. 退租入库无申请关联
    pg.goto(BASE + '租赁管理/退租入库列表.html')
    pg.wait_for_selector('tbody tr')
    ths = pg.eval_on_selector_all('thead th', 'els=>els.map(e=>e.textContent.trim())')
    check('退租入库表头无「关联退租申请单号」', '关联退租申请单号' not in ths, str(ths))
    first = pg.eval_on_selector('tbody tr:first-child', 'e=>e.textContent')
    check('退租入库首行无 TZSQ', 'TZSQ' not in first)
    hint = pg.eval_on_selector('.pn-hint', 'e=>e.textContent')
    check('退租入库口径注记=直接录入', hint and '直接录入' in hint and '无申请单' in hint, hint[:40] if hint else '')
    # 6. 四模块页面已删 + 迁移落位（文件系统断言）
    REMOVED = ['租赁管理/退租申请列表.html', '仓储作业/组装列表.html', '仓储作业/组装录单.html',
               '仓储作业/拆卸管理列表.html', '租赁管理/丢损赔偿单.html',
               '租赁管理/弹窗/退租申请详情.html', '租赁管理/弹窗/退租申请审核.html', '租赁管理/弹窗/退租申请新建.html',
               '仓储作业/弹窗/组装单详情.html', '仓储作业/弹窗/拆卸单详情.html', '仓储作业/弹窗/拆卸审核.html',
               '仓储作业/弹窗/拆卸新建.html', '租赁管理/弹窗/丢损赔偿单详情.html', '租赁管理/弹窗/丢损赔偿审核.html']
    for gone in REMOVED:
        check(f'已移除 {gone}', not (PROTO / gone).exists())
    MOVED = ['我的待办.html', '采购管理/采购入库列表.html', '采购管理/采购入库录单.html', '采购管理/弹窗/采购入库单详情.html',
             '销售管理/销售出库列表.html', '销售管理/弹窗/销售出库新建.html', '租赁管理/租赁单列表.html', '租赁管理/弹窗/租赁单详情.html',
             '租赁管理/租入单列表.html', '租赁管理/弹窗/租入单新建.html', '租赁管理/租入入库列表.html', '租赁管理/组合出库列表.html',
             '租赁管理/组合出库录单.html', '租赁管理/退租入库列表.html', '租赁管理/租入归还列表.html', '租赁管理/弹窗/租入归还审核.html']
    for mv in MOVED:
        check(f'已迁至 {mv}', (PROTO / mv).exists())
    # 7. 详情弹窗互溯链改写抽验（点开含退租链的行：角色应为「退租入库」而非「退租申请」）
    pg.goto(BASE + '租赁管理/租赁单列表.html')
    pg.wait_for_selector('tbody tr')
    keys = pg.eval_on_selector_all('tbody a[data-detail-key]', 'els=>els.map(e=>e.getAttribute("data-detail-key"))')
    found_rk, saw_apply = False, False
    for k in keys:
        pg.eval_on_selector(f'tbody a[data-detail-key="{k}"]', 'e=>e.click()')
        pg.wait_for_selector('#detailModal.show')
        roles = pg.eval_on_selector_all('#detailBody .chain .n-role', 'els=>els.map(e=>e.textContent.trim())')
        body_txt = pg.eval_on_selector('#detailBody', 'e=>e.textContent')
        if '退租申请' in body_txt: saw_apply = True
        if '退租入库' in roles: found_rk = True
        pg.eval_on_selector('#detailModal .modal-close', 'e=>e.click()')
        pg.wait_for_timeout(120)
    check('租赁单详情链含「退租入库」角色（至少一条）', found_rk)
    check('全部租赁单详情无「退租申请」残留', not saw_apply)
    check('后段 JS 错 0', not errs, str(errs[:3]))
    b.close()

print(f'==== 批1 抽验：{len(PASS)} 过 / {len(FAIL)} 败 ====')
if FAIL:
    for n, d in FAIL:
        print('  ❌', n, d)
    sys.exit(1)
