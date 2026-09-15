# -*- coding: utf-8 -*-
"""G33 T1/T2: 三新列表页 + 8 弹窗模板（骨架改造·不新造样式）
- 采购管理/采购退货单列表.html <- 采购管理/采购入库列表.html
- 销售管理/销售退货单列表.html <- 销售管理/销售出库列表.html
- 财务协同/退款登记.html       <- 财务协同/付款登记.html
- 弹窗模板 ×8（采购3/销售3/财务2），底盘=采购管理/弹窗/采购入库审核.html 与 采购入库单详情.html
读入用 universal newline（文件全 CRLF），写回 newline='\\r\\n' 保持全 CRLF。
"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型', *a)

def rd(fp):
    with io.open(P(*fp.split('/')), encoding='utf-8') as f:  # universal newline → \n
        return f.read()

def wr(fp, s):
    with io.open(P(*fp.split('/')), 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(s)

def sub1(s, old, new, cnt=1, tag=''):
    n = s.count(old)
    assert n == cnt, 'G33 锚点[%s] 命中 %d 次(应%d): %s' % (tag, n, cnt, old[:60])
    return s.replace(old, new)

CHEV = '<svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>'

def ff_input(label, ph, extra=''):
    return '    <div class="ff%s"><span class="ff-label">%s：</span><input placeholder="%s"></div>\n' % (extra, label, ph)

def ff_select(label, opts, extra=''):
    inner = ''.join('<option>%s</option>' % o for o in opts)
    return '    <div class="ff%s"><span class="ff-label">%s：</span>\n      <select><option value="">全部</option>%s</select>\n      %s\n    </div>\n' % (extra, label, inner, CHEV)

def filter_card(ffs):
    return ('<div class="filter-card collapsed" id="filterCard">\n  <div class="filter-grid">\n' + ''.join(ffs) +
            '''    <div class="filter-actions">
      <button class="link-collapse" onclick="var f=document.getElementById('filterCard');f.classList.toggle('collapsed');this.querySelector('span').textContent=f.classList.contains('collapsed')?'展开':'收起'"><span>展开</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
      <button class="btn btn-default">重置</button>
      <button class="btn btn-primary">查询</button>
    </div>
  </div>
</div>

''')

def thead(cols):
    return ('<thead>\n        <tr>\n          <th></th>\n' +
            ''.join('          <th%s>%s</th>\n' % (' class="sticky-op"' if c == '操作' else '', c) for c in cols) +
            '        </tr>\n      </thead>')

def row(key, cells, ops):
    h = ('        <tr>\n          <td><input type="checkbox" class="cb"></td>\n'
         '          <td><span class="lk">%s</span></td>\n' % key)
    for c in cells:
        h += '          <td>%s</td>\n' % c
    h += '          <td class="sticky-op"><span class="ops">%s</span></td>\n        </tr>\n' % ops
    return h

def op_a(act, t): return '<a onclick="%s">%s</a>' % (act, t)

SUP = ['宁波华塑包装制品有限公司', '苏州联恒五金制品有限公司', '常州正大塑料托盘厂', '路凯包装运营（上海）有限公司']
CUST = ['一汽解放汽车有限公司', '上汽大众汽车有限公司宁波分公司', '小鹏汽车科技有限公司', '东风本田汽车有限公司']
RET_STAT = ['待审核', '已审核', '已退款']

# =====================================================================
# 1) 采购退货单列表.html
# =====================================================================
s = rd('采购管理/采购入库列表.html')
s = sub1(s, '<title>采购入库 - 包装租赁管理后台</title>', '<title>采购退货 - 包装租赁管理后台</title>', tag='title')
s = sub1(s, '<span class="tab active">采购入库 <span class="close">×</span></span>', '<span class="tab active">采购退货 <span class="close">×</span></span>', tag='tab')
s = sub1(s, '<li><div class="sm-link selected">采购入库</div></li>', '<li><div class="sm-link" onclick="go(\'../采购管理/采购入库列表.html\')">采购入库</div></li>', tag='sel-in')
s = sub1(s, '<li><div class="sm-link" onclick="go(\'../采购管理/采购退货单列表.html\')">采购退货</div></li>', '<li><div class="sm-link selected">采购退货</div></li>', tag='sel-new')
# 筛选卡整体替换
i0 = s.index('<div class="filter-card collapsed" id="filterCard">')
i1 = s.index('<div class="card">', i0)
NEWF = filter_card([
    ff_input('退货单号', '请输入退货单号'),
    ff_select('供应商', SUP),
    ff_select('退货类型', ['收货拒收', '入库后退货']),
    ff_input('关联原单号', '请输入采购入库单号', ' ff-row-extra'),
    ff_select('退货状态', RET_STAT, ' ff-row-extra'),
    '    <div class="ff ff-row-extra"><span class="ff-label">退货日期：</span><input placeholder="开始日期"><span class="ff-sep">→</span><input placeholder="结束日期"></div>\n',
])
s = s[:i0] + NEWF + s[i1:]
# 卡片头
s = re.sub(r'<h3 class="card-title"[^>]*>[^<]*</h3>', '<h3 class="card-title">采购退货单</h3>', s, count=1)
s = re.sub(r'<div class="head-btns">.*?</div>', '<div class="head-btns"><button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新建退货单</button></div>', s, count=1, flags=re.S)
# stabs
s = re.sub(r'<div class="stabs">.*?</div>', '''<div class="stabs">
  <span class="stab active">全部<span class="stab-count">3</span></span>
  <span class="stab">待审核<span class="stab-count">1</span></span>
  <span class="stab">已审核<span class="stab-count">1</span></span>
  <span class="stab">已退款<span class="stab-count">1</span></span>
</div>''', s, count=1, flags=re.S)
# 表头+静态行
s = re.sub(r'<thead>.*?</thead>', thead(['退货单号', '退货类型', '关联原单号', '供应商', '物料', '数量', '金额(元)', '状态', '退货日期', '操作']), s, count=1, flags=re.S)
TB = '<tbody>\n' + \
     row('CGTH-20260914-001', ['入库后退货', '<span class="lk">CGRK-20260828-012</span>', '苏州联恒五金制品有限公司', '围板箱 1200×1000×970', '<span class="td-num">10 只</span>', '<span class="td-num">4,800.00</span>', '<span class="tag tag-green">已退款</span>', '2026-09-14'], op_a("openModal('detailModal')", '详情') + op_a("go('../财务协同/退款登记.html')", '退款登记')) + \
     row('CGTH-20260912-002', ['收货拒收', '<span class="lk">CGRK-20260828-011</span>', '宁波华塑包装制品有限公司', '锁扣组件', '<span class="td-num">500 套</span>', '<span class="td-num">2,000.00</span>', '<span class="tag tag-blue">已审核</span>', '2026-09-12'], op_a("openModal('detailModal')", '详情') + op_a("go('../财务协同/退款登记.html')", '退款登记')) + \
     row('CGTH-20260910-003', ['入库后退货', '<span class="lk">CGRK-20260827-010</span>', '常州正大塑料托盘厂', '塑料托盘 1200×1000×150', '<span class="td-num">40 张</span>', '<span class="td-num">2,400.00</span>', '<span class="tag tag-orange">待审核</span>', '2026-09-10'], op_a("openModal('auditModal')", '审核') + op_a("openModal('detailModal')", '详情')) + \
     '      </tbody>'
s = re.sub(r'<tbody>.*?</tbody>', lambda m: TB, s, count=1, flags=re.S)
# 审核弹窗内容替换
s = sub1(s, '<div class="dval">CGRK-20260827-009</div>', '<div class="dval">CGTH-20260910-003</div>', tag='a-no')
s = sub1(s, '<div class="dval">采购入库单</div>', '<div class="dval">采购退货单</div>', tag='a-type')
s = sub1(s, '<div class="drow"><div class="dlabel">到货数量</div><div class="dval">12 托（零部件）</div></div>', '<div class="drow"><div class="dlabel">退货类型</div><div class="dval">入库后退货（已入库再退）</div></div>\n        <div class="drow"><div class="dlabel">退货数量</div><div class="dval">40 张（塑料托盘）</div></div>', tag='a-qty')
s = sub1(s, '<div class="dval">李国栋 / 2026-08-27 09:20</div>', '<div class="dval">李国栋 / 2026-09-10 11:05</div>', tag='a-sub')
s = sub1(s, '<div class="dval">物流主管 · 李国栋</div>', '<div class="dval">采购主管 · 徐蔚</div>', tag='a-aud')
s = sub1(s, '验收通过后库存入账，并可生成应付账单', '审核通过后按退货类型处理库存（收货拒收不动库存流水），并可登记应付退款；不修改原入库单（D-109）', tag='a-rmk')
s = sub1(s, '<h3 class="modal-title" id="detailTitle">采购入库单详情</h3>', '<h3 class="modal-title" id="detailTitle">采购退货单详情</h3>', tag='dt')
# 插入 createModal（auditModal 之前）
CREATE_CGTH = '''<!-- G33 新建采购退货单（模板：采购管理/弹窗/新建采购退货单.html） -->
<div class="modal-overlay" id="createModal">
  <div class="modal modal-lg" style="width:780px;">
    <div class="modal-header">
      <h3 class="modal-title">新建采购退货单</h3>
      <span class="modal-close" onclick="closeModal('createModal')">×</span>
    </div>
    <div class="modal-body">
      <div class="form-row">
        <span class="form-label"><span class="req">*</span>退货类型</span>
        <div><span class="radio checked"><span class="dot"></span>收货拒收（未入库直接退）</span><span class="radio"><span class="dot"></span>入库后退货（已入库再退）</span></div>
      </div>
      <div class="form-row">
        <span class="form-label"><span class="req">*</span>供应商</span>
        <div class="input-box select-box" style="width:350px;"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option>苏州联恒五金制品有限公司</option><option>宁波华塑包装制品有限公司</option><option>常州正大塑料托盘厂</option><option>路凯包装运营（上海）有限公司</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      </div>
      <div class="form-row">
        <span class="form-label"><span class="req">*</span>关联原单</span>
        <div class="input-box select-box" style="width:350px;"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>CGRK-20260828-012（苏州联恒 · 可退 10 只）</option><option>CGRK-20260828-011（宁波华塑 · 可退 500 套）</option><option>CGRK-20260827-010（常州正大 · 可退 40 张）</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
        <div class="form-tip" style="margin-left:12px;">选择原单后带出物料行与可退上限</div>
      </div>
      <div class="form-row">
        <span class="form-label"><span class="req">*</span>退货日期</span>
        <div class="input-box" style="width:350px;"><input value="2026-09-15" placeholder="请输入"></div>
      </div>
      <div class="form-row">
        <span class="form-label">退货原因</span>
        <div class="input-box" style="width:350px;"><input placeholder="选填"></div>
      </div>
      <div class="form-row">
        <span class="form-label">备注</span>
        <div class="input-box" style="width:350px;"><input placeholder="选填"></div>
      </div>
      <div style="margin:12px 0 8px;font-size:13px;font-weight:600;">退货明细（可退上限内填写）</div>
      <div class="table-wrap">
        <table class="edit-tbl">
          <thead><tr><th>物料</th><th>可退上限</th><th>退货数量</th><th>单价(元)</th><th>金额(元)</th></tr></thead>
          <tbody id="retItems">
            <tr><td class="auto-cell">围板箱 1200×1000×970</td><td class="auto-cell">10 只</td><td><input value="10"></td><td><input value="480.00"></td><td class="auto-cell">4,800.00</td></tr>
          </tbody>
        </table>
      </div>
      <div style="margin-top:8px;"><button class="btn btn-dashed btn-sm" onclick="addRetRow()">+ 添加一行</button></div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-default" onclick="closeModal('createModal')">取消</button>
      <button class="btn btn-default" onclick="closeModal('createModal')">保存草稿</button>
      <button class="btn" onclick="closeModal('createModal')">提交审核</button>
    </div>
  </div>
</div>
<script>
/* G33 退货明细行新增（DOM 追加行） */
function addRetRow() {
  var tb = document.getElementById('retItems');
  if (!tb) return;
  var tr = document.createElement('tr');
  tr.innerHTML = '<td><input placeholder="选择物料"></td><td class="auto-cell">—</td><td><input value="1"></td><td><input value="0.00"></td><td class="auto-cell">0.00</td>';
  tb.appendChild(tr);
}
</script>

'''
s = sub1(s, '<div class="modal-overlay" id="auditModal">', CREATE_CGTH + '<div class="modal-overlay" id="auditModal">', tag='ins-create')
# renderListPage cfg
s = re.sub(r"renderListPage\(\{.*?\}\);", """renderListPage({
  entity: 'purchaseReturns',
  stabs: true,
  filters: [
    { label: '退货单号', field: '_key', match: 'contains' },
    { label: '供应商', field: 'supplier' },
    { label: '退货类型', field: 'type' },
    { label: '关联原单号', field: 'ref' },
    { label: '退货状态', field: 'status' },
    { label: '退货日期', field: 'date', range: true }
  ]
});""", s, count=1, flags=re.S)
wr('采购管理/采购退货单列表.html', s)
print('OK 采购管理/采购退货单列表.html', len(s), 'chars')

# =====================================================================
# 2) 销售退货单列表.html
# =====================================================================
s = rd('销售管理/销售出库列表.html')
s = sub1(s, '<title>销售出库 - 包装租赁管理后台</title>', '<title>销售退货 - 包装租赁管理后台</title>', tag='title')
s = sub1(s, '<span class="tab active">销售出库 <span class="close">×</span></span>', '<span class="tab active">销售退货 <span class="close">×</span></span>', tag='tab')
s = sub1(s, '<li><div class="sm-link selected">销售出库</div></li>', '<li><div class="sm-link" onclick="go(\'../销售管理/销售出库列表.html\')">销售出库</div></li>', tag='sel-in')
s = sub1(s, '<li><div class="sm-link" onclick="go(\'../销售管理/销售退货单列表.html\')">销售退货</div></li>', '<li><div class="sm-link selected">销售退货</div></li>', tag='sel-new')
i0 = s.index('<div class="filter-card collapsed" id="filterCard">')
i1 = s.index('<div class="card">', i0)
NEWF = filter_card([
    ff_input('退货单号', '请输入退货单号'),
    ff_select('客户名称', CUST),
    ff_select('退货类型', ['收货拒收', '入库后退货']),
    ff_input('关联出库单号', '请输入销售出库单号', ' ff-row-extra'),
    ff_select('退货状态', RET_STAT, ' ff-row-extra'),
    '    <div class="ff ff-row-extra"><span class="ff-label">退货日期：</span><input placeholder="开始日期"><span class="ff-sep">→</span><input placeholder="结束日期"></div>\n',
])
s = s[:i0] + NEWF + s[i1:]
s = re.sub(r'<h3 class="card-title"[^>]*>[^<]*</h3>', '<h3 class="card-title">销售退货单</h3>', s, count=1)
s = re.sub(r'<div class="head-btns">.*?</div>', '<div class="head-btns"><button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新建退货单</button></div>', s, count=1, flags=re.S)
s = re.sub(r'<div class="stabs">.*?</div>', '''<div class="stabs">
  <span class="stab active">全部<span class="stab-count">3</span></span>
  <span class="stab">待审核<span class="stab-count">1</span></span>
  <span class="stab">已审核<span class="stab-count">1</span></span>
  <span class="stab">已退款<span class="stab-count">1</span></span>
</div>''', s, count=1, flags=re.S)
s = re.sub(r'<thead>.*?</thead>', thead(['退货单号', '退货类型', '关联出库单号', '客户', '物料', '数量', '金额(元)', '状态', '退货日期', '操作']), s, count=1, flags=re.S)
# demo 已反查键（与 T4 同口径：fields.so → 实体键）
_dd = rd('_data/demo-data.js')
_seg = _dd[_dd.index('salesOutbounds: {'):_dd.index('otherInbounds: {')]
_xk = re.findall(r"'(XSCK-[0-9-]+)':", _seg)
_so2 = {}
for _i, _k in enumerate(_xk):
    _st = _seg.index("'" + _k + "':")
    _en = _seg.index("'" + _xk[_i + 1] + "':", _st) if _i + 1 < len(_xk) else len(_seg)
    _m = re.search(r'"so": "([^"]+)"', _seg[_st:_en])
    if _m: _so2[_m.group(1)] = _k
K1 = _so2['SO-20260830-0043']; K2 = _so2['SO-20260828-0041']; K3 = _so2['SO-20260822-0038']
TB = '<tbody>\n' + \
     row('XSTH-20260913-001', ['收货拒收', '<span class="lk">%s</span>' % K1, '一汽解放汽车有限公司', '箱盖 ABS 吸塑', '<span class="td-num">200 件</span>', '<span class="td-num">3,600.00</span>', '<span class="tag tag-green">已退款</span>', '2026-09-13'], op_a("openModal('detailModal')", '详情') + op_a("go('../财务协同/退款登记.html')", '退款登记')) + \
     row('XSTH-20260912-002', ['入库后退货', '<span class="lk">%s</span>' % K2, '东风本田汽车有限公司', '锁扣组件', '<span class="td-num">100 套</span>', '<span class="td-num">800.00</span>', '<span class="tag tag-blue">已审核</span>', '2026-09-12'], op_a("openModal('detailModal')", '详情') + op_a("go('../财务协同/退款登记.html')", '退款登记')) + \
     row('XSTH-20260911-003', ['收货拒收', '<span class="lk">%s</span>' % K3, '上汽大众汽车有限公司宁波分公司', '内衬', '<span class="td-num">300 件</span>', '<span class="td-num">1,500.00</span>', '<span class="tag tag-orange">待审核</span>', '2026-09-11'], op_a("openModal('auditModal')", '审核') + op_a("openModal('detailModal')", '详情')) + \
     '      </tbody>'
s = re.sub(r'<tbody>.*?</tbody>', lambda m: TB, s, count=1, flags=re.S)
# createModal 整块替换（含原出库表单）→ 新建销售退货单
j0 = s.index('<div class="modal-overlay" id="createModal">')
j1 = s.index('<div class="modal-overlay" id="auditModal">')
CREATE_XSTH = CREATE_CGTH \
    .replace('新建采购退货单', '新建销售退货单') \
    .replace('<option>苏州联恒五金制品有限公司</option><option>宁波华塑包装制品有限公司</option><option>常州正大塑料托盘厂</option><option>路凯包装运营（上海）有限公司</option>', '<option>一汽解放汽车有限公司</option><option>上汽大众汽车有限公司宁波分公司</option><option>小鹏汽车科技有限公司</option><option>东风本田汽车有限公司</option>') \
    .replace('<span class="form-label"><span class="req">*</span>供应商</span>', '<span class="form-label"><span class="req">*</span>客户</span>') \
    .replace('<option selected>CGRK-20260828-012（苏州联恒 · 可退 10 只）</option><option>CGRK-20260828-011（宁波华塑 · 可退 500 套）</option><option>CGRK-20260827-010（常州正大 · 可退 40 张）</option>', '<option selected>%s（一汽解放 · 可退 200 件）</option><option>%s（东风本田 · 可退 100 套）</option><option>%s（上汽大众宁波 · 可退 300 件）</option>' % (K1, K2, K3)) \
    .replace('关联原单后带出物料行与可退上限', '选择销售出库单后带出物料行与可退上限') \
    .replace('<td class="auto-cell">围板箱 1200×1000×970</td><td class="auto-cell">10 只</td><td><input value="10"></td><td><input value="480.00"></td><td class="auto-cell">4,800.00</td>', '<td class="auto-cell">箱盖 ABS 吸塑</td><td class="auto-cell">200 件</td><td><input value="200"></td><td><input value="18.00"></td><td class="auto-cell">3,600.00</td>') \
    .replace('<!-- G33 新建采购退货单（模板：采购管理/弹窗/新建采购退货单.html） -->', '<!-- G33 新建销售退货单（模板：销售管理/弹窗/新建销售退货单.html） -->')
s = s[:j0] + CREATE_XSTH + s[j1:]
# 审核弹窗内容
s = sub1(s, '<div class="dval">XSCK-20260902-015</div>', '<div class="dval">XSTH-20260911-003</div>', tag='a-no')
s = sub1(s, '<div class="dval">销售出库单</div>', '<div class="dval">销售退货单</div>', tag='a-type')
s = sub1(s, '<div class="drow"><div class="dlabel">出库数量</div><div class="dval">1,500 件</div></div>', '<div class="drow"><div class="dlabel">退货类型</div><div class="dval">收货拒收（客户未收货直接退回）</div></div>\n        <div class="drow"><div class="dlabel">退货数量</div><div class="dval">300 件（内衬）</div></div>', tag='a-qty')
s = sub1(s, '<div class="dval">张伟 / 2026-09-02 14:10</div>', '<div class="dval">王琳 / 2026-09-11 14:30</div>', tag='a-sub')
s = sub1(s, '<div class="dval">物流主管 · 李国栋</div>', '<div class="dval">销售主管 · 王琳</div>', tag='a-aud')
s = re.sub(r'<h3 class="modal-title" id="detailTitle">[^<]*</h3>', '<h3 class="modal-title" id="detailTitle">销售退货单详情</h3>', s, count=1)
s = re.sub(r"renderListPage\(\{.*?\}\);", """renderListPage({
  entity: 'salesReturns',
  stabs: true,
  filters: [
    { label: '退货单号', field: '_key', match: 'contains' },
    { label: '客户名称', field: 'customer' },
    { label: '退货类型', field: 'type' },
    { label: '关联出库单号', field: 'ref' },
    { label: '退货状态', field: 'status' },
    { label: '退货日期', field: 'date', range: true }
  ]
});""", s, count=1, flags=re.S)
wr('销售管理/销售退货单列表.html', s)
print('OK 销售管理/销售退货单列表.html', len(s), 'chars')

# =====================================================================
# 3) 退款登记.html
# =====================================================================
s = rd('财务协同/付款登记.html')
s = sub1(s, '<title>付款登记 - 包装租赁管理后台</title>', '<title>退款登记 - 包装租赁管理后台</title>', tag='title')
s = sub1(s, '<span class="tab active">付款登记 <span class="close">×</span></span>', '<span class="tab active">退款登记 <span class="close">×</span></span>', tag='tab')
s = sub1(s, '<li><div class="sm-link selected">付款登记</div></li>', '<li><div class="sm-link" onclick="go(\'../财务协同/付款登记.html\')">付款登记</div></li>', tag='sel-in')
s = sub1(s, '<li><div class="sm-link" onclick="go(\'../财务协同/退款登记.html\')">退款登记</div></li>', '<li><div class="sm-link selected">退款登记</div></li>', tag='sel-new')
i0 = s.index('<div class="filter-card collapsed" id="filterCard">')
i1 = s.index('<div class="card">', i0)
NEWF = filter_card([
    ff_input('退款编号', '请输入退款编号'),
    ff_select('退款类型', ['应付退款', '应收退款']),
    ff_input('关联退货单号', '请输入退货单号'),
    ff_input('往来单位', '请输入供应商或客户名称', ' ff-row-extra'),
    ff_select('状态', ['待审核', '已确认'], ' ff-row-extra'),
    '    <div class="ff ff-row-extra"><span class="ff-label">退款日期：</span><input placeholder="开始日期"><span class="ff-sep">→</span><input placeholder="结束日期"></div>\n',
])
s = s[:i0] + NEWF + s[i1:]
s = re.sub(r'<h3 class="card-title"[^>]*>[^<]*</h3>', '<h3 class="card-title">退款登记</h3>', s, count=1)
s = re.sub(r'<div class="head-btns">.*?</div>', '<div class="head-btns"><button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="openModal(\'createModal\')">新建退款单</button></div>', s, count=1, flags=re.S)
s = re.sub(r'<div class="stabs">.*?</div>', '''<div class="stabs">
  <span class="stab active">全部<span class="stab-count">3</span></span>
  <span class="stab">待审核<span class="stab-count">1</span></span>
  <span class="stab">已确认<span class="stab-count">2</span></span>
</div>''', s, count=1, flags=re.S)
s = re.sub(r'<thead>.*?</thead>', thead(['退款编号', '退款类型', '关联退货单号', '往来单位', '退款金额(元)', '资金方向', '状态', '退款日期', '操作']), s, count=1, flags=re.S)
TB = '<tbody>\n' + \
     row('TKD-20260914-001', ['应付退款（对供应商）', '<span class="lk">CGTH-20260912-002</span>', '宁波华塑包装制品有限公司', '<span class="td-num">2,000.00</span>', '收款（供应商退回）', '<span class="tag tag-orange">待审核</span>', '2026-09-14'], op_a("openModal('auditModal')", '确认') + op_a("openModal('detailModal')", '详情')) + \
     row('TKD-20260913-002', ['应收退款（对客户）', '<span class="lk">XSTH-20260913-001</span>', '一汽解放汽车有限公司', '<span class="td-num">3,600.00</span>', '付款（退回客户）', '<span class="tag tag-green">已确认</span>', '2026-09-13'], op_a("openModal('detailModal')", '详情')) + \
     row('TKD-20260912-003', ['应付退款（对供应商）', '<span class="lk">CGTH-20260914-001</span>', '苏州联恒五金制品有限公司', '<span class="td-num">4,800.00</span>', '收款（供应商退回）', '<span class="tag tag-green">已确认</span>', '2026-09-12'], op_a("openModal('detailModal')", '详情')) + \
     '      </tbody>'
s = re.sub(r'<tbody>.*?</tbody>', lambda m: TB, s, count=1, flags=re.S)
# createModal（含分期计划脚本）整块替换 → 新建退款登记（无分期）
j0 = s.index('<div class="modal-overlay" id="createModal">')
j1 = s.index('<div class="modal-overlay" id="auditModal">')
CREATE_TKD = '''<!-- G33 新建退款登记（模板：财务协同/弹窗/退款登记新建.html）·一页双向 -->
<div class="modal-overlay" id="createModal">
  <div class="modal">
    <div class="modal-header">
      <h3 class="modal-title">新建退款登记</h3>
      <span class="modal-close" onclick="closeModal('createModal')">×</span>
    </div>
    <div class="modal-body">
      <div class="form-row">
        <span class="form-label"><span class="req">*</span>退款类型</span>
        <div class="input-box select-box" style="width:350px;"><select id="refundTypeSel" style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>应付退款（对供应商）</option><option>应收退款（对客户）</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
        <div class="form-tip" style="margin-left:12px;">采购退货→应付退款；销售退货→应收退款（D-123）</div>
      </div>
      <div class="form-row">
        <span class="form-label"><span class="req">*</span>往来单位</span>
        <div class="input-box select-box" style="width:350px;"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option>宁波华塑包装制品有限公司</option><option>苏州联恒五金制品有限公司</option><option>常州正大塑料托盘厂</option><option>一汽解放汽车有限公司</option><option>上汽大众汽车有限公司宁波分公司</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      </div>
      <div class="form-row">
        <span class="form-label"><span class="req">*</span>关联退货单</span>
        <div class="input-box select-box" style="width:350px;"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>CGTH-20260912-002（宁波华塑 · 已审核 2,000.00）</option><option>XSTH-20260912-002（东风本田 · 已审核 800.00）</option><option>CGTH-20260910-003（常州正大 · 待审核）</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      </div>
      <div class="form-row">
        <span class="form-label"><span class="req">*</span>退款金额(元)</span>
        <div class="input-box" style="width:350px;"><input value="2,000.00" placeholder="请输入"></div>
      </div>
      <div class="form-row">
        <span class="form-label">资金方向</span>
        <div class="input-box" style="width:350px;"><input class="auto" value="收款（供应商退回）" readonly></div>
        <div class="form-tip" style="margin-left:12px;">应付退款=收款；应收退款=付款（随类型自动带出）</div>
      </div>
      <div class="form-row">
        <span class="form-label">退款日期</span>
        <div class="input-box" style="width:350px;"><input value="2026-09-15" placeholder="请输入"></div>
      </div>
      <div class="form-row">
        <span class="form-label">收退款账户</span>
        <div class="input-box select-box" style="width:350px;"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>招商银行苏州分行 1109××××8821</option><option>中国银行常州分行 3325××××0067</option><option>工商银行宁波分行 4402××××5531</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      </div>
      <div class="form-row">
        <span class="form-label">备注</span>
        <div class="input-box" style="width:350px;"><input placeholder="选填"></div>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-default" onclick="closeModal('createModal')">取消</button>
      <button class="btn btn-default" onclick="closeModal('createModal')">保存草稿</button>
      <button class="btn" onclick="closeModal('createModal')">提交审核</button>
    </div>
  </div>
</div>

'''
s = s[:j0] + CREATE_TKD + s[j1:]
# 审核弹窗（确认付款→退款确认）
s = sub1(s, '<h3 class="modal-title">确认付款</h3>', '<h3 class="modal-title">退款确认</h3>', tag='a-title')
s = sub1(s, '<div class="dval">PAY-20260902-005</div>', '<div class="dval">TKD-20260914-001</div>', tag='a-no')
s = sub1(s, '<div class="dval">付款登记</div>', '<div class="dval">退款登记</div>', tag='a-type')
s = sub1(s, '<div class="dlabel">付款金额</div><div class="dval">6,000.00 元</div>', '<div class="dlabel">退款金额</div><div class="dval">2,000.00 元（应付退款 · 收款）</div>', tag='a-amt')
s = sub1(s, '<div class="dlabel">付款方式</div><div class="dval">银行转账</div>', '<div class="dlabel">资金方向</div><div class="dval">收款（供应商退回）</div>', tag='a-dir')
s = sub1(s, '<div class="dval">财务·周敏 / 2026-09-02 13:26</div>', '<div class="dval">财务·周敏 / 2026-09-14 10:15</div>', tag='a-sub')
s = re.sub(r'<h3 class="modal-title" id="detailTitle">[^<]*</h3>', '<h3 class="modal-title" id="detailTitle">退款登记详情</h3>', s, count=1)
s = re.sub(r"renderListPage\(\{.*?\}\);", """renderListPage({
  entity: 'refunds',
  stabs: true,
  filters: [
    { label: '退款编号', field: '_key', match: 'contains' },
    { label: '退款类型', field: 'type' },
    { label: '关联退货单号', field: 'ref' },
    { label: '往来单位', field: 'partner' },
    { label: '状态', field: 'status' },
    { label: '退款日期', field: 'date', range: true }
  ]
});""", s, count=1, flags=re.S)
wr('财务协同/退款登记.html', s)
print('OK 财务协同/退款登记.html', len(s), 'chars')

# =====================================================================
# 4) 三个新页：剥离旧 pins（data-note 属性 + proto-pin 块），保留 fab
# =====================================================================
for fp in ['采购管理/采购退货单列表.html', '销售管理/销售退货单列表.html', '财务协同/退款登记.html']:
    s = rd(fp)
    n_attr = len(re.findall(r' data-note="\d+"', s))
    s = re.sub(r' data-note="\d+"', '', s)
    s2, n_pin = re.subn(r'(<div id="proto-pins">)<div class="proto-pin".*?(<style id="f01-fab-style">)', r'\1\2', s, count=1, flags=re.S)
    assert n_pin == 1, 'G33 pin 剥离失败: ' + fp
    wr(fp, s2)
    print('pins stripped:', fp, '(attrs %d, block 1)' % n_attr)

# =====================================================================
# 5) 弹窗模板 ×8
# =====================================================================
def tpl_from_audit(out_fp, title, modal_html, inject_mark):
    t = rd('采购管理/弹窗/采购入库审核.html')
    t = sub1(t, '<title>采购入库审核 - 包装租赁管理后台</title>', '<title>%s - 包装租赁管理后台</title>' % title, tag='t-title')
    t = sub1(t, '<!-- 弹窗模板：审核确认（auditModal） -->', '<!-- 弹窗模板：%s -->' % title, tag='t-c1')
    t = sub1(t, '<!-- 注入标记：采购管理/采购入库列表.html -->', '<!-- 注入标记：%s -->' % inject_mark, tag='t-c2')
    a = t.index('<div class="modal-overlay" id="auditModal">')
    b = t.index('<script>', a)
    t = t[:a] + modal_html.rstrip('\n') + '\n' + t[b:]
    wr(out_fp, t)
    print('OK', out_fp)

def tpl_from_detail(out_fp, title, entity, key, inject_mark):
    t = rd('采购管理/弹窗/采购入库单详情.html')
    t = sub1(t, '<title>采购入库单详情 - 包装租赁管理后台</title>', '<title>%s - 包装租赁管理后台</title>' % title, tag='d-title')
    t = re.sub(r'<!-- 弹窗模板：[^>]*-->', '<!-- 弹窗模板：%s -->' % title, t, count=1)
    t = sub1(t, '<!-- 注入标记：采购管理/采购入库列表.html -->', '<!-- 注入标记：%s -->' % inject_mark, tag='d-c2')
    t = re.sub(r'<h3 class="modal-title" id="detailTitle">[^<]*</h3>', '<h3 class="modal-title" id="detailTitle">%s</h3>' % title, t, count=1)
    t = sub1(t, "openGenericDetail('purchaseInbounds', 'CGRK-20260828-012', '../../');", "openGenericDetail('%s', '%s', '../../');" % (entity, key), tag='d-ogd')
    wr(out_fp, t)
    print('OK', out_fp)

# 审核/新建模板 modal 体（从新列表页内嵌弹窗原样取，保证双层一致）
cg = rd('采购管理/采购退货单列表.html')
xs = rd('销售管理/销售退货单列表.html')
tk = rd('财务协同/退款登记.html')

def extract_modal(page, mid):
    a = page.index('<div class="modal-overlay" id="%s">' % mid)
    # 找 overlay 收尾：下一个顶层标记（</div> 后跟 <script/<style/<!--/下一个 overlay）
    m = re.search(r'</div>\s*</div>\s*\n(?=\s*(?:<script|<style|<!--|<div class="modal-overlay"))', page[a:])
    end = a + m.end() - 1
    return page[a:end]

m_cg_create = extract_modal(cg, 'createModal')
m_cg_audit = extract_modal(cg, 'auditModal')
m_xs_create = extract_modal(xs, 'createModal')
m_xs_audit = extract_modal(xs, 'auditModal')
m_tk_create = extract_modal(tk, 'createModal')
m_tk_audit = extract_modal(tk, 'auditModal')

ADD_ROW_JS = '''
<script>
/* G33 退货明细行新增（DOM 追加行） */
function addRetRow() {
  var tb = document.getElementById('retItems');
  if (!tb) return;
  var tr = document.createElement('tr');
  tr.innerHTML = '<td><input placeholder="选择物料"></td><td class="auto-cell">—</td><td><input value="1"></td><td><input value="0.00"></td><td class="auto-cell">0.00</td>';
  tb.appendChild(tr);
}
</script>
'''

tpl_from_audit('采购管理/弹窗/采购退货审核.html', '采购退货审核', m_cg_audit, '采购管理/采购退货单列表.html')
tpl_from_detail('采购管理/弹窗/采购退货单详情.html', '采购退货单详情', 'purchaseReturns', 'CGTH-20260914-001', '采购管理/采购退货单列表.html')
tpl_from_audit('采购管理/弹窗/新建采购退货单.html', '新建采购退货单', m_cg_create + ADD_ROW_JS, '采购管理/采购退货单列表.html')
tpl_from_audit('销售管理/弹窗/销售退货审核.html', '销售退货审核', m_xs_audit, '销售管理/销售退货单列表.html')
tpl_from_detail('销售管理/弹窗/销售退货单详情.html', '销售退货单详情', 'salesReturns', 'XSTH-20260913-001', '销售管理/销售退货单列表.html')
tpl_from_audit('销售管理/弹窗/新建销售退货单.html', '新建销售退货单', m_xs_create + ADD_ROW_JS, '销售管理/销售退货单列表.html')
tpl_from_audit('财务协同/弹窗/退款登记新建.html', '退款登记新建', m_tk_create, '财务协同/退款登记.html')
tpl_from_detail('财务协同/弹窗/退款登记详情.html', '退款登记详情', 'refunds', 'TKD-20260914-001', '财务协同/退款登记.html')

print('=== G33 T1/T2 全部产出完成 ===')
