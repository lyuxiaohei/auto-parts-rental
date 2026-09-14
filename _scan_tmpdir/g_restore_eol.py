# -*- coding: utf-8 -*-
"""恢复非任务文件的行尾翻搅（重注幂等·内容与 HEAD 一致仅行尾差异）"""
import subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
KEEP = {
    "P3-R01-包装租赁管理后台原型/租赁管理/租入单列表.html",
    "P3-R01-包装租赁管理后台原型/租赁管理/弹窗/租入单新建.html",
    "P3-R01-包装租赁管理后台原型/租赁管理/租入归还列表.html",
    "P3-R01-包装租赁管理后台原型/租赁管理/弹窗/租入归还新建.html",
    "P3-R01-包装租赁管理后台原型/基础数据/产品档案.html",
    "P3-R01-包装租赁管理后台原型/基础数据/弹窗/新建产品.html",
    "P3-R01-包装租赁管理后台原型/基础数据/客商管理.html",
    "P3-R01-包装租赁管理后台原型/基础数据/弹窗/新建客商.html",
    "P3-R01-包装租赁管理后台原型/基础数据/弹窗/客商开票资料.html",
    "P3-R01-包装租赁管理后台原型/_data/demo-data.js",
    "P3-R01-包装租赁管理后台原型/P3-R01-A03-标注数据.json",
    "P3-R01-包装租赁管理后台原型/P3-R01-A04-流程链标注数据.json",
}
r = subprocess.run(["git", "status", "--porcelain"], capture_output=True)
restored = kept = 0
for line in r.stdout.decode("utf-8", errors="replace").splitlines():
    p = line[3:]
    if p.startswith('"'):
        p = p[1:-1]  # git 引号路径 → 恢复 UTF-8
        p = p.encode("latin1", errors="ignore").decode("unicode_escape").encode("latin1", errors="ignore").decode("utf-8", errors="ignore")
    p = p.replace("\\", "/")
    if not p.startswith("P3-R01"):
        continue
    if p in KEEP or any(k.endswith(p.split("/")[-1]) and p.replace("/", "\\") for k in KEEP):
        # 精确匹配为主
        pass
    if p in KEEP:
        kept += 1
        continue
    subprocess.run(["git", "checkout", "--", p.replace("/", "\\")], capture_output=True)
    restored += 1
print("保留 %d（任务文件）·恢复 %d（行尾翻搅）" % (kept, restored))
r2 = subprocess.run(["git", "status", "--porcelain"], capture_output=True)
lines = r2.stdout.decode("utf-8", errors="replace").splitlines()
print("剩余改动 %d：" % len(lines))
for l in lines:
    print(" ", l[:60])
