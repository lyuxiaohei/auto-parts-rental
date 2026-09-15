# -*- coding: utf-8 -*-
"""采购入库录单 内容区 div 深度追踪"""
import io, re, os

FP = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\采购管理\采购入库录单.html'
s = io.open(FP, encoding='utf-8', newline='').read()
lines = s.split('\n')
start = next(i for i, l in enumerate(lines) if '<div class="content' in l)
d = 0
for i in range(start, min(len(lines), start + 170)):
    l = lines[i].replace('\r', '')
    o = len(re.findall(r'<div(?:\s[^>]*)?>', l))
    c = len(re.findall(r'</div>', l))
    d += o - c
    t = l.strip()
    if t and (o or c):
        print('%4d d=%-3d (+%d/-%d) %s' % (i + 1, d, o, c, t[:100]))
