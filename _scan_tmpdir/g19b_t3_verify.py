# -*- coding: utf-8 -*-
"""G19b T3 门3 Playwright 三段流：默认已登录/退出流/登录流+空值提示+企微 toast+JS 0
file:// 同 context 多页共享 localStorage（mobile m-auth 同款先例）。"""
from playwright.sync_api import sync_playwright
from urllib.parse import unquote
import pathlib, io, sys

BASE = pathlib.Path('P3-R01-包装租赁管理后台原型').resolve()
out = []
js_errors = []

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context()
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: js_errors.append(str(e)))

    def url_of(rel):
        return (BASE / rel).as_uri()

    # ===== 段1 默认已登录：无键直达 =====
    pg.goto(url_of('我的待办.html'))
    pg.wait_for_load_state('load')
    pg.evaluate("() => localStorage.removeItem('pc-logout')")
    pg.goto(url_of('我的待办.html'))
    pg.wait_for_load_state('load')
    u1 = unquote(pg.url)
    ok1 = '我的待办' in u1 and '登录' not in u1 and pg.locator('.topbar').count() == 1
    out.append(f"{'PASS' if ok1 else 'FAIL'} 段1 默认已登录：清键直开 我的待办 不跳登录（URL={u1[-30:]}）")

    # ===== 段2 退出流 =====
    pg.click('.topbar .avatar')
    pg.wait_for_timeout(200)
    menu_items = pg.locator('div', has_text='退出登录').all_inner_texts()
    # 点退出登录（动态下拉项）
    pg.locator('text=退出登录').first.click()
    pg.wait_for_timeout(600)
    u2 = unquote(pg.url)
    ok2a = '登录.html' in u2
    out.append(f"{'PASS' if ok2a else 'FAIL'} 段2a 头像下拉退出登录→落登录页（URL={u2[-20:]}）")
    # 他页守卫拦截
    pg.goto(url_of('仓储作业/库存查询.html'))
    pg.wait_for_timeout(800)
    u2b = unquote(pg.url)
    ok2b = '登录.html' in u2b and '库存查询' not in u2b
    out.append(f"{'PASS' if ok2b else 'FAIL'} 段2b 退出态开库存查询被守卫拦截→登录页（URL={u2b[-20:]}）")

    # ===== 段3 登录流 =====
    # 3a 空账号行内提示
    pg.goto(url_of('登录.html'))
    pg.wait_for_load_state('load')
    pg.evaluate("() => { document.getElementById('loginUser').value=''; document.getElementById('loginPwd').value=''; }")
    pg.click('#btnLogin')
    pg.wait_for_timeout(200)
    ok3a = pg.locator('#errUser').is_visible() and pg.locator('#errPwd').is_visible()
    out.append(f"{'PASS' if ok3a else 'FAIL'} 段3a 空账号点登录→行内红字提示双现（errUser={pg.locator('#errUser').is_visible()} errPwd={pg.locator('#errPwd').is_visible()}）")
    # 3b 企微 toast
    pg.click('#btnWecom')
    pg.wait_for_timeout(300)
    ok3b = pg.locator('#toast').is_visible() and '暂未接入' in pg.locator('#toast').text_content()
    out.append(f"{'PASS' if ok3b else 'FAIL'} 段3b 企微扫码按钮→toast「演示原型 · 暂未接入」")
    # 3c 登录成功进看板+守卫解除
    pg.evaluate("() => { document.getElementById('loginUser').value='liu.dy'; document.getElementById('loginPwd').value='123456'; }")
    pg.click('#btnLogin')
    pg.wait_for_timeout(900)
    u3c = unquote(pg.url)
    ok3c = '项目看板' in u3c
    out.append(f"{'PASS' if ok3c else 'FAIL'} 段3c 登录→落项目看板（URL={u3c[-25:]}）")
    pg.goto(url_of('我的待办.html'))
    pg.wait_for_timeout(500)
    u3d = unquote(pg.url)
    ok3d = '我的待办' in u3d and '登录' not in u3d
    out.append(f"{'PASS' if ok3d else 'FAIL'} 段3d 登录后再开待办→守卫解除不跳（URL={u3d[-25:]}）")

    b.close()

out.append(f"{'PASS' if not js_errors else 'FAIL'} JS 错误 = {len(js_errors)} {js_errors[:3]}")
report = '\n'.join(out)
pathlib.Path('_scan_tmpdir/g19b_t3_pw.txt').write_text(report, encoding='utf-8')
with io.open(1, 'w', encoding='utf-8', closefd=False) as f:
    f.write(report + '\n')
sys.exit(0 if all(l.startswith('PASS') for l in out) else 1)
