# -*- coding: utf-8 -*-
"""卡片化改造 · 阶段 1：卡标题统一（.card-head 包裹）+ 空标签提示行修复"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'


def rd(p):
    return io.open(os.path.join(ROOT, p.replace('/', os.sep)), encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(os.path.join(ROOT, p.replace('/', os.sep)), 'w', encoding='utf-8', newline='').write(s)


# ---------- 1) 卡标题补 .card-head 包裹（与样板一致） ----------
BARE = [
    ('仓储作业/盘点录入.html', '<h3 class="card-title" data-note="2">盈亏处理</h3>'),
    ('基础数据/BOM维护.html', '<h3 class="card-title">版本记录</h3>'),
    ('系统管理/数据字典.html', '<h3 class="card-title" data-note="2">计费方式</h3>'),
    ('财务协同/盈亏报表.html', '<h3 class="card-title">项目毛利对比</h3>'),
    ('首页/项目看板.html', '<h3 class="card-title">项目营收对比</h3>'),
]
print('== 卡标题统一 ==')
for p, h in BARE:
    s = rd(p)
    assert s.count(h) == 1, '%s 标题锚 %d' % (p, s.count(h))
    # 缩进沿用该行
    m = re.search(r'([ \t]*)' + re.escape(h), s)
    ind = m.group(1)
    new = ind + '<div class="card-head">\r\n' + ind + '  ' + h + '\r\n' + ind + '</div>'
    s = s.replace(ind + h, new)
    wr(p, s)
    print('  %-30s ✓' % p.split('/')[-1])

# ---------- 2) 销售出库新建：空标签提示行 → .pn-hint 并入关联销售订单行 ----------
p = '销售管理/销售出库新建.html'
s = rd(p)
m = re.search(r'<div class="form-row">\r?\n\s*<div class="form-label"><span class="req">\*</span>关联销售订单：</div>\r?\n\s*(<div class="input-box select-box"[^>]*>.*?</div>)\r?\n\s*</div>\r?\n\s*<div class="form-row">\r?\n\s*<div class="form-label">：</div>\r?\n\s*<div style="font-size:12px;color:#8c8c8c;line-height:1\.7;">(.*?)</div>\r?\n\s*</div>\r?\n\s*<div class="form-row">\r?\n\s*<div class="form-label">：</div>\r?\n\s*<div style="font-size:12px;color:#fa8c16;line-height:1\.7;font-weight:600;">(.*?)</div>\r?\n\s*</div>', s, re.S)
assert m, '销售出库新建 提示行锚未匹配'
sel, hint1, hint2 = m.group(1), m.group(2), m.group(3)
new = ('<div class="form-row">\r\n'
       '    <div class="form-label"><span class="req">*</span>关联销售订单：</div>\r\n'
       '    <div>\r\n'
       '      ' + sel + '\r\n'
       '      <div class="pn-hint">' + hint1 + '</div>\r\n'
       '      <div class="pn-hint" style="color:#fa8c16;font-weight:600;">' + hint2 + '</div>\r\n'
       '    </div>')
s = s[:m.start()] + new + s[m.end():]
wr(p, s)
print('== 销售出库新建 空标签提示行 → .pn-hint ✓（并入关联销售订单行）')

# 校验：全站不应再有空标签行
n = 0
for dp, dn, fns in os.walk(ROOT):
    if '.git' in dp:
        continue
    for f in fns:
        if f.endswith('.html'):
            x = io.open(os.path.join(dp, f), encoding='utf-8', errors='ignore').read()
            c = len(re.findall(r'<div class="form-label">：</div>', x))
            if c:
                print('  !! 残留空标签:', os.path.relpath(os.path.join(dp, f), ROOT), c)
                n += c
print('  空标签行残留 =', n)
