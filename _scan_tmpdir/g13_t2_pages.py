# -*- coding: utf-8 -*-
"""G13 页面层改动：库存查询 / 租赁单列表 / 租入单列表 / 租入归还列表 / 我的待办 + assetTracks 转租记录"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")

def load(rel):
    raw = (ROOT / rel).read_bytes().decode('utf-8')
    return raw, ('\r\n' if '\r\n' in raw else '\n')

def rep(s, old, new, cnt, tag):
    n = s.count(old)
    assert n == cnt, f"[{tag}] 期望 {cnt} 实际 {n}: {old[:70]!r}"
    return s.replace(old, new)

def save(rel, s):
    (ROOT / rel).write_bytes(s.encode('utf-8'))

TOAST_JS = """<script>/* G13 演示 toast（背靠背草稿链 / 三步入口反馈） */
function showToast(msg) {
  var t = document.getElementById('g13Toast');
  if (!t) { t = document.createElement('div'); t.id = 'g13Toast'; t.style.cssText = 'position:fixed;top:56px;left:50%;transform:translateX(-50%);z-index:1200;background:#fff;border:1px solid #1677ff;color:#1677ff;padding:8px 16px;border-radius:6px;font-size:13px;box-shadow:0 4px 12px rgba(0,0,0,.12);max-width:80vw;'; document.body.appendChild(t); }
  t.textContent = msg; t.style.display = 'block';
  clearTimeout(window.__g13ToastT); window.__g13ToastT = setTimeout(function () { t.style.display = 'none'; }, 3200);
}</script>
"""

# ================= 1. 库存查询.html =================
rel = "仓储作业/库存查询.html"
s, NL = load(rel)
# 1a filter-card CSS（页内原本无）
css_anchor = "/* ===== 本页业务样式 ===== */"
filter_css = """/* ===== 参考页筛选区样式 ===== */
.filter-card { background:#fff; border-radius:8px; padding:16px 18px; margin:0 0 12px; box-shadow:0 1px 3px rgba(0,0,0,0.05); }
.filter-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; }
.ff { display:flex; align-items:center; border:1px solid #d9d9d9; border-radius:6px; padding:0 10px; height:32px; background:#fff; transition:border-color .2s; }
.ff:focus-within { border-color:#1677ff; }
.ff .ff-label { flex-shrink:0; font-size:13px; color:#262626; margin-right:6px; white-space:nowrap; }
.ff input, .ff select { flex:1; min-width:0; border:none; outline:none; height:100%; font-size:13px; color:#262626; background:transparent; font-family:inherit; }
.ff input::placeholder { color:#bfbfbf; }
.ff select { appearance:none; -webkit-appearance:none; color:#8c8c8c; cursor:pointer; }
.ff .ff-chev { width:12px; height:12px; color:#8c8c8c; flex-shrink:0; pointer-events:none; }
.ff .ff-sep { margin:0 6px; color:#8c8c8c; flex-shrink:0; }
.filter-actions { display:flex; align-items:center; justify-content:flex-end; gap:10px; height:32px; }
""" + css_anchor
s = rep(s, css_anchor, filter_css, 1, "库存查询 filter CSS")
# 1b filter-card HTML（插在库存四态查询卡片前）
card_anchor = '<div class="card">' + NL + '  <div class="card-head">' + NL + '    <h3 class="card-title" data-note="1">库存四态查询</h3>'
filter_html = """<div class="filter-card" id="filterCard">
  <div class="filter-grid">
    <div class="ff"><span class="ff-label">物料编码：</span><input placeholder="请输入物料编码"></div>
    <div class="ff"><span class="ff-label">库存状态：</span>
      <select><option selected>全部</option><option>在库</option><option>客户端(租出)</option><option>客户端(转租)</option><option>退租待入库</option></select>
      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    </div>
    <div class="filter-actions">
      <button class="btn btn-default">重置</button>
      <button class="btn btn-primary">查询</button>
    </div>
  </div>
</div>
""" + card_anchor
s = rep(s, card_anchor, filter_html, 1, "库存查询 filter HTML")
# 1c renderListPage filters 接线
s = rep(s, "  stabs: false," + NL + "  filters: [],",
        "  stabs: false," + NL + "  filters: [" + NL + "    { label: '物料编码', field: '_key' }," + NL + "    { label: '库存状态', field: 'status' }" + NL + "  ],",
        1, "库存查询 filters cfg")
# 1d 主表加「成本单价」列（th）
s = rep(s, "          <th>总量</th>" + NL + "          <th>单位</th>",
        "          <th>总量</th>" + NL + "          <th>成本单价</th>" + NL + "          <th>单位</th>",
        1, "库存查询 th 成本单价")
# 1e 客户在租下钻弹窗：desc 注记 + th + 5 行成本 td + 转租演示行
s = rep(s, "客户端（租出）按客户/项目下钻；行内「资产轨迹」查看该器具出租履历，「退租」直达退租入库录单。",
        "客户端（租出）按客户/项目下钻；行内「资产轨迹」查看该器具出租履历，「退租」直达退租入库录单。转租＝在租的子状态：客户将器具转租给终端用户，按来源标记区分（库存状态「客户端(转租)」）。",
        1, "rentDrill 转租注记")
s = rep(s, "<th>在租数量</th><th>资产来源</th>", "<th>在租数量</th><th>成本单价</th><th>资产来源</th>", 1, "rentDrill th")
for qty, unit, nxt, cost in [
    ("3,120", "只", "<td>自有</td>", "340.00"),
    ("1,020", "只", "<td>自有</td>", "296.00"),
    ("1,860", "块", "<td>自有</td>", "98.00"),
    ("180", "套", '<td><span class="tag tag-orange">混合（自购 + 租入-路凯）</span></td>', "428.00"),
    ("40", "套", "<td>自有</td>", "356.00"),
]:
    old = f'<b>{qty}</b> {unit}</span></td>' + nxt
    new = f'<b>{qty}</b> {unit}</span></td><td><span class="td-num">{cost}</span></td>' + nxt
    s = rep(s, old, new, 1, f"rentDrill row {qty}")
zz_tr = ('<tr><td><span class="lk">XNC-ZZ-WBX</span></td><td>围板箱 1200×1000×970（安吉智行·转租终端用户）</td>'
         '<td>安吉智行 → 终端用户·延锋座椅厂</td><td>PRJ-2605</td><td><span class="td-num"><b>240</b> 只</span></td>'
         '<td><span class="td-num">340.00</span></td><td>客户转租</td><td><span class="tag tag-orange">在租·转租</span></td>'
         '<td class="sticky-op"><span class="ops"><a onclick="openTrack(\'XNC-ZZ-WBX\')">资产轨迹</a><a onclick="go(\'../租赁管理/退租入库列表.html\')">退租</a></span></td></tr>')
# rentDrill 表尾（最后一行后插转租演示行）
old_tail = '</span></td></tr>' + NL + '      </tbody></table></div>'
new_tail = '</span></td></tr>' + NL + '        ' + zz_tr + NL + '      </tbody></table></div>'
s = rep(s, old_tail, new_tail, 1, "rentDrill 转租行")
save(rel, s)
print("库存查询.html OK：filter CSS+筛选卡+状态筛选+成本列+rentDrill 成本列+转租行+注记")

# ================= 2. 租赁单列表.html（⑧ toast + ⑤ cmpModal）=================
rel = "租赁管理/租赁单列表.html"
s, NL = load(rel)
# 2a 审核确认 toast（背靠背）
old_btn = '<button class="btn" onclick="closeModal(\'auditModal\')">确认提交</button>'
new_btn = '<button class="btn" onclick="closeModal(\'auditModal\');showToast(\'已生成租入单草稿 RZD-20260910-009，供应商待选（背靠背自动生成）\')">确认提交</button>'
s = rep(s, old_btn, new_btn, 1, "租赁单审核 toast")
# 2b cmpModal 插在 auditModal 之后
idx = s.index("id=\"auditModal\"")
endmark = '</div>' + NL + '</div>'
pos = s.index(endmark, idx) + len(endmark)
cmp = NL + '<!-- G13 ⑤ 退回对比弹窗（少退/丢损 · 纪要八.4） -->' + NL + """<div class="modal-overlay" id="cmpModal">
  <div class="modal modal-lg" style="width:720px;">
    <div class="modal-header">
      <h3 class="modal-title">退回对比 · ZL-20260828-031</h3>
      <span class="modal-close" onclick="closeModal('cmpModal')">×</span>
    </div>
    <div class="modal-body">
      <p style="font-size:12px;color:#8c8c8c;line-height:1.7;margin-bottom:10px;">少退/丢损对比：出库量 vs 已退回；未退回差异转丢损赔偿依据（丢损赔偿单联动应收）。静态演示数据。</p>
      <div class="table-wrap"><table><thead><tr><th>货品</th><th>出库量</th><th>已退回</th><th>未退回差异</th><th>状态</th></tr></thead><tbody>
        <tr><td>ZH-2602-B 冲压件料箱组套</td><td><span class="td-num">120 套</span></td><td><span class="td-num">118 套</span></td><td><span class="td-num" style="color:#ff4d4f;">-2 套</span></td><td><span class="tag tag-orange">丢损待赔</span></td></tr>
        <tr><td>PLT-1210P 塑料托盘 1200×1000</td><td><span class="td-num">60 块</span></td><td><span class="td-num">60 块</span></td><td><span class="td-num">0 块</span></td><td><span class="tag tag-green">全部退回</span></td></tr>
        <tr><td>LJ-D400 箱盖 ABS 吸塑</td><td><span class="td-num">300 件</span></td><td><span class="td-num">296 件</span></td><td><span class="td-num" style="color:#ff4d4f;">-4 件</span></td><td><span class="tag tag-orange">丢损待赔</span></td></tr>
        <tr><td>BTC-6040 料箱 600×400×340</td><td><span class="td-num">40 只</span></td><td><span class="td-num">12 只</span></td><td><span class="td-num" style="color:#fa8c16;">-28 只</span></td><td><span class="tag tag-blue">部分退租（12/40）</span></td></tr>
      </tbody></table></div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-default" onclick="closeModal('cmpModal')">关 闭</button>
    </div>
  </div>
</div>"""
s = s[:pos] + cmp + s[pos:]
# 2c showToast helper（</body> 前）
s = rep(s, "</body>", TOAST_JS + "</body>", 1, "租赁单列表 toast js")
save(rel, s)
print("租赁单列表.html OK：审核 toast+cmpModal+showToast")

# ================= 3. 租入单列表.html（⑧ stab+筛选 option+showToast）=================
rel = "租赁管理/租入单列表.html"
s, NL = load(rel)
s = rep(s, '<span class="stab active">全部<span class="stab-count">5</span></span>',
        '<span class="stab active">全部<span class="stab-count">6</span></span>' + NL + '  <span class="stab">新建(草稿)<span class="stab-count">1</span></span>',
        1, "租入单 stab")
s = rep(s, '<select><option value="">全部</option><option>待审核</option>',
        '<select><option value="">全部</option><option>新建(草稿)</option><option>待审核</option>',
        1, "租入单 状态筛选 option")
s = rep(s, "</body>", TOAST_JS + "</body>", 1, "租入单列表 toast js")
save(rel, s)
print("租入单列表.html OK：新建(草稿) stab+筛选 option+showToast")

# ================= 4. 租入归还列表.html（⑨ 关联租入单+明细同步+分批）=================
RI_NEW_SELECT = """<select id="riSelect" onchange="syncReturnItems(this)" style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected data-key="RZD-20260815-005">RZD-20260815-005（路凯·围板箱×10 · 部分归还）</option><option data-key="RZD-20260815-003">RZD-20260815-003（路凯·围板箱×30 · 履行中）</option><option data-key="RZD-20260902-008">RZD-20260902-008（路凯·塑料托盘×60 · 待审核）</option></select>"""
RI_OLD_SELECT = """<select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>RZD-20260815-005（围板箱 × 10 只 · 履行中）</option><option>RZD-20260815-003（路凯·围板箱×30）</option><option>RZD-20260815-005（路凯·围板箱×10）</option><option>RZD-20260902-008（待审核）</option></select>"""
RI_DETAIL = """<div class="form-row" id="riDetailRow">
        <span class="form-label"><span class="req">*</span>归还明细</span>
        <div style="flex:1;min-width:0;">
          <div class="table-wrap" style="border:1px solid var(--border);border-radius:6px;">
            <table class="edit-tbl">
              <thead><tr><th>货品</th><th>租入数量</th><th>已归还</th><th>本次归还数量</th></tr></thead>
              <tbody id="riItemsBody"></tbody>
            </table>
          </div>
          <div class="pn-hint">支持分批：多个归还单可对应一个租入单；逐货品填写本次归还数量，「已归还」为该租入单历史累计（数据源：demo-data rentInOrders）。</div>
        </div>
      </div>"""
RI_JS = """<script>/* G13 ⑨ 关联租入单 → 归还明细同步（demo-data rentInOrders.returnItems；无数据环境回退静态演示） */
function syncReturnItems(sel) {
  var key = sel.selectedOptions[0].getAttribute('data-key');
  var items = null;
  try {
    var rec = window.DEMO_DATA && window.DEMO_DATA.rentInOrders && window.DEMO_DATA.rentInOrders[key];
    if (rec && rec.returnItems) items = rec.returnItems;
  } catch (e) { /* 独立模板无 demo-data，走静态回退 */ }
  if (!items) items = [{ item: 'WBX-1210L 围板箱 1200×1000×970', rentQty: 10, returned: 4, unit: '只' }];
  var tb = document.getElementById('riItemsBody');
  tb.innerHTML = items.map(function (it) {
    var left = Math.max(0, it.rentQty - it.returned);
    return '<tr><td>' + it.item + '</td><td><span class="td-num">' + it.rentQty + ' ' + it.unit + '</span></td>' +
      '<td><span class="td-num">' + it.returned + ' ' + it.unit + '</span></td>' +
      '<td><input value="' + left + '" placeholder="≤' + left + '"></td></tr>';
  }).join('');
}
syncReturnItems(document.getElementById('riSelect'));</script>
"""
for rel in ["租赁管理/租入归还列表.html", "租赁管理/弹窗/租入归还新建.html"]:
    s, NL = load(rel)
    s = rep(s, RI_OLD_SELECT, RI_NEW_SELECT, 1, rel + " ri select")
    # 明细块插在「归还类型」行后（锚=归还类型行的收尾 + 器具行开头）
    anchor = '分流归还（退租拆散后部分归还）</span></div>' + NL + '      </div>'
    s = rep(s, anchor, anchor + NL + '      ' + RI_DETAIL, 1, rel + " ri detail")
    s = rep(s, "</body>", RI_JS + "</body>", 1, rel + " ri js")
    save(rel, s)
    print(rel, "OK：关联下拉 data-key+明细同步+分批注记")

# ================= 5. 我的待办.html（⑫ 审核人筛选）=================
rel = "我的待办.html"
s, NL = load(rel)
s = rep(s, '<div class="ff"><span class="ff-label">关键词：</span>',
        """<div class="ff"><span class="ff-label">审核人：</span>
      <select id="todoAuditor" onchange="filterTodo()"><option>全部</option><option>王琳</option><option>袁丽晶</option><option>徐蔚</option><option>王强</option><option>李国栋</option><option>陈金</option><option>袁明</option></select>
    </div>
    <div class="ff"><span class="ff-label">关键词：</span>""",
        1, "待办 审核人筛选")
s = rep(s, "  var ty = document.getElementById('todoType').value;",
        "  var ty = document.getElementById('todoType').value;" + NL +
        "  var auEl = document.getElementById('todoAuditor');" + NL +
        "  var au = auEl ? auEl.value : '全部';",
        1, "待办 filterTodo 审核人读取")
s = rep(s, "var ok = (!ty || ty === '全部' || ty === tr.getAttribute('data-type')) && (!kw || tr.innerText.toLowerCase().indexOf(kw) > -1);",
        "var ok = (!ty || ty === '全部' || ty === tr.getAttribute('data-type')) && (au === '全部' || au === tr.getAttribute('data-auditor')) && (!kw || tr.innerText.toLowerCase().indexOf(kw) > -1);",
        1, "待办 filterTodo 条件")
s = rep(s, "html += '<tr data-type=\"' + f.type + '\">",
        "html += '<tr data-type=\"' + f.type + '\" data-auditor=\"' + (f.auditor || '') + '\">",
        1, "待办 行 data-auditor")
s = rep(s, "document.getElementById('todoKw').value='';document.getElementById('todoType').value='全部';filterTodo()",
        "document.getElementById('todoKw').value='';document.getElementById('todoType').value='全部';document.getElementById('todoAuditor').value='全部';filterTodo()",
        1, "待办 重置")
save(rel, s)
print("我的待办.html OK：审核人筛选+filterTodo 扩展+data-auditor+重置")

# ================= 6. demo-data assetTracks 转租轨迹记录 =================
rel = "_data/demo-data.js"
s, NL = load(rel)
i = s.index("assetTracks: {")
j = s.index("partners: {", i)
sec = s[i:j]
track = (
f"""    'XNC-ZZ-WBX': {{
      'title': '资产轨迹',
      'info': [
        {{'label': '器具编码', 'text': 'XNC-ZZ-WBX'}},
        {{'label': '名称', 'text': '围板箱 1200×1000×970（安吉智行·转租终端用户）', 'full': True}},
        {{'label': '库存状态', 'text': '客户端(转租)＝在租子状态'}},
        {{'label': '当前持有人', 'text': '终端用户·延锋座椅厂（客户安吉智行转租）', 'full': True}},
        {{'label': '在租数量', 'text': '240 只'}}
      ],
      'chain': [
        {{'role': '租入单', 'name': 'RZD-20260815-005 · 路凯', 'url': '租赁管理/租入单列表.html'}},
        {{'role': '租赁单', 'name': '客户安吉智行 · 转租出库', 'url': '租赁管理/租赁单列表.html'}},
        {{'role': '转租终端仓（当前）', 'name': 'XNC-ZZ-WBX · 240 只', 'self': True}}
      ],
      'timeline': [
        {{'t': '08-15', 'text': '路凯租入 240 只（RZD-20260815-005 关联批次）', 'who': '王志远'}},
        {{'t': '09-06', 'text': '客户安吉智行转租终端用户 · 240 只（转租＝在租子状态）', 'who': '王琳'}}
      ]
    }},
"""
).replace("True", "true").replace("\n", NL)
anchor = NL + "  },"
pos = sec.rindex(anchor)
sec = sec[:pos] + NL + track + sec[pos:]
s = s[:i] + sec + s[j:]
save(rel, s)
print("demo-data.js OK：assetTracks 增 XNC-ZZ-WBX 转租轨迹记录")
print("== g13_t2 全部完成 ==")
