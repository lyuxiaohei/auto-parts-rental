# -*- coding: utf-8 -*-
"""批2 Playwright 抽验：产品档案（分类/归属权/税率区/12行）+ 菜单 + 六角色 + 客商供应商 + 虚拟仓 + 审核人行"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

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

    # 1. 产品档案页
    pg.goto(BASE + '基础数据/产品档案.html')
    pg.wait_for_selector('tbody tr')
    check('页面标题=产品档案', pg.title().startswith('产品档案'), pg.title())
    sel = pg.eval_on_selector_all('.sm-link.selected', 'els=>els.map(e=>e.textContent.trim())')
    check('selected=产品档案', sel == ['产品档案'], str(sel))
    ths = pg.eval_on_selector_all('thead th', 'els=>els.map(e=>e.textContent.trim())')
    check('表头含 产品编码/产品名称/分类/归属权', all(x in ths for x in ['产品编码', '产品名称', '分类', '归属权']), str(ths))
    check('表头列序：租金单价在状态前', ths.index('租金单价(元/天)') < ths.index('状态'), '')
    rows = pg.evaluate("document.querySelectorAll('.table-wrap')[0].querySelectorAll('tbody tr').length")
    check('12 行（6 器具+6 组件）', rows == 12, str(rows))
    body = pg.eval_on_selector('tbody', 'e=>e.textContent')
    check('含组件行 LJ-A100', 'LJ-A100' in body and '组件' in body)
    check('含归属权 租入-路凯', '租入-路凯' in body)
    check('供应商税率维护区存在', pg.eval_on_selector_all('.card-title', 'els=>els.map(e=>e.textContent.trim())').__contains__('供应商税率维护'))
    tax_rows = pg.eval_on_selector_all('.card:nth-of-type(2) tbody tr', 'els=>els.length') if False else None
    hint = pg.eval_on_selector_all('.pn-hint', 'els=>els.map(e=>e.textContent)')
    check('税率口径注记（同产品不同供应商）', any('供应商维护不同税率' in h for h in hint), str(hint)[:80])
    # 分类筛选含组件
    sel_opts = pg.eval_on_selector_all('.filter-card select:first-of-type option', 'els=>els.map(e=>e.textContent)')
    check('分类筛选选项含料架/组件', any('组件' in o for o in sel_opts), str(sel_opts))
    # 详情弹窗（首行 LJ-A100 前? 详情锚点）
    pg.eval_on_selector('tbody a[data-detail-key]', 'e=>e.click()')
    pg.wait_for_selector('#detailModal.show')
    ttl = pg.eval_on_selector('#detailTitle', 'e=>e.textContent')
    check('详情标题=产品详情', '产品详情' in ttl, ttl)
    info_txt = pg.eval_on_selector('#detailBody', 'e=>e.textContent')
    check('详情含 归属权/分类 字段', '归属权' in info_txt and '分类' in info_txt)
    pg.eval_on_selector('#detailModal .modal-close', 'e=>e.click()')
    # 菜单无零部件档案
    menu = pg.eval_on_selector('.side-menu', 'e=>e.textContent')
    check('菜单无「零部件档案」', '零部件档案' not in menu)
    check('菜单含「产品档案」', '产品档案' in menu)
    check('JS 错 0', not errs, str(errs[:2]))

    # 2. 用户权限六角色
    errs.clear()
    pg.goto(BASE + '系统管理/用户权限.html')
    pg.wait_for_selector('tbody tr')
    roles = pg.eval_on_selector_all('tbody tr td:nth-child(4)', 'els=>els.map(e=>e.textContent.trim())')
    check('六角色齐（财务/商务/物流/三主管）', all(r in roles for r in ['财务', '商务', '物流', '财务主管', '商务主管', '物流主管']), str(roles))
    sides = pg.eval_on_selector_all('tbody tr td:nth-child(5)', 'els=>els.map(e=>e.textContent.trim())')
    check('所属方无运营方·含供应商', '运营方' not in str(sides) and '供应商' in str(sides), str(sides))
    page_txt = pg.eval_on_selector('body', 'e=>e.textContent')
    check('页面无运营方字样', '运营方' not in page_txt)
    role_opts = pg.eval_on_selector_all('.filter-card select:nth-of-type(1) option', 'els=>els.map(e=>e.textContent)')
    check('角色筛选含六角色', all(o in role_opts for o in ['财务主管', '商务主管', '物流主管']), str(role_opts))
    # 角色管理弹窗
    pg.eval_on_selector("button[onclick=\"openModal('roleModal')\"]", 'e=>e.click()')
    pg.wait_for_selector('#roleModal.show')
    rrows = pg.eval_on_selector_all('#roleModal tbody tr td:first-child', 'els=>els.map(e=>e.textContent.trim())')
    check('角色表含六角色+供应商账号', all(r in rrows for r in ['财务主管', '物流主管', '供应商账号']), str(rrows))
    check('JS 错 0', not errs, str(errs[:2]))

    # 3. 客商管理
    errs.clear()
    pg.goto(BASE + '基础数据/客商管理.html')
    pg.wait_for_selector('tbody tr')
    stabs = pg.eval_on_selector_all('.stabs .stab', 'els=>els.map(e=>e.childNodes[0].textContent.trim()+":"+e.querySelector(".stab-count").textContent)')
    check('客商机签 全部8/客户4/供应商4·无运营方', stabs == ['全部:8', '客户:4', '供应商:4'], str(stabs))
    rows = pg.eval_on_selector_all('tbody tr', 'els=>els.length')
    check('客商 8 行', rows == 8, str(rows))
    body = pg.eval_on_selector('tbody', 'e=>e.textContent')
    check('路凯行为供应商类型', '路凯' in body and '运营方' not in body.replace('运营方角色已去掉', ''))

    # 4. 库位档案虚拟仓 + 库存查询虚拟仓
    errs.clear()
    pg.goto(BASE + '基础数据/库位档案.html')
    pg.wait_for_selector('tbody tr')
    rows = pg.eval_on_selector_all('tbody tr', 'els=>els.length')
    check('库位档案 11 行（+虚拟仓）', rows == 11, str(rows))
    body = pg.eval_on_selector('tbody', 'e=>e.textContent')
    check('含 安吉智行客户虚拟仓·类型虚拟仓', 'XNC-AJZX' in body and '虚拟仓' in body and '安吉智行' in body)
    # 详情弹窗首行=虚拟仓
    pg.eval_on_selector('tbody a[data-detail-key]', 'e=>e.click()')
    pg.wait_for_selector('#detailModal.show')
    ttl = pg.eval_on_selector('#detailTitle', 'e=>e.textContent')
    check('库位详情标题含 XNC-AJZX', 'XNC-AJZX' in ttl, ttl)
    dbody = pg.eval_on_selector('#detailBody', 'e=>e.textContent')
    check('库位详情含 on-hire 口径', 'on-hire' in dbody)
    pg.eval_on_selector('#detailModal .modal-close', 'e=>e.click()')

    pg.goto(BASE + '仓储作业/库存查询.html')
    pg.wait_for_selector('tbody tr')
    body = pg.eval_on_selector('tbody', 'e=>e.textContent')
    check('库存查询含客户虚拟仓行', 'XNC-AJZX-WBX' in body and '安吉智行' in body)
    rows = pg.evaluate("[...document.querySelectorAll('tbody')].find(t=>t.textContent.indexOf('XNC-AJZX-WBX')>-1).querySelectorAll('tr').length")
    check('库存查询 10 行（+虚拟仓）', rows == 10, str(rows))
    hints = pg.eval_on_selector_all('.pn-hint', 'els=>els.map(e=>e.textContent)')
    check('虚拟仓口径注记存在', any('客户虚拟仓' in h for h in hints), '')
    check('JS 错 0', not errs, str(errs[:2]))

    # 5. 审核弹窗审核人行（租赁单审核·商务主管）
    errs.clear()
    pg.goto(BASE + '租赁管理/弹窗/租赁单审核.html')
    pg.wait_for_selector('#auditModal.show')
    body = pg.eval_on_selector('#auditModal', 'e=>e.textContent')
    check('租赁单审核含 审核人·商务主管·王琳', '审核人' in body and '商务主管' in body and '王琳' in body)
    pg.goto(BASE + '财务协同/弹窗/付款确认.html')
    pg.wait_for_selector('.modal-overlay.show')
    body = pg.eval_on_selector('.modal-overlay.show', 'e=>e.textContent')
    check('付款确认含 审核人·财务主管·周敏', '财务主管' in body and '周敏' in body)
    pg.goto(BASE + '采购管理/弹窗/采购入库审核.html')
    pg.wait_for_selector('.modal-overlay.show')
    body = pg.eval_on_selector('.modal-overlay.show', 'e=>e.textContent')
    check('采购入库审核含 审核人·物流主管·李国栋', '物流主管' in body and '李国栋' in body)
    check('JS 错 0', not errs, str(errs[:2]))
    b.close()

print(f'==== 批2 抽验：{len(PASS)} 过 / {len(FAIL)} 败 ====')
if FAIL:
    for n, d in FAIL:
        print('  ❌', n, d)
    sys.exit(1)
