# -*- coding: utf-8 -*-
"""任务二·列表数据驱动全量推广主脚本（2026-09-08）· 批次1 仓储作业 12 页
步骤：备份 → 提取 tbody 行（禁凭印象）→ 生成 row → 注入 demo-data.js → 页面 renderListPage 接线
用法：python listfull_apply.py batch1 [--dry]
"""
import sys, io, re, json, shutil, argparse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
DD = PROTO / '_data' / 'demo-data.js'

# ---------------- 批次配置 ----------------
BATCH1 = [
    dict(page='仓储作业/其他入库列表.html', entity='otherInbounds', modalId='detailModal',
         fields=dict(type='入库类型', material='物料名称', warehouse='入库仓库', date='入库日期', status='状态'),
         filters=[('单号', '_key'), ('入库类型', 'type'), ('物料名称', 'material'), ('状态', 'status'),
                  ('入库日期', 'date', 'r'), ('入库仓库', 'warehouse')], stabs=True),
    dict(page='仓储作业/租入入库列表.html', entity='rentInbounds', modalId='detailModal',
         fields=dict(ref='关联租入单', operator='运营方', appliance='器具', area='入库库区', status='状态', maker='制单人', date='入库时间'),
         filters=[('入库单号', '_key'), ('关联租入单', 'ref'), ('运营方', 'operator'), ('器具', 'appliance'),
                  ('状态', 'status'), ('入库时间', 'date', 'r')], stabs=True),
    dict(page='仓储作业/销售出库列表.html', entity='salesOutbounds', modalId='detailModal',
         fields=dict(so='关联销售订单号', customer='客户名称', project='所属项目', summary='出库明细摘要', warehouse='出库仓库', date='出库日期', status='状态'),
         filters=[('出库单号', '_key'), ('关联销售订单号', 'so'), ('客户名称', 'customer'), ('状态', 'status'),
                  ('出库日期', 'date', 'r'), ('所属项目', 'project')], stabs=True),
    dict(page='仓储作业/组合出库列表.html', entity='comboOutbounds', modalId='detailModal',
         fields=dict(project='所属项目', customer='客户', zl='关联租赁单号', combo='出库组合件 × 数量', so='关联销售订单', addr='收货地点', status='状态', date='出库时间'),
         filters=[('出库单号', '_key'), ('所属项目', 'project'), ('客户', 'customer'), ('出库状态', 'status'),
                  ('出库时间', 'date', 'r'), ('组合件编码', 'combo')], stabs=True),
    dict(page='仓储作业/其他出库列表.html', entity='otherOutbounds', modalId='detailModal',
         fields=dict(type='出库类型', material='物料名称', warehouse='出库仓库', date='出库日期', status='状态'),
         filters=[('单号', '_key'), ('出库类型', 'type'), ('物料名称', 'material'), ('状态', 'status'),
                  ('出库日期', 'date', 'r'), ('出库仓库', 'warehouse')], stabs=True),
    dict(page='仓储作业/租入归还列表.html', entity='rentInReturns', modalId='detailModal',
         fields=dict(ref='关联租入单', operator='运营方', rtype='归还类型', appliance='器具', status='状态', maker='制单人', date='归还时间'),
         filters=[('归还单号', '_key'), ('关联租入单', 'ref'), ('运营方', 'operator'), ('归还类型', 'rtype'),
                  ('状态', 'status'), ('归还时间', 'date', 'r')], stabs=True),
    dict(page='仓储作业/退租入库列表.html', entity='returnInbounds', modalId='detailModal',
         fields=dict(apply='关联退租申请单号', customer='客户名称', project='所属项目', appliance='退租器具名称', dest='拆散去向', warehouse='入库仓库', date='入库日期', result='验收结果', status='状态'),
         filters=[('退租入库单号', '_key'), ('关联退租申请单号', 'apply'), ('客户名称', 'customer'),
                  ('验收结果', 'result'), ('入库日期', 'date', 'r'), ('所属项目', 'project')], stabs=True),
    dict(page='仓储作业/组装列表.html', entity='assemblyOrders', modalId='detailModal',
         fields=dict(project='所属项目', parent='父项（组合件）', src='配方来源', prog='组装进度（已组装/计划）', operator='运营方', worker='组装人', date='开始时间', status='状态'),
         filters=[('组装单号', '_key'), ('所属项目', 'project'), ('父项（组合件）', 'parent'),
                  ('组装状态', 'status'), ('组装时间', 'date', 'r'), ('运营方', 'operator')], stabs=True),
    dict(page='仓储作业/拆卸管理列表.html', entity='disassemblyOrders', modalId='detailModal',
         fields=dict(unit='组合单元编码', uname='组合单元名称', warehouse='拆卸仓库', date='拆卸日期', status='状态'),
         filters=[('拆卸单号', '_key'), ('组合单元编码', 'unit'), ('拆卸仓库', 'warehouse'),
                  ('状态', 'status'), ('拆卸日期', 'date', 'r')], stabs=True),
    dict(page='仓储作业/盘点列表.html', entity='stocktakes', modalId='detailModal',
         fields=dict(scope='盘点范围', caliber='盘点口径', status='状态', checker='盘点人', date='盘点日期'),
         filters=[('盘点单号', '_key'), ('盘点范围', 'scope'), ('盘点口径', 'caliber'), ('盘点状态', 'status'),
                  ('盘点日期', 'date', 'r'), ('盘点人', 'checker')], stabs=True),
    dict(page='仓储作业/库存调拨列表.html', entity='transfers', modalId='detailModal',
         fields=dict(material='物料名称', frm='调出仓库', to='调入仓库', date='调拨日期', status='状态'),
         filters=[('调拨单号', '_key'), ('物料名称', 'material'), ('调出仓库', 'frm'), ('调入仓库', 'to'),
                  ('调拨日期', 'date', 'r'), ('状态', 'status')], stabs=True),
    dict(page='仓储作业/库存查询.html', entity='stockFlows', modalId='flowModal', noCheckbox=True, tbodyIndex=0,
         fields=dict(name='名称', cls='物料类别', project='适用项目', area='库区'),
         filters=[], stabs=False),
]
BATCHES = dict(batch1=BATCH1)

