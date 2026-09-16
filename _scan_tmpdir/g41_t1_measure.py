# -*- coding: utf-8 -*-
"""G41 T1 差异实测：任务书第一节 12 项逐项复测现值（只读）。输出 g41_doc_diff.md 数据。"""
import io, os, re, json

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
PROTO = os.path.join(ROOT, "P3-R01-包装租赁管理后台原型")

def rd(p, root=ROOT):
    return io.open(os.path.join(root, p), encoding="utf-8").read()

R = []
def sec(t): R.append("\n## " + t); print("\n== " + t + " ==")

# 基准
sec("基准")
htmls = []
for dp, dn, fn in os.walk(PROTO):
    if ".prompts" in dn: dn.remove(".prompts")
    htmls += [os.path.join(dp, f) for f in fn if f.endswith(".html")]
print("HTML 总数 %d（PC %d + mobile %d）" % (len(htmls), len(htmls) - 5, 5))
R.append("- HTML 总数 **%d**（PC %d + mobile 5）" % (len(htmls), len(htmls) - 5))

dd = rd(os.path.join("P3-R01-包装租赁管理后台原型", "_data", "demo-data.js"))
ents = re.findall(r"^const (\w+) = \[", dd, re.M)
if not ents:
    ents = re.findall(r"^(?:const|var|let) (\w+)\s*=\s*\[", dd, re.M)
print("demo-data 顶层实体 %d：%s" % (len(ents), ",".join(ents)))
R.append("- demo-data 顶层实体 **%d**" % len(ents))
R.append("- 实体清单：%s" % "、".join(ents))

# ① 术语
sec("① D-142 术语三条（白名单外）")
WHITELIST = {"P3-R01-A05-字段字典.md", "P3-R01-F01-业务流程导航图.html"}
cnt = {"水单": 0, "盈亏": 0, "回款": 0}; wl = {"水单": 0, "盈亏": 0, "回款": 0}
for dp, dn, fn in os.walk(PROTO):
    if ".prompts" in dn: dn.remove(".prompts")
    for f in fn:
        if os.path.splitext(f)[1].lower() not in {".html", ".js", ".md", ".json", ".css", ".txt"}: continue
        c = io.open(os.path.join(dp, f), encoding="utf-8").read()
        for t in cnt:
            n = c.count(t)
            if n:
                (wl if f in WHITELIST else cnt)[t] += n
print("白名单外：%s；白名单内：%s" % (cnt, wl))
R.append("- 白名单外残留：%s → %s" % (cnt, "全 0 ✅" if all(v == 0 for v in cnt.values()) else "❌"))
R.append("- 白名单内（A05 沿革/禁用列＋F01 SRC_DATA 会议原文）：%s" % wl)

# ② A05 实体计数
sec("② A05 实体计数")
a05 = rd(os.path.join("P3-R01-包装租赁管理后台原型", "P3-R01-A05-字段字典.md"))
decl = re.findall(r"[^\d]([34]\d)\s*(?:个|个顶层)?实体", a05[:3000])
head = a05[:1500].replace("\n", " ")[:300]
print("A05 头部计数句候选：%s" % decl)
R.append("- A05 头部实体计数候选串：%s（原文头 300 字见下）" % decl)
R.append("- A05 头部摘录：`%s`" % head)
print("实测（demo-data）=%d" % len(ents))

# ③ A06
sec("③ A06 收口项")
a06m = rd(os.path.join("P3-R01-包装租赁管理后台原型", "P3-R01-A06-实体关系与状态机.md"))
for t in ["transferOutbounds", "stockEvents", "转移单审核", "转租登记"]:
    print("  A06 md 含 %-18s %d" % (t, a06m.count(t)))
    R.append("- A06 md `%s` ×%d" % (t, a06m.count(t)))

# ④ A02 新旧混排
sec("④ A02 新旧混排")
a02 = rd(os.path.join("P3-R01-包装租赁管理后台原型", "P3-R01-A02-页面类型与入口对照表.md"))
for t in ["132", "v6", "128", "67", "v3.5", "v6.1", "v6.2"]:
    print("  A02 含 %-6s %d" % (t, a02.count(t)))
    R.append("- A02 `%s` ×%d" % (t, a02.count(t)))

# ⑤ P1-R04
sec("⑤ P1-R04")
p104 = rd("P1-R04-术语表.md")
for t in ["日租金", "次单价", "期段", "卡板箱", "待拍板", "水单", "盈亏", "回款", "V0.6", "V0.7"]:
    print("  P1-R04 含 %-8s %d" % (t, p104.count(t)))
    R.append("- P1-R04 `%s` ×%d" % (t, p104.count(t)))
m = re.search(r"物料类型[^\n]{0,120}", p104)
print("  物料类型行：%s" % (m.group(0)[:110] if m else "无"))
R.append("- 物料类型行摘录：`%s`" % (m.group(0)[:110] if m else "无"))

