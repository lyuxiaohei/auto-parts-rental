# -*- coding: utf-8 -*-
"""G25 T4：角色管理 auditPermMatrix 追加 付款登记/收款确认（checked）14→16（CRLF 保持）"""
import io, sys

PG = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\系统管理\角色管理.html"
NL = "\r\n"

txt = io.open(PG, encoding="utf-8", newline="").read()
anchor = ('        <span class="checkbox" data-audit="租入归还"><span class="box"></span>租入归还</span>' + NL +
          "      </div>")
n = txt.count(anchor)
assert n == 1, "锚点命中 %d 次" % n
assert txt.count("data-audit=") == 14, "改前 data-audit 应 14，实际 %d" % txt.count("data-audit=")

new = ('        <span class="checkbox" data-audit="租入归还"><span class="box"></span>租入归还</span>' + NL +
       '        <span class="checkbox checked" data-audit="付款登记"><span class="box">✓</span>付款登记</span>' + NL +
       '        <span class="checkbox checked" data-audit="收款确认"><span class="box">✓</span>收款确认</span>' + NL +
       "      </div>")
txt = txt.replace(anchor, new)
io.open(PG, "w", encoding="utf-8", newline="").write(txt)

t2 = io.open(PG, encoding="utf-8", newline="").read()
assert t2.count("data-audit=") == 16, "改后应 16，实际 %d" % t2.count("data-audit=")
assert t2.count('data-audit="付款登记"') == 1 and t2.count('data-audit="收款确认"') == 1
# 标签配平（span/div 计数改前改后一致比例）
import re
before = io.open(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\backup-g25-20260912\系统管理\角色管理.html", encoding="utf-8", newline="").read()
def cnt(s, tag):
    return len(re.findall("<%s[\\s>]" % tag, s)) - len(re.findall("</%s>" % tag, s))
bal = all(cnt(before, tg) == cnt(t2, tg) for tg in ("span", "div"))
raw = open(PG, "rb").read()
print("PASS T4：data-audit=16（付款登记/收款确认 checked 各 1）·标签配平 %s·CRLF=%d 裸LF=%d" % (
    bal, raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")))
assert bal
