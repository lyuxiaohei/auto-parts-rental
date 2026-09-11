# -*- coding: utf-8 -*-
"""G16 T1: 从 demo-data dump + 38 页 cfg 逆向提取字段字典 → P3-R01-A05-字段字典.md
标签优先级（任务书 D2 写死）：cfg filter label > info/cells 值反查 label > 键语义直译+待核
"""
import json, re, pathlib, collections, html as htmllib

ROOT = pathlib.Path(__file__).resolve().parent.parent          # 项目根
PROT = ROOT / 'P3-R01-包装租赁管理后台原型'
D = json.loads((ROOT / '_scan_tmpdir/g16_data_dump.json').read_text(encoding='utf-8'))

# ---------- 1. 页面消费关系 + filters 标签 ----------
entity_pages = collections.defaultdict(list)   # ent -> [(page, title)]
entity_filters = collections.defaultdict(dict) # ent -> {field: label}
for f in sorted(PROT.rglob('*.html')):
    if 'backup' in str(f) or 'mobile' in f.parts: continue
    s = f.read_text(encoding='utf-8')
    m = re.search(r'<title>([^<]*)</title>', s)
    title = (m.group(1).replace(' - 包装租赁管理后台', '') if m else f.stem)
    rel = str(f.relative_to(PROT)).replace('\\', '/')
    for mm in re.finditer(r'renderListPage\(\{', s):
        blk = s[mm.start():mm.start()+2500]
        ent = re.search(r"entity:\s*'(\w+)'", blk)
        if not ent: continue
        e = ent.group(1)
        entity_pages[e].append((rel, title))
        for fm in re.finditer(r"label:\s*'([^']+)',\s*field:\s*'([^']+)'", blk):
            entity_filters[e].setdefault(fm.group(2), fm.group(1))
    # 非列表消费（弹窗/字典/待办/履历）
    for e in ('rentTracks', 'assetTracks', 'todoItems', 'dictItems'):
        if re.search(r'DEMO_DATA\.' + e + r'\b', s):
            if (rel, title) not in entity_pages[e]: entity_pages[e].append((rel, title))

# ---------- 2. 键语义直译兜底（D2：无 cfg/反查标签时用，标 待核） ----------
DICT = {'status':'状态','date':'日期','project':'所属项目','customer':'客户','name':'名称',
'ref':'关联单据','summary':'摘要','supplier':'供应商','type':'类型','period':'账期',
'appliance':'器具','warehouse':'仓库','time':'时间','operator':'操作人','area':'库区',
'material':'物料','scope':'数据权限','btype':'账单类型','bank':'银行','start':'开始日期',
'agent':'经办人','maker':'制单人','cls':'分类','src':'归属权','spec':'规格','inbound':'入库单号',
'docs':'单据','gen':'生成方式','receipt':'回单','no':'编号','buyer':'采购员','billing':'计费方式',
'addr':'地址','dest':'目标','result':'结果','mtype':'物料类型','mode':'方式','po':'采购订单号',
'bizType':'业务类型','inTime':'入库时间','caliber':'口径','checker':'审核人','frm':'调出方',
'to':'调入方','back':'退回','contact':'联系人','wh':'库房','ltype':'库位类型','usage':'用途',
'desc':'描述','accts':'关联账号','user':'用户','module':'模块','opType':'操作类型','role':'角色',
'side':'方向','category':'字典大类','abbr':'简码','auditor':'审核人','docNo':'单据编号',
'submitter':'提交人','action':'操作','suppliers':'绑定供应商','end':'结束日期','owner':'权属',
'qty':'数量','code':'编码','ver':'版本','mix':'混拆','updater':'更新人','update':'更新时间',
'billNo':'账单编号','billType':'账单类型','amount':'金额','paid':'已付金额','genMode':'生成方式',
'scenario':'演示场景','titleNo':'单据编号','feeType':'费用类型','verified':'已核销','genDate':'生成日期',
'title':'标题','feeSecTitle':'费用区标题','link':'链接','so':'销售订单号','sd':'销售单号',
'who':'负责人','zl':'租赁单号','itype':'类型','rtype':'类型','ltype2':'类型','search':'查询范围'}

# ---------- 3. 逐实体逐键分析 ----------
DATE_RE = re.compile(r'^\d{4}-\d{2}(-\d{2})?$')
def celltext(c):
    return htmllib.unescape(re.sub(r'<[^>]+>', '', str(c))).strip()

