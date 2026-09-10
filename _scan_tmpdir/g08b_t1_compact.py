# -*- coding: utf-8 -*-
"""G08 续改: T1 紧凑型重排——节点间距统一 20px、四行等距 20px、①②标签行内化、
客户转租/客户虚拟仓两注记下移口径注记区；T2 块 -128、财务通道区 -96；viewBox 1762→1666
"""
import re
from pathlib import Path

P = Path(r'P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图.html')
s = P.read_text(encoding='utf-8')

NEW_T1 = '''    <line x1="210" y1="930" x2="230" y2="930" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <a href="租赁管理/租赁单列表.html">
      <rect x="40" y="902" width="170" height="56" rx="6" fill="rgba(75,85,99,0.10)" stroke="#4b5563" stroke-width="1"/>
      <text x="125" y="927" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁单「退租」</text>
      <text x="125" y="946" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">客户退回 · 直接录入退租入库</text>
    </a>
    <a href="租赁管理/退租入库列表.html">
      <rect x="230" y="902" width="170" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="315" y="927" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">退租入库</text>
      <text x="315" y="946" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">客户退租统一入口 · 验收+缺损核对</text>
    </a>
    <text x="430" y="924" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">退租无申请单：客户退回后直接录入退租入库单 · 入库仅更新库存（2026-09-08 会议）</text>
    <text x="430" y="940" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">核对二分（赔偿 / 继续）· 完好后按资产归属分流 ↓</text>
    <path d="M 400 930 H 420 V 1158" fill="none" stroke="#4b5563" stroke-width="1"/>
    <text x="40" y="1010" fill="#374151" font-size="11" font-weight="700" font-family="'Geist',sans-serif">① 缺损核对 · 要么赔偿，要么继续</text>
    <line x1="420" y1="1006" x2="440" y2="1006" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <a href="财务协同/应付账单.html">
      <rect x="440" y="978" width="170" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="525" y="1003" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">直接转应收/应付</text>
      <text x="525" y="1022" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">缺损/丢失/损坏 · 转 AR/AP</text>
    </a>
    <text x="640" y="1010" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">自有 → 应收（客户赔）· 租入 → 应付（供应商赔）· 无赔偿单直接建账单（费用分类）· 详见 S4</text>
    <text x="40" y="1086" fill="#374151" font-size="11" font-weight="700" font-family="'Geist',sans-serif">② 完好 · 自有回库（是否拆散＝退租入库的记录粒度 · 非流程分支）</text>
    <line x1="420" y1="1082" x2="440" y2="1082" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <g>
      <rect x="440" y="1054" width="96" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#93c5fd" stroke-width="1"/>
      <text x="488" y="1079" fill="#1f2937" font-size="11.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">自有资产</text>
      <text x="488" y="1098" fill="#6b7280" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">回库 · 按产品入库</text>
    </g>
    <line x1="536" y1="1082" x2="556" y2="1082" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <a href="仓储作业/库存查询.html">
      <rect x="556" y="1054" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="626" y="1079" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">在库 · 五态</text>
      <text x="626" y="1098" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">整器或拆后零件 · 统一按单一产品记录</text>
    </a>
    <line x1="696" y1="1082" x2="716" y2="1082" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <a href="租赁管理/租赁单列表.html">
      <rect x="716" y="1054" width="140" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="786" y="1079" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">循环再出租</text>
      <text x="786" y="1098" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">再租出 · 退回进度跟踪</text>
    </a>
    <text x="1186" y="1086" fill="#9ca3af" font-size="9.5" font-family="'Geist Mono',monospace">↩ 自有（L1/L2）</text>
    <text x="40" y="1162" fill="#374151" font-size="11" font-weight="700" font-family="'Geist',sans-serif">② 完好 · 租入回库（回库后交棒 T2）</text>
    <line x1="420" y1="1158" x2="440" y2="1158" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <g>
      <rect x="440" y="1130" width="96" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#93c5fd" stroke-width="1"/>
      <text x="488" y="1155" fill="#1f2937" font-size="11.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租入资产</text>
      <text x="488" y="1174" fill="#6b7280" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">回库 · 租入在库</text>
    </g>
    <line x1="536" y1="1158" x2="556" y2="1158" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <a href="仓储作业/库存查询.html">
      <rect x="556" y="1130" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="626" y="1155" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租入在库</text>
      <text x="626" y="1174" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">客户态 → 租入在库（待归还）</text>
    </a>
    <line x1="696" y1="1158" x2="716" y2="1158" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <a href="租赁管理/租入归还列表.html">
      <rect x="716" y="1130" width="140" height="56" rx="6" fill="rgba(75,85,99,0.10)" stroke="#4b5563" stroke-width="1"/>
      <text x="786" y="1155" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">⇢ T2 · 租入归还</text>
      <text x="786" y="1174" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">归还供应商 · 见 T2</text>
    </a>
    <text x="1186" y="1162" fill="#9ca3af" font-size="9.5" font-family="'Geist Mono',monospace">↩ 租入（L3/L4）</text>'''

