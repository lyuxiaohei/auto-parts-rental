#!/usr/bin/env python3
# G42 T7b: 详情页补差集——19 实体 info 行 + 应付/应收专用渲染器 3 行 + 项目详情静态 2 行
# 值取 fields/cells 派生，无值 '—' 占位；只补详情不删新建字段
import io, re

ROOT = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型'
DD = ROOT + '/_data/demo-data.js'
s = io.open(DD, encoding='utf-8').read()

def esc(t):
    return t.replace("'", "\\'")

def row_multiline(label, text):
    return ("{\n          'label': '%s',\n          'text': '%s'\n        }" % (label, text))

# 实体 → 追加行规格：(label, 取值方式)  取值: ('lit', 文本) | ('field', 键, 默认) | ('cells', idx, 默认)
PLAN = {
    'stocktakes':      [('盘点库房', ('lit', '—')), ('处理方式', ('lit', '—')), ('复盘人', ('lit', '—')), ('备注', ('lit', '—'))],
    'products':        [('物料型号', ('field', 'model', '—')), ('供应商内部编码', ('field', 'innerCode', '—')), ('备注', ('lit', '—'))],
    'partners':        [('联系电话', ('cells', 3, '—')), ('备注', ('lit', '—'))],
    'locations':       [('规格/承载', ('field', 'spec', '—')), ('备注', ('lit', '—'))],
    'bomVersions':     [('状态', ('lit', '—')), ('备注', ('lit', '—'))],
    'rentInOrders':    [('所属项目', ('lit', '—')), ('备注', ('lit', '—'))],
    'rentInReturns':   [('备注', ('lit', '—'))],
    'leaseOrders':     [('单据类型', ('lit', '—')), ('建单日期', ('lit', '—')), ('备注', ('lit', '—'))],
    'comboOutbounds':  [('要货日期', ('lit', '—')), ('出库备注', ('lit', '—'))],
    'returnInbounds':  [('验收备注', ('lit', '—'))],
    'transferOutbounds': [('备注', ('lit', '—'))],
    'payments':        [('备注', ('lit', '—'))],
    'invoices':        [('备注', ('lit', '—'))],
    'refunds':         [('备注', ('lit', '—'))],
    'purchaseOrders':  [('所属项目', ('lit', '—')), ('客户', ('lit', '—')), ('备注', ('lit', '—'))],
    'purchaseInbounds':[('到货日期', ('lit', '—')), ('质检要求', ('lit', '—')), ('随货单据', ('lit', '—'))],
    'purchaseReturns': [('备注', ('lit', '—'))],
    'salesOrders':     [('要求交货日期', ('lit', '—'))],
    'salesOutbounds':  [('出库日期', ('field', 'date', '—')), ('备注', ('lit', '—'))],
    'salesReturns':    [('备注', ('lit', '—'))],
}

# 单行 info 风格实体（compact）与多行风格区别：探测每条记录 info 收尾 '\n      ],'
total_ins = 0
for ent, rows in PLAN.items():
    estart = s.index('  %s: {' % ent)
    eend = s.index('\n  },', estart)
    keys = re.findall(r"\n    '([^']+)': \{", s[estart:eend])
    for key in keys:
        ks = estart + s[estart:eend].index("\n    '%s': {" % key)
        idx = s.index('\n      ],', ks)
        seg = s[ks:idx]
        assert "'info': [" in seg or 'info: [' in seg, (ent, key)
        style_b = ('info: [' in seg) and ("'info': [" not in seg.split('info: [')[0][-20:])
        # 实际探测：info 后首行若是单行紧凑行则 style B
        m_info = re.search(r"info: \[\n\s+\{( label:|\s*\n)", seg)
        if m_info and m_info.group(1) == ' label:':
            style_b = True
        mfields = re.search(r'"fields": \{(.*?)\}', seg)
        fields = {}
        if mfields:
            fields = dict(re.findall(r'"(\w+)": "([^"]*)"', mfields.group(1)))
        mcells = re.search(r'"cells": \[(.*?)\]', seg)
        cells = []
        if mcells:
            cells = re.findall(r'"([^"]*)"', mcells.group(1).replace('\\"', '"').replace("\\'", "'"))
        built = []
        for label, spec in rows:
            kind = spec[0]
            if kind == 'lit':
                val = spec[1]
            elif kind == 'field':
                val = fields.get(spec[1]) or spec[2]
            elif kind == 'cells':
                val = (cells[spec[1]] if len(cells) > spec[1] else '') or spec[2]
            if style_b:
                built.append("{ label: '%s', text: '%s' }" % (label, esc(val)))
            else:
                built.append(row_multiline(label, esc(val)))
        ins = ',\n        ' + ',\n        '.join(built)
        s = s[:idx] + ins + s[idx:]
        eend = s.index('\n  },', estart)
        total_ins += len(built)

