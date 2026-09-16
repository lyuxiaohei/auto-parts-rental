#!/usr/bin/env python3
# G42 T7b 终扫（fresh 重采 + 同义覆盖表 + TH 明细列登记性口径）
import json, re, os
from playwright.sync_api import sync_playwright

ROOT = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型'
OUT = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/_scan_tmpdir/g42_t7b_rescan.json'

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

SYNONYMS = [
    ('物料', '器具'), ('盘点口径', '盘点基准'), ('盘点日期', '创建日期'),
    ('合同起止（框架）', '租期'), ('出库类型', '出库方式'), ('收货地点', '送达地点'),
    ('退回日期', '入库日期'), ('付款银行', '付款账户'), ('收款银行', '收款账户'),
    ('费用分类', '费用类型'), ('费用分类', '费用说明'), ('关联采购订单号', '来源单据'),
    ('关联租入单号', '来源单据'), ('预计到货日期', '交货日期'), ('仓管员', '制单人'),
    ('关联原单', '关联采购入库'), ('关联原单', '关联销售出库'), ('退款日期', '登记日期'),
]
EXCLUDE = re.compile(r'附件|上传|审核结论|审核意见|驳回原因')

def norm(t):
    return re.sub(r'[\s\*：:\u3000]', '', t or '')

def covered(flabel, dlabels):
    core = norm(flabel)
    ds = [norm(x) for x in dlabels]
    for d in ds:
        if d == core or (len(core) >= 2 and core in d) or (len(d) >= 2 and d in core):
            return True
    for a, b in SYNONYMS:
        if norm(a) == core and norm(b) in ds:
            return True
        if norm(b) == core and norm(a) in ds:
            return True
    return False

JS_NEW = """() => {
  const out = [];
  document.querySelectorAll('.form-label').forEach(el => out.push(el.textContent.trim()));
  document.querySelectorAll('table th').forEach(el => {
    const t = el.textContent.trim();
    if (t && t.length <= 12) out.push('TH::' + t);
  });
  return out;
}"""
JS_DET = """() => {
  const out = [];
  document.querySelectorAll('.dlabel').forEach(el => out.push(el.textContent.trim()));
  document.querySelectorAll('.dt-sec').forEach(el => out.push(el.textContent.trim()));
  document.querySelectorAll('.content table th, #detailBody table th').forEach(el => {
    const t = el.textContent.trim();
    if (t && t.length <= 12) out.push(t);
  });
  return out;
}"""

final = []
total_form_gaps = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    for newf, detf in PAIRS:
        item = {'pair': newf + ' × ' + detf, 'form_gaps': [], 'th_info': []}
        pg.goto('file://' + os.path.join(ROOT, newf), wait_until='networkidle')
        pg.wait_for_timeout(200)
        raw = pg.evaluate(JS_NEW)
        form, ths = [], []
        for t in raw:
            is_th = t.startswith('TH::')
            label = t[4:] if is_th else t
            if not label or EXCLUDE.search(label):
                continue
            (ths if is_th else form).append(label)
        pg.goto('file://' + os.path.join(ROOT, detf), wait_until='networkidle')
        pg.wait_for_timeout(200)
        det = [x for x in pg.evaluate(JS_DET) if x]
        item['form_gaps'] = [f for f in form if not covered(f, det)]
        item['th_info'] = [t for t in ths if not covered(t, det)]
        total_form_gaps += len(item['form_gaps'])
        final.append(item)
        print(item['pair'], '| 表单差集:', len(item['form_gaps']), item['form_gaps'] or '', '| 明细列登记:', len(item['th_info']))
    b.close()

json.dump(final, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('复查差集（表单区）:', total_form_gaps)
