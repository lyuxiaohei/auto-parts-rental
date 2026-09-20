# -*- coding: utf-8 -*-
"""全量列对齐验证（只读）：期望表 → 右对齐列集合；逐页逐列核对 td/th 对齐与 tabular-nums、其余列左、JS 0"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
SPEC = {
 "基础数据/产品档案.html": [(".colsett-tbl", [7,8,9,10,12])],
 "基础数据/客商管理.html": [(".colsett-tbl", [9])],
 "仓储作业/其他入库列表.html": [(".table-wrap table", [5,7])],
 "仓储作业/其他出库列表.html": [(".table-wrap table", [5,7])],
 "仓储作业/库存调拨列表.html": [(".table-wrap table", [4,7])],
 "仓储作业/盘点列表.html": [(".table-wrap table", [4,5,9])],
 "基础数据/BOM.html": [(".table-wrap table", [4,7])],
 "基础数据/BOM维护.html": [(".table-wrap table", [6])],
 "基础数据/库位档案.html": [(".table-wrap table", [5])],
 "仓储作业/库存查询.html": [(".aln-a",[5,6,7,8,9,10]),(".aln-b",[4,5,6]),(".aln-c",[5,6])],
 "租赁管理/租赁单列表.html": [(".aln-a",[6,7,8]),(".aln-b",[2,3,4])],
 "租赁管理/租赁出库列表.html": [(".table-wrap table", [9])],
 "租赁管理/转移出库列表.html": [(".table-wrap table", [5,7])],
 "租赁管理/退租入库列表.html": [(".table-wrap table", [5,9])],
 "租入管理/租入入库列表.html": [(".table-wrap table", [5,9])],
 "租入管理/租入单列表.html": [(".table-wrap table", [5,6,8,9,12])],
 "租入管理/归还出库列表.html": [(".table-wrap table", [6,9])],
 "租入管理/归还出库新建.html": [("table", [4,5,6])],
 "租入管理/租入单新建.html": [("table", [2,4,5,6,7])],
 "租赁管理/租赁出库录单.html": [("table", [5,6,8,9,10,11])],
 "租赁管理/租赁单新建.html": [("table", [4,5,7,8,9,10])],
 "租赁管理/转移出库新建.html": [("table", [6])],
 "租赁管理/退租入库新建.html": [("table", [4,5])],
 "采购管理/采购订单列表.html": [(".aln-a",[5,6,8]),(".aln-b",[2,4])],
 "销售管理/销售订单列表.html": [(".aln-a",[5,6,9]),(".aln-b",[2,4])],
 "采购管理/采购入库列表.html": [(".table-wrap table", [8])],
 "采购管理/采购退货单列表.html": [(".table-wrap table", [6,7,9])],
 "销售管理/销售出库列表.html": [(".table-wrap table", [6,8])],
 "销售管理/销售退货单列表.html": [(".table-wrap table", [6,7,9])],
 "采购管理/采购入库录单.html": [("table", [5,6,7,8,9])],
 "采购管理/采购退货新建.html": [("table", [2,3,4,5])],
 "采购管理/采购订单新建.html": [(".table-wrap table", [6,7,8,9,10])],
 "销售管理/销售出库新建.html": [("table", [4,5,6,7,8,9])],
 "销售管理/销售退货新建.html": [("table", [2,3,4,5])],
 "销售管理/销售订单新建.html": [(".table-wrap table", [5,6,7,8,9,10])],
 "财务协同/应付账单.html": [(".aln-a",[8,9,10,11,12]),(".aln-b",[1,2,3,4])],
 "财务协同/银行回单核销.html": [("#sdTable",[3,5,6,7]),("#dzTable",[5,6,7]),("#hxTable",[4,6])],
 "财务协同/付款登记.html": [(".table-wrap table", [4,5])],
 "财务协同/应收账单.html": [(".table-wrap table", [7,8,11])],
 "财务协同/开票登记.html": [(".table-wrap table", [6,7,8])],
 "财务协同/损益报表.html": [(".table-wrap table", [3,4,5,6,7,8,9,10,11])],
 "财务协同/收款登记.html": [(".table-wrap table", [4,5])],
 "财务协同/退款登记.html": [(".table-wrap table", [5,8])],
 "财务协同/付款新建.html": [(".table-wrap table", [1,2,3,4])],
 "财务协同/应付新建.html": [(".table-wrap table", [1,2,3,4])],
 "财务协同/应收生成.html": [(".table-wrap table", [1,2,3,4])],
 "仓储作业/其他入库新建.html": [("table", [6])],
 "仓储作业/其他出库新建.html": [("table", [6])],
 "仓储作业/盘点录入.html": [("table", [4,5,6])],
 "仓储作业/调拨新建.html": [("table", [6])],
 "系统管理/操作日志.html": [(".table-wrap table", [2])],
 "系统管理/数据字典.html": [(".aln-a", [4])],
 "系统管理/用户权限.html": [(".table-wrap table", [7])],
 "系统管理/角色管理.html": [(".table-wrap table", [4])],
 "项目管理/项目详情.html": [(".table-wrap table", [3,5])],
 "首页/项目看板.html": [(".table-wrap table", [5,6,7,8,9])],
 "我的待办.html": [(".table-wrap table", [6])],
}

fails = []
errs_all = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.on("pageerror", lambda e: errs_all.append(str(e)))
    pg.on("console", lambda m: errs_all.append(m.text) if m.type == "error" else None)
    npage = 0
    for rel, tables in SPEC.items():
        pg.goto((ROOT / rel).as_uri())
        pg.wait_for_timeout(450)
        npage += 1
        for sel, rights in tables:
            r = pg.evaluate("""([sel, rights]) => {
              const tbl = document.querySelector(sel);
              if (!tbl) return {err: 'NO-TABLE ' + sel};
              const ths = [...tbl.querySelectorAll('thead th')];
              const tr = tbl.querySelector('tbody tr');
              if (!tr) return {err: 'NO-ROW ' + sel};
              const tds = [...tr.children];
              const out = {err: null, n: tds.length, bad: []};
              rights.forEach(i => {
                const td = tds[i-1], th = ths[i-1];
                if (!td) { out.bad.push('td'+i+'-missing'); return; }
                const a = getComputedStyle(td).textAlign;
                const fv = getComputedStyle(td).fontVariantNumeric;
                const thA = th ? getComputedStyle(th).textAlign : '?';
                if (a !== 'right' || fv !== 'tabular-nums' || thA !== 'right')
                  out.bad.push('td'+i+'='+a+'/'+fv+'/th'+thA);
              });
              tds.forEach((td, k) => {
                const i = k + 1;
                if (rights.includes(i)) return;
                const a = getComputedStyle(td).textAlign;
                if (a === 'right' || a === 'center') out.bad.push('nonR td'+i+'='+a);
              });
              return out;
            }""", [sel, rights])
            if not r or r.get("err"):
                fails.append(f"{rel} {sel}: {r.get('err') if r else 'evaluate-null'}")
                print(f"FAIL {rel} {sel}: {r.get('err') if r else 'null'}")
            elif r["bad"]:
                fails.append(f"{rel} {sel}: {';'.join(r['bad'])}")
                print(f"FAIL {rel} {sel} (n={r['n']}): {';'.join(r['bad'])}")
    b.close()
print(f"pages={npage} tables={sum(len(v) for v in SPEC.values())}")
print("JS_ERRORS:", len(errs_all), errs_all[:3])
print("VERDICT:", "PASS" if not fails and not errs_all else f"FAIL x{len(fails)}")
