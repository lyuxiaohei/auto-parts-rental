# -*- coding: utf-8 -*-
"""G35 T3 v2：实施 P0/P1 补筛选（读取-精确替换＋assert 计数·CRLF/LF 自适应·幂等）
Batch A：8 页 cfg label 脱钩修复（P0）
Batch B：10 页 renderListPage 新增筛选（HTML .ff + cfg entry + 值域动态渲染脚本）＋用户权限状态接线
Batch C：我的待办（自定义页）所属项目/提交人
Batch D：demo-data fields 补齐（opLogs.result ×10 / purchaseInbounds.maker+area ×8）
"""
import io, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
FAILS = []

def rd(p):
    return io.open(ROOT + '\\' + p, encoding='utf-8', newline='').read()

def wr(p, txt):
    import time
    last = None
    for _ in range(3):
        try:
            io.open(ROOT + '\\' + p, 'w', encoding='utf-8', newline='').write(txt)
            return
        except OSError as e:
            last = e
            time.sleep(1)
    raise last

def eol_of(t):
    return '\r\n' if '\r\n' in t else '\n'

def eolize(s, eol):
    return s.replace('\n', eol)

def rep(p, txt, old, new, expect=1, tag=''):
    """幂等精确替换：old 缺席但 new 已在=已完成；否则须 count==expect"""
    eol = eol_of(txt)
    old, new = eolize(old, eol), eolize(new, eol)
    n = txt.count(old)
    if n != expect:
        if n == 0 and txt.count(new) == expect:
            return txt, True  # 已应用过
        FAILS.append(('T3-rep', p, '%s: count=%d expect=%d' % (tag, n, expect)))
        return txt, False
    return txt.replace(old, new), True

CHEV = '<svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>'

def sel_ff(label, sid, extra=True):
    cls = 'ff ff-row-extra' if extra else 'ff'
    return '    <div class="%s"><span class="ff-label">%s：</span><select id="%s"><option selected>全部</option></select>%s</div>\n' % (cls, label, sid, CHEV)

FILL_HDR = """<script>/* G35 筛选值域动态渲染（实体/字典取值·渲染失败保留静态兜底） */
(function () {
  var D = window.DEMO_DATA || {};
  function fill(id, vals) {
    if (!vals || !vals.length) return;
    var s = document.getElementById(id);
    if (s) s.innerHTML = '<option selected>全部</option>' + vals.map(function (o) { return '<option>' + o + '</option>'; }).join('');
  }
  function ent(e, fld) {
    var out = [];
    Object.keys(D[e] || {}).forEach(function (k) {
      var f = (D[e][k].row || {}).fields || {};
      var v = f[fld];
      if (v && out.indexOf(v) < 0) out.push(v);
    });
    return out;
  }
"""

def fill_body_js(body):
    return FILL_HDR + body + '})();\n</script>\n'

def insert_fill_after_cfg(p, t, body, tag):
    """把 fill 脚本插在 renderListPage 调用块所属 <script> 的 </script> 之后"""
    i = t.find('renderListPage(')
    if i < 0:
        FAILS.append(('T3-fill', p, tag + ': 无 renderListPage'))
        return t, False
    j = t.find('</script>', i)
    if j < 0:
        FAILS.append(('T3-fill', p, tag + ': 无 </script>'))
        return t, False
    j += len('</script>')
    eol = eol_of(t)
    ins = eolize(fill_body_js(body), eol).rstrip(eol)
    return t[:j] + eol + ins + t[j:], True

# ============ Batch A：label 脱钩修复（8 页·P0·幂等） ============
LABEL_FIX = [
    ('租赁管理\\租赁单列表.html', "{ label: '客户', field: 'customer' },", "{ label: '客户名称', field: 'customer' },"),
    ('租赁管理\\退租入库列表.html', "{ label: '客户', field: 'customer' },", "{ label: '客户名称', field: 'customer' },"),
    ('财务协同\\付款登记.html', "{ label: '供应商', field: 'supplier' },", "{ label: '供应商名称', field: 'supplier' },"),
    ('财务协同\\应付账单.html', "{ label: '供应商', field: 'supplier' },", "{ label: '供应商名称', field: 'supplier' },"),
    ('销售管理\\销售出库列表.html', "{ label: '客户', field: 'customer' },", "{ label: '客户名称', field: 'customer' },"),
    ('销售管理\\销售订单列表.html', "{ label: '客户', field: 'customer' },", "{ label: '客户名称', field: 'customer' },"),
    ('基础数据\\客商管理.html', "{ label: '客商', field: 'name' },", "{ label: '客商名称', field: 'name' },"),
    ('项目管理\\项目档案.html', "{ label: '客户', field: 'customer' },", "{ label: '客户名称', field: 'customer' },"),
]
print('== Batch A: label FIX x%d ==' % len(LABEL_FIX))
for p, old, new in LABEL_FIX:
    t = rd(p)
    t2, ok = rep(p, t, old, new, 1, 'labelFix')
    if ok:
        wr(p, t2)
        print('  OK', p)

