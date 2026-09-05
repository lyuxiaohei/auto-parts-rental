# -*- coding: utf-8 -*-
"""F01 v2.9: 在 L4 泳道后插入 T1 退租专项泳道（公共入口+四分支），财务通道下移 432px。
精确替换式脚本：每处替换前 assert 锚点命中数；末尾做标签配平与 href 目标存在性检查。"""
import re
from pathlib import Path

P = Path(r"P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图.html")
src = P.read_text(encoding="utf-8")
orig_len = len(src)

def rep(old, new, n=1):
    global src
    c = src.count(old)
    assert c == n, f"anchor count {c} != {n}: {old[:60]!r}"
    src = src.replace(old, new)

# ── 1. 主线 SVG viewBox 加高 936 → 1368（Δ=432）
rep('<svg viewBox="0 0 1280 936"', '<svg viewBox="0 0 1280 1368"')

# ── 2. 财务通道块整体 y+432
rep('y="812" width="1200" height="116"', 'y="1244" width="1200" height="116"')
rep('<rect x="1124" y="825"', '<rect x="1124" y="1257"')          # fin src-tag rect
rep('<text x="1174" y="838"', '<text x="1174" y="1270"')          # fin src-tag text
rep('<text x="58" y="838" fill="#1f2937" font-size="13"', '<text x="58" y="1270" fill="#1f2937" font-size="13"')  # 财务通道标题
rep('<text x="58" y="866"', '<text x="58" y="1298"')
rep('<text x="58" y="892"', '<text x="58" y="1324"')
rep('<text x="58" y="916"', '<text x="58" y="1348"')

# ── 3. T1 泳道块（插在财务通道底板 rect 之前）
def lane(label, sub, y_top, nodes, tail):
    """一行分支：分流键标签(600) + 节点A(716) + 节点B(886) + 行尾注记。y_top=节点顶，中心=y_top+28"""
    yc = y_top + 28
    A, B = nodes  # (href, title, sub, blue)
    bA = 'rgba(37,99,235,0.08)" stroke="#2563eb' if A[3] else '#ffffff" stroke="#111827'
    bB = 'rgba(37,99,235,0.08)" stroke="#2563eb' if B[3] else '#ffffff" stroke="#111827'
    subA = A[2].replace('＋', '＋')
    return f'''    <g>
      <rect x="600" y="{y_top}" width="96" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#93c5fd" stroke-width="1"/>
      <text x="648" y="{y_top+25}" fill="#1f2937" font-size="11.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">{label}</text>
      <text x="648" y="{y_top+44}" fill="#6b7280" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">{sub}</text>
    </g>
    <line x1="696" y1="{yc}" x2="716" y2="{yc}" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <a href="{A[0]}">
      <rect x="716" y="{y_top}" width="150" height="56" rx="6" fill="{bA}" stroke-width="1"/>
      <text x="791" y="{y_top+25}" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">{A[1]}</text>
      <text x="791" y="{y_top+44}" fill="{'#2563eb' if A[3] else '#4b5563'}" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">{subA}</text>
    </a>
    <line x1="866" y1="{yc}" x2="886" y2="{yc}" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <a href="{B[0]}">
      <rect x="886" y="{y_top}" width="150" height="56" rx="6" fill="{bB}" stroke-width="1"/>
      <text x="961" y="{y_top+25}" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">{B[1]}</text>
      <text x="961" y="{y_top+44}" fill="{'#2563eb' if B[3] else '#4b5563'}" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">{B[2]}</text>
    </a>
    <text x="1046" y="{yc+4}" fill="#9ca3af" font-size="9.5" font-family="'Geist Mono',monospace">{tail}</text>
'''

