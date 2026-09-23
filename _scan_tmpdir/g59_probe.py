import asyncio, json, sys
from playwright.async_api import async_playwright

PROBE_JS = """
() => {
  window.__muts = [];
  new MutationObserver(ml => {
    for (const m of ml) {
      const t = m.target;
      window.__muts.push((m.attributeName ? 'attr:' + m.attributeName + '@' : m.type + '@') +
        t.nodeName + (t.id ? '#' + t.id : '') + (typeof t.className === 'string' && t.className ? '.' + t.className.trim().split(/\s+/).join('.') : ''));
    }
  }).observe(document.documentElement, { subtree: true, attributes: true, childList: true, characterData: true });
}
"""

async def probe(url, label):
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(url)
        await pg.evaluate(PROBE_JS)
        await pg.evaluate("openModal('importModal')")
        await pg.wait_for_timeout(150)
        await pg.evaluate("window.__muts=[]")
        await pg.locator('text=选择文件').click()
        await pg.wait_for_timeout(250)
        muts = await pg.evaluate("window.__muts")
        print(label, json.dumps(muts, ensure_ascii=False), '| JS错:', errs)
        await b.close()

if __name__ == '__main__':
    B = 'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'
    pages = [(B + '/采购管理/采购入库列表.html', 'G57采购入库'), (B + '/仓储作业/其他出库列表.html', 'G59其他出库')]
    for u, l in pages:
        asyncio.run(probe(u, l))
