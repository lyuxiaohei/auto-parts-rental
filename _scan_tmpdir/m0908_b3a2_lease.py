# -*- coding: utf-8 -*-
"""批3 A2-补：租赁单新建（模板+内嵌）重构重跑（两文件已从 git 恢复）"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"

PRODUCTS = ['WBX-1210L 围板箱 1200×1000×970', 'WBX-1210M 围板箱 1200×1000×590', 'PLT-1210W 木托盘 1200×1000',
            'PLT-1210P 塑料托盘 1200×1000', 'BTC-6040 料箱 600×400×340', 'LJ-A100 锁扣组件', 'LJ-C300 围板',
            'LJ-D400 箱盖', 'LJ-F600 内衬']
ZH = ['ZH-2601-A 驾驶室围板箱整箱套件', 'ZH-2602-B 冲压件料箱组套', 'ZH-2603-C 电池托盘护角套件', 'ZH-2604-D 混合组合套件']
SEL_STYLE = 'width:100%;min-width:0;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;'
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

def make_select(options, cur):
    opts = []
    for p in options:
        sel = ' selected' if p.startswith(cur) else ''
        opts.append(f'<option{sel}>{p}</option>')
    return '<select style="' + SEL_STYLE + '">' + ''.join(opts) + '</select>'

def fmt(n):
    return f'{n:,.2f}'

def trans_lease(txt, tag):
    nl = '\r\n' if '\r\n' in txt else '\n'
    m = re.search(r'<div class="form-row">\s*<span class="form-label"><span class="req">\*</span>约定归还日期</span>.*?</div>\s*</div>\s*', txt, re.S)
    assert m, f'{tag} 约定归还日期行未找到'
    txt = txt[:m.start()] + txt[m.end():]
    c = txt.count('<span class="req">*</span>起租日期')
    assert c == 1, (tag, c)
    txt = txt.replace('<span class="req">*</span>起租日期', '<span class="req">*</span>建单日期')
    type_row = ('  <div class="form-row">' + nl +
                '    <span class="form-label"><span class="req">*</span>单据类型</span>' + nl +
                '    <div class="input-box select-box" style="width:350px;"><select onchange="var n=document.getElementById(\'bbNote\');if(n)n.style.display=(this.value==\'背靠背\')?\'block\':\'none\'" style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>常规</option><option>背靠背</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>' + nl +
                '  </div>' + nl +
                '  <div id="bbNote" style="display:none;margin:0 0 8px 128px;font-size:12px;color:#d4380d;">背靠背：租赁单确认后自动生成租入单草稿（供应商自选 → 新建状态 → 修改 → 提交）</div>' + nl)
    m2 = re.search(r'(<div class="form-row">\s*<span class="form-label"><span class="req">\*</span>客户</span>.*?</div>\s*</div>)\s*', txt, re.S)
    assert m2, f'{tag} 客户行未找到'
    txt = txt[:m2.end()] + nl + type_row + txt[m2.end():]
    old_th = '<th>器具编码</th><th>器具名称</th><th>类型</th><th>单位</th><th>数量</th><th>日租金(元)</th>'
    new_th = ('<th>产品</th><th>产品名称</th><th>单位</th><th>数量</th>'
              '<th style="font-size:13.5px;font-weight:700;">未税单价(元)</th>'
              '<th style="font-size:13.5px;font-weight:700;">税率</th>'
              '<th style="font-size:13.5px;font-weight:700;">含税单价(元)</th><th>含税金额(元)</th>')
    c = txt.count(old_th)
    assert c == 1, (tag, c)
    txt = txt.replace(old_th, new_th)
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
    new_tbody = ('<tbody>' + lr('ZH-2601-A', '驾驶室围板箱整箱套件', '套', '180', '2.40') + lr('PLT-1210P', '塑料托盘 1200×1000', '块', '180', '0.15') +
                 f'<tr><td colspan="7" style="text-align:right;font-weight:700;">租赁总价（含税 · 逐行加总）</td><td class="td-num" style="font-weight:700;">{fmt(total)}</td></tr></tbody>')
    tbl_pos = txt.find('<table class="edit-tbl"')
    assert tbl_pos > -1, f'{tag} edit-tbl 表格未找到'
    m3 = re.search(r'<tbody>.*?</tbody>', txt[tbl_pos:], re.S)
    assert m3, f'{tag} 明细 tbody 未找到'
    pos = tbl_pos + m3.start()
    txt = txt[:pos] + new_tbody + txt[pos + m3.end():]
    if TAX_JS_MARKER not in txt:
        txt = txt.replace('</body>', TAX_JS + '</body>')
    return txt

for rel in ['租赁管理/弹窗/租赁单新建.html', '租赁管理/租赁单列表.html']:
    f = PROTO / rel
    txt = trans_lease(f.read_bytes().decode('utf-8'), rel)
    f.write_bytes(txt.encode('utf-8'))
    print('✓', rel, '| data-tax:', txt.count('data-tax'), '| JS:', txt.count(TAX_JS_MARKER), '| 背靠背:', txt.count('背靠背'), '| 建单日期:', txt.count('建单日期'))
