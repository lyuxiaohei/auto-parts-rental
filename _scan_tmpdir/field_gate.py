# -*- coding: utf-8 -*-
"""
field_gate.py —— G38 字段闸工具（四检）
  检1 列数配平：静态表＝表头列数(colspan 计入)等于数据行格数；
              数据驱动表＝表头列数 == (勾选框?)+1(单号)+cells.length+(操作?)（noCheckbox/noOps 变体）
  检2 悬空表头：某表头列下全部数据行为空（控件格按 input value 取值；勾选格记 [cb] 不算空）
  检3 同义异名：字段名位置（th / cfg filter label / ff-label / feeCols / info label）出现禁用写法
              ＋时间粒度错配（X日期 vs 含时分值 / X时间 vs 纯日期值）
  检4 未登记字段：demo-data 实体/fields 键在 A05 无记录（按 实体.字段 去重）
豁免口径：页面脚本对 tbody 赋 innerHTML 的运行时整写表（源码种子行≠渲染结果＝源码卫生非缺陷）记入 excluded 不计问题。
用法：python field_gate.py [--proto PROTO] [--out REPORT.md] [--tag TAG]
"""
import io, os, re, sys, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PROTO = os.path.abspath(os.path.join(HERE, '..', 'P3-R01-包装租赁管理后台原型'))
TAG = 'scan'
OUT = None

args = sys.argv[1:]
i = 0
while i < len(args):
    if args[i] == '--proto': PROTO = os.path.abspath(args[i+1]); i += 2
    elif args[i] == '--out': OUT = args[i+1]; i += 2
    elif args[i] == '--tag': TAG = args[i+1]; i += 2
    else: i += 1

A05 = os.path.join(PROTO, 'P3-R01-A05-字段字典.md')
DEMO = os.path.join(PROTO, '_data', 'demo-data.js')

# ---------------- 数据装载 ----------------
def load_demo():
    cache = os.path.join(HERE, 'g38_field_gate_data.json')
    if os.path.exists(cache) and os.path.getmtime(cache) >= os.path.getmtime(DEMO):
        return json.load(io.open(cache, encoding='utf-8'))
    js = "global.window={};const fs=require('fs');eval(fs.readFileSync(%r,'utf8'));fs.writeFileSync(%r,JSON.stringify(window.DEMO_DATA));console.log(Object.keys(window.DEMO_DATA).length)" % (DEMO, cache.replace('\\', '/'))
    r = subprocess.run(['node', '-e', js], capture_output=True, text=True, shell=(os.name == 'nt'))
    if r.returncode != 0:
        raise RuntimeError('node dump failed: ' + r.stderr[:500])
    return json.load(io.open(cache, encoding='utf-8'))

DATA = load_demo()

# ---------------- A05 解析（检4） ----------------
def load_a05():
    t = io.open(A05, encoding='utf-8').read()
    secs = {}
    cur = None
    for ln in t.splitlines():
        m = re.match(r'^#{2,4} ([A-Za-z_][\w]*)[ \t·]', ln)
        if m:
            cur = m.group(1); secs.setdefault(cur, set()); continue
        if cur:
            m2 = re.match(r'^\|\s*`([\w]+)`\s*\|', ln)
            if m2: secs[cur].add(m2.group(1))
    return secs

A05SECS = load_a05()

# ---------------- 概念禁用写法（检3） ----------------
# 来源＝G38 任务书默认决策表（价格四件套/物料列/库房层级/T7 托列/裸金额）＋A05「字段概念索引」禁用写法列
FORBIDDEN_EXACT = {'单价(元)', '金额(元)'}
FORBIDDEN_SUBSTR = ['货品', '库区', '零件号', '托数', '每托数量', '入库总数', '租赁器具']
SUBSTR_EXEMPT = ['供货品类', '品类']  # 「货品」豁免：供货品类中的字面重叠

