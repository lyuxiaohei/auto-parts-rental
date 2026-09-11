# -*- coding: utf-8 -*-
"""复证：viewport 截图（非 full_page）——确认 fixed tabbar 真实形态+列表底部不被遮挡"""
import pathlib
from playwright.sync_api import sync_playwright
MOB = pathlib.Path(r'P3-R01-包装租赁管理后台原型/mobile').resolve()
with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page(viewport={'width': 375, 'height': 812})
    pg.goto((MOB / '登录.html').as_uri())
    pg.evaluate("localStorage.setItem('m-auth', JSON.stringify({name:'王琳',role:'商务主管',ts:Date.now()}))")
    pg.goto((MOB / '待办审批.html').as_uri())
    pg.wait_for_timeout(600)
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")   # 滚到底
    pg.wait_for_timeout(300)
    # 几何断言：最后一个 .m-item 底边 在 tabbar 顶边 之上（不被遮挡）
    geo = pg.evaluate("""() => {
      const items = document.querySelectorAll('.m-item');
      const last = items[items.length-1].getBoundingClientRect();
      const tab = document.querySelector('.m-tabbar').getBoundingClientRect();
      const body = document.querySelector('.m-body');
      const cs = getComputedStyle(body);
      return { lastBottom: last.bottom, tabTop: tab.top, padBottom: cs.paddingBottom,
               noOverlap: last.bottom <= tab.top, tabOpaque: getComputedStyle(document.querySelector('.m-tabbar')).backgroundColor };
    }""")
    print('[geo]', geo)
    pg.screenshot(path=str(pathlib.Path(r'_scan_tmpdir/g19a-mobile-待办审批-viewport-bottom.png')))
    print('viewport shot saved')
    br.close()
    assert geo['noOverlap'], 'OVERLAP!'
    print('NO-OVERLAP PASS')
