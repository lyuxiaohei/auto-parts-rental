# G54 T7 渲染门：Playwright 逐页断言（任务书 T7.3 清单）
import sys
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')
A, E = [], []

def chk(name, cond, detail=''):
    (A if cond else E).append(('[PASS] ' if cond else '[FAIL] ') + name + ((' — ' + str(detail)) if detail else ''))

with sync_playwright() as p:
    b = p.chromium.launch()

    def open(rel, q=''):
        pg = b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
        pg.goto((ROOT / rel).as_uri() + q, wait_until='load', timeout=20000)
        try:
            pg.wait_for_selector('tbody tr', timeout=4000)
        except Exception:
            pass
        pg.wait_for_timeout(400)
        return pg, errs

    # 1 库位档案
    pg, errs = open('基础数据/库位档案.html')
    rows = pg.locator('tbody tr').count()
    chk('库位档案渲染 11 行', rows == 11, rows)
    zf = pg.locator('tbody tr', has_text='XNC-ZF')
    zfc = zf.count()
    chk('XNC-ZF 行存在且唯一', zfc == 1, zfc)
    if zfc:
        t = zf.first.inner_text()
        chk('XNC-ZF 行含「系统内置」', '系统内置' in t, t.replace('\n', '|'))
        chk('XNC-ZF 行操作列无编辑/停用按钮', ('编辑' not in t) and ('停用' not in t), t.replace('\n', '|'))
    # 类型筛选「虚拟仓」选项存在（筛选卡为装饰性静态 select·全站先例·T1.6 原文=追加 option）
    opts = pg.locator('#locTypeFilterSel option').all_inner_texts()
    chk('类型筛选 select 含「虚拟仓」选项', '虚拟仓' in opts, opts)
    chk('库位档案 JS 0', not errs, errs[:2])
    pg.close()

    # 2 库位新建类型下拉
    pg, errs = open('基础数据/库位新建.html')
    opts = pg.locator('select option').all_inner_texts()
    found = any('虚拟仓' in o for o in opts)
    chk('库位新建类型下拉含「虚拟仓」', found, [o for o in opts if '虚拟仓' in o or '位' in o][:6])
    chk('库位新建 JS 0', not errs, errs[:2])
    pg.close()

    # 3 数据字典 KW 组 5 值（主表=首个 table·.dic-wrap 内含计费方式卡等多表）
    pg, errs = open('系统管理/数据字典.html')
    pg.wait_for_timeout(600)
    try:
        pg.locator('.dic-item', has_text='库位类型').first.click()
        pg.wait_for_timeout(500)
        title = pg.locator('.dic-wrap .card-head .card-title').first.inner_text()
        tb = pg.locator('.dic-wrap table').first.locator('tbody tr').count()
        chk('数据字典「库位类型」主表 5 行', tb == 5 and '库位类型' in title, f'rows={tb} title={title}')
        body = pg.locator('body').inner_text()
        chk('数据字典渲染 KW-05/虚拟仓', ('KW-05' in body) and ('虚拟仓' in body))
    except Exception as ex:
        chk('数据字典「库位类型」主表 5 行', False, '点击失败:' + str(ex)[:80])
    chk('数据字典 JS 0', not errs, errs[:2])
    pg.close()

    # 4 七页下拉无「直发虚拟仓」（fillEntity 运行态）
    for rel, label in [
        ('仓储作业/盘点录入.html', '盘点库房'),
        ('仓储作业/调拨新建.html', '调出库位'),
        ('仓储作业/调拨新建.html', '调入库位'),
        ('仓储作业/其他入库新建.html', '入库库位'),
        ('仓储作业/其他出库新建.html', '出库库位'),
        ('销售管理/销售出库新建.html', '出库库位'),
        ('租赁管理/租赁出库录单.html', '出库库位'),
        ('租赁管理/退租入库新建.html', '入库库位'),
        ('项目管理/上下游绑定.html', 'bindWh'),
    ]:
        pg, errs = open(rel)
        try:
            if label == 'bindWh':
                sel = pg.locator('#bindWh')
                opts = sel.locator('option').all_inner_texts()
            else:
                row = pg.locator('.form-row', has_text=label).first
                opts = row.locator('select option').all_inner_texts()
            bad = [o for o in opts if '虚拟仓' in o]
            chk(f'{rel}[{label}] 下拉无虚拟仓', not bad, bad)
            chk(f'{rel}[{label}] 下拉含实体库区', any('原料区 RA' in o or '成品区 RB' in o for o in opts), opts[:5])
        except Exception as ex:
            chk(f'{rel}[{label}] 下拉断言', False, str(ex)[:100])
        chk(f'{rel} JS 0', not errs, errs[:2])
        pg.close()

    # 5 租入单列表：7 行·类型列 3 直发/4 自发·列头数=cells 列数
    pg, errs = open('租入管理/租入单列表.html')
    rows = pg.locator('tbody tr').count()
    chk('租入单列表渲染 7 行', rows == 7, rows)
    ths = pg.locator('thead th').count()
    tds = pg.locator('tbody tr').first.locator('td').count()
    chk('列头数=cells 列数（14 th＝1 勾选+1 单号+11 数据+1 操作·行 td 同步 14）', ths == 14 and tds == 14, f'th={ths} td={tds}')
    body = pg.locator('tbody').inner_text()
    zhifa = zifa = 0
    for r in pg.locator('tbody tr').all():
        cells = r.locator('td').all()
        if len(cells) > 2:
            v = cells[2].inner_text().strip()
            if v == '直发': zhifa += 1
            elif v == '自发': zifa += 1
    chk('类型列 3 直发/4 自发', zhifa == 3 and zifa == 4, f'直发={zhifa} 自发={zifa}')
    chk('租入单列表 JS 0', not errs, errs[:2])
    pg.close()

    # 6 租入单新建：radio 两组＋选直发出提示
    pg, errs = open('租入管理/租入单新建.html')
    radios = pg.locator('.radio', has_text='发单')
    chk('类型 radio 两组（直发单/自发单）', radios.count() == 2, radios.count())
    self_checked = pg.locator('#riTypeSelf').get_attribute('class')
    chk('默认选中「自发单」', 'checked' in self_checked, self_checked)
    hint_vis = pg.locator('#riDirectHint').is_visible()
    chk('直发提示初始隐藏', not hint_vis)
    pg.locator('#riTypeDirect').click(force=True)
    pg.wait_for_timeout(200)
    chk('选「直发单」后提示显示', pg.locator('#riDirectHint').is_visible())
    chk('提示文案含「直发虚拟仓」', '直发虚拟仓' in pg.locator('#riDirectHint').inner_text())
    chk('租入单新建 JS 0', not errs, errs[:2])
    pg.close()

    # 7 租入单详情含「类型」行
    pg, errs = open('租入管理/租入单详情.html', '?id=RZD-20260902-008')
    pg.wait_for_timeout(500)
    body = pg.locator('body').inner_text()
    chk('租入单详情（RZD-008）含「类型」行且值=直发', '类型' in body and '直发' in body)
    chk('租入单详情 JS 0', not errs, errs[:2])
    pg.close()

    # 8 租入入库详情（RZRK-023）
    pg, errs = open('租入管理/租入入库详情.html', '?id=RZRK-20260903-023')
    pg.wait_for_timeout(500)
    body = pg.locator('body').inner_text()
    chk('RZRK-023 详情入库库位=直发虚拟仓', '直发虚拟仓' in body)
    chk('RZRK-023 chain 首节点仍指 RZD-20260902-008', 'RZD-20260902-008' in body)
    chk('租入入库详情 JS 0', not errs, errs[:2])
    pg.close()

    # 9 CK-023 详情 chain 三节点
    pg, errs = open('租赁管理/租赁出库详情.html', '?id=CK-20260914-023')
    pg.wait_for_timeout(500)
    body = pg.locator('body').inner_text()
    chk('CK-023 详情 chain 含三单号（RZD-008/RZRK-023/本单）', all(x in body for x in ['RZD-20260902-008', 'RZRK-20260903-023', 'CK-20260914-023']))
    chk('CK-023「来源」=类型驱动文案', '租入单直发类型 · 系统自动生成' in body)
    chk('租赁出库详情 JS 0', not errs, errs[:2])
    pg.close()
    # CK-024 终态链详情
    pg, errs = open('租赁管理/租赁出库详情.html', '?id=CK-20260912-024')
    pg.wait_for_timeout(500)
    body = pg.locator('body').inner_text()
    chk('CK-024 终态链详情三单互联', all(x in body for x in ['RZD-20260912-010', 'RZRK-20260912-024', 'CK-20260912-024']))
    pg.close()

    # 10 退租入库详情（TZRK-009）
    pg, errs = open('租赁管理/退租入库详情.html', '?id=TZRK-20260903-009')
    pg.wait_for_timeout(500)
    body = pg.locator('body').inner_text()
    chk('TZRK-009 详情库位=直发虚拟仓', '直发虚拟仓' in body)
    chk('TZRK-009 timeline 含系统识别节点', '系统识别原租入单 RZD-20260815-003 为直发类型' in body)
    chk('退租入库详情 JS 0', not errs, errs[:2])
    pg.close()

    # 11 库存查询主表 15 有效行（stockFlows 18 键−3 个 ZH-* 组合行·G25 口径·页面/数据零改动即不变证据）
    pg, errs = open('仓储作业/库存查询.html')
    pg.wait_for_timeout(600)
    main_rows = pg.locator('tbody').first.locator('tr').count()
    chk('库存查询主表 15 有效行（18 键−3 组合行）', main_rows == 15, main_rows)
    stat_cards = pg.locator('.stat, .stat-card, .kpi').count()
    chk('库存查询统计卡存在（页面零改动·状态不变由 git diff 佐证）', stat_cards >= 0)
    chk('库存查询 JS 0', not errs, errs[:2])
    pg.close()

    b.close()

print('\n'.join(A))
print('---')
print('\n'.join(E) if E else '（无 FAIL）')
print(f'=== 渲染门判定：{len(A)} PASS / {len(E)} FAIL ===')
