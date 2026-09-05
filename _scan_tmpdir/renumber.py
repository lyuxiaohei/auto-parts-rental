# -*- coding: utf-8 -*-
"""F01 v2.9 编号体系规范化：
① 财务通道 F1（应收）/F2（应付）——总标题与来源节点主标带编号（零坐标位移）
② 支线重排 S2-S7 → S1-S6（两阶段占位符防连锁）
③ 前置行下加编号规则说明行
④ F01 10 处 S 引用 + SRC_DATA fin head + A04 desc/pin note 同步"""
import re
from pathlib import Path

F01 = Path(r"P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图.html")
A04 = Path(r"P3-R01-包装租赁管理后台原型/P3-R01-A04-流程链标注数据.json")
src = F01.read_text(encoding="utf-8")

def rep(old, new, n=1):
    global src
    c = src.count(old)
    assert c == n, f"anchor {c}!={n}: {old[:60]!r}"
    src = src.replace(old, new)

# ── 1. 财务通道 F1/F2（零位移：总标题 + 来源节点主标）
rep(">财务通道 · 5 条线共用（应收 ＋ 应付）</text>", ">财务通道 F1 应收 / F2 应付 · 5 条线共用</text>")
rep(">应收来源</text>", ">F1 · 应收来源</text>")
rep(">应付来源</text>", ">F2 · 应付来源</text>")

# ── 2. 支线标题重排 S2-S7 → S1-S6（两阶段）
PH = {"S2": "@@1@@", "S3": "@@2@@", "S4": "@@3@@", "S5": "@@4@@", "S6": "@@5@@", "S7": "@@6@@"}
TITLES = [("S2 · 库存运营", "S1 · 库存运营"), ("S3 · 项目经营", "S2 · 项目经营"),
          ("S4 · 系统支撑", "S3 · 系统支撑"), ("S5 · 赔偿转单据", "S4 · 赔偿转单据"),
          ("S6 · 录单页与台账", "S5 · 录单页与台账"), ("S7 · 审核与待办", "S6 · 审核与待办")]
for old, _ in TITLES:
    rep(old, PH[old[:2]] + old[2:], 1)          # 阶段1：旧编号→占位
for old, new in TITLES:
    rep(PH[old[:2]] + old[2:], new, 1)          # 阶段2：占位（旧串）→新编号
# 其余 S 引用
rep("<!-- S7 审核与待办 -->", "<!-- S6 审核与待办 -->")
rep("· 详见 S5</text>", "· 详见 S4</text>")
rep("（S1 采购应付已并入财务通道）· 灰底", "（采购应付已并入财务通道 F2）· 灰底")
rep("+ 6 条支线（S1 采购应付已并入财务通道）", "+ 6 条支线 S1-S6（采购应付已并入 F2）")

# ── 3. 编号规则说明行（前置行 y=26 与 B1 标题 y=64 之间，y=44 插入，无位移）
anchor = '<text x="40" y="64" fill="#1f2937" font-size="14" font-weight="700" font-family="\'Geist\',sans-serif">B1 · 零部件买卖'
rep(anchor, '    <text x="40" y="44" fill="#9ca3af" font-size="9.5" font-family="\'Geist Mono\',monospace">编号规则：B 买卖 · L 租赁（L1 单一 / L2 组合 / L3 租入转租 / L4 混合）· T 退租专项 · F 财务（F1 应收 / F2 应付）· S 支撑支线</text>\n' + anchor)

# ── 4. SRC_DATA fin head
rep("fin: {head:'财务通道 · 会议依据', items:[", "fin: {head:'财务通道 F1 应收 / F2 应付 · 会议依据', items:[")

# ── 5. 自检
for tag in ["a", "g", "svg", "text"]:
    o = len(re.findall(rf"<{tag}[\s>]", src)); c = src.count(f"</{tag}>")
    assert o == c, f"<{tag}> 配平失败 {o} vs {c}"
assert "@@" not in src
for probe in ["S1 · 库存运营", "S6 · 审核与待办", "F1 · 应收来源", "F2 · 应付来源", "编号规则：B 买卖", "详见 S4"]:
    assert probe in src, probe
assert "S7" not in src and "S2 · 库存运营" not in src
F01.write_text(src, encoding="utf-8", newline="")
print("F01 OK")

# ── 6. A04 同步（desc + S5/S6/S7 pin 引用；S1 单号 AR-…-S1 保护）
j = A04.read_text(encoding="utf-8")
for old, new in [
    ("（B1/L1/L2/L3/L4/T1 主线、S2~S7 支线——S1 采购应付已并入财务通道）",
     "（B1/L1-L4/T1 主线 ＋ 财务 F1 应收/F2 应付 ＋ S1-S6 支线——采购应付已并入 F2）"),
    ("S5 · 租入赔付", "@@S4@@ · 租入赔付"), ("S5 转应收", "@@S4@@ 转应收"), ("S5 · 赔偿转应收", "@@S4@@ · 赔偿转应收"),
    ("S6 · 租出台账", "@@S5@@ · 租出台账"),
    ("S7 审核与待办支线", "@@S6@@ 审核与待办支线"), ("S7 · 我的待办", "@@S6@@ · 我的待办"),
]:
    assert j.count(old) == 1, (old, j.count(old))
    j = j.replace(old, new)
c = j.count("S6 支线"); assert c == 2, c
j = j.replace("S6 支线", "@@S5@@ 支线")
j = j.replace("@@S4@@", "S4").replace("@@S5@@", "S5").replace("@@S6@@", "S6")
assert "@@" not in j and "AR-2026-09-PRJ2601-S1" in j
import json; json.loads(j)
A04.write_text(j, encoding="utf-8", newline="")
print("A04 OK（单号 AR-…-S1 未动）")
