# -*- coding: utf-8 -*-
"""批量渲染实测 75 页：控件宽/textarea/提交条/顶部返回列表冗余"""
import asyncio, os, io, re
from playwright.async_api import async_playwright

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

PAGES = [l.strip() for l in io.open(os.path.join(BASE, '..', '_scan_tmpdir', 'g36pages.txt'), encoding='utf-8') if l.strip() and not l.startswith('_scan_tmpdir')] if os.path.exists(os.path.join(BASE, '..', '_scan_tmpdir', 'g36pages.txt')) else []

# 内联完整清单（不依赖外部文件）
PAGES = [
    '基础数据/物料新建.html', '基础数据/客商新建.html', '基础数据/库位新建.html', '基础数据/客商开票资料.html',
    '基础数据/客商收货信息.html', '基础数据/物料详情.html', '基础数据/客商详情.html', '基础数据/库位详情.html',
    '基础数据/BOM版本查看.html', '项目管理/项目新建.html', '项目管理/上下游绑定.html', '项目管理/编码规则.html',
    '采购管理/采购订单详情.html', '采购管理/采购订单审核.html', '采购管理/采购入库详情.html', '采购管理/采购入库审核.html',
    '采购管理/采购退货详情.html', '采购管理/采购退货审核.html', '采购管理/采购退货新建.html',
    '销售管理/销售订单详情.html', '销售管理/销售订单审核.html', '销售管理/销售订单新建.html',
    '销售管理/销售出库详情.html', '销售管理/销售出库审核.html', '销售管理/销售出库新建.html',
    '销售管理/销售退货详情.html', '销售管理/销售退货审核.html', '销售管理/销售退货新建.html',
    '租赁管理/租赁单详情.html', '租赁管理/租赁单审核.html', '租赁管理/租赁单新建.html',
    '租赁管理/租赁出库详情.html', '租赁管理/租赁出库确认.html', '租赁管理/退租入库详情.html',
    '租赁管理/退租入库审核.html', '租赁管理/退租入库新建.html', '租赁管理/器具出租履历.html',
    '租入管理/租入单详情.html', '租入管理/租入单审核.html', '租入管理/租入单新建.html',
    '租入管理/租入入库详情.html', '租入管理/租入入库确认.html', '租入管理/租入归还详情.html',
    '租入管理/租入归还审核.html', '租入管理/租入归还新建.html',
    '仓储作业/其他入库详情.html', '仓储作业/其他入库审核.html', '仓储作业/其他入库新建.html',
    '仓储作业/其他出库详情.html', '仓储作业/其他出库审核.html', '仓储作业/其他出库新建.html',
    '仓储作业/库存流水.html', '仓储作业/盘点详情.html', '仓储作业/盘点审核.html',
    '仓储作业/调拨详情.html', '仓储作业/调拨审核.html', '仓储作业/调拨新建.html',
    '财务协同/付款新建.html', '财务协同/付款详情.html', '财务协同/付款确认.html', '财务协同/回款详情.html',
    '财务协同/应付新建.html', '财务协同/应付详情.html', '财务协同/应收生成.html', '财务协同/应收详情.html',
    '财务协同/开票新建.html', '财务协同/开票详情.html', '财务协同/收款新建.html', '财务协同/水单核销详情.html',
    '财务协同/退款新建.html', '财务协同/退款详情.html',
    '系统管理/字典项新建.html', '系统管理/用户新建.html', '系统管理/角色新建.html', '系统管理/权限配置.html',
]

def url(rel):
    return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')

PROBE = """() => {
    var ws = {};
    document.querySelectorAll('.form-row > div > .input-box').forEach(function (b) {
        var w = Math.round(b.getBoundingClientRect().width);
        ws[w] = (ws[w] || 0) + 1;
    });
    var tas = Array.from(document.querySelectorAll('textarea')).map(function (t) {
        var cs = getComputedStyle(t);
        return {h: Math.round(t.getBoundingClientRect().height), minH: cs.minHeight, resize: cs.resize};
    });
    var bar = document.querySelector('.submit-bar');
    var headBack = Array.from(document.querySelectorAll('.card-head .head-btns button')).some(function (b) {
        return b.textContent.indexOf('返回') > -1;
    });
    return {ws: ws, tas: tas, bar: !!bar, headBack: headBack};
}"""

async def main():
    rows = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        for p in PAGES:
            if not os.path.exists(os.path.join(BASE, p)):
                rows.append({'p': p, 'missing': True})
                continue
            await pg.goto(url(p))
            await pg.wait_for_timeout(260)
            r = await pg.evaluate(PROBE)
            r['p'] = p
            r['js'] = len(errs)
            errs.clear()
            rows.append(r)
        await b.close()

    print('==== 控件渲染宽异常（非 380，且非样板式三段式 116/72/220）====')
    n = 0
    for r in rows:
        if r.get('missing'):
            print('  MISSING', r['p']); continue
        ws = r['ws']
        bad = {k: v for k, v in ws.items() if k not in (380, 220, 116, 72)}
        if bad:
            print('  %-32s %s' % (r['p'], bad)); n += 1
    print('  小计 %d 页\n' % n)

    print('==== textarea 非样板规格（样板 h=72 minH=72px resize=vertical）====')
    n = 0
    for r in rows:
        if r.get('missing'): continue
        for t in r['tas']:
            if not (t['h'] == 72 and t['minH'] == '72px' and t['resize'] == 'vertical'):
                # 空 textarea 有时渲染略小，记录
                print('  %-32s h=%s minH=%s resize=%s' % (r['p'], t['h'], t['minH'], t['resize'])); n += 1
                break
    print('  小计 %d 页\n' % n)

    print('==== 顶部「返回列表」与提交条并存（规范：提交条已含取消则顶部不再放返回）====')
    n = 0
    for r in rows:
        if r.get('missing'): continue
        if r['bar'] and r['headBack']:
            print('  %-32s submit-bar + 返回列表' % r['p']); n += 1
    print('  小计 %d 页\n' % n)

    print('==== 无提交条的详情/查阅页（顶部应有返回列表）====')
    n = 0
    for r in rows:
        if r.get('missing'): continue
        if not r['bar'] and not r['headBack']:
            print('  %-32s 无提交条也无返回列表' % r['p']); n += 1
    print('  小计 %d 页\n' % n)

    print('==== JS 错误页 ====')
    for r in rows:
        if r.get('js'):
            print('  %-32s JS=%d' % (r['p'], r['js']))

asyncio.run(main())