io.open(DD, 'w', encoding='utf-8').write(s)
print('entity info rows inserted:', total_ins)

# bomVersions 状态值修正：keyHtml 已带「已生效」——'—' 不佳，取 titleNo 版本语义补 '已生效'
# （bomVersions 无 fields，保持 '—' 会误导；按 G36 数据 keyHtml tag 推 '已生效'）
s = io.open(DD, encoding='utf-8').read()
bv = s.index('  bomVersions: {')
bve = s.index('\n  },', bv)
blk = s[bv:bve]
blk = blk.replace("{\n          'label': '状态',\n          'text': '—'\n        }", "{\n          'label': '状态',\n          'text': '已生效'\n        }")
s = s[:bv] + blk + s[bve:]
io.open(DD, 'w', encoding='utf-8').write(s)
print('bomVersions status fixed')

# ---------- 应付专用渲染器：账单日期/到期日/备注 ----------
P = ROOT + '/_data/payable-bill-detail.js'
t = io.open(P, encoding='utf-8').read()
o = "    h += drow('账期', b.period);\n"
n = ("    h += drow('账期', b.period);\n"
     "    /* G42 T7b：账单日期/到期日/备注（详情-新建字段匹配补差） */\n"
     "    h += drow('账单日期', (b.row && b.row.fields && b.row.fields.date) || '—');\n"
     "    h += drow('到期日', (function () { var c = b.row && b.row.cells; return (c && c[10] && /^\\d{4}-\\d{2}-\\d{2}$/.test(c[10])) ? c[10] : '—'; })());\n"
     "    h += drow('备注', '—');\n")
assert t.count(o) == 1
t = t.replace(o, n)
io.open(P, 'w', encoding='utf-8').write(t)
print('payable renderer +3 rows')

# ---------- 应收专用渲染器：账单类型/备注 ----------
P = ROOT + '/_data/receivable-bill-detail.js'
t = io.open(P, encoding='utf-8').read()
o = "    h += drow('账期', b.period);\n"
n = ("    h += drow('账期', b.period);\n"
     "    h += drow('账单类型', b.billType || '—');\n"
     "    h += drow('备注', '—');\n")
assert t.count(o) == 1
t = t.replace(o, n)
io.open(P, 'w', encoding='utf-8').write(t)
print('receivable renderer +2 rows')

# ---------- 项目详情静态 2 行（客户/供应商多选·PRJ-2601 静态页） ----------
P = ROOT + '/项目管理/项目详情.html'
t = io.open(P, encoding='utf-8').read()
o = '    <div class="drow"><div class="dlabel">项目名称</div><div class="dval">华骏重卡·长春基地 驾驶室围板箱租赁</div></div>\n'
n = (o +
     '    <div class="drow"><div class="dlabel">客户</div><div class="dval">华骏重卡汽车有限公司</div></div>\n'
     '    <div class="drow"><div class="dlabel">供应商（多选）</div><div class="dval">甬城塑业 / 吴越联合五金 / 环通循环包装</div></div>\n')
assert t.count(o) == 1
t = t.replace(o, n)
io.open(P, 'w', encoding='utf-8').write(t)
print('project detail static +2 rows')
