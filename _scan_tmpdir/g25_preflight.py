# -*- coding: utf-8 -*-
"""G25 前置校验：单写者互斥/防重复/G24 已执行/工具就绪（1-4 项；5-6 项 git+备份另行执行）"""
import os, time, subprocess, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
PROTO = os.path.join(ROOT, "P3-R01-包装租赁管理后台原型")
HANDOFF = os.path.join(ROOT, "agent-handoff")
SCAN = os.path.join(ROOT, "_scan_tmpdir")
NOW = time.time()
results = []

def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (" | " + detail if detail else ""))

# ---- 1. 单写者互斥：原型目录与 agent-handoff/ 最近文件 mtime >= 30 分钟 ----
# 豁免：本任务书 20260912-G25-会前原型修复包.md、失败清单 goal-failures-g25.md
EXEMPT = {"20260912-G25-会前原型修复包.md", "goal-failures-g25.md"}
def latest_mtime(top, exempt_abs=()):
    latest = (None, 0)
    for dirpath, dirnames, filenames in os.walk(top):
        # 备份目录自身豁免?备份是本 goal 建的，预检时还不存在；git 目录跳过
        if ".git" in dirnames:
            dirnames.remove(".git")
        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            if os.path.abspath(fp) in exempt_abs:
                continue
            try:
                m = os.path.getmtime(fp)
            except OSError:
                continue
            if m > latest[1]:
                latest = (fp, m)
    return latest

tbook = os.path.join(HANDOFF, "20260912-G25-会前原型修复包.md")
failist = os.path.join(HANDOFF, "goal-failures-g25.md")
pf, pm = latest_mtime(PROTO, (tbook, failist))
hf, hm = latest_mtime(HANDOFF, (tbook, failist))
age_p = (NOW - pm) / 60.0
age_h = (NOW - hm) / 60.0
check("1a 原型目录最近 mtime>=30min", age_p >= 30, "最近=%s 距今 %.1f 分钟" % (pf, age_p))
check("1b agent-handoff 最近 mtime>=30min", age_h >= 30, "最近=%s 距今 %.1f 分钟" % (hf, age_h))

# ---- 2. 防重复 ----
idx = os.path.join(HANDOFF, "_索引.md")
idx_txt = open(idx, encoding="utf-8").read() if os.path.exists(idx) else ""
check("2a _索引.md 无 G25 行", "| G25 |" not in idx_txt and "G25" not in idx_txt.split("G25-会前")[0] or "G25" not in idx_txt.replace("20260912-G25-会前原型修复包", ""), "grep G25 行=" + str(idx_txt.count("| G25")))
g25_files = [f for f in os.listdir(SCAN) if f.startswith("g25_")]
BUILD_EXEMPT = {"g25_prompt.md"}  # 建档文件豁免
exec_products = [f for f in g25_files if f not in BUILD_EXEMPT]
check("2b _scan_tmpdir 无 g25_* 执行产物", len(exec_products) == 0, "现存=%s（本预检脚本自身除外视作首产物）" % g25_files)

# ---- 3. G24 已执行 ----
p2r02 = os.path.join(ROOT, "P2-R02-决策落实与场景闭环检查报告.md")
check("3a P2-R02 报告在", os.path.exists(p2r02), p2r02)
check("3b _索引.md 有 G24 行", "G24" in idx_txt)

# ---- 4. 工具就绪 ----
try:
    nv = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=30)
    check("4a node 可用", nv.returncode == 0, nv.stdout.strip())
except Exception as e:
    check("4a node 可用", False, str(e))
check("4b g17_audit_diff.py 在", os.path.exists(os.path.join(SCAN, "g17_audit_diff.py")))
g17base = [f for f in os.listdir(SCAN) if "g17baseline" in f] if os.path.isdir(SCAN) else []
check("4c g17baseline 在", len(g17base) > 0, str(g17base))

# ---- 汇总 ----
fails = [r for r in results if not r[1]]
print("\n== 前置校验 1-4 汇总：%d 项，FAIL %d 项 ==" % (len(results), len(fails)))
sys.exit(1 if fails else 0)
