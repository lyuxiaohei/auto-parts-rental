# -*- coding: utf-8 -*-
"""G40（prompt 旧编号 G41）续跑复核 · 只读取证脚本
零写入：仅读取原型目录与文档，打印各完成判定项的新鲜证据。
"""
import io, os, sys, subprocess

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
PROTO = os.path.join(ROOT, "P3-R01-包装租赁管理后台原型")
F01 = os.path.join(PROTO, "P3-R01-F01-业务流程导航图.html")
RULES = os.path.join(PROTO, "P3-R01-F01-业务流程导航图-开发规则.md")
P2R01 = os.path.join(ROOT, "P2-R01-产品需求文档.md")

TEXT_EXTS = {".html", ".js", ".md", ".json", ".css", ".txt"}
WHITELIST_FILES = {
    "P3-R01-A05-字段字典.md",          # 禁用写法列与沿革注记（G40 白名单）
    "P3-R01-F01-业务流程导航图.html",  # SRC_DATA 会议音频原文句（G40 白名单）
}
A05 = "P3-R01-A05-字段字典.md"

def collect_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(PROTO):
        if ".prompts" in dirnames:
            dirnames.remove(".prompts")  # gitignore 工具日志，范围排除（G40 R-02）
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in TEXT_EXTS:
                out.append(os.path.join(dirpath, fn))
    return out

FILES = collect_files()
results = []

def report(section, ok, detail=""):
    results.append((section, ok))
    print("[%s] %s %s" % ("PASS" if ok else "FAIL", section, detail))

print("=" * 72)
print("扫描文件数（文本类·排除 .prompts）：%d" % len(FILES))
print("=" * 72)

