# -*- coding: utf-8 -*-
"""批3 Script C：财务 4v4 + 赔偿直建文案 + 分期付款互算块
- receivableBills +2：供应商应收（路凯赔付我方）/ 预付款（保证金）
- payableBills +1：对客户应付（交付延误·断产赔偿）
- 应收/应付页加「账单类型」筛选（页面 select + renderListPage cfg）
- genMode 赔偿文案 → 直接口径
- 应付账单 + 付款登记新建（双层）分期计划块（1/2/3 期 · 比例⇄金额互算 · 末期补差 · 超额拦截注记）
"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"
DD = PROTO / "_data" / "demo-data.js"
LOG = []

src = DD.read_bytes().decode('utf-8')

def seg_bounds(txt, name):
    m = re.search(r'^  ' + name + r': \{', txt, re.M)
    assert m, name
    nxt = re.search(r'^  (?:[a-zA-Z_]+: \{|/\* -)', txt[m.end():], re.M)
    return m.start(), (m.end() + nxt.start() if nxt else len(txt))

# ============================================================
# 1. 应收 +2 记录（插在 receivableBills 首记录前）
# ============================================================
AR_SUPPLIER = """    'AR-20260904-015': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2603", "customer": "路凯包装运营（上海）有限公司", "btype": "供应商应收", "docs": "租入单 RZD-20260815-005 · 赔付我方", "gen": "直接生成", "date": "2026-09-04", "status": "未开票"}, "cells": ["2026-09", "PRJ-2603", "路凯包装运营（上海）有限公司", "<span class=\\"tag tag-blue\\">供应商应收</span><div style=\\"color:#8c8c8c;font-size:11px;\\">供应商赔付我方 · 租入围板箱缺损 6 只</div>", "租入单 RZD-20260815-005 · 赔付我方", "<span class=\\"td-num\\"><b>2,850.00</b></span>", "<span class=\\"td-num\\">0.00</span>", "<span class=\\"tag tag-red\\">未开票</span>", "<span class=\\"tag tag-orange\\">直接生成</span>", "2026-09-04 10:12"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "详情", "detail": true}, {"t": "开票", "act": "go('../财务协同/开票登记.html')"}]},
      'title': '应收账单详情',
      'billNo': 'AR-20260904-015',
      'billType': '供应商应收',
      'status': '未开票',
      'customer': '路凯包装运营（上海）有限公司',
      'project': 'PRJ-2603',
      'period': '2026-09',
      'amount': 2850,
      'paid': 0,
      'genMode': '直接生成（供应商赔付我方 · 无赔偿单，2026-09-08 会议 4v4）',
      'scenario': 'F1 · 供应商应收（4 来源）',
      'refs': [
        { label: '关联租入单', no: 'RZD-20260815-005', url: '租赁管理/租入单列表.html' }
      ],
      'fees': [
        { src: 'RZD-20260815-005', desc: '租入围板箱缺损赔付 · 供应商赔付我方', qty: '6 只', price: '475.00', amount: 2850, url: '租赁管理/租入单列表.html' }
      ],
      'chain': [
        { role: '租入单', name: 'RZD-20260815-005', url: '租赁管理/租入单列表.html' },
        { role: '应收账单（本单）', name: 'AR-20260904-015 · 供应商应收', self: true }
      ],
      'timeline': [
        { t: '09-04', text: '退租验收缺损 6 只 · 直接生成供应商应收（不走赔偿单）', who: '张伟' },
        { t: '—', text: '对方确认 → 开票 → 回款核销', who: '系统', off: true }
      ]
    },

