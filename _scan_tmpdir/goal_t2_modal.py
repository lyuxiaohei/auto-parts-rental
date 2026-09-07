# -*- coding: utf-8 -*-
"""
任务二：弹窗宽度全站推广（二进制精确替换 + assert + 幂等）
- .modal-lg { width:680px; }   -> .modal-lg { width:780px; max-width:92vw; }
- .modal-lg{width:680px}       -> .modal-lg{width:780px;max-width:92vw}
- 样板页 采购管理/采购订单列表.html 已是 780，幂等跳过；F01 无 modal-lg
- 备份 _scan_tmpdir/backup-goal-t2-20260905/（原相对路径）
"""
from pathlib import Path
import shutil

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
BK = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-goal-t2-20260905")

A = b".modal-lg { width:680px; }"
B = b".modal-lg { width:780px; max-width:92vw; }"
C = b".modal-lg{width:680px}"
D = b".modal-lg{width:780px;max-width:92vw}"

def main():
    pages = sorted(ROOT.rglob("*.html"))
    BK.mkdir(parents=True, exist_ok=True)
    log = []
    total = 0
    for p in pages:
        rel = p.relative_to(ROOT)
        b = p.read_bytes()
        c1, c2 = b.count(A), b.count(C)
        if not (c1 or c2):
            continue
        dst = BK / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(p, dst)
        nb = b.replace(A, B).replace(C, D)
        n = nb.count(B) - b.count(B) + nb.count(D) - b.count(D)
        assert A not in nb and C not in nb, f"{rel} 仍有 680 旧形态"
        p.write_bytes(nb)
        total += c1 + c2
        log.append(f"{rel}  spaced:{c1} compact:{c2}")
    # 幂等复跑校验：全站不再有 680 形态
    left = []
    for p in pages:
        b = p.read_bytes()
        if A in b or C in b:
            left.append(str(p.relative_to(ROOT)))
    assert not left, f"复跑仍有旧形态: {left}"
    print(f"完成 {len(log)} 页，共 {total} 处；幂等复跑通过")
    (BK / "_t2_log.txt").write_text("\n".join(log), encoding="utf-8")

if __name__ == "__main__":
    main()
