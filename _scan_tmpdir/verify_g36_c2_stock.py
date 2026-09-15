# -*- coding: utf-8 -*-
"""G36 验收·第11项 C2 库存查询五项目对平 PW 实测"""
import io, sys, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

BASE = "file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型/仓储作业/库存查询.html"
PROJS = ["PRJ-2601", "PRJ-2602", "PRJ-2603", "PRJ-2604", "PRJ-2605"]

READ_TABLE = """() => {
    let main = null;
    document.querySelectorAll('table').forEach(t => {
        const th = t.querySelector('thead');
        if (th && th.textContent.indexOf('适用项目') > -1 && th.textContent.indexOf('总量') > -1) main = t;
    });
    if (!main) return null;
    return [...main.querySelector('tbody').rows].map(tr => {
        const cells = [...tr.cells].map(c => c.textContent.trim());
        return {key: cells[0], proj: cells[3], nums: cells.slice(4, 9)};
    });
}"""

def tonum(s):
    return int(s.replace(",", "").replace("，", "").strip() or 0)

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto(BASE, wait_until="networkidle")
    page.wait_for_timeout(800)

    # ---- 0) 数据层基线：stockFlows 每行 qtyByProject 各项目分摊列求和 = cells 四态；四态和 = 总量 ----
    data_check = page.evaluate("""() => {
        const sf = window.DEMO_DATA.stockFlows || {};
        const bad = [];
        let nrows = 0;
        Object.keys(sf).forEach(k => {
            const r = sf[k].row || {};
            const q = (r.fields || {}).qtyByProject;
            const cells = r.cells || [];
            if (!q || cells.length < 8) return;
            nrows++;
            const sum = [0,0,0,0];
            Object.keys(q).forEach(P => { for (let i=0;i<4;i++) sum[i]+=q[P][i]; });
            const cellNums = cells.slice(3,8).map(c => { const m = String(c).match(/[\\d,]+/); return m ? parseInt(m[0].replace(/,/g,''),10) : NaN; });
            for (let i=0;i<4;i++) if (sum[i]!==cellNums[i]) bad.push(k+' state'+i+' 分摊和'+sum[i]+'!=cells'+cellNums[i]);
            if (sum[0]+sum[1]+sum[2]+sum[3]!==cellNums[4]) bad.push(k+' 总量不平: '+ (sum[0]+sum[1]+sum[2]+sum[3]) + ' vs ' + cellNums[4]);
        });
        return {nrows, bad};
    }""")
    print("C2-0 数据层基线: stockFlows 有分摊行 =", data_check["nrows"], "| 不平行数 =", len(data_check["bad"]))
    for b in data_check["bad"][:5]: print("   ", b)

    # ---- 1) 页面全量基线（未筛选）----
    base_rows = page.evaluate(READ_TABLE)
    print("C2-1 页面基线行数 =", len(base_rows))
    base = {}
    base_ok = True
    for r in base_rows:
        nums = [tonum(x) for x in r["nums"]]
        base[r["key"]] = nums
        if nums[0]+nums[1]+nums[2]+nums[3] != nums[4]:
            base_ok = False
            print("    基线行四态!=总量:", r["key"], nums)
    print("C2-1 基线每行四态和=总量:", base_ok)

    # ---- 2) 三项目筛选：每行四态和=总量、适用项目列=所选 ----
    proj_sel = page.locator(".ff", has_text="项目：").locator("select").first
    for P in PROJS[:3]:
        proj_sel.select_option(P)
        page.get_by_role("button", name="查询", exact=True).click()
        page.wait_for_timeout(500)
        rows = page.evaluate(READ_TABLE)
        bad_sum, bad_proj = [], []
        for r in rows:
            nums = [tonum(x) for x in r["nums"]]
            if nums[0]+nums[1]+nums[2]+nums[3] != nums[4]:
                bad_sum.append((r["key"], nums))
            if r["proj"] != P:
                bad_proj.append((r["key"], r["proj"]))
        print(f"C2-2 筛选{P}: 行数={len(rows)} 四态和!=总量行数={len(bad_sum)} 适用项目!=所选行数={len(bad_proj)}")
        for b in bad_sum[:3]: print("     sum:", b)
        for b in bad_proj[:3]: print("     proj:", b)

    # ---- 3) 五项目累计逐行对平基线 ----
    acc = {}
    allrow_ok = True
    for P in PROJS:
        proj_sel.select_option(P)
        page.get_by_role("button", name="查询", exact=True).click()
        page.wait_for_timeout(500)
        rows = page.evaluate(READ_TABLE)
        if len(rows) != len(base_rows):
            print(f"    警告: {P} 视图行数 {len(rows)} != 基线 {len(base_rows)}")
            allrow_ok = False
        for r in rows:
            nums = [tonum(x) for x in r["nums"]]
            cur = acc.setdefault(r["key"], [0]*5)
            for i in range(5): cur[i] += nums[i]
    mismatch = []
    for k, bn in base.items():
        an = acc.get(k)
        if an is None:
            mismatch.append((k, "缺行", bn)); continue
        if an != bn:
            mismatch.append((k, an, bn))
    print("C2-3 五项目累计 vs 基线: 基线行数 =", len(base), "| 对上行数 =", len(base)-len(mismatch), "| 不平行数 =", len(mismatch), "| 各视图行数一致:", allrow_ok)
    for m in mismatch[:6]: print("    ", m)

    # 恢复全部
    proj_sel.select_option("全部")
    page.get_by_role("button", name="查询", exact=True).click()
    print("pageerror:", len(errs))
    browser.close()
print("DONE")
