# -*- coding: utf-8 -*-
"""
任务三c 补充：F01 S1 支线·五态口径注记（P3-R04 修复任务 B 落点之二）
- 在 S1 既有灰字注记（盘点差异行 y=70）下方 y=84 加一行灰字，不移动任何既有元素
- SRC_DATA 无支线键，无需同步
"""
from pathlib import Path
import shutil

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
BK = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-goal-t3-20260905")
F = "P3-R01-F01-业务流程导航图.html"

ANCHOR = '<text x="336" y="70" fill="#9ca3af" font-size="8.5" font-family="\'Geist Mono\',monospace">盘点差异 → 盘盈转其他入库 · 盘亏转其他出库</text>'.encode("utf-8")
NEW = ANCHOR + ('\n    <text x="200" y="84" fill="#9ca3af" font-size="8.5" font-family="\'Geist Mono\',monospace">五态口径：在途＝应入库未入库（退租待入库/采购到货/租入到货/调拨在途）· 租入＝在库未转租，转租后计入客户态</text>').encode("utf-8")

def main():
    p = ROOT / F
    b = p.read_bytes()
    dst = BK / F
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copy2(p, dst)
    if "五态口径：在途＝应入库未入库".encode("utf-8") in b:
        print("已改过，跳过")
        return
    assert b.count(ANCHOR) == 1, f"锚点 {b.count(ANCHOR)} != 1"
    b = b.replace(ANCHOR, NEW, 1)
    assert b.count(NEW) == 1
    p.write_bytes(b)
    print(f"{F}: S1 口径注记已加")

if __name__ == "__main__":
    main()
