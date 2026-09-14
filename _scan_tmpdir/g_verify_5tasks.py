# -*- coding: utf-8 -*-
"""G-五任务总验证：T1 租入单押金备注上移 / T2 归还明细多行 / T3 标注 / T4 税率字号 / T5 客商开票资料"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path
from playwright.sync_api import sync_playwright

PROTO = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型").resolve()
OUT = PROTO.parent.parent / "_scan_tmpdir"
results = []

def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (" | " + detail if detail else ""))

with sync_playwright() as pw:
    b = pw.chromium.launch()

    def open_modal(pg, mid):
        return pg.evaluate("(m) => { const el = document.getElementById(m); el.classList.add('show'); }", mid)

    def order_note_before(pg, scope_sel, label, det_kw):
        return pg.evaluate("""([scope, label, kw]) => {
          const s = document.querySelector(scope) || document;
          const note = [...s.querySelectorAll('.form-label')].find(l => l.textContent.trim() === label);
          const det = [...s.querySelectorAll('div')].find(d => d.textContent.includes(kw) && (d.getAttribute('style')||'').includes('margin:4px 0 8px'));
          if (!note || !det) return {found: false};
          return {found: true, ok: !!(note.compareDocumentPosition(det) & Node.DOCUMENT_POSITION_FOLLOWING)};
        }""", [scope_sel, label, det_kw])

    # ---- T1 租入单（双层）----
    for label, rel, mid in [("T1 列表页", "租赁管理/租入单列表.html", "createModal"),
                            ("T1 模板页", "租赁管理/弹窗/租入单新建.html", "createModal")]:
        pg = b.new_page(viewport={"width": 1440, "height": 960})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:100]))
        pg.goto((PROTO / rel).as_uri(), wait_until="load"); pg.wait_for_timeout(300)
        open_modal(pg, mid); pg.wait_for_timeout(150)
        r = order_note_before(pg, "#" + mid, "押金（元）", "租入明细（多货品")
        r2 = order_note_before(pg, "#" + mid, "备注", "租入明细（多货品")
        check(label + " 押金在明细上", r.get("found") and r["ok"])
        check(label + " 备注在明细上", r2.get("found") and r2["ok"], "JS错 %d" % len(errs))
        pg.close()

    # ---- T2 租入归还（列表页）----
    pg = b.new_page(viewport={"width": 1440, "height": 960})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:100]))
    pg.goto((PROTO / "租赁管理/租入归还列表.html").as_uri(), wait_until="load"); pg.wait_for_timeout(300)
    open_modal(pg, "createModal"); pg.wait_for_timeout(150)
    r = pg.evaluate("""() => {
      const body = document.getElementById('riItemsBody');
      const modal = document.getElementById('createModal');
      return {行数: body.querySelectorAll('tr').length,
              无遗留物料行: ![...modal.querySelectorAll('.form-label')].some(l => l.textContent.includes('物料')),
              无遗留数量行: ![...modal.querySelectorAll('.form-label')].some(l => l.textContent.includes('归还数量')),
              无pnhint: !modal.querySelector('.pn-hint')};
    }""")
    check("T2 默认租入单明细行数=1（RZD-003 单行）", r["行数"] == 1, str(r["行数"]))
    check("T2 遗留单行已删", r["无遗留物料行"] and r["无遗留数量行"])
    check("T2 pn-hint 已摘", r["无pnhint"])
    # 切换租入单 → 行数随 returnItems
    rows_by_sel = pg.evaluate("""() => {
      const sel = document.getElementById('riSelect');
      const out = [];
      [...sel.options].forEach(o => {
        const k = o.getAttribute('data-key');
        const rec = window.DEMO_DATA.rentInOrders[k];
        out.push({k: k, 期望: rec && rec.returnItems ? rec.returnItems.length : 1});
      });
      return out;
    }""")
    multi_ok = True
    for item in rows_by_sel[:3]:
        pg.evaluate("""(k) => {
          const sel = document.getElementById('riSelect');
          const opt = [...sel.options].find(o => o.getAttribute('data-key') === k);
          sel.value = opt.value; sel.dispatchEvent(new Event('change'));
          document.getElementById('riSelect').onchange && null;
          syncReturnItems(sel);
        }""", item["k"])
        pg.wait_for_timeout(80)
        got = pg.evaluate("document.getElementById('riItemsBody').querySelectorAll('tr').length")
        if got != item["期望"]:
            multi_ok = False
            check("T2 联动 %s" % item["k"], False, "got %d expect %d" % (got, item["期望"]))
    check("T2 切换租入单明细行数联动（前 3 项）", multi_ok)
    r3 = order_note_before(pg, "#createModal", "备注", "归还明细")
    check("T2 备注在归还明细上", r3.get("found") and r3["ok"], "JS错 %d" % len(errs))
    # T3 标注：列表页 ?notes=1 pin3
    pg2 = b.new_page(viewport={"width": 1440, "height": 960})
    pg2.goto((PROTO / "租赁管理/租入归还列表.html").as_uri() + "?notes=1", wait_until="load"); pg2.wait_for_timeout(400)
    n3 = pg2.evaluate("""() => {
      const tb = document.getElementById('riItemsBody');
      const pins = document.querySelectorAll('.proto-pin').length;
      return {tbody有角标: tb && tb.hasAttribute('data-note'), 角标值: tb && tb.getAttribute('data-note'), pin数: pins};
    }""")
    check("T3 列表页 tbody 挂角标(=3)+pin 数 3", n3["tbody有角标"] and n3["角标值"] == "3" and n3["pin数"] == 3, str(n3))
    pg2.close(); pg.close()

    # T3 模板页标注
    pg = b.new_page(viewport={"width": 1440, "height": 960})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:100]))
    pg.goto((PROTO / "租赁管理/弹窗/租入归还新建.html").as_uri() + "?notes=1", wait_until="load"); pg.wait_for_timeout(400)
    n4 = pg.evaluate("""() => {
      const tb = document.getElementById('riItemsBody');
      return {角标: tb && tb.getAttribute('data-note'), fab: !!document.getElementById('protoNotesFab'), pnhint: !!document.querySelector('.pn-hint')};
    }""")
    check("T3 模板页角标=1+fab 在+pn-hint 0", n4["角标"] == "1" and n4["fab"] and not n4["pnhint"], str(n4) + " JS错 %d" % len(errs))
    pg.close()

    # ---- T4 字号 ----
    pg = b.new_page(viewport={"width": 1440, "height": 960})
    pg.goto((PROTO / "基础数据/弹窗/新建产品.html").as_uri(), wait_until="load"); pg.wait_for_timeout(300)
    open_modal(pg, "createModal"); pg.wait_for_timeout(100)
    fs = pg.evaluate("""() => {
      const m = document.getElementById('createModal');
      return {表单: getComputedStyle(m.querySelector('.form-row input')).fontSize,
              税率表头: getComputedStyle(m.querySelector('.tax-edit-hd')).fontSize,
              税率输入: getComputedStyle(m.querySelector('.tax-in, .tax-sel')).fontSize};
    }""")
    check("T4 税率区字号对齐 13px", fs["税率表头"] == "13px" and fs["税率输入"] == "13px" and fs["表单"] == "13px", str(fs))
    pg.close()

    # ---- T5 客商管理 ----
    pg = b.new_page(viewport={"width": 1440, "height": 960})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:100]))
    pg.goto((PROTO / "基础数据/客商管理.html").as_uri(), wait_until="load"); pg.wait_for_timeout(400)
    r5 = pg.evaluate("""() => {
      const cm = document.getElementById('createModal');
      const im = document.getElementById('invoiceInfoModal');
      const noInvInCreate = ![...cm.querySelectorAll('.form-label')].some(l => l.textContent === '开票资料');
      // 点第一行开票资料按钮（编程点击·数据驱动行）
      const a = [...document.querySelectorAll('tbody .ops a')].find(x => x.textContent === '开票资料');
      if (a) a.click();
      const imShown = im.classList.contains('show');
      const hasCycle = [...im.querySelectorAll('.form-label')].some(l => l.textContent.includes('结算周期'));
      const cmShown = document.getElementById('createModal').classList.contains('show');
      return {create无开票行: noInvInCreate, 新弹窗存在: !!im, 点击后开新弹窗: imShown, 编辑弹窗未开: !cmShown, 结算周期在: hasCycle};
    }""")
    check("T5 createModal 已无开票资料行", r5["create无开票行"])
    check("T5 开票资料按钮→独立弹窗（非编辑弹窗）", r5["新弹窗存在"] and r5["点击后开新弹窗"] and r5["编辑弹窗未开"])
    check("T5 开票资料弹窗含结算周期", r5["结算周期在"], "JS错 %d" % len(errs))
    pg.screenshot(path=str(OUT / "g-t5-invoice-modal.png"))
    pg.close()
    # 模板两页
    for label, rel in [("T5 新建客商模板", "基础数据/弹窗/新建客商.html"), ("T5 开票资料模板", "基础数据/弹窗/客商开票资料.html")]:
        pg = b.new_page(viewport={"width": 1440, "height": 960})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:100]))
        pg.goto((PROTO / rel).as_uri(), wait_until="load"); pg.wait_for_timeout(300)
        r = pg.evaluate("""() => {
          const labels = [...document.querySelectorAll('.form-label')].map(l => l.textContent.trim());
          return {开票资料行: labels.includes('开票资料'), 结算周期: labels.some(l => l.includes('结算周期')), 标题: (document.querySelector('.modal-title')||{}).textContent};
        }""")
        if "新建客商" in label:
            check(label + " 无开票资料行", not r["开票资料行"] and not r["结算周期"], "JS错 %d" % len(errs))
        else:
            check(label + " 含发票字段+结算周期", r["标题"] == "开票资料" and r["结算周期"], str(r) + " JS错 %d" % len(errs))
        pg.close()
    b.close()

fails = results.count(False)
print("\n==== 五任务总验证：%d 项，FAIL %d ====" % (len(results), fails))
sys.exit(1 if fails else 0)
