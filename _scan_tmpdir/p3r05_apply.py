# -*- coding: utf-8 -*-
"""P3-R05 收口·demo-data 数据层一次性施工（A 标签 5 组 / B 库房区名化 / C 删虚拟仓行）"""
import io, re

P = "P3-R01-包装租赁管理后台原型/_data/demo-data.js"
s = io.open(P, encoding="utf-8", newline="").read()
orig = s

def rep(old, new, expect):
    global s
    n = s.count(old)
    assert n == expect, "计数不符 %r: %d != %d" % (old, n, expect)
    s = s.replace(old, new)

# ---- A 组标签 ----
rep("'label': '交货日期'", "'label': '预计到货日期'", 7)
rep("'label': '盘点方式'", "'label': '盘点口径'", 5)
rep("'label': '出库仓库'", "'label': '出库库房'", 1)
rep("'label': '提交时间'", "'label': '出库时间'", 1)
rep("'label': '制单日期'", "'label': '制单时间'", 5)

ZONE = {"RA": "原料区 RA", "RB": "成品区 RB", "RC": "次品区 RC", "RD": "成品区 RB"}

# ---- B1：locations 主数据 wh 区名化（逐行块） ----
i = s.index("  locations: {")
j = s.index("\n  },", i)
blk = s[i:j]

def rowmap(m):
    key, body = m.group(1), m.group(0)
    wh = ZONE[key[:2]]
    body = body.replace('"wh": "正品仓"', '"wh": "' + wh + '"')
    body = body.replace('"wh": "次品仓"', '"wh": "' + wh + '"')
    body = body.replace("<td>正品仓</td>", "<td>" + wh + "</td>")
    body = body.replace("<td>次品仓</td>", "<td>" + wh + "</td>")
    return body

blk = re.sub(r"'([A-Z]{2}-[A-Z0-9\-]+)': \{.*?\n    \},", rowmap, blk, flags=re.S)
s = s[:i] + blk + s[j:]
print("locations 残留 正品仓/次品仓:", blk.count("正品仓"), blk.count("次品仓"))

# ---- B2：stockFlows 18 行 area 按 loc 前缀重映射 ----
i = s.index("  stockFlows: {")
j = s.index("\n  },", i)
blk = s[i:j]
out = []
n_chg = 0
for ln in blk.split("\n"):
    if '"area": "正品仓"' in ln:
        lm = re.search(r'"loc": "([A-Z]{2})-', ln)
        zone = ZONE.get(lm.group(1), "成品区 RB") if lm else "成品区 RB"
        ln = ln.replace('"area": "正品仓"', '"area": "' + zone + '"')
        n_chg += 1
    out.append(ln)
blk = "\n".join(out)
s = s[:i] + blk + s[j:]
print("stockFlows 改写行数:", n_chg, "残留 正品仓:", blk.count("正品仓"))

# ---- C：删 locations XNC-AJZX 行 ----
assert s.count("'XNC-AJZX': {") == 1
i = s.index("'XNC-AJZX': {")
start = s.rfind("\n", 0, i)
rowend = s.index("}", s.index("'row':", i))
end = s.index("\n", s.index("},", rowend)) + 1
removed = s[start:end]
assert "客户虚拟仓" in removed and len(removed) < 600, "删除块异常: %r" % removed[:120]
s = s[:start] + s[end:]

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("完成。全文件残留: 正品仓 %d 次品仓 %d XNC-AJZX %d 交货日期 %d 出库仓库 %d 制单日期 %d" % (
    s.count("正品仓"), s.count("次品仓"), s.count("XNC-AJZX"),
    s.count("交货日期"), s.count("出库仓库"), s.count("制单日期")))
print("字节差:", len(s) - len(orig))
