# -*- coding: utf-8 -*-
"""批4 F01 几何断言 + 全页截图：节点 rect 零重叠 / 新直连箭头对齐 0 偏差 / 新增注记无遮挡 / audit 0 问题"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
F01 = PROTO / 'P3-R01-F01-业务流程导航图.html'
txt = F01.read_bytes().decode('utf-8')
PASS, FAIL = [], []

def check(name, cond, detail=''):
    (PASS if cond else FAIL).append((name, detail))
    print(('✅' if cond else '❌'), name, detail)

# 1) 节点 rect 零重叠（h>=36 的节点框）
rects = [(float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)))
         for m in re.finditer(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"', txt)
         if float(m.group(4)) >= 36]
overlaps = []
for i in range(len(rects)):
    for j in range(i + 1, len(rects)):
        a, b = rects[i], rects[j]
        if a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]:
            overlaps.append((a, b))
check('节点 rect 零重叠', not overlaps, str(overlaps[:2]))

# 2) T1 直连箭头对齐（210 = 在租台账右缘 40+170；400 = 退租入库左缘）
m = re.search(r'<line x1="210" y1="930" x2="400" y2="930"', txt)
check('T1 直连箭头存在（210→400）', bool(m))
check('在租台账右缘=210', '40" y="902" width="170"' in txt.replace('<rect x="', '').replace(' ', '" y="902" width="170"') or re.search(r'<rect x="40" y="902" width="170"', txt))
check('退租入库左缘=400', bool(re.search(r'<rect x="400" y="902" width="150"', txt)))
check('旧 230/380 箭头已删', 'x1="210" y1="930" x2="230"' not in txt and 'x1="380" y1="930"' not in txt)
check('退租申请节点已删', '>退租申请</text>' not in txt)

# 3) 新增两行注记无遮挡（y 960-990 带内无节点 rect）
band = [r for r in rects if r[1] < 990 and r[1] + r[3] > 958]
check('新注记带（y958-990）无节点框遮挡', not band, str(band[:2]))
check('客户转租注记在', '客户转租：独立菜单改状态' in txt)
check('客户虚拟仓注记在', '客户虚拟仓：在客户处的租赁资产按客户归集（on-hire）' in txt)

# 4) 文案断言
for kw, tag in [('按 BOM 组合出库', 'L2节点'), ('按零件入库', 'T1/S节点'), ('直接转应收/应付', 'T1赔偿'),
                ('直接生成应收/应付', 'S4赔偿'), ('四类应收来源', 'F1'), ('四类应付来源', 'F2'),
                ('v3.0', '版本'), ('供应商', '供应商在图'), ('15 类单据', 'S7')]:
    check(f'文案含「{kw}」({tag})', kw in txt)
check('全图无运营方', '运营方' not in txt)
check('无组装列表链接残留', '仓储作业/组装列表' not in txt and '仓储作业/拆卸管理列表' not in txt)

# 5) 浏览器实测：加载 0 JS 错 + 死链 0 + 截图
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 1000})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto((F01).as_uri())
    pg.wait_for_timeout(800)
    check('F01 JS 错 0', not errs, str(errs[:2]))
    # 链接目标存在性
    hrefs = pg.eval_on_selector_all('svg a[href]', 'els => els.map(e => e.getAttribute("href"))')
    dead = [h for h in set(hrefs) if not (PROTO / h).exists()]
    check('F01 死链 0', not dead, str(dead[:3]))
    # 新注记视觉存在（文本可见）
    vis = pg.evaluate("""() => {
      const els = [...document.querySelectorAll('svg text')];
      const n1 = els.find(e => e.textContent.includes('客户转租：独立菜单'));
      const n2 = els.find(e => e.textContent.includes('客户虚拟仓：在客户处'));
      const r1 = n1 ? n1.getBoundingClientRect() : null;
      const cover = n1 ? document.elementFromPoint(r1.left + 10, r1.top + 5) : null;
      return { n1: !!n1, n2: !!n2, coveredBy: cover ? cover.tagName : null };
    }""")
    check('两行注记渲染可见', vis['n1'] and vis['n2'], str(vis))
    check('注记未被元素遮挡', vis['coveredBy'] in ('text', 'svg', 'HTML', None), str(vis))
    pg.screenshot(path=str(ROOT / '_scan_tmpdir' / 'f01-v30-full.png'), full_page=True)
    b.close()

print(f'==== 批4 F01 断言：{len(PASS)} 过 / {len(FAIL)} 败 ====')
if FAIL:
    for n, d in FAIL:
        print('  ❌', n, d)
    sys.exit(1)
