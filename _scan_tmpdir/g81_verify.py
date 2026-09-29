# -*- coding: utf-8 -*-
"""G81 吴越第二供应商示例数据＋归还类型退场·PW 验证（只读验证脚本·0929）"""
import sys
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-A03-汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
NEW = ROOT + r"\租入管理\归还出库新建.html"
LIST = ROOT + r"\租入管理\归还出库列表.html"
DET = ROOT + r"\租入管理\归还出库详情.html"
RZD_DET = ROOT + r"\租入管理\租入单详情.html"
results, js_errors = [], []

def check(name, cond, evidence=""):
    results.append((name, bool(cond), evidence))
    print(("[PASS] " if cond else "[FAIL] ") + name + (" | " + evidence if evidence else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.on("console", lambda m: js_errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: js_errors.append(str(e)))

    # ① 新建页：类型退场＋吴越候选在位
    pg.goto("file:///" + NEW)
    pg.wait_for_timeout(900)
    body = pg.text_content("body") or ""
    check("①a 归还类型字段退场（无 radio/词样）", "归还类型" not in body and "整退归还" not in body and "分流归还" not in body)
    sups = pg.locator("#g80RzdBody td:nth-child(4)").all_inner_texts()
    check("①b 候选含吴越两单（真实多供应商）", any("吴越" in s for s in sups), "候选供应商分布=" + str({s[:4] for s in sups}))
    check("①c 候选含环通单", any("环通" in s for s in sups))

    # ② 真实跨供应商拦截：勾吴越 011 → 勾环通 003 → toast+复位
    ckWY = pg.locator('.g80Ck[data-key="RZD-20260916-011"]')
    ckHT = pg.locator('.g80Ck[data-key="RZD-20260815-003"]')
    ckWY.check(); pg.wait_for_timeout(300)
    ckHT.click(); pg.wait_for_timeout(600)
    toast = pg.text_content("body") or ""
    still = ckHT.is_checked()
    check("② 真实跨供应商拦截（toast+复位）", ("只能对应一个供应商" in toast) and (not still),
          "toast=" + str("只能对应一个供应商" in toast) + " 复位=" + str(not still))
    # ②b 同供应商多选仍通：吴越 011+012
    ckWY2 = pg.locator('.g80Ck[data-key="RZD-20260920-012"]')
    ckWY2.check(); pg.wait_for_timeout(400)
    rzdshow = (pg.text_content("#g80RzdShow") or "").strip()
    supshow = (pg.text_content("#g80SupShow") or "").strip()
    check("②b 同供应商多选通过（共 2 张·吴越）", "共 2 张" in rzdshow and "吴越" in supshow, rzdshow[:46])
    pg.screenshot(path=r"D:\工作台-吕道远\5-A03-汽车物流包装租赁\_scan_tmpdir\g81_wuyue_multi.png", full_page=True)

    # ③ 列表页：类型列退场＋GHCK-004 吴越行在位
    pg.goto("file:///" + LIST)
    pg.wait_for_timeout(900)
    ths = pg.evaluate("()=>Array.from(document.querySelectorAll('.card .table-wrap thead th')).map(t=>t.textContent.trim())")
    check("③a 表头无归还类型", "归还类型" not in ths, str(ths[:6]))
    lbody = pg.text_content("body") or ""
    check("③b GHCK-004 吴越行在位", "GHCK-20260924-004" in lbody and "吴越联合" in lbody)
    first = pg.locator(".card tbody tr").first
    check("③c 行格数=表头数", first.locator("td").count() == len(ths),
          "格=" + str(first.locator("td").count()) + "/th=" + str(len(ths)))

    # ④ 详情：GHCK-004 三卡渲染＋无类型标签
    pg.goto("file:///" + DET + "?id=GHCK-20260924-004")
    pg.wait_for_timeout(900)
    db = pg.text_content("body") or ""
    check("④a GHCK-004 详情渲染（吴越/押金部分退还/结算）", ("吴越联合" in db) and ("部分退还 ¥3,840.00" in db) and ("96.00 元" in db))
    check("④b 详情无归还类型标签", "归还类型" not in db)

    # ⑤ 新租入单详情渲染（011 三卡）
    pg.goto("file:///" + RZD_DET + "?id=RZD-20260916-011")
    pg.wait_for_timeout(900)
    rb = pg.text_content("body") or ""
    check("⑤ 新租入单 011 详情（金属托盘 80 块/PRJ-2606/履行中）", ("金属托盘" in rb) and ("PRJ-2606" in rb) and ("履行中" in rb))

    # ⑥ 闭环动线（类型退场后）：列表→新建→勾选→明细→提交条在位
    pg.goto("file:///" + LIST); pg.wait_for_timeout(700)
    pg.click(".card-head .head-btns button:has-text('新建')"); pg.wait_for_timeout(800)
    check("⑥a 列表新建→新建页", "归还出库新建.html" in unquote(pg.url))
    pg.locator('.g80Ck[data-key="RZD-20260916-011"]').check(); pg.wait_for_timeout(400)
    n = pg.locator("#riItemsBody tr:not(:has(td[colspan]))").count()
    check("⑥b 勾选→明细带出（闭环不受类型退场影响）", n >= 1, "明细行=" + str(n))
    check("⑥c 提交条在位（提交审核）", pg.locator(".submit-bar button:has-text('提交审核')").count() == 1)
    b.close()

fails = [r for r in results if not r[1]]
print("\nJS 错误:", len(js_errors), (js_errors[:3] if js_errors else ""))
print("总判定: %d PASS / %d FAIL" % (len(results) - len(fails), len(fails)))
sys.exit(1 if fails or js_errors else 0)
