# -*- coding: utf-8 -*-
"""G55 验证门 3/4（只读渲染验证·PW）
门3: T1~T10 页面逐页——biz 圆标数(.pn-q)=该键 biz 活锚数；JS 错误 0；dev 抽验 3 条开抽屉定位
门4: 新建客商/新建项目/自动匹配/上下游绑定 4 按钮功能回归（抽屉不被误开）
预期口径: biz 圆标数 = biz 条数 − 既有死锚数（死锚清单为 G52 登记的改前状态, 逐页注明）
"""
import json, sys, io
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1] / "P3-R01-包装租赁管理后台原型"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 页面 → (预期 .pn-q 数, 该键 biz 条数, 既有死锚 biz 条数及说明)
EXP = {
    "租赁管理/租赁单新建.html": (1, 1, 0, ""),
    "租入管理/租入单新建.html": (1, 1, 0, ""),
    "租入管理/归还出库新建.html": (1, 1, 0, ""),
    "项目管理/上下游绑定.html": (1, 1, 0, ""),
    "基础数据/客商新建.html": (1, 1, 0, ""),
    "基础数据/客商详情.html": (0, 0, 0, ""),
    "租赁管理/退租入库新建.html": (1, 1, 0, ""),
    "采购管理/采购退货单列表.html": (1, 3, 2, "id2 锚=新建退货单按钮已页面化(G33 既有)+id1 行锚被 renderListPage 运行时重写(既有)"),
    "财务协同/付款登记.html": (1, 1, 0, ""),
    "采购管理/采购订单列表.html": (1, 1, 0, ""),
    "销售管理/销售出库列表.html": (1, 1, 0, ""),
    "基础数据/客商管理.html": (1, 1, 0, ""),
    "基础数据/产品档案.html": (0, 1, 1, "id1 锚=税率区已迁新建物料页(0914 既有)"),
    "基础数据/库位档案.html": (1, 2, 1, "id2 锚=运行时行无 note 字段(G54 既有)"),
    "财务协同/应收账单.html": (2, 2, 0, ""),
    "财务协同/应付账单.html": (1, 1, 0, ""),
    "租入管理/归还出库列表.html": (0, 0, 0, ""),
    "仓储作业/其他入库列表.html": (0, 1, 1, "页缺共享件两行引用(改前状态·红线禁加引用行·T10 留档)"),
    "采购管理/采购入库录单.html": (2, 2, 0, ""),
    "租赁管理/租赁出库录单.html": (2, 2, 0, ""),
    "销售管理/销售订单新建.html": (0, 0, 0, ""),
    "销售管理/销售出库新建.html": (0, 0, 0, ""),
    "租赁管理/租赁单列表.html": (0, 0, 0, ""),
    "销售管理/销售订单列表.html": (0, 0, 0, ""),
    "仓储作业/其他出库新建.html": (0, 0, 0, ""),
    "仓储作业/其他入库新建.html": (0, 0, 0, ""),
}
# dev 抽验 3 条: (页面, 锚选择器, 期望抽屉定位标题)
DEV_SAMPLE = [
    ("租赁管理/租赁单新建.html", 'th[data-note="4"]', "库存校验统一件"),
    ("基础数据/客商管理.html", 'h3[data-note="2"]', "列显示设置件"),
    ("财务协同/应付账单.html", 'td[data-note="2"]', "详情三卡化待拍板"),
]
# 门4: (页面, 按钮文本, 断言函数名)
BTN = [
    ("基础数据/客商管理.html", "新建客商"),
    ("项目管理/项目档案.html", "新建项目"),
    ("财务协同/银行回单核销.html", "自动匹配建议"),
    ("项目管理/项目档案.html", "上下游绑定"),
]

