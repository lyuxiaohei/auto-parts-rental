# -*- coding: utf-8 -*-
"""
G43 T2+T3+T4 总接线脚本（幂等可续跑）：
- 每页在 </body> 前插入 select-source.js include + fill 调用块（静态 option 不动作兜底）
- T4 五页静态占位清洗（删「全部/待定选项（演示数据）」）
- 读取-精确替换 + assert 计数；已含 select-source.js 的页跳过（续跑幂等）
差集矩阵真值源：_scan_tmpdir/g43_接线差集_v2.md
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "P3-R01-包装租赁管理后台原型"

PROD = "label:function(k,f){return k+' '+(f.name||'');}"
PCUST = "label:'name',keepFirst:true,filter:function(k,f){return f.type==='客户';}"
PSUP = "label:'name',keepFirst:true,filter:function(k,f){return f.type==='供应商';}"
FCUST = "label:'name',filter:function(k,f){return f.type==='客户';}"
FSUP = "label:'name',filter:function(k,f){return f.type==='供应商';}"
PRJ6 = "filter:function(k,f){return f.status!=='已完结';},label:function(k,f){return k+' '+(f.name||'');}"
# 明细物料 select 定位收窄（防误伤同表计费 g39mode/其他 select）：
# g39mat=租赁/租入单新建；data-tax="prod"=销售订单/出库新建；值源除注明外=products
EDITPROD_G39 = "document.querySelectorAll('.edit-tbl td select.g39mat').forEach(function(s){SSEL.fillEntity(s,'products',{%s});});" % PROD
EDITPROD_TAX = "document.querySelectorAll('.edit-tbl td select[data-tax=\"prod\"]').forEach(function(s){SSEL.fillEntity(s,'products',{%s});});" % PROD
# 租赁明细含 BOM 组合件 → products ∪ bomList
EDITPROD_LEASE = "document.querySelectorAll('.edit-tbl td select.g39mat').forEach(function(s){SSEL.fillEntity(s,['products','bomList'],{%s});});" % PROD
USERN = "label:function(k,f){return (f.search||'').split(' ').slice(1).join(' ');},emptyKeep:true"

PAGES = {
    # ---------- B 类字典渲染 ----------
    "仓储作业/其他入库列表.html": [
        "SSEL.fillDict(SSEL.byLabel('入库类型'),'入库类型',true);",
        "SSEL.fillEntity(SSEL.byLabel('入库库房'),'otherInbounds',{field:'warehouse',keepFirst:true});",
    ],
    "仓储作业/其他出库列表.html": [
        "SSEL.fillDict(SSEL.byLabel('出库类型'),'出库类型',true);",
        "SSEL.fillEntity(SSEL.byLabel('出库库房'),'otherOutbounds',{field:'warehouse',keepFirst:true});",
    ],
    "仓储作业/库存查询.html": [
        "SSEL.fillDict(SSEL.byLabel('库存状态'),'库存状态',true);",
        "SSEL.fillEntity(SSEL.byLabel('库房'),'stockFlows',{field:'area',keepFirst:true,append:['次品仓']});",
        "SSEL.fillEntity(SSEL.byLabel('库位'),'stockFlows',{field:'loc',keepFirst:true});",
        "SSEL.fillEntity(SSEL.byLabel('项目'),'projects',{keepFirst:true});",
    ],
    "仓储作业/盘点列表.html": [
        "SSEL.fillDict(SSEL.byLabel('盘点口径'),'盘点口径',true);",
        "SSEL.fillEntity(SSEL.byLabel('盘点范围'),'stocktakes',{field:'scope',keepFirst:true});",
        "SSEL.fillEntity(SSEL.byLabel('盘点人'),'stocktakes',{field:'checker',keepFirst:true});",
    ],
    "基础数据/产品档案.html": ["SSEL.fillDict(SSEL.byLabel('物料类型'),'物料类型',true);"],
    "我的待办.html": [
        "SSEL.fillDict(document.getElementById('todoType'),'待办单据类型',true);",
        "SSEL.fillEntity(document.getElementById('todoAuditor'),'todoItems',{field:'auditor',keepFirst:true});",
    ],
    "系统管理/角色新建.html": ["SSEL.fillDict(SSEL.byFormLabel('数据权限范围'),'数据权限范围');"],
    "系统管理/角色管理.html": ["SSEL.fillDict(SSEL.byLabel('数据权限'),'数据权限范围',true);"],
    "财务协同/付款新建.html": [
        "SSEL.fillDict(SSEL.byFormLabel('付款方式'),'支付方式');",
        "SSEL.fillEntity(SSEL.byFormLabel('供应商'),'partners',{%s});" % FSUP,
        "SSEL.fillEntity(SSEL.byFormLabel('关联应付账单'),'payableBills',{desc:true,limit:30,label:function(k,f){return k+' · '+(f.supplier||'');}});",
        "var _bk=SSEL.byFormLabel('付款银行');if(_bk){_bk.title='正式版银行账户主数据（演示值）';}",
    ],
    "财务协同/应付新建.html": [
        "SSEL.fillDict(SSEL.byFormLabel('费用分类'),'费用分类');",
        "SSEL.fillDict(document.getElementById('cmBtype'),'应付账单类型',false,{value:{'采购应付':'purchase','租金应付':'rent','丢损赔偿（赔付供应商）':'loss','对客户应付':'customer','无订单预付款':'prepay'},title:{'采购应付':'按采购订单自动汇总','租金应付':'按租入单自动汇总','丢损赔偿（赔付供应商）':'赔付供应商','对客户应付':'赔付客户：交付延误·断产·收款违约金；押金退还','无订单预付款':'付供应商保证金，T2 挂账侧待财务确认'}});",
    ],
    "财务协同/退款新建.html": ["SSEL.fillDict(document.getElementById('refundTypeSel'),'退款类型');"],
    "财务协同/退款登记.html": ["SSEL.fillDict(SSEL.byLabel('退款类型'),'退款类型',true);"],
    "采购管理/采购退货单列表.html": [
        "SSEL.fillDict(SSEL.byLabel('退货类型'),'退货类型',true);",
        "SSEL.fillEntity(SSEL.byLabel('供应商'),'partners',{%s});" % PSUP,
    ],
    "销售管理/销售退货单列表.html": [
        "SSEL.fillDict(SSEL.byLabel('退货类型'),'退货类型',true);",
        "SSEL.fillEntity(SSEL.byLabel('客户名称'),'partners',{%s});" % PCUST,
    ],
    "财务协同/应收账单.html": [
        "SSEL.fillDict(SSEL.byLabel('账单类型'),'应收账单类型',true,{title:{'丢损赔偿':'客户赔付我方','供应商应收':'供应商赔付我方','押金':'收客户·租赁押金，退时转对客户应付','预付款（保证金）':'收客户·无订单直接建单','预收':'收客户·无订单直接建单'}});",
        "SSEL.fillEntity(SSEL.byLabel('客户'),'partners',{%s});" % PCUST,
        "SSEL.fillEntity(SSEL.byLabel('所属项目'),'projects',{keepFirst:true});",
        "SSEL.fillPeriods(SSEL.byLabel('账期'),12,true);",
    ],
    "财务协同/应付账单.html": [
        "SSEL.fillDict(SSEL.byLabel('账单类型'),'应付账单类型',true,{value:{'丢损赔偿（赔付供应商）':'赔付应付','无订单预付款':'预付'},title:{'丢损赔偿（赔付供应商）':'赔付供应商','无订单预付款':'付供应商保证金·T2 挂账侧待财务确认'}});",
        "SSEL.fillEntity(SSEL.byLabel('供应商名称'),'partners',{%s});" % PSUP,
    ],
    "财务协同/开票登记.html": [
        "SSEL.fillDict(SSEL.byLabel('发票类型'),'发票类型',true,{title:{'增值税普通发票':'简称：增值税普票'}});",
    ],
    "财务协同/开票新建.html": [
        "SSEL.fillDict(SSEL.byFormLabel('发票类型'),'发票类型');",
        "SSEL.fillEntity(SSEL.byFormLabel('购方名称（客户）'),'partners',{%s});" % FCUST,
        "SSEL.fillEntity(SSEL.byFormLabel('关联应收账单'),'receivableBills',{desc:true,limit:30,label:function(k,f){return k+' · '+(f.customer||'')+' · '+(f.period||'');}});",
    ],
    "财务协同/应收生成.html": [
        "SSEL.fillDict(document.getElementById('cmBtype'),'应收账单类型',false,{only:['租赁费','销售费','丢损赔偿','供应商应收','押金','预收'],value:{'租赁费':'lease','销售费':'sale','丢损赔偿':'loss','供应商应收':'supplier','押金':'deposit','预收':'prepay'},title:{'租赁费':'按租赁出库自动汇总','销售费':'按销售出库自动汇总','丢损赔偿':'客户赔付我方','供应商应收':'供应商赔付我方','押金':'收客户·租赁押金，退时转对客户应付','预收':'收客户，无订单直接建单'}});",
        "SSEL.fillEntity(SSEL.byFormLabel('所属项目'),'projects',{%s});" % PRJ6,
    ],
    # ---------- A 类实体渲染 ----------
    "仓储作业/库存调拨列表.html": [
        "SSEL.fillEntity(SSEL.byLabel('调出库房'),'transfers',{field:'frm',keepFirst:true});",
        "SSEL.fillEntity(SSEL.byLabel('调入库房'),'transfers',{field:'to',keepFirst:true});",
    ],
    "租赁管理/租赁出库列表.html": [
        "SSEL.fillEntity(SSEL.byLabel('客户'),'partners',{%s});" % PCUST,
        "SSEL.fillEntity(SSEL.byLabel('所属项目'),'projects',{keepFirst:true});",
    ],
    "租赁管理/租赁单列表.html": [
        "SSEL.fillEntity(SSEL.byLabel('客户名称'),'partners',{%s});" % PCUST,
        "SSEL.fillEntity(SSEL.byLabel('所属项目'),'projects',{keepFirst:true});",
    ],
    "租赁管理/退租入库列表.html": [
        "SSEL.fillEntity(SSEL.byLabel('客户名称'),'partners',{%s});" % PCUST,
        "SSEL.fillEntity(SSEL.byLabel('所属项目'),'projects',{keepFirst:true});",
    ],
    "财务协同/收款登记.html": [
        "SSEL.fillEntity(SSEL.byLabel('客户'),'partners',{%s});" % PCUST,
    ],
    "销售管理/销售出库列表.html": [
        "SSEL.fillEntity(SSEL.byLabel('客户名称'),'partners',{%s});" % PCUST,
        "SSEL.fillEntity(SSEL.byLabel('所属项目'),'projects',{keepFirst:true});",
    ],
    "销售管理/销售订单列表.html": [
        "SSEL.fillEntity(SSEL.byLabel('客户名称'),'partners',{%s});" % PCUST,
        "SSEL.fillEntity(SSEL.byLabel('所属项目'),'projects',{keepFirst:true});",
    ],
    "销售管理/销售退货新建.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('客户'),'partners',{%s});" % FCUST,
        "SSEL.fillEntity(SSEL.byFormLabel('关联原单'),'salesOutbounds',{desc:true,limit:30,label:function(k,f){return k+' · '+(f.summary||f.customer||'');}});",
    ],
    "销售管理/销售订单新建.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('客户'),'partners',{%s});" % FCUST,
        "SSEL.fillEntity(SSEL.byFormLabel('所属项目'),'projects',{%s});" % PRJ6,
        EDITPROD_TAX,
    ],
    "仓储作业/库存调拨列表.html": ["调出库房：", "调入库房："],
    "采购管理/采购订单列表.html": [
        "SSEL.fillEntity(SSEL.byLabel('供应商'),'partners',{%s});" % PSUP,
        "SSEL.fillEntity(SSEL.byLabel('所属项目'),'projects',{keepFirst:true});",
    ],
    "采购管理/采购入库列表.html": [
        "SSEL.fillEntity(SSEL.byLabel('供应商'),'partners',{%s});" % PSUP,
        "SSEL.fillEntity(SSEL.byLabel('所属项目'),'projects',{keepFirst:true});",
    ],
    "采购管理/采购退货新建.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('供应商'),'partners',{%s});" % FSUP,
        "SSEL.fillEntity(SSEL.byFormLabel('关联原单'),'purchaseInbounds',{desc:true,limit:30,label:function(k,f){return k+' · '+(f.supplier||'');}});",
    ],
    "采购管理/采购订单新建.html": [
        "SSEL.fillEntity(document.getElementById('cmProject'),'projects',{%s});" % PRJ6,
    ],
    "采购管理/采购入库录单.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('关联采购订单号'),'purchaseOrders',{desc:true,limit:30,label:function(k,f){return k+' · '+(f.summary||'');}});",
        "SSEL.fillEntity(SSEL.byFormLabel('仓管员'),'users',{%s});" % USERN,
    ],
    "租入管理/租入入库列表.html": [
        "SSEL.fillEntity(SSEL.byLabel('供应商'),'rentInbounds',{field:'operator',keepFirst:true,filterV:function(v){return v.indexOf('待选')<0;}});",
        "SSEL.fillEntity(SSEL.byLabel('物料'),'rentInbounds',{field:'appliance',keepFirst:true});",
    ],
    "租入管理/租入单列表.html": [
        "SSEL.fillEntity(SSEL.byLabel('供应商'),'rentInOrders',{field:'operator',keepFirst:true,filterV:function(v){return v.indexOf('待选')<0;}});",
        "SSEL.fillEntity(SSEL.byLabel('物料'),'rentInOrders',{field:'appliance',keepFirst:true});",
    ],
    "租入管理/租入归还列表.html": [
        "SSEL.fillEntity(SSEL.byLabel('供应商'),'rentInReturns',{field:'operator',keepFirst:true,filterV:function(v){return v.indexOf('待选')<0;}});",
    ],
    "租入管理/租入单新建.html": [
        "SSEL.fillEntity(document.getElementById('cmProject'),'projects',{%s});" % PRJ6,
        EDITPROD_G39,
    ],
    "租入管理/租入归还新建.html": [
        "SSEL.fillEntity(document.getElementById('riSelect'),'rentInOrders',{desc:true,limit:30,filter:function(k,f){return f.status!=='新建(草稿)';},label:function(k,f){return k+' · '+(f.operator||'')+' · '+(f.status||'');}});",
        "if(typeof syncReturnItems==='function'){var _r=document.getElementById('riSelect');if(_r)syncReturnItems(_r);}",
    ],
    "租赁管理/租赁单新建.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('客户'),'partners',{%s});" % FCUST,
        "SSEL.fillEntity(SSEL.byFormLabel('所属项目'),'projects',{%s});" % PRJ6,
        EDITPROD_LEASE,
    ],
    "项目管理/项目新建.html": [
        "SSEL.fillEntity(document.getElementById('prjCust'),'partners',{%s});" % FCUST,
    ],
    "项目管理/上下游绑定.html": [
        "SSEL.fillEntity(document.getElementById('bindWh'),'locations',{field:'wh'});",
    ],
    "项目管理/项目档案.html": [
        "SSEL.fillEntity(SSEL.byLabel('项目负责人'),'projects',{field:'owner',keepFirst:true});",
    ],
    "基础数据/库位档案.html": [
        "SSEL.fillEntity(SSEL.byLabel('仓库'),'locations',{field:'wh',keepFirst:true});",
    ],
    "系统管理/用户权限.html": [
        "SSEL.fillEntity(SSEL.byLabel('角色'),'roles',{label:'name',keepFirst:true});",
    ],
    "系统管理/操作日志.html": [
        "SSEL.fillEntity(SSEL.byLabel('操作人'),'opLogs',{field:'user',keepFirst:true});",
    ],
    "系统管理/用户新建.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('角色'),'roles',{label:'name'});",
        "SSEL.fillDict(SSEL.byFormLabel('数据权限范围'),'数据权限范围');",
    ],
    "系统管理/字典项新建.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('字典分类'),'dictItems',{field:'category'});",
    ],
    "财务协同/损益报表.html": [
        "SSEL.fillPeriods(SSEL.byLabel('账期'),12,true);",
        "SSEL.fillEntity(SSEL.byLabel('所属项目'),'projects',{keepFirst:true});",
    ],
    "财务协同/收款新建.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('客户'),'partners',{%s});" % FCUST,
        "SSEL.fillEntity(SSEL.byFormLabel('关联应收账单'),'receivableBills',{desc:true,limit:30,label:function(k,f){return k+' · '+(f.customer||'')+' · '+(f.period||'');}});",
        "var _bk=SSEL.byFormLabel('收款银行');if(_bk){_bk.title='正式版银行账户主数据（演示值）';}",
    ],
    "仓储作业/其他入库新建.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('物料'),'products',{%s});" % PROD,
        "SSEL.fillEntity(SSEL.byFormLabel('入库库房'),'locations',{field:'wh'});",
    ],
    "仓储作业/其他出库新建.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('物料'),'products',{%s});" % PROD,
        "SSEL.fillEntity(SSEL.byFormLabel('出库库房'),'locations',{field:'wh'});",
    ],
    "仓储作业/调拨新建.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('物料'),'products',{%s});" % PROD,
        "SSEL.fillEntity(SSEL.byFormLabel('调出库房'),'locations',{field:'wh'});",
        "SSEL.fillEntity(SSEL.byFormLabel('调入库房'),'locations',{field:'wh'});",
    ],
    "仓储作业/盘点录入.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('盘点库房'),'locations',{field:'wh'});",
        "SSEL.fillEntity(SSEL.byFormLabel('盘点人'),'users',{%s});" % USERN,
        "SSEL.fillEntity(SSEL.byFormLabel('复盘人'),'users',{%s});" % USERN,
    ],
    "销售管理/销售出库新建.html": [
        "SSEL.fillEntity(SSEL.byFormLabel('关联销售订单'),'salesOrders',{desc:true,limit:30,label:function(k,f){return k+' · '+(f.summary||f.customer||'');}});",
        "SSEL.fillEntity(SSEL.byFormLabel('出库库房'),'locations',{field:'wh'});",
        EDITPROD_TAX,
    ],
}

# T4 静态占位清洗（页 → 期望替换次数）
T4_CLEAN = {
    "系统管理/字典项新建.html": 1,
    "系统管理/用户新建.html": 2,
    "财务协同/付款新建.html": 1,
    "财务协同/收款新建.html": 1,
    "财务协同/开票新建.html": 1,
}
T4_OLD = "<option>全部</option><option>待定选项（演示数据）</option>"

# 定位文本预检（页 → 必须出现的锚串）
ANCHORS = {
    "仓储作业/其他入库列表.html": ["入库类型：", "入库库房："],
    "仓储作业/其他出库列表.html": ["出库类型：", "出库库房："],
    "仓储作业/库存查询.html": ["库存状态：", "库房：", "库位：", "项目："],
    "仓储作业/盘点列表.html": ["盘点口径：", "盘点范围：", "盘点人："],
    "基础数据/产品档案.html": ["物料类型："],
    "我的待办.html": ['id="todoType"', 'id="todoAuditor"'],
    "系统管理/角色新建.html": ["数据权限范围："],
    "系统管理/角色管理.html": ["数据权限："],
    "财务协同/付款新建.html": ["付款方式：", "供应商：", "关联应付账单：", "付款银行："],
    "财务协同/应付新建.html": ["费用分类：", 'id="cmBtype"'],
    "财务协同/退款新建.html": ['id="refundTypeSel"'],
    "财务协同/退款登记.html": ["退款类型："],
    "采购管理/采购退货单列表.html": ["退货类型：", "供应商："],
    "销售管理/销售退货单列表.html": ["退货类型：", "客户名称："],
    "财务协同/应收账单.html": ["账单类型：", "客户：", "所属项目：", "账期："],
    "财务协同/应付账单.html": ["账单类型：", "供应商名称："],
    "财务协同/开票登记.html": ["发票类型："],
    "财务协同/开票新建.html": ["发票类型：", "购方名称（客户）：", "关联应收账单："],
    "财务协同/应收生成.html": ["所属项目：", 'id="cmBtype"'],
    "租赁管理/租赁出库列表.html": ["客户：", "所属项目："],
    "租赁管理/租赁单列表.html": ["客户名称：", "所属项目："],
    "租赁管理/退租入库列表.html": ["客户名称：", "所属项目："],
    "财务协同/收款登记.html": ["客户："],
    "销售管理/销售出库列表.html": ["客户名称：", "所属项目："],
    "销售管理/销售订单列表.html": ["客户名称：", "所属项目："],
    "销售管理/销售退货新建.html": ["客户："],
    "销售管理/销售订单新建.html": ["客户：", "所属项目：", 'data-tax="prod"'],
    "采购管理/采购订单列表.html": ["供应商："],
    "采购管理/采购入库列表.html": ["供应商：", "所属项目："],
    "采购管理/采购退货新建.html": ["供应商：", "关联原单："],
    "采购管理/采购订单新建.html": ['id="cmProject"'],
    "采购管理/采购入库录单.html": ["关联采购订单号：", "仓管员：", "demo-data.js"],
    "租入管理/租入入库列表.html": ["供应商：", "物料："],
    "租入管理/租入单列表.html": ["供应商：", "物料："],
    "租入管理/租入归还列表.html": ["供应商："],
    "租入管理/租入单新建.html": ['id="cmProject"', "g39mat"],
    "租入管理/租入归还新建.html": ['id="riSelect"', "syncReturnItems"],
    "租赁管理/租赁单新建.html": ["客户：", "所属项目：", "g39mat"],
    "项目管理/项目新建.html": ['id="prjCust"'],
    "项目管理/上下游绑定.html": ['id="bindWh"'],
    "项目管理/项目档案.html": ["项目负责人："],
    "基础数据/库位档案.html": ["仓库："],
    "系统管理/用户权限.html": ["角色："],
    "系统管理/操作日志.html": ["操作人："],
    "系统管理/用户新建.html": ["角色：", "数据权限范围："],
    "系统管理/字典项新建.html": ["字典分类："],
    "财务协同/损益报表.html": ["账期：", "所属项目："],
    "财务协同/收款新建.html": ["客户：", "关联应收账单：", "收款银行："],
    "仓储作业/其他入库新建.html": ["物料：", "入库库房："],
    "仓储作业/其他出库新建.html": ["物料：", "出库库房："],
    "仓储作业/调拨新建.html": ["物料：", "调出库房：", "调入库房："],
    "仓储作业/盘点录入.html": ["盘点库房：", "盘点人：", "复 盘 人", "demo-data.js"],
    "销售管理/销售出库新建.html": ["关联销售订单：", "出库库房：", 'data-tax="prod"'],
}

fails = []
wired, skipped = 0, 0
for rel, calls in PAGES.items():
    f = ROOT / rel
    html = f.read_text(encoding="utf-8")
    # 锚点预检
    for a in ANCHORS.get(rel, []):
        if a not in html:
            fails.append(f"[锚点缺失] {rel}: {a}")
    # 幂等
    if "select-source.js" in html:
        skipped += 1
        continue
    # demo-data 依赖
    if "demo-data.js" not in html:
        fails.append(f"[缺 demo-data.js] {rel}")
    # T4 清洗
    if rel in T4_CLEAN:
        n = html.count(T4_OLD)
        if n != T4_CLEAN[rel]:
            fails.append(f"[T4 计数不符] {rel}: 期望 {T4_CLEAN[rel]} 实测 {n}")
        else:
            html = html.replace(T4_OLD, "")
    # 插入接线块
    prefix = "" if "/" not in rel else "../"
    block = (
        '<script src="%s_data/select-source.js"></script>\n<script>\n'
        "/* G43 下拉数据源化：静态 option 为无 JS 兜底，运行时按字典/实体重渲染（矩阵见 _scan_tmpdir/g43_接线差集_v2.md） */\n"
        "%s\n</script>\n" % (prefix, "\n".join(calls))
    )
    marker = "</body>"
    idx = html.rfind(marker)
    assert idx > 0, rel
    html2 = html[:idx] + block + html[idx:]
    # 标签配平自检（script 标签开闭数一致）
    if html2.count("<script") != html2.count("</script>"):
        fails.append(f"[script 配平] {rel}")
    f.write_text(html2, encoding="utf-8")
    wired += 1

print(f"wired={wired} skipped(已接)={skipped} fails={len(fails)}")
for x in fails:
    print(x)
sys.exit(1 if fails else 0)
