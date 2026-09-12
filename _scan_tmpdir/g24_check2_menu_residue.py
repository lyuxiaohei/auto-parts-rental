# -*- coding: utf-8 -*-
"""G24 T2 证据采集②：菜单结构+残留词上下文+A02 对照"""
import os, re, io

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
PROTO = os.path.join(ROOT, "P3-R01-包装租赁管理后台原型")

def read(rel):
    return io.open(os.path.join(PROTO, rel), encoding="utf-8", errors="replace").read()

print("== 菜单抽取（销售订单列表.html 中 class 含 menu/nav/sidebar 片段探测）==")
t = read("销售管理/销售订单列表.html")
# 找含「项目管理」与「系统管理」同时出现的最短段=侧边栏
i1, i2 = t.find("项目管理"), t.find("系统管理")
seg = None
for m in re.finditer(r'<(aside|nav|div)[^>]*(menu|side|nav)[^>]*>', t, re.I):
    end = t.find('</' + m.group(1) + '>', m.start())
    cand = t[m.start():end]
    if cand.count('href') > 10:
        seg = cand
        break
if seg is None:
    # 兜底：取 body 内第一个 <ul> 群
    m = re.search(r'<ul[^>]*>.*?</ul>\s*</', t, re.S)
    seg = m.group(0) if m else t[:2000]
links = re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', seg, re.S)
for href, txt in links:
    txt = re.sub(r'<[^>]+>', '', txt).strip()
    print(f"  {txt}  →  {href}")

print()
print("== 组名抽取（group-title/组标题类）==")
for mm in re.finditer(r'<(?:div|span|p)[^>]*class="[^"]*(group|title|nav-label|menu-label)[^"]*"[^>]*>([^<]{2,12})</', seg, re.I):
    s = mm.group(2).strip()
    if s and 'href' not in s:
        print("  ", s)

print()
print("== 残留词上下文采样 ==")
def ctx(rel, kw, n=3, w=60):
    t = read(rel)
    out = []
    start = 0
    for _ in range(n):
        i = t.find(kw, start)
        if i < 0:
            break
        out.append(t[max(0, i - w):i + w].replace("\n", " "))
        start = i + 1
    return out

for rel, kw in [
    ("P3-R01-F01-业务流程导航图.html", "退租申请"),
    ("仓储作业/库存查询.html", "退租申请"),
    ("P3-R01-F01-业务流程导航图.html", "拆卸"),
    ("租赁管理/退租入库列表.html", "拆卸"),
    ("租赁管理/租赁单列表.html", "丢损赔偿单"),
    ("财务协同/应收账单.html", "丢损赔偿单"),
    ("系统管理/数据字典.html", "丢损赔偿单"),
    ("仓储作业/库存查询.html", "组装"),
]:
    print(f"[{rel} · {kw}]")
    for c in ctx(rel, kw, 2):
        print("   …" + c + "…")
    print()
