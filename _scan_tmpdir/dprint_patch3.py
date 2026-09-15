# -*- coding: utf-8 -*-
"""出货单打印：A02 + P1-R08 登记"""
import io, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
FAILS = []
def rd(p):
    return io.open(ROOT + '\\' + p, encoding='utf-8', newline='').read()
def wr(p, t):
    io.open(ROOT + '\\' + p, 'w', encoding='utf-8', newline='').write(t)

# ---------- A02 ----------
p = r'P3-R01-包装租赁管理后台原型\P3-R01-A02-页面类型与入口对照表.md'
t = rd(p)
if '出货单打印' in t:
    print('A02 已登记，跳过')
else:
    eol = '\r\n' if '\r\n' in t else '\n'
    old13 = '- **菜单外页面 17 个**（G36 B1 前 5＋页面化 12，见第五节 G36 B1 子节）'
    new13 = '- **菜单外页面 18 个**（G36 B1 前 5＋页面化 12＋出货单打印 1，见第五节 G36 B1 子节）'
    assert t.count(old13) == 1
    t = t.replace(old13, new13)
    anchor = '| 17 | 租赁管理/租赁出库录单.html | 租赁出库录单 | 表单页 | 租赁出库列表「新增出库单」（菜单外） | — |'
    assert t.count(anchor) == 1, 'A02 行17锚=%d' % t.count(anchor)
    add = (anchor + eol +
      '| 18 | 租赁管理/出货单打印.html | 出货单打印 | 打印页（单据版式=送货单·D-144） | 租赁出库列表操作栏「打印出货单」（菜单外·?key=CK-xxx 数据驱动） | comboOutbounds/bomList |')
    t = t.replace(anchor, add)
    wr(p, t)
    print('A02：菜单外 18 个 + 行18 登记')

# ---------- P1-R08 ----------
p2 = r'P1-R08-项目文件索引.md'
t2 = rd(p2)
if '出货单打印' in t2:
    print('P1-R08 已登记，跳过')
else:
    # 找 租赁出库录单 行
    m = re.search(r'^.*租赁出库录单\.html.*$', t2, re.M)
    assert m, 'P1-R08 录单行未找到'
    line = m.group(0)
    eol2 = '\r\n' if '\r\n' in t2 else '\n'
    new_line = line + eol2 + line.replace('租赁出库录单', '出货单打印').replace('录单', '打印页（送货单版式·D-144·?key=）', 1) if False else line + eol2 + '| 租赁管理/出货单打印.html | 出货单打印页（送货单版式·D-144·列表操作栏进入·?key=CK-xxx） |'
    # 若是表格行保持 | 前缀；若为列表行保持 - 前缀——统一用与原行相同前缀风格
    prefix = line[:2] if line.startswith('- ') else ('| ' if line.startswith('|') else '- ')
    if not line.startswith('|'):
        new_line = line + eol2 + prefix + '租赁管理/出货单打印.html —— 出货单打印页（送货单版式·D-144·列表操作栏「打印出货单」进入·?key=CK-xxx 数据驱动）'
    t2 = t2.replace(line, new_line, 1)
    wr(p2, t2)
    print('P1-R08：出货单打印行已加（沿原行风格 %s...）' % prefix.strip())

for f in FAILS:
    print('FAIL:', f)
print('DONE' if not FAILS else 'HAS FAILS')
