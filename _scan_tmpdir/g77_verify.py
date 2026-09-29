# -*- coding: utf-8 -*-
"""G77 退租入库列表「新建」按钮恢复·PW 验证（只读验证脚本·0929）"""
import sys, time
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-A03-汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
LIST = ROOT + r"\租赁管理\退租入库列表.html"
NEW = ROOT + r"\租赁管理\退租入库新建.html"
results, js_errors = [], []

def check(name, cond, evidence=""):
    results.append((name, bool(cond), evidence))
    print(("[PASS] " if cond else "[FAIL] ") + name + (" | " + evidence if evidence else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.on("console", lambda m: js_errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: js_errors.append(str(e)))

    # ① 列表页：新建按钮在位（批量审核之后）+ 点击跳两步选单页
    pg.goto("file:///" + LIST)
    pg.wait_for_timeout(600)
    btns = pg.locator(".card-head .head-btns button")
    texts = [btns.nth(i).text_content().strip() for i in range(btns.count())]
    check("①a 列表头部按钮序=批量导出/批量审核/新建", texts == ["批量导出", "批量审核", "新建"], str(texts))
    pg.click(".card-head .head-btns button:has-text('新建')")
    pg.wait_for_timeout(800)
    url = unquote(pg.url)
    check("①b 点击新建→两步选单页", "退租入库新建.html" in url, url.split("/")[-1])

    # ② 两步页结构：说明条/第一步/第二步/提交条在位
    check("②a 页顶两步说明在位", "第一步选退回客户" in pg.text_content(".pn-hint"))
    check("②b 第一步卡片在位", "第一步 · 选择退回客户" in pg.text_content("body"))
    check("②c 第二步出库单候选表有行", pg.locator("#g57TzOrders tr").count() >= 3,
          "rows=" + str(pg.locator("#g57TzOrders tr").count()))
    check("②d 提交条在位（取消/提交审核）", pg.locator(".submit-bar button").count() == 2)

    # ③ 演示动线：选客户（换星途）→ 第二步重渲染该客户单 → 点「选择」带出明细
    pg.select_option("#g57TzCust", label="星途新能源汽车科技有限公司")
    pg.wait_for_timeout(900)
    rows_after = pg.locator("#g57TzOrders tr").count()
    cust_cells = [pg.locator("#g57TzOrders tr").nth(i).locator("td").nth(3).text_content().strip()
                  for i in range(rows_after)]
    check("③a 换客户后第二步联动过滤", rows_after >= 1 and all("星途" in c for c in cust_cells),
          "rows=" + str(rows_after) + " cust=" + (cust_cells[0] if cust_cells else "无"))
    if rows_after:
        pg.locator("#g57TzOrders tr").first.locator("a:has-text('选择')").click()
        pg.wait_for_timeout(600)
        det_rows = pg.locator("#tzItems tr").count()
        orig_qty = pg.locator("#tzItems tr").first.locator("td").nth(3).text_content().strip()
        check("③b 点选择→明细带出（含原出库数量列）", det_rows >= 1 and orig_qty != "",
              "明细行=" + str(det_rows) + " 原出库数量=" + orig_qty)
        # ③c 超量校验：退租数量填超原出库 → 红字
        qty_input = pg.locator("#tzItems tr").first.locator(".tzQty")
        maxv = int(qty_input.get_attribute("data-max") or orig_qty)
        qty_input.fill(str(maxv + 5))
        pg.wait_for_timeout(400)
        body = pg.text_content("body")
        check("③c 超原出库数量红字拦截", ("超原出库数量" in body) and (str(maxv + 5) in body),
              "max=" + str(maxv) + " 输入=" + str(maxv + 5))
        qty_input.fill(str(maxv))
        pg.wait_for_timeout(300)
    # ④ 客户带出只读显示随第一步
    show = pg.text_content("#g57TzCustShow") or ""
    check("④ 信息卡客户随第一步带出", "星途" in show, show.strip()[:30])
    # ⑤ 取消返回列表
    pg.click(".submit-bar button:has-text('取消')")
    pg.wait_for_timeout(800)
    check("⑤ 取消返回退租入库列表", "退租入库列表.html" in unquote(pg.url))
    # ⑥ 截图留档（新建页全页）
    pg.goto("file:///" + NEW)
    pg.wait_for_timeout(700)
    pg.screenshot(path=r"D:\工作台-吕道远\5-A03-汽车物流包装租赁\_scan_tmpdir\g77_tzrk_new.png", full_page=True)
    b.close()

fails = [r for r in results if not r[1]]
print("\nJS 错误:", len(js_errors), (js_errors[:3] if js_errors else ""))
print("总判定: %d PASS / %d FAIL" % (len(results) - len(fails), len(fails)))
sys.exit(1 if fails or js_errors else 0)
