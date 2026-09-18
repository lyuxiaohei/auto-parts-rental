# -*- coding: utf-8 -*-
import re

OLD = ('<style id="f01-fab-style">.f01-fab{position:fixed;right:12px;bottom:12px;z-index:1001;display:flex;align-items:center;'
       'height:24px;padding:0 10px;border-radius:4px;background:#fff;border:1px solid #d9d9d9;color:#8c8c8c;font-size:11px;'
       "font-family:-apple-system,'Segoe UI','Microsoft YaHei',sans-serif;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.06);"
       'opacity:.6;transition:opacity .15s}.f01-fab:hover{opacity:1;border-color:#722ed1;color:#722ed1}</style>')
LINK = '<a class="f01-fab" href="../P3-R01-F01-业务流程导航图.html">流程图</a>'
STRAY = '<div class="pn-fab" id="protoNotesFab">标注</div>'

pages = ['租入管理/租入入库列表.html', '租入管理/租入单列表.html', '租入管理/租入单新建.html',
         '租入管理/租入归还列表.html', '租入管理/租入归还新建.html', '仓储作业/库存调拨列表.html',
         '系统管理/权限配置.html']

for pg in pages:
    t = open(pg, encoding='utf-8').read()
    lns = t.split('\n')
    ix = {}
    for i, ln in enumerate(lns):
        s = ln.strip()
        if s == OLD: ix.setdefault('独立样式行', []).append(i + 1)
        if s == LINK: ix.setdefault('独立链接行', []).append(i + 1)
        if s == STRAY: ix.setdefault('游离fab行', []).append(i + 1)
    fabrow_lines = [i + 1 for i, ln in enumerate(lns) if '<div class="fab-row">' in ln]
    # fab 行内嵌旧样式确认
    emb = [i + 1 for i, ln in enumerate(lns) if OLD in ln and ln.strip() != OLD]
    print(pg, '->', ix, 'fab行:', fabrow_lines, '内嵌旧行:', emb)

# 输出两段样式全文（供 Edit 用）
print()
print('=== OLD (%d chars) ===' % len(OLD))
print(OLD)
c = open('../_scan_tmpdir/g52_canon_style.txt', encoding='utf-8').read()
print('=== CANON (%d chars) ===' % len(c))
print(c)
