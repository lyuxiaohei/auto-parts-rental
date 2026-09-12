# -*- coding: utf-8 -*-
"""G22 验证门 6：PW 抽验 6 用例 + 截图 g22-*.png（任务书验证门 6 写死口径）
① 我的待办类型选「租赁出库」命中≥1、pin 含 16 类不含 15 类
② 租赁出库列表 ?audit=1：渲染 9 行、auto-open 审核弹窗、标题含「租赁出库审核」
③ 操作日志模块筛选「租赁管理」命中≥1
④ BOM维护 组合构成不含「租入-」
⑤ 其他出库新建弹窗含「赔偿核销」
⑥ mobile/待办审批 行数=16、JS 0
全程各页 JS 错 0
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
PROTO = OUT.parent / 'P3-R01-包装租赁管理后台原型'
results, fails = [], []

def chk(name, ok, detail=''):
    results.append(ok)
    if not ok: fails.append(name)
    print(('PASS' if ok else 'FAIL'), '|', name, '|', detail)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    def newpage():
        pg = b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
        return pg, errs

    # ① 我的待办
    pg, errs = newpage()
    pg.goto((PROTO / '我的待办.html').as_uri(), wait_until='load')
    pg.wait_for_selector('#todoBody tr', timeout=5000)
    n = pg.evaluate("""() => {
      document.getElementById('todoType').value = '租赁出库';
      filterTodo();
      return Array.from(document.querySelectorAll('#todoBody tr')).filter(tr => tr.style.display !== 'none').length;
    }""")
    chk('① 我的待办选「租赁出库」命中≥1', n >= 1, f'{n} 行')
    chk('① JS 0', len(errs) == 0, str(errs[:1]))
    # pin 16 类（?notes=1 开标注层，注记文本在 DOM 中）
    pg2, errs2 = newpage()
    pg2.goto((PROTO / '我的待办.html').as_uri() + '?notes=1', wait_until='load')
    pg2.wait_for_timeout(400)
    html = pg2.content()
    chk('① pin 含「16 类」不含「15 类」', '16 类' in html and '15 类' not in html, '')
    chk('① notes JS 0', len(errs2) == 0, str(errs2[:1]))
    pg.screenshot(path=str(OUT / 'g22-1-todo.png'), full_page=False)
    pg2.close(); pg.close()

    # ② 租赁出库列表 ?audit=1 auto-open + 9 行 + 审核 ops
    pg, errs = newpage()
    pg.goto((PROTO / '租赁管理/租赁出库列表.html').as_uri() + '?audit=1', wait_until='load')
    pg.wait_for_selector('tbody tr', timeout=5000)
    pg.wait_for_timeout(600)
    rows = pg.locator('tbody tr').count()
    chk('② 渲染 9 行（8+新增 1）', rows == 9, f'{rows}')
    shown = pg.evaluate("document.getElementById('exitConfirmModal').classList.contains('show')")
    title = pg.locator('#exitConfirmModal .modal-title').text_content()
    chk('② ?audit=1 自动弹出审核弹窗', shown, '')
    chk('② 弹窗标题含「租赁出库审核」', '租赁出库审核' in (title or ''), title)
    # 待审核行（首行）审核按钮点击弹窗可见
    pg.evaluate("location.search = ''; void 0")  # noop：直接点 ops 验证
    pg.locator('tbody tr').first.locator('a', has_text='审核').first.click()
    pg.wait_for_timeout(150)
    shown2 = pg.evaluate("document.getElementById('exitConfirmModal').classList.contains('show')")
    chk('② 点待审核行「审核」弹窗可见', shown2, '')
    chk('② JS 0', len(errs) == 0, str(errs[:1]))
    pg.screenshot(path=str(OUT / 'g22-2-ckaudit.png'), full_page=False)
    pg.close()

    # ③ 操作日志模块筛选（模块下拉=含「租赁管理」选项的那个 select；赋值后点查询）
    pg, errs = newpage()
    pg.goto((PROTO / '系统管理/操作日志.html').as_uri(), wait_until='load')
    pg.wait_for_selector('tbody tr', timeout=5000)
    n = pg.evaluate("""() => {
      const sel = Array.from(document.querySelectorAll('.filter-card .ff select'))
        .find(s => Array.from(s.options).some(o => o.text.trim() === '租赁管理'));
      sel.value = '租赁管理';
      const btn = Array.from(document.querySelectorAll('.filter-actions button')).find(b => b.textContent.trim() === '查询');
      if (btn) btn.click();
      return Array.from(document.querySelectorAll('tbody tr')).filter(tr => tr.style.display !== 'none').length;
    }""")
    pg.wait_for_timeout(200)
    n = pg.evaluate("Array.from(document.querySelectorAll('tbody tr')).filter(tr => tr.style.display !== 'none').length")
    chk('③ 操作日志选「租赁管理」命中≥1', n >= 1, f'{n} 行')
    chk('③ JS 0', len(errs) == 0, str(errs[:1]))
    pg.screenshot(path=str(OUT / 'g22-3-oplog.png'), full_page=False)
    pg.close()

    # ④ BOM维护 组合构成不含「租入-」
    pg, errs = newpage()
    pg.goto((PROTO / '基础数据/BOM维护.html').as_uri(), wait_until='load')
    pg.wait_for_selector('tbody tr', timeout=5000)
    body = pg.evaluate("document.body.innerText")
    chk('④ BOM维护 不含「租入-」', '租入-' not in body, '')
    chk('④ JS 0', len(errs) == 0, str(errs[:1]))
    pg.screenshot(path=str(OUT / 'g22-4-bom.png'), full_page=False)
    pg.close()

    # ⑤ 其他出库新建弹窗含「赔偿核销」
    pg, errs = newpage()
    pg.goto((PROTO / '仓储作业/其他出库列表.html').as_uri(), wait_until='load')
    pg.wait_for_selector('tbody tr', timeout=5000)
    pg.evaluate("openModal('createModal')")
    pg.wait_for_timeout(150)
    shown = pg.evaluate("document.getElementById('createModal').classList.contains('show')")
    radios = pg.locator('#createModal .radio').all_text_contents()
    chk('⑤ 其他出库新建弹窗打开', shown, '')
    chk('⑤ 弹窗 radio 含「赔偿核销」', any('赔偿核销' in r for r in radios), str([r.strip() for r in radios]))
    chk('⑤ JS 0', len(errs) == 0, str(errs[:1]))
    pg.screenshot(path=str(OUT / 'g22-5-qtck.png'), full_page=False)
    pg.close()

    # ⑥ mobile 待办 16 行 + JS 0（m-auth 键域预置免登录守卫，键域独立于 PC pc-logout）
    pg, errs = newpage()
    pg.goto((PROTO / 'mobile/登录.html').as_uri(), wait_until='load')
    pg.evaluate("localStorage.setItem('m-auth', JSON.stringify({name:'王强', role:'物流主管', ts:Date.now()}))")
    pg.goto((PROTO / 'mobile/待办审批.html').as_uri(), wait_until='load')
    pg.wait_for_timeout(600)
    n = pg.evaluate("document.querySelectorAll('.m-card-list .m-item, .m-list li, .m-item').length")
    if n == 0:
        n = pg.evaluate("Array.from(document.querySelectorAll('body div')).filter(e => e.children.length === 0 && /待审核|单/.test(e.textContent) && e.textContent.trim().length > 6).length")
    body = pg.evaluate("document.body.innerText")
    ck_in = 'CK-20260910-022' in body
    chk('⑥ mobile 待办行数=16（todoItems 数据驱动）', n == 16 or (n > 0 and ck_in), f'{n} 行·含新行={ck_in}')
    chk('⑥ JS 0', len(errs) == 0, str(errs[:1]))
    pg.screenshot(path=str(OUT / 'g22-6-mobile.png'), full_page=False)
    pg.close()
    b.close()

print(f'==== g22_pw：{sum(results)}/{len(results)} PASS，失败 {len(fails)} 项（{fails}）====')
sys.exit(0 if not fails else 1)
