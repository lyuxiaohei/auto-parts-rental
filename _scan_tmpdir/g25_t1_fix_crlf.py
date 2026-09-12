# -*- coding: utf-8 -*-
"""G25 T1 修复重放：从备份以 newline='' 读写（保 CRLF），重放 12 处替换"""
import io, sys

BAK = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\backup-g25-20260912\P3-R01-F01-业务流程导航图.html"
F01 = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\P3-R01-F01-业务流程导航图.html"

txt = io.open(BAK, encoding="utf-8", newline="").read()  # 保留 \r\n
assert txt.count("\r\n") == 822 and (txt.count("\n") - txt.count("\r\n")) == 0, "备份行尾异常"

REPL = [
    ("<b>B1</b> 零部件买卖", "<b>B1</b> 物料买卖"),
    ("B1 零部件买卖、", "B1 物料买卖、"),
    ("<!-- ======== B1 · 零部件买卖 ======== -->", "<!-- ======== B1 · 物料买卖 ======== -->"),
    ("B1 · 零部件买卖（一进一出 · 无组装）", "B1 · 物料买卖（一进一出 · 无组装）"),
    ('subgraph B1["B1 · 零部件买卖（一进一出）"]', 'subgraph B1["B1 · 物料买卖（一进一出）"]'),
    ("b1: {head:'B1 · 零部件买卖 · 会议依据'", "b1: {head:'B1 · 物料买卖 · 会议依据'"),
    ("L3 · 租赁 · 租入转租（向供应商/供应商租入 → 转租客户）", "L3 · 租赁 · 租入转租（向供应商租入 → 转租客户）"),
    ('text-anchor="middle">向供应商/供应商租入</text>', 'text-anchor="middle">向供应商租入</text>'),
    ("业务流程 · 按第2次沟通纪要", "业务流程 · 按第3次沟通纪要"),
    ('text-anchor="middle">器具 · 资产采购</text>', 'text-anchor="middle">物料 · 资产采购</text>'),
    ('text-anchor="middle">单一器具 · 直接出租</text>', 'text-anchor="middle">单一物料 · 直接出租</text>'),
    ('text-anchor="middle">器具A/B/C 采购</text>', 'text-anchor="middle">物料A/B/C 采购</text>'),
]
for old, new in REPL:
    n = txt.count(old)
    assert n == 1, "count(%r)=%d" % (old[:30], n)
    txt = txt.replace(old, new)

io.open(F01, "w", encoding="utf-8", newline="").write(txt)

# 终态核
t2 = io.open(F01, encoding="utf-8", newline="").read()
raw = open(F01, "rb").read()
crlf = raw.count(b"\r\n"); lf = raw.count(b"\n") - crlf
ok = (t2.count("零部件买卖") == 0 and t2.count("向供应商/供应商") == 0
      and t2.count("按第2次沟通纪要") == 0 and t2.count("物料买卖") == 6
      and t2.count("器具") == 4 and crlf == 822 and lf == 0)
print("终态断言:", "PASS" if ok else "FAIL",
      "| CRLF=%d 裸LF=%d 零部件买卖=%d 物料买卖=%d 器具=%d" % (crlf, lf, t2.count("零部件买卖"), t2.count("物料买卖"), t2.count("器具")))
sys.exit(0 if ok else 1)
