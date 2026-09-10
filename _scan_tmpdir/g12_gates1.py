# -*- coding: utf-8 -*-
"""G12 T5 验证门 1/2/4：audit 逐键 diff / grep 引用门 / 白名单零改动门"""
import json, io, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'

# ===== 门 1：audit 逐键 diff =====
base = json.load(open(ROOT + r'\_scan_tmpdir\audit_results_g12baseline.json', encoding='utf-8'))
final = json.load(open(ROOT + r'\_scan_tmpdir\audit_results.json', encoding='utf-8'))
bmap = {e['page']: e for e in base}
fmap = {e['page']: e for e in final}
assert set(bmap) == set(fmap), '页面集不一致: %s' % (set(fmap) ^ set(bmap))
new_items = []
for pg, fe in fmap.items():
    be = bmap[pg]
    for field in ('dead_links', 'js_errors', 'problems'):
        bset = set(json.dumps(x, ensure_ascii=False, sort_keys=True) for x in be[field])
        fset = set(json.dumps(x, ensure_ascii=False, sort_keys=True) for x in fe[field])
        added = fset - bset
        if added:
            new_items.append((pg, field, sorted(added)[:3]))
dead_total = sum(len(e['dead_links']) for e in final)
js_total = sum(len(e['js_errors']) for e in final)
print('【门1 audit】108 页 死链=%d JS错=%d | 相对 g12baseline 逐键新增=%d' % (dead_total, js_total, len(new_items)))
for pg, field, its in new_items[:10]:
    print('  NEW:', pg, field, its)
print('门1 判定:', 'PASS' if (dead_total == 0 and js_total == 0 and not new_items) else 'FAIL')

# ===== 门 2：grep A 类引用 =====
cls = json.load(open(ROOT + r'\_scan_tmpdir\g12-classify.json', encoding='utf-8'))
A = [it['path'] for it in cls['A']]
have = [p for p in A if 'demo-data.js' in open(ROOT + r'\P3-R01-包装租赁管理后台原型' + '\\' + p.replace('/', '\\'), encoding='utf-8').read()]
print()
print('【门2 grep】A=%d，含 demo-data.js 引用=%d → %s' % (len(A), len(have), 'PASS N=N' if len(A) == len(have) else 'FAIL'))
for p in A:
    print('  ✓' if p in have else '  ✗', p)

# ===== 门 4：白名单零改动 =====
r = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
changed = set()
for line in r.stdout.splitlines():
    pth = line[3:].strip().strip('"')
    changed.add(pth.replace('/', '\\'))
B = [it['path'] for it in cls['B_pages']] + [it['path'] for it in cls['B_modals']]
Bset = set('P3-R01-包装租赁管理后台原型' + '\\' + p.replace('/', '\\') for p in B)
inter = changed & Bset
print()
print('【门4 白名单】git 改动 %d 文件，与 B 类 46 文件交集 = %s → %s' % (len(changed), (list(inter) if inter else '∅'), 'PASS' if not inter else 'FAIL'))
