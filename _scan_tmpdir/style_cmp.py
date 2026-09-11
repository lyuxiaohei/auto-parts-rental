from playwright.sync_api import sync_playwright
import pathlib
base = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1600,'height':900})
    # 绑定弹窗
    pg.goto((base/'项目管理'/'项目档案.html').as_uri()); pg.wait_for_timeout(1200)
    pg.locator('tbody a:has-text("上下游绑定")').first.click(); pg.wait_for_timeout(400)
    pg.screenshot(path='_scan_tmpdir/style-bind.png')
    # 新建项目弹窗
    pg.locator('#bindModal .modal-close').click(); pg.wait_for_timeout(200)
    pg.click('button:has-text("新建项目")'); pg.wait_for_timeout(400)
    pg.screenshot(path='_scan_tmpdir/style-newproj.png')
    b.close()
print('done')
