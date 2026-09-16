# -*- coding: utf-8 -*-
"""G41 T4：A02 内部对齐（132/v6 现行·旧数转沿革）＋A06 html 孪生件实体数同步。"""
import io

BASE = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
A02 = BASE + r"\P3-R01-A02-页面类型与入口对照表.md"
A06H = BASE + r"\P3-R01-A06-实体关系与状态机.html"

c = io.open(A02, encoding="utf-8", newline="").read()
lines = c.split("\n")

def replace_line(prefix, new, tag):
    for i, l in enumerate(lines):
        if l.startswith(prefix):
            lines[i] = new
            print("[OK] %s (L%d)" % (tag, i + 1))
            return
    raise AssertionError("未找到行首锚: %s" % tag)

# E1 日期行追加 v6.3/v6.4
for i, l in enumerate(lines):
    if l.startswith("> **日期**："):
        assert "字段登记见 A05 G39 节）" in l
        lines[i] = l + ("｜ 2026-09-16 v6.3 增订（**G40 原型侧变更包·D-149**：财务协同 5 文件改名〔收款登记/收款详情/损益报表/银行回单核销/银行回单核销详情〕＋引用同步·零页面增删 132 不变；F01 v3.7）"
                        "｜ 2026-09-16 v6.4 增订（**G41 文档收口·D-150**：A02 内部对齐——范围行 128→132〔PC 127＝功能页 121＋模板 3＋F01＋登录＋A06 渲染页〕·模板 67→3·菜单树标题 v3.5→v6 并依活页面侧边栏重列 37 项〔补缺失的租入管理组行〕·实体 41→42·§三标题 38→121；v6 行「128→131」勘误＝G37 基线误计·实测 132；F01 v3.8〔转移出库自 L1/L3 抽离独立支线 S7·道远 09-16 拍板〕）")
        print("[OK] 日期行 v6.3/v6.4 (L%d)" % (i + 1))
        break
else:
    raise AssertionError("日期行未找到")

# E2-E6 行级替换
replace_line("> **范围**：**128 个 HTML**",
    "> **范围**：**132 个 HTML** = PC 端 127（**121 功能页**〔菜单内 37＋菜单外 84·G41 实测〕 + **3 独立弹窗模板**〔基础数据/弹窗/停用确认＋系统管理/弹窗/停用确认＋系统管理/弹窗/重置密码确认〕 + F01 导航图 + **登录页** + **A06 实体关系图渲染页**）+ **移动端 H5 5 页（`mobile/`，G14 新增·G19a 规范化，见第七节）**；页面自包含，数据驱动页另挂 `_data/` 六件（mobile/ 页共用同一 `../_data/demo-data.js` 只读复用；41 业务页统一挂 `pc-auth.js` 默认登录态守卫·G19b）；**A06 渲染页**=`P3-R01-A06-实体关系与状态机.html`（原型根·7 图·内嵌 mermaid 离线可用·不入菜单不进业务页计数·G16a）",
    "范围行 132")
replace_line("- **53 业务页**",
    "- **121 功能页**（PC·含菜单外·2026-09-16 G41 实测）：菜单内 37（菜单 v6 37 项一一对应）＋菜单外 84。沿革：G36 B1 前 41 业务页→G36 全量页面化＋G37 转移出库 3 页后至 121；B1 期类型分布沿革见第五节增订记录",
    "功能页 bullet")
replace_line("- **菜单外页面 18 个**",
    "- **菜单外页面 84 个**（G41 实测；沿革：G36 B1 期 18→B2-B5 页面化 62＋G37 转移出库新建/单详情·出货单打印等，见第五节增订）例如：项目详情（档案行内「详情」）、采购入库录单、租赁出库录单、盘点录入（入口=盘点列表按钮，v3.1 起退出菜单）、BOM维护（BOM 行内「维护」）",
    "菜单外 bullet")
replace_line("- **67 独立弹窗模板**",
    "- **3 独立弹窗模板**（现行＝基础数据/弹窗/停用确认＋系统管理/弹窗/停用确认＋系统管理/弹窗/重置密码确认·G41 实测；沿革：v5 期 79→67→G36 B2-B5 全量页面化 22→4→G37 后实测 3；纯二次确认类保留弹窗载体）：与页内弹层双层同步维护（页面内 modal-overlay 为运行态，`弹窗/` 同名模板可独立打开演示）；详情类弹窗为 `_data/` 数据驱动（改内容=改 demo-data.js，不改页面 H",
    "模板 bullet")
replace_line("- 入口覆盖：38 业务页",
    "- 入口覆盖：121 功能页全部有菜单或按钮入口可达（菜单内 37 页一一对应菜单 v6；菜单外 84 页由列表行内/详情/待办等入口可达·audit 死链 0 背书）",
    "入口覆盖 bullet")
replace_line("- **数据驱动**：`_data/demo-data.js` 41 实体",
    "- **数据驱动**：`_data/demo-data.js` **42 实体**（G41 实测顶层键·含 stockEvents〔G39〕/transferOutbounds〔G37〕/purchaseReturns·salesReturns·refunds〔G33〕/productTaxes〔09-11〕；`assetTracks` 开键缺失退役留档不计入——见 A05/A06 注记）+ list-generic.js / detail-generic.js / receivable-bill-",
    "实体 bullet")

