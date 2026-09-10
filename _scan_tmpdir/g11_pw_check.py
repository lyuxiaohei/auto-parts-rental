# -*- coding: utf-8 -*-
"""G11-B5: Playwright 抽 3 页（库存查询/租赁单列表/销售订单列表）标注层验证
默认态：无便签裸露（.pn-open=0 且迁移前 pn-hint 已不在页面本体）+ 右下角「标注 N」入口在
?notes=1：body.proto-notes-on + [data-note] 角标渲染计数 > 0
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

PROTO = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
PAGES = ['仓储作业/库存查询.html', '租赁管理/租赁单列表.html', '销售管理/销售订单列表.html']

fails = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for rel in PAGES:
        try:
            # 默认态（全新 context=localStorage 干净）
            ctx = br.new_context()
            pg = ctx.new_page()
            pg.goto((PROTO / rel).as_uri())
            pg.wait_for_load_state('load')
            fab = pg.evaluate("() => { const f=document.querySelector('.pn-fab'); return f ? f.textContent.trim() : null }")
            open_pins = pg.evaluate("() => document.querySelectorAll('.proto-pin.pn-open').length")
            notes_on = pg.evaluate("() => document.body.classList.contains('proto-notes-on')")
            n_dn_default = pg.evaluate("() => document.querySelectorAll('[data-note]').length")
            assert fab and '标注' in fab, f'fab 入口缺失: {fab}'
            assert open_pins == 0, f'默认态便签裸露 {open_pins} 张'
            assert notes_on is False, '默认态不应开启'
            # 便签文本不应出现在页面本体可见文本（迁移闭环抽查：库存查询；innerText 尊重 display:none，注入块不计）
            if '库存查询' in rel:
                body_txt = pg.evaluate("() => document.querySelector('.main, body').innerText")
                assert '客户虚拟仓＝' not in body_txt and '原在租台账' not in body_txt, '页面本体可见文本仍含迁移前 hint'
            ctx.close()
            # ?notes=1 开启态
            ctx2 = br.new_context()
            pg2 = ctx2.new_page()
            pg2.goto((PROTO / rel).as_uri().rstrip('.html') + '.html?notes=1' if False else (PROTO / rel).as_uri() + '?notes=1')
            pg2.wait_for_load_state('load')
            on2 = pg2.evaluate("() => document.body.classList.contains('proto-notes-on')")
            n2 = pg2.evaluate("() => document.querySelectorAll('[data-note]').length")
            assert on2 and n2 > 0, f'?notes=1 未开启或角标 0（on={on2} n={n2}）'
            ctx2.close()
            print(f'PASS {rel} ｜ 默认态：fab「{fab}」·便签裸露 0·开关关 ｜ ?notes=1：角标 {n2} 个')
        except Exception as e:
            fails.append((rel, str(e)))
            print(f'FAIL {rel}: {e}')
    br.close()
print(f'==== G11 Playwright 抽查：{len(PAGES) - len(fails)}/{len(PAGES)} PASS，失败 {len(fails)} ====')
sys.exit(1 if fails else 0)
