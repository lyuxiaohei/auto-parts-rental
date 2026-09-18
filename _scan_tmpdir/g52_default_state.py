# -*- coding: utf-8 -*-
"""G52 补丁验证：抽屉默认态三场景（localStorage 预置 / 全新默认 / ?notes=1）"""
from playwright.sync_api import sync_playwright
from pathlib import Path

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')
PG = ROOT / '财务协同' / '银行回单核销.html'

DRAWER_OPEN = "() => document.querySelector('.pn-drawer').classList.contains('pn-show')"

with sync_playwright() as pw:
    b = pw.chromium.launch()
    # 场景1：localStorage 预置 '1'（模拟浏览器里曾打开过抽屉）→ 无 ?notes=1 时是否默认开
    ctx = b.new_context()
    ctx.add_init_script("try{localStorage.setItem('proto-notes-on','1')}catch(e){}")
    p = ctx.new_page(); p.goto(PG.as_uri()); p.wait_for_timeout(300)
    print('场景1 localStorage=1 无?notes=1 抽屉开 =', p.evaluate(DRAWER_OPEN))
    ctx.close()
    # 场景2：全新默认态
    p2 = b.new_page(); p2.goto(PG.as_uri()); p2.wait_for_timeout(300)
    print('场景2 全新默认 抽屉开 =', p2.evaluate(DRAWER_OPEN),
          '｜fab =', p2.evaluate("() => document.getElementById('protoNotesFab').textContent.trim()"))
    # 场景3：?notes=1 显式初始开
    p3 = b.new_page(); p3.goto(PG.as_uri() + '?notes=1'); p3.wait_for_timeout(300)
    print('场景3 ?notes=1 抽屉开 =', p3.evaluate(DRAWER_OPEN))
    b.close()
