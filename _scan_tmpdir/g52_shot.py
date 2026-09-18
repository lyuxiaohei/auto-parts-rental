# -*- coding: utf-8 -*-
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
OUT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir"
PAGES = [r"仓储作业\调拨新建.html", r"仓储作业\其他入库新建.html", r"仓储作业\其他出库新建.html", r"租赁管理\转移出库新建.html"]

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    for rel in PAGES:
        page = ctx.new_page()
        page.goto("file:///" + os.path.join(ROOT, rel).replace("\\", "/"))
        page.wait_for_timeout(500)
        name = os.path.splitext(os.path.basename(rel))[0]
        out = os.path.join(OUT, "g52_" + name + ".png")
        page.screenshot(path=out, full_page=True)
        print(out, os.path.getsize(out))
        page.close()
    b.close()
