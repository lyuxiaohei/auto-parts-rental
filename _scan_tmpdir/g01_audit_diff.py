# -*- coding: utf-8 -*-
"""G01 audit 基线 diff：执行前 baseline-G01-pre-20260909.json vs 执行后 audit_results.json
口径：死链/JS错 绝对合计 + 逐页 problems/dead_links/js_errors 多重集 diff（新增数）。
用法：python _scan_tmpdir/g01_audit_diff.py
"""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pre = {r['page']: r for r in json.load(open(r'_scan_tmpdir/baseline-G01-pre-20260909.json', encoding='utf-8'))}
post = {r['page']: r for r in json.load(open(r'_scan_tmpdir/audit_results.json', encoding='utf-8'))}

def sig(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True)

print('页数：基线 %d → 执行后 %d（口径 109+2 新模板=111）' % (len(pre), len(post)))
print('新增页：', [p for p in post if p not in pre])
print('消失页：', [p for p in pre if p not in post])

tot_dl = sum(len(r['dead_links']) for r in post.values())
tot_js = sum(len(r['js_errors']) for r in post.values())
tot_pb = sum(len(r['problems']) for r in post.values())
pre_pb = sum(len(r['problems']) for r in pre.values())
print('执行后合计：死链 %d / JS错 %d / 问题 %d（基线问题 %d）' % (tot_dl, tot_js, tot_pb, pre_pb))
for r in post.values():
    if r['js_errors']:
        print('  JS错明细：%s → %s' % (r['page'], json.dumps(r['js_errors'], ensure_ascii=False)[:200]))

new_issues = []
for pg, r in post.items():
    base = pre.get(pg)
    pre_pb_sigs = [sig(x) for x in (base['problems'] if base else [])]
    pre_dl = set(map(sig, base['dead_links'])) if base else set()
    pre_js = set(map(sig, base['js_errors'])) if base else set()
    for x in r['problems']:
        s = sig(x)
        if s in pre_pb_sigs:
            pre_pb_sigs.remove(s)
        else:
            new_issues.append((pg, '问题', x))
    for x in r['dead_links']:
        if sig(x) not in pre_dl:
            new_issues.append((pg, '死链', x))
    for x in r['js_errors']:
        if sig(x) not in pre_js:
            new_issues.append((pg, 'JS错', x))

if new_issues:
    print('\n相对基线新增 %d 条：' % len(new_issues))
    for pg, kind, x in new_issues:
        print(' ✗ [%s] %s: %s' % (kind, pg, json.dumps(x, ensure_ascii=False)[:160]))
else:
    print('\n相对执行前基线新增 0 条 ✅')
sys.exit(1 if new_issues else 0)
