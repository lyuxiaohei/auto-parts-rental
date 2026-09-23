# -*- coding: utf-8 -*-
"""三点菜单（⋮ 折叠）按钮丢失审计（只读）：
丢失A：detail 类 op 落池位≥4 → 折进 ⋮ 后 tbody 委托够不着 → 点击无反应
丢失B：同页多 renderListPage 实例 → __opMenuHost 被后者覆盖 → 前列表 ⋮ 全哑"""
import io, sys, json, re, subprocess
from pathlib import Path

ROOT = (Path(__file__).resolve().parents[1] / "P3-R01-包装租赁管理后台原型")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BRIDGE = r"""
const fs = require('fs');
global.window = {};
eval(fs.readFileSync(process.argv[2], 'utf8'));
const D = window.DEMO_DATA;
const out = {};
for (const [ent, recs] of Object.entries(D)) {
  if (typeof recs !== 'object' || recs === null) continue;
  const pool = []; const detailOps = {}; const rowCnt = {};
  for (const [k, rec] of Object.entries(recs)) {
    if (!rec || !rec.row) continue;
    (rec.row.ops || []).forEach(o => {
      if (pool.indexOf(o.t) < 0) pool.push(o.t);
      if (o.detail && !detailOps[o.t]) detailOps[o.t] = 0;
      if (o.detail) detailOps[o.t]++;
    });
    rowCnt[k] = (rec.row.ops || []).length;
  }
  if (pool.length) out[ent] = { pool: pool, detail: detailOps };
}
fs.writeFileSync(process.argv[3], JSON.stringify(out), 'utf8');
console.log('ok');
"""
tmp = Path(__file__).resolve().parent / "opmenu_dump.js"
tmp.write_text(BRIDGE, encoding="utf-8")
dumppath = Path(__file__).resolve().parent / "opmenu_dump.json"
subprocess.run(["node", str(tmp), str(ROOT / "_data" / "demo-data.js"), str(dumppath)],
               capture_output=True, text=True)
entdata = json.loads(dumppath.read_text(encoding="utf-8"))

loss_a, multi = [], []
for p in sorted(ROOT.rglob("*.html")):
    rel = p.relative_to(ROOT)
    if rel.parts[0] in ("mobile", "P3-R01-F01-业务流程导航图"):
        continue
    html = p.read_text(encoding="utf-8")
    # 页内全部 renderListPage 调用的 entity 与 opsTop
    calls = []
    for m in re.finditer(r"renderListPage\(\{(.{0,2500}?)\n\s*\}\)", html, re.S):
        seg = m.group(1)
        em = re.search(r"entity:\s*'([^']+)'", seg)
        ot = re.search(r"opsTop:\s*\[([^\]]*)\]", seg)
        if em:
            tops = re.findall(r"'([^']+)'", ot.group(1)) if ot else []
            calls.append((em.group(1), tops))
    if not calls:
        continue
    if len(calls) > 1:
        multi.append((str(rel), calls))
    for ent, tops in calls:
        info = entdata.get(ent)
        if not info:
            continue
        pool = list(info["pool"])
        for t in tops:                      # 模拟 opsTop 钉前缀
            if t in pool:
                pool.remove(t); pool.insert(0, t)
        for t, cnt in info["detail"].items():
            pos = pool.index(t) + 1 if t in pool else None
            if pos and pos >= 4:
                loss_a.append((str(rel), ent, t, pos, cnt, len(pool)))

print("=== 丢失A：detail 类按钮折进 ⋮（点击无反应）===")
for rel, ent, t, pos, cnt, plen in loss_a:
    print(f"  {rel} | {ent} | 「{t}」池位 {pos}/{plen}（{cnt} 行使用·detail:true）")
print("合计:", len(loss_a), "处")
print()
print("=== 丢失B 候选：同页多 renderListPage 实例（host 覆盖·前列表 ⋮ 全哑）===")
for rel, calls in multi:
    print(f"  {rel} | " + " + ".join(e for e, _ in calls))
print("合计:", len(multi), "页")
tmp.unlink()
