# -*- coding: utf-8 -*-
"""G57 验收抽验·只读浏览器检查（截图只写 _scan_tmpdir/g57_accept/）"""
import asyncio, json, re
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
OUT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g57_accept")
R = {}

async def newpage(ctx):
    page = await ctx.new_page()
    errs = {"console": [], "pageerror": []}
    page.on("console", lambda m: errs["console"].append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errs["pageerror"].append(str(e)))
    return page, errs

async def uri(rel):
    return (ROOT / rel).as_uri()

async def wait_modals(page):
    return await page.eval_on_selector_all(".modal-overlay.show", "els=>els.map(e=>e.id||'')")

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1560, "height": 940})

        # ---- a. 收发存 ----
        page, errs = await newpage(ctx)
        await page.goto(await uri("仓储作业/收发存.html"))
        await page.wait_for_timeout(900)
        a = {}
        a["title"] = await page.title()
        ths = await page.eval_on_selector_all("table thead th", "els=>els.map(e=>e.innerText.trim())")
        main_tbl = await page.query_selector("table tbody tr")
        # 找含 轨迹 的主表表头（可能有多个表）
        a["first8_of_track_table"] = None
        for tbl in await page.query_selector_all("table"):
            t = await tbl.eval_on_selector("thead", "e=>[...e.querySelectorAll('th')].map(x=>x.innerText.trim())") if await tbl.query_selector("thead") else []
            if any("轨迹" in x for x in t):
                a["first8_of_track_table"] = t[:8]; break
        body_txt = await page.evaluate("document.body.innerText")
        a["note_closed_loop"] = "退租关联闭环后数据完整" in body_txt
        tr1 = page.locator("table tbody tr", has_text="轨迹").first
        await tr1.get_by_text("轨迹", exact=True).click()
        await page.wait_for_timeout(600)
        a["modal_after_track"] = await wait_modals(page)
        await page.screenshot(path=str(OUT / "sfs.png"))
        R["a_收发存"] = {**a, "errors": errs}
        await page.close()

        # ---- b. 退租入库新建 ----
        page, errs = await newpage(ctx)
        await page.goto(await uri("租赁管理/退租入库新建.html"))
        await page.wait_for_timeout(900)
        b = {}
        body_txt = await page.evaluate("document.body.innerText")
        b["step1"] = "第一步·选择退回客户" in body_txt
        b["step2"] = "第二步·选择租赁出库单" in body_txt
        b["note_multi"] = "多次退租从多个出库单分别登记" in body_txt
        b["note_noedit"] = "退租只新增不改原单" in body_txt
        rows_sel = page.locator("table tbody tr", has_text="选择")
        b["outorder_rows_with_select"] = await rows_sel.count()
        await rows_sel.first.get_by_text("选择", exact=True).click()
        await page.wait_for_timeout(800)
        # 退回明细区
        det_rows = -1
        for tbl in await page.query_selector_all("table"):
            cap = await tbl.evaluate("e=>e.closest('div,section')?.innerText?.slice(0,200)||''")
            if "退回明细" in (await tbl.evaluate("e=>e.innerText")) or "退回明细" in cap:
                det_rows = await tbl.eval_on_selector_all("tbody tr", "els=>els.filter(e=>e.innerText.trim()).length")
                if det_rows: break
        b["detail_rows_after_select"] = det_rows
        await page.screenshot(path=str(OUT / "tz.png"))
        R["b_退租登记"] = {**b, "errors": errs}
        await page.close()

        # ---- c. 销售出库新建 ----
        page, errs = await newpage(ctx)
        await page.goto(await uri("销售管理/销售出库新建.html"))
        await page.wait_for_timeout(900)
        c = {}
        body_txt = await page.evaluate("document.body.innerText")
        c["over_label_200"] = bool(re.search(r"超订单数量\s*200", body_txt))
        row = page.locator("table tbody tr", has_text="超订单数量").first
        inp = row.locator("input[type=number], input.qty, input").first
        c["qty_border"] = await inp.evaluate("e=>getComputedStyle(e).borderColor") if await inp.count() else None
        c["qty_class"] = await inp.get_attribute("class") if await inp.count() else None
        await page.get_by_text("提交审核", exact=True).first.click()
        await page.wait_for_timeout(700)
        toast = await page.evaluate("()=>{const t=document.querySelector('.toast,.toast-msg,#toast');if(t)return t.innerText;const m=document.body.innerText.split(String.fromCharCode(10)).filter(l=>l.includes('存在超量行'));return m.length?m[0]:''}")
        c["toast"] = toast
        await page.screenshot(path=str(OUT / "over.png"))
        R["c_销售超量"] = {**c, "errors": errs}
        await page.close()

        # ---- d. 客商管理 ----
        page, errs = await newpage(ctx)
        await page.goto(await uri("基础数据/客商管理.html"))
        await page.wait_for_timeout(900)
        d = {}
        ths = await page.eval_on_selector_all("table thead th", "els=>els.map(e=>e.innerText.trim())")
        d["has_col"] = "供应商类型" in ths
        dw = page.locator("table tbody tr", has_text="DW-0201").first
        cells = [c.strip() for c in await dw.locator("td").all_text_contents()]
        idx = ths.index("供应商类型") if "供应商类型" in ths else -1
        d["dw0201_type"] = cells[idx] if 0 <= idx < len(cells) else None
        d["filter_select_present"] = await page.evaluate("""()=>{
          for (const s of document.querySelectorAll('select')) {
            const lbl = s.closest('label,div,li,span');
            if ((lbl?.innerText||'').includes('供应商类型')) return true;
            if ([...s.options].some(o=>o.innerText.includes('租赁供应商'))) return true;
          }
          return document.body.innerText.includes('供应商类型');
        }""")
        await page.screenshot(path=str(OUT / "ks.png"))
        R["d_客商"] = {**d, "errors": errs}
        await page.close()

        # ---- e. 采购入库列表 ----
        page, errs = await newpage(ctx)
        await page.goto(await uri("采购管理/采购入库列表.html"))
        await page.wait_for_timeout(900)
        e = {}
        e["btn_import"] = await page.get_by_text("批量导入", exact=True).count()
        e["btn_export"] = await page.get_by_text("导出", exact=True).count()
        await page.get_by_text("批量导入", exact=True).first.click()
        await page.wait_for_timeout(600)
        e["modal_open"] = await wait_modals(page)
        # 弹窗内点确定
        clicked = False
        for ov in await page.query_selector_all(".modal-overlay.show"):
            btn = await ov.query_selector("text=确定")
            if btn:
                await btn.click(); clicked = True; break
        await page.wait_for_timeout(700)
        toast = await page.evaluate("()=>{const t=document.querySelector('.toast,.toast-msg,#toast');return t?t.innerText:''}")
        e["confirm_clicked"] = clicked
        e["toast"] = toast
        await page.screenshot(path=str(OUT / "imp.png"))
        R["e_采购入库"] = {**e, "errors": errs}
        await page.close()

        # ---- f. 库存查询 ----
        page, errs = await newpage(ctx)
        await page.goto(await uri("仓储作业/库存查询.html"))
        await page.wait_for_timeout(900)
        f = {}
        await page.locator("table tbody tr", has_text="客户在租").first.get_by_text("客户在租", exact=True).click()
        await page.wait_for_timeout(600)
        shown = await page.query_selector_all(".modal-overlay.show")
        f["cust_modal_open"] = len(shown)
        f["cust_filter_select"] = False
        for ov in shown:
            has_sel = await ov.eval_on_selector_all("select", "els=>els.length")
            txt = await ov.evaluate("e=>e.innerText")
            f["cust_filter_select"] = bool(has_sel) and ("客户" in txt)
            f["cust_modal_text_head"] = txt[:120]
        await page.screenshot(path=str(OUT / "kccx_cust.png"))
        # 关掉弹窗再开库位明细
        await page.keyboard.press("Escape")
        await page.evaluate("()=>document.querySelectorAll('.modal-overlay.show').forEach(m=>m.remove())")
        lj = page.locator("table tbody tr", has_text=re.compile("LJ")).first
        await lj.get_by_text("库位明细", exact=True).click()
        await page.wait_for_timeout(600)
        shown2 = await page.query_selector_all(".modal-overlay.show")
        f["loc_modal_open"] = len(shown2)
        f["loc_modal_has_code"] = False; f["loc_modal_head"] = ""
        for ov in shown2:
            txt = await ov.evaluate("e=>e.innerText")
            f["loc_modal_head"] = txt[:200]
            f["loc_modal_has_code"] = "库位编码" in txt or bool(re.search(r"[A-Z]{2,3}-\d+", txt))
        await page.screenshot(path=str(OUT / "kccx.png"))
        R["f_库存查询"] = {**f, "errors": errs}
        await page.close()

        await browser.close()
    print(json.dumps(R, ensure_ascii=False, indent=1))

asyncio.run(main())
