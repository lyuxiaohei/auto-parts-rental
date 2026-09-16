# -*- coding: utf-8 -*-
"""F01 v3.8 渲染核对（只读·Playwright）
1. 文本溢出：全部 SVG 内 <a> 节点 getComputedTextLength vs rect 宽
2. S7 三节点在位（href 可达）＋ L1/L3 转移出库节点已撤
3. 既有节点对账：主图/支图 <a>·rect·text 计数 vs v3.7 备份
4. viewBox 渲染宽高 vs 声明（无裁切）
5. 截图：整页 + S7 支线 + L1 行 + L3 行
"""
import io, json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent.parent
PROTO = BASE / 'P3-R01-包装租赁管理后台原型'
BK = BASE / '_scan_tmpdir' / 'backup-导航图F01-20260916' / 'P3-R01-F01-业务流程导航图-v3.7-人名已复原.html'
F01 = PROTO / 'P3-R01-F01-业务流程导航图.html'
OUT = BASE / '_scan_tmpdir'
S = 2
fails = []

def check(name, cond, detail=''):
    print('  [%s] %s %s' % ('PASS' if cond else 'FAIL', name, detail))
    if not cond:
        fails.append(name)

MEASURE = r"""() => {
  const out = {overflow: [], counts: [], vb: []};
  document.querySelectorAll('svg').forEach((svg, si) => {
    let na = 0, nrect = 0, ntext = 0;
    svg.querySelectorAll('*').forEach(el => {
      if (el.tagName === 'A' && el.closest('svg') === svg) na++;
      if (el.tagName === 'RECT') nrect++;
      if (el.tagName === 'TEXT') ntext++;
    });
    out.counts.push({svg: si, a: na, rect: nrect, text: ntext});
    const vb = svg.getAttribute('viewBox').split(' ').map(Number);
    const bb = svg.getBBox();
    out.vb.push({svg: si, vb: vb, bbox: {x: bb.x, y: bb.y, w: bb.width, h: bb.height}});
    svg.querySelectorAll(':scope > a').forEach(a => {
      const rect = a.querySelector('rect');
      if (!rect) return;
      const rw = parseFloat(rect.getAttribute('width'));
      a.querySelectorAll('text').forEach(t => {
        let len = 0;
        try { len = t.getComputedTextLength(); } catch (e) { len = -1; }
        if (len > rw) out.overflow.push({svg: si, text: t.textContent.trim().slice(0, 26), box: rw, len: Math.round(len)});
      });
    });
  });
  const s7 = [...document.querySelectorAll('svg')][1];
  const s7links = [...s7.querySelectorAll(':scope > a')].map(a => a.getAttribute('href'));
  out.s7links = s7links.filter(h => h && h.indexOf('转移出库') >= 0);
  const mainSvg = [...document.querySelectorAll('svg')][0];
  out.mainTransfer = [...mainSvg.querySelectorAll(':scope > a')].map(a => a.getAttribute('href')).filter(h => h && h.indexOf('转移出库') >= 0);
  out.jsErrors = window.__jserrs || [];
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1280, 'height': 1200}, device_scale_factor=S)
    jserrs = []
    pg.on('pageerror', lambda e: jserrs.append(str(e)))
    pg.goto(F01.as_uri(), wait_until='load')
    pg.wait_for_timeout(800)
    r = pg.evaluate(MEASURE)
    box_main = pg.locator('svg').nth(0).bounding_box()
    box_sub = pg.locator('svg').nth(1).bounding_box()
    pg.evaluate('window.scrollTo(0,0)')
    pg.wait_for_timeout(200)
    pg.screenshot(path=str(OUT / 'g41fix_f01_fullpage.png'), full_page=True)

    # S7 / L1 / L3 裁切坐标（svg 显示宽 box.width，k=width/880）
    k = box_main['width'] / 880.0
    from PIL import Image
    im = Image.open(OUT / 'g41fix_f01_fullpage.png')
    ox, oy = int(box_main['x'] * S), int(box_main['y'] * S)
    def crop(x0, y0, x1, y1, name, svgbox, svgoff):
        kk = svgbox['width'] / 880.0
        cx0 = int(svgoff['x'] * S + x0 * kk * S); cy0 = int(svgoff['y'] * S + y0 * kk * S)
        cx1 = int(svgoff['x'] * S + x1 * kk * S); cy1 = int(svgoff['y'] * S + y1 * kk * S)
        im.crop((cx0, cy0, cx1, cy1)).save(OUT / name)
        print('  crop %s -> %s' % (name, (cx1-cx0, cy1-cy0)))
    # 主图 L1 行(约 y300-530) L3 行(约 y760-990)；支图 S7(y780-944)
    crop(0, 300, 880, 530, 'g41fix_f01_L1_row.png', box_main, {'x': box_main['x'], 'y': box_main['y']})
    crop(0, 760, 880, 990, 'g41fix_f01_L3_row.png', box_main, {'x': box_main['x'], 'y': box_main['y']})
    ksub = box_sub['width'] / 880.0
    cx0 = int(box_sub['x'] * S); cy0 = int(box_sub['y'] * S + 780 * ksub * S)
    cx1 = int((box_sub['x'] + box_sub['width']) * S); cy1 = int(box_sub['y'] * S + 944 * ksub * S)
    im.crop((cx0, cy0, cx1, cy1)).save(OUT / 'g41fix_f01_S7.png')
    print('  crop g41fix_f01_S7.png')
    b.close()

print('== 1. 文本溢出（全部 SVG <a> 节点）==')
check('溢出 0 处', len(r['overflow']) == 0, str(r['overflow'][:4]))
print('== 2. S7 在位 / L1L3 已撤 ==')
check('S7 三链接在位', r['s7links'] == ['租赁管理/转移出库列表.html', '租赁管理/转移出库新建.html', '租赁管理/转移出库单详情.html'], str(r['s7links']))
check('主图转移出库 <a> = 0', len(r['mainTransfer']) == 0, str(r['mainTransfer']))
print('== 3. 计数对账（静态正则·两文件同法）==')
print('  now:', r['counts'])
import re
now_src = io.open(F01, encoding='utf-8').read()
bkc = io.open(BK, encoding='utf-8').read()
def counts(txt, vb):
    seg = txt.split('viewBox="0 0 880 %d"' % vb, 1)
    seg = seg[1] if len(seg) > 1 else ''
    seg = seg.split('</svg>')[0] if '</svg>' in seg else seg
    return (len(re.findall(r'<a ', seg)), len(re.findall(r'<rect ', seg)), len(re.findall(r'<text ', seg)))
bm = counts(bkc, 2184); bs = counts(bkc, 846)
nm = counts(now_src, 2184); ns = counts(now_src, 944)
print('  主图 v3.7备份(a,rect,text)=%s → v3.8=%s（预期 a-2）' % (bm, nm))
print('  支图 v3.7备份(a,rect,text)=%s → v3.8=%s（预期 a+3）' % (bs, ns))
check('主图 a 数=备份-2（撤 L1/L3 两节点）', nm[0] == bm[0] - 2, '%d vs %d-2' % (nm[0], bm[0]))
check('支图 a 数=备份+3（S7 三节点）', ns[0] == bs[0] + 3, '%d vs %d+3' % (ns[0], bs[0]))
print('== 4. viewBox 渲染几何 ==')
for v in r['vb']:
    declared_h = v['vb'][3]
    bbox_bottom = v['bbox']['y'] + v['bbox']['h']
    check('SVG%d 内容底 %.0f ≤ viewBox 高 %d（不裁切）' % (v['svg'], bbox_bottom, declared_h), bbox_bottom <= declared_h + 0.5, 'bbox=%dx%d' % (v['bbox']['w'], v['bbox']['h']))
print('== 5. JS 错误 ==')
check('JS 错误 0', len(jserrs) == 0, str(jserrs[:2]))
print('=' * 60)
print('总判定：%s' % ('ALL PASS' if not fails else 'FAIL: %s' % fails))
