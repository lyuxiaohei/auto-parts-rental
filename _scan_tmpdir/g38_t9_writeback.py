# -*- coding: utf-8 -*-
"""G38 T9 回写：P2-R01 D-147 ✅＋A05 G38 登记节"""
import io

# 1. P2-R01 D-147 状态
p = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P2-R01-产品需求文档.md'
t = io.open(p, encoding='utf-8', newline='').read()
old = '| 道远 09-15 指示「不能并入 G37 的生成 G38」＋字段统一方案一~四＋物料类型「看行业通用·给 10 个示例·在数据字典维护」 | 🔄（G38 执行中） |'
new = '| 道远 09-15 指示「不能并入 G37 的生成 G38」＋字段统一方案一~四＋物料类型「看行业通用·给 10 个示例·在数据字典维护」 | ✅（G38 完成·2026-09-16·field_gate 四检 0/0/0/0＋audit 132 页 0/0/0） |'
assert t.count(old) == 1
t = t.replace(old, new)
old2 = '> **版本**：V1.3（＋G38 字段口径统一立项 D-147）｜ **最后更新**：2026-09-16（**D-147 字段口径统一立项＋物料类型 10 值（G38 执行中）🔄**；前值 2026-09-15：'
new2 = '> **版本**：V1.3（＋G38 字段口径统一落地 D-147）｜ **最后更新**：2026-09-16（**D-147 字段口径统一＋物料类型 10 值（G38 完成）✅**；前值 2026-09-15：'
assert t.count(old2) == 1
t = t.replace(old2, new2)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('[OK] P2-R01 D-147 ✅')

# 2. A05 G38 登记节
p2 = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\P3-R01-A05-字段字典.md'
t2 = io.open(p2, encoding='utf-8', newline='').read()
EOL = '\r\n' if '\r\n' in t2 else '\n'
sec = EOL + '## G38 字段口径统一登记（2026-09-16 · D-147 · 任务档=agent-handoff/20260915-G38-字段口径统一.md）' + EOL + EOL + \
'> **改动面**：①「字段概念索引」60 概念（本文件新节·页面字段名引用源）②42 表加「概念 id」列回填 367 行（含拆 1 组合行＋12 行补登记：products.model/innerCode/rentIn 四键·opLogs.result·projects.settle·purchaseInbounds.maker/area·stockFlows.loc/qtyByProject·salesReturns 5 键拆行）③〔待核〕清账 112 行（渲染元字段落注记·业务字段按取值域落标准名）④两处缺列缺陷修复：采购入库录单 14/10→12 列配平（+四价格格·值按参考未税采购价 6.80/4.20/36.00×13%）、租赁出库录单 12/8→12 列配平（+四价格格·值按租赁单新建跨页一致 2.40/0.15）⑤T7 托计量退场：采购入库录单删「托数/每托数量/入库总数」三列改「数量 *」＋「单位」→「基本单位」＋「零件号 / 物料编码」→「物料编码」；采购入库列表删「到货托数」列（cells 8→7）；purchaseInbounds/purchaseOrders feeCols「零件号→物料编码」「托数 × 件数→数量」⑥库房层级：入库/出库/调出/调入库区→库房（HTML 4 页＋demo-data info 标签 64 处）⑦时间粒度：建档/创建/更新/立项/制单（纯日期值者）→「日期」；rentInbounds/rentInReturns 因 cells 含时分维持「时间」（fields 纯日期属数据级怪癖·登记不改值）⑧物料类型 10 值（D-147）：dictItems +WL-07~10（141→145 项）·WL-06 释义改「BOM 组合件」·products 重归类（LJ-A100~D400 组件→零部件·LJ-E500/F600→内衬）＋新增 3 示例行 KBX-1040M/PLT-1210G/KJ-2701（12→15 行）·stockFlows.cls 租赁器具→形态值（11 行）·产品档案/物料新建 option 6→10 ⑨退货单四件套：purchaseReturns/salesReturns feeCols＋两新建页 th 裸「单价/金额」→四件套名 ⑩分期表「金额(元)」→「分期金额(元)」（4 页）·订单列表「金额(元)」→「含税金额(元)」（2 页）·invoices feeCols「金额(元)」→「开票金额(元)」⑪物料列：「货品」→「物料」（租入归还新建/租赁单列表 th＋租入域 多货品→多物料）·products info 裸「名称」→「物料名称」⑫A03/A04 标注文案同步（以托为单位/零件号/逐货品 表述退场·75 文件）。' + EOL + \
'> **验证**：field_gate 四检 0/0/0/0（首扫 5/0/158/17）·audit 132 页 0/0/0＋对 g37baseline 逐键新增 0（g38baseline 落盘）·node --check 0·g28c 18 弹窗 0 溢出·PW 10/10。' + EOL
t2 = t2.rstrip(EOL) + EOL + sec
io.open(p2, 'w', encoding='utf-8', newline='').write(t2)
print('[OK] A05 G38 登记节')
