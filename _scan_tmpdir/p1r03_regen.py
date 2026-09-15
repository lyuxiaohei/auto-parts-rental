# -*- coding: utf-8 -*-
# P1-R03-20260915 全新生生：0906 样式规格 × 0915 数据集；只产 xlsx，不动任何其他文件
import shutil, datetime
from copy import copy
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.formatting import ConditionalFormattingList
from openpyxl.formatting.rule import Rule
from openpyxl.styles.differential import DifferentialStyle

BASE = '_scan_tmpdir/backup-g30-20260914/P1-R03-工期评估表-20260906.xlsx'
CUR = 'P1-R03-工期评估表-20260915.xlsx'
OUT = '_scan_tmpdir/P1-R03-工期评估表-20260915-重新生成.xlsx'

# ---------- 0906 样式规格 ----------
NAVY = 'FF1F4E79'; BANDGRAY = 'FF595959'; MONTHBG = 'FFEDF2F9'; PARAMBG = 'FFF2F2F2'
VC = {'前置': 'FFF2F2F2', 'V1.0': 'FFDDEBF7', 'V1.1': 'FFE2EFDA', 'V2.0': 'FFFCE4D6', '各版': 'FFF2F2F2'}
THIN = Side(style='thin', color='FFBFBFBF')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
F_HDR = Font(name='Calibri', bold=True, size=10, color='FFFFFFFF')
F_TITLE = Font(bold=True, size=13, color=NAVY)
F_SEC = Font(bold=True, size=10, color=NAVY)
F_DAT = Font(size=9)
F_DAY = Font(size=8, color=BANDGRAY)
F_BAND = Font(bold=True, size=9, color='FFFFFFFF')
F_MONTH = Font(bold=True, size=9, color=NAVY)
AL_C = Alignment(horizontal='center', vertical='center', wrap_text=True)
AL_C1 = Alignment(horizontal='center', vertical='center')
AL_L = Alignment(horizontal='left', vertical='center', wrap_text=True)
FILL_HDR = PatternFill('solid', start_color=NAVY)
FILL_BAND = PatternFill('solid', start_color=BANDGRAY)
FILL_MONTH = PatternFill('solid', start_color=MONTHBG)
FILL_PARAM = PatternFill('solid', start_color=PARAMBG)
FILL_A = PatternFill('solid', start_color='FFDEEBF7')

def workdays(d1, d2, skip=frozenset([datetime.date(2026, 10, d) for d in range(1, 8)])):
    out, d = [], d1
    while d <= d2:
        if d.weekday() < 5 and d not in skip: out.append(d)
        d += datetime.timedelta(days=1)
    return out
AXIS = workdays(datetime.date(2026, 9, 2), datetime.date(2026, 12, 25))

# ---------- 数据集：从现 0915 读取 ----------
cur = load_workbook(CUR)
cfp = cur['功能点评估（全栈）']; chs = cur['汇总']; ct = cur['甘特图-任务级']; cg = cur['甘特图-功能点级']
rows = []
for r in range(4, 72):
    if not cfp.cell(row=r, column=1).value: continue
    rows.append([cfp.cell(row=r, column=c).value for c in range(1, 14)])
assert len(rows) == 68, len(rows)
tot = sum(x[7] for x in rows if isinstance(x[7], (int, float)))

def grab(ws, r1, r2, c1, c2):
    return [[ws.cell(row=r, column=c).value for c in range(c1, c2 + 1)] for r in range(r1, r2 + 1)]

sum_all = grab(chs, 1, 50, 1, 8)          # 汇总全量值/公式
gtask = grab(ct, 6, 77, 1, 7)              # 任务级 meta
gov = grab(cg, 6, 32, 1, 5)                # 功能点级 meta
bands_t = {str(ct.cell(row=r, column=1).value): r for r in [5, 15, 41, 58, 69]}
# 任务级按现带行切分 meta：直接扫描重建（带行也在 gtask 里？带行在 5/15/41/58/69，grab 从 6 起——单独取带文本
band_texts = [ct.cell(row=r, column=1).value for r in sorted(bands_t.values())]
# 重算任务级数据行归属（按现 0915 的 D 列版本序列，含带行位置）
task_seq = []
for r in range(6, 78):
    a = ct.cell(row=r, column=1).value
    if a in (None, ''): continue
    task_seq.append([ct.cell(row=r, column=c).value for c in range(1, 8)] + [r in set(bands_t.values())])

