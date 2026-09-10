# -*- coding: utf-8 -*-
"""G08: F01 T1 退租专项拆分为 T1 客户退租 / T2 租入归还（v3.2→v3.3）
顺序：①y<1400 文案/节点精确替换 ②第一 SVG 内 y>=1400 坐标整体 +144 ③插入 T2 块与新注记
"""
import re
from pathlib import Path

P = Path(r'P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图.html')
s = P.read_text(encoding='utf-8')
SHIFT = 144
THRESH = 1400

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, f'count={c} (expect {n}): {old[:70]}'
    s = s.replace(old, new)

# ── ① 头部 ──
rep('<title>P3-R01-F01 · 业务流程导航图（v3.2）</title>',
    '<title>P3-R01-F01 · 业务流程导航图（v3.3）</title>')
rep('<p class="eyebrow">P3-R01-F01 · v3.2 原型业务流程导航</p>',
    '<p class="eyebrow">P3-R01-F01 · v3.3 原型业务流程导航</p>')
rep('包装租赁管理后台原型 v3.2（2026-09-10 修正',
    '包装租赁管理后台原型 v3.3（2026-09-10 修正')
rep('· <b>38</b> 个页面 · 6 条业务流程泳道（第3次沟通纪要 09-08）',
    '· <b>38</b> 个页面 · 7 条业务流程泳道（第3次沟通纪要 09-08）')
rep('· <b>T1</b> 退租专项（两事件：客户退租→退租入库 ｜ 归还供应商→租入归还 · 09-10 拍板）·',
    '· <b>T1</b> 客户退租（退租入库统一入口）· <b>T2</b> 租入归还（归还供应商独立事件 · 两事件拆分 T1/T2 · 09-10 拍板）·')
rep('+L4 组合环节去流程化（BOM 计算·无组装单）</p>',
    '+L4 组合环节去流程化（BOM 计算·无组装单）· v3.3（09-10 修正）：退租专项拆分为 T1 客户退租 / T2 租入归还两条编号流程（T1 止于回库交棒 T2 · T2 双入口=退租回库租入行＋未转租直还 · 6→7 条主线泳道）</p>')
rep('· T 退租专项 · F 财务（F1 应收 / F2 应付）·',
    '· T 退租/归还（T1 客户退租 / T2 租入归还） · F 财务（F1 应收 / F2 应付）·')

# ── ② L3/L4 跨泳道指引 ──
rep('<text x="820" y="594" fill="#9ca3af" font-size="9.5" font-family="\'Geist Mono\',monospace">→ 退租及后续见 T1 专项</text>',
    '<text x="820" y="594" fill="#9ca3af" font-size="9.5" font-family="\'Geist Mono\',monospace">→ 退租见 T1 · 租入归还见 T2</text>')
rep('<text x="832" y="800" fill="#9ca3af" font-size="9.5" font-family="\'Geist Mono\',monospace">→ 退租及后续见 T1 专项</text>',
    '<text x="832" y="800" fill="#9ca3af" font-size="9.5" font-family="\'Geist Mono\',monospace">→ 退租见 T1 · 租入归还见 T2</text>')

# ── ③ T1 泳道收窄 ──
rep('<!-- T1 退租专项泳道（v2.9：09-05 道远裁定——核对二分：要么赔偿要么继续；完好走②归还分流） -->',
    '<!-- T1 客户退租泳道（v3.3：09-10 两事件拆分——T1=客户退租→退租入库→回库；租入行回库后交棒 T2） -->')
rep('<text x="40" y="882" fill="#1f2937" font-size="14" font-weight="700" font-family="\'Geist\',sans-serif">T1 · 租赁 · 退租专项（两事件模型 · 2026-09-10 拍板）</text>',
    '<text x="40" y="882" fill="#1f2937" font-size="14" font-weight="700" font-family="\'Geist\',sans-serif">T1 · 租赁 · 客户退租（退租入库 · 统一入口 · 2026-09-10 拍板）</text>')
rep('<text x="1240" y="882" fill="#2563eb" font-size="9.5" font-family="\'Geist Mono\',monospace" text-anchor="end">核对：要么赔偿，要么继续 · 完好后按归属：自有回库 / 租入另起归还</text>',
    '<text x="1240" y="882" fill="#2563eb" font-size="9.5" font-family="\'Geist Mono\',monospace" text-anchor="end">核对：要么赔偿，要么继续 · 完好：自有回库再出租 / 租入回库后交棒 T2</text>')
rep('② 完好 · 按资产归属分流（是否拆散＝退租入库的记录粒度 · 非流程分支 · 2026-09-10 拍板两事件模型）',
    '② 完好 · 按资产归属分流（是否拆散＝退租入库的记录粒度 · 非流程分支 · 租入行回库后交棒 T2）')

