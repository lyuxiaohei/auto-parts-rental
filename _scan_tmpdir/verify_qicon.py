# -*- coding: utf-8 -*-
"""0920 ? 圆标换素材图（PNG base64 内嵌）渲染验证——只读验证，不改任何页面/数据"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
PAGES = [
    ("首页/项目看板.html", "子目录页·标题后 ?"),
    ("基础数据/BOM维护.html", "混合页·标题 ? + 数字角标"),
    ("我的待办.html", "根级页"),
]

results = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    js_errors = []
    pg.on("pageerror", lambda e: js_errors.append(str(e)))
    pg.on("console", lambda m: js_errors.append(m.text) if m.type == "error" else None)

    for rel, tag in PAGES:
        pg.goto((ROOT / rel).as_uri())
        pg.wait_for_timeout(600)
        icons = pg.locator(".pn-q")
        n = icons.count()
        row = {"page": rel, "tag": tag, "n_icons": n}
        if n:
            q = icons.first
            cs = pg.evaluate("""() => {
              const el = document.querySelector('.pn-q');
              const c = getComputedStyle(el);
              const r = el.getBoundingClientRect();
              const anc = el.closest('[data-note]');
              const ar = anc ? anc.getBoundingClientRect() : null;
              return {
                bg: c.backgroundImage.slice(0, 40),
                w: c.width, h: c.height,
                disp: c.display, va: c.verticalAlign,
                inBtn: !!el.closest('button'),
                x: Math.round(r.x), y: Math.round(r.y),
                overlapsAnchor: ar ? (r.left >= ar.left - 2 && r.right <= ar.right + 40 && r.bottom <= ar.bottom + 6 && r.top >= ar.top - 6) : null
              };
            }""")
            row.update(cs)
            # 点击第一个 ? → 弹窗
            q.click()
            pg.wait_for_timeout(250)
            row["tip_open"] = pg.locator(".pn-tip").evaluate("el => el.classList.contains('pn-show')")
            row["tip_text_ok"] = pg.locator(".pn-tip .pn-tip-b").count() > 0
            pg.locator(".pn-tip .pn-tip-x").click()
            pg.wait_for_timeout(200)
            row["tip_close"] = not pg.locator(".pn-tip").evaluate("el => el.classList.contains('pn-show')")
            # Esc 兜底关
            pg.keyboard.press("Escape")
        results.append(row)

    # 混合页：dev 数字角标仍走抽屉（fab 点击开抽屉）
    pg.goto((ROOT / "基础数据/BOM维护.html").as_uri())
    pg.wait_for_timeout(400)
    fab = pg.locator("#protoNotesFab")
    if fab.count():
        fab.click()
        pg.wait_for_timeout(400)
        drawer_open = pg.locator(".pn-drawer").evaluate("el => el.classList.contains('pn-show')")
        badge_items = pg.locator(".pn-item").count()
        dev_badge = pg.locator(".pn-aud-dev").count()
        pg.locator(".pn-close").click()
    else:
        drawer_open = badge_items = dev_badge = "no-fab"
    results.append({"page": "基础数据/BOM维护.html", "tag": "抽屉", "drawer_open": drawer_open, "items": badge_items, "dev_badges": dev_badge})
    b.close()

for r in results:
    print(r)
print("JS_ERRORS:", len(js_errors), js_errors[:3])
fails = []
for r in results:
    if r.get("tag") != "抽屉":
        if not str(r.get("bg", "")).startswith('url("data:image/png;base64'):
            fails.append(f'{r["page"]}: bg={r.get("bg")}')
        if r.get("w") != "18px" or r.get("h") != "18px":
            fails.append(f'{r["page"]}: size={r.get("w")}x{r.get("h")}')
        if r.get("tip_open") is not True or r.get("tip_close") is not True:
            fails.append(f'{r["page"]}: tip open/close={r.get("tip_open")}/{r.get("tip_close")}')
        if r.get("overlapsAnchor") is False:
            fails.append(f'{r["page"]}: icon outside anchor box')
if js_errors:
    fails.append(f"JS errors: {js_errors[:3]}")
print("VERDICT:", "PASS" if not fails else "FAIL " + "; ".join(fails))
