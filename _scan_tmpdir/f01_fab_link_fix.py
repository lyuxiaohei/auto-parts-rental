# -*- coding: utf-8 -*-
"""F01 流程图按钮断链修复：旧根级单文件(已归档删除) → 新文件夹主线图
两种形态：子目录页 ../P3-R01-F01-业务流程导航图.html / 根级页无 ../ 前缀
幂等：已是新路径跳过；排除 F01 文件夹自身、mobile、zip"""
import io, sys, time
from pathlib import Path

ROOT = (Path(__file__).resolve().parents[1] / "P3-R01-包装租赁管理后台原型")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
NEW = "P3-R01-F01-业务流程导航图/P3-R01-F01-业务流程导航图-主线.html"
OLD_SUB = 'href="../P3-R01-F01-业务流程导航图.html"'
OLD_ROOT = 'href="P3-R01-F01-业务流程导航图.html"'
NEW_SUB = 'href="../' + NEW + '"'
NEW_ROOT = 'href="' + NEW + '"'

def write_retry(p, data):
    for i in range(3):
        try:
            tmp = p.with_suffix(p.suffix + ".tmp")
            tmp.write_bytes(data)
            tmp.replace(p)
            return
        except OSError:
            if i == 2:
                raise
            time.sleep(0.3)

changed = skipped = 0
for p in sorted(ROOT.rglob("*.html")):
    rel = p.relative_to(ROOT)
    if rel.parts[0] == "mobile" or "P3-R01-F01-业务流程导航图" in rel.parts:
        continue
    txt = p.read_bytes().decode("utf-8")
    if NEW_SUB in txt or NEW_ROOT in txt:
        skipped += 1
        continue
    n = txt.count(OLD_SUB) + txt.count(OLD_ROOT)
    if not n:
        continue
    txt = txt.replace(OLD_SUB, NEW_SUB).replace(OLD_ROOT, NEW_ROOT)
    write_retry(p, txt.encode("utf-8"))
    changed += 1

residual = 0
for p in sorted(ROOT.rglob("*.html")):
    if p.relative_to(ROOT).parts[0] == "mobile":
        continue
    txt = p.read_bytes().decode("utf-8", "ignore")
    if 'href="../P3-R01-F01-业务流程导航图.html"' in txt or 'href="P3-R01-F01-业务流程导航图.html"' in txt:
        residual += 1
        print("RESIDUAL:", p)
print("changed:", changed, "| already-new skip:", skipped, "| residual:", residual)
sys.exit(1 if residual else 0)
