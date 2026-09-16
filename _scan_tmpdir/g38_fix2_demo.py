# -*- coding: utf-8 -*-
"""G38 fix2：demo-data.js 口径改造（标签/feeCols/托格删除/物料类型 10 值/重归类/新增示例行）
   精确替换＋计数断言；完成后必跑 node --check（外部执行）"""
import io, re, sys

DEMO = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\_data\demo-data.js'
t = io.open(DEMO, encoding='utf-8', newline='').read()
orig_len = len(t)

def block_of(name, s):
    m = re.search(re.escape(name) + r': \{', s)
    assert m, 'entity %s not found' % name
    i = m.start(); k = s.find('{', i); d = 0
    while True:
        if s[k] == '{': d += 1
        elif s[k] == '}':
            d -= 1
            if d == 0: break
        k += 1
    return i, k + 1

def sub_expect(s, old, new, exp, tag=''):
    n = s.count(old)
    assert n == exp, '[%s] %r count %d != %d' % (tag, old[:40], n, exp)
    return s.replace(old, new)

def sub_in_block(s, ent, pairs):
    """实体块内替换（其余不动）"""
    i, j = block_of(ent, s)
    blk = s[i:j]
    for old, new, exp in pairs:
        blk = sub_expect(blk, old, new, exp, ent)
    return s[:i] + blk + s[j:]

# ---------- 1. info 标签：库区→库房 ----------
for old, new, exp in [
    ("'label': '入库库区'", "'label': '入库库房'", 22),
    ("'label': '出库库区'", "'label': '出库库房'", 20),
    ("'label': '调出库区'", "'label': '调出库房'", 3),
    ("'label': '调入库区'", "'label': '调入库房'", 3),
    ("'label': '库区'", "'label': '库房'", 16),
]:
    t = sub_expect(t, old, new, exp, 'label')

# ---------- 2. 时间粒度（块内替换） ----------
t = sub_in_block(t, 'returnInbounds', [("'label': '入库时间'", "'label': '入库日期'", 8)])
# salesOutbounds 制单时间 6 条：5 条纯日期→制单日期；1 条含时分（XSCK-20260902-015）保留「制单时间」（标签随值·数据级混粒度登记）
i, j = block_of('salesOutbounds', t)
blk = t[i:j]
pat = re.compile(r"'label': '制单时间',(\s+'text': '\d{4}-\d{2}-\d{2}')")
blk, n = pat.subn(lambda m: "'label': '制单日期'," + m.group(1), blk)
assert n == 5, 'salesOutbounds 制单日期 renamed %d != 5' % n
t = t[:i] + blk + t[j:]
# partners 更新时间 8 条全纯日期 → 更新日期（配对正则防误伤）
i, j = block_of('partners', t)
blk = t[i:j]
pat2 = re.compile(r"'label': '更新时间',(\s+'text': '\d{4}-\d{2}-\d{2}')")
blk, n2 = pat2.subn(lambda m: "'label': '更新日期'," + m.group(1), blk)
assert n2 == 8, 'partners 更新日期 renamed %d != 8' % n2
t = t[:i] + blk + t[j:]
t = sub_in_block(t, 'products', [("'label': '名称'", "'label': '物料名称'", 12)])

# ---------- 3. feeCols 口径 ----------
t = sub_expect(t, "'零件号',", "'物料编码',", 15, 'feeCols零件号')
t = sub_expect(t, "'托数 × 件数'", "'数量'", 8, 'feeCols托数')
# 退货单裸名（块内）
for ent in ('purchaseReturns', 'salesReturns'):
    t = sub_in_block(t, ent, [
        ("'单价(元)'", "'未税单价(元)'", 3),
        ("'金额(元)'", "'含税金额(元)'", 3),
    ])
t = sub_in_block(t, 'invoices', [("'金额(元)'", "'开票金额(元)'", 6)])
# 租入明细标题 多货品→多物料
t = sub_expect(t, '租入明细（多货品', '租入明细（多物料', 5, 'feeSecTitle')

