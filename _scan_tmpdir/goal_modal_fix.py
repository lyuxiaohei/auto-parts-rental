# -*- coding: utf-8 -*-
"""
④ 全站弹窗 dval 单行验证与兜底（/goal 20260905）
判据：dval 文本 Range 行盒数（top 聚类，容差10px）== 1 为单行（元素高度会被网格同轨拉伸污染，不可用）。
兜底级联（文本≤34字）：
  A. 普通 .modal（非 modal-lg）→ 该 .modal div 内联 width:720px，复测
  B. 仍超（或本就是 modal-lg）→ 该 drow 加 grid-column:1/-1，复测
  C. 仍超 → 豁免记录
文本>34字：天然豁免。BOM.html 门禁要求不动：全部豁免并注明。
"""
import json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

PROTO = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
OUT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir")
EXCLUDE_FILES = {PROTO / "P3-R01-F01-业务流程导航图.html"}  # 无弹窗
KEEP_FILES = {PROTO / "基础数据" / "BOM.html"}  # 门禁：不动，违例只豁免

MEASURE = r"""
(overlayId) => {
  const ov = document.getElementById(overlayId);
  if (!ov) return null;
  if (typeof openModal === 'function') openModal(overlayId); else ov.classList.add('show');
  const modal = ov.querySelector('.modal');
  const isLg = modal ? modal.classList.contains('modal-lg') : false;
  const mw = modal ? Math.round(modal.getBoundingClientRect().width) : 0;
  const drows = [];
  ov.querySelectorAll('.drow').forEach((row, ri) => {
    const dv = row.querySelector('.dval');
    if (!dv) return;
    const rng = document.createRange(); rng.selectNodeContents(dv);
    const rects = [...rng.getClientRects()].filter(r => r.width > 0.5 && r.height > 0.5);
    const tops = rects.map(r => r.top).sort((a, b) => a - b);
    let lines = tops.length ? 1 : 0, anchor = tops[0] || 0;
    for (let i = 1; i < tops.length; i++) { if (tops[i] - anchor > 10) { lines++; anchor = tops[i]; } }
    const txt = (dv.textContent || '').replace(/\s+/g, '');
    drows.push({ ri, lines, len: txt.length,
      label: (dv.previousElementSibling ? dv.previousElementSibling.textContent.trim() : '').slice(0, 10),
      txt: txt.slice(0, 26), h: Math.round(dv.getBoundingClientRect().height) });
  });
  if (typeof closeModal === 'function') closeModal(overlayId); else ov.classList.remove('show');
  return { isLg, mw, drows };
}
"""

def measure_page(pg, f, only_ids=None):
    pg.goto(f.as_uri())
    pg.wait_for_timeout(120)
    ids = pg.evaluate("() => [...document.querySelectorAll('.modal-overlay')].map(o => o.id)")
    res = {}
    for oid in ids:
        if only_ids is not None and oid not in only_ids:
            continue
        r = pg.evaluate(MEASURE, oid)
        if r:
            res[oid] = r
    return res

def collect_violations(page_results, f):
    """返回 [(overlay_id, drowIdx, len, lines, label, txt, isLg)]"""
    v = []
    for oid, r in page_results.items():
        for d in r["drows"]:
            if d["lines"] > 1:
                v.append((oid, d["ri"], d["len"], d["lines"], d["label"], d["txt"], r["isLg"]))
    return v

def widen_modal_in_file(f, oid):
    """该 overlay 内首个 <div class="modal" 追加内联 width:720px（幂等）"""
    t = f.read_bytes().decode("utf-8")
    m = re.search(r'id="' + re.escape(oid) + r'"', t)
    if not m:
        return False
    nxt = t.find('<div class="modal-overlay', m.end())
    seg_end = nxt if nxt != -1 else len(t)
    seg = t[m.start():seg_end]
    if 'class="modal" style="width:720px"' in seg:
        return True  # 幂等
    new_seg, n = re.subn(r'(<div class="modal")', r'\1 style="width:720px"', seg, count=1)
    if n != 1:
        return False
    f.write_bytes((t[: m.start()] + new_seg + t[seg_end:]).encode("utf-8"))
    return True

def fullwidth_drow_in_file(f, oid, ri):
    """该 overlay 内第 ri 个 drow 开始标签加 grid-column:1/-1（幂等）"""
    t = f.read_bytes().decode("utf-8")
    m = re.search(r'id="' + re.escape(oid) + r'"', t)
    if not m:
        return False
    nxt = t.find('<div class="modal-overlay', m.end())
    seg_end = nxt if nxt != -1 else len(t)
    seg = t[m.start():seg_end]
    hits = [mm for mm in re.finditer(r'<div class="drow[^"]*"[^>]*>', seg)]
    if ri >= len(hits):
        return False
    tag = hits[ri].group(0)
    if "grid-column" in tag:
        return True  # 幂等
    if "style=" in tag:
        new_tag = tag[: tag.rindex('"')] + ' grid-column:1/-1;"' + tag[tag.rindex('"') + 1 :]
    else:
        new_tag = tag[:-1] + ' style="grid-column:1/-1;">'
    new_seg = seg[: hits[ri].start()] + new_tag + seg[hits[ri].end():]
    f.write_bytes((t[: m.start()] + new_seg + t[seg_end:]).encode("utf-8"))
    return True

