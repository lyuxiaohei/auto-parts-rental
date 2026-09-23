# 验证：我的页头像恢复 56px 圆形，其余 hero 区不受影响
import pathlib, sys
from playwright.sync_api import sync_playwright

root = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\mobile")
url = (root / "我的.html").as_uri()
out = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\avatar_fix_shot.png")

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script("localStorage.setItem('m-auth','1')")
    pg.goto(url)
    pg.wait_for_timeout(600)

    av = pg.locator("#m-avatar")
    box = av.bounding_box()
    print("avatar box:", box)
    if not box or abs(box["width"] - 32) > 1 or abs(box["height"] - 32) > 1:
        fails.append(f"avatar 尺寸非 32x32: {box}")
    radius = av.evaluate("el => getComputedStyle(el).borderRadius")
    print("border-radius:", radius)
    if radius != "50%":
        fails.append(f"border-radius 异常: {radius}")
    # SVG 撑满容器
    svg_box = pg.locator("#m-avatar svg").bounding_box()
    print("svg box:", svg_box)
    if not svg_box or abs(svg_box["width"] - 28) > 2 or abs(svg_box["height"] - 28) > 2:
        fails.append(f"svg 未贴合容器: {svg_box}")
    # 姓名行未被挤掉
    name = pg.locator("#m-me-name").inner_text()
    print("name:", name)
    if not name.strip():
        fails.append("姓名为空")
    # 指标卡仍在
    for i in ["#m-st-todo", "#m-st-done", "#m-st-sku", "#m-st-instk"]:
        t = pg.locator(i).inner_text()
        if not t.strip():
            fails.append(f"{i} 为空")
    if errs:
        fails.append(f"JS 错误: {errs}")

    pg.screenshot(path=str(out), full_page=True)
    b.close()

print("FAILS:", fails if fails else "无")
sys.exit(1 if fails else 0)
