# -*- coding: utf-8 -*-
"""G78 退租入库单显式关联租赁单·PW 验证（只读验证脚本·0929）"""
import sys
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-A03-汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
NEW = ROOT + r"\租赁管理\退租入库新建.html"
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

    # ① 新建页：候选表 9 列含「关联租赁单号」
    pg.goto("file:///" + NEW)
    pg.wait_for_timeout(800)
    ths = [t.strip() for t in pg.locator("#g57TzOrders").evaluate("el=>[]")]
    head = pg.locator(".table-wrap table thead th").all_inner_texts()
    head = [h.strip() for h in head]
    check("①a 候选表含「关联租赁单号」列", "关联租赁单号" in head, str(head[:6]))
    first_cells = [c.strip() for c in pg.locator("#g57TzOrders tr").first.locator("td").all_inner_texts()]
    check("①b 运行时行 9 格且第 2 格为 ZL", len(first_cells) == 9 and first_cells[1].startswith("ZL-"),
          "格数=" + str(len(first_cells)) + " 第2格=" + (first_cells[1] if len(first_cells) > 1 else "无"))
    check("①c 信息卡「关联租赁单号」占位行在位", "第二步选单后由出库单带出" in (pg.text_content("#g57TzZlShow") or ""))

    # ② 点「选择」→ 带出 zl（首行 CK-20260830-015 → ZL-20260610-015）
    pg.locator("#g57TzOrders tr").first.locator("a:has-text('选择')").click()
    pg.wait_for_timeout(500)
    zl = pg.text_content("#g57TzZlShow") or ""
    check("②a 选单后带出关联租赁单号", zl.startswith("ZL-") and "由出库单带出" in zl, zl.strip()[:44])
    # ②b 换客户复位
    pg.select_option("#g57TzCust", label="星途新能源汽车科技有限公司")
    pg.wait_for_timeout(800)
    zl2 = pg.text_content("#g57TzZlShow") or ""
    check("②b 换客户后复位占位", "第二步选单后由出库单带出" in zl2, zl2.strip()[:30])
    # ②c 星途选单带出
    if pg.locator("#g57TzOrders tr a:has-text('选择')").count():
        pg.locator("#g57TzOrders tr").first.locator("a:has-text('选择')").click()
        pg.wait_for_timeout(400)
        zl3 = pg.text_content("#g57TzZlShow") or ""
        check("②c 星途选单后带出", zl3.startswith("ZL-"), zl3.strip()[:40])
    pg.screenshot(path=r"D:\工作台-吕道远\5-A03-汽车物流包装租赁\_scan_tmpdir\g78_tzrk_zl.png", full_page=True)

    # ③ 详情页（数据驱动）：TZRK-011 显示关联租赁单号行
    pg.goto("file:///" + DET + "?id=TZRK-20260908-011")
    pg.wait_for_timeout(900)
    body = pg.text_content("body") or ""
    check("③a 详情含「关联租赁单号」标签", "关联租赁单号" in body)
    check("③b TZRK-011 值含 ZL-20260823-033（与修正后出库单一致）", "ZL-20260823-033" in body)
    # ③c 转租例外行
    pg.goto("file:///" + DET + "?id=TZRK-20260915-012")
    pg.wait_for_timeout(900)
    body2 = pg.text_content("body") or ""
    check("③c TZRK-012 转租例外注记", "经转移出库 ZY-20260914-001" in body2)
    # ③d 审核页同样带出
    pg.goto("file:///" + ROOT + r"\租赁管理\退租入库审核.html?id=TZRK-20260903-009")
    pg.wait_for_timeout(900)
    body3 = pg.text_content("body") or ""
    check("③d 审核页 TZRK-009 含 ZL-20260816-029", "ZL-20260816-029" in body3)
    b.close()

fails = [r for r in results if not r[1]]
print("\nJS 错误:", len(js_errors), (js_errors[:3] if js_errors else ""))
print("总判定: %d PASS / %d FAIL" % (len(results) - len(fails), len(fails)))
sys.exit(1 if fails or js_errors else 0)
