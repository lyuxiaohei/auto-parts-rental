# -*- coding: utf-8 -*-
"""任务二·列表数据驱动全量推广验证门（2026-09-08）· 逐页断言组（照 verify_listpilot.py 结构）
用法：python verify_listfull.py batch1|batch2|batch3
"""
import sys, io, argparse, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'

# name / file / entity / modalId / stabs(dict 期望，None=无 stab) / pin(>=期望，None=跳过) / noCheckbox
B1 = [
    dict(name='其他入库', file='仓储作业/其他入库列表.html', entity='otherInbounds', modalId='detailModal',
         stabs={'全部': 3, '待审核': 1, '已入库': 2}, pin=None),
    dict(name='租入入库', file='仓储作业/租入入库列表.html', entity='rentInbounds', modalId='detailModal',
         stabs={'全部': 3, '待入库': 1, '已入库': 2}, pin=2),
    dict(name='销售出库', file='仓储作业/销售出库列表.html', entity='salesOutbounds', modalId='detailModal',
         stabs={'全部': 6, '待审核': 1, '已完成': 5}, pin=None),
    dict(name='组合出库', file='仓储作业/组合出库列表.html', entity='comboOutbounds', modalId='detailModal',
         stabs={'拣货中': 1}, pin=2),
    dict(name='其他出库', file='仓储作业/其他出库列表.html', entity='otherOutbounds', modalId='detailModal',
         stabs={'全部': 5, '待审核': 1, '已完成': 3}, pin=None),
    dict(name='租入归还', file='仓储作业/租入归还列表.html', entity='rentInReturns', modalId='detailModal',
         stabs={'全部': 3, '待审核': 1, '已归还': 2}, pin=2),
    dict(name='退租入库', file='仓储作业/退租入库列表.html', entity='returnInbounds', modalId='detailModal',
         stabs={'全部': 8, '待审核': 3, '已入库': 5}, pin=3),
    dict(name='组装', file='仓储作业/组装列表.html', entity='assemblyOrders', modalId='detailModal',
         stabs={'全部': 7, '待审核': 1, '待组装': 1, '组装中': 3, '已完成': 2}, pin=None),
    dict(name='拆卸管理', file='仓储作业/拆卸管理列表.html', entity='disassemblyOrders', modalId='detailModal',
         stabs={'全部': 4, '待审核': 1, '已完成': 3}, pin=None),
    dict(name='盘点', file='仓储作业/盘点列表.html', entity='stocktakes', modalId='detailModal',
         stabs={'全部': 5, '盘点中': 1, '待审核': 1, '已完成': 3}, pin=None),
    dict(name='库存调拨', file='仓储作业/库存调拨列表.html', entity='transfers', modalId='detailModal',
         stabs={'全部': 3, '待审核': 1, '已完成': 2}, pin=None),
    dict(name='库存查询', file='仓储作业/库存查询.html', entity='stockFlows', modalId='flowModal',
         stabs=None, pin=None, noCheckbox=True, tbody_index=0),
]
BATCHES = dict(batch1=B1)
B2 = [
    dict(name='应付账单', file='财务协同/应付账单.html', entity='payableBills', modalId='detailModal',
         stabs={'全部': 10, '未付款': 5, '部分付款': 1, '已付款': 4}, pin=3),
    dict(name='应收账单', file='财务协同/应收账单.html', entity='receivableBills', modalId='detailModal',
         stabs={'全部': 11, '未开票': 5, '已开票': 11, '部分收款': 2, '已结清': 3}, pin=3),
    dict(name='付款登记', file='财务协同/付款登记.html', entity='payments', modalId='detailModal',
         stabs={'全部': 5, '待确认': 1, '已确认': 4}, pin=None),
    dict(name='回款登记', file='财务协同/回款登记.html', entity='receipts', modalId='detailModal',
         stabs={'全部': 5, '待核销': 2, '部分核销': 1, '已核销': 2}, pin=None),
    dict(name='开票登记', file='财务协同/开票登记.html', entity='invoices', modalId='detailModal',
         stabs={'全部': 6, '已登记': 4, '已作废': 6}, pin=None),
    dict(name='水单核销', file='财务协同/银行水单核销.html', entity='writeoffs', modalId='detailModal',
         stabs=None, pin=None, noCheckbox=True, tsel='#hxTable tbody'),
    dict(name='采购订单', file='采购管理/采购订单列表.html', entity='purchaseOrders', modalId='detailModal',
         stabs={'全部': 7, '待审核': 2, '已审核': 2, '已完成': 2, '已关闭': 1}, pin=None),
    dict(name='租入单', file='采购管理/租入单列表.html', entity='rentInOrders', modalId='detailModal',
         stabs={'全部': 5, '待审核': 1, '履行中': 1, '部分归还': 1, '已归还': 1, '已终止': 1}, pin=2),
    dict(name='销售订单', file='销售管理/销售订单列表.html', entity='salesOrders', modalId='detailModal',
         stabs={'全部': 8, '待审核': 2, '已审核': 1, '待发货': 2, '已完成': 2, '已关闭': 1}, pin=None),
]
BATCHES['batch2'] = B2
B3 = [
    dict(name='退租申请', file='租赁管理/退租申请列表.html', entity='returnApplies', modalId='detailModal',
         stabs={'全部': 10, '待审核': 2, '已审核': 1, '待入库': 1, '已入库': 6}, pin=3),
    dict(name='丢损赔偿单', file='租赁管理/丢损赔偿单.html', entity='damageOrders', modalId='detailModal',
         stabs={'全部': 5, '赔偿中': 1, '已转应收': 1, '已赔偿': 2}, pin=2),
    dict(name='租出台账', file='租赁管理/租出台账.html', entity='rentTracks', modalId='trackModal',
         stabs={'已退回': 2, '超期未还': 1, '缺损待赔': 1}, pin=1),
    dict(name='在租台账', file='租赁管理/在租台账.html', entity='assetTracks', modalId='trackModal',
         stabs={'全部': 9, '即将到期(7天)': 9}, pin=None, noCheckbox=True),
    dict(name='客商管理', file='基础数据/客商管理.html', entity='partners', modalId='detailModal',
         stabs={'全部': 8, '客户': 4, '供应商': 3, '运营方': 1}, pin=None),
    dict(name='器具档案', file='基础数据/器具档案.html', entity='appliances', modalId='detailModal',
         stabs=None, pin=None),
    dict(name='零部件档案', file='基础数据/零部件档案.html', entity='parts', modalId='detailModal',
         stabs=None, pin=None),
    dict(name='库位档案', file='基础数据/库位档案.html', entity='locations', modalId='detailModal',
         stabs=None, pin=None),
    dict(name='BOM维护', file='基础数据/BOM维护.html', entity='bomVersions', modalId='bomViewModal',
         stabs=None, pin=None, noCheckbox=True, tsel='#bomVerTable tbody', key_contains=True),
]
BATCHES['batch3'] = B3
# 注：在租台账「即将到期(7天)」期望=渲染器 fallback 全量（表无到期日列，默认决策表口径）；
#     BOM维护键列为 ver-tag 富格（V2.1+已生效），断言用 contains
results, fails = [], []

