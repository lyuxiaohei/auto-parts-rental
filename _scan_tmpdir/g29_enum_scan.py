# -*- coding: utf-8 -*-
"""全站枚举值盘点：提取写死的 select option 组 / radio 组 / stabs / 状态 tag
与 demo-data dictItems 对照，输出分类清单（只读）
"""
import io, os, sys, re, json
from collections import defaultdict

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def strip_tags(s):
    return re.sub(r"<[^>]+>|\\s+", " ", s).strip()

groups = defaultdict(lambda: {"pages": set(), "labels": set(), "kind": set()})

for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if not d.startswith("backup-")]
    for f in fn:
        if not f.endswith(".html"):
            continue
        rel = os.path.relpath(os.path.join(dp, f), ROOT).replace("\\", "/")
        if rel.startswith("mobile/"):
            continue
        t = io.open(os.path.join(dp, f), encoding="utf-8", errors="replace", newline="").read()
        # 1) select option 组（含 label 线索：前文 120 字内的 form-label/ff-label）
        for m in re.finditer(r"<select[^>]*>(.*?)</select>", t, re.S):
            body = m.group(1)
            opts = [re.sub(r"<[^>]+>", "", o).strip() for o in re.findall(r"<option[^>]*>(.*?)</option>", body, re.S)]
            opts = [o for o in opts if o]
            if len(opts) < 2:
                continue
            pre = t[max(0, m.start()-200):m.start()]
            lab = re.findall(r"(?:form-label|ff-label)[^>]*>(?:<span[^>]*>[^<]*</span>)?([^<]{1,20})<", pre)
            key = "select|" + "|".join(opts)
            groups[key]["pages"].add(rel); groups[key]["kind"].add("select")
            if lab: groups[key]["labels"].add(lab[-1].strip())
        # 2) radio 组
        for m in re.finditer(r'<input[^>]*type="radio"[^>]*>(.*?)(?=</div>\s*</div>|<div class="form-row">)', t, re.S):
            labs = re.findall(r">(?:\s*)([^<>]{1,16})(?:\s*)</span>", m.group(1))
            labs = [l for l in labs if l and not l.startswith("✓")]
            if len(labs) >= 2:
                key = "radio|" + "|".join(labs)
                groups[key]["pages"].add(rel); groups[key]["kind"].add("radio")
        # 3) stabs 页签
        for m in re.finditer(r'class="stabs">(.*?)</div>\s*(?=<div class="table-wrap"|<div class="toolbar")', t, re.S):
            tabs = [re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r'<span class="stab[^"]*">(.{1,30}?)<span class="stab-count"', m.group(1), re.S)]
            tabs = [re.sub(r"\d+$", "", x).strip() for x in tabs if x]
            if len(tabs) >= 2:
                key = "stabs|" + "|".join(tabs)
                groups[key]["pages"].add(rel); groups[key]["kind"].add("stabs")

out = []
for key, v in sorted(groups.items(), key=lambda kv: -len(kv[1]["pages"])):
    kind, vals = key.split("|", 1)
    out.append({"kind": kind, "选项": vals.split("|"), "页数": len(v["pages"]), "label": sorted(v["labels"])[:2],
                "示例页": sorted(v["pages"])[:3]})
json.dump(out, open(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g29_enum_scan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("聚合枚举组：", len(out), "组（select/radio/stabs 全站去重）")
for o in out:
    print("[%s×%d页] %s  label=%s  示例:%s" % (o["kind"], o["页数"], " / ".join(o["选项"])[:80],
          o["label"], o["示例页"][0] if o["示例页"] else ""))
