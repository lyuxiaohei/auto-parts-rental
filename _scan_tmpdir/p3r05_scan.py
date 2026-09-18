# -*- coding: utf-8 -*-
"""P3-R05 排查·页面四层结构扫描：列表(thead/筛选/页签/配置)·详情(ENT)·表单(labels)·弹窗(modal labels)
只读；输出 _scan_tmpdir/p3r05_pages.json + 控制台摘要。"""
import io, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "P3-R01-包装租赁管理后台原型"
OUT = Path(__file__).resolve().parent / "p3r05_pages.json"

TAG = re.compile(r"<[^>]+>")
def text(s):
    return TAG.sub("", s).replace("&nbsp;", " ").strip()

def strip_count(s):
    return re.sub(r"\d+\s*$", "", s).strip()

pages = []
for p in sorted(ROOT.rglob("*.html")):
    rel = p.relative_to(ROOT).as_posix()
    if rel.startswith("mobile/"):
        continue
    s = io.open(p, encoding="utf-8", newline="").read()
    info = {"page": rel, "dir": rel.split("/")[0] if "/" in rel else "(根)"}

    # ---- 列表页：renderListPage 配置 ----
    m = re.search(r"renderListPage\(\{(.{0,1200}?)\}\);", s, re.S)
    if m:
        cfg = m.group(1)
        ent = re.search(r"entity:\s*'([^']+)'", cfg)
        info["type"] = "list"
        info["entity"] = ent.group(1) if ent else None
        info["cfgOpts"] = [o for o in ("noCheckbox", "noOps", "stabField", "tbodySel", "detailFn") if o + ":" in cfg or o + " :" in cfg]
        stabf = re.search(r"stabField:\s*'([^']+)'", cfg)
        if stabf:
            info["stabField"] = stabf.group(1)
        ths = [text(t) for t in re.findall(r"<thead>.*?</thead>", s, re.S) and re.findall(r"<th[^>]*>(.*?)</th>", re.search(r"<thead>(.*?)</thead>", s, re.S).group(1), re.S)]
        info["thead"] = ths
        info["filtersCfg"] = re.findall(r"label:\s*'([^']+)'\s*,\s*field:\s*'([^']+)'", cfg)
        info["filtersDom"] = [text(x) for x in re.findall(r'ff-label">([^<]+)</span>', s)]
        info["filtersDom"] = [f.rstrip("：: ") for f in info["filtersDom"]]
        stabs = [strip_count(text(t)) for t in re.findall(r'<span class="stab[^"]*">(.*?)</span>', s, re.S)]
        info["stabs"] = [x for x in stabs if x]

    # ---- 详情页：ENT 接线 ----
    m2 = re.search(r"var ENT = '([^']+)'", s)
    if m2 and "detailBody" in s:
        info["type"] = info.get("type", "") + "+detail" if info.get("type") else "detail"
        info["entity"] = m2.group(1)

    # ---- 表单页：form-label 存在且非列表 ----
    labels = re.findall(r'<div class="form-label"[^>]*>(.*?)</div>', s, re.S)
    if labels and info.get("type") != "list":
        info["type"] = info.get("type") or "form"
        info["formLabels"] = [("必填:" if "req" in lb else "") + text(lb) for lb in labels]

    # ---- 弹窗（页内 + 模板页）----
    modals = []
    for mm in re.finditer(r'<div class="modal-overlay[^"]*"\s*id="([^"]+)"(.*?)</div>\s*<div class="modal-footer|<div class="modal-overlay[^"]*"\s*id="([^"]+)"(.{0,8000}?)</div>\s*</div>', s, re.S):
        mid = mm.group(1) or mm.group(3)
        body = mm.group(2) or mm.group(4) or ""
        lab = [text(x) for x in re.findall(r'<div class="form-label"[^>]*>(.*?)</div>|class="dlabel"[^>]*>(.*?)</div>|<th[^>]*>(.*?)</th>', body, re.S) for x in x if x]
        if mid:
            modals.append({"id": mid, "labels": lab[:24]})
    if modals:
        info["modals"] = modals
    pages.append(info)

# 实体已在别的扫描器处理；这里只落页面侧
OUT.write_text(json.dumps(pages, ensure_ascii=False, indent=1), encoding="utf-8")

lists = [x for x in pages if x.get("type") == "list"]
details = [x for x in pages if "detail" in (x.get("type") or "")]
forms = [x for x in pages if x.get("type") == "form"]
withmodal = [x for x in pages if x.get("modals")]
print("页数(PC):", len(pages), " 列表:", len(lists), " 详情:", len(details), " 表单:", len(forms), " 含弹窗:", len(withmodal))
data = json.loads(io.open(Path(__file__).resolve().parent / "p3r05_data.json", encoding="utf-8").read())

# ---- C1 cells vs thead ----
print("\n== C1 列表行 cells 数 vs 表头列数 ==")
bad = 0
for pg in lists:
    ent = pg.get("entity")
    th = len(pg.get("thead") or [])
    off = (0 if "noCheckbox" in pg.get("cfgOpts", []) else 1) + 1 + (0 if "noOps" in pg.get("cfgOpts", []) else 1)
    exp = th - off
    d = data.get(ent or "", {})
    lens = set()
    for k, r in d.get("records", {}).items():
        if r["cellsLen"] is not None:
            lens.add(r["cellsLen"])
    ok = lens == {exp} if lens else False
    if not ok:
        bad += 1
        print(f"  ✗ {pg['page']} entity={ent} thead={th} 期望cells={exp} 实际={sorted(lens)}")
print("  异常页数:", bad, "/", len(lists))

# ---- C4 fees vs feeCols ----
print("\n== C4 明细 fees cells vs feeCols ==")
bad4 = 0
for ent, d in data.items():
    for k, r in d["records"].items():
        if r["feeCols"] and r["feesCells"]:
            if any(c != len(r["feeCols"]) for c in r["feesCells"]):
                bad4 += 1
                print(f"  ✗ {ent}.{k} feeCols={len(r['feeCols'])} fees={r['feesCells']}")
print("  异常记录:", bad4)

# ---- C5 stab vs status 值域 ----
print("\n== C5 页签 vs 状态值域 ==")
bad5 = 0
for pg in lists:
    ent = pg.get("entity")
    stabs = [x for x in (pg.get("stabs") or []) if x != "全部"]
    if not stabs:
        continue
    fld = pg.get("stabField", "status")
    vals = set()
    for k, r in data.get(ent or "", {}).get("records", {}).items():
        v = (fld in r["fieldKeys"])
        if v:
            vals.add(r["status"] if fld == "status" else None)
    if vals and None not in vals:
        miss = [s for s in stabs if s not in vals]
        if miss:
            bad5 += 1
            print(f"  ✗ {pg['page']} 页签{miss} 不在状态值域{sorted(vals)}")
print("  页签失配页数:", bad5)

# ---- C6 筛选 cfg.field 是否存在于实体 fields ----
print("\n== C6 筛选字段存在性 ==")
bad6 = 0
for pg in lists:
    ent = pg.get("entity")
    recs = data.get(ent or "", {}).get("records", {})
    union = set()
    for k, r in recs.items():
        union |= set(r["fieldKeys"])
    for lab, fld in pg.get("filtersCfg", []):
        if fld in ("_key", "note"):
            continue
        if union and fld not in union:
            bad6 += 1
            print(f"  ✗ {pg['page']} 筛选「{lab}」field={fld} 不在 {ent} fields")
print("  失配筛选数:", bad6)
