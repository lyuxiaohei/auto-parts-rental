# -*- coding: utf-8 -*-
"""G19a T4: 索引 G19a 行 ⏳→✅（读最新→仅改本行→立即写回；D7 并发防护）"""
import pathlib, time, re

idx = pathlib.Path('agent-handoff/_索引.md')
t0 = idx.stat().st_mtime
s = idx.read_text(encoding='utf-8')
t1 = idx.stat().st_mtime
assert t0 == t1, 'read raced, retry needed'

lines = s.splitlines(keepends=True)
hit = [i for i, l in enumerate(lines) if l.strip().startswith('| G19a ')]
assert len(hit) == 1, f'G19a rows: {len(hit)}'
old = lines[hit[0]]
print('[before]', old.strip()[:150])

# ⏳→✅（哈希待回填），保留行内其余描述
new = old.replace('⏳', '✅（哈希待回填）', 1) if '⏳' in old else old.replace('| G19a |', '| G19a |', 1)
if new == old:  # 无 ⏳ 标记则前置 ✅
    parts = old.split('|')
    parts[4] = ' ✅（哈希待回填） '
    new = '|'.join(parts)
lines[hit[0]] = new
idx.write_text(''.join(lines), encoding='utf-8')

# 回读验证：本行已变、其余行零变化
s2 = idx.read_text(encoding='utf-8')
l2 = s2.splitlines(keepends=True)
assert l2[hit[0]] != old, 'row unchanged'
assert len(l2) == len(lines)
same = sum(1 for a, b in zip(lines, l2) if a == b)
print('[after] ', new.strip()[:150])
print(f'row changed OK; other rows identical: {same}/{len(l2)-1}')
