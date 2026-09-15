# -*- coding: utf-8 -*-
"""G34 试点验证 v2：新建采购订单表单页（含道远 09-15 四条意见）"""
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

    print('=== 采购订单新建.html ===')
    pg.goto(NEW.as_uri()); pg.wait_for_timeout(900)
    chk('JS 错误为 0', len(errs) == 0, str(errs[:2]))
    chk('两卡结构（订单信息/采购明细）', pg.evaluate("document.querySelectorAll('.content .card').length") == 2)
    _ta = pg.evaluate("""() => { const ta=document.querySelector('textarea'); if(!ta) return null;
      const card=ta.closest('.card'); const rows=[...card.querySelectorAll('.form-row')];
      return {h:Math.round(ta.getBoundingClientRect().height), card:card.querySelector('.card-title').textContent.trim(),
              isLast: rows[rows.length-1]===ta.closest('.form-row')}; }""")
    chk('备注=文本域·高72px·在表单卡末尾', bool(_ta) and _ta['h'] >= 60 and _ta['card'] == '订单信息' and _ta['isLast'], str(_ta))
    chk('「随附信息」独立卡已删', pg.evaluate("""() => !document.body.innerHTML.includes('随附信息')"""))
    chk('明细行=2', pg.evaluate("document.querySelectorAll('.edit-tbl tbody tr').length") == 2)
    chk('明细列=11', pg.evaluate("document.querySelectorAll('.edit-tbl tbody tr')[0].querySelectorAll('td').length") == 11)

    # ---- 意见 1：返回列表按钮已删 ----
    chk('①「返回列表」按钮已删', pg.evaluate("""() => ![...document.querySelectorAll('button')].some(b=>b.textContent.includes('返回列表'))"""))
    chk('① 提交条三按钮仍在', pg.evaluate("""() => [...document.querySelectorAll('.submit-bar button')].length === 3"""))

    # ---- 意见 2：物料类型（字典驱动 + 改名 + 物料档案行删除） ----
    chk('②「类别」已改名「物料类型」', pg.evaluate("""() => [...document.querySelectorAll('.form-label')].some(l=>l.textContent.includes('物料类型'))"""))
    mt = pg.evaluate("""() => { const s=document.getElementById('cmMtype'); return s? [...s.options].map(o=>o.text) : []; }""")
    chk('② 物料类型=字典物料类型组 6 值', mt == ['围板箱','塑料托盘','木托盘','料箱','料架','组件'], str(mt))
    chk('②「物料档案」行已删', pg.evaluate("() => !document.getElementById('poQjRow')"))

    # ---- 意见 3：单位 / 税率 字典下拉 ----
    us = pg.evaluate("""() => { const s=document.querySelector('.edit-tbl tbody select[data-unit]'); return s? [...s.options].map(o=>o.text) : []; }""")
    chk('③ 单位=字典计量单位组 7 值', us == ['个','套','只','张','件','台','托'], str(us))
    rs = pg.evaluate("""() => { const s=document.querySelector('.edit-tbl tbody select[data-tax="rate"]'); return s? [...s.options].map(o=>o.text) : []; }""")
    chk('③ 税率=字典供应商税率组 6 值', rs == ['0%','1%','3%','6%','9%','13%'], str(rs))
    chk('③ 单位/税率均为下拉', pg.evaluate("""() => !!document.querySelector('.edit-tbl tbody select[data-unit]') && !!document.querySelector('.edit-tbl tbody select[data-tax="rate"]')"""))

    # ---- 意见 4：物料编码 ↔ 物料名称 双向联动 ----
    r1 = pg.evaluate("""() => { const tr=document.querySelector('.edit-tbl tbody tr');
      const sk=tr.querySelector('select[data-prod-key]'), sn=tr.querySelector('select[data-prod-name]');
      sk.value='BTC-6040'; sk.dispatchEvent(new Event('change', {bubbles: true}));
      return {k: sk.value, n: sn.value, sp: (tr.querySelector('input[data-spec]')||{}).value}; }""")
    chk('④ 改「物料编码」→「物料名称」自动变更', r1['n'] == 'BTC-6040', str(r1))
    chk('④ 顺带带出规格', bool(r1.get('sp')), f"spec={r1.get('sp')}")
    r2 = pg.evaluate("""() => { const tr=document.querySelector('.edit-tbl tbody tr');
      const sn=tr.querySelector('select[data-prod-name]'); sn.value='WBX-1210L'; sn.dispatchEvent(new Event('change', {bubbles: true}));
      return {k: tr.querySelector('select[data-prod-key]').value}; }""")
    chk('④ 改「物料名称」→「物料编码」自动变更', r2['k'] == 'WBX-1210L', str(r2))
    chk('④ 两列选项取自物料档案', pg.evaluate("""() => { const s=document.querySelector('.edit-tbl tbody select[data-prod-key]');
      return s.options.length >= 10 && [...s.options].some(o=>o.text==='WBX-1210L'); }"""))

    # ---- 税率换算（下拉 change 触发） ----
    rg = pg.evaluate("""() => { const tr=document.querySelector('.edit-tbl tbody tr');
      const rd = a => a ? (a.tagName==='INPUT'? a.value : a.textContent).trim() : '';
      const before = rd(tr.querySelector('[data-tax="amt"]'));
      const q=tr.querySelector('input[data-tax="qty"]'); q.value='1000'; q.dispatchEvent(new Event('input', {bubbles: true}));
      const after = rd(tr.querySelector('[data-tax="amt"]'));
      const r=tr.querySelector('select[data-tax="rate"]'); r.value='13%'; r.dispatchEvent(new Event('change', {bubbles: true}));
      return {before, after, afterRate: rd(tr.querySelector('[data-tax="amt"]'))}; }""")
    chk('税率换算：改数量→金额重算（真值变化）', rg['after'] != rg['before'] and rg['after'] not in ('', '0.00'), str(rg))

    # ---- 添加一行 ----
    pg.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='添加一行'); if(b) b.click(); }""")
    pg.wait_for_timeout(300)
    chk('「添加一行」后=3 行且新行下拉已渲染', pg.evaluate("""() => { const trs=document.querySelectorAll('.edit-tbl tbody tr');
      return trs.length===3 && trs[2].querySelectorAll('select').length === 4; }"""))

    # ---- 关联销售订单搜索 ----
    pg.evaluate("""() => { const i=document.getElementById('poSoInput'); i.value='SO-20260903'; i.dispatchEvent(new Event('input', {bubbles: true})); }""")
    pg.wait_for_timeout(300)
    chk('搜索下拉展开', pg.evaluate("getComputedStyle(document.getElementById('poSoDrop')).display") == 'block')
    pg.evaluate("""() => { if (typeof poSoPick==='function') poSoPick('SO-20260903-0047'); }""")
    pg.wait_for_timeout(400)
    chk('选中后带出客户', '上汽大众' in pg.evaluate("(document.getElementById('poSoCust')||{}).value || ''"))
    chk('带出行=11 列且下拉已渲染', pg.evaluate("""() => { const tr=document.querySelector('.edit-tbl tbody tr');
      return tr.querySelectorAll('td').length===11 && tr.querySelectorAll('select').length===4; }"""))

    # ---- 提交条避让 ----
    gap = pg.evaluate("""() => { const f=document.querySelector('.fab-row').getBoundingClientRect();
      const btn=[...document.querySelectorAll('.submit-bar button')].pop().getBoundingClientRect();
      return Math.round(f.left - btn.right); }""")
    chk('提交条与右下 fab 不重叠', gap > 0, f'间隙={gap}px')

    pg.screenshot(path=str(SHOT / '01_new_page.png'), full_page=True)

    # ---- 列表页入口回归 ----
    print('=== 采购订单列表.html ===')
    errs.clear()
    pg.goto(LIST.as_uri()); pg.wait_for_timeout(700)
    chk('列表页 JS 错误为 0', len(errs) == 0, str(errs[:2]))
    chk('列表页 createModal 已移除', pg.evaluate("document.querySelectorAll('#createModal').length") == 0)
    pg.evaluate("""() => { window.__navs=[]; window.go=function(u){ window.__navs.push(String(u)); };
      const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='新建采购订单'); if(b) b.click(); }""")
    chk('新建入口 → go 新页', any('采购订单新建.html' in str(n) for n in pg.evaluate("window.__navs")))
    pg.evaluate("""() => { window.__navs=[]; const a=[...document.querySelectorAll('a')].find(x=>x.textContent.trim()==='编辑'); if(a) a.click(); }""")
    chk('编辑入口 → go 带 ?mode=edit', any('mode=edit' in str(n) for n in pg.evaluate("window.__navs")))
    pg.screenshot(path=str(SHOT / '02_list_page.png'), full_page=True)

    b.close()

print()
print(f'结果：PASS {len(ok)} / FAIL {len(bad)}')
if bad: print('失败项:', bad)