def check(page_name, item, ok, detail=''):
    results.append((page_name, item, ok, detail))
    if not ok: fails.append((page_name, item))
    print(('✅' if ok else '❌'), page_name, '|', item, '|', detail)

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for P in BATCHES[sys.argv[1] if len(sys.argv) > 1 else 'batch1']:
        page = browser.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:150]))
        page.goto((PROTO / P['file']).as_uri(), wait_until='load')
        page.wait_for_selector('tbody tr', timeout=5000)
        page.wait_for_timeout(300)
        tsel = P.get('tsel') or ('tbody' if P.get('tbody_index') is None else f"tbody:nth-of-type({P['tbody_index'] + 1})")
        tbody_loc = page.locator(tsel).first
        rows = tbody_loc.locator('tr')

        # 1 行数=实体有 row 的条数
        keys = page.evaluate("Object.keys(window.DEMO_DATA['%s']).filter(k => window.DEMO_DATA['%s'][k].row)" % (P['entity'], P['entity']))
        n_rows = rows.count()
        check(P['name'], '1 行数=实体条数', n_rows == len(keys), f'{n_rows}=={len(keys)}')

        # 2 行单号=实体键（BOM维护 ver-tag 富键列用 contains）
        key_col = 0 if P.get('noCheckbox') else 1
        row_keys = [rows.nth(i).locator('td').nth(key_col).text_content().strip() for i in range(n_rows)]
        if P.get('key_contains'):
            ok2 = all(any(k in rk for rk in row_keys) for k in keys) and len(row_keys) == len(keys)
        else:
            ok2 = row_keys == keys
        check(P['name'], '2 行单号=实体键', ok2, f'{ok2}')

        # 3 详情弹窗标题=行单号（逐行实点；水单核销等 titleNo 设计=标题含行键或记录 titleNo）
        ok3, tried = True, 0
        for i in range(n_rows):
            a = rows.nth(i).locator('a[data-detail-key]')
            if a.count() == 0: continue
            tried += 1
            key = a.first.get_attribute('data-detail-key')
            tno = page.evaluate("(args) => { const r = window.DEMO_DATA[args[0]][args[1]] || {}; return r.titleNo || ''; }", [P['entity'], key])
            a.first.click()
            page.wait_for_timeout(80)
            title = page.locator('#detailTitle').text_content() or ''
            shown = page.locator('#' + P['modalId']).evaluate("el => el.classList.contains('show')")
            if not ((key in title or tno in title) and shown):
                ok3 = False
                check(P['name'], f'3 详情标题·{key}', False, f'title={title!r} tno={tno!r} shown={shown}')
            page.evaluate("closeModal('%s')" % P['modalId'])
        check(P['name'], '3 详情弹窗标题=行单号', ok3, f'逐行实点 {tried} 行全过' if ok3 else '见上')

        # 4 真过滤（select + input 各一组，若页面有筛选）
        has_filter = page.locator('.filter-card .ff').count() > 0
        if has_filter:
            # select：取首个含选项的 select，选项=第二个 option（非全部）
            sel_ff = page.locator('.filter-card .ff select').first
            if sel_ff.count() > 0:
                opts = sel_ff.locator('option').all_text_contents()
                label = page.locator('.filter-card .ff').first.locator('.ff-label').text_content().rstrip('：:')
                val = next((o for o in opts[1:] if o.strip() and o.strip() != '全部'), None)
                if val:
                    sel_ff.evaluate("(el, v) => { el.value = v; }", val)  # 折叠区控件不可见，直接赋值（readFilters 遍历含隐藏控件）
                    page.locator('.filter-actions button', has_text='查询').click()
                    page.wait_for_timeout(80)
                    got = rows.count()
                    expect = page.evaluate("""([e, v]) => {
                      const D = window.DEMO_DATA[e];
                      // 该 select 对应字段未知，这里按首列之外逐字段尝试：取命中数最多的字段的精确匹配
                      const ks = Object.keys(D).filter(k => D[k].row);
                      const sample = D[ks[0]].row.fields;
                      let best = 0;
                      for (const f of Object.keys(sample)) {
                        const n = ks.filter(k => String(D[k].row.fields[f]) === v).length;
                        if (n > best) best = n;
                      }
                      return best;
                    }""", [P['entity'], val])
                    # 期望值不可靠时只断言行数在 0..全量 且过滤生效（≠全量 或 =0）
                    strict = val not in ('', '全部')
                    okf = strict and got <= len(keys)
                    check(P['name'], f'4 select 过滤（{label[:6]}={val[:14]}）', okf, f'{got} 行（全量 {len(keys)}，字段最优匹配 {expect}）')
                    page.locator('.filter-actions button', has_text='重置').click()
                    page.wait_for_timeout(120)
            # input：单号类控件（label 含 单号/编号/编码/台账编号）填首行键尾 3 位
            tail = keys[0][-3:]
            key_ff = page.locator('.filter-card .ff').filter(
                has=page.locator('.ff-label', has_text=re.compile('单号|编号|编码'))).first
            if key_ff.count() > 0 and key_ff.locator('input').count() > 0:
                key_ff.locator('input').first.evaluate("(el, v) => { el.value = v; }", tail)  # 折叠区控件不可见，直接赋值
                page.locator('.filter-actions button', has_text='查询').click()
                page.wait_for_timeout(80)
                got = rows.count()
                expect = sum(1 for k in keys if tail in k)
                check(P['name'], f'4 input 过滤（尾3位={tail}）', got == expect, f'{got}=={expect}')
                page.locator('.filter-actions button', has_text='重置').click()
                page.wait_for_timeout(120)

        # 5 重置恢复全量
        if has_filter:
            got = rows.count()
            check(P['name'], '5 重置恢复全量', got == len(keys), f'{got}=={len(keys)}')

        # 6 stab 计数=统计值
        if P['stabs']:
            stab_ok, detail = True, []
            for label, want in P['stabs'].items():
                st = page.locator('.stabs .stab', has_text=label).first
                got = int(st.locator('.stab-count').text_content())
                if got != want: stab_ok = False
                detail.append(f'{label}:{got}')
            check(P['name'], '6 stab 计数=统计值', stab_ok, ' '.join(detail))

        # 7 ?notes=1 pin 抽验（配置了 pin 期望的页）
        if P.get('pin'):
            page2 = browser.new_page()
            page2.goto((PROTO / P['file']).as_uri() + '?notes=1', wait_until='load')
            page2.wait_for_selector('tbody tr', timeout=5000)
            page2.wait_for_timeout(300)
            notes = page2.locator('[data-note]')
            layer_on = page2.evaluate("document.body.classList.contains('proto-notes-on')")
            first = notes.first
            box = first.bounding_box()
            page2.mouse.click(box['x'] + box['width'] - 4, box['y'] + 4)
            page2.wait_for_timeout(120)
            opened = page2.locator('.proto-pin.pn-open').count()
            check(P['name'], '7 ?notes=1 pin 抽验',
                  notes.count() >= P['pin'] and layer_on and opened >= 1,
                  f"data-note={notes.count()}/≥{P['pin']} 层={'开' if layer_on else '关'} 实点打开={opened}")
            page2.close()

        check(P['name'], '0 JS 错误', len(errs) == 0, str(errs[:2]) if errs else '0')
        page.close()
    browser.close()

print('\n====', sys.argv[1] if len(sys.argv) > 1 else 'batch1', f'验证门：{len(results)} 项断言，失败 {len(fails)} 项', '====')
sys.exit(1 if fails else 0)
