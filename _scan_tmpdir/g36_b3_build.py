# -*- coding: utf-8 -*-
"""G36 B3：租赁 9＋租入 8 → 17 页面（含两个有字段确认类＋3 个带标注模板 pin 迁移）"""
import sys, io, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g36_factory import dpage, apage, fpage, cut_overlay, cut_script_containing, rd, wr, rew_detail_audit, rew_act, rew_regex, rew_todo_links, assemble, ROOT

L = '租赁管理'; R = '租入管理'
H_ZL = '../租赁管理/租赁单列表.html'; H_CK = '../租赁管理/租赁出库列表.html'; H_TZ = '../租赁管理/退租入库列表.html'
H_RZD = '../租入管理/租入单列表.html'; H_RZ = '../租入管理/租入入库列表.html'; H_GH = '../租入管理/租入归还列表.html'
H_KC = '../仓储作业/库存查询.html'

built = []
# ---- 租赁 9 ----
built.append(dpage('租赁管理/租赁单详情.html', 'leaseOrders', 'ZL-20260823-033', H_ZL, '租赁单', '租赁单详情', '租赁单详情', L, '租赁单', H_ZL))
built.append(apage('租赁管理/租赁单审核.html', 'leaseOrders', 'ZL-20260823-033', H_ZL, '租赁单', '租赁单审核', '租赁单审核', L, '租赁单', H_ZL))
built.append(fpage('租赁管理/租赁单新建.html', '租赁管理/弹窗/租赁单新建.html', H_ZL, '租赁单', '新建租赁单', '新建租赁单', L, '租赁单', H_ZL, card_title='租赁信息'))
built.append(dpage('租赁管理/租赁出库详情.html', 'comboOutbounds', 'CK-20260910-022', H_CK, '租赁出库', '租赁出库详情', '租赁出库单详情', L, '租赁出库', H_CK))
built.append(apage('租赁管理/租赁出库确认.html', 'comboOutbounds', 'CK-20260910-022', H_CK, '租赁出库', '租赁出库确认', '租赁出库确认', L, '租赁出库', H_CK, hint='确认后按明细扣减库存、生成客户在租并起租；驳回退回录单修改。'))
built.append(dpage('租赁管理/退租入库详情.html', 'returnInbounds', 'TZRK-20260902-010', H_TZ, '退租入库', '退租入库详情', '退租入库单详情', L, '退租入库', H_TZ))
built.append(apage('租赁管理/退租入库审核.html', 'returnInbounds', 'TZRK-20260902-010', H_TZ, '退租入库', '退租入库审核', '退租入库审核', L, '退租入库', H_TZ, hint='验收通过后资产回库并终止租期计费；驳回退回待验收。'))
built.append(fpage('租赁管理/退租入库新建.html', '租赁管理/弹窗/退租入库新建.html', H_TZ, '退租入库', '新建退租入库单', '新建退租入库单', L, '退租入库', H_TZ, card_title='退租入库信息'))
# 器具出租履历（特殊：assetTracks 按物料码 ?key=，回退 rentTracks ?id=）
content = ('<div class="card">\n  <div class="card-head">\n'
           '    <h3 class="card-title" id="dtTitle">器具出租履历</h3>\n'
           '    <div class="head-btns"><button class="btn btn-default btn-sm" onclick="go(\'%s\')">返回列表</button></div>\n'
           '  </div>\n  <div id="detailBody"><!-- 资产轨迹/出租履历（detail-generic 按物料或单号渲染） --></div>\n</div>\n' % H_KC)
scripts = ('<script src="../_data/detail-generic.js"></script>\n<script>\n'
           '(function () {\n'
           '  var k = null, rec = null, ent = null;\n'
           '  try { k = new URLSearchParams(location.search).get("key") || new URLSearchParams(location.search).get("id"); } catch (e) {}\n'
           '  var A = (window.DEMO_DATA || {}).assetTracks || {};\n'
           '  var T = (window.DEMO_DATA || {}).rentTracks || {};\n'
           '  if (A[k]) { rec = A[k]; ent = "assetTracks"; }\n'
           '  else if (T[k]) { rec = T[k]; ent = "rentTracks"; }\n'
           '  else { k = Object.keys(A)[0] || Object.keys(T)[0]; rec = A[k] || T[k] || {}; ent = A[k] ? "assetTracks" : "rentTracks"; }\n'
           '  var t = document.getElementById("dtTitle");\n'
           '  if (t) t.textContent = (rec.title || "器具出租履历") + " · " + (rec.titleNo || k);\n'
           '  var el = document.getElementById("detailBody");\n'
           '  if (el && window.renderGenericDetailHTML) el.innerHTML = window.renderGenericDetailHTML(rec, "../");\n'
           '})();\n</script>')
