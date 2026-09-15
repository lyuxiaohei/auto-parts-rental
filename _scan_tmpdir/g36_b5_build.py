# -*- coding: utf-8 -*-
"""G36 B5：财务 14＋系统 4 → 18 页（应付/应收专用渲染器·权限配置参数化·2 保留弹窗）"""
import sys, io, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g36_factory import dpage, apage, fpage, cut_overlay, cut_script_containing, rd, wr, rew_detail_audit, rew_act, rew_regex, rew_todo_links, assemble, ROOT

F = '财务管理'; S = '系统管理'
H_FK = '../财务协同/付款登记.html'; H_HK = '../财务协同/回款登记.html'; H_YF = '../财务协同/应付账单.html'
H_YS = '../财务协同/应收账单.html'; H_KP = '../财务协同/开票登记.html'; H_SD = '../财务协同/银行水单核销.html'
H_TK = '../财务协同/退款登记.html'; H_ZD = '../系统管理/数据字典.html'; H_YH = '../系统管理/用户权限.html'; H_JS = '../系统管理/角色管理.html'
MC_F = '财务协同'

built = []
# ---- 财务 14 ----
built.append(fpage(MC_F + '/付款新建.html', '财务协同/弹窗/付款登记新建.html', H_FK, '付款登记', '新建付款登记', '新建付款登记', F, '付款登记', H_FK, card_title='付款信息'))
built.append(dpage(MC_F + '/付款详情.html', 'payments', 'PAY-20260902-005', H_FK, '付款登记', '付款详情', '付款登记详情', F, '付款登记', H_FK))
built.append(apage(MC_F + '/付款确认.html', 'payments', 'PAY-20260902-005', H_FK, '付款登记', '付款确认', '付款确认', F, '付款登记', H_FK, hint='确认后流水核销应付并更新付款状态；驳回退回待确认。'))
built.append(dpage(MC_F + '/回款详情.html', 'receipts', 'HK-20260830-014', H_HK, '收款登记', '回款详情', '回款登记详情', F, '收款登记', H_HK))
built.append(fpage(MC_F + '/应付新建.html', '财务协同/弹窗/应付账单新建.html', H_YF, '应付账单', '新建应付账单', '新建应付账单', F, '应付账单', H_YF, card_title='账单信息'))
built.append(fpage(MC_F + '/应收生成.html', '财务协同/弹窗/应收账单生成.html', H_YS, '应收账单', '生成应收账单', '生成应收账单', F, '应收账单', H_YS, card_title='生成口径'))
built.append(fpage(MC_F + '/开票新建.html', '财务协同/弹窗/开票登记新建.html', H_KP, '开票登记', '新建开票登记', '新建开票登记', F, '开票登记', H_KP, card_title='开票信息'))
built.append(dpage(MC_F + '/开票详情.html', 'invoices', 'INV-20260902-013', H_KP, '开票登记', '开票详情', '开票登记详情', F, '开票登记', H_KP))
built.append(fpage(MC_F + '/收款新建.html', '财务协同/弹窗/收款登记新建.html', H_HK, '收款登记', '新建收款登记', '新建收款登记', F, '收款登记', H_HK, card_title='收款信息'))
built.append(dpage(MC_F + '/水单核销详情.html', 'writeoffs', 'HX-20260830-012', H_SD, '收款核销', '水单核销详情', '水单核销详情 · SD', F, '收款核销', H_SD))
built.append(fpage(MC_F + '/退款新建.html', '财务协同/弹窗/退款登记新建.html', H_TK, '退款登记', '新建退款登记', '新建退款登记', F, '退款登记', H_TK, card_title='退款信息'))
built.append(dpage(MC_F + '/退款详情.html', 'refunds', 'TKD-20260914-001', H_TK, '退款登记', '退款详情', '退款登记详情', F, '退款登记', H_TK))

# 应付详情（专用渲染器 renderPayableBillDetailHTML）
content = ('<div class="card">\n  <div class="card-head">\n'
           '    <h3 class="card-title" id="dtTitle">应付账单详情</h3>\n'
           '    <div class="head-btns"><button class="btn btn-default btn-sm" onclick="go(\'%s\')">返回列表</button></div>\n'
           '  </div>\n  <div id="detailBody"><!-- 内容由 _data/payable-bill-detail.js 按账单号渲染 --></div>\n</div>\n' % H_YF)
