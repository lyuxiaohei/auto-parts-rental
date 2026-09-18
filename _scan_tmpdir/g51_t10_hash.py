# -*- coding: utf-8 -*-
"""G51 T10b: 哈希回填——任务书 commit 行 + 索引 G51 行 ⏳→✅"""
import io

H = '98806a7'

# 1. 任务书哈希行
p1 = 'agent-handoff/20260917-G51-施工后文档落后修正.md'
t1 = io.open(p1, encoding='utf-8', newline='').read()
old1 = '| commit 哈希 | （收尾回填） |'
n1 = t1.count(old1)
if n1 != 1:
    old1 = None
    # CRLF 差异尝试
    for cand in ['| commit 哈希 | （收尾回填） |']:
        pass
assert n1 == 1, 'taskdoc hash anchor: %d' % n1
t1 = t1.replace(old1, '| commit 哈希 | %s（＋前置批次 e27ed9e） |' % H)
with io.open(p1, 'w', encoding='utf-8', newline='') as f:
    f.write(t1)

# 2. 索引 G51 行
p2 = 'agent-handoff/_索引.md'
t2 = io.open(p2, encoding='utf-8', newline='').read()
anchor2 = '任务书=20260917-G51-施工后文档落后修正.md | ⏳ | — | 20260917-G51-施工后文档落后修正.md |'
assert t2.count(anchor2) == 1, 'index G51 anchor: %d' % t2.count(anchor2)
t2 = t2.replace(anchor2, '任务书=20260917-G51-施工后文档落后修正.md | ✅ | %s（＋前置 e27ed9e） | 20260917-G51-施工后文档落后修正.md |' % H)
with io.open(p2, 'w', encoding='utf-8', newline='') as f:
    f.write(t2)

# 回读验证
c1 = io.open(p1, encoding='utf-8').read()
c2 = io.open(p2, encoding='utf-8').read()
assert H in c1 and '（待执行）' not in c1
assert ('| ✅ | %s' % H) in c2 and '⏳' not in c2.split('G51')[-1][:500]
print('T10b OK: hash backfilled to taskdoc + index (%s)' % H)
