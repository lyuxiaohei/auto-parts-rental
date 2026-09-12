# -*- coding: utf-8 -*-
"""G25 T1：F01 旧术语清理——12 处精确替换+assert 计数+标签配平自检
改：零部件买卖×6→物料买卖 / 向供应商/供应商租入×2→向供应商租入 / 按第2次→按第3次沟通纪要 / 器具×3 单指概念→物料
保留：零部件/器具 并列×2、器具类(WL-01 类型值)×1、SRC_DATA v3.0 决策注记沿革句×1
"""
import io, sys

F01 = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\P3-R01-F01-业务流程导航图.html"
txt = io.open(F01, encoding="utf-8").read()
before_len = len(txt)

# (旧串, 新串, 预期次数, 说明)
REPL = [
    # --- 零部件买卖 ×6 → 物料买卖 ---
    ("<b>B1</b> 零部件买卖", "<b>B1</b> 物料买卖", 1, "行69 头部叙事"),
    ("B1 零部件买卖、", "B1 物料买卖、", 1, "行79 无障碍 desc"),
    ("<!-- ======== B1 · 零部件买卖 ======== -->", "<!-- ======== B1 · 物料买卖 ======== -->", 1, "行90 泳道区块注释"),
    ("B1 · 零部件买卖（一进一出 · 无组装）", "B1 · 物料买卖（一进一出 · 无组装）", 1, "行91 泳道标签"),
    ('subgraph B1["B1 · 零部件买卖（一进一出）"]', 'subgraph B1["B1 · 物料买卖（一进一出）"]', 1, "行669 mermaid 源块"),
    ("b1: {head:'B1 · 零部件买卖 · 会议依据'", "b1: {head:'B1 · 物料买卖 · 会议依据'", 1, "行725 SRC_DATA b1 头"),
    # --- 向供应商/供应商租入 ×2 → 向供应商租入 ---
    ("L3 · 租赁 · 租入转租（向供应商/供应商租入 → 转租客户）", "L3 · 租赁 · 租入转租（向供应商租入 → 转租客户）", 1, "行255 L3 泳道标题坏句"),
    ('text-anchor="middle">向供应商/供应商租入</text>', 'text-anchor="middle">向供应商租入</text>', 1, "行269 L3 节点标签坏句"),
    # --- 按第2次沟通纪要 ×1 → 按第3次 ---
    ("业务流程 · 按第2次沟通纪要", "业务流程 · 按第3次沟通纪要", 1, "行73 区块标题口径对齐"),
    # --- 器具 ×3 单指物料概念 → 物料 ---
    ('text-anchor="middle">器具 · 资产采购</text>', 'text-anchor="middle">物料 · 资产采购</text>', 1, "行157 L1 采购线副标"),
    ('text-anchor="middle">单一器具 · 直接出租</text>', 'text-anchor="middle">单一物料 · 直接出租</text>', 1, "行178 L1 租赁线副标"),
    ('text-anchor="middle">器具A/B/C 采购</text>', 'text-anchor="middle">物料A/B/C 采购</text>', 1, "行207 L2 采购线副标"),
]

fails = []
for old, new, expect, note in REPL:
    n = txt.count(old)
    if n != expect:
        fails.append("%s：命中 %d 次（预期 %d）——跳过" % (note, n, expect))
        print("ASSERT FAIL %s：count=%d expect=%d" % (note, n, expect))
        continue
    txt = txt.replace(old, new)
    assert txt.count(new) >= 1
    print("PASS %s" % note)

if fails:
    print("\n有 assert 失败，不写回文件")
    sys.exit(1)

io.open(F01, "w", encoding="utf-8", newline="").write(txt)

# ---- 终态断言 ----
t2 = io.open(F01, encoding="utf-8").read()
checks = [
    ("零部件买卖=0", t2.count("零部件买卖") == 0, t2.count("零部件买卖")),
    ("向供应商/供应商=0", t2.count("向供应商/供应商") == 0, t2.count("向供应商/供应商")),
    ("按第2次沟通纪要=0", t2.count("按第2次沟通纪要") == 0, t2.count("按第2次沟通纪要")),
    ("物料买卖=6", t2.count("物料买卖") == 6, t2.count("物料买卖")),
    ("按第3次沟通纪要=1", t2.count("按第3次沟通纪要") == 1, t2.count("按第3次沟通纪要")),
    ("器具保留=4（并列×2+类型值×1+沿革×1）", t2.count("器具") == 4, t2.count("器具")),
]
ok = True
for name, cond, val in checks:
    print(("PASS " if cond else "FAIL ") + "%s（实际 %d）" % (name, val))
    ok = ok and cond

# ---- 标签配平自检（改前后计数一致） ----
import re
def tag_counts(s):
    return {t: len(re.findall("<%s[\\s>]" % t, s)) for t in ["text", "div", "script", "svg", "a ", "pre", "details"]}
# 用改前内容重算（txt 变量已是改后）
before = io.open(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\backup-g25-20260912\P3-R01-F01-业务流程导航图.html", encoding="utf-8").read()
cb, ca = tag_counts(before), tag_counts(t2)
bal = cb == ca
print(("PASS " if bal else "FAIL ") + "标签配平：改前 %s == 改后 %s" % (cb, ca))
print("文件长度：改前 %d → 改后 %d（差 %d）" % (before_len, len(t2), len(t2) - before_len))
sys.exit(0 if (ok and bal) else 1)
