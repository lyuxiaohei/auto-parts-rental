# -*- coding: utf-8 -*-
"""优化后验证（只读）：静态标记 + 渲染实测"""
import asyncio, io, os, re
from playwright.async_api import async_playwright

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

FORM_PAGES = ['采购管理/采购退货新建.html',
              '销售管理/销售订单新建.html', '销售管理/销售出库新建.html', '销售管理/销售退货新建.html',
              '租赁管理/租赁单新建.html', '租赁管理/退租入库新建.html',
              '租入管理/租入单新建.html', '租入管理/租入归还新建.html',
              '仓储作业/其他入库新建.html', '仓储作业/其他出库新建.html', '仓储作业/调拨新建.html',
              '财务协同/付款新建.html', '财务协同/应付新建.html', '财务协同/应收生成.html',
              '财务协同/开票新建.html', '财务协同/收款新建.html', '财务协同/退款新建.html',
              '系统管理/字典项新建.html', '系统管理/用户新建.html', '系统管理/角色新建.html']
AUDIT_PAGES = ['采购管理/采购订单审核.html', '采购管理/采购入库审核.html', '采购管理/采购退货审核.html',
               '销售管理/销售订单审核.html', '销售管理/销售出库审核.html', '销售管理/销售退货审核.html',
               '租赁管理/租赁单审核.html', '租赁管理/租赁出库确认.html', '租赁管理/退租入库审核.html',
               '租入管理/租入单审核.html', '租入管理/租入入库确认.html', '租入管理/租入归还审核.html',
               '仓储作业/其他入库审核.html', '仓储作业/其他出库审核.html', '仓储作业/盘点审核.html', '仓储作业/调拨审核.html',
               '财务协同/付款确认.html']

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', errors='ignore').read()

print('==== A. 静态标记检查（20 表单页）====')
bad = 0
for p in FORM_PAGES:
    s = rd(p)
    issues = []
    if '<span class="form-label">' in s:
        issues.append('仍有 span 标签')
    # 标签冒号
    for m in re.finditer(r'<div class="form-label"[^>]*>((?:<span[^>]*>[^<]*</span>|[^<])*)</div>', s):
        t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if t and not t.endswith('：'):
            issues.append('标签缺冒号: %s' % t)
    if '<span class="caret"><svg' in s:
        issues.append('仍有 svg 箭头')
    if '.form-row .input-box{width:380px;}' in s:
        issues.append('仍有页级宽度覆盖')
    if 'width:170px' in s:
        issues.append('仍有 170px 控件')
    # 备注
    m = re.search(r'备注：</div>(.{0,400}?)</div>\s*</div>', s, re.S)
    if '备注：' in s:
        seg = s[s.index('备注：'):s.index('备注：') + 700]
        if '<textarea' not in seg:
            issues.append('备注非 textarea')
        if 'min-height:72px' not in seg:
            issues.append('备注 textarea 非 72px')
        if 'align-items:flex-start' not in s[max(0, s.index('备注：') - 200):s.index('备注：')]:
            issues.append('备注行非顶部对齐')
        if 'padding-top:6px' not in s[max(0, s.index('备注：') - 200):s.index('备注：')]:
            issues.append('备注 label 无 padding-top')
    # form-row 内 input-box 是否都有内联宽
    for m in re.finditer(r'<div class="input-box[^"]*"([^>]*)>', s):
        if 'width:' not in m.group(1):
            issues.append('input-box 缺内联宽度: %s' % m.group(1)[:50])
    if issues:
        bad += 1
        print('  %-26s %s' % (p.split('/')[-1], '; '.join(sorted(set(issues))[:4])))
print('  异常页 %d / %d' % (bad, len(FORM_PAGES)))

print()
print('==== B. 审核页检查（17）====')
bad2 = 0
for p in AUDIT_PAGES:
    s = rd(p)
    if '返回列表' in s:
        bad2 += 1
        print('  %-26s 仍有返回列表' % p.split('/')[-1])
    if 'class="submit-bar"' not in s:
        bad2 += 1
        print('  %-26s 缺提交条' % p.split('/')[-1])
