# -*- coding: utf-8 -*-
"""④ 探针（只读）：打开每页全部弹窗，测量 .dval 高度，统计 >32px 违例分布"""
import json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

PROTO = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
SAMPLE = [
    "仓储作业/其他入库列表.html", "仓储作业/弹窗/其他入库单详情.html", "仓储作业/弹窗/采购入库审核.html",
    "包装管理/租赁单列表.html", "包装管理/弹窗/租赁单详情.html", "销售管理/销售订单列表.html",
    "财务协同/应收账单.html", "基础数据/客户管理.html", "系统管理/用户管理.html", "首页/我的待办.html",
]

MEASURE = r"""
(overlayId) => {
  const ov = document.getElementById(overlayId);
  if (!ov) return null;
  if (typeof openModal === 'function') openModal(overlayId); else ov.classList.add('show');
  const modal = ov.querySelector('.modal');
  const isLg = modal ? modal.classList.contains('modal-lg') : false;
  const mw = modal ? modal.getBoundingClientRect().width : 0;
  const out = [];
  ov.querySelectorAll('.dval').forEach(dv => {
    const r = dv.getBoundingClientRect();
    const txt = (dv.textContent || '').replace(/\s+/g, '');
    out.push({ h: Math.round(r.height), len: txt.length, label: (dv.previousElementSibling ? dv.previousElementSibling.textContent.trim().slice(0,10) : ''), txt: txt.slice(0, 26) });
  });
  if (typeof closeModal === 'function') closeModal(overlayId); else ov.classList.remove('show');
  return { isLg, mw: Math.round(mw), dvals: out };
}
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    pg = browser.new_page(viewport={"width": 1600, "height": 900})
    total = vio = 0
    vlist = []
    for rel in SAMPLE:
        f = PROTO / rel
        if not f.exists():
            print("!! missing", rel); continue
        pg.goto(f.as_uri())
        pg.wait_for_timeout(150)
        ids = pg.evaluate("() => [...document.querySelectorAll('.modal-overlay')].map(o => o.id)")
        for oid in ids:
            r = pg.evaluate(MEASURE, oid)
            if not r:
                print("!! no result", rel, oid); continue
            for d in r["dvals"]:
                total += 1
                if d["h"] > 32:
                    vio += 1
                    vlist.append((rel, oid, r["isLg"], d["len"], d["h"], d["label"], d["txt"]))
        print(f"{rel}: overlays={len(ids)}")
    browser.close()
    print(f"\n样本 dval 总数 {total}，超32px 违例 {vio}")
    for v in vlist[:40]:
        print("  V:", v)
    Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\modal-probe-sample.json").write_text(
        json.dumps(vlist, ensure_ascii=False, indent=1), encoding="utf-8")
