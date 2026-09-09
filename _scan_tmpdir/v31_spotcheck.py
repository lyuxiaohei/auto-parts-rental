# -*- coding: utf-8 -*-
"""菜单重组 v3.1 · Playwright 抽验（第十五节 D 清单 ≥16 项）
口径：编程点击（IAB 管道规避）· textContent 断言 · URL unquote。
"""
import io, sys
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROTO = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
results, fails = [], []

def check(name, ok, detail=''):
    results.append((name, ok))
    if not ok:
        fails.append(name)
    print(('✅' if ok else '❌'), name, '|', detail)

def open_page(pg, browser):
    page = browser.new_page()
    page.goto((PROTO / pg).as_uri(), wait_until='load')
    page.wait_for_timeout(250)
    return page

def sidebar_eval(page, js):
    return page.evaluate(js)

def click_menu(page, label, suffix):
    """编程点击侧边栏/按钮后等导航落地（轮询 URL，规避提交时序）"""
    page.evaluate("(lb) => {[...document.querySelectorAll('a, button, .sm-link')].find(d => d.textContent.trim() === lb).click()}", label)
    for _ in range(50):
        if unquote(page.url).replace(chr(92), '/').endswith(suffix):
            break
        try:
            page.wait_for_timeout(100)
        except Exception:
            pass
    try:
        page.wait_for_load_state('load', timeout=8000)
    except Exception:
        pass
    for _ in range(20):
        if unquote(page.url).replace(chr(92), '/').endswith(suffix):
            break
        page.wait_for_timeout(150)
    return unquote(page.url)

# 断言用的侧边栏抽取 JS：返回 [{kind:group/item/tag/single, text, onclick, cls}]
SB_JS = """() => {
  const as = document.querySelector('aside.sidebar');
  const out = [];
  as.querySelectorAll('ul.side-menu > li').forEach(li => {
    if (li.classList.contains('sm-item') && li.classList.contains('has-sub')) {
      const hd = li.querySelector(':scope > .sm-link');
      out.push({kind:'group', text: hd.textContent.replace(/^[^一-龥A-Za-z0-9]+/, '').trim(), open: li.classList.contains('open')});
      li.querySelectorAll(':scope > ul.sm-sub > li').forEach(sub => {
        const d = sub.querySelector(':scope > .sm-link');
        if (d) out.push({kind: d.classList.contains('selected') ? 'item-selected' : 'item',
                         text: d.textContent.trim(), onclick: d.getAttribute('onclick') || ''});
        else out.push({kind:'tag', text: sub.textContent.trim()});
      });
    } else {
      const d = li.querySelector(':scope > .sm-link');
      if (d) out.push({kind: d.classList.contains('selected') ? 'single-selected' : 'single',
                       text: d.textContent.trim(), onclick: d.getAttribute('onclick') || ''});
    }
  });
  return out;
}"""

