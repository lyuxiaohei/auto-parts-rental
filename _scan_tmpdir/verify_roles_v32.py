# -*- coding: utf-8 -*-
"""G01 角色管理数据驱动验证门（2026-09-09）· 12 项断言（明细=G01 文档 C 表写死）
纪律⑤：Playwright 编程点击（evaluate el.click()）+ 等待；文本断言 textContent。
用法：python _scan_tmpdir/verify_roles_v32.py
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
PAGE = '系统管理/角色管理.html'
TPLS = [('系统管理/弹窗/权限配置.html', '权限配置'), ('系统管理/弹窗/新增角色.html', '新增角色')]

results, fails = [], []

def check(item, ok, detail=''):
    results.append((item, ok))
    if not ok:
        fails.append(item)
    print(('✅' if ok else '❌'), item, '|', detail)

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page()
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)[:150]))
    page.goto((PROTO / PAGE).as_uri(), wait_until='load')
    page.wait_for_selector('tbody tr', timeout=5000)
    page.wait_for_timeout(300)

    # ① roles 实体存在
    has_ent = page.evaluate("!!(window.DEMO_DATA && window.DEMO_DATA.roles)")
    check('①roles 实体存在', has_ent)
    keys = page.evaluate("Object.keys(window.DEMO_DATA.roles||{}).filter(function(k){return window.DEMO_DATA.roles[k].row})") if has_ent else []

    # ② 行数=9（实体 row 键数与渲染行数）
    n_rows = page.locator('tbody tr').count()
    check('②行数=9', len(keys) == 9 and n_rows == 9, '实体 %d / 渲染 %d' % (len(keys), n_rows))

    # ③ 列结构 th=5 且每行 td 数一致
    st = page.evaluate("""() => {
      const tb = document.querySelector('tbody');
      const nTh = tb.closest('table').querySelectorAll('thead th').length;
      const counts = [...new Set(Array.from(tb.querySelectorAll('tr')).map(tr => tr.cells.length))];
      return {nTh, counts};
    }""")
    check('③列结构 th=5 且每行 td 数一致', st['nTh'] == 5 and st['counts'] == [5],
          'th=%s 行td集=%s' % (st['nTh'], st['counts']))

    # ④ 首行逐格=cells（系统管理员）
    fc = page.evaluate("""() => {
      const tr = document.querySelector('tbody tr');
      const rec = window.DEMO_DATA.roles['RL-01'];
      return { rendered: Array.from(tr.cells).map(td => td.textContent.trim().replace(/\\s+/g, ' ')),
               want: ['系统管理员'].concat(rec.row.cells.map(c => c.replace(/<[^>]+>/g, '').replace(/\\s+/g, ' ').trim())).concat(['权限配置']) };
    }""")
    check('④首行逐格=cells（系统管理员）', fc['rendered'] == fc['want'], ' | '.join(fc['rendered']))

    # ⑤ 末行=供应商账号
    last = page.evaluate("Array.from(document.querySelectorAll('tbody tr')).pop().cells[0].textContent.trim()")
    check('⑤末行=供应商账号', last == '供应商账号', last)

    # ⑥ 筛选"财务"→2 行（财务/财务主管）
    page.evaluate("document.querySelector('.filter-card .ff input').value = '财务'")
    page.evaluate("[...document.querySelectorAll('.filter-card button')].find(b => b.textContent.trim() === '查询').click()")
    page.wait_for_timeout(200)
    names = page.evaluate("Array.from(document.querySelectorAll('tbody tr')).map(tr => tr.cells[0].textContent.trim())")
    check('⑥筛选"财务"→2 行', names == ['财务', '财务主管'], '%d 行 %s' % (len(names), names))

    # ⑦ 权限配置点击→roleModal show+标题含「权限配置 · 财务」（筛选态首行=财务）
    page.evaluate("document.querySelector('tbody tr .ops a').click()")
    page.wait_for_timeout(200)
    shown = page.evaluate("document.getElementById('roleModal').classList.contains('show')")
    title = page.evaluate("document.getElementById('rolePermTitle').textContent")
    check('⑦权限配置→roleModal show+标题含「权限配置 · 财务」', shown and '权限配置 · 财务' in title, title)

    # ⑧ 矩阵抽查：财务=勾 2 组含财务管理·不含仓储管理
    mx = page.evaluate("""Array.from(document.querySelectorAll('#roleModal .checkbox'))
      .filter(c => c.classList.contains('checked')).map(c => c.getAttribute('data-perm'))""")
    check('⑧矩阵抽查：财务勾 2 组含财务管理·不含仓储管理',
          len(mx) == 2 and '财务管理' in mx and '仓储管理' not in mx, str(mx))
    page.evaluate("[...document.querySelectorAll('#roleModal .modal-footer button')].pop().click()")  # 保存=closeModal
    page.wait_for_timeout(150)

    # ⑨ 新增角色→createModal show+表单含 角色名称/说明/数据权限范围 三字段
    page.evaluate("[...document.querySelectorAll('.card-head button')].find(b => b.textContent.trim() === '新增角色').click()")
    page.wait_for_timeout(200)
    cshow = page.evaluate("document.getElementById('createModal').classList.contains('show')")
    cbody = page.evaluate("document.querySelector('#createModal .modal-body').textContent")
    has3 = all(t in cbody for t in ['角色名称', '说明', '数据权限范围'])
    check('⑨新增角色→createModal show+表单三字段', cshow and has3, 'show=%s 三字段齐=%s' % (cshow, has3))

    # ⑩ 弹窗关闭恢复
    page.evaluate("[...document.querySelectorAll('#createModal .modal-footer button')].pop().click()")
    page.wait_for_timeout(150)
    closed = page.evaluate("!document.getElementById('roleModal').classList.contains('show') && !document.getElementById('createModal').classList.contains('show')")
    check('⑩弹窗关闭恢复', closed)

    # ⑪ 角色页 0 JS 错
    check('⑪角色页 0 JS 错', len(errs) == 0, '; '.join(errs) if errs else '无')

    # ⑫ 两新模板独立打开 0 JS 错+标题正确
    ok12, det12 = True, []
    for f, t in TPLS:
        p2 = browser.new_page()
        e2 = []
        p2.on('pageerror', lambda e: e2.append(str(e)[:150]))
        p2.goto((PROTO / f).as_uri(), wait_until='load')
        p2.wait_for_timeout(300)
        t2 = p2.evaluate("document.title + '|' + ((document.querySelector('.modal-title') || {}).textContent || '')")
        good = len(e2) == 0 and t in t2
        ok12 = ok12 and good
        det12.append('%s 标题含「%s」=%s JS错 %d' % (f.split('/')[-1], t, good, len(e2)))
        p2.close()
    check('⑫两新模板独立打开 0 JS 错+标题正确', ok12, '；'.join(det12))

    browser.close()

n_fail = len(fails)
print('\n==== 角色管理数据驱动验证门：%d 项断言，失败 %d 项 ====' % (len(results), n_fail))
if fails:
    print('失败明细：' + '；'.join(fails))
sys.exit(1 if n_fail else 0)
