from playwright.sync_api import sync_playwright
import pathlib
base = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
errs = []
def check(pg, tag):
    radios = pg.locator("#createModal .radio")
    n = radios.count()
    g = [radios.nth(i).bounding_box() for i in range(n)]
    same_y = len(set(round(b["y"]) for b in g)) == 1
    no_wrap = all(b["height"] < 30 for b in g)
    # 归属权 label 与单位 label 不同行
    lbls = pg.locator("#createModal .form-label")
    ys = {lbls.nth(i).inner_text().strip("*\n"): lbls.nth(i).bounding_box()["y"] for i in range(lbls.count())}
    own_row = ys.get("归属权") != ys.get("单位")
    print(f"[{tag}] radio数:{n} 同行:{same_y} 单行高:{no_wrap} 归属权独占行:{own_row}")
    return same_y and no_wrap and own_row
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((base / "基础数据" / "产品档案.html").as_uri())
    pg.wait_for_timeout(400)
    pg.evaluate("openModal('createModal')")
    pg.wait_for_timeout(300)
    ok1 = check(pg, "内嵌弹窗")
    pg.screenshot(path=r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\ownfix-inner.png")
    pg.goto((base / "基础数据" / "弹窗" / "新建产品.html").as_uri())
    pg.wait_for_timeout(400)
    ok2 = check(pg, "预览页")
    pg.screenshot(path=r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\ownfix-preview.png")
    print(f"JS errors: {errs if errs else '无'} | 结论: {'PASS' if ok1 and ok2 and not errs else 'FAIL'}")
    b.close()
