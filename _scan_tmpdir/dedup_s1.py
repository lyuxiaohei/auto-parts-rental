# -*- coding: utf-8 -*-
"""F01 v2.9 冗余处理（入口节点原则）：
① B1 销售线尾 3 节点（应收账单/开票/收款核销）→ 1 个灰底财务入口节点
② S1 采购应付支线整条删，S2-S7 上移 120，支线 SVG 840→720（编号留洞不重排）
位移用全套坐标正则（y=/y1=/y2=），含 line-vs-rect 对齐与遮挡验证。"""
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
    assert n == 1, f"[{label}] {n} != 1"
    src = new

# ── 1. B1 销售线尾：删 3 节点 + 2 连线，插 1 个财务入口节点
for x in [384, 556, 728]:
    sub1(rf'<a href="财务协同/[^"]+">\s*<rect x="{x}" y="168"[\s\S]*?</a>\n\s*', '', f'B1 fin 节点 x={x}')
for x1, x2 in [(534, 556), (706, 728)]:
    sub1(rf'<line x1="{x1}" y1="196" x2="{x2}" y2="196"[^/]*/>\n\s*', '', f'B1 连线 {x1}->{x2}')
ENTRY = '''    <a href="财务协同/应收账单.html">
      <rect x="384" y="168" width="150" height="56" rx="6" fill="rgba(75,85,99,0.10)" stroke="#4b5563" stroke-width="1"/>
      <text x="459" y="193" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">应收账单</text>
      <text x="459" y="212" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">→ 财务通道 · 销售费自动汇总</text>
    </a>
'''
sub1(r'(<line x1="362" y1="196" x2="384" y2="196"[^/]*/>\n)', r'\1' + ENTRY.replace("\\", "\\\\"), 'B1 入口节点插入')

# ── 2. S1 整条删（标题行起到 S2 标题行前）
i = src.find('<text x="40" y="42" fill="#1f2937" font-size="14" font-weight="700" font-family="\'Geist\',sans-serif">S1 · 采购应付</text>')
j = src.find('<text x="40" y="162" fill="#1f2937" font-size="14" font-weight="700" font-family="\'Geist\',sans-serif">S2 · 库存运营</text>')
assert i != -1 and j != -1 and i < j, (i, j)
src = src[:i] + src[j:]

# ── 3. S2-S7 上移 120（支线 SVG 内 S2 标题起至 </svg>）
k = src.find('<text x="40" y="162" fill="#1f2937" font-size="14" font-weight="700" font-family="\'Geist\',sans-serif">S2 · 库存运营</text>')
m = src.find('</svg>', k)
assert k != -1 and m != -1
block = src[k:m]
block = re.sub(r'y="(\d+)"', lambda mm: f'y="{int(mm.group(1)) - 120}"', block)
block = re.sub(r'y1="(\d+)"', lambda mm: f'y1="{int(mm.group(1)) - 120}"', block)
block = re.sub(r'y2="(\d+)"', lambda mm: f'y2="{int(mm.group(1)) - 120}"', block)
src = src[:k] + block + src[m:]
rep('<svg viewBox="0 0 1280 840"', '<svg viewBox="0 0 1280 720"')

# ── 4. 叙事同步
rep("采购应付 · 库存运营 · 项目经营 · 系统支撑 · 赔偿转单据 · 录单页与台账 · 审核与待办 · 灰底",
    "库存运营 · 项目经营 · 系统支撑 · 赔偿转单据 · 录单页与台账 · 审核与待办（S1 采购应付已并入财务通道）· 灰底")
rep("+ 7 条支线", "+ 6 条支线（S1 采购应付已并入财务通道）")
rep("<b>7</b> 条支线", "<b>6</b> 条支线")

# ── 5. 自检
for tag in ["a", "g", "svg", "text"]:
    o = len(re.findall(rf"<{tag}[\s>]", src)); c = src.count(f"</{tag}>")
    assert o == c, f"<{tag}> 配平失败 {o} vs {c}"
assert "S1 · 采购应付" not in src and "S2 · 库存运营" in src and "S7 · 审核与待办" in src
assert "→ 财务通道 · 销售费自动汇总" in src
assert src.count(">应收账单</text>") == 2   # B1 入口 + 财务应收行（S5 的是"应收账单（客户赔付）"）
F01.write_text(src, encoding="utf-8", newline="")
print("F01 OK")

# ── 6. A04：desc + 2 个 pin title + 1 个 pin note（单号 AR-...-S1 不碰）
j2 = A04.read_text(encoding="utf-8")
for old, new in [
    ("（B1/L1/L2/L3/L4 主线、S1~S7 支线）", "（B1/L1/L2/L3/L4/T1 主线、S2~S7 支线——S1 采购应付已并入财务通道）"),
    ('"title": "S1 · 采购应付"', '"title": "财务通道 · 采购应付"'),
    ('"note": "S1 采购应付支线：采购入库 → 应付账单 → 付款登记（买卖线与器具采购共用）。"',
     '"note": "采购应付：采购入库 → 应付账单 → 付款登记（财务通道应付行；v2.9 起 S1 支线并入）。"'),
    ('"title": "S1 · 付款登记"', '"title": "财务通道 · 付款登记"'),
]:
    assert j2.count(old) == 1, old[:50]
    j2 = j2.replace(old, new)
assert "AR-2026-09-PRJ2601-S1" in j2  # 单号未误伤
import json; json.loads(j2)
A04.write_text(j2, encoding="utf-8", newline="")
print("A04 OK（单号 AR-...-S1 未动）")
