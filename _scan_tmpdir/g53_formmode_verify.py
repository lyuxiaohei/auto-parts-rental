# -*- coding: utf-8 -*-
"""G53 详情向新建版式靠拢 · 样板实测（调拨详情/审核 + 三条记录）
断言：新版式分段（信息/明细/流转）、form-row 行数与字段序、明细表列口径、链与时间线保留、无 JS 错误、旧四段式不残留
"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"

CASES = [
    ("调拨详情·待审核单", r"仓储作业\调拨详情.html?id=DB-20260901-003", ["调拨单号", "状态", "调出库位", "调入库位", "调拨类型", "调拨原因", "调拨日期", "备注", "制单人", "审核人"], 3),
    ("调拨详情·已完成单A", r"仓储作业\调拨详情.html?id=DB-20260826-002", None, 1),
    ("调拨详情·已完成单B", r"仓储作业\调拨详情.html?id=DB-20260812-001", None, 1),
    ("调拨审核·默认单", r"仓储作业\调拨审核.html", None, 3),
    ("调拨详情·默认(无参)", r"仓储作业\调拨详情.html", None, 3),
]

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    allfail = 0
    for name, rel, want_labels, want_rows in CASES:
        page = ctx.new_page()
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        page.goto("file:///" + os.path.join(ROOT, rel).replace("\\", "/"))
        page.wait_for_timeout(600)
        print("=" * 8, name)
        errs = [e for e in errs if "favicon" not in e.lower()]
        print("  JS错误:", "无" if not errs else errs[:3]); allfail += len(errs)
        # 分段
        secs = page.eval_on_selector_all(".dt-sec", "els=>els.map(e=>e.textContent.trim())")
        ok_secs = secs[:3] == ["调拨信息", "调拨明细", "流转信息"]
        print("  分段:", secs, "PASS" if ok_secs else "FAIL"); allfail += 0 if ok_secs else 1
        # form 行
        rows = page.eval_on_selector_all(".fm-row", "els=>els.map(e=>e.querySelector('.form-label').textContent.replace(/：$/,''))")
        if want_labels:
            ok = rows == want_labels
            print("  字段序:", rows, "PASS" if ok else "FAIL"); allfail += 0 if ok else 1
        else:
            print("  字段序:", rows)
        # 值盒样式（只读盒）
        box = page.evaluate("() => { const v=document.querySelector('.fm-val'); if(!v) return null; const s=getComputedStyle(v); return {w:v.getBoundingClientRect().width, bg:s.backgroundColor, h:v.getBoundingClientRect().height}; }")
        print("  值盒:", box)
        # 明细表
        ths = page.eval_on_selector_all(".detailBody table thead th, #detailBody table thead th", "els=>els.map(e=>e.textContent.trim())")
        trs = page.locator("#detailBody table tbody tr").count() if page.locator("#detailBody table tbody tr").count() else page.locator(".detailBody table tbody tr").count()
        ok_tbl = ths[:7] == ["序号", "物料编码", "物料名称", "规格", "单位", "调拨数量", "备注"] and trs == want_rows
        print("  明细列:", ths, "| 行数:", trs, "PASS" if ok_tbl else "FAIL"); allfail += 0 if ok_tbl else 1
        # 链与时间线
        chain = page.locator("#detailBody .chain .node").count()
        tl = page.locator("#detailBody .tl .tl-i").count()
        print("  单据链节点:", chain, "| 时间线:", tl, "PASS" if chain >= 3 and tl >= 2 else "FAIL"); allfail += 0 if (chain >= 3 and tl >= 2) else 1
        # 旧四段式残留
        old = page.locator("#detailBody .dgrid").count()
        print("  旧四段式 dgrid 残留:", old, "PASS" if old == 0 else "FAIL"); allfail += old
        # 截图（仅首例）
        if want_labels:
            page.screenshot(path=r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g53_调拨详情_新版式.png", full_page=True)
        page.close()
    b.close()
    print()
    print("总 FAIL:", allfail)