# ---------- 生成 ----------
shutil.copy(BASE, OUT)
wb = load_workbook(OUT)
for nm in ['汇总', '甘特图-功能点级', '甘特图-任务级', '功能点评估（全栈）']:
    if nm in wb.sheetnames: wb.remove(wb[nm])

# ============ 功能点评估（全栈） ============
fp = wb.create_sheet('功能点评估（全栈）')
fp.cell(1, 1, 'P1-R03 工期评估表 · 功能点级（全栈口径）').font = F_TITLE
note = cfp.cell(2, column=1).value
fp.cell(2, 1, note).font = Font(size=9, color='FF6B7280')
hdr = ['WBS', '模块/阶段', '功能点', '任务', '类型', '对应原型页面', '版本', '人日',
       '含缓冲人日\n（=人日×1.15）', '评估人', '开始时间', '结束时间', '备注（风险/依赖）']
for c, h in enumerate(hdr, 1):
    cell = fp.cell(3, c, h); cell.font = F_HDR; cell.fill = FILL_HDR; cell.alignment = AL_C; cell.border = BORDER
for i, x in enumerate(rows):
    r = 4 + i
    ver = x[6]
    for c, v in enumerate(x, 1):
        cell = fp.cell(r, c)
        if c == 9:
            cell.value = '=H%d*(1+汇总!$C$46)' % r
        else:
            cell.value = v
        cell.font = F_DAT; cell.border = BORDER
        if c == 1: cell.fill = FILL_A; cell.alignment = AL_C1
        elif c == 7: cell.fill = PatternFill('solid', start_color=VC.get(ver, 'FFFFFFFF')); cell.alignment = AL_C1
        elif c in (2, 5, 10, 11, 12): cell.alignment = AL_C1
        elif c == 8: cell.alignment = AL_C1; cell.number_format = '0.##'
        elif c in (11, 12) or (c in (11, 12)): pass
        else: cell.alignment = AL_L
    fp.cell(r, 11).number_format = 'mm-dd-yy'; fp.cell(r, 11).alignment = AL_C1
    fp.cell(r, 12).number_format = 'mm-dd-yy'; fp.cell(r, 12).alignment = AL_C1
    fp.cell(r, 9).number_format = '0.##'; fp.cell(r, 9).alignment = AL_C1
for L, w in zip('ABCDEFGHIJKLM', [6, 15, 11, 38, 6, 26, 7, 13, 12, 9, 12, 13, 34]):
    fp.column_dimensions[L].width = w
fp.freeze_panes = 'A4'

# ============ 汇总 ============
hs = wb.create_sheet('汇总', 0)
for r in range(1, 51):
    for c in range(1, 9):
        v = sum_all[r - 1][c - 1]
        if v is None: continue
        hs.cell(r, c, v)
for r in range(1, 51):
    for c in range(1, 9):
        cell = hs.cell(r, c)
        if cell.value is None: continue
        if r == 1: cell.font = F_TITLE; continue
        if r in (19, 29, 37, 44): cell.font = F_SEC; continue
        if r in (3, 20, 30):
            cell.font = F_HDR; cell.fill = FILL_HDR; cell.alignment = AL_C; cell.border = BORDER; continue
        cell.font = F_DAT; cell.border = BORDER
        cell.alignment = AL_C if c != 3 else AL_L
        if r == 28: cell.font = F_SEC
for r in range(22, 28):
    hs.cell(r, 4).fill = FILL_PARAM; hs.cell(r, 5).fill = FILL_PARAM
for rr, cc in [(46, 3), (47, 3), (48, 3)]:
    hs.cell(rr, cc).fill = FILL_PARAM
for L, w in zip('ABCDEFGH', [10, 16, 44, 10, 10, 12, 12, 13]):
    hs.column_dimensions[L].width = w

