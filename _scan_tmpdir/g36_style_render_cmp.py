# -*- coding: utf-8 -*-
"""渲染实测对比：样板 vs 偏差页（量 label 宽度/控件宽/箭头/textarea/卡片内距）"""
import asyncio, os, json
from playwright.async_api import async_playwright

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
SAMPLE = '采购管理/采购订单新建.html'
TARGETS = ['采购管理/采购退货新建.html', '财务协同/付款新建.html', '租赁管理/租赁单新建.html',
           '仓储作业/其他入库新建.html', '系统管理/用户新建.html', '租赁管理/退租入库新建.html',
           '基础数据/物料新建.html', '租入管理/租入单新建.html']

def url(rel):
    return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')

PROBE = """() => {
    function first(sel) { var e = document.querySelector(sel); return e; }
    var out = {};
    var lb = document.querySelector('.form-row .form-label');
    if (lb) {
        var r = lb.getBoundingClientRect(), cs = getComputedStyle(lb);
        out.label = {tag: lb.tagName, w: Math.round(r.width), ta: cs.textAlign, fs: cs.fontSize, disp: cs.display, flex: cs.flex};
    }
    var boxes = Array.from(document.querySelectorAll('.form-row .input-box')).slice(0, 4).map(function (b) {
        var cs = getComputedStyle(b), r = b.getBoundingClientRect();
        return {w: Math.round(r.width), h: Math.round(r.height), inline: b.getAttribute('style') || ''};
    });
    out.boxes = boxes;
    var car = document.querySelector('.input-box .caret');
    if (car) {
        var cr = car.getBoundingClientRect(), ccs = getComputedStyle(car);
        out.caret = {html: car.innerHTML.slice(0, 40), w: Math.round(cr.width), h: Math.round(cr.height), color: ccs.color};
    }
    var ta = document.querySelector('textarea');
    if (ta) {
        var tcs = getComputedStyle(ta), tr = ta.getBoundingClientRect();
        out.textarea = {h: Math.round(tr.height), minH: tcs.minHeight, resize: tcs.resize, border: tcs.borderTopWidth};
        var shell = ta.closest('.input-box');
        out.textareaShell = shell ? {has: true, h: Math.round(shell.getBoundingClientRect().height)} : {has: false};
    }
    var card = document.querySelector('.content .card');
    if (card) {
        var ccs2 = getComputedStyle(card);
        out.card = {pad: ccs2.padding, radius: ccs2.borderRadius, mb: ccs2.marginBottom};
    }
    var ct = document.querySelector('.content .card .card-title');
    if (ct) { var ccr = getComputedStyle(ct); out.cardTitle = {fs: ccr.fontSize, fw: ccr.fontWeight, mb: ccr.marginBottom}; }
    var row = document.querySelector('.form-row');
    if (row) out.rowMB = getComputedStyle(row).marginBottom;
    var bar = document.querySelector('.submit-bar');
    if (bar) { var bcs = getComputedStyle(bar); out.bar = {justify: bcs.justifyContent, pad: bcs.padding, left: bcs.left}; }
    return out;
}"""

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        res = {}
        for p in [SAMPLE] + TARGETS:
            await pg.goto(url(p))
            await pg.wait_for_timeout(320)
            res[p] = await pg.evaluate(PROBE)
        await b.close()
    base = res[SAMPLE]
    print('==== 样板 %s ====' % SAMPLE)
    print(json.dumps(base, ensure_ascii=False, indent=1))
    print()
    for p in TARGETS:
        r = res[p]
        diffs = []
        if 'label' in r and 'label' in base:
            if r['label']['tag'] != base['label']['tag']:
                diffs.append('label 标签 %s vs 样板 %s' % (r['label']['tag'], base['label']['tag']))
            for k in ('w', 'ta', 'fs', 'disp'):
                if r['label'].get(k) != base['label'].get(k):
                    diffs.append('label %s: %s vs %s' % (k, r['label'].get(k), base['label'].get(k)))
        bw = [x['w'] for x in base.get('boxes', [])]
        tw = [x['w'] for x in r.get('boxes', [])]
        if tw and bw and set(tw) != set(bw):
            diffs.append('控件渲染宽 %s vs 样板 %s' % (sorted(set(tw)), sorted(set(bw))))
        if r.get('caret') and base.get('caret'):
            if r['caret']['html'] != base['caret']['html']:
                diffs.append('箭头 html 不同（渲染 %sx%s vs %sx%s）' % (r['caret']['w'], r['caret']['h'], base['caret']['w'], base['caret']['h']))
        if r.get('textarea') and base.get('textarea'):
            for k in ('h', 'minH', 'resize', 'border'):
                if r['textarea'].get(k) != base['textarea'].get(k):
                    diffs.append('textarea %s: %s vs %s' % (k, r['textarea'].get(k), base['textarea'].get(k)))
        for kk in ('card', 'cardTitle', 'rowMB', 'bar'):
            if r.get(kk) != base.get(kk):
                diffs.append('%s: %s vs %s' % (kk, r.get(kk), base.get(kk)))
        print('--- %s' % p)
        if diffs:
            for d in diffs:
                print('    * %s' % d)
        else:
            print('    (渲染一致)')

asyncio.run(main())
