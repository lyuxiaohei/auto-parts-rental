# -*- coding: utf-8 -*-
"""G13 冒烟：改动页逐页关键断言（JS 错 0 + 新功能生效）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

PROTO = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
fails = []

def page(pw, rel):
    pg = pw.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
    pg.on('console', lambda m: errs.append(m.text[:150]) if m.type == 'error' else None)
    pg.goto((PROTO / rel).as_uri(), wait_until='load')
    pg.wait_for_timeout(400)
    return pg, errs

def chk(name, ok, detail=''):
    print(('✅' if ok else '❌'), name, '|', detail)
    if not ok:
        fails.append(name)

with sync_playwright() as pw:
    browser = pw.chromium.launch()

    # 库存查询：13 行 / 13 列 / 筛选
    pg, errs = page(browser, "仓储作业/库存查询.html")
    chk('库存查询 JS错0', not errs, str(errs[:2]))
    n = pg.locator('tbody:nth-of-type(1)').first.locator('tr').count()
    th = pg.locator('tbody:nth-of-type(1)').first.evaluate("tb => tb.closest('table').querySelectorAll('thead th').length")
    chk('库存查询 13行/13列', n == 13 and th == 13, f'rows={n} th={th}')
    pg.locator('.filter-card select').first.evaluate("el => { el.value='客户端(转租)'; }")
    pg.evaluate("[...document.querySelectorAll('.filter-actions button')].find(b=>b.textContent.trim()==='查询').click()")
    pg.wait_for_timeout(150)
    n2 = pg.locator('tbody:nth-of-type(1)').first.locator('tr').count()
    chk('库存查询 转租筛选 13→3', n2 == 3, f'{n2} 行')
    pg.locator('.filter-card input').first.evaluate("el => { el.value='WBX'; }")
    pg.locator('.filter-card select').first.evaluate("el => { el.selectedIndex=0; }")
    pg.evaluate("[...document.querySelectorAll('.filter-actions button')].find(b=>b.textContent.trim()==='查询').click()")
    pg.wait_for_timeout(150)
    n3 = pg.locator('tbody:nth-of-type(1)').first.locator('tr').count()
    chk('库存查询 编码筛选 WBX=4', n3 == 4, f'{n3} 行')
    chk('库存查询 成本列文本', '340.00' in pg.locator('tbody:nth-of-type(1)').first.text_content())
    pg.close()

    # 租赁单列表：9 行+退回对比 op+cmpModal
    pg, errs = page(browser, "租赁管理/租赁单列表.html")
    chk('租赁单列表 JS错0', not errs, str(errs[:2]))
    n = pg.locator('tbody').first.locator('tr').count()
    cmp_ops = pg.locator('tbody a', has_text='退回对比').count()
    chk('租赁单列表 9行+退回对比9', n == 9 and cmp_ops == 9, f'rows={n} cmp={cmp_ops}')
    pg.evaluate("openModal('cmpModal')")
    chk('租赁单列表 cmpModal 打开', pg.locator('#cmpModal').evaluate("el=>el.classList.contains('show')"))
    pg.evaluate("closeModal('cmpModal')")
    chk('租赁单列表 计费方式radio', pg.locator('#createModal', has_text='计费方式').count() == 1 and pg.locator('#createModal .radio', has_text='按次套数对账').count() >= 1)
    chk('租赁单列表 库存提示条', pg.locator('#createModal #stockWarn').count() == 1)
    pg.close()

    # 租入单列表：6 行+stab+草稿行三步 op+toast
    pg, errs = page(browser, "租赁管理/租入单列表.html")
    chk('租入单列表 JS错0', not errs, str(errs[:2]))
    n = pg.locator('tbody').first.locator('tr').count()
    stab = pg.locator('.stabs .stab', has_text='新建(草稿)').locator('.stab-count').text_content()
    chk('租入单列表 6行+草稿stab=1', n == 6 and stab.strip() == '1', f'rows={n} stab={stab}')
    pg.locator('tbody a', has_text='选供应商').first.evaluate("el => el.click()")
    pg.wait_for_timeout(120)
    chk('租入单列表 草稿行toast', pg.locator('#g13Toast').count() == 1 and pg.locator('#g13Toast').is_visible())
    pg.close()

    # 租入归还列表：关联同步
    pg, errs = page(browser, "租赁管理/租入归还列表.html")
    chk('租入归还列表 JS错0', not errs, str(errs[:2]))
    rows0 = pg.locator('#riItemsBody tr').count()
    pg.locator('#riSelect').evaluate("el => { el.selectedIndex = 1; el.dispatchEvent(new Event('change', {bubbles:true})); }")
    pg.wait_for_timeout(120)
    rows1 = pg.locator('#riItemsBody tr').count()
    txt = pg.locator('#riItemsBody').text_content()
    chk('租入归还 关联同步 明细行>0', rows0 >= 1 and rows1 >= 1 and '租入数量' not in txt and ('围板箱' in txt or '托盘' in txt), f'默认{rows0}行→切换后{rows1}行: {txt[:50]!r}')
    chk('租入归还 分批注记', '支持分批' in pg.locator('#createModal').text_content())
    pg.close()

    # 弹窗/租入归还新建（独立模板回退）
    pg, errs = page(browser, "租赁管理/弹窗/租入归还新建.html")
    chk('租入归还新建模板 JS错0', not errs, str(errs[:2]))
    chk('租入归还新建模板 明细回退', pg.locator('#riItemsBody tr').count() >= 1)
    pg.close()

    # 我的待办：审核人筛选
    pg, errs = page(browser, "我的待办.html")
    chk('我的待办 JS错0', not errs, str(errs[:2]))
    n = pg.locator('#todoBody tr').count()
    pg.locator('#todoAuditor').evaluate("el => { el.value='王琳'; el.dispatchEvent(new Event('change',{bubbles:true})); }")
    pg.wait_for_timeout(120)
    n2 = pg.locator('#todoBody tr:visible').count()
    chk('我的待办 审核人筛选 12→2', n == 12 and n2 == 2, f'{n}→{n2}')
    pg.close()

    # 应收账单：14 行+usage 行
    pg, errs = page(browser, "财务协同/应收账单.html")
    chk('应收账单 JS错0', not errs, str(errs[:2]))
    n = pg.locator('tbody').first.locator('tr').count()
    usage = pg.locator('tbody tr', has_text='按实际使用量').count()
    chk('应收账单 14行+usage1', n == 14 and usage == 1, f'rows={n} usage={usage}')
    chk('应收账单 生成方式radio', pg.locator('#createModal .radio', has_text='按实际使用量').count() >= 1)
    pg.close()

    # 付款登记：付款方式×2 弹窗
    pg, errs = page(browser, "财务协同/付款登记.html")
    chk('付款登记 JS错0', not errs, str(errs[:2]))
    n = pg.locator('select', has_text='承兑').count()
    chk('付款登记 付款方式下拉(新建)=1', n == 1, f'{n}')
    chk('付款确认 付款方式行', '付款方式' in pg.locator('#auditModal').text_content() and '按角色匹配' in pg.locator('#auditModal').text_content())
    pg.close()

    # 权限三层
    for rel in ["系统管理/弹窗/权限配置.html", "系统管理/角色管理.html", "系统管理/用户权限.html"]:
        pg, errs = page(browser, rel)
        chk(rel + ' JS错0', not errs, str(errs[:2]))
        cnt = pg.locator('[data-audit]').count()
        chk(rel + ' 可审单据14', cnt == 14, f'{cnt}')
        pg.close()

    # 销售订单：附件+库存
    pg, errs = page(browser, "销售管理/弹窗/新建销售订单.html")
    chk('新建销售订单 JS错0', not errs, str(errs[:2]))
    att = pg.locator('.att-row').count()
    hints = pg.locator('.stock-hint').count()
    warn_vis = pg.locator('#stockWarn').is_visible()
    chk('新建销售订单 附件2+库存提示2+不足条可见', att == 2 and hints == 2 and warn_vis, f'att={att} hints={hints} warn={warn_vis}')
    pg.locator('#attName').evaluate("el => { el.value='G13-测试附件.pdf'; }")
    pg.evaluate("[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='添加').click()")
    pg.wait_for_timeout(100)
    chk('新建销售订单 假上传添加', pg.locator('.att-row').count() == 3)
    pg.close()

    # 租赁单新建模板：库存提示
    pg, errs = page(browser, "租赁管理/弹窗/租赁单新建.html")
    chk('租赁单新建 JS错0', not errs, str(errs[:2]))
    hints = pg.locator('.stock-hint').count()
    chk('租赁单新建 库存提示2行', hints == 2, f'{hints}')
    chk('租赁单新建 不足条隐藏(默认充足)', not pg.locator('#stockWarn').is_visible())
    pg.locator('.edit-tbl td select').first.evaluate("el => { el.selectedIndex = 2; el.dispatchEvent(new Event('change',{bubbles:true})); }")  # PLT-1210W 60<180
    pg.wait_for_timeout(120)
    chk('租赁单新建 切稀缺品→不足条可见', pg.locator('#stockWarn').is_visible())
    pg.close()

    # 租赁单审核模板：toast
    pg, errs = page(browser, "租赁管理/弹窗/租赁单审核.html")
    chk('租赁单审核模板 JS错0', not errs, str(errs[:2]))
    pg.locator('button', has_text='确认提交').first.evaluate("el => el.click()")
    pg.wait_for_timeout(120)
    chk('租赁单审核 背靠背toast', pg.locator('#g13Toast').is_visible() and 'RZD-20260910-009' in pg.locator('#g13Toast').text_content())
    pg.close()

    # 上下游绑定三处注记
    for rel in ["项目管理/弹窗/上下游绑定.html", "项目管理/项目档案.html", "项目管理/项目详情.html"]:
        pg, errs = page(browser, rel)
        chk(rel + ' JS错0+多对多注记', not errs and pg.locator('#bindModal', has_text='一对多/多对多').count() == 1)
        pg.close()

    browser.close()

print(f"\n==== G13 冒烟：失败 {len(fails)} 项 ====" if fails else "\n==== G13 冒烟：全过 ====")
sys.exit(1 if fails else 0)
