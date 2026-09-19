# -*- coding: utf-8 -*-
"""待办 #5 样板验证：客商管理「列设置」——开关面板/勾选显隐/记忆/恢复默认/勾选框与操作列固定。"""
import sys
from pathlib import Path

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁')
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
sys.path.insert(0, str(ROOT / '_scan_tmpdir'))

from playwright.sync_api import sync_playwright

COLS_JS = """() => {
  const ths = [...document.querySelectorAll('.colsett-tbl thead th')];
  return { total: ths.length,
           visible: ths.filter(t => t.offsetParent !== null || getComputedStyle(t).display !== 'none').length,
           labels: ths.filter(t => getComputedStyle(t).display !== 'none').map(t => t.textContent.trim()) };
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)

    pg.goto((PROTO / '基础数据/客商管理.html').as_uri(), wait_until='networkidle')
    r = pg.evaluate(COLS_JS)
    print('初始: 列=%d 可见=%d' % (r['total'], r['visible']))

    # 开面板
    pg.evaluate("toggleColSett()")
    vis = pg.evaluate("() => document.getElementById('colSettPanel').style.display")
    print('面板开关:', vis)

    # 取消 勾选 联系电话 + 客商类型
    pg.evaluate("""() => {
      document.querySelector('#colSettList .csItem[value=\\'联系电话\\']').checked = false;
      document.querySelector('#colSettList .csItem[value=\\'客商类型\\']').checked = false;
      applyColSett();
    }""")
    r = pg.evaluate(COLS_JS)
    print('隐藏2列后: 可见=%d 列序=%s' % (r['visible'], r['labels']))
    body_hidden = pg.evaluate("() => [...document.querySelectorAll('.colsett-tbl tbody tr')].every(tr => getComputedStyle(tr.children[4]).display === 'none' && getComputedStyle(tr.children[3]).display === 'none')")
    print('  tbody 对应 td 隐藏:', body_hidden)

    # 刷新页面 → localStorage 记忆
    pg.reload(wait_until='networkidle')
    r = pg.evaluate(COLS_JS)
    chk = pg.evaluate("() => [...document.querySelectorAll('#colSettList .csItem:not(:checked)')].map(i=>i.value)")
    print('刷新后记忆: 可见=%d 未勾选=%s' % (r['visible'], chk))

    # 恢复默认
    pg.evaluate("resetColSett()")
    r = pg.evaluate(COLS_JS)
    saved = pg.evaluate("() => localStorage.getItem('colsett-ksgl')")
    print('恢复默认: 可见=%d 存储=%s' % (r['visible'], saved))

    # 点外部关闭
    pg.evaluate("toggleColSett()")
    pg.evaluate("() => document.querySelector('.filter-card, .card-title').dispatchEvent(new MouseEvent('click', {bubbles: true}))")
    vis = pg.evaluate("() => document.getElementById('colSettPanel').style.display")
    print('点外部关闭:', vis)
    print('JS 错误:', len(errs), errs[:2] if errs else '')

    from _run_filter_audit3 import audit_page
    res = audit_page(b, PROTO / '基础数据/客商管理.html')
    print('审计: problems=%d dead=%d js=%d' % (len(res['problems']), len(res['dead_links']), len(res['js_errors'])), res['problems'][:2] if res['problems'] else '')
    ctx.close()
    b.close()
