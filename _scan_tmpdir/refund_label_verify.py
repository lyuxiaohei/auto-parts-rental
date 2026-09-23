# -*- coding: utf-8 -*-
"""退款菜单小节标题渲染验证：三类页（根级/子目录/退款登记本体）·样式与应付一致·零JS错误"""
import io, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = (Path(__file__).resolve().parents[1] / "P3-R01-包装租赁管理后台原型")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
results = []

def ck(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(detail) if detail else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))

    for page_path, tag in [("我的待办.html", "root"), ("财务协同/付款登记.html", "sub"),
                           ("财务协同/退款登记.html", "self")]:
        pg.goto((ROOT / page_path).as_uri())
        pg.wait_for_load_state("networkidle")
        st = pg.evaluate("""() => {
          const items = [...document.querySelectorAll('.sm-sub li')];
          const lbl = items.find(li => li.textContent.trim() === '退款' && li.style.padding);
          const yf  = items.find(li => li.textContent.trim() === '应付' && li.style.padding);
          const reg = items.find(li => li.querySelector('.sm-link') &&
                li.querySelector('.sm-link').textContent.trim() === '退款登记');
          if (!lbl || !yf || !reg) return {ok: false, has: [!!lbl, !!yf, !!reg]};
          const cl = getComputedStyle(lbl), cy = getComputedStyle(yf);
          const idx = items.indexOf(lbl), idxReg = items.indexOf(reg), idxYf = items.indexOf(yf);
          return {ok: true, order: [idxYf, idx, idxReg],
                  sameStyle: cl.fontSize === cy.fontSize && cl.color === cy.color
                             && cl.letterSpacing === cy.letterSpacing,
                  txt: lbl.textContent.trim(), fs: cl.fontSize, color: cl.color,
                  sel: reg.querySelector('.sm-link').classList.contains('selected')};
        }""")
        ck("[%s] 「退款」标签存在·样式与「应付」一致" % tag, st.get("ok") and st.get("sameStyle"),
           "字号=%s 色=%s" % (st.get("fs"), st.get("color")) if st.get("ok") else st)
        ck("[%s] 顺序：…应付→应付账单→付款登记→退款→退款登记（标签紧邻菜单项）" % tag,
           st.get("ok") and st["order"][1] == st["order"][2] - 1 and st["order"][1] > st["order"][0],
           st.get("order"))
        if tag == "self":
            ck("[self] 退款登记自身页 selected 态保留", st.get("sel"))
        if tag == "sub":
            pg.screenshot(path=str(Path(__file__).resolve().parent / "refund_label.png"))

    ck("全程零 JS 错误", len(errs) == 0, errs[:3])
    b.close()

print("==== %d/%d PASS ====" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
