# -*- coding: utf-8 -*-
"""G36 C1+C2 PW 验证：背靠背转租互溯 + 库存查询项目闭环对平"""
import asyncio, os, re
from playwright.async_api import async_playwright

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def url(rel):
    return 'file:///' + os.path.join(BASE, rel).replace('\\', '/')

def num(t):
    d = re.findall(r'[\d,]+', t or '')
    return int(d[0].replace(',', '')) if d else 0

async def main():
    ok = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))

        # ================= C1 =================
        # 1) 租入单 RZD-008 详情 → 链路含 CK-023（可点跳租赁出库列表）
        await pg.goto(url('租入管理/租入单列表.html'))
        await pg.wait_for_timeout(500)
        row = pg.locator('tbody tr', has_text='RZD-20260902-008').first
        await row.locator('.ops a', has_text='详情').click()
        await pg.wait_for_timeout(300)
        chain_txt = await pg.eval_on_selector('.modal-overlay.show .chain', 'el=>el.textContent')
        has_ck = 'CK-20260914-023' in chain_txt
        has_rz = 'RZRK-20260903-023' in chain_txt
        ok.append(('C1-1 租入单详情链含 租入入库+CK-023', has_ck and has_rz, chain_txt[:80]))
        ck_link = pg.locator('.modal-overlay.show .chain .lk', has_text='CK-20260914-023').first
        async with pg.expect_navigation():
            await ck_link.click()
        u1 = await pg.evaluate('()=>location.pathname')
        ok.append(('C1-2 租入单→CK 链接跳租赁出库列表', '租赁出库列表' in u1, u1.split('/')[-1]))

        # 2) 租赁出库 CK-023 详情 → 关联租入入库 + 关联租入单
        await pg.goto(url('租赁管理/租赁出库列表.html'))
        await pg.wait_for_timeout(500)
        row = pg.locator('tbody tr', has_text='CK-20260914-023').first
        await row.locator('.ops a', has_text='详情').click()
        await pg.wait_for_timeout(300)
        info_txt = await pg.eval_on_selector('.modal-overlay.show .modal-body', 'el=>el.textContent')
        ok.append(('C1-3 CK详情回链 RZRK-023 + RZD-008', ('RZRK-20260903-023' in info_txt) and ('RZD-20260902-008' in info_txt), ''))
        rz_link = pg.locator('.modal-overlay.show .dval .lk', has_text='RZD-20260902-008').first
        async with pg.expect_navigation():
            await rz_link.click()
        u2 = await pg.evaluate('()=>location.pathname')
        ok.append(('C1-4 CK→租入单回链可跳', '租入单列表' in u2, u2.split('/')[-1]))

        # 3) 租入入库 RZRK-023 详情 → 链路含 CK-023
        await pg.goto(url('租入管理/租入入库列表.html'))
        await pg.wait_for_timeout(500)
        row = pg.locator('tbody tr', has_text='RZRK-20260903-023').first
        await row.locator('.ops a', has_text='详情').click()
        await pg.wait_for_timeout(300)
        chain_txt = await pg.eval_on_selector('.modal-overlay.show .chain', 'el=>el.textContent')
        ok.append(('C1-5 租入入库详情链含 RZD-008+CK-023', ('CK-20260914-023' in chain_txt) and ('RZD-20260902-008' in chain_txt), ''))
        # 确认弹窗 立即转租 默认勾选
        chk = await pg.eval_on_selector('#confirmModal input[type=checkbox]', 'el=>el.checked') if await pg.eval_on_selector_all('#confirmModal input[type=checkbox]', 'els=>els.length') else None
        ok.append(('C1-6 确认弹窗立即转租默认勾选', chk is True, 'checked=%s' % chk))

        # ================= C2 =================
        await pg.goto(url('仓储作业/库存查询.html'))
        await pg.wait_for_timeout(600)
        main_tb = None
        for t in await pg.eval_on_selector_all('table', 'els=>els.map(e=>e.querySelector("thead")?e.querySelector("thead").textContent:"")'):
            pass
        async def get_rows():
            return await pg.evaluate("""() => {
                var main = null;
                document.querySelectorAll('table').forEach(function (t) {
                    var th = t.querySelector('thead');
                    if (th && th.textContent.indexOf('适用项目') > -1 && th.textContent.indexOf('总量') > -1) main = t;
                });
                if (!main) return [];
                return Array.prototype.map.call(main.querySelector('tbody').rows, function (tr) {
                    return { key: tr.cells[0].textContent.trim(), proj: tr.cells[3].textContent.trim(),
                             nums: [4,5,6,7,8].map(function(c){ return tr.cells[c] ? tr.cells[c].textContent : ''; }) };
                });
            }""")

        # 不筛选基线（总量=四态之和已由 C2 口径修正）
        base_rows = await get_rows()
        base = {r['key']: [num(x) for x in r['nums']] for r in base_rows}

        async def select_proj(p):
            await pg.evaluate("""(p) => {
                var ffs = document.querySelectorAll('.ff');
                for (var i = 0; i < ffs.length; i++) {
                    var lb = ffs[i].querySelector('.ff-label');
                    if (lb && lb.textContent.indexOf('项目') === 0) {
                        var sel = ffs[i].querySelector('select');
                        if (sel) { sel.value = p; }
                    }
                }
            }""", p)
            await pg.click('button:has-text("查 询")') if await pg.locator('button:has-text("查 询")').count() else await pg.click('button:has-text("查询")')
            await pg.wait_for_timeout(300)

        per_proj_sum = {}
        for P in ['PRJ-2601', 'PRJ-2602', 'PRJ-2603', 'PRJ-2604', 'PRJ-2605']:
            await select_proj(P)
            rows = await get_rows()
            closed = len(rows) > 0
            for r in rows:
                n = [num(x) for x in r['nums']]
                if n[0] + n[1] + n[2] + n[3] != n[4]:
                    closed = False
                if r['proj'] != P:
                    closed = False
            for r in rows:
                k = r['key']
                n = [num(x) for x in r['nums']]
                per_proj_sum.setdefault(k, [0, 0, 0, 0, 0])
                for c in range(5):
                    per_proj_sum[k][c] += n[c]
            if P in ('PRJ-2601', 'PRJ-2602', 'PRJ-2603'):
                ok.append(('C2 项目 %s 行数=%d 各状态列之和=总量' % (P, len(rows)), closed, ''))

        # 全项目之和 = 不筛选总数
        total_match = True
        detail = []
        for k, v in base.items():
            ps = per_proj_sum.get(k)
            if ps != v:
                total_match = False
                detail.append('%s %s!=%s' % (k, ps, v))
        ok.append(('C2 全项目之和=不筛选总数（%d 行对平）' % len(base), total_match, '; '.join(detail[:3])))

        # 下钻同步：PRJ-2601 → WBX-1210L 在租 1,800
        await select_proj('PRJ-2601')
        await pg.evaluate("()=>{var _=document.querySelector('tbody tr .ops a[href], tbody tr .ops a');}")
        drill_open = await pg.evaluate("""() => {
            var rows = document.querySelectorAll('table');
            var main = null;
            document.querySelectorAll('table').forEach(function (t) {
                var th = t.querySelector('thead');
                if (th && th.textContent.indexOf('适用项目') > -1) main = t;
            });
            var tr = main.querySelector('tbody').rows[0];
            var a = tr.querySelector('.ops a');
            return a ? a.textContent : '';
        }""")
        # 打开下钻弹窗（客户在租 op）
        opened = await pg.evaluate("""() => {
            var main = null;
            document.querySelectorAll('table').forEach(function (t) {
                var th = t.querySelector('thead');
                if (th && th.textContent.indexOf('适用项目') > -1) main = t;
            });
            var links = main.querySelectorAll('.ops a');
            for (var i = 0; i < links.length; i++) {
                if (links[i].textContent.indexOf('客户在租') > -1) { links[i].click(); return true; }
            }
            return false;
        }""")
        await pg.wait_for_timeout(300)
        drill = await pg.evaluate("""() => {
            var out = [];
            document.querySelectorAll('table').forEach(function (t) {
                var th = t.querySelector('thead');
                if (th && th.textContent.indexOf('所属项目') > -1 && th.textContent.indexOf('在租数量') > -1) {
                    Array.prototype.forEach.call(t.querySelector('tbody').rows, function (tr) {
                        out.push([tr.cells[0].textContent.trim(), tr.cells[3].textContent.trim(), tr.cells[4].textContent.trim()]);
                    });
                }
            });
            return out;
        }""")
        drill_ok = len(drill) > 0 and all((d[1].find('PRJ-2601') > -1) for d in drill)
        wbx = [d for d in drill if d[0] == 'WBX-1210L']
        ok.append(('C2 下钻按项目过滤（%d 行·全 PRJ-2601）' % len(drill), drill_ok, str(drill[:2])))
        ok.append(('C2 下钻 WBX-1210L 在租=1,800（项目口径）', bool(wbx) and '1,800' in wbx[0][2], str(wbx)))

        ok.append(('C1+C2 全程 JS 错误 0', not errs, '; '.join(errs[:3])))
        await b.close()

    print('=' * 70)
    fails = 0
    for name, passed, ev in ok:
        print('[%s] %s %s' % ('PASS' if passed else 'FAIL', name, ('| ' + ev) if ev else ''))
        if not passed:
            fails += 1
    print('总判定：%d PASS / %d FAIL' % (len(ok) - fails, fails))

asyncio.run(main())