# ============ 甘特构建函数 ============
def build_gantt(name, idx, meta_hdr, first_col, data_rows, band_spec, fday_fmt_col):
    """band_spec: [(row_offset 前行数, 文本, 颜色)]；data_rows: [(vals, ver, start, end, is_band, band_text)]"""
    ws = wb.create_sheet(name, idx)
    n0 = len(meta_hdr)
    # r3 表头 + r4 轴
    for c, h in enumerate(meta_hdr, 1):
        cell = ws.cell(3, c, h); cell.font = F_HDR; cell.fill = FILL_HDR; cell.alignment = AL_C1; cell.border = BORDER
    prev = None; mstart = None
    for i, d in enumerate(AXIS):
        c = first_col + i
        cell = ws.cell(4, c, d); cell.font = F_DAY; cell.alignment = AL_C1; cell.number_format = 'd'
        ws.cell(3, c).border = BORDER
        if prev is None or d.month != prev.month:
            if mstart is not None:
                ws.merge_cells(start_row=3, start_column=mstart, end_row=3, end_column=c - 1)
            mstart = c
            mc = ws.cell(3, c, '%d月' % d.month); mc.font = F_MONTH; mc.fill = FILL_MONTH; mc.alignment = AL_C1; mc.border = BORDER
        prev = d
    ws.merge_cells(start_row=3, start_column=mstart, end_row=3, end_column=first_col + len(AXIS) - 1)
    ws.row_dimensions[3].height = 14.5
    # 数据/带行
    r = 5
    sec_spans = []
    for item in data_rows:
        if item[-1]:  # 带行
            band = ws.cell(r, 1, item[1]); band.font = F_BAND; band.fill = FILL_BAND; band.border = BORDER
            for c in range(2, first_col):
                bc = ws.cell(r, c); bc.fill = FILL_BAND; bc.border = BORDER
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=first_col - 1)
            strip = ws.cell(r, first_col)
            if item[2]:
                strip.fill = PatternFill('solid', start_color=item[2])
            r += 1
        else:
            vals, ver = item[0], item[1]
            for c, v in enumerate(vals[:n0], 1):
                cell = ws.cell(r, c, v); cell.font = F_DAT; cell.border = BORDER
                if c == 1: cell.alignment = AL_C1; cell.font = Font(bold=True, size=9)
                elif c == n0 - 1: cell.alignment = AL_L
                else: cell.alignment = AL_C1
                if c in (n0 - 1, n0): cell.number_format = 'm/d'
                if c == n0 - 2: cell.number_format = '0.##'
            r += 1
    last_row = r - 1
    # 列宽/冻结
    widths = {1: 6, 2: 10, 3: 40, 4: 7, 5: 6, 6: 8, 7: 8}
    for c in range(1, first_col + 1):
        ws.column_dimensions[get_column_letter(c)].width = widths.get(c, 9)
    for i in range(len(AXIS)):
        ws.column_dimensions[get_column_letter(first_col + i)].width = 2.64
    ws.freeze_panes = '%s5' % get_column_letter(first_col)
    return ws, last_row

def add_cf(ws, first_col, last_row, spans, ref_end, ref_start):
    colL = get_column_letter(first_col); colR = get_column_letter(first_col + len(AXIS) - 1)
    ws.conditional_formatting = ConditionalFormattingList()
    def dxf(hexv):
        return DifferentialStyle(fill=PatternFill(bgColor=hexv))
    r1 = Rule(type='expression', dxf=dxf('FFFCE4EC'),
              formula=['OR(%s$4=DATE(2026,10,20),%s$4=DATE(2026,11,24),%s$4=DATE(2026,12,14),%s$4=DATE(2026,12,25))' % (colL, colL, colL, colL)])
    r2 = Rule(type='expression', dxf=dxf('FFFFF2CC'), formula=['%s$4=TODAY()' % colL])
    ws.conditional_formatting.add('%s5:%s%d' % (colL, colR, last_row), r1)
    ws.conditional_formatting.add('%s5:%s%d' % (colL, colR, last_row), r2)
    fills = ['FFD9E2F3', 'FFDDEBF7', 'FFE2EFDA', 'FFFCE4D6', 'FFE7E6E6']
    for (a, b), fl in zip(spans, fills):
        rule = Rule(type='expression', dxf=dxf(fl),
                    formula=['AND(%s$4<>"",%s$4<=$%s%d,%s$4>=$%s%d)' % (colL, colL, ref_end, a, colL, ref_start, a)])
        ws.conditional_formatting.add('%s%d:%s%d' % (colL, a, colR, b), rule)

