# -*- coding: utf-8 -*-
from pathlib import Path

f = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P1-R05-agent交接文档.md")
t = f.read_bytes().decode("utf-8")

FIXES = [
    ("：① 480px→640px", "：①`.modal` 480px→640px"),
    ("）② word-break:break-all", "）②`.dval` word-break:break-all"),
    ("截图 10 张 。改前备份 （124 文件原相对路径）；执行脚本 // 留档；失败清单 。",
     "截图 10 张 `_scan_tmpdir/modal-beauty/`。改前备份 `_scan_tmpdir/backup-modal-20260905/`（124 文件原相对路径）；执行脚本 `goal_modal_beauty.py`/`goal_modal_fix.py`/`goal_modal_gate2.py` 留档；失败清单 `goal-failures-modal.md`。"),
]
for old, new in FIXES:
    assert t.count(old) == 1, (old, t.count(old))
    t = t.replace(old, new)
f.write_bytes(t.encode("utf-8"))
print("修复完成，3 处")
