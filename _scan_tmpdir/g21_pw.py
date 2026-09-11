#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G21 验证门 5：PW 抽验 5 用例 + 截图。
① 产品档案 createModal 三段式：两字段在；租入价切「按次」→ 周期单位禁用+hint=元/只·次；切回→元/只·月
② 新建产品模板同款断言
③ 数据字典点「计费方式」分类 → 主表 5 行、按张行停用 tag、pin-2 无「预留」
④ 租入单新建明细首行计费方式 select 首项=按月
⑤ 项目详情 计费方式 dval=按月计租 · 按次计费
JS 错 0；输出 PASS/FAIL 清单。
"""
import io, sys, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / 'P3-R01-包装租赁管理后台原型').as_posix()
SHOTS = ROOT / '_scan_tmpdir'
results = []
js_errors = []


def chk(name, cond, detail=''):
    results.append(('PASS' if cond else 'FAIL', name, detail))


with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})

    # ===== ① 产品档案 createModal 三段式 =====
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: js_errors.append(('产品档案', str(e))))
    pg.goto((BASE + '/基础数据/产品档案.html').as_uri() if False else pathlib.Path(BASE + '/基础数据/产品档案.html').as_uri())
    pg.wait_for_load_state('load')
    pg.evaluate("() => document.getElementById('createModal').classList.add('show')")
    chk('① createModal 三段式两字段在',
        pg.locator('#rentInModeSel').count() == 1 and pg.locator('#rentalModeSel').count() == 1
        and pg.locator('#rentInUnitSel').count() == 1 and pg.locator('#rentalUnitSel').count() == 1
        and pg.locator('#rentInHint').count() == 1 and pg.locator('#rentalHint').count() == 1)
    chk('① 单位下拉已注 unitSel', pg.evaluate("() => !!document.getElementById('unitSel')"))
    # 初始 hint
    h0 = pg.locator('#rentInHint').text_content()
    chk('① 初始 hint=元/只·月', h0.strip() == '元/只·月', h0)
    # 切「按次」→ 单位禁用 + hint=元/只·次
    pg.locator('#rentInModeSel').select_option('按次')
    dis = pg.evaluate("() => document.getElementById('rentInUnitSel').disabled")
    h1 = pg.locator('#rentInHint').text_content()
    chk('① 租入价按次→周期单位禁用+hint=元/只·次', dis is True and h1.strip() == '元/只·次', 'disabled=%s hint=%s' % (dis, h1))
    # 切回→恢复
    pg.locator('#rentInModeSel').select_option('按时间周期')
    dis2 = pg.evaluate("() => document.getElementById('rentInUnitSel').disabled")
    h2 = pg.locator('#rentInHint').text_content()
    chk('① 切回按时间周期→启用+hint=元/只·月', dis2 is False and h2.strip() == '元/只·月', 'disabled=%s hint=%s' % (dis2, h2))
    # 租赁价同款抽验（切按次）
    pg.locator('#rentalModeSel').select_option('按次')
    h3 = pg.locator('#rentalHint').text_content()
    chk('① 租赁价按次→hint=元/只·次', h3.strip() == '元/只·次', h3)
    pg.locator('#rentalModeSel').select_option('按时间周期')
    pg.evaluate("() => document.getElementById('createModal').classList.remove('show')")
    pg.screenshot(path=str(SHOTS / 'g21-cp-archive.png'), full_page=True)

    # ===== ② 新建产品模板同款 =====
    pg2 = ctx.new_page()
    pg2.on('pageerror', lambda e: js_errors.append(('新建产品', str(e))))
    pg2.goto(pathlib.Path(BASE + '/基础数据/弹窗/新建产品.html').as_uri())
    pg2.wait_for_load_state('load')
    ok2 = all(pg2.locator('#' + i).count() == 1 for i in
              ['rentInModeSel', 'rentInUnitSel', 'rentalModeSel', 'rentalUnitSel', 'rentInHint', 'rentalHint', 'unitSel'])
    chk('② 模板三段式控件齐', ok2)
    pg2.locator('#rentInModeSel').select_option('按次')
    d = pg2.evaluate("() => document.getElementById('rentInUnitSel').disabled")
    hh = pg2.locator('#rentInHint').text_content()
    chk('② 模板按次联动', d is True and hh.strip() == '元/只·次', 'disabled=%s hint=%s' % (d, hh))
    pg2.screenshot(path=str(SHOTS / 'g21-tpl-newproduct.png'), full_page=True)

    # ===== ③ 数据字典 =====
    pg3 = ctx.new_page()
    pg3.on('pageerror', lambda e: js_errors.append(('数据字典', str(e))))
    pg3.goto(pathlib.Path(BASE + '/系统管理/数据字典.html').as_uri())
    pg3.wait_for_load_state('load')
    pg3.locator('.dic-item', has_text='计费方式').click()
    pg3.wait_for_timeout(600)
    rows = pg3.locator('.table-wrap table tbody tr, .card table tbody tr').all_inner_texts()
    # 主表=运行时 dictItems 驱动表（行含 BF- 编码前缀）
    bill_rows = [r for r in rows if r.strip().startswith('BF-')]
    chk('③ 计费方式主表 5 行', len(bill_rows) == 5, '%d 行: %s' % (len(bill_rows), [r.split(chr(9))[1] if chr(9) in r else r[:12] for r in bill_rows]))
    zhang = [r for r in rows if '按张' in r]
    chk('③ 按张行停用 tag（主表+静态卡均停用）', len(zhang) >= 1 and all('停用' in r for r in zhang), ' / '.join(r.replace(chr(9), '/')[:36] for r in zhang))
    pin2 = pg3.evaluate("""() => { const el = document.getElementById('proto-pin-2'); return el ? el.textContent : ''; }""")
    chk('③ pin-2 无「预留」+含计费方式', '预留' not in pin2 and '计费方式' in pin2 and '2026-09-11 拍板' in pin2, pin2[:60])
    pg3.screenshot(path=str(SHOTS / 'g21-dict-bf5.png'), full_page=True)

    # ===== ④ 租入单新建明细首行 select 首项=按月 =====
    pg4 = ctx.new_page()
    pg4.on('pageerror', lambda e: js_errors.append(('租入单新建', str(e))))
    pg4.goto(pathlib.Path(BASE + '/租赁管理/弹窗/租入单新建.html').as_uri())
    pg4.wait_for_load_state('load')
    first_opt = pg4.evaluate("""() => {
      const sels = [...document.querySelectorAll('select')].filter(s => [...s.options].some(o => o.text === '按月'));
      if (!sels.length) return null;
      return sels[0].options[0].text + '|' + sels[0].selectedOptions[0].text;
    }""")
    chk('④ 租入单新建首个计费 select 首项/选中=按月', first_opt == '按月|按月', str(first_opt))
    seg = pg4.evaluate("""() => document.body.textContent.includes('租入明细（多货品 · 计费方式：按月 / 按次）')""")
    chk('④ 新段标题渲染', seg)
    pg4.screenshot(path=str(SHOTS / 'g21-rzx-neworder.png'), full_page=True)

    # ===== ⑤ 项目详情 dval =====
    pg5 = ctx.new_page()
    pg5.on('pageerror', lambda e: js_errors.append(('项目详情', str(e))))
    pg5.goto(pathlib.Path(BASE + '/项目管理/项目详情.html').as_uri())
    pg5.wait_for_load_state('load')
    dval = pg5.evaluate("""() => { const els = [...document.querySelectorAll('.dval')]; return els.map(e => e.textContent.trim()).filter(t => t.includes('计')); }""")
    chk('⑤ 项目详情计费方式 dval=按月计租 · 按次计费', '按月计租 · 按次计费' in dval, str(dval)[:80])
    pg5.screenshot(path=str(SHOTS / 'g21-xmxq-dval.png'), full_page=True)

    b.close()

chk('全 5 页 JS 错 0', not js_errors, '; '.join('%s:%s' % e for e in js_errors[:3]))
fails = [r for r in results if r[0] == 'FAIL']
for st, name, detail in results:
    print(st, name, ('(%s)' % detail) if detail else '')
print('==== G21 PW 门：', 'ALL PASS' if not fails else 'FAIL %d 项' % len(fails), '共 %d 项 ====' % len(results))
sys.exit(1 if fails else 0)
