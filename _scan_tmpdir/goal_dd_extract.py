# -*- coding: utf-8 -*-
"""
详情弹窗数据驱动 · 第B步提取工具
逐页提取：tbody 各行单元格文本 + detailModal 静态块（含标题/段落结构摘要）
输出 JSON dump 供建模参照（禁止凭印象建模——数据一律来自本提取）。
用法: python goal_dd_extract.py 页面1.html 页面2.html ...
      不带参数 = 提取 A 表 25 个触发页全量
"""
import json, re, sys
from pathlib import Path

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
OUT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir")

# A 表触发页（列表页）——批次顺序
PAGES = [
    # 批次1
    "销售管理/租赁单列表.html",
    "采购管理/租入单列表.html",
    "仓储作业/组合出库列表.html",
    "仓储作业/退租入库列表.html",
    "租赁管理/退租申请列表.html",
    "租赁管理/丢损赔偿单.html",
    "仓储作业/租入归还列表.html",
    "仓储作业/租入入库列表.html",
    # 批次2
    "采购管理/采购订单列表.html",
    "销售管理/销售订单列表.html",
    "仓储作业/采购入库列表.html",
    "仓储作业/销售出库列表.html",
    "仓储作业/其他入库列表.html",
    "仓储作业/其他出库列表.html",
    "仓储作业/组装列表.html",
    "仓储作业/拆卸管理列表.html",
    # 批次3
    "仓储作业/盘点列表.html",
    "仓储作业/库存调拨列表.html",
    "仓储作业/库存查询.html",
    "租赁管理/租出台账.html",
    "租赁管理/在租台账.html",
    "基础数据/客商管理.html",
    "基础数据/器具档案.html",
    "基础数据/零部件档案.html",
    "基础数据/库位档案.html",
    "基础数据/BOM维护.html",
]

CELL = re.compile(r'<td[^>]*>(.*?)</td>', re.S)
TAG = re.compile(r'<[^>]+>')


def cell_text(html):
    t = TAG.sub('', html)
    return re.sub(r'\s+', ' ', t).strip()


def extract_page(rel):
    raw = (ROOT / rel).read_bytes().decode('utf-8')
    out = {'page': rel, 'rows': [], 'modal': None, 'detail_css': 'detail-modal-css' in raw}
    # 所有 tbody（页内可能有多个表：主表 + 弹窗内明细表）
    for mb in re.finditer(r'<tbody[^>]*>(.*?)</tbody>', raw, re.S):
        body = mb.group(1)
        rows = []
        for rb in re.finditer(r'<tr[^>]*>(.*?)</tr>', body, re.S):
            cells = [cell_text(c) for c in CELL.findall(rb.group(1))]
            if cells:
                rows.append(cells)
        if rows:
            out['rows'].append(rows)
    # detailModal 块
    m = re.search(r'<div class="modal-overlay" id="detailModal">(.*?)</div>\s*(?=<script|<!--|<div class="modal-overlay"|</body>)', raw, re.S)
    if m:
        out['modal'] = m.group(0)[:6000]
    return out


if __name__ == '__main__':
    targets = sys.argv[1:] or PAGES
    dump = []
    for rel in targets:
        p = ROOT / rel
        if not p.exists():
            dump.append({'page': rel, 'error': 'FILE NOT FOUND'})
            continue
        dump.append(extract_page(rel))
    tag = 'batch1' if len(targets) == 8 and '租赁单列表' in targets[0] else ('all' if len(targets) > 10 else 'custom')
    outp = OUT / ('dd-extract-%s.json' % tag)
    outp.write_text(json.dumps(dump, ensure_ascii=False, indent=1), encoding='utf-8')
    print('written:', outp, len(dump), 'pages')