# ---------- 4. purchaseInbounds：删「X 托」cells 格（到货托数列已删） ----------
i, j = block_of('purchaseInbounds', t)
blk = t[i:j]
pat = re.compile(r'"<span class=\\"td-num\\">\d+ 托</span>", ')
blk2, n = pat.subn('', blk)
assert n == 7, '托 cells removed %d != 7' % n
blk2 = sub_expect(blk2, '"<span class=\\"td-num\\">80 件（折叠隔板）</span>", ', '', 1, 'CGRK-20260820-006 到货数量格')
print('[OK] purchaseInbounds 到货数量格删除 ×8（7 托＋1 件）')
# cells 长度断言：8 行 cells 均为 7
for m in re.finditer(r'"cells": \[(.*?)\]', blk2):
    seg = m.group(1)
    depth = 0; cells = 1; k = 0
    while k < len(seg):
        c = seg[k]
        if c == '[': depth += 1
        elif c == ']': depth -= 1
        elif c == ',' and depth == 0: cells += 1
        k += 1
    assert cells == 7, 'cells len %d != 7 (%s...)' % (cells, seg[:40])
t = t[:i] + blk2 + t[j:]
print('[OK] purchaseInbounds 托格删除 ×8·cells 均 7 格')

# ---------- 5. dictItems：WL-06 释义更新＋WL-07~10 追加 ----------
t = sub_expect(t, '「锁扣内衬等散件」', '「锁扣内衬等散件」', 0, 'noop') if False else t
t = sub_expect(t, '"锁扣内衬等散件"', '"BOM 组合件（ZH-* 母件）"', 1, 'WL-06 desc')
WL06_LINE_END = "'WL-06': { 'row': {\"fields\": {\"category\": \"物料类型\", \"abbr\": \"WL-06\", \"name\": \"组件\", \"status\": \"启用\"}, \"cells\": [\"WL-06\", \"组件\", \"<span class=\\\"td-num\\\">6</span>\", \"BOM 组合件（ZH-* 母件）\", \"<span class=\\\"tag tag-green\\\">启用</span>\"], \"ops\": [{\"t\": \"编辑\"}, {\"t\": \"停用\", \"act\": \"openModal('stopModal')\"}]} },"
assert t.count(WL06_LINE_END) == 1, 'WL-06 line not found after desc update'
NEW_WL = ("\n    'WL-07': { 'row': {\"fields\": {\"category\": \"物料类型\", \"abbr\": \"WL-07\", \"name\": \"卡板箱\", \"status\": \"启用\"}, \"cells\": [\"WL-07\", \"卡板箱\", \"<span class=\\\"td-num\\\">7</span>\", \"钢制/塑钢卡板箱\", \"<span class=\\\"tag tag-green\\\">启用</span>\"], \"ops\": [{\"t\": \"编辑\"}, {\"t\": \"停用\", \"act\": \"openModal('stopModal')\"}]} },"
"\n    'WL-08': { 'row': {\"fields\": {\"category\": \"物料类型\", \"abbr\": \"WL-08\", \"name\": \"金属托盘\", \"status\": \"启用\"}, \"cells\": [\"WL-08\", \"金属托盘\", \"<span class=\\\"td-num\\\">8</span>\", \"钢制金属托盘\", \"<span class=\\\"tag tag-green\\\">启用</span>\"], \"ops\": [{\"t\": \"编辑\"}, {\"t\": \"停用\", \"act\": \"openModal('stopModal')\"}]} },"
"\n    'WL-09': { 'row': {\"fields\": {\"category\": \"物料类型\", \"abbr\": \"WL-09\", \"name\": \"内衬\", \"status\": \"启用\"}, \"cells\": [\"WL-09\", \"内衬\", \"<span class=\\\"td-num\\\">9</span>\", \"E500/F600 等隔衬件\", \"<span class=\\\"tag tag-green\\\">启用</span>\"], \"ops\": [{\"t\": \"编辑\"}, {\"t\": \"停用\", \"act\": \"openModal('stopModal')\"}]} },"
"\n    'WL-10': { 'row': {\"fields\": {\"category\": \"物料类型\", \"abbr\": \"WL-10\", \"name\": \"零部件\", \"status\": \"启用\"}, \"cells\": [\"WL-10\", \"零部件\", \"<span class=\\\"td-num\\\">10</span>\", \"锁扣/铰链/围板/箱盖/底托架\", \"<span class=\\\"tag tag-green\\\">启用</span>\"], \"ops\": [{\"t\": \"编辑\"}, {\"t\": \"停用\", \"act\": \"openModal('stopModal')\"}]} },")
t = t.replace(WL06_LINE_END, WL06_LINE_END + NEW_WL, 1)
print('[OK] dictItems WL-06 释义更新＋WL-07~10 追加（141→145 项）')

