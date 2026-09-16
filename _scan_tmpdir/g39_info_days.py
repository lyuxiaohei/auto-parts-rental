# -*- coding: utf-8 -*-
"""G39 T3 补 · 详情 info 起租日+天数展示（D-148）
  leaseOrders：计租天数块前插 起租日期（值=fields.start·9 行）
  rentInOrders：租期块后插 起租日期/止租日期/计租天数（由 period 区间解析·天数=max(2,止-起+1)）"""
import io, re
from datetime import date

P = r'P3-R01-包装租赁管理后台原型\_data\demo-data.js'
s = io.open(P, 'rb').read().decode('utf-8')
NL = '\r\n'

def ent_span(x, name):
    m = re.search(r'^ {2}(?:/\*.*?\*/[ \t]*)?%s: \{' % name, x, re.M)
    assert m
    nxt = re.search(r'^ {2}(?:/\*.*?\*/[ \t]*)?[A-Za-z_][A-Za-z0-9_]*: \{', x[m.end():], re.M)
    return m.start(), (m.end() + nxt.start()) if nxt else len(x)

def info_block(label, text, full=False):
    return ("        {" + NL +
            "          'label': '%s'," % label + NL +
            "          'text': '%s'%s" % (text, "," if full else "") + NL +
            ("          'full': true" + NL + "        },") if full else "        },")

def blk(label, text):
    return "        {\r\n          'label': '%s',\r\n          'text': '%s'\r\n        },\r\n" % (label, text)

# ---- leaseOrders：计租天数前插 起租日期 ----
a, b = ent_span(s, 'leaseOrders')
seg = s[a:b]
if "'label': '起租日期'" not in seg:
    n = 0
    out = []
    for m in re.finditer(r"^    '(ZL-[^']+)': \{", seg, re.M):
        key = m.group(1)
        rs = seg.find("'row': {", m.start())
        if rs < 0: continue
        rowline_end = seg.find('\r\n', rs)
        rowtxt = seg[rs:rowline_end]
        sm = re.search(r'"start": "(\d{4}-\d{2}-\d{2})"', rowtxt)
        if not sm: continue
        startd = sm.group(1)
        nxt_rec = re.search(r"^    '[^']+': \{", seg[m.end():], re.M)
        rec_end = m.end() + nxt_rec.start() if nxt_rec else len(seg)
        rec = seg[m.start():rec_end]
        anchor = "        {\r\n          'label': '计租天数',"
        if anchor not in rec:
            print('  [skip] %s 无计租天数块' % key); continue
        ins = blk('起租日期', startd) + anchor
        rec2 = rec.replace(anchor, ins, 1)
        out.append((m.start(), rec_end, rec2))
    for st, en, rep in reversed(out):
        seg = seg[:st] + rep + seg[en:]
        n += 1
    assert n == 9, 'leaseOrders 起租日期 inserted=%d expect 9' % n
    s = s[:a] + seg + s[b:]
    print('[leaseOrders] +起租日期 ×%d' % n)

# ---- rentInOrders：租期后插 起租日期/止租日期/计租天数 ----
a, b = ent_span(s, 'rentInOrders')
seg = s[a:b]
if "'label': '起租日期'" not in seg:
    n = 0
    out = []
    pos = 0
    for m in re.finditer(r"^    '(RZD-[^']+)': \{", seg, re.M):
        key = m.group(1)
        rs = seg.find("'row': {", m.start())
        rowline_end = seg.find('\r\n', rs)
        rowtxt = seg[rs:rowline_end]
        pm = re.search(r'"period": "(\d{4}-\d{2}-\d{2}) ~ (\d{4}-\d{2}-\d{2})"', rowtxt)
        if not pm:
            print('  [skip] %s 无 period' % key); continue
        d1 = date(*map(int, pm.group(1).split('-')))
        d2 = date(*map(int, pm.group(2).split('-')))
        days = max(2, (d2 - d1).days + 1)
        nxt_rec = re.search(r"^    '[^']+': \{", seg[m.end():], re.M)
        rec_end = m.end() + nxt_rec.start() if nxt_rec else len(seg)
        rec = seg[m.start():rec_end]
        anchor_re = re.compile(r"(\{\r\n          'label': '租期',\r\n          'text': '[^']*',?\r\n(          'full': true\r\n)?        \},\r\n)")
        mm = anchor_re.search(rec)
        if not mm:
            print('  [skip] %s 无租期块' % key); continue
        ins = mm.group(1) + blk('起租日期', pm.group(1)) + blk('止租日期', pm.group(2)) + blk('计租天数', '%d 天（合同期整期·止租当日仍计）' % days)
        rec2 = rec.replace(mm.group(1), ins, 1)
        out.append((m.start(), rec_end, rec2))
    # 倒序应用
    for st, en, rep in reversed(out):
        seg = seg[:st] + rep + seg[en:]
        n += 1
    s = s[:a] + seg + s[b:]
    print('[rentInOrders] +起租/止租/计租天数 ×%d' % n)

io.open(P, 'wb').write(s.encode('utf-8'))
print('OK 写盘')
