# -*- coding: utf-8 -*-
"""G39 T1 事件流结构化 · demo-data 手术（精确替换＋断言＋幂等）
改体：comboOutbounds / returnInbounds / rentInReturns 三实体
  1) row.fields 增 mat/matName/qty/unit（数量从文本提为字段）
  2) 退租入库/租入归还 fees 首列补「物料编码」（feeCols 同步）
  3) returnInbounds info 中 8 处「关联租赁单」块清退（D-106 对齐）
"""
import io, re, sys

P = r'P3-R01-包装租赁管理后台原型\_data\demo-data.js'
raw = io.open(P, 'rb').read().decode('utf-8')
orig = raw
NL = '\r\n'
assert raw.count('\r\n') == raw.count('\n'), 'not pure CRLF'

def rec_span(s, key):
    """实体内记录切片（单引号键 'KEY': { 形态）"""
    m = re.search(r"^    '%s': \{" % re.escape(key), s, re.M)
    assert m, 'record not found: ' + key
    start = m.start()
    nxt = re.search(r"^    '[^']+': \{", s[m.end():], re.M)
    end = m.end() + nxt.start() if nxt else len(s)
    return start, end

def rec_replace(s, key, old, new, cnt=1):
    a, b = rec_span(s, key)
    seg = s[a:b]
    assert seg.count(old) == cnt, 'anchor %r in %s count=%d expect=%d' % (old[:60], key, seg.count(old), cnt)
    return s[:a] + seg.replace(old, new, cnt) + s[b:]

# ---------- 1) comboOutbounds fields 增量 ----------
CK = [
 ('CK-20260910-022', 'ZH-2603-B × 30 套', 'ZH-2603-B', '冲压件料箱组套', '30', '套'),
 ('CK-20260914-023', '塑料托盘 1200×1000 × 50 只', 'PLT-1210P', '塑料托盘 1200×1000', '50', '只'),
 ('CK-20260903-016', 'ZH-2601-A × 60 套（退租回库件循环出库）', 'ZH-2601-A', '驾驶室围板箱整箱套件', '60', '套'),
 ('CK-20260830-015', 'ZH-2601-A × 180 套', 'ZH-2601-A', '驾驶室围板箱整箱套件', '180', '套'),
 ('CK-20260830-014', 'ZH-2602-B × 120 套', 'ZH-2602-B', '冲压件料箱组套', '120', '套'),
 ('CK-20260829-013', 'ZH-2603-C × 60 套', 'ZH-2603-C', '电池托盘护角套件', '60', '套'),
 ('CK-20260829-012', 'ZH-2601-A × 120 套', 'ZH-2601-A', '驾驶室围板箱整箱套件', '120', '套'),
 ('CK-20260828-011', 'ZH-2601-A × 96 套', 'ZH-2601-A', '驾驶室围板箱整箱套件', '96', '套'),
 ('CK-20260824-009', 'ZH-2604-D 混合组合套件 × 40 套', 'ZH-2604-D', '混合组合套件', '40', '套'),
 ('CK-20260828-010', 'ZH-2602-B × 200 套', 'ZH-2602-B', '冲压件料箱组套', '200', '套'),
]
for key, combo, mat, matName, qty, unit in CK:
    old = '"combo": "%s", ' % combo
    if '"mat": ' in raw[rec_span(raw, key)[0]:rec_span(raw, key)[1]]:  # 幂等
        continue
    new = '"combo": "%s", "mat": "%s", "matName": "%s", "qty": "%s", "unit": "%s", ' % (combo, mat, matName, qty, unit)
    raw = rec_replace(raw, key, old, new)

