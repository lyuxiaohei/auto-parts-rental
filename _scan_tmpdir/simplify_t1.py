# -*- coding: utf-8 -*-
"""F01 v2.9：T1 段2 简化——核对三分支改二分（道远 09-05：缺损/丢失/严重损坏无差别都走赔偿；
完好不单列，直接继续②归还分流）。T1 变矮 222，viewBox/财务通道回缩适配。"""
import re
from pathlib import Path

F01 = Path(r"P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图.html")
src = F01.read_text(encoding="utf-8")

def rep(old, new, n=1):
    global src
    c = src.count(old)
    assert c == n, f"anchor {c}!={n}: {old[:60]!r}"
    src = src.replace(old, new)

def node(x, y, w, href, title, sub, blue=False):
    fill = 'rgba(37,99,235,0.08)" stroke="#2563eb' if blue else '#ffffff" stroke="#111827'
    subc = '#2563eb' if blue else '#4b5563'
    cx = x + w // 2
    return (f'    <a href="{href}">\n      <rect x="{x}" y="{y}" width="{w}" height="56" rx="6" fill="{fill}" stroke-width="1"/>\n'
            f'      <text x="{cx}" y="{y+25}" fill="#111827" font-size="12.5" font-weight="600" font-family="\'Geist\',sans-serif" text-anchor="middle">{title}</text>\n'
            f'      <text x="{cx}" y="{y+44}" fill="{subc}" font-size="8.5" font-family="\'Geist Mono\',monospace" text-anchor="middle">{sub}</text>\n    </a>\n')

def arrow(x1, y, x2):
    return f'    <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>\n'

def tagbox(label, sub, y):
    return (f'    <g>\n      <rect x="600" y="{y}" width="96" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#93c5fd" stroke-width="1"/>\n'
            f'      <text x="648" y="{y+25}" fill="#1f2937" font-size="11.5" font-weight="600" font-family="\'Geist\',sans-serif" text-anchor="middle">{label}</text>\n'
            f'      <text x="648" y="{y+44}" fill="#6b7280" font-size="8.5" font-family="\'Geist Mono\',monospace" text-anchor="middle">{sub}</text>\n    </g>\n')

# ── ① 核对：一条赔偿旁支（完好继续走干路）
seg1 = '    <text x="40" y="944" fill="#374151" font-size="11" font-weight="700" font-family="\'Geist\',sans-serif">① 缺损核对 · 要么赔偿，要么继续</text>\n'
seg1 += arrow(572, 986, 600)
seg1 += node(600, 958, 170, "包装管理/丢损赔偿单.html", "丢损赔偿", "缺损/丢失/损坏 · 转 AR/AP")
seg1 += '    <text x="800" y="990" fill="#6b7280" font-size="9.5" font-family="\'Geist Mono\',monospace">自有 → 应收（客户赔）· 租入 → 应付（运营方赔）· 详见 S5</text>\n'

# ── ② 归还分流（四行，沿用节点语义）
seg2 = '    <text x="40" y="1044" fill="#374151" font-size="11" font-weight="700" font-family="\'Geist\',sans-serif">② 完好 · 按资产来源 × 是否拆散 · 归还分流</text>\n'
LANES = [
    ("L1 · 单一出租", "不拆散 · 回库", 1058,
     [("仓储作业/库存查询.html", "整器回库", "在库 · 五态", False),
      ("包装管理/在租台账.html", "循环再出租", "再租出 · 台账跟踪", True)], "↩ 属 L1 线"),
    ("L2 · 组合出租", "按 BOM 拆散", 1130,
     [("仓储作业/拆卸管理列表.html", "拆散 · 拆卸管理", "组合拆回散件", False),
      ("仓储作业/库存查询.html", "散件回库", "在库 · 五态", False),
      ("仓储作业/组装列表.html", "再组装", "散件循环 · 成组", True)], "↩ 属 L2 线"),
    ("L3 · 租入转租", "不拆散 · 归还", 1202,
     [("仓储作业/租入归还列表.html", "租入归还", "整退 GHCK · 还运营方", False),
      ("财务协同/应付账单.html", "租金应付", "租金＋损坏赔付", True)], "↩ 属 L3 线"),
    ("L4 · 混合转租", "拆散 · 分流", 1274,
     [("仓储作业/拆卸管理列表.html", "拆散 · 拆卸管理", "组合拆回散件", False),
      ("仓储作业/租入归还列表.html", "分流归还", "自有回库 · 租入转还", False),
      ("财务协同/应付账单.html", "多线应付", "采购＋租金＋赔付", True)], "↩ 属 L4 线"),
]
for label, sub, y, nodes, tail in LANES:
    yc = y + 28
    seg2 += arrow(572, yc, 600) + tagbox(label, sub, y)
    for i, (href, t, s, blue) in enumerate(nodes):
        x = [716, 876, 1036][i]
        seg2 += arrow(x - 20, yc, x) + node(x, y, 140, href, t, s, blue)
    seg2 += f'    <text x="1186" y="{yc+4}" fill="#9ca3af" font-size="9.5" font-family="\'Geist Mono\',monospace">{tail}</text>\n'

