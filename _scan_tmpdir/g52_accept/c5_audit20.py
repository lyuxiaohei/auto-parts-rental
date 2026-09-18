# -*- coding: utf-8 -*-
# G52 独立验收 ⑤：复用 audit_interaction.py 的 audit_page/HARNESS/check_dead_links 逻辑，
# 抽跑 20 页（全部为 G52 改造页），口径 problems/dead_links/js_errors（net::ERR_ 豁免）。
# 结果只写入 _scan_tmpdir/g52_accept/（不触碰审计器自身输出路径）。
import asyncio, json, sys
from pathlib import Path

SCAN = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir")
sys.path.insert(0, str(SCAN))
import audit_interaction as AI  # 只读导入；main guard 保证不会自动跑全量

OUT = SCAN / "g52_accept"
ROOT = AI.ROOT  # _scan_tmpdir 的 parent + 原型目录

PAGES = [
    "财务协同/银行回单核销.html",   # G52 样板
    "财务协同/付款登记.html",
    "财务协同/应收账单.html",
    "财务协同/损益报表.html",
    "首页/项目看板.html",
    "仓储作业/库存查询.html",
    "仓储作业/盘点录入.html",
    "采购管理/采购入库列表.html",
    "采购管理/采购入库录单.html",
    "租赁管理/租赁出库列表.html",
    "租赁管理/转移出库新建.html",
    "租入管理/租入入库列表.html",
    "租入管理/租入归还新建.html",   # 推广清单内无数据键页（39 键中仅 弹窗/租入归还新建.html）
    "基础数据/BOM维护.html",
    "基础数据/客商管理.html",
    "系统管理/用户权限.html",
    "系统管理/数据字典.html",
    "项目管理/项目详情.html",
    "销售管理/销售退货单列表.html",
    "我的待办.html",                 # 根级 G52 页
]

async def main():
    paths = [ROOT / p for p in PAGES]
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        print("MISSING:", missing); return
    results = await AI._run(paths)
    total_p = total_d = total_j = 0
    rows = []
    for r in results:
        js = [e for e in r["js_errors"] if "net::ERR_" not in e.get("text", "")]
        p, d, j = len(r["problems"]), len(r["dead_links"]), len(js)
        total_p += p; total_d += d; total_j += j
        flag = "" if (p == d == j == 0 and not r.get("audit_error")) else "  <<<"
        rows.append(f"{r['page']}  问题:{p} 死链:{d} JS错:{j}"
                    + (f" 审计异常:{r.get('audit_error','')[:60]}" if r.get("audit_error") else "") + flag)
        if j:
            for e in js[:3]:
                rows.append(f"    js_err: {e.get('type')}: {e.get('text')[:120]}")
        for pr in r["problems"][:3]:
            rows.append(f"    problem: {pr.get('cat')}/{pr.get('type')} @ {json.dumps(pr.get('where'), ensure_ascii=False)[:100]}")
        for dl in r["dead_links"][:3]:
            rows.append(f"    dead: {dl}")
    print("\n".join(rows))
    print("=" * 60)
    print(f"20 页合计: problems={total_p} dead_links={total_d} js_errors={total_j}")
    (OUT / "c5_audit20_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

asyncio.run(main())
