# -*- coding: utf-8 -*-
"""通用 macOS 路径换算包装器（跨机说明：D:\ 前缀=主机口径，副机按项目根等价换算）。
用法：python3 run_script_mac.py <脚本名.py> [args...]
既有脚本零改：读源码 → 把 Windows 绝对路径前缀换算为本机项目根（余段反斜杠按 / 解析）→ exec。"""
import sys, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
target = HERE / sys.argv[1]
src = target.read_text(encoding="utf-8")
WIN = "D:\\工作台-吕道远\\5-【ACTIVE】汽车物流包装租赁"

def conv(m):
    rest = m.group(0)[len(WIN):].replace("\\", "/")
    return str(PROJ) + rest

src2 = re.sub(re.escape(WIN) + '[^"]*', conv, src)
assert WIN not in src2, "路径换算未全命中"
sys.argv = [str(target)] + sys.argv[2:]
exec(compile(src2, str(target), "exec"), {"__name__": "__main__", "__file__": str(target)})
