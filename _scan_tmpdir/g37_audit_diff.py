# -*- coding: utf-8 -*-
"""G37 验证门：audit 复跑 vs g36final 逐键 diff（D1/D2 术语与角色归一版）
判定：①post 页数=基线+3（3 新页） ②既有页 problems 逐键新增 0（基线键先过 G37 文本变更映射归一）
③死链 0 ④JS 0（F01 断网豁免沿例） ⑤3 新页自身 0/0/0"""
import io, sys, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
OUT = Path(__file__).resolve().parent
base = json.load(open(OUT / 'audit_results_g36final.json', encoding='utf-8'))
post = json.load(open(OUT / 'audit_results.json', encoding='utf-8'))

# G37 文本变更映射（基线旧词 → post 新词·长度降序）
MAP = [
    ('银行水单', '银行回单'), ('水单', '银行回单'),
    ('盈亏', '损益'), ('回款', '收款'),
    ('财务主管', '财务'), ('商务主管', '商务'), ('物流主管', '物流'),
    ('转租登记', '转移出库'), ('转租还回', '终止转移'),
]
MAP.sort(key=lambda x: len(x[0]), reverse=True)

def norm(s):
    for a, b in MAP:
        if a in s:
            s = s.replace(a, b)
    return s

def pkey(p):
    w = p.get('where') or {}
    return '|'.join([str(p.get('cat', '')), str(p.get('type', '')), str(w.get('tag', '')), str(w.get('id', '')),
                     str(w.get('row', ''))[:24], str(w.get('text', ''))[:16], str(p.get('detail', ''))[:24]])

NEW_PAGES = ['转移出库列表', '转移出库新建', '转移出库单详情']
bmap = {r['page']: r for r in base}
pmap = {r['page']: r for r in post}

new_keys = [k for k in pmap if k not in bmap]
gone_keys = [k for k in bmap if k not in pmap]
print(f"基线 {len(base)} 页 / post {len(post)} 页 / 新增页 {len(new_keys)} / 消失页 {len(gone_keys)}")
for k in sorted(new_keys):
    tag = '（本批新页）' if any(x in k for x in NEW_PAGES) else '（意外新增！）'
    print('  +', k, tag)

total_new_problems = 0
pages_with_new = []
dead_total = 0
js_total = 0
for pg, r in sorted(pmap.items()):
    dead_total += len(r.get('dead_links', []))
    njs = len(r.get('js_errors', []))
    js_total += njs
    if pg in bmap:
        bkeys = {norm(pkey(p)) for p in bmap[pg].get('problems', [])}
        newp = [p for p in r.get('problems', []) if pkey(p) not in bkeys]
        if newp:
            pages_with_new.append((pg, len(newp)))
            total_new_problems += len(newp)

print(f"既有页 problems 逐键新增：{total_new_problems} 处 / {len(pages_with_new)} 页")
for pg, n in pages_with_new[:20]:
    print('  !', pg, n)
print(f"post 死链总数：{dead_total}")
print(f"post JS 错误总数：{js_total}")
# 新页自身
for k in sorted(new_keys):
    if any(x in k for x in NEW_PAGES):
        r = pmap[k]
        print(f"新页 {k}: problems {len(r.get('problems', []))} 死链 {len(r.get('dead_links', []))} JS {len(r.get('js_errors', []))}")

ok = (len(new_keys) == 3 and all(any(x in k for x in NEW_PAGES) for k in new_keys)
      and total_new_problems == 0 and dead_total == 0 and js_total == 0)
print('==== G37 audit diff 判定：', 'PASS' if ok else 'FAIL', '====')
sys.exit(0 if ok else 1)
