# -*- coding: utf-8 -*-
"""
P3-R01 全站弹窗美观化 ①②③（/goal 2026-09-05）
① .modal width:480px → 640px + max-width:92vw（两形态；已带 90vw 的仅改 90vw→92vw）
② .dval word-break:break-all → overflow-wrap:break-word
③ dval 纯文本 >22 字符的 drow 加 style="grid-column:1/-1;"（幂等）
纪律：读取-精确替换，每步 assert；BOM.html / F01 / 99-归档 不在范围。
"""
import re
from pathlib import Path

PROTO = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
FAIL = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\goal-failures-modal.md")
EXCLUDE = {"基础数据\\BOM.html", "P3-R01-F01-业务流程导航图.html"}  # Windows 反斜杠；路径比较勿用正斜杠

FORM_A_OLD = ".modal { background:#fff; border-radius:8px; width:480px; max-height:80vh; overflow-y:auto; box-shadow:0 6px 16px rgba(0,0,0,.12); }"
FORM_A_NEW = ".modal { background:#fff; border-radius:8px; width:640px; max-width:92vw; max-height:80vh; overflow-y:auto; box-shadow:0 6px 16px rgba(0,0,0,.12); }"
FORM_B_OLD = ".modal{background:#fff;border-radius:8px;width:480px;max-width:90vw;max-height:85vh;overflow-y:auto;box-shadow:0 4px 20px rgba(0,0,0,.15)}"
FORM_B_NEW = ".modal{background:#fff;border-radius:8px;width:640px;max-width:92vw;max-height:85vh;overflow-y:auto;box-shadow:0 4px 20px rgba(0,0,0,.15)}"
DVAL_OLD = ".dval { flex:1; min-width:0; color:var(--text); word-break:break-all; }"
DVAL_NEW = ".dval { flex:1; min-width:0; color:var(--text); overflow-wrap:break-word; }"
A_DONE = ".modal { background:#fff; border-radius:8px; width:640px; max-width:92vw;"
B_DONE = ".modal{background:#fff;border-radius:8px;width:640px;max-width:92vw;"

failures = []
stat = {"a": 0, "b": 0, "dval": 0, "drow": 0, "files": 0}

for f in sorted(PROTO.rglob("*.html")):
    rel = f.relative_to(PROTO)
    if str(rel) in EXCLUDE:
        continue
    t = f.read_bytes().decode("utf-8")
    orig = t

    # ① 形态A
    na = t.count(FORM_A_OLD)
    if na == 1:
        t = t.replace(FORM_A_OLD, FORM_A_NEW); stat["a"] += 1
    elif na == 0 and A_DONE in t:
        pass  # 已 640 跳过（样板页）
    else:
        failures.append(f"{rel} | ①形态A 命中{na}次(预期1或已改)")

    # ① 形态B（紧凑·原带90vw）
    nb = t.count(FORM_B_OLD)
    if nb == 1:
        t = t.replace(FORM_B_OLD, FORM_B_NEW); stat["b"] += 1
    elif nb == 0 and B_DONE in t:
        pass
    else:
        failures.append(f"{rel} | ①形态B 命中{nb}次(预期1或已改)")

    # 兜底：仍有 width:480px 的 .modal 规则 → 记失败不改
    for m in re.finditer(r"\.modal\s*\{[^}]*width:\s*480px[^}]*\}", t):
        failures.append(f"{rel} | ①残留480px规则: {m.group(0)[:70]}")

    # ② dval
    nd = t.count(DVAL_OLD)
    if nd == 1:
        t = t.replace(DVAL_OLD, DVAL_NEW); stat["dval"] += 1
    elif nd == 0 and DVAL_NEW in t:
        pass  # 样板页已改
    else:
        failures.append(f"{rel} | ②dval 命中{nd}次(预期1或已改)")

    # ③ dval 纯文本 >22 字符 → drow 跨全宽（仅改开始标签，幂等）
    def fix_drow(m):
        whole = m.group(0)
        dv = re.search(r'<div class="dval[^"]*">(?:(?!<div|</div>).)*</div>', whole, re.S)
        if not dv:
            return whole
        txt = re.sub(r"<[^>]+>", "", dv.group(0))
        txt = re.sub(r"\s+", "", txt)
        if len(txt) <= 22:
            return whole
        gt = whole.index(">")
        open_tag = whole[: gt + 1]
        rest = whole[gt + 1 :]
        if "grid-column" in open_tag:
            return whole  # 幂等
        stat["drow"] += 1
        if "style=" in open_tag:
            new_open = open_tag[: open_tag.rindex('"')] + ' grid-column:1/-1;"' + open_tag[open_tag.rindex('"') + 1 :]
        else:
            new_open = open_tag[:-1] + ' style="grid-column:1/-1;">'
        return new_open + rest

    t = re.sub(r'<div class="drow[^"]*"[^>]*>\s*(?:<div class="dlabel[^"]*">(?:(?!<div|</div>).)*</div>\s*)?<div class="dval[^"]*">(?:(?!<div|</div>).)*</div>\s*</div>', fix_drow, t, flags=re.S)

    if t != orig:
        f.write_bytes(t.encode("utf-8"))
        stat["files"] += 1

FAIL.write_text("# /goal 弹窗美观化 失败清单（①②③阶段）\n\n" + ("\n".join(failures) if failures else "（无）") + "\n", encoding="utf-8")
print("改动文件:", stat["files"], "| 形态A:", stat["a"], "形态B:", stat["b"], "dval:", stat["dval"], "drow跨全宽:", stat["drow"])
print("失败项:", len(failures))
for x in failures:
    print("  -", x)
