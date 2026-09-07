# -*- coding: utf-8 -*-
"""从 P3-R01-F01 提取绘图信息 → JSON（供生成 md 规格）"""
import re, json
from pathlib import Path

SRC = Path(r'P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图.html')
s = SRC.read_text(encoding='utf-8')

out = {}

# ── 1. 文档与画布 ──
out['title'] = re.search(r'<h1[^>]*>([^<]+)</h1>', s).group(1).strip()
sub = re.search(r'<div class="sub">( [\s\S]*?)</div>', s)
out['sub_raw'] = re.sub(r'<[^>]+>', '', sub.group(1)).strip() if sub else ''
svgs = re.findall(r'<svg[^>]*viewBox="([\d .]+)"[^>]*>', s)
out['svg_viewboxes'] = svgs
out['v_latest'] = re.findall(r'v2\.\d', out['title'] + out['sub_raw'])

# ── 2. 泳道标题（含区域名） ──
lanes = []
for m in re.finditer(r'<text[^>]*font-size="1[34]"[^>]*>((?:<b>)?[A-Z]\d(?:</b>)? [·•][^<]*)</text>', s):
    lanes.append({'y': int(re.search(r'y="(\d+)"', m.group(0)).group(1)),
                  'title': re.sub(r'</?b>', '', m.group(1)).strip()})
out['lane_titles'] = lanes

# ── 3. 全部可点节点 <a href> ──
nodes = []
for m in re.finditer(r'<a href="([^"]+)">\s*<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"( rx="(\d+)")? fill="([^"]+)"(?: stroke="([^"]+)"(?: stroke-width="([\d.]+)")?(?: stroke-dasharray="([^"]+)")?)?[^/]*/>\s*<text[^>]*y="([\d.]+)"[^>]*fill="([^"]+)" font-size="([\d.]+)"[^>]*>([^<]+)</text>(?:\s*<text[^>]*fill="([^"]+)" font-size="([\d.]+)"[^>]*>([^<]*)</text>)?', s):
    (href, x, y, w, h, _rx_tag, rx, fill, stroke, sw, dash, ty1, tfill1, fs1, t1, tfill2, fs2, t2) = m.groups()
    nodes.append({'href': href, 'x': float(x), 'y': float(y), 'w': float(w), 'h': float(h),
                  'rx': int(rx or 4), 'fill': fill, 'stroke': stroke, 'dash': dash or '',
                  'main': t1.strip(), 'sub': (t2 or '').strip(),
                  'fs_main': float(fs1), 'fs_sub': float(fs2 or 0)})
out['n_nodes'] = len(nodes)

# ── 4. src-tag 溯源 chip ──
out['src_tags'] = re.findall(r'class="src-tag"[^>]*onclick="showSrc\(\'(\w+)\'\)"', s)
out['src_data_keys'] = re.findall(r'^\s{2}(\w+): \{head:', s, re.M)

# ── 5. 样式 token 定量 ──
def cnt(pat):
    from collections import Counter
    return dict(Counter(re.findall(pat, s)).most_common())
out['fills'] = cnt(r'fill="(#[0-9a-fA-F]{3,6})"')
out['strokes'] = cnt(r'stroke="(#[0-9a-fA-F]{3,6})"')
out['font_sizes_svg'] = cnt(r'font-size="([\d.]+)"')
out['text_fills'] = cnt(r'<text[^>]*fill="(#[0-9a-fA-F]{3,6})"')
out['markers'] = re.findall(r'<marker id="([\w-]+)"', s)
out['marker_used'] = cnt(r'marker-end="url\(#([\w-]+)\)"')

json.dump({'meta': out, 'nodes': nodes}, open('_scan_tmpdir/f01_spec.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('节点数:', len(nodes), '| 泳道标题:', len(lanes), '| SRC_DATA 键:', out['src_data_keys'])
print('主标字号分布:', {k: v for k, v in out['font_sizes_svg'].items()})
