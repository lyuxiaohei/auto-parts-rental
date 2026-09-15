# -*- coding: utf-8 -*-
"""修复前后渲染等价性验证：备份页临时就位 → 同页对比几何量 → 清理"""
import asyncio, os, shutil
from playwright.async_api import async_playwright

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
BAK = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-g36-balance-20260915'
CASES = ['仓储作业/其他入库列表.html', '租入管理/租入入库列表.html', '我的待办.html',
         '采购管理/采购订单列表.html', '财务协同/应付账单.html']

MEASURE = """() => {
    function r(sel) { var e = document.querySelector(sel); if (!e) return null; var b = e.getBoundingClientRect();
        return [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)]; }
    var fab = document.querySelector('.f01-fab');
    var pnf = document.querySelector('.pn-fab');
    return {
        scrollH: document.body.scrollHeight,
        scrollW: document.body.scrollWidth,
        nDiv: document.querySelectorAll('div').length,
        nEl: document.querySelectorAll('*').length,
        tbl: r('table'),
        content: r('.content'),
        sidebar: r('.sidebar'),
        fab: fab ? [Math.round(fab.getBoundingClientRect().right), Math.round(fab.getBoundingClientRect().bottom)] : null,
        pnfab: pnf ? [Math.round(pnf.getBoundingClientRect().right), Math.round(pnf.getBoundingClientRect().bottom)] : null,
        bodyKids: Array.from(document.body.children).map(function (e) { return e.tagName; }).join(',')
    };
}"""


def url(rel):
    return 'file:///' + os.path.join(ROOT, rel).replace('\\', '/')


def precheck_rel(rel):
    parts = rel.split('/')
    return ('/'.join(parts[:-1]) + '/' if len(parts) > 1 else '') + '_precheck_' + parts[-1]


def scratch_path(rel):
    parts = rel.split('/')
    sub = os.path.join(ROOT, *parts[:-1]) if len(parts) > 1 else ROOT
    return os.path.join(sub, '_precheck_' + parts[-1])


async def main():
    # 清理任何遗留
    for dp, dn, fns in os.walk(ROOT):
        for f in fns:
            if '_precheck_' in f:
                os.remove(os.path.join(dp, f))
                print('清理遗留:', f)
    made = []
    try:
        for rel in CASES:
            shutil.copy2(os.path.join(BAK, rel.replace('/', os.sep)), scratch_path(rel))
            made.append(scratch_path(rel))
        async with async_playwright() as pw:
            b = await pw.chromium.launch()
            pg = await b.new_page(viewport={'width': 1440, 'height': 900})
            for rel in CASES:
                await pg.goto(url(rel)); await pg.wait_for_timeout(500)
                cur = await pg.evaluate(MEASURE)
                await pg.goto(url(precheck_rel(rel))); await pg.wait_for_timeout(500)
                pre = await pg.evaluate(MEASURE)
                diffs = ['%s: %s → %s' % (k, pre[k], cur[k]) for k in cur if cur[k] != pre[k]]
                print('%-30s %s' % (rel.split('/')[-1], '渲染一致 ✓' if not diffs else '差异: ' + ' | '.join(diffs)))
            await b.close()
    finally:
        for f in made:
            if os.path.exists(f):
                os.remove(f)
        left = [f for dp, dn, fns in os.walk(ROOT) for f in fns if '_precheck_' in f]
        print('临时文件已清理；残留 =', len(left))

asyncio.run(main())
