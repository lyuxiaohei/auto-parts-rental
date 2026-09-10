# -*- coding: utf-8 -*-
"""G12 T2b：todoItems 补 time 字段 / profitRows 补 code 字段（整块重生成替换）"""
import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PATH = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\_data\demo-data.js'
data = open(PATH, 'rb').read().decode('utf-8')

# ---- todoItems 整块替换（fields 增 time） ----
todos = [
 ('销售订单','SO-20260910-0047','一汽解放 · 驾驶室围板箱 160 套','PRJ-2601','王琳','09-10 09:20','待审核','销售管理/销售订单列表.html?audit=1'),
 ('采购订单','PO-20260910-019','华塑包装 · 围板箱 120 只','PRJ-2601','李国栋','09-10 08:55','待审核','采购管理/采购订单列表.html?audit=1'),
 ('租赁单','LZ-20260909-012','一汽解放 · 围板箱续租 200 只','PRJ-2601','王琳','09-09 15:40','待审核','租赁管理/租赁单列表.html?audit=1'),
 ('销售出库','CK-20260909-021','组合出库 · 驾驶室围板箱 160 套','PRJ-2601','陈金','09-09 14:05','待审核','销售管理/销售出库列表.html?audit=1'),
 ('退租入库','TK-20260908-006','一汽解放 · 退租围板箱 86 只（含缺损 3 只）','PRJ-2601','袁明','09-08 16:30','待审核','租赁管理/退租入库列表.html?audit=1'),
 ('盘点','PD-20260907-003','华东中心仓 9 月初盘点（差异 5 只）','华东中心仓','李国栋','09-07 10:12','待审核','仓储作业/盘点列表.html?audit=1'),
 ('采购入库','RK-20260906-014','华塑包装 · 围板箱到货 200 只','PRJ-2601','李国栋','09-06 09:45','待验收','采购管理/采购入库列表.html?audit=1'),
 ('租入库','RZ-20260905-004','路凯 · 围板箱租入 300 只','PRJ-2603','王强','09-05 11:20','待入库','租赁管理/租入入库列表.html?audit=1'),
 ('租入归还','GH-20260904-002','路凯 · 归还围板箱 100 只','PRJ-2603','王强','09-04 15:08','待审核','租赁管理/租入归还列表.html?audit=1'),
 ('其他入库','QT-20260903-001','调拨余量回库 · 托盘 40 张','华东中心仓','赵磊','09-03 14:22','待审核','仓储作业/其他入库列表.html?audit=1'),
 ('付款登记','FK-20260902-005','华塑包装 · 8 月应付结算','PRJ-2601','李静','09-02 10:30','待确认','财务协同/付款登记.html?audit=1'),
 ('收款确认','SK-20260901-003','一汽解放 · 8 月租金回款','PRJ-2601','李静','09-01 09:15','待确认','财务协同/回款登记.html?audit=1'),
]
lines = []
for ty,no,sm,prj,who,tm,act,link in todos:
    f = {"type": ty, "docNo": no, "summary": sm, "project": prj, "submitter": who, "time": tm, "action": act}
    lines.append("    '%s': { 'row': %s, 'link': '%s' }," % (no, json.dumps({"fields": f}, ensure_ascii=False), link))
new_todo = '  todoItems: {\r\n' + '\r\n'.join(lines) + '\r\n  },'
m = re.search(r'  todoItems: \{[\s\S]*?\r\n  \},', data)
assert m, 'todoItems block not found'
data = data[:m.start()] + new_todo + data[m.end():]

# ---- profitRows fields 增 code ----
m = re.search(r'(  profitRows: \{[\s\S]*?\r\n  \},)', data)
assert m, 'profitRows block not found'
blk = m.group(1)
n = blk.count('"fields": {"name":')
blk2 = re.sub(r'\'(PRJ-\d+)\': \{ \'row\': \{"fields": \{"name"', lambda mm: "'%s': { 'row': {\"fields\": {\"code\": \"%s\", \"name\"" % (mm.group(1), mm.group(1)), blk)
assert blk2.count('"code"') == 6, 'code patch count: %d' % blk2.count('"code"')
data = data[:m.start()] + blk2 + data[m.end():]

open(PATH, 'wb').write(data.encode('utf-8'))
# 校验
assert '"time": "09-10 09:20"' in data and data.count('  todoItems: {') == 1
assert data.count('"code": "PRJ-2601"') >= 2  # profitRows + boardRows 无 code…只 profitRows
print('OK：todoItems time 补齐 12 行；profitRows code 补齐 6 行')
