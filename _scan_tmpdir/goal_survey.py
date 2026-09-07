# -*- coding: utf-8 -*-
"""目标面盘点：任务一 sticky-op / 任务二 modal-lg / 任务四 菜单顺序"""
from pathlib import Path
import re, json

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
pages = sorted(ROOT.rglob("*.html"))
print(f"总 HTML: {len(pages)}")

# ---- 任务一：th 操作 / td ops 分布 ----
th_op, td_ops, mismatch = [], [], []
for p in pages:
    t = p.read_text(encoding="utf-8")
    c1 = t.count("<th>操作</th>")
    c2 = t.count('<td><span class="ops"')
    sticky = t.count('class="sticky-op"')
    if c1 or c2:
        th_op.append((str(p.relative_to(ROOT)), c1, c2, sticky))
        if c1 != c2:
            mismatch.append((str(p.relative_to(ROOT)), c1, c2))
print("\n== 任务一：含操作列页面 ==")
for r, c1, c2, s in th_op:
    print(f"  {r}  th:{c1} td:{c2} sticky已有:{s}")
print(f"共 {len(th_op)} 页；th/td 数不匹配: {mismatch}")

# th 其他变体（含 th class 或别的写法）
print("\n== th 操作 变体检查 ==")
for p in pages:
    t = p.read_text(encoding="utf-8")
    for m in re.finditer(r"<th[^>]*>\s*操作\s*</th>", t):
        s = m.group(0)
        if s != "<th>操作</th>":
            print(f"  {p.relative_to(ROOT)}: {s!r}")

# td ops 变体
print("\n== td ops 变体检查 ==")
for p in pages:
    t = p.read_text(encoding="utf-8")
    for m in re.finditer(r'<td[^>]*>\s*<span class="ops"', t):
        s = m.group(0)
        if s != '<td><span class="ops"':
            print(f"  {p.relative_to(ROOT)}: {s!r}")

# ---- 任务二：modal-lg 宽度形态 ----
forms = {}
for p in pages:
    t = p.read_text(encoding="utf-8")
    for m in re.finditer(r"\.modal-lg\s*\{[^}]*\}", t):
        forms.setdefault(m.group(0), []).append(str(p.relative_to(ROOT)))
print("\n== 任务二：modal-lg 定义形态 ==")
for k, v in forms.items():
    print(f"  {k!r}  x{len(v)} 页")
    if len(v) <= 3:
        print("    ", v)

# 每页出现次数分布
cnt = {}
for p in pages:
    t = p.read_text(encoding="utf-8")
    n = len(re.findall(r"\.modal-lg\s*\{", t))
    cnt[n] = cnt.get(n, 0) + 1
print(f"  每页定义次数分布: {cnt}")

# ---- 任务四：菜单结构 ----
print("\n== 任务四：菜单 租赁单/销售订单 相邻结构（抽1页） ==")
sample = ROOT / "首页" / "项目看板.html"
t = sample.read_text(encoding="utf-8")
i = t.find("销售订单")
print(t[i-400:i+500])

# 统计各页面租赁单菜单项形态
pat_zl = re.compile(r'<a[^>]*onclick="go\(\x27\.\./包装管理/租赁单列表\.html\x27\)"[^>]*>')
pat_so = re.compile(r'<a[^>]*onclick="go\(\x27\.\./销售管理/销售订单列表\.html\x27\)"[^>]*>')
n_zl = n_so = n_both = 0
for p in pages:
    t = p.read_text(encoding="utf-8")
    zl = pat_zl.search(t)
    so = pat_so.search(t)
    if zl and so:
        n_both += 1
    if zl: n_zl += 1
    if so: n_so += 1
print(f"\n含租赁单菜单项页: {n_zl}；含销售订单菜单项页: {n_so}；两者都有: {n_both}")

# 弹窗独立页里菜单路径可能是 ../../
pat_zl2 = re.compile(r'<a[^>]*onclick="go\(\x27\.\./\.\./包装管理/租赁单列表\.html\x27\)"[^>]*>')
pat_so2 = re.compile(r'<a[^>]*onclick="go\(\x27\.\./\.\./销售管理/销售订单列表\.html\x27\)"[^>]*>')
n2 = n3 = 0
for p in pages:
    t = p.read_text(encoding="utf-8")
    if pat_zl2.search(t): n2 += 1
    if pat_so2.search(t): n3 += 1
print(f"../../ 版菜单：租赁单 {n2} 页；销售订单 {n3} 页")
