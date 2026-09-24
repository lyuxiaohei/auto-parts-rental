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
        await pg.goto(B + '/系统管理/数据字典.html')
        await pg.wait_for_timeout(800)

        n = await pg.evaluate("document.querySelectorAll('#dicGroupList .dic-item').length")
        out.append('%s 左栏分组数(期望28): %d' % ('PASS' if n == 28 else 'FAIL', n))
        items = await pg.evaluate("[...document.querySelectorAll('#dicGroupList .dic-item')].slice(0,3).map(x=>x.innerText.replace(/\\n/g,' '))")
        out.append('左栏前三项: %s' % items)
        cnts = await pg.evaluate("(() => { const o={}; document.querySelectorAll('#dicGroupList .dic-item').forEach(x=>{const s=x.querySelectorAll('span'); o[s[0].textContent.trim()]=+s[1].textContent.trim();}); return o; })()")
        out.append('%s 计数抽查: 计费方式=%s 缺损类型=%s 库存状态=%s 待办单据类型=%s 结算周期=%s' % (
            'PASS' if cnts.get('计费方式') == 6 and cnts.get('库存状态') == 5 and cnts.get('待办单据类型') == 20 and cnts.get('结算周期') == 9 else 'FAIL',
            cnts.get('计费方式'), cnts.get('缺损类型'), cnts.get('库存状态'), cnts.get('待办单据类型'), cnts.get('结算周期')))
        t = await pg.evaluate("document.getElementById('dicItemTitle').innerText")
        rows = await pg.evaluate("document.querySelectorAll('#dicItemBody tr').length")
        out.append('%s 默认分类: 标题=%s 行数=%d' % ('PASS' if rows == cnts.get(items[0].split(' ')[0]) else 'FAIL', t, rows))

        # 切换 库存状态
        await pg.locator('#dicGroupList .dic-item', has_text='库存状态').first.click()
        await pg.wait_for_timeout(300)
        t2 = await pg.evaluate("document.getElementById('dicItemTitle').innerText")
        r2 = await pg.evaluate("[...document.querySelectorAll('#dicItemBody tr td:first-child')].map(x=>x.innerText.trim())")
        active = await pg.evaluate("document.querySelector('#dicGroupList .dic-item.active span').innerText.trim()")
        out.append('%s 切换库存状态: 标题=%s active=%s 行=%s' % ('PASS' if '库存状态' in t2 and active == '库存状态' and len(r2) == 5 else 'FAIL', t2, active, r2))

        # 切 计费方式（? 圆标锚）
        await pg.locator('#dicGroupList .dic-item', has_text='计费方式').first.click()
        await pg.wait_for_timeout(300)
        t3 = await pg.evaluate("document.getElementById('dicItemTitle').innerText")
        r3 = await pg.evaluate("document.querySelectorAll('#dicItemBody tr').length")
        q = await pg.evaluate("!!document.querySelector('#dicGroupList .dic-item[data-note=\"2\"] .pn-q')")
        out.append('%s 切换计费方式: 标题=%s 行=%d · 项上?圆标=%s' % ('PASS' if '计费方式' in t3 and r3 == 6 else 'FAIL', t3, r3, q))

        # 无常驻「计费方式」卡：卡片数应为 2（左栏列表 + 右栏字典项卡）
        cards = await pg.evaluate("document.querySelectorAll('.content .card').length")
        out.append('%s 内容区卡片数(期望1·另一为dic-list非card): %d' % ('PASS' if cards == 1 else 'FAIL', cards))

        # 停用弹窗回归
        await pg.locator('#dicItemBody tr').first.locator('a', has_text='停用').click()
        await pg.wait_for_timeout(300)
        modal = await pg.evaluate("document.getElementById('stopModal').classList.contains('show')")
        out.append('%s 停用弹窗可开: %s' % ('PASS' if modal else 'FAIL', modal))
        out.append('JS 错: %s %s' % (len(errs), errs[:3]))

        await pg.goto(B + '/系统管理/数据字典.html'); await pg.wait_for_timeout(700)
        await pg.screenshot(path='_scan_tmpdir/g72_dict.png')
        await b.close()
    print('\n'.join(out))

asyncio.run(main())
