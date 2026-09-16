# -*- coding: utf-8 -*-
"""G41 T7：P2-R02 V2.0 复检取证——①P2-R01 附录 A 台账五态解析 ②场景表 83 行锚点复检（页面存在+demo-data 单号在位）③R-06 现状。"""
import io, os, re

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
PROTO = os.path.join(ROOT, "P3-R01-包装租赁管理后台原型")
p2r01 = io.open(os.path.join(ROOT, "P2-R01-产品需求文档.md"), encoding="utf-8").read()
p2r02 = io.open(os.path.join(ROOT, "P2-R02-决策落实与场景闭环检查报告.md"), encoding="utf-8").read()
dd = io.open(os.path.join(PROTO, "_data", "demo-data.js"), encoding="utf-8").read()

out = []

# ---------- ① 附录 A 台账五态 ----------
sec = p2r01.split("## 附录 A", 1)[-1] if "## 附录 A" in p2r01 else p2r01.split("附录 A", 1)[-1]
rows = re.findall(r"^\| (D-\d{1,3}) \|(.*?)\|\s*([^|]*?)\s*\|\s*$", sec, re.M)
tally = {"✅": 0, "⚠": 0, "❌": 0, "⏸": 0, "⊘": 0}
unknown = []
dnums = []
for did, body, status in rows:
    dnums.append(int(did[2:]))
    s = status.strip()
    for k in tally:
        if s.startswith(k):
            tally[k] += 1
            break
    else:
        # 状态列可能不在末列——全行找
        head = s[:2]
        if head.startswith("✅"): tally["✅"] += 1
        elif head.startswith("⊘"): tally["⊘"] += 1
        else:
            unknown.append((did, s[:40]))
print("附录 A 台账行：%d（D-%d~D-%d）" % (len(rows), min(dnums), max(dnums)))
print("五态：", tally, "未识别：%d" % len(unknown))
for u in unknown[:6]: print("  未识别样例：", u)
out.append("附录 A 台账行 %d（D-%d~D-%d）五态=%s 未识别=%d" % (len(rows), min(dnums), max(dnums), tally, len(unknown)))

# ---------- ② 场景表锚点复检 ----------
# 取 3.1 与 3.2 两节的表行
def section(a, b):
    ia = p2r02.find(a); ib = p2r02.find(b)
    assert ia > 0 and ib > ia
    return p2r02[ia:ib]

s31 = section("### 3.1", "### 3.2")
s32 = section("### 3.2", "### 3.3")
pages_exist_cache = {}
def page_ok(path):
    if path in pages_exist_cache: return pages_exist_cache[path]
    p = path.replace("`", "").strip()
    full = os.path.join(PROTO, p)
    ok = os.path.exists(full)
    pages_exist_cache[path] = ok
    return ok

def check_rows(seg, label):
    rows = [l for l in seg.splitlines() if l.startswith("| ") and "---" not in l and "业务场景" not in l and "场景" not in l[:4]]
    # 行 id 形如 | 一-1 | 或 | 二-20 |
    results = []
    for l in rows:
        m = re.match(r"^\| ((?:[一二三四五六七]-\d+)) \|", l)
        if not m: continue
        rid = m.group(1)
        pages = set(re.findall(r"([A-Za-z0-9\u4e00-\u9fa5/]*\.html)", l))
        # 排除非路径词（纯 .html 且含 / 或中文即算页面引用）
        pages = {p for p in pages if "/" in p or any("\u4e00" <= ch <= "\u9fa5" for ch in p)}
        docs = set(re.findall(r"((?:P[123]-R\d+-A?\d*[^`]*)\.md)", l))
        tokens = set(t for t in re.findall(r"\b([A-Z]{2,6}-\d{2,4}(?:-\d{2,4}){0,2}[A-Za-z]?)\b", l)
                     if not t.startswith(("HTML", "URL")))
        bad_pages = [p for p in pages if not page_ok(p)]
        bad_tokens = []
        for t in tokens:
            if t not in dd:
                # 单号可能留档于其他实体或历史——再查页面
                anywhere = any(t in io.open(os.path.join(dp, f), encoding="utf-8").read()
                               for dp, dn, fn in os.walk(PROTO) if ".prompts" not in dn
                               for f in fn if f.endswith((".html", ".js")) and "backup" not in dp)
                if not anywhere: bad_tokens.append(t)
        ok = not bad_pages and not bad_tokens
        results.append((rid, ok, bad_pages, bad_tokens))
    npass = sum(1 for r in results if r[1])
    print("%s：%d 行·锚点全过 %d·异常 %d" % (label, len(results), npass, len(results) - npass))
    for rid, ok, bp, bt in results:
        if not ok:
            print("  ✗ %s 页面缺失=%s 单号未命中=%s" % (rid, bp, bt))
    out.append("%s：%d 行·锚点全过 %d·异常 %d" % (label, len(results), npass, len(results) - npass))
    return results

r1 = check_rows(s31, "3.1 主表 77 行")
r2 = check_rows(s32, "3.2 补充 6 行")

# ---------- ③ R-06 现状 ----------
inv = io.open(os.path.join(PROTO, "仓储作业", "库存查询.html"), encoding="utf-8").read()
print("R-06 线索：库存查询「在库(已组装)」=%d「在库（组合视图）」=%d" % (inv.count("在库(已组装)"), inv.count("在库（组合视图）")))
out.append("R-06：在库(已组装)×%d 在库（组合视图）×%d" % (inv.count("在库(已组装)"), inv.count("在库（组合视图）")))

io.open(os.path.join(ROOT, "_scan_tmpdir", "g41_p2r02_recheck.txt"), "w", encoding="utf-8").write("\n".join(out))
print("\n已写 g41_p2r02_recheck.txt")
