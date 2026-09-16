# -*- coding: utf-8 -*-
"""G41 T3：A05 实体计数订正＋assetTracks 退役注记；A06 名册 37→42＋补 transferOutbounds/stockEvents 等 6 实体＋状态驱动方。"""
import io

BASE = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"

def edit(fp, edits):
    c = io.open(fp, encoding="utf-8", newline="").read()
    for old, new, tag in edits:
        n = c.count(old)
        assert n == 1, "[%s] 锚点命中 %d" % (tag, n)
        c = c.replace(old, new)
        print("[OK] %s" % tag)
    io.open(fp, "w", encoding="utf-8", newline="").write(c)

# ---------------- A05 ----------------
A05 = BASE + r"\P3-R01-A05-字段字典.md"
edit(A05, [
    ("＋G39 增补（2026-09-16：按天计租落地·stockEvents 新实体＋5 实体增量字段＋feeCols 编码列·D-148·见文末登记节）  ",
     "＋G39 增补（2026-09-16：按天计租落地·stockEvents 新实体＋5 实体增量字段＋feeCols 编码列·D-148·见文末登记节）＋G41 订正（2026-09-16：实体计数 43→**42**〔实测 demo-data 顶层键·含 products〕＋assetTracks 退役注记）  ",
     "A05 版本行"),
    ("> **统计**：实体 43 ｜",
     "> **统计**：实体 42（G41 订正·实测 `_data/demo-data.js` 顶层键 42；前值 43 系将 `assetTracks` 计入——该实体对象开键行已缺失·数据散键留档·见其节注记） ｜",
     "A05 统计行"),
    ("### assetTracks · 资产轨迹\n\n记录数 10 ｜ 消费页面：库存查询（仓储作业/库存查询.html）",
     "### assetTracks · 资产轨迹（**已退役·G41 T3 登记**）\n\n> ⚠ **退役注记（2026-09-16 G41）**：本实体在 `_data/demo-data.js` 中的**对象开键行已缺失**（历史批次施工丢失）——其 10 行数据以散键形态留档于 `DEMO_DATA` 顶层（语法合法·`node --check` 0）。消费方 `器具出租履历.html` 有 `|| {}` 守卫回退 `rentTracks`、库存查询 openTrack 跳履历页正常——**运行时无缺陷表现**。开键补回或数据正式移除留专门任务处置（G41 零业务改动红线不动作）。\n\n记录数 10 ｜ 消费页面：~~库存查询~~（现跳 器具出租履历.html·回退 rentTracks）",
     "A05 assetTracks 退役注记"),
])

# ---------------- A06 ----------------
A06 = BASE + r"\P3-R01-A06-实体关系与状态机.md"
edit(A06, [
    ("## 1. 实体分域清单（37 实体）",
     "## 1. 实体分域清单（42 实体·G41 订正实测 2026-09-16；37＝G16 时点，此后 +productTaxes〔09-11〕+purchaseReturns/salesReturns/refunds〔G33〕+transferOutbounds〔G37〕+stockEvents〔G39〕，assetTracks 开键缺失退役不计入）",
     "A06 §1 标题"),
    ("| 基础资料 | `bomList` | BOM 列表 | 基础数据/BOM.html | 6 |",
     "| 基础资料 | `bomList` | BOM 列表 | 基础数据/BOM.html | 6 |\n| 基础资料 | `productTaxes` | 供应商税率 | 基础数据/产品档案.html（税率行编辑器·09-11 增） | 5 |",
     "A06 +productTaxes"),
    ("| 采购 | `purchaseInbounds` | 采购入库 | 采购管理/采购入库列表.html | 8 |",
     "| 采购 | `purchaseInbounds` | 采购入库 | 采购管理/采购入库列表.html | 8 |\n| 采购 | `purchaseReturns` | 采购退货单 | 采购管理/采购退货单列表.html（G33·方案 B） | 3 |",
     "A06 +purchaseReturns"),
    ("| 销售 | `salesOutbounds` | 销售出库 | 销售管理/销售出库列表.html | 6 |",
     "| 销售 | `salesOutbounds` | 销售出库 | 销售管理/销售出库列表.html | 6 |\n| 销售 | `salesReturns` | 销售退货单 | 销售管理/销售退货单列表.html（G33·方案 B） | 3 |",
     "A06 +salesReturns"),
    ("| 租赁·租出 | `returnInbounds` | 退租入库 | 租赁管理/退租入库列表.html | 8 |",
     "| 租赁·租出 | `returnInbounds` | 退租入库 | 租赁管理/退租入库列表.html | 8 |\n| 租赁·租出 | `transferOutbounds` | 转移出库单 | 租赁管理/转移出库列表.html（G37·D-146·状态流 待转移→已转移→已终止） | 5 |",
     "A06 +transferOutbounds"),
    ("| 仓储 | `stockFlows` | 库存查询 | 仓储作业/库存查询.html | 16 |",
     "| 仓储 | `stockFlows` | 库存查询 | 仓储作业/库存查询.html | 16 |\n| 仓储 | `stockEvents` | 在租量事件流水 | 派生每日在租量·无独立页面（G39·D-148·不勾稽 D-106） | 22 |",
     "A06 +stockEvents"),
    ("| 仓储 | `assetTracks` | 资产轨迹 | 库存查询·资产轨迹弹窗 | 10 |",
     "| 仓储 | ~~`assetTracks`~~ | 资产轨迹（**已退役**·对象开键缺失·数据散键留档·G41 登记；消费回退 rentTracks） | — | 10 |",
     "A06 assetTracks 退役"),
    ("| 财务 | `writeoffs` | 银行回单核销 | 财务协同/银行回单核销.html | 4 |",
     "| 财务 | `writeoffs` | 银行回单核销 | 财务协同/银行回单核销.html | 4 |\n| 财务 | `refunds` | 退款登记 | 财务协同/退款登记.html（G33·一页双向：应付退款对供应商／应收退款对客户） | 3 |",
     "A06 +refunds"),
    ("### 3.2 库存状态（stockFlows · 口径漂移注记）",
     "### 3.2 库存状态（stockFlows · 口径漂移注记）\n\n> **状态驱动方（G41 补·D-146）**：五态之外「客户转租出」由**转移出库单审核驱动**（行内「转移出库」跳转移出库新建·「终止转移」后回「在客户（租出）」）；原「转租登记弹窗/拉表改状态」交互已退场（D-78 被替代）。转移出库不勾稽原租赁单（D-106）·结算两模式见 P2-R01 D-132（按租出＝默认不进财务链路／按终端＝特例·账单主体切终端·历史不回改）。",
     "A06 §3.2 状态驱动方"),
])
print("A05/A06 编辑全部落盘")
