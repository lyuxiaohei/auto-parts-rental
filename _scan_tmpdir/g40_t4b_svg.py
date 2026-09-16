# -*- coding: utf-8 -*-
"""G40 T4-b F01 结构改动（②新增「转移出库」节点——全图唯一结构改动）
- L1／L3 业务线行各补 1 个「转移出库」节点（170×56 白底流程节点 · 指向 租赁管理/转移出库列表.html）
- L1 补给线右侧空白区补 1 个跨线决策备注框（「L1–L4 通用」＋注记四点）——沿用规则 §5「决策备注只用虚线框·位置=补给线右侧空白区」
- L3 只补节点＋指向 L1 注记框的短注记（不重复画注记）
- 连接线：从「租赁出库」顶边上引 → 横走 → 下入新节点顶边（正交·实线·marker #arr），带箭头标签「分批 · 非必经」
- 同步 Mermaid 源（规则 §10 每次改图必须同步），坐标不动既有节点
"""
import io, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(BASE, 'P3-R01-包装租赁管理后台原型', 'P3-R01-F01-业务流程导航图.html')

# ---------- L1：装配到 ⇢T1 退租 之后、y=524 分隔线之前 ----------
L1_ANCHOR = '''    <line x1="40" y1="524" x2="840" y2="524" stroke="rgba(17,24,39,0.10)" stroke-width="1"/>'''
L1_INS = '''    <!-- v3.7 新增 · 转移出库（L1 · 客户间转移 · 全图唯一结构改动 · D-146） -->
    <rect x="504" y="344" width="336" height="76" rx="6" fill="rgba(17,24,39,0.02)" stroke="#d1d5db" stroke-width="0.8" stroke-dasharray="4,3"/>
    <text x="516" y="360" fill="#6b7280" font-size="8" font-family="'Geist Mono',monospace">决策备注 · 转移出库（L1–L4 通用 · D-146）</text>
    <text x="516" y="374" fill="#6b7280" font-size="8" font-family="'Geist Mono',monospace">① 不勾稽原租赁单（D-106）· 只记转出方 → 接收方</text>
    <text x="516" y="388" fill="#6b7280" font-size="8" font-family="'Geist Mono',monospace">② 按租出结算＝默认 · 转移单不进财务链路</text>
    <text x="516" y="402" fill="#6b7280" font-size="8" font-family="'Geist Mono',monospace">③ 按终端结算＝特例 · 账单主体切终端（历史不回改）</text>
    <text x="516" y="416" fill="#6b7280" font-size="8" font-family="'Geist Mono',monospace">④ 终止转移＝回「在客户（租出）」· 待转移 → 已转移 → 已终止</text>
    <path d="M 300 444 V 432 H 545 V 444" fill="none" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <rect x="512" y="426" width="72" height="12" rx="4" fill="#fafafa"/>
    <text x="548" y="435" fill="#4b5563" font-size="8" font-family="'Geist Mono',monospace" text-anchor="middle">分批 · 非必经</text>
    <a href="租赁管理/转移出库列表.html">
      <rect x="460" y="444" width="170" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="545" y="469" fill="#111827" font-size="12" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">转移出库</text>
      <text x="545" y="488" fill="#4b5563" font-size="8" font-family="'Geist Mono',monospace" text-anchor="middle">客户间转移 · 直接客户 → 终端客户</text>
    </a>

'''
L1_ANCHOR_NEW = L1_INS + L1_ANCHOR

# ---------- L3：装配到 ⇢T1/T2 之后、y=980 分隔线之前 ----------
L3_ANCHOR = '''    <line x1="40" y1="980" x2="840" y2="980" stroke="rgba(17,24,39,0.10)" stroke-width="1"/>'''
L3_INS = '''    <!-- v3.7 新增 · 转移出库（L3 · 客户间转移 · 注记见 L1 跨线框） -->
    <path d="M 300 900 V 890 H 545 V 900" fill="none" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>
    <rect x="512" y="884" width="72" height="12" rx="4" fill="#fafafa"/>
    <text x="548" y="893" fill="#4b5563" font-size="8" font-family="'Geist Mono',monospace" text-anchor="middle">分批 · 非必经</text>
    <a href="租赁管理/转移出库列表.html">
      <rect x="460" y="900" width="170" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="545" y="925" fill="#111827" font-size="12" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">转移出库</text>
      <text x="545" y="944" fill="#4b5563" font-size="8" font-family="'Geist Mono',monospace" text-anchor="middle">客户间转移 · 直接客户 → 终端客户</text>
    </a>
    <text x="642" y="925" fill="#6b7280" font-size="8" font-family="'Geist Mono',monospace">转移出库 · L1–L4 通用 · 注记见 L1 右侧框</text>
    <text x="642" y="939" fill="#6b7280" font-size="8" font-family="'Geist Mono',monospace">结算默认＝项目档案「转租结算方式」（D-132）</text>

'''
L3_ANCHOR_NEW = L3_INS + L3_ANCHOR

