# -*- coding: utf-8 -*-
"""G57 Playwright 抽验：≥10 页覆盖 T1–T6 每组≥1 页·JS 错 0·新元素可见·截图存 g57_shots/"""
import io, sys, os
from pathlib import Path
from urllib.parse import quote
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')
SHOTS = ROOT.parent / '_scan_tmpdir' / 'g57_shots'
SHOTS.mkdir(parents=True, exist_ok=True)

PASS, FAIL = [], []

def check(name, cond, note=''):
    (PASS if cond else FAIL).append(f'{name}——{note}')
    print(('PASS ' if cond else 'FAIL ') + name + ' | ' + note)

def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={'width': 1560, 'height': 900})
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)

        def goto(rel, shot=None):
            errs.clear()
            base, _, q = rel.partition('?')
            uri = (ROOT / base).as_uri() + (('?' + q) if q else '')
            pg.goto(uri)
            pg.wait_for_timeout(700)
            if shot:
                pg.screenshot(path=str(SHOTS / shot), full_page=False)
            return errs

        # ---- T1.2 采购入库列表：批量导入/导出 + 弹窗 + toast
        e = goto('采购管理/采购入库列表.html', '01_cgrk_list.png')
        btns = pg.locator('.head-btns button')
        txts = [btns.nth(i).text_content().strip() for i in range(btns.count())]
        check('T1.2 采购入库列表按钮', '批量导入' in txts and '导出' in txts, f'按钮={txts}')
        check('T1.2 JS错0', not e, str(e[:2]))
        pg.click('button:has-text("批量导入")')
        pg.wait_for_timeout(300)
        check('T1.2 导入弹窗打开', pg.locator('#importModal.show').count() == 1, 'importModal.show=1')
        pg.screenshot(path=str(SHOTS / '02_cgrk_import.png'))
        pg.click('#importModal .modal-footer .btn-primary')
        pg.wait_for_timeout(400)
        check('T1.2 确定toast', pg.locator('#g57Toast').is_visible(), pg.locator('#g57Toast').text_content() or '')

        # ---- T1.3 采购退货新建：退库库位列+注记
        e = goto('采购管理/采购退货新建.html', '03_cgth_new.png')
        check('T1.3 退库库位列头', pg.locator('th:has-text("退库库位")').count() == 1, 'th=1')
        check('T1.3 库位select', pg.locator('select.retLoc').count() >= 1, f'{pg.locator("select.retLoc").count()}个')
        check('T1.3 灰字注记', '工人按所选库位出货' in pg.locator('.pn-hint').first.text_content(), '注记在')
        check('T1.3 JS错0', not e, str(e[:2]))

        # ---- T2 采购订单列表：新列
        e = goto('采购管理/采购订单列表.html', '04_cgdd_list.png')
        ths = [pg.locator('thead th').nth(i).text_content().strip() for i in range(pg.locator('thead th').count())]
        check('T2 采购订单列头', '供应商订单号' in ths and '创建日期' in ths, f'th={ths[-4:]}')
        cell = pg.locator('tbody tr').first.locator('td').nth(11).text_content().strip()
        check('T2 采购订单外订号值', cell == 'GYS-240902-11', cell)
        check('T2 JS错0', not e, str(e[:2]))

        # ---- T2 销售订单新建：客户订单号字段
        e = goto('销售管理/销售订单新建.html')
        check('T2 销售订单新建客户订单号', pg.locator('.form-label:has-text("客户订单号")').count() == 1, '字段在')
        check('T2 JS错0(销售订单新建)', not e, str(e[:2]))

        # ---- T2.7 销售出库新建：超订单校验
        e = goto('销售管理/销售出库新建.html', '05_xsck_over.png')
        pg.wait_for_timeout(500)
        check('T2.7 超订单红字', pg.locator('.g57-over').count() >= 1, pg.locator('.g57-over').first.text_content() if pg.locator('.g57-over').count() else '无')
        qi = pg.locator('input[data-tax="qty"]').first
        check('T2.7 数量红框', '255, 77, 79' in (qi.evaluate('el=>getComputedStyle(el).borderColor') or ''), qi.evaluate('el=>getComputedStyle(el).borderColor'))
        pg.click('.submit-bar button:has-text("提交审核")')
        pg.wait_for_timeout(300)
        check('T2.7 提交toast', pg.locator('#g57Toast').is_visible() and '存在超量行' in (pg.locator('#g57Toast').text_content() or ''), 'toast出')
        check('T2.7 JS错0', not e, str(e[:2]))

        # ---- T2/T3 租赁单列表：客户订单号+创建日期
        e = goto('租赁管理/租赁单列表.html', '06_zld_list.png')
        ths = [pg.locator('thead th').nth(i).text_content().strip() for i in range(pg.locator('thead th').count())]
        check('T3 租赁单列头', '客户订单号' in ths and '创建日期' in ths, f'th={ths[-4:]}')
        check('T3 JS错0', not e, str(e[:2]))

        # ---- T3.8 复制 op → 录单带参
        e = goto('租赁管理/租赁出库列表.html', '07_zlck_list.png')
        pg.wait_for_timeout(500)
        # 复制在⋮菜单内：打开第一行⋮
        pg.locator('a.op-more').first.click()
        pg.wait_for_timeout(300)
        menu_copy = pg.locator('.ops-menu a:has-text("复制"), body > div a:has-text("复制")')
        check('T3.8 ⋮菜单含复制', pg.evaluate("()=>[...document.querySelectorAll('a')].some(a=>a.textContent.trim()==='复制')"), '菜单有复制')
        pg.keyboard.press('Escape')
        e = goto('租赁管理/租赁出库录单.html?copy=CK-20260824-009', '08_zlck_copy.png')
        pg.wait_for_timeout(600)
        banner = pg.locator('.content .pn-hint').first.text_content()
        check('T3.8 复制banner', banner and '复制生成新批次·仅改数量/明细' in banner, (banner or '')[:40])
        check('T3.8 明细带出', pg.locator('#detailTable tbody tr, .edit-tbl tbody tr').count() >= 1, '明细行≥1')
        check('T3.8 JS错0', not e, str(e[:2]))

        # ---- T3.9/T5.14 库存查询
        e = goto('仓储作业/库存查询.html', '09_kccx.png')
        pg.locator('a:has-text("客户在租")').first.click()
        pg.wait_for_timeout(400)
        check('T3.9 客户筛选下拉', pg.locator('#g57RentCust').count() == 1, '下拉在')
        pg.select_option('#g57RentCust', '华骏重卡汽车有限公司')
        pg.wait_for_timeout(300)
        vis = pg.locator('#rentDrillModal tbody tr').first.is_visible()
        check('T3.9 筛选生效', vis, '华骏行可见')
        pg.screenshot(path=str(SHOTS / '10_kccx_custfilter.png'))
        pg.click('#rentDrillModal .modal-close')
        pg.wait_for_timeout(300)
        # 库位明细（LJ 行）
        ljrow = pg.locator('tbody tr', has_text='LJ-A100').first
        ljrow.locator('a:has-text("库位明细")').click()
        pg.wait_for_timeout(400)
        check('T5.14 库位明细弹窗', pg.locator('#locDrillModal.show').count() == 1 and 'LJ-A100' in (pg.locator('#locDrillCap').text_content() or ''), pg.locator('#locDrillCap').text_content() or '')
        pg.screenshot(path=str(SHOTS / '11_kccx_locdrill.png'))
        check('T3.9/T5.14 JS错0', not e, str(e[:2]))

        # ---- T4.11 退租登记两步
        e = goto('租赁管理/退租入库新建.html', '12_tz_two_step.png')
        check('T4.11 Step1选客户', pg.locator('.card-title:has-text("第一步")').count() == 1, '第一步卡在')
        check('T4.11 Step2出库单表', pg.locator('#g57TzOrders tr').count() >= 1, f'{pg.locator("#g57TzOrders tr").count()}单')
        check('T4.11 页顶注记', '多次退租从多个出库单分别登记' in pg.content() and '应收账单照常生成' in pg.content(), '两条注记在')
        pg.locator('#g57TzOrders a:has-text("选择")').nth(1).click()
        pg.wait_for_timeout(300)
        check('T4.11 选单带明细', pg.locator('#tzItems tbody tr, #tzItems tr').count() >= 1, '明细带出')
        check('T4.11 JS错0', not e, str(e[:2]))

        # ---- T4.11/12 退租入库列表
        e = goto('租赁管理/退租入库列表.html', '13_tz_list.png')
        btns = [pg.locator('.head-btns button').nth(i).text_content().strip() for i in range(pg.locator('.head-btns button').count())]
        check('T4.11 列表无新建', '新建' not in btns and '批量审核' in btns, f'按钮={btns}')
        pg.locator('button:has-text("批量审核")').click()
        pg.wait_for_timeout(300)
        check('T4.12 批量审核toast', pg.locator('#g57Toast').is_visible(), pg.locator('#g57Toast').text_content() or '')
        check('T4.11/12 JS错0', not e, str(e[:2]))

        # ---- T4.12 退租详情：清洗完工+时间线
        e = goto('租赁管理/退租入库详情.html?id=TZRK-20260902-010', '14_tz_detail.png')
        pg.wait_for_timeout(600)
        check('T4.12 清洗完工按钮', pg.locator('button:has-text("清洗完工")').count() == 1, '按钮在')
        check('T4.12 时间线清洗节点', '清洗完工' in pg.content() and '转可用库存' in pg.content(), '节点在')
        pg.locator('button:has-text("清洗完工")').click()
        pg.wait_for_timeout(300)
        check('T4.12 清洗toast', pg.locator('#g57Toast').is_visible(), 'toast出')
        check('T4.12 JS错0', not e, str(e[:2]))

        # ---- T5.13 收发存
        e = goto('仓储作业/收发存.html', '15_sfs.png')
        pg.wait_for_timeout(600)
        ths = [pg.locator('thead th').nth(i).text_content().strip() for i in range(pg.locator('thead th').count())]
        check('T5.13 收发存列', ths[:8] == ['物料', '物料类型', '期初', '本期入库', '本期出库', '转移', '期末结存', '操作'], f'th={ths}')
        rows = pg.locator('#sfsBody tr').count()
        check('T5.13 汇总行实算', rows >= 5, f'{rows}行')
        check('T5.13 口径注记', '退租关联闭环后数据完整' in pg.content(), '注记在')
        pg.locator('#sfsBody a:has-text("轨迹")').first.click()
        pg.wait_for_timeout(400)
        check('T5.13 轨迹弹窗', pg.locator('#sfsTrackModal.show').count() == 1, '弹窗开')
        pg.screenshot(path=str(SHOTS / '16_sfs_track.png'))
        check('T5.13 JS错0', not e, str(e[:2]))

        # ---- T6.15/16 客商管理/新建
        e = goto('基础数据/客商管理.html', '17_ksgl.png')
        pg.wait_for_timeout(500)
        ths = [pg.locator('thead th').nth(i).text_content().strip() for i in range(pg.locator('thead th').count())]
        check('T6.15 供应商类型列', '供应商类型' in ths, f'th={ths}')
        cell = pg.locator('tbody tr', has_text='DW-0201').first.locator('td').nth(4).text_content().strip()
        check('T6.15 环通行值', '租赁供应商' == cell, cell)
        check('T6.15 JS错0', not e, str(e[:2]))
        e = goto('基础数据/客商新建.html', '18_ks_new.png')
        check('T6.16 协议税点chips', pg.locator('.g57-chip[data-v="9%"]').count() >= 1 and pg.locator('.g57-chip[data-v="13%"]').count() >= 1, '税点chips')
        check('T3.10 结算口径radio', pg.locator('#g57SettleRow .radio').count() == 2, 'radio两值')
        pg.select_option('#ksTypeSel', '供应商')
        pg.wait_for_timeout(300)
        check('T6.15 供应商类型chips联动', pg.locator('#g57SupTypeRow').is_visible(), '选供应商显chips')
        check('T6 JS错0', not e, str(e[:2]))

        # ---- T6.15 客商详情（partners 三卡新行）
        e = goto('基础数据/客商详情.html?id=DW-0101')
        pg.wait_for_timeout(600)
        check('T6.15 详情供应商类型行', '供应商类型' in pg.content() and '租赁供应商 / 采购供应商' in pg.content(), '行在')
        check('T6.16 详情协议税点行', '协议税点' in pg.content(), '行在')
        e2 = goto('基础数据/客商详情.html?id=DW-0003')
        pg.wait_for_timeout(600)
        check('T3.10 详情结算口径行', '结算口径' in pg.content() and '按转移结算' in pg.content(), '星途=按转移结算')
        check('T6 详情JS错0', not e and not e2, str((e + e2)[:2]))

        # ---- T2 租入单列表
        e = goto('租入管理/租入单列表.html')
        ths = [pg.locator('thead th').nth(i).text_content().strip() for i in range(pg.locator('thead th').count())]
        check('T2 租入单列头', '供应商订单号' in ths and '创建日期' in ths, f'th={ths[-3:]}')
        check('T2 租入JS错0', not e, str(e[:2]))

        # ---- 菜单抽验：收发存入口+退租登记改名
        e = goto('仓储作业/盘点列表.html')
        check('菜单 收发存入口', pg.locator('.sm-link:has-text("收发存")').count() == 1, '入口在')
        check('菜单 退租登记', pg.locator('.sm-link:has-text("退租登记")').count() == 1 and pg.locator('.sm-link:has-text("退租入库")').count() == 0, '改名成')

        browser.close()

    print('\n===== PW 抽验汇总 =====')
    print(f'{len(PASS)} PASS / {len(FAIL)} FAIL')
    for f in FAIL:
        print('FAIL项:', f)
    shots = sorted(os.listdir(SHOTS))
    print(f'截图 {len(shots)} 张:', shots)

run()
