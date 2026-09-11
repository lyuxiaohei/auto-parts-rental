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
    # 1. 物料档案页
    pg.goto((base/'基础数据'/'产品档案.html').as_uri()); pg.wait_for_timeout(1000)
    chk('W-1 页面标题=物料档案', '物料档案' in pg.title())
    sel = pg.locator('.sm-link.selected').inner_text()
    chk('W-2 侧边栏选中=物料档案', '物料档案' in sel)
    body = pg.locator('body').inner_text()
    chk('W-3 页面无"产品"字样', '产品' not in body)
    chk('W-4 物料编码列头', '物料编码' in body or '编码' in body)
    # 2. 列表页明细列头（租入单）
    pg.goto((base/'租赁管理'/'租入单列表.html').as_uri()); pg.wait_for_timeout(1000)
    th = pg.locator('thead th').all_inner_texts()
    chk('W-5 租入单明细列头=物料', any(t.strip()=='物料' for t in th))
    chk('W-6 页面无"产品"', '产品' not in pg.locator('body').inner_text())
    # 3. 采购订单弹窗（产品档案引用字段）
    pg.goto((base/'采购管理'/'采购订单列表.html').as_uri()); pg.wait_for_timeout(1000)
    pg.click('button:has-text("新建采购订单")'); pg.wait_for_timeout(300)
    cm = pg.locator('#createModal').inner_text()
    chk('W-7 采购弹窗含物料无产品', '物料' in cm and '产品' not in cm)
    # 4. 全站抽查菜单（库存查询侧边栏）
    pg.goto((base/'仓储作业'/'库存查询.html').as_uri()); pg.wait_for_timeout(800)
    sb = pg.locator('.sidebar').inner_text()
    chk('W-8 侧边栏含物料档案', '物料档案' in sb)
    chk('JS错误0', len(errs) == 0)
    b.close()
ok = sum(1 for _, c in r if c)
for n, c in r: print(('PASS' if c else 'FAIL'), n)
print('==', ok, '/', len(r), '==')
