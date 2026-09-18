# -*- coding: utf-8 -*-
"""G52 T3.5 PW 抽验 12 页：零 JS 错 / fab 计数=数据条数 / 无数据页 fab 隐藏 / 点角标开抽屉定位 / 样板流程图钮在 / ?notes=1 直开"""
import sys, os, json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')

# (相对路径, 期望条目数, 是否点角标, 是否 ?notes=1 直开)
CASES = [
    ('仓储作业/库存查询.html', 6, True, False),
    ('系统管理/用户权限.html', 3, True, False),
    ('财务协同/损益报表.html', 6, True, False),
    ('项目管理/项目详情.html', 7, True, False),
    ('我的待办.html', 5, True, False),
    ('租赁管理/租赁出库列表.html', 2, True, False),
    ('财务协同/付款确认.html', 0, False, False),
    ('租赁管理/租赁单审核.html', 0, False, False),
    ('基础数据/物料新建.html', 0, False, False),
    ('财务协同/银行回单核销.html', 4, True, False),   # 样板页
    ('首页/项目看板.html', 7, False, True),            # ?notes=1 直开
    ('财务协同/应收账单.html', 2, False, True),        # ?notes=1 直开
]

def run():
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for rel, expect, click_badge, notes1 in CASES:
            errs = []
            page = browser.new_page()
            page.on('pageerror', lambda e: errs.append('pageerror: %s' % e))
            page.on('console', lambda m: errs.append('console.error: %s' % m.text) if m.type == 'error' else None)
            url = (ROOT / rel).as_uri() + ('?notes=1' if notes1 else '')
            try:
                page.goto(url, wait_until='load', timeout=15000)
                page.wait_for_timeout(400)
                js_err = [e for e in errs if 'net::ERR_' not in e]
                checks = [('零JS错', len(js_err) == 0)]
                fab = page.evaluate("() => { var f = document.getElementById('protoNotesFab'); return f ? {display: getComputedStyle(f).display, text: f.textContent.trim()} : null; }")
                if expect == 0:
                    checks.append(('fab隐藏', fab is not None and fab['display'] == 'none'))
                else:
                    # 计数以抽屉标题 .pn-fab-n 为准（fab 开态文案=收起，不含计数）
                    title_cnt = page.evaluate("() => { var s = document.querySelector('.pn-drawer-title .pn-fab-n'); return s ? s.textContent : null; }")
                    checks.append(('计数=%d' % expect, title_cnt == str(expect)))
                drawer_items = page.evaluate("() => document.querySelectorAll('.pn-drawer .pn-item').length")
                drawer_open = page.evaluate("() => document.querySelector('.pn-drawer').classList.contains('pn-show')")
                if notes1 and expect > 0:
                    checks.append(('?notes=1直开抽屉', drawer_open))
                if click_badge and expect > 0:
                    # 编程点击第一个角标（evaluate 点击惯例）＋捕获点击/高亮
                    got = page.evaluate("""() => {
                        var el = document.querySelector('[data-note]');
                        if (!el) return {err: 'no [data-note]'};
                        el.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, clientX: 10, clientY: 5}));
                        var dr = document.querySelector('.pn-drawer');
                        var hl = dr ? dr.querySelector('.pn-item.pn-hl') : null;
                        return {open: dr ? dr.classList.contains('pn-show') : false,
                                hlId: hl ? hl.getAttribute('data-id') : null,
                                wantId: el.getAttribute('data-note')};
                    }""")
                    page.wait_for_timeout(150)
                    checks.append(('点角标开抽屉', got.get('open') is True))
                    checks.append(('高亮定位=%s' % got.get('wantId'), str(got.get('hlId')) == str(got.get('wantId'))))
                if expect > 0:
                    checks.append(('抽屉条目数=%d' % expect, drawer_items == expect))
                if rel == '财务协同/银行回单核销.html':
                    f01 = page.evaluate("() => { var a = document.querySelector('.fab-row a.f01-fab'); return a ? a.href : null; }")
                    checks.append(('样板流程图钮在', f01 is not None and 'F01' in f01))
                ok = all(v for _, v in checks)
                results.append((ok, rel, checks, js_err[:2]))
            except Exception as e:
                results.append((False, rel, [('异常', False)], [str(e)]))
            finally:
                page.close()
        browser.close()
    npass = sum(1 for r in results if r[0])
    for ok, rel, checks, errs in results:
        print('%s %s' % ('PASS' if ok else 'FAIL', rel))
        for name, v in checks:
            if not v: print('    ✗ %s' % name)
        if errs: print('    JS错误: %s' % errs)
    print('总判定：%d PASS / %d FAIL' % (npass, len(results) - npass))
    sys.exit(0 if npass == len(results) else 1)

run()