def forbidden_hits(text):
    hits = []
    s = text.strip()
    if not s: return hits
    if s in FORBIDDEN_EXACT: hits.append('裸「%s」' % s)
    for w in FORBIDDEN_SUBSTR:
        if w in s:
            if w == '货品' and any(e in s for e in SUBSTR_EXEMPT): continue
            hits.append(w)
    return hits

# ---------------- HTML 表格解析 ----------------
COLSPAN = re.compile(r'^colspan=["\']?(\d+)')
def parse_cells(seg):
    """tr 内格数（colspan 计入）与各格文本；含控件(input/select/textarea)的格记 [ctl] 非空"""
    n = 0; texts = []
    for m in re.finditer(r'<(td|th)([^>]*)>(.*?)</\1>', seg, re.S):
        attrs = m.group(2); body = m.group(3)
        cs = COLSPAN.match(attrs.strip())
        w = int(cs.group(1)) if cs else 1
        if re.search(r'type=["\']checkbox', attrs):
            txt = '[cb]'
        elif re.search(r'<(input|select|textarea)\b', body):
            vm = re.search(r'value=["\']([^"\']*)["\']', body)
            inner = re.sub(r'<[^>]+>', '', body).strip()
            txt = (vm.group(1) if (vm and vm.group(1)) else '') or inner or '[ctl]'
        else:
            txt = re.sub(r'<[^>]+>', '', body).strip()
        n += w
        texts.append(txt)
        for _ in range(w - 1): texts.append('')
    return n, texts

def iter_tables(html):
    """产出 (表起点, 表终点, ths, rows)；rows 优先取 tbody 内 tr，无 tbody 则取 thead 后的松散 tr"""
    for tm in re.finditer(r'<table\b[^>]*>.*?</table>', html, re.S):
        seg = tm.group(0)
        ths = []; rows = []
        hm = re.search(r'<thead\b[^>]*>(.*?)</thead>', seg, re.S)
        if hm:
            for trm in re.finditer(r'<tr\b[^>]*>(.*?)</tr>', hm.group(1), re.S):
                _, texts = parse_cells(trm.group(1))
                ths = texts
        body_part = hm.end() if hm else seg.find('>') + 1
        body_seg = seg[body_part:]
        bm_all = re.search(r'<tbody\b[^>]*>(.*?)</tbody>', body_seg, re.S)
        if bm_all:
            for trm in re.finditer(r'<tr\b[^>]*>(.*?)</tr>', bm_all.group(1), re.S):
                n, texts = parse_cells(trm.group(1))
                rows.append((n, texts))
        else:
            for trm in re.finditer(r'<tr\b[^>]*>(.*?)</tr>', body_seg, re.S):
                n, texts = parse_cells(trm.group(1))
                rows.append((n, texts))
        yield tm.start(), tm.end(), ths, rows

def parse_cfgs(html):
    cfgs = []
    for m in re.finditer(r'renderListPage\(\{', html):
        i = m.end() - 1; depth = 0; j = i
        while j < len(html):
            if html[j] == '{': depth += 1
            elif html[j] == '}':
                depth -= 1
                if depth == 0: break
            j += 1
        blk = html[i:j+1]
        cfg = {}
        em = re.search(r"entity:\s*'([\w]+)'", blk)
        if em: cfg['entity'] = em.group(1)
        cfg['noCheckbox'] = bool(re.search(r'\bnoCheckbox:\s*true', blk))
        cfg['noOps'] = bool(re.search(r'\bnoOps:\s*true', blk))
        sm = re.search(r"tbodySel:\s*'([^']+)'", blk)
        if sm: cfg['tbodySel'] = sm.group(1)
        cfg['filters'] = re.findall(r"label:\s*'([^']+)'(?:[^}]*?field:\s*'([\w]+)')?", blk)
        cfgs.append(cfg)
    return cfgs

