# -*- coding: utf-8 -*-
"""菜单重组方案 B · 任务二：全站引用替换（git mv 后执行）
顺序铁律：先专项（租赁单迁移）后目录改名（包装管理→租赁管理），避免交叉污染。
纪律：二进制读-精确替换-二进制写（保行尾），每形态全站计数 assert 并留存。
基线（mv 前实测）：专项 75 / 形态1 243（含形态2 内嵌 19）/ 形态2 19 / 形态3 10（专项占 4）"""
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJ = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = PROJ / "P3-R01-包装租赁管理后台原型"
OUT = PROJ / "_scan_tmpdir"

# 基线计数在 mv 前用 grep 实测；文件内容 mv 不变，故总数应一致
EXPECT = {"专项": 75, "形态1_含内嵌形态2": 243, "形态2": 19, "形态3_改前总数": 10}

REPL = [
    # (名称, 旧 bytes, 新 bytes, 期望全站计数或 None=仅记录)
    ("专项", "包装管理/租赁单列表.html".encode(), "销售管理/租赁单列表.html".encode(), 75),
    # 形态2 先数后并：../包装管理/ 替换会连 ../../包装管理/ 的尾段一起正确转换
    ("形态1", "../包装管理/".encode(), "../租赁管理/".encode(), 243),
    ("形态3", 'href="包装管理/'.encode(), 'href="租赁管理/'.encode(), 6),  # 10-4 被专项消耗
]

pages = sorted(PROTO.rglob("*.html"))
print(f"扫描 HTML：{len(pages)} 个（含 F01）")

stats = {"pages": len(pages)}
remaining_scan = []
for name, old, new, expect in REPL:
    total, nfiles = 0, 0
    per_file = {}
    for p in pages:
        b = p.read_bytes()
        c = b.count(old)
        if c:
            total += c; nfiles += 1
            per_file[str(p.relative_to(PROTO)).replace("\\", "/")] = c
            p.write_bytes(b.replace(old, new))
    print(f"{name}: {total} 处 / {nfiles} 文件" + (f"（assert=={expect}）" if expect else ""))
    if expect is not None:
        assert total == expect, f"{name} 计数异常: {total} != {expect}"
    stats[name] = {"count": total, "files": nfiles, "per_file": per_file}

# 形态2 专项计数（改前口径：形态2 内嵌于形态1 尾段，形态1 替换已同步完成）
# 用备份目录实测形态2 基线留存
bk = OUT / "backup-menub-20260906" / "P3-R01-包装租赁管理后台原型"
f2 = sum(p.read_bytes().count("../../包装管理/".encode()) for p in bk.rglob("*.html"))
stats["形态2"] = {"count": f2, "note": "内嵌于形态1 尾段，由形态1 替换同步完成（备份目录实测基线）"}
print(f"形态2 基线（备份实测）：{f2} 处")
assert f2 == 19, f"形态2 基线异常: {f2} != 19"

# 终扫：残留 包装管理 字样分类（应仅剩 F01 SRC_DATA 引文类文字，若与路径无关则保留）
for p in pages:
    t = p.read_text(encoding="utf-8")
    if "包装管理" in t:
        n = t.count("包装管理")
        # 提取残留上下文片段
        ctxs = []
        i = 0
        while True:
            i = t.find("包装管理", i)
            if i < 0: break
            ctxs.append(t[max(0, i-30):i+45].replace("\n", "␤"))
            i += 5
        for c in ctxs:
            remaining_scan.append({"page": str(p.relative_to(PROTO)).replace("\\", "/"), "ctx": c})
        print(f"RESIDUAL {p.relative_to(PROTO)}: {n} 处")

stats["残留包装管理"] = remaining_scan
(OUT / "goal-menub-refs-counts.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK 计数已留存 {OUT/'goal-menub-refs-counts.json'}；残留 {len(remaining_scan)} 处（见上）")