# ---------- 6. products 重归类（组件→零部件/内衬）＋新增 3 行 ----------
i, j = block_of('products', t)
blk = t[i:j]
# 6a. 逐记录重归类
RECLASS = {
    'LJ-A100': '零部件', 'LJ-B200': '零部件', 'LJ-C300': '零部件', 'LJ-D400': '零部件',
    'LJ-E500': '内衬', 'LJ-F600': '内衬',
}
for code, cls in RECLASS.items():
    rm = re.search(r"'" + code + r"': \{.*?\n    \},?", blk, re.S)
    assert rm, 'record %s' % code
    rec = rm.group(0)
    rec2 = rec.replace('"cls": "组件"', '"cls": "%s"' % cls)
    rec2 = rec2.replace('>组件</span>', '>%s</span>' % cls)
    rec2 = rec2.replace("'text': '组件'", "'text': '%s'" % cls)
    assert rec2 != rec, 'record %s no change' % code
    blk = blk.replace(rec, rec2, 1)
# 6b. 新增 3 行（模板=BTC-6040S 结构）
def new_product(code, name, cls, spec, unit, buy, rentin, rentinprice, rental, rentalprice, date, supplier, tagc):
    return ("    '" + code + "': {\n"
      "      'row': {\"fields\": {\"name\": \"" + name + "\", \"cls\": \"" + cls + "\", \"spec\": \"" + spec + "\", \"status\": \"启用\", \"date\": \"" + date + "\", \"supplier\": \"" + supplier + "\", \"rentInMode\": \"" + rentin + "\", \"rentInPrice\": " + rentinprice + ", \"rentalMode\": \"" + rental + "\", \"rentalPrice\": " + rentalprice + "}, \"cells\": [\"" + name + "\", \"<span class=\\\"tag " + tagc + "\\\">" + cls + "</span>\", \"" + spec + "\", \"" + unit + "\", \"<span class=\\\"td-num\\\">" + buy + "</span>\", \"—\", \"<span class=\\\"td-num\\\">" + rentinprice + " 元/" + unit + "·月</span>\", \"<span class=\\\"td-num\\\">" + rentalprice + " 元/" + unit + "·月</span>\", \"<span class=\\\"tag tag-green\\\">启用</span>\", \"" + date + "\"], \"ops\": [{\"t\": \"详情\", \"act\": \"go('../基础数据/物料详情.html?id=" + code + "')\"}, {\"t\": \"编辑\", \"act\": \"go('../基础数据/物料新建.html')\"}, {\"t\": \"停用\", \"act\": \"openModal('stopModal')\"}]},\n"
      "      'title': '物料详情',\n"
      "      'info': [\n"
      "        {\n          'label': '物料编码',\n          'text': '" + code + "'\n        },\n"
      "        {\n          'label': '物料名称',\n          'text': '" + name + "',\n          'full': true\n        },\n"
      "        {\n          'label': '物料类型',\n          'text': '" + cls + "'\n        },\n"
      "        {\n          'label': '规格',\n          'text': '" + spec + "',\n          'full': true\n        },\n"
      "        {\n          'label': '计量单位',\n          'text': '" + unit + "'\n        },\n"
      "        {\n          'label': '参考未税采购价',\n          'text': '" + buy + " 元'\n        },\n"
      "        {\n          'label': '参考未税销售价',\n          'text': '—（租赁器具不零售）'\n        },\n"
      "        {\n          'label': '参考未税租入价',\n          'text': '" + rentinprice + " 元/" + unit + "·月'\n        },\n"
      "        {\n          'label': '参考未税租赁价',\n          'text': '" + rentalprice + " 元/" + unit + "·月'\n        },\n"
      "        {\n          'label': '状态',\n          'tag': '启用'\n        },\n"
      "        {\n          'label': '建档日期',\n          'text': '" + date + "'\n        }\n      ],\n"
      "      'feeSecTitle': '在租状态（库存状态口径）',\n"
      "      'feeCols': ['在租', '待归还（超期）', '平均循环', '平均租期', '台账'],\n"
      "      'fees': [\n        {\n          'cells': ['0 " + unit + "', '0 " + unit + "', '—', '—', '客户在租（无在租）'],\n          'links': {\n            4: '仓储作业/库存查询.html'\n          }\n        }\n      ],\n"
      "      'chain': [\n        {\n          'role': '物料档案（本档）',\n          'name': '" + code + " · 启用',\n          'self': true\n        }\n      ],\n"
      "      'timeline': [\n        {\n          't': '" + date + "',\n          'text': '建档 · 启用（G38 物料类型 10 值扩展示例）',\n          'who': '张帆'\n        }\n      ]\n    }")
