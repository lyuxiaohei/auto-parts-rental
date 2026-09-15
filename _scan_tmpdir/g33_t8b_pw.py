# -*- coding: utf-8 -*-
"""G33 T8b: Playwright 抽验三新页（JS 0 + 关键交互 + 截图留档）+ verify_listfull batch2 由外部跑"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
SHOTS = ROOT / '_scan_tmpdir' / 'g33_shots'
SHOTS.mkdir(exist_ok=True)

PAGES = [
    ('采购退货单列表', '采购管理/采购退货单列表.html'),
    ('销售退货单列表', '销售管理/销售退货单列表.html'),
    ('退款登记', '财务协同/退款登记.html'),
]

results, fails = [], []
def check(no, name, ok, note=''):
    results.append((no, name, ok, note))
    if not ok: fails.append(no)

with sync_playwright() as pw:
    br = pw.chromium.launch()
    for label, rel in PAGES:
        pg = br.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto((PROTO / rel).as_uri())
        pg.wait_for_load_state('load')
        pg.wait_for_timeout(600)
        # 1) JS 0
        check(label + '-1', 'JS 错误 0', len(errs) == 0, '; '.join(errs[:2]))
        # 2) 列表渲染 3 行（数据驱动）
        rows = pg.evaluate("() => document.querySelectorAll('.card .table-wrap table tbody > tr').length")
        check(label + '-2', 'tbody 渲染 3 行', rows == 3, f'实测 {rows}')
        # 3) stab 计数=3
        cnt = pg.evaluate("() => { const s=document.querySelector('.stabs .stab .stab-count'); return s?s.textContent:null }")
        check(label + '-3', '全部 stab 计数=3', cnt == '3', f'实测 {cnt}')
        # 4) 菜单新项在组内且 selected 正确
        sel = pg.evaluate("() => { const e=document.querySelector('.sm-link.selected'); return e?e.textContent.trim():null }")
        check(label + '-4', 'selected=' + label, unquote(sel) == ('采购退货' if '采购' in label else '销售退货' if '销售' in label else '退款登记'), f'selected={sel}')
        # 5) 新建弹窗开合（createModal）
        pg.evaluate("() => openModal('createModal')")
        pg.wait_for_timeout(250)
        vis = pg.evaluate("() => document.getElementById('createModal').classList.contains('show')")
        check(label + '-5', 'createModal 可开', vis)
        pg.evaluate("() => closeModal('createModal')")
        # 6) 审核弹窗 ?audit=1 auto-open（编程导航）
        pg.goto((PROTO / rel).as_uri() + '?audit=1')
        pg.wait_for_timeout(1500)
        avis = pg.evaluate("() => document.getElementById('auditModal') ? document.getElementById('auditModal').classList.contains('show') : false")
        check(label + '-6', '?audit=1 自动开审核弹窗', avis)
        # 7) 详情弹窗 onclick 直达（openRetDetail）
        pg.evaluate("() => { const a=[...document.querySelectorAll('tbody a')].find(x=>x.textContent.trim()==='详情'); if(a) a.click(); }")
        pg.wait_for_timeout(400)
        dvis = pg.evaluate("() => document.getElementById('detailModal').classList.contains('show')")
        dbody = pg.evaluate("() => (document.getElementById('detailBody')||{}).textContent ? document.getElementById('detailBody').textContent.length : 0")
        check(label + '-7', '详情 onclick 打开 detailModal 且有内容', dvis and dbody > 50, f'show={dvis} bodyLen={dbody}')
        # 截图（列表态）
        pg.goto((PROTO / rel).as_uri())
        pg.wait_for_load_state('load')
        pg.wait_for_timeout(500)
        shot = SHOTS / (rel.split('/')[-1].replace('.html', '') + '.png')
        pg.screenshot(path=str(shot), full_page=False)
        print('截图:', shot)
        pg.close()
    br.close()

for no, name, ok, note in results:
    print(('PASS ' if ok else 'FAIL ') + no + ' ' + name + ((' ｜' + note) if not ok else ''))
print('==== G33 PW 抽验：%d 项断言，失败 %d 项 ====' % (len(results), len(fails)))
sys.exit(1 if fails else 0)
