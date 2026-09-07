# -*- coding: utf-8 -*-
"""
任务一：操作栏冻结全站推广（二进制读取-精确替换 + assert + 幂等，行尾不动）
- P1: <th>操作</th>            -> <th class="sticky-op">操作</th>
- P2: <td><span class="ops"    -> <td class="sticky-op"><span class="ops"
- P3(默认决策): <td class="ops"> -> <td class="ops sticky-op">（录单/BOM维护编辑表 td 形态）
- 样板页已挂类，幂等跳过；改前备份 _scan_tmpdir/backup-goal-t1-20260905/（原相对路径）
"""
from pathlib import Path
import shutil

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
BK = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-goal-t1-20260905")

A = "<th>操作</th>".encode("utf-8")
B = '<th class="sticky-op">操作</th>'.encode("utf-8")
C = '<td><span class="ops"'.encode("utf-8")
D = '<td class="sticky-op"><span class="ops"'.encode("utf-8")
E = '<td class="ops">'.encode("utf-8")
F = '<td class="ops sticky-op">'.encode("utf-8")

def main():
    pages = sorted(ROOT.rglob("*.html"))
    BK.mkdir(parents=True, exist_ok=True)
    log = []
    total = {"P1": 0, "P2": 0, "P3": 0}
    for p in pages:
        rel = p.relative_to(ROOT)
        b = p.read_bytes()
        c1, c2, c3 = b.count(A), b.count(C), b.count(E)
        if not (c1 or c2 or c3):
            continue
        dst = BK / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(p, dst)
        nb = b
        n1 = nb.count(A); nb = nb.replace(A, B); total["P1"] += n1
        n2 = nb.count(C); nb = nb.replace(C, D); total["P2"] += n2
        n3 = nb.count(E); nb = nb.replace(E, F); total["P3"] += n3
        assert A not in nb and C not in nb and E not in nb, f"{rel} 仍有旧形态"
        if nb != b:
            p.write_bytes(nb)
        log.append(f"{rel}  th:{n1} td-span:{n2} td-ops:{n3}")
    # 幂等复跑校验
    for p in pages:
        b = p.read_bytes()
        assert A not in b and C not in b and E not in b, f"复跑仍有旧形态: {p.relative_to(ROOT)}"
    print(f"完成 {len(log)} 页；替换计数 {total}")
    for l in log:
        print(" ", l)
    (BK / "_t1_log.txt").write_text("\n".join(log), encoding="utf-8")

if __name__ == "__main__":
    main()
