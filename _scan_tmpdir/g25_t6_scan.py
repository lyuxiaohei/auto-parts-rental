# -*- coding: utf-8 -*-
"""G25 T6 扫描：弹窗模板注入残块实测（只读）
判据（G11 登记）：部分注入=有标注层 style 块/proto-notes CSS，但无 fab/pins/注入 script
另查：空 <script></script>、孤立 </style>（2026-09-03 坏块回归防线）
"""
import io, os, re

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
rows = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if not d.startswith("backup-")]
    if "弹窗" not in dirpath:
        continue
    for fn in sorted(filenames):
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(dirpath, fn)
        t = io.open(fp, encoding="utf-8", errors="replace", newline="").read()
        has_style = bool(re.search(r"<style[^>]*>\s*/\*[^*]*(?:标注|proto-notes|annotate)", t)) or "protoNotesStyle" in t or bool(re.search(r"#protoNotesFab|\.pn-fab|\.proto-pin", t))
        has_fab = "protoNotesFab" in t or "proto-notes-js" in t or "id=\"protoNotesData\"" in t
        has_datanote = "data-note" in t
        empty_script = len(re.findall(r"<script\s*>\s*</script>", t))
        orphan_style_close = len(re.findall(r"</style>", t)) - len(re.findall(r"<style[^>]*>", t))
        n_style_marks = len(re.findall(r"proto-pin|pn-fab|protoNotesFab|protoNotes", t))
        rows.append((os.path.relpath(fp, ROOT), has_style, has_fab, has_datanote, empty_script, orphan_style_close, n_style_marks, len(t)))

partial = [r for r in rows if (r[1] or r[6] > 0) and not r[2]]
bad = [r for r in rows if r[4] > 0 or r[5] != 0]
print("弹窗 HTML 总数:", len(rows))
print("\n== 部分注入残块（标注样式痕迹在·fab/script 无）==", len(partial))
for r in partial:
    print("  %s | datanote=%s 痕迹数=%d 空 script=%d 孤立</style>=%d" % (r[0].replace(chr(92), "/"), r[3], r[6], r[4], r[5]))
print("\n== 坏块（空 script/孤立 style 配平异常）==", len(bad))
for r in bad:
    print("  %s | 空 script=%d 孤立=%d" % (r[0].replace(chr(92), "/"), r[4], r[5]))
