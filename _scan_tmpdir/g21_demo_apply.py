#!/usr/bin/env python3
# G21 demo-data.js 三组改动（读取-精确替换+assert 计数，禁整页生成）：
#  T1a dictItems BF-03 停用 + BF-04/BF-05 追加
#  T2a products 12 行 fields 追加 rentInMode/rentInPrice/rentalMode/rentalPrice 四键
#  T3c rentInOrders feeSecTitle 月租/按套 → 按月/按次（5 处）
import re, sys, subprocess, os

ROOT = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental'
P = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型/_data/demo-data.js')
src = open(P, encoding='utf-8').read()

def kv(v):
    return 'null' if v is None else ('"%s"' % v if isinstance(v, str) else v)

# ===== T1a-1 BF-03 按张停用（恰 1 行，行内两处替换）=====
lines = src.splitlines(keepends=True)
bf03 = [i for i, l in enumerate(lines) if "'BF-03'" in l]
assert len(bf03) == 1, 'T1a BF-03 行数=%d' % len(bf03)
i = bf03[0]
assert lines[i].count('"status": "启用"') == 1, 'T1a BF-03 status 启用 非 1 处'
assert lines[i].count('tag tag-green') == 1, 'T1a BF-03 tag-green 非 1 处'
lines[i] = lines[i].replace('"status": "启用"', '"status": "停用"', 1) \
                    .replace('<span class=\\"tag tag-green\\">启用</span>', '<span class=\\"tag tag-gray\\">停用</span>', 1)
assert '"status": "停用"' in lines[i] and 'tag-gray' in lines[i]

# ===== T1a-2 BF-04/BF-05 追加（BF-03 行后，字段形态照 BF-01 逐字）=====
BF04 = '    \'BF-04\': { \'row\': {"fields": {"category": "计费方式", "abbr": "按年", "name": "按年计租", "status": "启用"}, "cells": ["按年", "按年计租", "<span class=\\"td-num\\">4</span>", "年租金 × 租期年数 · 长周期备用口径", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal(\'stopModal\')"}]} },\n'
BF05 = '    \'BF-05\': { \'row\': {"fields": {"category": "计费方式", "abbr": "按日", "name": "按日计租", "status": "启用"}, "cells": ["按日", "按日计租", "<span class=\\"td-num\\">5</span>", "日租金 × 在租天数 · 短期备用口径（本期无日租金业务）", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal(\'stopModal\')"}]} },\n'
assert src.count("'BF-04'") == 0 and src.count("'BF-05'") == 0, 'T1a BF-04/05 已存在'
lines[i + 1:i + 1] = [BF04, BF05]
src = ''.join(lines)
assert src.count("'BF-04'") == 1 and src.count("'BF-05'") == 1
print('T1a dictItems: BF-03 停用 + BF-04/BF-05 追加 PASS')

# ===== T2a products 12 行四键（行级精确插入，date/supplier 键后）=====
VALS = {
    '围板箱 1200×1000×970':    ('按月', '45.00', '按月', '60.00'),
    '围板箱 1200×1000×590':    (None, None, '按月', '55.00'),
    '木托盘 1200×1000':        (None, None, '按次', '15.00'),
    '塑料托盘 1200×1000':      ('按月', '12.00', '按月', '18.00'),
    '料箱 600×400×220（带盖）': (None, None, None, None),
    '料箱 600×400×340':        ('按月', '10.00', '按次', '14.00'),
    '锁扣组件': (None, None, None, None),
    '铰链':     (None, None, None, None),
    '围板':     (None, None, None, None),
    '箱盖':     (None, None, None, None),
    '底托架':   (None, None, None, None),
    '内衬':     (None, None, None, None),
}
lines = src.splitlines(keepends=True)
# products 块行范围
start = next(i for i, l in enumerate(lines) if l.rstrip().endswith('products: {'))
end = next(i for i in range(start + 1, len(lines)) if re.match(r'^  [A-Za-z][A-Za-z0-9]*: \{', lines[i]))
before_rows = {}
hit = 0
for i in range(start, end):
    l = lines[i]
    if "'row': {" not in l or '"fields"' not in l:
        continue
    m = re.search(r'"name": "([^"]+)"', l)
    assert m, 'T2a 行 %d 无 name' % (i + 1)
    name = m.group(1)
    assert name in VALS, 'T2a 意外物料 %s' % name
    before_rows[i] = l
    m2 = re.search(r'("(?:date|supplier)": "[^"]*")\}, "cells"', l)
    assert m2, 'T2a 行 %d fields 结尾锚失配' % (i + 1)
    rm, rp, lm, lp = VALS[name]
    frag = ', "rentInMode": %s, "rentInPrice": %s, "rentalMode": %s, "rentalPrice": %s' % (kv(rm), kv(rp), kv(lm), kv(lp))
    lines[i] = l[:m2.start()] + m2.group(1) + frag + '}, "cells"' + l[m2.end():]
    hit += 1
assert hit == 12, 'T2a 命中行=%d' % hit
# cells 价格格零改动自检：除插入片段外行内容逐字节一致（价格格文本原样保留）
for i, old in before_rows.items():
    new = lines[i]
    core_old = re.search(r'"cells": \[.*', old, re.S).group(0)
    core_new = re.search(r'"cells": \[.*', new, re.S).group(0)
    assert core_old == core_new, 'T2a 行 %d cells 被改动！' % (i + 1)
src = ''.join(lines)
assert src.count('rentInMode') == 12 and src.count('rentalMode') == 12, 'T2a 四键计数 %d/%d' % (src.count('rentInMode'), src.count('rentalMode'))
modes = re.findall(r'"(?:rentInMode|rentalMode)": ([^,]+),', src)
assert set(modes) <= {'null', '"按月"', '"按次"'}, 'T2a mode 越权值: %s' % set(modes)
print('T2a products 四键 12 行 PASS（cells 零改动自检过）')

# ===== T3c feeSecTitle 5 处 =====
OLD = '租入明细（多货品 · 月租/按套 · 无日租金）'
NEW = '租入明细（多货品 · 按月/按次 · 无日租金）'
n = src.count(OLD)
assert n == 5, 'T3c feeSecTitle 旧串=%d 处' % n
src = src.replace(OLD, NEW)
assert src.count(NEW) == 5 and src.count(OLD) == 0
# 复核：rentInOrders 块内 月租/按套 残留
assert src.count('月租/按套') == 0, 'T3c 残留 月租/按套'
print('T3c feeSecTitle 5 处 PASS')

open(P, 'w', encoding='utf-8').write(src)
print('demo-data.js 写入完成')

# ===== node --check =====
r = subprocess.run(['node', '--check', P], capture_output=True, text=True)
print('node --check 退出码:', r.returncode, r.stderr[:500] if r.returncode else '')
sys.exit(r.returncode)
