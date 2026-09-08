# -*- coding: utf-8 -*-
"""任务二·页面结构提取（禁凭印象）：筛选区控件 / stab 页签 / thead 列 / tbody 行 / 实体键匹配 / row 已建情况"""
import sys, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'

src = (PROTO / '_data' / 'demo-data.js').read_text(encoding='utf-8')
ent_re = re.compile(r'^  ([A-Za-z_][A-Za-z0-9_]*): \{$', re.M)
key_re = re.compile(r"^    '([^']+)': \{$", re.M)
spans = [(m.group(1), m.start()) for m in ent_re.finditer(src)]
ENTS = {}
for i, (n, p) in enumerate(spans):
    e = spans[i + 1][1] if i + 1 < len(spans) else len(src)
    body = src[p:e]
    ENTS[n] = dict(keys=key_re.findall(body),
                   has_row=re.findall(r"^    '([^']+)': \{\n      'row':", body, re.M))

def strip_tags(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h)).strip()

def extract(page_f, entity):
    txt = (PROTO / page_f).read_text(encoding='utf-8')
    out = {'page': page_f, 'entity': entity}
    # 筛选控件
    ffs = re.findall(r'<div class="ff">.*?</div>\s*</div>|<div class="ff">.*?</div>', txt, re.S)
    labels = re.findall(r'<span class="ff-label">([^<]+)</span>', txt)
    sels = re.findall(r'<div class="ff">(.*?)</div>\s*(?=<div class="ff">|<div class="filter-actions">|</div>)', txt, re.S)
    ctl = []
    for lab in labels:
        ctl.append(lab.rstrip('：:'))
    out['filters'] = ctl
    # 每个控件类型
    ff_blocks = re.findall(r'<span class="ff-label">([^<]+)</span>(.*?)(?=<span class="ff-label">|<div class="filter-actions">|</div>\s*</div>\s*<!--)', txt, re.S)
    types = []
    for lab, blk in ff_blocks:
        n_sel = len(re.findall(r'<select', blk))
        n_inp = len(re.findall(r'<input', blk))
        types.append((lab.rstrip('：:'), 'select' if n_sel else ('range' if n_inp >= 2 else ('input' if n_inp else '?'))))
    out['filter_types'] = types
    # stab 页签
    stabs = re.findall(r'<span class="stab[^"]*"[^>]*>([^<]+)<span class="stab-count">(\d+)</span>', txt)
    out['stabs'] = stabs
    # thead
    theads = re.findall(r'<thead>(.*?)</thead>', txt, re.S)
    out['theads'] = [re.findall(r'<th[^>]*>([^<]*)</th>', t) for t in theads]
    # tbody 行
    tbodys = re.findall(r'<tbody[^>]*>(.*?)</tbody>', txt, re.S)
    rows_all = []
    for tb in tbodys:
        rows_all.append(re.findall(r'<tr>(.*?)</tr>', tb, re.S))
    out['n_tbodys'] = len(tbodys)
    out['n_rows'] = [len(r) for r in rows_all]
    # 首行 cells + ops
    if rows_all:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', rows_all[0][0], re.S)
        out['first_row_cells'] = [strip_tags(t) for t in tds]
        out['first_row_ops'] = rows_all[0][0].split('<td class="sticky-op">')[-1] if 'sticky-op' in rows_all[0][0] else '(无)'
    # 行→键匹配（照 wireDetailModal：插入序 indexOf）
    keys = ENTS.get(entity, {}).get('keys', [])
    matched = []
    if rows_all:
        for row in rows_all[0]:
            rt = strip_tags(row)
            k = next((x for x in keys if x in rt), None)
            matched.append(k)
    out['row_keys'] = matched
    out['keys_no_row'] = [k for k in keys if k not in ENTS.get(entity, {}).get('has_row', [])]
    out['keys_total'] = len(keys)
    return out

PAGES = json.loads(sys.argv[1]) if len(sys.argv) > 1 else [
    ('otherInbounds', '仓储作业/其他入库列表.html'),
    ('rentInbounds', '仓储作业/租入入库列表.html'),
    ('salesOutbounds', '仓储作业/销售出库列表.html'),
    ('comboOutbounds', '仓储作业/组合出库列表.html'),
    ('otherOutbounds', '仓储作业/其他出库列表.html'),
    ('rentInReturns', '仓储作业/租入归还列表.html'),
    ('returnInbounds', '仓储作业/退租入库列表.html'),
    ('assemblyOrders', '仓储作业/组装列表.html'),
    ('disassemblyOrders', '仓储作业/拆卸管理列表.html'),
    ('stocktakes', '仓储作业/盘点列表.html'),
    ('transfers', '仓储作业/库存调拨列表.html'),
    ('stockFlows', '仓储作业/库存查询.html'),
]
for ent, pg in PAGES:
    o = extract(pg, ent)
    print('=' * 100)
    print(f"{o['page']}  实体={o['entity']} 键数={o['keys_total']} tbody数={o['n_tbodys']} 行数={o['n_rows']}")
    print('  筛选:', o['filter_types'])
    print('  页签:', o['stabs'])
    print('  表头:', o['theads'][0] if o['theads'] else '(无)')
    print('  首行:', o['first_row_cells'])
    print('  行键:', o['row_keys'])
    print('  缺row的键:', o['keys_no_row'] if len(o['keys_no_row']) < 30 else f"{len(o['keys_no_row'])} 个")
