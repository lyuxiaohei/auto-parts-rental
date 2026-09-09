# -*- coding: utf-8 -*-
"""G01 角色管理数据驱动化补丁（2026-09-09）
纪律：读取-精确替换+assert 计数；二进制读写保行尾（demo-data.js=LF，角色管理.html=CRLF）；
     禁止裸 open('w') 整页写；roles row.cells 不带外层 td；新增 onclick 自带 DOM 副作用（closeModal 类）。
用法：python _scan_tmpdir/g01_patch.py
"""
import io, json, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DD = r'P3-R01-包装租赁管理后台原型/_data/demo-data.js'      # LF
PAGE = r'P3-R01-包装租赁管理后台原型/系统管理/角色管理.html'  # CRLF
N = '\r\n'

def load(p):
    return open(p, 'rb').read().decode('utf-8')

def save(p, s):
    open(p, 'wb').write(s.encode('utf-8'))

def rep(s, old, new, n, tag):
    c = s.count(old)
    assert c == n, '%s: 匹配 %d != 期望 %d' % (tag, c, n)
    print('  ✓ %-28s 替换 %d 处' % (tag, c))
    return s.replace(old, new)

def conv(t):  # LF 块 -> CRLF（PAGE 用）
    assert '\r' not in t
    return t.replace('\n', N)

# ========== B1 demo-data.js 增 roles 实体 9 条（内容=v3.1 静态 9 行原文） ==========
print('[B1] demo-data.js 增 roles 实体')
ROLES = [
    ('RL-01', '系统管理员', '全部功能 + 系统管理', '全部项目', '2'),
    ('RL-02', '财务', '财务应收/应付/项目损益', '全部项目', '1'),
    ('RL-03', '财务主管', '财务全模块 + 付款/回款确认审核', '全部项目', '1'),
    ('RL-04', '商务', '订单/租赁全流程', '全部项目', '2'),
    ('RL-05', '商务主管', '订单/租赁全流程 + 单据审核', '全部项目', '1'),
    ('RL-06', '物流', '仓储作业 + 库存查询', '全部项目', '1'),
    ('RL-07', '物流主管', '仓储作业 + 库存查询 + 出/入库审核', '全部项目', '1'),
    ('RL-08', '客户账号', '仅查看与下单申请', '所属客户', '7'),
    ('RL-09', '供应商账号', '下发回执与对账', '所属供应商', '3'),
]
dd = load(DD)
assert '\r' not in dd, 'demo-data.js 应为 LF'
blk = ['',
       '  /* --------------------------------------------------------------------------',
       '   * 角色 roles：键 = RL-xx（角色管理页列表驱动，2026-09-09 G01）',
       '   *   fields: name=角色名 desc=说明 scope=数据权限 accts=账号数；cells 不含外层 td',
       '   * ------------------------------------------------------------------------ */',
       '  roles: {']
for k, name, desc, scope, accts in ROLES:
    row = {"fields": {"name": name, "desc": desc, "scope": scope, "accts": accts},
           "keyHtml": "<b>%s</b>" % name,
           "cells": [desc, scope, '<span class="td-num">%s</span>' % accts],
           "ops": [{"t": "权限配置", "act": "openRolePerm('%s')" % name}]}
    blk.append("    '%s': { 'row': %s }," % (k, json.dumps(row, ensure_ascii=False)))
blk[-1] = blk[-1].rstrip(',')
blk.append('  }')
dd = rep(dd, '\n  }\n};', '\n  },' + '\n'.join(blk) + '\n};', 1, 'demo-data 尾插 roles')
save(DD, dd)

# ========== B2-B4 角色管理.html ==========
print('[B2-B4] 系统管理/角色管理.html')
s = load(PAGE)
assert N in s, '角色管理.html 应为 CRLF'
before_div = (s.count('<div'), s.count('</div>'))
before_script = (s.count('<script'), s.count('</script>'))
before_style = (s.count('<style'), s.count('</style>'))

# ---- B2a 筛选区 CSS（产品档案同构，本页原缺） ----
CSS = """/* ===== 筛选区（13px 控件，样板：仓储作业/采购入库列表） ===== */
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
.link-collapse { display:flex; align-items:center; gap:4px; font-size:13px; color:#1677ff; cursor:pointer; background:none; border:none; font-family:inherit; }
.link-collapse svg { width:12px; height:12px; transition:transform .2s; }
.filter-card.collapsed .filter-grid .ff-row-extra { display:none; }
.filter-card:not(.collapsed) .link-collapse svg { transform:rotate(180deg); }
"""
anchor_btn = '/* ===== 按钮（13px 体系，表单/卡片头/弹窗用；筛选区 12px 另按作用域覆盖） ===== */'
s = rep(s, anchor_btn, conv(CSS) + anchor_btn, 1, 'B2a 筛选区 CSS')

