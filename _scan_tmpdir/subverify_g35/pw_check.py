# -*- coding: utf-8 -*-
"""G35 独立验收·筛选可用性验证（只读·subverify_g35 自有脚本）：
页1 财务协同/应付账单.html：g35ProjectSel 选第 1 个非全部值 → 编程点击「查询」→ tbody tr 数变化
页2 我的待办.html：todoProject 选值 → 调 filterTodo() → #todoBody 可见 tr 数变化
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')

results = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    pg = browser.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))

    # ---- 页1 应付账单 ----
    url = (ROOT / '财务协同' / '应付账单.html').as_uri()
    pg.goto(url)
    pg.wait_for_load_state('networkidle')
    before = pg.eval_on_selector_all('tbody tr', 'els => els.length')
    opts = pg.eval_on_selector('#g35ProjectSel', """s => {
        var o = [];
        for (var i = 0; i < s.options.length; i++) o.push(s.options[i].text.trim());
        return o;
    }""")
    non_all = [o for o in opts if o and o != '全部']
    picked = non_all[0] if non_all else None
    if picked is None:
        results.append(('应付账单', 'FAIL', 'g35ProjectSel 无非全部选项', before, None, opts))
    else:
        pg.eval_on_selector('#g35ProjectSel', """(s, v) => {
            s.value = v;
            s.dispatchEvent(new Event('change', {bubbles: true}));
        }""", picked)
        # 编程点击「查询」按钮
        clicked = pg.evaluate("""() => {
            var btns = document.querySelectorAll('.filter-actions button, button');
            for (var i = 0; i < btns.length; i++) {
                if (btns[i].textContent.trim() === '查询') { btns[i].click(); return true; }
            }
            return false;
        }""")
        pg.wait_for_timeout(300)
        after = pg.eval_on_selector_all('tbody tr', 'els => els.length')
        ok = clicked and before != after and after > 0
        results.append(('应付账单', 'PASS' if ok else 'FAIL',
                        '选中值=%s, 查询按钮点击=%s' % (picked, clicked), before, after, None))

    # ---- 页2 我的待办 ----
    url2 = (ROOT / '我的待办.html').as_uri()
    pg.goto(url2)
    pg.wait_for_load_state('networkidle')
    vis_before = pg.eval_on_selector_all('#todoBody tr',
        "els => els.filter(t => t.style.display !== 'none').length")
    total = pg.eval_on_selector_all('#todoBody tr', 'els => els.length')
    opts2 = pg.eval_on_selector('#todoProject', """s => {
        var o = [];
        for (var i = 0; i < s.options.length; i++) o.push(s.options[i].text.trim());
        return o;
    }""")
    non_all2 = [o for o in opts2 if o and o != '全部']
    picked2 = non_all2[0] if non_all2 else None
    if picked2 is None:
        results.append(('我的待办', 'FAIL', 'todoProject 无非全部选项', vis_before, None, opts2))
    else:
        pg.eval_on_selector('#todoProject', """(s, v) => {
            s.value = v;
        }""", picked2)
        pg.evaluate('filterTodo()')
        pg.wait_for_timeout(200)
        vis_after = pg.eval_on_selector_all('#todoBody tr',
            "els => els.filter(t => t.style.display !== 'none').length")
        ok2 = vis_before != vis_after and vis_after > 0
        results.append(('我的待办', 'PASS' if ok2 else 'FAIL',
                        '选中值=%s' % picked2, vis_before, vis_after, None))

    browser.close()
    print('pageerrors:', errs if errs else '无')

for name, st, msg, b, a, extra in results:
    print('[%s] %s | before=%s after=%s | %s %s' % (st, name, b, a, msg, ('opts=%s' % extra) if extra else ''))