# ============ Batch B：renderListPage 页新增筛选 ============
JOBS = [
 ('财务协同\\应付账单.html',
  [('    <div class="ff ff-row-extra"><span class="ff-label">账单类型：</span>', sel_ff('所属项目', 'g35ProjectSel')),
   ('    <div class="ff ff-row-extra"><span class="ff-label">账单日期：</span>', sel_ff('账期', 'g35PeriodSel'))],
  [("    { label: '关联采购订单号', field: 'ref' },\n", "    { label: '关联采购订单号', field: 'ref' },\n    { label: '所属项目', field: 'project' },\n"),
   ("    { label: '状态', field: 'status' },\n", "    { label: '状态', field: 'status' },\n    { label: '账期', field: 'period' },\n")],
  "  fill('g35ProjectSel', Object.keys(D.projects || {}));\n  fill('g35PeriodSel', ent('payableBills', 'period'));\n"),
 ('仓储作业\\库存查询.html',
  [('    <div class="filter-actions">', sel_ff('物料类型', 'g35ClsSel', extra=False))],
  [("    { label: '库存状态', field: 'status' },\n", "    { label: '库存状态', field: 'status' },\n    { label: '物料类型', field: 'cls' },\n")],
  "  fill('g35ClsSel', ent('stockFlows', 'cls'));\n"),
 ('基础数据\\BOM.html',
  [('    <div class="filter-actions">', sel_ff('更新人', 'g35UpdaterSel'))],
  [("    { label: '更新时间', field: 'update', range: true }\n", "    { label: '更新时间', field: 'update', range: true },\n    { label: '更新人', field: 'updater' }\n")],
  "  fill('g35UpdaterSel', ent('bomList', 'updater'));\n"),
 ('租入管理\\租入入库列表.html',
  [('    <div class="filter-actions">', sel_ff('制单人', 'g35MakerSel') + sel_ff('入库库区', 'g35AreaSel'))],
  [("    { label: '入库时间', field: 'date', range: true }\n", "    { label: '入库时间', field: 'date', range: true },\n    { label: '制单人', field: 'maker' },\n    { label: '入库库区', field: 'area' }\n")],
  "  fill('g35MakerSel', ent('rentInbounds', 'maker'));\n  fill('g35AreaSel', ent('rentInbounds', 'area'));\n"),
 ('租入管理\\租入归还列表.html',
  [('    <div class="filter-actions">', sel_ff('制单人', 'g35MakerSel'))],
  [("    { label: '归还时间', field: 'date', range: true }\n", "    { label: '归还时间', field: 'date', range: true },\n    { label: '制单人', field: 'maker' }\n")],
  "  fill('g35MakerSel', ent('rentInReturns', 'maker'));\n"),
 ('租赁管理\\退租入库列表.html',
  [('    <div class="filter-actions">', sel_ff('入库库房', 'g35WhSel'))],
  [("    { label: '所属项目', field: 'project' }\n", "    { label: '所属项目', field: 'project' },\n    { label: '入库库房', field: 'warehouse' }\n")],
  "  fill('g35WhSel', ent('returnInbounds', 'warehouse'));\n"),
 ('采购管理\\采购入库列表.html',
  [('    <div class="filter-actions">', sel_ff('制单人', 'g35MakerSel') + sel_ff('入库库区', 'g35AreaSel'))],
  [("    { label: '业务类型', field: 'bizType' }\n", "    { label: '业务类型', field: 'bizType' },\n    { label: '制单人', field: 'maker' },\n    { label: '入库库区', field: 'area' }\n")],
  "  fill('g35MakerSel', ent('purchaseInbounds', 'maker'));\n  fill('g35AreaSel', ent('purchaseInbounds', 'area'));\n"),
 ('销售管理\\销售出库列表.html',
  [('    <div class="filter-actions">', sel_ff('出库库房', 'g35WhSel'))],
  [("    { label: '所属项目', field: 'project' }\n", "    { label: '所属项目', field: 'project' },\n    { label: '出库库房', field: 'warehouse' }\n")],
  "  fill('g35WhSel', ent('salesOutbounds', 'warehouse'));\n"),
 ('销售管理\\销售订单列表.html',
  [('        <div class="filter-actions">', sel_ff('下单人', 'g35AgentSel'))],
  [("    { label: '下单日期', field: 'date', range: true }\n", "    { label: '下单日期', field: 'date', range: true },\n    { label: '下单人', field: 'agent' }\n")],
  "  fill('g35AgentSel', ent('salesOrders', 'agent'));\n"),
 ('系统管理\\操作日志.html',
  [('    <div class="filter-actions">', sel_ff('操作结果', 'g35ResultSel'))],
  [("    { label: '内容关键字', field: 'summary' }\n", "    { label: '内容关键字', field: 'summary' },\n    { label: '操作结果', field: 'result' }\n")],
  "  fill('g35ResultSel', ent('opLogs', 'result'));\n"),
]
print('== Batch B: ADD filters x%d pages ==' % len(JOBS))
FILL_MARK = 'G35 筛选值域动态渲染'
for p, html_edits, cfg_edits, fbody in JOBS:
    t = rd(p)
    ok_all = True
    for anchor, newblock in cfg_edits:
        t2, ok = rep(p, t, anchor, newblock, 1, 'cfg')
        t = t2; ok_all = ok_all and ok
    for anchor, ins in html_edits:
        # 幂等守卫：select id 已在 = 已插入过，跳过
        import re as _re
        sids = _re.findall(r'id="([^"]+)"', ins)
        if sids and all(('id="%s"' % s) in t for s in sids):
            continue
        t2, ok = rep(p, t, anchor, ins + anchor, 1, 'html')
        t = t2; ok_all = ok_all and ok
    if ok_all and FILL_MARK not in t:
        t2, ok = insert_fill_after_cfg(p, t, fbody, p)
        t = t2; ok_all = ok_all and ok
    if ok_all:
        wr(p, t)
        print('  OK', p)
    else:
        print('  SKIP(fail)', p)