# ---------- A. 术语三条残留 ----------
print("\n--- A. 术语三条（水单/盈亏/回款）逐文件 str.count ---")
term_total_nonwl = {"水单": 0, "盈亏": 0, "回款": 0}
term_total_wl = {"水单": 0, "盈亏": 0, "回款": 0}
for fp in FILES:
    rel = os.path.relpath(fp, PROTO)
    try:
        with io.open(fp, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print("  !! 读取失败 %s: %s" % (rel, e)); continue
    for term in ("水单", "盈亏", "回款"):
        n = content.count(term)
        if n:
            is_wl = os.path.basename(fp) in WHITELIST_FILES
            (term_total_wl if is_wl else term_total_nonwl)[term] += n
            print("  %-6s ×%-3d %s%s" % (term, n, rel, "（白名单文件）" if is_wl else "  <== 非白名单!"))
            for i, line in enumerate(content.splitlines(), 1):
                if term in line:
                    print("      L%d: %s" % (i, line.strip()[:90]))
print("白名单外计数：水单=%d 盈亏=%d 回款=%d" % (term_total_nonwl["水单"], term_total_nonwl["盈亏"], term_total_nonwl["回款"]))
report("A. 术语清零（白名单外=0）", all(v == 0 for v in term_total_nonwl.values()),
       "（白名单内保留：水单=%d 盈亏=%d 回款=%d）" % (term_total_wl["水单"], term_total_wl["盈亏"], term_total_wl["回款"]))

# ---------- B. 改名 5 处 ----------
print("\n--- B. 文件改名 5 处 ---")
NEW5 = ["收款登记.html", "收款详情.html", "损益报表.html", "银行回单核销.html", "银行回单核销详情.html"]
OLD5 = ["回款登记.html", "回款详情.html", "盈亏报表.html", "银行水单核销.html", "水单核销详情.html"]
ok_new = True
for n in NEW5:
    p = os.path.join(PROTO, "财务协同", n)
    ex = os.path.exists(p)
    ok_new &= ex
    print("  新名存在 %-22s %s" % (n, "OK" if ex else "缺失!"))
ok_old = True
found_old = []
for dirpath, dirnames, filenames in os.walk(PROTO):
    if ".prompts" in dirnames: dirnames.remove(".prompts")
    for fn in filenames:
        if fn in OLD5:
            found_old.append(os.path.relpath(os.path.join(dirpath, fn), PROTO)); ok_old = False
print("  旧名文件存在性：%s" % ("0 处（OK）" if not found_old else "残留! %s" % found_old))
report("B1. 5 新名存在 / 5 旧名不存在", ok_new and ok_old)

# 旧名引用字符串（href 等）
old_ref_bad = []
new_ref_files = {n: 0 for n in NEW5}
a0x_new = {n: 0 for n in NEW5}
for fp in FILES:
    rel = os.path.relpath(fp, PROTO)
    with io.open(fp, "r", encoding="utf-8") as f: content = f.read()
    for o in OLD5:
        if o in content:
            old_ref_bad.append((rel, o))
    for n in NEW5:
        if n in content:
            new_ref_files[n] += 1
            if os.path.basename(fp).startswith("P3-R01-A0"):
                a0x_new[n] += 1
print("  旧名引用字符串命中：%d 处%s" % (len(old_ref_bad), "（OK）" if not old_ref_bad else " <== 死链源!"))
for n in NEW5:
    print("  新名引用：%-22s 被引用于 %d 个文件（A02/A05/A06 命中 %d）" % (n, new_ref_files[n], a0x_new[n]))
report("B2. 旧名引用 0 + 新名引用在位（含 A0x 路径行）",
       len(old_ref_bad) == 0 and all(new_ref_files[n] > 0 and a0x_new[n] > 0 for n in NEW5))

# ---------- C. 残留复核（货品/库龄/在库时长/流转次数/零件号/入库库区） ----------
print("\n--- C. 残留复核（页面域＝排除 .prompts 与 A05 白名单） ---")
RESID = ["库龄", "在库时长", "流转次数", "零件号", "入库库区"]
page_hits = []
for fp in FILES:
    rel = os.path.relpath(fp, PROTO)
    if os.path.basename(fp) == A05: continue
    with io.open(fp, "r", encoding="utf-8") as f: content = f.read()
    masked = content.replace("供货品类", "\x00")  # 货品 子串假阳性掩码（G40 R-03）
    if "货品" in masked:
        for i, line in enumerate(masked.splitlines(), 1):
            if "货品" in line:
                page_hits.append("%s L%d: %s" % (rel, i, line.strip()[:80]))
    for t in RESID:
        if t in content:
            for i, line in enumerate(content.splitlines(), 1):
                if t in line:
                    page_hits.append("%s L%d [%s]: %s" % (rel, i, t, line.strip()[:80]))
a05_counts = {}
with io.open(os.path.join(PROTO, A05), "r", encoding="utf-8") as f:
    a05c = f.read()
for t in ["货品", "零件号", "入库库区", "库龄", "水单", "盈亏", "回款"]:
    a05_counts[t] = a05c.count(t)
print("  页面域命中：%d 条%s" % (len(page_hits), "（OK·全 0）" if not page_hits else ""))
for h in page_hits[:10]: print("    " + h)
print("  A05 白名单内计数（登记对照）：%s" % a05_counts)
report("C. 货品=0；库龄/在库时长/流转次数/零件号/入库库区 页面域=0", len(page_hits) == 0)

# ---------- D. F01 五类改动 ----------
print("\n--- D. F01 业务流程导航图 ---")
with io.open(F01, "r", encoding="utf-8") as f: f01 = f.read()
title_line = ""
for line in f01.splitlines():
    if "<title>" in line: title_line = line.strip(); break
c_v37, c_v36 = f01.count("v3.7"), f01.count("v3.6")
c_bill = f01.count("按持有量计租")
c_drv = f01.count("转移单审核驱动")
c_vw = f01.count("客户虚拟仓不维护")
c_sub = f01.count("客户间转移 · 直接客户 → 终端客户")
c_note = f01.count("L1–L4 通用")
c_arrow = f01.count("分批 · 非必经")
c_zy = f01.count("转移出库")
print("  <title>：%s" % title_line[:90])
print("  版本：v3.7 ×%d · v3.6 ×%d（预期 7/1）" % (c_v37, c_v36))
print("  计费文案『按持有量计租』×%d（预期 ≥7）" % c_bill)
print("  状态驱动『转移单审核驱动』×%d（预期 2）" % c_drv)
print("  虚拟仓『客户虚拟仓不维护』×%d（预期 1）" % c_vw)
print("  转移出库节点副标『客户间转移 · 直接客户 → 终端客户』×%d（预期 2）" % c_sub)
print("  跨线注记『L1–L4 通用』×%d（预期 ≥1）" % c_note)
print("  箭头标签『分批 · 非必经』×%d（预期 ≥1）" % c_arrow)
print("  『转移出库』全文 ×%d（含节点/注记/Mermaid 源）" % c_zy)
ok_d = ("v3.7" in title_line and c_v37 == 7 and c_v36 == 1 and c_bill >= 7
        and c_drv == 2 and c_vw == 1 and c_sub == 2 and c_note >= 1 and c_arrow >= 1)
report("D. F01 五类改动全部在位（title/版本/计费/驱动/虚拟仓/节点/注记）", ok_d)

# ---------- E. 开发规则同步 ----------
print("\n--- E. F01 开发规则 ---")
with io.open(RULES, "r", encoding="utf-8") as f: rules = f.read()
has_v37 = "v3.7" in rules
has_date = "2026-09-16" in rules
has_s12 = "计费与状态口径" in rules
import re
heads = re.findall(r"^#{1,3}\s*(\d+)[\.、\s]", rules, re.M)
nums = [int(h) for h in heads]
cont = nums == sorted(nums) and set(nums) == set(range(1, 14))
print("  v3.7=%s · 日期 2026-09-16=%s · §12 计费与状态口径=%s" % (has_v37, has_date, has_s12))
print("  章节号序列：%s（1–13 连续且升序=%s）" % (nums, cont))
report("E. 开发规则 v3.7 同步（节点规格/计费口径/日期/章节连续）", has_v37 and has_date and has_s12 and cont)

# ---------- F. node --check ----------
print("\n--- F. node --check（_data/*.js） ---")
datadir = os.path.join(PROTO, "_data")
js_files = sorted(fn for fn in os.listdir(datadir) if fn.endswith(".js"))
npass = 0
for fn in js_files:
    r = subprocess.run(["node", "--check", os.path.join(datadir, fn)],
                       capture_output=True, text=True, shell=False)
    st = "exit 0" if r.returncode == 0 else "exit %d %s" % (r.returncode, r.stderr[:80])
    if r.returncode == 0: npass += 1
    print("  node --check %-24s %s" % (fn, st))
report("F. node --check %d/%d exit 0" % (npass, len(js_files)), npass == len(js_files))

# ---------- G. P2-R01 台账 D-149 ----------
print("\n--- G. P2-R01 台账 D-149 落账 ---")
with io.open(P2R01, "r", encoding="utf-8") as f: p2 = f.read()
hits = [(i, l.strip()) for i, l in enumerate(p2.splitlines(), 1) if "D-149" in l]
for i, l in hits: print("  L%d: %s" % (i, l[:100]))
ok_g = len(hits) >= 2 and any("D-142" in l for _, l in hits)
report("G. P2-R01 含 D-149 且 D-142 状态更正在案", ok_g)

# ---------- 汇总 ----------
print("\n" + "=" * 72)
n_pass = sum(1 for _, ok in results if ok)
for s, ok in results: print("  [%s] %s" % ("PASS" if ok else "FAIL", s))
print("=" * 72)
print("总判定：%d/%d PASS" % (n_pass, len(results)))
sys.exit(0 if n_pass == len(results) else 1)
