# g62 库存台账增强验证（0924 道远拍板：收发类别细分列+仓库筛选）
# 只读验证：列结构 / 下拉选项 / 渲染行 / 期初归还列有值 / 筛选联动 / JS 零报错 / 截图
import threading, http.server, functools, json, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8932), functools.partial(http.server.SimpleHTTPRequestHandler))
threading.Thread(target=srv.serve_forever, daemon=True).start()

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    errs = []
    pg.on('pageerror', lambda e: errs.append('PAGEERROR: ' + str(e)))
    pg.on('console', lambda m: errs.append('CONSOLE: ' + m.text) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:8932/%E4%BB%93%E5%82%A8%E4%BD%9C%E4%B8%9A/%E6%94%B6%E5%8F%91%E5%AD%98.html')
    pg.wait_for_timeout(600)

    ths = pg.eval_on_selector_all('thead th', 'els=>els.map(e=>e.innerText.trim())')
    rows_all = pg.eval_on_selector_all('#sfsBody tr', 'els=>els.length')
    area_opts = pg.eval_on_selector_all('#sfsArea option', 'els=>els.map(e=>e.innerText)')
    row1 = pg.eval_on_selector('#sfsBody tr:first-child', 'e=>Array.from(e.children).map(c=>c.innerText.trim())')
    print('TH =', json.dumps(ths, ensure_ascii=False))
    print('ROWS_ALL =', rows_all)
    print('AREA_OPTS =', json.dumps(area_opts, ensure_ascii=False))
    print('ROW1 =', json.dumps(row1, ensure_ascii=False))

    # 仓库筛选联动：选 客户虚拟仓 → 行数应变少
    pg.select_option('#sfsArea', '客户虚拟仓')
    pg.click('button:has-text("查询")')
    pg.wait_for_timeout(300)
    rows_area = pg.eval_on_selector_all('#sfsBody tr', 'els=>els.length')
    print('ROWS_AREA(客户虚拟仓) =', rows_area)

    # 回全部，取期初列/归还列前几行（验证 G57 漏计修正后两列有值）
    pg.select_option('#sfsArea', '全部')
    pg.click('button:has-text("查询")')
    pg.wait_for_timeout(300)
    ini_col = pg.eval_on_selector_all('#sfsBody td:nth-child(3)', 'els=>els.map(e=>e.innerText.trim())')
    gui_col = pg.eval_on_selector_all('#sfsBody td:nth-child(6)', 'els=>els.map(e=>e.innerText.trim())')
    print('INI_COL =', json.dumps(ini_col[:8], ensure_ascii=False))
    print('GUI_COL =', json.dumps(gui_col[:8], ensure_ascii=False))
    ini_nonzero = sum(1 for v in ini_col if v not in ('0', ''))
    gui_nonzero = sum(1 for v in gui_col if v not in ('0', ''))
    print('INI_NONZERO_ROWS =', ini_nonzero, '| GUI_NONZERO_ROWS =', gui_nonzero)

    print('JS_ERR =', json.dumps(errs, ensure_ascii=False))
    pg.screenshot(path='_scan_tmpdir/g62_sfs_enhanced.png', full_page=True)
    b.close()
srv.shutdown()
print('SHOT = ok')
