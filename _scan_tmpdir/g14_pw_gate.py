# -*- coding: utf-8 -*-
"""G14 验证门 3：Playwright 5 项（移动端 H5·file:// 直开·编程点击沿纪律）
①未登录直访待办审批→守卫跳登录 ②登录→跳待办+m-auth 写入+卡片≥10
③审批详情点「通过」→状态变化+toast ④库存 chips「客户端(转租)」→行数变化
⑤我的点退出→清标记回登录"""
import io, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\mobile")

def u(name): return (ROOT / name).as_uri()

def wait_url(page, frag, timeout=8000):
    t0 = time.time()
    while time.time() - t0 < timeout / 1000:
        if frag in unquote(page.url):
            return True
        page.wait_for_timeout(100)
    return False

def click_js(page, sel):
    page.eval_on_selector(sel, "el => el.click()")   # 编程点击（IAB 管道缺陷纪律）

results = []
def check(name, ok, detail=''):
    results.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" · {detail}" if detail else ''))

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    ctx = browser.new_context()
    page = ctx.new_page()

    # ① 未登录直访 待办审批 → 守卫跳 登录
    page.goto(u('待办审批.html'), wait_until='load')
    ok1 = wait_url(page, '登录.html')
    check('①未登录守卫跳登录', ok1, unquote(page.url).split('/')[-1])

    # ② 登录：填账号密码 → 跳待办 + m-auth 写入 + 卡片 ≥10
    page.fill('#m-acc', 'wanglin')
    page.fill('#m-pwd', '123456')
    click_js(page, '#m-btn-login')
    ok2a = wait_url(page, '待办审批.html')
    auth = page.evaluate("localStorage.getItem('m-auth')")
    cards = page.eval_on_selector_all('.m-item', 'els => els.length') if ok2a else 0
    check('②登录跳待办+m-auth写入+卡片≥10', ok2a and auth and cards >= 10, f'url={unquote(page.url).split("/")[-1]} m-auth={auth[:40] if auth else None} 卡片={cards}')

    # ③ 待办首卡 → 审批详情 → 点「通过」→ 状态变化 + toast
    click_js(page, '.m-item')                       # 第一张卡（SO-20260910-0047）
    ok3a = wait_url(page, '审批详情.html')
    if ok3a:
        before = page.eval_on_selector('#m-status-badge', 'e => e.textContent.trim()')
        click_js(page, '#m-btn-pass')
        page.wait_for_timeout(150)
        after = page.eval_on_selector('#m-status-badge', 'e => e.textContent.trim()')
        toast_shown = page.eval_on_selector('#m-toast', 'e => e.classList.contains("show")')
        toast_txt = page.eval_on_selector('#m-toast', 'e => e.textContent')
        ok3b = wait_url(page, '待办审批.html')      # 900ms 后自动返回
        done_badge = page.eval_on_selector_all('.m-badge', 'els => els.some(e => e.textContent.trim()==="已通过")') if ok3b else False
        check('③审批通过→状态变化+toast', ok3a and before == '待审核' and after == '已通过' and toast_shown and done_badge,
              f'{before}→{after} toast="{toast_txt}" 返回待办后已通过徽标={done_badge}')
    else:
        check('③审批通过→状态变化+toast', False, '未跳到审批详情')

    # ④ 库存查询 → chips「客户端(转租)」→ 行数变化
    page.goto(u('库存查询.html'), wait_until='load')
    page.wait_for_selector('.m-item')
    n_all = page.eval_on_selector_all('.m-item', 'els => els.length')
    page.eval_on_selector('.m-chip[data-s="客户端(转租)"]', 'el => el.click()')
    page.wait_for_timeout(250)
    n_zz = page.eval_on_selector_all('.m-item', 'els => els.length')
    check('④库存chips客户端(转租)行数变化', n_all == 13 and n_zz == 3 and n_all != n_zz, f'{n_all}→{n_zz}')

    # ⑤ 我的 → 退出登录 → 清 m-auth 回登录
    page.goto(u('我的.html'), wait_until='load')
    page.wait_for_selector('#m-btn-logout')
    click_js(page, '#m-btn-logout')
    ok5 = wait_url(page, '登录.html')
    auth5 = page.evaluate("localStorage.getItem('m-auth')")
    check('⑤退出清标记回登录', ok5 and auth5 is None, f'url={unquote(page.url).split("/")[-1]} m-auth={auth5}')

    ctx.close()
    browser.close()

n_pass = sum(1 for _, ok, _ in results if ok)
print(f"\n==== PW 门：{n_pass}/5 {'PASS' if n_pass == 5 else 'FAIL'} ====")
sys.exit(0 if n_pass == 5 else 1)
