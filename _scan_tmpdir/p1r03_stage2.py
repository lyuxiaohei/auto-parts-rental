# -*- coding: utf-8 -*-
# 甘特图原版样式上增量更新：轴 09-02 起 78 工作日、插 6 新行、带行/日期、CF 重建（修正 0914 滞后区间）
import datetime
from copy import copy, deepcopy
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.formatting.formatting import ConditionalFormattingList

F = 'P1-R03-工期评估表-20260915.xlsx'
wb = load_workbook(F)
D = lambda m, d: datetime.datetime(2026, m, d)
fail = []
def chk(c, m):
    if not c: fail.append(m)

def workdays(d1, d2, skip=frozenset([datetime.date(2026, 10, d) for d in range(1, 8)])):
    out, d = [], d1
    while d <= d2:
        if d.weekday() < 5 and d not in skip: out.append(d)
        d += datetime.timedelta(days=1)
    return out

AXIS = workdays(datetime.date(2026, 9, 2), datetime.date(2026, 12, 25))
chk(len(AXIS) == 78, '轴 %d≠78' % len(AXIS))

def rewrite_axis(ws, first_col, old_last_col):
    """轴头 78 天 + 月份带重排；返回新末列号"""
    new_last = first_col + len(AXIS) - 1
    # 抓月份带锚点样式与文本
    months = []
    for mr in ws.merged_cells.ranges:
        if mr.min_row == 3 and mr.min_col >= first_col:
            months.append((mr.min_col, mr.max_col, ws.cell(row=3, column=mr.min_col).value,
                           copy(ws.cell(row=3, column=mr.min_col)._style)))
    chk(len(months) == 4, '月份带 %d≠4' % len(months))
    for mr in [m for m in list(ws.merged_cells.ranges) if m.min_row == 3 and m.min_col >= first_col]:
        ws.unmerge_cells(str(mr))
    # 日期行样式基准
    st4 = copy(ws.cell(row=4, column=first_col)._style)
    for i, d in enumerate(AXIS):
        c = first_col + i
        cell = ws.cell(row=4, column=c, value=d)
        cell._style = st4
        cell.number_format = 'd'
    # 月份带按新月界重排
    style_m = months[0][3]
    prev = None; start = None
    spans = []
    for i, d in enumerate(AXIS + [None]):
        cur = d.month if d else None
        if cur != prev:
            if prev is not None: spans.append((start, i - 1, prev))
            start = i; prev = cur
    chk(len(spans) == 4, '月界 %d≠4' % len(spans))
    for (a, b, mon) in spans:
        c1, c2 = first_col + a, first_col + b
        cell = ws.cell(row=3, column=c1, value='%d月' % mon)
        cell._style = style_m
        ws.merge_cells(start_row=3, start_column=c1, end_row=3, end_column=c2)
    # 新增 3 列列宽
    wref = ws.column_dimensions[get_column_letter(old_last_col)].width
    for c in range(old_last_col + 1, new_last + 1):
        ws.column_dimensions[get_column_letter(c)].width = wref
    return new_last

def rebuild_cf(ws, first_col, last_col, last_row, bar_spans, milestone_rule_old):
    """bar_spans: [(start,end,fill_hex)]；milestone/today 全表范围"""
    captured = []
    for rng in ws.conditional_formatting:
        for rule in rng.rules:
            captured.append(rule)
    chk(len(captured) == 7, 'CF 规则 %d≠7' % len(captured))
    colL = get_column_letter(first_col); colR = get_column_letter(last_col)
    ms = next(r for r in captured if r.formula and str(r.formula[0]).startswith('OR('))
    td = next(r for r in captured if r.formula and 'TODAY' in str(r.formula[0]))
    fills = ['FFD9E2F3', 'FFDDEBF7', 'FFE2EFDA', 'FFFCE4D6', 'FFE7E6E6']
    old_bars = {str(r.dxf.fill.start_color.rgb): r for r in captured
                if r.formula and 'AND(' in str(r.formula[0]) and r.dxf and r.dxf.fill}
    ws.conditional_formatting = ConditionalFormattingList()
    ms2 = deepcopy(ms)
    ms2.formula = ['OR(%s$4=DATE(2026,10,20),%s$4=DATE(2026,11,24),%s$4=DATE(2026,12,14),%s$4=DATE(2026,12,25))' % (colL, colL, colL, colL)]
    ws.conditional_formatting.add('%s5:%s%d' % (colL, colR, last_row), ms2)
    ws.conditional_formatting.add('%s5:%s%d' % (colL, colR, last_row), td)
    for (a, b, hexv) in bar_spans:
        rule = old_bars[hexv]
        r2 = deepcopy(rule)
        r2.formula = ['AND(%s$4<>"",%s$4<=$%s%d,%s$4>=$%s%d)' % (colL, colL, rule.formula[0].split('$')[1][0], a, colL, rule.formula[0].split('$')[1][0], a)]
        ws.conditional_formatting.add('%s%d:%s%d' % (colL, a, colR, b), r2)
    return len(list(ws.conditional_formatting))

