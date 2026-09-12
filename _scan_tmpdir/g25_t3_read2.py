# -*- coding: utf-8 -*-
"""读 BS-20260828-004 完整条目+应收页结构+应付 AP-20260905-013（对称参照）"""
import io, re

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
t = io.open(ROOT + r"\_data\demo-data.js", encoding="utf-8", newline="").read()

def dump_entity(seg, key):
    m = re.search(r"^    '" + re.escape(key) + r"': \{", seg, re.M)
    if not m:
        print("未找到", key); return
    nxt = list(re.finditer(r"^    '[^']+': \{", seg[m.start() + 10:], re.M))
    e = m.start() + 10 + (nxt[0].start() if nxt else len(seg) - m.start() - 10)
    print(seg[m.start():e])

m = re.search(r"^  receivableBills: \{", t, re.M)
seg = t[m.start():t.find("\n  /* ----", m.start())]
dump_entity(seg, "BS-20260828-004")
print("\n" + "=" * 60 + "\n")
mp = re.search(r"^  payableBills: \{", t, re.M)
segp = t[mp.start():t.find("\n  /* ----", mp.start())]
dump_entity(segp, "AP-20260905-013")