T1 = f'''
    <!-- T1 退租专项泳道（v2.9 新增：09-04 道远 3:49 提出、王琳总确认"退租入库拆出来"） -->
    <text x="40" y="826" fill="#1f2937" font-size="14" font-weight="700" font-family="'Geist',sans-serif">T1 · 租赁 · 退租专项（L1~L4 四线共用 · 复杂在分流）</text>
    <g class="src-tag" onclick="showSrc(event,'t1')" style="cursor:pointer">
      <rect x="620" y="812" width="96" height="18" rx="3" fill="#fafafa" stroke="#c9cdd4" stroke-width="0.8"/>
      <text x="668" y="825" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace" text-anchor="middle">📎 会议材料 ▸</text>
    </g>
    <text x="1240" y="826" fill="#2563eb" font-size="9.5" font-family="'Geist Mono',monospace" text-anchor="end">缺损计赔 → <a href="包装管理/丢损赔偿单.html" fill="#2563eb">丢损赔偿（S5）</a> · 租入侧 → <a href="财务协同/应付账单.html" fill="#2563eb">应付账单</a></text>

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
    <text x="570" y="868" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">审核通过自动生成「退租入库单」（退租申请列表 · 审核弹窗）</text>
    <text x="570" y="884" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">↓ 按资产来源 × 是否拆散，分流四条链路</text>

    <path d="M 550 874 H 572 V 1174" fill="none" stroke="#4b5563" stroke-width="1"/>
    <line x1="572" y1="958" x2="600" y2="958" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <line x1="572" y1="1030" x2="600" y2="1030" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <line x1="572" y1="1102" x2="600" y2="1102" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <line x1="572" y1="1174" x2="600" y2="1174" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
{lane("L1 · 单一出租", "自有 · 直接回库", 930,
      [("包装管理/丢损赔偿单.html", "丢损赔偿", "缺损核对 · 转应收", False),
       ("包装管理/在租台账.html", "在租台账核销", "回库 · 循环再出租", True)], "↩ 详见 L1 泳道")}
{lane("L2 · 组合出租", "自有组合 · 按BOM拆散", 1002,
      [("包装管理/丢损赔偿单.html", "丢损赔偿", "拆散 · 缺损转应收", False),
       ("仓储作业/组装列表.html", "散件回库 · 再组装", "拆回A/B/C · 循环", True)], "↩ 详见 L2 泳道")}
{lane("L3 · 租入转租", "租入 · 整箱退回", 1074,
      [("仓储作业/租入归还列表.html", "租入归还", "整退 GHCK · 还运营方", False),
       ("财务协同/应付账单.html", "租金应付", "租金＋损坏赔付", True)], "↩ 详见 L3 泳道")}
{lane("L4 · 混合转租", "自购＋租入 · 拆散分流", 1146,
      [("仓储作业/租入归还列表.html", "分流归还", "自有回库 · 租入转还", False),
       ("财务协同/应付账单.html", "多线应付", "采购＋租金＋赔付", True)], "↩ 详见 L4 泳道")}
    <text x="40" y="1214" fill="#9ca3af" font-size="9.5" font-family="'Geist',sans-serif">报废 ＝ 退租完成后的资产核销路径（在租器具须先办理退租）→ <a href="仓储作业/其他出库列表.html" fill="#2563eb">其他出库（S2）</a> · 缺损/丢失计赔口径见 <a href="包装管理/丢损赔偿单.html" fill="#2563eb">丢损赔偿单（S5）</a></text>
    <line x1="40" y1="1232" x2="1240" y2="1232" stroke="rgba(17,24,39,0.06)" stroke-width="1"/>
'''

anchor_fin = '    <rect x="40" y="1244" width="1200" height="116"'
assert src.count(anchor_fin) == 1
src = src.replace(anchor_fin, T1 + anchor_fin)

