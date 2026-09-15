# -*- coding: utf-8 -*-
"""G36 B2：采购 7＋销售 9 → 16 页面"""
import sys, io, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g36_factory import dpage, apage, fpage, cut_overlay, cut_script_containing, rd, wr, rew_detail_audit, rew_act, rew_regex, rew_todo_links

G = '采购管理'; S = '销售管理'
H_PO = '../采购管理/采购订单列表.html'; H_PI = '../采购管理/采购入库列表.html'; H_PR = '../采购管理/采购退货单列表.html'
H_SO = '../销售管理/销售订单列表.html'; H_SE = '../销售管理/销售出库列表.html'; H_SR = '../销售管理/销售退货单列表.html'

built = []
# ---- 采购 7 ----
built.append(dpage('采购管理/采购订单详情.html', 'purchaseOrders', 'PO-20260902-018', H_PO, '采购订单', '采购订单详情', '采购订单详情', G, '采购订单', H_PO))
built.append(apage('采购管理/采购订单审核.html', 'purchaseOrders', 'PO-20260902-018', H_PO, '采购订单', '采购订单审核', '采购订单审核', G, '采购订单', H_PO))
built.append(dpage('采购管理/采购入库详情.html', 'purchaseInbounds', 'CGRK-20260828-012', H_PI, '采购入库', '采购入库详情', '采购入库单详情', G, '采购入库', H_PI))
built.append(apage('采购管理/采购入库审核.html', 'purchaseInbounds', 'CGRK-20260828-012', H_PI, '采购入库', '采购入库审核', '采购入库审核', G, '采购入库', H_PI))
built.append(dpage('采购管理/采购退货详情.html', 'purchaseReturns', 'CGTH-20260914-001', H_PR, '采购退货', '采购退货详情', '采购退货单详情', G, '采购退货', H_PR))
built.append(apage('采购管理/采购退货审核.html', 'purchaseReturns', 'CGTH-20260914-001', H_PR, '采购退货', '采购退货审核', '采购退货审核', G, '采购退货', H_PR))
built.append(fpage('采购管理/采购退货新建.html', '采购管理/弹窗/新建采购退货单.html', H_PR, '采购退货', '新建采购退货单', '新建采购退货单', G, '采购退货', H_PR, card_title='退货信息'))
# ---- 销售 9 ----
built.append(dpage('销售管理/销售订单详情.html', 'salesOrders', 'SO-20260903-0047', H_SO, '销售订单', '销售订单详情', '销售订单详情', S, '销售订单', H_SO))
built.append(apage('销售管理/销售订单审核.html', 'salesOrders', 'SO-20260903-0047', H_SO, '销售订单', '销售订单审核', '销售订单审核', S, '销售订单', H_SO))
built.append(fpage('销售管理/销售订单新建.html', '销售管理/弹窗/新建销售订单.html', H_SO, '销售订单', '新建销售订单', '新建销售订单', S, '销售订单', H_SO, card_title='订单信息'))
built.append(dpage('销售管理/销售出库详情.html', 'salesOutbounds', 'XSCK-20260902-015', H_SE, '销售出库', '销售出库详情', '销售出库单详情', S, '销售出库', H_SE))
built.append(apage('销售管理/销售出库审核.html', 'salesOutbounds', 'XSCK-20260902-015', H_SE, '销售出库', '销售出库审核', '销售出库审核', S, '销售出库', H_SE))
built.append(fpage('销售管理/销售出库新建.html', '销售管理/弹窗/销售出库新建.html', H_SE, '销售出库', '新建销售出库单', '新建销售出库单', S, '销售出库', H_SE, card_title='出库信息'))
built.append(dpage('销售管理/销售退货详情.html', 'salesReturns', 'XSTH-20260913-001', H_SR, '销售退货', '销售退货详情', '销售退货单详情', S, '销售退货', H_SR))
built.append(apage('销售管理/销售退货审核.html', 'salesReturns', 'XSTH-20260913-001', H_SR, '销售退货', '销售退货审核', '销售退货审核', S, '销售退货', H_SR))
built.append(fpage('销售管理/销售退货新建.html', '销售管理/弹窗/新建销售退货单.html', H_SR, '销售退货', '新建销售退货单', '新建销售退货单', S, '销售退货', H_SR, card_title='退货信息'))
print('BUILT B2 %d pages' % len(built))

