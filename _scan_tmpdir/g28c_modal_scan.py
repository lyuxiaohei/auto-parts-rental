# -*- coding: utf-8 -*-
"""全站弹窗样式检查：每页所有 .modal-overlay 强开，测 modal 横溢/竖溢/超视口
口径：1440×900 演示视口；溢出>2px 判问题；输出 JSON+控制台清单
用法：python g28c_modal_scan.py [过滤串]
"""
import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

PROTO = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型").resolve()
OUT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g28c_modal_scan.json")
FILTER = sys.argv[1] if len(sys.argv) > 1 else ""

pages = [p for p in sorted(PROTO.rglob("*.html"))
         if "backup-" not in str(p) and (not FILTER or FILTER in str(p))]
print("待扫页面:", len(pages))

JS = """() => {
  const out = [];
  document.querySelectorAll('.modal-overlay').forEach(mo => {
    const m = mo.querySelector('.modal') || mo.querySelector('[class*=modal]');
    if (!m) { out.push({id: mo.id || '(无id)', 无modal: true}); return; }
    const was = mo.classList.contains('show');
    mo.classList.add('show');
    const r = m.getBoundingClientRect();
    const rec = {
      id: mo.id || '(无id)',
      title: (m.querySelector('.modal-title,h3')||{}).textContent || '',
      w: Math.round(r.width), h: Math.round(r.height),
      横溢: m.scrollWidth - m.clientWidth,
      竖溢: m.scrollHeight - m.clientHeight,
      超视口: r.bottom > innerHeight + 1 || r.right > innerWidth + 1
    };
    if (!was) mo.classList.remove('show');
    out.push(rec);
  });
  return out;
}"""

results, errs_pages = [], []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    for idx, p in enumerate(pages, 1):
        rel = p.relative_to(PROTO).as_posix()
        if rel.startswith('mobile/'):
            continue  # PC 口径先扫，mobile 另列
        try:
            pg.goto(p.as_uri(), wait_until='load', timeout=15000)
            pg.wait_for_timeout(150)
            recs = pg.evaluate(JS)
            for r in recs:
                r['page'] = rel
                results.append(r)
        except Exception as e:
            errs_pages.append((rel, str(e)[:80]))
        if idx % 20 == 0:
            print("…%d/%d" % (idx, len(pages)))
    b.close()

bad = [r for r in results if r.get('横溢', 0) > 2 or r.get('竖溢', 0) > 2 or r.get('超视口') or r.get('无modal')]
json.dump({"扫描": len(results), "问题": bad, "异常页": errs_pages},
          open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print("\n==== 弹窗总数 %d · 问题 %d · 页异常 %d ====" % (len(results), len(bad), len(errs_pages)))
for r in bad:
    tag = []
    if r.get('横溢', 0) > 2: tag.append('横溢%d' % r['横溢'])
    if r.get('竖溢', 0) > 2: tag.append('竖溢%d' % r['竖溢'])
    if r.get('超视口'): tag.append('超视口')
    if r.get('无modal'): tag.append('无modal节点')
    print("  [%s] %s · %s (%s)" % ("+".join(tag), r['page'], r.get('id'), (r.get('title') or '')[:18]))
print("\n清单已写:", OUT)
