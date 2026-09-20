# -*- coding: utf-8 -*-
"""G53 提取 v2：准确实体边界（顶级键缩进 2 空格），每实体取首条含 info 记录的 label 序列"""
import sys, io, os, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
os.chdir(ROOT)

dd = open('_data/demo-data.js', encoding='utf-8').read()
# 顶级键：\n  key: { （2 空格缩进，值是对象或数组）
tops = [(m.start(), m.group(1)) for m in re.finditer(r'\n  ([A-Za-z_][\w]*):\s*[\[{]', dd)]
bounds = {}
for idx, (pos, key) in enumerate(tops):
    end = tops[idx + 1][0] if idx + 1 < len(tops) else len(dd)
    bounds[key] = dd[pos:end]

def ent_info(ent):
    if ent not in bounds: return None
    seg = bounds[ent]
    for m in re.finditer(r"'info':\s*\[", seg):
        j = seg.find(']', m.start())
        labels = re.findall(r"'label':\s*'([^']+)'", seg[m.start():j])
        if labels: return labels
    return None

def strip_tags(x):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', x)).strip().rstrip('：:').lstrip('*').strip()

ENT_MAP = {
    "采购订单": "purchaseOrders", "采购入库": "purchaseInbounds", "采购退货": "purchaseReturns",
    "租入单": "rentInOrders", "租入入库": "rentInbounds", "租入归还": "rentInReturns",
    "租赁单": "leaseOrders", "租赁出库": "comboOutbounds", "退租入库": "returnInbounds",
    "转移出库": "transferOutbounds", "盘点": "stocktakes", "库存调拨": "transfers",
    "其他入库": "otherInbounds", "其他出库": "otherOutbounds",
    "销售订单": "salesOrders", "销售出库": "salesOutbounds", "销售退货": "salesReturns",
    "应收账单": "receivableBills", "应付账单": "payableBills", "收款登记": "receipts",
    "付款登记": "payments", "开票登记": "invoices", "退款登记": "refunds",
}
for name, ent in ENT_MAP.items():
    labels = ent_info(ent)
    print('=' * 6, name, '→', ent, '| 记录数:', len(re.findall(r"\n    '[^']+': \{", bounds.get(ent, ''))) if ent in bounds else '无实体')
    print('  info:', labels)