def tbody_sel_position(html, sel):
    if not sel or sel == 'tbody': return html.find('<tbody')
    m = re.match(r'#([\w-]+)\s+tbody', sel)
    if not m: return html.find('<tbody')
    idm = re.search(r'id=["\']%s["\']' % re.escape(m.group(1)), html)
    if not idm: return html.find('<tbody')
    return html.find('<tbody', idm.end())

# ---------------- 主扫描 ----------------
problems = {1: [], 2: [], 3: [], 4: []}
excluded = []

def flag_time_grain(rel, label, vals):
    lab = label.strip().rstrip('：:')
    if not lab: return
    has_hm = any(re.search(r'\d{1,2}:\d{2}', v) for v in vals)
    all_date = all(re.fullmatch(r'\d{4}-\d{2}-\d{2}', v.strip()[:10]) and len(v.strip()) <= 10 for v in vals)
    if lab.endswith('日期') and has_hm:
        problems[3].append((rel, '时间粒度错配：标签「%s」（日期）但值含时分 %s' % (lab, vals[0])))
    elif lab.endswith('时间') and all_date and not has_hm:
        problems[3].append((rel, '时间粒度错配：标签「%s」（时间）但值为纯日期 %s' % (lab, vals[0])))

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', str(s)).strip()

n_pages = 0; n_tables = 0; n_driven = 0; n_static = 0

