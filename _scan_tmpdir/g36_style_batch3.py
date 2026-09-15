# -*- coding: utf-8 -*-
"""第三轮：标签冒号一致性 + 备注控件视觉规格 + 全角/半角标点"""
import asyncio, os
from playwright.async_api import async_playwright

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

PAGES = ['采购管理/采购订单新建.html',
         '基础数据/物料新建.html', '基础数据/客商新建.html', '基础数据/库位新建.html', '基础数据/客商开票资料.html',
         '项目管理/项目新建.html', '项目管理/上下游绑定.html', '项目管理/编码规则.html',
         '采购管理/采购退货新建.html', '销售管理/销售订单新建.html', '销售管理/销售出库新建.html', '销售管理/销售退货新建.html',
         '租赁管理/租赁单新建.html', '租赁管理/退租入库新建.html', '租入管理/租入单新建.html', '租入管理/租入归还新建.html',
         '仓储作业/其他入库新建.html', '仓储作业/其他出库新建.html', '仓储作业/调拨新建.html',
         '财务协同/付款新建.html', '财务协同/应付新建.html', '财务协同/应收生成.html', '财务协同/开票新建.html',
         '财务协同/收款新建.html', '财务协同/退款新建.html',
         '系统管理/字典项新建.html', '系统管理/用户新建.html', '系统管理/角色新建.html', '系统管理/权限配置.html']

def url(rel):
    return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')

PROBE = """() => {
    var labels = Array.from(document.querySelectorAll('.form-row .form-label')).map(function (l) {
        return l.textContent.replace(/\\s+/g, '');
    });
    var noColon = labels.filter(function (t) { return t && t.indexOf('：') < 0 && t.indexOf(':') < 0; });
    var ta = document.querySelector('.form-row textarea');
    var inp = null;
    var rows = Array.from(document.querySelectorAll('.form-row'));
    for (var i = 0; i < rows.length; i++) {
        var lb = rows[i].querySelector('.form-label');
        if (lb && lb.textContent.indexOf('备注') > -1) {
            var e = rows[i].querySelector('textarea') || rows[i].querySelector('input');
            if (e) { var cs = getComputedStyle(e); inp = {tag: e.tagName, h: Math.round(e.getBoundingClientRect().height), shell: !!e.closest('.input-box'), resize: cs.resize}; }
            break;
        }
    }
    return {noColon: noColon, note: inp};
}"""

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        print('==== 标签缺冒号 / 备注控件规格（样板：备注=textarea·h=72·.input-box 外壳）====')
        for p in PAGES:
            await pg.goto(url(p))
            await pg.wait_for_timeout(240)
            r = await pg.evaluate(PROBE)
            tag = '样板' if '采购订单新建' in p else '    '
            parts = []
            if r['noColon']:
                parts.append('缺冒号标签=%s' % r['noColon'])
            if r['note']:
                n = r['note']
                mark = '' if (n['tag'] == 'TEXTAREA' and n['h'] == 72 and n['shell']) else '  <<< 不符'
                parts.append('备注=%s h=%s 外壳=%s%s' % (n['tag'], n['h'], n['shell'], mark))
            print('%s %-28s %s' % (tag, p.split('/')[-1], ' | '.join(parts) if parts else '(正常)'))
        await b.close()

asyncio.run(main())
