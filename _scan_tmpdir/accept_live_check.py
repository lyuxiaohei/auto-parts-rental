# -*- coding: utf-8 -*-
"""任务一·行-弹窗一致全量重跑（2026-09-08）：http.server + Playwright 逐行实点 26 列表页全部触发行 + 24 模板预览页"""
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
BASE = 'http://127.0.0.1:8907/' + quote(str(PROTO.name))

# (序号, 实体, 列表页, 锚文本, modalId)
MODALS = [
    (1, 'leaseOrders', '销售管理/租赁单列表.html', '详情', 'detailModal'),
    (2, 'rentInOrders', '采购管理/租入单列表.html', '详情', 'detailModal'),
    (3, 'comboOutbounds', '仓储作业/组合出库列表.html', '详情', 'detailModal'),
    (4, 'returnInbounds', '仓储作业/退租入库列表.html', '详情', 'detailModal'),
    (5, 'returnApplies', '租赁管理/退租申请列表.html', '详情', 'detailModal'),
    (6, 'damageOrders', '租赁管理/丢损赔偿单.html', '详情', 'detailModal'),
    (7, 'rentInReturns', '仓储作业/租入归还列表.html', '详情', 'detailModal'),
    (8, 'rentInbounds', '仓储作业/租入入库列表.html', '详情', 'detailModal'),
    (9, 'purchaseOrders', '采购管理/采购订单列表.html', '详情', 'detailModal'),
    (10, 'salesOrders', '销售管理/销售订单列表.html', '详情', 'detailModal'),
    (11, 'purchaseInbounds', '仓储作业/采购入库列表.html', '详情', 'detailModal'),
    (12, 'salesOutbounds', '仓储作业/销售出库列表.html', '详情', 'detailModal'),
    (13, 'otherInbounds', '仓储作业/其他入库列表.html', '详情', 'detailModal'),
    (14, 'otherOutbounds', '仓储作业/其他出库列表.html', '详情', 'detailModal'),
    (15, 'assemblyOrders', '仓储作业/组装列表.html', '详情', 'detailModal'),
    (16, 'disassemblyOrders', '仓储作业/拆卸管理列表.html', '详情', 'detailModal'),
    (17, 'stocktakes', '仓储作业/盘点列表.html', '详情', 'detailModal'),
    (18, 'transfers', '仓储作业/库存调拨列表.html', '详情', 'detailModal'),
    (19, 'stockFlows', '仓储作业/库存查询.html', '库存流水', 'flowModal'),
    (20, 'rentTracks', '租赁管理/租出台账.html', '详情', 'trackModal'),
    ('20b', 'assetTracks', '租赁管理/在租台账.html', '资产轨迹', 'trackModal'),
    (21, 'partners', '基础数据/客商管理.html', '详情', 'detailModal'),
    (22, 'appliances', '基础数据/器具档案.html', '详情', 'detailModal'),
    (23, 'parts', '基础数据/零部件档案.html', '详情', 'detailModal'),
    (24, 'locations', '基础数据/库位档案.html', '详情', 'detailModal'),
    (25, 'bomVersions', '基础数据/BOM维护.html', '查看', 'bomViewModal'),
]
TEMPLATES = [
    '销售管理/弹窗/租赁单详情.html', '采购管理/弹窗/租入单详情.html', '仓储作业/弹窗/组合出库单详情.html',
    '仓储作业/弹窗/退租入库单详情.html', '租赁管理/弹窗/退租申请详情.html', '租赁管理/弹窗/丢损赔偿单详情.html',
    '仓储作业/弹窗/租入归还单详情.html', '仓储作业/弹窗/租入入库单详情.html', '采购管理/弹窗/采购订单详情.html',
    '销售管理/弹窗/销售订单详情.html', '仓储作业/弹窗/采购入库单详情.html', '仓储作业/弹窗/销售出库单详情.html',
    '仓储作业/弹窗/其他入库单详情.html', '仓储作业/弹窗/其他出库单详情.html', '仓储作业/弹窗/组装单详情.html',
    '仓储作业/弹窗/拆卸单详情.html', '仓储作业/弹窗/盘点单详情.html', '仓储作业/弹窗/调拨单详情.html',
    '仓储作业/弹窗/库存流水.html', '租赁管理/弹窗/器具出租履历.html', '基础数据/弹窗/客商详情.html',
    '基础数据/弹窗/器具详情.html', '基础数据/弹窗/零部件详情.html', '基础数据/弹窗/库位详情.html',
    '基础数据/弹窗/BOM版本查看.html',
]