print('  异常页 %d / %d' % (bad2, len(AUDIT_PAGES)))

print()
print('==== C. 渲染实测 ====')
def url(rel):
    return 'file:///' + os.path.join(ROOT, rel).replace('\\', '/')

PROBE = """() => {
    var lb = document.querySelector('.form-row .form-label');
    var boxes = Array.from(document.querySelectorAll('.form-row .input-box')).filter(function (b) {
        return b.offsetParent !== null;  // 排除 display:none 的条件行（样板同样有）
    }).map(function (b) { return Math.round(b.getBoundingClientRect().width); });
    var car = document.querySelector('.input-box .caret');
    var ta = null;
    Array.from(document.querySelectorAll('.form-row')).forEach(function (r) {
        var l = r.querySelector('.form-label');
        if (l && l.textContent.indexOf('备注') > -1) {
            var t = r.querySelector('textarea');
            if (t) { var cs = getComputedStyle(t); ta = {h: Math.round(t.getBoundingClientRect().height), minH: cs.minHeight, resize: cs.resize, inShell: !!t.closest('.input-box')}; }
        }
    });
    var dates = Array.from(document.querySelectorAll('.form-row input[type=date]')).length;
    var headBack = Array.from(document.querySelectorAll('.card-head .head-btns button')).some(function (b) { return b.textContent.indexOf('返回') > -1; });
    var bar = !!document.querySelector('.submit-bar');
    return {labelTag: lb ? lb.tagName : '', labelText: lb ? lb.textContent.replace(/\\s+/g, '') : '',
            widths: boxes, caret: car ? car.textContent.trim() : '', note: ta, dates: dates,
            headBack: headBack, bar: bar};
}"""

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        # 样板
        await pg.goto(url('采购管理/采购订单新建.html')); await pg.wait_for_timeout(300)
        base = await pg.evaluate(PROBE)
        print('  样板:', {k: base[k] for k in ('labelTag', 'labelText', 'caret', 'note', 'widths')})
        nbad = 0
        for p in FORM_PAGES:
            await pg.goto(url(p)); await pg.wait_for_timeout(260)
            r = await pg.evaluate(PROBE)
            iss = []
            if r['labelTag'] != base['labelTag']:
                iss.append('labelTag=%s' % r['labelTag'])
            if r['labelText'] != base['labelText'] and not r['labelText'].endswith('：'):
                iss.append('labelText=%s' % r['labelText'])
            if r['caret'] not in ('▾', ''):
                iss.append('caret=%r' % r['caret'])
            wbad = sorted(set(w for w in r['widths'] if w not in (380,)))
            if wbad:
                iss.append('宽度=%s' % wbad)
            if r['note'] and not (r['note']['h'] == 72 and r['note']['minH'] == '72px' and r['note']['resize'] == 'vertical' and r['note']['inShell']):
                iss.append('备注=%s' % r['note'])
            if errs:
                iss.append('JS:%s' % errs[0][:40])
                errs.clear()
            if iss:
                nbad += 1
                print('  %-26s %s' % (p.split('/')[-1], '; '.join(iss)))
        print('  表单页渲染异常 %d / %d' % (nbad, len(FORM_PAGES)))
        # 审核页
        nbad2 = 0
        for p in AUDIT_PAGES:
            await pg.goto(url(p)); await pg.wait_for_timeout(260)
            r = await pg.evaluate(PROBE)
            if r['headBack'] or not r['bar'] or errs:
                nbad2 += 1
                print('  %-26s headBack=%s bar=%s JS=%s' % (p.split('/')[-1], r['headBack'], r['bar'], errs[:1]))
                errs.clear()
        print('  审核页渲染异常 %d / %d' % (nbad2, len(AUDIT_PAGES)))
        # 日期控件汇总
        print()
        print('==== D. 日期控件（type=date）====')
        for p in FORM_PAGES:
            await pg.goto(url(p)); await pg.wait_for_timeout(220)
            r = await pg.evaluate(PROBE)
            if r['dates']:
                print('  %-26s type=date ×%d' % (p.split('/')[-1], r['dates']))
        await b.close()

asyncio.run(main())
