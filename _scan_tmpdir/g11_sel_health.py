# -*- coding: utf-8 -*-
"""G11-B4 前置：A03/A04 全量 selector 健康体检（miss/ambiguous/replaced/页面不存在）"""
import json, re, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"

def find_block_end(html, start, tag):
    pat = re.compile(r'<' + tag + r'\b|</' + tag + r'\s*>', re.I)
    d, p = 0, start
    while True:
        m = pat.search(html, p)
        if m is None:
            return html.find('>', start) + 1
        d += 1 if not m.group(0).startswith('</') else -1
        p = m.end()
        if d == 0:
            return p

def strip_injected(html):
    for tag, marker in (('style', 'id="proto-notes-style"'), ('div', 'id="proto-pins"'), ('script', 'id="proto-notes-js"')):
        while marker in html:
            i = html.find(marker)
            s = html.rfind('<' + tag, 0, i)
            e = find_block_end(html, s, tag)
            html = html[:s] + html[e:]
    html = re.sub(r'\s*data-note="\d+"', '', html)
    html = re.sub(r'\s*pn-flash(?=["\s>])', '', html)
    return html

for name in ('P3-R01-A03-标注数据.json', 'P3-R01-A04-流程链标注数据.json'):
    data = json.load(open(os.path.join(ROOT, name), encoding='utf-8'))
    pages = {k: v for k, v in data.items() if not k.startswith('_')}
    print(f'==== {name}: {len(pages)} 页键 ====')
    miss = amb = rep = gone = ok = 0
    for rel, items in sorted(pages.items()):
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            print(f'  页面不存在: {rel} ({len(items)} 条)')
            gone += len(items)
            continue
        html = strip_injected(open(p, encoding='utf-8').read())
        for it in items:
            n = html.count(it['selector'])
            if n == 0:
                print(f"  MISS {rel} #{it['id']} {it['selector'][:60]}")
                miss += 1
            elif re.match(r'<(input|img|br|hr|textarea)\b', it['selector'], re.I):
                print(f"  REPLACED {rel} #{it['id']} {it['selector'][:60]}")
                rep += 1
            elif n > 1:
                print(f"  AMBIG {rel} #{it['id']} x{n} {it['selector'][:60]}")
                amb += 1
            else:
                ok += 1
    print(f'  小计: ok={ok} miss={miss} ambiguous={amb} replaced={rep} 页面不存在条目={gone}')
