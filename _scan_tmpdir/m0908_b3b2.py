# -*- coding: utf-8 -*-
"""批3 Script B2：demo-data fees 修复（逐记录精细处理）
- purchaseInbounds：feeCols 已改、cells 未插 → 逐行在 金额 后插 税率/含税/含税金额（含尾随批次/库位格）
- leaseOrders：逐记录重构 fees（产品明细+合计）
- rentInOrders：剩余记录重构
- salesOrders：残留 po fields/cells 清理
"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
DD = ROOT / "P3-R01-包装租赁管理后台原型" / "_data" / "demo-data.js"
src = DD.read_bytes().decode('utf-8')
LOG = []

def seg_of(txt, name):
    m = re.search(r'^  ' + name + r': \{', txt, re.M)
    assert m, name
    nxt = re.search(r'^  (?:[a-zA-Z_]+: \{|/\* -)', txt[m.end():], re.M)
    return m.start(), (m.end() + nxt.start() if nxt else len(txt))

def edit(txt, name, fn):
    s, e = seg_of(txt, name)
    return txt[:s] + fn(txt[s:e]) + txt[e:]

def inc2(p):
    return round(float(p) * 1.13, 2)

def fmtn(n):
    return f'{n:,.2f}'

# ============================================================
# 1. purchaseInbounds：cells 在 单价/金额 后插（行内可能还有批次/库位尾格）
# ============================================================
def fix_pib(seg):
    # cells 里形态：..., '6.80', '3,264.00', 'B2026...', 'RA-A-01-01'  或以金额结尾
    pat = re.compile(r"'cells': \[([^\]]*?)'([\d.]+)', '([\d,.]+)'(, '[^']*'(?:, '[^']*')*)?\]")
    k = [0]
    def repl(m):
        head, price, amt, tail = m.group(1), m.group(2), m.group(3), m.group(4) or ''
        # 数量来自 head 中的 托数×件数 或直接数字格：取 head 最后一个纯数字格
        mq = re.findall(r"'([\d,]+)'(?:,|$)", head)
        qty = mq[-1] if mq else '1'
        qn = float(qty.replace(',', ''))
        # 数量可能是 '10 托 × 480' 文本——取金额/单价推数量
        if qn <= 1:
            try:
                qn = float(amt.replace(',', '')) / float(price)
            except Exception:
                qn = 1
        inc = inc2(price)
        k[0] += 1
        return "'cells': [" + head + f"'{price}', '13%', '{inc:.2f}', '{fmtn(qn * inc)}'" + tail + ']'
    seg2 = pat.sub(repl, seg)
    LOG.append(f'purchaseInbounds fees 修复 {k[0]} 行')
    return seg2

src = edit(src, 'purchaseInbounds', fix_pib)

# ============================================================
# 2. leaseOrders：逐记录重构 fees
# ============================================================
def fix_lease(seg):
    recs = re.split(r"(?=^    'ZL-[\d-]+': \{)", seg, flags=re.M)
    cnt = 0
    for i, r in enumerate(recs):
        if not r.startswith("    'ZL-"):
            continue
        # 器具名 = row.cells 第 3 格（index 2）
        mc = re.search(r'"cells": \["[^"]*", "[^"]*", "([^"]*)"', r)
        appl = mc.group(1) if mc else '围板箱 1200×1000×970'
        # 旧 fees 首行：套数 / 日租金
        mf = re.search(r"'fees': \[\s*\{\s*'cells': \['[^']*', '[^']*', '[^']*', '([\d,]+)', '([\d.]+)', '[\d,.]+'", r)
        if not mf:
            continue
        qty, price = mf.group(1), mf.group(2)
        qn = float(qty.replace(',', ''))
        inc = inc2(price)
        newfees = (f"'fees': [\n        {{\n          'cells': ['{appl}', '{qty}', '{price}', '13%', '{inc:.2f}', '{fmtn(qn * inc)}']\n        }},\n"
                   f"        {{\n          'cells': ['合计', '—', '—', '—', '—', '{fmtn(qn * inc)}']\n        }}\n      ]")
        r2 = re.sub(r"'fees': \[\s*\{.*?\}\s*\]", newfees, r, count=1, flags=re.S)
        if r2 != r:
            recs[i] = r2
            cnt += 1
    LOG.append(f'leaseOrders fees 重构 {cnt} 条')
    return ''.join(recs)

src = edit(src, 'leaseOrders', fix_lease)

# ============================================================
# 3. rentInOrders：剩余记录（多行/带 links）重构
# ============================================================
def fix_rzd(seg):
    cnt = [0]
    pat = re.compile(r"'fees': \[\s*(\{.*?\})\s*\]", re.S)
    def repl(m):
        block = m.group(1)
        mc = re.search(r"'cells': \['([^']*)'[^\]]*\]", block)
        if not mc:
            return m.group(0)
        desc = mc.group(1)
        first_pay = ''
        mp = re.search(r"'([\d,.]+)'(?:,|'\])", block[mc.end():])
        mfp = re.findall(r"'([\d,]+\.\d{2})'", block)
        first_pay = mfp[-1] if mfp else '36,000.00'
        mq = re.search(r'([\d.]+)\s*元\s*×\s*(\d+)\s*(只|套|块)', desc)
        if mq:
            price, qty, unit = mq.group(1), mq.group(2), mq.group(3)
        else:
            nums = re.findall(r'([\d.]+)', desc)
            price, qty, unit = (nums[0] if nums else '400.00'), '30', '只'
        mode = '按套' if '按套' in desc else '月租'
        inc = inc2(price)
        qn = float(qty)
        prod = 'WBX-1210L 围板箱 1200×1000×970（租入）'
        cnt[0] += 1
        return (f"'fees': [\n        {{\n          'cells': ['{prod}', '{qty} {unit}', '{mode}', '{price}', '13%', '{inc:.2f}', '{first_pay}']\n        }}\n      ]")
    # 已转换过的（含 '计费方式' 已在 feeCols，cells 7 格含 '13%'）跳过
    seg2 = re.sub(r"'fees': \[\s*\{\s*'cells': \['[^']*', '[^']*', '(?:月租|按套)'[^\]]*\}\s*\]", lambda m: m.group(0), seg)
    seg2 = pat.sub(repl, seg2)
    LOG.append(f'rentInOrders fees 重构 {cnt[0]} 条')
    return seg2

src = edit(src, 'rentInOrders', fix_rzd)

# ============================================================
# 4. salesOrders：残留 po fields（无尾逗号形态）清理
# ============================================================
def fix_so(seg):
    n1 = len(re.findall(r', "po": "PO-[\d-]+"', seg))
    seg = re.sub(r', "po": "PO-[\d-]+"', '', seg)
    n2 = len(re.findall(r', "—"\]', seg))
    LOG.append(f'salesOrders po fields 尾形态删 {n1}；末格 — 删 {n2}（若为关联列）')
    return seg

src = edit(src, 'salesOrders', fix_so)

DD.write_bytes(src.encode('utf-8'))
import subprocess
r = subprocess.run(['node', '--check', str(DD)], capture_output=True, text=True)
assert r.returncode == 0, 'node --check: ' + r.stderr[:400]

# 一致性校验：每实体 feeCols 列数 == 每 fees 行 cells 数
def check_cols(txt):
    problems = []
    for ent in ['purchaseOrders', 'salesOrders', 'purchaseInbounds', 'salesOutbounds', 'comboOutbounds', 'leaseOrders', 'rentInOrders']:
        s, e = seg_of(txt, ent)
        seg = txt[s:e]
        mcols = re.findall(r"'feeCols': \[([^\]]*)\]", seg)
        for mc in mcols:
            ncols = len(re.findall(r"'[^']*'", mc))
        # fees cells 数
        for m in re.finditer(r"'fees': \[(.*?)\n      \]", seg, re.S):
            for c in re.finditer(r"'cells': \[([^\]]*)\]", m.group(1)):
                ncells = len(re.findall(r"'[^']*'", c.group(1)))
                if ncells != ncols:
                    problems.append((ent, ncols, ncells, c.group(1)[:60]))
    return problems

probs = check_cols(src)
if probs:
    for p in probs[:12]:
        print('  ✗', p)
LOG.append(f'列数一致性: {"PASS" if not probs else f"{len(probs)} 处失配"}')

print('== 批3 Script B2 ==')
for l in LOG:
    print(' ✓', l)
assert not probs, f'{len(probs)} 处 feeCols/cells 失配'
