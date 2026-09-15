# -*- coding: utf-8 -*-
"""G35 T1 勘察（只读）：33 个标准列表页逐页提取
- 现有筛选项（.filter-card 内 .ff-label，标注是否 select/input/range）
- 表格列（thead th 文本）
- renderListPage cfg（entity + filters labels）
- 状态页签（stabs）
输出：_scan_tmpdir/g35_t1_raw.json（供 T2 分级用）
"""
import io, os, re, json

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
OUT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g35_t1_raw.json'

PAGES = [
    ('仓储作业', '其他入库列表'), ('仓储作业', '其他出库列表'), ('仓储作业', '库存查询'),
    ('仓储作业', '库存调拨列表'), ('仓储作业', '盘点列表'),
    ('基础数据', 'BOM'), ('基础数据', '产品档案'), ('基础数据', '客商管理'), ('基础数据', '库位档案'),
    ('租入管理', '租入入库列表'), ('租入管理', '租入单列表'), ('租入管理', '租入归还列表'),
    ('租赁管理', '租赁出库列表'), ('租赁管理', '租赁单列表'), ('租赁管理', '退租入库列表'),
    ('系统管理', '操作日志'), ('系统管理', '用户权限'), ('系统管理', '角色管理'),
    ('财务协同', '付款登记'), ('财务协同', '回款登记'), ('财务协同', '应付账单'), ('财务协同', '应收账单'),
    ('财务协同', '开票登记'), ('财务协同', '盈亏报表'), ('财务协同', '退款登记'),
    ('采购管理', '采购入库列表'), ('采购管理', '采购订单列表'), ('采购管理', '采购退货单列表'),
    ('销售管理', '销售出库列表'), ('销售管理', '销售订单列表'), ('销售管理', '销售退货单列表'),
    ('项目管理', '项目档案'),
    ('.', '我的待办'),
]

def get_filter_card(txt):
    """提取 body 中 filter-card 到其闭合（以 filter-actions 后的 </div></div> 为界）"""
    i = txt.find('<div class="filter-card')
    if i < 0:
        return None
    # 从 i 起做 div 配平
    depth = 0
    j = i
    for m in re.finditer(r'<div\b|</div>', txt[i:]):
        if m.group(0).startswith('<div'):
            depth += 1
        else:
            depth -= 1
        if depth == 0:
            j = i + m.end()
            break
    return txt[i:j]

def parse_filters(card):
    """解析 .ff 项：label / 控件类型 / 静态 options"""
    out = []
    if not card:
        return out
    for m in re.finditer(r'<div class="ff[^"]*"[^>]*>(.*?)</div>', card, re.S):
        seg = m.group(1)
        lm = re.search(r'<span class="ff-label"[^>]*>(.*?)</span>', seg, re.S)
        if not lm:
            continue
        label = re.sub(r'[:：]\s*$', '', lm.group(1).strip())
        is_extra = 'ff-row-extra' in m.group(0)
        ctype = None
        opts = []
        if '<select' in seg:
            ctype = 'select'
            opts = [re.sub(r'<[^>]+>', '', o).strip() for o in re.findall(r'<option[^>]*>(.*?)</option>', seg, re.S)]
        elif seg.count('<input') >= 2:
            ctype = 'range'
        elif '<input' in seg:
            ctype = 'input'
        out.append({'label': label, 'type': ctype, 'extra': is_extra, 'options': opts})
    return out

def get_ths(txt):
    """主表 thead th 列（取第一个含 3 列以上的 thead；排除筛选区内无表格情形）"""
    best = []
    for m in re.finditer(r'<thead>(.*?)</thead>', txt, re.S):
        ths = [re.sub(r'<[^>]+>', '', t).strip() for t in re.findall(r'<th[^>]*>(.*?)</th>', m.group(1), re.S)]
        ths = [t for t in ths if t]
        if len(ths) > len(best):
            best = ths
    return best

def get_cfg(txt):
    """renderListPage 调用的 entity 与 filters"""
    m = re.search(r'renderListPage\(\{[\s\S]*?\}\);', txt)
    if not m:
        return None
    seg = m.group(0)
    em = re.search(r"entity:\s*'([^']+)'", seg)
    labels = re.findall(r"label:\s*'([^']+)'", seg)
    return {'entity': em.group(1) if em else None, 'cfgFilters': labels, 'raw_len': len(seg)}

def get_stabs(txt):
    i = txt.find('class="stabs"')
    if i < 0:
        return []
    j = txt.find('</div>', i)
    seg = txt[i:j]
    return [re.sub(r'<[^>]+>', '', s).strip() for s in re.findall(r'<span class="stab[^"]*"[^>]*>(.*?)</span>', seg, re.S)]

def main():
    result = {}
    for d, n in PAGES:
        p = os.path.join(ROOT, d, n + '.html') if d != '.' else os.path.join(ROOT, n + '.html')
        txt = io.open(p, encoding='utf-8').read()
        card = get_filter_card(txt)
        entry = {
            'path': os.path.relpath(p, ROOT),
            'filters': parse_filters(card),
            'has_filter_card': card is not None,
            'ths': get_ths(txt),
            'cfg': get_cfg(txt),
            'stabs': get_stabs(txt),
        }
        result[n] = entry
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(json.dumps(result, ensure_ascii=False, indent=1))
    # 摘要打印
    print('pages surveyed:', len(result))
    for n, e in result.items():
        fl = ', '.join('%s(%s%s)' % (f['label'], f['type'], '·extra' if f['extra'] else '') for f in e['filters'])
        ent = e['cfg']['entity'] if e['cfg'] else 'STATIC'
        cfgf = '|'.join(e['cfg']['cfgFilters']) if e['cfg'] else '-'
        print('%-10s %-8s th=%2d  筛%d项[%s]  cfg[%s]' % (n, ent, len(e['ths']), len(e['filters']), fl, cfgf))

if __name__ == '__main__':
    main()