# E7 菜单树标题+整表替换
for i, l in enumerate(lines):
    if l.startswith("## 二、菜单树（v3.5"):
        lines[i] = "## 二、菜单树（v6 · 37 项 · 九组序 · 全站侧边栏统一·G41 依活页面侧边栏实测重列）"
        break
else:
    raise AssertionError("菜单树标题未找到")

start = end = None
for i, l in enumerate(lines):
    if l.startswith("| # | 组（序）"):
        start = i
    if start is not None and l.startswith("| 10 | 系统管理"):
        end = i
        break
assert start is not None and end is not None, "菜单表边界未找到"
new_table = """| # | 组（序） | 菜单项 → 页面文件 |
|---|---|---|
| 1 | 项目管理 | 项目看板 → `首页/项目看板.html`；项目列表 → `项目管理/项目档案.html` |
| 2 | 我的待办（一级直达） | 我的待办 → `我的待办.html` |
| 3 | 基础资料 | 客商管理 → `基础数据/客商管理.html`；物料档案 → `基础数据/产品档案.html`；BOM → `基础数据/BOM.html`；库位档案 → `基础数据/库位档案.html` |
| 4 | 采购管理 | 采购订单 → `采购管理/采购订单列表.html`；采购入库 → `采购管理/采购入库列表.html`；采购退货 → `采购管理/采购退货单列表.html`（G33 v5） |
| 5 | 销售管理 | 销售订单 → `销售管理/销售订单列表.html`；销售出库 → `销售管理/销售出库列表.html`；销售退货 → `销售管理/销售退货单列表.html`（G33 v5） |
| 6 | 租赁管理 | 租赁单 → `租赁管理/租赁单列表.html`；租赁出库 → `租赁管理/租赁出库列表.html`；转移出库 → `租赁管理/转移出库列表.html`（G37 v6·客户转租承载·D-146）；退租入库 → `租赁管理/退租入库列表.html` |
| 7 | 租入管理 | 租入单 → `租入管理/租入单列表.html`；租入入库 → `租入管理/租入入库列表.html`；租入归还 → `租入管理/租入归还列表.html` |
| 8 | 仓储管理（目录仍 `仓储作业/`） | 库存查询 → `仓储作业/库存查询.html`；盘点记录 → `仓储作业/盘点列表.html`；库存调拨 → `仓储作业/库存调拨列表.html`；其他入库 → `仓储作业/其他入库列表.html`；其他出库 → `仓储作业/其他出库列表.html` |
| 9 | 财务管理（目录仍 `财务协同/`） | **财务看板（组首普通项·v3.5 移位改名，原「项目损益」）** → `财务协同/损益报表.html`；应收账单 → `财务协同/应收账单.html`；开票登记 → `财务协同/开票登记.html`；收款登记（原「回款登记」·G40 改名 D-142）→ `财务协同/收款登记.html`；收款核销（页面 银行回单核销.html·G40 改名）→ `财务协同/银行回单核销.html`；应付账单 → `财务协同/应付账单.html`；付款登记 → `财务协同/付款登记.html`；退款登记 → `财务协同/退款登记.html`（G33 v5） |
| 10 | 系统管理 | 用户权限 → `系统管理/用户权限.html`；**角色管理（v3.1 独立菜单）** → `系统管理/角色管理.html`；操作日志 → `系统管理/操作日志.html`；数据字典 → `系统管理/数据字典.html` |"""
lines[start:end + 1] = new_table.split("\n")
print("[OK] 菜单树整表 v6 重列（L%d-L%d）" % (start + 1, end + 1))

# E8 §三标题
for i, l in enumerate(lines):
    if l.startswith("## 三、页面类型清单（38 业务页）"):
        lines[i] = "## 三、页面类型清单（121 功能页·G41 实测；沿革 38＝G35 前业务页口径，G36 起页面化增量与菜单外表随版入列）"
        print("[OK] §三标题 (L%d)" % (i + 1))
        break
else:
    raise AssertionError("§三标题未找到")

io.open(A02, "w", encoding="utf-8", newline="").write("\n".join(lines))

# ---- A06 html 孪生件 ----
h = io.open(A06H, encoding="utf-8", newline="").read()
assert h.count("37_实体") == 2 and h.count("37 实体") == 2, "A06 html 锚点异常: %d/%d" % (h.count("37_实体"), h.count("37 实体"))
h = h.replace("37_实体", "42_实体").replace("37 实体", "42 实体")
io.open(A06H, "w", encoding="utf-8", newline="").write(h)
print("[OK] A06 html 37→42 ×2（含 toc 锚 id 同步）")

# ---- 自检 ----
c2 = io.open(A02, encoding="utf-8").read()
checks = {
    "132 个 HTML": c2.count("132 个 HTML") >= 1,
    "v6.4 增订": "v6.4 增订" in c2,
    "租入管理组行": "| 7 | 租入管理 |" in c2,
    "121 功能页": "121 功能页" in c2,
    "42 实体": "42 实体" in c2,
    "残留「67 独立」": "67 独立" not in c2,
    "残留「53 业务页」": "53 业务页" not in c2,
}
for k, v in checks.items():
    print(("[PASS] " if v else "[FAIL] ") + k)
assert all(checks.values())
print("A02 内部对齐完成")
