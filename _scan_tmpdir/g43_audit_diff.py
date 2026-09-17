# -*- coding: utf-8 -*-
"""G43 验证门 2：收尾 audit（audit_results_g43post.json）vs g43pre（=G50 收尾快照·git HEAD 在案）逐键 diff。
判定：①页数一致（G43 零增删）②既有页 problems 逐键新增 0 ③全站死链 0 ④JS 错 0（net::ERR_* 断网类豁免·G13 期 F01 先例）"""
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
OUT = Path(__file__).resolve().parent
base = json.load(open(OUT / 'audit_results_g43pre.json', encoding='utf-8'))
post = json.load(open(OUT / 'audit_results_g43post.json', encoding='utf-8'))

def pkey(p):
    w = p.get('where') or {}
    return '|'.join([str(p.get('cat', '')), str(p.get('type', '')), str(w.get('tag', '')), str(w.get('id', '')),
                     str(w.get('row', ''))[:24], str(w.get('text', ''))[:16], str(p.get('detail', ''))[:24]])

basemap = {}
for r in base:
    basemap.setdefault(r['page'].replace('\\', '/'), set()).update(pkey(p) for p in r['problems'])
postmap = {}
for r in post:
    postmap.setdefault(r['page'].replace('\\', '/'), set()).update(pkey(p) for p in r['problems'])

new_pages = sorted(set(postmap) - set(basemap))
gone_pages = sorted(set(basemap) - set(postmap))
added = {}
for pg, keys in postmap.items():
    extra = keys - basemap.get(pg, set())
    if extra:
        added[pg] = sorted(extra)

bad_pages = [r for r in post if r['problems']]
deadlink_total = sum(len(r.get('dead_links') or []) for r in post)
def real_js(r):
    return [e for e in (r.get('js_errors') or []) if 'net::ERR_' not in str(e.get('text', ''))]
jserr_total = sum(len(real_js(r)) for r in post)

print(f"pre 页数={len(basemap)} post 页数={len(postmap)} 新增页={new_pages or '无'} 消失页={gone_pages or '无'}")
print(f"坏页（problems>0）={len(bad_pages)} 死链总数={deadlink_total} JS错总数={jserr_total}")
if added:
    print("逐键新增（非零即 FAIL）:")
    for pg, ks in added.items():
        for k in ks[:6]:
            print(f"  + {pg}: {k[:110]}")
else:
    print("逐键 diff：新增 0")
ok = (not new_pages) and (not gone_pages) and (not added) and not bad_pages and deadlink_total == 0 and jserr_total == 0
print("判定：" + ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
