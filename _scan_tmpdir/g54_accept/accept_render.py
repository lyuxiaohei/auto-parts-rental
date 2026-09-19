# -*- coding: utf-8 -*-
# G54 独立验收 ② 六页 Playwright 渲染检查（只读，file:// 直开）
import sys, json, pathlib
from playwright.sync_api import sync_playwright

P3 = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
OUT = []

def log(s): OUT.append(s); print(s, flush=True)

def open_page(ctx, rel, query=""):
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    url = (P3 / rel).as_uri() + query
    page.goto(url, wait_until="domcontentloaded")
    try:
        page.wait_for_selector("tbody tr", timeout=8000)
    except Exception:
        page.wait_for_timeout(500)
    page.wait_for_timeout(300)
    return page, errors

def row_select_options(page, label):
    """返回页面中包含 label 文本的行内所有 select 的 option 文本列表"""
    return page.evaluate("""(label)=>{
      const sels=[...document.querySelectorAll('select')];
      const out=[];
      for(const s of sels){
        let n=s, row=null;
        while(n && n!==document.body){
          const t=(n.innerText||'')+(n.previousElementSibling?(n.previousElementSibling.innerText||''):'');
          if(t && t.replace(/\\s+/g,'').includes(label)){ row=n; break; }
          n=n.parentElement;
        }
        if(!row){
          n=s;
          while(n && n!==document.body){
            const t=(n.innerText||'');
            if(t && t.replace(/\\s+/g,'').includes(label)){ row=n; break; }
            n=n.parentElement;
          }
        }
        if(row) out.push([...s.options].map(o=>o.textContent.trim()));
      }
      return out;
    }""", label)

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context()

    # a. 库位档案
    page, errs = open_page(ctx, r"基础数据\库位档案.html")
    rows = page.locator("tbody tr").count()
    zrow = page.locator("tbody tr", has_text="XNC-ZF")
    zcount = zrow.count()
    ztext = zrow.first.inner_text().replace("\n", "|") if zcount else ""
    zbtns = zrow.first.locator("a,button,.op-btn,[class*=op]").count() if zcount else -1
    has_sys = "系统内置" in ztext
    has_edit_stop = ("编辑" in ztext) or ("停用" in ztext)
    filt = page.eval_on_selector_all("#locTypeFilterSel", "els=>els.map(e=>[...e.options].map(o=>o.textContent.trim()))")
    log(f"[a] 库位档案: tbody行={rows} (期望11); XNC-ZF行数={zcount}; 行文含系统内置={has_sys}; 行文含编辑/停用={has_edit_stop}; 行内可点元素={zbtns}; #locTypeFilterSel options={filt}; pageerror={len(errs)} {errs[:1]}")
    page.close()

    # b. 库位新建
    page, errs = open_page(ctx, r"基础数据\库位新建.html")
    allopts = page.evaluate("()=>[...document.querySelectorAll('select')].map(s=>({id:s.id,name:s.name,opts:[...s.options].map(o=>o.textContent.trim())}))")
    hit = [s for s in allopts if any("虚拟仓" in o for o in s["opts"])]
    log(f"[b] 库位新建: 含『虚拟仓』选项的select={[(h['id'] or h['name'], [o for o in h['opts'] if '虚拟仓' in o]) for h in hit]}; pageerror={len(errs)} {errs[:1]}")
    page.close()

    # c1. 盘点录入（盘点库房）
    page, errs = open_page(ctx, r"仓储作业\盘点录入.html")
    pd = row_select_options(page, "盘点库房")
    flat = [o for lst in pd for o in lst]
    bad = [o for o in flat if ("虚拟仓" in o)]
    need = [k for k in ["原料区 RA", "成品区 RB", "次品区 RC"] if any(k in o for o in flat)]
    log(f"[c1] 盘点录入·盘点库房: 命中select数={len(pd)}; options={flat}; 含虚拟仓={bad}; 含RA/RB/RC={len(need)}/3 {need}; pageerror={len(errs)} {errs[:1]}")
    page.close()

    # c2. 调拨新建（调出库位/调入库位）
    page, errs = open_page(ctx, r"仓储作业\调拨新建.html")
    out_all = {}
    for lab in ["调出库位", "调入库位"]:
        pd = row_select_options(page, lab)
        flat = [o for lst in pd for o in lst]
        bad = [o for o in flat if ("虚拟仓" in o)]
        need = [k for k in ["原料区 RA", "成品区 RB", "次品区 RC"] if any(k in o for o in flat)]
        out_all[lab] = (len(pd), bad, need, flat)
    log(f"[c2] 调拨新建·调出库位: select数={out_all['调出库位'][0]} 含虚拟仓={out_all['调出库位'][1]} RA/RB/RC={len(out_all['调出库位'][2])}/3 opts={out_all['调出库位'][3]}")
    log(f"[c2] 调拨新建·调入库位: select数={out_all['调入库位'][0]} 含虚拟仓={out_all['调入库位'][1]} RA/RB/RC={len(out_all['调入库位'][2])}/3 opts={out_all['调入库位'][3]}")
    log(f"[c2] pageerror={len(errs)} {errs[:1]}")
    page.close()

    # d. 租入单列表
    page, errs = open_page(ctx, r"租入管理\租入单列表.html")
    info = page.evaluate("""()=>{
      const trs=[...document.querySelectorAll('tbody tr')];
      const types=trs.map(tr=>{const tds=tr.querySelectorAll(':scope > td'); return tds.length? tds[2].innerText.trim():'(rowspan)'});
      return {n:trs.length, types};
    }""")
    t = info["types"]
    log(f"[d] 租入单列表: tbody行={info['n']} (期望7); 第3列取值={t}; 直发={t.count('直发')} 自发={t.count('自发')}; pageerror={len(errs)} {errs[:1]}")
    page.close()

    # e. 租入单新建
    page, errs = open_page(ctx, r"租入管理\租入单新建.html")
    radios = page.locator("input[type=radio]")
    rn = radios.count()
    labels = page.evaluate("""()=>[...document.querySelectorAll('input[type=radio]')].map(r=>{
      let lb=r.closest('label'); let tx=lb?lb.innerText:'';
      if(!tx){const sib=r.nextElementSibling; tx=sib?sib.innerText:'';}
      return {val:r.value, checked:r.checked, tx:tx.trim()};
    })""")
    zf_checked = [l for l in labels if "直发" in (l["tx"] + l["val"]) and l["checked"]]
    zf_default = [l for l in labels if "自发" in (l["tx"] + l["val"]) and l["checked"]]
    # 点击 直发单
    target = page.locator("label", has_text="直发单").first
    clicked = "no-label"
    if target.count():
        target.click(); clicked = "label"
    else:
        r = page.locator("input[type=radio]").nth(0)
        r.click(); clicked = "radio0"
    page.wait_for_timeout(300)
    body = page.locator("body").inner_text()
    hint_ok = "直发虚拟仓" in body
    log(f"[e] 租入单新建: radio数={rn}; radios={labels}; 默认自发选中={bool(zf_default)}; 点击直发({clicked})后行内提示含『直发虚拟仓』={hint_ok}; pageerror={len(errs)} {errs[:1]}")
    page.close()

    # f. 退租入库详情?id=TZRK-20260903-009
    page, errs = open_page(ctx, r"租赁管理\退租入库详情.html", "?id=TZRK-20260903-009")
    body = page.locator("body").inner_text()
    has_loc = ("XNC-ZF" in body) and ("直发虚拟仓" in body)
    idx = body.find("入库库位")
    seg = body[idx:idx+60].replace("\n", "|") if idx >= 0 else "(未找到入库库位)"
    node = "系统识别原租入单 RZD-20260815-003 为直发类型"
    has_node = node.replace(" ", "") in body.replace(" ", "").replace("\n", "")
    log(f"[f] 退租入库详情: 入库库位段='{seg}'; 全文含XNC-ZF+直发虚拟仓={has_loc}; timeline含识别节点={has_node}; pageerror={len(errs)} {errs[:1]}")
    page.close()

    browser.close()

with open(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g54_accept\accept_render.out", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
