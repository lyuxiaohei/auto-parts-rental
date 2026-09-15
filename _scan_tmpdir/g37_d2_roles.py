# -*- coding: utf-8 -*-
"""G37 D2（D-143）：审核角色 7→6——系统管理员/财务/商务/物流/采购/项目经理
主管并入部门（desc 吸收主管职责）；补采购（徐文）与项目经理（沈婷·「项目经理代下」承载角色）。
改动面：demo-data roles/users＋角色管理/用户权限/权限配置三页＋退款登记 1 处＋A05/A02 演示值。"""
import io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
def rd(p): return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()
def wr(p, s): io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

def cut_span(s, a, b):
    i = s.index(a)
    j = s.index(b, i) + len(b)
    return s[:i] + s[j:]

# ============ 1. demo-data roles 7→6（重排 RL-01~06） ============
p = os.path.join('_data', 'demo-data.js')
d = rd(p)
if "'RL-07'" in d or '物流主管' in d[d.index('roles: {'):d.index('\n  },', d.index('roles: {'))]:
    old_ent = cut_span(d, 'roles: {', '\n  },')
    NEW = '''roles: {
    'RL-01': { 'row': {"fields": {"name": "系统管理员", "desc": "全部功能 + 系统管理", "scope": "全部项目", "accts": "2"}, "keyHtml": "<b>系统管理员</b>", "cells": ["全部功能 + 系统管理", "全部项目", "<span class=\\"td-num\\">2</span>"], "ops": [{"t": "权限配置", "act": "go('../系统管理/权限配置.html?role=系统管理员')"}]} },
    'RL-02': { 'row': {"fields": {"name": "财务", "desc": "财务全模块 + 付款/收款确认审核（主管职责并入）", "scope": "全部项目", "accts": "2"}, "keyHtml": "<b>财务</b>", "cells": ["财务全模块 + 付款/收款确认审核（主管职责并入）", "全部项目", "<span class=\\"td-num\\">2</span>"], "ops": [{"t": "权限配置", "act": "go('../系统管理/权限配置.html?role=财务')"}]} },
    'RL-03': { 'row': {"fields": {"name": "商务", "desc": "订单/租赁全流程 + 单据审核（主管职责并入）", "scope": "全部项目", "accts": "2"}, "keyHtml": "<b>商务</b>", "cells": ["订单/租赁全流程 + 单据审核（主管职责并入）", "全部项目", "<span class=\\"td-num\\">2</span>"], "ops": [{"t": "权限配置", "act": "go('../系统管理/权限配置.html?role=商务')"}]} },
    'RL-04': { 'row': {"fields": {"name": "物流", "desc": "仓储作业 + 库存查询 + 出/入库审核（主管职责并入）", "scope": "全部项目", "accts": "2"}, "keyHtml": "<b>物流</b>", "cells": ["仓储作业 + 库存查询 + 出/入库审核（主管职责并入）", "全部项目", "<span class=\\"td-num\\">2</span>"], "ops": [{"t": "权限配置", "act": "go('../系统管理/权限配置.html?role=物流')"}]} },
    'RL-05': { 'row': {"fields": {"name": "采购", "desc": "采购全流程（订单/入库/退货）+ 供应商税率维护", "scope": "全部项目", "accts": "1"}, "keyHtml": "<b>采购</b>", "cells": ["采购全流程（订单/入库/退货）+ 供应商税率维护", "全部项目", "<span class=\\"td-num\\">1</span>"], "ops": [{"t": "权限配置", "act": "go('../系统管理/权限配置.html?role=采购')"}]} },
    'RL-06': { 'row': {"fields": {"name": "项目经理", "desc": "项目管理 + 销售订单代下 + 转移出库", "scope": "所属项目", "accts": "1"}, "keyHtml": "<b>项目经理</b>", "cells": ["项目管理 + 销售订单代下 + 转移出库", "所属项目", "<span class=\\"td-num\\">1</span>"], "ops": [{"t": "权限配置", "act": "go('../系统管理/权限配置.html?role=项目经理')"}]} }
  },'''
    i = d.index('roles: {')
    j = d.index('\n  },', i) + len('\n  },')
    d = d[:i] + NEW + d[j:]
    wr(p, d)
    print('1 roles 7→6（RL-01~06 重排）')
else:
    print('1 roles：已是 6（跳过）')