for root, ds, fs in os.walk(PROTO):
    ds[:] = [d for d in ds if d not in ('node_modules',)]
    for f in sorted(fs):
        if not f.endswith('.html'): continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, PROTO).replace('\\', '/')
        n_pages += 1
        html = io.open(path, encoding='utf-8').read()
        cfgs = parse_cfgs(html)

        # 运行时整写 tbody 检测（innerHTML 赋值前缀 80 字符内含 tbody）
        page_rewrites_tb = any(
            'tbody' in html[max(0, m.start() - 80):m.start()].lower()
            for m in re.finditer(r'\.innerHTML\s*=', html))

        tables = list(iter_tables(html))
        tb_positions = []   # (tbody 文档位置, 表序, ths, rows)
        for ti, (tstart, tend, ths, rows) in enumerate(tables):
            for bm in re.finditer(r'<tbody\b[^>]*>', html[tstart:tend]):
                tb_positions.append((tstart + bm.start(), ti, ths, rows))

        target_pos = []
        driven_th_labels = set()   # 数据驱动表 th 文本（列检已覆盖同名标签的时间粒度）
        for cfg in cfgs:
            if not cfg.get('entity'): continue
            p = tbody_sel_position(html, cfg.get('tbodySel'))
            if p >= 0: target_pos.append((p, cfg))
        target_pos.sort()
        driven_map = {}   # tbody位置 -> cfg
        for p, cfg in target_pos:
            cand = [t for t in tb_positions if t[0] >= p]
            if cand: driven_map[cand[0][0]] = cfg

        for tpos, ti, ths, rows in tb_positions:
            if not ths: continue
            n_tables += 1
            thead_n = len(ths)
            if tpos in driven_map:
                n_driven += 1
                cfg = driven_map[tpos]
                ent = cfg.get('entity')
                if ent not in DATA: continue
                rowsd = [v['row'] for v in DATA[ent].values() if isinstance(v, dict) and v.get('row')]
                if not rowsd: continue
                exp = (0 if cfg['noCheckbox'] else 1) + 1 + len(rowsd[0]['cells']) + (0 if cfg['noOps'] else 1)
                if thead_n != exp:
                    problems[1].append((rel, '数据驱动表 %s：表头 %d 列 ≠ 公式 %d（勾%d+单号1+cells%d+操%d）' % (ent, thead_n, exp, 0 if cfg['noCheckbox'] else 1, len(rowsd[0]['cells']), 0 if cfg['noOps'] else 1)))
                lens = set(len(r['cells']) for r in rowsd)
                if len(lens) > 1:
                    problems[1].append((rel, '数据驱动表 %s：cells 长度不齐 %s' % (ent, sorted(lens))))
                off = 0 if cfg['noCheckbox'] else 1
                for ci in range(len(rowsd[0]['cells'])):
                    idx = off + 1 + ci
                    vals = [str(r['cells'][ci]) for r in rowsd if len(r['cells']) > ci]
                    if vals and all(strip_tags(v) == '' for v in vals):
                        hname = ths[idx] if idx < len(ths) else '?'
                        problems[2].append((rel, '数据驱动表 %s 列「%s」全部数据行为空' % (ent, hname)))
                    if idx < len(ths):
                        sv = [strip_tags(v) for v in vals if strip_tags(v)]
                        if sv: flag_time_grain(rel, ths[idx], sv)
                        hl = (ths[idx] or '').strip().rstrip('：:')
                        if hl: driven_th_labels.add(hl)
            else:
                if page_rewrites_tb and rows and all(n != thead_n for n, _ in rows):
                    excluded.append((rel, '表 #%d 种子行 %s 格 ≠ 表头 %d（运行时 innerHTML 整写·源码卫生豁免）' % (ti, [n for n, _ in rows][:3], thead_n)))
                    continue
                n_static += 1
                for rn, texts in rows:
                    if rn == 0: continue
                    if rn != thead_n:
                        problems[1].append((rel, '静态表 #%d：表头 %d 列 ≠ 行格数 %d（行首格「%s」）' % (ti, thead_n, rn, (texts[0] or '')[:14])))
                if rows:
                    for ci in range(min(thead_n, max((len(t) for _, t in rows), default=0))):
                        col_vals = [(texts[ci] if ci < len(texts) else '') for _, texts in rows]
                        if col_vals and all((v or '').strip() in ('', '[cb]') for v in col_vals):
                            if ths[ci].strip() == '' and '[cb]' in col_vals: continue  # 勾选列
                            problems[2].append((rel, '静态表 #%d 列「%s」全部数据行为空' % (ti, (ths[ci] or '').strip() or '(空)')))
                    for ci in range(thead_n):
                        h = (ths[ci] or '').strip()
                        if not h: continue
                        vals = [texts[ci] for _, texts in rows if ci < len(texts) and (texts[ci] or '').strip()]
                        vals = [v for v in vals if v != '[cb]']
                        if vals: flag_time_grain(rel, h, vals)

        # 检3：th 文本禁用写法
        for tstart, tend, ths, rows in tables:
            for h in ths:
                for hit in forbidden_hits(h):
                    problems[3].append((rel, 'th「%s」命中禁用写法：%s' % (h.strip(), hit)))
        for m in re.finditer(r'class="ff-label">([^<]+)<', html):
            for hit in forbidden_hits(m.group(1)):
                problems[3].append((rel, '筛选标签「%s」命中禁用写法：%s' % (m.group(1).strip(), hit)))
        for cfg in cfgs:
            for lab, fld in cfg['filters']:
                for hit in forbidden_hits(lab):
                    problems[3].append((rel, 'cfg 标签「%s」命中禁用写法：%s' % (lab, hit)))
                if fld and cfg.get('entity') in DATA:
                    lab_key = lab.strip().rstrip('：:')
                    if lab_key in driven_th_labels:
                        continue  # 同名 th 已按列值判粒度（cells 为准）
                    vals = [v['row']['fields'].get(fld) for v in DATA[cfg['entity']].values() if isinstance(v, dict) and v.get('row')]
                    vals = [str(v) for v in vals if v]
                    if vals: flag_time_grain(rel, lab, vals)

