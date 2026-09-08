# -*- coding: utf-8 -*-
"""任务三·滚动条改造验证（2026-09-08）：全站 styleSheets 断言 + 三类 15 页截图"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
OUT = ROOT / '_scan_tmpdir' / 'scrollbar-check'
OUT.mkdir(exist_ok=True)

EXCLUDE = {'BOM.html'}
pages = sorted(p for p in PROTO.rglob('*.html')
               if '99-归档' not in str(p) and p.name not in EXCLUDE)

CHECK_JS = """() => {
  for (const sheet of document.styleSheets) {
    let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
    for (const r of rules) {
      if (r.selectorText && r.selectorText.indexOf('-webkit-scrollbar-thumb') > -1) {
        const bg = (r.style.background || r.style.backgroundColor || '').replace(/\\s+/g, '');
        if (bg === '#d9d9d9' || bg === 'rgb(217,217,217)') return 'PASS';
        return 'WRONG_BG:' + bg;
      }
    }
  }
  return 'NO_RULE';
}"""

SHOTS = [
    # (相对路径, 视口(w,h), 存名, 类别)
    ('首页/我的待办.html', (1280, 480), 'menu-1-我的待办', '菜单溢出'),
    ('项目管理/项目详情.html', (1280, 480), 'menu-2-项目详情', '菜单溢出'),
    ('财务协同/盈亏报表.html', (1280, 480), 'menu-3-盈亏报表', '菜单溢出'),
    ('系统管理/操作日志.html', (1280, 480), 'menu-4-操作日志', '菜单溢出'),
    ('仓储作业/盘点录入.html', (1280, 480), 'menu-5-盘点录入', '菜单溢出'),
    ('仓储作业/退租入库列表.html', (860, 800), 'table-1-退租入库列表', '宽表列表'),
    ('财务协同/应付账单.html', (860, 800), 'table-2-应付账单', '宽表列表'),
    ('销售管理/销售订单列表.html', (860, 800), 'table-3-销售订单列表', '宽表列表'),
    ('租赁管理/在租台账.html', (860, 800), 'table-4-在租台账', '宽表列表'),
    ('基础数据/器具档案.html', (860, 800), 'table-5-器具档案', '宽表列表'),
    ('销售管理/弹窗/租赁单详情.html', (1280, 560), 'modal-1-租赁单详情', '长内容弹窗'),
    ('采购管理/弹窗/租入单详情.html', (1280, 560), 'modal-2-租入单详情', '长内容弹窗'),
    ('仓储作业/弹窗/采购入库单详情.html', (1280, 560), 'modal-3-采购入库单详情', '长内容弹窗'),
    ('基础数据/弹窗/客商详情.html', (1280, 560), 'modal-4-客商详情', '长内容弹窗'),
    ('租赁管理/弹窗/丢损赔偿单详情.html', (1280, 560), 'modal-5-丢损赔偿单详情', '长内容弹窗'),
]

n_pass, fails = 0, []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for p in pages:
        pg = browser.new_page()
        try:
            pg.goto(p.resolve().as_uri(), wait_until='load')
            pg.wait_for_timeout(60)
            r = pg.evaluate(CHECK_JS)
            if r == 'PASS': n_pass += 1
            else: fails.append((str(p.relative_to(PROTO)), r))
        except Exception as e:
            fails.append((str(p.relative_to(PROTO)), 'EXC:' + str(e)[:60]))
        pg.close()
    print(f'styleSheets 断言: PASS {n_pass}/{len(pages)}，失败 {len(fails)}')
    for f in fails[:10]: print('  FAIL:', f)

    for rel, (w, h), name, cat in SHOTS:
        pg = browser.new_page(viewport=dict(width=w, height=h))
        pg.goto((PROTO / rel).resolve().as_uri(), wait_until='load')
        pg.wait_for_timeout(250)
        pg.screenshot(path=str(OUT / f'{name}.png'), full_page=False)
        pg.close()
    print(f'截图 {len(SHOTS)} 张 → {OUT}')
    browser.close()

sys.exit(1 if fails or n_pass != len(pages) else 0)