# ============ 2. demo-data users：3 行 role 改＋2 新用户 ============
d = rd(p)
i = d.index('users: {')
j = d.index('\n  },', i)
blk = d[i:j]
changed = False
for old, new in [('"role": "商务主管"', '"role": "商务"'), ('"role": "财务主管"', '"role": "财务"'), ('"role": "物流主管"', '"role": "物流"')]:
    n = blk.count(old)
    if n:
        blk = blk.replace(old, new)
        # cells/tag 同步（tag-blue 文案）
        blk = blk.replace('<span class=\\"tag tag-blue\\">' + old.split('"')[3] + '</span>', '<span class=\\"tag tag-blue\\">' + new.split('"')[3] + '</span>')
        changed = True
# search 字段含角色名的（admin 行「admin 系统管理员」保留——系统管理员角色名未变）
if "'xuwen'" not in blk:
    NEW_USERS = '''
    'xuwen': { 'row': {"fields": {"search": "xuwen 徐文", "role": "采购", "scope": "全部数据", "status": "启用"}, "cells": ["徐文", "<span class=\\"tag tag-blue\\">采购</span>", "全部数据", "132****7801", "<span class=\\"tag tag-green\\">启用</span>", "2026-09-14 10:20"], "ops": [{"t": "编辑", "act": "go('../系统管理/用户新建.html')"}, {"t": "权限配置", "act": "go('../系统管理/权限配置.html')"}, {"t": "重置密码", "act": "openModal('resetModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'shenting': { 'row': {"fields": {"search": "shenting 沈婷", "role": "项目经理", "scope": "所属项目", "status": "启用"}, "cells": ["沈婷", "<span class=\\"tag tag-blue\\">项目经理</span>", "所属项目", "131****9012", "<span class=\\"tag tag-green\\">启用</span>", "2026-09-14 10:22"], "ops": [{"t": "编辑", "act": "go('../系统管理/用户新建.html')"}, {"t": "权限配置", "act": "go('../系统管理/权限配置.html')"}, {"t": "重置密码", "act": "openModal('resetModal')"}, {"t": "停用", "act": "openModal('stopModal')"}]} },'''
    blk = blk.rstrip() + NEW_USERS
    changed = True
    print('2 users：主管 3 行并入部门＋新增 徐文(采购)/沈婷(项目经理)')
if changed:
    d = d[:i] + blk + d[j:]
    wr(p, d)
else:
    print('2 users：已改（跳过）')

# ============ 3. 角色管理.html 静态 7→6 行 ============
p3 = os.path.join('系统管理', '角色管理.html')
s3 = rd(p3)
if '财务主管' in s3:
    i = s3.index('<tbody')
    j = s3.index('</tbody>', i)
    rows = '''<tbody>
            <tr><td><b>系统管理员</b></td><td>全部功能 + 系统管理</td><td>全部项目</td><td><span class="td-num">2</span></td><td class="sticky-op"><span class="ops"><a onclick="go('../系统管理/权限配置.html?role=系统管理员')">权限配置</a></span></td></tr>
            <tr><td><b>财务</b></td><td>财务全模块 + 付款/收款确认审核（主管职责并入）</td><td>全部项目</td><td><span class="td-num">2</span></td><td class="sticky-op"><span class="ops"><a onclick="go('../系统管理/权限配置.html?role=财务')">权限配置</a></span></td></tr>
            <tr><td><b>商务</b></td><td>订单/租赁全流程 + 单据审核（主管职责并入）</td><td>全部项目</td><td><span class="td-num">2</span></td><td class="sticky-op"><span class="ops"><a onclick="go('../系统管理/权限配置.html?role=商务')">权限配置</a></span></td></tr>
            <tr><td><b>物流</b></td><td>仓储作业 + 库存查询 + 出/入库审核（主管职责并入）</td><td>全部项目</td><td><span class="td-num">2</span></td><td class="sticky-op"><span class="ops"><a onclick="go('../系统管理/权限配置.html?role=物流')">权限配置</a></span></td></tr>
            <tr><td><b>采购</b></td><td>采购全流程（订单/入库/退货）+ 供应商税率维护</td><td>全部项目</td><td><span class="td-num">1</span></td><td class="sticky-op"><span class="ops"><a onclick="go('../系统管理/权限配置.html?role=采购')">权限配置</a></span></td></tr>
            <tr><td><b>项目经理</b></td><td>项目管理 + 销售订单代下 + 转移出库</td><td>所属项目</td><td><span class="td-num">1</span></td><td class="sticky-op"><span class="ops"><a onclick="go('../系统管理/权限配置.html?role=项目经理')">权限配置</a></span></td></tr>
          '''
    s3 = s3[:i] + rows + s3[j:]
    wr(p3, s3)
    print('3 角色管理.html：静态 6 行')
else:
    print('3 角色管理：已改（跳过）')

