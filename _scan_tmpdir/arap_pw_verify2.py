from playwright.sync_api import sync_playwright
import pathlib
base = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
r = []
def chk(n, c): r.append((n, bool(c)))
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1600,'height':900})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto((base/'财务协同'/'应付账单.html').as_uri())
    pg.wait_for_timeout(1000)
    chk('AP-1 页面流无 instCard 卡片', pg.locator('.content > .card#instCard').count() == 0)
    pg.click('button:has-text("新建应付账单")')
    pg.wait_for_timeout(300)
    # 比例→金额：50% × 84000 = 42000
    pg.fill('#createModal input[data-k="rate"][data-i="0"]', '50')
    pg.wait_for_timeout(250)
    a0 = float(pg.locator('#createModal input[data-k="amt"][data-i="0"]').input_value().replace(',',''))
    chk('AP-5 比例→金额互算(50%→42,000)', abs(a0-42000.0) < 1)
    # 金额→比例：50000/84000=59.52%
    pg.fill('#createModal input[data-k="amt"][data-i="0"]', '50000')
    pg.wait_for_timeout(250)
    rt = float(pg.locator('#createModal input[data-k="rate"][data-i="0"]').input_value())
    chk('AP-6 金额→比例互算(50,000→~59.52%)', abs(rt - 50000/84000*100) < 0.5)
    # 末期补差：第2期金额=84000-50000=34000
    a1 = float(pg.locator('#createModal input[data-k="amt"][data-i="1"]').input_value().replace(',',''))
    chk('AP-6b 末期自动补差(→34,000)', abs(a1-34000.0) < 1)
    # 超额拦截：第1期金额改 90000 → 合计超 84000 → 红框
    pg.fill('#createModal input[data-k="amt"][data-i="0"]', '90000')
    pg.wait_for_timeout(250)
    bc = pg.locator('#createModal input[data-k="amt"][data-i="0"]').evaluate('el=>el.style.borderColor')
    chk('AP-6c 超额红框拦截', 'ff4d4f' in bc or '255, 77, 79' in bc)
    # 类型联动：切对客户应付 → 对方单位含客户名单
    pg.select_option('#cmBtype', 'customer')
    pg.wait_for_timeout(250)
    party = pg.locator('#cmParty').evaluate('el=>Array.from(el.options).map(o=>o.text).join("|")')
    chk('AP-3b 对客户应付→对方单位=客户名单', '一汽解放' in party)
    lbl = pg.evaluate("()=>{const l=[...document.querySelectorAll('#createModal .form-label')];return l.map(x=>x.textContent.trim()).join('|')}")
    chk('AP-3c 费用分类字段出现', '费用分类' in lbl)
    # 截图留证
    pg.screenshot(path='_scan_tmpdir/arap-fixed-应付-createModal.png')
    pg.locator('#createModal .modal-close').click()
    pg.wait_for_timeout(200)
    pg.locator('.ops a:has-text("分期付款")').first.click()
    pg.wait_for_timeout(300)
    chk('AP-7 分期付款op→instModal', pg.locator('#instModal.show').count() == 1)
    # instModal 互算也测一把（基数 68400：改 60%→41,040）
    pg.fill('#instModal input[data-k="rate"][data-i="0"]', '60')
    pg.wait_for_timeout(250)
    ia = float(pg.locator('#instModal input[data-k="amt"][data-i="0"]').input_value().replace(',',''))
    chk('AP-9 instModal互算(60%→41,040)', abs(ia-41040.0) < 1)
    pg.screenshot(path='_scan_tmpdir/arap-fixed-应付-instModal.png')
    b.close()
chk('JS错误0', len(errs)==0)
ok = sum(1 for _,c in r if c)
for n,c in r: print(('PASS' if c else 'FAIL'), n)
print(f'== PASS {ok} / FAIL {len(r)-ok} ==')
