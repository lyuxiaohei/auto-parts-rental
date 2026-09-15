# -*- coding: utf-8 -*-
"""出货单打印：P1-R08 页数口径 + P1-R01 附录10.2 P3-R01 行尾追加"""
import io

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
FAILS = []
def rd(p):
    return io.open(ROOT + '\\' + p, encoding='utf-8', newline='').read()
def wr(p, t):
    io.open(ROOT + '\\' + p, 'w', encoding='utf-8', newline='').write(t)

# ---------- P1-R08 ----------
p = r'P1-R08-项目文件索引.md'
t = rd(p)
old = '### 3.1 `P3-R01-包装租赁管理后台原型/`（128 HTML = PC 123 + mobile 5·G33 后口径）'
if '129 HTML' in t:
    print('P1-R08 已刷，跳过')
else:
    assert t.count(old) == 1, '3.1 标题锚=%d' % t.count(old)
    t = t.replace(old, '### 3.1 `P3-R01-包装租赁管理后台原型/`（129 HTML = PC 124 + mobile 5·09-15 出货单打印页 +1·D-144）')
    wr(p, t)
    print('P1-R08 页数口径已刷')

# ---------- P1-R01 附录 10.2 ----------
p = r'P1-R01-需求梳理与功能框架.md'
t = rd(p)
if '出货单打印' in t:
    print('P1-R01 已登记，跳过')
else:
    anchor = '（详见 agent-handoff/20260911-G22-租赁出库称呼统一与杂项清理.md）。注：本文档正文'
    assert t.count(anchor) == 1, '10.2 P3-R01 行尾锚=%d' % t.count(anchor)
    add = ('**09-15·出货单打印页（D-144）**：+`租赁管理/出货单打印.html`（列表操作栏「打印出货单」进入·?key=CK-xxx 数据驱动·'
           '单据版式=送货单·可打印·菜单外上下文页）——128→129 HTML；同批租赁出库录单页简化（备注移入基本信息·删随箱资料与「其他信息」模块）。'
           '（G33/G34/G35/G36B1 等后续沿革见 agent-handoff/ 各任务档与 _AGENT基线 快照）注：本文档正文')
    t = t.replace(anchor, add, 1)
    wr(p, t)
    print('P1-R01 附录10.2 P3-R01 行已追加')

for f in FAILS:
    print('FAIL:', f)
print('DONE')
