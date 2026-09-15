# -*- coding: utf-8 -*-
"""逐行深度曲线，定位 付款新建 多余闭合标签"""
import io, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'


def depth_map(path, lo, hi):
    s = io.open(path, encoding='utf-8', newline='').read()
    lines = s.split('\n')
    d = 0
    out = []
    for idx, ln in enumerate(lines[:hi], start=1):
        opens = len(re.findall(r'<div(?:\s[^>]*)?>', ln))
        closes = len(re.findall(r'</div>', ln))
        d += opens - closes
        if idx >= lo:
            out.append((idx, d, opens, closes, ln.strip()[:70]))
    return out


print('===== 付款新建（可疑）=====')
for idx, d, o, c, t in depth_map(ROOT + '\\财务协同\\付款新建.html', 344, 392):
    flag = '  <<<' if (o or c) and t else ''
    print('%4d d=%-3d (+%d/-%d) %s%s' % (idx, d, o, c, t, flag))
print()
print('===== 应付新建（正常·对照）=====')
for idx, d, o, c, t in depth_map(ROOT + '\\财务协同\\应付新建.html', 344, 396):
    flag = '  <<<' if (o or c) and t else ''
    print('%4d d=%-3d (+%d/-%d) %s%s' % (idx, d, o, c, t, flag))
