# -*- coding: utf-8 -*-
"""修复 G13 新记录插入点缺逗号（原末条记录结尾 `}` 无逗号）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
F = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\_data\demo-data.js")
s = F.read_bytes().decode('utf-8')
NL = '\r\n' if '\r\n' in s else '\n'
fixes = [
    ("    }" + NL + "   'XNC-ZZ-WBX': {", "    }," + NL + "   'XNC-ZZ-WBX': {"),
    ("    }" + NL + "   'RZD-20260910-009': {", "    }," + NL + "   'RZD-20260910-009': {"),
    ("    }" + NL + "    'AR-2026-09-PRJ2603-U1': {", "    }," + NL + "    'AR-2026-09-PRJ2603-U1': {"),
    ("    }" + NL + "    'XNC-ZZ-WBX': {", "    }," + NL + "    'XNC-ZZ-WBX': {"),
]
for old, new in fixes:
    n = s.count(old)
    if n == 1:
        s = s.replace(old, new)
        print("修复:", old.split(NL)[1][:30])
    else:
        print("跳过(n=%d):" % n, old.split(NL)[1][:30])
F.write_bytes(s.encode('utf-8'))
print("done")
