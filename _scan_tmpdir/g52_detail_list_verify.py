# -*- coding: utf-8 -*-
"""G52 四页「添加明细」改造渲染实测（2026-09-18 袁工指示·第5次沟通前）
断言：明细卡结构 / 表头口径 / 预填行 / 添加明细克隆 / MSEL 搜索组件 / 编码↔名称联动+规格带出 / 转移出库 URL 带参
"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
PAGES = [
    (r"仓储作业\调拨新建.html",   "调拨明细", "调拨数量 *"),
    (r"仓储作业\其他入库新建.html", "入库明细", "入库数量 *"),
    (r"仓储作业\其他出库新建.html", "出库明细", "出库数量 *"),
    (r"租赁管理\转移出库新建.html", "转移明细", "转移数量 *"),
]

def check(page, url, card_title, qty_th):
    r = {"errors": [], "pass": [], "fail": []}
    def ok(name): r["pass"].append(name)
    def bad(name, detail=""): r["fail"].append(f"{name} :: {detail}")

    page.goto(url)
    page.wait_for_timeout(600)

    # 1 明细卡与表头
    ths = page.eval_on_selector_all(".edit-tbl thead th", "els=>els.map(e=>e.textContent.trim())")
    if card_title in page.content(): ok(f"明细卡[{card_title}]")
    else: bad("明细卡", card_title)
    if len(ths) == 8 and ths[0] == "序号" and ths[1] == "物料编码" and ths[2] == "物料名称" and ths[4] == "单位" and ths[6] == "备注":
        ok(f"表头8列口径 {ths}")
    else: bad("表头口径", str(ths))
    if qty_th in ths: ok(f"数量列[{qty_th}]")
    else: bad("数量列", qty_th)

    # 2 头部物料下拉已撤
    has_mat_label = page.evaluate("""() => [...document.querySelectorAll('.form-label')].some(l => /物料：/.test(l.textContent) && l.closest('.form-row'))""")
    if not has_mat_label: ok("头部物料字段已撤")
    else: bad("头部物料字段残留")

    # 3 预填 3 行
    n0 = page.locator(".edit-tbl tbody tr").count()
    if n0 == 3: ok("预填3行")
    else: bad("预填行数", str(n0))

    # 4 添加明细 → 克隆行 + 序号重排
    page.click("button:has-text('添加明细')")
    page.wait_for_timeout(200)
    n1 = page.locator(".edit-tbl tbody tr").count()
    seqs = page.eval_on_selector_all(".edit-tbl tbody tr td:first-child", "els=>els.map(e=>e.textContent.trim())")
    if n1 == 4 and seqs == ["1","2","3","4"]: ok("添加明细克隆+序号1-4")
    else: bad("添加明细", f"rows={n1} seq={seqs}")

    # 5 MSEL 搜索组件挂载（含克隆行）
    wraps = page.locator(".edit-tbl .ms-wrap").count()
    if wraps >= 8: ok(f"MSEL 搜索框 {wraps} 个(4行×2列)")
    else: bad("MSEL 挂载", str(wraps))

    # 6 搜索下拉浮层
    page.click(".edit-tbl tbody tr:first-child .ms-wrap input")
    page.wait_for_timeout(200)
    drop_visible = page.evaluate("() => { const d=document.querySelector('.ms-drop'); return d && d.style.display!=='none' && d.children.length>0; }")
    if drop_visible: ok("搜索浮层弹出含选项")
    else: bad("搜索浮层")
    page.keyboard.press("Escape")

    # 7 编码↔名称联动+规格带出（首行换成该页演示外的另一编码）
    switch = page.evaluate("""() => {
      const tr = document.querySelector('.edit-tbl tbody tr');
      const code = tr.querySelector('select.pkMat');
      const opts = [...code.options].map(o=>o.value);
      const cur = code.value;
      const target = opts.find(v => v !== cur) || opts[0];
      code.value = target;
      code.dispatchEvent(new Event('change', {bubbles:true}));
      const name = tr.querySelector('select.pkName');
      const spec = tr.querySelector('input[data-spec]').value;
      return {target, nameVal: name.value, spec, optsN: opts.length};
    }""")
    if switch["nameVal"] == switch["target"]: ok(f"联动 名称随编码[{switch['target']}]")
    else: bad("联动", str(switch))
    if switch["spec"] and switch["spec"] != "": ok(f"规格带出[{switch['spec'][:20]}]")
    else: bad("规格带出", str(switch))
    if switch["optsN"] >= 14: ok(f"products 全量渲染({switch['optsN']}项)")
    else: bad("products 渲染", str(switch["optsN"]))

    return r

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    all_fail = 0
    for rel, title, qty in PAGES:
        url = "file:///" + os.path.join(ROOT, rel).replace("\\", "/")
        page = ctx.new_page()
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        res = check(page, url, title, qty)
        errs = [e for e in errs if "favicon" not in e.lower()]
        print("=" * 8, rel)
        print("  JS错误:", "无" if not errs else errs[:3])
        for x in res["pass"]: print("  PASS", x)
        for x in res["fail"]: print("  FAIL", x)
        all_fail += len(res["fail"]) + len(errs)
        page.close()

    # 转移出库 URL 带参：?mat=物料名称 → 明细首行选中
    page = ctx.new_page()
    url = "file:///" + os.path.join(ROOT, r"租赁管理\转移出库新建.html").replace("\\", "/") + "?mat=" + __import__("urllib.parse", fromlist=["quote"]).quote("围板箱 1200×1000×970")
    page.goto(url); page.wait_for_timeout(600)
    first = page.evaluate("() => document.querySelector('.edit-tbl tbody tr select.pkName').value")
    spec = page.evaluate("() => document.querySelector('.edit-tbl tbody tr input[data-spec]').value")
    print("=" * 8, "转移出库 URL 带参 ?mat=围板箱 1200×1000×970")
    print("  PASS 首行选中", first, "| 规格", spec) if first == "WBX-1210L" else print("  FAIL 带参预选", first, spec)
    all_fail += 0 if first == "WBX-1210L" else 1
    page.close()
    browser.close()
    print()
    print("总 FAIL 数:", all_fail)
