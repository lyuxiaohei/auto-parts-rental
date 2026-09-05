# -*- coding: utf-8 -*-
"""F01 v2.9 迭代：L1-L4 泳道「退租申请+退租入库」两节点压缩为一个虚线占位节点。
正则锚定 x/y 坐标精确替换（T1 泳道同 href 节点 x=230/400 y=846 不受影响），每处 assert 命中 1 次。"""
import re
from pathlib import Path

F01 = Path(r"P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图.html")
A04 = Path(r"P3-R01-包装租赁管理后台原型/P3-R01-A04-流程链标注数据.json")
src = F01.read_text(encoding="utf-8")

def sub1(pat, repl, label):
    global src
    new, n = re.subn(pat, repl, src)
    assert n == 1, f"[{label}] 命中 {n} != 1"
    src = new

def placeholder(x, w, y, sub_text):
    cx = x + w // 2
    return (
        f'    <a href="包装管理/退租申请列表.html">\n'
        f'      <rect x="{x}" y="{y}" width="{w}" height="56" rx="6" fill="#fafafa" stroke="#6b7280" stroke-width="1" stroke-dasharray="5,4"/>\n'
        f'      <text x="{cx}" y="{y+25}" fill="#111827" font-size="12.5" font-weight="600" font-family="\'Geist\',sans-serif" text-anchor="middle">退租</text>\n'
        f'      <text x="{cx}" y="{y+44}" fill="#6b7280" font-size="8.5" font-family="\'Geist Mono\',monospace" text-anchor="middle">{sub_text}</text>\n'
        f'    </a>\n'
    )

LANES = [  # (退租申请x, 退租入库x, y, 中间连线(x1,y,x2), 占位x, 占位w, 副标)
    (664, 820, 282, (804, 310, 820), 664, 296, "退租申请→退租入库 · 缺损核对 · 详见 T1"),   # L1
    (784, 908, 422, (896, 450, 908), 784, 236, "按 BOM 拆散 · 详见 T1 专项"),               # L2
    (664, 820, 562, (804, 590, 820), 664, 296, "退租申请→退租入库 · 整箱退回 · 详见 T1"),   # L3
    (784, 908, 702, (896, 730, 908), 784, 236, "拆散分流 · 详见 T1 专项"),                  # L4
]

for ax, ix, y, (lx1, ly, lx2), px, pw, sub in LANES:
    # 1) 退租申请块 → 占位节点
    sub1(rf'<a href="包装管理/退租申请列表\.html">\s*<rect x="{ax}" y="{y}"[\s\S]*?</a>\n',
         placeholder(px, pw, y, sub).replace("\\", "\\\\"), f"L@y={y} 退租申请→占位")
    # 2) 退租入库块 → 删除
    sub1(rf'<a href="仓储作业/退租入库列表\.html">\s*<rect x="{ix}" y="{y}"[\s\S]*?</a>\n\s*', '', f"L@y={y} 退租入库删除")
    # 3) 中间连线删除
    sub1(rf'<line x1="{lx1}" y1="{ly}" x2="{lx2}" y2="{ly}" stroke="#4b5563" stroke-width="1" marker-end="url\(#arr\)"/>\n\s*', '', f"L@y={y} 连线删除")

# ── 配套文字
for old, new in [
    ("↩ 详见 L1 泳道", "↩ 属 L1 线"), ("↩ 详见 L2 泳道", "↩ 属 L2 线"),
    ("↩ 详见 L3 泳道", "↩ 属 L3 线"), ("↩ 详见 L4 泳道", "↩ 属 L4 线"),
    ("——各租赁线 退租申请→退租入库 独立成段'",
     "——各租赁线退租独立成段；v2.9 泳道内压缩为「退租」占位节点，完整四链路见 T1 专项'"),
    ("·T1 退租专项汇总四线）", "·T1 退租专项汇总四线·泳道内退租段压缩为占位节点）"),
]:
    assert src.count(old) == 1, f"锚点异常: {old[:30]!r} x{src.count(old)}"
    src = src.replace(old, new)

# ── 自检：配平 + 计数
for tag in ["a", "g", "svg", "text"]:
    o = len(re.findall(rf"<{tag}[\s>]", src)); c = src.count(f"</{tag}>")
    assert o == c, f"<{tag}> 配平失败 {o} vs {c}"
assert src.count(">退租</text>") == 4, src.count(">退租</text>")        # 4 个占位主标
assert src.count(">退租申请</text>") == 1                                # 仅 T1 公共入口
assert src.count(">退租入库</text>") == 1                                # 仅 T1 公共入口
baseline = Path(r"_scan_tmpdir/backup-v2.8-20260904/backup-F01-v2.9-t1.html").read_text(encoding="utf-8")
for probe in ["丢损赔偿", "丢损赔偿单", "租入归还", "分流归还", "租金应付", "多线应付", "在租台账", "组合出库", "租赁单"]:
    b, a = baseline.count(f">{probe}</text>"), src.count(f">{probe}</text>")
    assert a == b, f"下游节点计数变化: {probe} {b} -> {a}"
F01.write_text(src, encoding="utf-8", newline="")
print(f"F01 OK  {len(src)} chars")

# ── A04 json：仅 3 处备注字符串
j = A04.read_text(encoding="utf-8")
import json
pins_before = len(json.loads(j).get("pins", json.loads(j).get("标注", []))) if False else None
for old, new in [
    ("v2.8（5 主线 + 7 支线，唯一流程口径维护处）", "v2.9（6 主线含 T1 退租专项 + 7 支线，唯一流程口径维护处）"),
    ("F01 v2.8 起 L4 泳道补画本环节（09-04 王琳总：退租入库单独拆出），单据本就独立。",
     "F01 v2.8 起 L4 泳道补画本环节（09-04 王琳总：退租入库单独拆出），单据本就独立。v2.9 起 L1-L4 泳道退租段压缩为占位节点，完整链路见 T1 专项。"),
    ("步骤分母为该流程在 F01 中的节点总数", "步骤分母为该流程在 F01 v2.8 全展开泳道中的节点总数（v2.9 退租段压缩为占位，分母不变）"),
]:
    assert j.count(old) == 1, f"A04 锚点异常: {old[:30]!r} x{j.count(old)}"
    j = j.replace(old, new)
data = json.loads(j)  # 合法性校验
A04.write_text(j, encoding="utf-8", newline="")
print(f"A04 OK  json 合法，顶层键: {list(data.keys())[:6]}")
