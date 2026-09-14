# -*- coding: utf-8 -*-
"""物料合并 PW 验证：数据字典页 23 组+物料类型组 6 行渲染；产品档案筛选 6 值/列头/单级弹窗/
托盘拆分渲染；新建产品模板单级 6 值；JS 0+截图。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
OUT = Path(__file__).resolve().parent
CAT6 = ['围板箱', '塑料托盘', '木托盘', '料箱', '料架', '组件']
fails = []
def check(name, ok, detail=''):
    print(('PASS' if ok else 'FAIL'), '|', name, ('| ' + detail) if detail else '')
    if not ok: fails.append(name)

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    # ---- 数据字典页 ----
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    page.goto((PROTO / '系统管理/数据字典.html').as_uri(), wait_until='load')
    page.wait_for_timeout(400)
    n_items = page.locator('.dic-list .dic-item').count()
    check('数据字典 dic-item=23（24-物料分类）', n_items == 23, 'n=%d' % n_items)
    has_fl = page.evaluate("""() => [...document.querySelectorAll('.dic-list .dic-item span')]
        .some(s => s.textContent.trim() === '物料分类')""")
    check('物料分类 dic-item 已删除', not has_fl)
    page.evaluate("""() => {
      const its = document.querySelectorAll('.dic-list .dic-item');
      for (const it of its) if (it.querySelector('span').textContent.trim() === '物料类型') { it.click(); break; }
    }""")
    page.wait_for_timeout(150)
    rows = page.locator('.dic-wrap table').first.locator('tbody tr').count()
    names = page.locator('.dic-wrap table').first.locator('tbody tr td:nth-child(3)').all_text_contents()
    check('物料类型组渲染 6 行=分类值', rows == 6 and [n.strip() for n in names] == CAT6,
          '%d 行 %s' % (rows, names))
    check('数据字典 JS 0', len(errs) == 0, str(errs[:2]))
    page.screenshot(path=str(OUT / 'g-merge-dict.png'))
    page.close()

    # ---- 产品档案 ----
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    page.goto((PROTO / '基础数据/产品档案.html').as_uri(), wait_until='load')
    page.wait_for_timeout(400)
    ff = page.evaluate("""() => {
      const ffs = [...document.querySelectorAll('.ff')];
      const f = ffs.find(x => x.querySelector('.ff-label').textContent.includes('物料类型'));
      return f ? [...f.querySelectorAll('option')].map(o => o.textContent) : null;
    }""")
    check('筛选 ff=物料类型+全部+6 值', ff == ['全部'] + CAT6, str(ff))
    th = page.evaluate("""() => [...document.querySelectorAll('thead th')].map(t => t.textContent.trim())""")
    check('列头含「物料类型」无「物料分类」', '物料类型' in th and '物料分类' not in th, str(th[:4]))
    body = page.locator('tbody').first.text_content()
    check('列表渲染：木托盘/塑料托盘 tag 拆分', '木托盘' in body and '塑料托盘' in body)
    n_rows = page.locator('tbody tr').count()
    check('列表 12 行不変', n_rows == 12, 'n=%d' % n_rows)
    # 弹窗单级
    page.evaluate("document.getElementById('createModal').classList.add('show')")
    labels = page.evaluate("""() => [...document.querySelectorAll('#createModal .form-label')]
        .map(x => x.textContent.replace('*','').trim())""")
    check('createModal 单级：含物料类型·无物料分类·无器具/零部件',
          '物料类型' in labels and '物料分类' not in labels,
          str(labels[:6]))
    opts = page.evaluate("""() => {
      const rows = [...document.querySelectorAll('#createModal .form-row')];
      const r = rows.find(x => x.querySelector('.form-label').textContent.includes('物料类型'));
      return [...r.querySelectorAll('option')].map(o => o.textContent);
    }""")
    check('createModal 物料类型 option=6 分类值', opts == CAT6, str(opts))
    check('产品档案 JS 0', len(errs) == 0, str(errs[:2]))
    page.screenshot(path=str(OUT / 'g-merge-product.png'))
    page.close()

    # ---- 新建产品模板 ----
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    page.goto((PROTO / '基础数据/弹窗/新建产品.html').as_uri(), wait_until='load')
    page.wait_for_timeout(300)
    labels = page.evaluate("""() => [...document.querySelectorAll('.form-label')]
        .map(x => x.textContent.replace('*','').trim())""")
    check('模板单级：含物料类型·无物料分类·无器具选项',
          '物料类型' in labels and '物料分类' not in labels and '器具</option>' not in page.content(),
          str(labels[:5]))
    check('模板 JS 0', len(errs) == 0, str(errs[:2]))
    page.close()
    browser.close()

print()
print('==== 物料合并 PW：失败 %d 项 ====' % len(fails))
sys.exit(1 if fails else 0)
