# -*- coding: utf-8 -*-
"""盘点2：菜单结构 + 录单页操作列形态"""
from pathlib import Path
import re

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
pages = sorted(ROOT.rglob("*.html"))

# 菜单项：租赁单
n_menu = 0
forms = {}
for p in pages:
    t = p.read_text(encoding="utf-8")
    for m in re.finditer(r'[^\n]*go\([\'"]([^\'"]*租赁单列表\.html)[\'"]\)[^\n]*', t):
        line = m.group(0).strip()
        if 'sm-link' in line or '<li' in line:
            forms.setdefault(line, []).append(str(p.relative_to(ROOT)))
            n_menu += 1
print("== 租赁单菜单项形态 ==")
for k, v in forms.items():
    print(f"  x{len(v)}: {k[:150]}")

# 销售订单菜单项
forms2 = {}
for p in pages:
    t = p.read_text(encoding="utf-8")
    for m in re.finditer(r'[^\n]*go\([\'"]([^\'"]*销售订单列表\.html)[\'"]\)[^\n]*', t):
        line = m.group(0).strip()
        if 'sm-link' in line or '<li' in line:
            forms2.setdefault(line, []).append(str(p.relative_to(ROOT)))
print("\n== 销售订单菜单项形态 ==")
for k, v in forms2.items():
    print(f"  x{len(v)}: {k[:150]}")

# 弹窗独立页是否有侧边栏菜单
has_sidebar = [p for p in pages if 'sm-link' in p.read_text(encoding="utf-8") and 'sm-item' in p.read_text(encoding="utf-8")]
print(f"\n含侧边栏结构页数: {len(has_sidebar)}")

# F01 有无侧边栏
f01 = ROOT / "P3-R01-F01-业务流程导航图.html"
t = f01.read_text(encoding="utf-8")
print(f"F01 含 sm-item: {'sm-item' in t}, 含 sm-link: {'sm-link' in t}")

# 包装管理组完整结构（抽 1 页）
sample = ROOT / "首页" / "项目看板.html"
t = sample.read_text(encoding="utf-8")
i = t.find("包装管理")
# 找第二次出现（菜单里）
j = t.find("包装管理", i+10)
while j != -1 and 'sm-link' not in t[max(0,j-200):j]:
    j = t.find("包装管理", j+10)
start = t.rfind('<li', 0, j)
end = t.find('</ul>', j)
end = t.find('</li>', end+10)
print("\n== 包装管理组结构（项目看板页） ==")
print(t[start:end+10])

# 录单页操作列形态
for f in ["仓储作业/组合出库录单.html", "仓储作业/采购入库录单.html"]:
    t = (ROOT / f).read_text(encoding="utf-8")
    i = t.find("<th>操作</th>")
    print(f"\n== {f} 操作列表格上下文 ==")
    print(t[i-200:i+600])
