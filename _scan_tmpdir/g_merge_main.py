# -*- coding: utf-8 -*-
"""物料类型×物料分类合并（D-96）：名称取「物料类型」，值取物料分类 6 值。
域=字典(WL/FL 合并)+产品档案域(实体值/筛选/列头/cfg/弹窗双层)+数据字典页；
单据域（purchaseOrders mtype 器具/零部件·poQjRow 联动）零改动挂注记。"""
import io, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def row(code, cat, name, note, seq):
    return ('    \'' + code + '\': { \'row\': {"fields": {"category": "' + cat
            + '", "abbr": "' + code + '", "name": "' + name + '", "status": "启用"}, "cells": ["'
            + code + '", "' + name + '", "<span class=\\"td-num\\">' + str(seq)
            + '</span>", "' + note + '", "<span class=\\"tag tag-green\\">启用</span>"], '
            + '"ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal(\'stopModal\')"}]} },')

# ---------- ① demo-data.js ----------
P = ROOT + r'\_data\demo-data.js'
t = io.open(P, encoding='utf-8', newline='').read()
assert t.count('\r\n') > 1000
assert t.count('FL-0') == 0 or True

# A1: WL 两行 → 6 行
A_WL = ('    \'WL-01\': { \'row\': {"fields": {"category": "物料类型", "abbr": "QJ", "name": "器具", '
        '"status": "启用"}, "cells": ["QJ", "器具", "<span class=\\"td-num\\">1</span>", '
        '"循环包装器具（围板箱/托盘/料箱/料架）", "<span class=\\"tag tag-green\\">启用</span>"], '
        '"ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal(\'stopModal\')"}]} },\r\n'
        '    \'WL-02\': { \'row\': {"fields": {"category": "物料类型", "abbr": "LBJ", "name": "零部件", '
        '"status": "启用"}, "cells": ["LBJ", "零部件", "<span class=\\"td-num\\">2</span>", '
        '"汽车零部件散件（对客销售件）", "<span class=\\"tag tag-green\\">启用</span>"], '
        '"ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal(\'stopModal\')"}]} },')
NEW_WL = '\r\n'.join([
    row('WL-01', '物料类型', '围板箱', '可折叠周转箱', 1),
    row('WL-02', '物料类型', '塑料托盘', '塑料栈板', 2),
    row('WL-03', '物料类型', '木托盘', '木质栈板', 3),
    row('WL-04', '物料类型', '料箱', '小型周转箱', 4),
    row('WL-05', '物料类型', '料架', '金属料架', 5),
    row('WL-06', '物料类型', '组件', '锁扣内衬等散件', 6)])
assert t.count(A_WL) == 1 or t.count(NEW_WL) == 1, 'WL 块既非改前也非改后态：%d/%d' % (t.count(A_WL), t.count(NEW_WL))
if t.count(A_WL) == 1:
    t = t.replace(A_WL, NEW_WL)
    print('PASS A1 WL 两行→6 行')
else:
    print('SKIP A1 WL 已是改后态')

# A2: FL 六行删除
FL_NOTES = ['可折叠周转箱', '塑料栈板', '木质栈板', '小型周转箱', '金属料架', '锁扣内衬等散件']
FL_NAMES = ['围板箱', '塑料托盘', '木托盘', '料箱', '料架', '组件']
fl_lines = [row('FL-%02d' % i, '物料分类', n, FL_NOTES[i-1], i) for i, n in enumerate(FL_NAMES, 1)]
A_FL = '\r\n'.join(fl_lines)
if t.count(A_FL) == 1:
    t = t.replace('\r\n' + A_FL, '')
    print('PASS A2 FL 六行删除')
else:
    assert t.count("'FL-0") == 0, 'FL 块锚 %d 且残留 %d' % (t.count(A_FL), t.count("'FL-0"))
    print('SKIP A2 FL 已删除')

# A3: products 段内 cls 托盘拆分 + info 分类 label
ps = t.find('\n  partners:')
pe = t.find('\n  bomVersions:', ps)
assert 0 < ps < pe
seg = t[ps:pe]
if seg.count('"cls": "托盘"') == 0 and seg.count('"cls": "木托盘"') == 1 and seg.count('"cls": "塑料托盘"') == 1:
    print('SKIP A3 cls 拆分已完成')
