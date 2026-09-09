# -*- coding: utf-8 -*-
"""批3 Script B：demo-data 明细三件套化（详情弹窗同步展示）
- purchaseOrders/salesOrders/purchaseInbounds：单价/金额 → 未税/税率/含税/含税金额
- salesOutbounds/comboOutbounds：数量后插三件套（价格取产品参考单价）
- leaseOrders：fees 重构为产品明细（数量/未税/税率/含税/含税金额+合计行）
- rentInOrders：fees 重构为多货品明细（产品/数量/计费方式/未税/税率/含税/首期应付）
- salesOrders：去关联采购订单（fields.po + cells 末格）
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
    seg = txt[s:e]
    seg2 = fn(seg)
    return txt[:s] + seg2 + txt[e:]

def inc2(p):
    return round(float(p) * 1.13, 2)

def fmtn(n):
    return f'{n:,.2f}'

# ============================================================
# 1. PO / SO / 采购入库：单价/金额 → 三件套
# ============================================================
def trans_price_cols(seg):
    old_cols = "'单价(元)', '金额(元)'"
    new_cols = "'未税单价(元)', '税率', '含税单价(元)', '含税金额(元)'"
    n = seg.count(old_cols)
    seg = seg.replace(old_cols, new_cols)
    LOG.append(f'  feeCols 改写 {n} 处')
    pat = re.compile(r"'cells': \[([^\]]*?)'([\d,]+)', '([\d.]+)', '([\d,.]+)'\]")
    k = 0
    def repl(m):
        nonlocal k
        head, qty, price, _old = m.group(1), m.group(2), m.group(3), m.group(4)
        qn = float(qty.replace(',', ''))
        inc = inc2(price)
        return ("'cells': [" + head + f"'{qty}', '{price}', '13%', '{inc:.2f}', '{fmtn(qn * inc)}'" + ']')
    seg = pat.sub(repl, seg)
    LOG.append(f'  fees 行三件套 {k if k else pat.subn.__name__} (计数见下)')
    c = len(re.findall(r"'13%', '\d+\.\d+'", seg))
    LOG.append(f'  13% 插入验证 {c} 行')
    return seg

for ent in ['purchaseOrders', 'salesOrders', 'purchaseInbounds']:
    src = edit(src, ent, trans_price_cols)
    LOG.append(f'{ent} 三件套完成')

# ============================================================
# 2. 销售出库 / 组合出库：数量后插三件套
# ============================================================
PRICE = {'WBX-1210L': '38.00', 'WBX-1210M': '32.00', 'PLT-1210W': '12.00', 'PLT-1210P': '18.00',
         'BTC-6040': '8.50', 'LJ-A100': '6.80', 'LJ-B200': '4.20', 'LJ-C300': '52.00', 'LJ-D400': '36.00',
         'LJ-E500': '78.00', 'LJ-F600': '15.50', 'ZH-2601-A': '2.40', 'ZH-2602-B': '1.80', 'ZH-2603-C': '3.20', 'ZH-2604-D': '2.60'}

def trans_qty_insert(seg):
    old_cols = "'数量', '库位'"
    new_cols = "'数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)', '库位'"
    n = seg.count(old_cols)
    seg = seg.replace(old_cols, new_cols)
    LOG.append(f'  feeCols 数量后插 {n} 处')
    pat = re.compile(r"'cells': \[([^\]]*?), '([\d,]+)', ('[^']*')\]")
    k = [0]
    def repl(m):
        head, qty, last = m.group(1), m.group(2), m.group(3)
        code = ''
        mc = re.search(r"'([A-Z]+-[\w]+)", head)
        if mc:
            code = mc.group(1)
        price = PRICE.get(code, '1.00')
        qn = float(qty.replace(',', ''))
        inc = inc2(price)
        k[0] += 1
        return ("'cells': [" + head + f", '{qty}', '{price}', '13%', '{inc:.2f}', '{fmtn(qn * inc)}', " + last + ']')
    seg = pat.sub(repl, seg)
    LOG.append(f'  fees 行插三件套 {k[0]} 行')
    return seg

for ent in ['salesOutbounds', 'comboOutbounds']:
    src = edit(src, ent, trans_qty_insert)
    LOG.append(f'{ent} 完成')

# ============================================================
# 3. leaseOrders：fees 重构为产品明细
# ============================================================
def trans_lease_fees(seg):
    n_cols = seg.count("'feeCols': ['阶段', '起止', '天数', '套数', '日租金(元/套)', '金额(元)']")
    assert n_cols == 9, n_cols
    seg = seg.replace("'feeCols': ['阶段', '起止', '天数', '套数', '日租金(元/套)', '金额(元)']",
                      "'feeCols': ['产品', '数量', '未税单价(元)', '税率', '含税单价(元)', '含税金额(元)']")
    seg = seg.replace("'feeSecTitle': '租金明细'", "'feeSecTitle': '租赁明细（未税为基准 · 含税自动换算 · 总价=逐行加总）'")
    # 逐记录：行 cells[2]=器具名，旧 fees 首行 套数/日租金
    out = []
    pos = 0
    cnt = 0
    pat_rec = re.compile(r"('cells': \[\"[^\"]*\", \"[^\"]*\", \"([^\"]*)\".*?\])[\s\S]*?'feeSecTitle'[^\n]*\n\s*'feeCols'[^\n]*\n\s*'fees': \[\s*\{\s*'cells': \['[^']*', '[^']*', '[^']*', '([\d,]+)', '([\d.]+)', '[\d,.]+'\]")
    for m in pat_rec.finditer(seg):
        appl, qty, price = m.group(2), m.group(3), m.group(4)
        qn = float(qty.replace(',', ''))
        inc = inc2(price)
        newfees = (f"'fees': [\n        {{\n          'cells': ['{appl}', '{qty}', '{price}', '13%', '{inc:.2f}', '{fmtn(qn * inc)}']\n        }},\n"
                   f"        {{\n          'cells': ['合计', '—', '—', '—', '—', '{fmtn(qn * inc)}']\n        }}\n      ]")
        out.append(seg[pos:m.start()])
        block = m.group(0)
        block2 = re.sub(r"'fees': \[\s*\{\s*'cells': \['[^']*', '[^']*', '[^']*', '[\d,]+', '[\d.]+', '[\d,.]+'\]\s*\}\s*\]", newfees, block, count=1)
        assert block2 != block, appl
        out.append(block2)
        pos = m.end()
        cnt += 1
    out.append(seg[pos:])
    LOG.append(f'  leaseOrders fees 重构 {cnt} 条')
    return ''.join(out)

src = edit(src, 'leaseOrders', trans_lease_fees)
LOG.append('leaseOrders 完成')

# ============================================================
# 4. rentInOrders：fees 重构为多货品明细
# ============================================================
RZD_MAP = {}  # 逐记录构建：器具 → (产品名, 数量, 计费, 单价)
def trans_rzd_fees(seg):
    n_cols = seg.count("'feeCols': ['计费方式', '结算周期', '首期应付(元)', '关联账单', '状态']")
    LOG.append(f'  rentInOrders feeCols {n_cols} 处')
    seg = seg.replace("'feeCols': ['计费方式', '结算周期', '首期应付(元)', '关联账单', '状态']",
                      "'feeCols': ['产品', '数量', '计费方式', '未税单价(元)', '税率', '含税单价(元)', '首期应付(元)']")
    seg = seg.replace("'feeSecTitle': '租金条款 / 结算'", "'feeSecTitle': '租入明细（多货品 · 月租/按套 · 无日租金）'")
    cnt = [0]
    pat_fee = re.compile(r"'fees': \[\s*\{\s*'cells': \['([^']*)', '[^']*', '([\d,.]+)'(, '[^']*')?(, '[^']*')?\](, 'links': \{[^}]*\})?\s*\}\s*\]")
    def repl(m):
        cnt[0] += 1
        desc, first_pay = m.group(1), m.group(2)
        # desc 形如 '日租金 400.00 元 × 30 只' / '按套 50.00 元/套 × 40 套'
        mp = re.search(r'([\d.]+)\s*元\s*×\s*(\d+)\s*(只|套|块)', desc)
        price, qty, unit = (mp.group(1), mp.group(2), mp.group(3)) if mp else ('400.00', '30', '只')
        mode = '月租' if '日租金' in desc or '月' in desc else '按套'
        inc = inc2(price)
        qn = float(qty)
        prod = 'WBX-1210L 围板箱 1200×1000×970（租入）'
        return (f"'fees': [\n        {{\n          'cells': ['{prod}', '{qty} {unit}', '{mode}', '{price}', '13%', '{inc:.2f}', '{first_pay}']\n        }}\n      ]")
    seg2 = pat_fee.sub(repl, seg)
    LOG.append(f'  rentInOrders fees 重构 {cnt[0]} 条')
    return seg2

src = edit(src, 'rentInOrders', trans_rzd_fees)
LOG.append('rentInOrders 完成')

# ============================================================
# 5. salesOrders：去关联采购订单（fields.po + cells 末格）
# ============================================================
def trans_so_remove_po(seg):
    # fields.po 删
    n1 = len(re.findall(r'"po": "PO-[\d-]+", ', seg))
    seg = re.sub(r'"po": "PO-[\d-]+", ', '', seg)
    # cells 末格（PO 链接或 —）
    n2 = len(re.findall(r', "(<span class=\\"lk\\">)?PO-[\d-]+(</span>)?"\]', seg))
    seg = re.sub(r', "(<span class=\\"lk\\">)?PO-[\d-]+(</span>)?"\]', ']', seg)
    LOG.append(f'  salesOrders fields.po 删 {n1} + cells 末格删 {n2}')
    return seg

src = edit(src, 'salesOrders', trans_so_remove_po)
LOG.append('salesOrders 去关联采购订单完成')

DD.write_bytes(src.encode('utf-8'))
import subprocess
r = subprocess.run(['node', '--check', str(DD)], capture_output=True, text=True)
assert r.returncode == 0, 'node --check: ' + r.stderr[:400]
LOG.append('node --check OK')

print('== 批3 Script B ==')
for l in LOG:
    print(' ✓', l)