analysis = {}  # ent -> [ {key, label, src, type, vals} ]
for ent, v in sorted(D.items()):
    if ent.startswith('_') or not isinstance(v, dict): continue
    # 收键：row.fields 优先，再记录级标量
    keys, pool, recs = [], {}, []
    for rk, rec in v.items():
        if not isinstance(rec, dict): continue
        recs.append((rk, rec))
    seen = set()
    for rk, rec in recs:
        for k in (rec.get('row', {}).get('fields') or {}):
            if k not in seen: keys.append(k); seen.add(k)
    for rk, rec in recs:
        for k in rec:
            if k in ('row',) or not isinstance(rec[k], (str, int, float)): continue
            if k not in seen: keys.append(k); seen.add(k)
    # info/cells 值反查表（值 → label 计数）
    val_label = collections.defaultdict(collections.Counter)
    for rk, rec in recs:
        info = rec.get('info')
        if isinstance(info, list):
            for it in info:
                if isinstance(it, dict) and it.get('label'):
                    val_label[str(it.get('text', '')).strip()][it['label']] += 1
        cells = rec.get('row', {}).get('cells')
        if isinstance(cells, list) and cells:
            pass  # th 对齐在本页静态头，脚本外不做（位置对齐脆弱，宁缺毋滥 D8 精神）
    rows = []
    allk = ['_key'] + keys
    for k in allk:
        vals = []
        for rk, rec in recs:
            fv = (rec.get('row', {}).get('fields') or {}).get(k)
            if fv is None and k != '_key': fv = rec.get(k) if isinstance(rec.get(k), (str, int, float)) else None
            if k == '_key': fv = rk
            if fv is not None: vals.append(str(fv).strip())
        if not vals: continue
        # 标签三级
        if k == '_key':
            kl = entity_filters.get(ent, {}).get('_key')
            label, src = (kl, 'cfg') if kl else ('记录键（单号/编码）', '键语义')
        elif k in entity_filters.get(ent, {}):
            label, src = entity_filters[ent][k], 'cfg'
        else:
            c = None
            for val in set(vals):
                if val in val_label and val_label[val]:
                    top = val_label[val].most_common(1)[0]
                    if c is None or top[0] == c: c = top[0]
            if c and len(c) <= 12:
                label, src = c, '值反查'
            else:
                label, src = DICT.get(k, k) + '〔待核〕', '直译待核'
        # 类型
        uniq = list(dict.fromkeys(vals))
        if all(DATE_RE.match(x) for x in uniq): typ = '日期'
        elif all(re.match(r'^-?[\d,\.]+(元|套|只|个)?$', x) for x in uniq): typ = '数值'
        elif len(uniq) <= 8: typ = '枚举'
        else: typ = '文本'
        # 取值域
        if typ == '枚举': dom = ' / '.join(uniq)
        elif typ == '数值':
            nums = [float(re.sub(r'[^\d\.\-]', '', x) or 0) for x in uniq]
            dom = f'{min(nums):g} ~ {max(nums):g}'
        elif typ == '日期': dom = uniq[0] + ' 等'
        else: dom = ' / '.join(uniq[:5]) + (' …' if len(uniq) > 5 else '')
        if len(dom) > 90: dom = dom[:87] + '…'
        rows.append({'key': k, 'label': label, 'src': src, 'type': typ, 'dom': dom, 'n': len(vals)})
    analysis[ent] = rows

# ---------- 4. 实体中文名与模块分域 ----------
ENT_CN = {'payableBills':'应付账单','receivableBills':'应收账单','payments':'付款登记','receipts':'回款登记',
'invoices':'开票登记','writeoffs':'银行水单核销','leaseOrders':'租赁单','rentInOrders':'租入单',
'comboOutbounds':'租赁出库(组合出库)','returnInbounds':'退租入库','rentInReturns':'租入归还',
'rentInbounds':'租入入库','purchaseOrders':'采购订单','salesOrders':'销售订单','purchaseInbounds':'采购入库',
'salesOutbounds':'销售出库','otherInbounds':'其他入库','otherOutbounds':'其他出库','stocktakes':'盘点记录',
'transfers':'库存调拨','stockFlows':'库存查询','rentTracks':'出租履历','assetTracks':'资产轨迹',
'partners':'客商','products':'物料档案','locations':'库位档案','bomVersions':'BOM 维护','bomList':'BOM 列表',
'roles':'角色','opLogs':'操作日志','users':'用户','dictItems':'数据字典项','todoItems':'我的待办',
'projects':'项目档案','projectDocs':'项目详情','boardRows':'项目看板','profitRows':'项目损益'}
MODULES = [
 ('基础资料', ['products','partners','locations','bomVersions','bomList','dictItems']),
 ('项目管理', ['projects','projectDocs','boardRows']),
 ('采购管理', ['purchaseOrders','purchaseInbounds']),
 ('销售管理', ['salesOrders','salesOutbounds']),
 ('租赁管理（租出）', ['leaseOrders','comboOutbounds','returnInbounds','rentTracks']),
 ('租赁管理（租入）', ['rentInOrders','rentInbounds','rentInReturns']),
 ('仓储作业', ['otherInbounds','otherOutbounds','stocktakes','transfers','stockFlows','assetTracks']),
 ('财务协同', ['payableBills','receivableBills','payments','receipts','invoices','writeoffs','profitRows']),
 ('系统管理', ['roles','users','opLogs','todoItems']),
]

# ---------- 5. B 类白名单静态页表头兜底 ----------
wl = (ROOT / 'agent-handoff/g12-whitelist.md').read_text(encoding='utf-8')
wl_files = re.findall(r'`([^`]+\.html)`', wl)
wl_th = []
for rel in wl_files:
    f = PROT / rel
    if not f.exists(): continue
    ths = re.findall(r'<th[^>]*>(.*?)</th>', f.read_text(encoding='utf-8'), re.S)
    ths = [celltext(t) for t in ths]
    ths = [t for t in ths if t and t not in ('复选框','操作')]
    if ths: wl_th.append((rel.replace('\\','/'), ths))

