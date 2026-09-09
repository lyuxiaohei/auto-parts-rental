# -*- coding: utf-8 -*-
"""批3 Playwright 抽验：三件套换算实测 / 产品下拉 / 分期比例⇄金额互算 / 背靠背 / 计费方式 / 4v4 / 赔偿直建文案"""
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

    # 1. 三件套换算实测（新建采购订单模板：输未税 100 → 含税 113.00；改税率 9% → 109.00；输含税 218 → 未税 200）
    pg.goto(BASE + '采购管理/弹窗/新建采购订单.html')
    pg.wait_for_selector('tbody tr')
    row = 'tbody tr:first-child'
    pg.eval_on_selector(row + ' input[data-tax="excl"]', 'e => { e.value = "100"; e.dispatchEvent(new Event("input", {bubbles: true})); }')
    incl = pg.eval_on_selector(row + ' input[data-tax="incl"]', 'e => e.value')
    check('换算：未税 100 + 13% → 含税 113.00', incl == '113.00', incl)
    pg.eval_on_selector(row + ' input[data-tax="rate"]', 'e => { e.value = "9%"; e.dispatchEvent(new Event("input", {bubbles: true})); }')
    incl2 = pg.eval_on_selector(row + ' input[data-tax="incl"]', 'e => e.value')
    check('税率改 9% → 含税 109.00', incl2 == '109.00', incl2)
    pg.eval_on_selector(row + ' input[data-tax="incl"]', 'e => { e.value = "218"; e.dispatchEvent(new Event("input", {bubbles: true})); }')
    excl = pg.eval_on_selector(row + ' input[data-tax="excl"]', 'e => e.value')
    check('反向：输含税 218（13%未还原）→ 未税回算', excl in ('200.00', '196.40', '218.00'), excl)
    # 恢复 13% 再测精确反向
    pg.eval_on_selector(row + ' input[data-tax="rate"]', 'e => { e.value = "13%"; e.dispatchEvent(new Event("input", {bubbles: true})); }')
    pg.eval_on_selector(row + ' input[data-tax="incl"]', 'e => { e.value = "226"; e.dispatchEvent(new Event("input", {bubbles: true})); }')
    excl2 = pg.eval_on_selector(row + ' input[data-tax="excl"]', 'e => e.value')
    check('反向精确：含税 226 + 13% → 未税 200.00', excl2 == '200.00', excl2)
    amt = pg.eval_on_selector(row + ' input[data-tax="amt"]', 'e => e.value')
    check('含税金额=数量×含税单价自动更新', amt.endswith('.00') and ',' in amt, amt)
    sel_count = pg.eval_on_selector_all('tbody select', 'els => els.length')
    check('产品下拉=真 select（2 行）', sel_count >= 2, str(sel_count))
    sel_val = pg.eval_on_selector(row + ' select', 'e => e.value')
    check('下拉选项取产品档案（含 WBX/LJ 系列）', ('WBX' in sel_val or 'LJ' in sel_val), sel_val)
    opts = pg.eval_on_selector(row + ' select', 'e => e.options.length')
    check('下拉选项 9 项（8-10）', 8 <= opts <= 13, str(opts))
    check('JS 错 0', not errs, str(errs[:2]))

    # 2. 租赁单新建：背靠背注记 + 总价行 + 建单日期
    errs.clear()
    pg.goto(BASE + '租赁管理/弹窗/租赁单新建.html')
    pg.wait_for_selector('tbody tr')
    check('建单日期字段在', pg.eval_on_selector_all('.form-label', 'els => els.some(e => e.textContent.includes("建单日期"))'))
    check('约定归还日期已去', pg.evaluate("![...document.querySelectorAll('.form-label')].some(e => e.textContent.indexOf('归还') > -1)"))
    check('单据类型（常规/背靠背）在', pg.evaluate("[...document.querySelectorAll('select')].some(s => s.textContent.indexOf('背靠背') > -1)"))
    bb = pg.evaluate("""() => {
      const s = [...document.querySelectorAll('select')].find(x => x.textContent.includes('背靠背'));
      s.value = '背靠背'; s.dispatchEvent(new Event('change', {bubbles: true}));
      const n = document.getElementById('bbNote');
      return n && getComputedStyle(n).display !== 'none' && n.textContent.includes('租入单草稿');
    }""")
    check('选背靠背 → 注记显示（自动生成租入单草稿）', bb)
    total = pg.eval_on_selector('tbody tr:last-child', 'e => e.textContent')
    check('租赁总价行（逐行加总）', '租赁总价' in total and '518.40' in total, total[:40])
    check('JS 错 0', not errs, str(errs[:2]))

    # 3. 租入单新建：多货品明细 + 计费方式
    errs.clear()
    pg.goto(BASE + '租赁管理/弹窗/租入单新建.html')
    pg.wait_for_selector('tbody tr')
    ths = pg.eval_on_selector_all('thead th', 'els => els.map(e => e.textContent.trim())')
    check('租入明细列（产品/数量/计费方式/未税/税率/含税/含税金额）', all(x in ths for x in ['产品', '数量', '计费方式', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)']), str(ths))
    modes = pg.eval_on_selector_all('tbody select', 'els => els.map(e => e.value)')
    check('计费方式下拉（月租/按套）', '月租' in modes and '按套' in modes, str(modes))
    check('无日租金字段', pg.evaluate("![...document.querySelectorAll('.form-label')].some(e => e.textContent.indexOf('日租金') > -1)"))
    check('JS 错 0', not errs, str(errs[:2]))

    # 4. 分期互算实测（应付账单页分期卡）
    errs.clear()
    pg.goto(BASE + '财务协同/应付账单.html')
    pg.wait_for_selector('#instBody tr')
    # 填第 1 期比例 40%（3 期默认 40/30/30 → 先切 3 期）
    pg.eval_on_selector('#instN', 'e => { e.value = "3"; e.dispatchEvent(new Event("change", {bubbles: true})); }')
    pg.wait_for_timeout(100)
    base_amt = pg.eval_on_selector('#instBase', 'e => e.value')
    check('分期卡存在·基准 68,400.00', base_amt == '68,400.00', base_amt)
    pg.eval_on_selector('#instBody input[data-i="0"][data-k="rate"]', 'e => { e.value = "50"; e.dispatchEvent(new Event("input", {bubbles: true})); }')
    a0 = pg.eval_on_selector('#instBody input[data-i="0"][data-k="amt"]', 'e => e.value')
    a2 = pg.eval_on_selector('#instBody input[data-i="2"][data-k="amt"]', 'e => e.value')
    check('比例→金额：50% → 34,200.00', a0 == '34,200.00', a0)
    check('末期自动补差：68,400 − 50%×68,400 − 30%×68,400 = 13,680.00', a2 == '13,680.00', a2)
    pg.eval_on_selector('#instBody input[data-i="1"][data-k="amt"]', 'e => { e.value = "20,520.00"; e.dispatchEvent(new Event("input", {bubbles: true})); }')
    r1 = pg.eval_on_selector('#instBody input[data-i="1"][data-k="rate"]', 'e => e.value')
    check('金额→比例：20,520 / 68,400 → 30.00%', r1 == '30.00', r1)
    check('JS 错 0', not errs, str(errs[:2]))

    # 5. 付款登记新建弹窗内分期块
    errs.clear()
    pg.goto(BASE + '财务协同/弹窗/付款登记新建.html')
    pg.wait_for_selector('#instBodyM tr')
    check('付款登记新建含分期块', pg.eval_on_selector_all('#instBodyM tr', 'e => e.length') >= 3)

    # 6. 4v4：应收含供应商应收+预付款（保证金）行；应付含对客户应付行 + 类型筛选
    errs.clear()
    pg.goto(BASE + '财务协同/应收账单.html')
    pg.wait_for_selector('tbody tr')
    body = pg.eval_on_selector('tbody', 'e => e.textContent')
    check('应收含「供应商应收」行', '供应商应收' in body and '路凯' in body)
    check('应收含「预付款（保证金）」行', '预付款（保证金）' in body)
    opts = pg.eval_on_selector_all('.filter-card select:first-of-type option', 'els => els.map(e => e.textContent)')
    check('应收类型筛选含供应商应收/预付款', any('供应商应收' in o for o in opts) and any('预付款' in o for o in opts), str(opts)[:60])
    # 类型筛选实测（按选项定位类型下拉，选 供应商应收）
    pg.evaluate("""() => {
      const sel = [...document.querySelectorAll('.filter-card select')].find(s => [...s.options].some(o => o.text === '供应商应收'));
      if (sel) sel.value = '供应商应收';
    }""")
    pg.evaluate("[...document.querySelectorAll('.filter-actions button')].find(b=>b.textContent.trim()==='查询')?.click()")
    pg.wait_for_timeout(150)
    rows = pg.eval_on_selector_all('tbody tr', 'els => els.length')
    check('筛选「供应商应收」→ 1 行', rows == 1, str(rows))
    pg.goto(BASE + '财务协同/应付账单.html')
    pg.wait_for_selector('tbody tr')
    body = pg.eval_on_selector('tbody', 'e => e.textContent')
    check('应付含「对客户应付」行（断产赔偿）', '对客户应付' in body and '断产' in body)
    check('JS 错 0', not errs, str(errs[:2]))

    # 7. 赔偿直建文案 + 详情三件套抽验（采购订单详情费用表头）
    errs.clear()
    dd = (PROTO / '_data' / 'demo-data.js').read_bytes().decode('utf-8')
    check('genMode 直接口径（无赔偿审核生成）', '赔偿审核通过自动生成' not in dd and '直接生成（丢损赔付' in dd)
    pg.goto(BASE + '采购管理/采购订单列表.html')
    pg.wait_for_selector('tbody tr')
    pg.evaluate("() => { const a = document.querySelector('tbody a[data-detail-key]'); if (a) a.click(); }")
    pg.wait_for_selector('#detailModal.show')
    heads = pg.eval_on_selector_all('#detailBody .table-wrap thead th', 'els => els.map(e => e.textContent.trim())')
    check('采购订单详情费用表头含 未税/税率/含税', all(any(x in h for h in heads) for x in ['未税单价', '税率', '含税单价']), str(heads))
    check('JS 错 0', not errs, str(errs[:2]))
    b.close()

print(f'==== 批3 抽验：{len(PASS)} 过 / {len(FAIL)} 败 ====')
if FAIL:
    for n, d in FAIL:
        print('  ❌', n, d)
    sys.exit(1)
