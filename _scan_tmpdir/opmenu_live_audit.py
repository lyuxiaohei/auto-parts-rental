# -*- coding: utf-8 -*-
"""三点菜单按钮丢失·实测对账（只读）：逐 renderListPage 页面逐行
期望集=demo-data row.ops ｜ 实际集=直显可用+⋮菜单可用 ｜ 差集=丢失
另报：⋮ 菜单内 data-detail-key 项（tbody 委托够不着·机制性死键）"""
import io, sys, re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = (Path(__file__).resolve().parents[1] / "P3-R01-包装租赁管理后台原型")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

pages = []
for p in sorted(ROOT.rglob("*.html")):
    if p.relative_to(ROOT).parts[0] in ("mobile", "P3-R01-F01-业务流程导航图"):
        continue
    html = p.read_text(encoding="utf-8")
    ents = re.findall(r"renderListPage\(\{(.{0,2500}?)\n\s*\}\)", html, re.S)
    ms = []
    for seg in ents:
        em = re.search(r"entity:\s*'([^']+)'", seg)
        if em:
            ms.append(em.group(1))
    if ms:
        pages.append((p, ms))
print("renderListPage 页面数:", len(pages))

loss, deadkeys, errs = [], [], []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    for p, ents in pages:
        try:
            pg.goto(p.as_uri())
            pg.wait_for_load_state("networkidle")
            rows = pg.evaluate("""() => {
              const out = [];
              document.querySelectorAll('table tbody tr').forEach(tr => {
                const key = tr.querySelector('.lk');
                if (!key) return;
                const direct = [...tr.querySelectorAll('.ops > a')].filter(a => !a.classList.contains('op-dis') && !a.classList.contains('op-more')).map(a => a.textContent.trim());
                const hasMore = !!tr.querySelector('.op-more');
                const rowKey = key.textContent.trim();
                out.push({rowKey, direct, hasMore});
              });
              return out;
            }""")
            for i, r in enumerate(rows):
                menu = []
                if r["hasMore"]:
                    try:
                        pg.click(f'table tbody tr:nth-child({i+1}) .op-more')
                        pg.wait_for_timeout(80)
                        menu = pg.evaluate("""() => {
                          const m = document.getElementById('op-menu-pop');
                          if (!m) return null;
                          return [...m.querySelectorAll('a')].filter(a => !a.classList.contains('op-dis')).map(a => ({t: a.textContent.trim(), dk: a.getAttribute('data-detail-key'), oc: !!a.getAttribute('onclick')}));
                        }""")
                        pg.keyboard.press("Escape")
                        pg.wait_for_timeout(40)
                    except Exception as ex:
                        menu = None  # ⋮ 点了没开
                if menu is None:
                    loss.append((str(p.relative_to(ROOT)), r["rowKey"], "⋮ 打开失败", []))
                    continue
                for it in menu:
                    if it["dk"] and not it["oc"]:
                        deadkeys.append((str(p.relative_to(ROOT)), r["rowKey"], it["t"]))
                actual = set(r["direct"]) | {it["t"] for it in menu}
                expect = pg.evaluate("""(rk) => {
                  for (const e in (window.DEMO_DATA||{})) {
                    const R = window.DEMO_DATA[e][rk];
                    if (R && R.row && R.row.ops) return R.row.ops.map(o => o.t);
                  }
                  return null;
                }""", r["rowKey"])
                if expect is None:
                    continue
                missing = [t for t in expect if t not in actual]
                if missing:
                    loss.append((str(p.relative_to(ROOT)), r["rowKey"], "期望按钮不可达", missing))
        except Exception as ex:
            errs.append("PAGE " + str(p.relative_to(ROOT)) + ": " + str(ex)[:80])
    b.close()

print("\n=== 丢失：期望有、页面直显+⋮ 都拿不到 ===")
for f, k, kind, ms in loss:
    print(f"  {f} | {k} | {kind}" + (f" | 缺: {ms}" if ms else ""))
print("合计:", len(loss))
print("\n=== ⋮ 内 detail 死键（点了无反应）===")
seen = set()
for f, k, t in deadkeys:
    sig = (f, t)
    if sig in seen:
        continue
    seen.add(sig)
    print(f"  {f} | 「{t}」(首见行 {k})")
print("合计(页×按钮):", len(seen))
print("\nJS/页面错误:", len(errs), errs[:5])
