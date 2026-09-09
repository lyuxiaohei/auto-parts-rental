# -*- coding: utf-8 -*-
"""批1 Stage3：全站路径替换（11 组映射），二进制读写保行尾，assert 计数留档"""
from pathlib import Path
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"

MAPS = [
    ('仓储作业/采购入库列表.html', '采购管理/采购入库列表.html'),
    ('仓储作业/采购入库录单.html', '采购管理/采购入库录单.html'),
    ('仓储作业/销售出库列表.html', '销售管理/销售出库列表.html'),
    ('销售管理/租赁单列表.html', '租赁管理/租赁单列表.html'),
    ('采购管理/租入单列表.html', '租赁管理/租入单列表.html'),
    ('仓储作业/租入入库列表.html', '租赁管理/租入入库列表.html'),
    ('仓储作业/组合出库列表.html', '租赁管理/组合出库列表.html'),
    ('仓储作业/组合出库录单.html', '租赁管理/组合出库录单.html'),
    ('仓储作业/退租入库列表.html', '租赁管理/退租入库列表.html'),
    ('仓储作业/租入归还列表.html', '租赁管理/租入归还列表.html'),
    ('首页/我的待办.html', '我的待办.html'),
]

files = sorted(PROTO.rglob("*.html"))
files += sorted((PROTO / "_data").glob("*.js"))
files += [PROTO / "P3-R01-A04-流程链标注数据.json", PROTO / "P3-R01-A03-标注数据.json",
          ROOT / "_scan_tmpdir" / "verify_listfull.py"]

total = {old: 0 for old, _ in MAPS}
per_file = {}
for f in files:
    if not f.exists(): continue
    raw = f.read_bytes()
    txt = raw.decode('utf-8')
    n0 = 0
    for old, new in MAPS:
        c = txt.count(old)
        if c:
            txt = txt.replace(old, new)
            total[old] += c
            n0 += c
    if n0:
        f.write_bytes(txt.encode('utf-8'))
        per_file[str(f.relative_to(ROOT))] = n0

print("== 每映射计数 ==")
for old, n in total.items():
    print(f"  {old} -> {n} 处")
print("== 每文件计数 ==")
for k, v in per_file.items():
    print(f"  {v:3d}  {k}")
print(f"合计 {sum(total.values())} 处，改写 {len(per_file)} 文件")

# 校验：全站无旧路径残留
leftover = []
for f in files:
    if not f.exists(): continue
    txt = f.read_bytes().decode('utf-8')
    for old, _ in MAPS:
        if old in txt:
            leftover.append((str(f.relative_to(ROOT)), old))
assert not leftover, f"旧路径残留: {leftover}"
print("PASS: 无旧路径残留")
