# -*- coding: utf-8 -*-
"""G16 T3: 生成 P3-R01-A06-实体关系与状态机.md
数据派生部分（实体清单/行数/状态枚举）取自 g16_data_dump.json；关系表为策展+证据列（D8 宁缺毋滥）。
"""
import json, pathlib, collections, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROT = ROOT / 'P3-R01-包装租赁管理后台原型'
D = json.loads((ROOT / '_scan_tmpdir/g16_data_dump.json').read_text(encoding='utf-8'))

ENT_CN = {'payableBills':'应付账单','receivableBills':'应收账单','payments':'付款登记','receipts':'回款登记',
'invoices':'开票登记','writeoffs':'银行水单核销','leaseOrders':'租赁单','rentInOrders':'租入单',
'comboOutbounds':'租赁出库(组合出库)','returnInbounds':'退租入库','rentInReturns':'租入归还',
'rentInbounds':'租入入库','purchaseOrders':'采购订单','salesOrders':'销售订单','purchaseInbounds':'采购入库',
'salesOutbounds':'销售出库','otherInbounds':'其他入库','otherOutbounds':'其他出库','stocktakes':'盘点记录',
'transfers':'库存调拨','stockFlows':'库存查询','rentTracks':'出租履历','assetTracks':'资产轨迹',
'partners':'客商','products':'物料档案','locations':'库位档案','bomVersions':'BOM 维护','bomList':'BOM 列表',
'roles':'角色','opLogs':'操作日志','users':'用户','dictItems':'数据字典项','todoItems':'我的待办',
'projects':'项目档案','projectDocs':'项目详情','boardRows':'项目看板','profitRows':'项目损益'}
PAGE = {'payableBills':'财务协同/应付账单.html','receivableBills':'财务协同/应收账单.html','payments':'财务协同/付款登记.html',
'receipts':'财务协同/回款登记.html','invoices':'财务协同/开票登记.html','writeoffs':'财务协同/银行水单核销.html',
'leaseOrders':'租赁管理/租赁单列表.html','rentInOrders':'租赁管理/租入单列表.html',
'comboOutbounds':'租赁管理/组合出库列表.html','returnInbounds':'租赁管理/退租入库列表.html',
'rentInReturns':'租赁管理/租入归还列表.html','rentInbounds':'租赁管理/租入入库列表.html',
'purchaseOrders':'采购管理/采购订单列表.html','salesOrders':'销售管理/销售订单列表.html',
'purchaseInbounds':'采购管理/采购入库列表.html','salesOutbounds':'销售管理/销售出库列表.html',
'otherInbounds':'仓储作业/其他入库列表.html','otherOutbounds':'仓储作业/其他出库列表.html',
'stocktakes':'仓储作业/盘点列表.html','transfers':'仓储作业/库存调拨列表.html','stockFlows':'仓储作业/库存查询.html',
'rentTracks':'库存查询·出租履历弹窗','assetTracks':'库存查询·资产轨迹弹窗','partners':'基础数据/客商管理.html',
'products':'基础数据/产品档案.html','locations':'基础数据/库位档案.html','bomVersions':'基础数据/BOM维护.html',
'bomList':'基础数据/BOM.html','roles':'系统管理/角色管理.html','opLogs':'系统管理/操作日志.html',
'users':'系统管理/用户权限.html','dictItems':'系统管理/数据字典.html','todoItems':'首页/我的待办',
'projects':'项目管理/项目档案.html','projectDocs':'项目管理/项目详情.html','boardRows':'首页/项目看板.html',
'profitRows':'财务协同/盈亏报表.html'}
MODULES = [
 ('基础资料', ['products','partners','locations','bomVersions','bomList','dictItems']),
 ('项目管理', ['projects','projectDocs','boardRows']),
 ('采购', ['purchaseOrders','purchaseInbounds']),
 ('销售', ['salesOrders','salesOutbounds']),
 ('租赁·租出', ['leaseOrders','comboOutbounds','returnInbounds','rentTracks']),
 ('租赁·租入', ['rentInOrders','rentInbounds','rentInReturns']),
 ('仓储', ['otherInbounds','otherOutbounds','stocktakes','transfers','stockFlows','assetTracks']),
 ('财务', ['payableBills','receivableBills','payments','receipts','invoices','writeoffs','profitRows']),
 ('系统', ['roles','users','opLogs','todoItems']),
]

