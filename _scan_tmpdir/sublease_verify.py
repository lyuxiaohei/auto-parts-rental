from playwright.sync_api import sync_playwright
import pathlib
base = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
r = []
def chk(n, c): r.append((n, bool(c)))
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1600,'height':900})
    pg.on('pageerror', lambda e: errs.append(str(e)))
    # PC 库存查询：状态筛选选客户转租出
    pg.goto((base/'仓储作业'/'库存查询.html').as_uri()); pg.wait_for_timeout(1200)
    body = pg.locator('body').inner_text()
    chk('PC-1 状态值=客户转租出', '客户转租出' in body)
    chk('PC-2 无旧词客户端(转租)', '客户端(转租)' not in body)
    # 筛选实测
    pg.select_option('.ff:has-text("库存状态") select', label='客户转租出')
    pg.click('button:has-text("查询")'); pg.wait_for_timeout(500)
    rows = pg.locator('tbody tr').count()
    chk('PC-3 转租筛选→3行', rows == 3)
    tb = pg.locator('tbody').inner_text()
    chk('PC-4 筛后全为转租行', tb.count('客户转租出') >= 3)
    pg.screenshot(path='_scan_tmpdir/sublease-pc.png')
    # mobile M03
    pg2 = b.new_page(viewport={'width':390,'height':844})
    pg2.goto((base/'mobile'/'库存查询.html').as_uri()); pg2.wait_for_timeout(1000)
    mb = pg2.locator('body').inner_text()
    chk('MB-1 移动端转租词', '客户转租出' in mb)
    badge = pg2.evaluate("""()=>{const el=[...document.querySelectorAll('.m-badge,.m-card *')].find(e=>e.textContent.trim().startsWith('客户转租出'));if(!el)return null;return el.className}""")
    chk('MB-2 转租徽标紫色', badge is not None and 'purple' in badge)
    # chips 筛选
    chips = pg2.evaluate("()=>[...document.querySelectorAll('.m-chip')].map(c=>c.textContent.trim())")
    chk('MB-3 chips 含转租', any('客户转租出' in c for c in chips))
    b.close()
chk('JS错误0', len(errs) == 0)
ok = sum(1 for _, c in r if c)
for n, c in r: print(('PASS' if c else 'FAIL'), n)
print('==', ok, '/', len(r), '==')
