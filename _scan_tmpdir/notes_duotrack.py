# -*- coding: utf-8 -*-
"""#9 双轨数据：A03 json + notes-data.js 为 dev 条目加 "aud":"dev"（其余默认 biz）；
顺带修正过时口径（我的待办 #1「15 类」→「20 类」）。"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
BK = ROOT / 'backup-notes-duotrack-20260919'

DEV = {  # (页面键尾段, id) -> dev
    ('BOM维护.html', '3'): None,
    ('损益报表.html', '2'): None,
    ('用户权限.html', '3'): None,
    ('租赁单新建.html', '1'): None,
    ('租赁单新建.html', '2'): None,
    ('审批详情.html', '1'): None,
}

def mark(items_key, items):
    hit = 0
    for it in items:
        tail = items_key.split('/')[-1]
        if (tail, str(it.get('id'))) in DEV and 'aud' not in it:
            # 保持键序：id,title,note,aud,fp,req → 直接在 id 后插 aud
            it2 = {}
            for k, v in it.items():
                it2[k] = v
                if k == 'id':
                    it2['aud'] = 'dev'
            it.clear()
            it.update(it2)
            hit += 1
    return hit

# --- A03 json ---
a03 = PROTO / 'P3-R01-A03-标注数据.json'
BK.mkdir(parents=True, exist_ok=True)
shutil.copy2(a03, BK / 'P3-R01-A03-标注数据.json')
data = json.loads(a03.read_text(encoding='utf-8'))
n = 0
for key in list(data.keys()):
    if isinstance(data[key], list):
        n += mark(key, data[key])
a03.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print('A03 标 dev:', n)

# --- notes-data.js（逐条目对象内 "id": "N" 后插 "aud": "dev"）---
nd = PROTO / '_data/notes-data.js'
if not (BK / 'notes-data.js.orig').exists():
    (BK / 'notes-data.js.orig').write_bytes((BK / 'notes-data.js').read_bytes())
t = (BK / 'notes-data.js.orig').read_text(encoding='utf-8')  # 从原备份重放（含 15->20 一起重放）
cnt = 0
for tail, id_ in DEV:
    pat = re.compile(r'[^"]*' + re.escape(tail) + r'"\s*:\s*\[([\s\S]*?)\n\s*\]', re.M)
    m = pat.search(t)
    if not m:
        print('  未命中页键:', tail); continue
    block = m.group(1)
    nb, k = re.subn(r'("id"\s*:\s*' + id_ + r'\s*,\s*\n)', r'\1      "aud": "dev",\n', block, count=1)
    if k:
        t = t[:m.start(1)] + nb + t[m.end(1):]
        cnt += k
    else:
        print('  未命中条目:', tail, id_)
# 我的待办 #1 口径修正 15->20
t2 = t.replace('覆盖 15 类单据', '覆盖 20 类单据')
fixed = t2 != t
nd.write_text(t2, encoding='utf-8')
print('notes-data 标 dev:', cnt, '| 15->20 修正:', fixed)
