# -*- coding: utf-8 -*-
"""09-14 道远拍板：租价三段式按次→周期单位隐藏（非禁用）
改双层：产品档案.html + 弹窗/新建产品.html（各 3 处）+ P2-R01 正文 UC-BAS-02 + 台账 D-91
"""
import io, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
FILES = [ROOT + r"\基础数据\产品档案.html", ROOT + r"\基础数据\弹窗\新建产品.html"]

# ---- 1. 原型双层 ----
old_fn = "var u=document.getElementById(p+'UnitSel');u.disabled=(m==='按次');var us="
new_fn = "var u=document.getElementById(p+'UnitSel');u.disabled=(m==='按次');var ub=document.getElementById(p+'UnitBox');if(ub)ub.style.display=(m==='按次')?'none':'';var us="
old_cmt = "/* G21 租价三段式联动：计费方式(按时间周期/按次)×周期单位(月/年/日·默认月)+数值，后缀=元/计量单位·周期（单位取同表单「单位」下拉） */"
new_cmt = "/* G21 租价三段式联动：计费方式(按时间周期/按次)×周期单位(月/年/日·默认月)+数值，后缀=元/计量单位·周期（单位取同表单「单位」下拉）；按次→周期单位隐藏（2026-09-14 道远拍板·原为禁用置灰） */"
for fp in FILES:
    t = io.open(fp, encoding="utf-8", newline="").read()
    assert t.count(old_fn) == 1, fp + " 函数锚点 %d" % t.count(old_fn)
    assert t.count(old_cmt) == 1, fp + " 注释锚点 %d" % t.count(old_cmt)
    t = t.replace(old_fn, new_fn, 1).replace(old_cmt, new_cmt, 1)
    for pfx in ("rentIn", "rental"):
        old_box = '<div class="input-box select-box" style="width:72px;flex:none;"><select id="%sUnitSel"' % pfx
        new_box = '<div class="input-box select-box" id="%sUnitBox" style="width:72px;flex:none;"><select id="%sUnitSel"' % (pfx, pfx)
        n = t.count(old_box)
        assert n == 1, "%s %s box 锚点 %d" % (fp, pfx, n)
        t = t.replace(old_box, new_box, 1)
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    raw = open(fp, "rb").read()
    print("PASS", fp.split("\\")[-1], "函数+注释+双 box id·CRLF=%d 裸LF=%d" % (
        raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")))

# ---- 2. P2-R01 正文 + 台账 ----
R01 = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P2-R01-产品需求文档.md"
t = io.open(R01, encoding="utf-8", newline="").read()
old_uc = "按次时周期单位禁用；后缀联动「元/单位·周期」"
new_uc = "按次时周期单位隐藏不显示（2026-09-14 道远拍板·原禁用置灰）；后缀联动「元/单位·周期」"
assert t.count(old_uc) == 1, "UC-BAS-02 锚点 %d" % t.count(old_uc)
t = t.replace(old_uc, new_uc, 1)
anchor = "| D-90 | P3-R04 二节执行层采纳 7 条"
i = t.find(anchor)
assert i > 0
line_end = t.find("\n", i)
d91 = "| D-91 | 租价三段式：计费方式选「按次」时周期单位控件隐藏（不显示），非禁用置灰——新建/编辑物料弹窗双层联动 | 道远 09-14 拍板（新建物料弹窗目检·修订 UC-BAS-02） | ✅ |"
NL = "\r\n" if t.count("\r\n") > (t.count("\n") - t.count("\r\n")) else "\n"
t = t[:line_end + 1] + d91 + NL + t[line_end + 1:]
io.open(R01, "w", encoding="utf-8", newline="").write(t)
t2 = io.open(R01, encoding="utf-8", newline="").read()
import re
n = len(re.findall(r"^\| D-\d+ \|", t2, re.M))
print("PASS P2-R01：UC-BAS-02 改隐藏+D-91 落账·台账 D 行=%d（预期 91）" % n)
assert n == 91