# ================= 任务级 =================
t = wb['甘特图-任务级']
# 1) 带行文本
t['A5'] = '前置（09-02 ~ 09-18 · 需求+原型+底座）'
for addr, olds in [('A15', ('V1.0 买卖版 ★ 10-16 上线', 'V1.0 买卖版 ★ 10-20 上线（09-15 增补·初估）')),
                   ('A38', ('V1.1 租赁版（含移动端 H5）★ 11-17 上线', 'V1.1 租赁版（含移动端 H5）★ 11-24 上线（初估）')),
                   ('A51', ('V2.0 深化版 ★ 12-07 上线', 'V2.0 深化版 ★ 12-14 上线（初估）'))]:
    chk(t[addr].value == olds[0], '%s=%r' % (addr, t[addr].value)); t[addr] = olds[1]
# 2) 解除下部带行合并（防插行错位）
for rng in ['A51:G51', 'A62:G62']:
    if rng in [str(m) for m in t.merged_cells.ranges]: t.unmerge_cells(rng)
# 3) 插 6 行（自下而上·样式抄上行 1..85 列）
NEW = [  # (pos, WBS, 功能点, 任务, 版本, 人日, 开始, 结束)
 (51, 'B6', '（待补）', '退款登记（一页双向）：应付退款（对供应商）/应收退款（对客户）', 'V1.1', 1, D(11, 3), D(11, 4)),
 (49, 'B4', '（待补）', '按持有量计租引擎：Σ(每日在租量×日租金)·天数=max(2,止−起+1)', 'V1.1', 2.5, D(10, 29), D(11, 2)),
 (49, 'B4', '（待补）', '转移出库单：列表+录单+详情+终止转移；结算方式两值·项目档案带出可覆盖', 'V1.1', 2, D(10, 26), D(10, 28)),
 (38, 'B8', '（待补）', '采购退货单：收货拒收/入库后退货·可退上限·关联采购入库', 'V1.0', 1.5, D(9, 29), D(9, 30)),
 (31, 'B5', '（待补）', '销售退货单：收货拒收/入库后退货·可退上限·关联销售出库', 'V1.0', 1.5, D(9, 23), D(9, 24)),
 (29, 'B3', '（待补）', '库存事件流水与每日在租量（按天计租数据基座·出库/退租/归还/调拨）', 'V1.0', 2.5, D(9, 25), D(9, 28)),
]
for pos, a, b, c, d_, e, f_, g_ in NEW:
    styles = [copy(t.cell(row=pos - 1, column=cc)._style) for cc in range(1, 86)]
    t.insert_rows(pos, 1)
    for cc, st in enumerate(styles, 1): t.cell(row=pos, column=cc)._style = st
    for cc, v in enumerate([a, b, c, d_, e, f_, g_], 1): t.cell(row=pos, column=cc).value = v
# 4) 找回带行并重合并
def find_band(prefix):
    for r in range(5, 90):
        v = str(t.cell(row=r, column=1).value or '')
        if v.startswith(prefix): return r
    return None
bands = {k: find_band(k) for k in ['前置（', 'V1.0 买卖版', 'V1.1 租赁版', 'V2.0 深化版', '各版支撑']}
chk(all(bands.values()), '带行定位 %s' % bands)
for k in ['V2.0 深化版', '各版支撑']:
    r = bands[k]; t.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
# 5) 静态 F/G 日期更新（按任务名/版本定位）
def setfg(prefix, f=None, g=None):
    for r in range(6, 90):
        if str(t.cell(row=r, column=3).value or '').startswith(prefix):
            if f: t.cell(row=r, column=6).value = f
            if g: t.cell(row=r, column=7).value = g
            return r
    fail.append('FG 定位失败: ' + prefix); return None
setfg('原型走查', D(9, 2), D(9, 14))
setfg('计费规则', None, D(9, 15))
setfg('PRD 评审', None, D(9, 18))
setfg('原型按评审反馈修订', D(9, 14), D(9, 18))
setfg('原型评审确认', D(9, 18), D(9, 18))
n2 = 0
for r in range(6, 90):
    if t.cell(row=r, column=4).value == 'V2.0':
        for c in (6, 7):
            v = t.cell(row=r, column=c).value
            if isinstance(v, datetime.datetime): t.cell(row=r, column=c).value = v + datetime.timedelta(days=7)
        n2 += 1
chk(n2 == 10, '任务级 V2.0 %d≠10' % n2)
CMAP = {'集成测试': (D(10, 13), D(12, 11)), 'UAT': (D(10, 19), D(12, 14)), '主数据': (D(10, 13), D(12, 9)),
        '期初库存': (D(10, 16), D(12, 10)), '迁移核对': (D(10, 19), D(12, 11)), '环境部署': (D(10, 19), D(12, 11)),
        '上线切换': (D(10, 20), D(12, 14)), '线上试运行': (D(10, 20), D(12, 25))}
