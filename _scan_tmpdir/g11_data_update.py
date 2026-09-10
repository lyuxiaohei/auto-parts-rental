# -*- coding: utf-8 -*-
"""G11-B4a: A03 清退/修锚/新增 pin + A04 追加 pin（数据文件手术·全部 assert）"""
import json, io, sys, os, shutil, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
BK = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-g11-20260910"
A3P = os.path.join(ROOT, 'P3-R01-A03-标注数据.json')
A4P = os.path.join(ROOT, 'P3-R01-A04-流程链标注数据.json')

os.makedirs(BK, exist_ok=True)
for src in (A3P, A4P):
    dst = os.path.join(BK, os.path.basename(src))
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
print('备份 A03/A04 完成')

a3 = json.load(open(A3P, encoding='utf-8'))
a4 = json.load(open(A4P, encoding='utf-8'))

# ---- 1) A03 清退 15 个已删页键 ----
STALE = ['仓储作业/小组装列表.html', '仓储作业/小组装录单.html', '仓储作业/退租验收列表.html', '仓储作业/退租验收录单.html',
         '基础数据/包材档案.html', '基础数据/子母件BOM.html', '基础数据/往来单位.html', '基础数据/零部件档案.html',
         '客户端/下单.html', '客户端/我的订单.html', '租赁管理/在租资产跟踪.html', '租赁管理/缺损赔偿.html',
         '订单协同/客户订单.html', '订单协同/结算导出.html', '订单协同/路凯下发.html']
pruned = 0
for k in STALE:
    assert k in a3, f'A03 无此键: {k}'
    assert not os.path.exists(os.path.join(ROOT, k)), f'页面其实存在?! {k}'
    pruned += len(a3.pop(k))
print(f'A03 清退 {len(STALE)} 键 {pruned} 条')

# ---- 2) A03 selector 修复（11 改锚） ----
FIXES = [
    ('仓储作业/库存查询.html', 1, '<h3 class="card-title">库存双视角查询</h3>', '<h3 class="card-title">库存四态查询</h3>'),
    ('仓储作业/库存查询.html', 2, '<th>组装占用</th>', '<div class="st-foot">其中组装占用'),
    ('基础数据/BOM维护.html', 1, '<h3 class="card-title">子件明细</h3>', '<h3 class="card-title">子项明细</h3>'),
    ('租赁管理/组合出库列表.html', 1, '<h3 class="card-title">组合出库单</h3>', '<h3 class="card-title">租赁出库单</h3>'),
    ('租赁管理/组合出库列表.html', 2, '<th>关联客户订单</th>', '<th>关联销售订单</th>'),
    ('财务协同/回款登记.html', 1, '<h3 class="card-title">回款登记</h3>', '<h3 class="card-title">收款登记</h3>'),
    ('财务协同/回款登记.html', 2, '<th>银行水单</th>', '<th>银行回单</th>'),
    ('财务协同/应收账单.html', 2, '<button class="btn btn-sm">手动生成账单</button>',
     '<button class="btn btn-sm" onclick="openModal(\'createModal\')">手动生成账单</button>'),
    ('财务协同/盈亏报表.html', 1, '<h3 class="card-title">项目盈亏报表</h3>', '<h3 class="card-title">项目损益</h3>'),
    ('财务协同/银行水单核销.html', 1, '<h3 class="card-title">① 银行水单</h3>', '<h3 class="card-title">① 银行回单</h3>'),
    ('首页/项目看板.html', 3, '<button class="btn btn-default btn-sm" onclick="go(\'../财务协同/盈亏报表.html\')">盈亏报表</button>',
     '<button class="btn btn-default btn-sm" onclick="go(\'../财务协同/盈亏报表.html\')">损益报表</button>'),
]
for pg, nid, old, new in FIXES:
    it = next(x for x in a3[pg] if x['id'] == nid)
    assert it['selector'] == old, f'{pg}#{nid} selector 形态不符: {it["selector"][:60]}'
    it['selector'] = new
# 组合出库列表#2 title 同步列名
it = next(x for x in a3['租赁管理/组合出库列表.html'] if x['id'] == 2)
assert it['title'] == '关联客户订单'
it['title'] = '关联销售订单'
print(f'A03 修复 {len(FIXES)} 条 selector（+1 title 同步）')

# ---- 3) A03 退役 项目档案#2（按钮随弹窗提取消失） ----
before = len(a3['项目管理/项目档案.html'])
a3['项目管理/项目档案.html'] = [x for x in a3['项目管理/项目档案.html'] if x['id'] != 2]
assert len(a3['项目管理/项目档案.html']) == before - 1
print('A03 退役 项目档案#2（编码规则按钮已随弹窗提取移出页面）')

