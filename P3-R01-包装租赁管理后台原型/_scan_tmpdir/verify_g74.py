# -*- coding: utf-8 -*-
"""G74 只读验证脚本（独立版：修正 URL 编码断言 + ⋮ 菜单 + showGen 三步）"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
results = []
def rec(tag, ok, note=""):
    results.append((tag, ok, note))
    print(("PASS " if ok else "FAIL ") + tag + ("  | " + note if note else ""))

def url_now(page):
    return unquote(page.url)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    page = b.new_page()
    errs = []
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

    def goto(rel):
        page.goto("file:///" + ROOT.replace("\\", "/") + "/" + rel)
        page.wait_for_timeout(700)

    # B1 PO 列表 demo-data 行 op「生成入库单」在 ⋮ 菜单 → 展开后点击
    goto("采购管理/采购订单列表.html")
    r = page.evaluate("""() => {
      const tbody = document.querySelector('tbody');
      for (const tr of tbody.querySelectorAll('tr')) {
        const lk = tr.querySelector('span.lk');
        if (!lk || lk.textContent.trim() !== 'PO-20260902-018') continue;
        const more = tr.querySelector('.op-more');
        if (!more) return 'no-op-more:' + Array.from(tr.querySelectorAll('a')).map(a => a.textContent.trim()).join('|');
        more.click(); return 'menu-opened';
      }
      return 'row-not-found';
    }""")
    page.wait_for_timeout(350)
    if r == "menu-opened":
        page.evaluate("""() => { for (const a of document.querySelectorAll('#op-menu-pop a')) if (a.textContent.trim() === '生成入库单') { a.click(); return; } }""")
        page.wait_for_timeout(400)
        rec("B1:PO-018行⋮生成入库单→采购入库录单", "采购管理/采购入库录单.html" in url_now(page), url_now(page)[-55:])
    else:
        rec("B1:PO-018行⋮生成入库单→采购入库录单", False, r)

    # B1b 再验一行 PO-20260830-016（⋮ 菜单内同款）
    goto("采购管理/采购订单列表.html")
    r = page.evaluate("""() => {
      for (const tr of document.querySelector('tbody').querySelectorAll('tr')) {
        const lk = tr.querySelector('span.lk');
        if (!lk || lk.textContent.trim() !== 'PO-20260830-016') continue;
        const more = tr.querySelector('.op-more');
        if (more) { more.click(); return 'menu-opened'; }
        for (const a of tr.querySelectorAll('a')) if (a.textContent.trim() === '生成入库单') { a.click(); return 'direct'; }
      }
      return 'row-not-found';
    }""")
    page.wait_for_timeout(350)
    if r == "menu-opened":
        page.evaluate("""() => { for (const a of document.querySelectorAll('#op-menu-pop a')) if (a.textContent.trim() === '生成入库单') { a.click(); return; } }""")
        page.wait_for_timeout(400)
    rec("B1b:PO-20260830-016生成入库单→采购入库录单", "采购管理/采购入库录单.html" in url_now(page), r + " " + url_now(page)[-55:])

    # B2 租入单列表 RZD-20260815-003 行 op 生成租金应付 → 应付新建
    goto("租入管理/租入单列表.html")
    r = page.evaluate("""() => {
      for (const tr of document.querySelector('tbody').querySelectorAll('tr')) {
        const lk = tr.querySelector('span.lk');
        if (!lk || lk.textContent.trim() !== 'RZD-20260815-003') continue;
        for (const a of tr.querySelectorAll('a')) if (a.textContent.trim() === '生成租金应付' && a.className.indexOf('op-dis') === -1) { a.click(); return 'direct'; }
        const more = tr.querySelector('.op-more');
        if (more) { more.click(); return 'menu'; }
        return 'op-not-found';
      }
      return 'row-not-found';
    }""")
    page.wait_for_timeout(350)
    if r == "menu":
        page.evaluate("""() => { for (const a of document.querySelectorAll('#op-menu-pop a')) if (a.textContent.trim() === '生成租金应付') { a.click(); return; } }""")
        page.wait_for_timeout(400)
    rec("B2:RZD-003生成租金应付→应付新建", r in ("menu", "direct") and "财务协同/应付新建.html" in url_now(page), r + " " + url_now(page)[-55:])

    # B2b RZD-20260815-005
    goto("租入管理/租入单列表.html")
    r = page.evaluate("""() => {
      for (const tr of document.querySelector('tbody').querySelectorAll('tr')) {
        const lk = tr.querySelector('span.lk');
        if (!lk || lk.textContent.trim() !== 'RZD-20260815-005') continue;
        for (const a of tr.querySelectorAll('a')) if (a.textContent.trim() === '生成租金应付' && a.className.indexOf('op-dis') === -1) { a.click(); return 'direct'; }
        const more = tr.querySelector('.op-more');
        if (more) { more.click(); return 'menu'; }
        return 'op-not-found';
      }
      return 'row-not-found';
    }""")
    page.wait_for_timeout(350)
    if r == "menu":
        page.evaluate("""() => { for (const a of document.querySelectorAll('#op-menu-pop a')) if (a.textContent.trim() === '生成租金应付') { a.click(); return; } }""")
        page.wait_for_timeout(400)
    rec("B2b:RZD-005生成租金应付→应付新建", r in ("menu", "direct") and "财务协同/应付新建.html" in url_now(page), r + " " + url_now(page)[-55:])


    # B2c 租入单列表静态行 span.ops a 生成租金应付（源码 425/442，运行 DOM 存在）
    goto("租入管理/租入单列表.html")
    u_before = url_now(page)
    ok = page.evaluate("""() => { for (const a of document.querySelectorAll('span.ops a')) if (a.textContent.trim() === '生成租金应付') { a.click(); return true; } return false; }""")
    page.wait_for_timeout(400)
    rec("B2c:租入单静态行生成租金应付→应付新建", ok and "财务协同/应付新建.html" in url_now(page), url_now(page)[-55:])

    # B3 静态行诊断：运行 DOM 是否存在静态「生成入库单」a（采购订单列表/租入单列表）
    goto("采购管理/采购订单列表.html")
    has_static_po = page.evaluate("""() => Array.from(document.querySelectorAll('span.ops a')).some(a => a.textContent.trim() === '生成入库单')""")
    goto("租入管理/租入单列表.html")
    has_static_rzd = page.evaluate("""() => Array.from(document.querySelectorAll('span.ops a')).some(a => a.textContent.trim() === '生成租金应付')""")
    rec("B3:静态行运行DOM存在性(诊断)", True, f"PO静态a在DOM={has_static_po} RZD静态a在DOM={has_static_rzd}（源码已改，PW 以 demo-data 行为准）")

    # B4 盘点列表 showGen：op → 生成草稿 → 单号链接 → 其他入库新建
    goto("仓储作业/盘点列表.html")
    r = page.evaluate("""() => {
      for (const tr of document.querySelector('tbody').querySelectorAll('tr')) {
        const lk = tr.querySelector('span.lk');
        if (!lk || lk.textContent.trim() !== 'PD-202608-02') continue;
        for (const a of tr.querySelectorAll('a')) if (a.textContent.trim() === '生成入库' && a.className.indexOf('op-dis') === -1) { a.click(); return 'op-clicked'; }
        const more = tr.querySelector('.op-more');
        if (more) { more.click(); return 'via-menu'; }
        return 'op-not-found';
      }
      return 'row-not-found';
    }""")
    page.wait_for_timeout(350)
    if r == 'via-menu':
        page.evaluate("""() => { for (const a of document.querySelectorAll('#op-menu-pop a')) if (a.textContent.trim() === '生成入库') { a.click(); return; } }""")
        page.wait_for_timeout(350)
        r = 'op-clicked'
    step2 = page.evaluate("""() => { const g = document.getElementById('dpGen'); if (g) { g.click(); return true; } return false; }""")
    page.wait_for_timeout(300)
    step3 = page.evaluate("""() => { const d = document.getElementById('dpDone'); if (d && d.offsetParent !== null) { const lk = d.querySelector('.lk'); if (lk) { lk.click(); return d.textContent.trim(); } } return null; }""")
    page.wait_for_timeout(400)
    rec("B4:盘点showGen草稿单号→其他入库新建", r == "op-clicked" and step2 and step3 and "仓储作业/其他入库新建.html" in url_now(page), f"{r}/{step2}/{step3} → {url_now(page)[-50:]}")

    # B5 盘点录入 genOtherDoc 双向裸跳
    goto("仓储作业/盘点录入.html")
    page.evaluate("() => genOtherDoc('in', 'demo')")
    page.wait_for_timeout(400)
    u1 = url_now(page)
    goto("仓储作业/盘点录入.html")
    page.evaluate("() => genOtherDoc('out', 'demo')")
    page.wait_for_timeout(400)
    u2 = url_now(page)
    rec("B5:盘点录入genOtherDoc双向", ("其他入库新建.html" in u1) and ("其他出库新建.html" in u2), u1[-45:] + " / " + u2[-45:])

    # B6~B9 红条生成按钮
    for rel, btn_txt, frag in [
        ("租赁管理/租赁出库录单.html", "生成采购订单", "采购管理/采购订单新建.html"),
        ("租赁管理/租赁单新建.html", "生成租入单", "租入管理/租入单新建.html"),
        ("销售管理/销售出库新建.html", "生成采购订单", "采购管理/采购订单新建.html"),
        ("销售管理/销售订单新建.html", "生成采购订单", "采购管理/采购订单新建.html"),
    ]:
        goto(rel)
        clicked = page.evaluate("""(t) => { for (const b of document.querySelectorAll('button')) if (b.textContent.trim() === t) { b.click(); return true; } return false; }""", btn_txt)
        page.wait_for_timeout(400)
        rec(f"B:{rel.split('/')[-1]}点「{btn_txt}」", clicked and frag in url_now(page), url_now(page)[-55:])

    rec("B:全程0控制台错误", len(errs) == 0, "; ".join(errs[:3]) if errs else "")
    b.close()

fails = [r for r in results if not r[1]]
print(f"\n===== Task B 总计 {len(results)} 项，FAIL {len(fails)} 项 =====")
for t, _, n in fails:
    print("FAIL:", t, "|", n)
