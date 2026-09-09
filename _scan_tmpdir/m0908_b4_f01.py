# -*- coding: utf-8 -*-
"""批4 Script A：F01 v3.0 改版（09-08 会议）
- T1：删退租申请节点（直连箭头）；丢损赔偿→直接转应收/应付；拆散·拆卸管理→按零件入库；再组装→再组合出库
- L2：组装节点→按 BOM 组合出库（出库时组合扣减组件注记）
- F1/F2：各 4 来源；S 支线组装/拆卸/赔偿节点同步；全图运营方→供应商
- 新增两行注记（客户转租/客户虚拟仓）；头部副标与 footer v3.0
"""
from pathlib import Path
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
F01 = ROOT / "P3-R01-包装租赁管理后台原型" / "P3-R01-F01-业务流程导航图.html"
txt = F01.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'
LOG = []

def rep(old, new, exp=1, tag=''):
    global txt
    c = txt.count(old)
    assert c == exp, f'[{tag}] {c}≠{exp} 「{old[:60]}」'
    txt = txt.replace(old, new)
    LOG.append(f'{tag} ✓')

# ---------- T1 ----------
# 1) 在租台账 sub
rep('双入口发起退租申请', '客户退回 · 直接录入退租入库', 1, 'T1在租sub')
# 2) 删退租申请节点：两段箭头(210→230 / 380→400)合一直连 + 节点块删除
old_node = ('    <a href="租赁管理/退租入库列表.html">' + nl +
            '      <rect x="230" y="902" width="150" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>' + nl +
            '      <text x="305" y="927" fill="#111827" font-size="12.5" font-weight="600" font-family="' + "'Geist'" + ',sans-serif" text-anchor="middle">退租申请</text>' + nl +
            '      <text x="305" y="946" fill="#4b5563" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">待审核→已审核→待入库→已入库</text>' + nl +
            '    </a>' + nl)
rep(old_node, '', 1, 'T1删退租申请节点')
rep('    <line x1="210" y1="930" x2="230" y2="930" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>' + nl +
    '    <line x1="380" y1="930" x2="400" y2="930" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>' + nl,
    '    <line x1="210" y1="930" x2="400" y2="930" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>' + nl, 1, 'T1直连箭头')
# 3) 审核通过自动生成 注记 → 直接录入口径
rep('审核通过自动生成「退租入库单」（退租申请列表 · 审核弹窗）',
    '退租无申请单：客户退回后直接录入退租入库单 · 入库仅更新库存（2026-09-08 会议）', 1, 'T1注记')
# 4) 丢损赔偿节点 → 直接转应收/应付
rep('<text x="685" y="1039" fill="#111827" font-size="12.5" font-weight="600" font-family="' + "'Geist'" + ',sans-serif" text-anchor="middle">丢损赔偿</text>',
    '<text x="685" y="1039" fill="#111827" font-size="12.5" font-weight="600" font-family="' + "'Geist'" + ',sans-serif" text-anchor="middle">直接转应收/应付</text>', 1, 'T1赔偿节点')
rep('自有 → 应收（客户赔）· 租入 → 应付（运营方赔）· 审核即核销库存 · 详见 S4',
    '自有 → 应收（客户赔）· 租入 → 应付（供应商赔）· 无赔偿单直接建账单（费用分类）· 详见 S4', 1, 'T1赔偿注记')
# 5) L2 分支：按零件入库 / 再组合出库
rep('<text x="648" y="1230" fill="#6b7280" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">按 BOM 拆散</text>',
    '<text x="648" y="1230" fill="#6b7280" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">按零件入库</text>', 1, 'T1-L2组sub')
rep('<text x="786" y="1211" fill="#111827" font-size="12.5" font-weight="600" font-family="' + "'Geist'" + ',sans-serif" text-anchor="middle">拆散 · 拆卸管理</text>' + nl +
    '      <text x="786" y="1230" fill="#4b5563" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">组合拆回散件</text>',
    '<text x="786" y="1211" fill="#111827" font-size="12.5" font-weight="600" font-family="' + "'Geist'" + ',sans-serif" text-anchor="middle">按零件入库</text>' + nl +
    '      <text x="786" y="1230" fill="#4b5563" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">退租按拆后零件记录（无拆卸单）</text>', 1, 'T1-L2拆散节点')
