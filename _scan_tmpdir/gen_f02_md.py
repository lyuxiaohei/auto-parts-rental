# -*- coding: utf-8 -*-
"""生成 P1-R03-F02-业务流程导航图绘图信息.md"""
import re, json
from pathlib import Path

ROOT = Path('.')
SRC = ROOT / 'P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图.html'
s = SRC.read_text(encoding='utf-8')

# 切分主 SVG / 支线 SVG
svg_spans = [m.start() for m in re.finditer(r'<svg', s)]
main_svg, branch_svg = s[:svg_spans[1]], s[svg_spans[1]:]

NODE_RE = re.compile(
    r'<a href="([^"]+)">\s*<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"(?: rx="(\d+)")? '
    r'fill="([^"]+)"(?: stroke="([^"]+)"(?: stroke-width="([\d.]+)")?(?: stroke-dasharray="([^"]+)")?)?[^/]*/>\s*'
    r'<text[^>]*y="[\d.]+"[^>]*fill="(#[0-9a-f]+)" font-size="([\d.]+)"[^>]*>([^<]+)</text>'
    r'(?:\s*<text[^>]*fill="(#[0-9a-f]+)" font-size="([\d.]+)"[^>]*>([^<]*)</text>)?')

def extract(part):
    ns = []
    for m in NODE_RE.finditer(part):
        href, x, y, w, h, rx, fill, stroke, sw, dash, tf1, fs1, t1, tf2, fs2, t2 = m.groups()
        ns.append({'href': href, 'x': float(x), 'y': float(y), 'w': float(w), 'h': float(h),
                   'rx': int(rx or 4), 'fill': fill, 'stroke': stroke or '', 'dash': dash or '',
                   'main': t1.strip(), 'sub': (t2 or '').strip(), 'fs': float(fs1)})
    return ns

main_nodes, branch_nodes = extract(main_svg), extract(branch_svg)

# 分区定义（标题 y 起点 → 带域上界）
MAIN_BANDS = [('B1 · 零部件买卖', 64, 248), ('L1 · 租赁 · 单一出租', 266, 388),
              ('L2 · 租赁 · 组合出租', 406, 528), ('L3 · 租赁 · 租入转租', 546, 668),
              ('L4 · 租赁 · 混合转租', 686, 856), ('T1 · 租赁 · 客户退租', 882, 1210),
              ('T2 · 租赁 · 租入归还', 1210, 1450), ('财务通道 F1/F2', 1450, 1666)]
BRANCH_BANDS = [('S1 · 库存运营', 42, 162), ('S2 · 项目经营', 162, 282), ('S3 · 系统支撑', 282, 386),
                ('S4 · 赔偿转单据', 386, 522), ('S5 · 录单页与台账', 522, 642), ('S6 · 审核与待办', 642, 720)]

def box_style(n):
    if n['dash']: return '虚线框'
    if n['fill'] == '#2563eb': return '蓝底强调'
    if n['fill'] not in ('#ffffff', '#fff'): return '灰底入口'
    return '白底实体'

def lane_md(nodes, bands):
    out = []
    for name, lo, hi in bands:
        ns = sorted([n for n in nodes if lo <= n['y'] < hi], key=lambda n: (n['y'], n['x']))
        if not ns: continue
        out.append(f'\n#### {name}\n\n| 主标 | 副标 | 盒样式 | 跳转 | x,y | w×h |\n|---|---|---|---|---|---|\n')
        for n in ns:
            sub = n['sub'].replace('|', '\\|') if n['sub'] else '—'
            out.append(f"| {n['main']} | {sub} | {box_style(n)} | `{n['href']}` | {n['x']:.0f},{n['y']:.0f} | {n['w']:.0f}×{n['h']:.0f} |\n")
    return ''.join(out)

meta = json.load(open('_scan_tmpdir/f01_spec.json', encoding='utf-8'))['meta']

