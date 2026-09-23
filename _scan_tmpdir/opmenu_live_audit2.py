# -*- coding: utf-8 -*-
"""三点菜单按钮丢失·实测对账 v2（只读）：
- 期望集只认页面 renderListPage 实体的 row.ops（跨实体键撞名排除）
- 行枚举与 ⋮ 点击用同一 locator 序列（多表格不错位）
- ⋮ 打不开时判 host.DATA[key] 是否缺键（真死键 vs 误报）"""
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
    ents = []
    for m in re.finditer(r"renderListPage\(\{(.{0,2500}?)\n\s*\}\)", html, re.S):
        em = re.search(r"entity:\s*'([^']+)'", m.group(1))
        if em:
            ents.append(em.group(1))
    if ents:
        pages.append((p, ents))
print("renderListPage 页面数:", len(pages))

loss, dead, errs, checked = [], [], [], 0
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.on("pageerror", lambda e: errs.append(str(e)[:100]))
    for p, ents in pages:
        try:
            pg.goto(p.as_uri())
            pg.wait_for_load_state("networkidle")
            trs = pg.locator("table tbody tr")
            n = trs.count()
            for i in range(n):
                tr = trs.nth(i)
                if not tr.locator(".lk").count():
                    continue
                key = tr.locator(".lk").first.inner_text().strip()
                direct = tr.evaluate("""el => [...el.querySelectorAll('.ops > a')]
                  .filter(a => !a.classList.contains('op-dis') && !a.classList.contains('op-more'))
                  .map(a => a.textContent.trim())""")
                hasMore = tr.locator(".op-more").count() > 0
                # 期望集：仅页面实体
                expect = pg.evaluate("""(args) => {
                  const [ents, key] = args;
                  for (const e of ents) {
                    const R = (window.DEMO_DATA || {})[e] && window.DEMO_DATA[e][key];
                    if (R && R.row) return { ops: (R.row.ops || []).map(o => o.t), ent: e };
                  }
                  return null;
                }""", [ents, key])
                if not expect:
                    continue  # 页面自定义表格行（非本页实体渲染）→ 不在三点菜单管辖
                checked += 1
                menu = []
                if hasMore:
                    hostOk = pg.evaluate("""(key) => !!(window.__opMenuHost && window.__opMenuHost.DATA[key])""", key)
                    tr.locator(".op-more").click()
                    pg.wait_for_timeout(90)
                    got = pg.evaluate("""() => { const m = document.getElementById('op-menu-pop'); return m ? [...m.querySelectorAll('a')].filter(a => !a.classList.contains('op-dis')).map(a => a.textContent.trim()) : null; }""")
                    pg.keyboard.press("Escape")
                    pg.wait_for_timeout(40)
                    if got is None:
                        dead.append((str(p.relative_to(ROOT)), key, "⋮无反应（host键缺：%s）" % ("否" if hostOk else "是")))
                        continue
                    menu = got
                actual = set(direct) | set(menu)
                missing = [t for t in expect["ops"] if t not in actual]
                if missing:
                    loss.append((str(p.relative_to(ROOT)), key, expect["ent"], missing))
        except Exception as ex:
            errs.append("PAGE %s: %s" % (p.relative_to(ROOT), str(ex)[:80]))
    b.close()

print("对账行数:", checked)
print("\n=== A. ⋮ 点开无反应（死键）===")
for f, k, why in dead:
    print(f"  {f} | {k} | {why}")
print("合计:", len(dead))
print("\n=== B. 期望按钮直显+⋮ 均不可达 ===")
for f, k, e, ms in loss:
    print(f"  {f} | {k} | {e} | 缺: {ms}")
print("合计:", len(loss))
print("\nJS/页面错误:", len(errs), errs[:5])
