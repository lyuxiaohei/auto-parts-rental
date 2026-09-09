# -*- coding: utf-8 -*-
"""批1 Stage4：全站侧边栏重写为菜单终版五块结构（40 业务页 + BOM.html 含内）
规范块整体替换 <aside class="sidebar">...</aside>，保留每页 selected/open 态；二进制读写保行尾。
"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"

ARROW = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>'
def ico(inner):
    return '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + inner + '</svg>'

I_HOME = ico('<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>')
I_TODO = ico('<polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>')
I_FOLDER = ico('<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>')
I_DB = ico('<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>')
I_CART = ico('<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>')
I_TAG = ico('<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>')
I_BOX = ico('<polyline points="21 8 21 21 3 21 3 8"/><rect x="1" y="3" width="22" height="5" rx="1"/><line x1="10" y1="12" x2="14" y2="12"/>')
I_WH = ico('<polyline points="21 8 21 21 3 21 3 8"/><rect x="1" y="3" width="22" height="5"/><line x1="10" y1="12" x2="14" y2="12"/>')
I_AR = ico('<polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>')
I_AP = ico('<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>')
I_PL = ico('<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>')
I_SET = ico('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h.01a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51h.01a1.65 1.65 0 0 0 1.82.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82v.01a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>')

# 页 → (selected 标签, open 组名)；None=无选中（维持原状：项目管理/项目详情/盈亏报表）
PAGE_STATE = {
    '首页/项目看板.html': ('项目看板', None),
    '我的待办.html': ('我的待办', None),
    '项目管理/项目档案.html': (None, None),
    '项目管理/项目详情.html': (None, None),
    '基础数据/客商管理.html': ('客商管理', '基础资料'),
    '基础数据/器具档案.html': ('器具档案', '基础资料'),
    '基础数据/零部件档案.html': ('零部件档案', '基础资料'),
    '基础数据/BOM.html': ('BOM', '基础资料'),
    '基础数据/BOM维护.html': ('BOM', '基础资料'),
    '基础数据/库位档案.html': ('库位档案', '基础资料'),
    '采购管理/采购订单列表.html': ('采购订单', '采购管理'),
    '采购管理/采购入库列表.html': ('采购入库', '采购管理'),
    '采购管理/采购入库录单.html': ('采购入库', '采购管理'),
    '销售管理/销售订单列表.html': ('销售订单', '销售管理'),
    '销售管理/销售出库列表.html': ('销售出库', '销售管理'),
    '租赁管理/租赁单列表.html': ('租赁单', '租赁管理'),
    '租赁管理/租入单列表.html': ('租入单', '租赁管理'),
    '租赁管理/租入入库列表.html': ('租入入库', '租赁管理'),
    '租赁管理/组合出库列表.html': ('组合出库', '租赁管理'),
    '租赁管理/组合出库录单.html': ('组合出库', '租赁管理'),
    '租赁管理/退租入库列表.html': ('退租入库', '租赁管理'),
    '租赁管理/租入归还列表.html': ('租入归还', '租赁管理'),
    '租赁管理/在租台账.html': ('在租台账', '租赁管理'),
    '租赁管理/租出台账.html': ('租出台账', '租赁管理'),
    '仓储作业/库存查询.html': ('库存查询', '仓储作业'),
    '仓储作业/盘点列表.html': ('盘点', '仓储作业'),
    '仓储作业/盘点录入.html': ('盘点录入', '仓储作业'),
    '仓储作业/库存调拨列表.html': ('库存调拨', '仓储作业'),
    '仓储作业/其他入库列表.html': ('其他入库', '仓储作业'),
    '仓储作业/其他出库列表.html': ('其他出库', '仓储作业'),
    '财务协同/应收账单.html': ('应收账单', '财务应收'),
    '财务协同/开票登记.html': ('开票登记', '财务应收'),
    '财务协同/回款登记.html': ('收款登记', '财务应收'),
    '财务协同/银行水单核销.html': ('收款核销', '财务应收'),
    '财务协同/应付账单.html': ('应付账单', '财务应付'),
    '财务协同/付款登记.html': ('付款登记', '财务应付'),
    '财务协同/盈亏报表.html': (None, None),
    '系统管理/用户权限.html': ('用户权限', '系统管理'),
    '系统管理/操作日志.html': ('操作日志', '系统管理'),
    '系统管理/数据字典.html': ('数据字典', '系统管理'),
}

def build(P, sel, open_grp, nl):
    def item(label, target=None):
        if target is None:
            return f'<li><div class="sm-link">{label}</div></li>'
        if label == sel:
            return f'<li><div class="sm-link selected">{label}</div></li>'
        return f'<li><div class="sm-link" onclick="go(\'{P}{target}\')">{label}</div></li>'
    def single(label, ico_svg, target):
        cls = ' selected' if label == sel else ''
        inner = f'<span class="sm-ico">{ico_svg}</span>{label}'
        if cls:
            return f'      <li class="sm-item"><div class="sm-link{cls}">{inner}</div></li>'
        return f'      <li class="sm-item"><div class="sm-link" onclick="go(\'{P}{target}\')">{inner}</div></li>'
    def group(name, ico_svg, items):
        cls = 'sm-item has-sub open' if name == open_grp else 'sm-item has-sub'
        lines = [
            f'      <li class="{cls}">',
            f'   <div class="sm-link"><span class="sm-ico">{ico_svg}</span>{name}<span class="sm-arrow">{ARROW}</span></div>',
            '   <ul class="sm-sub">',
        ]
        for lb, tg in items:
            lines.append('   ' + item(lb, tg))
        lines.append('   </ul>')
        lines.append('      </li>')
        return lines

    L = []
    L.append('<aside class="sidebar">')
    L.append('  <ul class="side-menu">')
    L.append(single('项目看板', I_HOME, '首页/项目看板.html').strip())
    L.append(single('我的待办', I_TODO, '我的待办.html').strip())
    L.append(single('项目管理', I_FOLDER, '项目管理/项目档案.html').strip())
    L += group('基础资料', I_DB, [
        ('客商管理', '基础数据/客商管理.html'),
        ('器具档案', '基础数据/器具档案.html'),
        ('零部件档案', '基础数据/零部件档案.html'),
        ('BOM', '基础数据/BOM.html'),
        ('库位档案', '基础数据/库位档案.html'),
    ])
    L += group('采购管理', I_CART, [
        ('采购订单', '采购管理/采购订单列表.html'),
        ('采购入库', '采购管理/采购入库列表.html'),
    ])
    L += group('销售管理', I_TAG, [
        ('销售订单', '销售管理/销售订单列表.html'),
        ('销售出库', '销售管理/销售出库列表.html'),
    ])
    L += group('租赁管理', I_BOX, [
        ('租赁单', '租赁管理/租赁单列表.html'),
        ('租入单', '租赁管理/租入单列表.html'),
        ('租入入库', '租赁管理/租入入库列表.html'),
        ('组合出库', '租赁管理/组合出库列表.html'),
        ('退租入库', '租赁管理/退租入库列表.html'),
        ('租入归还', '租赁管理/租入归还列表.html'),
        ('在租台账', '租赁管理/在租台账.html'),
        ('租出台账', '租赁管理/租出台账.html'),
    ])
    L += group('仓储作业', I_WH, [
        ('库存查询', '仓储作业/库存查询.html'),
        ('盘点', '仓储作业/盘点列表.html'),
        ('盘点录入', '仓储作业/盘点录入.html'),
        ('库存调拨', '仓储作业/库存调拨列表.html'),
        ('其他入库', '仓储作业/其他入库列表.html'),
        ('其他出库', '仓储作业/其他出库列表.html'),
    ])
    L += group('财务应收', I_AR, [
        ('应收账单', '财务协同/应收账单.html'),
        ('开票登记', '财务协同/开票登记.html'),
        ('收款登记', '财务协同/回款登记.html'),
        ('收款核销', '财务协同/银行水单核销.html'),
    ])
    L += group('财务应付', I_AP, [
        ('应付账单', '财务协同/应付账单.html'),
        ('付款登记', '财务协同/付款登记.html'),
    ])
    L.append(single('项目损益', I_PL, '财务协同/盈亏报表.html').strip())
    L += group('系统管理', I_SET, [
        ('用户权限', '系统管理/用户权限.html'),
        ('操作日志', '系统管理/操作日志.html'),
        ('数据字典', '系统管理/数据字典.html'),
    ])
    L.append('  </ul> <div class="side-foot">')
    L.append('    <div class="sys-cur">')
    L.append('      <span class="sys-badge">租</span>')
    L.append('      <span class="sys-name">包装租赁管理后台</span>')
    L.append('    </div>')
    L.append('  </div></aside>')
    return nl.join(L)

rx = re.compile(r'<aside class="sidebar">.*?</aside>', re.S)
changed, skipped = [], []
for rel, (sel, og) in PAGE_STATE.items():
    f = PROTO / rel
    assert f.exists(), f'页面不存在: {rel}'
    raw = f.read_bytes()
    txt = raw.decode('utf-8')
    nl = '\r\n' if '\r\n' in txt else '\n'
    matches = rx.findall(txt)
    assert len(matches) == 1, f'{rel}: aside 匹配 {len(matches)} 处（应为 1）'
    P = '' if rel == '我的待办.html' else '../'
    new_aside = build(P, sel, og, nl)
    txt2 = rx.sub(lambda m: new_aside, txt, count=1)
    f.write_bytes(txt2.encode('utf-8'))
    changed.append(rel)

print(f'侧边栏重写 {len(changed)} 页')
for c in changed:
    print('  ✓', c)

# 校验：改后每页 selected 恰 1 处、菜单项各恰 1 次
labels = ['项目看板','我的待办','项目管理','客商管理','器具档案','零部件档案','BOM','库位档案',
          '采购订单','采购入库','销售订单','销售出库','租赁单','租入单','租入入库','组合出库','退租入库','租入归还','在租台账','租出台账',
          '库存查询','盘点','盘点录入','库存调拨','其他入库','其他出库',
          '应收账单','开票登记','收款登记','收款核销','应付账单','付款登记','项目损益','用户权限','操作日志','数据字典']
for rel in changed:
    txt = (PROTO / rel).read_bytes().decode('utf-8')
    aside = rx.search(txt).group(0)
    n_sel = aside.count('sm-link selected')
    assert n_sel <= 1, f'{rel}: selected {n_sel} 处'
    for lb in labels:
        n = aside.count(f'>{lb}</div>')
        assert n <= 1, f'{rel}: 菜单项 {lb} 出现 {n} 次'
    # 旧菜单残留检查
    for old in ['组装</div>', '拆卸管理</div>', '退租申请</div>', '丢损赔偿单</div>', '包装管理', '租赁出库</div>', '库存盘点</div>']:
        assert old not in aside, f'{rel}: 旧菜单残留 {old}'
print('PASS: selected≤1、菜单项≤1、无旧菜单残留（40 页）')
