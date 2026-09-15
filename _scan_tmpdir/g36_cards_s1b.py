# -*- coding: utf-8 -*-
"""销售出库新建：两个空标签提示行 → .pn-hint 并入关联销售订单行（行级精确改写）"""
import io, os, re

FP = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\销售管理\销售出库新建.html'
s = io.open(FP, encoding='utf-8', newline='').read()
lines = s.split('\n')
CR = '\r' if lines[0].endswith('\r') else ''


def clean(i):
    return lines[i].replace('\r', '')


# 断言锚（1-based 348..358）
assert clean(347) == '<div class="form-row">', repr(clean(347))
assert '关联销售订单' in clean(348), repr(clean(348))
assert '<div class="input-box select-box"' in clean(349), repr(clean(349))[:60]
assert clean(350) == '  </div><div class="form-row">', repr(clean(350))
assert clean(351) == '    <div class="form-label">：</div>', repr(clean(351))
h1 = clean(352)
assert h1.startswith('    <div style="font-size:12px;color:#8c8c8c;') and '库存可用量' in h1
assert clean(353) == '  </div><div class="form-row">', repr(clean(353))
assert clean(354) == '    <div class="form-label">：</div>', repr(clean(354))
h2 = clean(355)
assert h2.startswith('    <div style="font-size:12px;color:#fa8c16;') and '库存可用量不足' in h2
assert clean(356) == '  </div><div class="form-row">', repr(clean(356))
assert '出库库房' in clean(357), repr(clean(357))


def inner(divline):
    """取出 <div style=…>TEXT</div> 的 TEXT"""
    m = re.match(r'\s*<div[^>]*>(.*)</div>\s*$', divline)
    assert m, divline[:80]
    return m.group(1)


new_block = [
    '    <div>',
    '      ' + clean(349).strip(),
    '      <div class="pn-hint">' + inner(h1) + '</div>',
    '      <div class="pn-hint" style="color:#fa8c16;font-weight:600;">' + inner(h2) + '</div>',
    '    </div>',
    '  </div>',
    '<div class="form-row">',
]
lines[349:357] = [l + CR for l in new_block]
io.open(FP, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('销售出库新建：提示行并入关联销售订单行 ✓')
print('  新块:' if False else '')
for l in new_block:
    print('   ', l[:110])
