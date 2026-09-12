# -*- coding: utf-8 -*-
"""读 receivableBills 实体：全部键+btype 摘要+末条完整结构（CRLF 保持读）"""
import io, re

t = io.open(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\_data\demo-data.js", encoding="utf-8", newline="").read()
m = re.search(r"^  receivableBills: \{", t, re.M)
print("实体 @", m.start())
seg = t[m.start():t.find("\n  /* ----", m.start())]
print("段长:", len(seg))
for km in re.finditer(r"^    '([^']+)': \{", seg, re.M):
    key = km.group(1)
    rs = seg.find("'row'", km.start())
    bt = re.search(r'"btype": "([^"]+)"', seg[rs:rs + 400])
    st = re.search(r'"status": "([^"]+)"', seg[rs:rs + 400])
    print(key, "| btype:", bt.group(1) if bt else "?", "| status:", st.group(1) if st else "?")
# 末条键
last = list(re.finditer(r"^    '([^']+)': \{", seg, re.M))[-1]
print("\n末条:", last.group(1))
print(seg[last.start():last.start() + 2400])
