# -*- coding: utf-8 -*-
"""#8 统一执行：F01 主图 Geist/Instrument→体系栈·登录变体→标准栈·A06 trebuchet→体系栈·15px→14px（业务页）。
出货单打印 SimHei（单据风有意）与 A06 mermaid var() 机制不动；F01 SVG 内部标签字号（图表排版）不动。"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
BK = ROOT / 'backup-font-20260919'

MAIN_STACK = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif"
MONO_STACK = 'Consolas,Monaco,monospace'

def swap(rel, pairs):
    p = PROTO / rel
    b = p.read_bytes()
    n = 0
    for old, new in pairs:
        c = b.count(old.encode('utf-8'))
        if c:
            d = BK / rel
            d.parent.mkdir(parents=True, exist_ok=True)
            if not d.exists():
                shutil.copy2(p, d)
            b = b.replace(old.encode('utf-8'), new.encode('utf-8'))
            n += c
    if n:
        p.write_bytes(b)
    return n

total = 0
# 1) F01 主图：先探形态再换
f01 = PROTO / 'P3-R01-F01-业务流程导航图.html'
t = f01.read_text(encoding='utf-8')
import re
geist_forms = sorted(set(re.findall(r"font-family\s*:\s*[^;{}]{0,80}(?:Geist|Instrument Serif)[^;{}]{0,40}", t)))
print('F01 体系外声明形态:')
for g in geist_forms:
    print('  ', repr(g))
pairs = []
for g in geist_forms:
    if 'Mono' in g:
        pairs.append((g, 'font-family: ' + MONO_STACK))
    else:
        pairs.append((g, 'font-family: ' + MAIN_STACK))
n = swap('P3-R01-F01-业务流程导航图.html', pairs)
print('F01 替换 %d 处' % n); total += n

# 2) 登录页变体 → 主栈（body 级）
n = swap('登录.html', [
    ('font-family: "Microsoft YaHei", "PingFang SC", sans-serif', 'font-family: ' + MAIN_STACK),
])
print('登录 替换 %d 处' % n); total += n

# 3) A06 trebuchet 字面声明 → 体系栈（var() 机制行不动）
n = swap('P3-R01-A06-实体关系与状态机.html', [
    ("font-family: 'trebuchet ms', verdana, arial, sans-serif", 'font-family: ' + MAIN_STACK),
])
print('A06 替换 %d 处' % n); total += n

# 4) 业务页 15px → 14px（F01/A06/打印页不动）
biz_15 = ['登录.html', '采购管理/采购入库录单.html', '采购管理/采购订单列表.html', '销售管理/销售订单列表.html']
for rel in biz_15:
    p = PROTO / rel
    b = p.read_bytes()
    c = b.count(b'font-size:15px') + b.count(b'font-size: 15px')
    if c:
        d = BK / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        if not d.exists():
            shutil.copy2(p, d)
        b = b.replace(b'font-size:15px', b'font-size:14px').replace(b'font-size: 15px', b'font-size:14px')
        p.write_bytes(b)
    print(rel, '15px→14px %d 处' % c); total += c

print('合计替换 %d 处' % total)
