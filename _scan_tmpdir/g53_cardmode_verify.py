# -*- coding: utf-8 -*-
"""G53 详情三卡版式实测：信息卡/明细卡/流转卡独立成卡、壳卡透明化、几何与新建页一致"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"

CASES = [
    ("调拨详情·待审核", r"仓储作业\调拨详情.html?id=DB-20260901-003", 3),
    ("调拨详情·已完成A", r"仓储作业\调拨详情.html?id=DB-20260826-002", 1),
    ("调拨审核·默认", r"仓储作业\调拨审核.html", 3),
]

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    allfail = 0
    for name, rel, want_rows in CASES:
        page = ctx.new_page()
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        page.goto("file:///" + os.path.join(ROOT, rel).replace("\\", "/"))
        page.wait_for_timeout(600)
        errs = [e for e in errs if "favicon" not in e.lower()]
        print("=" * 8, name, "| JS错误:", "无" if not errs else errs[:3]); allfail += len(errs)
        # 三张独立卡
        titles = page.eval_on_selector_all("#detailBody > .fm-card > .card-head .card-title", "els=>els.map(e=>e.textContent.trim())")
        ok_t = titles == ["调拨信息", "调拨明细", "流转信息"]
        print("  卡片:", titles, "PASS" if ok_t else "FAIL"); allfail += 0 if ok_t else 1
        # 卡片真实独立（各卡有白底+阴影+圆角，卡间有间距）
        geo = page.evaluate("""() => {
          const cards=[...document.querySelectorAll('#detailBody > .fm-card')];
          const s=getComputedStyle(cards[0]);
          const r1=cards[0].getBoundingClientRect(), r2=cards[1].getBoundingClientRect();
          return {n:cards.length, bg:s.backgroundColor, shadow:s.boxShadow!=='none', radius:s.borderRadius, gap:r2.top-r1.bottom, w1:Math.round(r1.width), w2:Math.round(r2.width), left:Math.round(r1.left)};
        }""")
        ok_g = geo['n'] == 3 and geo['bg'] == 'rgb(255, 255, 255)' and geo['shadow'] and geo['gap'] > 8 and geo['w1'] == geo['w2'] and geo['left'] >= 200
        print("  卡几何:", geo, "PASS" if ok_g else "FAIL"); allfail += 0 if ok_g else 1
        # 壳卡透明化（背景透明、无阴影）
        shell = page.evaluate("""() => { const d=document.getElementById('detailBody'); const c=d.closest('.card'); const s=getComputedStyle(c); return {bg:s.backgroundColor, shadow:s.boxShadow, pad:s.padding}; }""")
        ok_s = shell['bg'] == 'rgba(0, 0, 0, 0)' and shell['shadow'] == 'none'
        print("  壳卡透明化:", shell, "PASS" if ok_s else "FAIL"); allfail += 0 if ok_s else 1
        # 与新建页第一张卡对齐（左缘/宽度）
        pg2 = ctx.new_page(); pg2.goto("file:///" + (ROOT + r"\仓储作业\调拨新建.html").replace("\\", "/")); pg2.wait_for_timeout(400)
        nc = pg2.evaluate("() => { const c=document.querySelector('.content > .card'); const r=c.getBoundingClientRect(); const s=getComputedStyle(c); return {left:Math.round(r.left), w:Math.round(r.width), shadow:s.boxShadow!=='none'}; }")
        pg2.close()
        ok_a = abs(nc['left'] - geo['left']) <= 1 and nc['w'] == geo['w1'] and nc['shadow']
        print("  对齐新建页卡:", nc, "PASS" if ok_a else "FAIL"); allfail += 0 if ok_a else 1
        # 字段/明细/链/时间线仍在
        rows = page.eval_on_selector_all(".fm-row .form-label", "els=>els.map(e=>e.textContent.replace(/：$/,''))")
        trs = page.locator("#detailBody table tbody tr").count()
        chain = page.locator("#detailBody .chain .node").count()
        tl = page.locator("#detailBody .tl .tl-i").count()
        ok_c = len(rows) == 10 and trs == want_rows and chain >= 3 and tl >= 2
        print("  字段", len(rows), "行·明细", trs, "行·链", chain, "·时间线", tl, "PASS" if ok_c else "FAIL"); allfail += 0 if ok_c else 1
        if want_rows == 3:
            page.screenshot(path=r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g53_调拨详情_三卡版式.png", full_page=True)
        page.close()
    b.close()
    print()
    print("总 FAIL:", allfail)
