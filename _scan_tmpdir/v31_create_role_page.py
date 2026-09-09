# -*- coding: utf-8 -*-
"""菜单重组 v3.1 · 新建 系统管理/角色管理.html
壳=系统管理/数据字典.html；主体=用户权限.html roleModal 九角色表格升为列表卡片；
携带 roleModal（照抄）+ 新增角色按钮 + ia-fix 块（随壳自带）；静态页不接 renderListPage。
侧边栏随后由 v31_sidebar.py 统一重写（selected=角色管理/open=系统管理）。
"""
import io, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROTO = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
shell = (PROTO / '系统管理/数据字典.html').read_bytes().decode('utf-8')
uq = (PROTO / '系统管理/用户权限.html').read_bytes().decode('utf-8')

# ---- 提取 roleModal 原文（照抄） ----
r0 = uq.find('<div class="modal-overlay" id="roleModal">')
r1 = uq.find('<style id="proto-notes-style">', r0)
assert r0 > -1 and r1 > r0, 'roleModal 定位失败'
role_modal = uq[r0:r1].rstrip('\r\n \t')
assert role_modal.count('modal-overlay') == 1 and '供应商账号' in role_modal
assert role_modal.rstrip().endswith('</div>'), 'roleModal 收口异常'

t = shell

def rep(old, new, cnt=1):
    global t
    n = t.count(old)
    assert n == cnt, f'锚点计数 {n}≠{cnt}: {old[:60]!r}'
    t = t.replace(old, new)

# 1 标题
rep('<title>数据字典 - 包装租赁管理后台</title>', '<title>角色管理 - 包装租赁管理后台</title>')

# 2 顶部页签（角色管理 active，兄弟页 用户权限/数据字典）
rep('<span class="tab active">数据字典 <span class="close">×</span></span>',
    '<span class="tab active">角色管理 <span class="close">×</span></span>')
rep('<span class="tab">操作日志 <span class="close">×</span></span>',
    '<span class="tab">数据字典 <span class="close">×</span></span>')

# 3 主体：dic-wrap 整块 → 九角色列表卡片（行=roleModal 原行，ops 权限配置→roleModal）
rows = [
    ('系统管理员', '全部功能 + 系统管理', '全部项目', '2'),
    ('财务', '财务应收/应付/项目损益', '全部项目', '1'),
    ('财务主管', '财务全模块 + 付款/回款确认审核', '全部项目', '1'),
    ('商务', '订单/租赁全流程', '全部项目', '2'),
    ('商务主管', '订单/租赁全流程 + 单据审核', '全部项目', '1'),
    ('物流', '仓储作业 + 库存查询', '全部项目', '1'),
    ('物流主管', '仓储作业 + 库存查询 + 出/入库审核', '全部项目', '1'),
    ('客户账号', '仅查看与下单申请', '所属客户', '7'),
    ('供应商账号', '下发回执与对账', '所属供应商', '3'),
]
tr = '\r\n'.join(
    f'            <tr><td><b>{nm}</b></td><td>{d}</td><td>{p}</td><td><span class="td-num">{c}</span></td>'
    f'<td class="sticky-op"><span class="ops"><a onclick="openModal(\'roleModal\')">权限配置</a></span></td></tr>'
    for nm, d, p, c in rows)
body = '\r\n'.join([
    '<div class="card">',
    '  <div class="card-head">',
    '    <h3 class="card-title">角色管理</h3>',
    '    <div class="head-btns"><button class="btn btn-sm" onclick="openModal(\'roleModal\')">新增角色</button></div>',
    '  </div>',
    '  <div class="table-wrap">',
    '    <table>',
    '      <thead><tr><th>角色</th><th>说明</th><th>数据权限</th><th>账号数</th><th class="sticky-op">操作</th></tr></thead>',
    '      <tbody>',
    tr,
    '      </tbody>',
    '    </table>',
    '  </div>',
    '  <div class="pager">',
    '    <span class="pg-info">第 1-9 条/总共 9 条</span>',
    '    <span class="pg-btn cur">1</span>',
    '    <span class="pg-size">10 条/页',
    '    </span>',
    '    <span class="pg-jump">跳至 <input value="" placeholder="跳转页码"> 页</span>',
    '  </div>',
    '</div>',
    '    </div>',
    '  </div>',
    '</div>',
    '',
    '',
    '',
])
i0 = t.find('<div class="dic-wrap">')
i1 = t.find('<style id="proto-notes-style">')
assert 0 < i0 < i1, 'dic-wrap 区定位失败'
t = t[:i0] + body + t[i1:]

# 4 标注 pins 清空（壳内 pin 指向字典 data-note 锚点，新主体无锚点；fab/样式/脚本保留）
p0 = t.find('<div id="proto-pins">')
p1 = t.find('<div class="pn-fab"', p0)
assert 0 < p0 < p1, 'pins 区定位失败'
t = t[:p0 + len('<div id="proto-pins">')] + t[p1:]

# 5 createModal（新增字典项）→ roleModal（照抄）
c0 = t.find('<div class="modal-overlay" id="createModal">')
c1 = t.find('<style id="detail-modal-css">')
assert 0 < c0 < c1, 'createModal 区定位失败'
t = t[:c0] + role_modal + '\r\n\r\n' + t[c1:]

# 6 stopModal（停用确认·字典项专用）移除
s0 = t.find('<!-- 操作确认弹窗 · 详情落地页补齐 2026-09-04 -->')
s1 = t.find('<script>', s0)
assert 0 < s0 < s1, 'stopModal 区定位失败'
t = t[:s0] + t[s1:]

# ---- 自检 ----
assert t.count('<aside class="sidebar">') == 1
assert t.count('roleModal') >= 11, 'roleModal 引用不足'  # 定义1+页签按钮1+9行ops+弹窗内引用
assert 'createModal' not in t and 'stopModal' not in t, '字典弹窗残留'
assert '<div class="dic-wrap">' not in t and '<div class="dic-item' not in t, '字典主体残留（CSS 选择器保留属正常）'
assert t.count('供应商账号') == 2, '九角色行数异常（页+弹窗各9）'
for tag in ['<div', '</div>']:
    pass
# 标签配平（div/table/ul/li/section/span 粗配平：开≥关且差不悬殊）
import re
for tag in ['div', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'ul', 'li', 'span', 'button', 'a']:
    o = len(re.findall(f'<{tag}[ >]', t))
    c = len(re.findall(f'</{tag}>', t))
    assert o == c, f'标签 {tag} 不配平 {o}≠{c}'

out = PROTO / '系统管理/角色管理.html'
assert not out.exists(), '目标已存在'
out.write_bytes(t.encode('utf-8'))
print('OK 已创建 系统管理/角色管理.html，长度', len(t))
