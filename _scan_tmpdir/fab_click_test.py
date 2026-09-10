from playwright.sync_api import sync_playwright
import pathlib
base = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto((base/'我的待办.html').as_uri()); pg.wait_for_timeout(600)
    pg.locator('a.f01-fab').click(); pg.wait_for_timeout(1000)
    print('jump-ok:', 'F01' in pg.url)
    pg.goto((base/'财务协同'/'应付账单.html').as_uri()); pg.wait_for_timeout(600)
    geom = pg.evaluate("""()=>{const f=document.querySelector('a.f01-fab');const p=document.querySelector('.pn-fab');
      const fr=f.getBoundingClientRect(),pr=p.getBoundingClientRect();
      return {noOverlap:!(fr.x<pr.x+pr.width&&pr.x<fr.x+fr.width&&fr.y<pr.y+pr.height&&pr.y<fr.y+fr.height), sameLine:Math.abs(fr.y-pr.y)<5}}""")
    print('geom:', geom)
    b.close()
