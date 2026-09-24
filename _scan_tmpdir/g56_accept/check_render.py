# -*- coding: utf-8 -*-
"""G56 acceptance - (4) render gate: playwright chromium opens F01 file:// URL"""
import sys, json, pathlib
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

F01 = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\P3-R01-F01-业务流程导航图.html")
url = F01.as_uri()

TEXTS = [
    "租入单（直发）",
    "系统自动 · 直发虚拟仓 XNC-ZF",
    "系统自动 · 供应商直发客户",
    "类型＝直发单／自发单",
    "采购退货单",
    "退款单",
    "销售退货单",
    "两守卫（D-157）",
    "直发件退租＝人工录入",
    "背靠背（GHCK）",
]
S7_NODES = ["转移出库列表", "转移出库新建", "转移出库单详情"]  # exact match

result = {"url": url, "pageerrors": [], "console_errors": [], "texts": {}, "s7": {}}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.on("pageerror", lambda e: result["pageerrors"].append(str(e)))
    page.on("console", lambda m: result["console_errors"].append(m.text) if m.type == "error" else None)
    page.goto(url, wait_until="load")
    page.wait_for_timeout(600)

    for t in TEXTS:
        loc = page.get_by_text(t)
        n = loc.count()
        bb = loc.first.bounding_box() if n > 0 else None
        result["texts"][t] = {"count": n, "bbox": bb}

    for t in S7_NODES:
        loc = page.get_by_text(t, exact=True)
        n = loc.count()
        bb = loc.first.bounding_box() if n > 0 else None
        result["s7"][t] = {"count": n, "bbox": bb}

    # page-level sanity: title
    result["title"] = page.title()
    # take a screenshot as evidence (kept inside g56_accept)
    page.screenshot(path=str(F01.parent.parent.parent / "_scan_tmpdir" / "g56_accept" / "render_full.png"), full_page=True)
    browser.close()

print(json.dumps(result, ensure_ascii=False, indent=1, default=str))
