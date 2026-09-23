# -*- coding: utf-8 -*-
"""订单执行数量字段渲染验证：采购累计入库/销售签收·详情+审核四页·退货差异·零JS错误"""
import io, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = (Path(__file__).resolve().parents[1] / "P3-R01-包装租赁管理后台原型")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
results = []

def ck(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(detail) if detail else ""))

def rows_text(pg):
    return pg.evaluate("""() => [...document.querySelectorAll('.fm-row')]
      .map(r => (r.querySelector('.form-label')||{}).textContent + (r.querySelector('.fm-val')||{}).textContent)""")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))

    # 1. PO-018 详情：六行勾稽全可见（原 info2 死数据复活）
    pg.goto((ROOT / "采购管理" / "采购订单详情.html").as_uri() + "?id=PO-20260902-018")
    pg.wait_for_load_state("networkidle")
    t = "\n".join(rows_text(pg))
    for lab, frag in [("订购数量", "锁扣 5,000 / 铰链 2,500"),
                      ("累计入库数量", "锁扣 2,400 / 铰链 2,000"),
                      ("待验收", "锁扣 800"),
                      ("采购退货", "CGTH-20260914-001"),
                      ("在途未到", "锁扣 1,800"),
                      ("勾稽对平", "5,000 ✓")]:
        ck("PO-018 详情含「%s」(%s)" % (lab, frag[:14]), lab + "：" in t and frag in t)

    # 2. PO-017 简单配对
    pg.goto((ROOT / "采购管理" / "采购订单详情.html").as_uri() + "?id=PO-20260901-017")
    pg.wait_for_load_state("networkidle")
    t = "\n".join(rows_text(pg))
    ck("PO-017 配对行（订购300/累计入库300）", "订购数量：围板箱 300" in t and "累计入库数量：围板箱 300（CGRK-20260828-011" in t)

    # 3. PO-013 退货修正
    pg.goto((ROOT / "采购管理" / "采购订单详情.html").as_uri() + "?id=PO-20260820-013")
    pg.wait_for_load_state("networkidle")
    t = "\n".join(rows_text(pg))
    ck("PO-013 退货行含 CGTH-003 净留存360", "采购退货：木托盘 40（CGTH-20260910-003" in t and "净留存 360" in t)
    ck("PO-013 不再显示「采购退货→无」", "采购退货：无" not in t)

    # 4. PO-015 未到货 0
    pg.goto((ROOT / "采购管理" / "采购订单审核.html").as_uri() + "?id=PO-20260828-015")
    pg.wait_for_load_state("networkidle")
    t = "\n".join(rows_text(pg))
    ck("PO-015 审核页也带（累计入库0·未到货）", "累计入库数量：0（尚未到货" in t)

    # 5. SO-0043 拒收差异
    pg.goto((ROOT / "销售管理" / "销售订单详情.html").as_uri() + "?id=SO-20260830-0043")
    pg.wait_for_load_state("networkidle")
    t = "\n".join(rows_text(pg))
    ck("SO-0043 签收1300（拒收200·已退款）", "签收数量：箱盖 1,300" in t and "XSTH-20260913-001 已退款" in t)

    # 6. SO-0039 分批全签
    pg.goto((ROOT / "销售管理" / "销售订单审核.html").as_uri() + "?id=SO-20260827-0039")
    pg.wait_for_load_state("networkidle")
    t = "\n".join(rows_text(pg))
    ck("SO-0039 审核页签收2500（两批）", "签收数量：箱盖 2,500" in t and "XSCK-20260910-016" in t)

    # 7. SO-0047 在途 0
    pg.goto((ROOT / "销售管理" / "销售订单详情.html").as_uri() + "?id=SO-20260903-0047")
    pg.wait_for_load_state("networkidle")
    t = "\n".join(rows_text(pg))
    ck("SO-0047 签收0（采购在途）", "签收数量：0（先采后销" in t)

    pg.screenshot(path=str(Path(__file__).resolve().parent / "order_qty_po18.png"))
    ck("全程零 JS 错误", len(errs) == 0, errs[:3])
    b.close()

print("==== %d/%d PASS ====" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
