# -*- coding: utf-8 -*-
"""G25 T1 前置扫描：F01 四组旧词出现位置+上下文（只读，不改）"""
import re, os

F01 = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\P3-R01-F01-业务流程导航图.html"
txt = open(F01, encoding="utf-8").read()
print("文件长度:", len(txt))

TERMS = ["零部件买卖", "向供应商/供应商租入", "向供应商/供应商", "第2次沟通纪要", "器具"]
for t in TERMS:
    hits = [m.start() for m in re.finditer(re.escape(t), txt)]
    print("\n===== 「%s」 共 %d 处 =====" % (t, len(hits)))
    for i, p in enumerate(hits):
        s = max(0, p - 60); e = min(len(txt), p + len(t) + 60)
        ctx = txt[s:e].replace("\n", "⏎").replace("\r", "")
        print("[%d] @%d …%s…" % (i + 1, p, ctx))