# ⑥ F01
sec("⑥ F01 现值")
f01 = rd(os.path.join("P3-R01-包装租赁管理后台原型", "P3-R01-F01-业务流程导航图.html"))
for t in ["v3.8", "v3.7", "S7 · 转移出库", "转移出库", "按持有量计租", "转移单审核驱动", "客户虚拟仓不维护", "王琳总", "袁丽晶", "陆鸣"]:
    print("  F01 含 %-14s %d" % (t, f01.count(t)))
    R.append("- F01 `%s` ×%d" % (t, f01.count(t)))
rules = rd(os.path.join("P3-R01-包装租赁管理后台原型", "P3-R01-F01-业务流程导航图-开发规则.md"))
for t in ["v3.8", "2026-09-16"]:
    print("  开发规则含 %-10s %d" % (t, rules.count(t)))
    R.append("- 开发规则 `%s` ×%d" % (t, rules.count(t)))

# ⑦ P3-R04
sec("⑦ P3-R04")
p304 = rd("P3-R04-演示场景覆盖梳理.md")
for t in ["转移出库", "按持有量", "期段", "事件流", "stockEvents"]:
    print("  P3-R04 含 %-10s %d" % (t, p304.count(t)))
    R.append("- P3-R04 `%s` ×%d" % (t, p304.count(t)))
dates = re.findall(r"2026-09-\d{2}", p304)
print("  最大日期：%s" % max(dates) if dates else "无")
R.append("- P3-R04 最大日期：%s" % (max(dates) if dates else "无"))

# ⑧ P2-R02
sec("⑧ P2-R02")
p202 = rd("P2-R02-决策落实与场景闭环检查报告.md")
ds = sorted(set(int(x) for x in re.findall(r"D-(\d{1,3})", p202)))
print("  P2-R02 D 号范围：%d~%d（命中 %d 个）" % (ds[0], ds[-1], len(ds)))
print("  V1.0=%d V2.0=%d" % (p202.count("V1.0"), p202.count("V2.0")))
R.append("- P2-R02 D 号最大 **D-%d**（现台账至 D-149）·V1.0×%d V2.0×%d" % (ds[-1], p202.count("V1.0"), p202.count("V2.0")))

# ⑨ P1-R08
sec("⑨ P1-R08")
p108 = rd("P1-R08-项目文件索引.md")
for t in ["G37", "G38", "G39", "G40", "G41", "G50", "132", "v6"]:
    print("  P1-R08 含 %-6s %d" % (t, p108.count(t)))
    R.append("- P1-R08 `%s` ×%d" % (t, p108.count(t)))

# ⑩ P1-R01
sec("⑩ P1-R01")
p101 = rd("P1-R01-需求梳理与功能框架.md")
for t in ["按持有量", "转移出库", "按天计租", "期段"]:
    print("  P1-R01 含 %-8s %d" % (t, p101.count(t)))
    R.append("- P1-R01 `%s` ×%d" % (t, p101.count(t)))

# ⑪ P2-R01 正文 7 角色
sec("⑪ P2-R01")
p201 = rd("P2-R01-产品需求文档.md")
lines7 = [(i, l.strip()[:80]) for i, l in enumerate(p201.splitlines(), 1) if "7 角色" in l or "七角色" in l]
print("  「7 角色」命中 %d 处：%s" % (len(lines7), [(i) for i, _ in lines7]))
R.append("- P2-R01 「7 角色」×%d（行 %s）" % (len(lines7), "/".join(str(i) for i, _ in lines7)))
for t in ["按持有量计租", "max(2", "日租金", "期段账单", "D-148", "D-149", "V1.4", "V1.5"]:
    print("  P2-R01 含 %-10s %d" % (t, p201.count(t)))
    R.append("- P2-R01 `%s` ×%d" % (t, p201.count(t)))
dnums = sorted(set(int(x) for x in re.findall(r"\bD-(\d{1,3})\b", p201)))
print("  台账 D 号最大：D-%d" % dnums[-1])
R.append("- P2-R01 台账最大 **D-%d**" % dnums[-1])

# ⑫ 货品
sec("⑫ 货品（页面域）")
hp = 0
for dp, dn, fn in os.walk(PROTO):
    if ".prompts" in dn: dn.remove(".prompts")
    for f in fn:
        if f == "P3-R01-A05-字段字典.md": continue
        if os.path.splitext(f)[1].lower() not in {".html", ".js", ".md", ".json", ".css", ".txt"}: continue
        c = io.open(os.path.join(dp, f), encoding="utf-8").read()
        hp += c.replace("供货品类", "").count("货品")
print("  页面域货品（掩码供货品类后）：%d" % hp)
R.append("- 页面域「货品」=%d" % hp)

io.open(os.path.join(ROOT, "_scan_tmpdir", "g41_t1_measures.txt"), "w", encoding="utf-8").write("\n".join(R))
print("\n已写 _scan_tmpdir/g41_t1_measures.txt")
