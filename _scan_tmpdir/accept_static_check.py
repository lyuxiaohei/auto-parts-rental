# -*- coding: utf-8 -*-
"""任务一·静态验收（2026-09-08）：数据层 + 25 弹窗覆盖三要素 + L3/L4 反查"""
import sys, io, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
DD = PROTO / '_data' / 'demo-data.js'

results = []
def check(item, ok, detail=''):
    results.append((item, ok, detail))
    print(('✅' if ok else '❌'), '|', item, '|', detail)

# ---------- 1. 数据层 ----------
# 1a. node --check 语法
r = subprocess.run(['node', '--check', str(DD)], capture_output=True, text=True)
check('1a demo-data.js node 语法通过', r.returncode == 0, r.stderr.strip()[:120])

# 1b. 解析实体与键（文本级：实体行=2空格缩进 name: {，键行=4空格 'key': {）
src = DD.read_text(encoding='utf-8')
ent_re = re.compile(r"^  ([A-Za-z_][A-Za-z0-9_]*): \{$", re.M)
key_re = re.compile(r"^    '([^']+)': \{$", re.M)
ents = {}
spans = [(m.group(1), m.start()) for m in ent_re.finditer(src)]
for i, (name, pos) in enumerate(spans):
    end = spans[i + 1][1] if i + 1 < len(spans) else len(src)
    keys = key_re.findall(src[pos:end])
    ents[name] = keys
n_ent = len(ents)
check('1b 实体数=33', n_ent == 33, f'{n_ent} 实体: {", ".join(list(ents)[:6])}...')

# 1c. 每实体内键唯一（文本级重复键检测）
dups = {e: [k for k in set(ks) if ks.count(k) > 1] for e, ks in ents.items()}
dups = {e: v for e, v in dups.items() if v}
check('1c 每实体内单号键唯一', not dups, str(dups) if dups else '33 实体全部唯一')

total = sum(len(v) for v in ents.values())
check('1d 记录总数=212', total == 212, f'实际 {total}')

# 1e. 抽 10 个新实体单号反查 L3/L4 数据链文件命中（列表页 HTML 中存在该单号）
L34 = [  # (实体, 键, 所在列表页)
    ('rentInOrders', 'RZD-20260815-003', '采购管理/租入单列表.html'),
    ('rentInbounds', 'RZRK-20260816-021', '仓储作业/租入入库列表.html'),
    ('leaseOrders', 'ZL-20260816-029', '销售管理/租赁单列表.html'),
    ('returnApplies', 'TZSQ-20260903-005', '租赁管理/退租申请列表.html'),
    ('returnInbounds', 'TZRK-20260903-009', '仓储作业/退租入库列表.html'),
    ('rentInReturns', 'GHCK-20260903-001', '仓储作业/租入归还列表.html'),
    ('rentInOrders', 'RZD-20260815-005', '采购管理/租入单列表.html'),
    ('assemblyOrders', 'ZZ-20260822-006', '仓储作业/组装列表.html'),
    ('leaseOrders', 'ZL-20260823-033', '销售管理/租赁单列表.html'),
    ('comboOutbounds', 'CK-20260824-009', '仓储作业/组合出库列表.html'),
]
ok10, miss = True, []
for ent, key, page in L34:
    hit_ent = key in ents.get(ent, [])
    hit_page = key in (PROTO / page).read_text(encoding='utf-8')
    if not (hit_ent and hit_page):
        ok10 = False; miss.append(f'{key}(实体{hit_ent}/页面{hit_page})')
check('1e L3/L4 链 10 单号反查命中', ok10, '；'.join(miss) if miss else '10/10 实体键+列表页 HTML 双命中')