# ---- B2b 筛选卡（两字段+查询/重置，content 内 card 前） ----
FILTER = """<div class="filter-card" id="filterCard">
  <div class="filter-grid">
    <div class="ff"><span class="ff-label">角色名称：</span><input placeholder="请输入"></div>
    <div class="ff"><span class="ff-label">数据权限：</span>
      <select><option selected>全部</option><option>全部项目</option><option>所属客户</option><option>所属供应商</option></select>
      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    </div>
    <div class="filter-actions">
      <button class="btn btn-default">重置</button>
      <button class="btn">查询</button>
    </div>
  </div>
</div>
"""
s = rep(s, conv('<div class="content">\n<div class="card">'),
        conv('<div class="content">\n' + FILTER + '<div class="card">'), 1, 'B2b 筛选卡插入')

# ---- B4 新增角色按钮改 createModal（先于 roleModal 整段替换执行，串唯一） ----
s = rep(s, '<div class="head-btns"><button class="btn btn-sm" onclick="openModal(\'roleModal\')">新增角色</button></div>',
        '<div class="head-btns"><button class="btn btn-sm" onclick="openModal(\'createModal\')">新增角色</button></div>',
        1, 'B4 新增角色→createModal')

# ---- B3 roleModal 整段 → 权限配置弹窗 + createModal（切片替换） ----
i1 = s.index('<div class="modal-overlay" id="roleModal">')
i2 = s.index('<style id="detail-modal-css">')
assert i1 < i2
MODALS = """<div class="modal-overlay" id="roleModal">
  <div class="modal modal-lg">
    <div class="modal-header">
      <h3 class="modal-title"><span id="rolePermTitle">权限配置 · 系统管理员</span></h3>
      <span class="modal-close" onclick="closeModal('roleModal')">×</span>
    </div>
    <div class="modal-body">
      <div class="dgrid c3" style="margin-bottom:8px;">
        <div class="drow"><span class="dlabel">角色名</span><span class="dval" id="rpName">系统管理员</span></div>
        <div class="drow"><span class="dlabel">说明</span><span class="dval" id="rpDesc">全部功能 + 系统管理</span></div>
        <div class="drow"><span class="dlabel">账号数</span><span class="dval" id="rpAccts">2</span></div>
      </div>
      <div class="dt-sec">菜单权限</div>
      <div id="permMatrix" style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px 16px;padding:4px 0 2px;">
        <span class="checkbox checked" data-perm="项目管理"><span class="box">✓</span>项目管理</span>
        <span class="checkbox checked" data-perm="我的待办"><span class="box">✓</span>我的待办</span>
        <span class="checkbox checked" data-perm="基础资料"><span class="box">✓</span>基础资料</span>
        <span class="checkbox checked" data-perm="采购管理"><span class="box">✓</span>采购管理</span>
        <span class="checkbox checked" data-perm="销售管理"><span class="box">✓</span>销售管理</span>
        <span class="checkbox checked" data-perm="租赁管理"><span class="box">✓</span>租赁管理</span>
        <span class="checkbox checked" data-perm="仓储管理"><span class="box">✓</span>仓储管理</span>
        <span class="checkbox checked" data-perm="财务管理"><span class="box">✓</span>财务管理</span>
        <span class="checkbox checked" data-perm="系统管理"><span class="box">✓</span>系统管理</span>
      </div>
      <div class="dt-sec">数据权限范围</div>
      <div style="display:flex;padding:4px 0 2px;">
        <span class="radio checked" data-scope="全部项目"><span class="dot"></span>全部项目</span>
        <span class="radio" data-scope="所属客户"><span class="dot"></span>所属客户</span>
        <span class="radio" data-scope="所属供应商"><span class="dot"></span>所属供应商</span>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-default" onclick="closeModal('roleModal')">取消</button>
      <button class="btn" onclick="closeModal('roleModal')">保存</button>
    </div>
  </div>
</div>

<div class="modal-overlay" id="createModal">
  <div class="modal">
    <div class="modal-header">
      <h3 class="modal-title">新增角色</h3>
      <span class="modal-close" onclick="closeModal('createModal')">×</span>
    </div>
    <div class="modal-body">
      <div class="form-row"><span class="form-label"><span class="req">*</span>角色名称</span><div class="input-box"><input placeholder="请输入角色名称"></div></div>
      <div class="form-row"><span class="form-label">说明</span><div class="input-box"><input placeholder="请输入说明"></div></div>
      <div class="form-row"><span class="form-label">数据权限范围</span><div class="input-box select-box"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>全部项目</option><option>所属客户</option><option>所属供应商</option></select><span class="caret">▾</span></div></div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-default" onclick="closeModal('createModal')">取消</button>
      <button class="btn" onclick="closeModal('createModal')">保存</button>
    </div>
  </div>
</div>

"""
s = s[:i1] + conv(MODALS) + s[i2:]
print('  ✓ %-28s 切片替换 1 段' % 'B3 roleModal→权限配置+createModal')