# 状态枚举（数据派生）
def status_enum(ent):
    vals = []
    for rk, rec in D[ent].items():
        st = (rec.get('row', {}).get('fields') or {}).get('status') or rec.get('status')
        if isinstance(st, str) and st not in vals: vals.append(st)
    return vals

L = []
L.append('# P3-R01-A06 · 实体关系与状态机')
L.append('')
L.append('> **版本**：V1.0（2026-09-11 · G16 生成）  ')
L.append(f'> **统计**：实体 {len(ENT_CN)}（demo-data 全量）｜ 关系 {26} 条（逐条带证据）｜ 状态机 3 组  ')
L.append('> **来源**：`_data/demo-data.js` dump（`g16_data_dump.json`）互引扫描 + 页面消费关系；生成脚本 `_scan_tmpdir/g16_t3_gen.py`。  ')
L.append('> **姊妹篇**：`P3-R01-A05-字段字典.md`（实体→字段级）；页面层演示见 `系统管理/数据字典.html`（仅 dictItems 子集）。')
L.append('')
L.append('## 1. 实体分域清单（37 实体）')
L.append('')
L.append('| 域 | 实体键 | 中文名 | 承载页面 | 行数 |')
L.append('|---|---|---|---|---|')
for mod, ents in MODULES:
    for e in ents:
        L.append(f'| {mod} | `{e}` | {ENT_CN[e]} | {PAGE[e]} | {len(D[e])} |')
