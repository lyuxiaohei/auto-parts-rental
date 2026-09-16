# -*- coding: utf-8 -*-
"""G42 独立验收 · 渲染抽验（只读）"""
import pathlib, sys
from playwright.sync_api import sync_playwright

P = pathlib.Path("/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型")
cases = [
    ("客商详情", "基础数据/客商详情.html?id=DW-0001",
     ["开票资料", "纳税人识别号", "91131015MA1FA00014"]),
    ("退款登记", "财务协同/退款登记.html",
     ["采购退货退款（供应商·我方收款）", "预收退回", "多付退回", "销售退货退款（客户·我方付款）"]),
    ("损益报表", "财务协同/损益报表.html",
     ["AR-2026-08-PRJ2601"]),
]
results = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    for name, rel, tokens in cases:
        errors.clear()
        f = P / rel.split("?")[0]
        url = f.resolve().as_uri() + ("?" + rel.split("?")[1] if "?" in rel else "")
        try:
            page.goto(url, wait_until="networkidle", timeout=15000)
        except Exception as e:
            try:
                page.goto(url, wait_until="load", timeout=15000)
            except Exception as e2:
                results.append((name, f"GOTO_FAIL {e2}", 0)); continue
        page.wait_for_timeout(600)
        body = page.inner_text("body")
        missing = [t for t in tokens if t not in body]
        status = "PASS" if not missing and not errors else "FAIL"
        results.append((name, status, len(errors), missing, errors[:3], url))
        # 携带 AR/AP 单号上下文行取证
        if name == "损益报表":
            for ln in body.splitlines():
                if "AR-2026-08-PRJ2601" in ln:
                    print("  损益行取证:", ln.strip()[:120]); break
    browser.close()

for r in results:
    print(r)