# ── 4. SRC_DATA 增加 t1（插在 fin 之前）
T1_SRC = '''  t1: {head:'T1 · 退租专项 · 会议依据与拍板', items:[
    ['第3次沟通前内部沟通 [音频转写] · 道远 3:49（王琳总确认）','"那这个退租入库给他拆出来……主要复杂就在于要退租"——退租按资产来源×是否拆散分 4 链路：L1 直接回库 / L2 按BOM拆散 / L3 整箱退回 / L4 拆散分流'],
    ['第2次沟通 [会后补充] · 袁丽晶','"退租明细入库，按照ABC单独的包材入库（而不是组合入库）"——L2/L4 拆散入库依据'],
    ['决策升级 · 2026-09-04 道远拍板','T1 泳道（v2.9）：四线退租共用「退租申请→退租入库」入口，审核后按分流键四分支；报废＝退租后资产核销（先退租后报废）'],
  ]},
'''
rep("  fin: {head:'财务通道 · 会议依据', items:[", T1_SRC + "  fin: {head:'财务通道 · 会议依据', items:[")

# ── 5. 版本与叙事（v2.8 → v2.9，5 条主线 → 6 条）
rep("（v2.8）</title>", "（v2.9）</title>")
rep("P3-R01-F01 · v2.8 原型业务流程导航", "P3-R01-F01 · v2.9 原型业务流程导航")
rep("包装租赁管理后台原型 v2.8 · <b>45</b> 个页面 · 5 条业务流程泳道（第2次沟通纪要）",
    "包装租赁管理后台原型 v2.9 · <b>45</b> 个页面 · 6 条业务流程泳道（第2次沟通纪要＋09-04 内部沟通）")
rep("<b>L4</b> 混合转租（2026-09-04 拍板第一期实现）· <b>7</b> 条支线",
    "<b>L4</b> 混合转租（2026-09-04 拍板第一期实现）· <b>T1</b> 退租专项（四线退租汇总 · 09-04 拍板）· <b>7</b> 条支线")
rep("<footer>P3-R01-F01 · v2.8 · 2026-09-04", "<footer>P3-R01-F01 · v2.9 · 2026-09-04")
rep("45 页 / 5 条主线泳道（B1/L1/L2/L3/L4 全部第一期实现·L3/L4 为 2026-09-04 拍板升级）",
    "45 页 / 6 条主线泳道（B1/L1/L2/L3/L4 全部第一期实现·L3/L4 为 2026-09-04 拍板升级·T1 退租专项汇总四线）")

# ── 6. 自检：标签配平（全文）
for a, b in [("<a ", "</a>"), ("<a\n", "</a>"), ("<g", "</g>"), ("<svg", "</svg>"), ("<text", "</text>"), ("<line", "</line>")]:
    pass
opens = len(re.findall(r"<a[\s>]", src)); closes = src.count("</a>")
assert opens == closes, f"<a> 配平失败 {opens} vs {closes}"
for tag in ["g", "svg", "text"]:
    o = len(re.findall(rf"<{tag}[\s>]", src)); c = src.count(f"</{tag}>")
    assert o == c, f"<{tag}> 配平失败 {o} vs {c}"
assert src.count("<script") == src.count("</script>") and src.count("<style") == src.count("</style>")

# ── 7. 自检：T1 块内 href 目标文件全部存在
base = P.parent
hrefs = set(re.findall(r'href="([^"#]+?\.html)"', T1))
for h in sorted(hrefs):
    assert (base / h).is_file(), f"href 目标不存在: {h}"
print("href targets OK:", len(hrefs))

# ── 8. 自检：v2.8 残留 0、新锚点就位
assert "v2.8" not in src, "v2.8 残留"
for probe in ["T1 · 租赁 · 退租专项", "showSrc(event,'t1')", "t1: {head:", 'viewBox="0 0 1280 1368"']:
    assert probe in src, f"缺: {probe}"
assert src.count(">退租申请</text>") == 5  # L1-L4 四泳道主标 + T1 公共入口主标（副标"…退租申请"不计）

P.write_text(src, encoding="utf-8", newline="")
print(f"OK  {orig_len} -> {len(src)} bytes (+{len(src)-orig_len})")
