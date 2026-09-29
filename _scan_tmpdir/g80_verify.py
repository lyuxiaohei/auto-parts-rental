# -*- coding: utf-8 -*-
"""G80 归还出库对齐 G79 形态（关联租入单列表多选）·PW 验证（只读验证脚本·0929）"""
import sys
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-A03-汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
NEW = ROOT + r"\租入管理\归还出库新建.html"
DET = ROOT + r"\租入管理\归还出库详情.html"
RZDLIST = ROOT + r"\租入管理\租入单列表.html"
results, js_errors = [], []

def check(name, cond, evidence=""):
    results.append((name, bool(cond), evidence))
    print(("[PASS] " if cond else "[FAIL] ") + name + (" | " + evidence if evidence else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.on("console", lambda m: js_errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: js_errors.append(str(e)))

    # ① 结构
    pg.goto("file:///" + NEW)
    pg.wait_for_timeout(900)
    body = pg.text_content("body") or ""
    check("①a 单选下拉退场（无 riSelect）", pg.locator("#riSelect").count() == 0)
    check("①b 关联租入单卡在位（可多选·同一供应商）", "关联租入单" in body and "可多选" in body)
    pf = pg.locator("#g80ProjF option").count()
    sf = pg.locator("#g80SupF option").count()
    check("①c 项目筛选有值（履行中/部分归还两单→2 项目）", pf == 3, "选项=" + str(pf))
    check("①d 供应商筛选有值", sf >= 2, "选项=" + str(sf))
    head = pg.evaluate("()=>Array.from(document.querySelectorAll('.table-wrap thead th')).map(t=>t.textContent.trim()).slice(0,10)")
    check("①e 候选表 10 列（类型/项目/已归还/可归还）", all(w in head for w in ["类型", "所属项目", "已归还", "可归还"]) and len(head) >= 10, str(head[:7]))
    check("①f 信息卡供应商/关联租入单带出行在位", ("供应商：" in body) and ("关联租入单：" in body))

    # ② 多选
    ckA = pg.locator('.g80Ck[data-key="RZD-20260815-005"]')
    ckB = pg.locator('.g80Ck[data-key="RZD-20260815-003"]')
    n0 = pg.locator("#riItemsBody tr:not(:has(td[colspan]))").count()
    ckA.check(); pg.wait_for_timeout(300)
    ckB.check(); pg.wait_for_timeout(300)
    n2 = pg.locator("#riItemsBody tr:not(:has(td[colspan]))").count()
    rzdshow = (pg.text_content("#g80RzdShow") or "").strip()
    supshow = (pg.text_content("#g80SupShow") or "").strip()
    check("②a 勾 2 张→明细汇总", n2 >= 2 and n2 > n0, "明细行 " + str(n0) + "→" + str(n2))
    check("②b 关联租入单带出（共 2 张）", "共 2 张" in rzdshow and rzdshow.count("RZD-") >= 2, rzdshow[:52])
    check("②c 供应商带出（环通）", "环通" in supshow, supshow[:36])
    ckB.uncheck(); pg.wait_for_timeout(300)
    rzdshow2 = (pg.text_content("#g80RzdShow") or "").strip()
    check("②d 取消→回退（共 1 张）", "共 1 张" in rzdshow2)

    # ③ 筛选联动
    pg.select_option("#g80ProjF", value="PRJ-2601")
    pg.wait_for_timeout(600)
    keys = pg.locator("#g80RzdBody .g80Ck").evaluate_all("els=>els.map(e=>e.getAttribute('data-key'))")
    check("③a 项目筛 PRJ-2601→仅 RZD-003", keys == ["RZD-20260815-003"], str(keys))
    pg.select_option("#g80ProjF", value=""); pg.wait_for_timeout(400)

    # ④ 跨供应商拦截（数据单供应商·运行时改 data-sup 模拟）
    pg.evaluate("()=>{document.querySelector('.g80Ck[data-key=\"RZD-20260815-003\"]').setAttribute('data-sup','模拟第二供应商')}")
    pg.locator('.g80Ck[data-key="RZD-20260815-003"]').click(); pg.wait_for_timeout(600)
    toast = pg.text_content("body") or ""
    still = pg.locator('.g80Ck[data-key="RZD-20260815-003"]').is_checked()
    check("④ 跨供应商拦截（toast+复位）", ("只能对应一个供应商" in toast) and (not still),
          "toast=" + str("只能对应一个供应商" in toast) + " 复位=" + str(not still))
    pg.screenshot(path=r"D:\工作台-吕道远\5-A03-汽车物流包装租赁\_scan_tmpdir\g80_ghck_multi.png", full_page=True)

    # ⑤ 超量红字
    ckB2 = pg.locator('.g80Ck[data-key="RZD-20260815-003"]')
    pg.evaluate("()=>{document.querySelector('.g80Ck[data-key=\"RZD-20260815-003\"]').setAttribute('data-sup','环通循环包装运营（上海）有限公司')}")
    ckB2.check(); pg.wait_for_timeout(400)
    q = pg.locator("#riItemsBody .riQty").last
    mx = int(q.get_attribute("data-max"))
    q.fill(str(mx + 2)); pg.wait_for_timeout(400)
    tag = pg.locator(".g80-over")
    check("⑤ 超可归还红字", tag.count() >= 1 and ("超可归还数量" in (tag.first.text_content() or "")))

    # ⑥ GHCK-002 详情两值
    pg.goto("file:///" + DET + "?id=GHCK-20260903-002")
    pg.wait_for_timeout(900)
    db = pg.text_content("body") or ""
    check("⑥ 详情 GHCK-002 关联两张租入单", ("RZD-20260815-005" in db) and ("RZD-20260815-003" in db) and ("分批归还" in db))

    # ⑦ 租入单列表发起归还→新建页（G74 同款修复）
    pg.goto("file:///" + RZDLIST)
    pg.wait_for_timeout(900)
    clicked = False
    for i in range(pg.locator("tbody tr").count()):
        row = pg.locator("tbody tr").nth(i)
        if row.locator("a:has-text('发起归还')").count():
            row.locator("a:has-text('发起归还')").first.click(); clicked = True; break
    pg.wait_for_timeout(800)
    check("⑦ 发起归还→归还出库新建页", clicked and ("归还出库新建.html" in unquote(pg.url)),
          "点击=" + str(clicked) + " → " + (unquote(pg.url).split("/")[-1] if clicked else "—"))
    b.close()

fails = [r for r in results if not r[1]]
print("\nJS 错误:", len(js_errors), (js_errors[:3] if js_errors else ""))
print("总判定: %d PASS / %d FAIL" % (len(results) - len(fails), len(fails)))
sys.exit(1 if fails or js_errors else 0)
