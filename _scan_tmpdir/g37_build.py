# -*- coding: utf-8 -*-
"""G37 T1：转移出库三页构建（列表/新建/详情·G36 终态范式=独立页面）
底版=采购退货三页（G33 建·G36 B2 页面化）。全部精确替换+assert，新文件允许整写。"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()

def wr(p, s):
    assert '\r\n' in s[:2000] or '\n' in s  # sanity
    io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

def swap(s, old, new, n=1):
    # 底版行尾混合（CRLF/LF）：先按原样匹配，失败再按 CRLF 规范化匹配
    for oe, ne in ((old, new), (old.replace('\n', '\r\n'), new.replace('\n', '\r\n'))):
        c = s.count(oe)
        if c == n:
            return s.replace(oe, ne)
    raise AssertionError('expect %d got %d/%d for: %r' % (n, s.count(old), s.count(old.replace('\n', '\r\n')), old[:80]))

# ============ 公共：菜单 v5→v6（租赁管理组插「转移出库」·退租入库前）+ 选中 ============
MENU_ZY = '<li><div class="sm-link" onclick="go(\'../租赁管理/转移出库列表.html\')">转移出库</div></li>'
MENU_TK = '<li><div class="sm-link" onclick="go(\'../租赁管理/退租入库列表.html\')">退租入库</div></li>'

def menu_v6(s, selected=False):
    assert s.count(MENU_TK) == 1
    item = MENU_ZY if not selected else '<li><div class="sm-link selected">转移出库</div></li>'
    return s.replace(MENU_TK, item + '\n   ' + MENU_TK)

def open_group(s):
    """租赁管理组展开（把 open 从采购组挪到租赁组——底版里采购组 open）"""
    # 底版：采购管理组 open。改：采购组收起、租赁组 open
    gi = s.index('采购管理<span class="sm-arrow">')
    li = s.rfind('<li class="sm-item has-sub open">', 0, gi)
    s = s[:li] + '<li class="sm-item has-sub">' + s[li + len('<li class="sm-item has-sub open">'):]
    gi = s.index('租赁管理<span class="sm-arrow">')
    li = s.rfind('<li class="sm-item has-sub">', 0, gi)
    s = s[:li] + '<li class="sm-item has-sub open">' + s[li + len('<li class="sm-item has-sub">'):]
    return s

def retie_selected(s):
    """底版 selected=采购退货 → 转移出库 selected"""
    old = '<li><div class="sm-link selected">采购退货</div></li>'
    assert s.count(old) == 1
    return s.replace(old, '<li><div class="sm-link" onclick="go(\'../采购管理/采购退货单列表.html\')">采购退货</div></li>')

PIN_LIST = ('<div class="proto-pin" id="proto-pin-1"><span class="pnp-close">×</span><div class="pnp-t"><span class="pnp-n">1</span>转移出库单（D-146）</div>'
            '<div class="pnp-d">直接客户→终端客户的器具转移，一步式·不勾稽原租赁单（D-106）。审核生效后库存状态转「客户转租出」；「终止转移」后回「在客户（租出）」。转租登记/转租还回弹窗已退场，由本单承载。</div>'
            '<div class="pnp-b"><span class="pnp-tag">D-106 · 转移出库</span><span class="pnp-tag">D-146 · 转租登记退场</span></div></div>')

# ================================================================
# 页1 转移出库列表
# ================================================================
def build_list():
    s = rd(os.path.join('采购管理', '采购退货单列表.html'))
    s = swap(s, '<title>采购退货 - 包装租赁管理后台</title>', '<title>转移出库 - 包装租赁管理后台</title>')
    # tabs
    s = swap(s, '''<div class="tabs">
  <span class="tab active">采购退货 <span class="close">×</span></span>
  <span class="tab">租赁出库 <span class="close">×</span></span>
  <span class="tab">库存查询 <span class="close">×</span></span>
</div>''', '''<div class="tabs">
  <span class="tab active">转移出库 <span class="close">×</span></span>
</div>''')
    # 菜单
    s = retie_selected(s)
    s = open_group(s)
    s = menu_v6(s, selected=True)
    # ---- 筛选卡整块替换 ----
    i = s.index('<div class="filter-card collapsed" id="filterCard">')
    j = s.index('</div>\r\n\r\n<div class="card">', i) + len('</div>')
    filt = '''<div class="filter-card" id="filterCard">
  <div class="filter-grid">
    <div class="ff"><span class="ff-label">转移单号：</span><input placeholder="请输入转移单号"></div>
    <div class="ff"><span class="ff-label">转出方：</span>
      <select><option value="">全部</option><option>安吉智行物流</option><option>长丰锂电科技</option><option>华骏重卡汽车有限公司</option></select>
      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    </div>
    <div class="ff"><span class="ff-label">接收方：</span><input placeholder="请输入终端客户名称"></div>
    <div class="ff"><span class="ff-label">结算方式：</span>
      <select><option value="">全部</option><option>按租出结算</option><option>按终端结算</option></select>
      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    </div>
    <div class="ff ff-row-extra"><span class="ff-label">状态：</span>
      <select><option value="">全部</option><option>待转移</option><option>已转移</option><option>已终止</option></select>
      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    </div>
    <div class="ff ff-row-extra"><span class="ff-label">转移日期：</span><input placeholder="开始日期"><span class="ff-sep">→</span><input placeholder="结束日期"></div>
    <div class="filter-actions">
      <button class="btn btn-default">重置</button>
      <button class="btn btn-primary">查询</button>
    </div>
  </div>
</div>'''
    s = s[:i] + filt + s[j:]
    # ---- 卡片区（title/stabs/表）替换：从 card-title 到 tbody 结尾 ----
    old_head = '<h3 class="card-title">采购退货单</h3>'
    assert s.count(old_head) == 1
    s = s.replace(old_head, '<h3 class="card-title">转移出库单</h3>')
    s = swap(s, '''<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="go('../采购管理/采购退货新建.html')">新建退货单</button>''',
             '''<button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="go('../租赁管理/转移出库新建.html')">新建转移出库</button>''')
    # stabs
    i = s.index('<div class="stabs">')
    j = s.index('</div>', s.index('<span class="stab">已退款', i)) + len('</div>')
    stabs = '''<div class="stabs">
  <span class="stab active">全部<span class="stab-count">5</span></span>
  <span class="stab">待转移<span class="stab-count">1</span></span>
  <span class="stab">已转移<span class="stab-count">3</span></span>
  <span class="stab">已终止<span class="stab-count">1</span></span>
</div>'''
    s = s[:i] + stabs + s[j:]
    # 表体
    i = s.index('<div class="table-wrap">', s.index('<div class="card">'))
    j = s.index('</table>', i) + len('</table>')
    tbl = '''<div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th></th>
          <th>转移单号</th>
          <th>转出方</th>
          <th>接收方</th>
          <th>物料</th>
          <th>数量</th>
          <th>结算方式</th>
          <th>转移日期</th>
          <th>状态</th>
          <th class="sticky-op">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">ZY-20260915-005</span></td>
          <td>安吉智行物流</td>
          <td>博世汽车部件（苏州）</td>
          <td>围板箱 1200×1000×970</td>
          <td><span class="td-num">200 只</span></td>
          <td>按租出结算</td>
          <td>2026-09-15</td>
          <td class="zy-status"><span class="tag tag-orange">待转移</span></td>
          <td class="sticky-op"><span class="ops"><a onclick="zyConfirm(this)">确认转移</a><a onclick="go('../租赁管理/转移出库单详情.html?id=ZY-20260915-005')">详情</a></span></td>
        </tr>
        <tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">ZY-20260914-003</span></td>
          <td>安吉智行物流</td>
          <td>博世汽车部件（苏州）</td>
          <td>料箱 600×400×340</td>
          <td><span class="td-num">360 只</span></td>
          <td>按租出结算</td>
          <td>2026-09-14</td>
          <td class="zy-status"><span class="tag tag-green">已转移</span></td>
          <td class="sticky-op"><span class="ops"><a onclick="go('../租赁管理/转移出库单详情.html?id=ZY-20260914-003')">详情</a><a onclick="zyStop(this)">终止转移</a></span></td>
        </tr>
        <tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk" data-note="1">ZY-20260914-002</span></td>
          <td>长丰锂电科技</td>
          <td>星辉动力电池有限公司</td>
          <td>电池包周转箱 1400×1000×680</td>
          <td><span class="td-num">80 只</span></td>
          <td>按终端结算</td>
          <td>2026-09-14</td>
          <td class="zy-status"><span class="tag tag-green">已转移</span></td>
          <td class="sticky-op"><span class="ops"><a onclick="go('../租赁管理/转移出库单详情.html?id=ZY-20260914-002')">详情</a><a onclick="zyStop(this)">终止转移</a></span></td>
        </tr>
        <tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">ZY-20260914-001</span></td>
          <td>安吉智行物流</td>
          <td>博世汽车部件（苏州）</td>
          <td>围板箱 1200×1000×970</td>
          <td><span class="td-num">240 只</span></td>
          <td>按租出结算</td>
          <td>2026-09-14</td>
          <td class="zy-status"><span class="tag tag-green">已转移</span></td>
          <td class="sticky-op"><span class="ops"><a onclick="go('../租赁管理/转移出库单详情.html?id=ZY-20260914-001')">详情</a><a onclick="zyStop(this)">终止转移</a></span></td>
        </tr>
        <tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">ZY-20260912-004</span></td>
          <td>安吉智行物流</td>
          <td>延锋汽车饰件（苏州）</td>
          <td>塑料托盘 1200×1000</td>
          <td><span class="td-num">120 张</span></td>
          <td>按租出结算</td>
          <td>2026-09-12</td>
          <td class="zy-status"><span class="tag tag-gray">已终止</span></td>
          <td class="sticky-op"><span class="ops"><a onclick="go('../租赁管理/转移出库单详情.html?id=ZY-20260912-004')">详情</a></span></td>
        </tr>
      </tbody>
    </table>
  </div>'''
    s = s[:i] + tbl + s[j:]
    # pager 总数
    s = swap(s, '<span class="pg-info">第 1-10 条/总共 326 条</span>', '<span class="pg-info">第 1-5 条/总共 5 条</span>')
    # 旧注释与 G33 脚本区
    s = swap(s, '''<!-- 审核已页面化（G36 B2） -->
<!-- 新建采购退货单已页面化：采购管理/采购退货新建.html（G36 B2·原 G33 模板） -->
<script>
/* G33 退货明细行新增（DOM 追加行） */
function addRetRow() {
  var tb = document.getElementById('retItems');
  if (!tb) return;
  var tr = document.createElement('tr');
  tr.innerHTML = '<td><input placeholder="选择物料"></td><td class="auto-cell">—</td><td><input value="1"></td><td><input value="0.00"></td><td class="auto-cell">0.00</td>';
  tb.appendChild(tr);
}
</script>''', '''<script>
/* G37 状态流：确认转移（待转移→已转移·库存状态转「客户转租出」）/ 终止转移（已转移→已终止·回「在客户（租出）」） */
function zyRow(a) {
  var tr = a.closest('tr');
  return { tr: tr, st: tr.querySelector('.zy-status') };
}
function zyConfirm(a) {
  var r = zyRow(a);
  if (!r.st || r.st.textContent.indexOf('待转移') < 0) return;
  r.st.innerHTML = '<span class="tag tag-green">已转移</span>';
  a.closest('.ops').innerHTML = '<a onclick="go(\\'../租赁管理/转移出库单详情.html?id=ZY-20260915-005\\')">详情</a><a onclick="zyStop(this)">终止转移</a>';
}
function zyStop(a) {
  var r = zyRow(a);
  if (!r.st || r.st.textContent.indexOf('已转移') < 0) return;
  r.st.innerHTML = '<span class="tag tag-gray">已终止</span>';
  a.closest('.ops').innerHTML = '<a onclick="go(\\'../租赁管理/转移出库单详情.html?id=ZY-20260914-001\\')">详情</a>';
}
</script>''')
    # pin 替换（pin-1 块边界 = 下一个 f01-fab-style）
    i = s.index('<div class="proto-pin" id="proto-pin-1">')
    j = s.index('<style id="f01-fab-style">', i)
    s = s[:i] + PIN_LIST + '\n' + s[j:]
    wr(os.path.join('租赁管理', '转移出库列表.html'), s)
    print('OK 转移出库列表.html', len(s))

# ================================================================
# 页2 转移出库新建
# ================================================================
def build_form():
    s = rd(os.path.join('采购管理', '采购退货新建.html'))
    s = swap(s, '<title>新建采购退货单 - 包装租赁管理后台</title>', '<title>新建转移出库单 - 包装租赁管理后台</title>')
    s = swap(s, '''<div class="tabs">
  <span class="tab">采购退货 <span class="close">×</span></span>
  <span class="tab active">新建采购退货单 <span class="close">×</span></span>
</div>''', '''<div class="tabs">
  <span class="tab" onclick="go('../租赁管理/转移出库列表.html')">转移出库 <span class="close">×</span></span>
  <span class="tab active">新建转移出库单 <span class="close">×</span></span>
</div>''')
    s = retie_selected(s)
    s = open_group(s)
    s = menu_v6(s, selected=True)
    # content 卡片整块（两张卡+提交条）
    i = s.index('<div class="card">')
    j = s.index('<script src="../_data/demo-data.js"></script>')
    body = '''<div class="card">
  <div class="card-head">
    <h3 class="card-title">转移信息</h3>
  </div>

      <div class="form-row">
        <div class="form-label">转移单号：</div>
        <div><div class="input-box" style="width:380px;background:#fafafa;"><span style="color:#8c8c8c;">ZY-20260915-006（自动生成 · 不可编辑）</span></div></div>
      </div>
      <div class="form-row">
        <div class="form-label"><span class="req">*</span>关联项目：</div>
        <div>
          <div class="input-box select-box" style="width:380px;"><select id="zyProj" onchange="zyProjChange()"><option selected>PRJ-2605 华骏重卡·蔚山基地 围板箱租赁扩建</option><option>PRJ-2603 长丰锂电·电池包周转箱租赁</option><option>PRJ-2601 华骏重卡·长春基地 驾驶室围板箱租赁</option></select><span class="caret">▾</span></div>
          <div class="form-tip" style="margin-left:12px;">选择项目后带出转出方与「转租结算方式」默认值，可按单覆盖</div>
        </div>
      </div>
      <div class="form-row">
        <div class="form-label"><span class="req">*</span>转出方（直接客户）：</div>
        <div><div class="input-box" style="width:380px;"><input id="zyFrom" value="安吉智行物流" placeholder="从项目带出，可修改"></div></div>
      </div>
      <div class="form-row">
        <div class="form-label"><span class="req">*</span>接收方（终端客户）：</div>
        <div>
          <div class="input-box select-box" style="width:380px;"><select id="zyToSel" onchange="zyToChange(this)"><option selected>博世汽车部件（苏州）</option><option>星辉动力电池有限公司</option><option>延锋汽车饰件（苏州）</option><option value="__manual">＋ 其他（手工录入）</option></select><span class="caret">▾</span></div>
          <div class="input-box" id="zyToInput" style="width:380px;display:none;margin-top:8px;"><input placeholder="输入终端客户简称/全称，不强制建档"></div>
        </div>
      </div>
      <div class="form-row">
        <div class="form-label"><span class="req">*</span>物料：</div>
        <div>
          <div class="input-box select-box" style="width:380px;"><select id="zyMat"><option selected>围板箱 1200×1000×970</option><option>塑料托盘 1200×1000</option><option>料箱 600×400×340</option><option>电池包周转箱 1400×1000×680</option></select><span class="caret">▾</span></div>
        </div>
      </div>
      <div class="form-row">
        <div class="form-label"><span class="req">*</span>转移数量：</div>
        <div><div class="input-box" style="width:380px;"><input value="200" placeholder="≤ 转出方当前在租量"></div></div>
      </div>
      <div class="form-row">
        <div class="form-label"><span class="req">*</span>转移日期：</div>
        <div><div class="input-box" style="width:380px;"><input type="date" value="2026-09-15"></div></div>
      </div>
      <div class="form-row" style="align-items:flex-start;">
        <div class="form-label" style="padding-top:6px;"><span class="req">*</span>结算方式：</div>
        <div>
          <div><span class="radio checked" id="zySettleL" onclick="zySettle('L')"><span class="dot"></span>按租出结算</span><span class="radio" id="zySettleT" onclick="zySettle('T')" style="margin-right:0;"><span class="dot"></span>按终端结算</span></div>
          <div class="pn-hint" id="zySettleHint">默认取项目档案「转租结算方式」（当前项目：按租出结算）。按租出结算＝租金仍向直接客户计收，转移单不进财务链路；按终端结算＝转移生效后后续账单主体切换为终端客户（历史账单不回改）。</div>
        </div>
      </div>
      <div class="form-row" style="align-items:flex-start;">
        <div class="form-label" style="padding-top:6px;">备注：</div>
        <div>
          <div class="input-box" style="width:380px;height:auto;padding:6px 11px;"><textarea placeholder="选填" style="width:100%;border:none;outline:none;background:transparent;font:inherit;color:inherit;resize:vertical;min-height:72px;line-height:1.6;"></textarea></div>
        </div>
      </div>
      </div>

<div class="submit-bar"><button class="btn btn-default" onclick="go('../租赁管理/转移出库列表.html')">取 消</button><button class="btn">保存草稿</button><button class="btn">提交审核</button></div>
    </div>
  </div>
</div>
<script>
/* G37：项目带出（客户+结算方式）/ 终端客户手工录入切换 / 结算方式覆盖 / 库存查询带参预填 */
var ZY_SETTLE = { 'PRJ-2605': ['安吉智行物流', '按租出结算'], 'PRJ-2603': ['长丰锂电科技', '按终端结算'], 'PRJ-2601': ['华骏重卡汽车有限公司', '按租出结算'] };
function zyProjChange() {
  var v = (document.getElementById('zyProj').value || '').split(' ')[0];
  var cfg = ZY_SETTLE[v] || ZY_SETTLE['PRJ-2605'];
  var from = document.getElementById('zyFrom');
  if (from) from.value = cfg[0];
  zySettle(cfg[1] === '按终端结算' ? 'T' : 'L');
  var hint = document.getElementById('zySettleHint');
  if (hint) hint.textContent = '默认取项目档案「转租结算方式」（当前项目：' + cfg[1] + '）。按租出结算＝租金仍向直接客户计收，转移单不进财务链路；按终端结算＝转移生效后后续账单主体切换为终端客户（历史账单不回改）。';
}
function zyToChange(sel) {
  var inp = document.getElementById('zyToInput');
  if (!inp) return;
  inp.style.display = (sel.value === '__manual') ? '' : 'none';
}
function zySettle(which) {
  var L = document.getElementById('zySettleL'), T = document.getElementById('zySettleT');
  if (!L || !T) return;
  L.classList.toggle('checked', which === 'L');
  T.classList.toggle('checked', which === 'T');
}
(function () {
  /* 库存查询行内「转移出库」跳转带参：?mat=物料名称&cust=转出客户 */
  try {
    var q = new URLSearchParams(location.search);
    var mat = q.get('mat'), cust = q.get('cust');
    if (mat) {
      var m = document.getElementById('zyMat');
      if (m) Array.prototype.forEach.call(m.options, function (o) { if (o.text === mat) m.value = o.value; });
    }
    if (cust) { var f = document.getElementById('zyFrom'); if (f) f.value = cust; }
  } catch (e) {}
})();
</script>
'''
    s = s[:i] + body + s[j:]
    # 删除 G33 addRetRow 脚本（若残留于 s[j:] 之前已替换则无）
    # pin 替换
    i = s.index('<div class="proto-pin" id="proto-pin-1">')
    j = s.index('<style id="f01-fab-style">', i)
    pin_form = ('<div class="proto-pin" id="proto-pin-1"><span class="pnp-close">×</span><div class="pnp-t"><span class="pnp-n">1</span>结算方式两值（D-132）</div>'
                '<div class="pnp-d">默认取项目档案「转租结算方式」，可单据级覆盖。按租出结算＝租金仍向直接客户计收，转移单不进财务链路；按终端结算＝生效后后续账单主体切终端客户，历史账单不回改。终端客户可选客商档案或手工录入（D-108·不强制建档）。</div>'
                '<div class="pnp-b"><span class="pnp-tag">D-132 · 结算方式两模式</span><span class="pnp-tag">D-108 · 终端客户口径</span></div></div>')
    s = s[:i] + pin_form + '\n' + s[j:]
    wr(os.path.join('租赁管理', '转移出库新建.html'), s)
    print('OK 转移出库新建.html', len(s))

# ================================================================
# 页3 转移出库单详情
# ================================================================
def build_detail():
    s = rd(os.path.join('采购管理', '采购退货详情.html'))
    s = swap(s, '<title>采购退货单详情 - 包装租赁管理后台</title>', '<title>转移出库单详情 - 包装租赁管理后台</title>')
    s = swap(s, '''<div class="tabs">
  <span class="tab">采购退货 <span class="close">×</span></span>
  <span class="tab active">采购退货详情 <span class="close">×</span></span>
</div>''', '''<div class="tabs">
  <span class="tab" onclick="go('../租赁管理/转移出库列表.html')">转移出库 <span class="close">×</span></span>
  <span class="tab active">转移出库单详情 <span class="close">×</span></span>
</div>''')
    s = swap(s, '<h3 class="card-title" id="dtTitle">采购退货单详情</h3>', '<h3 class="card-title" id="dtTitle">转移出库单详情</h3>')
    s = swap(s, '''<div class="head-btns"><button class="btn btn-default btn-sm" onclick="go('../采购管理/采购退货单列表.html')">返回列表</button></div>''',
             '''<div class="head-btns"><button class="btn btn-default btn-sm" onclick="go('../租赁管理/转移出库列表.html')">返回列表</button></div>''')
    s = retie_selected(s)
    s = open_group(s)
    s = menu_v6(s, selected=True)
    # 渲染脚本参数（ENT/DEF/title）
    s = re.sub(r"var ENT = 'purchaseReturns', DEF = 'CGTH-20260914-001';",
               "var ENT = 'transferOutbounds', DEF = 'ZY-20260914-001';", s, count=1)
    assert "ENT = 'transferOutbounds'" in s
    s = re.sub(r"var rec = D\[k\] \|\| \{\};\s*\n\s*var t = document\.getElementById\(\"dtTitle\"\);\s*\n\s*if \(t\) t\.textContent = \(rec\.title \|\| '采购退货单详情'\)",
               "var rec = D[k] || {};\n  var t = document.getElementById(\"dtTitle\");\n  if (t) t.textContent = (rec.title || '转移出库单详情')", s, count=1)
    assert "rec.title || '转移出库单详情'" in s
    # pin 替换
    i = s.index('<div class="proto-pin" id="proto-pin-1">')
    j = s.index('<style id="f01-fab-style">', i)
    s = s[:i] + PIN_LIST + '\n' + s[j:]
    wr(os.path.join('租赁管理', '转移出库单详情.html'), s)
    print('OK 转移出库单详情.html', len(s))

build_list()
build_form()
build_detail()
print('ALL DONE')