rep('<text x="1106" y="1211" fill="#111827" font-size="12.5" font-weight="600" font-family="' + "'Geist'" + ',sans-serif" text-anchor="middle">再组装</text>' + nl +
    '      <text x="1106" y="1230" fill="#2563eb" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">散件循环 · 成组</text>',
    '<text x="1106" y="1211" fill="#111827" font-size="12.5" font-weight="600" font-family="' + "'Geist'" + ',sans-serif" text-anchor="middle">再组合出库</text>' + nl +
    '      <text x="1106" y="1230" fill="#2563eb" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">按 BOM 组合扣减组件</text>', 1, 'T1-L2再组装')
# 6) L4 分支第二个 拆散·拆卸管理
rep('<text x="786" y="1355" fill="#111827" font-size="12.5" font-weight="600" font-family="' + "'Geist'" + ',sans-serif" text-anchor="middle">拆散 · 拆卸管理</text>',
    '<text x="786" y="1355" fill="#111827" font-size="12.5" font-weight="600" font-family="' + "'Geist'" + ',sans-serif" text-anchor="middle">按零件入库</text>', 1, 'T1-L4拆散节点')
# 7) 顶部凭单验收注记
rep('退租入库←退租申请', '退租入库←客户退回直接录入', 1, '凭单注记')

# ---------- L2 泳道：组装 → 按 BOM 组合出库 ----------
rep('<text x="468" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="' + "'Geist'" + ',sans-serif" text-anchor="middle">组装</text>' + nl +
    '      <text x="468" y="466" fill="#2563eb" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">选父项C·自动带子件</text>',
    '<text x="468" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="' + "'Geist'" + ',sans-serif" text-anchor="middle">按 BOM 组合出库</text>' + nl +
    '      <text x="468" y="466" fill="#2563eb" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">出库时组合扣减组件（无组装单）</text>', 1, 'L2组装节点')

# ---------- S 支线 ----------
rep('>拆卸管理</text><text x="998" y="50" fill="#6b7280" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">承接 T1 拆散</text>',
    '>按零件入库</text><text x="998" y="50" fill="#6b7280" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">退租拆后零件入库</text>', 1, 'S拆卸入口')
rep('>组装录单</text><text x="409" y="530" fill="#6b7280" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">⟷ 组装列表</text>',
    '>组合出库录单</text><text x="409" y="530" fill="#6b7280" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">⟷ 组合出库列表</text>', 1, 'S组装录单')
rep('>丢损赔偿单</text><text x="275" y="410" fill="#6b7280" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">按资产来源定对象</text>',
    '>直接生成应收/应付</text><text x="275" y="410" fill="#6b7280" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">无赔偿单 · 费用分类</text>', 1, 'S4赔偿节点')
rep('口径：按对象直接转单据，无中间结算环节；审核即核销库存（其他出库 · 赔偿核销，09-05 王琳总）',
    '口径：不走独立赔偿单，按对象直接生成应收/应付账单（带费用分类，2026-09-08 会议）；核销库存（其他出库 · 赔偿核销，09-05 王琳总）', 1, 'S4口径注记')
rep('18 类单据统一进待办（订单/出入库/租赁/退租/赔偿/盘点/调拨/拆卸/付款、收款/租入单据）',
    '15 类单据统一进待办（订单/出入库/租赁/退租/盘点/调拨/付款、收款/租入单据；赔偿/组装/拆卸随模块移除）', 1, 'S7待办注记')

# ---------- F1 / F2 四来源 ----------
rep('B1 销售费 · L1~L4 租赁费 · 丢损赔偿（对客户）',
    'B1 销售费 · L1~L4 租赁费 · 丢损赔偿（对客户）· 供应商应收（4 来源）', 1, 'F1四来源')
rep('<text x="406" y="1482" fill="#4b5563" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">三类应收自动汇总</text>',
    '<text x="406" y="1482" fill="#4b5563" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">四类应收来源（含供应商应收）</text>', 1, 'F1账单sub')
rep('采购应付 · 租金应付（按月）· 赔付应付',
    '采购应付 · 租金应付 · 赔付应付 · 对客户应付/预付款（4 来源）', 1, 'F2四来源')