# ---------- 2) returnInbounds fields 增量 ----------
TZ = [
 ('TZRK-20260902-010', 'ZH-2604-D 混合组合套件（自购隔板 + 租入大箱）', 'ZH-2604-D', '混合组合套件（自购隔板 + 租入大箱）', '40', '套'),
 ('TZRK-20260903-009', 'WBX-1210L 围板箱 1200×1000×970（租入）', 'WBX-1210L', '围板箱 1200×1000×970（租入）', '30', '只'),
 ('TZRK-20260902-008', 'ZH-2601-A 驾驶室围板箱整箱套件', 'ZH-2601-A', '驾驶室围板箱整箱套件', '60', '套'),
 ('TZRK-20260901-007', 'ZH-2602-B 冲压件料箱组套', 'ZH-2602-B', '冲压件料箱组套', '45', '套'),
 ('TZRK-20260831-006', 'ZH-2603-C 电池托盘护角套件', 'ZH-2603-C', '电池托盘护角套件', '20', '套'),
 ('TZRK-20260828-005', 'BTC-6040 料箱', 'BTC-6040', '料箱', '200', '只'),
 ('TZRK-20260825-004', 'PLT-1210P 塑料托盘', 'PLT-1210P', '塑料托盘', '150', '块'),
 ('TZRK-20260820-003', 'ZH-2601-A 驾驶室围板箱整箱套件', 'ZH-2601-A', '驾驶室围板箱整箱套件', '30', '套'),
]
for key, appl, mat, matName, qty, unit in TZ:
    a, b = rec_span(raw, key)
    if '"mat": ' in raw[a:b]:
        continue
    old = '"appliance": "%s", ' % appl
    new = '"appliance": "%s", "mat": "%s", "matName": "%s", "qty": "%s", "unit": "%s", ' % (appl, mat, matName, qty, unit)
    raw = rec_replace(raw, key, old, new)

# ---------- 3) rentInReturns fields 增量 ----------
GH = [
 ('GHCK-20260903-001', '围板箱 1200×1000×970', 'WBX-1210L', '围板箱 1200×1000×970', '30', '只'),
 ('GHCK-20260903-002', '围板箱 1200×1000×970（退租拆散后归还）', 'WBX-1210L', '围板箱 1200×1000×970（退租拆散后归还）', '4', '只'),
 ('GHCK-20260831-003', '金属料箱 800×600', 'BTC-6040', '金属料箱 800×600', '20', '只'),  # 800×600 无独立 SKU·取最近料箱码（演示近似·执行记录注记）
]
for key, appl, mat, matName, qty, unit in GH:
    a, b = rec_span(raw, key)
    if '"mat": ' in raw[a:b]:
        continue
    old = '"appliance": "%s", ' % appl
    new = '"appliance": "%s", "mat": "%s", "matName": "%s", "qty": "%s", "unit": "%s", ' % (appl, mat, matName, qty, unit)
    raw = rec_replace(raw, key, old, new)

# ---------- 4) returnInbounds feeCols + fees 首列物料编码 ----------
OLD_FC = "'feeCols': ['物料', '来源', '单位', '数量', '去向']"
NEW_FC = "'feeCols': ['物料编码', '物料名称', '来源', '单位', '数量', '去向']"
cnt = raw.count(OLD_FC)
assert cnt == 8, 'returnInbounds feeCols count=%d expect 8' % cnt
raw = raw.replace(OLD_FC, NEW_FC)