built.append(assemble('租赁管理/器具出租履历.html', '器具出租履历', '库存查询', '器具出租履历', L, '租赁单', H_ZL, content, scripts, '', detail=True))
# ---- 租入 8 ----
built.append(dpage('租入管理/租入单详情.html', 'rentInOrders', 'RZD-20260815-003', H_RZD, '租入单', '租入单详情', '租入单详情', R, '租入单', H_RZD))
built.append(apage('租入管理/租入单审核.html', 'rentInOrders', 'RZD-20260815-003', H_RZD, '租入单', '租入单审核', '租入单审核', R, '租入单', H_RZD))
built.append(fpage('租入管理/租入单新建.html', '租入管理/弹窗/租入单新建.html', H_RZD, '租入单', '新建租入单', '新建租入单', R, '租入单', H_RZD, card_title='租入信息'))
built.append(dpage('租入管理/租入入库详情.html', 'rentInbounds', 'RZRK-20260816-021', H_RZ, '租入入库', '租入入库详情', '租入入库单详情', R, '租入入库', H_RZ))
# 租入入库确认（有字段：立即转租勾选）→ apage 后插勾选行
built.append(apage('租入管理/租入入库确认.html', 'rentInbounds', 'RZRK-20260816-021', H_RZ, '租入入库', '租入入库确认', '租入入库确认', R, '租入入库', H_RZ, hint='确认后计入租入在库并按月生成租金应付；勾选立即转租则同时生成租赁出库单（供应商直发）。'))
CHK_ROW = ('  <div class="form-row" style="align-items:flex-start;">\n    <div class="form-label" style="padding-top:4px;">立即转租：</div>\n    <div>\n'
           '      <label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" class="cb" checked><span>供应商直发终端客户——确认同时自动生成租赁出库单（自动带物料 · 免重复填单）</span></label>\n'
           '      <div style="font-size:12px;color:#8c8c8c;margin-top:4px;">背靠背转租（D-105）：租赁出库列表可查该单；库存侧「转租登记」入口保留不变（D-78）；计费口径不受影响（D-122 梳理中）。</div>\n'
           '    </div>\n  </div>\n')
p = '租入管理/租入入库确认.html'
s = rd(p)
m4 = re.search(r'<div class="form-row">\s*<div class="form-label"><span class="req">\*</span>审核结论：</div>', s)
assert m4, 'audit conclusion row not found'
CHK_ROW_CRLF = CHK_ROW.replace('\n', '\r\n')
s = s[:m4.start()] + CHK_ROW_CRLF + s[m4.start():]
wr(p, s)
built.append(dpage('租入管理/租入归还详情.html', 'rentInReturns', 'GHCK-20260903-001', H_GH, '租入归还', '租入归还详情', '租入归还单详情', R, '租入归还', H_GH))
built.append(apage('租入管理/租入归还审核.html', 'rentInReturns', 'GHCK-20260903-001', H_GH, '租入归还', '租入归还审核', '租入归还审核', R, '租入归还', H_GH, hint='审核通过后归还出库并终止租金应付；支持分批归还（未还数量继续计租）。'))
built.append(fpage('租入管理/租入归还新建.html', '租入管理/弹窗/租入归还新建.html', H_GH, '租入归还', '新建租入归还单', '新建租入归还单', R, '租入归还', H_GH, card_title='归还信息'))
print('BUILT B3 %d pages' % len(built))

# ---- 标注 pin 迁移（3 个带 pin 模板 → 新页）----
def migrate_pins(tpl, page):
    t = io.open(os.path.join(ROOT, tpl), encoding='utf-8', newline='').read()
    a = t.index('<div id="proto-pins">')
    b = t.index('<script id="proto-notes-js">', a)
    pins = t[a:b]
    g = rd(page)
    ga = g.index('<div id="proto-pins">')
    gb = g.index('<script id="proto-notes-js">', ga)
    g = g[:ga] + pins + g[gb:]
    wr(page, g)
    print('pins 迁移: %s → %s (%d pins)' % (tpl.split('/')[-1], page.split('/')[-1], pins.count('proto-pin" id=')))

migrate_pins('租赁管理/弹窗/租赁单新建.html', '租赁管理/租赁单新建.html')
migrate_pins('租入管理/弹窗/租入单新建.html', '租入管理/租入单新建.html')
migrate_pins('租入管理/弹窗/租入归还新建.html', '租入管理/租入归还新建.html')

