from playwright.sync_api import sync_playwright
import pathlib
base = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((base / "基础数据" / "产品档案.html").as_uri())
    pg.wait_for_timeout(600)
    # 点击第一行 详情
    pg.locator("tbody tr").first.locator("a", has_text="详情").click()
    pg.wait_for_timeout(600)
    vis = pg.locator("#detailModal").is_visible()
    title = pg.locator("#detailTitle").inner_text() if vis else "(modal 不可见)"
    body_len = len(pg.locator("#detailModal .modal-body").inner_text()) if vis else 0
    print(f"detailModal 可见: {vis} | 标题: {title} | body 字符数: {body_len}")
    pg.screenshot(path=r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\matbug-detail.png")
    print("JS errors:", errs if errs else "无")
    b.close()