for k, (a, b) in CMAP.items(): setfg(k, a, b)
# 6) 轴与月份带
new_last = rewrite_axis(t, 8, 82)
# 7) CF 重建（按新带行定数据区间）
spans = [(bands['前置（'] + 1, bands['V1.0 买卖版'] - 1, 'FFD9E2F3'),
         (bands['V1.0 买卖版'] + 1, bands['V1.1 租赁版'] - 1, 'FFDDEBF7'),
         (bands['V1.1 租赁版'] + 1, bands['V2.0 深化版'] - 1, 'FFE2EFDA'),
         (bands['V2.0 深化版'] + 1, bands['各版支撑'] - 1, 'FFFCE4D6'),
         (bands['各版支撑'] + 1, 76, 'FFE7E6E6')]
n_cf = rebuild_cf(t, 8, new_last, 76, spans, None)
# 8) 标题口径
t['A1'] = '甘特图 · 任务级（%d 行全量·0915 增补）' % (76 - 5 - 5)
t['A2'] = '口径：横轴 78 个工作日（09-02~12-25·周末与国庆 10-01~07 不排）；09-15 增补口径 +12.5 人日·153.75，节点 10-20/11-24/12-14（初估·开发重估后刷新）'

# ================= 功能点级 =================
g = wb['甘特图-功能点级']
g['A5'] = '前置（09-02 ~ 09-18 · 需求+原型+底座）'
g['A9'] = str(g['A9'].value).replace('10-16', '10-20')
g['A17'] = str(g['A17'].value).replace('11-17', '11-24')
g['A24'] = str(g['A24'].value).replace('12-07', '12-14')
OV = [
 (6, '需求调研与 PRD（四轮走查+计费定案 09-15+评审冻结·09-18）', 6, D(9, 2), D(9, 18)),
 (7, '原型改造与定稿（G31~G39·128+ HTML·09-18 定稿）', 1, D(9, 14), D(9, 18)),
 (12, '仓储 V1.0（采购入库/库存查询五态/销售出库/其他出入库/调拨/库存事件流水）', 14, D(9, 11), D(9, 28)),
 (13, '销售订单（代下单+审核+附件/关闭+销售退货单）', 4.5, D(9, 11), D(9, 24)),
 (14, '财务（应收六来源含按天期段化 + 回款）', 5, D(9, 17), D(9, 23)),
 (15, '系统权限（6 角色·矩阵 19 类）', 1.5, D(9, 24), D(9, 25)),
 (16, '采购域（订单/审核/入库发起/买卖线/采购退货单）+ 站内信', 8, D(9, 21), D(9, 30)),
 (19, '看板 / 详情 / 我的待办（19 类）', 5, D(9, 25), D(10, 13)),
 (21, '计费（直录日租金）+ 租赁单 + 转移出库 + 持有量计租引擎', 11, D(10, 12), D(11, 2)),
 (22, '应付五来源（租入对称按天计租）+ 付款登记 + 退款登记', 6, D(9, 17), D(11, 4)),
 (27, '财务收口（开票/银行回单核销/财务看板）', 8, D(11, 18), D(11, 30)),
 (28, '操作日志 + 数据字典（28 组 141 项·物料类型 10 值）', 1.5, D(11, 20), D(11, 23)),
 (30, '集成测试 / UAT（F01 七泳道·轮 10-13/11-16/12-08）', 17, D(10, 13), D(12, 14)),
 (31, '数据迁移（主数据/期初五态导库/核对）', 13, D(10, 13), D(12, 11)),
 (32, '部署 / 切换 / 试运行', 15, D(10, 19), D(12, 25)),
]
for r, b, c, d_, e in OV:
    g.cell(row=r, column=2).value = b
    g.cell(row=r, column=3).value = c
    g.cell(row=r, column=4).value = d_
    g.cell(row=r, column=5).value = e
for r in (25, 26):  # 租入三单/路凯 V2.0 +7d
    for c in (4, 5):
        v = g.cell(row=r, column=c).value
        if isinstance(v, datetime.datetime): g.cell(row=r, column=c).value = v + datetime.timedelta(days=7)
new_last2 = rewrite_axis(g, 6, 80)
spans2 = [(6, 8, 'FFD9E2F3'), (10, 16, 'FFDDEBF7'), (18, 23, 'FFE2EFDA'), (24, 28, 'FFFCE4D6'), (30, 32, 'FFE7E6E6')]
n_cf2 = rebuild_cf(g, 6, new_last2, 32, spans2, None)
g['A1'] = '甘特图 · WBS × 版本（23 行概览·0915 增补）'
g['A2'] = t['A2'].value

wb.save(F)
print('失败 %d 条｜任务级 CF 组=%d 功能点级 CF 组=%d｜带行=%s' % (len(fail), n_cf, n_cf2, bands))
for x in fail: print('  ' + x)
