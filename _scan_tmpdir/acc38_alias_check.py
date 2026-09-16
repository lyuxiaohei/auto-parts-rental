# -*- coding: utf-8 -*-
# acc38 独立验收·第2项 异名清零复验（只读扫描）
# 全站 HTML + _data/demo-data.js 的 str.count；字段名位置（th/ff-label/cfg label/feeCols/info label）正则实读
import io, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PROTO = os.path.abspath(os.path.join(ROOT, '..', 'P3-R01-包装租赁管理后台原型'))

files = []
for dirpath, dirnames, filenames in os.walk(PROTO):
    # 排除任何 backup 目录（防误入）
    dirnames[:] = [d for d in dirnames if not d.startswith('backup')]
    for fn in filenames:
        if fn.lower().endswith('.html'):
            files.append(os.path.join(dirpath, fn))
DEMO = os.path.join(PROTO, '_data', 'demo-data.js')
files.append(DEMO)

WORDS = ['货品', '入库库区', '出库库区', '调出库区', '调入库区', '库区', '零件号',
         '托数', '每托数量', '入库总数', '到货托数', '以托为单位', '租赁器具']

def load(p):
    return io.open(p, encoding='utf-8').read()

# ---------- A. 全文 str.count（含值文本，供定位白名单） ----------
print('== A. 全文 str.count（HTML+demo-data，词 -> 总次数；0 不打印） ==')
total = {w: 0 for w in WORDS}
hits = {w: [] for w in WORDS}
for p in files:
    t = load(p)
    for w in WORDS:
        c = t.count(w)
        if c:
            total[w] += c
            hits[w].append((os.path.relpath(p, PROTO), c))
for w in WORDS:
    if total[w] == 0:
        print('  %-6s -> 0' % w)
    else:
        det = '; '.join('%s×%d' % (f, c) for f, c in hits[w][:12])
        print('  %-6s -> %d   [%s]' % (w, total[w], det))

# ---------- B. 字段名位置正则实读（必须为 0） ----------
print()
print('== B. 字段名位置实读（th 文本 / ff-label / cfg label / feeCols / info label） ==')
re_th = re.compile(r'<th[^>]*>(.*?)</th>', re.S | re.I)
re_fflabel = re.compile(r'class="ff-label"[^>]*>(.*?)<', re.S | re.I)
re_cfglabel = re.compile(r"label\s*:\s*'([^']*)'", re.S)
re_infolabel = re.compile(r'["\']label["\']\s*:\s*["\']([^"\']*)["\']')
# 值文本白名单（demo-data 中允许的值）
VALUE_OK = ('租赁器具不零售', '供货品类')

bad = []
for p in files:
    if not p.lower().endswith('.html'):
        continue
    t = load(p)
    rel = os.path.relpath(p, PROTO)
    spans = []  # (位置类别, 起始, 结束, 文本)
    for m in re_th.finditer(t):
        spans.append(('th', m.start(), m.end(), m.group(1)))
    for m in re_fflabel.finditer(t):
        spans.append(('ff-label', m.start(), m.end(), m.group(1)))
    for m in re_cfglabel.finditer(t):
        spans.append(('cfg.label', m.start(), m.end(), m.group(1)))
    for m in re_infolabel.finditer(t):
        spans.append(('info.label', m.start(), m.end(), m.group(1)))
    for cat, s, e, txt in spans:
        clean = re.sub(r'<[^>]+>', '', txt)
        clean = re.sub(r'\s+', '', clean)
        for w in WORDS:
            if w in clean:
                bad.append('%s [%s] %r 含 %r' % (rel, cat, clean[:40], w))

if bad:
    for b in bad:
        print('  BAD ' + b)
    print('  字段名位置命中数 =', len(bad))
else:
    print('  字段名位置命中数 = 0  （th/ff-label/cfg label/info label 全部无禁用词）')

# ---------- C. demo-data 值文本白名单核对 ----------
print()
print('== C. demo-data 值文本核对 ==')
dt = load(DEMO)
wl1 = dt.count('租赁器具不零售')
print('  「租赁器具不零售」出现次数 =', wl1, '（登记白名单，预期 10）')
# demo-data 中除白名单外是否还有「租赁器具」/「货品」/「库区」等
for w in WORDS:
    if w == '租赁器具':
        rest = dt.count(w) - wl1
    else:
        rest = dt.count(w)
    # 货品白名单：供货品类
    if w == '货品':
        rest = dt.count(w) - dt.count('供货品类')
    print('  demo-data 中 %-6s 去白名单后 = %d' % (w, rest))

# ---------- D. 白名单上下文打印（「库区」「货品」残留处上下文） ----------
print()
print('== D. 残留上下文（非字段名位置·人工核对用） ==')
for p in files:
    t = load(p)
    rel = os.path.relpath(p, PROTO)
    for w in ['库区', '货品', '租赁器具', '托数', '零件号', '以托为单位']:
        for m in re.finditer(re.escape(w), t):
            ctx = t[max(0, m.start()-60):m.end()+60].replace('\n', ' ').replace('\r', '')
            print('  [%s] %s …%s…' % (rel, w, ctx))
print('== done ==')
