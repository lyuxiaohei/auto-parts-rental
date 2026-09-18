# -*- coding: utf-8 -*-
"""G52 几何一致性断言：四改造页 vs 样板页（采购入库录单）——卡对齐/表格宽度/搜索框形态/操作列 sticky"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
PAGES = [r"仓储作业\调拨新建.html", r"仓储作业\其他入库新建.html", r"仓储作业\其他出库新建.html", r"租赁管理\转移出库新建.html"]
SAMPLE = r"采购管理\采购入库录单.html"

JS = """() => {
  const card = [...document.querySelectorAll('.card')].find(c => c.querySelector('.edit-tbl'));
  if (!card) return {err:'no card'};
  const tbl = card.querySelector('.table-wrap');
  const thead = card.querySelector('thead');
  const ths = [...thead.querySelectorAll('th')];
  const ms = card.querySelector('.ms-wrap input');
  const opTh = thead.querySelector('th.sticky-op');
  const headBtn = card.querySelector('.head-btns button');
  const firstFormCard = document.querySelector('.content .card');
  return {
    cardLeft: card.getBoundingClientRect().left,
    formCardLeft: firstFormCard ? firstFormCard.getBoundingClientRect().left : null,
    cardWidth: card.getBoundingClientRect().width,
    tblOverflowX: tbl.scrollWidth - tbl.clientWidth,
    thCount: ths.length,
    msBorder: ms ? getComputedStyle(ms).borderTopWidth : null,
    msH: ms ? Math.round(ms.getBoundingClientRect().height) : null,
    opSticky: opTh ? getComputedStyle(opTh).position : null,
    btnText: headBtn ? headBtn.textContent.trim() : null,
    btnW: headBtn ? Math.round(headBtn.getBoundingClientRect().width) : null,
    headBtnsRight: Math.round(card.querySelector('.head-btns').getBoundingClientRect().right),
    cardRight: Math.round(card.getBoundingClientRect().right),
  };
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    def run(rel):
        pg = ctx.new_page()
        pg.goto("file:///" + os.path.join(ROOT, rel).replace("\\", "/"))
        pg.wait_for_timeout(400)
        r = pg.evaluate(JS)
        pg.close()
        return r
    print("样板 采购入库录单:")
    s = run(SAMPLE)
    print("  ", s)
    for rel in PAGES:
        r = run(rel)
        print("=" * 6, rel)
        issues = []
        if r.get("err"): issues.append(r["err"])
        else:
            if abs(r["cardLeft"] - r["formCardLeft"]) > 1: issues.append(f"卡左缘不对齐 {r['cardLeft']} vs {r['formCardLeft']}")
            if r["tblOverflowX"] > 2: issues.append(f"表格横向溢出 {r['tblOverflowX']}px")
            if r["msH"] is None or r["msH"] < 20 or r["msH"] > 34: issues.append(f"搜索框高度异常 {r['msH']}")
            if r["opSticky"] not in ("sticky",): issues.append(f"操作列非sticky {r['opSticky']}")
            if r["btnText"] != "添加明细": issues.append(f"按钮文案 {r['btnText']}")
            if r["headBtnsRight"] > r["cardRight"]: issues.append("按钮溢出卡片")
            # 与样板比对（样板值：搜索框高/边框/按钮宽同量级）
            if s.get("msH") and r["msH"] and abs(r["msH"] - s["msH"]) > 6: issues.append(f"搜索框高与样板差 {r['msH']} vs {s['msH']}")
        print("  ", r)
        print("   ", "OK" if not issues else "ISSUES: " + "; ".join(issues))
    b.close()
