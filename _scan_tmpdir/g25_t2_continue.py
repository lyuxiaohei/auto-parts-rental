# -*- coding: utf-8 -*-
"""G25 T2 续：核对已插入状态（键 2 次=键声明+fees 格属预期）+ 补跑库存查询 option"""
import io, subprocess

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
DD = ROOT + r"\_data\demo-data.js"
PG = ROOT + r"\仓储作业\库存查询.html"

t2 = io.open(DD, encoding="utf-8", newline="").read()
i = t2.find("stockFlows: {")
seg = t2[i:t2.find("/* ----", i + 20)]
assert t2.count("'RZRK-20260910-024': {") == 1, "键声明 %d 次" % t2.count("'RZRK-20260910-024': {")
assert seg.count('"status": "租入"') == 1, "租入态 %d 次" % seg.count('"status": "租入"')
assert seg.count("'RZRK-20260910-024'") == 2, "段内键串 %d 次（预期 2=声明+fees）" % seg.count("'RZRK-20260910-024'")
r = subprocess.run(["node", "--check", DD], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:300]
raw = open(DD, "rb").read()
print("PASS demo-data：键声明 1·status 租入 1·node --check 0·CRLF=%d 裸LF=%d" % (
    raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")))

pg = io.open(PG, encoding="utf-8", newline="").read()
old = "<option>退租待入库</option></select>"
new = "<option>退租待入库</option><option>租入</option></select>"
cnt = pg.count(old)
if cnt == 1:
    pg = pg.replace(old, new)
    io.open(PG, "w", encoding="utf-8", newline="").write(pg)
    print("PASS option 追加：租入 option 已加")
elif pg.count("<option>租入</option>") == 1:
    print("PASS option 已在位（幂等跳过）")
else:
    raise SystemExit("FAIL option 锚点 %d 次" % cnt)
pg2 = io.open(PG, encoding="utf-8", newline="").read()
assert pg2.count("<option>租入</option>") == 1
raw = open(PG, "rb").read()
print("PASS 库存查询：租入 option 1 次·CRLF=%d 裸LF=%d" % (
    raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")))
print("T2 全部完成")
