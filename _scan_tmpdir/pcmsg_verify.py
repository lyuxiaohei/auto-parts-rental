# -*- coding: utf-8 -*-
"""pc-msg 抽屉化验证（改后）：开关/几何/条目排版/三路关闭/筛选/全部已读/跳转·含子目录页"""
import io, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1] / "P3-R01-包装租赁管理后台原型"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
OUT = Path(__file__).resolve().parent / "pcmsg_after.png"
results = []

def ck(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(detail) if detail else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((ROOT / "我的待办.html").as_uri())
    pg.wait_for_load_state("networkidle")

    # 1. 初始关：panel/mask 无 pc-msg-show，mask 不拦截
    st = pg.evaluate("""() => {
      const pn = document.querySelector('.pc-msg-panel'), mk = document.querySelector('.pc-msg-mask');
      const cs = getComputedStyle(mk);
      return {pnShow: pn.classList.contains('pc-msg-show'), mkShow: mk.classList.contains('pc-msg-show'),
              mkPe: cs.pointerEvents, mkOp: cs.opacity};
    }""")
    ck("初始态关闭（无 pc-msg-show·mask 不拦截）", not st["pnShow"] and not st["mkShow"] and st["mkPe"] == "none")

    # 2. 铃铛开抽屉
    pg.locator('.ico-btn[title="通知"]').click()
    pg.wait_for_timeout(350)
    st = pg.evaluate("""() => {
      const pn = document.querySelector('.pc-msg-panel'), mk = document.querySelector('.pc-msg-mask');
      const r = pn.getBoundingClientRect(); const cs = getComputedStyle(pn); const mcs = getComputedStyle(mk);
      return {pnShow: pn.classList.contains('pc-msg-show'), mkShow: mk.classList.contains('pc-msg-show'),
              mkPe: mcs.pointerEvents,
              rect: [r.x, r.y, r.width, r.height].map(v => Math.round(v)), vw: innerWidth, vh: innerHeight,
              transform: cs.transform};
    }""")
    ck("开抽屉（panel+mask 双 show）", st["pnShow"] and st["mkShow"])
    ck("几何：全高右贴边·360宽·已滑入(transform=none)", st["rect"] == [1080, 0, 360, 900] and st["transform"] == "none",
       st["rect"])
    ck("mask 拦截点击", st["mkPe"] == "auto")

    # 3. 条目排版：首条头行（点+标签+时间同行）时间右吸齐、正文第二行
    lay = pg.evaluate("""() => {
      const it = document.querySelector('.pc-msg-item[data-id="m1"]');
      const tag = it.querySelector('.pc-msg-tag').getBoundingClientRect();
      const time = it.querySelector('.pc-msg-time').getBoundingClientRect();
      const body = it.querySelector('.pc-msg-body').getBoundingClientRect();
      const item = it.getBoundingClientRect();
      return {sameRow: Math.abs(tag.top - time.top) < 1 && Math.abs(tag.height - time.height) < 8,
              timeRight: Math.round(item.right - time.right),
              bodyBelow: Math.round(body.top - tag.bottom)};
    }""")
    ck("条目头行=点+标签+时间同行", lay["sameRow"], lay)
    ck("时间右吸齐（贴条目右缘±6）", abs(lay["timeRight"] - 12) < 6, lay["timeRight"])
    ck("正文在头行下方另起", lay["bodyBelow"] > 0, lay["bodyBelow"])

    pg.screenshot(path=str(OUT))

    # 4. 筛选：选「押金应退」只剩 1 条
    pg.select_option('#pcMsgTag', '押金应退')
    pg.wait_for_timeout(100)
    n = pg.locator('.pc-msg-item').count()
    ck("筛选「押金应退」=1条", n == 1, n)
    pg.select_option('#pcMsgTag', '全部')
    pg.wait_for_timeout(100)

    # 5. 全部标为已读 → 4条全灰点 + 角标消失
    pg.click('.pc-msg-all')
    pg.wait_for_timeout(100)
    st = pg.evaluate("""() => ({
      dots: document.querySelectorAll('.pc-msg-dot.read').length,
      badgeShown: getComputedStyle(document.querySelector('.pc-msg-badge')).display !== 'none'
    })""")
    ck("全部标为已读（4灰点+角标隐藏）", st["dots"] == 4 and not st["badgeShown"], st)

    # 6. Esc 关
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)
    ck("Esc 关闭", not pg.locator('.pc-msg-panel').evaluate("el => el.classList.contains('pc-msg-show')"))

    # 7. 点遮罩关
    pg.locator('.ico-btn[title="通知"]').click(); pg.wait_for_timeout(300)
    pg.mouse.click(200, 450); pg.wait_for_timeout(300)
    ck("点遮罩关闭", not pg.locator('.pc-msg-panel').evaluate("el => el.classList.contains('pc-msg-show')"))

    # 8. × 关
    pg.locator('.ico-btn[title="通知"]').click(); pg.wait_for_timeout(300)
    pg.click('.pc-msg-close'); pg.wait_for_timeout(300)
    ck("× 关闭", not pg.locator('.pc-msg-panel').evaluate("el => el.classList.contains('pc-msg-show')"))

    # 9. 条目点击跳转（重置已读态后点 m4 → 租赁单列表）
    pg.evaluate("() => localStorage.removeItem('pc-msg-read')")
    pg.reload(); pg.wait_for_load_state("networkidle")
    pg.locator('.ico-btn[title="通知"]').click(); pg.wait_for_timeout(300)
    with pg.expect_navigation():
        pg.click('.pc-msg-item[data-id="m4"]')
    import urllib.parse
    ck("条目点击跳转租赁单列表", "租赁单列表" in urllib.parse.unquote(pg.url),
       urllib.parse.unquote(pg.url.split("/")[-1]))

    # 10. 子目录页（../_data 前缀）开合 + 零 JS 错误
    pg.goto((ROOT / "财务协同" / "应付账单.html").as_uri())
    pg.wait_for_load_state("networkidle")
    pg.locator('.ico-btn[title="通知"]').click(); pg.wait_for_timeout(300)
    ck("子目录页(应付账单)抽屉可开",
       pg.locator('.pc-msg-panel').evaluate("el => el.classList.contains('pc-msg-show')"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    ck("全程零 JS 错误", len(errs) == 0, errs[:3])
    b.close()

fails = [r for r in results if not r[1]]
print("\n==== %d/%d PASS · %d FAIL ====" % (len(results) - len(fails), len(results), len(fails)))
sys.exit(1 if fails else 0)
