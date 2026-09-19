# -*- coding: utf-8 -*-
# G54 验收 e/f 补充：div 型 radio + 退租入库详情
import pathlib
from playwright.sync_api import sync_playwright

P3 = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
OUT = []
def log(s): OUT.append(s); print(s, flush=True)

def open_page(ctx, rel, query=""):
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto((P3 / rel).as_uri() + query, wait_until="domcontentloaded")
    try:
        page.wait_for_selector("tbody tr", timeout=8000)
    except Exception:
        page.wait_for_timeout(500)
    page.wait_for_timeout(300)
    return page, errors

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context()

    # e. 租入单新建（div 型 radio）
    page, errs = open_page(ctx, r"租入管理\租入单新建.html")
    state = page.evaluate("""()=>{
      const g=id=>{const e=document.getElementById(id);return e?{txt:e.innerText.trim(),checked:e.classList.contains('checked')}:null};
      return {self:g('riTypeSelf'), direct:g('riTypeDirect'),
              hintHidden: document.getElementById('riDirectHint')? getComputedStyle(document.getElementById('riDirectHint')).display==='none':null};
    }""")
    page.locator("#riTypeDirect").click()
    page.wait_for_timeout(300)
    after = page.evaluate("""()=>{
      const h=document.getElementById('riDirectHint');
      return {hintVisible: h && getComputedStyle(h).display!=='none', hintTxt: h?h.innerText.trim():'',
              directChecked: document.getElementById('riTypeDirect').classList.contains('checked'),
              selfChecked: document.getElementById('riTypeSelf').classList.contains('checked')};
    }""")
    log(f"[e] 租入单新建: 默认态={state}; 点击直发单后={after}; 提示含直发虚拟仓={'直发虚拟仓' in after['hintTxt']}; pageerror={len(errs)} {errs[:1]}")
    page.close()

    # f. 退租入库详情?id=TZRK-20260903-009
    page, errs = open_page(ctx, r"租赁管理\退租入库详情.html", "?id=TZRK-20260903-009")
    body = page.locator("body").inner_text()
    has_xnc = "XNC-ZF" in body
    has_zf = "直发虚拟仓" in body
    idx = body.find("入库库位")
    seg = body[idx:idx+80].replace("\n", "|") if idx >= 0 else "(未找到)"
    flat = body.replace(" ", "").replace("\n", "")
    node = "系统识别原租入单RZD-20260815-003为直发类型"
    has_node = node in flat
    log(f"[f] 退租入库详情: 入库库位段='{seg}'; 含XNC-ZF={has_xnc}; 含直发虚拟仓={has_zf}; timeline识别节点={has_node}; pageerror={len(errs)} {errs[:1]}")
    page.close()

    # a 补充：XNC-ZF 行内 2 个可点元素到底是什么（确认非编辑/停用）
    page, errs = open_page(ctx, r"基础数据\库位档案.html")
    detail = page.evaluate("""()=>{
      const tr=[...document.querySelectorAll('tbody tr')].find(t=>t.innerText.includes('XNC-ZF'));
      if(!tr) return null;
      const els=[...tr.querySelectorAll('a,button,[class*=op],[onclick]')].map(e=>({tag:e.tagName,cls:e.className,txt:(e.innerText||'').trim()}));
      return {rowTxt: tr.innerText.replace(/\\n+/g,'|'), els};
    }""")
    log(f"[a补充] XNC-ZF行详情: rowTxt='{detail['rowTxt']}'; 可点元素={detail['els']}")
    page.close()

    browser.close()

with open(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g54_accept\accept_render_ef.out", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