# 用户权限 状态接线（P0）：cfg 补状态 + 既有 select 静态错值改 id 动态化
p = '系统管理\\用户权限.html'
t = rd(p)
t2, ok1 = rep(p, t, "    { label: '角色', field: 'role' },\n",
              "    { label: '角色', field: 'role' },\n    { label: '状态', field: 'status' },\n", 1, 'users cfg')
t2, ok2 = rep(p, t2,
              '<select><option selected>全部</option><option>全部用户</option><option>我方</option><option>客户</option><option>供应商</option></select>',
              '<select id="g35StatusSel"><option selected>全部</option></select>', 1, 'users select')
if ok1 and ok2:
    t2, ok3 = insert_fill_after_cfg(p, t2, "  fill('g35StatusSel', ent('users', 'status'));\n", 'users fill')
    if ok3:
        wr(p, t2)
        print('  OK 用户权限 状态接线')
    else:
        print('  SKIP(fail)', p)
else:
    print('  SKIP(fail)', p)

# ============ Batch C：我的待办（自定义页） ============
p = '我的待办.html'
t = rd(p)
if 'id="todoProject"' in t and 'G35 筛选值域动态渲染' in t:
    print('  OK 我的待办（已应用，跳过）')
else:
    ok_all = True
    t2, ok = rep(p, t, '    <div class="ff"><span class="ff-label">关键词：</span>',
        '    <div class="ff"><span class="ff-label">所属项目：</span><select id="todoProject" onchange="filterTodo()"><option>全部</option></select></div>\n'
        '    <div class="ff"><span class="ff-label">提交人：</span><select id="todoSubmitter" onchange="filterTodo()"><option>全部</option></select></div>\n'
        '    <div class="ff"><span class="ff-label">关键词：</span>', 1, 'todo html')
    ok_all = ok_all and ok
    t2, ok = rep(p, t2, 'data-auditor="\' + (f.auditor || \'\') + \'">',
        'data-auditor="\' + (f.auditor || \'\') + \'" data-project="\' + (f.project || \'\') + \'" data-submitter="\' + f.submitter + \'">', 1, 'todo tr')
    ok_all = ok_all and ok
    t2, ok = rep(p, t2, "  var au = auEl ? auEl.value : '全部';\n",
        "  var au = auEl ? auEl.value : '全部';\n"
        "  var pjEl = document.getElementById('todoProject');\n"
        "  var pj = pjEl ? pjEl.value : '全部';\n"
        "  var sbEl = document.getElementById('todoSubmitter');\n"
        "  var sb = sbEl ? sbEl.value : '全部';\n", 1, 'todo vars')
    ok_all = ok_all and ok
    t2, ok = rep(p, t2, "(au === '全部' || au === tr.getAttribute('data-auditor')) && (!kw",
        "(au === '全部' || au === tr.getAttribute('data-auditor')) && (pj === '全部' || pj === tr.getAttribute('data-project')) && (sb === '全部' || sb === tr.getAttribute('data-submitter')) && (!kw", 1, 'todo cond')
    ok_all = ok_all and ok
    t2, ok = rep(p, t2, "document.getElementById('todoAuditor').value='全部';filterTodo()",
        "document.getElementById('todoAuditor').value='全部';document.getElementById('todoProject').value='全部';document.getElementById('todoSubmitter').value='全部';filterTodo()", 1, 'todo reset')
    ok_all = ok_all and ok
    if ok_all:
        # fill 脚本挂在 G12 builder 脚本块后
        anchor = "  if (typeof filterTodo === 'function') filterTodo();\n})();\n</script>"
        eol = eol_of(t2)
        ins = anchor + eol + eolize(fill_body_js(
            "  fill('todoProject', ent('todoItems', 'project'));\n  fill('todoSubmitter', ent('todoItems', 'submitter'));\n"
        ), eol).rstrip(eol)
        t2, ok = rep(p, t2, anchor, ins, 1, 'todo fill')
        ok_all = ok_all and ok
    if ok_all:
        wr(p, t2)
        print('  OK 我的待办')
    else:
        print('  SKIP(fail)', p)