# 末条记录补逗号＋插入（EOL 感知：demo-data 为 CRLF）
EOL = '\r\n' if '\r\n' in blk else '\n'
TAIL = ']' + EOL + '    }' + EOL + '  }'
i2 = blk.rfind(TAIL)
assert i2 > 0, 'products tail not found'
blk = blk[:i2] + ']' + EOL + '    },' + EOL + new_product('KBX-1040M', '卡板箱 1040×800×590', '卡板箱', '1040×800×590 mm', '只', '120.00', '按月', '8.00', '按月', '12.00', '2026-06-18', '甬城塑业包装制品有限公司', 'tag-blue') + ',' + EOL + \
      new_product('PLT-1210G', '金属托盘 1200×1000', '金属托盘', '1200×1000×144 mm', '块', '165.00', '按月', '10.00', '按月', '15.00', '2026-02-10', '吴越联合五金制品有限公司', 'tag-blue') + ',' + EOL + \
      new_product('KJ-2701', '料架 1850×1000×1200', '料架', '1850×1000×1200 mm', '套', '420.00', '按月', '25.00', '按月', '38.00', '2026-04-22', '吴越联合五金制品有限公司', 'tag-blue') + EOL + '  }'
# 修正：上面把 "]…" 拼错了——重做：在 i2 处保留原 "]\n    }" 再补逗号
# （上面的拼接把末记录的 timeline 结尾 "]" 与 "    }" 替换为 "]\n    },\n<新记录>"，末尾再 "\n  }," 关实体——正确）
t = t[:i] + blk + t[j:]
print('[OK] products 重归类 6 行＋新增 3 行（KBX-1040M/PLT-1210G/KJ-2701）')