scripts = ('<script src="../_data/payable-bill-detail.js"></script>\n<script>\n'
           '(function () {\n'
           '  var k = null;\n'
           '  try { k = new URLSearchParams(location.search).get("id"); } catch (e) {}\n'
           '  var D = (window.DEMO_DATA || {}).payableBills || {};\n'
           '  if (!D[k]) k = Object.keys(D).filter(function (x) { return D[x] && (D[x].info || D[x].row); })[0] || "AP-20260905-013";\n'
           '  var rec = D[k] || {};\n'
           '  var t = document.getElementById("dtTitle");\n'
           '  if (t) t.textContent = "应付账单详情 · " + (rec.titleNo || ((rec.row || {}).fields || {})["key"] || k);\n'
           '  var el = document.getElementById("detailBody");\n'
           '  if (el && window.renderPayableBillDetailHTML) el.innerHTML = window.renderPayableBillDetailHTML(rec, "../");\n'
           '})();\n</script>')
built.append(assemble(MC_F + '/应付详情.html', '应付账单详情', '应付账单', '应付详情', F, '应付账单', H_YF, content, scripts, '', detail=True))
# 应收详情（专用渲染器）
content = ('<div class="card">\n  <div class="card-head">\n'
           '    <h3 class="card-title" id="dtTitle">应收账单详情</h3>\n'
           '    <div class="head-btns"><button class="btn btn-default btn-sm" onclick="go(\'%s\')">返回列表</button></div>\n'
           '  </div>\n  <div id="detailBody"><!-- 内容由 _data/receivable-bill-detail.js 按账单号渲染 --></div>\n</div>\n' % H_YS)
scripts = ('<script src="../_data/receivable-bill-detail.js"></script>\n<script>\n'
           '(function () {\n'
           '  var k = null;\n'
           '  try { k = new URLSearchParams(location.search).get("id"); } catch (e) {}\n'
           '  var D = (window.DEMO_DATA || {}).receivableBills || {};\n'
           '  if (!D[k]) k = Object.keys(D).filter(function (x) { return D[x] && (D[x].info || D[x].row); })[0] || "AR-20260904-015";\n'
           '  var rec = D[k] || {};\n'
           '  var t = document.getElementById("dtTitle");\n'
           '  if (t) t.textContent = "应收账单详情 · " + (rec.titleNo || ((rec.row || {}).fields || {})["key"] || k);\n'
           '  var el = document.getElementById("detailBody");\n'
           '  if (el && window.renderReceivableBillDetailHTML) el.innerHTML = window.renderReceivableBillDetailHTML(rec, "../");\n'
           '})();\n</script>')
built.append(assemble(MC_F + '/应收详情.html', '应收账单详情', '应收账单', '应收详情', F, '应收账单', H_YS, content, scripts, '', detail=True))

# ---- 系统 4 ----
built.append(fpage('系统管理/字典项新建.html', '系统管理/弹窗/新增字典项.html', H_ZD, '数据字典', '新增字典项', '新增字典项', S, '数据字典', H_ZD, card_title='字典项信息'))
built.append(fpage('系统管理/用户新建.html', '系统管理/弹窗/新增用户.html', H_YH, '用户权限', '新增用户', '新增用户', S, '用户权限', H_YH, card_title='用户信息'))
built.append(fpage('系统管理/角色新建.html', '系统管理/弹窗/新增角色.html', H_JS, '角色管理', '新增角色', '新增角色', S, '角色管理', H_JS, card_title='角色信息'))
# 权限配置（roleModal 参数化移植 + pins）
built.append(fpage('系统管理/权限配置.html', '系统管理/弹窗/权限配置.html', H_JS, '角色管理', '权限配置', '权限配置', S, '角色管理', H_JS, card_title='权限矩阵'))
# pins 迁移
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
    print('pins 迁移: %s (%d)' % (page, pins.count('proto-pin" id=')))
