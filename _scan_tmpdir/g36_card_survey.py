# -*- coding: utf-8 -*-
"""全量普查：新建/录单页的卡片划分与标题一致性"""
import asyncio, os, io, json
from playwright.async_api import async_playwright

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

PAGES = [
    # 样板
    '采购管理/采购订单新建.html',
    # 采购
    '采购管理/采购退货新建.html', '采购管理/采购入库录单.html',
    # 销售
    '销售管理/销售订单新建.html', '销售管理/销售出库新建.html', '销售管理/销售退货新建.html',
    # 租赁 / 租入
    '租赁管理/租赁单新建.html', '租赁管理/退租入库新建.html', '租赁管理/租赁出库录单.html',
    '租入管理/租入单新建.html', '租入管理/租入归还新建.html',
    # 仓储
    '仓储作业/其他入库新建.html', '仓储作业/其他出库新建.html', '仓储作业/调拨新建.html', '仓储作业/盘点录入.html',
    # 财务
    '财务协同/付款新建.html', '财务协同/应付新建.html', '财务协同/应收生成.html',
    '财务协同/开票新建.html', '财务协同/收款新建.html', '财务协同/退款新建.html',
    # 系统
    '系统管理/字典项新建.html', '系统管理/用户新建.html', '系统管理/角色新建.html', '系统管理/权限配置.html',
    # 基础数据 / 项目
    '基础数据/物料新建.html', '基础数据/客商新建.html', '基础数据/库位新建.html',
    '基础数据/客商开票资料.html', '基础数据/客商收货信息.html',
    '项目管理/项目新建.html', '项目管理/上下游绑定.html', '项目管理/编码规则.html',
    '基础数据/BOM维护.html',
]

PROBE = """() => {
    var c = document.querySelector('.content');
    if (!c) return {err: 'no .content'};
    var kids = [];
    Array.from(c.children).forEach(function (e) {
        var cs = getComputedStyle(e);
        var b = e.getBoundingClientRect();
        var t = e.querySelector('.card-title');
        var heads = e.querySelectorAll('.card-head').length;
        var innerHeads = Array.from(e.querySelectorAll('.card-title, .dt-sec, [style*="font-weight"]')).filter(function (h) {
            // 排除表内元素（表头/合计行）与提示行——它们不是分段标题
            return !h.closest('table') && !h.closest('.pn-hint') && !h.classList.contains('pn-hint');
        }).slice(0, 6).map(function (h) {
            var hcs = getComputedStyle(h);
            return {tag: h.tagName, cls: (h.className || '').slice(0, 22), txt: (h.textContent || '').trim().slice(0, 20),
                    fs: hcs.fontSize, fw: hcs.fontWeight, inHead: !!h.closest('.card-head')};
        });
        kids.push({tag: e.tagName, cls: (e.className || '').slice(0, 30), w: Math.round(b.width), h: Math.round(b.height),
                   bg: cs.backgroundColor, headCount: heads, title: t ? t.textContent.trim() : null,
                   titleFS: t ? getComputedStyle(t).fontSize : null,
                   hasTable: !!e.querySelector('table'), inner: innerHeads});
    });
    return {kids: kids, bar: !!c.querySelector('.submit-bar')};
}"""


async def main():
    rows = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        for p in PAGES:
            fp = os.path.join(ROOT, p.replace('/', os.sep))
            if not os.path.exists(fp):
                rows.append((p, 'MISSING', []))
                continue
            await pg.goto('file:///' + fp.replace('\\', '/'))
            await pg.wait_for_timeout(250)
            r = await pg.evaluate(PROBE)
            issues = []
            kids = r['kids']
            cards = [k for k in kids if 'card' in k['cls']]
            others = [k for k in kids if 'card' not in k['cls'] and 'submit-bar' not in k['cls']]
            if others:
                issues.append('内容区非卡片块 ×%d: %s' % (len(others), [o['cls'][:18] or o['tag'] for o in others]))
            for k in cards:
                if not k['title']:
                    issues.append('卡片无标题(%s)' % k['cls'][:18])
            # 卡内分段标题（应独立成卡）
            for k in cards:
                for h in k['inner']:
                    if not h['inHead'] and h['txt'] and (h['fw'] in ('600', '700', 'bold') or h['fs'] not in ('13px', '12px')):
                        issues.append('卡内分段标题「%s」未成卡（%s/%s）' % (h['txt'], h['fs'], h['fw']))
            rows.append((p, r, issues))
        await b.close()

    print('%-30s %-6s %s' % ('页面', '卡片数', '问题'))
    print('-' * 110)
    for p, r, iss in rows:
        if isinstance(r, str):
            print('%-30s %-6s %s' % (p.split('/')[-1], '-', r))
            continue
        cards = [k for k in r['kids'] if 'card' in k['cls']]
        print('%-30s %-6d %s' % (p.split('/')[-1], len(cards), ' | '.join(iss) if iss else 'OK'))
        for k in cards:
            print('        └ 卡: %-22s 标题=%-16s 标题字号=%-6s 含表=%s' % (k['cls'][:22], k['title'] or '(无)', k['titleFS'] or '-', k['hasTable']))
    print()
    print('==== 汇总 ====')
    print('页面数 %d ｜ 有问题 %d' % (len(rows), sum(1 for _, r, i in rows if isinstance(r, dict) and i)))

asyncio.run(main())
