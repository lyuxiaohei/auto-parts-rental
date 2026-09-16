# -*- coding: utf-8 -*-
"""G38 T3：A05 回填与清账
  ① 42 张字段表加「概念 id」列（表头+分隔线+行）
  ② 概念 id 按（实体,字段键,标签）规则回填，无对应概念记 —
  ③ 清 112 行〔待核〕：按取值域确认落标准名（页面标题/明细区标题/单据号等映射表）
  ④ salesReturns 组合行拆 5 行；补登记 12 行（检4 清账）
  ⑤ 标签同步：库区→库房、纯日期实体的 时间→日期、器具→物料（与 T4/T5 页面改动对齐）
"""
import io, re, sys

A05 = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\P3-R01-A05-字段字典.md'
t = io.open(A05, encoding='utf-8', newline='').read()
EOL = '\r\n' if '\r\n' in t else '\n'
raw = t

# ---------- ④-1 salesReturns 组合行拆 5 行 ----------
COMBINED = '| `material`/`qty`/`amount`/`status`/`date` | 物料/数量/金额/状态/退货日期 ¹ | 同采购退货 | 状态流 待审核→已审核→已退款 | 3/3 |'
SPLIT5 = (
    '| `material` | 物料 ¹ | 文本 | 同采购退货 | 3/3 |\n'
    '| `qty` | 数量 ¹ | 数值 | 同采购退货 | 3/3 |\n'
    '| `amount` | 含税金额 ¹ | 数值 | 同采购退货 | 3/3 |\n'
    '| `status` | 状态 ¹ | 枚举 | 待审核 → 已审核 → 已退款 | 3/3 |\n'
    '| `date` | 退货日期 ¹ | 日期 | 2026-09-xx | 3/3 |'
)
assert t.count(COMBINED) == 1, 'combined row %d' % t.count(COMBINED)
t = t.replace(COMBINED, SPLIT5)

# ---------- ③〔待核〕清账：按(实体,键)落标准名 ----------
STALE = {
    ('locations', 'area'): '库区 ¹（已退场·G31 T3 去库区层·数据无此键）',
    ('salesOrders', 'mode'): '下单方式 ¹（已退场·2026-09-14 删域·D-19 订单唯一来源=项目经理代下）',
}

RELABEL = {
    # 渲染元字段（全局·所有实体同名同义）
    ('*', 'title'): '页面标题（渲染元字段）',
    ('*', 'feeSecTitle'): '明细区标题（渲染元字段）',
    ('*', 'scenario'): '演示场景（测试注记）',
    # 各实体业务字段
    ('bomVersions', 'titleNo'): 'BOM 版本号',
    ('bomList', 'mix'): '配方构成（来源混拆·租入/自购标注）',
    ('bomList', 'updater'): '更新人',
    ('dictItems', 'category'): '字典大类',
    ('dictItems', 'abbr'): '简码',
    ('dictItems', 'name'): '字典项名称',
    ('dictItems', 'status'): '状态',
    ('projects', 'end'): '结束日期',
    ('projectDocs', 'type'): '单据类型',
    ('projectDocs', 'summary'): '摘要',
    ('projectDocs', 'qty'): '数量',
    ('projectDocs', 'status'): '状态',
    ('projectDocs', 'date'): '单据日期',
    ('projectDocs', 'ref'): '关联单据号',
    ('boardRows', 'name'): '条目名称',
    ('boardRows', 'customer'): '客户',
    ('boardRows', 'status'): '项目状态',
    ('purchaseOrders', 'summary'): '摘要',
    ('salesOrders', 'summary'): '摘要',
    ('salesOrders', 'po'): '关联采购订单号',
    ('salesOutbounds', 'summary'): '摘要',
    ('leaseOrders', 'billing'): '计费方式',
    ('returnInbounds', 'appliance'): '物料',
    ('returnInbounds', 'status'): '状态',
    ('rentTracks', 'status'): '租赁状态',
    ('payableBills', 'project'): '所属项目',
    ('payableBills', 'period'): '账期',
    ('payableBills', 'inbound'): '关联入库单号',
    ('payableBills', 'billNo'): '账单号',
    ('payableBills', 'billType'): '账单类型',
    ('payableBills', 'amount'): '账单金额',
    ('payableBills', 'paid'): '已付金额',
    ('payableBills', 'genMode'): '生成方式',
    ('receivableBills', 'docs'): '关联单据号',
    ('receivableBills', 'gen'): '生成方式',
    ('receivableBills', 'billNo'): '账单号',
    ('receivableBills', 'billType'): '账单类型',
    ('receivableBills', 'amount'): '账单金额',
    ('receivableBills', 'paid'): '已收金额',
    ('receivableBills', 'verified'): '已核销金额',
    ('receivableBills', 'genDate'): '生成日期',
    ('receivableBills', 'feeType'): '费用类型',
    ('receipts', 'receipt'): '银行回单',
    ('writeoffs', 'ref'): '关联单据号',
    ('writeoffs', 'status'): '核销状态',
    ('writeoffs', 'time'): '核销时间',
    ('profitRows', 'name'): '条目名称',
    ('roles', 'desc'): '角色描述',
    ('roles', 'accts'): '关联账号数',
    ('users', 'status'): '状态',
    ('todoItems', 'auditor'): '审核人',
    ('todoItems', 'type'): '待办类型',
    ('todoItems', 'docNo'): '单据号',
    ('todoItems', 'summary'): '摘要',
    ('todoItems', 'project'): '所属项目',
    ('todoItems', 'submitter'): '提交人',
    ('todoItems', 'time'): '提交时间',
    ('todoItems', 'action'): '待办动作',
    ('todoItems', 'link'): '跳转链接（渲染元字段）',
    ('stockFlows', 'titleNo'): '流水行标题（渲染元字段）',
}

