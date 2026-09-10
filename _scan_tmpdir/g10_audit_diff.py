# -*- coding: utf-8 -*-
"""G10-D: audit 新旧逐键 diff（相对 G09 基线，路径分隔符归一）"""
import json, io, sys
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

new = json.load(open(r'_scan_tmpdir/audit_results.json', encoding='utf-8'))
old = json.load(open(r'_scan_tmpdir/audit_results_g09baseline.json', encoding='utf-8'))

def key(r, p):
    pg = r['page'].replace('\\', '/')
    return tuple([pg, p.get('cat'), p.get('type'), p.get('phase'),
                  json.dumps(p.get('where'), ensure_ascii=False, sort_keys=True),
                  p.get('detail')])

old_keys = Counter(key(r, p) for r in old for p in r['problems'])
new_keys = Counter(key(r, p) for r in new for p in r['problems'])

added = new_keys - old_keys
removed = old_keys - new_keys

dead = sum(len(r['dead_links']) for r in new)
jserr = sum(len(r['js_errors']) for r in new)
audit_err = [r['page'] for r in new if r.get('audit_error')]

print(f'基线问题总数: {sum(old_keys.values())}  新问题总数: {sum(new_keys.values())}')
print(f'死链总数: {dead}  JS错误总数: {jserr}  审计异常页: {len(audit_err)}')
print(f'新增键: {sum(added.values())}  消失键: {sum(removed.values())}')
for k, n in added.items():
    print('  +', n, k)
for k, n in removed.items():
    print('  -', n, k)
print('==== audit 逐键 diff 结论：新增', sum(added.values()), '====')
