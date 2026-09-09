# -*- coding: utf-8 -*-
"""批1 Stage7：demo-data.js 手术
1) 删 returnApplies/assemblyOrders/disassemblyOrders/damageOrders 四实体（含段前注释块）
2) returnInbounds 深清理：fields.apply / cells[0] TZSQ 格 / info 关联退租申请 / chain 退租申请节点 / ops 生成赔偿单+创建拆卸单 / timeline 改写
3) leaseOrders：ops 创建退租申请→退租入库（3）；chain 申请节点→退租入库节点（TZSQ→TZRK 映射，5）；timeline 改写（5）
4) rentTracks/assetTracks：ops 退租→退租入库列表；rentTracks chain 申请节点→直接入库；timeline 改写
5) 全局：被移除页 url 行剥离 / fees links（纯被移除页键）剥离
纯 LF 文件；每步 assert 计数；结束 node --check + 残留校验。
"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
DD = ROOT / "P3-R01-包装租赁管理后台原型" / "_data" / "demo-data.js"
src = DD.read_bytes().decode('utf-8')
LOG = []

TZ2TZRK = {
    'TZSQ-20260902-008': 'TZRK-20260902-010',
    'TZSQ-20260903-005': 'TZRK-20260903-009',
    'TZSQ-20260901-006': 'TZRK-20260902-008',
    'TZSQ-20260830-005': 'TZRK-20260901-007',
    'TZSQ-20260829-004': 'TZRK-20260831-006',
    'TZSQ-20260826-003': 'TZRK-20260828-005',
    'TZSQ-20260823-002': 'TZRK-20260825-004',
    'TZSQ-20260818-001': 'TZRK-20260820-003',
}

def seg_of(txt, name):
    m = re.search(r'^  ' + name + r': \{', txt, re.M)
    assert m, f'实体未找到 {name}'
    start = m.start()
    nxt = re.search(r'^  (?:[a-zA-Z_]+: \{|/\* -)', txt[m.end():], re.M)
    end = m.end() + nxt.start() if nxt else len(txt)
    return start, end

# ---------- 1. 删四实体（含段前注释块） ----------
for ent in ['returnApplies', 'assemblyOrders', 'disassemblyOrders', 'damageOrders']:
    s, e = seg_of(src, ent)
    # 向前吞注释块
    head = src[:s]
    cstart = head.rfind('\n  /* ---')
    assert cstart > -1, f'{ent} 段前无注释块'
    # 段尾吞到下一实体注释块/实体行前的空行
    tail = src[e:]
    src = src[:cstart] + tail
    LOG.append(f'[实体删] {ent}')

# 校验删除干净
for ent in ['returnApplies', 'assemblyOrders', 'disassemblyOrders', 'damageOrders']:
    assert not re.search(r'^  ' + ent + r': \{', src, re.M), f'{ent} 未删净'

def edit_seg(txt, name, fn):
    s, e = seg_of(txt, name)
    seg = txt[s:e]
    seg2, notes = fn(seg)
    assert seg2 != seg or notes == [], f'{name} 段无变化'
    return txt[:s] + seg2 + txt[e:], notes

# ---------- 2. returnInbounds 深清理 ----------
def clean_return_inbounds(seg):
    notes = []
    # fields.apply 删
    n = 0
    for tz in TZ2TZRK:
        pat = '"apply": "' + tz + '", '
        n += seg.count(pat)
        seg = seg.replace(pat, '')
    assert n == 8, f'fields.apply {n}'
    notes.append(f'fields.apply 删 {n}')
    # cells[0] TZSQ 格删
    n = 0
    for tz in TZ2TZRK:
        pat = '"cells": ["<span class=\\"lk\\">' + tz + '</span>", '
        n += seg.count(pat)
        seg = seg.replace(pat, '"cells": [')
    assert n == 8, f'cells TZSQ {n}'
    notes.append(f'cells TZSQ 格删 {n}')
    # info 关联退租申请 字段块删（多行）
    pat_info = re.compile(r"        \{\n          'label': '关联退租申请',\n          'text': 'TZSQ-[\d\-]+',\n          'url': '租赁管理/退租申请列表\.html',\n          'full': true\n        \},\n")
    n = len(pat_info.findall(seg))
    assert n == 8, f'info 关联退租申请 {n}'
    seg = pat_info.sub('', seg)
    notes.append(f'info 关联退租申请块删 {n}')
    # chain 退租申请 节点块删
    pat_chain = re.compile(r"        \{\n          'role': '退租申请',\n          'name': 'TZSQ-[\d\-]+',\n          'url': '租赁管理/退租申请列表\.html'\n        \},\n")
    n = len(pat_chain.findall(seg))
    assert n == 8, f'chain 退租申请 {n}'
    seg = pat_chain.sub('', seg)
    notes.append(f'chain 退租申请节点删 {n}')
    # ops 生成赔偿单 / 创建拆卸单 删（对象级删除+悬空逗号清理）
    for op in ['{"t": "生成赔偿单", "act": "go(\'../租赁管理/丢损赔偿单.html\')"}',
               '{"t": "创建拆卸单", "act": "go(\'../仓储作业/拆卸管理列表.html\')"}']:
        c = seg.count(op)
        seg = seg.replace(op, '@@DEL@@')
    seg = seg.replace(', @@DEL@@', '').replace('@@DEL@@, ', '').replace('@@DEL@@', '')
    assert '生成赔偿单' not in seg and '创建拆卸单' not in seg, 'ops 未删净'
    notes.append('ops 生成赔偿单+创建拆卸单 删净')
    # timeline 改写
    c = seg.count("'text': '退租申请审核通过 · 等待到货'")
    assert c == 1, f'tl 等待到货 {c}'
    seg = seg.replace("'text': '退租申请审核通过 · 等待到货'", "'text': '客户退回 · 直接入库登记（无申请单）'")
    c = seg.count("'text': '退租申请审核通过'")
    assert c == 6, f'tl 审核通过 {c}'
    seg = seg.replace("'text': '退租申请审核通过'", "'text': '客户退回 · 直接入库登记'")
    notes.append('timeline 改写 7')
    return seg, notes

src, notes = edit_seg(src, 'returnInbounds', clean_return_inbounds)
LOG += [f'returnInbounds: {x}' for x in notes]

# ---------- 3. leaseOrders ----------
def clean_lease(seg):
    notes = []
    old = '{"t": "创建退租申请", "act": "go(\'../租赁管理/退租申请列表.html\')"}'
    new = '{"t": "退租入库", "act": "go(\'../租赁管理/退租入库列表.html\')"}'
    c = seg.count(old); assert c == 3, f'ops 创建退租申请 {c}'
    seg = seg.replace(old, new); notes.append(f'ops 创建退租申请→退租入库 {c}')
    # chain 申请节点 → 退租入库节点
    for tz, tzrk in TZ2TZRK.items():
        pat = ("        {\n          'role': '退租申请',\n          'name': '" + tz +
               "',\n          'url': '租赁管理/退租申请列表.html'\n        },")
        if pat in seg:
            rep = ("        {\n          'role': '退租入库',\n          'name': '" + tzrk +
                   "',\n          'url': '租赁管理/退租入库列表.html'\n        },")
            seg = seg.replace(pat, rep); notes.append(f'chain {tz}→{tzrk}')
    # 带后缀的 2 个（· 退 20 套 / · 退 200 只）；尾逗号两种变体
    for tz, suffix in [('TZSQ-20260829-004', '退 20 套'), ('TZSQ-20260826-003', '退 200 只')]:
        hit = False
        for tail_old, tail_new in [('},', '},'), ('}', '}')]:
            pat = ("        {\n          'role': '退租申请',\n          'name': '" + tz + " · " + suffix +
                   "',\n          'url': '租赁管理/退租申请列表.html'\n        " + tail_old)
            if pat in seg:
                rep = ("        {\n          'role': '退租入库',\n          'name': '" + TZ2TZRK[tz] + " · " + suffix +
                       "',\n          'url': '租赁管理/退租入库列表.html'\n        " + tail_new)
                seg = seg.replace(pat, rep); notes.append(f'chain {tz}·{suffix}→{TZ2TZRK[tz]}')
                hit = True
                break
        assert hit, f'申请后缀节点未找到 {tz}'
    # timeline 改写
    n = 0
    for tz, tzrk in TZ2TZRK.items():
        for pat in [f'退租申请 · {tz}（', f'退租申请 · {tz}'] :
            pass
    pat_re = re.compile(r"'text': '退租申请 · (TZSQ-[\d\-]+)（([^']+）)'")
    seg, k = pat_re.subn(lambda m: "'text': '客户退租 · " + TZ2TZRK[m.group(1)] + "（直接入库·" + m.group(2), seg)
    pat_re2 = re.compile(r"'text': '退租申请 · (TZSQ-[\d\-]+)'")
    seg, k2 = pat_re2.subn(lambda m: "'text': '客户退租 · " + TZ2TZRK[m.group(1)] + "（直接入库）'", seg)
    assert k + k2 == 5, f'lease timeline {k}+{k2}'
    notes.append(f'timeline 改写 {k}+{k2}')
    return seg, notes

src, notes = edit_seg(src, 'leaseOrders', clean_lease)
LOG += [f'leaseOrders: {x}' for x in notes]

# ---------- 4. rentTracks / assetTracks ----------
def clean_tracks(seg):
    notes = []
    old = '{"t": "退租", "act": "go(\'../租赁管理/退租申请列表.html\')"}'
    new = '{"t": "退租", "act": "go(\'../租赁管理/退租入库列表.html\')"}'
    c = seg.count(old)
    seg = seg.replace(old, new)
    notes.append(f'ops 退租重指 {c}')
    return seg, notes

for ent in ['rentTracks', 'assetTracks']:
    src, notes = edit_seg(src, ent, clean_tracks)
    LOG += [f'{ent}: {x}' for x in notes]

def clean_renttracks2(seg):
    notes = []
    pat = ("        {\n          'role': '退租申请',\n          'name': 'TZSQ-20260904-009 · 退 200 / 留 294',\n"
           "          'url': '租赁管理/退租申请列表.html'\n        },")
    assert pat in seg, 'rentTracks 申请节点未找到'
    rep = ("        {\n          'role': '退租入库',\n          'name': '退 200 / 留 294 · 直接入库',\n"
           "          'url': '租赁管理/退租入库列表.html'\n        },")
    seg = seg.replace(pat, rep); notes.append('chain 申请节点→直接入库 1')
    old_tl = "'text': '部分退租申请 · TZSQ-20260904-009（退 200 套）'"
    assert old_tl in seg
    seg = seg.replace(old_tl, "'text': '部分退租 · 退 200 套（直接入库）'")
    notes.append('timeline 改写 1')
    return seg, notes

src, notes = edit_seg(src, 'rentTracks', clean_renttracks2)
LOG += [f'rentTracks: {x}' for x in notes]

# ---------- 5. 全局 url 行 / links 剥离 ----------
REMOVED = r'(?:租赁管理/退租申请列表|仓储作业/组装列表|仓储作业/组装录单|仓储作业/拆卸管理列表|租赁管理/丢损赔偿单)\.html'

pat_url = re.compile(r"\n\s*'url': '" + REMOVED + r"',?")
src, k1 = pat_url.subn('', src)
LOG.append(f'[全局] 被移除页 url 行剥 {k1}')

# links 多行块（仅含被移除页键）
pat_links_ml = re.compile(r",\n\s*'links': \{\n\s*\d+: '" + REMOVED + r"'\n\s*\}")
src, k2 = pat_links_ml.subn('', src)
# links 单行内联（JSON 风格）
pat_links_inline = re.compile(r", links: \{ \d+: '" + REMOVED + r"' \}")
src, k3 = pat_links_inline.subn('', src)
LOG.append(f'[全局] links 块剥 {k2}+内联 {k3}')

DD.write_bytes(src.encode('utf-8'))
print('== demo-data 手术 ==')
for l in LOG:
    print(' ✓', l)

# ---------- 校验 ----------
assert not re.search(REMOVED, src), '被移除页路径残留'
import subprocess
r = subprocess.run(['node', '--check', str(DD)], capture_output=True, text=True)
assert r.returncode == 0, f'node --check 失败: {r.stderr[:500]}'
print('PASS: 无被移除页路径残留 + node --check 语法通过')
