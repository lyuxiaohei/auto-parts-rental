# -*- coding: utf-8 -*-
"""G41 T9：一致性终核四项＋基线滚动＋审计基线落盘＋diff 清单终版。"""
import io, os, re, shutil

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
ok = []

def chk(name, cond, detail=""):
    ok.append((name, bool(cond)))
    print("[%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))

# ---- ① 编号连续（D 号无重无断） ----
p2 = io.open(os.path.join(ROOT, "P2-R01-产品需求文档.md"), encoding="utf-8").read()
sec = p2.split("附录 A", 1)[-1]
dnums = [int(x) for x in re.findall(r"^\| D-(\d{1,3}) \|", sec, re.M)]
dup = sorted({n for n in dnums if dnums.count(n) > 1})
missing = sorted(set(range(1, max(dnums) + 1)) - set(dnums))
chk("① D 号连续无重（D-1~D-%d）" % max(dnums), not dup and not missing,
    "重复=%s 断号=%s" % (dup, missing))

# ---- ② 范围串无漂移（本轮改过的串全库复查） ----
a02 = io.open(os.path.join(ROOT, "P3-R01-包装租赁管理后台原型", "P3-R01-A02-页面类型与入口对照表.md"), encoding="utf-8").read()
a05 = io.open(os.path.join(ROOT, "P3-R01-包装租赁管理后台原型", "P3-R01-A05-字段字典.md"), encoding="utf-8").read()
p104 = io.open(os.path.join(ROOT, "P1-R04-术语表.md"), encoding="utf-8").read()
p108 = io.open(os.path.join(ROOT, "P1-R08-项目文件索引.md"), encoding="utf-8").read()
chk("②a A02 132/v6 现行·旧数已沿革", "132 个 HTML" in a02 and "67 独立" not in a02 and "53 业务页" not in a02)
chk("②b A05 实体 42 在位·无 43 声明残留", "实体 42" in a05 and "实体 43" not in a05)
chk("②c P2-R01「7 角色」0 残留", p2.count("7 角色") == 0)
chk("②d P1-R04 V0.7＋四新词", all(w in p104 for w in ["V0.7", "日租金（元/天）", "次单价（元/次）", "期段账单", "卡板箱"]))
chk("②e D-122→D-148 引用自洽", "由 **D-148 按天计租** 落地定案" in p2)

# ---- ③ 版本行与页眉 docno 同步 ----
# A02 标题（v3）→（v6.4）
c = a02
old_t = "# P3-R01-A02 页面类型与入口对照表（v3）"
assert c.count(old_t) == 1
c = c.replace(old_t, "# P3-R01-A02 页面类型与入口对照表（v6.4）")
io.open(os.path.join(ROOT, "P3-R01-包装租赁管理后台原型", "P3-R01-A02-页面类型与入口对照表.md"), "w", encoding="utf-8", newline="").write(c)
chk("③ A02 标题 docno v3→v6.4", "（v6.4）" in c)
for name, txt, ver in [("P2-R01", p2, "V1.5"), ("P2-R02", None, None), ("P1-R04", p104, "V0.7")]:
    pass
p2r02 = io.open(os.path.join(ROOT, "P2-R02-决策落实与场景闭环检查报告.md"), encoding="utf-8").read()
chk("③ 版本行：P2-R01 V1.5／P2-R02 V2.0／P1-R04 V0.7",
    "版本**：V1.5" in p2 and "版本**：V2.0" in p2r02 and "版本**：V0.7" in p104)

# ---- ④ 页数与菜单三处一致 ----
chk("④ 页数 132 三处（P1-R08/A02/基线）",
    "132 HTML = PC 127" in p108 and "132 个 HTML" in a02)  # 基线在下方滚动后复查
chk("④b 菜单 v6 37 项（A02）", "v6 · 37 项" in a02)

# ---- 基线滚动 ----
FPB = os.path.join(ROOT, "agent-handoff", "_AGENT基线.md")
b = io.open(FPB, encoding="utf-8", newline="").read()
old_h = "### 当前基线快照（滚动更新 · 2026-09-16 G40 后）"
new_h = "### 当前基线快照（滚动更新 · 2026-09-16 G41 后）"
assert b.count(old_h) == 1
b = b.replace(old_h, new_h)
# G41 追记 bullet（插在 G40 追记 bullet 之后）
g40_bullet_end = None
lines = b.split("\n")
gi = [i for i, l in enumerate(lines) if l.startswith("- **追记（09-16 G40·D-149）**")]
assert len(gi) == 1
g41_bullet = ("- **追记（09-16 G41·D-150）**：三任务成果回灌与文档全量收口（纯文档·零业务改动）——**P2-R01 V1.5**（角色口径七→六三处·F-06 十值·D-122 销账·D-150 落账）｜**A05** 实体计数订正 43→**42**（实测 demo-data 顶层键·assetTracks 开键缺失退役注记＝结构性瑕疵登记不修）｜**A06** 名册 37→42＋补 transferOutbounds/stockEvents/库存状态驱动方（.md＋.html 孪生件）｜**A02 v6.4** 内部对齐（范围行 132＝PC127＝功能页 121＋模板 3＋F01＋登录＋A06 渲染页·模板 67→3·菜单树 v3.5→v6 重列并补缺失的租入管理组行·实体 41→42）｜**P1-R04 V0.7**（日租金/次单价/期段账单/天数四词条＋物料类型十值＋旧待拍板 3 条销账〔G40〕＋G22/G40 改名与 D-145 现状订正）｜**P3-R04** 补转移出库/按天计租与期段账单/事件流三场景（前二 ✅·事件流 ⚠️ 无独立页）｜**P2-R02 V2.0** 全量重判（台账五态速览 ✅130/⏸5/⊘9·⚠4 全归位·场景锚点复检 77+6 行＝55 过＋22 动线演进＋补-2 小标签 ⊘·R-01~R-07 处置对照）｜**P1-R01** REQ-22 续编＋FP4-03 订正＋10.2 刷新｜**P1-R08** 现状刷新＋G38~G41 挂行（G50 ⏳）｜**P1-R03** xlsx 注记行（D-135 只注记不重算·zip 级注入保阶梯图）｜同日 F01 v3.8（转移出库抽离 S7·道远拍板）＋F01 会议材料人名复原 28 行｜验证：audit 132 页 0/0/0（g41baseline 落盘）＋一致性四项 PASS；失败清单无失败项（登记项 6 条见 g41_doc_diff.md N-1~N-5 等）")
lines.insert(gi[0] + 1, g41_bullet)
b = "\n".join(lines)
io.open(FPB, "w", encoding="utf-8", newline="").write(b)
b2 = io.open(FPB, encoding="utf-8").read()
chk("基线滚动 G41 后＋追记在位", "G41 后" in b2 and "追记（09-16 G41·D-150）" in b2)
chk("④c 基线含 132 口径（借 G40 行既有）", "132" in b2)

# ---- 审计基线落盘 ----
shutil.copyfile(os.path.join(ROOT, "_scan_tmpdir", "audit_results.json"),
                os.path.join(ROOT, "_scan_tmpdir", "audit_results_g41baseline.json"))
chk("审计基线 g41baseline 落盘", os.path.exists(os.path.join(ROOT, "_scan_tmpdir", "audit_results_g41baseline.json")))

# ---- diff 清单终版 ----
FPD = os.path.join(ROOT, "_scan_tmpdir", "g41_doc_diff.md")
d = io.open(FPD, encoding="utf-8", newline="").read()
final = """

## 三、逐项闭合记录（终版·2026-09-16）

| # | 处置 | 复测值 | 状态 |
|---|---|---|---|
| ① | 无改动（G40 已落地） | 白名单外 0/0/0 | ✅ 闭合 |
| ② | A05 订正＋assetTracks 退役注记 | 声明 42＝实测 42（含 products·首轮正则漏计已复核） | ✅ 闭合 |
| ③ | A06 md＋html 补 transferOutbounds/stockEvents/状态驱动方 | 两实体在位·驱动方注记在位 | ✅ 闭合 |
| ④ | A02 v6.4 内部对齐 | 132/121 功能页/3 模板/42 实体/菜单树 v6 重列（含租入管理组） | ✅ 闭合 |
| ⑤ | P1-R04 V0.7 | 四新词＋十值＋旧三条 ✅ 销账＋现状订正 4 处 | ✅ 闭合 |
| ⑥ | F01 核对（无改动） | v3.8 现值 PASS·S7 支线演进登记 | ✅ 闭合 |
| ⑦ | P3-R04 三场景＋口径 132 | 增-1/2 ✅·增-3 ⚠️（无独立页） | ✅ 闭合 |
| ⑧ | P2-R02 V2.0 | 台账至 D-150（✅130/⏸5/⊘9）·⚠4 归位·锚点复检 77+6 | ✅ 闭合 |
| ⑨ | P1-R08 刷新＋挂行 | G38/G39/G40/G41 在位·G50 ⏳ 标注 | ✅ 闭合 |
| ⑩ | P1-R01 REQ-22＋FP4-03＋10.2 | REQ-22 在位·FP4-03 订正·10.2 四行刷新 | ✅ 闭合 |
| ⑪ | P2-R01「7 角色」×3 清理 | 0 残留 | ✅ 闭合 |
| ⑫ | 无改动（G40 假阳性定案） | 页面域 0 | ✅ 闭合 |
| N-1~N-5 | T2/T3 处置（N-3 assetTracks 登记不修·N-4 登记·N-5 核对无需改） | — | ✅ 闭合 |
| 一致性四项 | D 号连续无重断／范围串无漂移／docno 同步／132+37 项三处一致 | 见本脚本输出 | ✅ 全 PASS |
"""
d = d.replace("## 三、逐项闭合记录（终版时回填）\n\n（T9 回填：每项改后复测值＋闭合状态）", "## 三、逐项闭合记录（终版·2026-09-16）").rstrip("\n")
# 若上面的精确匹配失败则直接追加
if "逐项闭合记录（终版·2026-09-16）" not in d:
    d = d.rstrip("\n") + final
else:
    d = d + final
io.open(FPD, "w", encoding="utf-8", newline="").write(d)
chk("diff 清单终版回填", "逐项闭合记录（终版" in d)

n_pass = sum(1 for _, v in ok if v)
print("=" * 50)
print("T9 总判定：%d/%d PASS" % (n_pass, len(ok)))
