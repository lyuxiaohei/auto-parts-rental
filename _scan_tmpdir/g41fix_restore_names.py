# -*- coding: utf-8 -*-
"""F01 人名复原：把 G35（cfbebcc）对 F01 的人名脱敏逆向还原。
方法：解析 cfbebcc 对 F01 的 diff，提取 (-,+) 行对；断言「+ 行经逆向映射 == - 行」；
对当前 F01 全文应用逆向替换；断言每条 - 行原文在还原后文件中逐字存在。
"""
import io, sys, re

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
DIFF = ROOT + r"\_scan_tmpdir\g41fix_g35_diff_nav2.txt"
F01 = ROOT + r"\P3-R01-包装租赁管理后台原型\P3-R01-F01-业务流程导航图.html"

# 逆向映射（fake -> real），顺序无关（token 互不为子串）
REV = [("沈总", "王琳总"), ("严丽", "袁丽晶"), ("陆鸣", "道远")]

# ---- 1. 解析 diff，按 hunk 内顺序配对 (-,+) ----
pairs = []
cur_minus, cur_plus = [], []
with io.open(DIFF, "r", encoding="utf-8") as f:
    for raw in f:
        line = raw.rstrip("\n").rstrip("\r")
        if line.startswith("---") or line.startswith("+++"):
            continue
        if line.startswith("@@"):
            if cur_minus or cur_plus:
                assert len(cur_minus) == len(cur_plus), "hunk 内 -/+ 数不等: %d/%d" % (len(cur_minus), len(cur_plus))
                pairs.extend(zip(cur_minus, cur_plus))
                cur_minus, cur_plus = [], []
            continue
        if line.startswith("-"):
            cur_minus.append(line[1:])
        elif line.startswith("+"):
            cur_plus.append(line[1:])
if cur_minus or cur_plus:
    assert len(cur_minus) == len(cur_plus), "尾 hunk -/+ 数不等"
    pairs.extend(zip(cur_minus, cur_plus))

print("提取 diff 行对：%d 对" % len(pairs))
assert len(pairs) == 28, "预期 28 对，实得 %d" % len(pairs)  # 28＝grep 计数 29 减去 diff 头 --- 行

# ---- 2. 断言：+ 行逆向映射 == - 行 ----
def reverse_map(s):
    for fake, real in REV:
        s = s.replace(fake, real)
    return s

bad = 0
for i, (minus, plus) in enumerate(pairs, 1):
    restored = reverse_map(plus)
    if restored != minus:
        bad += 1
        print("!! 行对 %d 逆映射不吻合\n  -: %s\n  +: %s\n  还原: %s" % (i, minus[:90], plus[:90], restored[:90]))
assert bad == 0, "%d 对逆映射不吻合" % bad
print("28 对全部满足「逆向映射还原原文」断言")

# ---- 3. 当前 F01 应用逆向替换 ----
with io.open(F01, "r", encoding="utf-8", newline="") as f:
    content = f.read()

counts_before = {fake: content.count(fake) for fake, _ in REV}
print("替换前计数：", counts_before)
for fake, real in REV:
    content = content.replace(fake, real)

counts_after = {fake: content.count(fake) for fake, _ in REV}
print("替换后计数：", counts_after)
assert all(v == 0 for v in counts_after.values()), "仍有残留假名"

# ---- 4. 断言：每条 - 行原文逐字存在 ----
missing = [m for m, _ in pairs if m not in content]
assert not missing, "还原后缺失原文行 %d 条:\n%s" % (len(missing), "\n".join(m[:100] for m in missing[:5]))
print("28 条污染前原文行全部在还原后文件中逐字在位")

# ---- 5. 附加核查：常见假企业名/其他人名在本文件应为 0 ----
extras = ["沈婷", "徐文", "华骏", "环通", "星河", "星途", "东海商用", "长风汽制", "长丰锂电", "南方汽造", "甬城塑业", "吴越联合", "延陵", "严丽", "陆鸣"]
left = {w: content.count(w) for w in extras if content.count(w) > 0}
print("其他脱敏词残留核查：", left if left else "全 0")
assert not left, "存在未预期的脱敏词残留"

# ---- 6. 写回（保持原行尾） ----
with io.open(F01, "w", encoding="utf-8", newline="") as f:
    f.write(content)
print("已写回 F01（人名复原完成）")