# ============ 宿主页接线 ============
def rewire_host(path, del_ovs, btn_map, static_map, extra_funcs=(), ret_detail_url=None, id_map=None):
    s = rd(path)
    for mid in del_ovs:
        if '<div class="modal-overlay" id="%s"' % mid in s:
            s = cut_overlay(s, mid)
    for oc, nk in btn_map.items():
        n = s.count(oc)
        s = s.replace(oc, nk)
        print('  %s: %s ×%d' % (path.split('/')[-1], oc[:44], n))
    for oc, nk in static_map.items():
        s = s.replace(oc, nk)
    if id_map:
        for mid, url in id_map.items():
            s, n = re.subn(r"openModal\('%s'\)" % mid, "go('%s')" % url, s)
            if n:
                print('  %s: openModal(%s) ×%d → go(%s)' % (path.split('/')[-1], mid, n, url.split('/')[-1]))
    if ret_detail_url:
        s, n = re.subn(r"onclick=\"openRetDetail\('[^']+', '([^']+)'\)\"", 'onclick="go(\'%s?id=\\1\')"' % ret_detail_url, s)
        print('  %s: openRetDetail 静态 ×%d → %s' % (path.split('/')[-1], n, ret_detail_url))
    for fn_marker in extra_funcs:
        if fn_marker in s:
            s = cut_script_containing(s, fn_marker)
    if 'auditModal' in del_ovs and '?audit=1 自动打开审核弹窗' in s:
        s = cut_script_containing(s, '?audit=1 自动打开审核弹窗')
    s = re.sub(r"\r?\n[ \t]*modalId: 'detailModal'", '', s)
    for mid in del_ovs:
        assert mid not in s, mid + ' residue in ' + path
    wr(path, s)

rewire_host('采购管理/采购订单列表.html', ['auditModal', 'detailModal'], {}, {},
    id_map={'detailModal': '../采购管理/采购订单详情.html', 'auditModal': '../采购管理/采购订单审核.html'})
rewire_host('采购管理/采购入库列表.html', ['auditModal', 'detailModal'], {}, {},
    id_map={'detailModal': '../采购管理/采购入库详情.html', 'auditModal': '../采购管理/采购入库审核.html'})
rewire_host('采购管理/采购退货单列表.html', ['createModal', 'auditModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../采购管理/采购退货新建.html')\""}, {},
    extra_funcs=['function openRetDetail'], ret_detail_url='../采购管理/采购退货详情.html',
    id_map={'auditModal': '../采购管理/采购退货审核.html'})
rewire_host('销售管理/销售订单列表.html', ['createModal', 'auditModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../销售管理/销售订单新建.html')\""}, {},
    id_map={'detailModal': '../销售管理/销售订单详情.html', 'auditModal': '../销售管理/销售订单审核.html'})
rewire_host('销售管理/销售出库列表.html', ['createModal', 'auditModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../销售管理/销售出库新建.html')\""}, {},
    id_map={'detailModal': '../销售管理/销售出库详情.html', 'auditModal': '../销售管理/销售出库审核.html'})
rewire_host('销售管理/销售退货单列表.html', ['createModal', 'auditModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../销售管理/销售退货新建.html')\""}, {},
    extra_funcs=['function openRetDetail'], ret_detail_url='../销售管理/销售退货详情.html',
    id_map={'auditModal': '../销售管理/销售退货审核.html'})