# ---------- Mermaid 源同步（规则 §10） ----------
MM = [
    ('    L1d[租赁单] --> L1e[租赁出库] --> L1f[⇢ T1 退租]',
     '    L1d[租赁单] --> L1e[租赁出库] --> L1f[⇢ T1 退租]\n    L1e -. 分批·非必经 .-> L1x[转移出库·客户间转移·L1–L4 通用]', 1),
    ('    L3d[租赁单·转租] --> L3e[租赁出库] --> L3f[⇢ T1/T2]',
     '    L3d[租赁单·转租] --> L3e[租赁出库] --> L3f[⇢ T1/T2]\n    L3e -. 分批·非必经 .-> L3x[转移出库·客户间转移·L1–L4 通用]', 1),
    ('subgraph F1["F1 · 应收（5 来源：B1 销售费/L1~L4 租赁费/丢损赔偿/供应商应收/预收款）"]',
     'subgraph F1["F1 · 应收（5 来源：B1 销售费/L1~L4 租赁费/丢损赔偿/供应商应收/预收款）｜计租＝按持有量计租·期段账单（起租日/止租日/天数/日单价/小计）"]', 1),
    ('subgraph F2["F2 · 应付（5 来源：采购应付/租金应付/赔付应付/对客户应付/预付款）"]',
     'subgraph F2["F2 · 应付（5 来源：采购应付/租金应付/赔付应付/对客户应付/预付款）｜租金应付＝按持有量计租·期段账单"]', 1),
    ('T2c[租金应付 ⇢ F2]', 'T2c[租金应付·按持有量计租 ⇢ F2]', 1),
    ('S1[库存运营：库存查询/盘点/调拨/其他出入库/按零件入库]',
     'S1[库存运营：库存查询/盘点/调拨/其他出入库/按零件入库｜客户转租出＝转移出库单审核驱动·终止转移回在客户（租出）]', 1),
]


def main():
    s = io.open(P, encoding='utf-8', newline='').read()
    for anchor, new, want in [(L1_ANCHOR, L1_ANCHOR_NEW, 1), (L3_ANCHOR, L3_ANCHOR_NEW, 1)]:
        c = s.count(anchor)
        assert c == want, 'SVG 锚点计数 %d != %d : %r' % (c, want, anchor[:60])
        s = s.replace(anchor, new)
        print('OK SVG 插入 @ %s' % anchor.strip()[:52])
    for old, new, want in MM:
        c = s.count(old)
        assert c == want, 'Mermaid 锚点计数 %d != %d : %r' % (c, want, old[:60])
        s = s.replace(old, new)
        print('OK Mermaid 同步 @ %s' % old.strip()[:52])
    io.open(P, 'w', encoding='utf-8', newline='').write(s)

    print('--- 复核 ---')
    import re
    s2 = io.open(P, encoding='utf-8', newline='').read()
    print('   转移出库 = %d （节点 a 标签 2 + 文本 2 + Mermaid 2 + Mermaid 引用 2 + 注记 2 = 期望 10）' % s2.count('转移出库'))
    print('   href 租赁管理/转移出库列表.html = %d （期望 2）' % s2.count('href="租赁管理/转移出库列表.html"'))
    print('   L1–L4 通用 = %d （期望 4：L1 框标题 + L3 注记 + Mermaid ×2）' % s2.count('L1–L4 通用'))
    print('   分批 · 非必经 = %d （期望 2）' % s2.count('分批 · 非必经'))
    print('   决策备注 · 转移出库 = %d （期望 1）' % s2.count('决策备注 · 转移出库'))
    # 标签配平
    for tag in ['svg', 'a', 'text', 'g', 'defs', 'details', 'footer']:
        o = len(re.findall(r'<%s[\s>]' % tag, s2))
        c = len(re.findall(r'</%s>' % tag, s2))
        print('   <%s> %d / </%s> %d %s' % (tag, o, tag, c, 'OK' if o == c else '<<< 不配平'))
    # viewBox 与内容上界
    print('   viewBox:', re.findall(r'viewBox="([^"]+)"', s2))
    ys = [float(y) for y in re.findall(r'y="(-?\d+(?:\.\d+)?)"', s2)]
    print('   最大 y 属性 = %.0f' % max(ys))
    return 0


if __name__ == '__main__':
    sys.exit(main())
