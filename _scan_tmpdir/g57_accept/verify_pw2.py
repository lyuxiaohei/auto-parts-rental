# -*- coding: utf-8 -*-
"""G57 验收·二次精查（a表头/b两步与明细/c红框/e toast）"""
import asyncio, json
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

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1560, "height": 940})

        # a. 收发存 主表头前8列
        page, errs = await newpage(ctx)
        await page.goto((ROOT / "仓储作业/收发存.html").as_uri())
        await page.wait_for_timeout(900)
        R["a_th8"] = await page.eval_on_selector_all(".sfs-tbl thead th", "els=>els.map(e=>e.innerText.trim())")
        R["a_errors"] = errs
        await page.close()

        # b. 退租入库新建 两步卡 + 选择后退回明细行数
        page, errs = await newpage(ctx)
        await page.goto((ROOT / "租赁管理/退租入库新建.html").as_uri())
        await page.wait_for_timeout(900)
        txt = await page.evaluate("document.body.innerText")
        R["b_step1"] = "第一步 · 选择退回客户" in txt
        R["b_step2"] = "第二步 · 选择租赁出库单" in txt
        R["b_step1_card"] = await page.locator(".step-card, [class*=step]", has_text="选择退回客户").count()
        rows = page.locator("table tbody tr", has_text="选择")
        R["b_outorder_rows"] = await rows.count()
        await rows.first.get_by_text("选择", exact=True).click()
        await page.wait_for_timeout(900)
        # 退回明细：找包含「退回明细」标题的区块后的表格行
        R["b_detail_rows"] = await page.evaluate("""()=>{
          const heads=[...document.querySelectorAll('h1,h2,h3,h4,h5,div,span,b,strong')].filter(e=>e.children.length===0&&e.innerText.trim().includes('退回明细'));
          for(const h of heads){ let n=h; for(let i=0;i<6&&n;i++){ n=n.nextElementSibling||n.parentElement; const tb=n&&n.querySelector?n.querySelector('table tbody'):null; if(tb&&tb.innerText.trim()) return tb.querySelectorAll('tr').length; } }
          const tb=[...document.querySelectorAll('table tbody')].filter(t=>t.closest('.modal-overlay')===null&&t.innerText.includes('退回明细')||t.closest('div')&&t.closest('div').innerText.slice(0,60).includes('退回明细'));
          return -1;
        }""")
        # 简化兜底：列出所有 tbody 的前 40 字与行数
        R["b_tbody_dump"] = await page.evaluate("()=>[...document.querySelectorAll('table tbody')].map(t=>({head:(t.closest('div')?.querySelector('h3,h4,b,strong')?.innerText||t.innerText.slice(0,24)).slice(0,30),rows:t.querySelectorAll('tr').length}))")
        await page.screenshot(path=str(OUT / "tz.png"))
        R["b_errors"] = errs
        await page.close()

        # c. 超量行数量框红框
        page, errs = await newpage(ctx)
        await page.goto((ROOT / "销售管理/销售出库新建.html").as_uri())
        await page.wait_for_timeout(1200)
        R["c_qty_border"] = await page.evaluate("""()=>{
          const tr=[...document.querySelectorAll('.edit-tbl tbody tr')].find(t=>t.innerText.includes('超订单数量'));
          if(!tr) return {found:false};
          const qi=tr.querySelector('input[data-tax="qty"]');
          return {found:true, border:qi?getComputedStyle(qi).borderColor:null, value:qi?qi.value:null, label:tr.innerText.match(/超订单数量[^\\s,，]*/)[0]};
        }""")
        R["c_errors"] = errs
        await page.close()

        # e. 采购入库列表 批量导入→确定→toast(#g57Toast)
        page, errs = await newpage(ctx)
        await page.goto((ROOT / "采购管理/采购入库列表.html").as_uri())
        await page.wait_for_timeout(900)
        await page.get_by_text("批量导入", exact=True).first.click()
        await page.wait_for_timeout(500)
        R["e_modal"] = await page.eval_on_selector_all(".modal-overlay.show", "els=>els.map(e=>e.querySelector('.modal-title')?.innerText||e.id)")
        await page.evaluate("g57ImportOk()")
        toast_seen = None
        for _ in range(20):
            t = await page.evaluate("()=>{const t=document.getElementById('g57Toast');return t&&t.style.display!=='none'?t.innerText:null}")
            if t: toast_seen = t; break
            await page.wait_for_timeout(100)
        R["e_toast"] = toast_seen
        await page.screenshot(path=str(OUT / "imp.png"))
        R["e_errors"] = errs
        await page.close()

        await browser.close()
    print(json.dumps(R, ensure_ascii=False, indent=1))

asyncio.run(main())
