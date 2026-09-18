# -*- coding: utf-8 -*-
"""G53 T3-3 审计门：复用 _run_filter_audit3.audit_page 跑 20 详情页 + 14 审核页。
problems / dead_links 全 0 才 PASS（JS 错误一并统计）。"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')

from _run_filter_audit3 import audit_page  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

PAGES = [
    '采购管理/采购订单详情.html', '采购管理/采购订单审核.html',
    '采购管理/采购入库详情.html', '采购管理/采购入库审核.html',
    '采购管理/采购退货详情.html', '采购管理/采购退货审核.html',
    '租入管理/租入单详情.html', '租入管理/租入单审核.html',
    '租入管理/租入入库详情.html',
    '租入管理/租入归还详情.html', '租入管理/租入归还审核.html',
    '租赁管理/租赁单详情.html', '租赁管理/租赁单审核.html',
    '租赁管理/租赁出库详情.html', '租赁管理/租赁出库确认.html',
    '租赁管理/退租入库详情.html', '租赁管理/退租入库审核.html',
    '租赁管理/转移出库单详情.html', '租赁管理/转移出库审核.html',
    '仓储作业/盘点详情.html', '仓储作业/盘点审核.html',
    '仓储作业/其他入库详情.html', '仓储作业/其他入库审核.html',
    '仓储作业/其他出库详情.html', '仓储作业/其他出库审核.html',
    '销售管理/销售订单详情.html', '销售管理/销售订单审核.html',
    '销售管理/销售出库详情.html', '销售管理/销售出库审核.html',
    '销售管理/销售退货详情.html', '销售管理/销售退货审核.html',
    '财务协同/收款详情.html', '财务协同/付款详情.html',
    '财务协同/开票详情.html', '财务协同/退款详情.html',
]

def main():
    fails = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for rel in PAGES:
            r = audit_page(browser, ROOT / rel)
            probs = len(r['problems'])
            dead = len(r['dead_links'])
            js = len(r['js_errors'])
            ok = probs == 0 and dead == 0
            print('%s %s problems=%d dead=%d js=%d' % ('PASS' if ok else 'FAIL', rel, probs, dead, js), flush=True)
            if not ok:
                fails.append((rel, r['problems'][:3], r['dead_links'][:3]))
        browser.close()
    print('AUDIT GATE: %d PASS / %d FAIL (共 %d 页)' % (len(PAGES) - len(fails), len(fails), len(PAGES)))
    for rel, pr, dl in fails:
        print('FAIL DETAIL', rel, pr, dl)
    sys.exit(0 if not fails else 1)

main()