md = f'''# P1-R03-F02-业务流程导航图绘图信息

> 对象：`P3-R01-F01-业务流程导航图.html`（**v3.3**，2026-09-10 重提取同步·G08 退租专项拆分 T1 客户退租/T2 租入归还；本文档为该图的机读绘图规格，供后续 agent 读取后改图/重绘，不必逆向解析 SVG）。由 `extract_f01_spec.py` + `gen_f02_md.py` 自动提取生成（`_scan_tmpdir/`），手工叙述部分基于 P1-R05 交接文档；v3.0/v3.1/v3.2/v3.3 变更见第 8 节演进史。

## 1. 画布与文档结构

- 双 `<svg>`：**主线区** viewBox `0 0 1280 1666`；**支线区** viewBox `0 0 1280 720`（两区坐标系独立，y 值均从 0 起，不可跨区比较）
- 页面骨架（自上而下）：h1 标题 → 编号规则行 → 前置行（基础资料链接）→ 主线区（7 泳道 + 财务通道）→ 支线区（6 支线）→ 页脚版本叙事
- 全图可点节点 **{len(main_nodes) + len(branch_nodes)} 个**（主线区 {len(main_nodes)} + 支线区 {len(branch_nodes)}），另有约 15 个不可点 `<g>`（决策框、灰底 tag、注记）

## 2. 编号体系

`B 买卖 · L 租赁（L1 单一 / L2 组合 / L3 租入转租 / L4 混合）· T 退租/归还（T1 客户退租 / T2 租入归还） · F 财务（F1 应收 / F2 应付）· S 支撑支线`

各域职责：**泳道=正向链**（来料→组装→租出→出库即止），**T1=客户退租回程**（退租入库统一入口→核对二分→完好按归属回库，租入行交棒 T2），**T2=归还供应商**（租入归还独立事件·双入口=退租回库租入行＋未转租直还），**财务通道=5 条线共用**（B1 销售费 + L1~L4 租金 + 赔偿），**支线=支撑模块**。

## 3. 主线区节点清单（含财务通道）

## 4. 支线区节点清单

## 5. 样式规格（token 级）

### 5.1 颜色
| 用途 | 色值 | 出现次数（fill/text 合并口径） |
|---|---|---|
| 深墨（节点主文字/重底） | `#111827` | fill {meta['fills'].get('#111827', 0)} + text {meta['text_fills'].get('#111827', 0)} |
| 近黑（次级文字） | `#1f2937` / `#374151` | {meta['text_fills'].get('#1f2937', 0)} / {meta['text_fills'].get('#374151', 0)} |
| 中灰（副标） | `#4b5563` | stroke {meta['strokes'].get('#4b5563', 0)} + text {meta['text_fills'].get('#4b5563', 0)} |
| 灰（注记） | `#6b7280` | fill {meta['fills'].get('#6b7280', 0)} + text {meta['text_fills'].get('#6b7280', 0)} |
| 浅灰（弱注记） | `#9ca3af` | fill {meta['fills'].get('#9ca3af', 0)} + text {meta['text_fills'].get('#9ca3af', 0)} |
| 唯一强调色 | `#2563eb` | fill {meta['fills'].get('#2563eb', 0)} + stroke {meta['strokes'].get('#2563eb', 0)} + text {meta['text_fills'].get('#2563eb', 0)} |
| T1 标签浅蓝 | `#93c5fd` | stroke {meta['strokes'].get('#93c5fd', 0)} |
| 纸底/chip | `#fafafa` / `#ffffff` | {meta['fills'].get('#fafafa', 0)} / {meta['fills'].get('#ffffff', 0)} |
| 分隔线 | `rgba(17,24,39,0.06)` | 6 处横线 |

另含 alpha 灰 4 档（0.02/0.06/0.10/0.28）：0.10=灰底入口节点填充，0.28=遮罩等。**已知问题**：9 级灰阶无角色映射、蓝有 `#2563eb`/`#93c5fd` 两个色值（K3 视觉评审 09-06，详见第 7 节）。

### 5.2 字号（SVG 内 9 档）
| 字号 | 用途 | 处数 |
|---|---|---|
| 28/19 | 页面 h1/区标题（HTML 层） | — |
| 14 | 泳道标题 | {meta['font_sizes_svg'].get('14', 0)} |
| 12.5 | 节点主标 | {meta['font_sizes_svg'].get('12.5', 0)} |
| 13/11.5/11 | 财务标题/支线节点主标/T1 小节 | 各 {meta['font_sizes_svg'].get('13', 0)}/{meta['font_sizes_svg'].get('11.5', 0)}/{meta['font_sizes_svg'].get('11', 0)} |
| 9.5/10 | 支线副标 | {meta['font_sizes_svg'].get('9.5', 0)}/{meta['font_sizes_svg'].get('10', 0)} |
| 8.5 | 主线节点副标（最小） | {meta['font_sizes_svg'].get('8.5', 0)} |
| 9 | 页脚 | {meta['font_sizes_svg'].get('9', 0)} |

字重 4 档（400/500/600/700）；字族 `'Geist',sans-serif`（主标）+ `'Geist Mono',monospace`（副标/注记），均无中文字形回落系统黑体。

### 5.3 盒样式（6 种语义）
| 样式 | 规格 | 语义 |
|---|---|---|
| 白底实体 | fill `#fff` + stroke `#111827` 1px + rx6 | 可点页面节点 |
| 灰底入口 | fill `rgba(75,85,99,0.10)` + 灰描边 + rx6 | 进入下段流程的入口（入口节点原则） |
| 蓝底强调 | fill `#2563eb` + 白字 | 强调节点（库存/组装/循环） |
| 浅蓝框 tag | stroke `#93c5fd` 虚实线 | T1 归属标记（不可点） |
| 虚线灰框 | stroke-dasharray | 决策框 |
| chip | `#fafafa` + stroke `#c9cdd4` rx3 | src-tag 溯源便签 |

### 5.4 连线与 marker
- 箭头 marker 3 个：`arr`（黑主用）/`arr-soft`（未使用，死代码）/`arr-blue`（B1 库存缓冲回流专用）
- 主线箭头统一 1px `#4b5563`；已知问题：T1 纵向主干 path（`M400 930 H420 V1158`）无 marker 贯穿三个分支行，视觉如划痕

## 6. 数据源 SRC_DATA（溯源弹窗）

JS 对象 `SRC_DATA` 共 {len(meta['src_data_keys'])} 键：{', '.join('`' + k + '`' for k in meta['src_data_keys'])}。每个泳道标题左侧有 `📎 会议材料 ▸` src-tag（onclick=showSrc），点击弹出该泳道的决策溯源（含 09-04/09-05 会议原话引用）。改泳道来源叙事时同步改对应键的 head/points。

## 7. 已知视觉问题（2026-09-06 K3 视觉评审结论，未修）

1. 灰阶 9 级无角色映射、蓝色语义超载（强调/链接/拍板 pill/归属 tag 四义一色）
2. 最小字（8.5px ×98 处）承担副标信息，`#9ca3af` on `#fafafa` 对比度仅 ~2.9:1
3. 三套 Google Fonts 无中文字形，实际回落混合渲染；国内演示有加载风险
4. 主线区右侧 ~40% 留白、支线区过稀，两区密度气质不一致
5. 圆角三档（rx3/4/6）并存；灰底入口与白底实体投影不可辨
6. 30 分钟最小修清单（P0-1~P0-5：灰阶收敛/蓝色统一/去 📎/修 T1 主干线/h1 字族落地）留档于本节，执行前按 P1-R05 纪律走精确替换

## 8. 演进史摘要

v2.7（09-04 前基线）→ v2.8（B1 拆双线+库存桥、退租入库独立成段）→ v2.9（09-04~09-05 四轮：T1 退租专项新增 → 泳道退租段压缩为虚线占位 → T1 两段式+核对二分 → L4 双线并行 → 财务 F1/F2 节点化 → 入口节点原则去冗余 → 编号体系 S1-S6 规范化 → 赔偿核销注记）→ **v3.0**（09-08 会议改造：四模块移除·T1 删退租申请直连退租入库·丢损赔偿直建应收/应付·拆散拆卸改按零件入库·L2 组装改按 BOM 组合出库·F1/F2 四来源·运营方→供应商·客户虚拟仓/客户转租注记）→ **v3.1**（09-09 G06：租赁四线 L1~L4 各插「库存」节点与 B1 买卖线同构·标签层 组合出库→租赁出库[href 文件名零移动]；节点数 76→79）→ **v3.2**（09-10 G07：T1 重画退租两事件模型——入口改 租赁单「退租」[href 租赁单列表]、②完好按归属分流两路[自有→在库五态→循环再出租 / 租入→租入在库→租入归还→租金应付]、四路 L1-L4 分支与「↩ 属」注记取消、底部三行口径注记；L4「混合组装」节点改「组合 C·BOM 计算」[无组装单]；S5 租出台账节点改「退回进度」；S6 审核弹窗 18→15 类；节点数 79→74）→ **v3.3**（09-10 G08：退租专项拆分两条编号流程——T1 客户退租[止于回库：租入行末端改「⇢ T2 · 租入归还」交棒 chip，删 T1 内租入归还/租金应付两节点]／T2 租入归还[归还供应商独立事件·双入口=退租回库租入行＋未转租直还·租入在库→租入归还→租金应付]；L3/L4 跨泳道指引改「退租见 T1 · 租入归还见 T2」；SRC_DATA 7→8 键[+t2]；财务通道区 y≥1400 整体 +144，viewBox 1618→1762；节点数 74→76，泳道 6→7；同会话续改：T1 紧凑重排——节点间距统一 20px（原入口箭头 190px）·四行等行距 20px·①② 标签行内化·客户转租/客户虚拟仓两注记下移口径注记区·T2 块 −128/财务通道区 −96，T1 高 432→304，viewBox 1762→1666）。完整过程见 P1-R05 冻结版与 agent-handoff/ 各 G 文档。改图铁律：块内坐标位移必须覆盖 `y=`/`y1=`/`y2=`/path `d` 全部形式并跑 line-vs-rect 对齐断言。
'''

# 注入第 3/4 节表格
md = md.replace('## 3. 主线区节点清单（含财务通道）\n', '## 3. 主线区节点清单（含财务通道）\n' + lane_md(main_nodes, MAIN_BANDS))
md = md.replace('## 4. 支线区节点清单\n', '## 4. 支线区节点清单\n' + lane_md(branch_nodes, BRANCH_BANDS))

Path('P1-R03/P1-R03-F02-业务流程导航图绘图信息.md').write_text(md, encoding='utf-8')
print('已写入 P1-R03/P1-R03-F02-业务流程导航图绘图信息.md，行数:', md.count(chr(10)))
