# -*- coding: utf-8 -*-
"""批1 Stage5/6：页面级清理
- F01 被移除页 href 暂指最近存活页（批4 v3.0 全面改版）
- 在租台账/租出台账 ops「退租」重指退租入库
- 租赁单列表 ops「创建退租申请」→「退租入库」
- 退租入库列表：ops 去生成赔偿单/创建拆卸单 + 去关联退租申请列/筛选/页签 + 口径注记改直接录入
- 项目详情：删组装单行
- 全站页签清理（组装/拆卸/退租申请/丢损赔偿单 命名页签）
- 我的待办：删 3 行+3 类+统计同步+根级路径前缀修正
- 销售出库/组合出库：打印 → 打印出货单
二进制读写保行尾；每步 assert 计数。
"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"
LOG = []

def patch(rel, old, new, expect, tag=''):
    f = PROTO / rel
    raw = f.read_bytes(); txt = raw.decode('utf-8')
    n = txt.count(old)
    assert n == expect, f'{rel} [{tag}] 「{old[:60]}」出现 {n} 次（应为 {expect}）'
    txt = txt.replace(old, new)
    f.write_bytes(txt.encode('utf-8'))
    LOG.append(f'{rel} [{tag}] {n} 处')

# ---------- 4. 退租入库列表：ops 与去关联 ----------
f = PROTO / '租赁管理/退租入库列表.html'
raw = f.read_bytes(); txt = raw.decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'
TR = lambda s: s.replace('\n', nl)

c = txt.count('<a onclick="go(\'../租赁管理/丢损赔偿单.html\')">生成赔偿单</a>')
assert c == 3, f'生成赔偿单 {c}'
txt = txt.replace('<a onclick="go(\'../租赁管理/丢损赔偿单.html\')">生成赔偿单</a>', '')
c = txt.count('<a onclick="go(\'../仓储作业/拆卸管理列表.html\')">创建拆卸单</a>')
assert c == 3, f'创建拆卸单 {c}'
txt = txt.replace('<a onclick="go(\'../仓储作业/拆卸管理列表.html\')">创建拆卸单</a>', '')
LOG.append('租赁管理/退租入库列表.html [ops删] 生成赔偿单3+创建拆卸单3')

# 静态行/表头删 TZSQ 列
c = txt.count('          <th>关联退租申请单号</th>' + nl)
assert c == 1, f'th {c}'
txt = txt.replace('          <th>关联退租申请单号</th>' + nl, '')
pat = re.compile(r'          <td><span class="lk">TZSQ-[\d\-]+</span></td>' + re.escape(nl))
n = len(pat.findall(txt))
assert n == 8, f'TZSQ td {n}'
txt = pat.sub('', txt)
LOG.append(f'租赁管理/退租入库列表.html [列删] th1+td{n}')

# 筛选删关联退租申请单号
c = txt.count('    <div class="ff"><span class="ff-label">关联退租申请单号：</span><input placeholder="请输入"></div>' + nl)
assert c == 1, f'filter {c}'
txt = txt.replace('    <div class="ff"><span class="ff-label">关联退租申请单号：</span><input placeholder="请输入"></div>' + nl, '')
LOG.append('租赁管理/退租入库列表.html [筛选删] 1')

# renderListPage 配置删 apply 筛选项（该 cfg 块为 LF 行尾）
CFG_LINE = "    { label: '关联退租申请单号', field: 'apply' },\n"
c = txt.count(CFG_LINE)
assert c == 1, f'cfg {c}'
txt = txt.replace(CFG_LINE, '')
LOG.append('租赁管理/退租入库列表.html [cfg筛选项删] 1')

# 页签删退租申请
c = txt.count('  <span class="tab">退租申请 <span class="close">×</span></span>' + nl)
assert c == 1, f'tab {c}'
txt = txt.replace('  <span class="tab">退租申请 <span class="close">×</span></span>' + nl, '')

# 口径注记改直接录入
old_hint = '退租入库单由包装管理模块的「退租申请」审核通过后自动生成，按 BOM 配方将组合单元拆回散件入库；本页面不支持手工新建。'
new_hint = '退租无申请单：客户退回后直接录入退租入库单（按拆后零件·单一产品记录）；入库仅更新库存状态，与财务结算解耦——租金只要发出去就要收，还了也收（2026-09-08 会议拍板）。'
c = txt.count(old_hint)
assert c == 1, f'hint {c}'
txt = txt.replace(old_hint, new_hint)
LOG.append('租赁管理/退租入库列表.html [口径注记] 1')

f.write_bytes(txt.encode('utf-8'))

# ---------- 5. 项目详情：删组装单行 ----------
f = PROTO / '项目管理/项目详情.html'
txt = f.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'
row = (f'        <tr>{nl}          <td><span class="lk" onclick="go(\'../仓储作业/组装列表.html\')">ZZ-20260826-002</span></td>{nl}'
       f'          <td>ZH-2601-A 组装</td>{nl}          <td><span class="td-num">200 套</span></td>{nl}'
       f'          <td><span class="tag tag-blue">组装中</span></td>{nl}          <td>2026-08-26</td>{nl}'
       f'          <td>—</td>{nl}          <td class="sticky-op"><span class="ops"><a onclick="go(\'../仓储作业/组装列表.html\')">查看单据</a></span></td>{nl}        </tr>{nl}')
c = txt.count(row)
assert c == 1, f'项目详情组装行 {c}'
txt = txt.replace(row, '')
f.write_bytes(txt.encode('utf-8'))
LOG.append('项目管理/项目详情.html [组装行删] 1')

# ---------- 6. 全站页签清理 ----------
TAB_FILES = {
    '我的待办.html': [('  <span class="tab">组装 <span class="close">×</span></span>', 1)],
    '仓储作业/库存查询.html': [('  <span class="tab">组装 <span class="close">×</span></span>', 1)],
    '租赁管理/租出台账.html': [('  <span class="tab">丢损赔偿单 <span class="close">×</span></span>', 1)],
    '租赁管理/在租台账.html': [('  <span class="tab">丢损赔偿单 <span class="close">×</span></span>', 1)],
    '系统管理/数据字典.html': [('  <span class="tab">丢损赔偿单 <span class="close">×</span></span>', 1)],
    '采购管理/采购入库列表.html': [('  <span class="tab">组装 <span class="close">×</span></span>', 1)],
    '采购管理/采购入库录单.html': [('  <span class="tab">组装 <span class="close">×</span></span>', 1)],
}
for rel, items in TAB_FILES.items():
    f = PROTO / rel
    txt = f.read_bytes().decode('utf-8')
    nl = '\r\n' if '\r\n' in txt else '\n'
    for old, exp in items:
        c = txt.count(old + nl)
        assert c == exp, f'{rel} tab {c}'
        txt = txt.replace(old + nl, '')
    f.write_bytes(txt.encode('utf-8'))
    LOG.append(f'{rel} [页签清理]')

# ---------- 7. 我的待办：删 3 行+3 类+统计同步+根级路径 ----------
f = PROTO / '我的待办.html'
txt = f.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'

def del_block(txt, start_marker, end_marker):
    i = txt.find(start_marker); j = txt.find(end_marker, i)
    assert i > -1 and j > -1, f'块未找到: {start_marker[:40]}'
    return txt[:i] + txt[j + len(end_marker):]

for dt in ['退租申请', '拆卸', '丢损赔偿']:
    m = re.search(r'        <tr data-type="' + dt + r'">.*?</tr>' + re.escape(nl), txt, re.S)
    assert m, f'待办行未找到: {dt}'
    txt = txt[:m.start()] + txt[m.end():]
    LOG.append(f'我的待办.html [行删] {dt}')

for opt in ['<option>退租申请</option>', '<option>拆卸</option>', '<option>丢损赔偿</option>']:
    c = txt.count(opt)
    assert c == 1, f'option {opt} {c}'
    txt = txt.replace(opt, '')
for chip in ['<span class="todo-chip" onclick="pickType(\'丢损赔偿\')">丢损赔偿</span> ',
             ' <span class="todo-chip" onclick="pickType(\'拆卸\')">拆卸</span>',
             ' <span class="todo-chip" onclick="pickType(\'退租申请\')">退租申请</span>']:
    c = txt.count(chip)
    assert c == 1, f'chip {chip[:30]} {c}'
    txt = txt.replace(chip, '')

# 统计卡 18→15 / 待审核 14→11 / 副标题去"赔偿"
reps = [
    ('<b id="todoCount">18</b>', '<b id="todoCount">15</b>', 1),
    ('覆盖 18 类单据 · 点击"去审核"直达审核弹窗', '覆盖 15 类单据 · 点击"去审核"直达审核弹窗', 1),
    ('<div class="st-num">14<span class="unit">单</span></div><div class="st-foot">订单/出入库/租赁/赔偿/盘点等</div>',
     '<div class="st-num">11<span class="unit">单</span></div><div class="st-foot">订单/出入库/租赁/盘点等</div>', 1),
    ('<span class="pg-info">第 1-18 条 / 总共 18 条待办</span>', '<span class="pg-info">第 1-15 条 / 总共 15 条待办</span>', 1),
]
for old, new, exp in reps:
    c = txt.count(old)
    assert c == exp, f'stat {old[:30]} {c}'
    txt = txt.replace(old, new)

# 根级路径前缀修正：go('../ → go('（页面已迁至原型根）
c = txt.count("go('../")
assert c >= 10, f'go(../ 前缀 {c}'
txt = txt.replace("go('../", "go('")
LOG.append(f'我的待办.html [根级前缀] go(../ {c} 处')

# 待办行内跳转页签清理（组装 tab 已在 TAB_FILES 处理）
f.write_bytes(txt.encode('utf-8'))

# ---------- 8. 打印出货单（L9）：组合出库改名 8+8；销售出库新增 6+6 ----------
PR_OLD = "this.classList.toggle('printed')>打印</a>"
PR_NEW = "this.classList.toggle('printed')>打印出货单</a>"
patch('租赁管理/组合出库列表.html', PR_OLD, PR_NEW, 8, '打印出货单')
# 销售出库：详情后追加打印出货单（页面静态行 6 处）
patch('销售管理/销售出库列表.html',
      '<a onclick="openModal(\'detailModal\')">详情</a>',
      '<a onclick="openModal(\'detailModal\')">详情</a><a onclick="window.print();this.classList.toggle(\'printed\')">打印出货单</a>',
      6, '销售出库新增打印出货单')

print('== Stage5/6 页面级清理 ==')
for l in LOG:
    print(' ✓', l)

# 校验：正文无被移除页引用（除 F01 外全站）
targets = ['租赁管理/退租申请列表.html', '仓储作业/组装列表.html', '仓储作业/组装录单.html', '仓储作业/拆卸管理列表.html', '租赁管理/丢损赔偿单.html']
left = []
for p in sorted(PROTO.rglob('*.html')):
    txt = p.read_bytes().decode('utf-8')
    body = re.sub(r'<aside class="sidebar">.*?</aside>', '', txt, flags=re.S)
    for t in targets:
        if t in body:
            left.append((str(p.relative_to(PROTO)), t))
assert not left, f'残留: {left}'
print('PASS: 全站正文无被移除页引用')
