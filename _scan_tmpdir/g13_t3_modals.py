# -*- coding: utf-8 -*-
"""G13 弹窗层改动（模板+宿主双层同步）：③付款方式 ④生成方式 ⑥计费方式 ⑦查库存 ⑧审核toast ⑩附件 ⑪可审单据+按角色匹配 ⑬上下游注记"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
WARN = []

def load(rel):
    raw = (ROOT / rel).read_bytes().decode('utf-8')
    return raw, ('\r\n' if '\r\n' in raw else '\n')

def rep(s, old, new, cnt, tag, soft=False):
    n = s.count(old)
    if n != cnt:
        if soft:
            WARN.append(f"[{tag}] 期望 {cnt} 实际 {n}（跳过）")
            return s
        raise AssertionError(f"[{tag}] 期望 {cnt} 实际 {n}: {old[:70]!r}")
    return s.replace(old, new)

def save(rel, s):
    (ROOT / rel).write_bytes(s.encode('utf-8'))

SEL_STYLE = "style=\"flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;\""
CARET = '<span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>'

# ================= ③ 付款方式（付款登记新建 模板+宿主）=================
PAY_ROW = ('<div class="form-row">' + '\n'
           + '    <span class="form-label">付款方式</span>' + '\n'
           + f'    <div class="input-box select-box" style="width:350px;"><select {SEL_STYLE}><option selected>银行转账</option><option>承兑</option><option>现金</option><option>票据</option></select>{CARET}</div>' + '\n'
           + '  </div>')
for rel in ["财务协同/弹窗/付款登记新建.html", "财务协同/付款登记.html"]:
    s, NL = load(rel)
    anchor = '</div><div class="form-row">' + NL + '    <span class="form-label">备注</span>'
    s = rep(s, anchor, '</div>' + PAY_ROW + '<div class="form-row">' + NL + '    <span class="form-label">备注</span>', 1, rel + " 付款方式")
    save(rel, s)
    print(rel, "OK：付款方式下拉（银行转账/承兑/现金/票据）")

# ================= ③b 付款确认（模板+宿主）：付款方式行 + 按角色匹配 =================
for rel in ["财务协同/弹窗/付款确认.html", "财务协同/付款登记.html"]:
    s, NL = load(rel)
    s = rep(s, '<div class="drow"><div class="dlabel">付款金额</div><div class="dval">6,000.00 元</div></div>',
            '<div class="drow"><div class="dlabel">付款金额</div><div class="dval">6,000.00 元</div></div>' + NL + '        <div class="drow"><div class="dlabel">付款方式</div><div class="dval">银行转账</div></div>',
            1, rel + " 付款方式行")
    s = rep(s, '<div class="dlabel">审核人（按角色配置）</div>', '<div class="dlabel">审核人（按角色匹配）</div>', 1, rel + " 按角色匹配", soft=True)
    save(rel, s)
    print(rel, "OK：付款确认 付款方式行+按角色匹配")

# ================= ④ 生成方式（应收账单生成 模板+宿主）=================
GEN_BLOCK = ('<div class="form-row">' + '\n'
    + '    <span class="form-label"><span class="req">*</span>生成方式</span>' + '\n'
    + '    <div><span class="radio checked" onclick="toggleUsageGen(false)"><span class="dot"></span>按月定期（现有默认）</span><span class="radio" onclick="toggleUsageGen(true)"><span class="dot"></span>按实际使用量</span></div>' + '\n'
    + '  </div>' + '\n'
    + '  <div id="usageHint" style="display:none;margin:-12px 0 12px 128px;font-size:12px;color:#595959;line-height:1.7;background:#fafafa;border:1px dashed #d9d9d9;border-radius:6px;padding:8px 12px;max-width:560px;">按实际使用量生成：按 <b>数量 × 单价</b> 计费，<b>按客户对账量录入</b>（以客户确认的对账量为准，非按月汇总）；示例：46,600 套·日 × 4.00 元 = 186,400.00 元。</div>')
GEN_JS = '<script>/* G13 ④ 生成方式切换 */' + '\n' + "function toggleUsageGen(usage) { var h = document.getElementById('usageHint'); if (h) h.style.display = usage ? 'block' : 'none'; }</script>" + '\n'
for rel in ["财务协同/弹窗/应收账单生成.html", "财务协同/应收账单.html"]:
    s, NL = load(rel)
    anchor = '<div class="form-row">' + NL + '    <span class="form-label"><span class="req">*</span>账单金额(元)</span>'
    s = rep(s, anchor, GEN_BLOCK + NL + anchor, 1, rel + " 生成方式")
    s = rep(s, "</body>", GEN_JS + "</body>", 1, rel + " 生成方式 js")
    save(rel, s)
    print(rel, "OK：生成方式单选+usage 说明区")

# ================= ⑥ 计费方式（租赁单新建 模板+宿主）+ ⑦ 查库存 =================
BILL_BLOCK = ('<div class="form-row">' + '\n'
    + '    <span class="form-label"><span class="req">*</span>计费方式</span>' + '\n'
    + '    <div><span class="radio checked" onclick="toggleBillingMode(false)"><span class="dot"></span>按月定期生成应收</span><span class="radio" onclick="toggleBillingMode(true)"><span class="dot"></span>按次套数对账</span></div>' + '\n'
    + '  </div>' + '\n'
    + '  <div id="billingHint" style="display:none;margin:-12px 0 12px 128px;font-size:12px;color:#595959;">按次套数对账：不按月生成应收，客户验收后按实际使用套数对账开单（G13 演示注记）。</div>')
BILL_JS = '<script>/* G13 ⑥ 租出计费方式切换 */' + '\n' + "function toggleBillingMode(byUsage) { var h = document.getElementById('billingHint'); if (h) h.style.display = byUsage ? 'block' : 'none'; }</script>" + '\n'

STOCK_JS_TPL = """<script>/* G13 ⑦ 新建优先查库存：选产品行内「可用库存 N 套」+不足红色提示条+生成采购订单/租入单（道远拍板） */
(function () {
  var STOCK_MAP = { 'WBX-1210L': [2120, '只'], 'WBX-1210M': [860, '只'], 'PLT-1210W': [60, '块'], 'PLT-1210P': [1410, '块'], 'BTC-6040': [3300, '只'], 'LJ-A100': [5260, '件'], 'LJ-B200': [2640, '件'], 'LJ-C300': [1860, '件'], 'LJ-D400': [980, '件'], 'LJ-F600': [1520, '件'], 'ZH-2601-A': [640, '套'], 'ZH-2602-B': [820, '套'], 'ZH-2603-C': [150, '套'], 'ZH-2604-D': [0, '套'] };
  var GOBASE = '__GB__';
  function num(v) { var x = parseFloat(String(v).replace(/,/g, '')); return isNaN(x) ? 0 : x; }
  function keyOf(text) { var m = String(text || '').trim().match(/^([A-Za-z]+-[\w.-]+)/); return m ? m[1] : ''; }
  function rowQty(tr) { var q = tr.querySelector('input[data-tax="qty"]'); return num(q ? q.value : 0); }
  function updRow(tr) {
    var sel = tr.querySelector('td select'); if (!sel) return;
    var k = keyOf(sel.value || (sel.options[sel.selectedIndex] || {}).text);
    var td = sel.closest('td');
    var hint = td.querySelector('.stock-hint');
    if (!hint) { hint = document.createElement('div'); hint.className = 'stock-hint'; hint.style.cssText = 'font-size:11px;color:#52c41a;margin-top:3px;white-space:nowrap;'; td.appendChild(hint); }
    var st = STOCK_MAP[k];
    if (!st) { hint.textContent = '可用库存 —（无库存记录）'; hint.style.color = '#8c8c8c'; return; }
    hint.textContent = '可用库存 ' + st[0] + ' ' + st[1];
    hint.style.color = rowQty(tr) > st[0] ? '#ff4d4f' : '#52c41a';
  }
  function refresh() {
    var lack = null;
    document.querySelectorAll('.edit-tbl tbody tr').forEach(function (tr) {
      if (!tr.querySelector('td select')) return;
      updRow(tr);
      var sel = tr.querySelector('td select');
      var k = keyOf(sel.value || (sel.options[sel.selectedIndex] || {}).text);
      var st = STOCK_MAP[k];
      if (st && rowQty(tr) > st[0]) lack = { name: k, need: rowQty(tr), have: st[0], unit: st[1] };
    });
    var w = document.getElementById('stockWarn');
    if (!w) return;
    if (lack) {
      w.style.display = 'block';
      var t = w.querySelector('.sw-txt');
      if (t) t.textContent = '可用库存不足（' + lack.name + '：需求 ' + lack.need + ' · 可用 ' + lack.have + ' ' + lack.unit + '）——可选择生成：';
    } else { w.style.display = 'none'; }
  }
  document.addEventListener('change', function (e) { if (e.target.matches && e.target.matches('.edit-tbl td select, .edit-tbl input[data-tax="qty"]')) refresh(); });
  document.addEventListener('input', function (e) { if (e.target.matches && e.target.matches('.edit-tbl input[data-tax="qty"]')) refresh(); });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', refresh); else refresh();
})();
</script>
"""
def warn_bar(gb):
    return ('<div id="stockWarn" style="display:none;margin-top:8px;padding:8px 12px;border:1px solid #ffa39e;background:#fff1f0;border-radius:6px;font-size:12px;color:#d4380d;line-height:1.9;">' + '\n'
        + '    <span class="sw-txt">可用库存不足——可选择生成：</span>' + '\n'
        + f'    <button class="btn btn-sm" style="margin-left:8px;" onclick="go(\'{gb}采购管理/采购订单列表.html\')">生成采购订单</button>' + '\n'
        + f'    <button class="btn btn-sm" style="margin-left:6px;" onclick="go(\'{gb}租赁管理/租入单列表.html\')">生成租入单</button>' + '\n'
        + '  </div>')

# ---- 租赁单新建（模板 ../../ + 宿主 ../）----
for rel, gb in [("租赁管理/弹窗/租赁单新建.html", "../../"), ("租赁管理/租赁单列表.html", "../")]:
    s, NL = load(rel)
    anchor = '</div><div style="margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;">租赁器具明细</div>'
    s = rep(s, anchor, '</div>' + BILL_BLOCK + '<div style="margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;">租赁器具明细</div>', 1, rel + " 计费方式")
    s = rep(s, '<button class="btn btn-dashed btn-sm" style="width:100%;margin-top:8px;">+ 添加一行</button>',
            '<button class="btn btn-dashed btn-sm" style="width:100%;margin-top:8px;">+ 添加一行</button>' + '\n  ' + warn_bar(gb), 1, rel + " 库存提示条")
    s = rep(s, "</body>", BILL_JS + STOCK_JS_TPL.replace("__GB__", gb) + "</body>", 1, rel + " 计费+库存 js")
    save(rel, s)
    print(rel, "OK：计费方式 radio+可用库存行内提示+不足双按钮")

# ---- 租赁单详情模板：⑥ 注释锚 ----
rel = "租赁管理/弹窗/租赁单详情.html"
s, NL = load(rel)
s = rep(s, "<!-- 注入标记：租赁管理/租赁单列表.html -->",
        "<!-- 注入标记：租赁管理/租赁单列表.html -->" + NL + "<!-- G13 ⑥ 计费方式：单据信息段动态渲染 demo-data leaseOrders info 行「计费方式」（按月定期生成应收/按次套数对账）——四段式详情无表单区，以信息行呈现 -->",
        1, rel + " 计费方式注释")
save(rel, s)
print(rel, "OK：计费方式注释锚")

# ---- 租赁单审核模板：⑧ toast + 按角色匹配 ----
rel = "租赁管理/弹窗/租赁单审核.html"
s, NL = load(rel)
s = rep(s, '<button class="btn" onclick="closeModal(\'auditModal\')">确认提交</button>',
        '<button class="btn" onclick="closeModal(\'auditModal\');showToast(\'已生成租入单草稿 RZD-20260910-009，供应商待选（背靠背自动生成）\')">确认提交</button>',
        1, rel + " 审核 toast")
s = rep(s, '<div class="dlabel">审核人（按角色配置）</div>', '<div class="dlabel">审核人（按角色匹配）</div>', 1, rel + " 按角色匹配")
s = rep(s, "</body>", '<script>/* G13 ⑧ 演示 toast */' + NL + "function showToast(msg) { var t = document.getElementById('g13Toast'); if (!t) { t = document.createElement('div'); t.id = 'g13Toast'; t.style.cssText = 'position:fixed;top:56px;left:50%;transform:translateX(-50%);z-index:1200;background:#fff;border:1px solid #1677ff;color:#1677ff;padding:8px 16px;border-radius:6px;font-size:13px;box-shadow:0 4px 12px rgba(0,0,0,.12);max-width:80vw;'; document.body.appendChild(t); } t.textContent = msg; t.style.display = 'block'; clearTimeout(window.__g13ToastT); window.__g13ToastT = setTimeout(function () { t.style.display = 'none'; }, 3200); }</script>" + NL + "</body>", 1, rel + " toast js")
save(rel, s)
print(rel, "OK：确认提交 toast+按角色匹配")

# ---- 销售订单审核：按角色匹配（模板+宿主，soft）----
for rel in ["销售管理/弹窗/销售订单审核.html", "销售管理/销售订单列表.html"]:
    s, NL = load(rel)
    s = rep(s, '<div class="dlabel">审核人（按角色配置）</div>', '<div class="dlabel">审核人（按角色匹配）</div>', 1, rel + " 按角色匹配", soft=True)
    save(rel, s)

# ---- 新建销售订单（模板+宿主）：⑦ 查库存 + ⑩ 附件 ----
ATT_BLOCK = ('<div style="margin:12px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;">订单附件（PDF / 邮件截图 · 演示上传）</div>' + '\n'
    + '  <div style="display:flex;gap:8px;align-items:center;margin-bottom:8px;">' + '\n'
    + '    <input id="attName" placeholder="输入附件文件名，如：PO-2601-合同.pdf / 客户邮件截图.png" style="flex:1;border:1px solid #d9d9d9;border-radius:4px;height:30px;padding:0 10px;font:inherit;font-size:13px;outline:none;">' + '\n'
    + '    <button class="btn btn-sm" type="button" onclick="addAttach()">添加</button>' + '\n'
    + '  </div>' + '\n'
    + '  <div id="attList">' + '\n'
    + '    <div class="att-row" style="display:flex;align-items:center;gap:8px;padding:6px 10px;border:1px solid #f0f0f0;border-radius:4px;margin-bottom:6px;font-size:12px;"><span>📄</span><span style="flex:1;">PO-2601-围板箱采购合同.pdf</span><span style="color:#8c8c8c;">1.2 MB</span><a onclick="delAttach(this)" style="color:#ff4d4f;cursor:pointer;">删除</a></div>' + '\n'
    + '    <div class="att-row" style="display:flex;align-items:center;gap:8px;padding:6px 10px;border:1px solid #f0f0f0;border-radius:4px;margin-bottom:6px;font-size:12px;"><span>📧</span><span style="flex:1;">客户下单确认邮件截图.png</span><span style="color:#8c8c8c;">356 KB</span><a onclick="delAttach(this)" style="color:#ff4d4f;cursor:pointer;">删除</a></div>' + '\n'
    + '  </div>')
ATT_JS = """<script>/* G13 ⑩ 订单附件假上传（文件名演示，不做真 file API） */
function addAttach() {
  var inp = document.getElementById('attName');
  if (!inp) return;
  if (!inp.value.trim()) { inp.style.borderColor = '#ff4d4f'; inp.placeholder = '请先输入附件文件名'; return; }
  var row = document.createElement('div');
  row.className = 'att-row';
  row.style.cssText = 'display:flex;align-items:center;gap:8px;padding:6px 10px;border:1px solid #f0f0f0;border-radius:4px;margin-bottom:6px;font-size:12px;';
  row.innerHTML = '<span>📄</span><span style="flex:1;">' + inp.value.trim().replace(/[<>]/g, '') + '</span><span style="color:#8c8c8c;">— KB</span><a onclick="delAttach(this)" style="color:#ff4d4f;cursor:pointer;">删除</a>';
  document.getElementById('attList').appendChild(row);
  inp.value = ''; inp.style.borderColor = '#d9d9d9';
}
function delAttach(a) { var r = a.closest('.att-row'); if (r) r.remove(); }</script>
"""
for rel, gb in [("销售管理/弹窗/新建销售订单.html", "../../"), ("销售管理/销售订单列表.html", "../")]:
    s, NL = load(rel)
    anchor = ('    <span class="form-label">备注</span>' + NL + '    <div class="input-box" style="width:350px;"><input placeholder="选填"></div>' + NL + '  </div>')
    s = rep(s, anchor, anchor + NL + '  ' + ATT_BLOCK, 1, rel + " 附件区")
    s = rep(s, '<button class="btn btn-dashed btn-sm" style="width:100%;margin-top:8px;">+ 添加一行</button>',
            '<button class="btn btn-dashed btn-sm" style="width:100%;margin-top:8px;">+ 添加一行</button>' + '\n  ' + warn_bar(gb), 1, rel + " 库存提示条")
    s = rep(s, "</body>", ATT_JS + STOCK_JS_TPL.replace("__GB__", gb) + "</body>", 1, rel + " 附件+库存 js")
    save(rel, s)
    print(rel, "OK：附件假上传+可用库存行内提示+不足双按钮")

# ---- 销售订单详情模板：⑩ 注释锚 ----
rel = "销售管理/弹窗/销售订单详情.html"
s, NL = load(rel)
s = rep(s, "<!-- 注入标记：销售管理/销售订单列表.html -->",
        "<!-- 注入标记：销售管理/销售订单列表.html -->" + NL + "<!-- G13 ⑩ 订单附件：单据信息段动态渲染 demo-data salesOrders info 行「订单附件」；新建弹窗侧为可交互假上传（文件名+添加+删除） -->",
        1, rel + " 附件注释")
save(rel, s)
print(rel, "OK：订单附件注释锚")

# ================= ⑪ 可审单据矩阵（模板+角色管理+用户权限）=================
MATRIX_ITEMS = ["采购订单", "销售订单", "租赁单", "租入单", "销售出库", "租赁出库", "采购入库", "租入入库", "退租入库", "其他入库", "其他出库", "盘点", "库存调拨", "租入归还"]
CHECKED = {"采购订单", "销售订单", "租赁单", "租入单", "销售出库", "租赁出库", "退租入库", "盘点"}
def matrix_html(intro):
    items = ''.join(
        f'        <span class="checkbox{" checked" if it in CHECKED else ""}" data-audit="{it}"><span class="box">{"✓" if it in CHECKED else ""}</span>{it}</span>' + '\n'
        for it in MATRIX_ITEMS)
    return ('      <div class="dt-sec" style="margin-top:18px;">可审单据</div>' + '\n'
        + '      <div id="auditPermMatrix" style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px 16px;padding:4px 0 2px;">' + '\n'
        + items
        + '      </div>' + '\n'
        + f'      <div style="font-size:12px;color:#8c8c8c;padding-top:6px;line-height:1.7;">{intro}</div>')
NOTE_STD = "勾选该角色可审核的单据类型；各审核弹窗「审核人（按角色匹配）」据此匹配（G13 · 纪要十.1）。"
# 权限配置模板 + 角色管理（数据权限范围后插）
for rel, note in [("系统管理/弹窗/权限配置.html", NOTE_STD), ("系统管理/角色管理.html", NOTE_STD)]:
    s, NL = load(rel)
    anchor = ('<span class="radio" data-scope="所属供应商"><span class="dot"></span>所属供应商</span>' + NL + '      </div>')
    s = rep(s, anchor, anchor + NL + matrix_html(note), 1, rel + " 可审单据")
    save(rel, s)
    print(rel, "OK：可审单据勾选矩阵")
# 用户权限（角色列表 modal 内同源矩阵段）
rel = "系统管理/用户权限.html"
s, NL = load(rel)
anchor = '</table>' + NL + '      </div>' + NL + '    </div>' + NL + '    <div class="modal-footer">'
s = rep(s, anchor,
        '</table>' + NL + '      </div>' + NL + matrix_html("与角色管理页·权限配置「可审单据」同源同步（双层同步 · G13）；正式版按所选角色加载勾选态。") + NL + '    </div>' + NL + '    <div class="modal-footer">',
        1, rel + " 可审单据")
save(rel, s)
print(rel, "OK：可审单据勾选矩阵（roleModal 内同源段）")

# ================= ⑬ 上下游绑定多对多注记（模板+项目档案+项目详情）=================
ZZ_NOTE = '<div style="font-size:12px;color:#8c8c8c;margin:10px 0 0;line-height:1.7;">设计预留：上下游支持一对多/多对多（2026-09-08 王总提出，本期不实现）——现演示为单客户/多供应商勾选，正式版关系结构预留扩展。</div>'
for rel in ["项目管理/弹窗/上下游绑定.html", "项目管理/项目档案.html", "项目管理/项目详情.html"]:
    s, NL = load(rel)
    anchor = '<option selected>华东中心仓（WH-01）</option><option>华南仓（WH-02）</option><option>西南仓（WH-03）</option></select><span class="caret">▾</span></div>'
    s = rep(s, anchor, anchor + NL + '    ' + ZZ_NOTE, 1, rel + " 多对多注记", soft=True)
    save(rel, s)
    print(rel, "OK：多对多设计预留注记")

# ================= ⑩b salesOrders info 行：订单附件（动态呈现）=================
rel = "_data/demo-data.js"
s, NL = load(rel)
i = s.index("salesOrders: {")
j = s.index("purchaseInbounds: {", i)
sec = s[i:j]
old = "{'label': '状态', 'text': '"
n = sec.count(old)
if n == 0:
    # info 块为多行样式：锚 'label': '状态',
    import re
    pat = re.compile(r"(\{\s*'label': '状态',\s*'text': '[^']*'\s*\},)")
    sec2, k = pat.subn(lambda mm: mm.group(1) + NL + "        {'label': '订单附件', 'text': 'PO-2601-围板箱采购合同.pdf · 客户下单确认邮件截图.png（新建可上传/删除，演示）'},", sec)
    assert k >= 6, f"salesOrders 附件 info 锚 {k} 处"
    sec = sec2
    n = k
else:
    sec = sec.replace(old, "{'label': '订单附件', 'text': 'PO-2601-围板箱采购合同.pdf · 客户下单确认邮件截图.png（新建可上传/删除，演示）'}," + NL + "        " + old)
s = s[:i] + sec + s[j:]
save(rel, s)
print(f"demo-data.js OK：salesOrders 订单附件 info 行 ×{n}")

print("\n== WARN 汇总 ==" if WARN else "\n== 无 WARN ==")
for w in WARN:
    print(" -", w)
