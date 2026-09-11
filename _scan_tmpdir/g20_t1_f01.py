# -*- coding: utf-8 -*-
"""G20 任务一：F01 v3.5→v3.6（S5 重复节点+S1 五态+S3 改链+应收应付 5 类+版本）。精确替换+assert。"""
import pathlib, re

F01 = pathlib.Path(__file__).resolve().parent.parent / 'P3-R01-包装租赁管理后台原型' / 'P3-R01-F01-业务流程导航图.html'
s = F01.read_text(encoding='utf-8')
n0 = s.count('租赁出库录单')
assert n0 == 3, f'改前租赁出库录单 {n0}≠3（chip×2+mermaid×1）'

# 1. chip#2（x=472 y=544 重复节点）→ 退租入库新建
old2 = ('<a href="租赁管理/组合出库录单.html"><rect x="472" y="544" width="120" height="36" rx="6" '
        'fill="#ffffff" stroke="#111827"/><text x="532" y="560" fill="#111827" font-size="12" '
        'font-weight="600" font-family="\'Geist\',sans-serif" text-anchor="middle">租赁出库录单</text>'
        '<text x="532" y="574" fill="#4b5563" font-size="8" font-family="\'Geist Mono\',monospace" '
        'text-anchor="middle">⟷ 租赁出库列表</text></a>')
assert s.count(old2) == 1, 'chip#2 锚'
new2 = old2.replace('租赁管理/组合出库录单.html', '租赁管理/弹窗/退租入库新建.html') \
           .replace('>租赁出库录单</text>', '>退租入库新建</text>') \
           .replace('>⟷ 租赁出库列表</text>', '>⟷ 退租入库列表 · 弹窗</text>')
s = s.replace(old2, new2)

# 2. 新增 chip：租入归还新建（插在租赁单列表 chip 后；锚=该 chip 整块尾）
k = s.find('<a href="租赁管理/租赁单列表.html"><rect x="472" y="588"')
assert k != -1, '租赁单列表 chip 锚'
j = s.find('</a>', k) + 4
NEW_CHIP = ('<a href="租赁管理/弹窗/租入归还新建.html"><rect x="658" y="588" width="120" height="36" rx="6" '
            'fill="#ffffff" stroke="#111827"/><text x="718" y="604" fill="#111827" font-size="12" '
            'font-weight="600" font-family="\'Geist\',sans-serif" text-anchor="middle">租入归还新建</text>'
            '<text x="718" y="618" fill="#4b5563" font-size="8" font-family="\'Geist Mono\',monospace" '
            'text-anchor="middle">弹窗 · ⟷ 租入归还列表</text></a>')
s = s[:j] + NEW_CHIP + s[j:]

# 3. S1 副标
old_sub = '>在库/在途/客户/退租/租入</text>'
assert s.count(old_sub) == 1
s = s.replace(old_sub, '>在库/客户/转租/退租/租入</text>')

# 4. 五态注记（x=200 y=130）改名 + y=144 新增定义行（删「调拨在途」——T2b.3 同口径）
old_note = '<text x="200" y="130" fill="#6b7280" font-size="8" font-family="\'Geist Mono\',monospace">库存状态口径：在途＝应入库未入库（退租待入库/采购到货/租入到货/调拨在途）· 租入＝在库未转租，转租后计入客户态</text>'
assert s.count(old_note) == 1, '五态注记锚'
new_notes = ('<text x="200" y="130" fill="#6b7280" font-size="8" font-family="\'Geist Mono\',monospace">库存状态五态：在库/在客户（租出）/客户转租出/退租在途/租入在库</text>\n    '
             '<text x="200" y="144" fill="#6b7280" font-size="8" font-family="\'Geist Mono\',monospace">在途＝应入库未入库（退租待入库/采购到货/租入到货）· 租入＝在库未转租，转租后计入客户态</text>')
s = s.replace(old_note, new_notes)

# 5. S3 角色管理改链
old_s3 = '<a href="系统管理/弹窗/角色管理.html" fill="#2563eb">弹窗</a>'
assert s.count(old_s3) == 1
s = s.replace(old_s3, '<a href="系统管理/角色管理.html" fill="#2563eb">独立页</a>')

# 6. 应收应付 5 类
old_ar_sub = '>四类应收来源 · 含供应商应收</text>'
old_ap_sub = '>四类应付来源 · 含对客户应付</text>'
assert s.count(old_ar_sub) == 1 and s.count(old_ap_sub) == 1
s = s.replace(old_ar_sub, '>五类应收来源 · 含供应商应收/预收</text>')
s = s.replace(old_ap_sub, '>五类应付来源 · 含对客户应付/预付</text>')

old_ar_note = ('<text x="680" y="1952" fill="#6b7280" font-size="8" font-family="\'Geist Mono\',monospace">来源 4 类：B1 销售费 · L1~L4 租赁费 ·</text>\n'
               '    <text x="680" y="1966" fill="#6b7280" font-size="8" font-family="\'Geist Mono\',monospace">丢损赔偿（对客户）· 供应商应收</text>')
