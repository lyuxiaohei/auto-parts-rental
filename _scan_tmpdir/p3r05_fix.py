# -*- coding: utf-8 -*-
"""P3-R05 收口·修复轮 v2：孤儿括号(\\r) / locations·stockFlows cells 区名化(行尾自适应)"""
import io, re

P = "P3-R01-包装租赁管理后台原型/_data/demo-data.js"
s = io.open(P, encoding="utf-8", newline="").read()

# a) 孤儿括号（\r 行尾形态）
bad = "  locations: {\r    },\r\n"
assert bad in s, "孤儿括号形态不符: %r" % s[s.index("  locations: {"):s.index("  locations: {") + 40]
s = s.replace(bad, "  locations: {\r\n", 1)

ZONE = {"RA": "原料区 RA", "RB": "成品区 RB", "RC": "次品区 RC", "RD": "成品区 RB"}

# b) locations 行内 cells 展示串（按键位置切片，行尾无关）
i = s.index("  locations: {")
j = s.index("\n  },", i)
blk = s[i:j]
keys = list(re.finditer(r"'([A-Z]{2}-[A-Z0-9\-]+)': \{", blk))
pieces = []
for a in range(len(keys)):
    start = keys[a].start()
    end = keys[a + 1].start() if a + 1 < len(keys) else len(blk)
    seg = blk[start:end]
    wh = ZONE[keys[a].group(1)[:2]]
    seg = seg.replace('"正品仓"', '"' + wh + '"').replace('"次品仓"', '"' + wh + '"')
    pieces.append(seg)
blk = "".join(pieces)
s = s[:i] + blk + s[j:]
print("locations 残留:", blk.count("正品仓"), blk.count("次品仓"))

# c) stockFlows 行内 cells 展示串
i = s.index("  stockFlows: {")
j = s.index("\n  },", i)
blk = s[i:j]
out = []
n = 0
for ln in blk.split("\n"):
    if "正品仓" in ln:
        lm = re.search(r'"loc": "([A-Z]{2})-', ln)
        zone = ZONE.get(lm.group(1), "成品区 RB") if lm else "成品区 RB"
        ln = ln.replace('"正品仓"', '"' + zone + '"')
        n += 1
    out.append(ln)
blk = "\n".join(out)
s = s[:i] + blk + s[j:]
print("stockFlows 修复行:", n, "残留 正品仓:", blk.count("正品仓"))

io.open(P, "w", encoding="utf-8", newline="").write(s)

# d) 交货日期 残留真身
for m in list(re.finditer(r".{30}交货日期.{15}", s))[:8]:
    print("交货日期上下文:", m.group(0).replace("\n", " ").replace("\r", " "))
