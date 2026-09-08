# -*- coding: utf-8 -*-
"""修复 P1-R05 变更记录：截掉 shell 反引号污染段，拼接 Write 工具写的干净版本"""
from pathlib import Path
HERE = Path(__file__).parent
ROOT = HERE.parent
p = ROOT / 'P1-R05-agent交接文档.md'
raw = p.read_bytes().decode('utf-8')
marker = '## 变更记录 · 2026-09-08（详情弹窗数据驱动全量推广'
i = raw.find(marker)
assert i > 0, '未找到污染段标记'
# 连同其前面的 --- 分隔线一起截掉（往前找最近的 '---' 行）
pre = raw[:i]
j = pre.rstrip().rfind('---')
assert j > 0
clean = pre[:j].rstrip() + '\n\n' + (HERE / 'p1r05-changelog-20260908.md').read_text(encoding='utf-8').strip() + '\n'
# 污染段中反引号内容已丢（如 `_data/demo-data.js` 变空）——校验干净版不再缺这些
assert 'demo-data.js` 新增 26 实体' in clean
assert 'backup-detail-批次1|2|3-20260908/' in clean
p.write_bytes(clean.encode('utf-8'))
print('修复完成，文件尾 80 字：', clean[-80:].replace('\n', '⏎'))
