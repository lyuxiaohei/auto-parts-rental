# -*- coding: utf-8 -*-
"""G23 前置校验 1/2/3/4/5（7 条中的文件系统部分；6=git 存档与 7=时间戳另行处理）"""
import os, time, datetime, io, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
PROTO = os.path.join(ROOT, "P3-R01-包装租赁管理后台原型")
HANDOFF = os.path.join(ROOT, "agent-handoff")

out = io.StringIO()
def w(s=""):
    out.write(s + "\n")

now = time.time()

# ---- 校验 1：单写者互斥（任务书与失败清单自身豁免）----
EXEMPT = {
    os.path.join(HANDOFF, "20260912-G23-PRD文档生成.md"),
    os.path.join(HANDOFF, "goal-failures-g23.md"),
}
def recent_files(base, minutes=30):
    hits = []
    for dirpath, dirnames, filenames in os.walk(base):
        # 跳过备份目录（备份目录内文件不是并行写入信号）
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            if p in EXEMPT:
                continue
            try:
                m = os.path.getmtime(p)
            except OSError:
                continue
            if (now - m) < minutes * 60:
                hits.append((p, m))
    return sorted(hits, key=lambda x: -x[1])

w("== 校验1 单写者互斥 ==")
ok1 = True
for base, label in ((PROTO, "原型目录"), (HANDOFF, "agent-handoff")):
    hits = recent_files(base)
    if hits:
        ok1 = False
        w(f"[FAIL] {label} 有 {len(hits)} 个文件 mtime < 30 分钟：")
        for p, m in hits[:10]:
            w(f"   {datetime.datetime.fromtimestamp(m).isoformat()}  {os.path.relpath(p, ROOT)}")
    else:
        w(f"[PASS] {label} 最近 30 分钟无文件改动")
w(f"校验1 结论: {'PASS' if ok1 else 'FAIL'}")

# ---- 校验 2：防重复执行 ----
w("")
w("== 校验2 防重复执行 ==")
idx = os.path.join(HANDOFF, "_索引.md")
ok2 = True
if os.path.exists(idx):
    txt = open(idx, encoding="utf-8").read()
    has_g23 = "| G23 |" in txt or "| G23　" in txt
    w(("[FAIL] _索引.md 已含 | G23 | 行" if has_g23 else "[PASS] _索引.md 无 | G23 | 行"))
    ok2 = ok2 and not has_g23
else:
    w("[FAIL] _索引.md 不存在")
    ok2 = False
prd = os.path.join(ROOT, "P2-R01-产品需求文档.md")
if os.path.exists(prd):
    w("[FAIL] 项目根已存在 P2-R01-产品需求文档.md")
    ok2 = False
else:
    w("[PASS] 项目根无 P2-R01-产品需求文档.md")
w(f"校验2 结论: {'PASS' if ok2 else 'FAIL'}")

# ---- 校验 3：技能 7 文件在位 ----
w("")
w("== 校验3 prd-auto-generator 技能 7 文件 ==")
SKILL = r"C:\Users\Administrator\.agents\skills\prd-auto-generator"
skill_files = [
    "SKILL.md",
    r"templates\version-prd.md",
    r"templates\prd-module-section.md",
    r"rules\structure-rules.md",
    r"rules\writing-rules.md",
    r"rules\flowchart-rules.md",
    r"rules\material-checklist.md",
]
ok3 = True
for f in skill_files:
    p = os.path.join(SKILL, f)
    e = os.path.exists(p)
    ok3 = ok3 and e
    w(f"[{'PASS' if e else 'FAIL'}] {f}")
w(f"校验3 结论: {'PASS' if ok3 else 'FAIL'}")

# ---- 校验 4：材料存在性（需求来源 1-7）----
w("")
w("== 校验4 需求来源 1-7 存在性 ==")
def find_meeting_doc():
    base = os.path.join(ROOT, "2026-09-08 汽车物流包装租赁第3次沟通原型演示")
    if not os.path.isdir(base):
        return None
    cands = []
    for dirpath, _, filenames in os.walk(base):
        for fn in filenames:
            if "会议纪要" in fn and "最终" in fn and fn.endswith(".md"):
                cands.append(os.path.join(dirpath, fn))
    return cands[0] if cands else None