"""
AR_PREPAY = """    'AR-20260906-016': {
      'row': {"fields": {"period": "2026-09", "project": "PRJ-2601", "customer": "一汽解放汽车有限公司", "btype": "预付款（保证金）", "docs": "客户保证金（N3 · 直接建单承载）", "gen": "直接生成", "date": "2026-09-06", "status": "已结清"}, "cells": ["2026-09", "PRJ-2601", "一汽解放汽车有限公司", "<span class=\\"tag tag-purple\\" style=\\"background:#f9f0ff;border-color:#d3adf7;color:#722ed1\\">预付款（保证金）</span><div style=\\"color:#8c8c8c;font-size:11px;\\">客户保证金 · 无订单 · 直接建单承载</div>", "客户保证金（N3 · 直接建单承载）", "<span class=\\"td-num\\"><b>50,000.00</b></span>", "<span class=\\"td-num\\">50,000.00</span>", "<span class=\\"tag tag-green\\">已结清</span>", "<span class=\\"tag tag-orange\\">直接生成</span>", "2026-09-06 09:30"], "ops": [{"t": "详情", "detail": true}]},
      'title': '应收账单详情',
      'billNo': 'AR-20260906-016',
      'billType': '预付款（保证金）',
      'status': '已结清',
      'customer': '一汽解放汽车有限公司',
      'project': 'PRJ-2601',
      'period': '2026-09',
      'amount': 50000,
      'paid': 50000,
      'genMode': '直接生成（无订单保证金/预付款 · 直接建单承载，挂应收侧 · T2 待财务确认）',
      'scenario': 'N3 · 预付款（保证金）',
      'refs': [],
      'fees': [
        { src: '—', desc: '客户保证金（无订单 · 退款场景待议）', qty: '—', price: '—', amount: 50000 }
      ],
      'chain': [
        { role: '预付款（保证金）', name: '客户直接建单 · 无订单', self: true }
      ],
      'timeline': [
        { t: '09-06', text: '客户保证金到账 50,000 · 直接建单承载（不做独立预付款模块/虚拟项目）', who: '财务-周敏' },
        { t: '—', text: '合同结束按约退还或冲抵后续应收', who: '系统', off: true }
      ]
    },

"""
s, e = seg_bounds(src, 'receivableBills')
first_rec = re.search(r"^    '", src[s:e], re.M)
ins = s + 1 + first_rec.start()
src = src[:ins] + AR_SUPPLIER + AR_PREPAY + src[ins:]
LOG.append('receivableBills +供应商应收 +预付款（保证金）')

# ============================================================
# 2. 应付 +1 对客户应付
# ============================================================
AP_CUST = """    'AP-20260905-013': {
      'row': {"fields": {"supplier": "一汽解放汽车有限公司", "btype": "对客户应付", "project": "PRJ-2601", "period": "2026-09", "ref": "—", "inbound": "—", "date": "2026-09-05", "status": "未付款"}, "cells": ["一汽解放汽车有限公司", "<span class=\\"tag tag-purple\\" style=\\"background:#f9f0ff;border-color:#d3adf7;color:#722ed1\\">对客户应付</span><div style=\\"color:#8c8c8c;font-size:11px;\\">交付延误 · 断产赔偿（赔付客户）</div>", "PRJ-2601", "2026-09", "—", "—", "<span class=\\"td-num\\">68,400.00</span>", "<span class=\\"td-num\\">0.00</span>", "<span class=\\"td-num\\" style=\\"color:var(--danger)\\">68,400.00</span>", "2026-09-05", "2026-09-20", "<span class=\\"tag tag-red\\">未付款</span>"], "ops": [{"t": "账单确认", "act": "openModal('auditModal')"}, {"t": "分期付款", "act": "go('../财务协同/付款登记.html')"}, {"t": "详情", "detail": true}]},
      'title': '应付账单详情',
      'billNo': 'AP-20260905-013',
      'billType': '对客户应付',
      'status': '未付款',
      'supplier': '一汽解放汽车有限公司（客户）',
      'project': 'PRJ-2601',
      'period': '2026-09',
      'amount': 68400,
      'paid': 0,
      'genMode': '直接生成（我方赔付客户 · 交付延误/断产/回款违约金，无赔偿单，2026-09-08 会议 4v4）',
      'scenario': 'F2 · 对客户应付（4 来源）',
      'refs': [],
      'fees': [
        { src: '—', desc: '断产赔偿 · 交付延误 12 天（合同条款）', amount: 68400 }
      ],
      'chain': [
        { role: '对客户应付（本单）', name: 'AP-20260905-013 · 赔付客户', self: true },
        { role: '付款登记', name: '分期计划 · 3 期', url: '财务协同/付款登记.html' }
      ],
      'timeline': [
        { t: '09-05', text: '断产赔偿认定 · 直接生成对客户应付（费用分类=违约金/断产赔偿）', who: '商务-王强' },
        { t: '—', text: '分期付款 3 期（40%/30%/30%）· 付款登记执行', who: '系统', off: true }
      ]
    },

"""
s, e = seg_bounds(src, 'payableBills')
first_rec = re.search(r"^    '", src[s:e], re.M)
ins = s + 1 + first_rec.start()
src = src[:ins] + AP_CUST + src[ins:]
LOG.append('payableBills +对客户应付')

# ============================================================
# 3. genMode 赔偿文案 → 直接口径
# ============================================================
n1 = src.count("genMode: '赔偿审核通过自动生成'")
src = src.replace("genMode: '赔偿审核通过自动生成'", "genMode: '直接生成（丢损赔付 · 无赔偿单，2026-09-08 会议）'")
n2 = src.count("genMode: '赔偿联动'")
src = src.replace("genMode: '赔偿联动'", "genMode: '直接生成（丢损赔付联动核销 · 无赔偿单）'")
LOG.append(f'genMode 赔偿文案改直接口径 {n1}+{n2}')

DD.write_bytes(src.encode('utf-8'))
import subprocess
r = subprocess.run(['node', '--check', str(DD)], capture_output=True, text=True)
assert r.returncode == 0, 'node --check: ' + r.stderr[:300]
LOG.append('node --check OK')

# ============================================================
# 4. 页面：类型筛选（应收/应付）+ 分期块
# ============================================================
def patch(rel, old, new, tag, exp=1):
    f = PROTO / rel
    txt = f.read_bytes().decode('utf-8')
    c = txt.count(old)
    assert c == exp, f'{rel}[{tag}] {c}≠{exp}'
    f.write_bytes(txt.replace(old, new).encode('utf-8'))
    LOG.append(f'{rel} [{tag}]')

# 4a 应收账单：加「账单类型」筛选（页面 select + cfg）
patch('财务协同/应收账单.html',
      '''    <div class="ff"><span class="ff-label">账单状态：</span>''',
      '''    <div class="ff"><span class="ff-label">账单类型：</span>
      <select><option selected>全部</option><option>租赁费</option><option>销售费</option><option>丢损赔偿（客户赔付我方）</option><option>供应商应收</option><option>预付款（保证金）</option></select>
      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    </div>
    <div class="ff"><span class="ff-label">账单状态：</span>''',
      '类型筛选', exp=1)
patch('财务协同/应收账单.html',
      "    { label: '账单编号', field: '_key' },",
      "    { label: '账单类型', field: 'btype', match: 'contains' },\n    { label: '账单编号', field: '_key' },",
      'cfg类型筛选')

# list-generic match contains? 检查：select 精确匹配字段 —— btype 含小字说明时用 contains。list-generic 的 select 匹配是 ===；
# 应收 btype fields 值为长文本，contains 更合适。list-generic 不支持 contains——改为把 fields.btype 存纯类型值。
# （上面 AR 记录 fields.btype 已是纯值；既有记录的 btype 是长文本 → 筛选按前缀 contains 需要 contains 支持）
# 方案：给 list-generic.js 增加 match:'contains' 支持
lg = PROTO / '_data' / 'list-generic.js'
txt = lg.read_bytes().decode('utf-8')
old_sel = """        var sel = ff.querySelector('select');
        if (sel) {
          var v = sel.value || (sel.options[sel.selectedIndex] || {}).text || '';
          v = v.trim();
          if (v && v !== '全部') preds.push(function (r) { return String(r.fields[f.field]) === v; });
          return;
        }"""
new_sel = """        var sel = ff.querySelector('select');
        if (sel) {
          var v = sel.value || (sel.options[sel.selectedIndex] || {}).text || '';
          v = v.trim();
          if (v && v !== '全部') preds.push(function (r) {
            var fv = String(r.fields[f.field] || '');
            return f.match === 'contains' ? fv.indexOf(v) > -1 : fv === v;
          });
          return;
        }"""
c = txt.count(old_sel)
assert c == 1, c
lg.write_bytes(txt.replace(old_sel, new_sel).encode('utf-8'))
LOG.append('list-generic.js select 筛选支持 match:contains')

# 4b 应付账单：加「账单类型」筛选
patch('财务协同/应付账单.html',
      '''    <div class="ff"><span class="ff-label">状态：</span>''',
      '''    <div class="ff"><span class="ff-label">账单类型：</span>
      <select><option selected>全部</option><option>采购应付</option><option>租金应付</option><option>赔付应付（赔付供应商）</option><option>对客户应付</option><option>预付</option></select>
      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    </div>
    <div class="ff"><span class="ff-label">状态：</span>''',
      '类型筛选')
m = re.search(r"filters: \[\n    \{ label: '应付账单号', field: '_key' \},", (PROTO / '财务协同/应付账单.html').read_bytes().decode('utf-8'))
assert m, '应付 cfg 未找到'
patch('财务协同/应付账单.html',
      "    { label: '应付账单号', field: '_key' },",
      "    { label: '账单类型', field: 'btype', match: 'contains' },\n    { label: '应付账单号', field: '_key' },",
      'cfg类型筛选')

# ============================================================
# 5. 分期计划块（应付账单卡片 + 付款登记新建弹窗双层）
# ============================================================
INST_HTML = '''<div class="card" id="instCard">
  <div class="card-head">
    <h3 class="card-title">分期计划（C-C/D · 比例⇄金额互算）</h3>
    <div class="head-btns">
      <select id="instN" style="border:1px solid #d9d9d9;border-radius:4px;padding:2px 6px;font:inherit;">
        <option value="1">分 1 期</option><option value="2" selected>分 2 期</option><option value="3">分 3 期</option>
      </select>
      <input id="instBase" value="68,400.00" style="border:1px solid #d9d9d9;border-radius:4px;padding:2px 8px;font:inherit;width:120px;text-align:right;" title="账单金额">
    </div>
  </div>
  <div class="table-wrap">
    <table>
      <thead><tr><th>期次</th><th>比例(%)</th><th>金额(元)</th><th>计划日期</th><th>状态</th></tr></thead>
      <tbody id="instBody"></tbody>
    </table>
  </div>
  <div class="pn-hint">分期互算：填比例自动算金额、填金额自动算比例，末期自动补差；账单头部展示「账单金额 / 已付 / 剩余」，付款时选金额，超出账单金额拦截（2026-09-08 会议 M2/C-C）。</div>
</div>
<script>/*C-C/D 分期比例⇄金额互算 · meeting0908 批3*/
(function () {
  function num(v){ var x = parseFloat(String(v).replace(/,/g,'')); return isNaN(x)?0:x; }
  function fmt(x){ return x.toLocaleString('zh-CN', {minimumFractionDigits:2, maximumFractionDigits:2}); }
  function base(){ var el = document.getElementById('instBase'); return el ? num(el.value) : 0; }
  function n(){ var el = document.getElementById('instN'); return el ? parseInt(el.value,10) : 2; }
  function render() {
    var tb = document.getElementById('instBody'); if (!tb) return;
    var rows = '', plans = ['2026-09-20', '2026-10-20', '2026-11-20'], N = n();
    var defs = N === 1 ? [100] : N === 2 ? [60, 40] : [40, 30, 30];
    for (var i = 0; i < N; i++) {
      var last = i === N - 1;
      rows += '<tr><td>第 ' + (i+1) + ' 期' + (last && N > 1 ? '（末期 · 自动补差）' : '') + '</td>'
        + '<td><input data-i="' + i + '" data-k="rate" value="' + defs[i].toFixed(2) + '" style="width:76px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 6px;"></td>'
        + '<td><input data-i="' + i + '" data-k="amt" value="' + fmt(base() * defs[i] / 100) + '" style="width:110px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 6px;text-align:right;"></td>'
        + '<td>' + plans[i] + '</td><td>' + (i === 0 ? '<span class="tag tag-orange">待付款</span>' : '<span class="tag tag-gray">未开始</span>') + '</td></tr>';
    }
    rows += '<tr><td style="font-weight:700;text-align:right;" colspan="2">合计（不得超账单金额，超出拦截）</td><td class="td-num" style="font-weight:700;" colspan="3">' + fmt(base()) + '</td></tr>';
    tb.innerHTML = rows;
  }
  document.addEventListener('input', function (e) {
    var i = e.target;
    if (!i.matches || !i.matches('#instCard input[data-i]')) return;
    var idx = parseInt(i.getAttribute('data-i'), 10), kind = i.getAttribute('data-k');
    var tb = document.getElementById('instBody'); if (!tb) return;
    var N = n(), b = base();
    var rates = [], amts = [], k, el;
    for (k = 0; k < N; k++) {
      var r = tb.querySelector('input[data-i="' + k + '"][data-k="rate"]');
      var a = tb.querySelector('input[data-i="' + k + '"][data-k="amt"]');
      rates.push(num(r.value)); amts.push(num(a.value));
    }
    if (kind === 'rate') { rates[idx] = num(i.value); amts[idx] = b * rates[idx] / 100; }
    else { amts[idx] = num(i.value); rates[idx] = b > 0 ? amts[idx] / b * 100 : 0; }
    if (N > 1) { /* 末期补差 */
      var rest = 0, rsum = 0;
      for (k = 0; k < N - 1; k++) { rest += amts[k]; rsum += rates[k]; }
      amts[N-1] = Math.max(0, b - rest); rates[N-1] = b > 0 ? amts[N-1] / b * 100 : 0;
    }
    for (k = 0; k < N; k++) {
      el = tb.querySelector('input[data-i="' + k + '"][data-k="rate"]'); if (el) el.value = rates[k].toFixed(2);
      el = tb.querySelector('input[data-i="' + k + '"][data-k="amt"]'); if (el) el.value = fmt(amts[k]);
    }
    if (rsum > 100.005 || (function(){ var s=0; for (k=0;k<N;k++) s+=amts[k]; return s > b + 0.005; })()) {
      i.style.borderColor = '#ff4d4f';
    } else { i.style.borderColor = '#d9d9d9'; }
  });
  document.addEventListener('change', function (e) { if (e.target && e.target.id === 'instN') render(); });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render); else render();
})();
</script>'''

# 5a 应付账单页：列表卡后插分期卡
f = PROTO / '财务协同' / '应付账单.html'
txt = f.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'
anchor = '<script src="../_data/demo-data.js"></script>'
assert txt.count(anchor) == 1
txt = txt.replace(anchor, INST_HTML + nl + anchor)
f.write_bytes(txt.encode('utf-8'))
LOG.append('应付账单 分期计划卡+互算JS')

# 5b 付款登记新建（弹窗模板 + 内嵌）：弹窗 body 尾部插分期块（modal 内版，id 前缀避免冲突——同页仅一处）
for rel in ['财务协同/弹窗/付款登记新建.html', '财务协同/付款登记.html']:
    f = PROTO / rel
    txt = f.read_bytes().decode('utf-8')
    nl = '\r\n' if '\r\n' in txt else '\n'
    m = re.search(r'(<div class="modal-overlay" id="createModal">.*?)(\n    </div>\s*\n    <div class="modal-footer">)', txt, re.S)
    assert m, rel + ' createModal footer 未找到'
    inst = INST_HTML.replace('id="instCard"', 'id="instCardModal"').replace("getElementById('instBody')", "getElementById('instBodyModal')") \
                    .replace("getElementById('instN')", "getElementById('instNModal')").replace("getElementById('instBase')", "getElementById('instBaseModal')") \
                    .replace('#instCard input', '#instCardModal input').replace("e.target.id === 'instN'", "e.target.id === 'instNModal'")
    # modal 内 card 样式简化：去 card 外壳、保留表+JS
    inst_block = ('<div style="margin:12px 0 4px;font-size:13px;font-weight:600;">分期计划（比例⇄金额互算 · 末期补差）</div>' + nl +
                  inst[inst.find('<div class="table-wrap">'):inst.find('<script>')].replace('id="instBodyModal"', 'id="instBodyModal"').replace('id="instNModal"', 'id="instNModal"').replace('id="instBaseModal"', 'id="instBaseModal"') + nl +
                  '<div style="font-size:12px;color:#8c8c8c;margin-top:4px;">填比例算金额 / 填金额算比例；末期自动补差；付款金额超出账单金额拦截。</div>' + nl +
                  inst[inst.find('<script>'):])
    txt = txt[:m.end(1)] + nl + inst_block + txt[m.end(1):]
    f.write_bytes(txt.encode('utf-8'))
    LOG.append(f'{rel} 分期块（弹窗内）')

print('== 批3 Script C ==')
for l in LOG:
    print(' ✓', l)