with sync_playwright() as pw:
    browser = pw.chromium.launch()

    # ── A. 组序列与残留（以数据字典页为样本） ──
    page = open_page('系统管理/数据字典.html', browser)
    sb = sidebar_eval(page, SB_JS)
    groups = [x['text'] for x in sb if x['kind'] == 'group']
    singles = [x['text'] for x in sb if x['kind'] in ('single', 'single-selected')]
    check('A1 组序首=项目管理且组序符合A表', groups == ['项目管理', '基础资料', '采购管理', '销售管理', '租赁管理', '仓储作业', '财务协同', '系统管理'], '→'.join(groups))
    check('A2 一级仅 我的待办（无项目看板/项目损益一级残留）', singles == ['我的待办'], '→'.join(singles))
    all_txt = page.evaluate("() => document.querySelector('aside.sidebar').textContent")
    check('A3 无旧组名（财务应收/财务应付/项目损益）', all(x not in all_txt for x in ['财务应收', '财务应付', '项目损益']), '')

    # ── B. 项目管理组 3 项与跳转 ──
    pm = [x for x in sb if x['text'] in ('项目看板', '项目列表', '损益') and x['kind'].startswith('item')]
    check('B1 项目管理组含 项目看板/项目列表/损益 三项', len(pm) == 3, str([(x['text'], x['onclick']) for x in pm]))
    check('B2 项目列表→项目档案.html', any(x['text'] == '项目列表' and '项目管理/项目档案.html' in x['onclick'] for x in pm), '')
    check('B3 损益→盈亏报表.html', any(x['text'] == '损益' and '财务协同/盈亏报表.html' in x['onclick'] for x in pm), '')

    # 跳转实测（编程点击）
    u = click_menu(page, '项目列表', '项目管理/项目档案.html')
    check('B4 点击项目列表落地 项目档案.html', u.endswith('项目管理/项目档案.html'), u.split('/')[-2:])
    page.close()
    page = open_page('系统管理/数据字典.html', browser)
    u = click_menu(page, '损益', '财务协同/盈亏报表.html')
    check('B5 点击损益落地 盈亏报表.html', u.endswith('财务协同/盈亏报表.html'), u.split('/')[-1])
    page.close()

    # ── C. 财务协同小标签（应收/应付及归属） ──
    page = open_page('财务协同/应收账单.html', browser)
    sb = sidebar_eval(page, SB_JS)
    i_fin = next(i for i, x in enumerate(sb) if x['kind'] == 'group' and x['text'] == '财务协同')
    i_next = next(i for i, x in enumerate(sb) if x['kind'] == 'group' and i > i_fin)
    fin = sb[i_fin:i_next]
    tags = [x['text'] for x in fin if x['kind'] == 'tag']
    ar_items = []
    cur = None
    for x in fin:
        if x['kind'] == 'tag':
            cur = x['text']
        elif x['kind'].startswith('item'):
            ar_items.append((cur, x['text']))
    check('C1 财务协同两小标签 应收/应付', tags == ['应收', '应付'], '→'.join(tags))
    check('C2 应收 4 项=应收账单/开票登记/收款登记/收款核销',
          [t for g, t in ar_items if g == '应收'] == ['应收账单', '开票登记', '收款登记', '收款核销'], str(ar_items))
    check('C3 应付 2 项=应付账单/付款登记',
          [t for g, t in ar_items if g == '应付'] == ['应付账单', '付款登记'], '')
    sel = [x['text'] for x in fin if x['kind'] == 'item-selected']
    check('C4 应收账单页 selected=应收账单 且财务协同组 open', sel == ['应收账单'] and sb[i_fin]['open'], str(sel))
    page.close()

    # ── D. 仓储小标签（库存管理/入库类/出库类及归属）+盘点录入退出菜单 ──
    page = open_page('仓储作业/库存查询.html', browser)
    sb = sidebar_eval(page, SB_JS)
    i_wh = next(i for i, x in enumerate(sb) if x['kind'] == 'group' and x['text'] == '仓储作业')
    i_next = next((i for i, x in enumerate(sb) if x['kind'] == 'group' and i > i_wh), len(sb))
    wh = sb[i_wh:i_next]
    tags = [x['text'] for x in wh if x['kind'] == 'tag']
    grp = {}
    cur = None
    for x in wh:
        if x['kind'] == 'tag':
            cur = x['text']; grp[cur] = []
        elif x['kind'].startswith('item'):
            grp[cur].append(x['text'])
    check('D1 仓储三小标签 库存管理/入库类/出库类', tags == ['库存管理', '入库类', '出库类'], '→'.join(tags))
    check('D2 库存管理 3 项=库存查询/盘点/库存调拨', grp.get('库存管理') == ['库存查询', '盘点', '库存调拨'], str(grp))
    check('D3 入库类=其他入库·出库类=其他出库', grp.get('入库类') == ['其他入库'] and grp.get('出库类') == ['其他出库'], '')
    check('D4 仓储菜单无盘点录入项', '盘点录入' not in [t for v in grp.values() for t in v], '')
    page.close()

    # ── E. 租赁小标签（租赁/租入/退租及归属）+租赁出库菜单名+跳转 ──
    page = open_page('租赁管理/租赁单列表.html', browser)
    sb = sidebar_eval(page, SB_JS)
    i_lz = next(i for i, x in enumerate(sb) if x['kind'] == 'group' and x['text'] == '租赁管理')
    i_next = next(i for i, x in enumerate(sb) if x['kind'] == 'group' and i > i_lz)
    lz = sb[i_lz:i_next]
    tags = [x['text'] for x in lz if x['kind'] == 'tag']
    grp = {}
    cur = None
    for x in lz:
        if x['kind'] == 'tag':
            cur = x['text']; grp[cur] = []
        elif x['kind'].startswith('item'):
            grp[cur].append(x['text'])
    check('E1 租赁三小标签 租赁/租入/退租', tags == ['租赁', '租入', '退租'], '→'.join(tags))
    check('E2 租赁 4 项=租赁单/租赁出库/在租台账/租出台账', grp.get('租赁') == ['租赁单', '租赁出库', '在租台账', '租出台账'], str(grp))
    check('E3 租入 3 项·退租 1 项', grp.get('租入') == ['租入单', '租入入库', '租入归还'] and grp.get('退租') == ['退租入库'], '')
    ck = next(x for x in lz if x['text'] == '租赁出库')
    check('E4 菜单含「租赁出库」且指向 组合出库列表.html', '租赁管理/组合出库列表.html' in ck['onclick'], ck['onclick'])
    sel = [x['text'] for x in lz if x['kind'] == 'item-selected']
    check('E5 租赁单列表页 selected=租赁单', sel == ['租赁单'], str(sel))
    u = click_menu(page, '租赁出库', '租赁管理/组合出库列表.html')
    check('E6 点击租赁出库落地 组合出库列表.html', u.endswith('租赁管理/组合出库列表.html'), u.split('/')[-1])
    page.wait_for_timeout(300)
    sb2 = sidebar_eval(page, SB_JS)
    sel2 = [x['text'] for x in sb2 if x['kind'] == 'item-selected']
    check('E7 组合出库列表页 selected=租赁出库', sel2 == ['租赁出库'], str(sel2))
    page.close()

    # ── F. 盘点录入页 selected=盘点 + 盘点列表新建盘点入口 ──
    page = open_page('仓储作业/盘点录入.html', browser)
    sb = sidebar_eval(page, SB_JS)
    sel = [x['text'] for x in sb if x['kind'] == 'item-selected']
    check('F1 盘点录入.html 页 selected=盘点（菜单无盘点录入项）', sel == ['盘点'] and all(x['text'] != '盘点录入' for x in sb), str(sel))
    page.close()
    page = open_page('仓储作业/盘点列表.html', browser)
    btn = page.evaluate("""() => {
      const b = [...document.querySelectorAll('button')].find(x => x.textContent.trim() === '新建盘点');
      return b ? b.getAttribute('onclick') : null;
    }""")
    check('F2 盘点列表「新建盘点」按钮跳 盘点录入.html', btn is not None and '仓储作业/盘点录入.html' in btn, str(btn))
    if btn:
        u = click_menu(page, '新建盘点', '仓储作业/盘点录入.html')
        check('F3 点击新建盘点落地 盘点录入.html', u.endswith('仓储作业/盘点录入.html'), u.split('/')[-1])
    page.close()

    # ── G. 角色管理页（selected/菜单可达/九角色/roleModal） ──
    page = open_page('系统管理/用户权限.html', browser)
    u = click_menu(page, '角色管理', '系统管理/角色管理.html')
    check('G1 侧边栏点击角色管理落地 角色管理.html', u.endswith('系统管理/角色管理.html'), u.split('/')[-1])
    sb = sidebar_eval(page, SB_JS)
    sel = [x['text'] for x in sb if x['kind'] == 'item-selected']
    sys_open = any(x['kind'] == 'group' and x['text'] == '系统管理' and x['open'] for x in sb)
    check('G2 角色管理页 selected=角色管理 且系统管理组 open', sel == ['角色管理'] and sys_open, str(sel))
    n_roles = page.evaluate("() => document.querySelectorAll('.content table tbody tr').length")
    check('G3 九角色行数=9', n_roles == 9, str(n_roles))
    has_role = page.evaluate("() => !!document.getElementById('roleModal')")
    check('G4 roleModal 权限配置弹窗存在', has_role, '')
    opened = page.evaluate("""() => {
      const a = [...document.querySelectorAll('.content table tbody a')].find(x => x.textContent.trim() === '权限配置');
      if (a) a.click();
      const m = document.getElementById('roleModal');
      return m ? m.classList.contains('show') : false;
    }""")
    check('G5 点击权限配置打开 roleModal', opened, '')
    mrows = page.evaluate("() => document.querySelectorAll('#roleModal tbody tr').length")
    check('G6 roleModal 内九角色行=9', mrows == 9, str(mrows))
    page.close()

    # ── H. 我的待办一级直达 ──
    page = open_page('首页/项目看板.html', browser)
    sb = sidebar_eval(page, SB_JS)
    first = next(x for x in sb if x['kind'] in ('group', 'single'))
    sel = [x['text'] for x in sb if x['kind'].startswith('item') and x['kind'] == 'item-selected']
    check('H1 项目看板页 selected=项目看板（组内）', sel == ['项目看板'], str(sel))
    check('H2 侧边栏首元素=项目管理组', first['kind'] == 'group' and first['text'] == '项目管理', first['text'])
    u = click_menu(page, '我的待办', '我的待办.html')
    check('H3 点击我的待办一级直达 我的待办.html', u.endswith('/我的待办.html'), u.split('/')[-1])
    page.close()
    browser.close()

print(f'\n==== 菜单重组 v3.1 抽验：{len(results) - len(fails)} 过 / {len(fails)} 败 ====')
if fails:
    print('失败项：', fails)
    sys.exit(1)
