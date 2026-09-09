# -*- coding: utf-8 -*-
"""菜单重组 v3.2 · G03 复验收抽验（v31_spotcheck.py 全量继承 + v3.2 口径更新 + 角色页数据驱动实测）
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

def click_menu(page, label, suffix):
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

    # ── A. 组序列与残留（样本=数据字典页） ──
    page = open_page('系统管理/数据字典.html', browser)
    sb = page.evaluate(SB_JS)
    groups = [x['text'] for x in sb if x['kind'] == 'group']
    singles = [x['text'] for x in sb if x['kind'] in ('single', 'single-selected')]
    check('A1 组序=v3.2 八组', groups == ['项目管理', '基础资料', '采购管理', '销售管理', '租赁管理', '仓储管理', '财务管理', '系统管理'], '→'.join(groups))
    check('A2 一级仅 我的待办', singles == ['我的待办'], '→'.join(singles))
    all_txt = page.evaluate("() => document.querySelector('aside.sidebar').textContent")
    check('A3 侧边栏无旧组名 财务协同/仓储作业', ('财务协同' not in all_txt) and ('仓储作业' not in all_txt), '')
    i_pm = next(i for i, x in enumerate(sb) if x['kind'] == 'group' and x['text'] == '项目管理')
    i_pm_next = next((i for i, x in enumerate(sb) if x['kind'] == 'group' and i > i_pm), len(sb))
    pm_items = [x['text'] for x in sb[i_pm:i_pm_next] if x['kind'].startswith('item')]
    check('A4 项目管理组居首且 2 项=项目看板/项目列表（损益已移出）', groups[0] == '项目管理' and pm_items == ['项目看板', '项目列表'], str(pm_items))
    ck = next((x for x in sb if x['text'] == '项目列表'), None)
    check('A5 项目列表→项目管理/项目档案.html', ck is not None and '项目管理/项目档案.html' in ck['onclick'], ck['onclick'] if ck else 'NONE')
    u = click_menu(page, '项目列表', '项目管理/项目档案.html')
    check('A6 点击项目列表落地 项目档案.html', u.endswith('项目管理/项目档案.html'), u.split('/')[-1])
    page.close()

    # ── B. 财务管理组（样本=应收账单页）＋项目损益组尾 ──
    page = open_page('财务协同/应收账单.html', browser)
    sb = page.evaluate(SB_JS)
    i_fin = next(i for i, x in enumerate(sb) if x['kind'] == 'group' and x['text'] == '财务管理')
    i_next = next(i for i, x in enumerate(sb) if x['kind'] == 'group' and i > i_fin)
    fin = sb[i_fin:i_next]
    tags = [x['text'] for x in fin if x['kind'] == 'tag']
    grp = {}
    cur = None
    for x in fin:
        if x['kind'] == 'tag':
            cur = x['text']; grp[cur] = []
        elif x['kind'].startswith('item'):
            grp.setdefault(cur, []).append(x)
    check('B1 财务管理组小标签=应收/应付', tags == ['应收', '应付'], '→'.join(tags))
    check('B2 应收 4 项=应收账单/开票登记/收款登记/收款核销',
          [x['text'] for x in grp.get('应收', [])] == ['应收账单', '开票登记', '收款登记', '收款核销'], str([x['text'] for x in grp.get('应收', [])]))
    check('B3 应付 2 项=应付账单/付款登记（项目损益为组尾普通项不计入小标签）',
          [x['text'] for x in grp.get('应付', []) if x['text'] != '项目损益'] == ['应付账单', '付款登记'],
          str([x['text'] for x in grp.get('应付', [])]))
    tail = grp.get(None, []) or grp.get('应付', []) + []
    sun_items = [x for x in fin if x['kind'].startswith('item')]
    last = sun_items[-1] if sun_items else None
    check('B4 项目损益=财务管理组尾普通项（非小标签）→财务协同/盈亏报表.html',
          last is not None and last['text'] == '项目损益' and '财务协同/盈亏报表.html' in last['onclick'],
          str((last['text'], last['onclick']) if last else 'NONE'))
    sel = [x['text'] for x in fin if x['kind'] == 'item-selected']
    check('B5 应收账单页 selected=应收账单 且财务管理组 open', sel == ['应收账单'] and sb[i_fin]['open'], str(sel))
    u = click_menu(page, '项目损益', '财务协同/盈亏报表.html')
    check('B6 点击项目损益落地 盈亏报表.html', u.endswith('财务协同/盈亏报表.html'), u.split('/')[-1])
    page.wait_for_timeout(300)
    sb2 = page.evaluate(SB_JS)
    sel2 = [x['text'] for x in sb2 if x['kind'] == 'item-selected']
    fin_open = any(x['kind'] == 'group' and x['text'] == '财务管理' and x['open'] for x in sb2)
    check('B7 盈亏报表页 selected=项目损益 且 open=财务管理', sel2 == ['项目损益'] and fin_open, str(sel2))
    page.close()

    # ── C. 仓储管理组（样本=库存查询页）＋盘点录入退出菜单 ──
    page = open_page('仓储作业/库存查询.html', browser)
    sb = page.evaluate(SB_JS)
    i_wh = next(i for i, x in enumerate(sb) if x['kind'] == 'group' and x['text'] == '仓储管理')
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
    check('C1 仓储管理组三小标签=库存管理/入库类/出库类', tags == ['库存管理', '入库类', '出库类'], '→'.join(tags))
    check('C2 库存管理 3 项=库存查询/盘点/库存调拨', grp.get('库存管理') == ['库存查询', '盘点', '库存调拨'], str(grp))
    check('C3 入库类=其他入库·出库类=其他出库', grp.get('入库类') == ['其他入库'] and grp.get('出库类') == ['其他出库'], '')
    check('C4 仓储菜单无盘点录入项', '盘点录入' not in [t for v in grp.values() for t in v], '')
    sel = [x['text'] for x in wh if x['kind'] == 'item-selected']
    check('C5 库存查询页 selected=库存查询 且仓储管理组 open', sel == ['库存查询'] and sb[i_wh]['open'], str(sel))
    page.close()

    # ── D. 租赁管理组（v3.1 复验收：三小标签归属+租赁出库跳转） ──
    page = open_page('租赁管理/租赁单列表.html', browser)
    sb = page.evaluate(SB_JS)
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
            grp[cur].append(x)
    check('D1 租赁三小标签=租赁/租入/退租', tags == ['租赁', '租入', '退租'], '→'.join(tags))
    check('D2 租赁 4 项=租赁单/租赁出库/在租台账/租出台账',
          [x['text'] for x in grp.get('租赁', [])] == ['租赁单', '租赁出库', '在租台账', '租出台账'], str([x['text'] for x in grp.get('租赁', [])]))
    check('D3 租入 3 项·退租 1 项',
          [x['text'] for x in grp.get('租入', [])] == ['租入单', '租入入库', '租入归还'] and [x['text'] for x in grp.get('退租', [])] == ['退租入库'], '')
    ck = next(x for x in lz if x['text'] == '租赁出库')
    check('D4 菜单含「租赁出库」且指向 组合出库列表.html', '租赁管理/组合出库列表.html' in ck['onclick'], ck['onclick'])
    sel = [x['text'] for x in lz if x['kind'] == 'item-selected']
    check('D5 租赁单列表页 selected=租赁单', sel == ['租赁单'], str(sel))
    u = click_menu(page, '租赁出库', '租赁管理/组合出库列表.html')
    check('D6 点击租赁出库落地 组合出库列表.html', u.endswith('租赁管理/组合出库列表.html'), u.split('/')[-1])
    page.wait_for_timeout(300)
    sb2 = page.evaluate(SB_JS)
    sel2 = [x['text'] for x in sb2 if x['kind'] == 'item-selected']
    check('D7 组合出库列表页 selected=租赁出库', sel2 == ['租赁出库'], str(sel2))
    page.close()

    # ── E. 盘点录入页（v3.1 复验收：selected=盘点·菜单无该项） ──
    page = open_page('仓储作业/盘点录入.html', browser)
    sb = page.evaluate(SB_JS)
    sel = [x['text'] for x in sb if x['kind'] == 'item-selected']
    check('E1 盘点录入.html 页 selected=盘点（菜单无盘点录入项）', sel == ['盘点'] and all(x['text'] != '盘点录入' for x in sb), str(sel))
    page.close()

    # ── F. 角色管理页数据驱动实测 ──
    page = open_page('系统管理/用户权限.html', browser)
    u = click_menu(page, '角色管理', '系统管理/角色管理.html')
    check('F1 侧边栏点击角色管理落地 角色管理.html', u.endswith('系统管理/角色管理.html'), u.split('/')[-1])
    sb = page.evaluate(SB_JS)
    sel = [x['text'] for x in sb if x['kind'] == 'item-selected']
    sys_open = any(x['kind'] == 'group' and x['text'] == '系统管理' and x['open'] for x in sb)
    check('F2 角色管理页 selected=角色管理 且系统管理组 open', sel == ['角色管理'] and sys_open, str(sel))
    page.wait_for_selector('.content table tbody tr', timeout=8000)
    page.wait_for_timeout(300)
    n_roles = page.evaluate("() => document.querySelectorAll('.content table tbody tr').length")
    check('F3 renderListPage 渲染行数=9（demo-data roles 数据驱动）', n_roles == 9, str(n_roles))
    opened = page.evaluate("""() => {
      const a = [...document.querySelectorAll('.content table tbody a')].find(x => x.textContent.trim() === '权限配置');
      if (a) a.click();
      const m = document.getElementById('roleModal');
      return m ? m.classList.contains('show') : false;
    }""")
    check('F4 点击权限配置打开 roleModal（openRolePerm）', opened, '')
    title = page.evaluate("() => document.getElementById('rolePermTitle').textContent")
    check('F5 roleModal 标题=「权限配置 · 系统管理员」', title == '权限配置 · 系统管理员', title)
    matrix = page.evaluate("""() => {
      const cbs = [...document.querySelectorAll('#roleModal .checkbox')];
      return { total: cbs.length, checked: cbs.filter(c => c.classList.contains('checked')).length };
    }""")
    check('F6 勾选矩阵抽查：系统管理员 9 项权限全勾选', matrix['total'] == 9 and matrix['checked'] == 9, str(matrix))
    scope = page.evaluate("""() => {
      const r = [...document.querySelectorAll('#roleModal .radio')].find(x => x.classList.contains('checked'));
      return r ? r.getAttribute('data-scope') : null;
    }""")
    check('F7 roleModal 数据权限单选=全部项目', scope == '全部项目', str(scope))
    page.evaluate("() => closeModal('roleModal')")
    opened2 = page.evaluate("""() => {
      const b = [...document.querySelectorAll('button, a')].find(x => x.textContent.trim() === '新增角色');
      if (b) b.click();
      const m = document.getElementById('createModal');
      return m ? m.classList.contains('show') : false;
    }""")
    check('F8 点击新增角色打开 createModal', opened2, '')
    fields = page.evaluate("""() => [...document.querySelectorAll('#createModal .form-label')].map(x => x.textContent.trim())""")
    need = ['角色名称', '说明', '数据权限范围']
    got = [f.replace('*', '').strip() for f in fields]
    check('F9 createModal 三字段=角色名称/说明/数据权限范围', all(any(n in g for g in got) for n in need), str(got))
    page.close()

    # ── G. 我的待办一级直达 ──
    page = open_page('首页/项目看板.html', browser)
    sb = page.evaluate(SB_JS)
    first = next(x for x in sb if x['kind'] in ('group', 'single'))
    sel = [x['text'] for x in sb if x['kind'] == 'item-selected']
    check('G1 项目看板页 selected=项目看板（组内）', sel == ['项目看板'], str(sel))
    check('G2 侧边栏首元素=项目管理组', first['kind'] == 'group' and first['text'] == '项目管理', first['text'])
    u = click_menu(page, '我的待办', '我的待办.html')
    check('G3 点击我的待办一级直达 我的待办.html', u.endswith('/我的待办.html'), u.split('/')[-1])
    page.close()
    browser.close()

print(f'\n==== 菜单重组 v3.2 抽验：{len(results) - len(fails)} 过 / {len(fails)} 败 ====')
if fails:
    print('失败项：', fails)
    sys.exit(1)