TZFEES = [  # (记录键, 旧行首格元组, 新编码)
 ('TZRK-20260902-010', "'cells': ['折叠隔板', '自购', '件', '80'", 'LJ-F600'),
 ('TZRK-20260902-010', "'cells': ['围板箱大箱 1200×1000×970', '租入 · 环通', '只', '10'", 'WBX-1210L'),
 ('TZRK-20260903-009', "'cells': ['WBX-1210L 围板箱 1200×1000×970', '租入 · 环通', '只', '30'", 'WBX-1210L'),
 ('TZRK-20260902-008', "'cells': ['围板', '自购', '件', '120'", 'LJ-C300'),
 ('TZRK-20260902-008', "'cells': ['箱体', '自购', '只', '60'", 'WBX-1210L'),
 ('TZRK-20260902-008', "'cells': ['锁扣组件', '自购', '件', '240'", 'LJ-A100'),
 ('TZRK-20260901-007', "'cells': ['料箱', '自购', '只', '45'", 'BTC-6040'),
 ('TZRK-20260901-007', "'cells': ['隔板', '自购', '件', '90'", 'LJ-F600'),
 ('TZRK-20260831-006', "'cells': ['托盘', '自购', '件', '20'", 'PLT-1210P'),
 ('TZRK-20260831-006', "'cells': ['护角', '自购', '件', '80'", 'LJ-F600'),
 ('TZRK-20260828-005', "'cells': ['BTC-6040 料箱', '自购', '只', '200'", 'BTC-6040'),
 ('TZRK-20260825-004', "'cells': ['PLT-1210P 塑料托盘', '自购', '块', '150'", 'PLT-1210P'),
 ('TZRK-20260820-003', "'cells': ['围板', '自购', '件', '60'", 'LJ-C300'),
 ('TZRK-20260820-003', "'cells': ['箱体', '自购', '只', '30'", 'WBX-1210L'),
 ('TZRK-20260820-003', "'cells': ['锁扣组件', '自购', '件', '120'", 'LJ-A100'),
]
for key, line, code in TZFEES:
    a, b = rec_span(raw, key)
    seg = raw[a:b]
    # 幂等：新行已存在则跳过
    if line.replace("'cells': ['", "'cells': ['%s', '" % code, 1) in seg:
        continue
    new_line = line.replace("'cells': ['", "'cells': ['%s', '" % code, 1)
    raw = rec_replace(raw, key, line, new_line)

# ---------- 5) rentInReturns feeCols + fees 编码列 ----------
OLD_FC2 = "'feeCols': ['序号', '器具', '归还类型', '单位', '数量', '状况']"
NEW_FC2 = "'feeCols': ['序号', '物料编码', '物料名称', '归还类型', '单位', '数量', '状况']"
cnt = raw.count(OLD_FC2)
assert cnt == 3, 'rentInReturns feeCols count=%d expect 3' % cnt
raw = raw.replace(OLD_FC2, NEW_FC2)
GHFEES = [
 ('GHCK-20260903-001', "'cells': ['1', '围板箱 1200×1000×970', '整退归还', '只', '30'", 'WBX-1210L'),
 ('GHCK-20260903-002', "'cells': ['1', '围板箱 1200×1000×970', '分流归还', '只', '4'", 'WBX-1210L'),
 ('GHCK-20260831-003', "'cells': ['1', '金属料箱 800×600', '整退归还', '只', '20'", 'BTC-6040'),
]
for key, line, code in GHFEES:
    new_line = line.replace("'cells': ['1', '", "'cells': ['1', '%s', '" % code, 1)
    raw = rec_replace(raw, key, line, new_line)

# ---------- 6) returnInbounds info 关联租赁单块清退（D-106） ----------
m0 = re.search(r'^  returnInbounds: \{', raw, re.M)
m1 = re.search(r'^  rentInReturns: \{', raw, re.M)
assert m0 and m1, 'entity block not found'
seg = raw[m0.start():m1.start()]
pat = re.compile(r"\{[^{}]*?'label': '关联租赁单'[^{}]*?\},\r\n")
hits = pat.findall(seg)
assert len(hits) == 8, '关联租赁单 blocks=%d expect 8' % len(hits)
seg2 = pat.sub('', seg)
assert seg2.count('关联租赁单') == 0
raw = raw[:m0.start()] + seg2 + raw[m1.start():]

# ---------- 校验 ----------
assert raw.count('"mat": "') >= 21, 'mat fields inserted=%d' % raw.count('"mat": "')
assert '关联租赁单' not in raw[raw.find('returnInbounds:'):raw.find('rentInReturns:')], 'returnInbounds 关联租赁单 残留'
assert raw != orig
io.open(P, 'wb').write(raw.encode('utf-8'))
print('[T1] OK · mat fields=%d · feeCols 改 8+3 · 关联租赁单清退 8' % raw.count('"mat": "'))
