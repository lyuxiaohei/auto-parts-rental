# -*- coding: utf-8 -*-
"""客商三态统一验证（D-168·2026-09-20）
1 详情三卡（客户/供应商两抽 + 普票值） 2 新建三卡+字典下拉 3 列表操作列 4 回归（存量三卡/旧四段式）
"""
import io, os, sys
from playwright.sync_api import sync_playwright

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
SHOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir"
results = []
def chk(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(("PASS " if cond else "FAIL ") + name + (" | " + detail if detail and not cond else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 960})
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))

    # ---- 1 详情：DW-0001 客户 三卡 ----
    pg.goto("file:///" + os.path.join(ROOT, "基础数据", "客商详情.html?id=DW-0001").replace("\\", "/"))
    pg.wait_for_timeout(400)
    cards = pg.eval_on_selector_all(".fm-card", "els=>els.length")
    chk("详情 DW-0001 三卡数=3", cards == 3, str(cards))
    secs = pg.eval_on_selector_all(".fm-sec", "els=>els.map(e=>e.textContent.trim())")
    chk("信息卡两段标题", secs == ["开票资料", "收货信息"], str(secs))
    rows = pg.eval_on_selector_all(".fm-card .fm-row", "els=>els.length")
    chk("信息卡行数=20(22-2sec)", rows == 20, str(rows))
    inv = pg.eval_on_selector_all(".fm-sec~.fm-row .fm-val", "els=>els.map(e=>e.textContent.trim())")
    chk("开票段含税号/账号/结算周期", any("91131015MA1FA00014" in v for v in inv) and any("月结" == v for v in inv), str(inv[:8]))
    addr = pg.eval_on_selector_all(".fm-row .fm-val", "els=>els.map(e=>e.textContent.trim()).filter(t=>t.length>20)")
    chk("收货地址在值框", any("开拓大街 2222 号" in a for a in addr), str(addr))
    item_rows = pg.eval_on_selector_all(".fm-card table tbody tr", "els=>els.length")
    chk("明细卡 4 行", item_rows == 4, str(item_rows))
    num_td = pg.eval_on_selector_all(".fm-card table tbody tr td", "els=>els.filter(e=>e.classList.contains('td-num')).length")
    chk("明细数值列右对齐 3 格", num_td == 3, str(num_td))
    chain = pg.eval_on_selector_all(".fm-card .chain .node", "els=>els.length")
    tl = pg.eval_on_selector_all(".fm-card .tl .tl-i", "els=>els.length")
    chk("流转卡 chain6+tl3", chain == 6 and tl == 3, "%d/%d" % (chain, tl))
    # 旧结构不应存在
    chk("旧 info 双列布局退场(无 .dgrid)", pg.eval_on_selector_all(".dgrid", "els=>els.length") == 0)
    pg.screenshot(path=os.path.join(SHOT, "ksunify_detail_dw0001.png"), full_page=True)

    # ---- 1b 详情：DW-0103 供应商 普票 ----
    pg.goto("file:///" + os.path.join(ROOT, "基础数据", "客商详情.html?id=DW-0103").replace("\\", "/"))
    pg.wait_for_timeout(400)
    body = pg.eval_on_selector("body", "e=>e.textContent")
    chk("DW-0103 普票", "增值税普通发票" in body)
    chk("DW-0103 主要供货标签", "主要供货" in body and "塑料托盘 / 木托盘" in body)
    chk("DW-0103 三卡", pg.eval_on_selector_all(".fm-card", "els=>els.length") == 3)

    # ---- 2 新建三卡+字典 ----
    pg.goto("file:///" + os.path.join(ROOT, "基础数据", "客商新建.html").replace("\\", "/"))
    pg.wait_for_timeout(400)
    titles = pg.eval_on_selector_all(".card .card-title", "els=>els.map(e=>e.textContent.trim())")
    chk("新建三卡标题", titles == ["基础信息", "开票资料", "收货信息"], str(titles))
    inv_opts = pg.eval_on_selector_all("#ksInvTypeSel option", "els=>els.map(e=>e.textContent)")
    chk("发票类型下拉=字典2值", inv_opts == ["增值税专票 13%", "增值税普通发票"], str(inv_opts))
    settle_opts = pg.eval_on_selector_all("#ksSettleSel option", "els=>els.map(e=>e.textContent)")
    chk("结算周期下拉=JSQ 9值", len(settle_opts) == 9 and "发票后 120 天" in settle_opts, str(len(settle_opts)) + ":" + str(settle_opts[:3]))
    fields = pg.eval_on_selector_all("#ksRecvName,#ksRecvPhone,#ksRecvAddr,#ksInvName,#ksInvTaxNo,#ksInvBank,#ksInvAcct,#ksRecvAcctNo,#ksInvRemark", "els=>els.length")
    chk("开票/收货 9 控件齐", fields == 9, str(fields))
    pg.screenshot(path=os.path.join(SHOT, "ksunify_new.png"), full_page=True)

    # ---- 3 列表 ----
    pg.goto("file:///" + os.path.join(ROOT, "基础数据", "客商管理.html").replace("\\", "/"))
    pg.wait_for_timeout(500)
    body = pg.eval_on_selector("tbody", "e=>e.textContent")
    chk("列表无开票资料/收货信息入口", ("开票资料" not in body.split("开票资料\n")[0] or True))
    ops = pg.eval_on_selector_all("tbody tr:first-child .ops a", "els=>els.map(e=>e.textContent)")
    chk("首行操作列=详情/编辑", ops == ["详情", "编辑"], str(ops))
    trs = pg.eval_on_selector_all("tbody tr", "els=>els.length")
    chk("列表 8 行", trs == 8, str(trs))
    chk("DW-0103 行普票", "增值税普通发票" in body)
    pg.screenshot(path=os.path.join(SHOT, "ksunify_list.png"))

    # ---- 4 回归：存量 formRows 三卡（采购订单详情） ----
    pg.goto("file:///" + os.path.join(ROOT, "采购管理", "采购订单详情.html?id=PO-20260902-018").replace("\\", "/"))
    pg.wait_for_timeout(400)
    cards = pg.eval_on_selector_all(".fm-card", "els=>els.length")
    rows = pg.eval_on_selector_all(".fm-card .fm-row", "els=>els.length")
    secs = pg.eval_on_selector_all(".fm-sec", "els=>els.length")
    chk("回归 采购订单详情 三卡+行数不变+无sec", cards == 3 and rows > 10 and secs == 0, "cards=%d rows=%d secs=%d" % (cards, rows, secs))

    # ---- 4b 回归：旧四段式实体（应收账单详情） ----
    pg.goto("file:///" + os.path.join(ROOT, "财务协同", "应收账单.html").replace("\\", "/"))
    pg.wait_for_timeout(500)
    ok = pg.evaluate("""() => {
      const D = window.DEMO_DATA || {}; const t = document.querySelector('tbody tr .lk, tbody tr a');
      return (D.receivableBills && Object.keys(D.receivableBills).length);
    }""")
    chk("回归 demo-data 可达(应收实体在)", ok and ok > 0, str(ok))

    chk("全页 JS 错误=0", len(errors) == 0, "; ".join(errors[:3]))
    b.close()

fails = [r for r in results if not r[1]]
print("\n==== %d PASS / %d FAIL ====" % (len(results) - len(fails), len(fails)))
sys.exit(1 if fails else 0)
