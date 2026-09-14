# -*- coding: utf-8 -*-
"""T3 标注数据：A04 租入归还列表追 pin3 + A03 新增弹窗键 + _meta.date 注记；输出注入页 EOL 快照"""
import io, json, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
A04 = ROOT + r"\P3-R01-A04-流程链标注数据.json"
A03 = ROOT + r"\P3-R01-A03-标注数据.json"

PIN_NOTE = ("支持分批归还：多张归还单可对应同一租入单；逐货品填写本次归还数量，「已归还」为该租入单历史累计。\n"
            "归还明细行随所选租入单的明细行数联动展示。")
PIN = {"id": 3, "selector": "<tbody id=\"riItemsBody\">", "title": "分批归还口径", "note": PIN_NOTE}

# ---- A04 追 pin ----
d4 = json.load(io.open(A04, encoding="utf-8"))
lst = d4["租赁管理/租入归还列表.html"]
assert len(lst) == 2 and all(p["id"] in (1, 2) for p in lst), "A04 租入归还现有 pin 异常"
if not any(p.get("selector") == PIN["selector"] for p in lst):
    lst.append(dict(PIN))
d4["_meta"]["date"] = d4["_meta"].get("date", "") + "；2026-09-14 会话：租入归还列表 +pin3 分批归还口径（弹窗 pn-hint 迁入）"
io.open(A04, "w", encoding="utf-8", newline="").write(
    json.dumps(d4, ensure_ascii=False, indent=1).replace("\n", "\r\n") + "\r\n")
print("PASS A04 pin3 追加")

# ---- A03 新键 ----
d3 = json.load(io.open(A03, encoding="utf-8"))
key = "租赁管理/弹窗/租入归还新建.html"
if key not in d3:
    d3[key] = [{"id": 1, "selector": PIN["selector"], "title": "分批归还口径", "note": PIN_NOTE}]
d3["_meta"]["date"] = d3["_meta"].get("date", "") + "；2026-09-14 会话：+弹窗键 租入归还新建（分批归还口径 pin·pn-hint 迁入·第 31 键）"
io.open(A03, "w", encoding="utf-8", newline="").write(
    json.dumps(d3, ensure_ascii=False, indent=1).replace("\n", "\r\n") + "\r\n")
print("PASS A03 弹窗键新增（现 %d 页键）" % len([k for k in d3 if k != "_meta"]))

# ---- EOL 快照（注入后归一用）----
eolmap = {}
for d in (d3, d4):
    for k in d:
        if k == "_meta":
            continue
        fp = ROOT + "\\" + k.replace("/", "\\")
        try:
            raw = open(fp, "rb").read()
        except OSError:
            continue
        crlf, lf = raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")
        eolmap[k] = "CRLF" if crlf >= lf and crlf > 0 else ("LF" if lf > 0 else "NONE")
io.open(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g_t3_eolmap.txt", "w",
        encoding="utf-8").write("\n".join("%s\t%s" % (k, v) for k, v in eolmap.items()))
print("PASS EOL 快照 %d 页" % len(eolmap))
