# -*- coding: utf-8 -*-
"""G36 B1 验收·第4项：4 个新页 PW 抽验（只读，输出到控制台）"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

BASE = "file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型/"
PAGES = [
    ("物料新建",   BASE + "基础数据/物料新建.html",  "form"),
    ("客商开票资料", BASE + "基础数据/客商开票资料.html", "form"),
    ("上下游绑定", BASE + "项目管理/上下游绑定.html", "form"),
    ("物料详情",   BASE + "基础数据/物料详情.html?id=WBX-1210L", "detail"),
]

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for name, url, kind in PAGES:
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        errs, cerrs = [], []
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.on("console", lambda m: cerrs.append(m.text) if m.type == "error" else None)
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(600)

        html = page.content()
        opens = len(re.findall(r"<div[\s>]", html))
        closes = len(re.findall(r"</div\s*>", html))

        rep = {"page": name, "pageerror": len(errs), "console_error": len(cerrs),
               "div_open": opens, "div_close": closes, "div_balanced": opens == closes}

        if kind == "form":
            widths = page.evaluate("""() => [...document.querySelectorAll('.form-row > div > .input-box')]
                .map(el => Math.round(el.getBoundingClientRect().width))""")
            rep["inputbox_count"] = len(widths)
            rep["inputbox_widths"] = sorted(set(widths))
            rep["inputbox_all_380"] = all(abs(w - 380) <= 2 for w in widths) if widths else False
            sb = page.evaluate("""() => {
                const bar = document.querySelector('.submit-bar');
                if (!bar) return null;
                const cs = getComputedStyle(bar);
                const btns = [...bar.querySelectorAll('button')].filter(b => {
                    const r = b.getBoundingClientRect(); return r.width > 0 && r.height > 0;
                });
                if (!btns.length) return {justify: cs.justifyContent, nbtn: 0};
                const br = bar.getBoundingClientRect();
                const first = btns[0].getBoundingClientRect(), last = btns[btns.length-1].getBoundingClientRect();
                return {justify: cs.justifyContent, nbtn: btns.length,
                        left_gap: Math.round(first.left - br.left),
                        right_gap: Math.round(br.right - last.right)};
            }""")
            rep["submit_bar"] = sb
            if sb:
                rep["bar_center"] = sb.get("justify") == "center"
                rep["bar_gap_diff_ok"] = sb.get("nbtn", 0) == 0 or abs(sb.get("left_gap", 999) - sb.get("right_gap", 999)) <= 40
        else:
            n = page.evaluate("() => document.querySelectorAll('#detailBody .dt-sec').length")
            rep["dt_sec_count"] = n
            rep["dt_sec_ok"] = n >= 3

        print(rep)
        if errs: print("  pageerrors:", errs[:3])
        if cerrs: print("  console errors:", cerrs[:3])
        page.close()
    browser.close()
print("DONE")
