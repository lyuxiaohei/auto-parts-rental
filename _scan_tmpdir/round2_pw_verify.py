from playwright.sync_api import sync_playwright
import pathlib
base = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
r = []
def chk(n, c): r.append((n, bool(c)))
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1600,'height':900})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))

    # === 1. 应付 createModal 自由笔数 ===
    pg.goto((base/'财务协同'/'应付账单.html').as_uri())
    pg.wait_for_timeout(1000)
    pg.click('button:has-text("新建应付账单")')
    pg.wait_for_timeout(300)
    chk('I-1 初始2笔', pg.locator('#createModal [data-k="rate"]').count() == 2)
    pg.click('#createModal button:has-text("添加一笔")')
    pg.wait_for_timeout(200)
    chk('I-2 加一笔变3笔', pg.locator('#createModal [data-k="rate"]').count() == 3)
    # 删第3笔
    pg.locator("#createModal a[data-del]").last.click()
    pg.wait_for_timeout(200)
    cnt = pg.locator('#createModal [data-k="rate"]').count()
    chk('I-3 删笔回2笔', cnt == 2)
    # 互算 50% -> 42000
    pg.fill('#createModal input[data-k="rate"][data-i="0"]', '50')
    pg.wait_for_timeout(250)
    a0 = float(pg.locator('#createModal input[data-k="amt"][data-i="0"]').input_value().replace(',',''))
    chk('I-4 互算50%→42,000', abs(a0-42000)<1)
    # 剩余全排
    pg.click('#createModal button:has-text("剩余全排")')
    pg.wait_for_timeout(250)
    a1 = float(pg.locator('#createModal input[data-k="amt"][data-i="1"]').input_value().replace(',',''))
    chk('I-5 剩余全排→末笔42,000', abs(a1-42000)<1)
    body = pg.locator('#createModal .modal-body').inner_text()
    chk('I-6 合计/剩余实时显示', ('剩余' in body) and ('84,000' in body or '84000' in body.replace(',','')))
    # 超额红框
    pg.fill('#createModal input[data-k="amt"][data-i="0"]', '90000')
    pg.wait_for_timeout(250)
    bc = pg.locator('#createModal input[data-k="amt"][data-i="0"]').evaluate('el=>el.style.borderColor')
    chk('I-7 超额红框', '255, 77, 79' in bc or 'ff4d4f' in bc)
    pg.screenshot(path='_scan_tmpdir/r2-应付-createModal-自由笔数.png')

    # === 2. f01-fab 三层抽查 ===
    # 2a 根级页：我的待办
    pg.goto((base/'我的待办.html').as_uri())
    pg.wait_for_timeout(800)
    chk('F-1 根级页有fab', pg.locator('.f01-fab, #f01Fab, [class*="f01-fab"]').count() >= 1)
    # 点击真实跳转
    pg.locator('[class*="f01-fab"]').first.click()
    pg.wait_for_timeout(1200)
    chk('F-2 点击跳转到F01', 'F01' in pg.url or '导航图' in (pg.title() or ''))
    pg.go_back(); pg.wait_for_timeout(600)
    # 2b 一层子目录：应付账单
    pg.goto((base/'财务协同'/'应付账单.html').as_uri())
    pg.wait_for_timeout(800)
    el = pg.locator('[class*="f01-fab"]').first
    chk('F-3 一层页fab存在', el.count() >= 1)
    # fab-row 并排 & 不重叠
    geo = pg.evaluate('''()=>{
      const f = document.querySelector('[class*="f01-fab"]');
      const p = document.querySelector('.pn-fab');
      if(!f) return null;
      const fr = f.getBoundingClientRect();
      const res = {f:[fr.x,fr.y,fr.width,fr.height]};
      if(p){ const pr = p.getBoundingClientRect(); res.p=[pr.x,pr.y,pr.width,pr.height];
        res.noOverlap = !(fr.x < pr.x+pr.width && pr.x < fr.x+fr.width && fr.y < pr.y+pr.height && pr.y < fr.y+fr.height);
        res.sameLine = Math.abs(fr.y - pr.y) < 5; }
      return res; }''')
    chk('F-4 与标注按钮不重叠', geo and geo.get('noOverlap'))
    chk('F-5 同一水平线', geo and geo.get('sameLine'))
    # href 指向正确
    href = pg.evaluate("()=>{const f=document.querySelector('[class*=\"f01-fab\"]');return (f.getAttribute('onclick')||'')+('|')+(f.querySelector('a')?f.querySelector('a').getAttribute('href'):'')} ")
    chk('F-6 一层页路径含 ../F01', '../P3-R01-F01' in href or 'P3-R01-F01' in href)
    pg.screenshot(path='_scan_tmpdir/r2-fabrow-应付.png')
    # 2c 两层深：弹窗预览页
    pg.goto((base/'租赁管理'/'弹窗'/'租入归还新建.html').as_uri())
    pg.wait_for_timeout(800)
    z = pg.evaluate("()=>{const f=document.querySelector('[class*=\"f01-fab\"]');if(!f)return null;return {z:getComputedStyle(f).zIndex, txt:(f.getAttribute('onclick')||'')}}")
    chk('F-7 两层页fab存在+z-index≥1000', z and int(z['z'] or 0) >= 1000)
    chk('F-8 两层页路径../../F01', '../../P3-R01-F01' in (z['txt'] if z else ''))
    # F01 自身
    pg.goto((base/'P3-R01-F01-业务流程导航图.html').as_uri())
    pg.wait_for_timeout(800)
    chk('F-9 F01自身无fab', pg.locator('[class*="f01-fab"]').count() == 0)
    chk('JS错误0', len(errs)==0)
    b.close()
ok = sum(1 for _,c in r if c)
for n,c in r: print(('PASS' if c else 'FAIL'), n)
print(f'== PASS {ok} / FAIL {len(r)-ok} ==')