# ---- B2c tbody 静态兜底行 9 条 onclick → openRolePerm（整行锚，逐条 count=1） ----
for k, name, desc, scope, accts in ROLES:
    old_row = '<td><b>%s</b></td><td>%s</td><td>%s</td><td><span class="td-num">%s</span></td><td class="sticky-op"><span class="ops"><a onclick="openModal(\'roleModal\')">权限配置</a></span></td>' % (name, desc, scope, accts)
    new_row = '<td><b>%s</b></td><td>%s</td><td>%s</td><td><span class="td-num">%s</span></td><td class="sticky-op"><span class="ops"><a onclick="openRolePerm(\'%s\')">权限配置</a></span></td>' % (name, desc, scope, accts, name)
    s = rep(s, old_row, new_row, 1, 'B2c 兜底行 %s' % name)

# ---- B2d 三 script 引入 + 页面级 ROLE_PERM/openRolePerm + renderListPage ----
WIRE = """<script src="../_data/demo-data.js"></script>
<script src="../_data/list-generic.js"></script>
<script>
/* G01 角色管理数据驱动（2026-09-09）：roles 实体渲染 + 权限配置矩阵（矩阵口径=G01 文档 C 默认决策表） */
window.ROLE_PERM = {
  '系统管理员': { desc:'全部功能 + 系统管理', accts:'2', scope:'全部项目', perms:['项目管理','我的待办','基础资料','采购管理','销售管理','租赁管理','仓储管理','财务管理','系统管理'] },
  '财务': { desc:'财务应收/应付/项目损益', accts:'1', scope:'全部项目', perms:['我的待办','财务管理'] },
  '财务主管': { desc:'财务全模块 + 付款/回款确认审核', accts:'1', scope:'全部项目', perms:['我的待办','财务管理'] },
  '商务': { desc:'订单/租赁全流程', accts:'2', scope:'全部项目', perms:['我的待办','基础资料','采购管理','销售管理','租赁管理'] },
  '商务主管': { desc:'订单/租赁全流程 + 单据审核', accts:'1', scope:'全部项目', perms:['我的待办','基础资料','采购管理','销售管理','租赁管理'] },
  '物流': { desc:'仓储作业 + 库存查询', accts:'1', scope:'全部项目', perms:['我的待办','仓储管理'] },
  '物流主管': { desc:'仓储作业 + 库存查询 + 出/入库审核', accts:'1', scope:'全部项目', perms:['我的待办','仓储管理'] },
  '客户账号': { desc:'仅查看与下单申请', accts:'7', scope:'所属客户', perms:['我的待办'] },
  '供应商账号': { desc:'下发回执与对账', accts:'3', scope:'所属供应商', perms:['我的待办'] }
};
function openRolePerm(name) {
  var p = window.ROLE_PERM[name] || { desc:'', accts:'', scope:'全部项目', perms:[] };
  document.getElementById('rolePermTitle').textContent = '权限配置 · ' + name;
  document.getElementById('rpName').textContent = name;
  document.getElementById('rpDesc').textContent = p.desc;
  document.getElementById('rpAccts').textContent = p.accts;
  document.querySelectorAll('#roleModal .checkbox').forEach(function (c) {
    c.classList.toggle('checked', p.perms.indexOf(c.getAttribute('data-perm')) > -1);
  });
  document.querySelectorAll('#roleModal .radio').forEach(function (r) {
    r.classList.toggle('checked', r.getAttribute('data-scope') === p.scope);
  });
  openModal('roleModal');
}
renderListPage({
  entity: 'roles',
  noCheckbox: true,
  filters: [
    { label: '角色名称', field: 'name' },
    { label: '数据权限', field: 'scope' }
  ]
});
</script>
"""
anchor_js = "<script>" + N + "function openModal(id) { document.getElementById(id).classList.add('show'); }"
s = rep(s, anchor_js, conv(WIRE) + anchor_js, 1, 'B2d script 引入+页面 JS')

# ---- 标签配平自检（改前差值 == 改后差值） ----
after_div = (s.count('<div'), s.count('</div>'))
after_script = (s.count('<script'), s.count('</script>'))
after_style = (s.count('<style'), s.count('</style>'))
assert after_div[0] - before_div[0] == after_div[1] - before_div[1], 'div 不配平 %s -> %s' % (before_div, after_div)
assert after_script[0] - before_script[0] == after_script[1] - before_script[1], 'script 不配平'
assert after_style[0] == before_style[0] and after_style[1] == before_style[1], 'style 数不应变'
print('  ✓ 标签配平自检通过 div %+d/%+d script %+d/%+d' % (
    after_div[0] - before_div[0], after_div[1] - before_div[1],
    after_script[0] - before_script[0], after_script[1] - before_script[1]))
save(PAGE, s)
print('G01 补丁完成')
