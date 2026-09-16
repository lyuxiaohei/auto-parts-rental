# -*- coding: utf-8 -*-
# acc38 独立验收·第11项红线：stockFlows 行 -/+ 配对比较，除 cls 外（及已知文案字段）其余键值必须不变
import io, re, ast, sys
t = io.open('acc38_demo_diff.txt', encoding='utf-8').read().splitlines()
minus, plus = [], []
for l in t:
    if l.startswith('-') and not l.startswith('---'):
        minus.append(l[1:])
    elif l.startswith('+') and not l.startswith('+++'):
        plus.append(l[1:])

# 取成对的 row 行（含 qtyByProject 或 cls 的）
mrows = [l for l in minus if "'row':" in l and ('qtyByProject' in l or "'cls'" in l)]
prows = [l for l in plus if "'row':" in l and ('qtyByProject' in l or "'cls'" in l)]
print('配对 -row 行数 =', len(mrows), '；+row 行数 =', len(prows))

def parse_row(l):
    m = re.search(r"\{'row': (\{.*\}), 'cells'", l.strip())
    if not m:
        m = re.search(r"\{'row': (\{.*\})\s*,\s*'cells'", l.strip())
    if not m:
        return None
    return ast.literal_eval(m.group(1))

diffs = 0
pairs = 0
for i in range(min(len(mrows), len(prows))):
    a, b = parse_row(mrows[i]), parse_row(prows[i])
    if a is None or b is None:
        print('  ! 第%d对解析失败' % (i+1)); diffs += 1; continue
    keys = set(a.get('fields', {})) | set(b.get('fields', {}))
    for k in sorted(keys):
        va, vb = a.get('fields', {}).get(k), b.get('fields', {}).get(k)
        if va != vb:
            print('  DIFF 第%d对 字段 %s: %r -> %r' % (i+1, k, va, vb))
            diffs += 1
    # row 层其它键（除 fields 外）
    for k in set(a) | set(b):
        if k == 'fields':
            continue
        if a.get(k) != b.get(k):
            print('  DIFF 第%d对 row.%s: %r -> %r' % (i+1, k, str(a.get(k))[:60], str(b.get(k))[:60]))
            diffs += 1
    pairs += 1
print('配对比较 %d 对，字段级差异 %d 处（仅 cls 及登记文案改动为合规）' % (pairs, diffs))

# 单独提取所有 qtyByProject 值对比（- 侧 vs + 侧集合）
def qvals(rows):
    out = []
    for l in rows:
        for m in re.finditer(r"qtyByProject['\"]?\s*:\s*(\{[^}]*\})", l):
            out.append(m.group(1))
    return sorted(out)
qm, qp = qvals(mrows), qvals(prows)
print('qtyByProject 值提取（-侧 %d 个 / +侧 %d 个）完全一致: %s' % (len(qm), len(qp), qm == qp))
if qm != qp:
    for x, y in zip(qm, qp):
        if x != y:
            print('  -', x[:100]); print('  +', y[:100])
print('== done ==')
