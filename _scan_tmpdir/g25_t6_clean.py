# -*- coding: utf-8 -*-
"""G25 T6：30 个弹窗模板孤立 proto-notes style 残块清理
仅清「style 块在·fab/script/data-note 属性均无」的文件；4 个活标注层弹窗跳过。
逐文件 assert：块恰 1→删后 0；style 开闭配平各 -1；行数差登记。
"""
import io, os, re

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
report = []
touched = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if not d.startswith("backup-")]
    if "弹窗" not in dirpath:
        continue
    for fn in sorted(filenames):
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(dirpath, fn)
        raw = open(fp, "rb").read()
        t = raw.decode("utf-8")
        if '<style id="proto-notes-style">' not in t:
            continue
        blk_s = t.find('<style id="proto-notes-style">')
        blk_e = t.find("</style>", blk_s)
        assert blk_e > blk_s, fp + " 残块无闭合"
        blk_e += len("</style>")
        outside = t[:blk_s] + t[blk_e:]
        # 活标注层判定（块外 data-note 属性或 fab/注入 script）→ 跳过
        if re.search(r'\sdata-note="[^"]*"', outside) or "protoNotesFab" in outside or "proto-notes-js" in outside:
            report.append((os.path.relpath(fp, ROOT), "SKIP 活标注层", 0))
            continue
        # 改前断言
        assert t.count('<style id="proto-notes-style">') == 1, fp + " style 块非 1"
        st_open, st_close = len(re.findall(r"<style[^>]*>", t)), t.count("</style>")
        # 删除块 + 紧随的一个 EOL（防双空行）
        tail = t[blk_e:blk_e + 2]
        cut_end = blk_e + (2 if tail == "\r\n" else (1 if tail == "\n" else 0))
        blk = t[blk_s:cut_end]
        t2 = t.replace(blk, "", 1)
        # 改后断言
        assert '<style id="proto-notes-style">' not in t2
        assert len(re.findall(r"<style[^>]*>", t2)) == st_open - 1, fp + " style 开配平异常"
        assert t2.count("</style>") == st_close - 1, fp + " style 闭配平异常"
        assert "protoNotesFab" not in t2 and "pn-fab" not in t2
        io.open(fp, "w", encoding="utf-8", newline="").write(t2)
        # EOL 保持校验
        raw2 = open(fp, "rb").read()
        crlf1, lf1 = raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")
        crlf2, lf2 = raw2.count(b"\r\n"), raw2.count(b"\n") - raw2.count(b"\r\n")
        assert (crlf2, lf2) == (crlf1 - blk.count("\r\n"), lf1 - blk.count("\n") + blk.count("\r\n")), fp + " EOL 漂移"
        touched += 1
        report.append((os.path.relpath(fp, ROOT), "CLEANED", blk.count("\n"), len(t) - len(t2)))

for r in report:
    print("%s | %s | 块行数=%d 删字节=%d" % r)
print("\n清理 %d 个·跳过(活标注层) %d 个" % (
    touched, len([r for r in report if r[1].startswith("SKIP")])))
