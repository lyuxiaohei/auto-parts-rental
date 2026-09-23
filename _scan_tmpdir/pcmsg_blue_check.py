# -*- coding: utf-8 -*-
"""pc-msg 蓝色主题验证：标签蓝底蓝字·面板内零紫元素·开合与零 JS 错误回归"""
import io, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = (Path(__file__).resolve().parents[1] / "P3-R01-包装租赁管理后台原型")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
results = []

def ck(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(detail) if detail else ""))

def rgb_eq(css_str, triple):
    import re
    m = re.search(r"rgb\((\d+), (\d+), (\d+)\)", css_str or "")
    return bool(m) and tuple(map(int, m.groups())) == triple

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((ROOT / "我的待办.html").as_uri())
    pg.wait_for_load_state("networkidle")
    pg.locator('.ico-btn[title="通知"]').click()
    pg.wait_for_timeout(350)

    st = pg.evaluate("""() => {
      const t = document.querySelector('.pc-msg-tag'); const cs = getComputedStyle(t);
      const all = [...document.querySelectorAll('.pc-msg-panel, .pc-msg-panel *')];
      const purple = all.filter(el => {
        const c = getComputedStyle(el);
        return c.color === 'rgb(114, 46, 209)' || c.backgroundColor === 'rgb(249, 240, 255)';
      }).map(el => el.className);
      return {tagColor: cs.color, tagBg: cs.backgroundColor, purple: purple,
              open: document.querySelector('.pc-msg-panel').classList.contains('pc-msg-show')};
    }""")
    ck("标签蓝字 #1677ff", rgb_eq(st["tagColor"], (22, 119, 255)), st["tagColor"])  # 0x16=22
    ck("标签蓝底 #e6f4ff", rgb_eq(st["tagBg"], (230, 244, 255)), st["tagBg"])
    ck("面板内零紫元素", len(st["purple"]) == 0, st["purple"])
    ck("抽屉正常打开（回归）", st["open"])
    pg.screenshot(path=str(Path(__file__).resolve().parent / "pcmsg_blue.png"))
    b.close()

print("==== %d/%d PASS ====" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
