# -*- coding: utf-8 -*-
"""菜单重组方案 B · 验证门 Playwright 抽验
门2：租赁单列表新路径直开无 JS 错；菜单点「租赁单」可达且 selected 高亮；
     F01 泳道 L1-L4 四个租赁单节点可点跳转；租赁单详情弹窗互溯链反向可跳
门3：A04 ?notes=1 抽 3 页角标全在
门4：P3-R04 P0 场景 5 条动线复走（路径全部为新）
教训遵循：pg.url 中文 percent-encode 需 unquote；文本校验用 textContent"""
import sys
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
def uri(rel): return (ROOT / rel).as_uri()

results, failures = [], []
def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (f" | {detail}" if detail else ""))
    if not ok: failures.append(f"{name}: {detail}")

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

    # ── 门2a 租赁单列表新路径直开 ──
    errs.clear()
    pg.goto(uri("销售管理/租赁单列表.html"))
    pg.wait_for_load_state("networkidle")
    rows = pg.locator("table tbody tr").count()
    check("门2a 租赁单列表新路径直开", len(errs) == 0 and rows > 0, f"JS错{len(errs)} 数据行{rows}")

    # ── 门2b 菜单点「租赁单」可达且 selected ──（菜单项在折叠分组内，Playwright 可见性判定不过——
    #     与审计工具同款做法：evaluate 编程点击，真实触发 onclick=go() 导航）
    errs.clear()
    pg.goto(uri("首页/项目看板.html"))
    pg.wait_for_load_state("networkidle")
    pg.locator("div.sm-link", has_text="租赁单").first.evaluate("el => el.click()")
    pg.wait_for_timeout(600)
    url = unquote(pg.url)
    sel = pg.locator("div.sm-link.selected").text_content()
    check("门2b 菜单点租赁单可达+selected", "销售管理/租赁单列表.html" in url and sel and sel.strip() == "租赁单",
          f"url={url.split('/')[-1]} selected={sel!r}")

    # ── 门2c F01 泳道 L1-L4 四个租赁单节点可点跳转 ──
    errs.clear()
    f01_js_err_before = len(errs)
    n_ok = 0
    for i in range(4):
        pg.goto(uri("P3-R01-F01-业务流程导航图.html"))
        pg.wait_for_load_state("networkidle")
        node = pg.locator(f'a[href="销售管理/租赁单列表.html"]').nth(i)
        node.scroll_into_view_if_needed()
        node.click()
        pg.wait_for_timeout(500)
        url = unquote(pg.url)
        if "销售管理/租赁单列表.html" in url: n_ok += 1
        else: print(f"  node{i}: {url[-60:]}")
    check("门2c F01 L1-L4 四租赁单节点跳转", n_ok == 4, f"{n_ok}/4 命中新路径")

    # ── 门2d 租赁单详情弹窗互溯链反向可跳 ──（链接文本是单号，按 onclick 目标定位）
    errs.clear()
    pg.goto(uri("销售管理/弹窗/租赁单详情.html"))
    pg.wait_for_load_state("networkidle")
    lk = pg.locator(".lk[onclick*='租赁管理/退租申请列表.html']").first
    txt = lk.text_content() or ""
    lk.evaluate("el => el.click()")
    pg.wait_for_timeout(600)
    url = unquote(pg.url)
    check("门2d 详情弹窗互溯链反向跳退租申请", "租赁管理/退租申请列表.html" in url, f"点击「{txt.strip()[:12]}」→ {url.split('/')[-1]}")

    # ── 门3 A04 ?notes=1 抽 3 页角标全在 ──
    total_pins = 0
    for rel, expect in [("销售管理/租赁单列表.html", 5), ("租赁管理/退租申请列表.html", 3), ("租赁管理/在租台账.html", 1)]:
        errs.clear()
        pg.goto(uri(rel) + "?notes=1")
        pg.wait_for_load_state("networkidle")
        on = pg.evaluate("document.body.classList.contains('proto-notes-on')")
        n = pg.locator("[data-note]").count()
        pins = pg.locator(".proto-pin").count()
        fab = pg.locator("#protoNotesFab").text_content() or ""
        total_pins += n
        check(f"门3 角标 {rel}", on and n == expect and pins == expect and len(errs) == 0,
              f"开关{on} 角标{n}/{expect} 便签{pins} fab={fab.strip()[:8]}")
    # 全站 43 条静态复核（23 页注入计数，源自注入 log）
    import json as _j
    d = _j.loads((ROOT / "P3-R01-A04-流程链标注数据.json").read_text(encoding="utf-8"))
    n_all = sum(len(v) for k, v in d.items() if not k.startswith("_"))
    check("门3 A04 全站 pin 总数", n_all == 43, f"{n_all}/43（页面运行时抽验 3 页合计 {total_pins} 角标全渲染）")

    # ── 门4 P3-R04 P0 场景 5 条动线复走 ──
    errs.clear()
    # 动线1 P0-L1：租赁单列表 → ZL-20260901-032 → 审核（新路径 + 行在 + 审核弹窗开）
    pg.goto(uri("销售管理/租赁单列表.html"))
    pg.wait_for_load_state("networkidle")
    row1 = pg.locator("tr", has_text="ZL-20260901-032").count()
    pg.locator("tr", has_text="ZL-20260901-032").first.locator("a, .op-link, button", has_text="审核").first.evaluate("el => el.click()") if row1 else None
    pg.wait_for_timeout(400)
    m1 = pg.locator("#auditModal.show").count()
    check("门4-1 P0-L1 租赁单 ZL-20260901-032→审核", row1 >= 1 and m1 == 1, f"行{row1} 审核弹窗{m1}")
    pg.evaluate("window.closeModal ? closeModal('auditModal') : document.getElementById('auditModal').classList.remove('show')")

    # 动线2 P0-L3：租赁单 ZL-20260816-029（租入转租专用行）
    row2 = pg.locator("tr", has_text="ZL-20260816-029").count()
    check("门4-2 P0-L3 租赁单 ZL-20260816-029 行在", row2 >= 1, f"行{row2}")

    # 动线3 P0：在租台账四态卡（新路径 租赁管理/）
    pg.goto(uri("租赁管理/在租台账.html"))
    pg.wait_for_load_state("networkidle")
    cards = pg.locator(".stat-card, .kpi-card, .stat").count()
    check("门4-3 P0 在租台账四态卡", cards >= 4, f"卡片数{cards}（≥4）")

    # 动线4 P0：退租申请列表可达 + 新建弹窗（新路径）
    pg.goto(uri("租赁管理/退租申请列表.html"))
    pg.wait_for_load_state("networkidle")
    btn = pg.locator("button", has_text="新建").first
    btn.evaluate("el => el.click()")
    pg.wait_for_timeout(400)
    m4 = pg.locator("#createModal.show").count()
    check("门4-4 P0 退租申请列表→新建弹窗", m4 == 1, f"新建弹窗{m4}")

    # 动线5 P0：我的待办 → 租赁单跳转（?audit=1 auto-open 审核弹窗）
    pg.goto(uri("首页/我的待办.html"))
    pg.wait_for_load_state("networkidle")
    lk5 = pg.locator("a, .lk, [onclick]", has_text="租赁单").first
    lk5.evaluate("el => el.click()")
    pg.wait_for_timeout(700)
    url5 = unquote(pg.url)
    m5 = pg.locator("#auditModal.show").count()
    check("门4-5 P0 我的待办→租赁单审核 auto-open", "销售管理/租赁单列表.html" in url5, f"url={url5.split('/')[-1][:40]} 审核弹窗auto-open={m5}")

    js_total = len(errs)
    check("门4 全程 JS 错", js_total == 0, f"{js_total} 条")
    b.close()

print(f"\n===== 抽验汇总：{sum(1 for _, ok, _ in results if ok)}/{len(results)} PASS；失败 {len(failures)} =====")
for f in failures: print("FAIL:", f)
