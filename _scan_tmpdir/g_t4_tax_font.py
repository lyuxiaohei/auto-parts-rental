# -*- coding: utf-8 -*-
"""T4 新建物料弹窗：供应商税率区 12px→13px 对齐上方表单（双层：产品档案 createModal+新建产品模板）"""
import io

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
FILES = [ROOT + r"\基础数据\产品档案.html", ROOT + r"\基础数据\弹窗\新建产品.html"]

REPL = [
    ("  .tax-edit-hd{display:flex;gap:8px;font-size:12px;color:#8c8c8c;padding:2px 0 6px;}",
     "  .tax-edit-hd{display:flex;gap:8px;font-size:13px;color:#8c8c8c;padding:2px 0 6px;}"),
    ("  .tax-sel,.tax-in{width:100%;height:28px;border:1px solid #d9d9d9;border-radius:4px;font-size:12px;padding:0 6px;outline:none;box-sizing:border-box;}",
     "  .tax-sel,.tax-in{width:100%;height:28px;border:1px solid #d9d9d9;border-radius:4px;font-size:13px;padding:0 6px;outline:none;box-sizing:border-box;}"),
    ("  .tax-del{color:#1677ff;font-size:12px;text-decoration:none;white-space:nowrap;}",
     "  .tax-del{color:#1677ff;font-size:13px;text-decoration:none;white-space:nowrap;}"),
]

for fp in FILES:
    t = io.open(fp, encoding="utf-8", newline="").read()
    name = fp.split(chr(92))[-1]
    if "font-size:13px;color:#8c8c8c" in t:
        print("SKIP 已完成", name)
        continue
    for old, new in REPL:
        assert t.count(old) == 1, name + " 锚点非 1: " + old[:50] + " = " + str(t.count(old))
        t = t.replace(old, new, 1)
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    print("PASS", name, "·税率区 13px 对齐")
