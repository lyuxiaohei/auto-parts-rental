# -*- coding: utf-8 -*-
"""收货信息 PW 验证：列表 ops 渲染 8 行按钮·编程点击开 recvInfoModal·三字段断言·JS 0
+ 模板页自开弹窗断言 + 截图留档。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
OUT = Path(__file__).resolve().parent
fails = []
def check(name, ok, detail=''):
    print(('PASS' if ok else 'FAIL'), '|', name, ('| ' + detail) if detail else '')
    if not ok: fails.append(name)

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    # ---- 列表页 ----
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    page.goto((PROTO / '基础数据/客商管理.html').as_uri(), wait_until='load')
    page.wait_for_timeout(500)
    n_btn = page.locator('tbody tr .ops a', has_text='收货信息').count()
    check('列表 ops 渲染「收货信息」按钮×8（实体驱动）', n_btn == 8, 'n=%d' % n_btn)
    n_kp = page.locator('tbody tr .ops a', has_text='开票资料').count()
    check('既有「开票资料」按钮仍在×8', n_kp == 8, 'n=%d' % n_kp)
    # 编程点击首行收货信息（IAB 管道缺陷规避）
    page.evaluate("""() => {
      const a = [...document.querySelectorAll('tbody tr .ops a')].find(x => x.textContent.trim() === '收货信息');
      a.click();
    }""")
    page.wait_for_timeout(200)
    shown = page.evaluate("document.getElementById('recvInfoModal').classList.contains('show')")
    labels = page.evaluate("""() => [...document.querySelectorAll('#recvInfoModal .form-label')]
        .map(x => x.textContent.trim())""")
    check('点击打开 recvInfoModal 且三字段=收货人/收货电话/收货地址',
          shown and labels == ['收货人', '收货电话', '收货地址'], str(labels))
    addr = page.locator('#recvInfoModal input').nth(2).input_value()
    check('收货地址预填演示值', '长春' in addr, addr[:30])
    page.evaluate("document.getElementById('recvInfoModal').classList.remove('show')")
    # 实体 ops 一致性：第 8 行（DW-0201）也有按钮（上面 count=8 已覆盖）
    check('客商管理页 JS 错误 0', len(errs) == 0, str(errs[:2]))
    page.screenshot(path=str(OUT / 'g-recv-list.png'))
    page.close()
    # ---- 模板页 ----
    page = browser.new_page(viewport={'width': 1440, 'height': 720})
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    page.goto((PROTO / '基础数据/弹窗/客商收货信息.html').as_uri(), wait_until='load')
    page.wait_for_timeout(300)
    shown = page.evaluate("document.querySelector('.modal-overlay').classList.contains('show')")
    title = page.locator('.modal-title').text_content()
    labels = page.evaluate("""() => [...document.querySelectorAll('.modal-body .form-label')]
        .map(x => x.textContent.trim())""")
    fab = page.locator('.f01-fab').count()
    check('模板页弹窗自开+标题收货信息+三字段+fab 在',
          shown and title == '收货信息' and labels == ['收货人', '收货电话', '收货地址'] and fab == 1,
          'title=%s labels=%s fab=%d' % (title, labels, fab))
    check('模板页 JS 错误 0', len(errs) == 0, str(errs[:2]))
    page.screenshot(path=str(OUT / 'g-recv-tpl.png'))
    page.close()
    browser.close()

print()
print('==== PW 验证：失败 %d 项 ====' % len(fails))
sys.exit(1 if fails else 0)