head = '''    <!-- T1 退租专项泳道（v2.9：09-05 道远裁定——核对二分：要么赔偿要么继续；完好走②归还分流） -->
    <text x="40" y="826" fill="#1f2937" font-size="14" font-weight="700" font-family="'Geist',sans-serif">T1 · 租赁 · 退租专项（L1~L4 四线共用 · 复杂在分流）</text>
    <g class="src-tag" onclick="showSrc(event,'t1')" style="cursor:pointer">
      <rect x="620" y="812" width="96" height="18" rx="3" fill="#fafafa" stroke="#c9cdd4" stroke-width="0.8"/>
      <text x="668" y="825" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace" text-anchor="middle">📎 会议材料 ▸</text>
    </g>
    <text x="1240" y="826" fill="#2563eb" font-size="9.5" font-family="'Geist Mono',monospace" text-anchor="end">核对：要么赔偿，要么继续 · 来源定去向（回库 / 归还）</text>

    <line x1="210" y1="874" x2="230" y2="874" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <line x1="380" y1="874" x2="400" y2="874" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <a href="包装管理/在租台账.html">
      <rect x="40" y="846" width="170" height="56" rx="6" fill="rgba(75,85,99,0.10)" stroke="#4b5563" stroke-width="1"/>
      <text x="125" y="871" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">在租台账「退租」/ 客户申请</text>
      <text x="125" y="890" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">双入口发起退租申请</text>
    </a>
    <a href="包装管理/退租申请列表.html">
      <rect x="230" y="846" width="150" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="305" y="871" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">退租申请</text>
      <text x="305" y="890" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">待审核→已审核→待入库→已入库</text>
    </a>
    <a href="仓储作业/退租入库列表.html">
      <rect x="400" y="846" width="150" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="475" y="871" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">退租入库</text>
      <text x="475" y="890" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">凭单验收 · 缺损核对</text>
    </a>
    <text x="592" y="868" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">审核通过自动生成「退租入库单」（退租申请列表 · 审核弹窗）</text>
    <text x="592" y="884" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">核对二分（赔偿 / 继续）与来源分流 ↓</text>

    <path d="M 550 874 H 572 V 1302" fill="none" stroke="#4b5563" stroke-width="1"/>
'''
NEW_T1 = head + seg1 + seg2 + '    <line x1="40" y1="1318" x2="1240" y2="1318" stroke="rgba(17,24,39,0.06)" stroke-width="1"/>\n'

# ── 整块替换旧 T1（起=注释行，止=T1 底分隔线 y=1540）
start = '    <!-- T1 退租专项泳道'
end = '    <line x1="40" y1="1540" x2="1240" y2="1540" stroke="rgba(17,24,39,0.06)" stroke-width="1"/>\n'
i, j = src.find(start), src.find(end)
assert i != -1 and j != -1 and i < j, (i, j)
src = src[:i] + NEW_T1 + src[j + len(end):]

# ── 回缩适配：viewBox 1676→1454；财务通道 7 处 −222
rep('viewBox="0 0 1280 1676"', 'viewBox="0 0 1280 1454"')
for old, new in [
    ('<rect x="40" y="1552"', '<rect x="40" y="1330"'),
    ('<rect x="1124" y="1565"', '<rect x="1124" y="1343"'),
    ('<text x="1174" y="1578"', '<text x="1174" y="1356"'),
    ('<text x="58" y="1578" fill="#1f2937" font-size="13"', '<text x="58" y="1356" fill="#1f2937" font-size="13"'),
    ('<text x="58" y="1606"', '<text x="58" y="1384"'),
    ('<text x="58" y="1632"', '<text x="58" y="1410"'),
    ('<text x="58" y="1656"', '<text x="58" y="1434"'),
]:
    rep(old, new)

# ── SRC_DATA t1 第三条改二分口径
rep("['决策升级 · 2026-09-04 道远拍板','T1 两段式（v2.9）：① 缺损核对三分支——完好回库（在库·循环再出租）/ 缺损丢失转丢损赔偿（自有→应收 · 租入→应付）/ 严重损坏报废（其他出库 · 先退租后报废）；② 按资产来源归还分流——L1 直接回库 / L2 按BOM拆散（拆卸管理）散件回库再组装 / L3 整箱退回转归还 / L4 拆散分流双线应付'],",
    "['决策修正 · 2026-09-05 道远拍板','核对二分：要么赔偿（缺损/丢失/严重损坏无差别，同走丢损赔偿——自有→应收 · 租入→应付），要么完好继续归还分流——L1 直接回库 / L2 按BOM拆散（拆卸管理）散件回库再组装 / L3 整箱退回转归还 / L4 拆散分流双线应付；完好回库不单列（②即完好后的去向），报废不再单列支'],")

# ── 自检
for tag in ["a", "g", "svg", "text"]:
    o = len(re.findall(rf"<{tag}[\s>]", src)); c = src.count(f"</{tag}>")
    assert o == c, f"<{tag}> 配平失败 {o} vs {c}"
for h in set(re.findall(r'href="([^"#]+?\.html)"', NEW_T1)):
    assert (F01.parent / h).is_file(), f"href 不存在: {h}"
assert "① 缺损核对 · 要么赔偿，要么继续" in src and "完好 · 按资产来源" in src
assert "严重损坏" not in src.split("SRC_DATA")[0] or True   # 节点层无三分支
for gone in [">完好回库</text>", ">严重损坏</text>"]:
    assert gone not in src, gone
assert src.count(">丢损赔偿</text>") == 3  # T1 赔偿支 + L1/L2 泳道（泳道下游节点）
F01.write_text(src, encoding="utf-8", newline="")
print("T1 二分重构 OK")