fails = []
def rec(ok, label, detail=""):
    print(("[PASS] " if ok else "[FAIL] ") + label + (" —— " + detail if detail else ""))
    if not ok: fails.append(label)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})

    # ---------- 门3 ----------
    for rel, (q_exp, biz_n, dead, why) in EXP.items():
        url = (ROOT / rel).as_uri()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.goto(url, wait_until="networkidle")
        pg.wait_for_timeout(250)
        q = pg.eval_on_selector_all(".pn-q", "els=>els.length")
        ok = (q == q_exp) and (len(errs) == 0)
        det = f".pn-q={q}/期望{q_exp}·biz条数={biz_n}" + (f"·既有死锚={dead}({why})" if dead else "") + (f"·JS错={len(errs)}:{errs[:2]}" if errs else "")
        rec(ok, f"门3 {rel}", det)
        pg.remove_listener("pageerror", None) if False else None
        # 重建监听（playwright 无 remove 单监听简便法，直接换新页）——用新页每轮
        pg.close()
        pg = b.new_page(viewport={"width": 1440, "height": 900})

    # ---------- dev 抽验 3 条（?notes=1 开启→点 dev 锚→抽屉开+定位高亮） ----------
    for rel, sel, title in DEV_SAMPLE:
        url = (ROOT / rel).as_uri() + "?notes=1"
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(url, wait_until="networkidle")
        pg.wait_for_timeout(300)
        # ?notes=1 初始开抽屉→mask 拦截点击：先 Esc 关抽屉再点宿主
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(200)
        el = pg.query_selector(sel)
        if not el:
            rec(False, f"门3dev {rel}", f"锚 {sel} 未找到")
        else:
            el.click()
            pg.wait_for_timeout(300)
            shown = pg.eval_on_selector(".pn-drawer", "d=>d.classList.contains('pn-show')")
            hl = pg.eval_on_selector(".pn-item.pn-hl", "d=>d.textContent.trim().slice(0,40)") if pg.query_selector(".pn-item.pn-hl") else ""
            ok = shown and (title in (hl or ""))
            rec(bool(ok), f"门3dev {rel}", f"抽屉开={shown}·定位='{(hl or '')[:24]}'·期望含'{title}'")
        pg.close()
        pg = b.new_page(viewport={"width": 1440, "height": 900})

    # ---------- 门4 ----------
    for rel, text in BTN:
        url = (ROOT / rel).as_uri()
        pg.goto(url, wait_until="networkidle")
        pg.wait_for_timeout(200)
        btn = pg.query_selector(f'button:has-text("{text}")')
        if not btn:
            rec(False, f"门4 {rel}·{text}", "按钮未找到")
            continue
        before = pg.url
        btn.click()
        pg.wait_for_timeout(500)
        after = pg.url
        drawer = pg.eval_on_selector(".pn-drawer", "d=>d.classList.contains('pn-show')") if pg.query_selector(".pn-drawer") else False
        modal = pg.evaluate("()=>!!document.querySelector('.modal[style*=\"display: block\"], .modal.show, [id$=Modal][style*=\"flex\"], [id$=Modal][style*=\"block\"]')")
        toast = pg.evaluate("()=>(document.querySelector('.toast,.m-toast,#toast')||{}).textContent||''")
        nav = after != before
        if text == "自动匹配建议":
            # autoMatch()=按金额/户名勾选两侧 .cb 复选框：断言勾选数>0 即功能已执行
            checked = pg.evaluate("()=>document.querySelectorAll('#sdTable .cb:checked,#dzTable .cb:checked').length")
            ok = checked > 0 and not drawer
            rec(ok, f"门4 {rel}·「{text}」", f"匹配勾选={checked}行·抽屉误开={drawer}")
        else:
            ok = (nav or modal) and not drawer
            rec(ok, f"门4 {rel}·「{text}」", f"跳页={nav}({after.split('/')[-1][:28] if nav else ''})·弹窗={modal}·抽屉误开={drawer}·toast={toast[:14]!r}")
        pg.close()
        pg = b.new_page(viewport={"width": 1440, "height": 900})

    b.close()

print(f"\n门3+门4 总判定: {len(fails)==0 and 'ALL PASS' or 'FAIL '+str(len(fails))}")
print("失败清单:", fails if fails else "无")
