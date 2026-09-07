# -*- coding: utf-8 -*-
"""业务场景补充 /goal · 验证门 Playwright 抽验
门A 在租台账：新页签渲染+可切换 active+口径注记在
门B 应收/应付：预收/预付行渲染；详情弹窗（内嵌+独立模板双层）时间线含预收/预付节点
门C 水单核销：类型筛选含 预收款/预付款 选项；dzTable 预收款示例行在
门D F01：预收/预付注记行渲染且无遮挡（text-vs-rect 差分断言：与押金行同环境、零新增交叠）
门E 标注层专项 3 页（客商管理/用户权限/盘点列表）：默认态无裸露便签；?notes=1 角标可点开便签、Alt+N/右下角按钮开关正常
教训遵循：中文 URL 判定 unquote()；文本断言用 textContent；点击用 Playwright 真实点击"""
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
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

    # ── 门A 在租台账 ──
    errs.clear()
    pg.goto(uri("租赁管理/在租台账.html"))
    pg.wait_for_load_state("networkidle")
    tabs = pg.locator(".stabs .stab")
    n_tabs, t_all, t_due = tabs.count(), tabs.nth(0), tabs.nth(1)
    txt_all, txt_due = t_all.text_content(), t_due.text_content()
    check("A1 即将到期页签渲染", n_tabs == 2 and "全部" in txt_all and "即将到期(7天)" in txt_due and "6" in txt_due,
          f"tabs={n_tabs} 全部={txt_all!r} 新={txt_due!r}")
    check("A2 默认 active=全部", "active" in (t_all.get_attribute("class") or ""), t_all.get_attribute("class"))
    t_due.click()
    check("A3 点击即将到期→active 切换", "active" in (t_due.get_attribute("class") or "") and "active" not in (t_all.get_attribute("class") or ""),
          f"due={t_due.get_attribute('class')!r}")
    hint = pg.locator(".pn-hint").first.text_content()
    check("A4 口径注记在（≤7 天/按页签过滤）", hint is not None and "≤7 天" in hint and "按页签过滤" in hint, (hint or "")[:50])
    check("A5 在租台账 0 JS 错", len(errs) == 0, "; ".join(errs[:2]))

    # ── 门B1 应收账单：预收行 + 内嵌详情时间线 ──
    errs.clear()
    pg.goto(uri("财务协同/应收账单.html"))
    pg.wait_for_load_state("networkidle")
    first = pg.locator("table tbody tr").first
    ftxt = first.text_content()
    check("B1a 应收首行=预收行（安吉智行/¥50,000/已收/冲抵备注）",
          "AR-2026-09-PRJ2601-YS" in ftxt and "安吉智行物流" in ftxt and "50,000.00" in ftxt and "预收" in ftxt and "按月冲抵" in ftxt,
          ftxt.replace("\n", " ")[:80])
    first.locator("a", has_text="详情").click()
    pg.wait_for_timeout(300)
    tl = pg.locator("#detailModal .tl").text_content()
    check("B1b 内嵌详情时间线含预收节点", "预收款到账 · 记预收" in tl and "租金自预收冲抵" in tl, (tl or "")[:80])
    check("B1c 应收 0 JS 错", len(errs) == 0, "; ".join(errs[:2]))

    # ── 门B2 应收独立模板 ──
    errs.clear()
    pg.goto(uri("财务协同/弹窗/应收账单详情.html"))
    pg.wait_for_load_state("networkidle")
    tl = pg.locator(".tl").text_content()
    check("B2 应收账单详情独立模板含预收节点", "预收款到账 · 记预收" in tl and "租金自预收冲抵" in tl, "")

    # ── 门B3 应付账单：预付行 + 内嵌详情时间线 ──
    errs.clear()
    pg.goto(uri("财务协同/应付账单.html"))
    pg.wait_for_load_state("networkidle")
    first = pg.locator("table tbody tr").first
    ftxt = first.text_content()
    check("B3a 应付首行=预付行（路凯/¥30,000/已付款/大箱备注）",
          "AP-20260905-012" in ftxt and "路凯包装运营" in ftxt and "30,000.00" in ftxt and "预付" in ftxt and "大箱租金" in ftxt,
          ftxt.replace("\n", " ")[:80])
    first.locator("a", has_text="详情").click()
    pg.wait_for_timeout(300)
    tl = pg.locator("#detailModal .tl").text_content()
    check("B3b 内嵌详情时间线含预付冲抵节点", "预付款支付 · 记预付" in tl and "预付冲抵" in tl, (tl or "")[:80])
    check("B3c 应付 0 JS 错", len(errs) == 0, "; ".join(errs[:2]))

    # ── 门B4 应付独立模板（数据驱动渲染：调 openPayableBillDetail 后断言）──
    errs.clear()
    pg.goto(uri("财务协同/弹窗/应付账单详情.html"))
    pg.wait_for_load_state("networkidle")
    tl = pg.evaluate("() => { openPayableBillDetail('AP-20260905-012', '../../'); return document.querySelector('.tl').textContent; }")
    check("B4 应付账单详情独立模板含预付冲抵节点（数据驱动）", "预付款支付 · 记预付" in tl and "预付冲抵" in tl, "")

    # ── 门C 水单核销 ──
    errs.clear()
    pg.goto(uri("财务协同/银行水单核销.html"))
    pg.wait_for_load_state("networkidle")
    opts = pg.locator("select[title='类型筛选'] option").all_text_contents()
    check("C1 类型筛选含预收款/预付款", "预收款" in opts and "预付款" in opts and opts[0].startswith("类型"), str(opts))
    dz = pg.locator("#dzTable").text_content()
    check("C2 dzTable 预收款示例行（关联 ¥50,000）", "AR-2026-09-PRJ2601-YS" in dz and "预收款" in dz and "50,000.00" in dz, "")
    check("C3 水单核销 0 JS 错", len(errs) == 0, "; ".join(errs[:2]))

    # ── 门D F01：注记行渲染 + text-vs-rect 差分断言 ──
    errs.clear()
    pg.goto(uri("P3-R01-F01-业务流程导航图.html"))
    pg.wait_for_load_state("networkidle")
    body_txt = pg.evaluate("document.body.textContent")
    check("D1 F01 预收/预付注记渲染", "预收/预付：客户预付租金记预收按月冲抵" in body_txt, "")
    overlap = pg.evaluate("""() => {
      const texts = [...document.querySelectorAll('svg text')].filter(t => (t.textContent || '').includes('押金') || (t.textContent || '').includes('预收/预付'));
      const dep = texts.find(t => (t.textContent || '').includes('预收/预付'));
      const old = texts.find(t => (t.textContent || '').includes('押金：'));
      if (!dep || !old) return {err: 'text 未找到'};
      const fin = dep.closest('svg');
      const rb = r => { const b = r.getBoundingClientRect(); return {x:b.x,y:b.y,w:b.width,h:b.height}; };
      const db = rb(dep), ob = rb(old);
      const rects = [...fin.querySelectorAll('rect')].map(rb);
      const hit = bb => rects.filter(r => !(bb.x + bb.w < r.x || r.x + r.w < bb.x || bb.y + bb.h < r.y || r.y + r.h < bb.y)).length;
      return {newBottom: db.y + db.h, oldBottom: ob.y + ob.h, belowOld: db.y >= ob.y + ob.h - 1,
              newRectHits: hit(db), oldRectHits: hit(ob), svgVB: fin.viewBox.baseVal.height};
    }""")
    ok_d2 = overlap.get("belowOld") and overlap.get("newRectHits") == overlap.get("oldRectHits")
    check("D2 注记行在押金行下方且零新增 rect 交叠（差分）", ok_d2, str(overlap))
    check("D3 F01 0 JS 错", len(errs) == 0, "; ".join(errs[:2]))

    # ── 门E 标注层专项（3 个修复页）──
    for rel in ["基础数据/客商管理.html", "系统管理/用户权限.html", "仓储作业/盘点列表.html"]:
        errs.clear()
        # E-1 默认态：无裸露便签（display:none）、fab 在
        pg.goto(uri(rel))
        pg.wait_for_load_state("networkidle")
        st = pg.evaluate("""() => {
          const pin = document.querySelector('.proto-pin');
          const fab = document.getElementById('protoNotesFab');
          const cs = pin ? getComputedStyle(pin) : null;
          return {pinExists: !!pin, pinDisplay: cs ? cs.display : null,
                  fabExists: !!fab, fabText: fab ? fab.textContent : null,
                  on: document.body.classList.contains('proto-notes-on')};
        }""")
        check(f"E1 {rel.split('/')[-1]} 默认态便签隐藏", st["pinExists"] and st["pinDisplay"] == "none" and not st["on"], str(st))
        # E-2 ?notes=1：角标可见可点、便签就地弹出
        pg.goto(uri(rel) + "?notes=1")
        pg.wait_for_load_state("networkidle")
        st2 = pg.evaluate("""() => ({
          on: document.body.classList.contains('proto-notes-on'),
          fabText: document.getElementById('protoNotesFab').textContent,
          n: document.querySelectorAll('[data-note]').length})""")
        check(f"E2 {rel.split('/')[-1]} ?notes=1 开启+fab 显示收起", st2["on"] and ("收起" in st2["fabText"] or "标注" in st2["fabText"]) and st2["n"] >= 1, str(st2))
        tgt = pg.locator("[data-note]").first
        box = tgt.bounding_box()
        tgt.click(position={"x": box["width"] - 4, "y": 4})
        pg.wait_for_timeout(300)
        pin_open = pg.evaluate("""() => {
          const p = document.querySelector('.proto-pin.pn-open');
          if (!p) return null;
          const b = p.getBoundingClientRect(); const cs = getComputedStyle(p);
          return {w: b.width, h: b.height, disp: cs.display};
        }""")
        check(f"E3 {rel.split('/')[-1]} 点角标便签弹出", pin_open and pin_open["disp"] == "block" and pin_open["w"] > 200, str(pin_open))
        # E-4 三通道：?notes=1 强制开（URL 优先）；fab/Alt+N 走 localStorage——干净页设 '1' 重载后点 fab 关、Alt+N 开
        pg.goto(uri(rel))
        pg.wait_for_load_state("networkidle")
        pg.evaluate("localStorage.setItem('proto-notes-on','1')")
        pg.reload()
        pg.wait_for_load_state("networkidle")
        on_pre = pg.evaluate("() => document.body.classList.contains('proto-notes-on')")
        pg.locator("#protoNotesFab").click()
        pg.wait_for_timeout(200)
        off = pg.evaluate("() => !document.body.classList.contains('proto-notes-on')")
        pg.keyboard.press("Alt+n")
        pg.wait_for_timeout(200)
        on2 = pg.evaluate("() => document.body.classList.contains('proto-notes-on')")
        check(f"E4 {rel.split('/')[-1]} fab 关/Alt+N 开", on_pre and off and on2, f"预开={on_pre} fab关={off} altN开={on2}")
        pg.evaluate("localStorage.removeItem('proto-notes-on')")
        check(f"E5 {rel.split('/')[-1]} 0 JS 错", len(errs) == 0, "; ".join(errs[:2]))

    b.close()

print()
print("=" * 60)
print(f"合计 {len(results)} 项：PASS {sum(1 for _, ok, _ in results if ok)} / FAIL {len(failures)}")
if failures:
    print("失败清单：")
    for f in failures: print(" -", f)
    sys.exit(1)
print("全部通过")