# 任务级数据行组装（带行按当前 0915 序列）
tdata = [(None, ct.cell(row=5, column=1).value, 'FF595959', True, ct.cell(row=5, column=1).value)]
spans_raw = []
cur_sec = None
for item in task_seq:
    is_band = item[-1]
    if is_band:
        tdata.append((None, item[0], 'FF595959', True, item[0]))
        cur_sec = item[3] if isinstance(item[3], str) else cur_sec
    else:
        tdata.append((item[:7], item[3], None, False, None))
# 计算 spans：带行行号（组装完成后全序列重扫，含补在头部的带）
band_rows = [i + 5 for i, x in enumerate(tdata) if x[3]]
spans = []
for i, br in enumerate(band_rows):
    end = (band_rows[i + 1] - 1) if i + 1 < len(band_rows) else len(tdata) + 4
    spans.append((br + 1, end))
assert len(spans) == 5, spans
last_row_t = len(tdata) + 4
wt, lr_t = build_gantt('甘特图-任务级', 3, ['WBS', '功能点', '任务', '版本', '人日', '开始', '结束'], 8, tdata, None, None)
add_cf(wt, 8, lr_t, spans, 'G', 'F')
wt['A1'] = '甘特图 · 任务级（%d 行全量·0915 增补）' % sum(1 for x in tdata if not x[3]); wt['A1'].font = F_TITLE
wt['A2'] = '口径：横轴 78 个工作日（09-02~12-25·周末与国庆不排）；09-15 增补口径 153.75 人日·节点 10-20/11-24/12-14（初估·开发重估后刷新）'; wt['A2'].font = Font(size=9, color='FF6B7280')

# 功能点级（带行固定 5 组位置由数据重排：前置3 + V1.0组 + V1.1组 + V2.0组 + 各版组）
# 从 gov（现 0915 的 6..32 行，含带行位置 9/17/24/29）重组
gdata = [(None, cg.cell(row=5, column=1).value, 'FF595959', True, cg.cell(row=5, column=1).value)]
gspans = []
r = 6
i = 0
while i < len(gov):
    row = gov[i]
    if row[0] and (str(row[0]).startswith(('前置（', 'V1.0 ', 'V1.1 ', 'V2.0 ', '各版')) and not row[1]):
        gdata.append((None, row[0], 'FF595959', True, row[0]))
        i += 1; continue
    gdata.append((row, row[0], None, False, None))
    i += 1
band_rows_g = [i2 + 5 for i2, x in enumerate(gdata) if x[3]]
for j, br in enumerate(band_rows_g):
    end = (band_rows_g[j + 1] - 1) if j + 1 < len(band_rows_g) else len(gdata) + 4
    gspans.append((br + 1, end))
assert len(gspans) == 5, gspans
wg, lr_g = build_gantt('甘特图-功能点级', 2, ['WBS', '模块 / 内容', '人日', '开始', '结束'], 6, gdata, None, None)
add_cf(wg, 6, lr_g, gspans, 'E', 'D')
wg['A1'] = '甘特图 · WBS × 版本（%d 行概览·0915 增补）' % sum(1 for x in gdata if not x[3]); wg['A1'].font = F_TITLE
wg['A2'] = wt['A2'].value; wg['A2'].font = Font(size=9, color='FF6B7280')

wb._sheets = [wb['版本交付阶梯图'], wb['汇总'], wg, wt, fp]
wb.save(OUT)
print('生成完成：%s｜功能点 %d 行=%.2f｜任务级 %d 行（带 %d）｜功能点级 %d 行（带 %d）' % (
    OUT, len(rows), tot, sum(1 for x in tdata if not x[3]), len(band_rows), sum(1 for x in gdata if not x[3]), len(band_rows_g)))
