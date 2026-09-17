# -*- coding: utf-8 -*-
"""
G43 验证门 4 · 渲染级 PW 抽验：≥10 页（B 类≥5 组＋A 类≥5 组·表单/筛选两类）
每页断言关键值 + 截图存 _scan_tmpdir/g43_shots/。
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent / "P3-R01-包装租赁管理后台原型"
OUT = Path(__file__).resolve().parent / "g43_shots"
OUT.mkdir(exist_ok=True)

# (页, 截图名, 定位器css, 期望包含的 option 文本列表, 选中演示值(可空), 联动断言(可空))
SHOTS = [
    # B 类
    ("基础数据/产品档案.html", "b01_产品档案_WL物料类型", ".filter-card",
     ["围板箱", "金属托盘", "零部件"], None, None),
    ("财务协同/应收账单.html", "b02_应收账单_ARB措辞统一", ".filter-card",
     ["租赁费", "丢损赔偿", "预收"], "丢损赔偿", "filtered>0"),
    ("财务协同/应付账单.html", "b03_应付账单_APB值映射", ".filter-card",
     ["采购应付", "丢损赔偿（赔付供应商）", "无订单预付款"], None, None),
    ("财务协同/开票登记.html", "b04_开票登记_FP普票全式", ".filter-card",
     ["增值税专票 13%", "增值税普通发票"], None, None),
    ("我的待办.html", "b05_待办_DJ20与审核人并集", ".filter-card",
     ["转移出库", "退款登记"], None, "auditorHasZhaoLei"),
    ("财务协同/退款登记.html", "b06_退款登记_TKL", ".filter-card",
     ["预收退回", "多付退回"], None, None),
    # A 类
    ("系统管理/字典项新建.html", "a01_字典项新建_分类28组", ".form-card, .card, form",
     ["缺损类型", "应收账单类型"], None, None),
    ("租赁管理/租赁单新建.html", "a02_租赁单新建_项目客户物料", ".form-card, .card, form",
     ["PRJ-2601 华骏重卡·长春基地 驾驶室围板箱租赁"], None, None),
    ("租入管理/租入归还新建.html", "a03_归还新建_关联租入单", ".form-card, .card, form",
     ["RZD-20260902-008"], None, "riSynced"),
    ("仓储作业/盘点列表.html", "a04_盘点列表_范围复合值", ".filter-card",
     ["华东中心仓 / 原料区 RA"], "华东中心仓 / 原料区 RA", "filtered>0"),
    ("仓储作业/库存查询.html", "a05_库存查询_库房库位", ".filter-card",
     ["转租终端仓", "XNC-AJZX"], None, None),
    ("财务协同/付款新建.html", "a06_付款新建_应付单号与支付方式", ".form-card, .card, form",
     ["AP-20260903-009", "银行转账", "票据"], None, None),
    ("采购管理/采购订单新建.html", "a07_采购订单新建_项目六在执行", ".form-card, .card, form",
     ["PRJ-2606"], None, "noFinished"),
    ("仓储作业/盘点录入.html", "a08_盘点录入_库房人名", ".form-card, .card, form",
     ["正品仓", "林国栋"], None, None),
]

with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True)
    pg = br.new_page(viewport={"width": 1440, "height": 900})
    npass = nfail = 0
    for page, name, sel_css, musts, pick, extra in SHOTS:
        f = ROOT / page
        try:
            pg.goto(f.as_uri(), wait_until="load", timeout=15000)
            pg.wait_for_timeout(300)
            # 展开折叠筛选卡（extra 行可见后再截图）
            try:
                pg.evaluate("() => { const c = document.querySelector('.filter-card.collapsed'); if (c) c.classList.remove('collapsed'); }")
            except Exception:
                pass
            # 值域断言：页面全 select 的 option 文本池包含 musts
            pool = pg.evaluate("() => [...document.querySelectorAll('select option')].map(o => o.textContent.trim())")
            for m in musts:
                if not any(m in t for t in pool):
                    raise Exception(f"option 缺失: {m}")
            # 演示选中
            if pick:
                pg.evaluate("([m]) => { for (const s of document.querySelectorAll('select')) { if ([...s.options].some(o => o.textContent.trim() === m)) { s.value = m; s.dispatchEvent(new Event('change', {bubbles:true})); break; } } }", [pick])
                pg.wait_for_timeout(400)
            if extra == "filtered>0":
                n = pg.evaluate("() => document.querySelectorAll('tbody tr').length")
                if not n:
                    raise Exception("筛选后 0 行")
            if extra == "auditorHasZhaoLei":
                has = pg.evaluate("() => { const s = document.getElementById('todoAuditor'); return s && [...s.options].some(o => o.textContent.trim() === '赵磊'); }")
                if not has:
                    raise Exception("审核人缺赵磊")
            if extra == "riSynced":
                n = pg.evaluate("() => document.getElementById('riItemsBody') ? document.getElementById('riItemsBody').rows.length : 0")
                if not n:
                    raise Exception("归还明细未联动")
            if extra == "noFinished":
                bad = pg.evaluate("() => [...document.querySelectorAll('select option')].some(o => /PRJ-259|已完结/.test(o.textContent.trim()) && o.textContent.indexOf('PRJ-259') === 0)")
                if bad:
                    raise Exception("项目下拉含已完结")
            # 截图（定位容器·失败退全页）
            el = pg.query_selector(sel_css)
            if el:
                el.screenshot(path=str(OUT / f"{name}.png"))
            else:
                pg.screenshot(path=str(OUT / f"{name}.png"), full_page=False)
            npass += 1
            print(f"[PASS] {page} · {name}")
        except Exception as e:
            nfail += 1
            print(f"[FAIL] {page} · {name}: {str(e)[:100]}")
    br.close()
print(f"\n总判定：{npass} PASS / {nfail} FAIL")
sys.exit(1 if nfail else 0)
