# -*- coding: utf-8 -*-
"""Generate per-sheet payloads for Tencent Docs replication."""
import json

DUMP = r"D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/_scan_tmpdir/gongqi_dump.json"
OUT = r"D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/_scan_tmpdir"

d = json.load(open(DUMP, encoding="utf-8"))
sheets = {s["name"]: s for s in d["sheets"]}


def build_payload(s, skip_cols_from=None):
    """Emit non-null cells as compact list. skip_cols_from: for gantt, skip empty day-area cells (value None anyway)."""
    cells = []
    for ri, row in enumerate(s["rows"]):
        for ci, v in enumerate(row):
            if v is None or (isinstance(v, str) and v.strip() == ""):
                continue
            if isinstance(v, bool):
                cells.append({"row": ri, "col": ci, "value_type": "BOOL", "bool_value": v})
            elif isinstance(v, (int, float)):
                cells.append({"row": ri, "col": ci, "value_type": "NUMBER", "number_value": v})
            else:
                cells.append({"row": ri, "col": ci, "value_type": "STRING", "string_value": str(v)})
    return cells


def merged_to_idx(m):
    import re
    m0 = re.match(r"([A-Z]+)(\d+):([A-Z]+)(\d+)", m)
    def col2num(c):
        n = 0
        for ch in c:
            n = n * 26 + (ord(ch) - 64)
        return n - 1
    c1, r1, c2, r2 = m0.group(1), int(m0.group(2)), m0.group(3), int(m0.group(4))
    return {"start_row": r1 - 1, "start_col": col2num(c1), "end_row": r2 - 1, "end_col": col2num(c2)}


out = {}
for name in ["汇总", "甘特图-功能点级", "甘特图-任务级", "功能点评估（全栈）"]:
    s = sheets[name]
    out[name] = {
        "values": build_payload(s),
        "merged": [merged_to_idx(m) for m in s["merged"]],
        "freeze": s["freeze"],
    }
    print(name, "cells:", len(out[name]["values"]), "merged:", len(out[name]["merged"]))

# extra structural info
hz = sheets["汇总"]
# percent cells: find rows where col A == 月份行之后的负载率 (col index 3, rows 2026-09..合计)
pct = []
for ri, row in enumerate(hz["rows"]):
    if ri >= 31 and ri <= 36 and isinstance(row[3], float):
        pct.append({"row": ri, "col": 3})
out["_huizong_percent_cells"] = pct
print("percent cells:", len(pct))

json.dump(out, open(f"{OUT}/payloads.json", "w", encoding="utf-8"), ensure_ascii=False)

# also dump per-sheet value arrays as separate files for easy paste
for name, key in [("汇总", "hz"), ("甘特图-功能点级", "gfp"), ("甘特图-任务级", "gtk"), ("功能点评估（全栈）", "fp")]:
    json.dump(out[name]["values"], open(f"{OUT}/pl_{key}.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump(out[name]["merged"], open(f"{OUT}/pl_{key}_merged.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

# gantt bar ranges: compute contiguous column spans from header dates + start/end per row
def gantt_bars(s, info_end_col, date_header_row_idx):
    """Return list of {row, start_col, end_col} bars (0-based), from date header row + per-row start/end dates."""
    dates = s["rows"][date_header_row_idx]
    # build map date-string -> col idx
    dmap = {}
    for ci, v in enumerate(dates):
        if isinstance(v, str) and v.startswith("20"):
            dmap[v] = ci
    bars = []
    for ri, row in enumerate(s["rows"]):
        # find start/end cols: 功能点级: D(3)=开始 E(4)=结束; 任务级: F(5)=开始 G(6)=结束
        sc = ec = None
        for ci in range(info_end_col):
            v = row[ci]
            pass
        # locate start/end by known positions
    return bars

# simpler: known column layouts
def bars_for(s, start_col_idx, end_col_idx, date_header_row_idx, only_rows_with_dates=True):
    dates = s["rows"][date_header_row_idx]
    dmap = {}
    for ci, v in enumerate(dates):
        if isinstance(v, str) and v[:2] == "20":
            dmap[v] = ci
    bars = []
    for ri, row in enumerate(s["rows"]):
        st, en = row[start_col_idx], row[end_col_idx]
        if isinstance(st, str) and isinstance(en, str) and st in dmap and en in dmap:
            bars.append({"row": ri, "start_col": dmap[st], "end_col": dmap[en]})
    return bars

gfp = sheets["甘特图-功能点级"]
gtk = sheets["甘特图-任务级"]
bars_fp = bars_for(gfp, 3, 4, 4)   # D/E, header row5 (idx4)
bars_tk = bars_for(gtk, 5, 6, 4)   # F/G, header row5 (idx4)
json.dump(bars_fp, open(f"{OUT}/bars_fp.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(bars_tk, open(f"{OUT}/bars_tk.json", "w", encoding="utf-8"), ensure_ascii=False)
print("bars fp:", len(bars_fp), "bars task:", len(bars_tk))
