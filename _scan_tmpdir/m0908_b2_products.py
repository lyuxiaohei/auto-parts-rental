# -*- coding: utf-8 -*-
"""批2 Script B：产品档案合并（N4）
- 产品档案.html：标题/页签/筛选/表头/按钮/弹窗文案 + 静态行重建 12 行（列序修正：租金在状态前）+ 供应商税率维护区
- 弹窗/产品详情.html、新建产品.html 文案与预览实体改 products
- demo-data.js：appliances→products（标签/列序/BTC-6040S 归属权修正）+ parts 6 条并入（重建 row/info）+ parts 段删除
"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"
LOG = []

def rep(txt, old, new, exp, tag):
    c = txt.count(old)
    assert c == exp, f'[{tag}] 「{old[:50]}」{c}≠{exp}'
    return txt.replace(old, new)

# ============================================================
# 1. demo-data.js 合并
# ============================================================
DD = PROTO / "_data" / "demo-data.js"
src = DD.read_bytes().decode('utf-8')

def seg_bounds(txt, name):
    m = re.search(r'^  ' + name + r': \{', txt, re.M)
    assert m, name
    nxt = re.search(r'^  (?:[a-zA-Z_]+: \{|/\* -)', txt[m.end():], re.M)
    return m.start(), (m.end() + nxt.start() if nxt else len(txt))

# ---- parts 段提取并转换 ----
ps, pe = seg_bounds(src, 'parts')
parts_seg = src[ps:pe]
head_cs = parts_seg.rfind('\n  /* ---', 0, parts_seg.find('  parts: {'))
parts_body = parts_seg[parts_seg.find('  parts: {'):]

PART_DATES = {'LJ-A100': '2026-01-06', 'LJ-B200': '2026-01-06', 'LJ-C300': '2026-02-02',
              'LJ-D400': '2026-02-02', 'LJ-E500': '2026-03-06', 'LJ-F600': '2026-03-06'}

new_records = []
for m in re.finditer(r"^    '(LJ-[\w]+)': \{\n      'row': (\{.*?\}),\n(.*?)\n    \},?", parts_body, re.M | re.S):
    key, row_txt, rest = m.group(1), m.group(2), m.group(3)
    name = re.search(r'"name": "([^"]+)"', row_txt).group(1)
    spec = re.search(r'"spec": "([^"]+)"', row_txt).group(1)
    supplier = re.search(r'"supplier": "([^"]+)"', row_txt).group(1)
    price = re.search(r'<span class=\\"td-num\\">([\d.]+)</span>', row_txt).group(1)
    date = PART_DATES[key]
    row = ('{"fields": {"name": "' + name + '", "cls": "组件", "spec": "' + spec + '", "src": "自有", '
           '"status": "启用", "date": "' + date + '", "supplier": "' + supplier + '"}, '
           '"cells": ["' + name + '", "<span class=\\"tag tag-blue\\">组件</span>", "' + spec + '", "件", '
           '"<span class=\\"tag tag-green\\">自有</span>", "<span class=\\"td-num\\">' + price + '</span>", '
           '"—", "<span class=\\"tag tag-green\\">启用</span>", "' + date + '"], '
           '"ops": [{"t": "详情", "detail": true}, {"t": "编辑", "act": "openModal(\'createModal\')"}, {"t": "停用", "act": "openModal(\'stopModal\')"}]}')
    # tail: feeSecTitle 起原样保留（含 fees/chain/timeline）
    tpos = rest.find("      'feeSecTitle':")
    assert tpos > -1, key
    tail = rest[tpos:].rstrip().rstrip(',')
    tail = tail.replace("'role': '零部件（本档）'", "'role': '产品档案（本档）'")
    info = ("'title': '产品详情',\n      'info': [\n"
            "        {\n          'label': '产品编码',\n          'text': '" + key + "'\n        },\n"
            "        {\n          'label': '名称',\n          'text': '" + name + "',\n          'full': true\n        },\n"
            "        {\n          'label': '分类',\n          'text': '组件'\n        },\n"
            "        {\n          'label': '规格',\n          'text': '" + spec + "',\n          'full': true\n        },\n"
            "        {\n          'label': '计量单位',\n          'text': '件'\n        },\n"
            "        {\n          'label': '归属权',\n          'text': '自有'\n        },\n"
            "        {\n          'label': '参考单价',\n          'text': '" + price + " 元'\n        },\n"
            "        {\n          'label': '租金单价',\n          'text': '—（采购件不计租金）'\n        },\n"
            "        {\n          'label': '供应商（带出）',\n          'text': '" + supplier + "',\n          'full': true\n        },\n"
            "        {\n          'label': '状态',\n          'tag': '启用'\n        },\n"
            "        {\n          'label': '建档日期',\n          'text': '" + date + "'\n        }\n"
            "      ],\n")
    new_records.append("    '" + key + "': {\n      'row': " + row + ",\n" + info + tail + "\n    }")

# ---- appliances 段转 products ----
as_, ae = seg_bounds(src, 'appliances')
app_seg = src[as_:ae]
head_ca = app_seg.rfind('\n  /* ---', 0, app_seg.find('  appliances: {'))
app_body = app_seg[app_seg.find('  appliances: {'):]
app_body = rep(app_body, '  appliances: {', '  products: {', 1, '实体名')
for old, new, exp, tag in [
    ("'title': '器具详情'", "'title': '产品详情'", 6, 'title'),
    ("'label': '器具编码'", "'label': '产品编码'", 6, 'info编码'),
    ("'label': '器具类别'", "'label': '分类'", 6, 'info分类'),
    ("'label': '资产来源'", "'label': '归属权'", 6, 'info归属权'),
    ("'role': '器具档案（本档）'", "'role': '产品档案（本档）'", 6, 'chain本档'),
]:
    app_body = rep(app_body, old, new, exp, tag)
# BTC-6040S 归属权修正（否→自有）
app_body = rep(app_body, '"src": "否"', '"src": "自有"', 1, 'BTC-6040S fields')
app_body = rep(app_body, '<span class=\\"tag tag-gray\\">否</span>', '<span class=\\"tag tag-green\\">自有</span>', 1, 'BTC-6040S cell')
app_body = app_body.replace("'text': '否'", "'text': '自有'")
# 列序修正：cells[6] 状态tag 与 cells[7] 租金 互换（6 条：5 启用绿 + BTC-6040S 停用灰）
k_swap = 0
for price, cls, st in [('38.00', 'tag-green', '启用'), ('32.00', 'tag-green', '启用'), ('12.00', 'tag-green', '启用'),
                       ('18.00', 'tag-green', '启用'), ('8.50', 'tag-green', '启用'), ('7.80', 'tag-gray', '停用')]:
    old = ('"<span class=\\"tag ' + cls + '\\">' + st + '</span>", "<span class=\\"td-num\\">' + price + '</span>"')
    new = ('"<span class=\\"td-num\\">' + price + '</span>", "<span class=\\"tag ' + cls + '\\">' + st + '</span>"')
    c = app_body.count(old)
    assert c == 1, f'列序对换 {price}/{st} 命中 {c}'
    app_body = app_body.replace(old, new)
    k_swap += 1
assert k_swap == 6
# 追加 parts 记录到 products 段尾（前一条记录补逗号）
close_i = app_body.rstrip().rfind('\n  },')
assert close_i > -1
app_body_new = app_body.rstrip()[:close_i] + ',' + '\n\n    /* ===== 组件（原零部件档案并入 · N4 合并） ===== */\n' + \
    '\n'.join(r + ',' for r in new_records[:-1]) + '\n' + new_records[-1] + '\n  },\n'
# 重拼：appliances 段（含注释头）替换为 products 版；parts 段整体删除
src = src[:as_ + head_ca] + app_body_new + src[ae:]
ps2, pe2 = seg_bounds(src, 'parts')
head_cs2 = src.rfind('\n  /* ---', 0, ps2)
src = src[:head_cs2] + src[pe2:]
DD.write_bytes(src.encode('utf-8'))
LOG.append(f'demo-data: appliances→products（6条·列序互换{k_swap}）+ parts 并入 6 条 + parts 段删除')

import subprocess
r = subprocess.run(['node', '--check', str(DD)], capture_output=True, text=True)
assert r.returncode == 0, 'node --check 失败: ' + r.stderr[:400]
LOG.append('node --check OK')

# ============================================================
# 2. 产品档案.html 页面改造
# ============================================================
PG = PROTO / "基础数据" / "产品档案.html"
txt = PG.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'

txt = rep(txt, '<title>器具档案 - 包装租赁管理后台</title>', '<title>产品档案 - 包装租赁管理后台</title>', 1, 'title')
txt = rep(txt, '<div class="sm-link selected">器具档案</div>', '<div class="sm-link selected">产品档案</div>', 1, 'selected')
txt = rep(txt, '<span class="tab active">器具档案 <span class="close">×</span></span>', '<span class="tab active">产品档案 <span class="close">×</span></span>', 1, 'tab')
txt = rep(txt, '<span class="ff-label">器具编码：</span>', '<span class="ff-label">产品编码：</span>', 1, '筛选编码')
txt = rep(txt, '<span class="ff-label">器具名称：</span>', '<span class="ff-label">产品名称：</span>', 1, '筛选名称')
txt = rep(txt, '<span class="ff-label">器具类别：</span>', '<span class="ff-label">分类：</span>', 1, '筛选分类')
txt = rep(txt, '<option>围板箱</option><option>托盘</option><option>料箱</option></select>',
          '<option>围板箱</option><option>托盘</option><option>料箱</option><option>料架</option><option>组件</option></select>', 1, '分类选项')
txt = rep(txt, '<span class="ff-label">资产来源：</span>', '<span class="ff-label">归属权：</span>', 1, '筛选归属权')
txt = rep(txt, '<h3 class="card-title" data-note="1">器具档案</h3>', '<h3 class="card-title" data-note="1">产品档案</h3>', 1, '卡片题')
txt = rep(txt, '>新建器具</button>', '>新建产品</button>', 1, '新建按钮')
txt = rep(txt, '<th>器具编码</th>', '<th>产品编码</th>', 1, 'th编码')
txt = rep(txt, '<th>器具名称</th>', '<th>产品名称</th>', 1, 'th名称')
txt = rep(txt, '<th>类别</th>', '<th>分类</th>', 1, 'th分类')
txt = rep(txt, '<th>资产来源</th>', '<th>归属权</th>', 1, 'th归属权')

# ---- 静态 tbody 重建（12 行 · 列序 [名称,分类,规格,单位,归属权,参考,租金,状态,更新]） ----
ROWS = [
    ('WBX-1210L', '围板箱 1200×1000×970', ('tag-blue', '围板箱'), '1200×1000×970 mm', '只', ('tag-green', '自有'), '38.00', '38.00', ('tag-green', '启用'), '2026-01-06'),
    ('WBX-1210M', '围板箱 1200×1000×590', ('tag-blue', '围板箱'), '1200×1000×590 mm', '只', ('tag-green', '自有'), '32.00', '32.00', ('tag-green', '启用'), '2026-01-06'),
    ('PLT-1210W', '木托盘 1200×1000', ('tag-green', '托盘'), '1200×1000×144 mm', '块', ('tag-green', '自有'), '12.00', '12.00', ('tag-green', '启用'), '2026-02-11'),
    ('PLT-1210P', '塑料托盘 1200×1000', ('tag-green', '托盘'), '1200×1000×150 mm', '块', ('tag-orange', '租入-路凯'), '18.00', '18.00', ('tag-green', '启用'), '2026-02-11'),
    ('BTC-6040', '料箱 600×400×340', ('tag-orange', '料箱'), '600×400×340 mm', '只', ('tag-orange', '租入-路凯'), '8.50', '8.50', ('tag-green', '启用'), '2026-03-02'),
    ('BTC-6040S', '料箱 600×400×220（带盖）', ('tag-orange', '料箱'), '600×400×220 mm', '只', ('tag-green', '自有'), '7.80', '7.80', ('tag-gray', '停用'), '2026-03-02'),
    ('LJ-A100', '锁扣组件', ('tag-blue', '组件'), '不锈钢 304 · M8', '件', ('tag-green', '自有'), '6.80', '—', ('tag-green', '启用'), '2026-01-06'),
    ('LJ-B200', '铰链', ('tag-blue', '组件'), '锌合金 · 65mm', '件', ('tag-green', '自有'), '4.20', '—', ('tag-green', '启用'), '2026-01-06'),
    ('LJ-C300', '围板', ('tag-blue', '组件'), 'HDPE 波纹板 · 970 高', '件', ('tag-green', '自有'), '52.00', '—', ('tag-green', '启用'), '2026-02-02'),
    ('LJ-D400', '箱盖', ('tag-blue', '组件'), 'ABS 吸塑 · 1200×1000', '件', ('tag-green', '自有'), '36.00', '—', ('tag-green', '启用'), '2026-02-02'),
    ('LJ-E500', '底托架', ('tag-blue', '组件'), '钢制喷塑 · 1200×1000', '件', ('tag-green', '自有'), '78.00', '—', ('tag-green', '启用'), '2026-03-06'),
    ('LJ-F600', '内衬', ('tag-blue', '组件'), 'EPE 珍珠棉 · 定制', '件', ('tag-green', '自有'), '15.50', '—', ('tag-green', '启用'), '2026-03-06'),
]
OPS = '<td class="sticky-op"><span class="ops"><a onclick="openModal(\'detailModal\')">详情</a><a onclick="openModal(\'createModal\')">编辑</a><a onclick="openModal(\'stopModal\')">停用</a></span></td>'
body_lines = []
for (k, name, cls, spec, unit, src, price, rent, st, date) in ROWS:
    body_lines.append('        <tr>')
    body_lines.append('          <td><input type="checkbox" class="cb"></td>')
    body_lines.append(f'          <td>{k}</td>')
    body_lines.append(f'          <td>{name}</td>')
    body_lines.append(f'          <td><span class="tag {cls[0]}">{cls[1]}</span></td>')
    body_lines.append(f'          <td>{spec}</td>')
    body_lines.append(f'          <td>{unit}</td>')
    body_lines.append(f'          <td><span class="tag {src[0]}">{src[1]}</span></td>')
    body_lines.append(f'          <td><span class="td-num">{price}</span></td>')
    body_lines.append(f'          <td><span class="td-num">{rent}</span></td>')
    body_lines.append(f'          <td><span class="tag {st[0]}">{st[1]}</span></td>')
    body_lines.append(f'          <td>{date}</td>')
    body_lines.append(f'          {OPS}')
    body_lines.append('        </tr>')
new_tbody = nl.join(body_lines) + nl

tb_s = txt.find('      <tbody>')
tb_e = txt.find('      </tbody>', tb_s)
assert tb_s > -1 and tb_e > tb_s
txt = txt[:tb_s + len('      <tbody>') + (1 if txt[tb_s + len('      <tbody>')] == '\n' else 0)] + new_tbody + txt[txt.rfind('      </tbody>', tb_s):] if False else txt
# 上面写法易错，改直接区段替换：
tb_s = txt.find('      <tbody>')
tb_e = txt.find('      </tbody>', tb_s) + len('      </tbody>')
assert tb_s > -1 and tb_e > tb_s
txt = txt[:tb_s] + '      <tbody>' + nl + new_tbody + '      </tbody>' + txt[tb_e:]

# ---- renderListPage cfg ----
txt = rep(txt, "  entity: 'appliances',", "  entity: 'products',", 1, 'cfg实体')
txt = rep(txt, "{ label: '器具编码', field: '_key' },", "{ label: '产品编码', field: '_key' },", 1, 'cfg筛1')
txt = rep(txt, "{ label: '器具名称', field: 'name' },", "{ label: '产品名称', field: 'name' },", 1, 'cfg筛2')
txt = rep(txt, "{ label: '器具类别', field: 'cls' },", "{ label: '分类', field: 'cls' },", 1, 'cfg筛3')
txt = rep(txt, "{ label: '资产来源', field: 'src' },", "{ label: '归属权', field: 'src' },", 1, 'cfg筛4')

# ---- 弹窗文案（页面内嵌） ----
txt = rep(txt, '<h3 class="modal-title">新建器具</h3>', '<h3 class="modal-title">新建产品</h3>', 1, 'createModal题')
txt = rep(txt, '<span class="req">*</span>器具编码', '<span class="req">*</span>产品编码', 1, '编码label')
txt = rep(txt, '<div class="dlabel">器具编码</div>', '<div class="dlabel">产品编码</div>', 1, 'stopModal编码')
txt = rep(txt, '<span class="req">*</span>器具名称', '<span class="req">*</span>产品名称', 1, '名称label')
txt = rep(txt, '<span class="form-label">类别</span>', '<span class="form-label">分类</span>', 1, '分类label')
txt = rep(txt, '<option selected>围板箱</option><option>塑料托盘</option><option>木托盘</option><option>料箱</option><option>料架</option>',
          '<option selected>围板箱</option><option>塑料托盘</option><option>木托盘</option><option>料箱</option><option>料架</option><option>组件</option>', 1, '分类选项create')
txt = rep(txt, '<span class="req">*</span>资产来源', '<span class="req">*</span>归属权', 1, '归属label')
txt = rep(txt, '<h3 class="modal-title" id="detailTitle">器具详情</h3>', '<h3 class="modal-title" id="detailTitle">产品详情</h3>', 1, 'detail题')

# ---- 供应商税率维护区（主卡后插入新卡） ----
tax_card = nl.join([
'<div class="card">',
'  <div class="card-head">',
'    <h3 class="card-title">供应商税率维护</h3>',
'    <div class="head-btns"><button class="btn btn-default btn-sm">批量导出</button></div>',
'  </div>',
'  <div class="table-wrap">',
'    <table>',
'      <thead>',
'        <tr><th>产品编码</th><th>产品名称</th><th>分类</th><th>供应商</th><th>税率</th><th>结算周期</th></tr>',
'      </thead>',
'      <tbody>',
'        <tr><td>WBX-1210L</td><td>围板箱 1200×1000×970</td><td>围板箱</td><td>宁波华塑包装制品有限公司</td><td><span class="td-num">13%</span></td><td>月结 30 天</td></tr>',
'        <tr><td>WBX-1210L</td><td>围板箱 1200×1000×970</td><td>围板箱</td><td>路凯包装运营（上海）有限公司</td><td><span class="td-num">13%</span></td><td>月结 30 天</td></tr>',
'        <tr><td>BTC-6040</td><td>料箱 600×400×340</td><td>料箱</td><td>路凯包装运营（上海）有限公司</td><td><span class="td-num">13%</span></td><td>月结 30 天</td></tr>',
'        <tr><td>LJ-A100</td><td>锁扣组件</td><td>组件</td><td>苏州联恒五金制品有限公司</td><td><span class="td-num">13%</span></td><td>月结 60 天</td></tr>',
'        <tr><td>LJ-F600</td><td>内衬</td><td>组件</td><td>宁波华塑包装制品有限公司</td><td><span class="td-num">13%</span></td><td>月结 60 天</td></tr>',
'      </tbody>',
'    </table>',
'  </div>',
'  <div class="pn-hint">口径：同一产品可按供应商维护不同税率（默认 13%；运费/杂费后续可能 6%/9%）；单据明细税率默认带出、可手动覆盖。产品档案 = 器具档案 + 零部件档案合并（2026-09-08 会议 N4）。</div>',
'</div>',
'']) 
anchor = '<script src="../_data/demo-data.js"></script>'
assert txt.count(anchor) == 1
txt = txt.replace(anchor, tax_card + nl + anchor)

# ---- inline pin 文案 ----
txt = rep(txt, '<span class="pnp-n">1</span>器具档案</div><div class="pnp-d">围板箱/托盘/料箱三类循环租赁器具，资产属客户自有</div>',
          '<span class="pnp-n">1</span>产品档案</div><div class="pnp-d">器具+零部件合并为产品档案：分类（围板箱/托盘/料箱/组件）×归属权（自有/租入）两维度</div>', 1, 'pin1')

PG.write_bytes(txt.encode('utf-8'))
LOG.append('产品档案.html：文案/筛选/表头/12行静态重建/税率维护区/cfg products')

# ============================================================
# 3. 弹窗模板
# ============================================================
for rel, pairs in {
    '基础数据/弹窗/产品详情.html': [
        ('<title>器具详情 - 包装租赁管理后台</title>', '<title>产品详情 - 包装租赁管理后台</title>'),
        ("<h3 class=\"modal-title\" id=\"detailTitle\">器具详情</h3>", '<h3 class="modal-title" id="detailTitle">产品详情</h3>'),
        ("openGenericDetail('appliances',", "openGenericDetail('products',"),
    ],
    '基础数据/弹窗/新建产品.html': [
        ('<title>新建器具 - 包装租赁管理后台</title>', '<title>新建产品 - 包装租赁管理后台</title>'),
        ('<h3 class="modal-title">新建器具</h3>', '<h3 class="modal-title">新建产品</h3>'),
        ('<span class="req">*</span>器具编码', '<span class="req">*</span>产品编码'),
        ('<span class="req">*</span>器具名称', '<span class="req">*</span>产品名称'),
        ('<span class="form-label">类别</span>', '<span class="form-label">分类</span>'),
        ('<option selected>围板箱</option><option>塑料托盘</option><option>木托盘</option><option>料箱</option><option>料架</option>',
         '<option selected>围板箱</option><option>塑料托盘</option><option>木托盘</option><option>料箱</option><option>料架</option><option>组件</option>'),
        ('<span class="req">*</span>资产来源', '<span class="req">*</span>归属权'),
    ],
}.items():
    f = PROTO / rel
    t = f.read_bytes().decode('utf-8')
    for old, new in pairs:
        c = t.count(old)
        assert c == 1, f'{rel} 「{old[:40]}」{c}'
        t = t.replace(old, new)
    f.write_bytes(t.encode('utf-8'))
    LOG.append(f'{rel} 改名完成')

print('== 批2 Script B ==')
for l in LOG:
    print(' ✓', l)
