from playwright.sync_api import sync_playwright
import pathlib
base = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1600,'height':900})
    for name in ['应收账单','应付账单']:
        pg.goto((base/'财务协同'/f'{name}.html').as_uri())
        pg.wait_for_timeout(1200)
        pg.screenshot(path=f'_scan_tmpdir/arbug-{name}-collapsed.png', full_page=False)
        # 滚到列表区中部再看
        pg.mouse.wheel(0,500)
        pg.wait_for_timeout(300)
        pg.screenshot(path=f'_scan_tmpdir/arbug-{name}-scrolled.png', full_page=False)
    b.close()
print('done')
