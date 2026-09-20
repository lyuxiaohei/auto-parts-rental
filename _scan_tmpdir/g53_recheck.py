# -*- coding: utf-8 -*-
"""#10 G53 会议决策核查：三卡/字段序/合理多出四类/链时间线/应收应付未动。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
sys.path.insert(0, str(ROOT / '_scan_tmpdir'))

from playwright.sync_api import sync_playwright

BIZ16 = [  # (实体, 详情页, 键) —— 16 业务单据
    ('purchaseOrders', '采购管理/采购订单详情.html', 'PO-20260902-018'),
    ('purchaseInbounds', '采购管理/采购入库详情.html', 'CGRK-20260828-012'),
    ('purchaseReturns', '采购管理/采购退货详情.html', 'CGTH-20260914-001'),
    ('rentInOrders', '租入管理/租入单详情.html', 'RZD-20260815-003'),
    ('rentInbounds', '租入管理/租入入库详情.html', 'RZRK-20260816-021'),
    ('rentInReturns', '租入管理/归还出库详情.html', 'GHCK-20260903-001'),
    ('leaseOrders', '租赁管理/租赁单详情.html', 'ZL-20260823-033'),
    ('comboOutbounds', '租赁管理/租赁出库详情.html', 'CK-20260910-022'),
    ('returnInbounds', '租赁管理/退租入库详情.html', 'TZRK-20260902-010'),
    ('transferOutbounds', '租赁管理/转移出库单详情.html', 'ZY-20260915-005'),
    ('stocktakes', '仓储作业/盘点详情.html', 'PD-202608-03'),
    ('otherInbounds', '仓储作业/其他入库详情.html', 'QTRK-20260901-003'),
    ('otherOutbounds', '仓储作业/其他出库详情.html', 'QTCK-20260905-005'),
    ('salesOrders', '销售管理/销售订单详情.html', 'SO-20260903-0047'),
    ('salesOutbounds', '销售管理/销售出库详情.html', 'XSCK-20260910-016'),
    ('salesReturns', '销售管理/销售退货详情.html', 'XSTH-20260913-001'),
]
FIN4 = [
    ('receipts', '财务协同/收款详情.html', 'HK-20260830-014'),
    ('payments', '财务协同/付款详情.html', 'PAY-20260902-005'),
    ('invoices', '财务协同/开票详情.html', 'INV-20260902-013'),
    ('refunds', '财务协同/退款详情.html', 'TKD-20260913-002'),
]
TRANSFER = ('transfers', '仓储作业/调拨详情.html', 'DB-20260901-003')

# 字段序核查样本（P3-R06 定稿序：单号+状态 开头 → 新建序 → 收尾）
SEQ_CHECKS = {
    'purchaseOrders': ['订单号', '状态', '所属项目', '供应商', '物料类型', '关联销售订单号'],
    'comboOutbounds': ['出库单号', '状态', '所属项目', '关联租赁单', '关联销售订单', '客户（带出）', '出库类型', '出库库位', '收货地点'],
    'stocktakes': ['盘点单号', '状态', '盘点库房', '盘点范围', '盘点口径', '盘点人', '盘点日期', '处理方式', '复盘人', '备注'],
}

# 合理多出四类启发式
IDENT = ('单号', '状态', '单据类型')
SYSTEM = ('制单人', '审核人', '经办人', '业务员', '登记人', '创建时间', '制单时间', '入库时间', '仓管员', '盘点人', '复盘人', '上期盘点')
AGG = ('金额', '合计', '月租', '租金标准', '退回进度', '计租天数', '货款支付状态', '已生成租金应付', '到货数量', '入库库位', '账面项数', '差异项数', '盘点基准', '资产来源', '租赁内容', '数量')
FLOW = ('财务口径', '库存状态', '终止日期', '关联退款单', '关联盘点单', '关联赔偿单', '租金结算', '押金退还', '器具状况', '缺损情况', '拆散去向', '发票关联', '银行回单', '核销状态', '计价方式', '退款', '资金方向', '收退款账户', '往来单位', '发票号码', '发票类型', '税率', '税率', '下单方式', '下单时间', '订单附件', '备注')

def cls(label):
    if any(k in label for k in IDENT): return '身份'
    if any(k in label for k in SYSTEM): return '系统'
    if any(k in label for k in AGG): return '汇总'
    if any(k in label for k in FLOW): return '流程/其他约定'
    return '?未归类'

import json, re, subprocess

# 从 demo-data 直接读 formRows（node 执行环境取数）
node_script = """
global.window={};
require(String.raw`""" + str(PROTO / '_data/demo-data.js').replace('\\', '/') + """`);
var D=window.DEMO_DATA;
var out={};
['purchaseOrders','purchaseInbounds','purchaseReturns','rentInOrders','rentInbounds','rentInReturns','leaseOrders','comboOutbounds','returnInbounds','transferOutbounds','stocktakes','otherInbounds','otherOutbounds','salesOrders','salesOutbounds','salesReturns','receipts','payments','invoices','refunds','transfers'].forEach(function(e){
  var k=Object.keys(D[e])[0]; out[e]={key:k, labels:(D[e][k].formRows||[]).map(function(f){return f.label;})};
});
console.log(JSON.stringify(out));
"""
tmp = ROOT / '_scan_tmpdir' / 'g53_recheck_node.js'
tmp.write_text(node_script, encoding='utf-8')
data = json.loads(subprocess.run(['node', str(tmp)], capture_output=True, text=True, encoding='utf-8', cwd=ROOT, check=True).stdout.strip())

print('== A. 字段序对照定稿（3 实体） ==')
okA = True
for ent, expect in SEQ_CHECKS.items():
    labels = data[ent]['labels']
    idx = [labels.index(e) if e in labels else -99 for e in expect]
    good = all(i >= 0 for i in idx) and idx == sorted(idx)
    okA &= good
    print('%s %s  索引=%s' % ('PASS' if good else 'FAIL', ent, idx))

print()
print('== B. 合理多出四类归类（21 实体全 formRows 字段） ==')
uncategorized = []
total_fields = 0
for ent, info in data.items():
    for lb in info['labels']:
        total_fields += 1
        if cls(lb) == '?未归类':
            uncategorized.append(ent + ':' + lb)
print('字段总数 %d · 启发式未归类 %d 条' % (total_fields, len(uncategorized)))
for u in uncategorized:
    print('  ?', u)

print()
print('== C. 渲染核查（21 张三卡+链时间线）＋应收/应付未动 ==')
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    okC = 0
    cases = BIZ16 + FIN4 + [TRANSFER]
    for ent, rel, key in cases:
        pg.goto((PROTO / rel).as_uri() + '?id=' + key, wait_until='networkidle')
        r = pg.evaluate("""() => {
          const cards = document.querySelectorAll('#detailBody > .fm-card');
          const titles = [...cards].map(c => c.querySelector('.card-title')?.textContent.trim());
          const flow = titles.includes('流转信息');
          const chain = document.querySelector('#detailBody .chain');
          const tl = document.querySelector('#detailBody .tl');
          return {n: cards.length, titles, flow, hasChainTl: !!(chain || tl)};
        }""")
        good = r['n'] >= 3 and r['flow'] and r['hasChainTl']
        okC += good
        if not good:
            print('FAIL', ent, r)
    print('三卡+流转卡+链/时间线: %d/%d PASS' % (okC, len(cases)))
    pg.goto((PROTO / '财务协同/应收详情.html').as_uri() + '?id=AR-2026-08-PRJ2601', wait_until='networkidle')
    r1 = pg.evaluate("() => document.querySelectorAll('#detailBody .fm-card').length")
    pg.goto((PROTO / '财务协同/应付详情.html').as_uri() + '?id=AP-20260901-008', wait_until='networkidle')
    r2 = pg.evaluate("() => document.querySelectorAll('#detailBody .fm-card').length")
    print('应收/应付 fm-card=%d/%d（0=仍走专用渲染器·符合「待另行拍板」决策）' % (r1, r2))
    b.close()

print()
print('== D. 总判定 ==')
print('字段序 %s · 未归类 %d 条 · 三卡 %d/21 · 应收应付未动 %s' % (
    'PASS' if okA else 'FAIL', len(uncategorized), okC, 'PASS' if (r1 == 0 and r2 == 0) else 'FAIL'))
