# -*- coding: utf-8 -*-
"""G34 试点验证：新建采购订单表单页 + 列表页入口接线"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')
NEW = ROOT / '采购管理' / '采购订单新建.html'
LIST = ROOT / '采购管理' / '采购订单列表.html'
SHOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g34p_shots')
SHOT.mkdir(parents=True, exist_ok=True)

ok = []; bad = []

def chk(name, cond, extra=''):
    (ok if cond else bad).append(name)
    print(f'  [{"PASS" if cond else "FAIL"}] {name} {extra}')

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))

    # ================= 新页 =================
    print('=== 采购订单新建.html ===')
    pg.goto(NEW.as_uri()); pg.wait_for_timeout(600)
    chk('JS 错误为 0', len(errs) == 0, str(errs[:2]))
    chk('页面标题', '新建采购订单' in pg.title(), pg.title())
    chk('侧边栏选中=采购订单', pg.evaluate("!!document.querySelector('.sm-link.selected') && document.querySelector('.sm-link.selected').textContent.trim()==='采购订单'"))
    chk('页签 active=新建采购订单', pg.evaluate("(document.querySelector('.tab.active')||{}).textContent||''").strip().startswith('新建采购订单'))
    ncard = pg.evaluate("document.querySelectorAll('.content .card').length")
    chk('内容卡片数=3', ncard == 3, f'实际 {ncard}')
    nrow = pg.evaluate("document.querySelectorAll('.edit-tbl tbody tr').length")
    chk('明细行数=2', nrow == 2, f'实际 {nrow}')
    ncol = pg.evaluate("document.querySelectorAll('.edit-tbl tbody tr')[0].querySelectorAll('td').length")
    chk('明细行默认列数=11', ncol == 11, f'列数={ncol}')

    # 税率换算（在带出明细之前测默认行）
    pg.evaluate("""() => { const i=document.querySelector('.edit-tbl tbody input[data-tax="qty"]'); i.value='1000'; i.dispatchEvent(new Event('input')); }""")
    pg.wait_for_timeout(300)
    amt = pg.evaluate("""() => { const el=document.querySelector('.edit-tbl tbody [data-tax="amt"]'); return el ? (el.tagName==="INPUT"? el.value : el.textContent).trim() : ""; }""")
    chk('税率换算自动计算金额', amt not in ('', '0.00'), f'amt={amt}')

    # 添加一行
    pg.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='添加一行'); if(b) b.click(); }""")
    pg.wait_for_timeout(200)
    nrow2 = pg.evaluate("document.querySelectorAll('.edit-tbl tbody tr').length")
    chk('点「添加一行」后=3 行', nrow2 == 3, f'实际 {nrow2}')

    # 类别 → 器具 联动
    pg.evaluate("""() => { const s=[...document.querySelectorAll('.content select')].find(x=>[...x.options].some(o=>o.text==='器具')); if(s){ s.selectedIndex=[...s.options].findIndex(o=>o.text==='器具'); s.dispatchEvent(new Event('change')); } }""")
    pg.wait_for_timeout(200)
    qj = pg.evaluate("getComputedStyle(document.getElementById('poQjRow')).display")
    chk('类别选「器具」→ 物料档案行显示', qj != 'none', f'display={qj}')

    # 关联销售订单搜索 → 带出客户 + 替换明细
    pg.evaluate("""() => { const i=document.getElementById('poSoInput'); i.value='SO-20260903'; i.dispatchEvent(new Event('input')); }""")
    pg.wait_for_timeout(300)
    drop = pg.evaluate("getComputedStyle(document.getElementById('poSoDrop')).display")
    chk('搜索下拉展开', drop == 'block', f'display={drop}')
    pg.evaluate("""() => { if (typeof poSoPick==='function') poSoPick('SO-20260903-0047'); }""")
    pg.wait_for_timeout(300)
    cust = pg.evaluate("(document.getElementById('poSoCust')||{}).value || ''")
    chk('选中后带出客户', '上汽大众' in cust, f'客户={cust}')
    rows_after = pg.evaluate("document.querySelectorAll('.edit-tbl tbody tr').length")
    chk('带出销售明细行', rows_after >= 1, f'行数={rows_after}')
    cols = pg.evaluate("""() => { const tr=document.querySelector('.edit-tbl tbody tr'); return tr? tr.querySelectorAll('td').length : 0; }""")
    chk('带出明细行列数=11（补丁验证）', cols == 11, f'列数={cols}')
    qty_ok = pg.evaluate("""() => !!document.querySelector('.edit-tbl tbody input[data-tax="qty"]')""")
    chk('带出明细行含 data-tax（税率换算可用）', qty_ok)

    # 项目→供应商联动
    sup_first = pg.evaluate("""() => { const p=document.getElementById('cmProject'); p.selectedIndex=2; p.dispatchEvent(new Event('change')); return document.getElementById('cmSupplier').options[0].text; }""")
    chk('项目切换→供应商联动（PRJ-2603=路凯）', '路凯' in sup_first, f'首个={sup_first}')

    # 提交条
    chk('提交条三按钮', pg.evaluate("""() => { const b=[...document.querySelectorAll('.submit-bar button')].map(x=>x.textContent.trim()); return b.length===3; }"""))
    pg.screenshot(path=str(SHOT / '01_new_page.png'), full_page=True)

    # 取消 → 回列表
    pg.evaluate("""() => { window.__navs=[]; window.go=function(u){ window.__navs.push(String(u)); }; const b=[...document.querySelectorAll('.submit-bar button')].find(x=>x.textContent.includes('取')); b.click(); }""")
    navs = pg.evaluate("window.__navs")
    chk('「取消」跳采购订单列表', any('采购订单列表' in str(n) for n in navs), str(navs))

    # ================= 列表页 =================
    print('=== 采购订单列表.html ===')
    errs.clear()
    pg.goto(LIST.as_uri()); pg.wait_for_timeout(600)
    chk('JS 错误为 0', len(errs) == 0, str(errs[:2]))
    chk('createModal 已移除', pg.evaluate("document.querySelectorAll('#createModal').length") == 0)
    chk('无 poSoDrop 残留节点', pg.evaluate("document.querySelectorAll('#poSoDrop').length") == 0)
    chk('列表数据仍渲染', pg.evaluate("document.querySelectorAll('tbody tr').length") > 0)

    pg.evaluate("""() => { window.__navs=[]; window.go=function(u){ window.__navs.push(String(u)); };
      const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='新建采购订单'); if(b) b.click(); }""")
    navs = pg.evaluate("window.__navs")
    chk('「新建采购订单」→ go 到新页', any('采购订单新建.html' in str(n) for n in navs), str(navs))

    pg.evaluate("""() => { window.__navs=[]; const a=[...document.querySelectorAll('a')].find(x=>x.textContent.trim()==='编辑'); if(a) a.click(); }""")
    navs2 = pg.evaluate("window.__navs")
    chk('「编辑」→ go 带 ?mode=edit', any('mode=edit' in str(n) for n in navs2), str(navs2))
    pg.screenshot(path=str(SHOT / '02_list_page.png'), full_page=True)

    b.close()

print()
print(f'结果：PASS {len(ok)} / FAIL {len(bad)}')
if bad:
    print('失败项:', bad)
print('截图:', SHOT)