# 批次2 · 财务+买卖 9 页（2026-09-08）
BATCHES['batch2'] = [
    dict(page='财务协同/应付账单.html', entity='payableBills', modalId='detailModal', wire='custom',
         detail_fn='openPayableBillDetail',
         fields=dict(supplier='供应商名称', btype='账单类型', project='所属项目', period='账期', ref='关联订单/租入单号', inbound='关联采购入库单号', date='账单日期', status='状态'),
         filters=[('应付账单号', '_key'), ('供应商名称', 'supplier'), ('关联采购订单号', 'ref'), ('状态', 'status'), ('账单日期', 'date', 'r')], stabs=True),
    dict(page='财务协同/应收账单.html', entity='receivableBills', modalId='detailModal', wire='custom',
         detail_fn='openReceivableBillDetail',
         fields=dict(period='账期', project='所属项目', customer='客户', btype='账单类型', docs='包含单据', gen='生成方式', date='生成时间', status='状态'),
         filters=[('账单编号', '_key'), ('客户', 'customer'), ('所属项目', 'project'), ('账单状态', 'status'), ('账期', 'period'), ('生成日期', 'date', 'r')], stabs=True),
    dict(page='财务协同/付款登记.html', entity='payments', modalId='detailModal',
         fields=dict(supplier='供应商名称', ref='关联应付账单号', bank='付款银行', date='付款日期', status='状态'),
         filters=[('付款编号', '_key'), ('供应商名称', 'supplier'), ('关联应付账单号', 'ref'), ('状态', 'status'), ('付款日期', 'date', 'r')], stabs=True),
    dict(page='财务协同/回款登记.html', entity='receipts', modalId='detailModal',
         fields=dict(customer='客户', ref='关联账单', bank='银行账户', receipt='银行回单', date='收款日期', status='核销状态'),
         filters=[('收款编号', '_key'), ('客户', 'customer'), ('收款日期', 'date', 'r'), ('核销状态', 'status'), ('银行账户', 'bank')], stabs=True),
    dict(page='财务协同/开票登记.html', entity='invoices', modalId='detailModal',
         fields=dict(no='发票号码', itype='类型', buyer='购方名称', ref='关联应收账单', date='开票日期', status='状态'),
         filters=[('发票登记号', '_key'), ('发票号码', 'no'), ('购方名称', 'buyer'), ('发票类型', 'itype'), ('开票日期', 'date', 'r'), ('开票状态', 'status')], stabs=True),
    dict(page='财务协同/银行水单核销.html', entity='writeoffs', modalId='detailModal',
         noCheckbox=True, table_id='hxTable', table_index=3,
         fields=dict(sd='银行回单', ref='冲抵单据', status='核销状态', time='核销时间', who='核销人'),
         filters=[], stabs=False),
    dict(page='采购管理/采购订单列表.html', entity='purchaseOrders', modalId='detailModal', tbodyIndex=0,
         fields=dict(supplier='供应商名称', mtype='物料类型', summary='采购明细摘要', date='预计到货日期', so='关联销售订单号', status='订单状态'),
         filters=[('采购订单号', '_key'), ('供应商', 'supplier'), ('物料类型', 'mtype'), ('订单状态', 'status'), ('下单日期', 'date', 'r')], stabs=True),
    dict(page='采购管理/租入单列表.html', entity='rentInOrders', modalId='detailModal',
         fields=dict(operator='运营方', appliance='器具', period='租期起止', status='状态', agent='经办人', date='租期起止'),
         filters=[('租入单号', '_key'), ('运营方', 'operator'), ('器具', 'appliance'), ('状态', 'status'), ('租期开始', 'date', 'r'), ('经办人', 'agent')], stabs=True),
    dict(page='销售管理/销售订单列表.html', entity='salesOrders', modalId='detailModal', tbodyIndex=0,
         fields=dict(customer='客户名称', project='所属项目', summary='订单明细摘要', mode='是否代下单', status='订单状态', agent='下单人', date='下单时间', po='关联采购订单号'),
         filters=[('销售订单号', '_key'), ('客户名称', 'customer'), ('所属项目', 'project'), ('订单状态', 'status'), ('下单日期', 'date', 'r'), ('下单方式', 'mode')], stabs=True),
]