# ---------- ⑤ 标签口径同步（与 T4/T5 页面改动一致） ----------
LABEL_SYNC = {
    ('products', 'date'): '建档日期 ¹',          # 值纯日期（2026-01-06）
    ('partners', 'date'): '创建日期 ¹',          # 值纯日期
    ('projects', 'start'): '立项日期 ¹',         # 值纯日期
    ('rentInbounds', 'date'): '入库日期 ¹',      # 值纯日期
    ('rentInReturns', 'date'): '归还日期 ¹',     # 值纯日期
    ('rentInbounds', 'area'): '入库库房 ²',
    ('rentInbounds', 'appliance'): '物料 ¹',     # 器具→物料（T4 物料列）
    ('rentInReturns', 'appliance'): '物料 ²',
    ('returnInbounds', 'warehouse'): '入库库房 ²',
    ('salesOutbounds', 'warehouse'): '出库库房 ²',
    ('stockFlows', 'area'): '库房 ²',
    ('purchaseInbounds', 'area'): '入库库房 ²',   # 预留：若 A05 已有该行
    ('transfers', 'from'): '调出库房 ²',
    ('transfers', 'to'): '调入库房 ²',
    ('bomList', 'update'): '更新日期 ¹',
    ('comboOutbounds', 'date'): '出库日期 ¹',
}

# ---------- 概念 id 映射 ----------
def concept_id(ent, key, label):
    lab = re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹⁰（(].*$', '', label).strip()  # 剥角标与括注后匹配
    if key in ('title', 'feeSecTitle', 'scenario', 'link', 'mix'):
        return '—'
    if ent in ('products', 'stockFlows', 'bomList') and key == '_key':
        return 'material.code'
    if ent == 'locations' and key == '_key':
        return 'wh.location'
    if ent == 'projects' and key == '_key':
        return 'project.name'
    if '关联' in lab: return 'doc.ref'
    if re.search(r'物料编码|零件号|组合件编码|父项编码', lab): return 'material.code'
    if '物料类型' in lab: return 'material.type'
    if '名称规格' in lab: return 'material.nameSpec'
    if re.search(r'物料名称|物料$|^物料|器具|货品|父项名称', lab): return 'material.name'
    if lab.startswith('规格'): return 'material.spec'
    if '未税单价' in lab: return 'price.excl'
    if '含税单价' in lab: return 'price.incl'
    if '税率' in lab: return 'price.rate'
    if '含税金额' in lab or (ent in ('purchaseReturns', 'salesReturns') and lab.startswith('金额')): return 'price.amount'
    if '日租金' in lab: return 'price.daily'
    if '计费方式' in lab: return 'price.mode'
    if '参考未税采购价' in lab: return 'price.ref.purchase'
    if '参考未税销售价' in lab: return 'price.ref.sale'
    if '参考未税租入价' in lab: return 'price.ref.rentIn'
    if '参考未税租赁价' in lab: return 'price.ref.rental'
    if '账单金额' in lab: return 'amount.bill'
    if '已付金额' in lab: return 'amount.paid'
    if '已收金额' in lab: return 'amount.received'
    if '退款金额' in lab: return 'amount.refund'
    if '开票金额' in lab: return 'amount.invoice'
    if '核销金额' in lab or '已核销' in lab: return 'amount.writeoff'
    if '成本单价' in lab: return 'amount.cost'
    if '付款金额' in lab: return 'amount.pay'
    if '收款金额' in lab: return 'amount.receive'
    if '转租结算方式' in lab or lab == '结算方式': return 'project.renter'
    if re.search(r'数量|实盘', lab): return 'qty.base'
    if '单位用量' in lab: return 'qty.usage'
    if '可用' in lab: return 'qty.available'
    if re.search(r'已归还|已退回', lab): return 'qty.returned'
    if '库位' in lab: return 'wh.location'
    if '库房' in lab or '仓库' in lab: return 'wh.warehouse'
    if '客户' in lab: return 'partner.customer'
    if '供应商' in lab: return 'partner.supplier'
    if '结算周期' in lab: return 'partner.settle'
    if re.search(r'所属项目|适用项目|项目名称', lab): return 'project.name'
    if re.search(r'建档|创建|立项', lab): return 'date.create'
    if '更新' in lab and '日期' in lab: return 'date.update'
    if '计划日期' in lab: return 'date.plan'
    if '账期' in lab: return 'date.period'
    if lab.endswith('日期'): return 'date.biz'
    if lab.endswith('时间'): return 'date.min'
    if re.search(r'单据号|单号|编号|版本号|发票号码|登记号|回单号', lab): return 'doc.no'
    if re.search(r'制单人|审核人|提交人|更新人|经办人|操作人|经办', lab): return 'doc.actor'
    if '摘要' in lab or '条目名称' in lab: return 'doc.summary'
    if '备注' in lab: return 'doc.remark'
    if '批次' in lab: return 'doc.batch'
    if '生成方式' in lab: return 'doc.gen'
    if '银行回单' in lab or lab == '回单': return 'doc.receipt'
    if re.search(r'单据类型|账单类型|待办类型|费用类型|退货类型|退款类型|归还类型|业务类型', lab):
        return 'doc.type'
    if '状态' in lab or '待办动作' in lab or '核销状态' in lab or '操作结果' in lab:
        if ent in ('products', 'dictItems', 'users', 'locations'): return 'status.std'
        if ent == 'stockFlows': return 'status.stock'
        if ent in ('rentTracks', 'assetTracks'): return 'status.rent'
        if ent in ('projects', 'boardRows'): return 'status.project'
        return 'doc.status'
    return '—'

