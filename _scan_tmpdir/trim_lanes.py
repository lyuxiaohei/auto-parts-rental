# -*- coding: utf-8 -*-
"""F01 v2.9：L1-L4 泳道止于组合出库——删退租占位+全部下游节点+回环，组合出库右侧加引导注记；
退租及后续链路统一在 T1（T1 无需补内容，逐项已有对应）。"""
import re
from pathlib import Path

F01 = Path(r"P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图.html")
A04 = Path(r"P3-R01-包装租赁管理后台原型/P3-R01-A04-流程链标注数据.json")
src = F01.read_text(encoding="utf-8")

def sub1(pat, repl, label):
    global src
    new, n = re.subn(pat, repl, src)
    assert n == 1, f"[{label}] 命中 {n} != 1"
    src = new

def rep(old, new, n=1):
    global src
    c = src.count(old)
    assert c == n, f"anchor {c}!={n}: {old[:60]!r}"
    src = src.replace(old, new)

# ── 1. 删四泳道尾部节点块（占位/丢损赔偿/租入归还/分流归还/在租台账/租金应付/多线应付）
for y, xs in [(282, [664, 976, 1132]), (422, [784, 1032, 1156]), (562, [664, 976, 1132]), (768, [708, 956, 1080])]:
    for x in xs:
        sub1(rf'<a href="[^"]+">\s*<rect x="{x}" y="{y}"[\s\S]*?</a>\n\s*', '', f'节点 x={x} y={y}')

# ── 2. 删占位前后连线（组合出库→占位、占位→下游、下游→终点）
LINES = [(310, [(648,664),(960,976),(1116,1132)]), (450, [(772,784),(1020,1032),(1144,1156)]),
         (590, [(648,664),(960,976),(1116,1132)]), (796, [(696,708),(944,956),(1068,1080)])]
for y, pairs in LINES:
    for x1, x2 in pairs:
        sub1(rf'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#4b5563" stroke-width="1" marker-end="url\(#arr\)"/>\n\s*', '', f'连线 {x1}->{x2}@y={y}')

# ── 3. 删 L1/L2 回环（path + 底衬 rect + 文字）
for path_d, rx, tx in [('M 1046 338 V 358 H 422 V 338', 'x="660" y="351" width="148"', '器具回库 · 循环再出租'),
                        ('M 964 478 V 498 H 468 V 478', 'x="638" y="491" width="156"', '拆回散件 · 循环再组装')]:
    sub1(rf'<path d="{path_d.replace(" ", r"\s*")}"[^/]*/>\n\s*', '', f'回环path {path_d[:12]}')
    sub1(rf'<rect {rx} height="13" rx="2" fill="#fafafa"/>\n\s*', '', f'回环rect {rx}')
    sub1(rf'<text [^>]*>{tx}</text>\n\s*', '', f'回环text {tx[:6]}')

# ── 4. 组合出库右侧加引导注记
NOTES = [(664, 310, 'L1'), (784, 450, 'L2'), (664, 590, 'L3'), (708, 796, 'L4')]
for x, y, lane in NOTES:
    mark = f'    <text x="{x}" y="{y+4}" fill="#9ca3af" font-size="9.5" font-family="\'Geist Mono\',monospace">→ 退租及后续见 T1 专项</text>\n'
    # 插在该泳道组合出库节点块 </a> 之后（锚=泳道末尾连线删除点前的组合出库块）——直接按坐标行插
    anchor = re.search(rf'(    <a href="仓储作业/组合出库列表\.html">\s*<rect x="\d+" y="{y-28}"[\s\S]*?</a>\n)', src)
    assert anchor, (y, lane)
    src = src[:anchor.end(1)] + mark + src[anchor.end(1):]

# ── 5. footer / 头部 sub 叙事
rep("泳道内退租段压缩为占位节点）", "泳道止于出库，退租及后续统一在 T1）")
rep("<b>T1</b> 退租专项（四线退租汇总 · 09-04 拍板）", "<b>T1</b> 退租专项（四线退租及后续链路汇总 · 09-04 拍板）")

# ── 6. SRC_DATA t1 补泳道口径
rep("报废不再单列支'],", "报废不再单列支；泳道止于组合出库，退租后链路全部归 T1'],")

# ── 7. 自检
for tag in ["a", "g", "svg", "text"]:
    o = len(re.findall(rf"<{tag}[\s>]", src)); c = src.count(f"</{tag}>")
    assert o == c, f"<{tag}> 配平失败 {o} vs {c}"
assert src.count(">退租</text>") == 0                      # 泳道占位全删
assert src.count("→ 退租及后续见 T1 专项") == 4            # 四条引导注记
for probe in [">丢损赔偿</text>", ">租入归还</text>", ">租金应付</text>", ">多线应付</text>", ">在租台账</text>"]:
    assert probe not in src or src.count(probe) <= 1, (probe, src.count(probe))  # 泳道删后仅剩 T1/S 区或 0
# T1 完整性不回退
for probe in ["① 缺损核对 · 要么赔偿，要么继续", "② 完好 · 按资产来源", "整退 GHCK", "采购＋租金＋赔付", "散件循环 · 成组"]:
    assert probe in src, probe
F01.write_text(src, encoding="utf-8", newline="")
print("F01 泳道裁剪 OK")

# ── 8. A04 分母口径备注更新
j = A04.read_text(encoding="utf-8")
rep_j = ("步骤分母为该流程在 F01 v2.8 全展开泳道中的节点总数（v2.9 退租段压缩为占位，分母不变）",
         "步骤分母为该流程在 F01 v2.8 全展开泳道中的节点总数（v2.9 起泳道止于组合出库，退租后链路统一在 T1 专项泳道；分母按 v2.8 口径不变）")
assert j.count(rep_j[0]) == 1
j = j.replace(*rep_j)
import json; json.loads(j)
A04.write_text(j, encoding="utf-8", newline="")
print("A04 OK")
