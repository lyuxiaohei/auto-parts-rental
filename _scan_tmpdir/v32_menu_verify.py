# -*- coding: utf-8 -*-
"""菜单重组 v4 · Playwright 菜单验证门（G31·D-114：小标签取消+租入管理升一级）
用法: python _scan_tmpdir/v32_menu_verify.py
纪律：编程点击+导航等待、URL unquote()、文本断言 textContent。
v5 断言基线（G33·D-123）：v4 基础上 采购管理+采购退货／销售管理+销售退货／财务管理+退款登记；菜单项 33→36。
"""
import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"

results = []
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

    # ① 九组序（v4：+租入管理·紧随租赁管理）
    gnames = [g['name'] for g in groups]
    check('①', '九组序=项目管理/基础资料/采购管理/销售管理/租赁管理/租入管理/仓储管理/财务管理/系统管理',
          gnames == ['项目管理', '基础资料', '采购管理', '销售管理', '租赁管理', '租入管理', '仓储管理', '财务管理', '系统管理'],
          '→'.join(gnames))

    # ② 一级仅我的待办
    singles = [m['name'] for m in menu if not m['hasSub']]
    check('②', '一级菜单仅「我的待办」', singles == ['我的待办'], '→'.join(singles))

    # ③ 项目管理组 2 项
    g_pm = next(g for g in groups if g['name'] == '项目管理')
    pm_items = [s['text'] for s in g_pm['sub'] if not s['isTag']]
    check('③', '项目管理组恰 2 项=项目看板/项目列表',
          pm_items == ['项目看板', '项目列表'], '→'.join(pm_items))

    # ④ 财务看板=财务管理组首普通项（非小标签）
    g_fin = next(g for g in groups if g['name'] == '财务管理')
    fin_first = g_fin['sub'][0]
    n_sun = pg.evaluate("() => [...document.querySelectorAll('.side-menu .sm-link')].filter(e=>e.textContent.trim()==='财务看板').length")
    check('④', '财务看板=财务管理组首普通菜单项（非小标签，全菜单恰 1 处）',
          fin_first['text'] == '财务看板' and not fin_first['isTag'] and n_sun == 1,
          f"组首={fin_first['text']} isTag={fin_first['isTag']} 出现{n_sun}次")

    # ⑥ 财务管理组小标签=应收(4)/应付(2)（D-114：财务组小标签维持）
    fin_seq = [('T' if s['isTag'] else 'I') + s['text'] for s in g_fin['sub']]
    check('⑥', '财务管理组 财务看板+应收(4)+应付(应付账单/付款登记)+退款登记（G33 v5）',
          fin_seq == ['I财务看板', 'T应收', 'I应收账单', 'I开票登记', 'I收款登记', 'I收款核销',
                      'T应付', 'I应付账单', 'I付款登记', 'I退款登记'], ' '.join(fin_seq))

    # ⑥b 采购管理组 v5：+采购退货（G33）
    g_pur = next(g for g in groups if g['name'] == '采购管理')
    pur_items = [s2['text'] for s2 in g_pur['sub'] if not s2['isTag']]
    check('⑥b', 'v5 采购管理组 3 项=采购订单/采购入库/采购退货', pur_items == ['采购订单', '采购入库', '采购退货'], '→'.join(pur_items))

    # ⑥c 销售管理组 v5：+销售退货（G33）
    g_sal = next(g for g in groups if g['name'] == '销售管理')
    sal_items = [s2['text'] for s2 in g_sal['sub'] if not s2['isTag']]
    check('⑥c', 'v5 销售管理组 3 项=销售订单/销售出库/销售退货', sal_items == ['销售订单', '销售出库', '销售退货'], '→'.join(sal_items))

    # ⑥d 菜单项合计 36（v5：33+3）
    n_items = pg.evaluate("() => document.querySelectorAll('.sm-sub .sm-link').length + document.querySelectorAll('.side-menu > li:not(.has-sub) > .sm-link').length")
    check('⑥d', '菜单项合计 36（v5：33+3）', n_items == 36, f'实测 {n_items}')

    # ⑦ 仓储管理组 v4 平铺（小标签取消·D-114）
    g_wh = next(g for g in groups if g['name'] == '仓储管理')
    wh_seq = [('T' if s['isTag'] else 'I') + s['text'] for s in g_wh['sub']]
    check('⑦', 'v4 仓储管理组无小标签·5 项平铺=库存查询/盘点记录/库存调拨/其他入库/其他出库',
          wh_seq == ['I库存查询', 'I盘点记录', 'I库存调拨', 'I其他入库', 'I其他出库'], ' '.join(wh_seq))

    # ⑧ 租赁管理组 v4 平铺（小标签取消·租入 3 项迁出）
    g_lease = next(g for g in groups if g['name'] == '租赁管理')
    lease_seq = [('T' if s['isTag'] else 'I') + s['text'] for s in g_lease['sub']]
    check('⑧', 'v4 租赁管理组无小标签·3 项平铺=租赁单/租赁出库/退租入库',
          lease_seq == ['I租赁单', 'I租赁出库', 'I退租入库'], ' '.join(lease_seq))

    # ⑧b 租入管理组 v4 新组（升一级·3 项）
    g_ri = next(g for g in groups if g['name'] == '租入管理')
    ri_seq = [('T' if s['isTag'] else 'I') + s['text'] for s in g_ri['sub']]
    check('⑧b', 'v4 租入管理组 3 项=租入单/租入入库/租入归还（无小标签）',
          ri_seq == ['I租入单', 'I租入入库', 'I租入归还'], ' '.join(ri_seq))

    # ⑨ 菜单无「盘点录入」项
    all_text = pg.evaluate("() => document.querySelector('.side-menu').textContent")
    check('⑨', '菜单无「盘点录入」项', '盘点录入' not in all_text)

    # ⑮ 菜单全部 go() 目标文件存在（v4：迁移页防死链·从看板页侧边栏收集）
    menu_html = pg.evaluate("() => document.querySelector('.side-menu').innerHTML")
    targets = re.findall(r"go\('([^']+)'\)", menu_html)
    missing = [t for t in set(targets)
               if not (PROTO / '首页' / t).exists()]
    check('⑮', f'侧边栏 {len(set(targets))} 个 go() 目标全部存在', not missing, '缺失: ' + '; '.join(missing))

    # ⑤ 点击财务看板落地 财务协同/盈亏报表.html
    with pg.expect_navigation():
        pg.evaluate("() => [...document.querySelectorAll('.sm-link')].find(e=>e.textContent.trim()==='财务看板').click()")
    pg.wait_for_load_state('load')
    url1 = unquote(pg.url)
    check('⑤', '点击财务看板落地 财务协同/盈亏报表.html',
          url1.endswith('财务协同/盈亏报表.html'), url1)
    sel1 = pg.evaluate("() => { const e=document.querySelector('.sm-link.selected'); return e?e.textContent.trim():null }")
    g_fin2 = pg.evaluate(MENU_JS)
    fin_open = next(g for g in g_fin2 if g['name'] == '财务管理')['open']
    check('⑤b', '盈亏报表页 selected=财务看板 且 财务管理组 open', sel1 == '财务看板' and fin_open, f'selected={sel1} open={fin_open}')

    # ⑪ 我的待办一级直达
    with pg.expect_navigation():
        pg.evaluate("() => [...document.querySelectorAll('.side-menu > li > .sm-link')].find(e=>e.textContent.trim()==='我的待办').click()")
    pg.wait_for_load_state('load')
    url2 = unquote(pg.url)
    check('⑪', '我的待办一级直达 我的待办.html', url2.endswith('我的待办.html'), url2)

    # ⑭ 租入单列表页（v4 迁移后）：selected=租入单·open=租入管理·租赁管理组不 open
    pg.goto((PROTO / '租入管理/租入单列表.html').as_uri())
    pg.wait_for_load_state('load')
    sel_ri = pg.evaluate("() => { const e=document.querySelector('.sm-link.selected'); return e?e.textContent.trim():null }")
    m_ri = pg.evaluate(MENU_JS)
    ri_open = next(g for g in m_ri if g['name'] == '租入管理')['open']
    lease_open = next(g for g in m_ri if g['name'] == '租赁管理')['open']
    check('⑭', '租入单列表页 selected=租入单·open=租入管理·租赁管理组不 open',
          sel_ri == '租入单' and ri_open and not lease_open,
          f'selected={sel_ri} 租入组open={ri_open} 租赁组open={lease_open}')

    # ⑩ 盘点录入.html 页 selected=盘点记录
    pg.goto((PROTO / '仓储作业/盘点录入.html').as_uri())
    pg.wait_for_load_state('load')
    sel2 = pg.evaluate("() => { const e=document.querySelector('.sm-link.selected'); return e?e.textContent.trim():null }")
    check('⑩', '盘点录入页 selected=盘点记录（open=仓储管理）',
          sel2 == '盘点记录' and next(g for g in pg.evaluate(MENU_JS) if g['name'] == '仓储管理')['open'],
          f'selected={sel2}')

    # ⑫ 角色管理页 selected=角色管理·open=系统管理
    pg.goto((PROTO / '系统管理/角色管理.html').as_uri())
    pg.wait_for_load_state('load')
    sel3 = pg.evaluate("() => { const e=document.querySelector('.sm-link.selected'); return e?e.textContent.trim():null }")
    sys_open = next(g for g in pg.evaluate(MENU_JS) if g['name'] == '系统管理')['open']
    check('⑫', '角色管理页 selected=角色管理·open=系统管理', sel3 == '角色管理' and sys_open, f'selected={sel3} open={sys_open}')

    # ⑬ 各页 0 JS 错误
    check('⑬', '各页 0 JS 错误（看板/盈亏报表/我的待办/租入单列表/盘点录入/角色管理）', len(js_errors) == 0, '; '.join(js_errors[:3]))

    br.close()

fails = [r for r in results if not r[2]]
for no, name, ok, note in results:
    print(f"{'PASS' if ok else 'FAIL'} {no} {name}" + (f'  ｜{note}' if not ok or no in ('⑤', '⑪', '⑮') else ''))
print(f"==== 菜单 v5 验证门：{len(results)} 项断言，失败 {len(fails)} 项 ====")
sys.exit(1 if fails else 0)
