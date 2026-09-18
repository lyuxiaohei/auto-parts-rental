# -*- coding: utf-8 -*-
# G52 独立验收 ③：10 页 Playwright 实测（file:// 直开）
# 断言：零 JS 错（net::ERR_ 豁免）；有数据页抽屉标题计数=NOTES_DATA 条数、fab 可见、
#       dispatchEvent click 角标(bubbles:true) → 抽屉开＋对应 data-id 条目高亮；
#       无数据页 fab display:none
import json, pathlib, sys
from playwright.sync_api import sync_playwright

PROTO = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
OUT = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g52_accept")

# NOTES_DATA 键 -> 条数（改前已用 node vm 验证 39/39；此处内联快照供断言）
import subprocess, re
code = (PROTO / "_data" / "notes-data.js").read_text(encoding="utf-8")
ND = {}
# 用 node 直接导出 JSON 快照（语义读取，非文本解析）
js = ("const fs=require('fs');const c={window:{}};require('vm').runInContext("
      "fs.readFileSync(process.argv[1],'utf8'),require('vm').createContext(c));"
      "const o={};for(const k of Object.keys(c.window.NOTES_DATA))o[k]=c.window.NOTES_DATA[k].map(e=>e.id);"
      "process.stdout.write(JSON.stringify(o));")
snap = subprocess.run(["node", "-e", js, str(PROTO / "_data" / "notes-data.js")],
                      capture_output=True, text=True, check=True).stdout
ND = json.loads(snap)  # key -> [ids]

PAGES = [
    ("财务协同/银行回单核销.html", "data"),   # 样板页
    ("财务协同/付款登记.html", "nodata"),     # 无数据页（推广清单内、NOTES_DATA 无键）
    ("首页/项目看板.html", "data"),
    ("仓储作业/库存查询.html", "data"),
    ("采购管理/采购入库列表.html", "data"),
    ("租赁管理/租赁出库列表.html", "data"),
    ("系统管理/用户权限.html", "data"),
    ("项目管理/项目详情.html", "data"),
    ("我的待办.html", "data"),                # 根级页（T1.2b 末段回退）
    ("销售管理/销售订单列表.html", "nodata"),  # 无数据页（页有 1 角标无键，决策表#9 登记情形）
]

CLICK_JS = """
() => {
  const els = Array.from(document.querySelectorAll('[data-note]'));
  if (!els.length) return { clicked: null };
  // 优先选值存在于抽屉条目 id 集合中的角标；全不存在则选第一个并标记
  const ids = Array.from(document.querySelectorAll('.pn-item')).map(e => e.getAttribute('data-id'));
  let el = els.find(e => ids.includes(e.getAttribute('data-note')));
  let mismatch = false;
  if (!el) { el = els[0]; mismatch = true; }
  el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  const drawer = document.querySelector('.pn-drawer');
  const hl = drawer ? drawer.querySelector('.pn-item.pn-hl') : null;
  return {
    clicked: el.getAttribute('data-note'),
    mismatchPick: mismatch,
    drawerOpen: !!(drawer && drawer.classList.contains('pn-show')),
    hlId: hl ? hl.getAttribute('data-id') : null,
  };
}
"""

results = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for rel, kind in PAGES:
        fp = PROTO / rel
        url = fp.as_uri()
        ctx = browser.new_context()  # 每页新 context：隔离 localStorage proto-notes-on
        page = ctx.new_page()
        js_errors = []
        page.on("pageerror", lambda e: js_errors.append("pageerror: %s" % e))
        page.on("console", lambda m: js_errors.append("console.error: %s" % m.text)
                if m.type == "error" else None)
        try:
            page.goto(url, wait_until="load", timeout=30000)
        except Exception as e:
            js_errors.append("goto: %s" % e)
        page.wait_for_timeout(400)

        entry = {"page": rel, "kind": kind, "js_errors": []}
        for e in js_errors:
            if "net::ERR_" in e:  # 断网类豁免
                continue
            entry["js_errors"].append(e)

        expected_key = rel.replace("\\", "/")
        ids = ND.get(expected_key, [])
        entry["expected_ids"] = ids

        fab = page.locator("#protoNotesFab")
        entry["fab_present"] = fab.count()
        if kind == "data" and ids:
            entry["fab_visible"] = fab.is_visible()
            cnt = page.locator(".pn-drawer-title .pn-fab-n").inner_text()
            entry["drawer_title_count"] = cnt.strip()
            entry["pn_item_count"] = page.locator(".pn-item").count()
            r = page.evaluate(CLICK_JS)
            entry.update(r)
        else:
            entry["fab_display"] = page.evaluate(
                "getComputedStyle(document.querySelector('#protoNotesFab')).display")
        results.append(entry)
        ctx.close()
    browser.close()

# 判定
fails = []
for r in results:
    name, kind = r["page"], r["kind"]
    if r["js_errors"]:
        fails.append(f"{name}: JS 错 {r['js_errors'][:2]}")
    if kind == "data":
        n = len(r["expected_ids"])
        if not r.get("fab_visible"):
            fails.append(f"{name}: fab 不可见")
        if r.get("drawer_title_count") != str(n):
            fails.append(f"{name}: 抽屉标题计数 {r.get('drawer_title_count')} != NOTES_DATA 条数 {n}")
        if r.get("pn_item_count") != n:
            fails.append(f"{name}: 抽屉条目数 {r.get('pn_item_count')} != {n}")
        if not r.get("drawerOpen"):
            fails.append(f"{name}: 点角标后抽屉未打开")
        if r.get("hlId") != r.get("clicked"):
            fails.append(f"{name}: 高亮 data-id {r.get('hlId')} != 所点角标 {r.get('clicked')}")
    else:
        if r.get("fab_display") != "none":
            fails.append(f"{name}: 无数据页 fab display={r.get('fab_display')} 而非 none")

report = json.dumps(results, ensure_ascii=False, indent=1)
(OUT / "c3_pw_results.json").write_text(report, encoding="utf-8")
print(report)
print("=" * 60)
print("PAGES:", len(results), "| modules>=", len({p.split('/')[0] for p, _ in PAGES if '/' in p}))
if fails:
    print("FAILS:")
    for f in fails:
        print(" -", f)
else:
    print("ALL 10 PAGES PASS")
