# -*- coding: utf-8 -*-
"""快速定向审计：本次改动 7 页 + 数据消费抽样 4 页，复用审计 harness"""
import io, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _run_filter_audit3 as A
from pathlib import Path
from playwright.sync_api import sync_playwright

TARGETS = [
    u"租赁管理/转移出库审核.html",
    u"租赁管理/转移出库列表.html",
    u"租赁管理/转移出库单详情.html",
    u"租赁管理/转移出库新建.html",
    u"仓储作业/库存查询.html",
    u"我的待办.html",
    u"系统管理/权限配置.html",
    u"P3-R01-F01-业务流程导航图.html",
    u"租赁管理/租赁单列表.html",
    u"采购管理/采购入库列表.html",
    u"mobile/待办审批.html",
    u"财务协同/退款登记.html",
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
print(u"\n定向审计 %d 页：坏 %d" % (len(results), len(bad)))
