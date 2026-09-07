# -*- coding: utf-8 -*-
"""菜单重组方案 B · 任务二（续）：形态3 + 终扫残留 + 计数留存
已完成（goal_menub_refs.py 首跑实测落盘）：专项 75 处/55 文件；形态1 175 处/50 文件（改前基线 243，
其中 68 处被专项先行消耗：243-175=68；形态2 的 19 处内嵌于形态1 尾段随其同步完成）
本脚本：形态3 href="包装管理/ → href="租赁管理/（期望 6=10-4）"""
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJ = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = PROJ / "P3-R01-包装租赁管理后台原型"
OUT = PROJ / "_scan_tmpdir"

pages = sorted(PROTO.rglob("*.html"))

# 已完成形态的幂等校验：全站应为 0 残留
for name, old in [("专项", "包装管理/租赁单列表.html".encode()), ("形态1", "../包装管理/".encode())]:
    c = sum(p.read_bytes().count(old) for p in pages)
    assert c == 0, f"{name} 残留 {c} 处"
    print(f"IDEM-CHECK {name}: 0 残留 OK")

# 形态3
old, new = 'href="包装管理/'.encode(), 'href="租赁管理/'.encode()
total, nfiles, per_file = 0, 0, {}
for p in pages:
    b = p.read_bytes()
    c = b.count(old)
    if c:
        total += c; nfiles += 1
        per_file[str(p.relative_to(PROTO)).replace("\\", "/")] = c
        p.write_bytes(b.replace(old, new))
print(f"形态3: {total} 处 / {nfiles} 文件（assert==6）")
assert total == 6, f"形态3 计数异常: {total} != 6"

# 终扫：残留 包装管理 字样（应仅 F01 SRC_DATA 引文类文字性内容，与路径无关则保留）
remaining = []
for p in pages:
    t = p.read_text(encoding="utf-8")
    if "包装管理" in t:
        i = 0
        while True:
            i = t.find("包装管理", i)
            if i < 0: break
            remaining.append({"page": str(p.relative_to(PROTO)).replace("\\", "/"),
                              "ctx": t[max(0, i-40):i+50].replace("\n", "␤")})
            i += 5
for r in remaining:
    print(f"RESIDUAL {r['page']}: …{r['ctx']}…")

# 计数留存（含首跑实测值）
bk = OUT / "backup-menub-20260906" / "P3-R01-包装租赁管理后台原型"
f2 = sum(p.read_bytes().count("../../包装管理/".encode()) for p in bk.rglob("*.html"))
f1_base = sum(p.read_bytes().count("../包装管理/".encode()) for p in bk.rglob("*.html"))
sp_base = sum(p.read_bytes().count("包装管理/租赁单列表.html".encode()) for p in bk.rglob("*.html"))
stats = {
    "pages_scanned": len(pages),
    "备份基线": {"专项": sp_base, "形态1_含形态2内嵌": f1_base, "形态2": f2,
               "形态3": sum(p.read_bytes().count('href="包装管理/'.encode()) for p in bk.rglob("*.html"))},
    "实际替换": {"专项_包装管理租赁单列表→销售管理租赁单列表": {"count": 75, "files": 55},
               "形态1_../包装管理→../租赁管理": {"count": 175, "files": 50,
                                    "note": "改前基线 243，其中 68 处被专项先行消耗（243-175=68，含 ../../ 前缀的租赁单引用）；形态2 的 19 处内嵌于形态1 尾段随其同步完成"},
               "形态3_href包装管理→href租赁管理": {"count": 6, "files": len(per_file),
                                  "note": "改前基线 10，其中 4 处（F01 泳道 L1-L4 租赁单节点）被专项先行消耗",
                                  "per_file": per_file}},
    "残留包装管理字样": remaining,
}
(OUT / "goal-menub-refs-counts.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK 计数留存 → goal-menub-refs-counts.json；残留 {len(remaining)} 处")
