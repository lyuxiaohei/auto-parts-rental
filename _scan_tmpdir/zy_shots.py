# -*- coding: utf-8 -*-
"""转移出库加审·截图验证六件：列表/审核页/待办/库存弹窗/权限矩阵/详情两态"""
import os, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + u"/P3-R01-包装租赁管理后台原型"
OUT = os.path.abspath(__file__).replace(u"zy_shots.py", u"zy_shots")
os.makedirs(OUT, exist_ok=True)

SHOTS = [
    # (名称, 相对路径, 打开后执行的 JS 或 None)
    (u"01-转移出库列表", u"租赁管理/转移出库列表.html", None),
    (u"02-转移出库审核", u"租赁管理/转移出库审核.html", None),
    (u"03-我的待办", u"我的待办.html", None),
    (u"04-库存查询弹窗", u"仓储作业/库存查询.html", "openModal('rentDrillModal')"),
    (u"05-权限配置矩阵", u"系统管理/权限配置.html", "document.getElementById('auditPermMatrix').scrollIntoView()"),
    (u"06-详情待审核态", u"租赁管理/转移出库单详情.html?id=ZY-20260915-005", None),
    (u"07-详情已转移态", u"租赁管理/转移出库单详情.html?id=ZY-20260914-001", None),
]

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)[:120]))
    for name, rel, js in SHOTS:
        page.goto(u"file:///" + os.path.join(ROOT, rel).replace(u"\\", u"/"), wait_until="load")
        try:
            page.wait_for_selector("tbody tr", timeout=3000)
        except Exception:
            pass
        page.wait_for_timeout(400)
        if js:
            page.evaluate(js)
            page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(OUT, name + u".png"), full_page=False)
        print("shot:", name)
    browser.close()
    print("pageerror 合计:", len(errs), errs[:3])
