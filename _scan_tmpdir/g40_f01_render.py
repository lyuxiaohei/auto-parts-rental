# -*- coding: utf-8 -*-
"""G40 T4/T6 F01 渲染核对（只读）
1. 文本溢出（getComputedTextLength vs 所在节点框宽）——全 SVG 扫描
2. 新增「转移出库」节点在位（L1/L3 各一）＋ href 可达
3. 既有节点无丢失（全 SVG <a> 数量·节点 rect 数量·文本节点数 对比备份基线）
4. 截图：整页 + L1 行 + L3 行 + 支线 S1（五态）
"""
import io, os, re, sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent.parent
PROTO = BASE / 'P3-R01-包装租赁管理后台原型'
BACKUP = BASE / '_scan_tmpdir' / 'backup-g40-20260915' / 'P3-R01-包装租赁管理后台原型'
OUT = BASE / '_scan_tmpdir'
F01 = PROTO / 'P3-R01-F01-业务流程导航图.html'
F01_BK = BACKUP / 'P3-R01-F01-业务流程导航图.html'

results = []


def check(name, cond, detail=''):
    results.append((name, bool(cond), detail))
    print('  [%s] %s %s' % ('PASS' if cond else 'FAIL', name, detail))


MEASURE = r"""() => {
  const svgs = [...document.querySelectorAll('svg')];
  const out = [];
  svgs.forEach((svg, si) => {
    const nodes = [];
    svg.querySelectorAll(':scope > a').forEach(a => {
      const rect = a.querySelector('rect');
      const texts = [...a.querySelectorAll('text')];
      if (!rect) return;
      const rw = parseFloat(rect.getAttribute('width'));
      texts.forEach(t => {
        let len = 0;
        try { len = t.getComputedTextLength(); } catch (e) { len = -1; }
        nodes.push({ svg: si, name: t.textContent.trim().slice(0, 20), box: rw, text: Math.round(len),
                     over: rw - len, x: t.getAttribute('x'), y: t.getAttribute('y'),
                     href: a.getAttribute('href') });
      });
    });
    out.push({ svg: si, links: svg.querySelectorAll(':scope > a').length,
               rects: svg.querySelectorAll('rect').length,
               texts: svg.querySelectorAll('text').length,
               nodes: nodes });
  });
  return out;
}"""


def main():
    print('=== F01 渲染核对 ===')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1280, 'height': 1000})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.on('console', lambda m: errs.append('console:' + m.text[:120]) if m.type == 'error' else None)
        pg.goto(F01.as_uri(), wait_until='load')
        pg.wait_for_timeout(600)
        data = pg.evaluate(MEASURE)

        # 1 溢出
        allnodes = [n for d in data for n in d['nodes']]
        over = [n for n in allnodes if n['over'] < 0]
        check('文本溢出 0 处', len(over) == 0, '共 %d 个节点内文本·溢出 %d' % (len(allnodes), len(over)))
        for n in over:
            print('      溢出 %+d  %s  box=%s text=%s  y=%s' % (n['over'], n['name'], n['box'], n['text'], n['y']))

        # 2 新节点在位
        tgt = [n for n in allnodes if n['name'] == '转移出库']
        check('「转移出库」节点 = 2（L1/L3 各一）', len(tgt) == 2,
              'y=%s' % sorted(n['y'] for n in tgt))
        check('「转移出库」节点 href 可达', all(n['href'] == '租赁管理/转移出库列表.html' for n in tgt),
              str(set(n['href'] for n in tgt)))
        sub = [n for n in allnodes if n['name'].startswith('客户间转移')]
        check('副标「客户间转移 · 直接客户 → 终端客户」×2', len(sub) == 2, 'box=%s' % [n['box'] for n in sub])

        # 3 既有节点基线对比（备份文件同样渲染计数）
        pg2 = b.new_page()
        pg2.goto(F01_BK.as_uri(), wait_until='load')
        pg2.wait_for_timeout(400)
        data_bk = pg2.evaluate(MEASURE)
        for d, db in zip(data, data_bk):
            check('svg%d 链接数（备份 %d → 现 %d）' % (d['svg'], db['links'], d['links']),
                  d['links'] == db['links'] + (2 if d['svg'] == 0 else 0), '')
            check('svg%d 文本节点数（备份 %d → 现 %d）' % (d['svg'], db['texts'], d['texts']),
                  d['texts'] == db['texts'] + (13 if d['svg'] == 0 else 0),
                  '' )
            check('svg%d rect 数（备份 %d → 现 %d）' % (d['svg'], db['rects'], d['rects']),
                  d['rects'] == db['rects'] + (5 if d['svg'] == 0 else 0), '')
        check('无 JS 报错', len(errs) == 0, str(errs[:3]))

        # 4 截图
        print('=== 截图 ===')
        page_h = pg.evaluate('document.documentElement.scrollHeight')
        pg.screenshot(path=str(OUT / 'g40_f01_full.png'), full_page=True)
        print('   g40_f01_full.png  (h=%s)' % page_h)
        for name, y0, h in [('g40_f01_L1.png', 300, 260), ('g40_f01_L3.png', 760, 250),
                            ('g40_f01_S1.png', 575, 165), ('g40_f01_fin.png', 1870, 200)]:
            el = pg.locator('svg').first
            pg.evaluate('window.scrollTo(0,%d)' % max(0, y0 - 60))
            pg.wait_for_timeout(150)
            pg.screenshot(path=str(OUT / name), clip={'x': 0, 'y': max(0, y0 - 60) - pg.evaluate('window.scrollY'), 'width': 900, 'height': h}) if False else None
            pg.screenshot(path=str(OUT / name))
            print('   %s' % name)
        b.close()

    ok = all(r[1] for r in results)
    print('\n--- 汇总 ---')
    for n, c, d in results:
        print('  %s  %s  %s' % ('PASS' if c else 'FAIL', n, d))
    print('总判定: %s' % ('PASS' if ok else 'FAIL'))
    io.open(OUT / 'g40_f01_render.json', 'w', encoding='utf-8').write(
        json.dumps([[n, c, d] for n, c, d in results], ensure_ascii=False, indent=1))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
