# -*- coding: utf-8 -*-
# 汇总 sheet 重排：值/公式不动，修表头错位/数字格式/列宽冲突（合并单元格分域借宽）
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

F = 'P1-R03-工期评估表-20260915.xlsx'
wb = load_workbook(F)
hs = wb['汇总']
fail = []

NAVY = 'FF1F4E79'; PARAMBG = 'FFF2F2F2'; BAND = 'FFDEEBF7'
THIN = Side(style='thin', color='FFBFBFBF'); MED = Side(style='medium', color=NAVY)
BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
F_TITLE = Font(bold=True, size=13, color=NAVY)
F_SEC = Font(bold=True, size=10, color=NAVY)
F_HDR = Font(name='Calibri', bold=True, size=10, color='FFFFFFFF')
F_DAT = Font(size=9); F_DATB = Font(size=9, bold=True)
FILL_HDR = PatternFill('solid', start_color=NAVY)
FILL_PARAM = PatternFill('solid', start_color=PARAMBG)
FILL_TOT = PatternFill('solid', start_color=BAND)
AL_C = Alignment(horizontal='center', vertical='center', wrap_text=True)
AL_CN = Alignment(horizontal='center', vertical='center')
AL_L = Alignment(horizontal='left', vertical='center', wrap_text=True)

# ---------- 1. 实测定位区界 ----------
def find_row(txt):
    for r in range(1, 60):
        v = str(hs.cell(row=r, column=1).value or '') + str(hs.cell(row=r, column=2).value or '')
        if txt in v: return r
    return None
sec = {'wbs_hdr': 3, 'mile': find_row('版本里程碑'), 'month': find_row('按月负载'),
       'ai': find_row('AI 协作'), 'param': find_row('参数与折算'), 'sum18': find_row('合计')}
chk = lambda k: fail.append('%s 定位失败' % k) if not sec[k] else None
for k in ['mile', 'month', 'ai', 'param', 'sum18']: chk(k)
if fail:
    print('\n'.join(fail)); raise SystemExit(1)

# ---------- 2. 全表先清旧样式痕迹（只清 fill/font/align，保值与公式） ----------
for r in range(1, 52):
    for c in range(1, 9):
        cell = hs.cell(row=r, column=c)
        cell.border = BD

# ---------- 3. 标题与表头 ----------
hs.cell(1, 1).font = F_TITLE
for r, hdr_cols in [(sec['wbs_hdr'], range(1, 7)), (sec['mile'] + 1, range(1, 9)), (sec['month'] + 1, range(1, 6))]:
    for c in hdr_cols:
        cell = hs.cell(row=r, column=c)
        if cell.value is None: continue
        cell.font = F_HDR; cell.fill = FILL_HDR; cell.alignment = AL_C
    hs.row_dimensions[r].height = 20
for r in [sec['mile'], sec['month'], sec['ai'], sec['param']]:
    for c in range(1, 9):
        hs.cell(row=r, column=c).font = F_SEC
        hs.cell(row=r, column=c).border = Border()

# ---------- 4. WBS 区（r4~r17 + 合计 r18） ----------
for r in range(4, 18):
    hs.cell(r, 1).font = F_DATB; hs.cell(r, 1).alignment = AL_CN
    hs.cell(r, 2).font = F_DAT; hs.cell(r, 2).alignment = AL_L
    hs.cell(r, 3).font = F_DAT; hs.cell(r, 3).alignment = AL_CN; hs.cell(r, 3).number_format = '0.##'
    for c in (4, 5):
        cell = hs.cell(r, c); cell.font = F_DAT; cell.alignment = AL_CN; cell.number_format = 'yyyy-mm-dd'
    hs.cell(r, 6).font = Font(size=8.5); hs.cell(r, 6).alignment = AL_L
    hs.merge_cells(start_row=r, start_column=6, end_row=r, end_column=8)
    hs.row_dimensions[r].height = 22
