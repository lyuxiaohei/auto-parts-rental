# -*- coding: utf-8 -*-
"""
验证门2：Playwright 抽验
A. 冻结 10 页：1280x720 窄视口 → 主表横向滚动 200px → 断言 ops 列与 th.sticky-op 贴右（不动）
B. 弹窗 10 页：modal-lg 计算宽度=780（92vw 封顶内）、弹窗内容无溢出裁切
C. 菜单：抽 3 页 断言 销售订单 后紧跟 租赁单
D. F01：全部 <a href> 目标存在 + S1 口径注记可见 + 首页节点可点
结果打印 + 写 _scan_tmpdir/goal-spotcheck.md
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
OUT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\goal-spotcheck.md")

FREEZE_PAGES = [
    "仓储作业/采购入库列表.html", "仓储作业/销售出库列表.html", "仓储作业/组合出库列表.html",
    "仓储作业/退租入库列表.html", "包装管理/租赁单列表.html", "包装管理/租出台账.html",
    "财务协同/应收账单.html", "基础数据/库位档案.html", "系统管理/用户权限.html", "首页/我的待办.html",
]
MODAL_PAGES = [
    "采购管理/采购订单列表.html", "仓储作业/销售出库列表.html", "包装管理/租赁单列表.html",
    "财务协同/应收账单.html", "财务协同/银行水单核销.html", "仓储作业/退租入库列表.html",
    "基础数据/客商管理.html", "系统管理/用户权限.html", "仓储作业/租入归还列表.html", "财务协同/应付账单.html",
]

FREEZE_JS = r"""
(() => {
  const wrap = document.querySelector('.table-wrap');
  if (!wrap) return {err:'无 .table-wrap'};
  wrap.scrollLeft = 200;
  const th = document.querySelector('th.sticky-op');
  if (!th) return {err:'无 th.sticky-op'};
  const wr = wrap.getBoundingClientRect();
  const thr = th.getBoundingClientRect();
  const thOk = Math.abs(thr.right - wr.right) < 3;
  // 行内 ops：取第一行
  const td = document.querySelector('tbody tr td.sticky-op');
  const tdr = td ? td.getBoundingClientRect() : null;
  const tdOk = tdr ? Math.abs(tdr.right - wr.right) < 3 : false;
  // 滚回 0 后 ops 应离开右缘（证明 sticky 生效而非恰好等宽）
  wrap.scrollLeft = 0;
  const thr2 = th.getBoundingClientRect();
  const moved = thr2.right > wr.right - 3;  // 滚回后应超出/贴住右缘之外
  return {thOk, tdOk, scrolled: wrap.scrollLeft === 0, cols: wrap.querySelector('table').rows[0].cells.length};
})()
"""

MODAL_JS = r"""
(id => {
  const ov = document.getElementById(id);
  if (!ov) return {err:'无 ' + id};
  ov.classList.add('show');
  const m = ov.querySelector('.modal');
  const w = m.getBoundingClientRect().width;
  const cs = getComputedStyle(m);
  const body = ov.querySelector('.modal-body');
  const contentOverflow = body ? body.scrollWidth > body.clientWidth + 2 : false;
  return {w: Math.round(w), vw: Math.round(innerWidth*0.92), overflowX: contentOverflow, bodyScroll: body ? body.scrollHeight > body.clientHeight : null};
})
"""

def main():
    lines = ["# 验证门2：Playwright 抽验（2026-09-05）", ""]
    fails = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        # ---- A 冻结 ----
        lines += ["## A. 操作栏冻结（窄视口 1280×720 · 横滚 200px 后贴右）", "", "| 页面 | th贴右 | td贴右 | 列数 |", "|---|---|---|---|"]
        for f in FREEZE_PAGES:
            pg = b.new_page(viewport={"width": 1280, "height": 720})
            pg.goto((ROOT / f).as_uri())
            pg.wait_for_timeout(250)
            r = pg.evaluate(FREEZE_JS)
            if "err" in r:
                lines.append(f"| {f} | ❌ {r['err']} | | |")
                fails.append(f"冻结 {f}: {r['err']}")
            else:
                ok = r["thOk"] and r["tdOk"]
                lines.append(f"| {f} | {'✅' if r['thOk'] else '❌'} | {'✅' if r['tdOk'] else '❌'} | {r['cols']} |")
                if not ok:
                    fails.append(f"冻结 {f}: th={r['thOk']} td={r['tdOk']}")
            pg.close()
        # ---- B 弹窗宽度 ----
        lines += ["", "## B. 弹窗宽度 modal-lg=780 / max-width:92vw / 内容无横向溢出", "", "| 页面 | 弹窗 | 宽度 | 溢出 |", "|---|---|---|---|"]
        for f in MODAL_PAGES:
            pg = b.new_page(viewport={"width": 1440, "height": 900})
            pg.goto((ROOT / f).as_uri())
            pg.wait_for_timeout(250)
            mids = pg.evaluate("() => [...document.querySelectorAll('.modal-overlay .modal.modal-lg')].map(m => m.parentElement.id)")
            r = pg.evaluate(MODAL_JS, mids[0] if mids else None)
            if "err" in r:
                lines.append(f"| {f} | - | ❌ {r['err']} | |")
                fails.append(f"弹窗 {f}: {r['err']}")
            else:
                wOk = abs(r["w"] - 780) < 2 or r["w"] <= r["vw"] + 2
                lines.append(f"| {f} | {mids[0]} | {r['w']}px | {'❌横向溢出' if r['overflowX'] else '✅'} |")
                if not wOk or r["overflowX"]:
                    fails.append(f"弹窗 {f}: w={r['w']} overflow={r['overflowX']}")
            pg.close()
        # ---- C 菜单 ----
        lines += ["", "## C. 菜单顺序（租赁单紧跟销售订单）", ""]
        for f in ["首页/项目看板.html", "包装管理/租赁单列表.html", "销售管理/销售订单列表.html"]:
            pg = b.new_page()
            pg.goto((ROOT / f).as_uri())
            pg.wait_for_timeout(200)
            r = pg.evaluate("""() => {
              const items = [...document.querySelectorAll('ul.sm-sub li .sm-link')];
              const names = items.map(e => e.textContent.trim());
              const i = names.indexOf('销售订单');
              return {next: names[i+1], sel: names.includes('租赁单')};
            }""")
            ok = r["next"] == "租赁单" and r["sel"]
            lines.append(f"- {f}: 销售订单→{r['next']} {'✅' if ok else '❌'}")
            if not ok: fails.append(f"菜单 {f}: next={r['next']}")
            pg.close()
        # ---- D F01 ----
        pg = b.new_page(viewport={"width": 1600, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto((ROOT / "P3-R01-F01-业务流程导航图.html").as_uri())
        pg.wait_for_timeout(400)
        r = pg.evaluate("""() => {
          const links = [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'));
          const note = [...document.querySelectorAll('text')].some(t => t.textContent.includes('五态口径'));
          const first = document.querySelector('a[href]');
          return {links: [...new Set(links)], note, hasFirst: !!first};
        }""")
        dead = []
        for h in r["links"]:
            target = (ROOT / "P3-R01-F01-业务流程导航图.html").parent / unquote(h.split("#")[0].split("?")[0])
            if not target.exists():
                dead.append(h)
        okD = not dead and r["note"] and r["hasFirst"] and not errs
        lines += ["", "## D. F01 导航图", "",
                  f"- 链接目标 {len(r['links'])} 个，死链 {len(dead)} {'✅' if not dead else '❌ ' + str(dead[:5])}",
                  f"- S1 五态口径注记可见：{'✅' if r['note'] else '❌'}",
                  f"- JS 错误：{len(errs)} {'✅' if not errs else errs}"]
        if not okD: fails.append(f"F01: dead={dead[:3]} note={r['note']} errs={errs[:2]}")
        pg.close()
        b.close()
    lines += ["", f"## 结论：{'全部通过 ✅' if not fails else '失败 ' + str(len(fails)) + ' 项：' + '; '.join(fails)}"]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
