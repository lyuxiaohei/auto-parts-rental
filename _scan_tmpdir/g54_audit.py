# G54 T7 审计门：_run_filter_audit3.audit_page 跑 18 页（T1 的 11 页＋租入域 4 页＋两详情＋库存查询）
import sys
sys.path.insert(0, r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir')
from pathlib import Path
from _run_filter_audit3 import audit_page, ROOT
from playwright.sync_api import sync_playwright

PAGES = [
    "基础数据/库位档案.html",
    "系统管理/数据字典.html",
    "基础数据/库位新建.html",
    "仓储作业/盘点录入.html",
    "仓储作业/调拨新建.html",
    "仓储作业/其他入库新建.html",
    "仓储作业/其他出库新建.html",
    "销售管理/销售出库新建.html",
    "项目管理/上下游绑定.html",
    "租赁管理/租赁出库录单.html",
    "租赁管理/退租入库新建.html",
    "租入管理/租入单列表.html",
    "租入管理/租入单新建.html",
    "租入管理/租入单详情.html",
    "租赁管理/退租入库详情.html",
    "租入管理/租入入库详情.html",
    "租赁管理/租赁出库详情.html",
    "仓储作业/库存查询.html",
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    npass = nfail = 0
    for rel in PAGES:
        path = ROOT / rel
        try:
            r = audit_page(browser, path)
        except Exception as e:
            print(f"[FAIL] {rel} — audit 异常 {type(e).__name__}: {e}")
            nfail += 1
            continue
        probs = r.get("problems", [])
        dl = r.get("dead_links", [])
        js = [e for e in r.get("js_errors", []) if "ERR_CONNECTION" not in str(e) and "net::ERR_" not in str(e)]
        audit_err = r.get("audit_error")
        ok = not probs and not dl and not js and not audit_err
        if ok:
            npass += 1
            print(f"[PASS] {rel} — problems 0 / dead_links 0 / js 0")
        else:
            nfail += 1
            print(f"[FAIL] {rel} — problems={len(probs)} dead_links={len(dl)} js={len(js)} audit_err={audit_err}")
            for x in probs[:5]:
                print("   problem:", x)
            for x in dl[:5]:
                print("   dead:", x)
            for x in js[:5]:
                print("   js:", x)
    browser.close()
    print(f"=== 审计门判定：{npass} PASS / {nfail} FAIL（共 {len(PAGES)} 页）===")
