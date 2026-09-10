# -*- coding: utf-8 -*-
"""菜单重组 v3.2 · Playwright 菜单验证门（G02 文档 C 表 12 项 + 各页 0 JS 错误 = 13 项）
用法: python _scan_tmpdir/v32_menu_verify.py
纪律：编程点击+导航等待、URL unquote()、文本断言 textContent。
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"

results = []  # (编号, 名称, 是否通过, 备注)
js_errors = []

def check(no, name, ok, note=''):
    results.append((no, name, bool(ok), note))

MENU_JS = r"""
() => {
  const top = [...document.querySelectorAll('.side-menu > li')];
  const parse = li => {
    const link = li.querySelector(':scope > .sm-link');
    const sub = [...li.querySelectorAll(':scope > .sm-sub > li')].map(s => ({
      isTag: (s.getAttribute('style') || '').includes('list-style:none'),
      text: s.textContent.trim()
    }));
    return {
      cls: li.className,
      hasSub: li.classList.contains('has-sub'),
      open: li.classList.contains('open'),
      name: link ? link.textContent.trim() : '',
      sub
    };
  };
  return top.map(parse);
}
"""

with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page()
    pg.on('pageerror', lambda e: js_errors.append(str(e)))

    # ---------- 主页：项目看板 ----------
    pg.goto((PROTO / '首页/项目看板.html').as_uri())
    pg.wait_for_load_state('load')
    menu = pg.evaluate(MENU_JS)
    groups = [m for m in menu if m['hasSub']]

    # ① 八组序
    gnames = [g['name'] for g in groups]
    check('①', '八组序=项目管理/基础资料/采购管理/销售管理/租赁管理/仓储管理/财务管理/系统管理',
          gnames == ['项目管理', '基础资料', '采购管理', '销售管理', '租赁管理', '仓储管理', '财务管理', '系统管理'],
          '→'.join(gnames))

    # ② 一级仅我的待办
    singles = [m['name'] for m in menu if not m['hasSub']]
    check('②', '一级菜单仅「我的待办」', singles == ['我的待办'], '→'.join(singles))

    # ③ 项目管理组 2 项
    g_pm = next(g for g in groups if g['name'] == '项目管理')
    pm_items = [s['text'] for s in g_pm['sub'] if not s['isTag']]
    check('③', '项目管理组恰 2 项=项目看板/项目列表（损益已移出）',
          pm_items == ['项目看板', '项目列表'], '→'.join(pm_items))

    # ④ 损益=财务管理组尾普通项（非小标签）
    g_fin = next(g for g in groups if g['name'] == '财务管理')
    fin_last = g_fin['sub'][-1]
    n_sun = pg.evaluate("() => [...document.querySelectorAll('.side-menu .sm-link')].filter(e=>e.textContent.trim()==='项目损益').length")
    check('④', '项目损益=财务管理组尾普通菜单项（非小标签，全菜单恰 1 处）',
          fin_last['text'] == '项目损益' and not fin_last['isTag'] and n_sun == 1,
          f"组尾={fin_last['text']} isTag={fin_last['isTag']} 出现{n_sun}次")

    # ⑥ 财务管理组小标签=应收(4)/应付(2)
    fin_seq = [('T' if s['isTag'] else 'I') + s['text'] for s in g_fin['sub']]
    check('⑥', '财务管理组 应收(应收账单/开票登记/收款登记/收款核销)+应付(应付账单/付款登记)+项目损益',
          fin_seq == ['T应收', 'I应收账单', 'I开票登记', 'I收款登记', 'I收款核销',
                      'T应付', 'I应付账单', 'I付款登记', 'I项目损益'], ' '.join(fin_seq))

    # ⑦ 仓储管理组三小标签=库存管理(3)/入库类(1)/出库类(1)
    g_wh = next(g for g in groups if g['name'] == '仓储管理')
    wh_seq = [('T' if s['isTag'] else 'I') + s['text'] for s in g_wh['sub']]
    check('⑦', '仓储管理组 库存管理(库存查询/盘点/库存调拨)+入库类(其他入库)+出库类(其他出库)',
          wh_seq == ['T库存管理', 'I库存查询', 'I盘点', 'I库存调拨',
                     'T入库类', 'I其他入库', 'T出库类', 'I其他出库'], ' '.join(wh_seq))

    # ⑧ 租赁管理组三小标签=租赁(2)/租入(3)/退租(1)（G07·2026-09-10 台账合并：在租台账/租出台账菜单项移除）
    g_lease = next(g for g in groups if g['name'] == '租赁管理')
    lease_seq = [('T' if s['isTag'] else 'I') + s['text'] for s in g_lease['sub']]
    check('⑧', '租赁管理组 租赁(租赁单/租赁出库)+租入(租入单/租入入库/租入归还)+退租(退租入库)',
          lease_seq == ['T租赁', 'I租赁单', 'I租赁出库',
                        'T租入', 'I租入单', 'I租入入库', 'I租入归还',
                        'T退租', 'I退租入库'], ' '.join(lease_seq))

    # ⑨ 菜单无「盘点录入」项
    all_text = pg.evaluate("() => document.querySelector('.side-menu').textContent")
    check('⑨', '菜单无「盘点录入」项', '盘点录入' not in all_text)

    # ⑤ 点击损益落地 财务协同/盈亏报表.html
    with pg.expect_navigation():
        pg.evaluate("() => [...document.querySelectorAll('.sm-link')].find(e=>e.textContent.trim()==='项目损益').click()")
    pg.wait_for_load_state('load')
    url1 = unquote(pg.url)
    check('⑤', '点击项目损益落地 财务协同/盈亏报表.html',
          url1.endswith('财务协同/盈亏报表.html'), url1)
    # 落地页 selected/open 顺带核对
    sel1 = pg.evaluate("() => { const e=document.querySelector('.sm-link.selected'); return e?e.textContent.trim():null }")
    g_fin2 = pg.evaluate(MENU_JS)
    fin_open = next(g for g in g_fin2 if g['name'] == '财务管理')['open']
    check('⑤b', '盈亏报表页 selected=项目损益 且 财务管理组 open', sel1 == '项目损益' and fin_open, f'selected={sel1} open={fin_open}')

    # ⑪ 我的待办一级直达（从盈亏报表页点击）
    with pg.expect_navigation():
        pg.evaluate("() => [...document.querySelectorAll('.side-menu > li > .sm-link')].find(e=>e.textContent.trim()==='我的待办').click()")
    pg.wait_for_load_state('load')
    url2 = unquote(pg.url)
    check('⑪', '我的待办一级直达 我的待办.html', url2.endswith('我的待办.html'), url2)

    # ⑩ 盘点录入.html 页 selected=盘点
    pg.goto((PROTO / '仓储作业/盘点录入.html').as_uri())
    pg.wait_for_load_state('load')
    sel2 = pg.evaluate("() => { const e=document.querySelector('.sm-link.selected'); return e?e.textContent.trim():null }")
    check('⑩', '盘点录入页 selected=盘点（open=仓储管理）',
          sel2 == '盘点' and next(g for g in pg.evaluate(MENU_JS) if g['name'] == '仓储管理')['open'],
          f'selected={sel2}')

    # ⑫ 角色管理页 selected=角色管理·open=系统管理
    pg.goto((PROTO / '系统管理/角色管理.html').as_uri())
    pg.wait_for_load_state('load')
    sel3 = pg.evaluate("() => { const e=document.querySelector('.sm-link.selected'); return e?e.textContent.trim():null }")
    sys_open = next(g for g in pg.evaluate(MENU_JS) if g['name'] == '系统管理')['open']
    check('⑫', '角色管理页 selected=角色管理·open=系统管理', sel3 == '角色管理' and sys_open, f'selected={sel3} open={sys_open}')

    # ⑬ 各页 0 JS 错误
    check('⑬', '各页 0 JS 错误（项目看板/盈亏报表/我的待办/盘点录入/角色管理）', len(js_errors) == 0, '; '.join(js_errors[:3]))

    br.close()

fails = [r for r in results if not r[2]]
for no, name, ok, note in results:
    print(f"{'PASS' if ok else 'FAIL'} {no} {name}" + (f'  ｜{note}' if not ok or no in ('⑤', '⑪') else ''))
print(f"==== 菜单 v3.2 验证门：{len(results)} 项断言，失败 {len(fails)} 项 ====")
sys.exit(1 if fails else 0)
