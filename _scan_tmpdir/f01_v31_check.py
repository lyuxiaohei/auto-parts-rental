# -*- coding: utf-8 -*-
"""G06-F01 v3.1 几何与一致性断言（合并命令 T1 验证门）。只读；基线=backup 内 F01 v3.0 原版。"""
import re, os
from urllib.parse import unquote
from itertools import combinations

ROOT = r"P3-R01-包装租赁管理后台原型"
F01 = os.path.join(ROOT, "P3-R01-F01-业务流程导航图.html")
BASE = r"_scan_tmpdir/backup-menuregroup32-20260909/F01-v3.0-原版.html"

t = open(F01, "rb").read().decode("utf-8")
tb = open(BASE, "rb").read().decode("utf-8")

results = []
def chk(name, ok, detail=""):
    results.append((name, ok, detail))

# ---- 取第一个 svg（主线泳道，viewBox 0 0 1280 1618）----
def main_svg(s):
    m = re.search(r'<svg viewBox="0 0 1280 1618".*?</svg>', s, re.S)
    return m.group(0)
sv, svb = main_svg(t), main_svg(tb)

RECT = re.compile(r'<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"')
def rects(s):
    return [(int(a), int(b), int(c), int(d)) for a, b, c, d in RECT.findall(s)]
def overlaps(rr):
    out = set()
    for (x1, y1, w1, h1), (x2, y2, w2, h2) in combinations(rr, 2):
        if x1 < x2 + w2 and x2 < x1 + w1 and y1 < y2 + h2 and y2 < y1 + h1:
            out.add(((x1, y1, w1, h1), (x2, y2, w2, h2)))
    return out

A_BLOCK = re.compile(r'<a href="([^"]+)">\s*<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"[^>]*?(fill="[^"]*")[^>]*/>\s*<text [^>]*>([^<]+)</text>\s*<text [^>]*fill="([^"]*)"[^>]*>([^<]+)</text>\s*</a>', re.S)
blocks = A_BLOCK.findall(sv)

# ---- 断言 1-4：四线库存节点存在（主标「库存」+ C 表写死副标 + B1 同构蓝样式 + href 库存查询）----
EXPECT = [
    ("L1 库存节点", 352, 282, 140, "自有在库"),
    ("L2 库存节点", 288, 422, 112, "自有在库·组合前"),
    ("L3 库存节点", 352, 562, 140, "租入在库"),
    ("L4 库存节点", 336, 768, 112, "自有+租入在库"),
]
for name, x, y, w, sub in EXPECT:
    hit = [b for b in blocks if int(b[1]) == x and int(b[2]) == y and int(b[3]) == w
           and b[6] == "库存" and b[8] == sub and b[5] == 'fill="rgba(37,99,235,0.08)"' and "库存查询.html" in b[0]]
    chk(name, len(hit) == 1, f"rect({x},{y},w{w}) 主标=库存 副标={sub} 蓝样式 href=仓储作业/库存查询.html")

# ---- 断言 5-8：连线经停库存且端点对齐 0 偏差（箭头 x1=前节点右缘 / x2=后节点左缘 / y=节点中线）----
LINE = re.compile(r'<line x1="(\d+)" y1="(\d+)" x2="(\d+)" y2="(\d+)"')
def lines_at(s, y):
    got = []
    for m in LINE.finditer(s):
        if int(m.group(2)) == y:
            got.append((int(m.group(1)), int(m.group(3))))
    return sorted(got)

def lane_ok(y, nodes):
    """nodes=[(x,w)] 按序；返回箭头是否逐段精确衔接。"""
    got = lines_at(sv, y)
    want = sorted((nodes[i][0] + nodes[i][1], nodes[i + 1][0]) for i in range(len(nodes) - 1))
    mid = [n for n in nodes]
    ys = set()
    return got == want

