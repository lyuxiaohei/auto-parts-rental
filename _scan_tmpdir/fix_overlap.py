# -*- coding: utf-8 -*-
"""F01 修复：T1 块整体 +56 下移（simplify_t1 重写时漏算 L4 双线加高的 56px，致 T1 标题压 L4 节点）。
viewBox 1454→1510，财务通道 7 处 +56。"""
import re
from pathlib import Path

F01 = Path(r"P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图.html")
src = F01.read_text(encoding="utf-8")

def rep(old, new, n=1):
    global src
    c = src.count(old)
    assert c == n, f"anchor {c}!={n}: {old[:60]!r}"
    src = src.replace(old, new)

# ── 1. T1 块整体 y+56（起=注释行，止=T1 底分隔线 y=1318）
start = '    <!-- T1 退租专项泳道（v2.9：09-05 道远裁定'
end = '    <line x1="40" y1="1318" x2="1240" y2="1318" stroke="rgba(17,24,39,0.06)" stroke-width="1"/>\n'
i, j = src.find(start), src.find(end)
assert i != -1 and j != -1 and i < j, (i, j)
block = src[i:j]
n_y = len(re.findall(r'y="\d+"', block))
block = re.sub(r'y="(\d+)"', lambda m: f'y="{int(m.group(1)) + 56}"', block)
# 干路 path 起点与终点
assert block.count('M 550 874 H 572 V 1302') == 1
block = block.replace('M 550 874 H 572 V 1302', 'M 550 930 H 572 V 1358')
src = src[:i] + block + src[j:]
rep('<line x1="40" y1="1318" x2="1240" y2="1318"', '<line x1="40" y1="1374" x2="1240" y2="1374"')

# ── 2. viewBox 1454→1510；财务通道 7 处 +56
rep('viewBox="0 0 1280 1454"', 'viewBox="0 0 1280 1510"')
for old, new in [
    ('<rect x="40" y="1330"', '<rect x="40" y="1386"'),
    ('<rect x="1124" y="1343"', '<rect x="1124" y="1399"'),
    ('<text x="1174" y="1356"', '<text x="1174" y="1412"'),
    ('<text x="58" y="1356" fill="#1f2937" font-size="13"', '<text x="58" y="1412" fill="#1f2937" font-size="13"'),
    ('<text x="58" y="1384"', '<text x="58" y="1440"'),
    ('<text x="58" y="1410"', '<text x="58" y="1466"'),
    ('<text x="58" y="1434"', '<text x="58" y="1490"'),
]:
    rep(old, new)

# ── 3. 自检：配平 + T1 标题新位置 + 与 L4 无重叠（y 层面）
for tag in ["a", "g", "svg", "text"]:
    o = len(re.findall(rf"<{tag}[\s>]", src)); c = src.count(f"</{tag}>")
    assert o == c, f"<{tag}> 配平失败 {o} vs {c}"
assert 'T1 · 租赁 · 退租专项' in src
t1_title_y = int(re.search(r'<text x="40" y="(\d+)"[^>]*>T1 · 租赁 · 退租专项', src).group(1))
l4_node_bottom = 824
assert t1_title_y - 14 > l4_node_bottom, f"T1 标题仍与 L4 节点重叠: {t1_title_y}"
print(f"T1 标题 y={t1_title_y}（L4 节点底 824，间距 {t1_title_y-14-824}px）✓")
F01.write_text(src, encoding="utf-8", newline="")
print(f"F01 OK（T1 块 {n_y} 处 y 坐标 +56）")