assert s.count(old_ar_note) == 1, '应收注记锚'
new_ar_note = ('<text x="680" y="1952" fill="#6b7280" font-size="8" font-family="\'Geist Mono\',monospace">来源 5 类：B1 销售费 · L1~L4 租赁费 · 丢损赔偿（对客户）·</text>\n'
               '    <text x="680" y="1966" fill="#6b7280" font-size="8" font-family="\'Geist Mono\',monospace">供应商应收 · 预收款（保证金）</text>')
s = s.replace(old_ar_note, new_ar_note)

old_ap_note = '<text x="368" y="2038" fill="#6b7280" font-size="8" font-family="\'Geist Mono\',monospace">来源 4 类：采购应付 · 租金应付 · 赔付应付 · 对客户应付/预付款</text>'
assert s.count(old_ap_note) == 1, '应付注记锚'
s = s.replace(old_ap_note, '<text x="368" y="2038" fill="#6b7280" font-size="8" font-family="\'Geist Mono\',monospace">来源 5 类：采购应付 · 租金应付 · 赔付应付 · 对客户应付 · 预付款</text>')

# Mermaid 源 2 处
old_m1 = 'subgraph F1["F1 · 应收（4 来源：B1 销售费/L1~L4 租赁费/丢损赔偿/供应商应收）"]'
old_m2 = 'subgraph F2["F2 · 应付（4 来源：采购应付/租金应付/赔付应付/对客户应付）"]'
assert s.count(old_m1) == 1 and s.count(old_m2) == 1
s = s.replace(old_m1, 'subgraph F1["F1 · 应收（5 来源：B1 销售费/L1~L4 租赁费/丢损赔偿/供应商应收/预收款）"]')
s = s.replace(old_m2, 'subgraph F2["F2 · 应付（5 来源：采购应付/租金应付/赔付应付/对客户应付/预付款）"]')

# Mermaid S5 描述补两入口
old_ms5 = 'S5[录单页与台账：采购入库录单/租赁出库录单/盘点录入/BOM维护/退回进度]'
assert s.count(old_ms5) == 1
s = s.replace(old_ms5, 'S5[录单页与台账：采购入库录单/租赁出库录单/退租入库新建/租入归还新建/盘点录入/BOM维护/退回进度]')

# 7. 版本 v3.6（4 处）+ 沿革追加
old_title = '<title>P3-R01-F01 · 业务流程导航图（v3.5 · 双线制）</title>'
assert s.count(old_title) == 1
s = s.replace(old_title, '<title>P3-R01-F01 · 业务流程导航图（v3.6 · 支线核验修正）</title>')
old_eyebrow = '<p class="eyebrow">P3-R01-F01 · v3.5 原型业务流程导航 · 2026-09-10 双线制修正</p>'
assert s.count(old_eyebrow) == 1
s = s.replace(old_eyebrow, '<p class="eyebrow">P3-R01-F01 · v3.6 原型业务流程导航 · 2026-09-11 支线核验修正</p>')
old_su = '包装租赁管理后台原型 v3.5（双线制：补给线与业务线不串行 · 业务内容沿用 v3.3）'
assert s.count(old_su) == 1
s = s.replace(old_su, '包装租赁管理后台原型 v3.6（支线核验修正 · 双线制：补给线与业务线不串行 · 业务内容沿用 v3.3）')
old_ft = s[s.find('<footer>'):]
ft_old_head = '<footer>P3-R01-F01 · v3.5 · 2026-09-10 · '
assert s.count(ft_old_head) == 1
s = s.replace(ft_old_head, '<footer>P3-R01-F01 · v3.6 · 2026-09-11 · ')

# 沿革末尾追加 v3.6 行（找 footer 内版本沿革数组/列表末尾——探实际结构）
# 沿革结构：文本「 · v3.5（09-10 结构修正）：前 5 条业务线改双线制——…」在一段内。追加在其段落后。
anchor_hist = ' · v3.5（09-10 结构修正）：前 5 条业务线改双线制——补给线（采购/租入→入库→库存）与业务线（单据→出库→交棒）不串行'
assert s.count(anchor_hist) == 1, '沿革锚'
add_hist = anchor_hist + ' · v3.6（09-11 支线核验修正）：S5 重复节点修正+补退租入库新建/租入归还新建两入口 · S1 五态命名对齐原型 · S3 角色管理改链独立页 · 应收应付来源改 5 类'
s = s.replace(anchor_hist, add_hist)

# ---- 终检 ----
checks = [
    ('租赁出库录单', 2),      # chip#1 + mermaid 源（任务书「恰 1」偏差记档：mermaid 源保留）
    ('退租入库新建', 3),      # chip + mermaid + ?
    ('租入归还新建', 3),
    ('在库/客户/转租/退租/租入', 1),
    ('在库/在途/客户/退租/租入', 0),
    ('系统管理/弹窗/角色管理.html', 0),
    ('五类应收来源', 1),
    ('五类应付来源', 1),
    ('4 来源', 0),            # Mermaid 2 处已改；SRC_DATA v3.0 历史为「各 4 来源」表述不含「4 来源」连续串——验证
    ('v3.6', 6),
]
for w, exp in checks:
    act = s.count(w)
    print(f"{'OK ' if act == exp else 'CHK'} [{w}] = {act} (期望 {exp})")
F01.write_text(s, encoding='utf-8')
print('F01 v3.6 WRITTEN, len', len(s))
