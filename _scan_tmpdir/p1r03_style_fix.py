# -*- coding: utf-8 -*-
# 终修：功能点表 A/G 列按 0906 映射全表重刷 + J 列格式清洗 + 全簿井号风险扫描修复
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter

F = 'P1-R03-工期评估表-20260915.xlsx'
wb = load_workbook(F)
fail = []

# ---------- 1. 功能点表 A/G 列按 0906 着色重刷 ----------
fp = wb['功能点评估（全栈）']
VCOLOR = {'前置': 'FFF2F2F2', 'V1.0': 'FFDDEBF7', 'V1.1': 'FFE2EFDA', 'V2.0': 'FFFCE4D6', '各版': 'FFF2F2F2'}
fill_a = PatternFill('solid', start_color='FFDEEBF7')
n = 0
for r in range(4, 71):
    if not fp.cell(row=r, column=1).value: continue
    ver = fp.cell(row=r, column=7).value
    fp.cell(row=r, column=1).fill = fill_a
    if ver in VCOLOR:
        fp.cell(row=r, column=7).fill = PatternFill('solid', start_color=VCOLOR[ver])
        n += 1
    else:
        fail.append('r%d 版本异常 %r' % (r, ver))
print('A/G 列重刷 %d 行' % n)

# ---------- 2. J 列（评估人）格式清洗为 0906 口径 ----------
for r in range(4, 71):
    c = fp.cell(row=r, column=10)
    c.number_format = 'General'
    if c.alignment.horizontal != 'left':
        from copy import copy
        al = copy(c.alignment); al.horizontal = 'left'; c.alignment = al
print('J 列格式已清洗')

# ---------- 3. 全簿井号风险扫描（列级：需要宽 > 列宽*1.05） ----------
def need_width(cell):
    v = cell.value
    if v is None: return 0
    fmt = cell.number_format or 'General'
    if isinstance(v, float) or isinstance(v, int):
        s = ('%.2f' % v) if ('0.00' in fmt) else str(v)
        return len(s) + 1
    import datetime as _dt
    if isinstance(v, _dt.datetime) or isinstance(v, _dt.date):
        if 'mm-dd-yy' in fmt: return 9
        if fmt in ('d', '0'): return 3
        return 12
    s = str(v)
    if s.startswith('='): return 8
    wide = sum(2.05 if ord(ch) > 127 else 1.05 for ch in s[:60])
    line = s.count('\n') + 1
    return max(wide / max(1, line), 4)

fixes = []
for ws in wb.worksheets:
    need = {}
    for row in ws.iter_rows():
        for c in row:
            if c.value is None: continue
            w = need_width(c)
            if w > need.get(c.column, 0): need[c.column] = w
    for col, w in need.items():
        L = get_column_letter(col)
        cur = ws.column_dimensions[L].width or 8.43
        if w > cur * 1.08:
            # 只修数值/日期列（文本列在 0906 就窄，折行是设计）；判据：该列样本多为日期或数字
            kinds = [c.value for r2 in ws.iter_rows(min_col=col, max_col=col) for c in r2 if c.value is not None]
            import datetime as _dt2
            nd = sum(1 for v in kinds[:40] if isinstance(v, (_dt2.datetime, _dt2.date, int, float)) and not isinstance(v, bool))
            if kinds and nd / min(len(kinds), 40) > 0.6:
                ws.column_dimensions[L].width = round(max(cur, w + 1.2), 1)
                fixes.append('%s!%s %.0f→%.1f' % (ws.title, L, cur, ws.column_dimensions[L].width))
print('井号修复 %d 处: %s' % (len(fixes), fixes if fixes else '无'))

wb.save(F)
print('失败 %d 条' % len(fail))
for x in fail: print('  ' + x)
