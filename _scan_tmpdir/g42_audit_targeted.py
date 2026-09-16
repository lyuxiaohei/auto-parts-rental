# -*- coding: utf-8 -*-
"""G42 定向审计：T1~T11 全部触碰页 + 数据消费抽样（detail-generic info2 波及面），复用审计 harness"""
import io, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _run_filter_audit3 as A
from pathlib import Path
from playwright.sync_api import sync_playwright

TARGETS = [
    # T1
    u"基础数据/BOM维护.html",
    # T2
    u"财务协同/付款登记.html", u"财务协同/付款详情.html",
    # T3
    u"租赁管理/租赁单新建.html", u"租赁管理/租赁单列表.html", u"租赁管理/租赁单详情.html",
    # T4
    u"财务协同/应收账单.html", u"财务协同/应收详情.html", u"系统管理/数据字典.html",
    # T5
    u"系统管理/用户权限.html",
    # T6
    u"财务协同/应收生成.html",
    # T7a/T7b
    u"基础数据/客商详情.html", u"基础数据/客商管理.html", u"基础数据/物料详情.html",
    u"基础数据/库位详情.html", u"基础数据/BOM版本查看.html", u"项目管理/项目详情.html",
    u"仓储作业/盘点详情.html", u"仓储作业/其他出库详情.html",
    # T8
    u"租赁管理/退租入库详情.html", u"仓储作业/库存流水.html",
    # T9
    u"租入管理/租入归还审核.html", u"租入管理/租入归还详情.html", u"租入管理/租入单详情.html",
    # T10
    u"首页/项目看板.html", u"财务协同/损益报表.html", u"财务协同/应付账单.html", u"财务协同/应付详情.html",
    # T11
    u"财务协同/退款新建.html", u"财务协同/退款登记.html", u"财务协同/退款详情.html",
    # 渲染器/详情抽样（采购/销售/租入出库域）
    u"采购管理/采购订单详情.html", u"采购管理/采购入库详情.html", u"销售管理/销售订单详情.html",
    u"租赁管理/租赁出库详情.html", u"租赁管理/退租入库列表.html",
]

results = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for t in TARGETS:
        p = Path(A.ROOT) / t
        r = A.audit_page(browser, p)
        results.append(r)
        n_err = len(r["js_errors"])
        flag = "" if not r["problems"] and not r["dead_links"] and n_err == 0 and not r.get("audit_error") else "  <-- 有问题"
        print(u"%s  问题:%d 死链:%d JS错:%d%s" % (t, len(r["problems"]), len(r["dead_links"]), n_err, flag))
        if r["problems"]:
            [print(u"   问题:", json.dumps(x, ensure_ascii=False)[:150]) for x in r["problems"][:5]]
        if r["dead_links"]:
            [print(u"   死链:", x) for x in r["dead_links"][:5]]
        if r["js_errors"]:
            [print(u"   JS错:", x["text"][:120]) for x in r["js_errors"][:5]]
        if r.get("audit_error"):
            print(u"   审计异常:", r["audit_error"][:150])
    browser.close()

bad = [r for r in results if r["problems"] or r["dead_links"] or r["js_errors"] or r.get("audit_error")]
print(u"\nG42 定向审计 %d 页：坏 %d" % (len(results), len(bad)))
