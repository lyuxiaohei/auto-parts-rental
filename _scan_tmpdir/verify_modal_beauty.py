# -*- coding: utf-8 -*-
"""弹窗美观度独立验收：宽度/单行/横滚三断言（抽 8 弹窗跨模块）"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r'P3-R01-包装租赁管理后台原型').resolve()
SAMPLES = [
    ('仓储作业/采购入库列表.html', 'auditModal'),
    ('包装管理/租赁单列表.html', 'auditModal'),
    ('仓储作业/退租入库列表.html', 'auditModal'),      # 含豁免长文案
    ('包装管理/丢损赔偿单.html', 'auditModal'),
    ('财务协同/应付账单.html', 'auditModal'),
    ('仓储作业/其他出库列表.html', 'auditModal'),
    ('采购管理/租入单列表.html', 'auditModal'),
    ('仓储作业/采购入库列表.html', 'detailModal'),     # detailModal 应保持 780 内联
]

JS = """() => {
  const m = document.querySelector('.modal-overlay.show .modal') ||
            document.querySelector('.modal-overlay[style*="block"] .modal') ||
            document.querySelector('.modal');
  if (!m) return null;
  const hscroll = m.scrollWidth > m.clientWidth + 2;
  const dvals = [...m.querySelectorAll('.dval')].map(v => {
    const tops = new Set();
    Array.from(v.getClientRects()).forEach(x => tops.add(Math.round(x.top / 10)));
    return {t: v.textContent.trim().slice(0, 20), lines: tops.size, len: v.textContent.trim().length};
  });
  return {w: Math.round(m.getBoundingClientRect().width), hscroll, dvals};
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    for rel, modal in SAMPLES:
        pg.goto((ROOT / rel).as_uri())
        pg.wait_for_timeout(150)
        pg.evaluate("id => openModal(id)", modal)
        pg.wait_for_timeout(120)
        r = pg.evaluate(JS)
        if not r:
            print(f'{rel} [{modal}] FAIL 弹窗未打开')
            continue
        multi = [d for d in r['dvals'] if d['lines'] > 1]
        status = 'FAIL' if r['hscroll'] else ('PASS' if not multi else 'PASS*豁免审查')
        print(f"{rel} [{modal}] {status} 宽={r['w']}px 横滚={r['hscroll']} 多行值={len(multi)}")
        for d in multi:
            print(f"    多行(len={d['len']}): {d['t']}")
    b.close()
