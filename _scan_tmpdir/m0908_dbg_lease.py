# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
BASE = 'file:///' + str(PROTO).replace('\\', '/').replace(' ', '%20') + '/'
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(BASE + '租赁管理/租赁单列表.html')
    pg.wait_for_selector('tbody tr')
    pg.evaluate("openModal('createModal')")
    pg.wait_for_timeout(200)
    shown = pg.evaluate("document.getElementById('createModal').classList.contains('show')")
    print('打开 createModal:', shown)
    # 结构：modal overlay 内 div 平衡检查
    bal = pg.evaluate("""() => {
      const ov = document.getElementById('createModal');
      const html = ov.outerHTML;
      let d = 0;
      for (const m of html.matchAll(/<div\\b/g)) d++;
      let c = 0;
      for (const m of html.matchAll(/<\\/div>/g)) c++;
      return {open: d, close: c};
    }""")
    print('createModal div 开/闭:', bal)
    # 点取消
    r = pg.evaluate("""() => {
      const btns = [...document.querySelectorAll('#createModal .modal-footer button')];
      const cancel = btns.find(b => b.textContent.trim() === '取消');
      const info = {
        cancelOnclick: cancel ? cancel.getAttribute('onclick') : null,
        hasCloseModal: typeof closeModal,
        dblCreate: document.querySelectorAll('#createModal').length,
        modalIds: [...document.querySelectorAll('.modal-overlay')].map(m => m.id),
      };
      if (!cancel) return 'no cancel ' + JSON.stringify(info);
      cancel.click();
      info.after = document.getElementById('createModal').classList.contains('show');
      return JSON.stringify(info);
    }""")
    print('取消点击:', r)
    print('errs:', errs[:3])
    b.close()
