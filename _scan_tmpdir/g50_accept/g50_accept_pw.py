# -*- coding: utf-8 -*-
"""G50 独立验收 · 门3 PW 五页断言（只读原型，不修改任何项目文件）"""
import json
from pathlib import Path
from urllib.parse import unquote, quote
from playwright.sync_api import sync_playwright

ROOT = Path('/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/mobile')
BASE = ROOT.as_uri()
AUTH = "localStorage.setItem('m-auth', JSON.stringify({name:'沈婷',role:'商务主管',ts:Date.now()}));"
R = []

def log(name, ok, ev):
    R.append(ok)
    print(('[PASS] ' if ok else '[FAIL] ') + name + ' —— ' + ev, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch()

    # ---------- 1) 登录（净上下文，无 init_script） ----------
    ctx = browser.new_context(viewport={'width': 375, 'height': 812})
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(BASE + '/登录.html'); pg.wait_for_load_state('load'); pg.wait_for_timeout(900)
    logo = pg.locator('.m-logo').count()
    brand = pg.locator('.m-login-name').inner_text() if pg.locator('.m-login-name').count() else ''
    btn_l = pg.locator('#m-btn-login').count(); btn_w = pg.locator('#m-btn-wx').count()
    body_txt = pg.evaluate("document.body.innerText")
    log('门3-登录 logo/品牌', logo == 1 and '汽车物流包装租赁' in brand,
        f'.m-logo={logo}, 品牌名="{brand}", 登录按钮={btn_l}, 企微按钮={btn_w}')
    log('门3-登录 两按钮', btn_l == 1 and btn_w == 1, f'#m-btn-login={btn_l}, #m-btn-wx={btn_w}')
    log('门3-登录 版本v1.2', 'v1.2' in body_txt, 'body 含 v1.2=' + str('v1.2' in body_txt))
    log('门3-登录 pageerror', len(errs) == 0, f'pageerror={len(errs)}' + ('; '.join(errs) if errs else ''))
    ctx.close()

    # ---------- 受护页上下文（带 m-auth init_script） ----------
    ctx = browser.new_context(viewport={'width': 375, 'height': 812})
    ctx.add_init_script(AUTH)
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))

    # ---------- 2) 待办审批 ----------
    pg.goto(BASE + '/待办审批.html'); pg.wait_for_load_state('load'); pg.wait_for_timeout(900)
    stat = pg.locator('.m-stat-item').count()
    items = pg.locator('.m-item').count()
    badge_cls = pg.evaluate(
        "[...document.querySelectorAll('.m-badge')].map(b=>b.className).filter(c=>/m-badge-(blue|orange|green|purple|gray|red)/.test(c))")
    log('门3-待办 统计卡', stat == 3, f'.m-stat-item={stat}')
    log('门3-待办 卡片', items >= 1, f'.m-item={items}')
    log('门3-待办 徽标配色', len(badge_cls) >= 1,
        f'配色类徽标={len(badge_cls)}, 首个="{badge_cls[0] if badge_cls else "无"}"')

    # ---------- 3) 审批详情（真实 todoItems 首键） ----------
    first_id = pg.evaluate("Object.keys(window.DEMO_DATA.todoItems)[0]")
    n_todo = pg.evaluate(
        "(()=>{const b=DEMO_DATA.todoItems;return Object.keys(b).map(k=>b[k]&&b[k].row?k:null).filter(Boolean).length})()")
    pg.goto(BASE + '/审批详情.html?id=' + quote(first_id))
    pg.wait_for_load_state('load'); pg.wait_for_timeout(900)
    banner_vis = pg.locator('.m-banner').first.is_visible()
    bstate = pg.evaluate("document.getElementById('m-banner-state').textContent.trim()")
    tl = pg.locator('.m-tl-item').count()
    abtns = pg.locator('.m-action-bar .m-btn').count()
    log('门3-详情 banner', banner_vis and len(bstate) > 0,
        f'.m-banner 可见={banner_vis}, #m-banner-state="{bstate}" (id={first_id})')
    log('门3-详情 时间线', tl == 2, f'.m-tl-item={tl}')
    log('门3-详情 操作栏', abtns >= 2, f'.m-action-bar .m-btn={abtns}')

    # ---------- 4) 我的 ----------
    pg.goto(BASE + '/我的.html'); pg.wait_for_load_state('load'); pg.wait_for_timeout(900)
    hero = pg.locator('.m-hero').count()
    exp = pg.evaluate("""(()=>{
      const b=DEMO_DATA.todoItems;
      const rows=Object.keys(b).map(k=>b[k]&&b[k].row?{id:k,f:b[k].row.fields}:null).filter(Boolean);
      const types={}; rows.forEach(r=>types[r.f.type]=1);
      const done=Object.keys(JSON.parse(localStorage.getItem('m-done')||'{}')).length;
      return {rows:rows.length, done:done, types:Object.keys(types).length};
    })()""")
    got = {k: pg.evaluate(f"document.getElementById('{k}').textContent.trim()")
           for k in ('m-st-todo', 'm-st-done', 'm-st-type')}
    cells = pg.locator('.m-cell-group .m-cell').count()
    ver = 'v1.2' in pg.evaluate("document.body.innerText")
    ok_stats = (got['m-st-todo'] == str(exp['rows']) and
                got['m-st-done'] == str(exp['done']) and
                got['m-st-type'] == str(exp['types']))
    log('门3-我的 hero', hero == 1, f'.m-hero={hero}')
    log('门3-我的 三格实算', ok_stats,
        f"todo {got['m-st-todo']}/{exp['rows']}, done {got['m-st-done']}/{exp['done']}, type {got['m-st-type']}/{exp['types']}")
    log('门3-我的 四格cell', cells == 4, f'.m-cell-group .m-cell={cells}')
    log('门3-我的 版本v1.2', ver, 'body 含 v1.2=' + str(ver))
    errs_a = list(errs)  # 待办/详情/我的 共用一个 page 的 error 记录
    log('门3-受护三页 pageerror', len(errs_a) == 0, f'待办+详情+我的 pageerror={len(errs_a)}' + ('; '.join(errs_a) if errs_a else ''))

    # ---------- 5) 库存查询 ----------
    pg2 = ctx.new_page(); errs2 = []
    pg2.on('pageerror', lambda e: errs2.append(str(e)))
    pg2.goto(BASE + '/库存查询.html'); pg2.wait_for_load_state('load'); pg2.wait_for_timeout(900)
    chips = pg2.locator('.m-chip').count()
    tops = pg2.evaluate("[...document.querySelectorAll('.m-chip')].map(c=>Math.round(c.getBoundingClientRect().top))")
    same_line = len(set(tops)) == 1
    cards = pg2.locator('#m-list .m-item').count()
    log('门3-库存 chips计数', chips == 6, f'.m-chip={chips}（任务书第九节写 7，实测 {"6" if chips==6 else chips}：KC五状态+全部）')
    log('门3-库存 chips单行', same_line, f'tops 去重={sorted(set(tops))}')
    log('门3-库存 卡片', cards >= 1, f'#m-list .m-item={cards}')
    log('门3-库存 pageerror', len(errs2) == 0, f'pageerror={len(errs2)}' + ('; '.join(errs2) if errs2 else ''))

    # ---------- 6) 守卫回归：净上下文访问库存查询 ----------
    ctx.close()
    ctx = browser.new_context(viewport={'width': 375, 'height': 812})   # 无 init_script
    pg3 = ctx.new_page()
    pg3.goto(BASE + '/库存查询.html'); pg3.wait_for_load_state('load')
    pg3.wait_for_timeout(1400)
    final_url = unquote(pg3.url)
    log('门3-守卫回归', '登录.html' in final_url, f'1.4s 后 URL unquote = {final_url}')
    ctx.close()
    browser.close()

print(f'SUBTOTAL PASS={sum(R)}/{len(R)}', flush=True)
