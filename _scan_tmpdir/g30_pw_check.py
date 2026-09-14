# -*- coding: utf-8 -*-
"""G30 验证门 4：PW 抽验——数据字典页（新 13 组各≥1 行渲染+dic-item 计数+JS 0）+库位档案
（筛选/表单 select 4 值+JS 0）+截图×2（g30-dict.png / g30-kw.png）。
IAB 点击管道缺陷规避：dic-item 分类切换用 evaluate 编程点击。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
OUT = Path(__file__).resolve().parent

CATS = ['库存状态', '入库类型', '出库类型', '应收账单类型', '应付账单类型', '费用分类', '发票类型',
        '客商类型', '数据权限范围', '盘点口径', '周期单位', '物料分类', '待办单据类型']
EXPECT_N = {'库存状态': 5, '入库类型': 3, '出库类型': 4, '应收账单类型': 6, '应付账单类型': 5,
            '费用分类': 7, '发票类型': 2, '客商类型': 3, '数据权限范围': 3, '盘点口径': 2,
            '周期单位': 3, '物料分类': 6, '待办单据类型': 16}

fails = []
def check(name, ok, detail=''):
    print(('PASS' if ok else 'FAIL'), '|', name, ('| ' + detail) if detail else '')
    if not ok: fails.append(name)

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    # ---------- 数据字典页 ----------
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    page.goto((PROTO / '系统管理/数据字典.html').as_uri(), wait_until='load')
    page.wait_for_timeout(500)
    n_items = page.locator('.dic-list .dic-item').count()
    check('数据字典 dic-item=24', n_items == 24, 'n=%d' % n_items)
    bad = []
    for cat in CATS:
        # 编程点击分类（IAB 管道缺陷规避）
        page.evaluate("""(c) => {
          const its = document.querySelectorAll('.dic-list .dic-item');
          for (const it of its) if (it.querySelector('span').textContent.trim() === c) { it.click(); break; }
        }""", cat)
        page.wait_for_timeout(120)
        # 主表=.dic-wrap 内第一个 table（第二张为静态计费方式卡表，不计入）
        rows = page.locator('.dic-wrap table').first.locator('tbody tr').count()
        title = page.locator('.dic-wrap .card-head .card-title').text_content()
        cnt = page.evaluate("""(c) => {
          const its = document.querySelectorAll('.dic-list .dic-item');
          for (const it of its) if (it.querySelector('span').textContent.trim() === c)
            return it.querySelector('.cnt').textContent.trim();
          return '?';
        }""", cat)
        ok = rows == EXPECT_N[cat] and ('· ' + cat) in title and cnt == str(EXPECT_N[cat])
        if not ok: bad.append('%s rows=%d/%d title=%s cnt=%s' % (cat, rows, EXPECT_N[cat], title, cnt))
    check('数据字典 新 13 组逐组渲染行数=期望+标题联动+计数联动', not bad, '; '.join(bad) if bad else '13 组全对')
    # 首组 KC 首行内容抽验
    page.evaluate("""() => {
      const its = document.querySelectorAll('.dic-list .dic-item');
      for (const it of its) if (it.querySelector('span').textContent.trim() === '库存状态') { it.click(); break; }
    }""")
    page.wait_for_timeout(120)
    r0 = page.locator('.dic-wrap table tbody tr').first.text_content()
    check('KC-01 在库 行渲染含 code+名称+启用', 'KC-01' in r0 and '在库' in r0 and '启用' in r0, r0[:60])
    # createModal select option 抽验
    page.evaluate("document.getElementById('createModal').classList.add('show')")
    n_opt = page.locator('#createModal select option').count()
    has13 = page.evaluate("""() => {
      const os = [...document.querySelectorAll('#createModal select option')].map(o => o.textContent);
      return ['库存状态','待办单据类型','物料分类'].every(c => os.includes(c));
    }""")
    check('createModal 字典分类 select option=16 且含新组', n_opt == 16 and has13, 'opts=%d has13=%s' % (n_opt, has13))
    page.evaluate("document.getElementById('createModal').classList.remove('show')")
    check('数据字典页 JS 错误 0', len(errs) == 0, str(errs[:2]))
    page.screenshot(path=str(OUT / 'g30-dict.png'), full_page=False)
    page.close()

    # ---------- 库位档案 ----------
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    page.goto((PROTO / '基础数据/库位档案.html').as_uri(), wait_until='load')
    page.wait_for_timeout(500)
    sel = page.evaluate("""() => {
      const ffs = [...document.querySelectorAll('.ff')];
      const f = ffs.find(x => x.querySelector('.ff-label').textContent.includes('库位类型'));
      return [...f.querySelectorAll('option')].map(o => o.textContent);
    }""")
    check('库位档案 筛选 select=全部+KW4值', sel == ['全部', '存储位', '拣选位', '暂存位', '不合格品位'], str(sel))
    form = page.evaluate("""() => {
      const rows = [...document.querySelectorAll('#createModal .form-row')];
      const r = rows.find(x => x.querySelector('.form-label').textContent.includes('库位类型'));
      return [...r.querySelectorAll('option')].map(o => o.textContent);
    }""")
    check('库位档案 表单 select=KW4值（存储位默认）', form == ['存储位', '拣选位', '暂存位', '不合格品位'], str(form))
    body_txt = page.locator('tbody').first.text_content()
    check('库位档案 列表渲染正常（locations 数据驱动 11 行）',
          page.locator('tbody tr').count() >= 11 and '存储位' in body_txt)
    check('库位档案 JS 错误 0', len(errs) == 0, str(errs[:2]))
    page.screenshot(path=str(OUT / 'g30-kw.png'), full_page=False)
    page.close()
    browser.close()

print()
print('==== PW 抽验：失败 %d 项 ====' % len(fails))
sys.exit(1 if fails else 0)
