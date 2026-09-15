# -*- coding: utf-8 -*-
"""G36 验收·第10项 C1 三单链路 PW 实测"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

BASE = "file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型/"

def open_detail(page, url, row_key):
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(500)
    tr = page.locator("table tbody tr", has_text=row_key).first
    btn = tr.locator(".ops a", has_text="详情").first
    btn.click()
    page.wait_for_timeout(400)
    mo = page.locator(".modal-overlay.show")
    mo.wait_for(state="visible", timeout=5000)
    return mo.first

with sync_playwright() as pw:
    browser = pw.chromium.launch()

    # --- C1-1 租入单列表 RZD → chain 含 RZRK + CK ---
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    mo = open_detail(page, BASE + "租入管理/租入单列表.html", "RZD-20260902-008")
    chain_txt = mo.locator(".chain").first.inner_text()
    print("C1-1 租入单详情.chain 含 RZRK-20260903-023:", "RZRK-20260903-023" in chain_txt,
          "| 含 CK-20260914-023:", "CK-20260914-023" in chain_txt)
    print("    chain 片段:", " ".join(chain_txt.split())[:220])
    page.close()

    # --- C1-2 租赁出库列表 CK → body 含 RZRK + RZD ---
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    mo = open_detail(page, BASE + "租赁管理/租赁出库列表.html", "CK-20260914-023")
    body_txt = mo.locator(".modal-body").inner_text()
    print("C1-2 出库单详情.body 含 RZRK-20260903-023:", "RZRK-20260903-023" in body_txt,
          "| 含 RZD-20260902-008:", "RZD-20260902-008" in body_txt)
    page.close()

    # --- C1-3 租入入库列表 RZRK → chain 含 RZD + CK ---
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    mo = open_detail(page, BASE + "租入管理/租入入库列表.html", "RZRK-20260903-023")
    chain_txt = mo.locator(".chain").first.inner_text()
    print("C1-3 入库单详情.chain 含 RZD-20260902-008:", "RZD-20260902-008" in chain_txt,
          "| 含 CK-20260914-023:", "CK-20260914-023" in chain_txt)
    print("    chain 片段:", " ".join(chain_txt.split())[:220])

    # --- C1-4 同页 auditModal（入库确认·含「立即转租」标签）checkbox 默认 checked ---
    # 重新加载页面确保弹窗为初始状态
    page.goto(BASE + "租入管理/租入入库列表.html", wait_until="networkidle")
    page.wait_for_timeout(500)
    page.evaluate("openModal('auditModal')")
    page.wait_for_timeout(300)
    mo = page.locator("#auditModal")
    has_label = mo.locator(".form-label", has_text="立即转租").count()
    cb = mo.locator("input[type=checkbox]").first
    checked = cb.evaluate("el => el.checked")
    default_checked = cb.evaluate("el => el.defaultChecked !== undefined ? el.defaultChecked : el.hasAttribute('checked')")
    print("C1-4 auditModal 含「立即转租」label:", has_label > 0,
          "| checkbox.checked:", checked, "| defaultChecked(初始HTML):", default_checked)
    page.close()
    browser.close()
print("DONE")
