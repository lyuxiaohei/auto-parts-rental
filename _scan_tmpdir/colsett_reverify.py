# -*- coding: utf-8 -*-
"""客商管理列设置·修复后重验：td 对应隐藏/恢复默认反馈/记忆/审计。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
sys.path.insert(0, str(ROOT / '_scan_tmpdir'))

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)

    pg.goto((PROTO / '基础数据/客商管理.html').as_uri(), wait_until='networkidle')
    pg.evaluate('toggleColSett()')
    pg.evaluate("""() => {
      document.querySelector('#colSettList .csItem[value="客商类型"]').checked = false;
      document.querySelector('#colSettList .csItem[value="联系电话"]').checked = false;
      applyColSett();
    }""")
    r = pg.evaluate("""() => {
      const tr = document.querySelector('.colsett-tbl tbody tr');
      const tdHid = [...tr.children].filter(td => getComputedStyle(td).display === 'none').map(td => td.textContent.trim().slice(0, 10));
      const thHid = [...document.querySelectorAll('.colsett-tbl thead th')].filter(t => getComputedStyle(t).display === 'none').map(t => t.textContent.trim());
      return {thHid, tdHid};
    }""")
    print('表头隐藏:', r['thHid'], '| 行内对应 td 隐藏:', r['tdHid'])

    pg.evaluate('resetColSett(document.querySelector(\'#colSettPanel a[onclick*="resetColSett"]\'))')
    tip = pg.evaluate("() => document.getElementById('colSettTip') ? document.getElementById('colSettTip').textContent : null")
    print('恢复默认反馈提示:', repr(tip))

    pg.reload(wait_until='networkidle')
    saved = pg.evaluate("() => localStorage.getItem('colsett-ksgl')")
    vis = pg.evaluate("() => [...document.querySelectorAll('.colsett-tbl thead th')].filter(t => getComputedStyle(t).display === 'none').length")
    print('恢复后刷新: 存储=%s 隐藏列数=%d' % (saved, vis))
    print('JS 错误:', len(errs))

    from _run_filter_audit3 import audit_page
    res = audit_page(b, PROTO / '基础数据/客商管理.html')
    print('审计: problems=%d dead=%d js=%d' % (len(res['problems']), len(res['dead_links']), len(res['js_errors'])), res['problems'][:1] if res['problems'] else '')
    ctx.close()
    b.close()
