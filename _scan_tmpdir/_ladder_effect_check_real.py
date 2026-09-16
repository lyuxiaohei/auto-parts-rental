# -*- coding: utf-8 -*-
# 现行阶梯图（P1-R03/）「替代效应」改动渲染核验：截图 + 单行断言 + 柱体溢出断言
from playwright.sync_api import sync_playwright
import pathlib

html = pathlib.Path(r"P1-R03/P1-R03-F01-版本业务能力阶梯图.html").resolve()
out_png = pathlib.Path(r"_scan_tmpdir/_ladder_effect_check_real.png").resolve()

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1600, "height": 1000})
    page.goto(html.as_uri())
    page.wait_for_timeout(500)
    page.screenshot(path=str(out_png), full_page=True)
    res = page.evaluate("""() => {
      const out = {effects: [], bodies: []};
      document.querySelectorAll('.effect').forEach(el => {
        // 数行盒：Range 覆盖整段文字，getClientRects 的行数即实际行数
        const rng = document.createRange();
        rng.selectNodeContents(el);
        const lines = Array.from(rng.getClientRects()).filter(r => r.width > 1).length;
        out.effects.push({text: el.textContent.trim(), lines: lines});
      });
      document.querySelectorAll('.body').forEach(el => {
        out.bodies.push({overflowY: el.scrollHeight - el.clientHeight,
                         overflowX: el.scrollWidth - el.clientWidth});
      });
      return out;
    }""")
    b.close()

ok = True
print("== 替代效应行 ==")
for i, e in enumerate(res["effects"]):
    good = e["lines"] == 1
    ok = ok and good
    print(f"{'PASS' if good else 'FAIL 折行'} | {e['lines']} 行 | {e['text']}")
print("== 柱体卡片溢出（scroll- client，<=0 为不溢出）==")
for i, bd in enumerate(res["bodies"]):
    good = bd["overflowY"] <= 0 and bd["overflowX"] <= 0
    ok = ok and good
    print(f"{'PASS' if good else 'FAIL 溢出'} | 柱#{i} | dY={bd['overflowY']} dX={bd['overflowX']}")
print("SCREENSHOT:", out_png)
print("RESULT:", "ALL PASS" if ok else "CHECK NEEDED")
