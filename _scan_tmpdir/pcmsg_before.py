# -*- coding: utf-8 -*-
"""pc-msg 改抽屉前取证：开铃铛消息面板截图 + 几何量测"""
import io, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1] / "P3-R01-包装租赁管理后台原型"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
OUT = Path(__file__).resolve().parent / "pcmsg_before.png"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((ROOT / "我的待办.html").as_uri())
    pg.wait_for_load_state("networkidle")
    bell = pg.locator('.ico-btn[title="通知"]')
    bell.click()
    pg.wait_for_timeout(300)
    pg.screenshot(path=str(OUT))
    box = pg.evaluate("""() => {
      const pn = document.querySelector('.pc-msg-panel');
      const r = pn.getBoundingClientRect();
      const flt = pn.querySelector('.pc-msg-flt');
      return {display: getComputedStyle(pn).display, rect: [r.x, r.y, r.width, r.height].map(v=>Math.round(v)),
              fltExists: !!flt, fltText: flt ? flt.innerText : null};
    }""")
    print("panel:", box)
    print("js errors:", errs)
    b.close()
print("shot:", OUT)
