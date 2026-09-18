# -*- coding: utf-8 -*-
"""G53 acceptance render check (2): open 8 detail pages via Playwright Chromium
over file:// URLs and assert, per page:
  (a) no pageerror and no console error
  (b) #detailBody > .fm-card count >= 2 and first card .card-title == expected formTitle
  (c) the item card's thead first 3 th texts == expected 3 columns
  (d) a 流转信息 card exists and contains a non-empty .chain or .tl
Read-only wrt repo; writes only JSON inside _scan_tmpdir/g53_accept/.
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"
HERE = ROOT / "_scan_tmpdir" / "g53_accept"

PAGES = [
    # (relpath, id, expected formTitle, expected first-3 item columns)
    ("采购管理/采购订单详情.html", "PO-20260902-018", "订单信息", ["序号", "物料编码", "物料名称"]),
    ("租赁管理/租赁单详情.html", "ZL-20260823-033", "租赁信息", ["序号", "物料编码", "物料名称"]),
    ("租赁管理/转移出库单详情.html", "ZY-20260915-005", "转移信息", ["序号", "物料编码", "物料名称"]),
    ("仓储作业/其他出库详情.html", "QTCK-20260905-005", "出库信息", ["序号", "物料编码", "物料名称"]),
    ("财务协同/收款详情.html", "HK-20260830-014", "收款信息", ["关联账单", "费用项", "本次收款(元)"]),
    ("采购管理/采购入库详情.html", "CGRK-20260828-012", "基本信息", ["序号", "物料编码", "物料名称"]),
    ("租赁管理/租赁出库详情.html", "CK-20260910-022", "基本信息", ["序号", "组合件编码", "组合件名称"]),
    ("财务协同/开票详情.html", "INV-20260902-013", "开票信息", ["费用项", "关联账单", "税率"]),
]

JS_PROBE = r"""
() => {
  const cards = Array.from(document.querySelectorAll('#detailBody > .fm-card'));
  const firstTitle = cards.length ? (cards[0].querySelector('.card-title') || {}).textContent || '' : null;
  // item card = the fm-card that owns a thead
  let itemTh = null, itemTitle = null;
  for (const c of cards) {
    const ths = c.querySelectorAll('table thead th');
    if (ths.length) {
      itemTh = Array.from(ths).slice(0, 5).map(t => t.textContent.trim());
      itemTitle = (c.querySelector('.card-title') || {}).textContent || '';
      break;
    }
  }
  // flow card
  let flow = null;
  for (const c of cards) {
    const t = (c.querySelector('.card-title') || {}).textContent || '';
    if (t.trim() === '流转信息') {
      const chain = Array.from(c.querySelectorAll('.chain')).filter(e => (e.textContent || '').trim());
      const tl = Array.from(c.querySelectorAll('.tl')).filter(e => (e.textContent || '').trim());
      const chainNodes = c.querySelectorAll('.chain .node').length;
      const tlItems = c.querySelectorAll('.tl .tl-i').length;
      flow = { found: true, chainNonEmpty: chain.length > 0, tlNonEmpty: tl.length > 0,
               chainNodes, tlItems };
      break;
    }
  }
  const allTitles = cards.map(c => ((c.querySelector('.card-title') || {}).textContent || '').trim());
  return { cardCount: cards.length, allTitles, firstTitle: (firstTitle || '').trim(),
           itemTitle: (itemTitle || '').trim(), itemTh, flow: flow || { found: false } };
}
"""


def main() -> int:
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page_errors = []
        console_errors = []
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)

        for rel, rid, want_title, want_cols in PAGES:
            page_errors.clear()
            console_errors.clear()
            fpath = (PROTO / rel).resolve()
            url = fpath.as_uri() + "?id=" + rid
            entry = {"page": rel, "id": rid, "url": url}
            try:
                page.goto(url, wait_until="load", timeout=30000)
                page.wait_for_timeout(600)  # let scripts settle
                probe = page.evaluate(JS_PROBE)
                entry["probe"] = probe
                entry["pageErrors"] = list(page_errors)
                entry["consoleErrors"] = list(console_errors)

                ok_a = not page_errors and not console_errors
                ok_b = probe["cardCount"] >= 2 and probe["firstTitle"] == want_title
                got_cols = (probe.get("itemTh") or [])[:3]
                ok_c = got_cols == want_cols
                fl = probe.get("flow") or {}
                ok_d = bool(fl.get("found")) and (bool(fl.get("chainNonEmpty")) or bool(fl.get("tlNonEmpty")))
                entry["checks"] = {
                    "a_noErrors": ok_a,
                    "b_cards_and_firstTitle": ok_b,
                    "c_itemThead3": ok_c,
                    "d_flowCard": ok_d,
                }
                entry["PASS"] = ok_a and ok_b and ok_c and ok_d
            except Exception as exc:  # noqa: BLE001
                entry["exception"] = repr(exc)
                entry["PASS"] = False
            results.append(entry)
        browser.close()

    out = HERE / "check_render.out.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
