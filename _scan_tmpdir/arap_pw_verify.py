from playwright.sync_api import sync_playwright
import pathlib
base = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
results = []
def chk(name, cond):
    results.append((name, bool(cond)))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1600,'height':900})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))

    # === 应付账单页 ===
    pg.goto((base/'财务协同'/'应付账单.html').as_uri())
    pg.wait_for_timeout(1000)
    chk('AP-1 页面流无 instCard 卡片', pg.locator('.content > .card#instCard').count() == 0)
    pg.click('button:has-text("新建应付账单")')
    pg.wait_for_timeout(300)
    chk('AP-2 createModal 弹出', pg.locator('#createModal.show').count() == 1)
    # 切对客户应付 → 对方单位变客户 + 费用分类出现
    pg.select_option('#createModal select >> nth=0', label='对客户应付（赔付客户：交付延误·断产·回款违约金）') if pg.locator('#createModal select >> nth=0').count() else None
    pg.wait_for_timeout(200)
    body_txt = pg.locator('#createModal .modal-body').inner_text()
    chk('AP-3 类型联动-费用分类出现', '费用分类' in body_txt)
    # 比例⇄金额互算：取分期表第一行比例输入框改为 50
    rate0 = pg.locator('#createModal [data-k="rate"]').first
    amt0 = pg.locator('#createModal [data-k="amt"]').first
    base_amt = pg.locator('#createModal input[id*="Base"], #createModal #cmInstBase').first
    chk('AP-4 分期计划输入框存在', rate0.count() > 0 and amt0.count() > 0)
    if rate0.count():
        rate0.fill('50')
        pg.wait_for_timeout(200)
        amt_val = amt0.input_value().replace(',', '')
        # 基数 68400 → 50% = 34200
        chk('AP-5 比例→金额互算(50%→34,200)', abs(float(amt_val) - 34200.0) < 1)
        # 反向：金额改 50000 → 比例≈73.10
        amt0.fill('50000')
        pg.wait_for_timeout(200)
        rate_val = float(rate0.input_value())
        chk('AP-6 金额→比例互算(50,000→~73.1%)', abs(rate_val - 50000/68400*100) < 0.5)
    pg.keyboard.press('Escape')
    pg.locator('#createModal .modal-close').click()
    pg.wait_for_timeout(200)
    # 列表行点分期付款 → instModal
    pg.locator('.ops a:has-text("分期付款")').first.click()
    pg.wait_for_timeout(300)
    chk('AP-7 分期付款op开instModal', pg.locator('#instModal.show').count() == 1)
    chk('AP-8 instModal标题带账单号', 'AP-' in pg.locator('#instModal .modal-title').inner_text())
    pg.locator('#instModal .modal-close').click()
    # 截图
    pg.screenshot(path='_scan_tmpdir/arap-fixed-应付-collapsed.png')

    # === 应收账单页 ===
    pg.goto((base/'财务协同'/'应收账单.html').as_uri())
    pg.wait_for_timeout(1000)
    pg.click('button:has-text("手动生成账单")')
    pg.wait_for_timeout(300)
    chk('AR-1 createModal 弹出', pg.locator('#createModal.show').count() == 1)
    ar_body = pg.locator('#createModal .modal-body').inner_text()
    chk('AR-2 五类型含供应商应收', '供应商应收' in ar_body and '丢损赔偿' in ar_body)
    chk('AR-3 分期收款计划区', '分期收款' in ar_body or '分期' in ar_body)
    chk('AR-4 无垃圾选项', '待定选项' not in ar_body)
    pg.screenshot(path='_scan_tmpdir/arap-fixed-应收-modal.png')
    chk('AR/AP 全程无JS错误', len(errs) == 0)
    b.close()

ok = sum(1 for _, c in results if c)
for n, c in results:
    print(('PASS' if c else 'FAIL'), n)
print(f'== 合计 PASS {ok} / FAIL {len(results)-ok} ==')
