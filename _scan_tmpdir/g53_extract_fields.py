# -*- coding: utf-8 -*-
"""G53 单据三态字段一致性梳理 · 数据提取（只读分析，不改页面）
- 新建/录单/录入/生成页：card-title（板块）+ form-label（表头字段）+ edit-tbl th（明细列）
- 审核/确认/详情页：ENT 实体名（detail-generic 数据源）
- demo-data 实体：info[].label 序列（详情/审核页字段真值）+ fees/chain/timeline 板块有无
"""
import sys, io, os, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
os.chdir(ROOT)

def strip_tags(x):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', x)).strip().rstrip('：:').lstrip('*').strip()

def page_info(path):
    s = open(path, encoding='utf-8').read()
    d = {}
    d['cards'] = [strip_tags(c) for c in re.findall(r'card-title[^>]*>([^<]+)<', s) if strip_tags(c)]
    labs = re.findall(r'class="form-label"[^>]*>(.*?)</div>', s, re.S)
    d['labels'] = [strip_tags(l) for l in labs if strip_tags(l)]
    ths = [strip_tags(t) for t in re.findall(r'<th[^>]*>(.*?)</th>', s, re.S) if strip_tags(t)]
    d['ths'] = ths
    ent = re.search(r"var ENT = '([^']+)'", s)
    d['ent'] = ent.group(1) if ent else None
    d['generic'] = 'detail-generic.js' in s
    return d

# demo-data 实体 info 提取
dd = open('_data/demo-data.js', encoding='utf-8').read()
def ent_info(ent):
    m = re.search(r'\b' + re.escape(ent) + r'\s*:\s*\{', dd)
    if not m: return None
    # 实体块：到下一个顶级实体（缩进 2 空格的 key）——用首条记录的 info 就够
    seg = dd[m.start():m.start() + 30000]
    i = seg.find("'info': [")
    if i < 0: i = seg.find('"info": [')
    if i < 0: return None
    j = seg.find(']', i)
    labels = re.findall(r"'label':\s*'([^']+)'", seg[i:j])
    return labels

DOCS = [
    # (单据名, 新建页, 审核页, 详情页)
    ("采购订单", "采购管理/采购订单新建.html", "采购管理/采购订单审核.html", "采购管理/采购订单详情.html"),
    ("采购入库", "采购管理/采购入库录单.html", "采购管理/采购入库审核.html", "采购管理/采购入库详情.html"),
    ("采购退货", "采购管理/采购退货新建.html", "采购管理/采购退货审核.html", "采购管理/采购退货详情.html"),
    ("租入单", "租入管理/租入单新建.html", "租入管理/租入单审核.html", "租入管理/租入单详情.html"),
    ("租入入库", "租入管理/租入入库确认.html", "租入管理/租入入库确认.html", "租入管理/租入入库详情.html"),
    ("租入归还", "租入管理/租入归还新建.html", "租入管理/租入归还审核.html", "租入管理/租入归还详情.html"),
    ("租赁单", "租赁管理/租赁单新建.html", "租赁管理/租赁单审核.html", "租赁管理/租赁单详情.html"),
    ("租赁出库", "租赁管理/租赁出库录单.html", "租赁管理/租赁出库确认.html", "租赁管理/租赁出库详情.html"),
    ("退租入库", "租赁管理/退租入库新建.html", "租赁管理/退租入库审核.html", "租赁管理/退租入库详情.html"),
    ("转移出库", "租赁管理/转移出库新建.html", "租赁管理/转移出库审核.html", "租赁管理/转移出库单详情.html"),
    ("盘点", "仓储作业/盘点录入.html", "仓储作业/盘点审核.html", "仓储作业/盘点详情.html"),
    ("库存调拨", "仓储作业/调拨新建.html", "仓储作业/调拨审核.html", "仓储作业/调拨详情.html"),
    ("其他入库", "仓储作业/其他入库新建.html", "仓储作业/其他入库审核.html", "仓储作业/其他入库详情.html"),
    ("其他出库", "仓储作业/其他出库新建.html", "仓储作业/其他出库审核.html", "仓储作业/其他出库详情.html"),
    ("销售订单", "销售管理/销售订单新建.html", "销售管理/销售订单审核.html", "销售管理/销售订单详情.html"),
    ("销售出库", "销售管理/销售出库新建.html", "销售管理/销售出库审核.html", "销售管理/销售出库详情.html"),
    ("销售退货", "销售管理/销售退货新建.html", "销售管理/销售退货审核.html", "销售管理/销售退货详情.html"),
    ("应收账单", "财务协同/应收生成.html", None, "财务协同/应收详情.html"),
    ("应付账单", "财务协同/应付新建.html", None, "财务协同/应付详情.html"),
    ("收款登记", "财务协同/收款新建.html", None, "财务协同/收款详情.html"),
    ("付款登记", "财务协同/付款新建.html", "财务协同/付款确认.html", "财务协同/付款详情.html"),
    ("开票登记", "财务协同/开票新建.html", None, "财务协同/开票详情.html"),
    ("退款登记", "财务协同/退款新建.html", None, "财务协同/退款详情.html"),
]

out = {}
for name, nw, au, dt in DOCS:
    rec = {'新建': page_info(nw) if nw else None}
    rec['审核'] = page_info(au) if au else None
    rec['详情'] = page_info(dt) if dt else None
    ent = (rec['详情'] or {}).get('ent') or (rec['审核'] or {}).get('ent')
    rec['ent'] = ent
    rec['ent_info'] = ent_info(ent) if ent else None
    out[name] = rec

print(json.dumps(out, ensure_ascii=False, indent=1))