else:
    for old_cls, new_cls, nm in [('木托盘', '木托盘', '木托盘 1200×1000'), ('塑料托盘', '塑料托盘', '塑料托盘 1200×1000')]:
        A_C = '"name": "%s", "cls": "托盘"' % nm
        assert seg.count(A_C) == 1, '%s cls 锚 %d' % (nm, seg.count(A_C))
        seg = seg.replace(A_C, '"name": "%s", "cls": "%s"' % (nm, new_cls))
    # 同行 cells tag：按行处理
    lines = seg.split('\r\n')
    n_fix = 0
    for i, l in enumerate(lines):
        if '"cls": "木托盘"' in l and '>托盘</span>' in l:
            lines[i] = l.replace('>托盘</span>', '>木托盘</span>'); n_fix += 1
        elif '"cls": "塑料托盘"' in l and '>托盘</span>' in l:
            lines[i] = l.replace('>托盘</span>', '>塑料托盘</span>'); n_fix += 1
    assert n_fix == 2, 'cells tag 替换 %d≠2' % n_fix
    seg = '\r\n'.join(lines)
    t = t[:ps] + seg + t[pe:]
    print('PASS A3 cls 拆托盘×2')
# A4: info 分类 label（幂等）
n_lb = seg.count("'label': '分类'")
n_lb_new = seg.count("'label': '物料类型'")
assert n_lb + n_lb_new == 12, 'info 分类行 %d+%d≠12' % (n_lb, n_lb_new)
if n_lb == 12:
    seg = seg.replace("'label': '分类'", "'label': '物料类型'")
    t = t[:ps] + seg + t[pe:]
    print('PASS A4 info 分类→物料类型×12')
else:
    print('SKIP A4 info 已改')
io.open(P, 'w', encoding='utf-8', newline='').write(t)
r = subprocess.run(['node', '--check', P], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:200]
print('PASS ① demo-data.js：WL 6 行(分类值)+FL 删除+cls 拆托盘×2+info 分类→物料类型×12·node 0')

# ---------- ② 产品档案.html ----------
P2 = ROOT + r'\基础数据\产品档案.html'
t = io.open(P2, encoding='utf-8', newline='').read()
crlf2 = t.count('\r\n')
# B1 筛选 ff（幂等：完成态=物料类型 label+6 值 option）
if t.count('<span class="ff-label">物料类型：</span>') == 1 and t.count('<option>塑料托盘</option>') >= 1:
    print('SKIP B1-B4 产品档案 已是改后态')
else:
    A_F = ('<div class="ff"><span class="ff-label">物料分类：</span>\r\n'
           '      <select><option selected>全部</option><option>围板箱</option><option>托盘</option>'
           '<option>料箱</option><option>料架</option><option>组件</option></select>')
    assert t.count(A_F) == 1, '筛选锚 %d' % t.count(A_F)
    N_F = ('<div class="ff"><span class="ff-label">物料类型：</span>\r\n'
           '      <select><option selected>全部</option><option>围板箱</option><option>塑料托盘</option>'
           '<option>木托盘</option><option>料箱</option><option>料架</option><option>组件</option></select>')
    t = t.replace(A_F, N_F)
    # B2 列头
    assert t.count('<th>物料分类</th>') == 1
    t = t.replace('<th>物料分类</th>', '<th>物料类型</th>')
    # B3 cfg
    A_CFG = "{ label: '物料分类', field: 'cls' }"
    assert t.count(A_CFG) == 1
    t = t.replace(A_CFG, "{ label: '物料类型', field: 'cls' }")
    # B4 createModal 两行合一（页内嵌粘连格式）
    A_T = ('<span class="form-label"><span class="req">*</span>物料类型</span>\r\n'
           '    <div class="input-box select-box"><select style="flex:1;min-width:0;border:none;outline:none;'
           'background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;'
           '-webkit-appearance:none;"><option selected>器具</option><option>零部件</option></select>')
    assert t.count(A_T) == 1, '页内嵌类型行锚 %d' % t.count(A_T)
    # 类型行整行（含行尾结构）+分类行整行 → 一行
    i0 = t.find(A_T)
    # 类型行 form-row 起点
    fr0 = t.rfind('<div class="form-row">', 0, i0)
    # 分类行终点=其 </div>（form-row 收尾）+ 下一段起点
    A_C2 = ('<span class="form-label">物料分类</span>')
    assert t.count(A_C2) == 1
    i1 = t.find(A_C2)
    fr1_end = t.find('</div>\r\n', t.find('</select>', i1))
    assert fr1_end > i1 > i0 > fr0
    OLD_BLOCK = t[fr0:fr1_end + len('</div>\r\n')]
    SEL6 = ('<select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;'
            'color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;">'
            '<option selected>围板箱</option><option>塑料托盘</option><option>木托盘</option><option>料箱</option>'
            '<option>料架</option><option>组件</option></select>')
    NEW_BLOCK = ('<div class="form-row">\r\n'
                 '    <span class="form-label"><span class="req">*</span>物料类型</span>\r\n'
                 '    <div class="input-box select-box">' + SEL6 + '<span class="caret"><svg width="12" height="12" '
                 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
                 'stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>\r\n'
                 '  </div>\r\n')
    t = t.replace(OLD_BLOCK, NEW_BLOCK)
    assert t.count('器具</option>') == 0 and t.count('<option>零部件</option>') == 0, '页内嵌旧值残留'
    io.open(P2, 'w', encoding='utf-8', newline='').write(t)
    print('PASS ② 产品档案.html：筛选/列头/cfg/弹窗合并（CRLF %d 保持）' % crlf2)

