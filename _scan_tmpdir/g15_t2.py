# -*- coding: utf-8 -*-
"""G15 T2 · 主 SVG 内容收编（读取-精确替换+assert 计数 · 小步写盘）
范围：分隔线 x2 1240→840（9 条，含支图例线的 x2）；右对齐注记 x=1240→840（7 处，避让📎标签下移）；
B1/L3/L4 决策框移位收窄；T1 长侧注拆行；适用注记移位；T2 双入口注记移位；F1 来源注记拆行。
F2 侧注/底部注记经复核右缘 ≤840 不动（见失败清单偏差注记）。"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

F = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\P3-R01-F01-业务流程导航图.html')
t = open(F, encoding='utf-8', newline='').read()

def rep(old, new, n=1, label=''):
    global t
    c = t.count(old)
    if c == 0 and new in t:
        print(f'  [幂等跳过] {label}')
        return
    assert c == n, f'ASSERT FAIL [{label}]: count={c} expect={n}'
    t = t.replace(old, new)
    print(f'  OK [{label}] ×{c}')

# 1. 分隔线 x2 批量 1240→840（9 条：主 8 + 支图例 1）
rep('x2="1240"', 'x2="840"', 9, '分隔线 x2 1240→840')

# 2. 右对齐注记 7 处（x=1240→840；避让 x=620-716 📎标签，y 下移——决策表#4 扩展适用）
N = ' fill="#6b7280" font-size="8" font-family="\'Geist Mono\',monospace" text-anchor="end">'
rep(f'<text x="1240" y="320"{N}租赁费 → <a href="财务协同/应收账单.html" fill="#2563eb">应收账单</a>（自动汇总）</text>',
    f'<text x="840" y="336"{N}租赁费 → <a href="财务协同/应收账单.html" fill="#2563eb">应收账单</a>（自动汇总）</text>', 1, 'L1注记→(840,336)')
rep(f'<text x="1240" y="548"{N}租赁费 → <a href="财务协同/应收账单.html" fill="#2563eb">应收账单</a>（按租赁出库自动汇总）</text>',
    f'<text x="840" y="564"{N}租赁费 → <a href="财务协同/应收账单.html" fill="#2563eb">应收账单</a>（按租赁出库自动汇总）</text>', 1, 'L2注记→(840,564)')
rep(f'<text x="1240" y="776"{N}租赁费 → <a href="财务协同/应收账单.html" fill="#2563eb">应收账单</a> · 租金 → <a href="财务协同/应付账单.html" fill="#2563eb">应付账单</a></text>',
    f'<text x="840" y="792"{N}租赁费 → <a href="财务协同/应收账单.html" fill="#2563eb">应收账单</a> · 租金 → <a href="财务协同/应付账单.html" fill="#2563eb">应付账单</a></text>', 1, 'L3注记→(840,792)')
rep(f'<text x="1240" y="1004"{N}租赁费 → <a href="财务协同/应收账单.html" fill="#2563eb">应收账单</a> · 租金 → <a href="财务协同/应付账单.html" fill="#2563eb">应付账单</a></text>',
    f'<text x="840" y="1020"{N}租赁费 → <a href="财务协同/应收账单.html" fill="#2563eb">应收账单</a> · 租金 → <a href="财务协同/应付账单.html" fill="#2563eb">应付账单</a></text>', 1, 'L4注记→(840,1020)')
rep(f'<text x="1240" y="1328"{N}核对：要么赔偿，要么继续 · 完好：自有回库再出租 / 租入回库后交棒 T2</text>',
    f'<text x="840" y="1344"{N}核对：要么赔偿，要么继续 · 完好：自有回库再出租 / 租入回库后交棒 T2</text>', 1, 'T1注记→(840,1344)')
rep(f'<text x="1240" y="1682"{N}方向：我方仓库 → 供应商 · 与 T1（客户 → 我方仓库）两事件方向相反</text>',
    f'<text x="840" y="1708"{N}方向：我方仓库 → 供应商 · 与 T1（客户 → 我方仓库）两事件方向相反</text>', 1, 'T2注记→(840,1708) 避让交棒虚线y=1696')
rep(f'<text x="1240" y="1888"{N}按客户/供应商汇总 · 同一账单可部分核销</text>',
    f'<text x="840" y="1904"{N}按客户/供应商汇总 · 同一账单可部分核销</text>', 1, 'F注记→(840,1904)')

# 3. B1 决策框：x=516 w=324，内文 2→3 行
rep('<rect x="560" y="116" width="680" height="56" rx="6" fill="rgba(17,24,39,0.02)" stroke="#d1d5db" stroke-width="0.8" stroke-dasharray="4,3"/>',
    '<rect x="516" y="116" width="324" height="56" rx="6" fill="rgba(17,24,39,0.02)" stroke="#d1d5db" stroke-width="0.8" stroke-dasharray="4,3"/>', 1, 'B1决策框→516/324')
M = ' fill="#6b7280" font-size="8" font-family="\'Geist Mono\',monospace">'
rep(f'<text x="572" y="140"{M}09-04 王琳总拍板：销售/采购两条独立线 · 库存缓冲 · 不以销定采</text>',
    f'<text x="528" y="134"{M}09-04 王琳总拍板：销售/采购两条独立线 · 库存缓冲 · 不以销定采</text>', 1, 'B1框文1→x528 y134')
rep(f'<text x="572" y="156"{M}原方案「先销后采互通」（袁丽晶 21:46 · 第2次沟通）· 采购订单零部件/器具两类公用</text>',
    f'<text x="528" y="148"{M}原方案「先销后采互通」（袁丽晶 21:46 · 第2次沟通）·</text>\n'
    f'    <text x="528" y="162"{M}采购订单零部件/器具两类公用</text>', 1, 'B1框文2拆两行')

# 4. L3 决策框：x=516 w=324，内文 2→3 行（行1 超 840 拆行，决策表#2）
rep('<rect x="560" y="800" width="680" height="56" rx="6" fill="rgba(17,24,39,0.02)" stroke="#d1d5db" stroke-width="0.8" stroke-dasharray="4,3"/>',
    '<rect x="516" y="800" width="324" height="56" rx="6" fill="rgba(17,24,39,0.02)" stroke="#d1d5db" stroke-width="0.8" stroke-dasharray="4,3"/>', 1, 'L3决策框→516/324')
rep(f'<text x="572" y="824"{M}决策变更 · 09-04 道远拍板第一期闭环（原会议暂缓 · 袁丽晶 37:35 · 第2次沟通）</text>',
    f'<text x="528" y="818"{M}决策变更 · 09-04 道远拍板第一期闭环</text>\n'
    f'    <text x="528" y="832"{M}（原会议暂缓 · 袁丽晶 37:35 · 第2次沟通）</text>', 1, 'L3框文1拆两行')
rep(f'<text x="572" y="840"{M}租入单 / 租入入库 / 租入归还独立成单 · 租金按月生成「租金应付」进应付账单</text>',
    f'<text x="528" y="846"{M}租入单 / 租入入库 / 租入归还独立成单 · 租金按月生成「租金应付」进应付账单</text>', 1, 'L3框文2→x528 y846')

# 5. L4 决策框：x=532 w=308
rep('<rect x="1112" y="1104" width="128" height="56" rx="6" fill="rgba(17,24,39,0.02)" stroke="#d1d5db" stroke-width="0.8" stroke-dasharray="4,3"/>',
    '<rect x="532" y="1104" width="308" height="56" rx="6" fill="rgba(17,24,39,0.02)" stroke="#d1d5db" stroke-width="0.8" stroke-dasharray="4,3"/>', 1, 'L4决策框→532/308')
rep(f'<text x="1124" y="1128"{M}决策升级 · 09-04 拍板</text>',
    f'<text x="544" y="1128"{M}决策升级 · 09-04 拍板</text>', 1, 'L4框文1→x544')
rep(f'<text x="1124" y="1144"{M}拍板 A1 → 租入单据独立闭环</text>',
    f'<text x="544" y="1144"{M}拍板 A1 → 租入单据独立闭环</text>', 1, 'L4框文2→x544')

# 6. T1 长侧注拆两行（从「·」拆，行距 14）
rep(f'<text x="556" y="1458"{M}自有 → 应收（客户赔）· 租入 → 应付（供应商赔）· 无赔偿单直接建账单（费用分类）· 详见 S4</text>',
    f'<text x="556" y="1458"{M}自有 → 应收（客户赔）· 租入 → 应付（供应商赔）·</text>\n'
    f'    <text x="556" y="1472"{M}无赔偿单直接建账单（费用分类）· 详见 S4</text>', 1, 'T1长侧注拆两行')

# 7. 适用注记移位（②移至(682,1572) 按文档；③移至(556,1646) 避让 T1→T2 交棒虚线 x=752——偏差注记）
rep(f'<text x="854" y="1534"{M}适用：L1/L2（自有资产）</text>',
    f'<text x="682" y="1572"{M}适用：L1/L2（自有资产）</text>', 1, '适用注记L1/L2→(682,1572)')
rep(f'<text x="854" y="1610"{M}适用：L3/L4（租入资产）</text>',
    f'<text x="556" y="1646"{M}适用：L3/L4（租入资产）</text>', 1, '适用注记L3/L4→(556,1646)')

# 8. T2 双入口注记 ×2 移位 + 既有租金应付注记下移避让（y=1744 被占——偏差注记）
rep(f'<text x="880" y="1700"{M}双入口：① T1 退租回库的租入行（先回库再归还）</text>',
    f'<text x="524" y="1724"{M}双入口：① T1 退租回库的租入行（先回库再归还）</text>', 1, 'T2双入口①→(524,1724)')
rep(f'<text x="880" y="1716"{M}② 租入未转租（租入在库）直接归还——不经退租入库（无客户环节）</text>',
    f'<text x="524" y="1740"{M}② 租入未转租（租入在库）直接归还——不经退租入库（无客户环节）</text>', 1, 'T2双入口②→(524,1740)')
rep(f'<text x="524" y="1744"{M}租金应付进 F2 应付账单（L3/L4 已实现 · 租入单按月生成）</text>',
    f'<text x="524" y="1760"{M}租金应付进 F2 应付账单（L3/L4 已实现 · 租入单按月生成）</text>', 1, 'T2既有注记下移→y1760')

# 9. F1 来源注记拆两行
rep(f'<text x="680" y="1952"{M}来源 4 类：B1 销售费 · L1~L4 租赁费 · 丢损赔偿（对客户）· 供应商应收</text>',
    f'<text x="680" y="1952"{M}来源 4 类：B1 销售费 · L1~L4 租赁费 ·</text>\n'
    f'    <text x="680" y="1966"{M}丢损赔偿（对客户）· 供应商应收</text>', 1, 'F1来源注记拆两行')

open(F, 'w', encoding='utf-8', newline='').write(t)
print('T2 写盘完成')