# ---------- 6. 生成 A05 ----------
n_fields = sum(len(r) for r in analysis.values())
n_pages = len({p for lst in entity_pages.values() for p, _ in lst})
L = []
L.append('# P3-R01-A05 · 字段字典（实体字段总表）')
L.append('')
L.append('> **版本**：V1.0（2026-09-11 · G16 生成）  ')
L.append(f'> **统计**：实体 {len(analysis)} ｜ 字段行 {n_fields} ｜ 覆盖页面 {n_pages}（A 类 33 列表页 + 履历/字典/待办消费页）  ')
L.append('> **来源**：`_data/demo-data.js`（37 实体 dump：`_scan_tmpdir/g16_t1_dump.js` → `g16_data_dump.json`）+ 各页 `renderListPage` cfg + B 类白名单静态表头。提取脚本：`_scan_tmpdir/g16_t1_extract.py`（重跑=重新生成全文）。')
L.append('')
L.append('## 维护规则')
L.append('')
L.append('1. **新增字段先登记本表**（实体章节补一行），再改 demo-data / 页面 cfg——字段字典是真值源，页面是投影。')
L.append('2. 中文标签三级来源：`cfg filter label`（列表页筛选/列定义）＞ `info/cells 值反查`（详情弹窗标签）＞ 键语义直译（标〔待核〕，G17 命名统一后回改）。')
L.append('3. 取值域口径：去重值 ≤8 判枚举全列；数值列给 min~max；文本列列前 5 个演示值。')
L.append('4. 与 `P3-R01-A06-实体关系与状态机.md`（实体分域/关系/状态机）互为姊妹篇；与页面层 `系统管理/数据字典.html` 演示页的关系：**真值源=本表**，演示页只展示 dictItems 实体（字典项）子集。')
L.append('5. 记录键 `_key`：demo-data 建模约定「单号即外键」——实体间用单号互引不复制数据，跨页互溯链因此一致。')
L.append('')
for mod, ents in MODULES:
    L.append(f'## {mod}')
    L.append('')
    for e in ents:
        if e not in analysis: continue
        pages = entity_pages.get(e, [])
        ptxt = '、'.join(f'{t}（{p}）' for p, t in pages[:3]) or '（弹窗/脚本消费，无列表页）'
        nrec = len(D[e])
        L.append(f'### {e} · {ENT_CN.get(e, e)}')
        L.append('')
        L.append(f'记录数 {nrec} ｜ 消费页面：{ptxt}')
        L.append('')
        L.append('| 字段键 | 中文标签 | 类型 | 取值域 / 演示值 | 覆盖行数 |')
        L.append('|---|---|---|---|---|')
        for r in analysis[e]:
            L.append(f"| `{r['key']}` | {r['label']}{' ¹' if r['src']=='cfg' else (' ²' if r['src']=='值反查' else '')} | {r['type']} | {r['dom']} | {r['n']}/{nrec} |")
        L.append('')
L.append('> 标签角标：¹=cfg 列表定义 ｜ ²=详情弹窗值反查 ｜ 无角标=直译〔待核〕')
L.append('')
L.append('## B 类白名单静态页表头（数据驱动豁免，字段以页面静态为准）')
L.append('')
L.append(f'> 来源：`agent-handoff/g12-whitelist.md`（B 类 46 文件，G12 登记）。有表格的页面摘录表头；纯表单弹窗无表头不列。共 {len(wl_th)} 页含表头。')
L.append('')
for rel, ths in wl_th:
    L.append(f'- **{rel}**：{"、".join(ths)}')
L.append('')
L.append('## 已知数据缺口（2026-09-11 多对多全量评估结论，G16 登记）')
L.append('')
L.append('1. **采购订单实体无 `project` 字段**——但采购订单列表页有「所属项目」筛选与 M:N 选项目联动（新建弹窗），数据层缺投影字段。')
L.append('2. **stockFlows 无供应商维度**——租入在库（状态=租入）无法按供应商查库存；路凯/吉客云对账场景需补 `supplier` 字段。')
L.append('3. **partners.supplier 字段为公司名字符串**而非客商编码（DW-xxx）——多对多绑定与单据互溯在演示层用名字匹配，正式版须改编码外键。')
L.append('')
out = PROT / 'P3-R01-A05-字段字典.md'
out.write_text('\n'.join(L), encoding='utf-8')
# 概览
print('entities:', len(analysis), 'field_rows:', n_fields, 'pages:', n_pages, 'wl_th_pages:', len(wl_th))
print('cfg-labeled:', sum(1 for r in analysis.values() for x in r if x['src']=='cfg'),
      'valrev:', sum(1 for r in analysis.values() for x in r if x['src']=='值反查'),
      'guess:', sum(1 for r in analysis.values() for x in r if x['src']=='直译待核'))
