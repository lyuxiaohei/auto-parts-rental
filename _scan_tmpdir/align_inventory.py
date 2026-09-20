# -*- coding: utf-8 -*-
"""全站列表页盘点（只读）：带 .table-wrap+thead 的页面 → 表头清单/渲染方式/锚点形态"""
import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
rows = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules')]
    for f in files:
        if not f.endswith('.html'):
            continue
        p = os.path.join(root, f).replace(os.sep, '/')
        if '/mobile/' in p or 'F01-' in f or '/弹窗/' in p:
            continue
        try:
            s = open(p, encoding='utf-8').read()
        except Exception:
            continue
        if '.table-wrap' not in s or '<thead>' not in s:
            continue
        m = re.search(r'<thead>(.*?)</thead>', s, re.S)
        first = re.findall(r'<th[^>]*>([^<]*)</th>', m.group(1)) if m else []
        colspan = 'colspan' in (m.group(1).lower() if m else '')
        nwrap = s.count('class="table-wrap"')
        rl = 'renderListPage' in s
        if '../_data/notes-data.js' in s:
            anchor = '..'
        elif '_data/notes-data.js' in s:
            anchor = 'root'
        else:
            anchor = 'NO-NOTES'
        rows.append((p, nwrap, rl, colspan, anchor, first))
print('TOTAL', len(rows))
for p, nw, rl, cs, an, first in sorted(rows):
    print(f'{p} | wrap:{nw} RL:{"Y" if rl else "n"} cs:{"Y" if cs else "-"} anc:{an} | ' + '|'.join(t.strip() for t in first))
