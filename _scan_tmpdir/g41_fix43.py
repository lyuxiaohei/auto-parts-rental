# -*- coding: utf-8 -*-
"""G41 实体数回订 42→43：node 仲裁推翻首版「assetTracks 开键缺失」判断——开键与块注释同行尾（基线已记陷阱）·A05 原声明 43 正确。"""
import io, os, re

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
P = lambda *p: os.path.join(ROOT, *p)

def ro(fp, pairs):
    c = io.open(fp, encoding="utf-8", newline="").read()
    for old, new, tag in pairs:
        n = c.count(old)
        assert n == 1, "[%s] %s 命中 %d" % (os.path.basename(fp), tag, n)
        c = c.replace(old, new)
        print("[OK] %s · %s" % (os.path.basename(fp), tag))
    io.open(fp, "w", encoding="utf-8", newline="").write(c)

# ---- A05 ----
ro(P("P3-R01-包装租赁管理后台原型", "P3-R01-A05-字段字典.md"), [
    ("＋G41 订正（2026-09-16：实体计数 43→**42**〔实测 demo-data 顶层键·含 products〕＋assetTracks 退役注记）",
     "＋G41 复核（2026-09-16：实体计数 node 运行时仲裁＝**43 确认**（44 键−_meta·含 assetTracks）——首判 42 系正则漏计〔assetTracks 开键与块注释同行尾·基线已知陷阱〕·复验轮纠正）",
     "版本行"),
    ("> **统计**：实体 42（G41 订正·实测 `_data/demo-data.js` 顶层键 42；前值 43 系将 `assetTracks` 计入——该实体对象开键行已缺失·数据散键留档·见其节注记） ｜",
     "> **统计**：实体 43（node 运行时仲裁：44 键−_meta＝43·含 `assetTracks`——**声明与实测一致**；沿革：G41 首轮正则漏计误判 42·复验轮 node 仲裁纠正） ｜",
     "统计行"),
    ("### assetTracks · 资产轨迹（**已退役·G41 T3 登记**）\n\n> ⚠ **退役注记（2026-09-16 G41）**：本实体在 `_data/demo-data.js` 中的**对象开键行已缺失**（历史批次施工丢失）——其 10 行数据以散键形态留档于 `DEMO_DATA` 顶层（语法合法·`node --check` 0）。消费方 `器具出租履历.html` 有 `|| {}` 守卫回退 `rentTracks`、库存查询 openTrack 跳履历页正常——**运行时无缺陷表现**。开键补回或数据正式移除留专门任务处置（G41 零业务改动红线不动作）。\n\n记录数 10 ｜ 消费页面：~~库存查询~~（现跳 器具出租履历.html·回退 rentTracks）",
     "### assetTracks · 资产轨迹（**现行有效**·检查注记见下）\n\n> ℹ **检查注记（2026-09-16 G41·复验轮纠正）**：本实体开键与块注释**同行尾**（`…渲染 */assetTracks: {`）——朴素缩进正则会漏计（基线已记陷阱·G41 首轮即因此误判「开键缺失」并误判实体 42·node 运行时仲裁纠正：`DEMO_DATA.assetTracks` 正常挂载 10 行）。消费页 `器具出租履历.html` 优先读本实体（`rentTracks` 为防御性回退）。\n\n记录数 10 ｜ 消费页面：租赁管理/器具出租履历.html（库存查询 openTrack 跳转）",
     "assetTracks 节纠正"),
])

