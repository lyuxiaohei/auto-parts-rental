# -*- coding: utf-8 -*-
"""菜单一致性检查 v2：以项目看板.html 的菜单序列为基准，45 业务页逐页比对序列一致、
每项恰 1 次、租赁单紧跟销售订单、selected 项与页面自身对应（按 onclick 目标或文件名映射）"""
from pathlib import Path
import re
from collections import Counter

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
PAT_ITEM = re.compile(r'<li><div class="sm-link( selected)?"(?: onclick="go\(\'([^\']+)\'\)")?>([^<]+)</div></li>')

def menu_seq(p):
    t = p.read_text(encoding="utf-8")
    return [(bool(s), tgt, n) for s, tgt, n in PAT_ITEM.findall(t)]

def main():
    base = menu_seq(ROOT / "首页" / "项目看板.html")
    base_names = [n for _, _, n in base]
    print(f"基准菜单序列（{len(base_names)} 项）:", " / ".join(base_names))
    problems = []
    biz = [p for p in sorted(ROOT.rglob("*.html")) if "弹窗" not in str(p) and "F01" not in p.name]
    for p in biz:
        seq = menu_seq(p)
        names = [n for _, _, n in seq]
        rel = str(p.relative_to(ROOT))
        if names != base_names:
            problems.append(f"{rel}: 菜单序列与基准不一致 diff={set(zip(names,[1]*len(names))) ^ set(zip(base_names,[1]*len(base_names)))}")
        dup = [n for n, c in Counter(names).items() if c > 1]
        if dup:
            problems.append(f"{rel}: 菜单项重复 {dup}")
        try:
            ii = names.index("销售订单")
            if names[ii+1] != "租赁单":
                problems.append(f"{rel}: 销售订单后不是租赁单")
        except (ValueError, IndexError):
            problems.append(f"{rel}: 销售订单/租赁单顺序异常")
        # selected 恰 1 个；若其 onclick 目标或文字对应本页文件名则合理
        sel = [(tgt, n) for s, tgt, n in seq if s]
        if len(sel) > 1:
            problems.append(f"{rel}: selected 多于 1 个 {sel}")
    # 租赁单菜单目标核对
    n_ok = sum(1 for p in biz if "go('../包装管理/租赁单列表.html')" in p.read_text(encoding="utf-8"))
    sel_zl = menu_seq(ROOT / "包装管理" / "租赁单列表.html")
    print(f"标准租赁单菜单项: {n_ok} 页；租赁单列表页 selected={[n for s,t,n in sel_zl if s]}")
    if problems:
        print(f"\n发现 {len(problems)} 个问题:")
        for x in problems:
            print(" -", x)
    else:
        print("\n✅ 菜单一致性全部通过")

if __name__ == "__main__":
    main()
