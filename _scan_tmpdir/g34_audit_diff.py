# -*- coding: utf-8 -*-
"""G34 验证门：audit 复跑（128 页）vs g33baseline 逐键 diff
判定：①post=128 页 ②既有页 problems 逐键新增 0 ③全站死链 0 ④JS 错 0（F01 断网豁免沿 G17 预注）
G34 零文件改名/增删 → 无 RENAMES 映射
"""
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
OUT = Path(__file__).resolve().parent
base = json.load(open(OUT / 'audit_results_g33baseline.json', encoding='utf-8'))
post = json.load(open(OUT / 'audit_results.json', encoding='utf-8'))

def pkey(p):
    w = p.get('where') or {}
    return '|'.join([str(p.get('cat','')), str(p.get('type','')), str(w.get('tag','')), str(w.get('id','')), str(w.get('row',''))[:24], str(w.get('text',''))[:16], str(p.get('detail',''))[:24]])

basemap = {}
for r in base:
    basemap.setdefault(r['page'].replace('\\', '/'), set()).update(pkey(p) for p in r['problems'])

new_probs, new_dl, new_js, exempt = [], [], [], []
tot_dl = tot_js = tot_prob = 0
mobile = [r for r in post if r['page'].replace('/', '\\').startswith('mobile\\')]
pc = [r for r in post if not r['page'].replace('/', '\\').startswith('mobile\\')]

for r in post:
    page = r['page'].replace('\\', '/')
    tot_prob += len(r['problems'])
    for p in r['problems']:
        k = pkey(p)
        if k not in basemap.get(page, set()):
            new_probs.append((page, k))
    tot_dl += len(r['dead_links'])
    new_dl += [(page, d) for d in r['dead_links']]
    for e in r['js_errors']:
        tot_js += 1
        if 'ERR_CONNECTION_' in e.get('text',''):
            exempt.append((page, e['text'][:80]))
        else:
            new_js.append((page, e['text'][:100]))

print(f"基线页数: {len(base)} ｜ post 页数: {len(post)}（PC {len(pc)} + mobile {len(mobile)}）")
print(f"全站问题合计: {tot_prob} ｜ 死链合计: {tot_dl} ｜ JS 错合计: {tot_js}（断网豁免 {len(exempt)} 条；非豁免 {len(new_js)}）")
for pg, t in exempt[:5]: print("  [豁免]", pg, t)
for pg, t in new_js[:10]: print("  [JS新增]", pg, t)
print(f"相对 g33baseline 逐键新增 problems: {len(new_probs)}")
for pg, k in new_probs[:15]: print("  [新增]", pg, '::', k)
print(f"相对 g33baseline 逐键新增 dead_links: {len(new_dl)}")
for pg, d in new_dl[:10]: print("  [死链新增]", pg, d)

ok = (len(post) == 128 and len(new_probs) == 0 and tot_dl == 0 and len(new_js) == 0)
print('G34 AUDIT GATE:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
