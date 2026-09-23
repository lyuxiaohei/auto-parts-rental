# -*- coding: utf-8 -*-
"""全库单物料审计（只读）：各实体 items 每记录行数统计·找出只有 1 行物料的单据"""
import io, sys, json
from pathlib import Path

ROOT = (Path(__file__).resolve().parents[1] / "P3-R01-包装租赁管理后台原型")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 用 node 把 demo-data.js 转成 JSON 读取（借 run_script 桥·只读）
bridge = """
const fs = require('fs');
global.window = {};
const src = fs.readFileSync(process.argv[1], 'utf8');
eval(src);
const D = window.DEMO_DATA;
const out = {};
for (const [ent, recs] of Object.entries(D)) {
  if (typeof recs !== 'object') continue;
  const rows = [];
  for (const [key, rec] of Object.entries(recs)) {
    if (rec && Array.isArray(rec.items)) rows.push([key, rec.items.length, rec.items.map(i => Array.isArray(i) ? i[2] : '?').join('｜')]);
  }
  if (rows.length) out[ent] = rows;
}
console.log(JSON.stringify(out));
"""
import subprocess, tempfile
with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
    f.write(bridge); bridge_path = f.name
r = subprocess.run(["node", bridge_path, str(ROOT / "_data" / "demo-data.js")],
                   capture_output=True, text=True, encoding="utf-8")
data = json.loads(r.stdout)

total_single = total_rec = 0
for ent, rows in data.items():
    singles = [x for x in rows if x[1] == 1]
    multis = [x for x in rows if x[1] > 1]
    total_rec += len(rows); total_single += len(singles)
    flag = "  ← 全部单物料" if singles and not multis else ""
    print("[%s] %d 单：%d 单物料 / %d 多物料%s" % (ent, len(rows), len(singles), len(multis), flag))
    for key, n, mats in multis:
        print("    多物料 %s（%d 行：%s）" % (key, n, mats))
print("\n合计：%d 实体 · %d 张单 · 单物料 %d 张（%.0f%%）" %
      (len(data), total_rec, total_single, 100.0 * total_single / max(total_rec, 1)))
Path(bridge_path).unlink()
