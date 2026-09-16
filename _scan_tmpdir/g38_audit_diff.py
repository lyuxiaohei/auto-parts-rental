# -*- coding: utf-8 -*-
"""G38 验证门：audit 复跑 vs g37baseline 逐键 diff（字段口径统一版）
判定：①页数=基线（132·无增删） ②既有页 problems 逐键新增 0（基线键先过 G38 文本变更映射归一）
③死链 0 ④JS 0（F01 断网豁免沿例）"""
import io, sys, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
OUT = Path(__file__).resolve().parent
base = json.load(open(OUT / 'audit_results_g37baseline.json', encoding='utf-8'))
post = json.load(open(OUT / 'audit_results.json', encoding='utf-8'))

# G38 文本变更映射（基线旧词 → post 新词·长度降序）
MAP = [
    ('零件号 / 物料编码', '物料编码'), ('零件号', '物料编码'),
    ('每托数量', '数量'), ('入库总数', '数量'), ('到货托数', '数量'), ('托数', '数量'),
    ('入库库区', '入库库房'), ('出库库区', '出库库房'), ('调出库区', '调出库房'), ('调入库区', '调入库房'), ('库区', '库房'),
    ('货品', '物料'),
    ('单价(元)', '未税单价(元)'), ('金额(元)', '含税金额(元)'),
    ('多货品', '多物料'),
    ('以托为单位', '以物料基本单位入库'),
    ('建档时间', '建档日期'), ('创建时间', '创建日期'), ('更新时间', '更新日期'), ('立项时间', '立项日期'),
    ('制单时间', '制单日期'),
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

bmap = {r['page']: r for r in base}
pmap = {r['page']: r for r in post}
new_pages = [k for k in pmap if k not in bmap]
gone_pages = [k for k in bmap if k not in pmap]
print(f"基线 {len(base)} 页 / post {len(post)} 页 / 新增 {len(new_pages)} / 消失 {len(gone_pages)}")
for k in new_pages + gone_pages:
    print('  !', k)

total_new = 0
pages_with_new = []
dead_total = 0
js_total = 0
for pg, r in sorted(pmap.items()):
    dead_total += len(r.get('dead_links', []))
    js_total += len(r.get('js_errors', []))
    if pg in bmap:
        bkeys = {norm(pkey(p)) for p in bmap[pg].get('problems', [])}
        added = [p for p in r.get('problems', []) if norm(pkey(p)) not in bkeys]
        if added:
            pages_with_new.append(pg)
            total_new += len(added)
            for p in added[:3]:
                print('  + [%s] %s' % (pg, pkey(p)[:100]))

print('死链合计 %d ｜ JS 错误合计 %d ｜ 逐键新增 %d（%d 页）' % (dead_total, js_total, total_new, len(pages_with_new)))
verdict = (len(post) == len(base) == 132 and not new_pages and not gone_pages
           and dead_total == 0 and js_total == 0 and total_new == 0)
print('VERDICT:', 'PASS' if verdict else 'FAIL')
sys.exit(0 if verdict else 1)