migrate_pins('系统管理/弹窗/权限配置.html', '系统管理/权限配置.html')
# 权限配置：?role= 参数应用（ROLE_PERM 从角色管理页取）
src = rd('系统管理/角色管理.html')
i = src.index('window.ROLE_PERM')
a0 = src.rfind('<script', 0, i)
j0 = src.index('</script>', i) + 9
roleperm_script = src[a0:j0]
# 从该 script 里只留 ROLE_PERM 定义（含 openRolePerm 时剥离）——直接整块带过（openRolePerm 引用 DOM 需守卫）
g = rd('系统管理/权限配置.html')
ins = roleperm_script + '\n<script>\n/* G36 B5：?role= 参数应用（openRolePerm 页面化重写） */\n' + '''
(function () {
  var name = null;
  try { name = new URLSearchParams(location.search).get("role"); } catch (e) {}
  if (!name) name = Object.keys(window.ROLE_PERM || {})[0] || "系统管理员";
  var p = window.ROLE_PERM && window.ROLE_PERM[name] || { desc: "", accts: "", scope: "全部项目", perms: [] };
  function ap() {
    var t = document.getElementById("rolePermTitle");
    if (t) t.textContent = "权限配置 · " + name;
    var n1 = document.getElementById("rpName"); if (n1) n1.textContent = name;
    var d1 = document.getElementById("rpDesc"); if (d1) d1.textContent = p.desc;
    var a1 = document.getElementById("rpAccts"); if (a1) a1.textContent = p.accts;
    document.querySelectorAll(".checkbox[data-perm]").forEach(function (c) {
      c.classList.toggle("checked", p.perms.indexOf(c.getAttribute("data-perm")) > -1);
    });
    document.querySelectorAll(".radio[data-scope]").forEach(function (r) {
      r.classList.toggle("checked", r.getAttribute("data-scope") === p.scope);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ap); else ap();
})();
</script>'''
anchor = '</body>'
assert g.count(anchor) == 1
g = g.replace(anchor, ins + '\n' + anchor)
wr('系统管理/权限配置.html', g)
print('权限配置 ?role= 应用脚本 ✓')
print('BUILT B5 %d pages' % len(built))

# ---- 宿主页接线 ----
def rewire_host(path, del_ovs, btn_map, id_map, extra_funcs=()):
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
    if '?audit=1 自动打开审核弹窗' in s:
        i0 = s.index('?audit=1 自动打开审核弹窗')
        a0 = s.rfind('<script', 0, i0)
        j0 = s.index('</script>', i0) + 9
        if any(mid in s[a0:j0] for mid in del_ovs):
            s = s[:a0] + s[j0:]
            print('  %s: audit=1 脚本剪除' % path.split('/')[-1])
    for mid in del_ovs:
        while True:
            hit = None
            for m2 in re.finditer(r'<script(?![^>]*src=)[^>]*>(?:(?!</script>).)*</script>', s, re.S):
                if mid in m2.group(0):
                    hit = m2
                    break
            if not hit:
                break
            s = s[:hit.start()] + s[hit.end():]
            print('  %s: 专属脚本块剪除（%s）' % (path.split('/')[-1], mid))
    for mid in del_ovs:
        assert mid not in s, mid + ' residue in ' + path
    wr(path, s)

rewire_host(MC_F + '/付款登记.html', ['createModal', 'auditModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../财务协同/付款新建.html')\""},
    {'detailModal': '../财务协同/付款详情.html', 'auditModal': '../财务协同/付款确认.html'})
rewire_host(MC_F + '/回款登记.html', ['createModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../财务协同/收款新建.html')\""},
    {'detailModal': '../财务协同/回款详情.html'})  # auditModal 保留（B5 清单外）
rewire_host(MC_F + '/应付账单.html', ['createModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../财务协同/应付新建.html')\""},
    {'detailModal': '../财务协同/应付详情.html'})  # 数据行走 detailFn（改 cfg·带键）；audit/inst 保留
s = rd(MC_F + '/应付账单.html')
old_fn = "detailFn: function (entity, key) { openPayableBillDetail(key); }"
assert s.count(old_fn) == 1
s = s.replace(old_fn, "detailFn: function (entity, key) { go('../财务协同/应付详情.html?id=' + key); }")
wr(MC_F + '/应付账单.html', s)
print('  应付账单: detailFn → go 应付详情?id=')
rewire_host(MC_F + '/应收账单.html', ['createModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../财务协同/应收生成.html')\""},
    {'detailModal': '../财务协同/应收详情.html'})
s = rd(MC_F + '/应收账单.html')
m5 = re.search(r"detailFn: function \(entity, key\) \{[^}]*\}", s)
assert m5, '应收 detailFn not found'
s = s.replace(m5.group(0), "detailFn: function (entity, key) { go('../财务协同/应收详情.html?id=' + key); }")
wr(MC_F + '/应收账单.html', s)
print('  应收账单: detailFn → go 应收详情?id=')
rewire_host(MC_F + '/开票登记.html', ['createModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../财务协同/开票新建.html')\""},
    {'detailModal': '../财务协同/开票详情.html'})
rewire_host(MC_F + '/银行水单核销.html', ['detailModal'], {},
    {'detailModal': '../财务协同/水单核销详情.html'})  # undoModal 保留
rewire_host(MC_F + '/退款登记.html', ['createModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../财务协同/退款新建.html')\""},
    {}, extra_funcs=['function openRetDetail'])
