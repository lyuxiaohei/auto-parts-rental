# -*- coding: utf-8 -*-
"""G25 PW 抽验：F01+库存查询/角色管理/应收账单 渲染无 JS 错+截图留档"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

PROTO = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型").resolve()
OUT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir")

PAGES = [
    ("F01", "P3-R01-F01-业务流程导航图.html", "g25-f01-after.png", ["物料买卖", "向供应商租入", "按第3次沟通纪要"]),
    ("库存查询", "仓储作业/库存查询.html", "g25-kucun-after.png", ["租入"]),
    ("角色管理", "系统管理/角色管理.html", "g25-juese-after.png", ["可审单据"]),
    ("应收账单", "财务协同/应收账单.html", "g25-ys-after.png", ["供应商应收"]),
]

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for name, rel, shot, kws in PAGES:
        pg = b.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
        pg.on("console", lambda m: errs.append(m.text[:150]) if m.type == "error" and "ERR_CONNECTION" not in m.text else None)
        pg.goto((PROTO / rel).as_uri(), wait_until="load")
        pg.wait_for_timeout(600)
        body = pg.evaluate("document.body.innerText")
        missing = [k for k in kws if k not in body]
        # F01 外链断网豁免（Google Fonts）
        real_errs = [e for e in errs if "ERR_CONNECTION" not in e and "net::" not in e]
        pg.screenshot(path=str(OUT / shot), full_page=True)
        ok = len(real_errs) == 0 and not missing
        print(("PASS " if ok else "FAIL ") + "%s：JS错 %d·关键词缺 %s·截图 %s" % (name, len(real_errs), missing or "无", shot))
        if real_errs:
            print("  JS:", real_errs[:3])
        pg.close()
    b.close()
