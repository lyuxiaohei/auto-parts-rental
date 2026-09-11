# -*- coding: utf-8 -*-
"""G15 T3 · 主 SVG 图例改两行 + viewBox 0 0 880 2184
图例行1 = 原 1-5 项（原位不动，右缘 ~728）；行2 = 原 6-9 项（决策备注/库存缓冲/跨泳道交棒/📎）y+16 重排自 x=120。"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

F = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\P3-R01-F01-业务流程导航图.html')
t = open(F, encoding='utf-8', newline='').read()

def rep(old, new, n=1, label=''):
    global t
    c = t.count(old)
    if c == 0 and new in t:
        print(f'  [幂等跳过] {label}')
        return
    assert c == n, f'ASSERT FAIL [{label}]: count={c} expect={n}'
    t = t.replace(old, new)
    print(f'  OK [{label}] ×{c}')

M = ' fill="#4b5563" font-size="8" font-family="\'Geist Mono\',monospace">'
# 图例项6 决策备注
rep('<rect x="784" y="2138" width="16" height="12" rx="4" fill="rgba(17,24,39,0.02)" stroke="#d1d5db" stroke-width="0.8" stroke-dasharray="4,3"/>',
    '<rect x="120" y="2154" width="16" height="12" rx="4" fill="rgba(17,24,39,0.02)" stroke="#d1d5db" stroke-width="0.8" stroke-dasharray="4,3"/>', 1, '图例6框→(120,2154)')
rep(f'<text x="804" y="2148"{M}决策备注</text>',
    f'<text x="140" y="2164"{M}决策备注</text>', 1, '图例6文→(140,2164)')
# 图例项7 库存缓冲（蓝虚线）
rep('<line x1="876" y1="2144" x2="892" y2="2144" stroke="#2563eb" stroke-width="1" stroke-dasharray="5,4" marker-end="url(#arr-blue)"/>',
    '<line x1="200" y1="2160" x2="216" y2="2160" stroke="#2563eb" stroke-width="1" stroke-dasharray="5,4" marker-end="url(#arr-blue)"/>', 1, '图例7线→(200,2160)')
rep(f'<text x="900" y="2148"{M}库存缓冲 · 非顺序衔接</text>',
    f'<text x="224" y="2164"{M}库存缓冲 · 非顺序衔接</text>', 1, '图例7文→(224,2164)')
# 图例项8 跨泳道交棒（灰虚线）
rep('<line x1="1020" y1="2144" x2="1036" y2="2144" stroke="#4b5563" stroke-width="1" stroke-dasharray="5,4" marker-end="url(#arr)"/>',
    '<line x1="340" y1="2160" x2="356" y2="2160" stroke="#4b5563" stroke-width="1" stroke-dasharray="5,4" marker-end="url(#arr)"/>', 1, '图例8线→(340,2160)')
rep(f'<text x="1044" y="2148"{M}跨泳道交棒</text>',
    f'<text x="364" y="2164"{M}跨泳道交棒</text>', 1, '图例8文→(364,2164)')
# 图例项9 📎
rep(f'<text x="1140" y="2148"{M}📎 = 会议依据弹窗</text>',
    f'<text x="440" y="2164"{M}📎 = 会议依据弹窗</text>', 1, '图例9文→(440,2164)')
# 主 viewBox
rep('<svg viewBox="0 0 1280 2168"', '<svg viewBox="0 0 880 2184"', 1, '主viewBox→880×2184')

open(F, 'w', encoding='utf-8', newline='').write(t)
print('T3 写盘完成')
