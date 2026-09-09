# -*- coding: utf-8 -*-
"""批3 Script A2：租赁单新建重构（去租期/背靠背/明细三件套+总价）+ 租入单多货品明细 + 两录单页三件套（含 ctl.sel→真 select 产品下拉）"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"
LOG = []

PRODUCTS = ['WBX-1210L 围板箱 1200×1000×970', 'WBX-1210M 围板箱 1200×1000×590', 'PLT-1210W 木托盘 1200×1000',
            'PLT-1210P 塑料托盘 1200×1000', 'BTC-6040 料箱 600×400×340', 'LJ-A100 锁扣组件', 'LJ-C300 围板',
            'LJ-D400 箱盖', 'LJ-F600 内衬']
ZH = ['ZH-2601-A 驾驶室围板箱整箱套件', 'ZH-2602-B 冲压件料箱组套', 'ZH-2603-C 电池托盘护角套件', 'ZH-2604-D 混合组合套件']
SEL_STYLE = 'width:100%;min-width:0;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;'

def make_select(options, cur, style_extra=''):
    opts = []
    for p in options:
        sel = ' selected' if p.startswith(cur) else ''
        opts.append(f'<option{sel}>{p}</option>')
    if cur and not any(p.startswith(cur) for p in options):
        opts.insert(0, f'<option selected>{cur}</option>')
    return '<select style="' + SEL_STYLE + style_extra + '">' + ''.join(opts) + '</select>'

TAX_JS_MARKER = 'F-A 税率三件套双向换算'
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
    if (amt) amt.value = (num(q('qty')) * num(q('incl'))).toLocaleString('zh-CN', {minimumFractionDigits: 2, maximumFractionDigits: 2});
  });
})();
</script>'''

def inject_js(txt):
    if TAX_JS_MARKER in txt:
        return txt, 0
    return txt.replace('</body>', TAX_JS + '</body>'), 1

def fmt(n):
    return f'{n:,.2f}'

# ============================================================
# 1. 租赁单新建（模板 + 内嵌）
# ============================================================
def trans_lease(txt, tag):
    nl = '\r\n' if '\r\n' in txt else '\n'
    # 1a 去约定归还日期行
    m = re.search(r'  <div class="form-row">' + re.escape(nl) + r'\s*<span class="form-label"><span class="req">\*</span>约定归还日期</span>.*?</div>' + re.escape(nl) + r'\s*</div>' + re.escape(nl), txt, re.S)
    if not m:
        m = re.search(r'<div class="form-row">\s*<span class="form-label"><span class="req">\*</span>约定归还日期</span>.*?</div>\s*</div>\s*', txt, re.S)
    assert m, f'{tag} 约定归还日期行未找到'
    txt = txt[:m.start()] + txt[m.end():]
    # 1b 起租日期→建单日期
    c = txt.count('<span class="req">*</span>起租日期')
    assert c == 1, (tag, c)
    txt = txt.replace('<span class="req">*</span>起租日期', '<span class="req">*</span>建单日期')
    # 1c 单据类型（常规/背靠背）插在 客户 行后（form 第一个 form-row 后）
    type_row = ('  <div class="form-row">' + nl +
                '    <span class="form-label"><span class="req">*</span>单据类型</span>' + nl +
                '    <div class="input-box select-box" style="width:350px;"><select onchange="var n=document.getElementById(\'bbNote\');if(n)n.style.display=(this.value==\'背靠背\')?\'block\':\'none\'" style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>常规</option><option>背靠背</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>' + nl +
                '  </div>' + nl +
                '  <div id="bbNote" style="display:none;margin:0 0 8px 128px;font-size:12px;color:#d4380d;">背靠背：租赁单确认后自动生成租入单草稿（供应商自选 → 新建状态 → 修改 → 提交）</div>' + nl)
    m2 = re.search(r'(<div class="form-row">\s*<span class="form-label"><span class="req">\*</span>客户</span>.*?</div>\s*</div>)\s*', txt, re.S)
    assert m2, f'{tag} 客户行未找到'
    txt = txt[:m2.end()] + nl + type_row + txt[m2.end():]
    # 1d 明细表头
    old_th = '<th>器具编码</th><th>器具名称</th><th>类型</th><th>单位</th><th>数量</th><th>日租金(元)</th>'
    new_th = ('<th>产品</th><th>产品名称</th><th>单位</th><th>数量</th>'
              '<th style="font-size:13.5px;font-weight:700;">未税单价(元)</th>'
              '<th style="font-size:13.5px;font-weight:700;">税率</th>'
              '<th style="font-size:13.5px;font-weight:700;">含税单价(元)</th><th>含税金额(元)</th>')
    c = txt.count(old_th)
    assert c == 1, (tag, c)
    txt = txt.replace(old_th, new_th)
    # 1e 明细体重建（2 行 + 合计行）
    r1_code, r1_name, r1_unit, r1_qty, r1_price = 'ZH-2601-A', '驾驶室围板箱整箱套件', '套', '180', '2.40'
    r2_code, r2_name, r2_unit, r2_qty, r2_price = 'PLT-1210P', '塑料托盘 1200×1000', '块', '180', '0.15'
    def lr(code, name, unit, qty, price):
        qn = float(qty.replace(',', ''))
        inc = round(float(price) * 1.13, 2)
        return ('<tr><td>' + make_select(PRODUCTS + ZH, code) + '</td>'
                f'<td><input value="{name}"></td><td><input value="{unit}" style="width:48px;"></td>'
                f'<td><input data-tax="qty" value="{qty}"></td>'
                f'<td><input data-tax="excl" value="{price}"></td>'
                f'<td><input data-tax="rate" value="13%" style="width:56px;"></td>'
                f'<td><input data-tax="incl" value="{inc:.2f}"></td>'
                f'<td><input data-tax="amt" class="auto" value="{fmt(qn * inc)}" readonly></td></tr>')
    total = 180 * round(2.40 * 1.13, 2) + 180 * round(0.15 * 1.13, 2)
    new_tbody = ('<tbody>' + lr(*[r1_code, r1_name, r1_unit, r1_qty, r1_price]) + lr(*[r2_code, r2_name, r2_unit, r2_qty, r2_price]) +
                 f'<tr><td colspan="7" style="text-align:right;font-weight:700;">租赁总价（含税 · 逐行加总）</td><td class="td-num" style="font-weight:700;">{fmt(total)}</td></tr></tbody>')
    # 定位：edit-tbl 表格标签处（非 CSS 类定义），其后的第一个 tbody
    tbl_pos = txt.find('<table class="edit-tbl"')
    assert tbl_pos > -1, f'{tag} edit-tbl 表格未找到'
    m3 = re.search(r'<tbody>.*?</tbody>', txt[tbl_pos:], re.S)
    assert m3, f'{tag} 明细 tbody 未找到'
    pos = tbl_pos + m3.start()
    txt = txt[:pos] + new_tbody + txt[pos + m3.end():]
    txt, j = inject_js(txt)
    return txt, j

for rel in ['租赁管理/弹窗/租赁单新建.html', '租赁管理/租赁单列表.html']:
    f = PROTO / rel
    txt, j = trans_lease(f.read_bytes().decode('utf-8'), rel)
    f.write_bytes(txt.encode('utf-8'))
    LOG.append(f'{rel}: 租赁单重构（去归还规划·建单日期·背靠背·明细三件套+总价 {fmt(0) if False else ""}）+ JS {j}')

# ============================================================
# 2. 租入单新建（模板 + 内嵌）：多货品明细表格
# ============================================================
DETAIL_BLOCK = '''<div style="margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;">租入明细（多货品 · 计费方式：月租 / 按套）</div>
  <div class="table-wrap" style="border:1px solid var(--border);border-radius:6px;">
    <table class="edit-tbl">
      <thead><tr><th>产品</th><th>数量</th><th>计费方式</th><th>未税单价(元)</th><th style="font-size:13.5px;font-weight:700;">税率</th><th style="font-size:13.5px;font-weight:700;">含税单价(元)</th><th>含税金额(元)</th></tr></thead>
      <tbody><tr><td>__SEL1__</td><td><input data-tax="qty" value="30" style="width:64px;"></td><td><select style="width:88px;__ST__"><option selected>月租</option><option>按套</option></select></td><td><input data-tax="excl" value="400.00"></td><td><input data-tax="rate" value="13%" style="width:56px;"></td><td><input data-tax="incl" value="452.00"></td><td><input data-tax="amt" class="auto" value="13,560.00" readonly></td></tr><tr><td>__SEL2__</td><td><input data-tax="qty" value="50" style="width:64px;"></td><td><select style="width:88px;__ST__"><option>月租</option><option selected>按套</option></select></td><td><input data-tax="excl" value="1.20"></td><td><input data-tax="rate" value="13%" style="width:56px;"></td><td><input data-tax="incl" value="1.36"></td><td><input data-tax="amt" class="auto" value="68.00" readonly></td></tr></tbody>
    </table>
  </div>
  <button class="btn btn-dashed btn-sm" style="width:100%;margin-top:8px;">+ 添加明细行</button>
  <div style="margin-top:6px;font-size:12px;color:#8c8c8c;">计费＝月租金 + 按套数单价（无日租金，2026-09-08 会议）；应付生成方式取决于租入单模式（静态租入 / 背靠背）。</div>
'''

def trans_rentin(txt, tag):
    nl = '\r\n' if '\r\n' in txt else '\n'
    # 删 器具 / 数量 / 日租金 三行
    for label in ['<span class="req">*</span>器具</span>', '<span class="req">*</span>数量（只）</span>', '<span class="req">*</span>日租金（元/只）</span>']:
        m = re.search(r'<div class="form-row">\s*<span class="form-label">' + re.escape(label) + r'.*?</div>\s*</div>\s*', txt, re.S)
        assert m, f'{tag} {label[:20]} 未找到'
        txt = txt[:m.start()] + txt[m.end():]
    # 明细块插在 押金 行前
    m2 = re.search(r'<div class="form-row">\s*<span class="form-label">押金（元）</span>', txt)
    assert m2, f'{tag} 押金行未找到'
    block = DETAIL_BLOCK.replace('__SEL1__', make_select(PRODUCTS, 'WBX-1210L')).replace('__SEL2__', make_select(PRODUCTS, 'PLT-1210P')).replace('__ST__', 'border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;')
    txt = txt[:m2.start()] + block + nl + '  ' + txt[m2.start():]
    txt, j = inject_js(txt)
    return txt, j

for rel in ['租赁管理/弹窗/租入单新建.html', '租赁管理/租入单列表.html']:
    f = PROTO / rel
    txt, j = trans_rentin(f.read_bytes().decode('utf-8'), rel)
    f.write_bytes(txt.encode('utf-8'))
    LOG.append(f'{rel}: 租入单多货品明细重构 + JS {j}')

# ============================================================
# 3. 采购入库录单：明细加三件套 + ctl.sel 产品真下拉
# ============================================================
f = PROTO / '采购管理' / '采购入库录单.html'
txt = f.read_bytes().decode('utf-8')
old_th = '<th style="width:100px;">入库总数</th>'
new_th = ('<th style="width:100px;">入库总数</th>'
          '<th style="font-size:13.5px;font-weight:700;">未税单价(元)</th>'
          '<th style="font-size:13.5px;font-weight:700;">税率</th>'
          '<th style="font-size:13.5px;font-weight:700;">含税单价(元)</th><th>含税金额(元)</th>')
c = txt.count(old_th)
assert c == 1, c
txt = txt.replace(old_th, new_th)
# 行：入库总数 cell 后插三件套；产品 ctl.sel → 真 select
PRICE_MAP = {'LJ-A100': '6.80', 'LJ-C300': '52.00', 'LJ-F600': '15.50', 'WBX-1210L': '38.00', 'BTC-6040': '8.50'}
pat_total = re.compile(r'(<td class="td-num auto-cell">([\d,]+)</td>)')
def row_ins(m):
    total_qty = float(m.group(2).replace(',', ''))
    price = '6.80'  # 默认；行内产品已知时按表
    return (m.group(1) +
            f'<td class="td-num"><input data-tax="excl" value="{price}"></td>'
            '<td class="td-num"><input data-tax="rate" value="13%" style="width:56px;"></td>'
            f'<td class="td-num"><input data-tax="incl" value="{round(float(price)*1.13,2):.2f}"></td>'
            f'<td class="td-num"><input data-tax="amt" class="auto" value="{total_qty * round(float(price)*1.13,2):,.2f}" readonly></td>')
# 每行的产品码在 auto-cell 前，需按行处理：先按 <tr> 分块逐行替换
def transform_rows(txt):
    def tr_repl(m):
        row = m.group(0)
        mm = re.search(r'<span class="v">([A-Z]+-[\w]+)</span>', row)
        code = mm.group(1) if mm else None
        price = PRICE_MAP.get(code, '6.80')
        def ins(mm2):
            total_qty = float(mm2.group(2).replace(',', ''))
            inc = round(float(price) * 1.13, 2)
            return (mm2.group(1) +
                    f'<td class="td-num"><input data-tax="excl" value="{price}"></td>'
                    '<td class="td-num"><input data-tax="rate" value="13%" style="width:56px;"></td>'
                    f'<td class="td-num"><input data-tax="incl" value="{inc:.2f}"></td>'
                    f'<td class="td-num"><input data-tax="amt" class="auto" value="{total_qty * inc:,.2f}" readonly></td>')
        row2 = re.sub(r'<td class="td-num auto-cell">([\d,]+)</td>', ins, row, count=1)
        # 产品 ctl.sel → 真 select（第一列）
        row2 = re.sub(r'<td><div class="ctl sel" style="min-width:110px;"><span class="v">([A-Z]+-[\w]+)</span>.*?</div></td>',
                      lambda mm3: '<td>' + make_select(PRODUCTS, mm3.group(1), 'min-width:110px;') + '</td>', row2, count=1)
        return row2
    return re.sub(r'<tr>\n.*?</tr>', tr_repl, txt, flags=re.S)

txt = transform_rows(txt)
txt, j = inject_js(txt)
f.write_bytes(txt.encode('utf-8'))
LOG.append(f'采购入库录单: 明细三件套 + 产品真下拉 + JS {j}')

# ============================================================
# 4. 组合出库录单：明细加三件套 + 组合件真下拉
# ============================================================
f = PROTO / '租赁管理' / '组合出库录单.html'
txt = f.read_bytes().decode('utf-8')
old_th = '<th style="width:110px;">出库数量 *</th>'
new_th = ('<th style="width:110px;">出库数量 *</th>'
          '<th style="font-size:13.5px;font-weight:700;">未税单价(元)</th>'
          '<th style="font-size:13.5px;font-weight:700;">税率</th>'
          '<th style="font-size:13.5px;font-weight:700;">含税单价(元)</th><th>含税金额(元)</th>')
c = txt.count(old_th)
assert c == 1, c
txt = txt.replace(old_th, new_th)

ZH_PRICE = {'ZH-2601-A': '2.40', 'ZH-2602-B': '1.80', 'ZH-2603-C': '3.20', 'ZH-2604-D': '2.60'}
def transform_rows2(txt):
    def tr_repl(m):
        row = m.group(0)
        mm = re.search(r'<span class="v">(ZH-[\w-]+)</span>', row)
        price = ZH_PRICE.get(mm.group(1), '2.40') if mm else '2.40'
        qty_m = re.search(r'<td class="td-num"><input value="([\d,]+)"></td>', row)
        qty = float(qty_m.group(1).replace(',', '')) if qty_m else 0
        inc = round(float(price) * 1.13, 2)
        ins = (f'<td class="td-num"><input data-tax="excl" value="{price}"></td>'
               '<td class="td-num"><input data-tax="rate" value="13%" style="width:56px;"></td>'
               f'<td class="td-num"><input data-tax="incl" value="{inc:.2f}"></td>'
               f'<td class="td-num"><input data-tax="amt" class="auto" value="{qty * inc:,.2f}" readonly></td>')
        # 插在 出库数量 input td 之后
        row2 = re.sub(r'(<td class="td-num"><input value="[\d,]+"></td>)', lambda mm2: mm2.group(1) + ins, row, count=1)
        row2 = re.sub(r'<td><div class="ctl sel" style="min-width:120px;"><span class="v">(ZH-[\w-]+)</span>.*?</div></td>',
                      lambda mm3: '<td>' + make_select(ZH, mm3.group(1), 'min-width:120px;') + '</td>', row2, count=1)
        return row2
    return re.sub(r'<tr>\n.*?</tr>', tr_repl, txt, flags=re.S)

txt = transform_rows2(txt)
txt, j = inject_js(txt)
f.write_bytes(txt.encode('utf-8'))
LOG.append(f'组合出库录单: 明细三件套 + 组合件真下拉 + JS {j}')

print('== 批3 Script A2 ==')
for l in LOG:
    print(' ✓', l)
