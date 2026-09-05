# -*- coding: utf-8 -*-
"""F01 v2.9：财务通道缩略板块 → 节点化具体流程（应收/应付双行）。
同时修 T1 底分隔线 1374 穿 L4 节点（底 1386）的 12px 错位 → 移到 1400。"""
import re
from pathlib import Path

F01 = Path(r"P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图.html")
src = F01.read_text(encoding="utf-8")

def rep(old, new, n=1):
    global src
    c = src.count(old)
    assert c == n, f"anchor {c}!={n}: {old[:60]!r}"
    src = src.replace(old, new)

def sub1(pat, repl, label):
    global src
    new, n = re.subn(pat, repl, src)
    assert n == 1, f"[{label}] {n} != 1"
    src = new

def node(x, y, w, href, t, s, gray=False):
    fill = 'rgba(75,85,99,0.10)" stroke="#4b5563' if gray else '#ffffff" stroke="#111827'
    subc = '#4b5563' if gray else '#4b5563'
    cx = x + w // 2
    return (f'    <a href="{href}">\n      <rect x="{x}" y="{y}" width="{w}" height="56" rx="6" fill="{fill}" stroke-width="1"/>\n'
            f'      <text x="{cx}" y="{y+25}" fill="#111827" font-size="12.5" font-weight="600" font-family="\'Geist\',sans-serif" text-anchor="middle">{t}</text>\n'
            f'      <text x="{cx}" y="{y+44}" fill="{subc}" font-size="8.5" font-family="\'Geist Mono\',monospace" text-anchor="middle">{s}</text>\n    </a>\n')

def arrow(x1, y, x2):
    return f'    <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>\n'

# ── 1. 删旧财务通道块（底板/标题/src-tag/三行文字）
sub1(r'<rect x="40" y="1386" width="1200" height="116"[^/]*/>\n\s*', '', '底板')
sub1(r'<text x="58" y="1412" fill="#1f2937" font-size="13"[^>]*>财务通道[\s\S]*?</text>\n\s*', '', '标题')
sub1(r'<g class="src-tag" onclick="showSrc\(event,\'fin\'\)"[\s\S]*?</g>\n\s*', '', 'fin src-tag')
for y, head in [(1440, '应收侧'), (1466, '应付侧'), (1490, '押金')]:
    sub1(rf'<text x="58" y="{y}"[^>]*>{head}[\s\S]*?</text>\n\s*', '', f'文字行 y={y}')

# ── 2. 新财务泳道（节点化双行），插在 T1 底分隔线之前；分隔线 1374→1400
FIN = f'''    <text x="40" y="1424" fill="#1f2937" font-size="13" font-weight="700" font-family="'Geist',sans-serif">财务通道 · 5 条线共用（应收 ＋ 应付）</text>
    <g class="src-tag" onclick="showSrc(event,'fin')" style="cursor:pointer">
      <rect x="1124" y="1410" width="100" height="18" rx="3" fill="#fafafa" stroke="#c9cdd4" stroke-width="0.8"/>
      <text x="1174" y="1423" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace" text-anchor="middle">📎 会议材料 ▸</text>
    </g>
{arrow(320, 1466, 336)}{node(40, 1438, 280, "仓储作业/组合出库列表.html", "应收来源", "B1 销售费 · L1~L4 租赁费 · 丢损赔偿（对客户）", gray=True)}{node(336, 1438, 140, "财务协同/应收账单.html", "应收账单", "三类应收自动汇总")}{arrow(476, 1466, 492)}{node(492, 1438, 140, "财务协同/开票登记.html", "开票登记", "发票登记 · 上传")}{arrow(632, 1466, 648)}{node(648, 1438, 140, "财务协同/回款登记.html", "回款登记", "回款录入 · 待审核")}{arrow(788, 1466, 804)}{node(804, 1438, 140, "财务协同/银行水单核销.html", "收款核销", "水单勾对 · 部分/撤销")}{arrow(320, 1542, 336)}{node(40, 1514, 280, "采购管理/租入单列表.html", "应付来源", "采购应付 · 租金应付（按月）· 赔付应付", gray=True)}{node(336, 1514, 140, "财务协同/应付账单.html", "应付账单", "三类应付汇总")}{arrow(476, 1542, 492)}{node(492, 1514, 140, "财务协同/付款登记.html", "付款登记", "付款确认 · 待审核")}
    <text x="660" y="1546" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">付款确认 <a href="财务协同/弹窗/付款确认.html" fill="#2563eb">弹窗独立打开</a> · 租金应付 L3/L4 已实现（租入单按月生成）</text>
    <text x="960" y="1470" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">按客户/供应商汇总 · 同一账单可部分核销</text>
    <text x="40" y="1594" fill="#9ca3af" font-size="8.5" font-family="'Geist',sans-serif">押金：租赁单现有押金字段（原型自带）；收退规则属商务口径待客户确认（计费单价/押金/缺损标准，见 P1-R01 待确认项）——非会议提出的需求</text>
'''
rep('    <line x1="40" y1="1374" x2="1240" y2="1374" stroke="rgba(17,24,39,0.06)" stroke-width="1"/>',
    FIN + '    <line x1="40" y1="1400" x2="1240" y2="1400" stroke="rgba(17,24,39,0.06)" stroke-width="1"/>')

# ── 3. viewBox 1510→1618
rep('viewBox="0 0 1280 1510"', 'viewBox="0 0 1280 1618"')

# ── 4. SRC_DATA fin 补画法
rep("可以同步到财务模块\"'],",
    "可以同步到财务模块\"——v2.9 通道节点化：应收/应付双行具体流程],")

# ── 5. 自检
for tag in ["a", "g", "svg", "text"]:
    o = len(re.findall(rf"<{tag}[\s>]", src)); c = src.count(f"</{tag}>")
    assert o == c, f"<{tag}> 配平失败 {o} vs {c}"
for h in set(re.findall(r'href="([^"#]+?\.html)"', FIN)):
    assert (F01.parent / h).is_file(), f"href 不存在: {h}"
for probe in ["应收来源", "应收账单", "开票登记", "回款登记", "收款核销", "应付来源", "应付账单", "付款登记", "押金：租赁单现有押金字段"]:
    assert probe in src, probe
F01.write_text(src, encoding="utf-8", newline="")
print("财务泳道节点化 OK")
