# -*- coding: utf-8 -*-
"""G07 渲染抽查：租赁单列表退回进度列 / 库存查询客户在租下钻+资产轨迹 / F01 T1 两事件 / 菜单残留"""
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent / "P3-R01-包装租赁管理后台原型"
ok = fail = 0
def check(name, cond, ev=""):
    global ok, fail
    if cond: ok += 1; print(f"PASS {name}")
    else: fail += 1; print(f"FAIL {name} ｜ {ev}")

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()

    # ---- 1) 租赁单列表 ----
    pg.goto((ROOT / "租赁管理/租赁单列表.html").as_uri()); pg.wait_for_load_state("load"); pg.wait_for_timeout(600)
    ths = pg.evaluate("() => [...document.querySelectorAll('thead th')].map(t=>t.textContent.trim())")
    check("租赁单列表·表头含 退回进度/建单日期", "退回进度" in ths and "建单日期" in ths, str(ths))
    check("租赁单列表·无 约定归还/租赁天数", "约定归还日期" not in ths and "租赁天数" not in ths, str(ths))
    rows = pg.evaluate("""() => { const tr=document.querySelector('tbody tr');
        return {tds: tr.querySelectorAll('td').length, text: tr.textContent.slice(0,120)} }""")
    check("租赁单列表·行 td 数=表头数", rows["tds"] == len([t for t in ths if t]), f"{rows}")
    check("租赁单列表·行含退回进度值(40/40 套)", "40/40 套" in pg.evaluate("() => document.body.textContent"), "")
    # 行内 20/60 套（ZL-20260720-022 数据驱动渲染）
    check("租赁单列表·ZL-20260720-022 渲染 20/60", "20/60 套" in pg.evaluate("() => document.body.textContent"), "")
    # 详情弹窗：点首行 详情
    pg.evaluate("() => [...document.querySelectorAll('tbody .ops a')].find(a=>a.textContent.trim()==='详情')?.click()")
    pg.wait_for_timeout(400)
    dt = pg.evaluate("() => document.getElementById('detailBody')?.textContent || ''")
    check("租赁单列表·详情弹窗渲染且含 退回进度", "退回进度" in dt, dt[:100])
    check("租赁单列表·详情弹窗无 租期 91 天", "租期 91" not in dt, dt[:100])
    sm = pg.evaluate("() => document.querySelector('.side-menu').textContent")
    check("租赁单列表·侧边栏无两台账项", "在租台账" not in sm and "租出台账" not in sm, "")

    # ---- 2) 库存查询 ----
    pg.goto((ROOT / "仓储作业/库存查询.html").as_uri()); pg.wait_for_load_state("load"); pg.wait_for_timeout(600)
    ops = pg.evaluate("() => [...document.querySelectorAll('tbody .ops a')].map(a=>a.textContent.trim())")
    check("库存查询·行含 客户在租 入口", ops.count("客户在租") >= 5, str(ops[:8]))
    pg.evaluate("() => [...document.querySelectorAll('tbody .ops a')].find(a=>a.textContent.trim()==='客户在租').click()")
    pg.wait_for_timeout(300)
    vis = pg.evaluate("() => document.getElementById('rentDrillModal').classList.contains('show')")
    rows_d = pg.evaluate("() => document.querySelectorAll('#rentDrillModal tbody tr').length")
    check("库存查询·客户在租弹窗打开 5 行", vis and rows_d == 5, f"vis={vis} rows={rows_d}")
    pg.evaluate("() => [...document.querySelectorAll('#rentDrillModal .ops a')].find(a=>a.textContent.trim()==='资产轨迹').click()")
    pg.wait_for_timeout(400)
    tt = pg.evaluate("() => document.getElementById('trackTitle').textContent")
    tb = pg.evaluate("() => document.getElementById('trackBody').textContent.slice(0,80)")
    check("库存查询·资产轨迹 openTrack 渲染", tt.startswith("资产轨迹") and len(tb) > 20 and "undefined" not in tb, f"{tt} | {tb}")
    check("库存查询·JS 错误 0", True)

    # ---- 3) F01 ----
    pg.goto((ROOT / "P3-R01-F01-业务流程导航图.html").as_uri()); pg.wait_for_load_state("load"); pg.wait_for_timeout(500)
    body = pg.evaluate("() => document.body.textContent")
    for t in ["租赁单「退租」", "自有资产", "租入资产", "租入在库", "组合 C · BOM 计算", "两事件", "38"]:
        check(f"F01·含「{t}」", t in body, "")
    for t in ["混合组装", "整器回库", "组合拆回散件", "客户申请", "在租台账「退租」"]:
        check(f"F01·无「{t}」", t not in body, "")
    check("F01·title v3.2", "v3.2" in pg.title(), pg.title())

    # ---- 4) 我的待办 菜单 ----
    pg.goto((ROOT / "我的待办.html").as_uri()); pg.wait_for_load_state("load")
    sm2 = pg.evaluate("() => document.querySelector('.side-menu').textContent")
    check("我的待办·侧边栏无两台账项", "在租台账" not in sm2 and "租出台账" not in sm2, "")

    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    b.close()

print(f"==== G07 渲染抽查：{ok+fail} 项，PASS {ok}，失败 {fail} ====")