# ============ 4. 用户权限.html：select＋静态行 ============
p4 = os.path.join('系统管理', '用户权限.html')
s4 = rd(p4)
if '财务主管' in s4:
    old_sel = '<option>财务</option><option>商务</option><option>物流</option><option>财务主管</option><option>商务主管</option><option>物流主管</option>'
    assert s4.count(old_sel) == 1
    s4 = s4.replace(old_sel, '<option>财务</option><option>商务</option><option>物流</option><option>采购</option><option>项目经理</option>')
    # 静态行 tag（周敏/沈婷/林国栋）
    s4 = s4.replace('<span class="tag tag-orange">财务主管</span>', '<span class="tag tag-orange">财务</span>')
    s4 = s4.replace('<span class="tag tag-green">商务主管</span>', '<span class="tag tag-green">商务</span>')
    s4 = s4.replace('<span class="tag tag-green">物流主管</span>', '<span class="tag tag-green">物流</span>')
    assert '主管' not in s4, '用户权限残留主管'
    wr(p4, s4)
    print('4 用户权限.html：select 6 角色＋静态行 tag')
else:
    print('4 用户权限：已改（跳过）')

# ============ 5. 权限配置.html：ROLE_PERM 7→6 ============
p5 = os.path.join('系统管理', '权限配置.html')
s5 = rd(p5)
if "'财务主管'" in s5:
    old_rp = '''  '财务': { desc:'财务管理（应收/应付/财务看板）', accts:'1', scope:'全部项目', perms:['我的待办','财务管理'] },
  '财务主管': { desc:'财务全模块 + 付款/收款确认审核', accts:'1', scope:'全部项目', perms:['我的待办','财务管理'] },
  '商务': { desc:'订单/租赁全流程', accts:'2', scope:'全部项目', perms:['我的待办','基础资料','采购管理','销售管理','租赁管理'] },
  '商务主管': { desc:'订单/租赁全流程 + 单据审核', accts:'1', scope:'全部项目', perms:['我的待办','基础资料','采购管理','销售管理','租赁管理'] },
  '物流': { desc:'仓储作业 + 库存查询', accts:'1', scope:'全部项目', perms:['我的待办','仓储管理'] },
  '物流主管': { desc:'仓储作业 + 库存查询 + 出/入库审核', accts:'1', scope:'全部项目', perms:['我的待办','仓储管理'] }'''
    new_rp = '''  '财务': { desc:'财务全模块 + 付款/收款确认审核（主管职责并入）', accts:'2', scope:'全部项目', perms:['我的待办','财务管理'] },
  '商务': { desc:'订单/租赁全流程 + 单据审核（主管职责并入）', accts:'2', scope:'全部项目', perms:['我的待办','基础资料','采购管理','销售管理','租赁管理'] },
  '物流': { desc:'仓储作业 + 库存查询 + 出/入库审核（主管职责并入）', accts:'2', scope:'全部项目', perms:['我的待办','仓储管理'] },
  '采购': { desc:'采购全流程（订单/入库/退货）+ 供应商税率维护', accts:'1', scope:'全部项目', perms:['我的待办','基础资料','采购管理'] },
  '项目经理': { desc:'项目管理 + 销售订单代下 + 转移出库', accts:'1', scope:'所属项目', perms:['项目管理','我的待办','销售管理','租赁管理'] }'''
    nl = '\r\n' if '\r\n' in s5[s5.index("'财务主管'")-100:s5.index("'财务主管'")] else '\n'
    assert s5.count(old_rp.replace('\n', nl)) == 1, 'ROLE_PERM 块不匹配'
    s5 = s5.replace(old_rp.replace('\n', nl), new_rp.replace('\n', nl))
    wr(p5, s5)
    print('5 权限配置.html：ROLE_PERM 6 角色')
else:
    print('5 权限配置：已改（跳过）')

# ============ 6. 退款登记.html 审核人行 ============
p6 = os.path.join('财务协同', '退款登记.html')
s6 = rd(p6)
if '财务主管' in s6:
    s6 = s6.replace('财务主管 · 周敏', '财务 · 周敏')
    assert '主管' not in s6
    wr(p6, s6)
    print('6 退款登记.html：审核人财务·周敏')
else:
    print('6 退款登记：已改（跳过）')

# ============ 7. A05/A02 演示值同步 ============
for pr, in [('P3-R01-A05-字段字典.md',), ('P3-R01-A02-页面类型与入口对照表.md',)]:
    sx = rd(pr)
    if '主管' in sx:
        before = sum(sx.count(x) for x in ['财务主管', '商务主管', '物流主管'])
        sx = sx.replace('财务主管', '财务').replace('商务主管', '商务').replace('物流主管', '物流')
        wr(pr, sx)
        print('7 %s：%d 处主管并入' % (pr, before))
print('D2 DONE')