# ── ① 锚点切取旧 T1 块（入口连线 → ↩租入注记），整体替换 ──
a = s.index('<line x1="210" y1="930" x2="400" y2="930"')
b_anchor = '<text x="1186" y="1290" fill="#9ca3af" font-size="9.5" font-family="\'Geist Mono\',monospace">↩ 租入（L3/L4）</text>'
b = s.index(b_anchor) + len(b_anchor)
old_block = s[a:b]
assert old_block.count('y1="1286"') == 3 and '租金应付' not in old_block, 'anchor block sanity'
s = s[:a] + NEW_T1 + s[b:]

# ── ② T2 块（y∈[1330,1530]）-128；财务通道区（y≥1540）-96（仅第一 SVG） ──
svg_start = s.index('<svg viewBox="0 0 1280 1762"')
svg_end = s.index('</svg>', svg_start)
seg = s[svg_start:svg_end]

def shift(m, lo, hi, d):
    v = int(m.group(2))
    return f'{m.group(1)}=\"{v + d}\"' if lo <= v <= hi else m.group(0)

nA = len([m for m in re.finditer(r'(?:y1?|y2)="(\d+)"', seg) if 1330 <= int(m.group(1)) <= 1530])
nB = len([m for m in re.finditer(r'(?:y1?|y2)="(\d+)"', seg) if int(m.group(1)) >= 1540])
seg = re.sub(r'(y1?|y2)="(\d+)"', lambda m: shift(m, 1330, 1530, -128), seg)
seg = re.sub(r'(y1?|y2)="(\d+)"', lambda m: shift(m, 1540, 99999, -96), seg)
seg = seg.replace('viewBox="0 0 1280 1762"', 'viewBox="0 0 1280 1666"')
s = s[:svg_start] + seg + s[svg_end:]
print('passA shifted', nA, '(expect 22) · passB shifted', nB, '(expect 45)')
assert nA == 22 and nB == 45

# ── ③ 两注记下移口径注记区（分隔线 y 已=1448） ──
NOTES = '''    <text x="40" y="1408" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">客户转租：独立菜单改状态 · 最简化——拉表改状态（如「客户转租出」）+ 可查（哪个客户/何时改的）+ 最终能还回（2026-09-08 会议）</text>
    <text x="40" y="1424" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">客户虚拟仓：在客户处的租赁资产按客户归集（on-hire）；客户转租为其子状态（T1 方向 · 库位档案/库存查询已示例）</text>
'''
anchor = '<line x1="40" y1="1448" x2="1240" y2="1448" stroke="rgba(17,24,39,0.06)" stroke-width="1"/>'
assert s.count(anchor) == 1
s = s.replace(anchor, NOTES + anchor)

P.write_text(s, encoding='utf-8')
print('OK · T1 compact written')
