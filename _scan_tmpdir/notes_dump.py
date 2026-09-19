# -*- coding: utf-8 -*-
"""导出 NOTES_DATA 全部条目（id/title/note/锚点键）供双轨分类。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
t = (ROOT / 'P3-R01-包装租赁管理后台原型/_data/notes-data.js').read_text(encoding='utf-8')
m = re.search(r'window\.NOTES_DATA\s*=\s*(\{[\s\S]*\});', t)
data = json.loads(m.group(1))
out = []
for key, items in data.items():
    for it in items:
        out.append({'page': key, 'id': it.get('id'), 'title': it.get('title', ''), 'note': (it.get('note') or '')[:70]})
for o in out:
    print('%3s | %-34s | %s | %s' % (o['id'], o['page'].split('/')[-1][:34], o['title'][:24], o['note'][:60]))
print('total', len(out))
