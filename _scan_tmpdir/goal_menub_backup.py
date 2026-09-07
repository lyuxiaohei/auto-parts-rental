# -*- coding: utf-8 -*-
"""菜单重组方案 B · 任务一：整目录备份（按原相对路径）到 _scan_tmpdir/backup-menub-20260906/
纪律：还原备份必须按原相对路径（历史事故：丢子目录产生游离文件）"""
import shutil, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJ = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = PROJ / "P3-R01-包装租赁管理后台原型"
BK = PROJ / "_scan_tmpdir" / "backup-menub-20260906"

# 备份范围：原型整目录（HTML+A04 JSON+A02 md）+ 三份台账文档
targets = [
    (PROTO, "P3-R01-包装租赁管理后台原型"),
    (PROJ / "P1-R05-agent交接文档.md", "P1-R05-agent交接文档.md"),
    (PROJ / "P1-R01-需求梳理与功能框架.md", "P1-R01-需求梳理与功能框架.md"),
    (PROJ / "P3-R04-演示场景覆盖梳理.md", "P3-R04-演示场景覆盖梳理.md"),
]

# 首次运行整体复制；已复制（存在完成标记）则跳过复制仅重跑校验（幂等）
BK.mkdir(parents=True, exist_ok=True)

done_marker = BK / "_DONE"
if not done_marker.exists():
    n_files = 0
    for src, rel in targets:
        dst = BK / rel
        if src.is_dir():
            shutil.copytree(src, dst)
            n_files += sum(1 for p in dst.rglob("*") if p.is_file())
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            n_files += 1
        print(f"BACKUP {rel}")
    done_marker.write_text("ok", encoding="utf-8")
else:
    print("SKIP 复制（已存在完成标记，仅重跑校验）")

# 校验：备份内文件数与源一致（按原相对路径逐一比对存在性）
src_files = set()
for src, rel in targets:
    if src.is_dir():
        src_files.update(f"{rel}/{p.relative_to(src)}".replace("\\", "/") for p in src.rglob("*") if p.is_file())
    else:
        src_files.add(rel)
bk_files = set(str(p.relative_to(BK)).replace("\\", "/") for p in BK.rglob("*") if p.is_file())
missing = src_files - bk_files
assert not missing, f"备份缺失 {len(missing)} 个文件: {sorted(missing)[:5]}"
print(f"OK 备份完成：{len(bk_files)} 个文件，源-备份逐相对路径比对 0 缺失")