# ---- A06 md ----
ro(P("P3-R01-包装租赁管理后台原型", "P3-R01-A06-实体关系与状态机.md"), [
    ("## 1. 实体分域清单（42 实体·G41 订正实测 2026-09-16；37＝G16 时点，此后 +productTaxes〔09-11〕+purchaseReturns/salesReturns/refunds〔G33〕+transferOutbounds〔G37〕+stockEvents〔G39〕，assetTracks 开键缺失退役不计入）",
     "## 1. 实体分域清单（43 实体·G41 复核实测 2026-09-16·node 仲裁；37＝G16 时点，此后 +productTaxes〔09-11〕+purchaseReturns/salesReturns/refunds〔G33〕+transferOutbounds〔G37〕+stockEvents〔G39〕）",
     "§1 标题"),
    ("| 仓储 | ~~`assetTracks`~~ | 资产轨迹（**已退役**·对象开键缺失·数据散键留档·G41 登记；消费回退 rentTracks） | — | 10 |",
     "| 仓储 | `assetTracks` | 资产轨迹（现行·开键与块注释同行尾易漏计——G41 检查注记） | 器具出租履历.html（库存查询 openTrack） | 10 |",
     "assetTracks 行纠正"),
])

# ---- A06 html ----
fp = P("P3-R01-包装租赁管理后台原型", "P3-R01-A06-实体关系与状态机.html")
c = io.open(fp, encoding="utf-8", newline="").read()
assert c.count("42_实体") == 2 and c.count("42 实体") == 2
c = c.replace("42_实体", "43_实体").replace("42 实体", "43 实体")
io.open(fp, "w", encoding="utf-8", newline="").write(c)
print("[OK] A06 html 42→43 ×2")

# ---- A02 ----
ro(P("P3-R01-包装租赁管理后台原型", "P3-R01-A02-页面类型与入口对照表.md"), [
    ("- **数据驱动**：`_data/demo-data.js` **42 实体**（G41 实测顶层键·含 stockEvents〔G39〕/transferOutbounds〔G37〕/purchaseReturns·salesReturns·refunds〔G33〕/productTaxes〔09-11〕；`assetTracks` 开键缺失退役留档不计入——见 A05/A06 注记）+ list-generic.js",
     "- **数据驱动**：`_data/demo-data.js` **43 实体**（G41 node 仲裁·含 assetTracks〔其开键与块注释同行尾·正则易漏计〕＋stockEvents〔G39〕/transferOutbounds〔G37〕/purchaseReturns·salesReturns·refunds〔G33〕/productTaxes〔09-11〕）+ list-generic.js",
     "实体 bullet 43"),
])

# ---- P2-R01 D-150 行 ----
ro(P("P2-R01-产品需求文档.md"), [
    ("＋A05 实体计数订正（声明 43→**实测 42**·demo-data 顶层键实测＋assetTracks 死节退役注记）",
     "＋A05 实体计数复核（**实测 43＝原声明**·node 运行时仲裁含 assetTracks——其开键与注释同行致首轮正则误判 42·复验轮纠正＋节检查注记）",
     "D-150 行"),
])

# ---- 基线追记 ----
ro(P("agent-handoff", "_AGENT基线.md"), [
    ("**A05** 实体计数订正 43→**42**（实测 demo-data 顶层键·assetTracks 开键缺失退役注记＝结构性瑕疵登记不修）｜**A06** 名册 37→42＋补 transferOutbounds/stockEvents/库存状态驱动方（.md＋.html 孪生件）",
     "**A05** 实体计数复核 **43 确认**（node 运行时仲裁·assetTracks 开键与注释同行易漏计——首轮误判 42 已纠正＋节检查注记）｜**A06** 名册 37→43＋补 transferOutbounds/stockEvents/库存状态驱动方（.md＋.html 孪生件）",
     "基线追记"),
])

# ---- 索引 G41 行 ----
ro(P("agent-handoff", "_索引.md"), [
    ("T3 A05 43→**42**（实测·assetTracks 退役注记）＋A06 补 transferOutbounds/stockEvents/状态驱动方",
     "T3 A05 实体复核 **43 确认**（node 仲裁·assetTracks 同行键陷阱纠正）＋A06 名册 43＋补 transferOutbounds/stockEvents/状态驱动方",
     "索引摘要"),
])

print("六件回改完成")
