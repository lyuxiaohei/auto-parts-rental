# -*- coding: utf-8 -*-
"""G79 退租入库·关联出库单列表多选（替代两步选单）·PW 验证（只读验证脚本·0929）"""
import sys
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-A03-汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
NEW = ROOT + r"\租赁管理\退租入库新建.html"
LIST = ROOT + r"\租赁管理\退租入库列表.html"
DET = ROOT + r"\租赁管理\退租入库详情.html"
results, js_errors = [], []

def check(name, cond, evidence=""):
    results.append((name, bool(cond), evidence))
    print(("[PASS] " if cond else "[FAIL] ") + name + (" | " + evidence if evidence else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.on("console", lambda m: js_errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: js_errors.append(str(e)))

    # ① 新建页结构：两步退场·关联出库单卡+双筛选在位
    pg.goto("file:///" + NEW)
    pg.wait_for_timeout(900)
    body = pg.text_content("body") or ""
    check("①a 两步卡退场（无第一步/第二步字样）", ("第一步" not in body) and ("第二步" not in body))
    check("①b 关联出库单卡在位", "关联出库单" in body and "可多选" in body)
    pf = pg.locator("#g79ProjF option").count()
    cf = pg.locator("#g79CustF option").count()
    check("①c 项目筛选有选项（>1）", pf > 1, "项目选项=" + str(pf))
    check("①d 客户筛选有选项（>1）", cf > 1, "客户选项=" + str(cf))
    head = pg.evaluate("()=>Array.from(document.querySelectorAll('.table-wrap thead th')).slice(0,9).map(t=>t.textContent.trim())")
    check("①e 候选表 9 列含关联租赁单号+所属项目", "关联租赁单号" in head and "所属项目" in head and len(head) >= 9, str(head))
    check("①f 基础信息无关联租赁单号行", ("关联租赁单号：" not in body))
    check("①g 基础信息有关联出库单行", "关联出库单：" in body)

    # ② 多选：勾 2 张华骏单 → 明细汇总+客户/出库单带出
    ckA = pg.locator('.g79Ck[data-key="CK-20260830-015"]')
    ckB = pg.locator('.g79Ck[data-key="CK-20260829-012"]')
    rows = pg.locator("#g57TzOrders .g79Ck")
    n0 = pg.locator("#tzItems tr:not(:has(td[colspan]))").count()
    ckA.check(); pg.wait_for_timeout(300)
    ckB.check(); pg.wait_for_timeout(300)
    n2 = pg.locator("#tzItems tr:not(:has(td[colspan]))").count()
    ckshow = (pg.text_content("#g79CkShow") or "").strip()
    custshow = (pg.text_content("#g57TzCustShow") or "").strip()
    check("②a 勾 2 张→明细汇总带出（行数增加）", n2 > n0 >= 0 and n2 >= 2, "明细行 " + str(n0) + "→" + str(n2))
    check("②b 关联出库单带出（共 2 张）", "共 2 张" in ckshow and ckshow.count("CK-") >= 2, ckshow[:56])
    check("②c 客户带出（华骏）", "华骏" in custshow, custshow[:30])
    # ②d 取消一张→明细回退
    ckB.uncheck(); pg.wait_for_timeout(300)
    n1 = pg.locator("#tzItems tr:not(:has(td[colstyle]))").count()
    n1 = pg.locator("#tzItems tr:not(:has(td[colspan]))").count()
    ckshow2 = (pg.text_content("#g79CkShow") or "").strip()
    check("②d 取消勾选→汇总回退（共 1 张）", "共 1 张" in ckshow2 and n1 < n2, "明细行 " + str(n2) + "→" + str(n1))

    # ③ 筛选联动：客户筛长风→仅长风行
    pg.select_option("#g79CustF", label="客户：长风汽车制造有限公司")
    pg.wait_for_timeout(700)
    custs = pg.locator("#g57TzOrders tr td:nth-child(5)").all_inner_texts()
    check("③a 客户筛选过滤生效", all("长风" in c for c in custs) and len(custs) >= 1, "行数=" + str(len(custs)))
    # ③b 跨客户拦截：已选华骏单（保留）+ 筛回全部后勾长风单 → toast 且复位
    pg.select_option("#g79CustF", label="客户：全部"); pg.wait_for_timeout(500)
    ckC = pg.locator('.g79Ck[data-key="CK-20260828-011"]')
    if ckC.count():
        ckC.click(); pg.wait_for_timeout(600)
        toast = pg.text_content("body") or ""
        blocked = ("只能对应一个客户" in toast)
        still = ckC.is_checked()
        check("③b 跨客户勾选拦截（toast+复位）", blocked and not still, "toast=" + str(blocked) + " 复位=" + str(not still))

    # ④ 超量校验沿用（ckA 华骏仍选中·明细在位）
    pg.wait_for_timeout(300)
    q = pg.locator("#tzItems .tzQty").first
    mx = int(q.get_attribute("data-max"))
    q.fill(str(mx + 3)); pg.wait_for_timeout(400)
    tag = pg.locator(".g57-over")
    check("④ 超量红字沿用", tag.count() >= 1 and ("超原出库数量" in (tag.first.text_content() or "")))
    pg.screenshot(path=r"D:\工作台-吕道远\5-A03-汽车物流包装租赁\_scan_tmpdir\g79_tzrk_multi.png", full_page=True)

    # ⑤ 列表页：关联租赁单号列
    pg.goto("file:///" + LIST)
    pg.wait_for_timeout(900)
    ths = pg.evaluate("()=>Array.from(document.querySelectorAll('.card .table-wrap thead th')).map(t=>t.textContent.trim())")
    check("⑤a 列表表头含关联租赁单号", "关联租赁单号" in ths, str(ths[:8]))
    first = pg.locator(".card tbody tr").first
    tdn = first.locator("td").count()
    zlcell = first.locator("td").nth(4).text_content().strip()
    check("⑤b 首行格数=表头数且第 5 格为 ZL", tdn == len(ths) and zlcell.startswith("ZL-"), "格=" + str(tdn) + "/th=" + str(len(ths)) + " 第5格=" + zlcell[:16])
    # ⑤c 对齐 CSS 生效（数量列右对齐）
    ta = first.locator("td").nth(5).evaluate("el=>getComputedStyle(el).textAlign")
    check("⑤c 数量列右对齐（CSS 已移位）", ta == "right", "textAlign=" + ta)

    # ⑥ 详情：关联出库单行·无关联租赁单号
    pg.goto("file:///" + DET + "?id=TZRK-20260908-011")
    pg.wait_for_timeout(900)
    db = pg.text_content("body") or ""
    check("⑥a 详情含关联出库单（TZRK-011 三张）", ("关联出库单" in db) and ("CK-20260829-012" in db))
    check("⑥b 详情基础信息无关联租赁单号标签", "关联租赁单号" not in db)
    # ⑦ G77 回归：列表新建按钮
    pg.goto("file:///" + LIST); pg.wait_for_timeout(700)
    pg.click(".card-head .head-btns button:has-text('新建')"); pg.wait_for_timeout(800)
    check("⑦ 列表「新建」仍跳本页", "退租入库新建.html" in unquote(pg.url))
    b.close()

fails = [r for r in results if not r[1]]
print("\nJS 错误:", len(js_errors), (js_errors[:3] if js_errors else ""))
print("总判定: %d PASS / %d FAIL" % (len(results) - len(fails), len(fails)))
sys.exit(1 if fails or js_errors else 0)
