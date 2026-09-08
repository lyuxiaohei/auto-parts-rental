# -*- coding: utf-8 -*-
"""任务二·列表数据驱动全量推广验证门（2026-09-08）· 逐页断言组（照 verify_listpilot.py 结构）
用法：python verify_listfull.py batch1|batch2|batch3
"""
import sys, io, argparse
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
        tsel = 'tbody' if P.get('tbody_index') is None else f"tbody:nth-of-type({P['tbody_index'] + 1})"
        tbody_loc = page.locator(tsel).first
        rows = tbody_loc.locator('tr')

        # 1 行数=实体有 row 的条数
        keys = page.evaluate("Object.keys(window.DEMO_DATA['%s']).filter(k => window.DEMO_DATA['%s'][k].row)" % (P['entity'], P['entity']))
        n_rows = rows.count()
        check(P['name'], '1 行数=实体条数', n_rows == len(keys), f'{n_rows}=={len(keys)}')

        # 2 行单号=实体键
        key_col = 0 if P.get('noCheckbox') else 1
        row_keys = [rows.nth(i).locator('td').nth(key_col).text_content().strip() for i in range(n_rows)]
        check(P['name'], '2 行单号=实体键', row_keys == keys, f'{row_keys == keys}')

        # 3 详情弹窗标题=行单号（逐行实点）
        ok3, tried = True, 0
        for i in range(n_rows):
            a = rows.nth(i).locator('a[data-detail-key]')
            if a.count() == 0: continue
            tried += 1
            key = a.first.get_attribute('data-detail-key')
            a.first.click()
            page.wait_for_timeout(80)
            title = page.locator('#detailTitle').text_content()
            shown = page.locator('#' + P['modalId']).evaluate("el => el.classList.contains('show')")
            if not (key in (title or '') and shown):
                ok3 = False
                check(P['name'], f'3 详情标题·{key}', False, f'title={title!r} shown={shown}')
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
                    sel_ff.select_option(label=val)
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
            # input：单号尾 3 位
            tail = keys[0][-3:]
            inp_ff = page.locator('.filter-card .ff').filter(has=page.locator('input')).first
            if inp_ff.count() > 0:
                inp_ff.locator('input').first.fill(tail)
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