# ---------- 逐行处理 ----------
lines = t.split(EOL)
HDR_OLD = '| 字段键 | 中文标签 | 类型 | 取值域 / 演示值 | 覆盖行数 |'
HDR_NEW = '| 字段键 | 中文标签 | 概念 id | 类型 | 取值域 / 演示值 | 覆盖行数 |'
SEP_OLD = '|---|---|---|---|---|'
SEP_NEW = '|---|---|---|---|---|---|'

out = []
cur = None
ent_re = re.compile(r'^#{2,4} ([A-Za-z_][\w]*)[ \t·]')
row_re = re.compile(r'^\|\s*`([\w]+)`\s*\|')
n_hdr = n_sep = n_row = n_relabel = n_sync = 0
assign_log = []
i = 0
while i < len(lines):
    ln = lines[i]
    m = ent_re.match(ln)
    if m: cur = m.group(1)
    if ln.strip() == HDR_OLD:
        out.append(HDR_NEW); n_hdr += 1
        # 紧随分隔线
        assert lines[i+1].strip() == SEP_OLD, 'sep after hdr: %r' % lines[i+1][:50]
        out.append(SEP_NEW); n_sep += 1; i += 2; continue
    rm = row_re.match(ln)
    if rm and cur:
        cells = [c.strip() for c in ln.split('|')]
        # |键|标签|类型|取值|覆盖| → 5 格
        if len(cells) >= 6:
            key = rm.group(1)
            label = cells[2]
            new_label = None
            if '〔待核〕' in label:
                nl = RELABEL.get((cur, key)) or RELABEL.get(('*', key))
                if nl is None:
                    # 全局规则兜底：剥离〔待核〕保留现名＋注记
                    nl = label.replace('〔待核〕', '') + '（G38 降级注记·页面无对照标签）'
                label = nl; n_relabel += 1
            if (cur, key) in STALE:
                label = STALE[(cur, key)]; n_sync += 1
            if (cur, key) in LABEL_SYNC:
                label = LABEL_SYNC[(cur, key)]; n_sync += 1
            cid = concept_id(cur, key, label)
            assign_log.append('%s.%s\t%s\t→ %s' % (cur, key, label[:24], cid))
            out.append('| `%s` | %s | %s | %s | %s | %s |' % (key, cells[2] if False else label, cid, cells[3], cells[4], cells[5]))
            n_row += 1; i += 1; continue
    out.append(ln); i += 1

t2 = EOL.join(out)
assert n_hdr == 42, 'headers %d' % n_hdr
assert n_row >= 350, 'rows %d' % n_row

