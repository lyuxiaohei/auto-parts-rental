# -*- coding: utf-8 -*-
"""G40 T6 PW 抽验（v2）
A. F01 新节点/改名页链接：真实导航断言（点击 → URL 落到目标页）
B. F01 📎 弹窗开合 + Mermaid 折叠
C. 5 个改名页独立加载 0 JS 错误且无旧名引用
"""
import io, json, sys
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent.parent
PROTO = BASE / 'P3-R01-包装租赁管理后台原型'
OUT = BASE / '_scan_tmpdir'
results = []


def check(name, cond, detail=''):
    results.append((name, bool(cond), detail))
    print('  [%s] %s  %s' % ('PASS' if cond else 'FAIL', name, detail))


def url(rel):
    return (PROTO / rel).as_uri()


F01 = 'P3-R01-F01-业务流程导航图.html'
RENAMED = ['财务协同/收款登记.html', '财务协同/收款详情.html', '财务协同/损益报表.html',
           '财务协同/银行回单核销.html', '财务协同/银行回单核销详情.html']
NAV = [('转移出库节点', '租赁管理/转移出库列表.html', 2),
       ('F1 收款登记节点', '财务协同/收款登记.html', None),
       ('F1 收款核销节点', '财务协同/银行回单核销.html', None),
       ('S2 财务看板节点', '财务协同/损益报表.html', None)]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1280, 'height': 1000})
    errs = []
    pg.on('pageerror', lambda e: errs.append('pageerror:' + str(e)[:160]))
    pg.on('console', lambda m: errs.append('console:' + m.text[:160]) if m.type == 'error' else None)

    print('=== A. F01 链接真实导航 ===')
    for label, href, want in NAV:
        pg.goto(url(F01), wait_until='load')
        pg.wait_for_timeout(400)
        n = pg.evaluate("""(h) => document.querySelectorAll('svg a[href="'+h+'"]').length""", href)
        exists = (PROTO / href).is_file()
        check('%s：a 标签数=%s（期望 %s）· 目标文件存在=%s' % (label, n, want or '>=1', exists),
              n > 0 and (want is None or n == want) and exists)
        try:
            with pg.expect_navigation(timeout=8000):
                pg.evaluate("""(h) => { const a=document.querySelector('svg a[href="'+h+'"]');
                    a.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true})); }""", href)
            landed = unquote(pg.url)
            check('   → 导航落地 %s' % href, landed.endswith(href.replace('/', '/')), landed.split('/原型/')[-1])
        except Exception as ex:
            check('   → 导航落地 %s' % href, False, str(ex)[:120])

    print('=== B. F01 弹窗与折叠 ===')
    pg.goto(url(F01), wait_until='load')
    pg.wait_for_timeout(500)
    for sid in ['l1', 'l3', 'fin']:
        r = pg.evaluate("""(id) => {
          const el=[...document.querySelectorAll('g.src-tag')].find(x=>new RegExp(id).test(x.getAttribute('onclick')||''));
          if(!el) return 'no-tag';
          el.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,clientX:300,clientY:300}));
          const pop=document.getElementById('srcPop');
          return (pop.style.display==='block'?'open':'closed')+'|'+document.getElementById('srcPopBody').textContent.trim().slice(0,30);
        }""", sid)
        check('F01 📎 %s' % sid, r.startswith('open'), r)
    mm = pg.evaluate("""() => { const d=document.querySelector('details.src-mermaid'); d.open=true;
        const t=d.querySelector('pre').textContent;
        return [t.includes('转移出库'), t.includes('按持有量计租')]; }""")
    check('F01 Mermaid 折叠区含转移出库 + 计租口径', all(mm), str(mm))

    print('=== C. 改名页独立加载 ===')
    for rel in RENAMED:
        errs.clear()
        pg.goto(url(rel), wait_until='load')
        pg.wait_for_timeout(400)
        html = pg.evaluate('document.documentElement.outerHTML')
        old = sum(html.count(x) for x in ['回款登记', '回款详情', '银行水单核销', '水单核销详情', '盈亏报表'])
        title = pg.evaluate('document.title')
        check('%s  JS错=%d 旧名=%d  title=%s' % (rel, len(errs), old, title),
              len(errs) == 0 and old == 0, str(errs[:1]))
    b.close()

ok = all(r[1] for r in results)
print('\n--- 汇总 ---')
for n, c, d in results:
    print('  %s  %s' % ('PASS' if c else 'FAIL', n))
print('总判定: %s' % ('PASS' if ok else 'FAIL'))
io.open(OUT / 'g40_pw.json', 'w', encoding='utf-8').write(
    json.dumps([[n, c, d] for n, c, d in results], ensure_ascii=False, indent=1))
sys.exit(0 if ok else 1)