# ---- 宿主页接线 ----
def rewire_host(path, del_ovs, btn_map, id_map, extra_funcs=(), audit_cut=True):
    s = rd(path)
    for mid in del_ovs:
        if '<div class="modal-overlay" id="%s"' % mid in s:
            s = cut_overlay(s, mid)
    for oc, nk in btn_map.items():
        n = s.count(oc)
        s = s.replace(oc, nk)
        print('  %s: %s ×%d' % (path.split('/')[-1], oc[:40], n))
    for mid, u in id_map.items():
        s, n = re.subn(r"openModal\('%s'\)" % mid, "go('%s')" % u, s)
        if n: print('  %s: openModal(%s) ×%d' % (path.split('/')[-1], mid, n))
    for fm in extra_funcs:
        if fm in s:
            s = cut_script_containing(s, fm)
    if audit_cut and '?audit=1 自动打开审核弹窗' in s:
        i0 = s.index('?audit=1 自动打开审核弹窗')
        a0 = s.rfind('<script', 0, i0)
        j0 = s.index('</script>', i0) + 9
        if any(mid in s[a0:j0] for mid in del_ovs):
            s = s[:a0] + s[j0:]
    s = re.sub(r"\r?\n[ \t]*modalId: 'detailModal'", '', s)
    for mid in del_ovs:
        assert mid not in s, mid + ' residue in ' + path
    wr(path, s)

rewire_host('租赁管理/租赁单列表.html', ['createModal', 'auditModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../租赁管理/租赁单新建.html')\""},
    {'detailModal': '../租赁管理/租赁单详情.html', 'auditModal': '../租赁管理/租赁单审核.html'})
rewire_host('租赁管理/租赁出库列表.html', ['exitConfirmModal', 'detailModal'], {},
    {'detailModal': '../租赁管理/租赁出库详情.html', 'exitConfirmModal': '../租赁管理/租赁出库确认.html'})
rewire_host('租赁管理/退租入库列表.html', ['auditModal', 'detailModal', 'createModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../租赁管理/退租入库新建.html')\""},
    {'detailModal': '../租赁管理/退租入库详情.html', 'auditModal': '../租赁管理/退租入库审核.html'})
rewire_host('租入管理/租入单列表.html', ['createModal', 'auditModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../租入管理/租入单新建.html')\""},
    {'detailModal': '../租入管理/租入单详情.html', 'auditModal': '../租入管理/租入单审核.html'})
rewire_host('租入管理/租入入库列表.html', ['auditModal', 'detailModal'], {},
    {'detailModal': '../租入管理/租入入库详情.html', 'auditModal': '../租入管理/租入入库确认.html'})
rewire_host('租入管理/租入归还列表.html', ['createModal', 'auditModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../租入管理/租入归还新建.html')\""},
    {'detailModal': '../租入管理/租入归还详情.html', 'auditModal': '../租入管理/租入归还审核.html'})
# 库存查询：trackModal → 器具出租履历页（openTrack 改跳转；其余弹窗保留）
s = rd('仓储作业/库存查询.html')
old_ot = re.search(r'function openTrack\(key\) \{.*?\n\}', s, re.S)
assert old_ot, 'openTrack not found'
s = s.replace(old_ot.group(0), "function openTrack(key) { go('../租赁管理/器具出租履历.html?key=' + encodeURIComponent(key)); }")
assert s.count('<div class="modal-overlay" id="trackModal"') == 1
s = cut_overlay(s, 'trackModal')
assert 'trackModal' not in s
wr('仓储作业/库存查询.html', s)
print('  库存查询: openTrack → go 器具出租履历；trackModal 删除 ✓')

# ---- demo-data ops ----
s = rd('_data/demo-data.js')
s, nd, na = rew_detail_audit(s, 'leaseOrders', '../租赁管理/租赁单详情.html', '../租赁管理/租赁单审核.html')
s, n = rew_act(s, 'leaseOrders', "openModal('createModal')", "go('../租赁管理/租赁单新建.html')")
print('leaseOrders: detail×%d audit×%d create×%d' % (nd, na, n))
s, nd, na = rew_detail_audit(s, 'comboOutbounds', '../租赁管理/租赁出库详情.html')
s, n = rew_act(s, 'comboOutbounds', "openModal('exitConfirmModal')", "go('../租赁管理/租赁出库确认.html?id=CK-20260910-022')")
# exitConfirm 需要按键——rew_act 无键；改用行级正则
a, b = s.index('comboOutbounds: {'), s.index('\n  },', s.index('comboOutbounds: {'))
blk = s[s.rfind('\n', 0, a) + 1:b]
lines = blk.split('\n'); key = None; nck = 0
for i, ln in enumerate(lines):
    mk = re.search(r"^\s*'([A-Za-z0-9\-\.]+)': \{", ln)
    if mk and mk.group(1) != 'row':
        key = mk.group(1)
    if "openModal('exitConfirmModal')" in ln:
        assert key
        ln = ln.replace("openModal('exitConfirmModal')", "go('../租赁管理/租赁出库确认.html?id=%s')" % key)
        nck += 1
    lines[i] = ln