s = rd(MC_F + '/退款登记.html')
s, n = re.subn(r"onclick=\"openRetDetail\('[^']+', '([^']+)'\)\"", r"onclick=\"go('../财务协同/退款详情.html?id=\1')\"", s)
wr(MC_F + '/退款登记.html', s)
print('  退款登记: openRetDetail 静态 ×%d' % n)
rewire_host('系统管理/数据字典.html', ['createModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../系统管理/字典项新建.html')\""},
    {})  # stopModal 保留
rewire_host('系统管理/用户权限.html', ['roleModal', 'createModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../系统管理/用户新建.html')\""},
    {'roleModal': '../系统管理/权限配置.html'})  # stop/reset 保留
rewire_host('系统管理/角色管理.html', ['roleModal', 'createModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../系统管理/角色新建.html')\""},
    {})  # openRolePerm 数据脚本保留（页面复用其 ROLE_PERM）
s = rd('系统管理/角色管理.html')
s, n = re.subn(r"openRolePerm\('([^']+)'\)", r"go('../系统管理/权限配置.html?role=\1')", s)
wr('系统管理/角色管理.html', s)
print('  角色管理: openRolePerm ×%d → 权限配置?role=' % n)

# ---- demo-data ops ----
s = rd('_data/demo-data.js')
s, nd, na = rew_detail_audit(s, 'payments', '../财务协同/付款详情.html', '../财务协同/付款确认.html')
print('payments: detail×%d audit×%d(→确认页)' % (nd, na))
s, nd, na = rew_detail_audit(s, 'receipts', '../财务协同/回款详情.html')
print('receipts: detail×%d（audit 保留）' % nd)
s, nd, na = rew_detail_audit(s, 'invoices', '../财务协同/开票详情.html')
print('invoices: detail×%d（audit 保留）' % nd)
s, nd, na = rew_detail_audit(s, 'writeoffs', '../财务协同/水单核销详情.html')
print('writeoffs: detail×%d（undo 保留）' % nd)
s, n = rew_regex(s, 'refunds', r"openRetDetail\('refunds', '([^']+)'\)", r"go('../财务协同/退款详情.html?id=\1')")
print('refunds: openRetDetail×%d' % n)
s, n = rew_act(s, 'users', "openModal('createModal')", "go('../系统管理/用户新建.html')")
print('users: create×%d' % n)
s, n = rew_act(s, 'users', "openModal('roleModal')", "go('../系统管理/权限配置.html')")
print('users: roleModal×%d' % n)
s, n = re.subn(r"openRolePerm\('([^']+)'\)", r"go('../系统管理/权限配置.html?role=\1')", s)
print('roles: openRolePerm×%d（全库）' % n)
s, n = rew_todo_links(s, {
    '财务协同/付款登记.html': '财务协同/付款确认.html',
})
print('todoItems links ×%d → 付款确认页（回款/退款审核弹窗保留·链接不动）' % n)
assert 'id=row' not in s
wr('_data/demo-data.js', s)
t = rd('我的待办.html')
oc = "go('财务协同/付款登记.html?audit=1')"
if oc in t:
    t = t.replace(oc, "go('../财务协同/付款确认.html')")
    print('待办静态: 付款登记 audit=1 → 付款确认页')
wr('我的待办.html', t)

# ---- 构建注释 + 删模板 ----
for hp in [MC_F + '/付款登记.html', MC_F + '/回款登记.html', MC_F + '/应付账单.html', MC_F + '/应收账单.html', MC_F + '/开票登记.html', MC_F + '/银行水单核销.html', MC_F + '/退款登记.html', '系统管理/数据字典.html', '系统管理/用户权限.html', '系统管理/角色管理.html']:
    x = rd(hp)
    for cmt in re.findall(r'<!--[^>]*弹窗/[^>]*-->', x):
        print('注释:', hp.split('/')[-1], '::', cmt[:70])
        x = x.replace(cmt, '<!-- G36 B5：弹窗已页面化 -->')
    wr(hp, x)
names = ['付款登记新建', '付款登记详情', '付款确认', '回款登记详情', '应付账单新建', '应付账单详情', '应收账单生成', '应收账单详情',
         '开票登记新建', '开票登记详情', '收款登记新建', '水单核销详情', '退款登记新建', '退款登记详情',
         '新增字典项', '新增用户', '新增角色', '权限配置']
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
assert total == 0
for n2 in names:
    for mod in (MC_F, '系统管理'):
        fp = os.path.join(ROOT, mod, '弹窗', n2 + '.html')
        if os.path.exists(fp):
            os.remove(fp)
print('deleted 18 templates ✓')