sources = {
    "源1 原型目录": PROTO,
    "源1 demo-data": os.path.join(PROTO, "_data", "demo-data.js"),
    "源2 _AGENT基线": os.path.join(HANDOFF, "_AGENT基线.md"),
    "源3 会议纪要最终版": find_meeting_doc(),
    "源4 术语表": os.path.join(ROOT, "P1-R04-术语表.md"),
    "源5 P1-R01": os.path.join(ROOT, "P1-R01-需求梳理与功能框架.md"),
    "源6 A02": os.path.join(PROTO, "P3-R01-A02-页面类型与入口对照表.md"),
    "源6 A05": os.path.join(PROTO, "P3-R01-A05-字段字典.md"),
    "源6 A06": os.path.join(PROTO, "P3-R01-A06-实体关系与状态机.md"),
    "源6 F01": os.path.join(PROTO, "P3-R01-F01-业务流程导航图.html"),
    "源0 G22任务文档": os.path.join(HANDOFF, "20260911-G22-租赁出库称呼统一与杂项清理.md"),
}
ok4 = True
meeting_path = None
for k, v in sources.items():
    e = bool(v) and os.path.exists(v)
    ok4 = ok4 and e
    w(f"[{'PASS' if e else 'FAIL'}] {k}: {v}")
    if k == "源3 会议纪要最终版" and e:
        meeting_path = v
w(f"校验4 结论: {'PASS' if ok4 else 'FAIL'}")

# ---- 校验 5：口径基数 ----
w("")
w("== 校验5 口径基数 ==")
htmls = []
for dirpath, dirnames, filenames in os.walk(PROTO):
    if os.sep + "backup" in dirpath:
        continue
    for fn in filenames:
        if fn.lower().endswith(".html"):
            htmls.append(os.path.join(dirpath, fn))
w(f"原型 HTML 总数 = {len(htmls)}（预期 115）")

dd = open(os.path.join(PROTO, "_data", "demo-data.js"), encoding="utf-8").read()
import re
entities = re.findall(r"^\s{2}([A-Za-z][A-Za-z0-9_]*)\s*:\s*\[", dd, re.M)
w(f"demo-data 实体数 = {len(entities)}（预期 38）")

# todoItems 待办键数：docNo 即键（G22 后 16 行）
m = re.search(r"todoItems\s*:\s*\[(.*?)\n\s{2}\]", dd, re.S)
todo_n = 0
if m:
    todo_n = len(re.findall(r"docNo\s*:", m.group(1)))
w(f"todoItems 行数(docNo 计) = {todo_n}（预期 16）")

a05 = open(os.path.join(PROTO, "P3-R01-A05-字段字典.md"), encoding="utf-8").read()
head = a05.split("\n")[:12]
w("A05 头部 12 行：")
for line in head:
    if line.strip():
        w("   " + line.strip()[:100])

# 废弃词表位置确认（第五节）
p1r04 = open(os.path.join(ROOT, "P1-R04-术语表.md"), encoding="utf-8").read()
w(f"P1-R04 含「废弃」字样行数 = {len([l for l in p1r04.splitlines() if '废弃' in l])}（供验证门 1 现场提取）")

w("")
w("== 总结论 ==")
allpass = ok1 and ok2 and ok3
w(f"校验1={ok1} 校验2={ok2} 校验3={ok3} 校验4={ok4}")
w(f">>> 前置校验（阻塞性 1/2/3）: {'全部通过' if allpass else '存在不符，停止执行'}")
if not ok4:
    w(">>> 校验4 有缺失：该源降级尽力提取并记失败清单（不阻塞）")
if meeting_path:
    w(f">>> 会议纪要路径: {meeting_path}")

sys.stdout.write(out.getvalue())
with open(os.path.join(ROOT, "_scan_tmpdir", "g23_preflight_out.txt"), "w", encoding="utf-8") as f:
    f.write(out.getvalue())
