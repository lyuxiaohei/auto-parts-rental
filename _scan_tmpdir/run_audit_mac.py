# -*- coding: utf-8 -*-
"""audit_interaction.py 的 macOS 路径换算包装器（既有脚本零改）：
读原脚本源码 → 替换 ROOT/OUT 两行 Windows 绝对路径为本机等价路径 → exec 执行。
跨机说明：文档内 D:\ 开头绝对路径=主机口径，副机一律按项目根等价换算。"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # _scan_tmpdir
PROJ = HERE.parent                               # 项目根
ROOT = PROJ / "P3-R01-包装租赁管理后台原型"

src = (HERE / "audit_interaction.py").read_text(encoding="utf-8")
src = src.replace(
    'ROOT = Path(r"D:\\工作台-吕道远\\5-【ACTIVE】汽车物流包装租赁\\P3-R01-包装租赁管理后台原型")',
    f'ROOT = Path(r"{ROOT}")',
)
src = src.replace(
    'OUT = Path(r"D:\\工作台-吕道远\\5-【ACTIVE】汽车物流包装租赁\\_scan_tmpdir")',
    f'OUT = Path(r"{HERE}")',
)
assert "D:\\工作台" not in src, "路径换算未全命中"
sys.argv = ["audit_interaction.py"] + sys.argv[1:]
exec(compile(src, str(HERE / "audit_interaction.py"), "exec"), {"__name__": "__main__", "__file__": str(HERE / "audit_interaction.py")})
