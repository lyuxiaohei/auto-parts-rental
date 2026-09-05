# -*- coding: utf-8 -*-
"""F01 v2.9：L4 泳道改双线并行画法——上行自购线（采购订单→采购入库）、下行租入线（租入单→租入入库，
两线汇入混合组装；租入入库显式成节点，不再合并隐含）。T1 整体下移 56，财务通道/viewBox 适配。"""
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

def sub1(pat, repl, label):
    global src
    new, n = re.subn(pat, repl, src)
    assert n == 1, f"[{label}] 命中 {n} != 1"
    src = new

# ── 1. 删旧 L4：9 节点块（y=702）+ 8 条连线（y=730）
for x in [40, 164, 288, 412, 536, 660, 784, 1032, 1156]:
    sub1(rf'<a href="[^"]+">\s*<rect x="{x}" y="702"[\s\S]*?</a>\n\s*', '', f'L4 节点 x={x}')
src, n = re.subn(r'<line x1="\d+" y1="730" x2="\d+" y2="730" stroke="#4b5563" stroke-width="1" marker-end="url\(#arr\)"/>\n\s*', '', src)
assert n == 8, f"L4 连线 {n} != 8"

# ── 2. 新 L4 双线块（插在 T1 注释行之前）
def n4(x, y, href, t, s, blue=False, dash=False):
    fill = 'rgba(37,99,235,0.08)" stroke="#2563eb' if blue else ('#fafafa" stroke="#6b7280' if dash else '#ffffff" stroke="#111827')
    extra = ' stroke-dasharray="5,4"' if dash else ''
    subc = '#2563eb' if blue else ('#6b7280' if dash else '#4b5563')
    cx = x + 56
    return (f'    <a href="{href}">\n      <rect x="{x}" y="{y}" width="112" height="56" rx="6" fill="{fill}" stroke-width="1"{extra}/>\n'
            f'      <text x="{cx}" y="{y+25}" fill="#111827" font-size="12.5" font-weight="600" font-family="\'Geist\',sans-serif" text-anchor="middle">{t}</text>\n'
            f'      <text x="{cx}" y="{y+44}" fill="{subc}" font-size="8.5" font-family="\'Geist Mono\',monospace" text-anchor="middle">{s}</text>\n    </a>\n')

L4 = f'''    <text x="40" y="694" fill="#9ca3af" font-size="8.5" font-family="'Geist Mono',monospace">自购线 ↘</text>
    <text x="40" y="762" fill="#9ca3af" font-size="8.5" font-family="'Geist Mono',monospace">租入线 ↗</text>
    <line x1="152" y1="728" x2="164" y2="728" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <line x1="152" y1="796" x2="164" y2="796" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
{n4(40, 700, "采购管理/采购订单列表.html", "采购订单", "自购辅材·器具类")}{n4(164, 700, "仓储作业/采购入库列表.html", "采购入库", "凭单验收 · 入库")}
{n4(40, 768, "采购管理/租入单列表.html", "租入单", "租入大箱/围板箱")}{n4(164, 768, "仓储作业/租入入库列表.html", "租入入库", "租入资产入库")}
    <path d="M 276 728 H 306 V 788 H 336" fill="none" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <path d="M 276 796 H 336" fill="none" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
{n4(336, 768, "仓储作业/组装列表.html", "混合组装", "自购+租入→C")}{n4(460, 768, "包装管理/租赁单列表.html", "租赁单", "组合C出租")}{n4(584, 768, "仓储作业/组合出库列表.html", "组合出库", "出库确认")}
''' + '''    <a href="包装管理/退租申请列表.html">
      <rect x="708" y="768" width="236" height="56" rx="6" fill="#fafafa" stroke="#6b7280" stroke-width="1" stroke-dasharray="5,4"/>
      <text x="826" y="793" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">退租</text>
      <text x="826" y="812" fill="#6b7280" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">拆散分流 · 详见 T1 专项</text>
    </a>
''' + f'''{n4(956, 768, "仓储作业/租入归还列表.html", "分流归还", "自购回库·租入归还")}{n4(1080, 768, "财务协同/应付账单.html", "多线应付", "采购+租金+赔付", blue=True)}
    <line x1="448" y1="796" x2="460" y2="796" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <line x1="572" y1="796" x2="584" y2="796" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <line x1="696" y1="796" x2="708" y2="796" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <line x1="944" y1="796" x2="956" y2="796" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <line x1="1068" y1="796" x2="1080" y2="796" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
'''
t1_anchor = '    <!-- T1 退租专项泳道'
rep(t1_anchor, L4 + t1_anchor)