# ---------------- 工具 ----------------
def strip_tags(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h)).strip()

def load_entities():
    src = DD.read_text(encoding='utf-8')
    ent_re = re.compile(r'^  ([A-Za-z_][A-Za-z0-9_]*): \{$', re.M)
    key_re = re.compile(r"^    '([^']+)': \{$", re.M)
    spans = [(m.group(1), m.start()) for m in ent_re.finditer(src)]
    out = {}
    for i, (n, p) in enumerate(spans):
        e = spans[i + 1][1] if i + 1 < len(spans) else len(src)
        out[n] = key_re.findall(src[p:e])
    return out, src

def extract_rows(cfg, ent_keys):
    """从页面 tbody 提取每行：键匹配（照 wireDetailModal：键插入序 indexOf）、cells、ops、note、fields"""
    txt = (PROTO / cfg['page']).read_text(encoding='utf-8')
    if cfg.get('table_index'):
        tables = re.findall(r'<table[^>]*>.*?</table>', txt, re.S)
        tbl = tables[cfg['table_index'] - 1]
    else:
        tbl = txt
    tbodys = re.findall(r'<tbody[^>]*>(.*?)</tbody>', tbl, re.S)
    tb = tbodys[cfg.get('tbodyIndex', 0)]
    rows = re.findall(r'<tr>(.*?)</tr>', tb, re.S)
    keys = ent_keys[cfg['entity']]
    thead_cols = re.findall(r'<th[^>]*>([^<]*)</th>', re.findall(r'<thead>(.*?)</thead>', tbl, re.S)[0])
    col_idx = {}
    for f, cname in cfg['fields'].items():
        col_idx[f] = thead_cols.index(cname)  # 断言列名存在
    rows_out, notes_out = [], []
    for row in rows:
        tds = re.findall(r'<td[^>]*>.*?</td>', row, re.S)
        rt = strip_tags(row)
        key = next((k for k in keys if k in rt), None)
        if not key:
            rows_out.append(None); continue
        no_cb = cfg.get('noCheckbox')
        # 列切分：[cb?][键列][cells...][ops]
        key_td_i = 1 if not no_cb else 0
        ops_td = tds[-1]
        cells = tds[key_td_i + 1:-1]
        # note：键列 td 的 data-note
        note = None
        m = re.search(r'data-note="(\d+)"', tds[key_td_i])
        if m: note = m.group(1)
        # ops 解析
        ops = []
        for am in re.finditer(r'<a([^>]*)>([^<]*)</a>', ops_td):
            attrs, t = am.group(1), am.group(2).strip()
            oc = re.search(r'onclick="([^"]*)"', attrs)
            act = oc.group(1) if oc else None
            if act and cfg['modalId'] in act:
                ops.append({'t': t, 'detail': True})
            elif act:
                ops.append({'t': t, 'act': act})
            else:
                ops.append({'t': t})
        # fields：按列索引取纯文本
        plain = [strip_tags(c) for c in tds]
        fields = {}
        for f, ci in col_idx.items():
            v = plain[ci] if ci < len(plain) else ''
            fields[f] = re.sub(r'\s*\(.*?$', '', v).strip() if f != 'date' else v[:10]
        rows_out.append(dict(key=key, cells=cells, ops=ops, note=note, fields=fields))
    return rows_out, thead_cols

