# -*- coding: utf-8 -*-
"""G56 F01 v3.9 结构验证：标签配平 / viewBox 边界 / line-vs-rect 对齐 / href 存在 / 关键串 grep"""
import re, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
P3 = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型')
F01 = os.path.join(P3, 'P3-R01-F01-业务流程导航图.html')
src = open(F01, encoding='utf-8').read()
fails = []

def check(name, ok, detail=''):
    print(('[PASS] ' if ok else '[FAIL] ') + name + ('  -- ' + detail if detail else ''))
    if not ok: fails.append(name)

# 1) 标签配平
for tag in ['svg', 'a', 'g', 'text', 'defs', 'details', 'div', 'script', 'style']:
    o = len(re.findall(r'<%s(?:\s|>)' % tag, src))
    c = src.count('</%s>' % tag)
    check('tag balance <%s> %d/%d' % (tag, o, c), o == c, '%d open %d close' % (o, c))
# rect/line/path 自闭合计数
for tag in ['rect', 'line', 'path']:
    o = len(re.findall(r'<%s[\s/]' % tag, src))
    c = len(re.findall(r'<%s[^>]*/>' % tag, src))
    check('self-closing <%s> %d/%d' % (tag, o, c), o == c)

# 2) 双 svg 切分与 viewBox
mains = re.findall(r'<svg viewBox="([^"]+)"', src)
check('viewBox count=2', len(mains) == 2, str(mains))
main_vb = [float(x) for x in mains[0].split()]
sub_vb = [float(x) for x in mains[1].split()]
check('main viewBox 0 0 880 2584', mains[0] == '0 0 880 2584', mains[0])
check('sub viewBox 0 0 880 944', mains[1] == '0 0 880 944', mains[1])
main_svg = src[src.index(mains[0]) - 10: src.index('id="p3r01f01-sub-title"')]
sub_svg = src[src.index('id="p3r01f01-sub-title"') - 200:]

def max_geom(seg):
    ys = [float(v) for v in re.findall(r'\by="([\d.]+)"', seg)]
    ys += [float(v) for v in re.findall(r'\by1="([\d.]+)"', seg)]
    ys += [float(v) for v in re.findall(r'\by2="([\d.]+)"', seg)]
    for d in re.findall(r'\bd="([^"]+)"', seg):
        ys += [float(t) for t in re.findall(r'[Vv]\s*(-?[\d.]+)', d)]
        for t in re.findall(r'[Qq]\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)', d):
            ys.append(float(t[1])); ys.append(float(t[3]))
        for t in re.findall(r'[MmLlHh]\s+(-?[\d.]+)[ ,]+(-?[\d.]+)', d):
            ys.append(float(t[1]))
    return max(ys)

mmax = max_geom(main_svg); smax = max_geom(sub_svg)
check('main maxY<=2568 (vb 2584-16)', mmax <= 2568, 'maxY=%.0f' % mmax)
check('sub maxY<=928 (vb 944-16)', smax <= 928, 'maxY=%.0f' % smax)
check('main maxY>=2500 (legend present)', mmax >= 2500, 'maxY=%.0f' % mmax)

# 3) line-vs-rect 对齐断言（行中心 = rect.y + 28）
rects = [(float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)))
         for m in re.finditer(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"', main_svg)]
node_rows = sorted({round(r[1]) for r in rects if r[3] == 56})
EXP_ROWS = [116, 216, 308, 408, 536, 636, 764, 864, 992, 1092, 1200, 1280, 1428, 1504, 1624, 1752, 1826, 1902, 1978, 2112, 2320, 2408]
check('56h node rows expected', node_rows == EXP_ROWS, str(node_rows))
lines_y = {float(m.group(1)) for m in re.finditer(r'<line x1="[\d.]+" y1="([\d.]+)" x2="[\d.]+" y2="[\d.]+"[^>]*marker-end', main_svg)}
bad = [y for y in lines_y if y < 2500 and not any(abs(y - (row + 28)) < 0.01 for row in EXP_ROWS)]
check('arrow lines align row centers', not bad, 'offenders=%s' % bad)
# 分隔线位置
seps = sorted(float(m.group(1)) for m in re.finditer(r'<line x1="40" y1="([\d.]+)" x2="840" y2="[\d.]+" stroke="rgba\(17,24,39,0.10\)" stroke-width="1"/>', main_svg))
check('lane separators', seps == [488.0, 716.0, 944.0, 1380.0, 1704.0, 2058.0, 2264.0], str(seps))
# 蓝色虚线 path 三条新坐标
for pat in ['M 422 592 V 614 H 266 V 636', 'M 422 820 V 842 H 266 V 864', 'M 422 1048 V 1070 H 266 V 1092',
            'M 446 1560 V 1592 H 170 V 1624', 'M 752 2034 V 2096 H 110 V 2112', 'M 336 1780 H 356 Q 364 1780 364 1788 V 2006']:
    check('path %s' % pat, pat in main_svg)

# 4) href 门
hrefs = re.findall(r'href="([^"]*\.html)"', src)
uniq = sorted(set(hrefs))
missing = [h for h in uniq if not os.path.exists(os.path.join(P3, h))]
check('href targets all exist (%d uniq)' % len(uniq), not missing, 'missing=%s' % missing)
for must in ['采购管理/采购退货单列表.html', '销售管理/销售退货单列表.html', '财务协同/退款登记.html',
             '租入管理/租入单列表.html', '租入管理/租入入库列表.html', '租入管理/归还出库列表.html']:
    check('new href present: %s' % must, must in uniq)

# 5) grep 门（文本层·title/sub/footer 更新前先看关键串）
def cnt(s): return src.count(s)
for kw, mn in [('v3.9', 4), ('直发', 5), ('背靠背', 2), ('XNC-ZF', 1), ('采购退货', 2), ('销售退货', 2), ('退款', 3), ('报数', 1), ('QTRK-004', 1), ('KW-05', 1)]:
    check('grep %s >= %d' % (kw, mn), cnt(kw) >= mn, 'count=%d' % cnt(kw))
for kw, exp in [('v3.8 原型业务流程导航', 0), ('67 个弹窗', 0), ('38 个页面', 0), ('38 页 /', 0), ('Geist', 0)]:
    check('grep %s == 0' % kw, cnt(kw) == exp, 'count=%d' % cnt(kw))

print('\nTOTAL: %d PASS / %d FAIL' % (sum(1 for _ in range(0)) , len(fails)) if False else '')
print('SUMMARY: %d FAIL -> %s' % (len(fails), fails) if fails else 'ALL PASS')
