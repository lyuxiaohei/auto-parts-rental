# -*- coding: utf-8 -*-
"""G24 T2 证据采集①：原型目录/页面清单/菜单结构/移除模块验证"""
import os, re, io, json

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
PROTO = os.path.join(ROOT, "P3-R01-包装租赁管理后台原型")

def read(rel, enc="utf-8"):
    p = os.path.join(PROTO, rel)
    if not os.path.exists(p):
        return None
    return io.open(p, encoding=enc, errors="replace").read()

print("== 目录结构（模块目录下页面）==")
for d in sorted(os.listdir(PROTO)):
    dp = os.path.join(PROTO, d)
    if os.path.isdir(dp) and d not in ("_data", "mobile"):
        pages = [f for f in sorted(os.listdir(dp)) if f.lower().endswith(".html")]
        modal = os.path.join(dp, "弹窗")
        modals = [f for f in sorted(os.listdir(modal))] if os.path.isdir(modal) else []
        print(f"[{d}] 页面 {len(pages)}: {pages}")
        if modals:
            print(f"    弹窗 {len(modals)}")

print()
print("== 根级 HTML ==")
print(sorted(f for f in os.listdir(PROTO) if f.lower().endswith(".html") and os.path.isfile(os.path.join(PROTO, f))))
print("mobile:", sorted(os.listdir(os.path.join(PROTO, "mobile"))))

print()
print("== 移除模块验证（全目录文件名+内容关键词）==")
removed_kw = ["退租申请", "组装管理", "拆卸管理", "丢损赔偿"]
fn_hits = []
for dirpath, dirnames, filenames in os.walk(PROTO):
    for fn in filenames:
        for kw in removed_kw:
            if kw in fn:
                fn_hits.append(os.path.relpath(os.path.join(dirpath, fn), PROTO))
print("文件名含移除模块词:", fn_hits if fn_hits else "0 处（PASS）")

# 页面内容中的残留（区分：菜单链接/待办选项/操作日志历史行属正常留档）
print()
print("== 内容残留扫描（业务页 HTML，弹窗模板单独列）==")
for kw in ["退租申请", "组装", "拆卸", "丢损赔偿单"]:
    biz_hits, modal_hits, other_hits = [], [], []
    for dirpath, dirnames, filenames in os.walk(PROTO):
        for fn in filenames:
            if not fn.lower().endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, PROTO).replace("\\", "/")
            try:
                t = io.open(fp, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            n = t.count(kw)
            if n:
                if "/弹窗/" in rel or "mobile/" in rel or rel.startswith("弹窗/"):
                    modal_hits.append((rel, n))
                else:
                    biz_hits.append((rel, n))
    print(f"关键词「{kw}」业务页命中: {biz_hits if biz_hits else 0}")
    if modal_hits:
        print(f"    弹窗/mobile 命中: {modal_hits}")

print()
print("== 菜单结构（取 销售管理/销售订单列表.html 侧边栏）==")
t = read("销售管理/销售订单列表.html")
m = re.search(r'<aside[^>]*>.*?</aside>', t, re.S) or re.search(r'<nav[^>]*class="[^"]*sidebar[^"]*"[^>]*>.*?</nav>', t, re.S)
if m:
    seg = m.group(0)
    # 抽组标题与链接
    for mm in re.finditer(r'<div class="group-title"[^>]*>([^<]+)</div>|<a [^>]*href="([^"]+)"[^>]*>\s*([^<]+?)\s*</a>', seg):
        if mm.group(1):
            print("组:", mm.group(1).strip())
        else:
            print("  链接:", (mm.group(2) or "").strip(), "→", (mm.group(3) or "").strip())
else:
    print("未匹配 aside/nav，改抽 menu 结构")
    seg = re.search(r'class="menu".*?(?=<main|class="content")', t, re.S)
    print(seg.group(0)[:3000] if seg else "无")
