# -*- coding: utf-8 -*-
"""对比并行版 audit_results.json 与串行基线 audit_results_serial_g51.json 逐页一致性"""
import json, io, sys
sys.stdout.reconfigure(encoding='utf-8')

par = json.load(io.open('_scan_tmpdir/audit_results.json', encoding='utf-8'))
ser = json.load(io.open('_scan_tmpdir/audit_results_serial_g51.json', encoding='utf-8'))

def counts(r):
    return (r['page'], len(r['problems']), len(r['dead_links']), len(r['js_errors']))

pm = {p: (a, b, c) for p, a, b, c in map(counts, par)}
sm = {p: (a, b, c) for p, a, b, c in map(counts, ser)}

print('pages: parallel=%d serial=%d' % (len(par), len(ser)))
print('page sets equal:', set(pm) == set(sm))

diffs = []
for p in sorted(set(pm) | set(sm)):
    if pm.get(p) != sm.get(p):
        diffs.append((p, sm.get(p), pm.get(p)))
print('per-page count diffs:', len(diffs))
for p, s, n in diffs:
    print('  DIFF', p, 'serial=', s, 'parallel=', n)

# 顺序一致性（写入顺序=页名排序）
po = [r['page'] for r in par]
so = [r['page'] for r in ser]
print('write order identical to serial:', po == so)

tp = tuple(map(sum, zip(*[v for v in pm.values()])))
ts = tuple(map(sum, zip(*[v for v in sm.values()])))
print('TOTAL parallel 问题/死链/JS错 =', tp)
print('TOTAL serial   问题/死链/JS错 =', ts)
print('VERDICT:', 'IDENTICAL' if not diffs and po == so and set(pm) == set(sm) else 'MISMATCH')