CLICK_SCAN = """(args) => {
  const [anchor, modalId, entity] = args;
  const keys = new Set(Object.keys(window.DEMO_DATA[entity] || {}));
  const out = [];
  const modal = document.getElementById(modalId);
  const tEl = document.getElementById('detailTitle');
  document.querySelectorAll('tbody a').forEach(a => {
    const txt = (a.textContent || '').trim();
    if (txt !== anchor) return;
    const rowText = a.closest('tr') ? a.closest('tr').textContent : '';
    if (modal) modal.classList.remove('show');
    if (tEl) tEl.textContent = '';
    a.click();
    const shown = modal && modal.classList.contains('show');
    const title = tEl ? tEl.textContent : '';
    const seg = title.indexOf('·') > -1 ? title.split('·').pop().trim() : null;
    /* titleNo 设计：partners=公司名 / stockFlows=编码+名称 / bomVersions=ZH编码+版本，故 seg 匹配键∪titleNo，
       行文本命中 seg 或对应键任一即判一致 */
    let key = null;
    if (seg && keys.has(seg)) key = seg;
    else if (seg) { for (const k of keys) { if ((window.DEMO_DATA[entity][k] || {}).titleNo === seg) { key = k; break; } } }
    out.push({
      rowText: rowText.slice(0, 90),
      shown, title,
      no: seg,
      ok: !!(shown && key && (rowText.indexOf(seg) > -1 || rowText.indexOf(key) > -1)),
    });
    if (window.closeModal) closeModal(modalId);
  });
  return out;
}"""

results, fails = [], []
def check(item, ok, detail=''):
    results.append((item, ok, detail))
    if not ok: fails.append((item, detail))
    print(('✅' if ok else '❌'), '|', item, '|', detail[:160])

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    ctx = browser.new_context()
    for no, ent, page_f, anchor, mid in MODALS:
        page = ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:120]))
        url = BASE + '/' + quote(page_f)
        page.goto(url, wait_until='load')
        page.wait_for_timeout(250)
        rows = page.evaluate(CLICK_SCAN, [anchor, mid, ent])
        n_pass = sum(1 for r in rows if r['ok'])
        n_all = len(rows)
        bad = [(r['rowText'][:40], r['title'][:50], r['shown']) for r in rows if not r['ok']]
        check(f'#{no} {ent} {page_f} 锚「{anchor}」', n_pass == n_all and n_all > 0,
              f'{n_pass}/{n_all} 实点过' + (f'；未过:{bad[:3]}' if bad else '') + (f' JS错:{errs[:2]}' if errs else ''))
        if errs:
            check(f'#{no} {ent} JS错0', False, str(errs[:3]))
        page.close()
    for tp in TEMPLATES:
        page = ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:120]))
        page.goto(BASE + '/' + quote(tp), wait_until='load')
        page.wait_for_timeout(200)
        st = page.evaluate("""() => {
          const t = document.getElementById('detailTitle');
          const b = document.getElementById('detailBody');
          const vis = document.querySelector('.modal-overlay.show');
          return { title: t ? t.textContent : '', segs: b ? b.children.length : 0, shown: !!vis };
        }""")
        ok = ('·' in st['title']) and st['segs'] > 0 and not errs
        check(f'模板 {tp}', ok, f"title={st['title'][:40]!r} 段数={st['segs']} show={st['shown']}" + (f' JS错:{errs[:2]}' if errs else ''))
        page.close()
    browser.close()

print()
print(f'==== 行-弹窗实点汇总：{len(results)} 项，失败 {len(fails)} 项 ====')
json.dump(results, open(ROOT / '_scan_tmpdir' / 'accept_live_out.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
sys.exit(1 if fails else 0)
