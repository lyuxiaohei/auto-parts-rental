# -*- coding: utf-8 -*-
"""补充检查：控件宽（含 170 定位）+ 备注字段形态/位置 + 详情页结构 vs 详情样板"""
import asyncio, os, io, re
from playwright.async_api import async_playwright

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
SAMPLE_FORM = '采购管理/采购订单新建.html'
SAMPLE_DETAIL = '项目管理/项目详情.html'

FORMS = ['基础数据/物料新建.html', '基础数据/客商新建.html', '基础数据/库位新建.html', '基础数据/客商开票资料.html',
         '基础数据/客商收货信息.html', '项目管理/项目新建.html', '项目管理/上下游绑定.html', '项目管理/编码规则.html',
         '采购管理/采购退货新建.html', '销售管理/销售订单新建.html', '销售管理/销售出库新建.html', '销售管理/销售退货新建.html',
         '租赁管理/租赁单新建.html', '租赁管理/退租入库新建.html', '租入管理/租入单新建.html', '租入管理/租入归还新建.html',
         '仓储作业/其他入库新建.html', '仓储作业/其他出库新建.html', '仓储作业/调拨新建.html',
         '财务协同/付款新建.html', '财务协同/应付新建.html', '财务协同/应收生成.html', '财务协同/开票新建.html',
         '财务协同/收款新建.html', '财务协同/退款新建.html',
         '系统管理/字典项新建.html', '系统管理/用户新建.html', '系统管理/角色新建.html', '系统管理/权限配置.html']
DETAILS = ['基础数据/物料详情.html', '基础数据/客商详情.html', '基础数据/库位详情.html', '基础数据/BOM版本查看.html',
           '采购管理/采购订单详情.html', '采购管理/采购订单审核.html', '销售管理/销售订单详情.html',
           '租赁管理/租赁单详情.html', '租赁管理/租赁出库确认.html', '租入管理/租入单详情.html',
           '仓储作业/库存流水.html', '财务协同/应付详情.html', '财务协同/付款确认.html']

def url(rel):
    return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')

def rd(p):
    return io.open(os.path.join(BASE, p), encoding='utf-8', errors='ignore').read()

PROBE_BOX = """() => {
    var out = [];
    document.querySelectorAll('.form-row').forEach(function (r) {
        var lb = r.querySelector('.form-label');
        var boxes = Array.from(r.querySelectorAll('.input-box'));
        if (!boxes.length) return;
        out.push({label: lb ? lb.textContent.trim().replace(/\\s+/g, '') : '',
                  ws: boxes.map(function (b) { return Math.round(b.getBoundingClientRect().width); })});
    });
    return out;
}"""

PROBE_NOTE = """() => {
    var rows = Array.from(document.querySelectorAll('.card .form-row'));
    var noteIdx = -1, total = rows.length, noteKind = null;
    rows.forEach(function (r, i) {
        var lb = r.querySelector('.form-label');
        if (lb && lb.textContent.indexOf('备注') > -1) { noteIdx = i; noteKind = r.querySelector('textarea') ? 'textarea' : (r.querySelector('input') ? 'input' : '?'); }
    });
    return {noteIdx: noteIdx, total: total, isLast: noteIdx > -1 && noteIdx === total - 1, noteKind: noteKind, hasNote: noteIdx > -1};
}"""

PROBE_DETAIL = """() => {
    var card = document.querySelector('.content .card');
    return {
        dgridC3: !!document.querySelector('.dgrid.c3'),
        dgrid: !!document.querySelector('.dgrid'),
        dtSec: document.querySelectorAll('.dt-sec').length,
        chain: document.querySelectorAll('.chain .node').length,
        tl: document.querySelectorAll('.tl-i').length,
        drow: document.querySelectorAll('.drow').length,
        cardTitleId: (document.querySelector('.card-title') || {}).id || '',
        headBtns: Array.from(document.querySelectorAll('.card-head .head-btns button')).map(function (b) { return b.textContent.trim(); })
    };
}"""

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        # --- 控件宽 ---
        print('==== 控件渲染宽（非 380）明细 ====')
        await pg.goto(url(SAMPLE_FORM)); await pg.wait_for_timeout(300)
        sb = await pg.evaluate(PROBE_BOX)
        print('样板各行:', [(x['label'][:12], x['ws']) for x in sb])
        for p in FORMS:
            await pg.goto(url(p)); await pg.wait_for_timeout(250)
            rows = await pg.evaluate(PROBE_BOX)
            bad = [(x['label'][:16], x['ws']) for x in rows if any(w != 380 for w in x['ws'])]
            if bad:
                print('  %-30s %s' % (p.split('/')[-1], bad))
        # --- 备注 ---
        print()
        print('==== 备注字段（样板：textarea·位于表单卡末尾）====')
        await pg.goto(url(SAMPLE_FORM)); await pg.wait_for_timeout(300)
        print('样板:', await pg.evaluate(PROBE_NOTE))
        for p in FORMS:
            await pg.goto(url(p)); await pg.wait_for_timeout(250)
            r = await pg.evaluate(PROBE_NOTE)
            if not r['hasNote']:
                print('  %-30s 无备注字段' % p.split('/')[-1])
            elif r['noteKind'] != 'textarea' or not r['isLast']:
                print('  %-30s kind=%s isLast=%s (idx %d/%d)' % (p.split('/')[-1], r['noteKind'], r['isLast'], r['noteIdx'], r['total']))
        # --- 详情 ---
        print()
        print('==== 详情/审核页结构（详情样板=项目管理/项目详情.html）====')
        await pg.goto(url(SAMPLE_DETAIL)); await pg.wait_for_timeout(300)
        print('详情样板:', await pg.evaluate(PROBE_DETAIL))
        for p in DETAILS:
            await pg.goto(url(p)); await pg.wait_for_timeout(300)
            print('  %-28s %s' % (p.split('/')[-1], await pg.evaluate(PROBE_DETAIL)))
        await b.close()

asyncio.run(main())
