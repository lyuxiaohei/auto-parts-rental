import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

async def main():
    out = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console: ' + m.text) if m.type == 'error' else None)

        # ① 客商新建
        await pg.goto(B + '/基础数据/客商新建.html')
        await pg.wait_for_timeout(600)
        body = await pg.evaluate('document.body.innerText')
        cards = await pg.evaluate("[...document.querySelectorAll('.card')].map(c=>c.innerText).join('')")
        out.append('PASS? 新建页卡片区无协议税点: %s（抽屉注记含"退场"说明属预期）: %s' % ('协议税点' not in cards, '协议税点' in body))
        # 结算周期归属卡
        card = await pg.evaluate("(() => { const cards=[...document.querySelectorAll('.card')]; const c=cards.find(x=>x.querySelector('.card-title') && x.querySelector('.card-title').textContent.indexOf('基础信息')>-1); const ic=cards.find(x=>x.querySelector('.card-title') && x.querySelector('.card-title').textContent.indexOf('开票资料')>-1); return {base: c? c.innerText.indexOf('结算周期')>-1 : null, inv: ic? ic.innerText.indexOf('结算周期')>-1 : null}; })()")
        out.append('PASS? 结算周期在基础信息卡=%s 在开票资料卡=%s' % (card['base'], card['inv']))
        opts = await pg.evaluate("[...document.querySelectorAll('#ksInvTypeSel option')].map(o=>o.textContent)")
        out.append('PASS? 发票类型选项(%d): %s' % (len(opts), ' / '.join(opts)))
        # 添加开票资料组 → 组内无协议税点/结算周期
        await pg.evaluate('ksAddInvGroup()')
        await pg.wait_for_timeout(200)
        g2 = await pg.evaluate("(() => { const gs=[...document.querySelectorAll('.ks-inv-group')]; const g=gs[1]; return {n: gs.length, txt: g.innerText}; })()")
        out.append('PASS? 克隆第2组=%d · 组内含协议税点=%s 含结算周期=%s' % (g2['n'], '协议税点' in g2['txt'], '结算周期' in g2['txt']))
        await pg.screenshot(path='_scan_tmpdir/g68_partner_new.png')

        # ② 客商详情 DW-0001
        await pg.goto(B + '/基础数据/客商详情.html?id=DW-0001')
        await pg.wait_for_timeout(500)
        body = await pg.evaluate('document.body.innerText')
        out.append('PASS? 详情无协议税点: %s · 结算周期出现次数=%d · 纳税人识别号×2=%s' % ('协议税点' not in body, body.count('结算周期'), body.count('纳税人识别号')))
        infocard = await pg.evaluate("(() => { const cards=[...document.querySelectorAll('.card')]; const c=cards[0]; return c? c.innerText.indexOf('结算周期')>-1 : null; })()")
        out.append('PASS? 详情首卡含结算周期: %s' % infocard)

        # ③ 客商管理列表
        await pg.goto(B + '/基础数据/客商管理.html')
        await pg.wait_for_timeout(500)
        body = await pg.evaluate('document.body.innerText')
        out.append('PASS? 列表无协议税点: %s · 开票资料列示例含专票: %s' % ('协议税点' not in body, '增值税专票' in body))

        out.append('JS 错总数: %s %s' % (len(errs), errs[:3]))
        await b.close()
    print('\n'.join(out))

asyncio.run(main())
