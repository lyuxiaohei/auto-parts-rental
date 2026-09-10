from playwright.sync_api import sync_playwright
import pathlib
base = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1600,'height':900})
    pg.goto((base/'财务协同'/'应付账单.html').as_uri())
    pg.wait_for_timeout(1000)
    pg.click('button:has-text("新建应付账单")')
    pg.wait_for_timeout(300)
    # 输出 createModal 内所有 input/select 的 id/value
    info = pg.evaluate('''() => {
      const m = document.querySelector('#createModal');
      const out = [];
      m.querySelectorAll('input,select').forEach(el=>{
        out.push({tag:el.tagName, id:el.id, dk:el.getAttribute('data-k'), di:el.getAttribute('data-i'), val:(el.value||'').slice(0,20)});
      });
      return out;
    }''')
    for i in info: print(i)
    # 互算测试：改第1期比例为 50
    pg.fill('#createModal input[data-k="rate"][data-i="0"]', '50')
    pg.wait_for_timeout(300)
    v = pg.evaluate('''() => {
      const m = document.querySelector('#createModal');
      return Array.from(m.querySelectorAll('input[data-k="amt"]')).map(e=>e.value);
    }''')
    print('改50%后金额行:', v)
    b.close()
