# -*- coding: utf-8 -*-
"""G11-B1 补充：日期缺位元词复核（可靠版·剥离注入后扫 演示/示例/待确认/预留/并入/改挂）"""
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
F01 = 'P3-R01-F01-业务流程导航图.html'

def strip_annotation(s):
    i = s.find('<style id="proto-notes-style">')
    if i >= 0:
        k = s.find('<script id="proto-notes-js">', i)
        if k > i:
            end = s.find('</script>', k) + len('</script>')
            mid = s[i:end]
            assert 'proto-pins' in mid and 'protoNotesFab' in mid
            s = s[:i] + s[end:]
        else:
            j = s.find('</style>', i)
            s = s[:i] + s[j + len('</style>'):]
    return re.sub(r'\s*data-note="\d+"', '', s)

RX = re.compile(r'演示|示例|待确认|预留|并入|改挂|挂靠|第[一二三]期|第一期')
for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('_data', '弹窗') and not d.startswith('backup')]
    for f in sorted(files):
        if not f.endswith('.html') or f == F01:
            continue
        p = os.path.join(root, f)
        s = strip_annotation(open(p, encoding='utf-8').read())
        assert 'proto-pins' not in s and 'proto-notes-js' not in s, p
        for m in RX.finditer(s):
            ln = s[:m.start()].count('\n') + 1
            line = s.split('\n')[ln - 1].strip()
            print(f"{os.path.relpath(p, ROOT)}|L{ln}|{m.group(0)}|{line[:150]}")
