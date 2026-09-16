# -*- coding: utf-8 -*-
# 阶梯图「替代效应」文案改动渲染核验：截图 + 实测文字 bbox 是否超出卡片右缘
from playwright.sync_api import sync_playwright
import pathlib

html = pathlib.Path(r"_scan_tmpdir/backup-阶梯图-20260907/P1-R03-F01-版本业务能力阶梯图.html").resolve()
out_png = pathlib.Path(r"_scan_tmpdir/_ladder_effect_check.png").resolve()

# 三张台阶卡片的右缘 x（卡片 x + 宽 244）
cards = {"V1.0": 140 + 244, "V1.1": 396 + 244, "V2.0": 652 + 244}

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1376, "height": 900})
    page.goto(html.as_uri())
    page.wait_for_timeout(600)  # 等 webfont
    page.screenshot(path=str(out_png), full_page=True)
    res = page.evaluate("""() => {
      const out = [];
      document.querySelectorAll('svg text').forEach(t => {
        const s = t.textContent || '';
        if (s.includes('替代效应')) {
          const bb = t.getBBox();
          out.push({text: s, x: bb.x, right: bb.x + bb.width, w: bb.width});
        }
      });
      return out;
    }""")
    b.close()

pad = 6  # 允许文字距卡片右缘的最小留白
ok = True
for r in res:
    # 依次对应 V1.0 / V1.1 / V2.0（文档顺序）
    name = ["V1.0", "V1.1", "V2.0"][len([1 for _ in res if True]) and 0] if False else None
for i, r in enumerate(res):
    name = ["V1.0", "V1.1", "V2.0"][i] if i < 3 else f"#{i}"
    limit = cards.get(name)
    fit = (limit is not None) and (r["right"] <= limit - pad)
    ok = ok and fit
    print(f"{name} | {r['text']} | 右缘 {r['right']:.1f} / 卡片右缘 {limit} | {'PASS' if fit else 'FAIL 超宽'}")

print("SCREENSHOT:", out_png)
print("RESULT:", "ALL PASS" if ok and len(res) == 3 else "CHECK NEEDED (count=%d)" % len(res))
