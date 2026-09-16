#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# G50 验证门 3：Playwright 五页断言 + 全页截图（file:// · m-auth 预置 · 守卫回归 unquote）
import os
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/mobile'
OUT = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/_scan_tmpdir/g50_after'
os.makedirs(OUT, exist_ok=True)

results = []
def check(name, ok, detail=''):
    results.append((name, ok))
    print(('[PASS]' if ok else '[FAIL]'), name, ('—— ' + detail) if detail else '')

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 375, 'height': 812}, locale='zh-CN')
    ctx.add_init_script(
        "localStorage.setItem('m-auth', JSON.stringify({name:'沈婷', role:'商务主管', ts:Date.now()}));"
        "localStorage.setItem('m-done', JSON.stringify({'XSTH-20260913-001':'已通过','CGTH-20260912-002':'已通过','PD-20260910-004':'已驳回'}));"
    )
    pg = ctx.new_page()
    errors = []
    pg.on('pageerror', lambda e: errors.append(str(e)))

    # ---- ① 登录（mGuardAuthed 会跳走——用无 init 脚本的独立上下文断言登录页本体） ----
    ctx2 = b.new_context(viewport={'width': 375, 'height': 812}, locale='zh-CN')
    pg2 = ctx2.new_page()
    pg2.goto('file://' + os.path.join(ROOT, '登录.html'), wait_until='networkidle')
    pg2.wait_for_timeout(900)
    check('登录 hero logo/品牌名/两按钮', pg2.query_selector('.m-logo') is not None
          and '汽车物流包装租赁' in pg2.inner_text('.m-login-name')
          and pg2.query_selector('#m-btn-login') is not None and pg2.query_selector('#m-btn-wx') is not None,
          'logo+品牌名+登录/企微按钮在位')
    check('登录 版本 v1.2', 'v1.2 · 2026-09-16' in pg2.inner_text('body'))
    pg2.screenshot(path=os.path.join(OUT, '01-登录.png'), full_page=True)

    # ---- ② 待办审批 ----
    pg.goto('file://' + os.path.join(ROOT, '待办审批.html'), wait_until='networkidle')
    pg.wait_for_timeout(400)
    check('待办 统计卡 3 格', len(pg.query_selector_all('.m-stat-item')) == 3)
    check('待办 item 卡片 ≥1', len(pg.query_selector_all('.m-item')) >= 1,
          'cards=' + str(len(pg.query_selector_all('.m-item'))))
    badges = pg.eval_on_selector_all('.m-badge', 'els => els.map(e => e.className)')
    check('待办 徽标配色类命中', any(('m-badge-orange' in c or 'm-badge-blue' in c or 'm-badge-green' in c
          or 'm-badge-purple' in c or 'm-badge-gray' in c or 'm-badge-red' in c) for c in badges),
          'badge 类样本=' + (badges[0] if badges else '无'))
    # 取一个真实单号供审批详情使用
    doc_id = pg.evaluate("() => Object.keys(window.DEMO_DATA.todoItems)[0]")
    pg.screenshot(path=os.path.join(OUT, '02-待办审批.png'), full_page=True)

    # ---- ③ 审批详情 ----
    pg.goto('file://' + os.path.join(ROOT, '审批详情.html?id=' + doc_id), wait_until='networkidle')
    pg.wait_for_timeout(400)
    ban = pg.query_selector('.m-banner')
    check('审批详情 .m-banner 存在且含状态大字', ban is not None and ban.is_visible()
          and pg.inner_text('#m-banner-state').strip() != '', '状态=' + pg.inner_text('#m-banner-state').strip())
    check('审批详情 .m-timeline 节点=2', len(pg.query_selector_all('.m-tl-item')) == 2,
          'nodes=' + str(len(pg.query_selector_all('.m-tl-item'))))
    check('审批详情 操作栏按钮 ≥2', len(pg.query_selector_all('.m-action-bar .m-btn')) >= 2)
    pg.screenshot(path=os.path.join(OUT, '03-审批详情.png'), full_page=True)

    # ---- ④ 我的 ----
    pg.goto('file://' + os.path.join(ROOT, '我的.html'), wait_until='networkidle')
    pg.wait_for_timeout(400)
    check('我的 .m-hero 存在', pg.query_selector('.m-hero') is not None)
    exp = pg.evaluate("""() => {
      const rows = Object.keys(window.DEMO_DATA.todoItems);
      const types = {}; rows.forEach(k => { types[window.DEMO_DATA.todoItems[k].row.fields.type] = 1; });
      const done = JSON.parse(localStorage.getItem('m-done') || '{}');
      return { todo: rows.length, done: Object.keys(done).length, type: Object.keys(types).length };
    }""")
    got = {'todo': pg.inner_text('#m-st-todo').strip(), 'done': pg.inner_text('#m-st-done').strip(), 'type': pg.inner_text('#m-st-type').strip()}
    check('我的 统计三格实算逐一相等', got == {'todo': str(exp['todo']), 'done': str(exp['done']), 'type': str(exp['type'])},
          'got=' + str(got) + ' exp=' + str(exp))
    check('我的 cell 分组卡（4 行入组）', len(pg.query_selector_all('.m-cell-group .m-cell')) == 4
          and pg.query_selector('.m-cell-group') is not None)
    check('我的 版本 v1.2', 'v1.2 · 2026-09-16' in pg.inner_text('body'))
    pg.screenshot(path=os.path.join(OUT, '04-我的.png'), full_page=True)

    # ---- ⑤ 库存查询 ----
    pg.goto('file://' + os.path.join(ROOT, '库存查询.html'), wait_until='networkidle')
    pg.wait_for_timeout(400)
    chips = pg.query_selector_all('.m-chip')
    tops = pg.eval_on_selector_all('.m-chip', 'els => els.map(e => e.getBoundingClientRect().top)')
    check('库存 chips=6 个单行横滑不换行', len(chips) == 6 and len(set(round(t) for t in tops)) == 1,
          'n=' + str(len(chips)) + ' 行数=' + str(len(set(round(t) for t in tops))) + '（任务书 7 系计数口径出入·见默认决策）')
    check('库存 卡片 ≥1', len(pg.query_selector_all('.m-item')) >= 1,
          'cards=' + str(len(pg.query_selector_all('.m-item'))))
    pg.screenshot(path=os.path.join(OUT, '05-库存查询.png'), full_page=True)

    # ---- ⑥ 守卫回归：无 m-auth 的净上下文访问受护页 → 跳登录页（unquote 后断言） ----
    # 注：主上下文挂了 add_init_script（每次导航重写 m-auth），须用净上下文验证守卫
    ctx3 = b.new_context(viewport={'width': 375, 'height': 812}, locale='zh-CN')
    pg3 = ctx3.new_page()
    pg3.goto('file://' + os.path.join(ROOT, '库存查询.html'), wait_until='load')
    pg3.wait_for_timeout(1400)
    url = unquote(pg3.url)
    check('守卫回归 清 m-auth 跳登录页', '登录.html' in url, url[-40:])
    ctx3.close()

    check('五页 JS 错误=0', len(errors) == 0, '; '.join(errors[:3]))
    b.close()

fails = [r for r in results if not r[1]]
print()
print('PW 总判定：', len(results) - len(fails), 'PASS /', len(fails), 'FAIL')
