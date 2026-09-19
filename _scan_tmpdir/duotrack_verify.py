# -*- coding: utf-8 -*-
"""#9 双轨验证：? 圆标常显/tooltip/数字角标保留/抽屉徽标/审计。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
sys.path.insert(0, str(ROOT / '_scan_tmpdir'))

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)

    # 1) 项目看板（全 biz）：默认态 ? 常显、无数字角标、tooltip
    pg.goto((PROTO / '首页/项目看板.html').as_uri(), wait_until='networkidle')
    r = pg.evaluate("""() => {
      const qs = document.querySelectorAll('.pn-q').length;
      const notesOn = document.body.classList.contains('proto-notes-on');
      return {qs, notesOn};
    }""")
    print('项目看板 默认态: ? 圆标=%d 个（notes-on=%s）' % (r['qs'], r['notesOn']))
    tip = pg.evaluate("""() => {
      const q = document.querySelector('.pn-q');
      q.dispatchEvent(new MouseEvent('mouseenter', {bubbles: false}));
      const t = document.querySelector('.pn-tip');
      return {show: t.classList.contains('pn-show'), text: t.textContent.slice(0, 40)};
    }""")
    print('  hover tooltip:', tip)
    pg.evaluate("() => document.querySelector('.pn-q').dispatchEvent(new MouseEvent('mouseleave', {bubbles: false}))")

    # 2) BOM维护（#1#2 biz / #3 dev）：混合
    pg.goto((PROTO / '基础数据/BOM维护.html').as_uri() + '?notes=1', wait_until='networkidle')
    r = pg.evaluate("""() => {
      const biz = document.querySelectorAll('.pn-biz').length;
      const qs = document.querySelectorAll('.pn-q').length;
      const devBadge = [...document.querySelectorAll('[data-note]')].filter(el => !el.classList.contains('pn-biz')).map(el => el.getAttribute('data-note'));
      const drawerB = document.querySelectorAll('.pn-drawer .pn-aud-biz').length;
      const drawerD = document.querySelectorAll('.pn-drawer .pn-aud-dev').length;
      return {biz, qs, devBadge, drawerB, drawerD};
    }""")
    print('BOM维护 ?notes=1: biz 锚=%d ?=%d dev 数字角标锚=%s 抽屉徽标 业务/开发=%d/%d' % (
        r['biz'], r['qs'], r['devBadge'], r['drawerB'], r['drawerD']))

    # 3) 用户权限 #3 dev 数字角标保留
    pg.goto((PROTO / '系统管理/用户权限.html').as_uri() + '?notes=1', wait_until='networkidle')
    r = pg.evaluate("""() => {
      const devAnchors = [...document.querySelectorAll('[data-note]')].filter(el => !el.classList.contains('pn-biz')).map(el => el.getAttribute('data-note'));
      return {devAnchors, qs: document.querySelectorAll('.pn-q').length};
    }""")
    print('用户权限: dev 数字角标锚=%s ? 圆标=%d' % (r['devAnchors'], r['qs']))
    print('JS 错误累计:', len(errs), errs[:2] if errs else '')

    from _run_filter_audit3 import audit_page
    for rel in ['首页/项目看板.html', '基础数据/BOM维护.html', '系统管理/用户权限.html', '财务协同/损益报表.html']:
        res = audit_page(b, PROTO / rel)
        print('%s problems=%d dead=%d js=%d' % (rel.split('/')[-1], len(res['problems']), len(res['dead_links']), len(res['js_errors'])))
    b.close()