# ============ Batch D：demo-data fields 补齐 ============
p = '_data\\demo-data.js'
t = rd(p)
eol = eol_of(t)
nl = t.count('\n'); crlf = t.count('\r\n')
if eol == '\r\n' and nl != crlf:
    FAILS.append(('T3-D', p, '混合行尾 LF=%d CRLF=%d 拒写' % (nl - crlf, crlf)))
    print('demo-data SKIP: 混合行尾')
else:
    lines = t.split(eol)
    CELL = re.compile(r'"((?:[^"\\]|\\.)*)"')

    def patch_block(lines, header, rowtest, patchline, expect):
        """返回 (new_lines, n)——块内逐行 patch；异常 raise"""
        i0 = next(i for i, l in enumerate(lines) if l.startswith(header))
        i1 = next(i for i, l in enumerate(lines) if i > i0 and l == '  },')
        n = 0
        newblk = []
        for i in range(i0, i1 + 1):
            l = lines[i]
            if rowtest(l):
                l = patchline(l)
                n += 1
            newblk.append(l)
        assert n == expect, '%s 修补行数=%d 期望 %d' % (header, n, expect)
        return lines[:i0] + newblk + lines[i1 + 1:], n

    def op_patch(l):
        cj = l.find('"cells": [') + len('"cells": [')
        cells = [re.sub(r'<[^>]+>', '', m.group(1)) for m in CELL.finditer(l[cj:l.find(']} ', cj)])]
        val = cells[-1] if cells else '成功'
        assert val in ('成功', '失败'), 'opLogs 结果值异常: ' + val
        return l.replace('}, "cells":', ', "result": "%s"}, "cells":' % val)

    def pi_patch(l):
        cj = l.find('"cells": [') + len('"cells": [')
        ce = l.find(', "ops"', cj)
        cells = [re.sub(r'<[^>]+>', '', m.group(1)) for m in CELL.finditer(l[cj:ce if ce > -1 else l.find(']} ', cj)])]
        assert len(cells) >= 9, 'PI cells 不足: %d' % len(cells)
        m2 = re.search(r'("inTime": "[^"]*")\}', l)
        assert m2, 'PI inTime 锚未命中: ' + l[:60]
        return l.replace(m2.group(0), m2.group(1) + ', "maker": "%s", "area": "%s"}' % (cells[7], cells[5]))

    try:
        already = '"result": "成功"' in t and '"result": "失败"' in t
        if already:
            print('opLogs result 已补过，跳过')
        else:
            lines, op_n = patch_block(lines, '  opLogs: {',
                lambda l: "'row': {\"fields\"" in l and 'LOG-' in l and '"result"' not in l, op_patch, 10)
            print('opLogs rows patched:', op_n)
        already2 = '"maker": "' in t.split('purchaseInbounds: {')[1].split('\n  },')[0] if 'purchaseInbounds: {' in t else False
        if already2:
            print('purchaseInbounds maker/area 已补过，跳过')
        else:
            lines, pi_n = patch_block(lines, '  purchaseInbounds: {',
                lambda l: "'row': {\"fields\"" in l and '"inTime"' in l and '"maker"' not in l, pi_patch, 8)
            print('purchaseInbounds rows patched:', pi_n)
        wr(p, eol.join(lines))
        print('demo-data written')
    except AssertionError as e:
        FAILS.append(('T3-D', p, str(e)))
        print('demo-data SKIP:', e)

print()
print('FAILS:', len(FAILS))
for f in FAILS:
    print('  ', f)
