# -*- coding: utf-8 -*-
"""采购入库录单附件列表改造验证：卡片结构/保留字段/上传/删除/详情页数据行同步/零JS错误"""
import io, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = (Path(__file__).resolve().parents[1] / "P3-R01-包装租赁管理后台原型")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
TMP = Path(__file__).resolve().parent
results = []

def ck(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(detail) if detail else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))

    # ---- 录单页 ----
    pg.goto((ROOT / "采购管理" / "采购入库录单.html").as_uri())
    pg.wait_for_load_state("networkidle")

    cards = pg.evaluate("""() => [...document.querySelectorAll('.main .card-title, .card-title')]
      .filter(t => t.closest('.card')).map(t => t.textContent.trim())""")
    ck("卡片序列含「附件」且在「随附信息」后", "随附信息" in cards and "附件" in cards
       and cards.index("附件") > cards.index("随附信息"), cards)

    ck("随货单据勾选已移除", pg.locator("text=随货单据").count() == 0)
    ck("质检要求 radio 保留（3 项）", pg.locator(".card:has(.card-title:text('随附信息')) .radio").count() == 3)
    ck("备注 textarea 保留", pg.locator(".card:has(.card-title:text('随附信息')) textarea").count() == 1)

    att = pg.locator(".card:has(.card-title:text('附件'))")
    ck("附件卡演示 2 行（送货单/质检报告）", att.locator("#attList tr").count() == 2)
    ths = att.locator("thead th").all_inner_texts()
    ck("附件表列头=销售订单同款", ths == ["文件名", "大小", "上传人", "上传时间", "操作"], ths)
    hint = att.locator(".pn-hint").inner_text()
    ck("提示行同款文案", "演示上传" in hint and "不真实传输" in hint, hint)

    # 上传按钮 → 真实文件选择器触发
    with pg.expect_file_chooser() as fc:
        att.locator("button:has-text('上传')").click()
    ck("上传按钮触发文件选择器", fc.value.is_multiple())

    # 真实模拟选文件 → 追加行
    (TMP / "测试送货单.xlsx").write_bytes(b"x" * 2048)
    pg.set_input_files("#attFilePick", str(TMP / "测试送货单.xlsx"))
    pg.wait_for_timeout(200)
    rows = att.locator("#attList tr")
    ck("选择文件后追加 1 行（图标📊·2 KB·当前用户）",
       rows.count() == 3 and "测试送货单.xlsx" in rows.nth(2).inner_text()
       and "📊" in rows.nth(2).inner_text() and "2 KB" in rows.nth(2).inner_text()
       and "当前用户" in rows.nth(2).inner_text(), rows.nth(2).inner_text().replace("\n", " · "))

    # 删除：删掉第 1 行
    rows.nth(0).locator("a:has-text('删除')").click()
    pg.wait_for_timeout(100)
    ck("删除行生效（3→2）", att.locator("#attList tr").count() == 2)
    pg.screenshot(path=str(TMP / "cg_attach_after.png"), full_page=False)

    # ---- 详情页数据行同步 ----
    pg.goto((ROOT / "采购管理" / "采购入库详情.html").as_uri() + "?id=CGRK-20260828-012")
    pg.wait_for_load_state("networkidle")
    body_txt = pg.locator("body").inner_text()
    ck("详情页含「附件」行+文件名", "附件" in body_txt and "送货单-吴越联合-20260828.pdf" in body_txt
       and "质检报告-QC-20260828.pdf" in body_txt)
    ck("详情页「随货单据」行已退场", "随货单据" not in body_txt)
    ck("详情页质检要求/备注保留", "质检要求" in body_txt and "备注" in body_txt)

    # 抽第二张记录确认 8 条同步
    pg.goto((ROOT / "采购管理" / "采购入库详情.html").as_uri() + "?id=CGRK-20260827-010")
    pg.wait_for_load_state("networkidle")
    t2 = pg.locator("body").inner_text()
    ck("第二张抽验（CGRK-20260827-010）同步", "附件" in t2 and "随货单据" not in t2)

    ck("全程零 JS 错误", len(errs) == 0, errs[:3])
    b.close()

print("==== %d/%d PASS ====" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
