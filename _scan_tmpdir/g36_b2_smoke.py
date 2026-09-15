# -*- coding: utf-8 -*-
"""B2 冒烟：16 新页 JS/配平/宽度/提交条 + 6 宿主页渲染/悬空 openModal/运行时 ops"""
import asyncio, os, re
from playwright.async_api import async_playwright

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def url(rel):
    return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')

PAGES = ['采购管理/采购订单详情.html?id=PO-20260910-019', '采购管理/采购订单审核.html', '采购管理/采购入库详情.html', '采购管理/采购入库审核.html',
         '采购管理/采购退货详情.html', '采购管理/采购退货审核.html', '采购管理/采购退货新建.html',
         '销售管理/销售订单详情.html', '销售管理/销售订单审核.html', '销售管理/销售订单新建.html',
         '销售管理/销售出库详情.html', '销售管理/销售出库审核.html', '销售管理/销售出库新建.html',
         '销售管理/销售退货详情.html', '销售管理/销售退货审核.html', '销售管理/销售退货新建.html']
HOSTS = ['采购管理/采购订单列表.html', '采购管理/采购入库列表.html', '采购管理/采购退货单列表.html',
         '销售管理/销售订单列表.html', '销售管理/销售出库列表.html', '销售管理/销售退货单列表.html']

async def main():
    fails = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        for p in PAGES:
            await pg.goto(url(p))
            await pg.wait_for_timeout(350)
            js0 = not errs; errs.clear()
            widths = await pg.evaluate("""() => {
                var out = [];
                document.querySelectorAll('.form-row > div > .input-box').forEach(function (b) {
                    out.push(Math.round(b.getBoundingClientRect().width));
                });
                return out;
            }""")
            uniq = sorted(set(widths))
            bar = await pg.evaluate("""() => {
                var bar = document.querySelector('.submit-bar');
                if (!bar) return {ok: true};
                var btns = bar.querySelectorAll('button');
                if (!btns.length) return {ok: false};
                var r = bar.getBoundingClientRect();
                var l = btns[0].getBoundingClientRect(), rr = btns[btns.length-1].getBoundingClientRect();
                return {ok: getComputedStyle(bar).justifyContent === 'center' && Math.abs((l.left - r.left) - (r.right - rr.right)) <= 40};
            }""")
            segs = await pg.evaluate("() => document.querySelectorAll('.dt-sec').length")
            radios = await pg.evaluate("() => document.querySelectorAll('.radio').length")
            okk = js0 and bar.get('ok', True) and all(340 <= w <= 400 for w in uniq) if uniq else js0 and bar.get('ok', True)
            print('[%s] %-44s JS=%s 宽=%s 条=%s dt-sec=%s radio=%s' % ('PASS' if okk else 'FAIL', p.split('/')[-1][:40], js0, uniq or '-', bar.get('ok'), segs, radios))
            if not okk: fails += 1
        for h in HOSTS:
            await pg.goto(url(h))
            await pg.wait_for_timeout(450)
            rows = await pg.eval_on_selector_all('tbody tr', 'els=>els.length')
            dangling = await pg.evaluate("""() => {
                var bad = [];
                document.querySelectorAll("a[onclick*='openModal']").forEach(function (e) {
                    var rest = (e.getAttribute('onclick') || '').split("openModal('")[1];
                    if (rest) { var id = rest.split("'")[0]; if (!document.getElementById(id)) bad.push(id); }
                });
                return bad;
            }""")
            ops1 = await pg.eval_on_selector_all('tbody tr:first-child .ops a', 'els=>els.slice(0,3).map(e=>e.getAttribute("onclick")||e.textContent)')
            okk = (not errs) and not dangling and rows > 0
            errs.clear()
            print('[%s] %-30s rows=%d dangling=%s ops=%s' % ('PASS' if okk else 'FAIL', h.split('/')[-1], rows, dangling, ops1))
            if not okk: fails += 1
        # 待办 audit=1 残留（B2 域 4 条应为 0）
        await pg.goto(url('我的待办.html'))
        await pg.wait_for_timeout(400)
        left = await pg.evaluate("() => Array.from(document.querySelectorAll('[onclick]')).filter(e => (e.getAttribute('onclick')||'').indexOf('audit=1') > -1 && (e.getAttribute('onclick')||'').indexOf('采购') > -1 || (e.getAttribute('onclick')||'').indexOf('销售') > -1 && (e.getAttribute('onclick')||'').indexOf('audit=1') > -1).length")
        print('[%s] 我的待办 采购/销售 audit=1 残留 = %d' % ('PASS' if left == 0 else 'FAIL', left))
        if left: fails += 1
        await b.close()
    print('B2 冒烟总判定：%s' % ('ALL PASS' if fails == 0 else '%d FAIL' % fails))

asyncio.run(main())