# 租入行：租入归还节点 → 交棒 chip；删 租金应付 节点与连线（↩ 租入(L3/L4) 注记保留在 T1）
rep('''    <a href="租赁管理/租入归还列表.html">
      <rect x="876" y="1258" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="946" y="1283" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租入归还</text>
      <text x="946" y="1302" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">关联租入单 · 同步明细 · 分批</text>
    </a>''',
    '''    <a href="租赁管理/租入归还列表.html">
      <rect x="876" y="1258" width="140" height="56" rx="6" fill="rgba(75,85,99,0.10)" stroke="#4b5563" stroke-width="1"/>
      <text x="946" y="1283" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">⇢ T2 · 租入归还</text>
      <text x="946" y="1302" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">归还供应商 · 见 T2</text>
    </a>''')
rep('''    <line x1="1016" y1="1286" x2="1036" y2="1286" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <a href="财务协同/应付账单.html">
      <rect x="1036" y="1258" width="140" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="1106" y="1283" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租金应付</text>
      <text x="1106" y="1302" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">租金＋损坏赔付</text>
    </a>
''', '')

# ── ④ 删旧三行注记（1352/1368/1384） ──
for old_note in [
    '<text x="40" y="1352" fill="#6b7280" font-size="9.5" font-family="\'Geist Mono\',monospace">L4 混合转租＝退租入库后按明细行归属分流：自有行走②回库、租入行走③归还供应商（先回库再归还）——两事件组合，非独立分支</text>\n',
    '<text x="40" y="1368" fill="#6b7280" font-size="9.5" font-family="\'Geist Mono\',monospace">租入资产未转租（租入在库）归还供应商：直接租入归还，不经退租入库（无客户环节）</text>\n',
    '<text x="40" y="1384" fill="#6b7280" font-size="9.5" font-family="\'Geist Mono\',monospace">退租入库仅更新库存、与财务结算解耦（应收按月/按实际使用量独立生成）；缺损核对在入口①一次完成，③只挂租金与归还侧赔付</text>\n',
]:
    rep(old_note, '')

# ── ⑤ footer ──
rep('<footer>P3-R01-F01 · v3.2 · 2026-09-10', '<footer>P3-R01-F01 · v3.3 · 2026-09-10')
rep('38 页 / 6 条主线泳道（B1/L1/L2/L3/L4 全部第一期实现·L3/L4 为 2026-09-04 拍板升级·T1 退租专项=两事件模型·泳道止于出库，退租及后续统一在 T1）',
    '38 页 / 7 条主线泳道（B1/L1/L2/L3/L4 全部第一期实现·L3/L4 为 2026-09-04 拍板升级·退租两事件=T1 客户退租＋T2 租入归还·泳道止于出库，退租及后续在 T1/T2）')
rep('· v3.2（09-10 修正）：退租两事件模型·台账合并（租出台账→租赁单列表·在租台账→库存查询）·L4 组合去流程化·40→38 页</footer>',
    '· v3.2（09-10 修正）：退租两事件模型·台账合并（租出台账→租赁单列表·在租台账→库存查询）·L4 组合去流程化·40→38 页 · v3.3（09-10 修正）：退租专项拆 T1/T2 两条编号流程（T1 客户退租止于回库交棒 T2 · T2 租入归还双入口）·6→7 条主线泳道</footer>')

# ── ⑥ SRC_DATA：t1 改名 + 新增 t2 ──
rep("t1: {head:'T1 · 退租专项 · 会议依据与拍板', items:[",
    "t1: {head:'T1 · 客户退租（退租入库）· 会议依据与拍板', items:[")
rep("""  fin: {head:'财务通道 F1 应收 / F2 应付 · 会议依据', items:[""",
    """  t2: {head:'T2 · 租入归还（归还供应商）· 会议依据与拍板', items:[
    ['决策变更 · 2026-09-04 道远拍板','L3 第一期闭环：租入单 / 租入入库 / 租入归还独立成单（不公用采购入库与其他出库），租金按月生成「租金应付」进应付账单'],
    ['决策修正 · 2026-09-10 道远拍板','租入归还＝归还供应商独立事件（关联租入单·同步明细·分批）；双入口：客户退租回库的租入行（先回库再归还）｜ 租入未转租（租入在库）直接归还——不经退租入库（无客户环节）'],
    ['v3.3 · 2026-09-10 拆分','退租专项由单条 T1 拆分为 T1 客户退租 / T2 租入归还两条编号流程——两事件方向相反（客户→我方 ｜ 我方→供应商）；T1 止于回库，L4＝T1+T2 按明细行归属组合'],
  ]},
  fin: {head:'财务通道 F1 应收 / F2 应付 · 会议依据', items:[""")