s = s[:s.rfind('\n', 0, a) + 1] + '\n'.join(lines) + s[b:]
print('comboOutbounds: detail×%d exitConfirm×%d' % (nd, nck))
s, nd, na = rew_detail_audit(s, 'returnInbounds', '../租赁管理/退租入库详情.html', '../租赁管理/退租入库审核.html')
print('returnInbounds: detail×%d audit×%d' % (nd, na))
s, nd, na = rew_detail_audit(s, 'rentInOrders', '../租入管理/租入单详情.html', '../租入管理/租入单审核.html')
print('rentInOrders: detail×%d audit×%d' % (nd, na))
s, nd, na = rew_detail_audit(s, 'rentInbounds', '../租入管理/租入入库详情.html', '../租入管理/租入入库确认.html')
print('rentInbounds: detail×%d audit×%d(→确认页)' % (nd, na))
s, nd, na = rew_detail_audit(s, 'rentInReturns', '../租入管理/租入归还详情.html', '../租入管理/租入归还审核.html')
print('rentInReturns: detail×%d audit×%d' % (nd, na))
s, n = rew_todo_links(s, {
    '租赁管理/租赁单列表.html': '租赁管理/租赁单审核.html',
    '租赁管理/退租入库列表.html': '租赁管理/退租入库审核.html',
    '租赁管理/租赁出库列表.html': '租赁管理/租赁出库确认.html',
    '租入管理/租入单列表.html': '租入管理/租入单审核.html',
    '租入管理/租入入库列表.html': '租入管理/租入入库确认.html',
    '租入管理/租入归还列表.html': '租入管理/租入归还审核.html',
})
print('todoItems links ×%d → B3 审核/确认页' % n)
assert 'id=row' not in s
wr('_data/demo-data.js', s)
t = rd('我的待办.html')
for lst, ap in [('租赁管理/租赁单列表.html?audit=1', '../租赁管理/租赁单审核.html'),
                ('租赁管理/退租入库列表.html?audit=1', '../租赁管理/退租入库审核.html'),
                ('租赁管理/租赁出库列表.html?audit=1', '../租赁管理/租赁出库确认.html'),
                ('租入管理/租入单列表.html?audit=1', '../租入管理/租入单审核.html'),
                ('租入管理/租入入库列表.html?audit=1', '../租入管理/租入入库确认.html'),
                ('租入管理/租入归还列表.html?audit=1', '../租入管理/租入归还审核.html')]:
    oc = "go('%s')" % lst
    if oc in t:
        t = t.replace(oc, "go('%s')" % ap)
        print('待办静态: %s → %s' % (lst.split('/')[-1], ap.split('/')[-1]))
wr('我的待办.html', t)

# ---- 删模板（先清注释引用） ----
s = rd('租入管理/租入归还列表.html')
for cmt in re.findall(r'<!--[^>]*弹窗/[^>]*-->', s):
    print('注释:', cmt[:90])
    s = s.replace(cmt, '<!-- G36 B3：弹窗已页面化 -->')
wr('租入管理/租入归还列表.html', s)
names = ['器具出租履历', '租赁出库单详情', '租赁出库确认', '租赁单审核', '租赁单新建', '租赁单详情', '退租入库单详情', '退租入库审核', '退租入库新建',
         '租入入库单详情', '租入入库确认', '租入单审核', '租入单新建', '租入单详情', '租入归还单详情', '租入归还审核', '租入归还新建']
total = 0
for dp, dn, fns in os.walk('.'):
    if '.git' in dp:
        continue
    for fn in fns:
        if fn.endswith(('.html', '.js', '.txt')):
            fp = os.path.join(dp, fn)
            txt = io.open(fp, encoding='utf-8', errors='ignore').read()
            for n2 in names:
                if ('弹窗/%s.html' % n2) in txt:
                    total += 1
                    print('REF:', fp.replace(os.sep, '/'), '::', n2)
print('删前引用数:', total)
if total == 0:
    for n2 in names:
        for mod in (L, R):
            fp = os.path.join(ROOT, mod, '弹窗', n2 + '.html')
            if os.path.exists(fp):
                os.remove(fp)
    print('deleted 17 templates ✓')
else:
    print('BLOCKED — 需先清引用')