# ============ demo-data ops ============
s = rd('_data/demo-data.js')
s, nd, na = rew_detail_audit(s, 'purchaseOrders', '../采购管理/采购订单详情.html', '../采购管理/采购订单审核.html')
print('purchaseOrders: detail×%d audit×%d' % (nd, na))
s, nd, na = rew_detail_audit(s, 'purchaseInbounds', '../采购管理/采购入库详情.html', '../采购管理/采购入库审核.html')
print('purchaseInbounds: detail×%d audit×%d' % (nd, na))
s, nd, na = rew_detail_audit(s, 'purchaseReturns', '../采购管理/采购退货详情.html', '../采购管理/采购退货审核.html')
print('purchaseReturns: detail×%d audit×%d' % (nd, na))
s, n = rew_regex(s, 'purchaseReturns', r"openRetDetail\('purchaseReturns', '([^']+)'\)", r"go('../采购管理/采购退货详情.html?id=\1')")
print('purchaseReturns openRetDetail×%d' % n)
s, nd, na = rew_detail_audit(s, 'salesOrders', '../销售管理/销售订单详情.html', '../销售管理/销售订单审核.html')
s, n = rew_act(s, 'salesOrders', "openModal('createModal')", "go('../销售管理/销售订单新建.html')")
print('salesOrders: detail×%d audit×%d create×%d' % (nd, na, n))
s, nd, na = rew_detail_audit(s, 'salesOutbounds', '../销售管理/销售出库详情.html', '../销售管理/销售出库审核.html')
print('salesOutbounds: detail×%d audit×%d' % (nd, na))
s, nd, na = rew_detail_audit(s, 'salesReturns', '../销售管理/销售退货详情.html', '../销售管理/销售退货审核.html')
s, n = rew_regex(s, 'salesReturns', r"openRetDetail\('salesReturns', '([^']+)'\)", r"go('../销售管理/销售退货详情.html?id=\1')")
print('salesReturns: detail×%d audit×%d openRetDetail×%d' % (nd, na, n))
assert 'id=row' not in s
s, n = rew_todo_links(s, {
    '采购管理/采购订单列表.html': '采购管理/采购订单审核.html',
    '采购管理/采购入库列表.html': '采购管理/采购入库审核.html',
    '销售管理/销售订单列表.html': '销售管理/销售订单审核.html',
    '销售管理/销售出库列表.html': '销售管理/销售出库审核.html',
})
print('todoItems links ×%d → B2 审核页' % n)
wr('_data/demo-data.js', s)
# 我的待办 静态 4 链接（无键→审核页默认待审记录）
t = rd('我的待办.html')
for lst, ap in [('采购管理/采购订单列表.html?audit=1', '../采购管理/采购订单审核.html'),
                ('采购管理/采购入库列表.html?audit=1', '../采购管理/采购入库审核.html'),
                ('销售管理/销售订单列表.html?audit=1', '../销售管理/销售订单审核.html'),
                ('销售管理/销售出库列表.html?audit=1', '../销售管理/销售出库审核.html'),
                ('采购管理/采购退货单列表.html?audit=1', '../采购管理/采购退货审核.html'),
                ('销售管理/销售退货单列表.html?audit=1', '../销售管理/销售退货审核.html')]:
    oc = "go('%s')" % lst
    if oc in t:
        t = t.replace(oc, "go('%s')" % ap)
        print('待办静态: %s → %s' % (lst, ap))
wr('我的待办.html', t)
print('demo-data B2 ✓')

