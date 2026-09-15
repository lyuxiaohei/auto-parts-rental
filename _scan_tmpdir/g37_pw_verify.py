# -*- coding: utf-8 -*-
"""G37 PW 抽验：结算方式/财务口径/转租退场/状态联动/演示数据/D2 角色/F1 用词/菜单跳转带参
纪律：编程点击（evaluate）+textContent+unquote。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent / 'P3-R01-包装租赁管理后台原型'
results = []
js_errors = []

def check(no, name, ok, note=''):
    results.append((no, name, bool(ok), note))

with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page()
    pg.on('pageerror', lambda e: js_errors.append(str(e)))

    # ===== 1. 新建页：结算方式两值＋项目带出＋可覆盖 =====
    pg.goto((ROOT / '租赁管理/转移出库新建.html').as_uri())
    pg.wait_for_load_state('load')
    r1 = pg.evaluate("""() => {
      const L = document.getElementById('zySettleL'), T = document.getElementById('zySettleT');
      const hint = document.getElementById('zySettleHint');
      return {
        two: !!(L && T),
        lChecked: L.classList.contains('checked'),
        tChecked: T.classList.contains('checked'),
        hint: hint ? hint.textContent : '',
        radioCnt: document.querySelectorAll('.radio').length
      };
    }""")
    check('1a', '新建页结算方式两 radio 在位·默认按租出选中', r1['two'] and r1['lChecked'] and not r1['tChecked'], str(r1))
    # 项目切换带出（PRJ-2603→按终端）
    r2 = pg.evaluate("""() => {
      const sel = document.getElementById('zyProj');
      sel.value = sel.options[1].value; // PRJ-2603
      zyProjChange();
      const L = document.getElementById('zySettleL'), T = document.getElementById('zySettleT');
      const hint = document.getElementById('zySettleHint');
      const from = document.getElementById('zyFrom');
      return { tChecked: T.classList.contains('checked'), lChecked: L.classList.contains('checked'),
               hint: hint.textContent.slice(0, 60), from: from.value };
    }""")
    check('1b', '切 PRJ-2603 → 按终端结算带出+客户带出长丰锂电科技', r2['tChecked'] and not r2['lChecked'] and r2['from'] == '长丰锂电科技' and '按终端结算' in r2['hint'], str(r2))
    # 可覆盖（点按租出）
    r3 = pg.evaluate("""() => { zySettle('L'); return document.getElementById('zySettleL').classList.contains('checked'); }""")
    check('1c', '单据级覆盖：点按租出结算 → checked 切换', r3)
    # 物料下拉动态取 products（≥8 项）
    r4 = pg.evaluate("""() => document.getElementById('zyMat').options.length""")
    check('1d', '物料下拉动态取产品档案（≥8 项）', r4 >= 8, f'实测 {r4}')

    # ===== 2. 详情页财务口径（?id= 驱动） =====
    pg.goto((ROOT / '租赁管理/转移出库单详情.html').as_uri() + '?id=ZY-20260914-001')
    pg.wait_for_load_state('load')
    t1 = pg.evaluate("""() => document.getElementById('detailBody').textContent""")
    check('2a', '按租出结算单（ZY-001）详情含「不生成应收账单」', '不生成应收账单' in t1)
    pg.goto((ROOT / '租赁管理/转移出库单详情.html').as_uri() + '?id=ZY-20260914-002')
    pg.wait_for_load_state('load')
    t2 = pg.evaluate("""() => document.getElementById('detailBody').textContent""")
    check('2b', '按终端结算单（ZY-002）详情含「后续应收账单主体切换为终端客户」＋「历史账单不回改」', '后续应收账单主体切换为终端客户' in t2 and '历史账单不回改' in t2)

    # ===== 3. 库存查询：zz 退场＋行内转移出库带参跳转 =====
    pg.goto((ROOT / '仓储作业/库存查询.html').as_uri())
    pg.wait_for_load_state('load')
    r5 = pg.evaluate("""() => ({
      zzReg: !!document.getElementById('zzRegModal'), zzBack: !!document.getElementById('zzBackModal'),
      th: [...document.querySelectorAll('thead th')].map(t => t.textContent.trim()),
      ops: [...document.querySelectorAll('tbody .ops a')].map(a => a.textContent.trim()).filter(t => t === '转移出库' || t === '终止转移')
    })""")
    check('3a', 'zzRegModal/zzBackModal 已删（null×2）', not r5['zzReg'] and not r5['zzBack'])
    check('3b', 'F1 列头：物料名称/库房 在位·旧词不在', '物料名称' in r5['th'] and '库房' in r5['th'] and '名称' not in r5['th'] and '仓库' not in r5['th'], str([x for x in r5['th'] if x in ('物料名称','库房')]))
    check('3c', '行内有「转移出库」跳转入口（renderListPage 数据驱动渲染）', '转移出库' in r5['ops'], str(r5['ops'][:6]))
    # 带参跳转（点击第一处 转移出库 op → 新建页带 mat/cust）
    with pg.expect_navigation():
        pg.evaluate("""() => { const a = [...document.querySelectorAll('tbody .ops a')].find(x => x.textContent.trim() === '转移出库'); a.click(); }""")
    pg.wait_for_load_state('load')
    u1 = unquote(pg.url)
    ok1 = '转移出库新建.html' in u1 and 'mat=' in u1 and 'cust=' in u1
    pre1 = pg.evaluate("""() => ({ mat: (document.getElementById('zyMat')||{}).value, from: (document.getElementById('zyFrom')||{}).value })""") if ok1 else {}
    check('3d', '行内「转移出库」跳新建页带参（mat+cust）且预填生效', ok1 and pre1.get('from'), f'{u1[-80:]} pre={pre1}')

    # ===== 4. 状态联动（列表行内动作·DOM 副作用） =====
    pg.goto((ROOT / '租赁管理/转移出库列表.html').as_uri())
    pg.wait_for_load_state('load')
    r6 = pg.evaluate("""() => {
      const row = [...document.querySelectorAll('tbody tr')].find(tr => tr.textContent.indexOf('ZY-20260915-005') > -1);
      const a = [...row.querySelectorAll('.ops a')].find(x => x.textContent.trim() === '确认转移');
      a.click();
      return { st: row.querySelector('.tag').textContent.trim(), ops: [...row.querySelectorAll('.ops a')].map(x => x.textContent.trim()) };
    }""")
    check('4a', '确认转移：待转移→已转移（库存状态联动「客户转租出」口径见 4c）', r6['st'] == '已转移' and '终止转移' in r6['ops'], str(r6))
    r7 = pg.evaluate("""() => {
      const row = [...document.querySelectorAll('tbody tr')].find(tr => tr.textContent.indexOf('ZY-20260914-003') > -1);
      const a = [...row.querySelectorAll('.ops a')].find(x => x.textContent.trim() === '终止转移');
      a.click();
      return { st: row.querySelector('.tag').textContent.trim() };
    }""")
    check('4b', '终止转移：已转移→已终止（状态回「在客户（租出）」口径见演示数据）', r7['st'] == '已终止', str(r7))

    # ===== 5. 演示数据：两项目各一结算方式＋库存联动 =====
    r8 = pg.evaluate("""() => {
      const T = (window.DEMO_DATA || {}).transferOutbounds || {};
      const rows = Object.keys(T).map(k => ({ k: k, settle: (T[k].row || {}).fields ? T[k].row.fields.settle : '', proj: T[k].row.fields.project, qty: T[k].row.fields.qty }));
      const SF = (window.DEMO_DATA || {}).stockFlows || {};
      const zz = Object.keys(SF).filter(k => (SF[k].row || {}).fields && SF[k].row.fields.status === '客户转租出');
      const plt = SF['XNC-ZZ-PLT'] ? SF['XNC-ZZ-PLT'].row.fields.status : '?';
      return { rows, zzKeys: zz, pltStatus: plt };
    }""")
    settles = {(x['proj'], x['settle']) for x in r8['rows']}
    check('5a', 'transferOutbounds ≥3 行·ZY- 前缀', len(r8['rows']) >= 3 and all(x['k'].startswith('ZY-') for x in r8['rows']), str(r8['rows']))
    check('5b', '两项目各一结算方式（PRJ-2605 按租出＋PRJ-2603 按终端）', ('PRJ-2605', '按租出结算') in settles and ('PRJ-2603', '按终端结算') in settles, str(settles))
    check('5c', '库存联动：客户转租出 3 行（WBX/BTC/PLT2）·PLT 已终止单回租出态', len(r8['zzKeys']) == 3 and r8['pltStatus'] == '客户端(租出)', str(r8['zzKeys']) + ' PLT=' + str(r8['pltStatus']))

    # ===== 6. D2 角色 6 个 =====
    r9 = pg.evaluate("""() => {
      const R = (window.DEMO_DATA || {}).roles || {};
      const names = Object.keys(R).map(k => (R[k].row || {}).fields ? R[k].row.fields.name : '?');
      const U = (window.DEMO_DATA || {}).users || {};
      const roles = Object.keys(U).map(k => (U[k].row || {}).fields ? U[k].row.fields.role : '?');
      return { names, roles };
    }""")
    check('6a', 'roles 恰 6 个=系统管理员/财务/商务/物流/采购/项目经理', sorted(r9['names']) == sorted(['系统管理员', '财务', '商务', '物流', '采购', '项目经理']), str(r9['names']))
    check('6b', 'users role 全在 6 角色域内（含采购/项目经理）', set(r9['roles']) <= set(r9['names']) and '采购' in r9['roles'] and '项目经理' in r9['roles'], str(r9['roles']))
    pg.goto((ROOT / '系统管理/角色管理.html').as_uri())
    pg.wait_for_load_state('load')
    r10 = pg.evaluate("""() => [...document.querySelectorAll('tbody tr td:first-child b')].map(x => x.textContent.trim())""")
    check('6c', '角色管理页 6 行与 demo-data 一致', sorted(r10) == sorted(r9['names']), str(r10))
    pg.goto((ROOT / '系统管理/用户权限.html').as_uri())
    pg.wait_for_load_state('load')
    r11 = pg.evaluate("""() => {
      const sel = [...document.querySelectorAll('.ff select')].find(s => [...s.options].some(o => o.text === '财务'));
      const tags = [...document.querySelectorAll('tbody .tag')].map(x => x.textContent.trim());
      return { opts: sel ? [...sel.options].map(o => o.text) : [], tags: [...new Set(tags)] };
    }""")
    check('6d', '用户权限筛选 select=6 角色·渲染 tag 无主管', '采购' in r11['opts'] and '项目经理' in r11['opts'] and not any('主管' in x for x in r11['tags'] + r11['opts']), str(r11['opts']))

    # ===== 7. 项目档案：转租结算方式列 =====
    pg.goto((ROOT / '项目管理/项目档案.html').as_uri())
    pg.wait_for_load_state('load')
    r12 = pg.evaluate("""() => {
      const th = [...document.querySelectorAll('thead th')].map(x => x.textContent.trim());
      const row2603 = [...document.querySelectorAll('tbody tr')].find(tr => tr.textContent.indexOf('PRJ-2603') > -1);
      return { th, row2603: row2603 ? row2603.textContent : '' };
    }""")
    check('7a', '项目档案列头含「转租结算方式」', '转租结算方式' in r12['th'], str([x for x in r12['th']]))
    check('7b', 'PRJ-2603 行带「按终端结算」', '按终端结算' in r12['row2603'])

    # ===== 8. 全程 0 JS 错误 =====
    check('8', '全程 0 JS 错误（新建/详情×2/库存查询/列表/角色/用户权限/项目档案）', len(js_errors) == 0, '; '.join(js_errors[:3]))
    br.close()

fails = [r for r in results if not r[2]]
for no, name, ok, note in results:
    print(f"{'PASS' if ok else 'FAIL'} {no} {name}" + (f"  ｜{note}" if (not ok or no in ('1b','3d','5c','6b')) else ''))
print(f"==== G37 PW 抽验：{len(results)} 项断言，失败 {len(fails)} 项 ====")
sys.exit(1 if fails else 0)