L.append('')
L.append('> 建模约定（demo-data 头注）：**单号即外键**——实体间用单号互引不复制数据；`_key`（记录键）=单号/编码。')
L.append('')
L.append('## 2. 核心关系表（26 条 · 逐条证据）')
L.append('')
L.append('> 证据类型：`数据`=dump 记录内单号/编码互引（括注引用记录数）；`页面`=页面列/弹窗/注记；关系方向 A→B=A 持 B 的引用。')
L.append('')
L.append('| # | 关系 | 类型 | 证据 |')
L.append('|---|---|---|---|')
REL = [
 ('projects ↔ partners（上下游绑定）', 'M:N', '页面=上下游绑定.html 多选弹窗+项目档案绑定区+新建租入单/采购订单选项目→供应商候选=绑定集合（2026-09-11 落地）；**数据层未落**：projects 无 suppliers 字段（缺口 #4）'),
 ('partners → products（供应商税率维护区）', '1:N', '数据=products 6/12 行带 supplier 名（苏州联恒/宁波华塑/常州正大）；名字外键（缺口 #3）'),
 ('partners → purchaseOrders', '1:N', '数据=partners 3 条记录被 PO- 引用；purchaseOrders.fields.supplier=供应商名'),
 ('partners → rentInOrders / payableBills', '1:N', '数据=payableBills.fields.supplier（11 行）；rentInOrders 供应商=路凯（A04 流程链 L3）'),
 ('partners → leaseOrders / receivableBills（客户侧）', '1:N', '数据=leaseOrders.fields.customer=客户名（9 行）；receivableBills 客户维度——名字外键同缺口 #3'),
 ('projects → leaseOrders / rentInOrders / purchaseOrders / salesOrders / stockFlows', '1:N', '数据=PRJ- 引用：leaseOrders 9/9、salesOrders 8/8、purchaseInbounds 8/8、payableBills 10/11、stockFlows fields.project、comboOutbounds 8/8、returnInbounds 8/8、salesOutbounds 6/6、assetTracks 8/10、profitRows 6/6（所属项目字段/筛选）'),
 ('projects → boardRows（看板行=项目键直连）', '1:1', '数据=boardRows._key=PRJ-2601…（6 行=6 项目）'),
 ('projects → projectDocs（项目详情档案）', '1:N', '数据=projectDocs 记录按 PRJ- 分组挂项目（11 行）'),
 ('bomVersions → bomList（版本挂父项）', 'N:1', '数据=bomVersions 3/3 条 info.父项编码=ZH-2601-A（V1.0/V2.0/V2.1）'),
 ('bomList 自引用（父项⇄子项）', '1:N', '数据=组合件行 ZH-2601-A/B/C 子项=WBX-/PLT-/BTC- 编码；BOM 语义=父项由子项按配比组成（术语表第四节）'),
 ('salesOrders → leaseOrders（代下租赁）', '流程', '页面/流程=订单唯一来源=项目经理代下销售订单（已拍板）；**数据层无 SO- 外键**（leaseOrders 0 行含 SO-）——流程口径非数据关系'),
 ('salesOrders → purchaseOrders', 'N:M', '数据=purchaseOrders 2 行含 SO-（销售联动采购）；页面=采购订单列表 so 筛选列'),
 ('leaseOrders → comboOutbounds（租赁出库）', '1:N', '数据=comboOutbounds 8/8 行含 ZL-（关联租赁单）'),
 ('leaseOrders → returnInbounds（退租入库）', '1:N', '数据=returnInbounds 8/8 行含 ZL-（TZRK- 单引 ZL-，按单退租）'),
 ('rentInOrders → rentInbounds（租入入库）', '1:N', '数据=rentInbounds 3/3 行含 RZD-'),
 ('rentInOrders → rentInReturns（租入归还）', '1:N', '数据=rentInReturns 3/3 行含 RZD-（关联租入单+明细同步+分批）'),
 ('rentInOrders ↔ leaseOrders（客户转租）', 'N:M', '数据=leaseOrders 2 行含 RZD-、rentInOrders 2 行含 ZL-；stockFlows XNC-ZZ-* 3 行状态=客户转租出（2026-09-10 转租演示线）'),
 ('purchaseOrders → purchaseInbounds（采购入库）', '1:N', '数据=purchaseInbounds 8/8 行含 PO-（凭单验收）'),
 ('salesOrders → salesOutbounds（销售出库）', '1:N', '数据=salesOutbounds 6/6 行含 SO-'),
 ('purchaseOrders / rentInOrders / rentInReturns → payableBills（应付四来源）', '1:N', '数据=payableBills btype：采购应付 6/租金应付 2/赔付应付 1/对客户应付 1/预付 1；5 行含 PO-、3 行含 RZD-'),
 ('salesOutbounds / comboOutbounds / 丢损 → receivableBills（应收四来源）', '1:N', '数据=receivableBills btype：租赁费 7/销售费 3（含 XSCK- 引用）/丢损赔偿 1/供应商应收 1/预付款 1/预收 1'),
 ('payableBills → payments（付款分期）', '1:N', '数据=payments 5/5 行含 AP-（分期自由笔数）'),
 ('receivableBills → receipts（收款分期）', '1:N', '数据=receipts 5 行含 AR-（4 记录级）'),
 ('receivableBills → invoices（开票）', '1:N', '数据=invoices 6/6 行含 AR-'),
 ('receivableBills / receipts → writeoffs（水单核销）', 'N:M', '数据=writeoffs 3 行含 AR-；核销=收付款与账单多对多冲抵（银行水单核销页）'),
 ('stocktakes → otherInbounds / otherOutbounds（盘盈亏生成其他出入库）', '1:N', '数据=otherInbounds 1 行含 PD-、otherOutbounds 1 行含 PD-（2026-09-11 盘点联动；关联单据列）'),
 ('locations → stockFlows（客户虚拟仓）', '1:N', '数据=stockFlows XNC-* 4 行键=库位编码 XNC-AJZX（客户在租按客户归集 on-hire 口径）'),
 ('todoItems → 全单据（审核待办）', 'N:1', '数据=todoItems 12 行 docNo 弱引用 SO-/PO-/ZL-/RZD-/TZRK- 等单号+auditor 审核人；我的待办审核人筛选（G13）'),
 ('rentTracks / assetTracks → leaseOrders / projects / products（履历视图）', '视图', '数据=rentTracks 10 行含 ZL-/PRJ-；assetTracks 8/10 含 PRJ-——聚合视图实体，非独立业务对象'),
]
for i, (rel, typ, ev) in enumerate(REL, 1):
    L.append(f'| {i} | {rel} | {typ} | {ev} |')
