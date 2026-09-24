# -*- coding: utf-8 -*-
"""G73/G74 只读验证脚本（不动页面数据；提交均为演示不落库）"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"

PAGES = [
    ("lz",   "租赁管理/租赁单列表.html",   "lzBatchModal", ["ZL-20260901-032"]),
    ("rzd",  "租入管理/租入单列表.html",   "rzdBatchModal", ["RZD-20260902-008"]),
    ("ck",   "租赁管理/租赁出库列表.html", "ckBatchModal", ["CK-20260910-022", "CK-20260914-023"]),
    ("ghck", "租入管理/归还出库列表.html", "ghckBatchModal", ["GHCK-20260903-002"]),
    ("so",   "销售管理/销售订单列表.html", "soBatchModal", ["SO-20260902-0046", "SO-20260901-0045"]),
    ("xsck", "销售管理/销售出库列表.html", "xsckBatchModal", ["XSCK-20260902-015"]),
    ("qtrk", "仓储作业/其他入库列表.html", "qtrkBatchModal", ["QTRK-20260901-003"]),
    ("qtck", "仓储作业/其他出库列表.html", "qtckBatchModal", ["QTCK-20260901-004"]),
    ("pd",   "仓储作业/盘点列表.html",     "pdBatchModal", ["PD-202608-02"]),
    ("db",   "仓储作业/库存调拨列表.html", "dbBatchModal", ["DB-20260901-003"]),
    ("cgth", "采购管理/采购退货单列表.html", "cgthBatchModal", ["CGTH-20260915-004"]),
    ("xsth", "销售管理/销售退货单列表.html", "xsthBatchModal", ["XSTH-20260911-003"]),
    ("zy",   "租赁管理/转移出库列表.html", "zyBatchModal", ["ZY-20260915-005"]),
    ("tzrk", "租赁管理/退租入库列表.html", "tzrkBatchModal", ["TZRK-20260902-010", "TZRK-20260903-009", "TZRK-20260902-008"]),
]
SHOT = {"lz", "ck", "so", "pd", "db", "tzrk"}

results = []
def rec(tag, ok, note=""):
    results.append((tag, ok, note))
    print(("PASS " if ok else "FAIL ") + tag + ("  | " + note if note else ""))

def toast_texts(page):
    return page.evaluate(
        "() => Array.from(document.querySelectorAll('body > div'))"
        ".filter(d => (d.id || '').toLowerCase().includes('toast') && d.style.display !== 'none' && d.textContent.trim())"
        ".map(d => d.textContent.trim())")

def run_page(page, p, path, mid, expect_keys):
    url = "file:///" + ROOT.replace("\\", "/") + "/" + path
    errs = []
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    page.goto(url)
    page.wait_for_timeout(700)

    btn = page.locator(f"button:has-text('批量审核')").first
    rec(f"{p}:按钮存在", btn.count() > 0)
    op0 = btn.evaluate("b => parseFloat(b.style.opacity || '1')")
    rec(f"{p}:初始禁用(opacity<1)", op0 < 1, f"opacity={op0}")

    # 禁用态点击 → 弹窗不开
    btn.click()
    page.wait_for_timeout(250)
    rec(f"{p}:禁用态点击不开弹窗", not page.locator(f"#{mid}.show").count())

    # 全勾 → 启用
    page.evaluate("() => document.querySelectorAll('tbody input[type=checkbox]').forEach(c => { if (!c.checked) c.click(); })")
    page.wait_for_timeout(250)
    op1 = btn.evaluate("b => parseFloat(b.style.opacity || '1')")
    rec(f"{p}:勾选后启用", op1 >= 1, f"opacity={op1}")

    btn.click()
    page.wait_for_timeout(300)
    shown = page.evaluate(f"() => document.getElementById('{mid}').classList.contains('show')")
    rec(f"{p}:弹窗打开", shown)
    if not shown:
        rec(f"{p}:SKIP后续", False, "弹窗未开，跳过本页后续断言")
        return
    cnt = page.evaluate(f"() => document.getElementById('{mid.replace('BatchModal','BatchCount')}').textContent.trim()")
    nrow = page.evaluate(f"() => document.querySelectorAll('#{mid.replace('BatchModal','BatchList')} tr').length")
    rec(f"{p}:计数=列表行数", cnt.isdigit() and int(cnt) == nrow and nrow >= 1, f"count={cnt} rows={nrow}")
    keys_in = page.evaluate(
        f"() => Array.from(document.querySelectorAll('#{mid.replace('BatchModal','BatchList')} td:first-child')).map(t => t.textContent.trim())")
    hit = [k for k in expect_keys if any(k in x for x in keys_in)]
    rec(f"{p}:列表含预期待审核单号", len(hit) >= 1, f"hit={hit}")

    # 结论切换 → 驳回
    page.evaluate(f"() => Array.from(document.querySelectorAll('#{mid} .radio')).find(r => r.getAttribute('data-v')==='驳回').click()")
    page.wait_for_timeout(150)
    st = page.evaluate(f"() => {{ const rs = document.querySelectorAll('#{mid} .radio'); return [rs[0].classList.contains('checked'), rs[1].classList.contains('checked')]; }}")
    rec(f"{p}:结论切换驳回", st == [False, True], str(st))

    page.locator(f"#{mid} button:has-text('确认提交')").click()
    page.wait_for_timeout(350)
    closed = not page.evaluate(f"() => document.getElementById('{mid}').classList.contains('show')")
    tt = [t for t in toast_texts(page) if "已批量审核" in t]
    rec(f"{p}:提交关窗+toast", closed and len(tt) == 1 and f"已批量审核 {nrow} 单：驳回（演示）" in tt[0], tt[0] if tt else "no-toast")

    # 遮罩关闭
    page.wait_for_timeout(200)
    btn.click()
    page.wait_for_timeout(250)
    page.evaluate(f"() => document.getElementById('{mid}').dispatchEvent(new MouseEvent('click', {{bubbles: true}}))")
    page.wait_for_timeout(250)
    rec(f"{p}:遮罩关闭", not page.evaluate(f"() => document.getElementById('{mid}').classList.contains('show')"))

    # 空勾选拦截
    page.evaluate("() => document.querySelectorAll('tbody input[type=checkbox]').forEach(c => { if (c.checked) c.click(); })")
    page.wait_for_timeout(250)
    btn.click()
    page.wait_for_timeout(300)
    notopen = not page.evaluate(f"() => document.getElementById('{mid}').classList.contains('show')")
    tt2 = [t for t in toast_texts(page) if t.startswith("勾选的行中没有待审核")]
    rec(f"{p}:空勾选拦截", notopen and len(tt2) >= 1, tt2[0] if tt2 else "no-toast")

    rec(f"{p}:0控制台错误", len(errs) == 0, "; ".join(errs[:3]) if errs else "")

    if p in SHOT:
        page.evaluate(f"() => {{ document.querySelectorAll('tbody input[type=checkbox]').forEach(c => {{ if (!c.checked) c.click(); }}); }}")
        page.wait_for_timeout(200)
        btn.click()
        page.wait_for_timeout(350)
        page.screenshot(path=ROOT + f"\\_scan_tmpdir\\g73_{p}.png")
        page.evaluate(f"() => document.getElementById('{mid}').classList.remove('show')")

def run_b(page):
    print("\n===== Task B 生成XX单跳转验证 =====")
    def goto(rel):
        page.goto("file:///" + ROOT.replace("\\", "/") + "/" + rel)
        page.wait_for_timeout(700)

    def click_row_op(page, key, optext):
        return page.evaluate(
            """([key, optext]) => {
              const tbody = document.querySelector('tbody');
              if (!tbody) return 'no-tbody';
              for (const tr of tbody.querySelectorAll('tr')) {
                const lk = tr.querySelector('span.lk');
                if (!lk || lk.textContent.trim() !== key) continue;
                for (const a of tr.querySelectorAll('a')) {
                  if (a.textContent.trim() === optext && a.className.indexOf('op-dis') === -1) { a.click(); return 'clicked'; }
                }
                const menu = tr.querySelector('.op-menu, [class*=menu]');
                return 'op-not-found:' + Array.from(tr.querySelectorAll('a')).map(a => a.textContent.trim()).join('|');
              }
              return 'row-not-found';
            }""", [key, optext])

    # B1 采购订单列表 demo-data 行 op 生成入库单 → 采购入库录单
    goto("采购管理/采购订单列表.html")
    r = click_row_op(page, "PO-20260902-018", "生成入库单")
    page.wait_for_timeout(400)
    ok = r == "clicked" and "采购管理/采购入库录单.html" in page.url
    rec("B1:PO列表行op生成入库单→录单页", ok, r + " url=" + page.url[-60:])

    # B2 租入单列表 行 op 生成租金应付 → 应付新建
    goto("租入管理/租入单列表.html")
    r = click_row_op(page, "RZD-20260815-003", "生成租金应付")
    page.wait_for_timeout(400)
    ok = r == "clicked" and "财务协同/应付新建.html" in page.url
    rec("B2:租入单行op生成租金应付→应付新建", ok, r + " url=" + page.url[-60:])

    # B3 采购订单列表静态 a 生成入库单（第一个）
    goto("采购管理/采购订单列表.html")
    href = page.evaluate(
        "() => { for (const a of document.querySelectorAll('a')) if (a.textContent.trim()==='生成入库单') { a.click(); return a.getAttribute('onclick') || a.getAttribute('href'); } return null; }")
    page.wait_for_timeout(400)
    ok = href is not None and "采购管理/采购入库录单.html" in page.url
    rec("B3:PO列表静态生成入库单→录单页", ok, str(href))

    # B4 盘点列表 showGen → 其他入库新建
    goto("仓储作业/盘点列表.html")
    r = click_row_op(page, "PD-202608-02", "生成入库")
    page.wait_for_timeout(400)
    clicked = page.evaluate(
        "() => { const els = Array.from(document.querySelectorAll('a, span.lk, .lk')); for (const e of els) { const oc = e.getAttribute('onclick') || ''; if (oc.indexOf('其他入库新建') > -1 && e.offsetParent) { e.click(); return oc; } } return null; }")
    page.wait_for_timeout(400)
    ok = clicked is not None and "仓储作业/其他入库新建.html" in page.url
    rec("B4:盘点showGen草稿链接→其他入库新建", ok, str(clicked) + " url=" + page.url[-50:])

    # B5 盘点录入 genOtherDoc → 其他入库新建 / 其他出库新建
    goto("仓储作业/盘点录入.html")
    page.evaluate("() => genOtherDoc('in', 'demo')")
    page.wait_for_timeout(400)
    u1 = page.url
    page.goto("file:///" + ROOT.replace("\\", "/") + "/仓储作业/盘点录入.html")
    page.wait_for_timeout(500)
    page.evaluate("() => genOtherDoc('out', 'demo')")
    page.wait_for_timeout(400)
    u2 = page.url
    rec("B5:盘点录入genOtherDoc双向", ("其他入库新建.html" in u1) and ("其他出库新建.html" in u2), u1[-40:] + " / " + u2[-40:])

    # B6~B9 红条生成按钮 4 页
    for rel, btn_txt, frag in [
        ("租赁管理/租赁出库录单.html", "生成采购订单", "采购管理/采购订单新建.html"),
        ("租赁管理/租赁单新建.html", "生成租入单", "租入管理/租入单新建.html"),
        ("销售管理/销售出库新建.html", "生成租入单", "租入管理/租入单新建.html"),
        ("销售管理/销售订单新建.html", "生成采购订单", "采购管理/采购订单新建.html"),
    ]:
        goto(rel)
        errs_before = page.evaluate("() => window.__errs || 0")
        ok = page.evaluate(
            """(btn_txt) => { for (const b of document.querySelectorAll('button')) if (b.textContent.trim() === btn_txt) { b.click(); return true; } return false; }""", btn_txt)
        page.wait_for_timeout(400)
        ok2 = ok and frag in page.url
        rec(f"B:{rel.split('/')[-1]}:{btn_txt}", ok2, page.url[-55:])

with sync_playwright() as pw:
    b = pw.chromium.launch()
    page = b.new_page()
    print("===== Task A 批量审核 14 页 =====")
    for p, path, mid, keys in PAGES:
        print(f"--- {p} {path}")
        try:
            run_page(page, p, path, mid, keys)
        except Exception as e:
            rec(f"{p}:EXCEPTION", False, str(e)[:160])
    run_b(page)
    b.close()

fails = [r for r in results if not r[1]]
print(f"\n===== 总计 {len(results)} 项，FAIL {len(fails)} 项 =====")
for t, _, n in fails:
    print("FAIL:", t, "|", n)
