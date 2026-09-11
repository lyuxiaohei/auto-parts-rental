# -*- coding: utf-8 -*-
"""G20 验证门 6：PW 抽验 4 段+截图。
①退租入库列表 新建→createModal 可见→提交→关闭
②我的待办 chip「租入入库」命中行≥1、pin-1 含「15 类」不含「18 类」（st-foot 已被 G18 删转标注——断言降级记偏差）
③系统管理/角色管理.html 直达渲染 9 角色行
④mobile/待办审批.html 渲染无 JS 错、待办行数=15
"""
import io, sys, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT/'P3-R01-包装租赁管理后台原型').as_posix()
SHOTS = ROOT/'_scan_tmpdir'
results = []

def chk(name, cond, detail=''):
    results.append(('PASS' if cond else 'FAIL', name, detail))

with sync_playwright() as pw:
    b = pw.chromium.launch()

    # ① 退租入库列表
    errs1 = []
    pg = b.new_page()
    pg.on('pageerror', lambda e: errs1.append(str(e)))
    pg.on('console', lambda m: errs1.append(m.text) if m.type == 'error' else None)
    pg.goto(f'file:///{BASE}/租赁管理/退租入库列表.html'); pg.wait_for_timeout(800)
    pg.click("button:has-text('新建退租入库单')"); pg.wait_for_timeout(300)
    vis1 = pg.is_visible('#createModal .modal')
    pg.screenshot(path=str(SHOTS/'g20-tzrkb-create.png'))
    pg.click("#createModal button:has-text('提交审核')"); pg.wait_for_timeout(300)
    vis2 = pg.is_visible('#createModal .modal')
    chk('①新建→createModal 可见', vis1)
    chk('①提交→弹窗关闭', not vis2)
    chk('①JS 错误=0', len(errs1) == 0, str(errs1[:1]))
    pg.close()

    # ② 我的待办
    errs2 = []
    pg = b.new_page()
    pg.on('pageerror', lambda e: errs2.append(str(e)))
    pg.on('console', lambda m: errs2.append(m.text) if m.type == 'error' else None)
    pg.goto(f'file:///{BASE}/我的待办.html'); pg.wait_for_timeout(1000)
    # 类型下拉选「租入入库」过滤（本页筛选为 select·非 chip）
    sel = pg.locator("select").first
    n_rows = -1
    opts = sel.locator("option").all_text_contents()
    chk('②类型下拉含「租入入库」', '租入入库' in [o.strip() for o in opts], str(opts[:5]))
    if '租入入库' in [o.strip() for o in opts]:
        sel.select_option(label='租入入库'); pg.wait_for_timeout(500)
        n_rows = pg.locator('tbody tr:visible').count()
    chk('②选「租入入库」命中行>=1', n_rows >= 1, f'rows={n_rows}')
    body = pg.content()
    chk('②pin 含「15 类」', '15 类' in body)
    chk('②pin 不含「18 类」', '18 类' not in body)
    stfoot = pg.locator(".st-foot:has-text('覆盖')").count()
    chk('②st-foot 已删或含15类（G18 降级）', stfoot == 0 or '15 类' in pg.locator(".st-foot:has-text('覆盖')").first.text_content(), f'stfoot={stfoot}')
    chk('②JS 错误=0', len(errs2) == 0, str(errs2[:1]))
    pg.screenshot(path=str(SHOTS/'g20-todo-15.png'))
    pg.close()

    # ③ 角色管理直达
    errs3 = []
    pg = b.new_page()
    pg.on('pageerror', lambda e: errs3.append(str(e)))
    pg.on('console', lambda m: errs3.append(m.text) if m.type == 'error' else None)
    pg.goto(f'file:///{BASE}/系统管理/角色管理.html'); pg.wait_for_timeout(1000)
    n_roles = pg.locator('tbody tr').count()
    chk('③角色行=9', n_roles == 9, f'={n_roles}')
    chk('③JS 错误=0', len(errs3) == 0, str(errs3[:1]))
    pg.screenshot(path=str(SHOTS/'g20-roles.png'))
    pg.close()

    # ④ mobile 待办审批（m-auth 预置——mobile 守卫无键跳登录页）
    errs4 = []
    pg = b.new_page(viewport={'width': 390, 'height': 844})
    pg.on('pageerror', lambda e: errs4.append(str(e)))
    pg.on('console', lambda m: errs4.append(m.text) if m.type == 'error' else None)
    pg.goto(f'file:///{BASE}/mobile/登录.html'); pg.wait_for_timeout(500)
    pg.evaluate("localStorage.setItem('m-auth', JSON.stringify({name:'王琳',role:'商务主管',ts:Date.now()}))")
    pg.goto(f'file:///{BASE}/mobile/待办审批.html'); pg.wait_for_timeout(1200)
    # 待办行：列表项（按实际类名兜底多种形态）
    n_todo = pg.locator('.m-item').count()
    chk('④mobile 待办行数=15', n_todo == 15, f'={n_todo}')
    chk('④JS 错误=0', len(errs4) == 0, str(errs4[:1]))
    pg.screenshot(path=str(SHOTS/'g20-mobile-todo.png'))
    pg.close()

    b.close()

npass = sum(1 for r in results if r[0] == 'PASS')
for st, name, detail in results:
    print(f'{st} {name}' + (f'  ({detail})' if detail and st == 'FAIL' else ''))
print(f'== {npass}/{len(results)} ==')
sys.exit(0 if npass == len(results) else 1)