L.append('')
L.append('## 3. 状态机')
L.append('')
L.append('### 3.1 单据审核流（全模块统一口径 · 术语表第四节）')
L.append('')
L.append('```mermaid')
L.append('stateDiagram-v2')
L.append('    [*] --> 待提交')
L.append('    待提交 --> 待审核: 提交')
L.append('    待审核 --> 待发货: 审核通过')
L.append('    待审核 --> [*]: 驳回')
L.append('    待发货 --> 已完成: 执行完成')
L.append('    已完成 --> 已关闭: 关闭')
L.append('```')
L.append('')
L.append('> 各单据在统一骨架上有**执行态变体**（数据实测枚举）：')
L.append('')
L.append('| 实体 | 实测状态枚举（dump 全量） |')
L.append('|---|---|')
for e in ['salesOrders','purchaseOrders','leaseOrders','rentInOrders','comboOutbounds','salesOutbounds',
          'purchaseInbounds','rentInbounds','returnInbounds','rentInReturns','otherInbounds','otherOutbounds',
          'stocktakes','transfers','payments','receipts','invoices','writeoffs','payableBills','receivableBills']:
    L.append(f'| `{e}` {ENT_CN[e]} | {" / ".join(status_enum(e))} |')
L.append('')
L.append('> 档案类启停：products/partners/locations/bomList=启用/停用；projects=筹备中/进行中/已暂停/已完结。')
L.append('')
L.append('### 3.2 库存状态（stockFlows · 口径漂移注记）')
L.append('')
L.append('| 层 | 枚举 | 出处 |')
L.append('|---|---|---|')
L.append('| **数据实测**（16 行） | 在库 / 客户端(租出) / 客户转租出 / 退租待入库 | dump fields.status（ZH-* 组合行 3 行无状态） |')
L.append('| **页面筛选** | 全部 / 在库 / 客户端(租出) / 客户转租出 / 退租待入库 | 仓储作业/库存查询.html 筛选 select |')
L.append('| **历史口径**（09-08 五态） | 在库 / 在途(退租未审核) / 客户端(租出) / 退租库存 / 租入 | 会议拍板（已拍板不复议区） |')
L.append('')
L.append('> **漂移结论**（G16 实测）：①「在途(退租未审核)」在数据层现名「退租待入库」（同义改名未回写会议口径）；②「退租库存」「租入」两态**无演示行**（缺口 #5）；③「客户转租出」为 09-10 转租演示新增态（会议口径之后产生）。09-11 已拍板**去数量词**（四态/五态字样全站清零 016ac01），口径=「库存状态」不带数字。')
L.append('')
L.append('### 3.3 账单生命周期（四来源 → 分期收付 → 核销）')
L.append('')
L.append('```mermaid')
L.append('flowchart LR')
L.append('    subgraph 应付侧')
L.append('    PO[采购订单] & RZ[租入单/归还] --> AP[应付账单·未付款]')
L.append('    AP -->|部分付款| AP2[部分付款] -->|付清| AP3[已付款]')
L.append('    AP --> PM[付款登记·分期多笔]')
L.append('    end')
L.append('    subgraph 应收侧')
L.append('    SO[销售/租赁出库] --> AR[应收账单·未开票/部分收款]')
L.append('    AR -->|收清| AR2[已结清/已收]')
L.append('    AR --> RC[回款登记] --> WO[水单核销·已核销/部分核销]')
L.append('    AR --> IV[开票登记·已登记/已红冲]')
L.append('    end')
L.append('```')
L.append('')
L.append('## 4. 数据缺口（与 A05 末节同源 · 5 条）')
L.append('')
L.append('1. **采购订单实体无 project 字段**——列表页有「所属项目」筛选+M:N 联动，数据层缺投影字段。')
L.append('2. **stockFlows 无供应商维度**——租入在库无法按供应商查；路凯对账需补 supplier 字段。')
L.append('3. **partners 引用为公司名字符串**非 DW-xxx 编码——演示层名字匹配，正式版须改编码外键。')
L.append('4. **上下游 M:N 绑定未落数据层**（G16 实测）——绑定弹窗 0 处 DEMO_DATA 引用、projects 无 suppliers 字段；正式版须建关系表。')
L.append('5. **库存「租入」「退租库存」两态无演示行**（G16 实测）——含 3.2 节口径漂移三条。')
L.append('')
L.append('## 5. 实体关系图（mermaid 文本）')
L.append('')
L.append('```mermaid')
L.append('erDiagram')
L.append('    PROJECTS ||--o{ LEASE_ORDERS : "所属项目"')
L.append('    PROJECTS ||--o{ RENT_IN_ORDERS : "所属项目"')
L.append('    PROJECTS ||--o{ PURCHASE_ORDERS : "所属项目(数据缺列)"')
L.append('    PROJECTS ||--o{ SALES_ORDERS : "所属项目"')
L.append('    PROJECTS ||--o{ STOCK_FLOWS : "库存行"')
L.append('    PROJECTS }o--o{ PARTNERS : "上下游绑定 M:N(未落数据)"')
L.append('    PARTNERS ||--o{ PRODUCTS : "供应商维护"')
L.append('    PARTNERS ||--o{ PURCHASE_ORDERS : "供应商"')
L.append('    PARTNERS ||--o{ PAYABLE_BILLS : "供应商"')
L.append('    PARTNERS ||--o{ LEASE_ORDERS : "客户"')
L.append('    PARTNERS ||--o{ RECEIVABLE_BILLS : "客户"')
L.append('    SALES_ORDERS ||--o{ LEASE_ORDERS : "代下租赁(流程)"')
L.append('    SALES_ORDERS ||--o{ SALES_OUTBOUNDS : "出库"')
L.append('    SALES_ORDERS ||--o{ PURCHASE_ORDERS : "联动采购"')
L.append('    LEASE_ORDERS ||--o{ COMBO_OUTBOUNDS : "租赁出库"')
L.append('    LEASE_ORDERS ||--o{ RETURN_INBOUNDS : "退租入库"')
L.append('    LEASE_ORDERS }o--o{ RENT_IN_ORDERS : "客户转租"')
L.append('    RENT_IN_ORDERS ||--o{ RENT_INBOUNDS : "租入入库"')
L.append('    RENT_IN_ORDERS ||--o{ RENT_IN_RETURNS : "租入归还"')
L.append('    PURCHASE_ORDERS ||--o{ PURCHASE_INBOUNDS : "采购入库"')
L.append('    PURCHASE_ORDERS ||--o{ PAYABLE_BILLS : "采购应付"')
L.append('    RENT_IN_ORDERS ||--o{ PAYABLE_BILLS : "租金应付"')
L.append('    SALES_OUTBOUNDS ||--o{ RECEIVABLE_BILLS : "销售费应收"')
L.append('    COMBO_OUTBOUNDS ||--o{ RECEIVABLE_BILLS : "租赁费应收"')
L.append('    PAYABLE_BILLS ||--o{ PAYMENTS : "付款分期"')
L.append('    RECEIVABLE_BILLS ||--o{ RECEIPTS : "收款分期"')
L.append('    RECEIVABLE_BILLS ||--o{ INVOICES : "开票"')
L.append('    RECEIPTS }o--o{ RECEIVABLE_BILLS : "水单核销"')
L.append('    STOCKTAKES ||--o{ OTHER_INBOUNDS : "盘盈生成"')
L.append('    STOCKTAKES ||--o{ OTHER_OUTBOUNDS : "盘亏生成"')
L.append('    LOCATIONS ||--o{ STOCK_FLOWS : "客户虚拟仓"')
L.append('    BOM_LIST ||--o{ BOM_LIST : "父项子项"')
L.append('    BOM_LIST ||--o{ BOM_VERSIONS : "版本"')
L.append('    TODO_ITEMS }o--|| PROJECTS : "docNo 弱引用"')
L.append('```')
L.append('')
out = PROT / 'P3-R01-A06-实体关系与状态机.md'
out.write_text('\n'.join(L), encoding='utf-8')
print('A06 written:', len(L), 'lines; relations:', len(REL), 'entities:', len(ENT_CN))
