# -*- coding: utf-8 -*-
"""G13 验证门 1：audit 复跑结果 vs g13baseline 逐键 diff（新增问题须 0；F01 ERR_CONNECTION_CLOSED 断网豁免预注）"""
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
OUT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir")
base = json.load(open(OUT / 'audit_results_g13baseline.json', encoding='utf-8'))
post = json.load(open(OUT / 'audit_results.json', encoding='utf-8'))

def pkey(p):
    w = p.get('where') or {}
    return '|'.join([str(p.get('cat','')), str(p.get('type','')), str(w.get('tag','')), str(w.get('id','')), str(w.get('row',''))[:24], str(w.get('text',''))[:16], str(p.get('detail',''))[:24]])

def jkey(e):
    return e.get('text','')[:120]

basemap = {}
for r in base:
    basemap.setdefault(r['page'], set()).update(pkey(p) for p in r['problems'])
new_probs, new_dl, new_js = [], [], []
tot_dl = tot_js = 0
exempt = []
for r in post:
    page = r['page']
    for p in r['problems']:
        if pkey(p) not in basemap.get(page, set()):
            new_probs.append((page, pkey(p)))
    tot_dl += len(r['dead_links'])
    new_dl += [(page, d) for d in r['dead_links']]
    for e in r['js_errors']:
        tot_js += 1
        if 'ERR_CONNECTION_CLOSED' in e.get('text',''):
            exempt.append((page, e['text'][:80]))
        else:
            new_js.append((page, e['text'][:100]))

print(f"post 页数: {len(post)}")
print(f"死链合计: {tot_dl}（新增 {len(new_dl)}）")
print(f"JS 错合计: {tot_js}（豁免 F01 外链断网 {len(exempt)} 条；其余新增 {len(new_js)}）")
for pg, t in exempt[:5]: print("  [豁免]", pg, t)
for pg, t in new_js[:10]: print("  [JS新增]", pg, t)
print(f"problems 逐键新增: {len(new_probs)}")
for pg, k in new_probs[:20]: print("  [新增]", pg, '|', k)
ok = len(post) == 108 and tot_dl == 0 and len(new_js) == 0 and len(new_probs) == 0
print('\n==== audit 门：', 'PASS（108 页·死链0·JS0·diff 新增 0）====' if ok else 'FAIL ====')
sys.exit(0 if ok else 1)
