# -*- coding: utf-8 -*-
"""菜单重组方案 B · 任务三：A04 标注数据键名替换
- 键 `包装管理/租赁单列表.html` → `销售管理/租赁单列表.html`（1 处）
- 其余 `包装管理/` 键 → `租赁管理/`（4 处：退租申请列表/丢损赔偿单/租出台账/在租台账）
- 读取-精确替换+assert；json.load 校验；pin note 路径文字核查（此前已查为 0）"""
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJ = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
JP = PROJ / "P3-R01-包装租赁管理后台原型" / "P3-R01-A04-流程链标注数据.json"

raw = JP.read_text(encoding="utf-8")

EDITS = [
    ('"包装管理/租赁单列表.html"', '"销售管理/租赁单列表.html"'),
    ('"包装管理/退租申请列表.html"', '"租赁管理/退租申请列表.html"'),
    ('"包装管理/丢损赔偿单.html"', '"租赁管理/丢损赔偿单.html"'),
    ('"包装管理/租出台账.html"', '"租赁管理/租出台账.html"'),
    ('"包装管理/在租台账.html"', '"租赁管理/在租台账.html"'),
]
for old, new in EDITS:
    c = raw.count(old)
    assert c == 1, f"键 {old} 出现 {c} 次（应为 1）"
    raw = raw.replace(old, new)
    print(f"OK 键替换 {old} → {new}")
assert "包装管理" not in raw, "A04 内仍残留 包装管理 字样"
JP.write_text(raw, encoding="utf-8", newline="")

# 校验：JSON 合法 + 结构断言
d = json.loads(JP.read_text(encoding="utf-8"))
pages = {k: v for k, v in d.items() if not k.startswith("_")}
pins = sum(len(v) for v in pages.values())
assert "销售管理/租赁单列表.html" in pages and len(pages["销售管理/租赁单列表.html"]) == 5
assert all(not k.startswith("包装管理") for k in pages)
print(f"VALID JSON：{len(pages)} 页 / {pins} 条 pin；销售管理/租赁单列表.html 5 条 ✓")
