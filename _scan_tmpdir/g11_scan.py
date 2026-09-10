# -*- coding: utf-8 -*-
"""G11-B1: 38 业务页元注释污染全量扫描（只读）→ g11-meta-scan.json；弹窗 69 页登记 → g11-modal-scan.md
口径：剥离标注层注入块（style#proto-notes-style 起 至 </body> 前）与 data-note 属性后，扫页面本体。
污染模式（G11 文档 C 表）：①日期+会议/拍板/纪要/决策/确认 ②G任务号 ③原..并入/改挂/随..删除/移除 ④FP/REQ 编号 ⑤标题括号尾巴/★ ⑥pn-hint 全文审查
"""
import os, re, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
OUTD = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir"
F01 = 'P3-R01-F01-业务流程导航图.html'

RE_DATE = re.compile(r'20\d{2}-\d{2}-\d{2}')
META_WORDS = ('会议', '拍板', '纪要', '决策', '道远', '王琳', '沟通')
RE_G = re.compile(r'(?<![A-Za-z0-9])G[012]\d(?![0-9])')
RE_TRACE = re.compile(r'原.{0,12}(?:并入|改挂|移除|删除)|原.{0,12}随.{0,8}(?:删除|移除)')
RE_FP = re.compile(r'(?<![A-Za-z0-9-])(?:FP\d|REQ-?\d)')
RE_TITLE = re.compile(
    r'<(h[123]|th|div|span)[^>]*?(?:class="([^"]*)"|data-note="?\d"?)?[^>]*>((?:[^<]|(?!<))*)</\1>')
TAIL_META = re.compile(r'20\d{2}-\d{2}|G[012]\d|原.{0,12}(?:并入|改挂|移除|删除)|会议|拍板|口径|演示|示例|数据源|v\d\.\d|FP\d|REQ-?\d|待确认 #|决策')

def strip_annotation(s):
    i = s.find('<style id="proto-notes-style">')
    if i >= 0:
        k = s.find('<script id="proto-notes-js">', i)
        if k > i:
            # 完整注入四件（style/pins/fab/script）连续，整体剥离
            end = s.find('</script>', k)
            assert end > k, '注入 script 未闭合'
            end += len('</script>')
            mid = s[i:end]
            assert 'proto-pins' in mid and 'protoNotesFab' in mid, '注入块内缺件'
            s = s[:i] + s[end:]
        else:
            # 弹窗模板部分注入形态（仅 style+data-note，无 pins/fab/script）：只剥 style
            j = s.find('</style>', i)
            assert j > i, '注入 style 未闭合'
            s = s[:i] + s[j + len('</style>'):]
    s = re.sub(r'\s*data-note="\d+"', '', s)
    return s

def ctx_of(line):
    if '<!--' in line:
        return 'html-comment'
    if '/*' in line or line.lstrip().startswith('*'):
        return 'js-css-comment'
    if 'pn-hint' in line:
        return 'pn-hint'
    m = re.match(r'\s*<(\w+)([^>]*)>', line)
    if m:
        cls = re.search(r'class="([^"]*)"', m.group(2))
        return f'tag:{m.group(1)}' + (f'.{cls.group(1).split()[0]}' if cls else '')
    return 'text'

def scan_page_text(txt, rel):
    hits = []
    lines = txt.split('\n')
    seen = set()
    for ln, line in enumerate(lines, 1):
        if not line.strip():
            continue
        kinds = []
        if RE_DATE.search(line) and any(w in line for w in META_WORDS):
            kinds.append('P1-date+meta')
        if RE_G.search(line):
            kinds.append('P2-Gnum')
        if RE_TRACE.search(line):
            kinds.append('P3-trace')
        if RE_FP.search(line):
            kinds.append('P4-FP/REQ')
        if '★' in line:
            kinds.append('P5-star')
        if not kinds:
            continue
        key = (ln, tuple(kinds))
        hits.append({'page': rel, 'line': ln, 'kinds': kinds, 'ctx': ctx_of(line),
                     'text': line.strip()[:220]})
    # pn-hint 全文审查（含无关键字的，交 B2 定案）
    for m in re.finditer(r'<div class="pn-hint"[^>]*>(.*?)</div>', txt, re.S):
        t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        line_no = txt[:m.start()].count('\n') + 1
        meta = bool(RE_DATE.search(t) or RE_G.search(t) or RE_TRACE.search(t)
                    or RE_FP.search(t) or TAIL_META.search(t))
        hits.append({'page': rel, 'line': line_no, 'kinds': ['P6-pnhint' + ('/meta' if meta else '/clean')],
                     'ctx': 'pn-hint', 'text': t[:220]})
    # 标题括号尾巴（th/h1/h2/h3/card-title）
    for m in re.finditer(r'<(h[123]|th)([^>]*)>([^<]*)</\1>', txt):
        label = m.group(3)
        if '（' in label and '）' in label:
            tail = label[label.find('（'):]
            if len(tail) <= 40 and TAIL_META.search(tail):
                line_no = txt[:m.start()].count('\n') + 1
                hits.append({'page': rel, 'line': line_no, 'kinds': ['P5-title-tail'],
                             'ctx': f'tag:{m.group(1)}', 'text': label.strip()[:220]})
    for m in re.finditer(r'<div[^>]*class="[^"]*card-title[^"]*"[^>]*>([^<]*)</div>', txt):
        label = m.group(1)
        if '（' in label:
            tail = label[label.find('（'):]
            if len(tail) <= 40 and TAIL_META.search(tail):
                line_no = txt[:m.start()].count('\n') + 1
                hits.append({'page': rel, 'line': line_no, 'kinds': ['P5-title-tail'],
                             'ctx': 'tag:div.card-title', 'text': label.strip()[:220]})
    return hits

biz, modals = [], []
for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('_data',) and not d.startswith('backup')]
    for f in sorted(files):
        if not f.endswith('.html'):
            continue
        p = os.path.join(root, f)
        rel = os.path.relpath(p, ROOT).replace(chr(92), '/')
        if f == F01:
            continue
        raw = open(p, encoding='utf-8').read()
        txt = strip_annotation(raw)
        hits = scan_page_text(txt, rel)
        if '/弹窗/' in rel:
            modals.append({'page': rel, 'hits': hits})
        else:
            biz.extend(hits)

json.dump({'scope': '38 业务页（F01 豁免·弹窗仅登记）', 'business_hits': biz},
          open(os.path.join(OUTD, 'g11-meta-scan.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

# 弹窗登记 md
n_mod_hit = sum(len(m['hits']) for m in modals)
with open(os.path.join(OUTD, 'g11-modal-scan.md'), 'w', encoding='utf-8') as fh:
    fh.write('# G11 弹窗模板扫描登记（69 页·仅登记不改）\n\n')
    fh.write(f'命中行总数 {n_mod_hit}（弹窗本任务不改动，登记备查；命中不进入业务页清除范围）\n\n')
    for m in modals:
        if m['hits']:
            fh.write(f"## {m['page']}（{len(m['hits'])} 处）\n")
            for h in m['hits']:
                fh.write(f"- L{h['line']} {','.join(h['kinds'])} [{h['ctx']}] {h['text'][:120]}\n")
            fh.write('\n')

print(f'业务页命中 {len(biz)} 条（含 pn-hint clean 登记）')
print(f'弹窗页命中 {n_mod_hit} 条 → g11-modal-scan.md')
ex = [h for h in biz if '原在租台账' in h['text'] or '客户虚拟仓' in h['text']]
print(f'需求原文示例行在列: {len(ex)} 条')
for h in ex[:4]:
    print('  EX|', h['page'], h['kinds'], h['text'][:80])
