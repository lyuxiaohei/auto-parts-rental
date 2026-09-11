# -*- coding: utf-8 -*-
"""G15 T4 · 支 SVG 两行重排（读取-精确替换+assert 计数）
S1 切 4+3；S5 切 3+3；S2/S3/S4 +44；S5 +44；S6 +76；支图例 +108；viewBox→0 0 880 846。
偏差：S6 三行注记文档目标 (200,706/720/734) 与 +76 后 chips(y=696-732) 相撞 → 实取 (200,746/760/774)。"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

F = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\P3-R01-F01-业务流程导航图.html')
lines = open(F, encoding='utf-8', newline='').read().split('\n')

def find_line(anchor):
    idx = [i for i, ln in enumerate(lines) if anchor in ln]
    assert len(idx) == 1, f'锚点不唯一/缺失 [{anchor}]: {len(idx)} 行'
    return idx[0]

def shift_y(anchor, off, expect, label):
    i = find_line(anchor)
    new, n = re.subn(r'y([12]?)="(\d+)"', lambda m: f'y{m.group(1)}="{int(m.group(2))+off}"', lines[i])
    assert n == expect, f'ASSERT FAIL [{label}]: y属性数={n} expect={expect}'
    lines[i] = new
    print(f'  OK [{label}] y{off:+d} ×{n}')

def xform(anchor, subs, label):
    i = find_line(anchor)
    ln = lines[i]
    for old, new, cnt in subs:
        c = ln.count(old)
        assert c == cnt, f'ASSERT FAIL [{label}] {old}: count={c} expect={cnt}'
        ln = ln.replace(old, new)
    lines[i] = ln
    print(f'  OK [{label}]')

def rep(old, new, label):
    global lines
    joined = '\n'.join(lines)
    c = joined.count(old)
    if c == 0 and new in joined:
        print(f'  [幂等跳过] {label}')
        return
    assert c == 1, f'ASSERT FAIL [{label}]: count={c}'
    joined = joined.replace(old, new)
    lines = joined.split('\n')
    print(f'  OK [{label}]')

M6 = ' fill="#6b7280" font-size="8" font-family="\'Geist Mono\',monospace">'
M4 = ' fill="#4b5563" font-size="8" font-family="\'Geist Mono\',monospace">'

print('== S1 切 4+3 ==')
xform('其他入库列表.html"><rect x="744"', [('x="744"','x="200"',1),('x="804"','x="260"',2),('y="20"','y="64"',1),('y="36"','y="80"',1),('y="50"','y="94"',1)], 'S1-chip5→(200,64)')
xform('其他出库列表.html"><rect x="880"', [('x="880"','x="336"',1),('x="940"','x="396"',2),('y="20"','y="64"',1),('y="36"','y="80"',1),('y="50"','y="94"',1)], 'S1-chip6→(336,64)')
xform('退租入库列表.html"><rect x="1016"', [('x="1016"','x="472"',1),('x="1076"','x="532"',2),('y="20"','y="64"',1),('y="36"','y="80"',1),('y="50"','y="94"',1)], 'S1-chip7→(472,64)')
rep(f'<text x="1016" y="72"{M6}来源：T1 退租拆散（L2/L4）</text>',
    f'<text x="608" y="76"{M6}来源：T1 退租拆散（L2/L4）</text>', 'S1来源注记→(608,76)')
rep(f'<text x="336" y="72"{M6}盘点差异 → 盘盈转其他入库 · 盘亏转其他出库</text>',
    f'<text x="336" y="116"{M6}盘点差异 → 盘盈转其他入库 · 盘亏转其他出库</text>', 'S1盘点注记→(336,116)')
rep(f'<text x="200" y="86"{M6}库存状态口径：在途＝应入库未入库（退租待入库/采购到货/租入到货/调拨在途）· 租入＝在库未转租，转租后计入客户态</text>',
    f'<text x="200" y="130"{M6}库存状态口径：在途＝应入库未入库（退租待入库/采购到货/租入到货/调拨在途）· 租入＝在库未转租，转租后计入客户态</text>', 'S1口径注记→(200,130)')

print('== S2 +44 ==')
shift_y('S2 · 项目经营</text>', 44, 1, 'S2标题')
shift_y('<line x1="320" y1="158"', 44, 6, 'S2箭头×3')
shift_y('项目看板.html"><rect', 44, 3, 'S2-chip1')
shift_y('项目档案.html"><rect', 44, 3, 'S2-chip2')
shift_y('项目详情.html"><rect', 44, 3, 'S2-chip3')
shift_y('盈亏报表.html"><rect', 44, 3, 'S2-chip4')
rep(f'<text x="760" y="162"{M4}上下游绑定 <a href="项目管理/弹窗/上下游绑定.html" fill="#2563eb">弹窗</a> · 详情页可查全流程明细</text>',
    f'<text x="200" y="238"{M4}上下游绑定 <a href="项目管理/弹窗/上下游绑定.html" fill="#2563eb">弹窗</a> · 详情页可查全流程明细</text>', 'S2注记→(200,238)')

print('== S3 +44 ==')
shift_y('S3 · 系统支撑</text>', 44, 1, 'S3标题')
shift_y('用户权限.html"><rect', 44, 3, 'S3-chip1')
shift_y('数据字典.html"><rect', 44, 3, 'S3-chip2')
shift_y('操作日志.html"><rect x="472"', 44, 3, 'S3-chip3')
shift_y('角色权限矩阵', 44, 1, 'S3注记')

print('== S4 +44（口径注记拆两行） ==')
shift_y('S4 · 赔偿转单据</text>', 44, 1, 'S4标题')
shift_y('应付账单.html"><rect x="200" y="380"', 44, 3, 'S4-汇总框')
shift_y('<line x1="320" y1="396"', 44, 2, 'S4-上分线')
shift_y('<rect x="350" y="378"', 44, 1, 'S4-自有tag框')
shift_y('<text x="366" y="387"', 44, 1, 'S4-自有tag文')
shift_y('应收账单.html"><rect x="412" y="364"', 44, 3, 'S4-应收chip')
shift_y('<line x1="320" y1="420"', 44, 2, 'S4-下分线')
shift_y('<rect x="350" y="426"', 44, 1, 'S4-租入tag框')
shift_y('<text x="366" y="435"', 44, 1, 'S4-租入tag文')
shift_y('应付账单.html"><rect x="412" y="416"', 44, 3, 'S4-应付chip')
rep(f'<text x="624" y="408"{M4}口径：不走独立赔偿单，按对象直接生成应收/应付账单（带费用分类，09-08 会议）；核销库存（其他出库 · 赔偿核销，09-05 王琳总）</text>',
    f'<text x="200" y="514"{M4}口径：不走独立赔偿单，按对象直接生成应收/应付账单（带费用分类，09-08 会议）；</text>\n'
    f'    <text x="200" y="528"{M4}核销库存（其他出库 · 赔偿核销，09-05 王琳总）</text>', 'S4口径注记拆两行→(200,514/528)')

print('== S5 +44 切 3+3 ==')
shift_y('S5 · 录单页与台账</text>', 44, 1, 'S5标题')
shift_y('采购入库录单.html"><rect', 44, 3, 'S5-chip1')
shift_y('组合出库录单.html"><rect x="336"', 44, 3, 'S5-chip2')
shift_y('组合出库录单.html"><rect x="472"', 44, 3, 'S5-chip3')
xform('盘点录入.html"><rect x="608"', [('x="608"','x="200"',1),('x="668"','x="260"',2),('y="500"','y="588"',1),('y="516"','y="604"',1),('y="530"','y="618"',1)], 'S5-chip4→(200,588)')
xform('BOM维护.html"><rect x="744"', [('x="744"','x="336"',1),('x="804"','x="396"',2),('y="500"','y="588"',1),('y="516"','y="604"',1),('y="530"','y="618"',1)], 'S5-chip5→(336,588)')
xform('租赁单列表.html"><rect x="880"', [('x="880"','x="472"',1),('x="965"','x="532"',2),('y="500"','y="588"',1),('y="516"','y="604"',1),('y="530"','y="618"',1)], 'S5-chip6→(472,588)')
rep(f'<text x="1082" y="522"{M4}录单页由列表页"新增/录入"进入</text>',
    f'<text x="200" y="638"{M4}录单页由列表页"新增/录入"进入</text>', 'S5注记→(200,638)')

print('== S6 +76（注记下移避让 chips） ==')
shift_y('S6 · 审核与待办</text>', 76, 1, 'S6标题')
shift_y('<line x1="320" y1="638"', 76, 2, 'S6箭头1')
shift_y('<line x1="456" y1="638"', 76, 2, 'S6箭头2')
shift_y('<line x1="592" y1="638"', 76, 2, 'S6箭头3')
shift_y('我的待办.html"><rect', 76, 3, 'S6-chip1')
shift_y('采购入库审核.html"><rect', 76, 3, 'S6-chip2')
shift_y('销售订单列表.html"><rect', 76, 3, 'S6-chip3')
shift_y('操作日志.html"><rect x="608"', 76, 3, 'S6-chip4')
rep(f'<text x="760" y="626"{M4}15 类单据统一进待办（订单/出入库/租赁/退租/盘点/调拨/</text>',
    f'<text x="200" y="746"{M4}15 类单据统一进待办（订单/出入库/租赁/退租/盘点/调拨/</text>', 'S6注记1→(200,746)')
rep(f'<text x="760" y="640"{M4}付款、收款/租入单据；赔偿/组装/拆卸随模块移除）；</text>',
    f'<text x="200" y="760"{M4}付款、收款/租入单据；赔偿/组装/拆卸随模块移除）；</text>', 'S6注记2→(200,760)')
rep(f'<text x="760" y="654"{M4}<tspan fill="#111827" font-weight="600">状态流范本＝销售订单</tspan>（待审核/已审核/待发货/已完成/已关闭）</text>',
    f'<text x="200" y="774"{M4}<tspan fill="#111827" font-weight="600">状态流范本＝销售订单</tspan>（待审核/已审核/待发货/已完成/已关闭）</text>', 'S6注记3→(200,774)')

print('== 支图例 +108 ==')
shift_y('<line x1="40" y1="684"', 108, 2, '支图例线')
shift_y('<text x="40" y="704"', 108, 1, '支图例标')
shift_y('<rect x="120" y="694"', 108, 1, '支图例框1')
shift_y('<text x="140" y="704"', 108, 1, '支图例文1')
shift_y('<rect x="264" y="694"', 108, 1, '支图例框2')
shift_y('<text x="284" y="704"', 108, 1, '支图例文2')
shift_y('<rect x="408" y="694"', 108, 1, '支图例框3')
shift_y('<text x="428" y="704"', 108, 1, '支图例文3')
shift_y('<line x1="552" y1="700"', 108, 2, '支图例箭头')
shift_y('<text x="576" y="704"', 108, 1, '支图例文4')
shift_y('<text x="684" y="704"', 108, 1, '支图例文5')

rep('<svg viewBox="0 0 1280 724"', '<svg viewBox="0 0 880 846"', '支viewBox→880×846')

open(F, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('T4 写盘完成')