rep('<text x="406" y="1558" fill="#4b5563" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">三类应付汇总</text>',
    '<text x="406" y="1558" fill="#4b5563" font-size="8.5" font-family="' + "'Geist Mono'" + ',monospace" text-anchor="middle">四类应付来源（含对客户应付）</text>', 1, 'F2账单sub')

# ---------- 两行注记（T1 注记区下 y=968/982 空带） ----------
anchor = '<text x="40" y="1000" fill="#374151" font-size="11" font-weight="700" font-family="' + "'Geist'" + ',sans-serif">① 缺损核对 · 要么赔偿，要么继续</text>'
notes = ('    <text x="40" y="968" fill="#6b7280" font-size="9.5" font-family="' + "'Geist Mono'" + ',monospace">客户转租：独立菜单改状态 · 最简化——拉表改状态（如「客户转租出」）+ 可查（哪个客户/何时改的）+ 最终能还回（2026-09-08 会议）</text>' + nl +
         '    <text x="40" y="982" fill="#6b7280" font-size="9.5" font-family="' + "'Geist Mono'" + ',monospace">客户虚拟仓：在客户处的租赁资产按客户归集（on-hire）；客户转租为其子状态（T1 方向 · 库位档案/库存查询已示例）</text>' + nl)
rep(anchor, notes + anchor, 1, '两行注记')

# ---------- 版本叙事 ----------
rep('<title>P3-R01-F01 · 业务流程导航图（v2.9）</title>', '<title>P3-R01-F01 · 业务流程导航图（v3.0）</title>', 1, 'title')
rep('<p class="eyebrow">P3-R01-F01 · v2.9 原型业务流程导航</p>', '<p class="eyebrow">P3-R01-F01 · v3.0 原型业务流程导航</p>', 1, 'eyebrow')
rep('包装租赁管理后台原型 v2.9 · <b>45</b> 个页面 · 6 条业务流程泳道（第2次沟通纪要＋09-04 内部沟通）',
    '包装租赁管理后台原型 v3.0（2026-09-08 会议改造）· <b>40</b> 个页面 · 6 条业务流程泳道（第3次沟通纪要 09-08）', 1, 'sub版本')
rep('· 实体节点点击直达</p>', '· 实体节点点击直达 · 09-08 改造：组装/拆卸/退租申请/丢损赔偿单移除（按 BOM 组合出库·按零件入库·赔偿直建账单）· 财务 4v4 · 客户虚拟仓/客户转租</p>', 1, 'sub改造句')
rep('<footer>P3-R01-F01 · v2.9 · 2026-09-04 · 汽车物流包装租赁 · 包装租赁管理后台原型 · 45 页 / 6 条主线泳道',
    '<footer>P3-R01-F01 · v3.0 · 2026-09-09 · 汽车物流包装租赁 · 包装租赁管理后台原型 · 40 页 / 6 条主线泳道', 1, 'footer头')
rep('· 全部流程化跳转 · 79 个弹窗可独立演示 ·', '· 全部流程化跳转 · 67 个弹窗可独立演示 ·', 1, 'footer弹窗数')
rep('· F02 演示流程图已归档，演示统一用本图</footer>',
    '· F02 演示流程图已归档，演示统一用本图 · v3.0（09-08 会议）：四模块移除·按 BOM 组合出库/按零件入库·赔偿直建 4v4·分期互算·产品档案合并·客户虚拟仓/客户转租·六角色审核</footer>', 1, 'footer尾')

# ---------- 决策注记追加 ----------
rep("    ['同上 · 道远 3:49（王琳总确认）',",
    "    ['v3.0 · 2026-09-08 会议拍板','组装/拆卸/退租申请/丢损赔偿单四模块移除——库存结果导向（出库按 BOM 组合扣减·退租按零件入库·赔偿直接建应收/应付）；财务应收应付各 4 来源；器具+零部件合并产品档案；客商去运营方；六角色审核；客户虚拟仓（on-hire）与客户转租最简化'],\n" +
    "    ['同上 · 道远 3:49（王琳总确认）',", 1, '决策注记')

# ---------- 全局 运营方→供应商 ----------
n = txt.count('运营方')
txt = txt.replace('运营方', '供应商')
LOG.append(f'运营方→供应商 {n} 处')

F01.write_bytes(txt.encode('utf-8'))
print('== 批4 F01 v3.0 ==')
for l in LOG:
    print(' ✓', l)
