# -*- coding: utf-8 -*-
"""验证门2：抽 15 个审核类弹窗——.modal 宽 640/720±2px、dval 单行占比 100%（按④豁免规则）；截图 10 张"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

PROTO = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
OUT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\modal-beauty")
OUT.mkdir(exist_ok=True)

SAMPLE = [  # (相对路径, 截图?)
    ("仓储作业/弹窗/采购入库审核.html", True),
    ("仓储作业/弹窗/其他入库审核.html", True),
    ("仓储作业/弹窗/其他出库审核.html", False),
    ("仓储作业/弹窗/拆卸审核.html", False),
    ("仓储作业/弹窗/盘点审核.html", True),
    ("仓储作业/弹窗/调拨审核.html", False),
    ("仓储作业/弹窗/租入归还审核.html", False),
    ("仓储作业/弹窗/退租入库审核.html", True),
    ("仓储作业/弹窗/销售出库审核.html", False),
    ("包装管理/弹窗/丢损赔偿审核.html", True),
    ("包装管理/弹窗/租赁单审核.html", True),
    ("包装管理/弹窗/退租申请审核.html", False),
    ("采购管理/弹窗/租入单审核.html", False),
    ("采购管理/弹窗/采购订单审核.html", True),
    ("销售管理/弹窗/销售订单审核.html", False),
]

CHECK = r"""
() => {
  const ov = document.querySelector('.modal-overlay.show') || document.querySelector('.modal-overlay');
  if (!ov) return { err: 'no overlay' };
  const modal = ov.querySelector('.modal');
  const w = modal ? modal.getBoundingClientRect().width : 0;
  const expect = /width:720px/.test(modal.getAttribute('style') || '') ? 720 : 640;
  const isLg = modal.classList.contains('modal-lg');
  const dvals = [];
  ov.querySelectorAll('.dval').forEach(dv => {
    const rng = document.createRange(); rng.selectNodeContents(dv);
    const rects = [...rng.getClientRects()].filter(r => r.width > 0.5 && r.height > 0.5);
    const tops = rects.map(r => r.top).sort((a, b) => a - b);
    let lines = tops.length ? 1 : 0, anchor = tops[0] || 0;
    for (let i = 1; i < tops.length; i++) { if (tops[i] - anchor > 10) { lines++; anchor = tops[i]; } }
    const txt = (dv.textContent || '').replace(/\s+/g, '');
    dvals.push({ lines, len: txt.length, txt: txt.slice(0, 24) });
  });
  return { w: Math.round(w * 10) / 10, expect, isLg, dvals };
}
"""

report = []
nshot = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1600, "height": 900})
    for rel, shot in SAMPLE:
        f = PROTO / rel
        pg.goto(f.as_uri())
        pg.wait_for_timeout(150)
        r = pg.evaluate(CHECK)
        if "err" in r:
            report.append({"page": rel, **r}); print("!!", rel, r); continue
        width_ok = (not r["isLg"]) and abs(r["w"] - r["expect"]) <= 2
        bad = [d for d in r["dvals"] if d["lines"] > 1 and d["len"] <= 34]  # >34字豁免
        exempt = [d for d in r["dvals"] if d["lines"] > 1 and d["len"] > 34]
        if shot and nshot < 10:
            pg.screenshot(path=str(OUT / (rel.split("/")[-1].replace(".html", "") + ".png")))
            nshot += 1
        report.append({"page": rel, "width": r["w"], "expect": r["expect"], "width_ok": width_ok,
                       "dvals": len(r["dvals"]), "multiline_nonexempt": bad, "exempt_longtext": exempt})
        print(f"{rel}: w={r['w']}(期望{r['expect']}){'✓' if width_ok else '✗'} dval={len(r['dvals'])} 违例={len(bad)} 豁免={len(exempt)}")
    b.close()

(OUT.parent / "modal-gate2-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
w_ok = sum(1 for r in report if r.get("width_ok"))
d_bad = sum(len(r.get("multiline_nonexempt", [])) for r in report)
print(f"\n门2汇总：宽度达标 {w_ok}/{len(report)}；非豁免多行 dval {d_bad}；截图 {nshot} 张")
