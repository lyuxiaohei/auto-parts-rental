# -*- coding: utf-8 -*-
"""G19a T3 Playwright：五页加载 JS 0 + 关键容器可见性 + 截图×5 留档"""
import pathlib, urllib.parse
from playwright.sync_api import sync_playwright

MOB = pathlib.Path(r'P3-R01-包装租赁管理后台原型/mobile').resolve()
OUT = pathlib.Path(r'_scan_tmpdir')
ok = True

with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page(viewport={'width': 375, 'height': 812})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)

    def shot(name):
        f = OUT / f'g19a-mobile-{name}.png'
        pg.screenshot(path=str(f), full_page=True)
        print(f'  [shot] {f.name} saved={f.exists()}')

    # ---- M01 登录（未登录态直开） ----
    pg.goto((MOB / '登录.html').as_uri())
    pg.wait_for_timeout(400)
    v = pg.locator('.m-login-hero .m-logo').is_visible()
    v2 = pg.locator('.m-card .m-field input#m-acc').is_visible()
    print(f'[M01 登录] hero={v} card-field={v2}'); ok &= (v and v2)
    shot('登录')

    # ---- M02 待办审批（预置 m-auth 免守卫跳转） ----
    pg.goto((MOB / '登录.html').as_uri())
    pg.evaluate("localStorage.setItem('m-auth', JSON.stringify({name:'王琳',role:'商务主管',ts:Date.now()}))")
    pg.goto((MOB / '待办审批.html').as_uri())
    pg.wait_for_timeout(600)
    v = pg.locator('.m-header').is_visible()
    n = pg.locator('.m-item').count()
    tb = pg.locator('.m-tabbar').is_visible()
    sv = pg.locator('.m-tabbar a.active .m-tab-ico svg').is_visible()
    st = pg.locator('.m-stat-item').count()
    print(f'[M02 待办] header={v} items={n} tabbar={tb} active-svg={sv} stat={st}'); ok &= (v and n > 0 and tb and sv and st == 3)
    shot('待办审批')

    # ---- M03 审批详情（从列表取真实单号） ----
    doc = pg.locator('.m-item .m-item-doc').first.inner_text().strip()
    pg.goto((MOB / '审批详情.html').as_uri() + '?id=' + urllib.parse.quote(doc))
    pg.wait_for_timeout(600)
    v = pg.locator('.m-header').is_visible()
    bk = pg.locator('.m-hd-back svg').is_visible()
    dl = pg.locator('.m-dl').count()
    ab = pg.locator('.m-action-bar .m-btn').count()
    dr = pg.locator('.m-detail-row').count()
    print(f'[M03 详情] doc={doc} header={v} back-svg={bk} dl-rows={dl} btns={ab} detail-rows={dr}'); ok &= (v and bk and dl >= 5 and ab == 2 and dr >= 1)
    shot('审批详情')

    # ---- M04 库存查询 ----
    pg.goto((MOB / '库存查询.html').as_uri())
    pg.wait_for_timeout(600)
    v = pg.locator('.m-header').is_visible()
    ch = pg.locator('.m-chip').count()
    it = pg.locator('.m-item').count()
    se = pg.locator('.m-search input').is_visible()
    print(f'[M04 库存] header={v} chips={ch} items={it} search={se}'); ok &= (v and ch == 5 and it > 0 and se)
    shot('库存查询')

    # ---- M05 我的 ----
    pg.goto((MOB / '我的.html').as_uri())
    pg.wait_for_timeout(600)
    v = pg.locator('.m-header').is_visible()
    av = pg.locator('.m-me-card .m-avatar').is_visible()
    ce = pg.locator('.m-cell').count()
    ki = pg.locator('.m-cell .m-cell-key svg').count()
    lo = pg.locator('#m-btn-logout').is_visible()
    print(f'[M05 我的] header={v} avatar={av} cells={ce} cell-svg={ki} logout={lo}'); ok &= (v and av and ce == 4 and ki == 4 and lo)
    shot('我的')

    print('JS ERRORS total:', len(errs))
    for e in errs[:5]: print('  ERR:', e[:160])
    ok &= (len(errs) == 0)
    br.close()

print('PLAYWRIGHT ALL PASS:', ok)