# ============ 删模板（先清构建注释/F01 链接，再引用校验） ============
COMMENT_FIX = {
    '采购管理/采购入库列表.html': [('<!-- 弹窗已提取到 弹窗/采购入库审核.html，构建时注入 -->', '<!-- 采购入库审核已页面化：采购管理/采购入库审核.html（G36 B2） -->')],
    '采购管理/采购订单列表.html': [('<!-- 弹窗已提取到 弹窗/采购订单审核.html，构建时注入 -->', '<!-- 采购订单审核已页面化：采购管理/采购订单审核.html（G36 B2） -->')],
    '采购管理/采购退货单列表.html': [('<!-- 弹窗已提取到 弹窗/采购入库审核.html，构建时注入 -->', '<!-- 审核已页面化（G36 B2） -->'), ('<!-- G33 新建采购退货单（模板：采购管理/弹窗/新建采购退货单.html） -->', '<!-- 新建采购退货单已页面化：采购管理/采购退货新建.html（G36 B2·原 G33 模板） -->')],
    '销售管理/销售出库列表.html': [('<!-- 弹窗已提取到 弹窗/销售出库新建.html，构建时注入 -->', '<!-- 销售出库新建已页面化：销售管理/销售出库新建.html（G36 B2） -->'), ('<!-- 弹窗已提取到 弹窗/销售出库审核.html，构建时注入 -->', '<!-- 销售出库审核已页面化：销售管理/销售出库审核.html（G36 B2） -->')],
    '销售管理/销售订单列表.html': [('<!-- 弹窗已提取到 弹窗/新建销售订单.html，构建时注入 -->', '<!-- 新建销售订单已页面化：销售管理/销售订单新建.html（G36 B2） -->'), ('<!-- 弹窗已提取到 弹窗/销售订单审核.html，构建时注入 -->', '<!-- 销售订单审核已页面化：销售管理/销售订单审核.html（G36 B2） -->')],
    '销售管理/销售退货单列表.html': [('<!-- 弹窗已提取到 弹窗/销售出库新建.html，构建时注入 -->', '<!-- 审核已页面化（G36 B2） -->'), ('<!-- G33 新建销售退货单（模板：采购管理/弹窗/新建销售退货单.html） -->', '<!-- 新建销售退货单已页面化：销售管理/销售退货新建.html（G36 B2·原 G33 模板） -->')],
}
for hp, pairs in COMMENT_FIX.items():
    s2 = rd(hp)
    for o3, n3 in pairs:
        if o3 in s2:
            s2 = s2.replace(o3, n3)
    wr(hp, s2)
s3 = rd('P3-R01-F01-业务流程导航图.html')
if '采购管理/弹窗/采购入库审核.html' in s3:
    s3 = s3.replace('采购管理/弹窗/采购入库审核.html', '采购管理/采购入库审核.html')
    wr('P3-R01-F01-业务流程导航图.html', s3)
    print('F01 采购入库审核链接改指新页 ✓')

names = ['新建采购退货单', '采购入库单详情', '采购入库审核', '采购订单审核', '采购订单详情', '采购退货单详情', '采购退货审核',
         '新建销售订单', '新建销售退货单', '销售出库单详情', '销售出库审核', '销售出库新建', '销售订单审核', '销售订单详情', '销售退货单详情', '销售退货审核']
total = 0
for n2 in names:
    for dp, dn, fns in os.walk('.'):
        if '.git' in dp:
            continue
        for fn in fns:
            if fn.endswith(('.html', '.js', '.txt')):
                fp = os.path.join(dp, fn)
                if ('/%s/弹窗/%s.html' % (G, n2) in fp.replace(os.sep, '/')) or ('/%s/弹窗/%s.html' % (S, n2) in fp.replace(os.sep, '/')):
                    continue
                if ('弹窗/%s.html' % n2) in io.open(fp, encoding='utf-8', errors='ignore').read():
                    total += 1
                    print('REF:', fp)
print('删前引用数:', total)
assert total == 0
for n2 in names:
    for mod in (G, S):
        fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'P3-R01-包装租赁管理后台原型', mod, '弹窗', n2 + '.html')
        fp = os.path.normpath(fp)
        if os.path.exists(fp):
            os.remove(fp)
print('deleted 16 templates ✓')