def run_sweep(pg, files, only=None):
    """返回 {file: {oid: result}}；only={file_rel: set(oid)} 限定复测范围"""
    all_res = {}
    for f in files:
        ids = only.get(f, None) if only else None
        if only and f not in only:
            continue
        try:
            all_res[f] = measure_page(pg, f, only_ids=ids)
        except Exception as e:
            print(f"  !! measure fail {f.name}: {e}")
    return all_res

files = sorted(p for p in PROTO.rglob("*.html") if p not in EXCLUDE_FILES)
print(f"共 {len(files)} 页（含 BOM.html 只测不改）")

log = {"round0_violations": 0}
with sync_playwright() as p:
    browser = p.chromium.launch()
    pg = browser.new_page(viewport={"width": 1600, "height": 900})

    # ---- R0：全量测量 ----
    res0 = run_sweep(pg, files)
    v0 = {f: collect_violations(r, f) for f, r in res0.items()}
    n0 = sum(len(v) for v in v0.values())
    print(f"R0 违例 dval：{n0}")

    # 天然豁免：>34 字 / BOM.html
    fixable = {}
    exempt_long, exempt_bom = [], []
    for f, vs in v0.items():
        for x in vs:
            if f in KEEP_FILES:
                exempt_bom.append((f.name, x[0], x[1], x[3], x[5]))
            elif x[2] > 34:
                exempt_long.append((f.name, x[0], x[1], x[2], x[5]))
            else:
                fixable.setdefault(f, []).append(x)
    print(f"可修复：{sum(len(v) for v in fixable.values())} | >34字豁免：{len(exempt_long)} | BOM豁免：{len(exempt_bom)}")

    # ---- 级 A：普通 .modal 内联加宽 720px ----
    widened = set()
    for f, vs in fixable.items():
        oids = {x[0] for x in vs if not x[6]}
        for oid in oids:
            if not widen_modal_in_file(f, oid):
                print(f"  !! widen fail {f.name}#{oid}")
            else:
                widened.add((f, oid))

    # ---- 复测 R1（被加宽的 overlay + modal-lg 违例 overlay） ----
    r1_targets = {}
    for f, vs in fixable.items():
        ids = {x[0] for x in vs}
        if ids:
            r1_targets[f] = ids
    res1 = run_sweep(pg, files, only=r1_targets)
    v1 = {f: collect_violations(r, f) for f, r in res1.items()}
    n1 = sum(len(v) for v in v1.values())
    print(f"R1 复测违例：{n1}")

    # ---- 级 B：drow 跨全宽（≤34字）----
    fw = {}
    for f, vs in v1.items():
        if f in KEEP_FILES:
            continue
        for x in vs:
            if x[2] <= 34:
                if not fullwidth_drow_in_file(f, x[0], x[1]):
                    print(f"  !! fullwidth fail {f.name}#{x[0]}#{x[1]}")
                else:
                    fw.setdefault(f, set()).add(x[0])
    r2_targets = fw
    res2 = run_sweep(pg, files, only=r2_targets) if r2_targets else {}
    v2 = {f: collect_violations(r, f) for f, r in res2.items()}
    n2 = sum(len(v) for v in v2.values())
    print(f"R2 复测违例：{n2}")

    exempt_stuck = []
    for f, vs in v2.items():
        for x in vs:
            exempt_stuck.append((str(f.relative_to(PROTO)), x[0], x[1], x[2], x[3], x[5]))
    browser.close()

summary = {
    "round0": n0,
    "fixable_input": sum(len(v) for v in fixable.values()),
    "widened_modals": len(widened),
    "fullwidth_drows": sum(len(s) for s in fw.values()),
    "exempt_longtext": exempt_long,
    "exempt_bom": exempt_bom,
    "exempt_stuck": exempt_stuck,
}
(OUT / "modal-fix-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print("\n=== 汇总 ===")
for k in ["round0", "fixable_input", "widened_modals", "fullwidth_drows"]:
    print(k, "=", summary[k])
print("豁免·>34字:", len(exempt_long), "| 豁免·BOM:", len(exempt_bom), "| 豁免·兜底仍超:", len(exempt_stuck))
for x in exempt_stuck[:30]:
    print("  STUCK:", x)
