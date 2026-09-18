# G53「单据三态三卡版式全站铺开」独立验收复验（只读）

- 验收员角色：只读独立复验，未改动任何仓库文件；本目录（`_scan_tmpdir/g53_accept/`）为唯一写入区。
- 复验时间：2026-09-18
- 复验对象：`P3-R01-包装租赁管理后台原型/_data/demo-data.js`（G53 三卡版式改造）+ 8 个详情页渲染
- 复验工具：node v24.14.2（`node --check`、DEMO_DATA 加载遍历）、Python 3.14.2 + Playwright Chromium（headless，file:// 直开）
- 本目录产物：`check_data.py` / `check_data.node.js` / `check_data.out.json`（③⑤数据面）、`check_render.py` / `check_render.out.json`（②渲染面）、本 `verify.md`

---

## ①【语法门】——PASS

- 命令：`node --check "P3-R01-包装租赁管理后台原型\_data\demo-data.js"`
- 结果：退出码 **0**，无任何输出（无语法错误）。

## ②【渲染抽验 8 实体】——PASS（8/8 页全过，四断言全绿）

Playwright Chromium headless 逐页 `file://…?id=<键>` 打开，每页断言 (a) 无 pageerror/console error、(b) `#detailBody > .fm-card` ≥2 且首卡标题=期望 formTitle、(c) 明细卡 thead 前三列=期望三列、(d) 「流转信息」卡存在且 `.chain`/`.tl` 至少一个非空。8 页 `cardCount` 均为 3（信息卡+明细卡+流转卡），chain/tl 双双非空，pageErrors=consoleErrors=0。

| 单号 | 页面 | 首卡标题 | 明细卡 thead 前三列 | 流转卡(chain/tl) | 错误 | 判定 |
|---|---|---|---|---|---|---|
| PO-20260902-018 | 采购管理/采购订单详情.html | 订单信息 | 序号/物料编码/物料名称 | 4节点/非空 | 0/0 | PASS |
| ZL-20260823-033 | 租赁管理/租赁单详情.html | 租赁信息 | 序号/物料编码/物料名称 | 非空 | 0/0 | PASS |
| ZY-20260915-005 | 租赁管理/转移出库单详情.html | 转移信息 | 序号/物料编码/物料名称 | 非空 | 0/0 | PASS |
| QTCK-20260905-005 | 仓储作业/其他出库详情.html | 出库信息 | 序号/物料编码/物料名称 | 非空 | 0/0 | PASS |
| HK-20260830-014 | 财务协同/收款详情.html | 收款信息 | 关联账单/费用项/本次收款(元) | 非空 | 0/0 | PASS |
| CGRK-20260828-012 | 采购管理/采购入库详情.html | 基本信息 | 序号/物料编码/物料名称 | 4节点/5条/非空 | 0/0 | PASS |
| CK-20260910-022 | 租赁管理/租赁出库详情.html | 基本信息 | 序号/组合件编码/组合件名称 | 3节点/非空 | 0/0 | PASS |
| INV-20260902-013 | 财务协同/开票详情.html | 开票信息 | 费用项/关联账单/税率 | 3节点/非空 | 0/0 | PASS |

明细：PO 页卡序=[订单信息, 采购明细, 流转信息]；HK 页首三列[关联账单, 费用项, 本次收款(元)]；INV 页 itemTh=[费用项, 关联账单, 税率, 开票金额(元)]。完整探针数据见 `check_render.out.json`。

## ③【命名统一 grep 抽验 6 组】——PASS

node 加载 DEMO_DATA 后，在 20 实体（purchaseOrders…refunds，不含 transfers/payableBills/receivableBills/writeoffs）每条记录的 `formRows`+`items` JSON 内检索：

- 旧标签 0 命中（四项全零）：
  - `关联原单` = **0**；`送达地点` = **0**；`价税合计` = **0**；`验收方式` = **0**
- 新命名各 ≥1 命中（在指定实体 formRows 的 label 精确匹配，括号为命中记录数）：
  - `关联采购入库` @purchaseReturns = **3**（3/3 全覆盖）
  - `关联销售订单号` @purchaseOrders = **7**（7/7 全覆盖）
  - `收货地点` @comboOutbounds = **10**（10/10 全覆盖）
  - `退回日期` @returnInbounds = **10**（10/10 全覆盖）
  - `盘点日期` @stocktakes = **5**（5/5 全覆盖）
  - `开票金额` @invoices = **6**（6/6 全覆盖）

20 实体记录数：7/8/3/6/3/3/9/10/10/5/5/3/5/8/7/3/5/5/6/4，共 115 条，全部在检索范围内。

## ④【改动面】——PASS（原型目录内非 mobile 的 .html 改动 = 0）

`git -c core.quotepath=false status --porcelain` 中 `P3-R01-包装租赁管理后台原型` 内全部 .html 改动仅以下 5 条，**均位于 `mobile/` 子目录**（按验收口径不算原型 PC 页改动；亦非审核页/详情页）：

- M `P3-R01-包装租赁管理后台原型/mobile/审批详情.html`
- M `P3-R01-包装租赁管理后台原型/mobile/库存查询.html`
- M `P3-R01-包装租赁管理后台原型/mobile/待办审批.html`
- M `P3-R01-包装租赁管理后台原型/mobile/我的.html`
- M `P3-R01-包装租赁管理后台原型/mobile/登录.html`

原型目录（剔除 mobile/）内 M/A/D 的 .html 计数 = **0**（过滤命令 `grep 'P3-R01' | grep -v 'mobile/'` 无输出）。原型目录内的其余改动为预期数据面文件：M `_data/demo-data.js`、M `P3-R01-A05-字段字典.md`，以及 3 个未跟踪 zip 包（并行残留）。

如实列出的**非原型目录** M html（与本任务无关的并行残留）：
- 根目录：M `2026-09-16 汽车物流包装租赁现有管理不合理清单.html`
- `skills/diagram-design/`：M `assets/template.html`、`assets/template-dark.html`、`assets/template-full.html`；D 约 44 个 `assets/example-*.html` 及 `assets/index.html`、`output/flowchart-decision.html`；?? 新增 `assets/template-motion.html`、`assets/template-terminal.html`

## ⑤【items 行长抽样 + 全量】——PASS

node 加载 DEMO_DATA（实体为按单号键控的 map，记录字段 row/title/formTitle/formRows/itemTitle/itemCols/items/chain/timeline）：

- 抽样 3 条（期望完全吻合）：
  - purchaseInbounds `CGRK-20260828-012`：itemCols=**12** 列，items=**2** 行，行长 [12,12]，全部一致 ✓（明细题=到货明细）
  - returnInbounds `TZRK-20260902-008`：itemCols=**8** 列，items=**3** 行，行长 [8,8,8]，全部一致 ✓（明细题=退回明细）
  - leaseOrders `ZL-20260823-033`：itemCols=**11** 列，items=**1** 行，行长 [11]，一致 ✓（明细题=租赁明细）
- 全量断言：20 实体 × **115** 条记录 × **129** 行明细，行长度 ≠ itemCols 长度的 = **0**（无 notArray、无错位）。

---

## 总判定：5 PASS / 0 FAIL

| # | 检查项 | 判定 |
|---|---|---|
| ① | 语法门 node --check | PASS |
| ② | 渲染抽验 8 实体（4 断言 × 8 页） | PASS |
| ③ | 命名统一（旧 0 命中 + 新 ≥1 命中 ×6） | PASS |
| ④ | 改动面（原型非 mobile .html = 0） | PASS |
| ⑤ | items 行长抽样 3 条 + 20 实体全量 | PASS |
