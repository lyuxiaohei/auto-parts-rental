# -*- coding: utf-8 -*-
"""G18 门2：Playwright 抽验 5 页（默认态零说明 + 开启态角标/便签含要点）+ JS 0"""
from playwright.sync_api import sync_playwright
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROT = ROOT/'P3-R01-包装租赁管理后台原型'
PAGES = [
    # (相对路径, 默认态不应含的特征词, data-note 元素选择器文本, 便签要点词, 需先开弹窗(可选 fn))
    ('仓储作业/库存调拨列表.html', '第一期仅支持同仓群', '库存调拨单', '同仓群', None),
    ('财务协同/银行水单核销.html', '取小核销', '② 待核销单据', '取小核销', None),
    ('财务协同/应付账单.html', '审核后自动生成（第一期', '应付账单', '按周期生成', None),
    ('项目管理/项目档案.html', '一对多/多对多', '项目上下游绑定', '一对多/多对多', "openModal('bindModal')"),
    ('租赁管理/弹窗/租入单新建.html', '计费＝月租金', '计费方式', '月租金', None),
]

results, js_errors = [], []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.on('pageerror', lambda e: js_errors.append(str(e)))
    for rel, absent, anchor_text, pin_kw, pre_js in PAGES:
        url = (PROT/rel).resolve().as_uri()
        # --- 默认态 ---
        pg.goto(url)
        pg.wait_for_timeout(300)
        body_txt = pg.evaluate("document.body.innerText")
        ok_absent = absent not in body_txt
        fab = pg.evaluate("() => { const f = document.getElementById('protoNotesFab'); return f ? f.textContent : ''; }")
        ok_fab = fab.startswith('标注')
        results.append((rel, '默认态零说明', ok_absent, f'innerText 含「{absent}」={not ok_absent}'))
        results.append((rel, 'fab 入口在', ok_fab, f'fab={fab!r}'))
        # --- 开启态 ---
        pg.evaluate("localStorage.setItem('proto-notes-on','1')")
        if pre_js:
            pg.evaluate(pre_js)
        pg.goto(url + '?notes=1')
        if pre_js:
            pg.evaluate(pre_js)
        pg.wait_for_timeout(300)
        on_cls = pg.evaluate("document.body.classList.contains('proto-notes-on')")
        results.append((rel, '开启态 class', on_cls, ''))
        el = pg.evaluate("""(t) => {
            const els = [...document.querySelectorAll('[data-note]')];
            const hit = els.find(e => e.textContent.includes(t));
            return hit ? {note: hit.getAttribute('data-note'), text: hit.textContent.slice(0, 30)} : null;
        }""", anchor_text)
        ok_el = el is not None
        results.append((rel, f'锚元素挂角标[{anchor_text}]', ok_el, str(el)))
        if ok_el:
            # 点击元素右上角打开便签
            box = pg.evaluate("""(t) => {
                const els = [...document.querySelectorAll('[data-note]')];
                const hit = els.find(e => e.textContent.includes(t));
                const r = hit.getBoundingClientRect();
                return {x: r.right - 10, y: r.top + 8};
            }""", anchor_text)
            pg.mouse.click(box['x'], box['y'])
            pg.wait_for_timeout(200)
            pin = pg.evaluate("""(n) => {
                const p = document.getElementById('proto-pin-' + n);
                if (!p) return null;
                return {open: p.classList.contains('pn-open'), text: p.innerText.slice(0, 220)};
            }""", el['note'])
            ok_pin = pin and pin['open'] and pin_kw in pin['text']
            results.append((rel, f'便签含要点[{pin_kw}]', bool(ok_pin), (pin['text'][:80] if pin else 'pin 未找到/未开')))
        pg.evaluate("localStorage.removeItem('proto-notes-on')")
    b.close()

fails = [r for r in results if not r[2]]
for rel, name, ok, info in results:
    print(f"[{'PASS' if ok else 'FAIL'}] {rel} | {name}" + (f" | {info}" if info and not ok else ''))
print(f"\nJS errors: {len(js_errors)}")
for e in js_errors:
    print('  ', e[:120])
print(f"\n门2 结果: {len(results)} 断言, FAIL={len(fails)}, JS0={len(js_errors) == 0}")
sys.exit(1 if fails or js_errors else 0)