# ── 3. L4/T1 分隔线 800→856
rep('<line x1="40" y1="800" x2="1240" y2="800"', '<line x1="40" y1="856" x2="1240" y2="856"')

# ── 4. T1 块整体 +56（y="n" 与干路 path）
i = src.find(t1_anchor)
j = src.find('<line x1="40" y1="1484"', i)
assert i != -1 and j != -1
block = src[i:j]
block = re.sub(r'y="(\d+)"', lambda m: f'y="{int(m.group(1)) + 56}"', block)
block = block.replace('M 550 874 H 572 V 1434', 'M 550 930 H 572 V 1490')
src = src[:i] + block + src[j:]
rep('<line x1="40" y1="1484" x2="1240" y2="1484"', '<line x1="40" y1="1540" x2="1240" y2="1540"')

# ── 5. viewBox 1620→1676；财务通道 7 处 +56
rep('viewBox="0 0 1280 1620"', 'viewBox="0 0 1280 1676"')
for old, new in [
    ('<rect x="40" y="1496"', '<rect x="40" y="1552"'),
    ('<rect x="1124" y="1509"', '<rect x="1124" y="1565"'),
    ('<text x="1174" y="1522"', '<text x="1174" y="1578"'),
    ('<text x="58" y="1522" fill="#1f2937" font-size="13"', '<text x="58" y="1578" fill="#1f2937" font-size="13"'),
    ('<text x="58" y="1550"', '<text x="58" y="1606"'),
    ('<text x="58" y="1576"', '<text x="58" y="1632"'),
    ('<text x="58" y="1600"', '<text x="58" y="1656"'),
]:
    rep(old, new)

# ── 6. SRC_DATA l4 第三条补画法
rep("['决策升级 · 2026-09-04 道远拍板','L4 第一期闭环：自购+租入混合组装；租入单据独立成单，退租拆散按来源分流归还；应付侧＝采购应付＋租金应付双线'],",
    "['决策升级 · 2026-09-04 道远拍板','L4 第一期闭环：自购+租入混合组装；租入单据独立成单，退租拆散按来源分流归还；应付侧＝采购应付＋租金应付双线'],\n    ['画法修正 · 2026-09-05 道远指出','自购与租入为并行来料非串行（v2.9 修正双线画法）；租入入库显式成节点，不再合并隐含于租入单'],")

# ── 7. 自检
for tag in ["a", "g", "svg", "text"]:
    o = len(re.findall(rf"<{tag}[\s>]", src)); c = src.count(f"</{tag}>")
    assert o == c, f"<{tag}> 配平失败 {o} vs {c}"
for h in set(re.findall(r'href="([^"#]+?\.html)"', L4)):
    assert (F01.parent / h).is_file(), f"href 不存在: {h}"
assert src.count(">租入入库</text>") == 2   # L3 泳道 + L4 新增
assert src.count(">退租</text>") == 4       # 4 泳道占位不变
for probe in ["自购线 ↘", "租入线 ↗", ">混合组装</text>"]:
    assert probe in src, probe
F01.write_text(src, encoding="utf-8", newline="")
print("F01 OK")

# ── 8. A04：title/note 两处（pin 结构不动）
j = A04.read_text(encoding="utf-8")
for old, new in [
    ('"title": "L4 · 租入入库（泳道隐含环节）"', '"title": "L4 · 租入入库"'),
    ('"note": "租入大箱入库，关联 RZD-20260815-005；F01 L4 泳道将租入入库合并在租入单环节。"',
     '"note": "租入大箱入库，关联 RZD-20260815-005；F01 v2.9 起 L4 泳道双线画法：租入库显式成节点，与自购线并行来料汇入混合组装。"'),
]:
    assert j.count(old) == 1, old[:50]
    j = j.replace(old, new)
import json; json.loads(j)
A04.write_text(j, encoding="utf-8", newline="")
print("A04 OK（json 合法）")
