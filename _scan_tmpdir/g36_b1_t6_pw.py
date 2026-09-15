# -*- coding: utf-8 -*-
"""G36 B1 T6：新页 PW 抽验——JS 0/控件宽 380/提交条居中/结构（div 配平）/截图"""
import asyncio, os
from playwright.async_api import async_playwright

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
SHOTS = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g36_b1_shots'
os.makedirs(SHOTS, exist_ok=True)

FORM_PAGES = ['基础数据/物料新建.html', '基础数据/客商新建.html', '基础数据/库位新建.html',
              '基础数据/客商开票资料.html', '基础数据/客商收货信息.html',
              '项目管理/上下游绑定.html', '项目管理/项目新建.html', '项目管理/编码规则.html']
DETAIL_PAGES = ['基础数据/物料详情.html?id=WBX-1210L', '基础数据/客商详情.html?id=DW-0001',
                '基础数据/库位详情.html', '基础数据/BOM版本查看.html']

def url(rel):
    return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')

async def main():
    results = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)

        for p in FORM_PAGES:
            await pg.goto(url(p))
            await pg.wait_for_timeout(400)
            js0 = not errs; errs.clear()
            # 控件宽：取所有 .form-row 直系 .input-box 宽度（三段式分段不计）
            widths = await pg.evaluate("""() => {
                var out = [];
                document.querySelectorAll('.form-row > div > .input-box').forEach(function (b) {
                    out.push(Math.round(b.getBoundingClientRect().width));
                });
                return out;
            }""")
            uniq = sorted(set(widths))
            # 提交条
            bar = await pg.evaluate("""() => {
                var bar = document.querySelector('.submit-bar');
                if (!bar) return null;
                var cs = getComputedStyle(bar);
                var r = bar.getBoundingClientRect();
                var btns = bar.querySelectorAll('button');
                var br = btns.length ? btns[0].getBoundingClientRect() : null;
                var last = btns.length ? btns[btns.length - 1].getBoundingClientRect() : null;
                var leftGap = br ? Math.round(br.left - r.left) : -1;
                var rightGap = last ? Math.round(r.right - last.right) : -1;
                return {justify: cs.justifyContent, leftGap: leftGap, rightGap: rightGap, nbtns: btns.length};
            }""")
            # 取消按钮回列表
            cancel = await pg.evaluate("""() => {
                var b = document.querySelector('.submit-bar button.btn-default');
                return b ? (b.getAttribute('onclick') || '') : '';
            }""")
            ok_js = js0
            ok_w = all(340 <= w <= 400 for w in uniq)  # 380±复合行容差
            ok_bar = bar and bar['justify'] == 'center' and abs(bar['leftGap'] - bar['rightGap']) <= 40
            ok_cancel = cancel.startswith('go(')
            results.append((p, ok_js and ok_w and ok_bar and ok_cancel,
                            'JS=%s 宽集合=%s 条=%s 取消=%s' % (js0, uniq, bar, cancel[:36])))
            await pg.screenshot(path=os.path.join(SHOTS, p.split('/')[-1].replace('.html', '').replace('?id=', '_') + '.png'), full_page=True)

        for p in DETAIL_PAGES:
            await pg.goto(url(p))
            await pg.wait_for_timeout(400)
            js0 = not errs; errs.clear()
            dt = await pg.evaluate("""() => {
                var t = document.getElementById('dtTitle');
                var b = document.getElementById('detailBody');
                var back = document.querySelector('.card-head button');
                return {title: t ? t.textContent : '', segs: b ? b.querySelectorAll('.dt-sec').length : 0,
                        back: back ? (back.getAttribute('onclick') || '') : ''};
            }""")
            results.append((p, js0 and dt['segs'] >= 3 and dt['back'].startswith('go('),
                            'JS=%s %s segs=%d 返回=%s' % (js0, dt['title'][:16], dt['segs'], dt['back'][:28])))
            await pg.screenshot(path=os.path.join(SHOTS, p.split('/')[-1].split('?')[0].replace('.html', '_d') + '.png'), full_page=True)
        await b.close()

    fails = 0
    for name, okk, ev in results:
        print('[%s] %s | %s' % ('PASS' if okk else 'FAIL', name, ev))
        if not okk:
            fails += 1
    print('总判定：%d PASS / %d FAIL' % (len(results) - fails, fails))
    print('截图目录：_scan_tmpdir/g36_b1_shots/')

asyncio.run(main())
