# -*- coding: utf-8 -*-
"""菜单重组方案 B · 任务一：git mv（保历史）
顺序：先移出租赁单 4 文件 → 再整体改名 包装管理/ → 租赁管理/
目标冲突检查：目标路径已存在则记失败跳过，不猜测改写"""
import subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJ = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = PROJ / "P3-R01-包装租赁管理后台原型"

MOVES = [
    ("包装管理/租赁单列表.html", "销售管理/租赁单列表.html"),
    ("包装管理/弹窗/租赁单新建.html", "销售管理/弹窗/租赁单新建.html"),
    ("包装管理/弹窗/租赁单审核.html", "销售管理/弹窗/租赁单审核.html"),
    ("包装管理/弹窗/租赁单详情.html", "销售管理/弹窗/租赁单详情.html"),
    ("包装管理", "租赁管理"),  # 目录整体改名（最后执行）
]

failures = []
for src_rel, dst_rel in MOVES:
    src, dst = PROTO / src_rel, PROTO / dst_rel
    if not src.exists():
        failures.append(f"{src_rel}: 源不存在（可能已移动）")
        print(f"SKIP {src_rel} → {dst_rel}：源不存在")
        continue
    if dst.exists():
        failures.append(f"{src_rel} → {dst_rel}: 目标已存在，冲突跳过")
        print(f"FAIL {src_rel} → {dst_rel}: 目标已存在")
        continue
    dst.parent.mkdir(parents=True, exist_ok=True)  # 销售管理/弹窗 已存在则不动
    r = subprocess.run(["git", "mv", str(src), str(dst)], cwd=PROJ,
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        failures.append(f"{src_rel} → {dst_rel}: git mv 失败 {r.stderr.strip()[:120]}")
        print(f"FAIL {src_rel} → {dst_rel}: {r.stderr.strip()[:120]}")
    else:
        print(f"OK git mv {src_rel} → {dst_rel}")

# 迁移后结构断言
expect_moved = ["销售管理/租赁单列表.html", "销售管理/弹窗/租赁单新建.html",
                "销售管理/弹窗/租赁单审核.html", "销售管理/弹窗/租赁单详情.html"]
expect_renamed = ["租赁管理/退租申请列表.html", "租赁管理/在租台账.html",
                  "租赁管理/租出台账.html", "租赁管理/丢损赔偿单.html",
                  "租赁管理/弹窗/退租申请详情.html", "租赁管理/弹窗/退租申请新建.html",
                  "租赁管理/弹窗/退租申请审核.html", "租赁管理/弹窗/丢损赔偿单详情.html",
                  "租赁管理/弹窗/丢损赔偿审核.html", "租赁管理/弹窗/器具出租履历.html",
                  "租赁管理/弹窗/报废确认.html"]
expect_gone = ["包装管理"]

ok = True
for f in expect_moved + expect_renamed:
    if not (PROTO / f).exists():
        print(f"ASSERT-FAIL 缺失: {f}"); ok = False
for d in expect_gone:
    if (PROTO / d).exists():
        print(f"ASSERT-FAIL 残留: {d}/"); ok = False
# BOM 不动断言
for f in ["基础数据/BOM.html", "基础数据/BOM维护.html"]:
    if not (PROTO / f).exists():
        print(f"ASSERT-FAIL BOM 被动: {f}"); ok = False

print("STRUCTURE:", "PASS" if ok else "FAIL")
print(f"FAILURES={len(failures)}")
for x in failures: print("  -", x)
