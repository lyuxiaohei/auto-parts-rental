# -*- coding: utf-8 -*-
"""修复 2+3（幂等版）：税率卡移除/A03 改挂 + 销售订单下单方式整域删除"""
import io, json, subprocess, sys, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"

# ---------- 修复 2：产品档案移除税率卡（幂等） ----------
fp = ROOT + r"\基础数据\产品档案.html"
t = io.open(fp, encoding="utf-8", newline="").read()
if '<tbody id="taxRateBody">' in t:
    i = t.find("供应商税率维护")
    start = t.rfind('<div class="card">', 0, i)
    d = 0
    p = start
    for m in re.finditer(r"<div\b|</div>", t[start:]):
        d += 1 if not m.group(0).startswith("</") else -1
        p = start + m.end()
        if d == 0:
            break
    card = t[start:p]
    assert "taxRateBody" in card, "卡片范围异常"
    t = t[:start] + t[p:]
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    print("PASS 修复2 税率卡移除")
else:
    print("SKIP 修复2 税率卡已移除")

fp = ROOT + r"\P3-R01-A03-标注数据.json"
d = json.load(io.open(fp, encoding="utf-8"))
pin = d["基础数据/产品档案.html"][0]
if pin["selector"] != '<div class="tax-sec-title">供应商税率':
    pin["selector"] = '<div class="tax-sec-title">供应商税率'
    pin["note"] = pin["note"] + "\n税率在新建物料弹窗内按供应商维护（行编辑器）；本页不再单列维护表。"
    d["_meta"]["date"] = d["_meta"].get("date", "") + "；2026-09-14 会话：产品档案 pin1 改挂新建物料弹窗税率区"
    io.open(fp, "w", encoding="utf-8", newline="").write(
        json.dumps(d, ensure_ascii=False, indent=1).replace("\n", "\r\n") + "\r\n")
    print("PASS 修复2 A03 pin1 改挂")
else:
    print("SKIP 修复2 A03 已改挂")

# ---------- 修复 3：demo-data ----------
fp = ROOT + r"\_data\demo-data.js"
t = io.open(fp, encoding="utf-8", newline="").read()
FRAGS = [
    ('"<span class=\\"tag tag-blue\\">项目经理代下</span>", ', 5),
    ('"<span class=\\"tag tag-gray\\">客户自助</span>", ', 3),
]
if t.count(FRAGS[0][0]) or t.count(FRAGS[1][0]) or '"mode"' in t:
    for frag, expect in FRAGS:
        n = t.count(frag)
        assert n == expect, "片段=%d 预期=%d: %s" % (n, expect, frag[:40])
        t = t.replace(frag, "", t.count(frag))
    n_mode = len(re.findall(r'"mode": "[^"]+", ', t))
    assert n_mode == 8, "mode=%d" % n_mode
    t = re.sub(r'"mode": "[^"]+", ', "", t)
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    r = subprocess.run(["node", "--check", fp], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:200]
    print("PASS 修复3 demo-data：tag×8+mode×8 移除·node --check 0")
else:
    print("SKIP 修复3 demo-data 已移除")

# ---------- 修复 3：销售订单列表 ----------
fp = ROOT + r"\销售管理\销售订单列表.html"
raw = open(fp, "rb").read()
c0, l0 = raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")
NL = "\r\n" if c0 > l0 else "\n"
t = io.open(fp, encoding="utf-8", newline="").read()
if "<th>是否代下单</th>" in t:
    assert t.count("<th>是否代下单</th>") == 1
    t = t.replace("<th>是否代下单</th>", "", 1)
    flt = "," + NL + "    { label: '下单方式', field: 'mode' }"
    assert t.count(flt) == 1, "筛选锚=%d" % t.count(flt)
    t = t.replace(flt, "", 1)
FF = ('<div class="ff ff-row-extra"><span class="ff-label">下单方式：</span>' + NL +
      '      <select><option selected>全部</option><option>客户自助</option><option>项目经理代下</option></select>' + NL +
      '      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>' + NL +
      '    </div>' + NL)
if FF in t:
    assert t.count(FF) == 1, "ff=%d" % t.count(FF)
    t = t.replace(FF, "", 1)
ROW = ("<div class=\"form-row\">" + NL +
       "    <span class=\"form-label\">下单方式</span>" + NL +
       "    <div><span class=\"radio\"><span class=\"dot\"></span>客户自助下单</span><span class=\"radio checked\"><span class=\"dot\"></span>项目经理代下单</span></div>" + NL +
       "  </div>")
if ROW in t:
    assert t.count(ROW) == 1
    t = t.replace(ROW, "", 1)
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    print("PASS 修复3 销售订单列表：th/筛选/radio 移除")
else:
    print("SKIP 修复3 销售订单列表 已移除")

# ---------- 修复 3：新建销售订单模板 ----------
fp = ROOT + r"\销售管理\弹窗\新建销售订单.html"
raw = open(fp, "rb").read()
c0, l0 = raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")
NL = "\r\n" if c0 > l0 else "\n"
ROW = ("<div class=\"form-row\">" + NL +
       "    <span class=\"form-label\">下单方式</span>" + NL +
       "    <div><span class=\"radio\"><span class=\"dot\"></span>客户自助下单</span><span class=\"radio checked\"><span class=\"dot\"></span>项目经理代下单</span></div>" + NL +
       "  </div>")
t = io.open(fp, encoding="utf-8", newline="").read()
if ROW in t:
    assert t.count(ROW) == 1
    t = t.replace(ROW, "", 1)
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    print("PASS 修复3 新建销售订单模板 radio 移除")
else:
    print("SKIP 修复3 模板 已移除")
