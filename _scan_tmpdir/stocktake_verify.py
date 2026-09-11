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
    pg.goto((base/'仓储作业'/'盘点列表.html').as_uri()); pg.wait_for_timeout(1000)
    # 1) 菜单名
    sb = pg.locator('.sm-link.selected').inner_text()
    chk('M-1 侧边栏选中项=盘点记录', '盘点记录' in sb)
    # 2) 表头列
    th = pg.locator('thead th').all_inner_texts()
    chk('T-1 关联单据列存在', any('关联单据' in t for t in th))
    # 3) 行数据
    tb = pg.locator('tbody').inner_text()
    chk('D-1 盘盈行第一单+1(QTRK+1)', 'QTRK-20260816-023' in tb)
    chk('D-2 盘亏行(QTCK-20260731-005)', 'QTCK-20260731-005' in tb)
    chk('D-3 无盈亏行=—', tb.count('—') >= 2)
    # 4) 生成按钮
    chk('G-1 生成入库×2', pg.locator('a:has-text("生成入库")').count() == 2)
    chk('G-2 生成出库×1', pg.locator('a:has-text("生成出库")').count() == 1)
    # 5) +1 气泡
    pg.locator('.docs-plus').first.click(); pg.wait_for_timeout(300)
    pop = pg.locator('#docsPop')
    chk('P-1 气泡显示', pop.is_visible())
    ptxt = pop.inner_text()
    chk('P-2 气泡列全部2条(023+024)', 'QTRK-20260816-023' in ptxt and 'QTRK-20260816-024' in ptxt)
    chk('P-3 无蒙层(无 overlay show)', pg.locator('.modal-overlay.show').count() == 0)
    pg.screenshot(path='_scan_tmpdir/stock-pop.png')
    # 点别处关闭
    pg.locator('.card-title').first.click(); pg.wait_for_timeout(200)
    chk('P-4 点别处关闭', not pop.is_visible())
    # 6) +2 气泡
    pg.locator('.docs-plus').nth(1).click(); pg.wait_for_timeout(300)
    p2 = pop.inner_text()
    chk('P-5 盘亏气泡3条(005/006/007)', '005' in p2 and '006' in p2 and '007' in p2)
    pg.locator('.card-title').first.click(); pg.wait_for_timeout(200)
    # 7) 生成入库小弹窗
    pg.locator('a:has-text("生成入库")').first.click(); pg.wait_for_timeout(300)
    chk('G-3 生成弹窗显示', pop.is_visible() and '盘盈明细' in pop.inner_text())
    pg.locator('#dpGen').click(); pg.wait_for_timeout(200)
    g = pop.inner_text()
    chk('G-4 生成草稿→已生成单号', '已生成' in g and 'QTRK-' in g)
    pg.screenshot(path='_scan_tmpdir/stock-gen.png')
    # 8) 表格行数完整性（5 行数据没被破坏）
    chk('R-1 行数=5', pg.locator('tbody tr').count() == 5)
    chk('R-2 每行列数=11(含新列)', all(pg.locator('tbody tr').nth(i).locator('td').count() == 11 for i in range(5)))
    chk('JS错误0', len(errs) == 0)
    b.close()
ok = sum(1 for _, c in r if c)
for n, c in r: print(('PASS' if c else 'FAIL'), n)
print('==', ok, '/', len(r), '==')
