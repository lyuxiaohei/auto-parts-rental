# -*- coding: utf-8 -*-
"""批3 Script A1：采购订单/销售订单/销售出库 表单三件套（模板+内嵌 6 文件）
- 明细列改：数量 / 未税单价 / 税率 / 含税单价 / 含税金额（未税·税率·含税列头加大加粗）
- 物料编码 input → 产品档案真 <select>（F-B）
- 注入 F-A 双向换算委托脚本（含税⇄未税，税率可改，金额=数量×含税）
- 采购订单：物料类型→类别、器具档案→产品档案
"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"
LOG = []

PRODUCTS = ['WBX-1210L 围板箱 1200×1000×970', 'WBX-1210M 围板箱 1200×1000×590', 'PLT-1210W 木托盘 1200×1000',
            'PLT-1210P 塑料托盘 1200×1000', 'BTC-6040 料箱 600×400×340', 'LJ-A100 锁扣组件', 'LJ-C300 围板',
            'LJ-D400 箱盖', 'LJ-F600 内衬']

SEL_STYLE = 'width:100%;min-width:0;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;'

def prod_select(cur):
    code = cur.strip()
    opts = []
    for p in PRODUCTS:
        sel = ' selected' if p.startswith(code) else ''
        opts.append(f'<option{sel}>{p}</option>')
    if code and not any(p.startswith(code) for p in PRODUCTS):
        opts.insert(0, f'<option selected>{code}</option>')
    return '<td><select data-tax="prod" style="' + SEL_STYLE + '">' + ''.join(opts) + '</select></td>'

def fmt(n):
    return f'{n:,.2f}'

TAX_JS = '''<script>/*F-A 税率三件套双向换算 · meeting0908 批3*/
(function () {
  function num(v){ var x = parseFloat(String(v).replace(/,/g,'')); return isNaN(x)?0:x; }
  document.addEventListener('input', function (e) {
    var i = e.target;
    if (!i.matches || !i.matches('input[data-tax]')) return;
    var tr = i.closest('tr'); if (!tr) return;
    function q(r){ var el = tr.querySelector('input[data-tax="'+r+'"]'); return el ? String(el.value).replace(/,/g,'') : '0'; }
    var rate = num(q('rate')) / 100;
    if (i.getAttribute('data-tax') === 'incl') {
      var ex = rate > 0 ? num(q('incl')) / (1 + rate) : num(q('incl'));
      var exEl = tr.querySelector('input[data-tax="excl"]'); if (exEl) exEl.value = ex.toFixed(2);
    } else {
      var inc = num(q('excl')) * (1 + rate);
      var incEl = tr.querySelector('input[data-tax="incl"]'); if (incEl) incEl.value = inc.toFixed(2);
    }
    var amt = tr.querySelector('input[data-tax="amt"]');
    if (amt) amt.value = fmtAmt(num(q('qty')) * num(q('incl')));
    function fmtAmt(x){ return x.toLocaleString('zh-CN', {minimumFractionDigits: 2, maximumFractionDigits: 2}); }
  });
})();
</script>'''

def inject_js(txt):
    if 'F-A 税率三件套双向换算' in txt:
        return txt, 0
    assert '</body>' in txt
    return txt.replace('</body>', TAX_JS + '</body>'), 1

def trans_po_so(txt, tag):
    n = 0
    # 1) 表头
    old_th = '<th>数量</th><th>单价(元)</th><th>金额(元)</th>'
    new_th = ('<th>数量</th><th style="font-size:13.5px;font-weight:700;">未税单价(元)</th>'
              '<th style="font-size:13.5px;font-weight:700;">税率</th>'
              '<th style="font-size:13.5px;font-weight:700;">含税单价(元)</th><th>含税金额(元)</th>')
    c = txt.count(old_th)
    assert c == 1, f'{tag} th {c}'
    txt = txt.replace(old_th, new_th); n += 1
    # 2) 行：数量/单价/金额 → 四件（data-tax + 预计算默认值兜底）
    pat = re.compile(r'<td><input value="([\d,]+)"></td><td><input value="([\d.]+)"></td><td><input class="auto" value="([\d,.]+)" readonly></td>')
    def row_repl(m):
        qty_s, price, _old_amt = m.group(1), m.group(2), m.group(3)
        qty = float(qty_s.replace(',', ''))
        inc = round(float(price) * 1.13, 2)
        amt = qty * inc
        return (f'<td><input data-tax="qty" value="{qty_s}"></td>'
                f'<td><input data-tax="excl" value="{price}"></td>'
                f'<td><input data-tax="rate" value="13%" style="width:56px;"></td>'
                f'<td><input data-tax="incl" value="{inc:.2f}"></td>'
                f'<td><input data-tax="amt" class="auto" value="{fmt(amt)}" readonly></td>')
    txt, k = pat.subn(row_repl, txt)
    assert k >= 1, f'{tag} rows {k}'
    n += k
    # 3) 物料编码 input → 产品 select（明细首列）
    pat2 = re.compile(r'<td><input value="([A-Z]{2,4}-[\w]+)"></td>')
    def sel_repl(m):
        return prod_select(m.group(1))
    txt, k2 = pat2.subn(sel_repl, txt)
    assert k2 >= 1, f'{tag} prod select {k2}'
    n += k2
    return txt, n

def process(rel, kind):
    f = PROTO / rel
    txt = f.read_bytes().decode('utf-8')
    if kind in ('po', 'so'):
        txt, n = trans_po_so(txt, rel)
    txt, j = inject_js(txt)
    f.write_bytes(txt.encode('utf-8'))
    LOG.append(f'{rel}: 三件套 {n} 处 + JS {j}')

# ---- 采购订单（模板+内嵌）+ 物料类型→类别 + 器具档案→产品档案 ----
for rel in ['采购管理/弹窗/新建采购订单.html', '采购管理/采购订单列表.html']:
    f = PROTO / rel
    txt = f.read_bytes().decode('utf-8')
    c1 = txt.count('<span class="req">*</span>物料类型')
    assert c1 == 1, (rel, c1)
    txt = txt.replace('<span class="req">*</span>物料类型', '<span class="req">*</span>类别')
    c2 = txt.count('<span class="req">*</span>器具档案')
    assert c2 == 1, (rel, c2)
    txt = txt.replace('<span class="req">*</span>器具档案', '<span class="req">*</span>产品档案')
    f.write_bytes(txt.encode('utf-8'))
    LOG.append(f'{rel}: 物料类型→类别 + 器具档案→产品档案')
    process(rel, 'po')

# ---- 销售订单（模板+内嵌）----
for rel in ['销售管理/弹窗/新建销售订单.html', '销售管理/销售订单列表.html']:
    process(rel, 'so')

# ---- 销售出库新建（模板+内嵌）：加三件套列 ----
for rel in ['销售管理/弹窗/销售出库新建.html', '销售管理/销售出库列表.html']:
    f = PROTO / rel
    txt = f.read_bytes().decode('utf-8')
    old_th = '<th>物料编码</th><th>物料名称</th><th>单位</th><th>出库数量</th><th>备注</th>'
    new_th = ('<th>产品</th><th>物料名称</th><th>单位</th><th>出库数量</th>'
              '<th style="font-size:13.5px;font-weight:700;">未税单价(元)</th>'
              '<th style="font-size:13.5px;font-weight:700;">税率</th>'
              '<th style="font-size:13.5px;font-weight:700;">含税单价(元)</th><th>含税金额(元)</th><th>备注</th>')
    c = txt.count(old_th)
    assert c == 1, (rel, c)
    txt = txt.replace(old_th, new_th)
    pat = re.compile(r'<td><input value="([A-Z]{2,4}-[\w]+)"></td>(<td><input value="[^"]*"></td><td><input value="[^"]*"></td>)<td><input value="([\d,]+)"></td><td><input value="" placeholder="选填"></td>')
    def row_repl(m):
        code, mid, qty_s = m.group(1), m.group(2), m.group(3)
        price = {'LJ-F600': '15.50'}.get(code, '1.28')
        qty = float(qty_s.replace(',', ''))
        inc = round(float(price) * 1.13, 2)
        return (prod_select(code) + mid +
                f'<td><input data-tax="qty" value="{qty_s}"></td>'
                f'<td><input data-tax="excl" value="{price}"></td>'
                f'<td><input data-tax="rate" value="13%" style="width:56px;"></td>'
                f'<td><input data-tax="incl" value="{inc:.2f}"></td>'
                f'<td><input data-tax="amt" class="auto" value="{fmt(qty * inc)}" readonly></td>'
                '<td><input value="" placeholder="选填"></td>')
    txt, k = pat.subn(row_repl, txt)
    assert k >= 1, (rel, k)
    txt, j = inject_js(txt)
    f.write_bytes(txt.encode('utf-8'))
    LOG.append(f'{rel}: 出库明细三件套 {k} 行 + JS {j}')

print('== 批3 Script A1 ==')
for l in LOG:
    print(' ✓', l)
