# -*- coding: utf-8 -*-
"""G25 验证门 1：g25_verify.py 逐行断言（F01/库存/应收/矩阵/node）"""
import io, re, subprocess, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
results = []

def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (" | " + detail if detail else ""))

# ---- 1. F01 ----
f01 = io.open(ROOT + r"\P3-R01-F01-业务流程导航图.html", encoding="utf-8", newline="").read()
check("F01 零部件买卖=0", f01.count("零部件买卖") == 0, str(f01.count("零部件买卖")))
check("F01 向供应商/供应商=0", f01.count("向供应商/供应商") == 0, str(f01.count("向供应商/供应商")))
check("F01 按第2次沟通纪要=0", f01.count("按第2次沟通纪要") == 0, str(f01.count("按第2次沟通纪要")))
check("F01 物料买卖≥5", f01.count("物料买卖") >= 5, str(f01.count("物料买卖")))
check("F01 按第3次沟通纪要=1", f01.count("按第3次沟通纪要") == 1, str(f01.count("按第3次沟通纪要")))

# ---- 2. 库存查询 + demo-data stockFlows ----
kc = io.open(ROOT + r"\仓储作业\库存查询.html", encoding="utf-8", newline="").read()
check("库存查询筛选含租入 option", kc.count("<option>租入</option>") == 1, str(kc.count("<option>租入</option>")))
check("库存查询五态注记在", "租入＝租入在库未转租" in kc, "")
dd = io.open(ROOT + r"\_data\demo-data.js", encoding="utf-8", newline="").read()
i = dd.find("stockFlows: {")
seg = dd[i:dd.find("/* ----", i + 20)]
check("stockFlows status=租入 行≥1", seg.count('"status": "租入"') >= 1, str(seg.count('"status": "租入"')))

# ---- 3. 应收 ----
mr = re.search(r"^  receivableBills: \{", dd, re.M)
rseg = dd[mr.start():dd.find("\n  /* ----", mr.start())]
n_sup = rseg.count('"btype": "供应商应收"')
check("receivableBills btype=供应商应收 行=1", n_sup == 1, str(n_sup) + "（既有行 AR-20260904-015·G25 前提修正零新增）")
ar = io.open(ROOT + r"\财务协同\应收账单.html", encoding="utf-8", newline="").read()
check("应收账单 option 供应商应收在", ar.count("<option>供应商应收</option>") == 1, str(ar.count("<option>供应商应收</option>")))

# ---- 4. 角色管理矩阵 ----
rj = io.open(ROOT + r"\系统管理\角色管理.html", encoding="utf-8", newline="").read()
n_au = rj.count("data-audit=")
check("auditPermMatrix data-audit=16", n_au == 16, str(n_au))
check("矩阵含付款登记", 'data-audit="付款登记"' in rj, "")
check("矩阵含收款确认", 'data-audit="收款确认"' in rj, "")

# 全站「可审单据矩阵（14」=0（排除备份）
import os
hits14 = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if not d.startswith("backup-")]
    for fn in filenames:
        if fn.endswith((".html", ".md", ".js", ".json")):
            t = io.open(os.path.join(dirpath, fn), encoding="utf-8", errors="ignore").read()
            hits14 += t.count("可审单据矩阵（14") + t.count("可审单据矩阵(14")
check("全站「可审单据矩阵（14」=0", hits14 == 0, str(hits14))

# ---- 5. node --check ----
r = subprocess.run(["node", "--check", ROOT + r"\_data\demo-data.js"], capture_output=True, text=True)
check("demo-data node --check 退出码 0", r.returncode == 0, "exit=%d" % r.returncode)

# ---- 6. T6 残块复核 ----
residual = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if not d.startswith("backup-")]
    if "弹窗" not in dirpath:
        continue
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        t = io.open(os.path.join(dirpath, fn), encoding="utf-8", errors="replace").read()
        if '<style id="proto-notes-style">' not in t:
            continue
        bs = t.find('<style id="proto-notes-style">')
        be = t.find("</style>", bs) + 8
        outside = t[:bs] + t[be:]
        if not (re.search(r'\sdata-note="[^"]*"', outside) or "protoNotesFab" in outside or "proto-notes-js" in outside):
            residual += 1
check("弹窗孤立 proto-notes style 残块=0（活标注层除外）", residual == 0, str(residual))

fails = [i for i, ok in enumerate(results) if not ok]
print("\n==== g25_verify：%d 项，FAIL %d 项 ====" % (len(results), len(fails)))
sys.exit(1 if fails else 0)
