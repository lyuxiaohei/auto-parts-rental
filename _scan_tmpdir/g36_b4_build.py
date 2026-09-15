# -*- coding: utf-8 -*-
"""G36 B4：仓储作业 12 → 12 页面"""
import sys, io, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g36_factory import dpage, apage, fpage, cut_overlay, cut_script_containing, rd, wr, rew_detail_audit, rew_act, rew_todo_links, ROOT

W = '仓储管理'  # 侧边栏组名（目录=仓储作业）
M = '仓储作业'
H_QT = '../仓储作业/其他入库列表.html'; H_QC = '../仓储作业/其他出库列表.html'
H_PD = '../仓储作业/盘点列表.html'; H_DB = '../仓储作业/库存调拨列表.html'; H_KC = '../仓储作业/库存查询.html'

built = []
built.append(dpage(M + '/其他入库详情.html', 'otherInbounds', 'QTRK-20260901-003', H_QT, '其他入库', '其他入库详情', '其他入库单详情', W, '其他入库', H_QT))
built.append(apage(M + '/其他入库审核.html', 'otherInbounds', 'QTRK-20260901-003', H_QT, '其他入库', '其他入库审核', '其他入库审核', W, '其他入库', H_QT, hint='审核通过后手工例外入库生效并计入在库；驳回作废。'))
built.append(fpage(M + '/其他入库新建.html', '仓储作业/弹窗/其他入库新建.html', H_QT, '其他入库', '新建其他入库单', '新建其他入库单', W, '其他入库', H_QT, card_title='入库信息'))
built.append(dpage(M + '/其他出库详情.html', 'otherOutbounds', 'QTCK-20260905-005', H_QC, '其他出库', '其他出库详情', '其他出库单详情', W, '其他出库', H_QC))
built.append(apage(M + '/其他出库审核.html', 'otherOutbounds', 'QTCK-20260905-005', H_QC, '其他出库', '其他出库审核', '其他出库审核', W, '其他出库', H_QC, hint='审核通过后手工例外出库生效并扣减在库；驳回作废。'))
built.append(fpage(M + '/其他出库新建.html', '仓储作业/弹窗/其他出库新建.html', H_QC, '其他出库', '新建其他出库单', '新建其他出库单', W, '其他出库', H_QC, card_title='出库信息'))
built.append(dpage(M + '/库存流水.html', 'stockFlows', 'LJ-A100', H_KC, '库存查询', '库存流水', '库存流水', W, '库存查询', H_KC))
built.append(dpage(M + '/盘点详情.html', 'stocktakes', 'PD-202608-03', H_PD, '盘点记录', '盘点详情', '盘点单详情', W, '盘点记录', H_PD))
built.append(apage(M + '/盘点审核.html', 'stocktakes', 'PD-202608-03', H_PD, '盘点记录', '盘点审核', '盘点审核', W, '盘点记录', H_PD, hint='审核通过后按盘盈盘亏生成调账并锁定盘点头；驳回退回盘点中。'))
built.append(dpage(M + '/调拨详情.html', 'transfers', 'DB-20260901-003', H_DB, '库存调拨', '调拨详情', '调拨单详情', W, '库存调拨', H_DB))
built.append(apage(M + '/调拨审核.html', 'transfers', 'DB-20260901-003', H_DB, '库存调拨', '调拨审核', '调拨审核', W, '库存调拨', H_DB, hint='审核通过后库存按调出/调入库房过账；驳回退回。'))
built.append(fpage(M + '/调拨新建.html', '仓储作业/弹窗/调拨新建.html', H_DB, '库存调拨', '新建调拨单', '新建调拨单', W, '库存调拨', H_DB, card_title='调拨信息'))
print('BUILT B4 %d pages' % len(built))

def rewire_host(path, del_ovs, btn_map, id_map):
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
    if '?audit=1 自动打开审核弹窗' in s:
        i0 = s.index('?audit=1 自动打开审核弹窗')
        a0 = s.rfind('<script', 0, i0)
        j0 = s.index('</script>', i0) + 9
        if any(mid in s[a0:j0] for mid in del_ovs):
            s = s[:a0] + s[j0:]
            print('  %s: audit=1 自动开脚本剪除' % path.split('/')[-1])
    s = re.sub(r"\r?\n[ \t]*modalId: 'detailModal'", '', s)
    s = re.sub(r"\r?\n[ \t]*modalId: 'flowModal'", '', s)
    # 引用已删 overlay 的专属脚本块整删（如 #createModal 内部 radio 绑定）
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

