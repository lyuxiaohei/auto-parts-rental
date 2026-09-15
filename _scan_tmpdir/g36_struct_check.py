# -*- coding: utf-8 -*-
"""全站结构体检：卡片是否被挤塌（宽度异常小）/ 内容区是否缺卡 / 提交条是否居中"""
import asyncio, os, io
from playwright.async_api import async_playwright

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

PAGES = []
for dp, dn, fns in os.walk(ROOT):
    if '.git' in dp:
        continue
    for f in sorted(fns):
        if f.endswith('.html'):
            PAGES.append(os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, '/'))
PAGES = [p for p in PAGES if not p.startswith('mobile/')]

PROBE = """() => {
    var c = document.querySelector('.content');
    var out = {cards: [], barJustify: null, hasBar: false, strayRow: 0};
    if (c) {
        Array.from(c.children).forEach(function (e) {
            var b = e.getBoundingClientRect();
            out.cards.push({cls: (e.className || '').slice(0, 24), w: Math.round(b.width), h: Math.round(b.height)});
        });
    }
    var bar = document.querySelector('.submit-bar');
    if (bar) { out.hasBar = true; out.barJustify = getComputedStyle(bar).justifyContent; }
    // 表单行是否脱离了卡片（父级不是 .card）
    Array.from(document.querySelectorAll('.form-row')).forEach(function (r) {
        var p = r.parentElement, inCard = false;
        while (p && p !== document.body) { if (p.classList && p.classList.contains('card')) { inCard = true; break; } p = p.parentElement; }
        if (!inCard && !r.closest('.modal-overlay')) out.strayRow++;  // 弹窗内表单行不属卡片体系
    });
    return out;
}"""


async def main():
    bad = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        for p in PAGES:
            await pg.goto('file:///' + os.path.join(ROOT, p).replace('\\', '/'))
            await pg.wait_for_timeout(230)
            try:
                r = await pg.evaluate(PROBE)
            except Exception as e:
                bad.append((p, ['探测失败: %s' % str(e)[:40]]))
                continue
            iss = []
            for k in r['cards']:
                if 'card' in k['cls'] and 0 < k['w'] < 300:
                    iss.append('卡片被挤塌 w=%d (%s)' % (k['w'], k['cls']))
            if r['strayRow']:
                iss.append('表单行脱离卡片 ×%d' % r['strayRow'])
            if r['hasBar'] and r['barJustify'] != 'center':
                iss.append('提交条未居中 (%s)' % r['barJustify'])
            if iss:
                bad.append((p, iss))
        await b.close()
    print('==== 结构体检异常页 %d / %d ====' % (len(bad), len(PAGES)))
    for p, iss in bad:
        print('  %-40s %s' % (p, ' | '.join(iss)))

asyncio.run(main())