l1 = lane_ok(310, [(40, 140), (196, 140), (352, 140), (508, 140), (664, 140)])
chk("L1 连线经停+端点对齐（采购入库→库存→租赁单→租赁出库，4 箭头 0 偏差）", l1, f"arrows={lines_at(sv,310)}")
l2 = lane_ok(450, [(40, 112), (164, 112), (288, 112), (412, 112), (536, 112), (660, 112), (784, 112)])
chk("L2 连线经停+端点对齐（采购入库→库存→BOM→按BOM租赁出库→租赁单→租赁出库，6 箭头）", l2, f"arrows={lines_at(sv,450)}")
l3 = lane_ok(590, [(40, 140), (196, 140), (352, 140), (508, 140), (664, 140)])
chk("L3 连线经停+端点对齐（租入入库→库存→租赁单→租赁出库，4 箭头）", l3, f"arrows={lines_at(sv,590)}")
want4 = sorted([(336 + 112, 460), (460 + 112, 584), (584 + 112, 708)])
got4 = lines_at(sv, 796)
l4 = all(w in got4 for w in want4) and got4 == sorted(want4 + [(152, 164)])  # (152,164)=租入线喂入箭头
p41 = 'd="M 276 728 H 306 V 788 H 336"' in sv   # 采购入库→（折线）→库存
p42 = 'd="M 276 796 H 336"' in sv               # 租入入库→库存
chk("L4 连线经停+端点对齐（双入库折线汇聚库存→混合组装→租赁单→租赁出库）", l4 and p41 and p42,
    f"arrows={lines_at(sv,796)} path1={p41} path2={p42}")

# ---- 断言 9：零重叠（新增节点与既有盒零新增重叠；既有装饰性重叠豁免不动）----
ov_before, ov_after = overlaps(rects(svb)), overlaps(rects(sv))
new_ov = ov_after - ov_before
chk("零重叠·新增 0（相对 v3.0 基线）", len(new_ov) == 0,
    f"v3.0 装饰性重叠 {len(ov_before)} 处（豁免不动）→ v3.1 {len(ov_after)} 处，新增 {len(new_ov)} 处")
chk("既有豁免不动（v3.0 重叠对在 v3.1 仍成立或因节点右移消除，未新增）", len(new_ov) == 0,
    f"豁免基数={len(ov_before)}")

# ---- 断言 10：死链 0（F01 全部 href 解析存在；外链 http 豁免）----
hrefs = re.findall(r'href="([^"]+)"', t)
dead = []
for h in hrefs:
    if h.startswith(("http", "#", "javascript:")):
        continue
    if not os.path.exists(os.path.join(ROOT, unquote(h))):
        dead.append(h)
chk("死链 0", len(dead) == 0, f"内链 {len(hrefs)} 条全解析，dead={dead}")

# ---- 断言 11：标签/叙事层 组合出库 0（href 路径串除外，逐形态）----
no_href = re.sub(r'<a href="[^"]*">', '', t)
no_href = re.sub(r'href="[^"]*"', '', no_href)
chk("标签与叙事层「组合出库」0 处", no_href.count("组合出库") == 0,
    f"href 保留形态：组合出库列表.html×{t.count('组合出库列表.html')} + 组合出库录单.html×{t.count('组合出库录单.html')}（均路径串）")
chk("href 组合出库列表.html 8 处保留", t.count('组合出库列表.html') == 8, "文件名零移动")

# ---- 断言 12-13：术语与版本 ----
chk("「租赁出库」≥16 处", t.count("租赁出库") >= 16, f"实际 {t.count('租赁出库')} 处")
chk("v3.1 字样 ≥1（v3.0 历史句保留 3 处）", t.count("v3.1") >= 1 and t.count("v3.0") == 3,
    f"v3.1={t.count('v3.1')} v3.0(历史)={t.count('v3.0')}")

# ---- 汇总 ----
fails = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + (" ｜ " + detail if detail else ""))
print(f"\n==== F01 v3.1 几何断言：{len(results)} 项全过，失败 {len(fails)} ====" if not fails
      else f"\n==== F01 v3.1 几何断言：{len(results) - len(fails)}/{len(results)} 过，失败 {len(fails)} ====")