rewire_host('仓储作业/其他入库列表.html', ['createModal', 'auditModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../仓储作业/其他入库新建.html')\""},
    {'detailModal': '../仓储作业/其他入库详情.html', 'auditModal': '../仓储作业/其他入库审核.html'})
rewire_host('仓储作业/其他出库列表.html', ['createModal', 'auditModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../仓储作业/其他出库新建.html')\""},
    {'detailModal': '../仓储作业/其他出库详情.html', 'auditModal': '../仓储作业/其他出库审核.html'})
rewire_host('仓储作业/盘点列表.html', ['auditModal', 'detailModal'], {},
    {'detailModal': '../仓储作业/盘点详情.html', 'auditModal': '../仓储作业/盘点审核.html'})
rewire_host('仓储作业/库存调拨列表.html', ['createModal', 'auditModal', 'detailModal'],
    {"onclick=\"openModal('createModal')\"": "onclick=\"go('../仓储作业/调拨新建.html')\""},
    {'detailModal': '../仓储作业/调拨详情.html', 'auditModal': '../仓储作业/调拨审核.html'})
# 库存查询：flowModal → 库存流水页（其余弹窗保留）
rewire_host('仓储作业/库存查询.html', ['flowModal'], {}, {'flowModal': '../仓储作业/库存流水.html'})

# demo-data ops
s = rd('_data/demo-data.js')
s, nd, na = rew_detail_audit(s, 'otherInbounds', '../仓储作业/其他入库详情.html', '../仓储作业/其他入库审核.html')
print('otherInbounds: detail×%d audit×%d' % (nd, na))
s, nd, na = rew_detail_audit(s, 'otherOutbounds', '../仓储作业/其他出库详情.html', '../仓储作业/其他出库审核.html')
print('otherOutbounds: detail×%d audit×%d' % (nd, na))
s, nd, na = rew_detail_audit(s, 'stocktakes', '../仓储作业/盘点详情.html', '../仓储作业/盘点审核.html')
print('stocktakes: detail×%d audit×%d' % (nd, na))
s, nd, na = rew_detail_audit(s, 'transfers', '../仓储作业/调拨详情.html', '../仓储作业/调拨审核.html')
print('transfers: detail×%d audit×%d' % (nd, na))
s, nd, na = rew_detail_audit(s, 'stockFlows', '../仓储作业/库存流水.html')
print('stockFlows: detail(库存流水)×%d' % nd)
s, n = rew_todo_links(s, {
    '仓储作业/盘点列表.html': '仓储作业/盘点审核.html',
    '仓储作业/其他入库列表.html': '仓储作业/其他入库审核.html',
    '仓储作业/其他出库列表.html': '仓储作业/其他出库审核.html',
    '仓储作业/库存调拨列表.html': '仓储作业/调拨审核.html',
})
print('todoItems links ×%d → B4 审核页' % n)
assert 'id=row' not in s
wr('_data/demo-data.js', s)
t = rd('我的待办.html')
for lst, ap in [('仓储作业/盘点列表.html?audit=1', '../仓储作业/盘点审核.html'),
                ('仓储作业/其他入库列表.html?audit=1', '../仓储作业/其他入库审核.html'),
                ('仓储作业/其他出库列表.html?audit=1', '../仓储作业/其他出库审核.html'),
                ('仓储作业/库存调拨列表.html?audit=1', '../仓储作业/调拨审核.html')]:
    oc = "go('%s')" % lst
    if oc in t:
        t = t.replace(oc, "go('%s')" % ap)
        print('待办静态: %s → %s' % (lst.split('/')[-1], ap.split('/')[-1]))
wr('我的待办.html', t)

# 构建注释清理 + 删模板
for hp in ['仓储作业/其他入库列表.html', '仓储作业/其他出库列表.html', '仓储作业/盘点列表.html', '仓储作业/库存调拨列表.html', '仓储作业/库存查询.html']:
    x = rd(hp)
    for cmt in re.findall(r'<!--[^>]*弹窗/[^>]*-->', x):
        print('注释:', hp.split('/')[-1], '::', cmt[:70])
        x = x.replace(cmt, '<!-- G36 B4：弹窗已页面化 -->')
    wr(hp, x)
names = ['其他入库单详情', '其他入库审核', '其他入库新建', '其他出库单详情', '其他出库审核', '其他出库新建',
         '库存流水', '盘点单详情', '盘点审核', '调拨单详情', '调拨审核', '调拨新建']
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
    fp = os.path.join(ROOT, '仓储作业', '弹窗', n2 + '.html')
    if os.path.exists(fp):
        os.remove(fp)
print('deleted 12 templates ✓')