# ---------------- 主流程 ----------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('batch'); ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    cfgs = BATCHES[a.batch]
    bak = ROOT / '_scan_tmpdir' / f'backup-listfull-{a.batch}-20260908'
    ent_keys, _ = load_entities()
    # 重新解析 demo-data.js 原文（二进制保 LF）
    dd_bytes = DD.read_bytes().decode('utf-8')

    # 1 备份
    if not a.dry:
        for c in cfgs:
            src = PROTO / c['page']
            dst = bak / c['page']
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        for f in ['_data/demo-data.js', '_data/list-generic.js']:
            dst = bak / f; dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PROTO / f, dst)
        print(f'备份 {len(cfgs)} 页 + _data 2 文件 → {bak}')

    # 2 提取
    all_rows = {}
    for c in cfgs:
        rows, thead = extract_rows(c, ent_keys)
        none_rows = [i for i, r in enumerate(rows) if r is None]
        assert not none_rows, f"{c['page']} 有行未匹配实体键: 行{none_rows}"
        all_rows[c['entity']] = rows
        keys = [r['key'] for r in rows]
        assert len(set(keys)) == len(keys), f"{c['page']} 键重复"
        statuses = {}
        for r in rows:
            statuses[r['fields'].get('status', '(无)')] = statuses.get(r['fields'].get('status', '(无)'), 0) + 1
        print(f"✔ {c['page']} {len(rows)} 行 | 状态分布 {statuses} | note {[r['note'] for r in rows if r['note']]}")

    if a.dry:
        print('--dry 结束'); return

    # 3 注入 demo-data.js（每键行后插 'row' 行；已有 row 的键跳过）
    n_inj = 0
    for entity, rows in all_rows.items():
        for r in rows:
            anchor = f"    '{r['key']}': {{\n"
            i = dd_bytes.find(anchor)
            assert i > -1, f"未找到键锚 {entity}:{r['key']}"
            after = i + len(anchor)
            if dd_bytes[after:after + 12].startswith("      'row'"):
                continue  # 已有 row（试点）
            row_js = json.dumps(dict(fields=r['fields'], **({'note': r['note']} if r['note'] else {}),
                                     cells=r['cells'], ops=r['ops']), ensure_ascii=False)
            dd_bytes = dd_bytes[:after] + f"      'row': {row_js},\n" + dd_bytes[after:]
            n_inj += 1
    DD.write_bytes(dd_bytes.encode('utf-8'))
    print(f'注入 row {n_inj} 条')

    # 4 页面接线
    for c in cfgs:
        p = PROTO / c['page']
        raw = p.read_bytes()
        crlf = raw.count(b'\r\n') * 2 > raw.count(b'\n')
        nl = '\r\n' if crlf else '\n'
        txt = raw.decode('utf-8')
        # 4a includes：三个 _data 渲染器任一后加 list-generic.js（若无）
        if '../_data/list-generic.js' not in txt:
            m = re.search(r'<script src="\.\./_data/(?:detail-generic|payable-bill-detail|receivable-bill-detail)\.js"></script>\n?', txt)
            assert m, f"{c['page']} 无 _data 渲染器 include"
            txt = txt[:m.end()] + f'<script src="../_data/list-generic.js"></script>' + nl + txt[m.end():]
        # 4a2 表 id 注入（多表页面：水单核销表③）
        if c.get('table_id'):
            tid = c['table_id']
            if f'id="{tid}"' not in txt:
                idx = int(c.get('table_index', 3))  # 第 N 个 <table 开标签
                hits = list(re.finditer(r'<table\b[^>]*>', txt))
                assert len(hits) >= idx, f"{c['page']} 找不到第 {idx} 个 <table"
                tag = hits[idx - 1].group(0)
                assert 'id=' not in tag, f"{c['page']} 第 {idx} 个 table 已有 id: {tag}"
                txt = txt[:hits[idx - 1].start()] + tag[:-1] + f' id="{tid}">' + txt[hits[idx - 1].end():]
        # 4b 生成 renderListPage 配置体
        fl = ',\n'.join(
            '    { label: \'%s\', field: \'%s\'%s }' % (
                lab, f, ', range: true' if (kr[0] if kr else None) == 'r' else '')
            for lab, f, *kr in c['filters'])
        extra = ''
        if c.get('noCheckbox'): extra += ',\n  noCheckbox: true'
        if c.get('table_id'): extra += f",\n  tbodySel: '#{c['table_id']} tbody'"
        elif c.get('tbodyIndex'): extra += f",\n  tbodySel: 'tbody:nth-of-type({c.get('tbodyIndex') + 1})'"
        if c.get('detail_fn'): extra += f",\n  detailFn: function (entity, key) {{ {c['detail_fn']}(key); }}"
        if c['modalId'] != 'detailModal': extra += f",\n  modalId: '{c['modalId']}'"
        cfg_js = (f"renderListPage({{\n  entity: '{c['entity']}',\n"
                  + (f"  stabs: {'true' if c.get('stabs') else 'false'},\n" if c.get('stabs') is not None else '')
                  + (('  filters: [\n' + fl + '\n  ]') if c['filters'] else '  filters: []')
                  + extra + '\n});')
        # 4c 替换接线：custom=整块 demo-data 接线 script；默认=wireDetailModal 行
        if c.get('wire') == 'custom':
            pat = re.compile(r"<script>\s*/\* demo-data 接线：[^*]*?\*/.*?</script>", re.S)
            m = pat.search(txt)
            assert m, f"{c['page']} 无 custom 接线块"
            block = ('<script>' + nl + f"/* demo-data 列表驱动：tbody 数据集渲染 + 真筛选 + stab 统计（2026-09-08 全量推广批2） */" + nl
                     + cfg_js + nl + '</script>')
            txt = txt[:m.start()] + block + txt[m.end():]
        else:
            pat = re.compile(r"wireDetailModal\('[^']+'(?:,\s*\{[^}]*\})?\);")
            m = pat.search(txt)
            assert m, f"{c['page']} 无 wireDetailModal 调用"
            txt = txt[:m.start()] + cfg_js + txt[m.end():]
        p.write_bytes(txt.encode('utf-8'))
        print(f'接线 {c["page"]}')
    print('批次完成')

if __name__ == '__main__':
    main()