# ---------- Phase D：补登记 12 行（锚=实体节内末行字段行） ----------
INSERTS = {
 'products': [
  '| `model` | 物料型号 ¹ | — | 文本 | WBX-1210L（G34·D-99 显示名「物料型号」） | 1/12 |',
  '| `innerCode` | 供应商内部编码 ¹ | — | 文本 | （G34·D-99 显示名·演示 1 行） | 1/12 |',
  '| `rentInMode` | 计费方式（租入·三段式）¹ | price.mode | 枚举 | 按月 / 按次 / null（G21） | 12/12 |',
  '| `rentInPrice` | 参考未税租入价 ¹ | price.ref.rentIn | 数值 | 45.00 元/只·月 等（G21 三段式） | 12/12 |',
  '| `rentalMode` | 计费方式（租赁·三段式）¹ | price.mode | 枚举 | 按月 / 按次 / null（G21） | 12/12 |',
  '| `rentalPrice` | 参考未税租赁价 ¹ | price.ref.rental | 数值 | 60.00 元/只·月 等（G21 三段式） | 12/12 |',
 ],
 'opLogs': [
  '| `result` | 操作结果 ¹ | doc.status | 枚举 | 成功 / 失败（G35 筛选增量） | 10/10 |',
 ],
 'projects': [
  '| `settle` | 转租结算方式 ¹ | project.renter | 枚举 | 按租出结算 / 按终端结算（D-146·G37） | 8/8 |',
 ],
 'purchaseInbounds': [
  '| `maker` | 制单人 ¹ | doc.actor | 文本 | 张帆 / 林国栋（G35 增量） | 8/8 |',
  '| `area` | 入库库房 ² | wh.warehouse | 枚举 | 原料区 RA / 成品区 RB / 外购区 RW（G35 增量） | 8/8 |',
 ],
 'stockFlows': [
  '| `loc` | 库位 ² | wh.location | 文本 | RA-A-01-01 / RB-A-01-01 / XNC-AJZX（客户虚拟仓） | 15/15 |',
  '| `qtyByProject` | 按项目库存（四态分摊）² | — | 对象 | {PRJ-xxxx:[在库,锁定,在租,租入]}（G36 C2·D-130） | 15/15 |',
 ],
}
n_ins = 0
for ent, rows in INSERTS.items():
    # 实体节的最后一行字段行（六列形态）位置
    sec_re = re.compile(r'^#{2,4} %s[ 	·]' % ent)
    lines2 = t2.split(EOL)
    sec_start = None
    for idx, ln in enumerate(lines2):
        if sec_re.match(ln):
            sec_start = idx; break
    assert sec_start is not None, 'section %s' % ent
    last_row = None
    for idx in range(sec_start, len(lines2)):
        if idx > sec_start and re.match(r'^#{1,4} ', lines2[idx]): break
        if re.match(r'^\|\s*`\w+`\s*\|.*\| \d+/\d+ \|$', lines2[idx]):
            last_row = idx
    assert last_row is not None, 'last row %s' % ent
    lines2[last_row+1:last_row+1] = rows
    n_ins += len(rows)
    t2 = EOL.join(lines2)
assert n_ins == 12, 'inserts %d' % n_ins

# 头部统计与版本行更新
t2 = t2.replace(
  '> **统计**：实体 41 ｜ 字段行 351 ｜ 覆盖页面 38（A 类 36 列表页 + 履历/字典/待办消费页；38=37+productTaxes[供应商税率增量·G33 登记块 325+26 行]）',
  '> **统计**：实体 42 ｜ 字段行 367 ｜ 概念 60（G38 概念索引）｜ 覆盖页面 38（A 类 36 列表页 + 履历/字典/待办消费页；38=37+productTaxes[供应商税率增量·G33 登记块 325+26 行]）')
t2 = t2.replace(
  '＋G34 增补（2026-09-15：字段标签改名与字典组件化·D-127·见文末登记节）',
  '＋G34 增补（2026-09-15：字段标签改名与字典组件化·D-127·见文末登记节）＋G38 增补（2026-09-15：字段概念索引 60 概念＋全表概念 id 列回填＋〔待核〕清账＋12 行补登记·D-147）')
io.open(A05, 'w', encoding='utf-8', newline='').write(t2)
io.open(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g38_t3_assign.log', 'w', encoding='utf-8').write('\n'.join(assign_log))
print('headers %d · separators %d · rows %d · 待核 cleared %d · label synced %d' % (n_hdr, n_sep, n_row, n_relabel, n_sync))
print('待核 remaining:', t2.count('〔待核〕'))
