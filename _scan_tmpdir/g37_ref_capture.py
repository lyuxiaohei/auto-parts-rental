# -*- coding: utf-8 -*-
"""G37 样式锚点截图：Axure 样板页 + 本项目 mobile 现状页。一次性建任务用。"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
OUT = ROOT / "_scan_tmpdir" / "g37_ref"
OUT.mkdir(parents=True, exist_ok=True)

BASE = "https://www.axured.cn/assets/axurefiles/b12c4e343bf8ed8771bacdba1d1216bc_1368"
import urllib.parse
AXURE = ["审批列表", "待办事项", "个人中心", "登录页", "数据列表", "Form 表单", "产品详情"]
LOCAL = ["待办审批", "审批详情", "库存查询", "我的", "登录"]

with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page(viewport={"width": 375, "height": 812})
    for name in AXURE:
        url = f"{BASE}/{urllib.parse.quote(name)}.html"
        pg.goto(url, wait_until="networkidle")
        pg.wait_for_timeout(1200)
        pg.screenshot(path=str(OUT / f"axure-{name}.png"), full_page=True)
        print(f"axure-{name}.png ok")
    for name in LOCAL:
        uri = (ROOT / "P3-R01-包装租赁管理后台原型" / "mobile" / f"{name}.html").as_uri()
        pg.goto(uri, wait_until="networkidle")
        pg.wait_for_timeout(900)
        pg.screenshot(path=str(OUT / f"now-{name}.png"), full_page=True)
        print(f"now-{name}.png ok")
    br.close()
print("ALL DONE")
