# -*- coding: utf-8 -*-
"""菜单重组 v3.1 · 全站侧边栏重写（39 现存页 + 新建角色管理页 = 40 页）
A 表组序：项目管理组居首(看板/项目列表/损益)·我的待办一级·基础资料·采购·销售·
租赁三分标签(租赁/租入/退租·菜单名"租赁出库"文件仍组合出库列表.html)·
仓储三分标签(库存管理/入库类/出库类·盘点录入退出菜单)·
财务协同两标签(应收/应付)·系统管理(用户权限/角色管理/操作日志/数据字典)。
规范块整体替换 <aside class="sidebar">...</aside>；小标签样式=旧仓储 li 原文；二进制读写保行尾。
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
I_SET = ico('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h.01a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51h.01a1.65 1.65 0 0 0 1.82.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82v.01a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>')

# 页 → (selected 标签, open 组名)；None=无选中（项目详情落地页）
PAGE_STATE = {
    '首页/项目看板.html': ('项目看板', '项目管理'),
    '我的待办.html': ('我的待办', None),
    '项目管理/项目档案.html': ('项目列表', '项目管理'),
    '项目管理/项目详情.html': (None, None),
    '基础数据/客商管理.html': ('客商管理', '基础资料'),
    '基础数据/产品档案.html': ('产品档案', '基础资料'),
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
    '租赁管理/组合出库列表.html': ('租赁出库', '租赁管理'),
    '租赁管理/组合出库录单.html': ('租赁出库', '租赁管理'),
    '租赁管理/退租入库列表.html': ('退租入库', '租赁管理'),
    '租赁管理/租入归还列表.html': ('租入归还', '租赁管理'),
    '租赁管理/在租台账.html': ('在租台账', '租赁管理'),
    '租赁管理/租出台账.html': ('租出台账', '租赁管理'),
    '仓储作业/库存查询.html': ('库存查询', '仓储作业'),
    '仓储作业/盘点列表.html': ('盘点', '仓储作业'),
    '仓储作业/盘点录入.html': ('盘点', '仓储作业'),
    '仓储作业/库存调拨列表.html': ('库存调拨', '仓储作业'),
    '仓储作业/其他入库列表.html': ('其他入库', '仓储作业'),
    '仓储作业/其他出库列表.html': ('其他出库', '仓储作业'),
    '财务协同/应收账单.html': ('应收账单', '财务协同'),
    '财务协同/开票登记.html': ('开票登记', '财务协同'),
    '财务协同/回款登记.html': ('收款登记', '财务协同'),
    '财务协同/银行水单核销.html': ('收款核销', '财务协同'),
    '财务协同/应付账单.html': ('应付账单', '财务协同'),
    '财务协同/付款登记.html': ('付款登记', '财务协同'),
    '财务协同/盈亏报表.html': ('损益', '项目管理'),
    '系统管理/用户权限.html': ('用户权限', '系统管理'),
    '系统管理/角色管理.html': ('角色管理', '系统管理'),
    '系统管理/操作日志.html': ('操作日志', '系统管理'),
    '系统管理/数据字典.html': ('数据字典', '系统管理'),
}

TAG_LI = '<li style="padding:4px 0 2px 48px;font-size:10px;color:#8c8c8c;letter-spacing:.08em;user-select:none;list-style:none">{}</li>'

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
        for it in items:
            if it[0] == '#':
                lines.append('   ' + TAG_LI.format(it[1]))
            else:
                lines.append('   ' + item(it[0], it[1]))
        lines.append('   </ul>')
        lines.append('      </li>')
        return lines

    L = []
    L.append('<aside class="sidebar">')
    L.append('  <ul class="side-menu">')
    L += group('项目管理', I_FOLDER, [
        ('项目看板', '首页/项目看板.html'),
        ('项目列表', '项目管理/项目档案.html'),
        ('损益', '财务协同/盈亏报表.html'),
    ])
    L.append(single('我的待办', I_TODO, '我的待办.html').strip())
    L += group('基础资料', I_DB, [
        ('客商管理', '基础数据/客商管理.html'),
        ('产品档案', '基础数据/产品档案.html'),
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
        ('#', '租赁'),
        ('租赁单', '租赁管理/租赁单列表.html'),
        ('租赁出库', '租赁管理/组合出库列表.html'),
        ('在租台账', '租赁管理/在租台账.html'),
        ('租出台账', '租赁管理/租出台账.html'),
        ('#', '租入'),
        ('租入单', '租赁管理/租入单列表.html'),
        ('租入入库', '租赁管理/租入入库列表.html'),
        ('租入归还', '租赁管理/租入归还列表.html'),
        ('#', '退租'),
        ('退租入库', '租赁管理/退租入库列表.html'),
    ])
    L += group('仓储作业', I_WH, [
        ('#', '库存管理'),
        ('库存查询', '仓储作业/库存查询.html'),
        ('盘点', '仓储作业/盘点列表.html'),
        ('库存调拨', '仓储作业/库存调拨列表.html'),
        ('#', '入库类'),
        ('其他入库', '仓储作业/其他入库列表.html'),
        ('#', '出库类'),
        ('其他出库', '仓储作业/其他出库列表.html'),
    ])
    L += group('财务协同', I_AR, [
        ('#', '应收'),
        ('应收账单', '财务协同/应收账单.html'),
        ('开票登记', '财务协同/开票登记.html'),
        ('收款登记', '财务协同/回款登记.html'),
        ('收款核销', '财务协同/银行水单核销.html'),
        ('#', '应付'),
        ('应付账单', '财务协同/应付账单.html'),
        ('付款登记', '财务协同/付款登记.html'),
    ])
    L += group('系统管理', I_SET, [
        ('用户权限', '系统管理/用户权限.html'),
        ('角色管理', '系统管理/角色管理.html'),
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

# ---- 目标态菜单标签序列（结构自检基准） ----
EXPECT_SEQ = ['项目管理', '项目看板', '项目列表', '损益', '我的待办', '基础资料', '客商管理', '产品档案', 'BOM', '库位档案',
              '采购管理', '采购订单', '采购入库', '销售管理', '销售订单', '销售出库',
              '租赁管理', '租赁', '租赁单', '租赁出库', '在租台账', '租出台账', '租入', '租入单', '租入入库', '租入归还', '退租', '退租入库',
              '仓储作业', '库存管理', '库存查询', '盘点', '库存调拨', '入库类', '其他入库', '出库类', '其他出库',
              '财务协同', '应收', '应收账单', '开票登记', '收款登记', '收款核销', '应付', '应付账单', '付款登记',
              '系统管理', '用户权限', '角色管理', '操作日志', '数据字典']
LABELS = [x for x in EXPECT_SEQ if x not in ('租赁', '租入', '退租', '库存管理', '入库类', '出库类', '应收', '应付')]
GROUPS = ['项目管理', '我的待办', '基础资料', '采购管理', '销售管理', '租赁管理', '仓储作业', '财务协同', '系统管理']

rx = re.compile(r'<aside class="sidebar">.*?</aside>', re.S)
changed = []
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
    # 结构自检（每页构建产物一致，逐页过一遍）
    got_seq = [a or b for a, b in [(m.group(1), m.group(2)) for m in re.finditer(
        r'<div class="sm-link[^>]*>(?:<span class="sm-ico">.*?</span>)?([^<>]+)(?:<span class="sm-arrow">|</div>)|list-style:none">([^<>]+)</li>',
        new_aside)]]
    assert got_seq == EXPECT_SEQ, f'{rel}: 菜单序列不符\n 获{"→".join(got_seq)}'
    txt2 = rx.sub(lambda m: new_aside, txt, count=1)
    f.write_bytes(txt2.encode('utf-8'))
    changed.append(rel)

print(f'侧边栏重写 {len(changed)} 页')

# ---- 改后逐页断言 ----
for rel in changed:
    raw = (PROTO / rel).read_bytes()
    txt = raw.decode('utf-8')
    nl2 = '\r\n' if '\r\n' in txt else '\n'
    aside = rx.search(txt).group(0)
    n_sel = aside.count('sm-link selected')
    assert n_sel <= 1, f'{rel}: selected {n_sel} 处'
    for lb in LABELS + GROUPS:
        n = aside.count(f'>{lb}</div>')
        assert n <= 1, f'{rel}: 菜单项/组 {lb} 出现 {n} 次'
    for old in ['财务应收', '财务应付', '项目损益', '>组合出库</div>', '>盘点录入</div>', '包装管理', '器具档案', '零部件档案']:
        assert old not in aside, f'{rel}: 旧菜单残留 {old}'
    # 项目看板不得为一级单页形态（须在项目管理组内）
    for line in aside.split(nl2):
        if '>项目看板</div>' in line:
            assert line.lstrip().startswith('<li><div class="sm-link'), f'{rel}: 项目看板为一级形态: {line[:80]}'
    # 小标签恰 8 个（租赁/租入/退租/库存管理/入库类/出库类/应收/应付）
    n_tag = aside.count('list-style:none')
    assert n_tag == 8, f'{rel}: 小标签 {n_tag} 个（应为 8）'
print(f'PASS: selected≤1、菜单项/组各≤1、无旧组名与错菜单形态、小标签×8（{len(changed)} 页）')