# ---- 4) A03 新增 pin：库存查询#3（B1+B2 合并）/产品档案新键#1/盈亏报表#2 ----
assert [x['id'] for x in a3['仓储作业/库存查询.html']] == [1, 2]
a3['仓储作业/库存查询.html'].append({
    'id': 3,
    'selector': '<div class="st-label"><span>客户端（租出在外）',
    'title': '客户虚拟仓与在租明细',
    'note': '客户虚拟仓＝在客户处的租赁资产按客户归集（on-hire）；客户转租为其子状态（2026-09-08 会议 T1 方向）。\n客户在租明细（原在租台账·2026-09-10 并入）＝行内「客户在租」按客户/项目下钻；租出与退回进度在租赁单列表「退回进度」列跟踪。',
    'fp': 'FP4-02', 'req': 'REQ-03'})
assert '基础数据/产品档案.html' not in a3
a3['基础数据/产品档案.html'] = [{
    'id': 1,
    'selector': '<h3 class="card-title">供应商税率维护',
    'title': '税率口径与档案合并',
    'note': '口径：同一产品可按供应商维护不同税率（默认 13%；运费/杂费后续可能 6%/9%）；单据明细税率默认带出、可手动覆盖。产品档案 = 器具档案 + 零部件档案合并（2026-09-08 会议 N4）。',
    'fp': '', 'req': ''}]
assert [x['id'] for x in a3['财务协同/盈亏报表.html']] == [1]
a3['财务协同/盈亏报表.html'].append({
    'id': 2,
    'selector': '<div class="pager">',
    'title': '演示链数据对齐',
    'note': '对齐说明（演示链数据）：PRJ-2601 收入合计 486,200.00 ＝ 应收账单 AR-2026-08-PRJ2601（已开票 186,200 · 水单部分核销 286,500，见开票登记 / 银行水单核销）；PRJ-2604 为 L4 混合链演示项目——租入大箱租金应付 AP-20260903-010（12,000.00 / 月）与自购隔板采购摊销计入成本合计，9 月销售费应收 AR-2026-09-PRJ2604-S1（1,280.00）见应收账单；当前成本大于收入、毛利为负（项目状态：已暂停）。',
    'fp': 'FP6-05', 'req': 'REQ-02'})
print('A03 新增 pin：库存查询#3 / 产品档案#1（新键）/ 盈亏报表#2')

# ---- 5) A04 追加 4 pin ----
def append_pin(data, pg, pin):
    ids = [x['id'] for x in data[pg]]
    assert pin['id'] == max(ids) + 1, f'{pg} id 续尾错误 {pin["id"]} vs {ids}'
    data[pg].append(pin)

append_pin(a4, '租赁管理/租入单列表.html', {
    'id': 3,
    'selector': '<button class="btn btn-dashed btn-sm" style="width:100%;margin-top:8px;">+ 添加明细行',
    'title': '租入计费口径',
    'note': '计费＝月租金 + 按套数单价（无日租金，2026-09-08 会议）；应付生成方式取决于租入单模式（静态租入 / 背靠背）。'})
append_pin(a4, '租赁管理/退租入库列表.html', {
    'id': 4,
    'selector': '<h3 class="card-title">退租入库单',
    'title': '退租无申请单口径',
    'note': '退租无申请单：客户退回后直接录入退租入库单（按拆后零件·单一产品记录）；入库仅更新库存状态，与财务结算解耦——租金只要发出去就要收，还了也收（2026-09-08 会议拍板）。'})
append_pin(a4, '财务协同/应付账单.html', {
    'id': 4,
    'selector': '<th>期次</th>',
    'title': '分期互算口径',
    'note': '分期互算：填比例自动算金额、填金额自动算比例，末期自动补差；账单头部展示「账单金额 / 已付 / 剩余」，付款时选金额，超出账单金额拦截（2026-09-08 会议 M2/C-C）。'})
append_pin(a4, '租赁管理/租赁单列表.html', {
    'id': 6,
    'selector': '<span class="form-label">押金(元)',
    'title': '押金预留字段',
    'note': '押金为设计预留字段——两次会议均未涉及，收退与计价商务口径待客户确认（F01 财务通道注记同步）。'})
print('A04 追加 4 pin（租入单列表#3/退租入库列表#4/应付账单#4/租赁单列表#6）')

# ---- 6) _meta 注记 ----
a3['_meta']['date'] += '；2026-09-10 G11：清退 15 个已删页键（29 条）+修复 12 条 selector 失配（11 改锚·G07 改版遗留+1 退役[项目档案#2 编码规则按钮随弹窗提取移出]）+新增 4 pin（库存查询#3 客户虚拟仓与在租明细/产品档案#1 新键/盈亏报表#2——页面元注释迁入标注层）'
a4['_meta']['date'] += '；2026-09-10 G11：追加 4 pin（租入单列表#3/退租入库列表#4/应付账单#4/租赁单列表#6——页面元注释迁入·此 4 页为 A04 独占页，落 A03 会被 A04 重注覆盖）'

json.dump(a3, open(A3P, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(a4, open(A4P, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'写回完成：A03 {len([k for k in a3 if not k.startswith("_")])} 键 / A04 {len([k for k in a4 if not k.startswith("_")])} 键')