r18 = sec['sum18']
for c in range(1, 9):
    cell = hs.cell(r18, c)
    if cell.value is None: continue
    cell.font = F_DATB; cell.fill = FILL_TOT
    cell.border = Border(left=THIN, right=THIN, top=MED, bottom=THIN)
    cell.alignment = AL_CN if c != 1 else AL_L
    if c == 3: cell.number_format = '0.##'

# ---------- 5. 里程碑区（标题+1 表头；数据 +2 起 6 行；校验行随后） ----------
m0 = sec['mile'] + 2
for i in range(6):
    r = m0 + i
    for c in range(1, 9):
        cell = hs.cell(r, column=c)
        if cell.value is None: continue
        cell.font = F_DAT; cell.border = BD
        if c in (1, 2): cell.alignment = AL_CN
        elif c == 3: cell.alignment = AL_L
        elif c in (4, 5):
            cell.alignment = AL_CN; cell.number_format = '0.##'; cell.fill = FILL_PARAM
        elif c in (6, 7): cell.alignment = AL_CN; cell.number_format = 'yyyy-mm-dd'
        else: cell.alignment = AL_CN
    hs.row_dimensions[r].height = 30
rchk = m0 + 6
for c in range(1, 9):
    cell = hs.cell(rchk, column=c)
    if cell.value is None: continue
    cell.font = F_DATB; cell.alignment = AL_CN; cell.number_format = '0.##' if c >= 4 else 'General'
    cell.border = Border(left=THIN, right=THIN, top=THIN, bottom=MED)

# ---------- 6. 按月负载区 ----------
k0 = sec['month'] + 2
for i in range(5):
    r = k0 + i
    last = (i == 4)
    for c in range(1, 6):
        cell = hs.cell(r, column=c)
        if cell.value is None: continue
        cell.font = F_DATB if last else F_DAT
        cell.alignment = AL_CN if c <= 4 else AL_L
        if c in (2, 3): cell.number_format = '0.##'
        if c == 4: cell.number_format = '0%'
        cell.border = BD
    hs.merge_cells(start_row=r, start_column=5, end_row=r, end_column=8)
    hs.row_dimensions[r].height = 22

# ---------- 7. AI 风险区（标题行+1 起 5 行） ----------
a0 = sec['ai'] + 1
for i in range(5):
    r = a0 + i
    hs.cell(r, 1).font = F_DATB; hs.cell(r, 1).alignment = AL_CN
    hs.cell(r, 2).font = F_DATB; hs.cell(r, 2).alignment = AL_CN
    hs.cell(r, 3).font = Font(size=8.5); hs.cell(r, 3).alignment = AL_L
    for c in range(1, 9): hs.cell(r, c).border = BD
    hs.merge_cells(start_row=r, start_column=3, end_row=r, end_column=8)
    hs.row_dimensions[r].height = 20

# ---------- 8. 参数区 ----------
p0 = sec['param'] + 1
for i in range(6):
    r = p0 + i
    hs.cell(r, 1).font = F_DAT; hs.cell(r, 1).alignment = AL_L
    hs.cell(r, 3).font = F_DATB; hs.cell(r, 3).alignment = AL_CN; hs.cell(r, 3).fill = FILL_PARAM
    hs.cell(r, 3).number_format = '0.0' if i >= 4 else '0.##'
    hs.cell(r, 4).font = Font(size=8.5); hs.cell(r, 4).alignment = AL_L
    for c in range(1, 9): hs.cell(r, c).border = BD
    hs.merge_cells(start_row=r, start_column=4, end_row=r, end_column=8)

# ---------- 9. 列宽与视图 ----------
for L, w in zip('ABCDEFGH', [10, 20, 42, 11, 11, 14, 12, 13]):
    hs.column_dimensions[L].width = w
hs.sheet_view.showGridLines = False

wb.save(F)
mg = len(hs.merged_cells.ranges)
print('重排完成：区界=%s｜合并 %d 处（WBS 风险 F:H×14·按月摘要 E:H×5·AI 描述 C:H×5·参数注记 D:H×6）' % (sec, mg))
