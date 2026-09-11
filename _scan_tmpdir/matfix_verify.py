from playwright.sync_api import sync_playwright
import pathlib, re
base = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.on("pageerror", lambda e: errs.append(str(e)))
    # 1) 从库存查询页点侧边栏「物料档案」菜单
    pg.goto((base / "仓储作业" / "库存查询.html").as_uri())
    pg.wait_for_timeout(400)
    pg.locator(".sm-link", has_text="物料档案").click()
    pg.wait_for_timeout(500)
    ok1 = "产品档案" in str(pg.url) and pg.locator("h1, .page-title").first.inner_text() != ""
    title1 = pg.title()
    print(f"[1 菜单跳转] url 含产品档案.html: {'产品档案.html' in str(pg.url)} | 页面标题: {title1}")
    # 2) 列表页点 详情 弹窗仍正常
    pg.goto((base / "基础数据" / "产品档案.html").as_uri())
    pg.wait_for_timeout(400)
    pg.locator("tbody tr").first.locator("a", has_text="详情").click()
    pg.wait_for_timeout(400)
    print(f"[2 详情弹窗] 可见: {pg.locator('#detailModal').is_visible()} | 标题: {pg.locator('#detailTitle').inner_text()}")
    # 3) F01 SVG 链接指向存在文件
    f01 = (base / "P3-R01-F01-业务流程导航图.html").read_text(encoding="utf-8")
    hrefs = re.findall(r'href="([^"#]*?\.html)"', f01)
    missing = [h for h in set(hrefs) if not (base / h).exists()]
    print(f"[3 F01 链接] {len(set(hrefs))} 个唯一链接, 缺失: {missing if missing else '0'}")
    print(f"[4 JS errors] {errs if errs else '无'}")
    b.close()