# ---------- 2. 25 弹窗覆盖三要素 ----------
MODALS = [  # (序号, 实体, 列表页, 模板页, 锚文本, modalId)
    (1, 'leaseOrders', '销售管理/租赁单列表.html', '销售管理/弹窗/租赁单详情.html', '详情', 'detailModal'),
    (2, 'rentInOrders', '采购管理/租入单列表.html', '采购管理/弹窗/租入单详情.html', '详情', 'detailModal'),
    (3, 'comboOutbounds', '仓储作业/组合出库列表.html', '仓储作业/弹窗/组合出库单详情.html', '详情', 'detailModal'),
    (4, 'returnInbounds', '仓储作业/退租入库列表.html', '仓储作业/弹窗/退租入库单详情.html', '详情', 'detailModal'),
    (5, 'returnApplies', '租赁管理/退租申请列表.html', '租赁管理/弹窗/退租申请详情.html', '详情', 'detailModal'),
    (6, 'damageOrders', '租赁管理/丢损赔偿单.html', '租赁管理/弹窗/丢损赔偿单详情.html', '详情', 'detailModal'),
    (7, 'rentInReturns', '仓储作业/租入归还列表.html', '仓储作业/弹窗/租入归还单详情.html', '详情', 'detailModal'),
    (8, 'rentInbounds', '仓储作业/租入入库列表.html', '仓储作业/弹窗/租入入库单详情.html', '详情', 'detailModal'),
    (9, 'purchaseOrders', '采购管理/采购订单列表.html', '采购管理/弹窗/采购订单详情.html', '详情', 'detailModal'),
    (10, 'salesOrders', '销售管理/销售订单列表.html', '销售管理/弹窗/销售订单详情.html', '详情', 'detailModal'),
    (11, 'purchaseInbounds', '仓储作业/采购入库列表.html', '仓储作业/弹窗/采购入库单详情.html', '详情', 'detailModal'),
    (12, 'salesOutbounds', '仓储作业/销售出库列表.html', '仓储作业/弹窗/销售出库单详情.html', '详情', 'detailModal'),
    (13, 'otherInbounds', '仓储作业/其他入库列表.html', '仓储作业/弹窗/其他入库单详情.html', '详情', 'detailModal'),
    (14, 'otherOutbounds', '仓储作业/其他出库列表.html', '仓储作业/弹窗/其他出库单详情.html', '详情', 'detailModal'),
    (15, 'assemblyOrders', '仓储作业/组装列表.html', '仓储作业/弹窗/组装单详情.html', '详情', 'detailModal'),
    (16, 'disassemblyOrders', '仓储作业/拆卸管理列表.html', '仓储作业/弹窗/拆卸单详情.html', '详情', 'detailModal'),
    (17, 'stocktakes', '仓储作业/盘点列表.html', '仓储作业/弹窗/盘点单详情.html', '详情', 'detailModal'),
    (18, 'transfers', '仓储作业/库存调拨列表.html', '仓储作业/弹窗/调拨单详情.html', '详情', 'detailModal'),
    (19, 'stockFlows', '仓储作业/库存查询.html', '仓储作业/弹窗/库存流水.html', '库存流水', 'flowModal'),
    (20, 'rentTracks', '租赁管理/租出台账.html', '租赁管理/弹窗/器具出租履历.html', '详情', 'trackModal'),
    ('20b', 'assetTracks', '租赁管理/在租台账.html', '(共用20模板)', '资产轨迹', 'trackModal'),
    (21, 'partners', '基础数据/客商管理.html', '基础数据/弹窗/客商详情.html', '详情', 'detailModal'),
    (22, 'appliances', '基础数据/器具档案.html', '基础数据/弹窗/器具详情.html', '详情', 'detailModal'),
    (23, 'parts', '基础数据/零部件档案.html', '基础数据/弹窗/零部件详情.html', '详情', 'detailModal'),
    (24, 'locations', '基础数据/库位档案.html', '基础数据/弹窗/库位详情.html', '详情', 'detailModal'),
    (25, 'bomVersions', '基础数据/BOM维护.html', '基础数据/弹窗/BOM版本查看.html', '查看', 'bomViewModal'),
]
rows2 = []
for no, ent, page, tpl, anchor, modal_id in MODALS:
    lp = PROTO / page
    txt = lp.read_text(encoding='utf-8')
    wired = (f"renderListPage({{" in txt and f"entity: '{ent}'" in txt) or f"wireDetailModal('{ent}'" in txt
    skel = 'id="detailTitle"' in txt and 'id="detailBody"' in txt
    if tpl.startswith('('):
        tpl_ok = True  # 共用模板，20 号已查
    else:
        tp = PROTO / tpl
        tpl_ok = tp.exists() and 'id="detailTitle"' in tp.read_text(encoding='utf-8')
    rows2.append((no, ent, wired, skel, tpl_ok))
    if not (wired and skel and tpl_ok):
        check(f'2 覆盖 #{no} {ent}', False, f'接线{wired}/骨架{skel}/模板{tpl_ok}')
n_ok = sum(1 for r in rows2 if r[2] and r[3] and r[4])
check('2 25 弹窗三要素在位（接线+骨架+模板）', n_ok == len(MODALS), f'{n_ok}/{len(MODALS)}（含20b在租台账分页）')

# ---------- 3. 09-07 业务补充行实体建全 ----------
biz = [
    ('receivableBills', 'AR-2026-09-PRJ2601-YS', '应收·预收行'),
    ('payableBills', 'AP-20260905-012', '应付·预付行'),
    ('returnApplies', 'TZSQ-20260904-009', '退租申请·部分退租行'),
    ('otherOutbounds', 'QTCK-20260905-005', '其他出库·赔偿核销行'),
    ('assemblyOrders', 'ZZ-20260904-007', '组装·拆散件再组装行'),
    ('rentTracks', 'ZL-20260903-034', '租出台账·循环再出租行'),
]
miss3 = [f'{e}:{k}' for e, k, _ in biz if k not in ents.get(e, [])]
check('3 09-07 业务补充行实体建全', not miss3, '6/6 全在' if not miss3 else '缺 ' + str(miss3))

# 驳回重提 ZL-20260905-035：goal 命令点名（若页面有此行）
zl_page = (PROTO / '销售管理/租赁单列表.html').read_text(encoding='utf-8')
has_row = 'ZL-20260905-035' in zl_page
has_ent = 'ZL-20260905-035' in ents.get('leaseOrders', [])
check('3b 驳回重提 ZL-20260905-035 口径', (not has_row) or (has_row and has_ent),
     f'页面行={has_row} 实体键={has_ent}' + ('（页面无此行则不强求实体）' if not has_row else ''))

print()
fails = [r for r in results if not r[1]]
print(f'==== 静态验收汇总：{len(results)} 项，失败 {len(fails)} 项 ====')
json.dump({'results': results, 'ents': {k: len(v) for k, v in ents.items()}},
          open(ROOT / '_scan_tmpdir' / 'accept_static_out.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
sys.exit(1 if fails else 0)