# ---------- ③ 新建产品.html 模板（双层·粘连格式区段替换） ----------
P3 = ROOT + r'\基础数据\弹窗\新建产品.html'
t = io.open(P3, encoding='utf-8', newline='').read()
i0 = t.find('<span class="form-label"><span class="req">*</span>物料类型')
A_C3m = '<span class="form-label">物料分类</span>'
assert 0 < i0 and t.count(A_C3m) == 1
i1 = t.find(A_C3m)
fr0 = t.rfind('<div class="form-row">', 0, i0)
fr1_end = t.find('</div>\r\n', t.find('</select>', i1))
assert 0 < fr0 < i0 < i1 < fr1_end
OLD_BLOCK = t[fr0:fr1_end + len('</div>\r\n')]
SEL6 = ('<select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;'
        'color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;">'
        '<option selected>围板箱</option><option>塑料托盘</option><option>木托盘</option><option>料箱</option>'
        '<option>料架</option><option>组件</option></select>')
NEW_T3 = ('<div class="form-row">\r\n'
          '    <span class="form-label"><span class="req">*</span>物料类型</span>\r\n'
          '    <div class="input-box select-box">' + SEL6 +
          '<span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" '
          'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
          '<polyline points="6 9 12 15 18 9"/></svg></span></div>\r\n'
          '  </div>\r\n')
t = t.replace(OLD_BLOCK, NEW_T3)
assert t.count('器具</option>') == 0
io.open(P3, 'w', encoding='utf-8', newline='').write(t)
print('PASS ③ 新建产品.html 模板：两行合一')

# ---------- ④ 数据字典.html ----------
P4 = ROOT + r'\系统管理\数据字典.html'
t = io.open(P4, encoding='utf-8', newline='').read()
A_C3 = '<div class="dic-item"><span>物料类型</span><span class="cnt">2</span></div>'
assert t.count(A_C3) == 1
t = t.replace(A_C3, '<div class="dic-item"><span>物料类型</span><span class="cnt">6</span></div>')
A_C4 = '          <div class="dic-item"><span>物料分类</span><span class="cnt">6</span></div>\r\n'
assert t.count(A_C4) == 1, '物料分类 dic-item 锚 %d' % t.count(A_C4)
t = t.replace(A_C4, '')
n_dom = t.count('<div class="dic-item">') + t.count('<div class="dic-item active">')
assert n_dom == 23, 'dic-item %d≠23' % n_dom
io.open(P4, 'w', encoding='utf-8', newline='').write(t)
print('PASS ④ 数据字典.html：物料类型 cnt6·物料分类行删除·dic-item 23')
