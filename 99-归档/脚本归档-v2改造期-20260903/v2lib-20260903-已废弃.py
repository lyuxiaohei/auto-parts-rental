# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃（v2工具链公共库，随工具链归档）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""v2 原型改造共享库：菜单定义 / 侧边栏生成 / 术语替换 / 路径重映射"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTO = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型')

ARROW = '<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>'

def icon(body):
    return ('<span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            + body + '</svg></span>')

ICONS = {
    'home':  '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    'folder':'<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
    'db':    '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
    'cart':  '<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>',
    'tag':   '<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>',
    'box':   '<polyline points="21 8 21 21 3 21 3 8"/><rect x="1" y="3" width="22" height="5"/><line x1="10" y1="12" x2="14" y2="12"/>',
    'repeat':'<polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
    'file':  '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    'moneyin': '<circle cx="12" cy="12" r="10"/><polyline points="8 12 12 16 16 12"/><line x1="12" y1="8" x2="12" y2="16"/>',
    'moneyout':'<circle cx="12" cy="12" r="10"/><polyline points="16 12 12 8 8 12"/><line x1="12" y1="16" x2="12" y2="8"/>',
    'chart': '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>',
    'gear':  '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h.01a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51h.01a1.65 1.65 0 0 0 1.82.33l.06-.06a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1.51h.01a1.65 1.65 0 0 0 1.82.33l.06.06a1.65 1.65 0 0 0 .33 1.82v.01a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
}

GROUP_LABEL_STYLE = 'padding:6px 24px 2px 48px;font-size:12px;color:#8c8c8c;cursor:default;user-select:none;'

# v2 完整菜单树（第四节终版）。叶子: (菜单名, 目标路径)；None 表示分组标签
MENU = [
    ('top', '首页', 'home', '../首页/项目看板.html'),
    ('top', '项目管理', 'folder', '../项目管理/项目档案.html'),
    ('group', '基础资料', 'db', [
        ('客商管理', '../基础数据/客商管理.html'),
        ('器具档案', '../基础数据/器具档案.html'),
        ('零部件档案', '../基础数据/零部件档案.html'),
        ('BOM', '../基础数据/BOM.html'),
        ('库位档案', '../基础数据/库位档案.html'),
    ]),
    ('group', '采购管理', 'cart', [
        ('采购订单', '../采购管理/采购订单列表.html'),
    ]),
    ('group', '销售管理', 'tag', [
        ('销售订单', '../销售管理/销售订单列表.html'),
    ]),
    ('group', '仓储作业', 'box', [
        ('__label__', '入库类'),
        ('采购入库', '../仓储作业/采购入库列表.html'),
        ('退租入库', '../仓储作业/退租入库列表.html'),
        ('其他入库', '../仓储作业/其他入库列表.html'),
        ('__label__', '出库类'),
        ('销售出库', '../仓储作业/销售出库列表.html'),
        ('组合出库', '../仓储作业/组合出库列表.html'),
        ('其他出库', '../仓储作业/其他出库列表.html'),
        ('__label__', '组装拆卸'),
        ('组装', '../仓储作业/组装列表.html'),
        ('拆卸管理', '../仓储作业/拆卸管理列表.html'),
        ('__label__', '库存管理'),
        ('库存盘点', '../仓储作业/盘点列表.html'),
        ('库存查询', '../仓储作业/库存查询.html'),
        ('库存调拨', '../仓储作业/库存调拨列表.html'),
    ]),
    ('group', '包装管理', 'repeat', [
        ('租赁单', '../包装管理/租赁单列表.html'),
        ('退租申请', '../包装管理/退租申请列表.html'),
        ('在租台账', '../包装管理/在租台账.html'),
        ('丢损赔偿单', '../包装管理/丢损赔偿单.html'),
    ]),
    ('group', '订单管理', 'file', [
        ('订单审核', '../订单协同/客户订单.html'),
        ('订单同步', '../订单协同/路凯下发.html'),
        ('对账结算', '../订单协同/结算导出.html'),
    ]),
    ('group', '财务应收', 'moneyin', [
        ('应收账单', '../财务协同/应收账单.html'),
        ('开票登记', '../财务协同/开票登记.html'),
        ('收款登记', '../财务协同/回款登记.html'),
        ('收款核销', '../财务协同/银行水单核销.html'),
    ]),
    ('group', '财务应付', 'moneyout', [
        ('应付账单', '../财务协同/应付账单.html'),
        ('付款登记', '../财务协同/付款登记.html'),
    ]),
    ('top', '项目损益', 'chart', '../财务协同/盈亏报表.html'),
    ('group', '系统管理', 'gear', [
        ('用户权限', '../系统管理/用户权限.html'),
        ('操作日志', '../系统管理/操作日志.html'),
        ('数据字典', '../系统管理/数据字典.html'),
    ]),
]

def render_sidebar(selected):
    """selected: 当前页面对应的菜单项文本（顶级或叶子）。生成整个 <aside> 块。"""
    out = ['<aside class="sidebar">', '  <ul class="side-menu">']
    for item in MENU:
        if item[0] == 'top':
            _, name, ico, url = item
            if name == selected:
                out.append(f'   <li class="sm-item"><div class="sm-link selected">{icon(ICONS[ico])}{name}</div></li>')
            else:
                out.append(f'   <li class="sm-item"><div class="sm-link" onclick="go(\'{url}\')">{icon(ICONS[ico])}{name}</div></li>')
        else:
            _, name, ico, children = item
            leaf_names = [c[0] for c in children if c[0] != '__label__']
            is_open = selected in leaf_names
            out.append(f'   <li class="sm-item has-sub{" open" if is_open else ""}">')
            out.append(f'   <div class="sm-link">{icon(ICONS[ico])}{name}{ARROW}</div>')
            out.append('   <ul class="sm-sub">')
            for c in children:
                if c[0] == '__label__':
                    out.append(f'   <li><div style="{GROUP_LABEL_STYLE}">{c[1]}</div></li>')
                    continue
                lname, url = c
                if lname == selected:
                    out.append(f'   <li><div class="sm-link selected">{lname}</div></li>')
                else:
                    out.append(f'   <li><div class="sm-link" onclick="go(\'{url}\')">{lname}</div></li>')
            out.append('   </ul>')
            out.append('   </li>')
    out.append('  </ul>')
    out.append('  <div class="side-foot">')
    out.append('    <div class="sys-cur">')
    out.append('      <span class="sys-badge">租</span>')
    out.append('      <span class="sys-name">包装租赁管理后台</span>')
    out.append('    </div>')
    out.append('  </div></aside>')
    return '\n'.join(out)

# ===== go() 路径重映射（文件改名/删除后） =====
PATH_REMAP = {
    '../基础数据/往来单位.html': '../基础数据/客商管理.html',
    '../基础数据/包材档案.html': '../基础数据/器具档案.html',
    '../基础数据/子母件BOM.html': '../基础数据/BOM.html',
    '../仓储作业/小组装列表.html': '../仓储作业/组装列表.html',
    '../仓储作业/小组装录单.html': '../仓储作业/组装录单.html',
    '../仓储作业/退租验收列表.html': '../仓储作业/退租入库列表.html',
    '../仓储作业/退租验收录单.html': '../包装管理/退租申请列表.html',
    '../租赁管理/在租资产跟踪.html': '../包装管理/在租台账.html',
    '../租赁管理/缺损赔偿.html': '../包装管理/丢损赔偿单.html',
    '../租赁管理/租出台账.html': '../包装管理/租出台账.html',
}

# ===== 可见文本术语替换（按序执行；go()/href 属性值会被预先保护） =====
TEXT_REPL = [
    ('子母件BOM', 'BOM'),
    ('子母件', 'BOM'),
    ('母件', '父项'),
    ('子件', '子项'),
    ('小组装', '组装'),
    ('包材档案', '器具档案'),
    ('包材', '器具'),
    ('企业管理', '客商管理'),
    ('往来单位', '客商管理'),
    ('拆散', '拆卸'),
    ('在租资产跟踪', '在租台账'),
    ('订单协同', '订单管理'),
    ('基础数据', '基础资料'),
    ('缺损赔偿', '丢损赔偿单'),
    ('退租验收', '退租入库'),
    ('银行水单核销', '收款核销'),
    ('银行水单', '银行回单'),
    ('回款登记', '收款登记'),
    ('回款', '收款'),
    ('项目盈亏报表', '项目损益'),
    ('盈亏报表', '损益报表'),
    ('缺损与赔偿记录', '丢损赔偿单'),
]

PROTECT_RE = re.compile(r'''(?:go\(\s*['"][^'"]*['"]\s*\)|href="[^"]*"|src="[^"]*")''')

def protect_attrs(html):
    stash = []
    def _keep(m):
        stash.append(m.group(0))
        return f'\x00{len(stash)-1}\x00'
    return PROTECT_RE.sub(_keep, html), stash

def restore_attrs(html, stash):
    def _back(m):
        return stash[int(m.group(1))]
    return re.sub('\x00(\\d+)\x00', _back, html)

def apply_path_remap(html):
    for old, new in PATH_REMAP.items():
        html = html.replace(old, new)
    return html

def apply_text_repl(html):
    """仅对可见文本做术语替换，保护 go()/href/src 属性值"""
    protected, stash = protect_attrs(html)
    for old, new in TEXT_REPL:
        protected = protected.replace(old, new)
    # 租赁管理 -> 包装管理，但不破坏产品名「包装租赁管理后台」
    protected = re.sub('(?<!包装)租赁管理', '包装管理', protected)
    return restore_attrs(protected, stash)

def strip_sys_switch(html):
    """删除系统切换器：CSS 块、JS 块（side-foot 由侧边栏重生成覆盖）"""
    # CSS：从 /* sys-switch */ 到 </style> 前
    html = re.sub(r'\n?/\* sys-switch \*/.*?\n(?=</style>)', '\n', html, flags=re.S)
    # JS：<script>/* sys-switch */ ... </script>
    html = re.sub(r'\n?<script>/\* sys-switch \*/.*?</script>\n?', '\n', html, flags=re.S)
    return html

def rebuild_sidebar(html, selected):
    new = render_sidebar(selected)
    out, n = re.subn(r'<aside class="sidebar">.*?</aside>', lambda m: new, html, flags=re.S)
    if n != 1:
        raise RuntimeError(f'侧边栏替换次数异常: {n}')
    return out

def read_page(rel):
    p = os.path.join(PROTO, rel)
    with open(p, encoding='utf-8') as f:
        return f.read()

def write_page(rel, html):
    p = os.path.join(PROTO, rel)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
