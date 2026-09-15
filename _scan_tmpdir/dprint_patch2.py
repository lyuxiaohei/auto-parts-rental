# -*- coding: utf-8 -*-
"""出货单打印 v2：demo-data 占位 act→跳转 + 静态行同步 + 录单页删卡移备注"""
import io, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
FAILS = []
def rd(p):
    return io.open(ROOT + '\\' + p, encoding='utf-8', newline='').read()
def wr(p, t):
    io.open(ROOT + '\\' + p, 'w', encoding='utf-8', newline='').write(t)

PLACE = '"act": "window.print();this.classList.toggle(\'printed\')"'

# ---------- A. demo-data comboOutbounds ----------
p = r'_data\demo-data.js'
t = rd(p)
eol = '\r\n' if '\r\n' in t else '\n'
block = t.split('  comboOutbounds: {')[1].split(eol + '  },')[0]
if '出货单打印.html?key=' in block and PLACE not in block:
    print('demo-data 已处理，跳过')
else:
    lines = t.split(eol)
    i0 = next(i for i, l in enumerate(lines) if l.startswith('  comboOutbounds: {'))
    i1 = next(i for i, l in enumerate(lines) if i > i0 and l == '  },')
    cur_key = None
    replaced = inserted = 0
    for idx in range(i0, i1 + 1):
        l = lines[idx]
        km = re.match(r"    '([A-Z][A-Z0-9-]+)': \{", l)
        if km:
            cur_key = km.group(1)
            continue
        if not cur_key:
            continue
        if PLACE in l:
            lines[idx] = l.replace(PLACE, '"act": "go(\'出货单打印.html?key=%s\')"' % cur_key, 1)
            replaced += 1
        elif '"t": "详情", "detail": true' in l and '打印出货单' not in l:
            lines[idx] = l.replace('"ops": [',
                '"ops": [{"t": "打印出货单", "act": "go(\'出货单打印.html?key=%s\')"}, ' % cur_key, 1)
            inserted += 1
    print('demo-data: replaced=%d inserted=%d (expect 8+2)' % (replaced, inserted))
    if replaced + inserted != 10:
        FAILS.append(('demo', p, 'replaced=%d inserted=%d' % (replaced, inserted)))
    else:
        wr(p, eol.join(lines))
eol = '\r\n' if '\r\n' in t else '\n'
lines = t.split(eol)
i0 = next(i for i, l in enumerate(lines) if l.startswith('  comboOutbounds: {'))
i1 = next(i for i, l in enumerate(lines) if i > i0 and l == '  },')
cur_key = None
replaced = inserted = 0
for idx in range(i0, i1 + 1):
    l = lines[idx]
    km = re.match(r"    '([A-Z][A-Z0-9-]+)': \{", l)
    if km:
        cur_key = km.group(1)
        continue
    if not cur_key:
        continue
    if PLACE in l:
        lines[idx] = l.replace(PLACE, '"act": "go(\'出货单打印.html?key=%s\')"' % cur_key, 1)
        replaced += 1
    elif '"t": "详情", "detail": true' in l and '打印出货单' not in l:
        lines[idx] = l.replace('"ops": [',
            '"ops": [{"t": "打印出货单", "act": "go(\'出货单打印.html?key=%s\')"}, ' % cur_key, 1)
        inserted += 1
print('demo-data: replaced=%d inserted=%d (expect 8+2)' % (replaced, inserted))
if replaced + inserted != 10:
    FAILS.append(('demo', p, 'replaced=%d inserted=%d' % (replaced, inserted)))
else:
    wr(p, eol.join(lines))

# ---------- B. 静态列表页占位 act 按 CK 块替换 ----------
p = r'租赁管理\租赁出库列表.html'
t = rd(p)
eol = '\r\n' if '\r\n' in t else '\n'
lines = t.split(eol)
cur_ck = None
rep_b = 0
for idx, l in enumerate(lines):
    km = re.search(r'<span class="lk">(CK-[0-9-]+)</span>', l)
    if km:
        cur_ck = km.group(1)
    if PLACE.replace('"act": ', '').replace('"', '') in l and '打印出货单' in l and cur_ck:
        old = "<a onclick=\"window.print();this.classList.toggle('printed')\">打印出货单</a>"
        new = "<a onclick=\"go('出货单打印.html?key=%s')\">打印出货单</a>" % cur_ck
        if old in l:
            lines[idx] = l.replace(old, new, 1)
            rep_b += 1
print('列表页静态行替换:', rep_b)
residual = eol.join(lines).count(PLACE)
if rep_b != 8 or residual:
    FAILS.append(('static', p, 'replaced=%d residual=%d expect 8/0' % (rep_b, residual)))
else:
    wr(p, eol.join(lines))

# ---------- C. 录单页 ----------
p = r'租赁管理\租赁出库录单.html'
t = rd(p)
eol = '\r\n' if '\r\n' in t else '\n'
if '其他信息' not in t and '随箱资料' not in t and '出库备注' in t:
    print('录单页已改过，跳过')
else:
    lines = t.split(eol)
    im = next(i for i, l in enumerate(lines) if '<h3 class="card-title">其他信息</h3>' in l)
    # card 开始 = 向上最近的无类 card div
    ib = im
    while ib > 0 and '<div class="card">' not in lines[ib]:
        ib -= 1
    assert ib < im, 'card 起始未找到'
    # 行级配平找卡尾
    depth = 0
    ie = None
    for j in range(ib, len(lines)):
        depth += len(re.findall(r'<div\b', lines[j])) - len(re.findall(r'</div>', lines[j]))
        if depth <= 0:
            ie = j
            break
    card_text = eol.join(lines[ib:ie + 1])
    assert '随箱资料' in card_text and '出库备注' in card_text, '卡内容异常'
    del lines[ib:ie + 1]
    # 可能残留空行清理：若 lines[ib] 为空行且 lines[ib+1] 也空，删一个
    if ib < len(lines) and lines[ib].strip() == '' and ib + 1 < len(lines) and lines[ib + 1].strip() == '':
        del lines[ib]
    t2 = eol.join(lines)
    # 备注行插基本信息卡（要货日期锚后）
    anchor = (
'  <div class="form-row">' + eol +
'    <div class="form-label"><span class="req">*</span>要货日期：</div>' + eol +
'    <div>' + eol +
'      <div class="input-box" style="width:180px;"><input type="text" value="2026-08-31" placeholder="请输入"></div>' + eol +
'    </div>' + eol +
'  </div>')
    assert t2.count(anchor) == 1, '要货日期锚 count=%d' % t2.count(anchor)
    note = (
'  <div class="form-row">' + eol +
'    <div class="form-label">出库备注：</div>' + eol +
'    <div>' + eol +
'      <div class="input-box" style="width:520px;"><input type="text" value="" placeholder="选填"></div>' + eol +
'    </div>' + eol +
'  </div>')
    t2 = t2.replace(anchor, anchor + eol + note, 1)
    assert '随箱资料' not in t2 and '其他信息' not in t2
    o = len(re.findall(r'<div\b', t2)); c = len(re.findall(r'</div>', t2))
    print('录单页改后 div: %d/%d %s' % (o, c, 'OK' if o == c else 'BAD'))
    if o != c:
        FAILS.append(('recform', p, 'div 配平 %d/%d' % (o, c)))
    else:
        wr(p, t2)

for f in FAILS:
    print('FAIL:', f)
print('DONE' if not FAILS else 'HAS FAILS')
