#!/usr/bin/env python3
# G42 T7b: 全站「新建表单页 × 详情页」字段匹配扫描（只读；产出差集底稿）
import json, re, os, sys
from playwright.sync_api import sync_playwright

ROOT = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型'
OUT = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/_scan_tmpdir/g42_t7b_scan.json'

PAIRS = [
    ('仓储作业/其他入库新建.html', '仓储作业/其他入库详情.html'),
    ('仓储作业/其他出库新建.html', '仓储作业/其他出库详情.html'),
    ('仓储作业/盘点录入.html',     '仓储作业/盘点详情.html'),
    ('仓储作业/调拨新建.html',     '仓储作业/调拨详情.html'),
    ('基础数据/物料新建.html',     '基础数据/物料详情.html'),
    ('基础数据/客商新建.html',     '基础数据/客商详情.html'),
    ('基础数据/库位新建.html',     '基础数据/库位详情.html'),
    ('基础数据/BOM维护.html',      '基础数据/BOM版本查看.html'),
    ('租入管理/租入单新建.html',   '租入管理/租入单详情.html'),
    ('租入管理/租入归还新建.html', '租入管理/租入归还详情.html'),
    ('租赁管理/租赁单新建.html',   '租赁管理/租赁单详情.html'),
    ('租赁管理/租赁出库录单.html', '租赁管理/租赁出库详情.html'),
    ('租赁管理/退租入库新建.html', '租赁管理/退租入库详情.html'),
    ('租赁管理/转移出库新建.html', '租赁管理/转移出库单详情.html'),
    ('财务协同/付款新建.html',     '财务协同/付款详情.html'),
    ('财务协同/应付新建.html',     '财务协同/应付详情.html'),
    ('财务协同/应收生成.html',     '财务协同/应收详情.html'),
    ('财务协同/开票新建.html',     '财务协同/开票详情.html'),
    ('财务协同/收款新建.html',     '财务协同/收款详情.html'),
    ('财务协同/退款新建.html',     '财务协同/退款详情.html'),
    ('采购管理/采购订单新建.html', '采购管理/采购订单详情.html'),
    ('采购管理/采购入库录单.html', '采购管理/采购入库详情.html'),
    ('采购管理/采购退货新建.html', '采购管理/采购退货详情.html'),
    ('销售管理/销售订单新建.html', '销售管理/销售订单详情.html'),
    ('销售管理/销售出库新建.html', '销售管理/销售出库详情.html'),
    ('销售管理/销售退货新建.html', '销售管理/销售退货详情.html'),
    ('项目管理/项目新建.html',     '项目管理/项目详情.html'),
]

EXCLUDE = re.compile(r'附件|上传|审核结论|审核意见|驳回原因')

def norm(t):
    t = re.sub(r'[\s\*：:\u3000]', '', t or '')
    return t

JS_NEW = """() => {
  const out = [];
  document.querySelectorAll('.form-label').forEach(el => {
    out.push(el.textContent.trim());
  });
  // 明细表列头（edit-tbl / 明细区内表格）
  document.querySelectorAll('table th').forEach(el => {
    const t = el.textContent.trim();
    if (t && t.length <= 12) out.push('TH::' + t);
  });
  return out;
}"""
JS_DET = """() => {
  const out = [];
  document.querySelectorAll('.dlabel').forEach(el => out.push(el.textContent.trim()));
  document.querySelectorAll('.dt-sec').forEach(el => out.push('SEC::' + el.textContent.trim()));
  document.querySelectorAll('.content table th, #detailBody table th').forEach(el => {
    const t = el.textContent.trim();
    if (t && t.length <= 12) out.push('TH::' + t);
  });
  return out;
}"""

res = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    for newf, detf in PAIRS:
        item = {'new': newf, 'detail': detf, 'form_fields': [], 'detail_labels': [], 'gaps': [], 'weak': []}
        try:
            pg.goto('file://' + os.path.join(ROOT, newf), wait_until='networkidle')
            pg.wait_for_timeout(250)
            raw = pg.evaluate(JS_NEW)
            seen = set()
            for t in raw:
                is_th = t.startswith('TH::')
                label = t[4:] if is_th else t
                n = norm(label)
                if not n or EXCLUDE.search(label):
                    continue
                key = ('TH::' if is_th else '') + n
                if key not in seen:
                    seen.add(key)
                    item['form_fields'].append(key)
        except Exception as e:
            item['err_new'] = str(e)[:120]
        try:
            pg.goto('file://' + os.path.join(ROOT, detf), wait_until='networkidle')
            pg.wait_for_timeout(250)
            raw = pg.evaluate(JS_DET)
            seen = set()
            for t in raw:
                n = norm(t)
                if n and n not in seen:
                    seen.add(n)
                    item['detail_labels'].append(n)
        except Exception as e:
            item['err_detail'] = str(e)[:120]
        dset = item['detail_labels']
        for f in item['form_fields']:
            core = f.split('::')[-1]
            exact = any(d == f or d.split('::')[-1] == core for d in dset)
            sub = any((len(core) >= 2 and core in d) or (len(d.split('::')[-1]) >= 2 and d.split('::')[-1] in core) for d in dset)
            if exact:
                continue
            elif sub:
                item['weak'].append(f)
            else:
                item['gaps'].append(f)
        res.append(item)
        print(f"{newf}  form={len(item['form_fields'])} detail={len(item['detail_labels'])} gaps={len(item['gaps'])} weak={len(item['weak'])}")
    b.close()

json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved', OUT)