# ── ⑦ 第一 SVG 内 y>=1400 坐标 +144（先切分，支线 SVG 不动） ──
svg_start = s.index('<svg viewBox="0 0 1280 1618"')
svg_end = s.index('</svg>', svg_start)
seg = s[svg_start:svg_end]

def bump(m):
    v = int(m.group(2))
    return f'{m.group(1)}=\"{v + SHIFT}\"' if v >= THRESH else m.group(0)

seg2 = re.sub(r'(y1?|y2)="(\d+)"', lambda m: bump(m), seg)
n_shifted = len([m for m in re.finditer(r'(?:y1?|y2)="(\d+)"', seg) if int(m.group(1)) >= THRESH])
assert n_shifted == 45, f'shifted {n_shifted} (expect 45)'  # 分隔线2+财务标题1+src2+F1线8+rect5+text10+F2线4+rect3+text6+注记4
seg2 = seg2.replace('viewBox="0 0 1280 1618"', 'viewBox="0 0 1280 1762"')
s = s[:svg_start] + seg2 + s[svg_end:]

# ── ⑧ 插入 T2 块 + 新三行注记（锚=移位后的分隔线） ──
T2 = '''    <!-- T2 租入归还泳道（v3.3：09-10 道远拍板两事件拆分——T1 客户退租止于回库，租入行交棒 T2 归还供应商） -->
    <text x="40" y="1362" fill="#1f2937" font-size="14" font-weight="700" font-family="'Geist',sans-serif">T2 · 租赁 · 租入归还（归还供应商 · 独立事件 · 2026-09-10 拍板）</text>
    <g class="src-tag" onclick="showSrc(event,'t2')" style="cursor:pointer">
      <rect x="620" y="1348" width="96" height="18" rx="3" fill="#fafafa" stroke="#c9cdd4" stroke-width="0.8"/>
      <text x="668" y="1361" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace" text-anchor="middle">📎 会议材料 ▸</text>
    </g>
    <text x="1240" y="1362" fill="#2563eb" font-size="9.5" font-family="'Geist Mono',monospace" text-anchor="end">方向：我方仓库 → 供应商 · 与 T1（客户 → 我方仓库）两事件方向相反</text>
    <text x="40" y="1388" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">双入口：① ⇢ T1 退租回库的租入行（先回库再归还）｜ ② 租入未转租（租入在库）直接归还——不经退租入库（无客户环节）</text>
    <line x1="210" y1="1424" x2="230" y2="1424" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <line x1="400" y1="1424" x2="420" y2="1424" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <a href="仓储作业/库存查询.html">
      <rect x="40" y="1396" width="170" height="56" rx="6" fill="rgba(75,85,99,0.10)" stroke="#4b5563" stroke-width="1"/>
      <text x="125" y="1421" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租入在库</text>
      <text x="125" y="1440" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">待归还 · 库存查询</text>
    </a>
    <a href="租赁管理/租入归还列表.html">
      <rect x="230" y="1396" width="170" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="315" y="1421" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租入归还</text>
      <text x="315" y="1440" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">关联租入单 · 同步明细 · 分批</text>
    </a>
    <a href="财务协同/应付账单.html">
      <rect x="420" y="1396" width="170" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="505" y="1421" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租金应付</text>
      <text x="505" y="1440" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">租金＋归还侧损坏赔付</text>
    </a>
    <text x="620" y="1428" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">租金应付进 F2 应付账单（L3/L4 已实现 · 租入单按月生成）</text>
    <text x="40" y="1488" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">L4 混合转租＝T1+T2 两事件按明细行归属组合：自有行 T1 内回库、租入行 T1 回库后交棒 T2 归还供应商——组合关系，非独立分支</text>
    <text x="40" y="1504" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">T2 双入口：T1 退租回库的租入行（先回库再归还）｜ 租入资产未转租（租入在库）直接归还——不经退租入库（无客户环节）</text>
    <text x="40" y="1520" fill="#6b7280" font-size="9.5" font-family="'Geist Mono',monospace">退租入库仅更新库存、与财务结算解耦（应收按月/按实际使用量独立生成）；缺损核对在 T1 入口一次完成，T2 只挂租金与归还侧赔付</text>
'''
anchor = '<line x1="40" y1="1544" x2="1240" y2="1544" stroke="rgba(17,24,39,0.06)" stroke-width="1"/>'
rep(anchor, T2 + anchor)

P.write_text(s, encoding='utf-8')
print('OK · shifted', n_shifted, 'coords · file written')
