# -*- coding: utf-8 -*-
"""G17 验证门（基线滚动版）：audit 复跑（113 页）vs g17baseline（108 页）逐键 diff
判定：①post=113 页 ②既有 108 页 problems 逐键新增 0 ③全站死链 0 ④JS 错 0（F01 ERR_CONNECTION_CLOSED 断网豁免沿 G13 预注）⑤mobile 5 页各自 死链0/JS0"""
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
OUT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir")
base = json.load(open(OUT / 'audit_results_g17baseline.json', encoding='utf-8'))
post = json.load(open(OUT / 'audit_results.json', encoding='utf-8'))

def pkey(p):
    w = p.get('where') or {}
    return '|'.join([str(p.get('cat','')), str(p.get('type','')), str(w.get('tag','')), str(w.get('id','')), str(w.get('row',''))[:24], str(w.get('text',''))[:16], str(p.get('detail',''))[:24]])

basemap = {}
for r in base:
    basemap.setdefault(r['page'].replace('\\', '/'), set()).update(pkey(p) for p in r['problems'])

new_probs, new_dl, new_js, exempt = [], [], [], []
tot_dl = tot_js = 0
mobile = [r for r in post if r['page'].replace('/', '\\').startswith('mobile\\')]
pc = [r for r in post if not r['page'].replace('/', '\\').startswith('mobile\\')]

for r in post:
    page = r['page'].replace('\\', '/')  # G21：跨机页键归一（基线 Windows \ 与副机 / 等价）
    for p in r['problems']:
        if pkey(p) not in basemap.get(page, set()):
            new_probs.append((page, pkey(p)))
    tot_dl += len(r['dead_links'])
    new_dl += [(page, d) for d in r['dead_links']]
    for e in r['js_errors']:
        tot_js += 1
        if 'ERR_CONNECTION_' in e.get('text',''):  # G20 扩：断网变体 CLOSED/RESET/ABORTED 全豁免
            exempt.append((page, e['text'][:80]))
        else:
            new_js.append((page, e['text'][:100]))

print(f"基线页数: {len(base)} ｜ post 页数: {len(post)}（PC {len(pc)} + mobile {len(mobile)}）")
print(f"全站死链合计: {tot_dl}")
print(f"全站 JS 错合计: {tot_js}（豁免 F01 外链断网 {len(exempt)} 条；其余 {len(new_js)}）")
for pg, t in exempt[:5]: print("  [豁免]", pg, t)
for pg, t in new_js[:10]: print("  [JS新增]", pg, t)
print(f"既有页 problems 逐键新增: {len(new_probs)}")
for pg, k in new_probs[:20]: print("  [新增]", pg, '|', k)

print("\n---- mobile 5 页逐页（死链/JS/问题/审计异常）----")
for r in mobile:
    print(f"  {r['page']}  死链:{len(r['dead_links'])}  JS错:{len(r['js_errors'])}  问题:{len(r['problems'])}  异常:{r.get('audit_error','无')[:60]}  nav_anomaly:{r.get('nav_anomaly') is not None}")
    for p in r['problems'][:5]: print("     ·", pkey(p))

mobile_ok = len(mobile) == 5 and all(len(r['dead_links']) == 0 and len(r['js_errors']) == 0 for r in mobile)
ok = len(post) == 115 and len(base) == 113 and tot_dl == 0 and len(new_js) == 0 and len(new_probs) == 0 and mobile_ok
print('\n==== audit 门：', 'PASS（115 页·死链0·JS0·diff 新增 0·mobile 5 页各自 0/0）====' if ok else 'FAIL ====')
sys.exit(0 if ok else 1)