# demo-data 侧检3：feeCols / info label / fees 时间粒度
for ent, recs in DATA.items():
    if ent == '_meta' or not isinstance(recs, dict): continue
    for key, rec in recs.items():
        if not isinstance(rec, dict): continue
        for c in rec.get('feeCols', []) or []:
            for hit in forbidden_hits(c):
                problems[3].append(('demo-data:%s' % ent, 'feeCols「%s」命中禁用写法：%s（%s）' % (c, hit, key)))
        for info in rec.get('info', []) or []:
            lab = info.get('label', '')
            for hit in forbidden_hits(lab):
                problems[3].append(('demo-data:%s' % ent, 'info 标签「%s」命中禁用写法：%s（%s）' % (lab, hit, key)))
            txt = str(info.get('text', ''))
            if txt: flag_time_grain('demo-data:%s' % ent, lab, [txt])
        fees = rec.get('fees') or []
        cols = rec.get('feeCols') or []
        if fees and cols:
            for ci, c in enumerate(cols):
                vals = [f.get('cells', [])[ci] for f in fees if len(f.get('cells', [])) > ci]
                vals = [str(v) for v in vals if v]
                if vals: flag_time_grain('demo-data:%s' % ent, c, vals)

# 检4：未登记字段（按 实体.字段 去重）
for ent, recs in sorted(DATA.items()):
    if ent == '_meta' or not isinstance(recs, dict): continue
    if ent not in A05SECS:
        problems[4].append(('demo-data:%s' % ent, '实体在 A05 无章节'))
        continue
    regd = A05SECS[ent]
    miss = set()
    for key, rec in recs.items():
        if not isinstance(rec, dict): continue
        row = rec.get('row')
        if not row: continue
        for f in (row.get('fields') or {}):
            if f not in regd: miss.add(f)
    for f in sorted(miss):
        problems[4].append(('demo-data:%s' % ent, '字段 `%s` 未登记 A05' % f))

# ---------------- 输出 ----------------
def uniq(seq):
    seen = set(); out = []
    for x in seq:
        if x not in seen: seen.add(x); out.append(x)
    return out

for k in problems: problems[k] = uniq(problems[k])
excluded = uniq(excluded)

c1, c2, c3, c4 = len(problems[1]), len(problems[2]), len(problems[3]), len(problems[4])
lines = []
lines.append('# G38 field_gate 全站扫描报告（%s）' % TAG)
lines.append('')
lines.append('- 扫描范围：%d HTML 页 · %d 张带表头表（数据驱动 %d / 静态 %d）· demo-data 实体 %d · A05 实体节 %d' % (
    n_pages, n_tables, n_driven, n_static, len([e for e in DATA if e != '_meta']), len(A05SECS)))
lines.append('- 汇总：**检1 列数配平 %d ｜ 检2 悬空表头 %d ｜ 检3 同义异名 %d ｜ 检4 未登记字段 %d**（运行时整写豁免 %d 表）' % (c1, c2, c3, c4, len(excluded)))
lines.append('')
names = {1: '检1 · 列数配平', 2: '检2 · 悬空表头', 3: '检3 · 同义异名（禁用写法＋时间粒度）', 4: '检4 · 未登记字段'}
for k in (1, 2, 3, 4):
    lines.append('## %s —— %d 项' % (names[k], len(problems[k])))
    lines.append('')
    if not problems[k]:
        lines.append('（无）')
    for src, desc in problems[k]:
        lines.append('- `%s` %s' % (src, desc))
    lines.append('')
lines.append('## 运行时整写豁免（源码卫生·非缺陷） —— %d 表' % len(excluded))
lines.append('')
for src, desc in excluded:
    lines.append('- `%s` %s' % (src, desc))
lines.append('')

report = '\n'.join(lines)
if OUT:
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(report)
    print('[field_gate:%s] 写出 %s' % (TAG, OUT))
print('[field_gate:%s] 页 %d · 表 %d（驱动 %d/静态 %d）· 检1 %d · 检2 %d · 检3 %d · 检4 %d · 豁免 %d' % (
    TAG, n_pages, n_tables, n_driven, n_static, c1, c2, c3, c4, len(excluded)))
sys.exit(0)