# ---------- 7. stockFlows cls 值域收敛 ----------
i, j = block_of('stockFlows', t)
blk = t[i:j]
FLOW_MAP = {
    'XNC-AJZX-WBX': '围板箱', 'WBX-1210L': '围板箱', 'WBX-1210M': '围板箱',
    'PLT-1210P': '塑料托盘', 'BTC-6040': '料箱',
    'XNC-ZZ-WBX': '围板箱', 'XNC-ZZ-PLT': '塑料托盘', 'XNC-ZZ-PLT2': '塑料托盘', 'XNC-ZZ-BTC': '料箱',
    'RZRK-20260910-024': '围板箱',
    'LJ-F600': '内衬',
}
n_changed = 0
for key, cls in FLOW_MAP.items():
    rm = re.search(r"'" + re.escape(key) + r"': \{.*?\n    \},?", blk, re.S)
    assert rm, 'flow %s' % key
    rec = rm.group(0)
    old_cls = '租赁器具' if key != 'LJ-F600' else '零部件'
    rec2 = rec.replace('"cls": "%s"' % old_cls, '"cls": "%s"' % cls)
    rec2 = rec2.replace('>%s</span>' % old_cls, '>%s</span>' % cls)
    rec2 = rec2.replace("'text': '%s'" % old_cls, "'text': '%s'" % cls)
    assert rec2 != rec, 'flow %s no change' % key
    blk = blk.replace(rec, rec2, 1)
    n_changed += 1
t = t[:i] + blk + t[j:]
print('[OK] stockFlows cls 收敛 %d 行（租赁器具→形态/零部件 LJ-F600→内衬）' % n_changed)

# ---------- 8. 库存查询 种子行 tag 同步（源码卫生） ----------
P = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\仓储作业\库存查询.html'
h = io.open(P, encoding='utf-8', newline='').read()
SEED = [
    (r'(围板箱 1200×1000×970</td>\s*<td><span class="tag tag-green">)租赁器具(</span>)', '围板箱'),
    (r'(围板箱 1200×1000×590</td>\s*<td><span class="tag tag-green">)租赁器具(</span>)', '围板箱'),
    (r'(塑料托盘 1200×1000</td>\s*<td><span class="tag tag-green">)租赁器具(</span>)', '塑料托盘'),
    (r'(料箱 600×400×340</td>\s*<td><span class="tag tag-green">)租赁器具(</span>)', '料箱'),
    (r'(安吉智行·客户虚拟仓）</td>\s*<td><span class="tag tag-blue">)租赁器具(</span>)', '围板箱'),
    (r'(内衬.*?</td>\s*<td><span class="tag tag-blue">)零部件(</span>)', '内衬'),
]
for pat_s, cls in SEED:
    pat = re.compile(pat_s, re.S)
    h2, n = pat.subn(lambda m: m.group(1) + cls + m.group(2), h)
    assert n == 1, 'seed %s matched %d' % (pat_s[:30], n)
    h = h2
assert h.count('租赁器具') == 0, '库存查询 租赁器具 residue %d' % h.count('租赁器具')
io.open(P, 'w', encoding='utf-8', newline='').write(h)
print('[OK] 库存查询 种子行 tag 同步 5 行（租赁器具 清零）')

# ---------- 9. 产品档案/物料新建 物料类型 option 6→10 ----------
for rel in (r'\基础数据\产品档案.html', r'\基础数据\物料新建.html'):
    P2 = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型' + rel
    h2 = io.open(P2, encoding='utf-8', newline='').read()
    anchor = '<option>组件</option>'
    assert h2.count(anchor) == 1, '%s 组件 option x%d' % (rel, h2.count(anchor))
    add = '<option>卡板箱</option><option>金属托盘</option><option>内衬</option><option>零部件</option>'
    h2 = h2.replace(anchor, anchor + add, 1)
    io.open(P2, 'w', encoding='utf-8', newline='').write(h2)
    print('[OK] %s 物料类型 option 6→10' % rel)

# ---------- 写盘（行尾整体归一 CRLF·与宿主一致） ----------
t = t.replace('\r\n', '\n').replace('\n', '\r\n')
io.open(DEMO, 'w', encoding='utf-8', newline='').write(t)
print('[OK] demo-data.js 写盘（len %d → %d）' % (orig_len, len(t)))
