# -*- coding: utf-8 -*-
"""G24 前置校验：单写者互斥/防重复执行/材料存在性/口径基数/工作区状态/开工时间戳"""
import os, time, datetime, subprocess, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
PROTO = os.path.join(ROOT, "P3-R01-包装租赁管理后台原型")
HANDOFF = os.path.join(ROOT, "agent-handoff")
FAILPATH = os.path.join(HANDOFF, "goal-failures-g24.md")
TS_PATH = os.path.join(ROOT, "_scan_tmpdir", "g24_starttime.txt")

now = time.time()
problems = []   # 阻塞性
notices = []    # 非阻塞偏差

def log(s):
    print(s)

# ---------- 1. 单写者互斥 ----------
EXEMPT = {"20260912-G24-决策落实与场景闭环检查.md", "goal-failures-g24.md", "g24_prompt.md"}
def recent_files(d, topn=5):
    items = []
    for dirpath, dirnames, filenames in os.walk(d):
        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            try:
                mt = os.path.getmtime(fp)
            except OSError:
                continue
            rel = os.path.relpath(fp, d)
            if d == HANDOFF and fn in EXEMPT:
                continue
            items.append((mt, rel))
    items.sort(reverse=True)
    return items[:topn]

log("== 1. 单写者互斥（mtime 距今分钟数，阈值 30）==")
blocking_conflict = False
for label, d in (("原型目录", PROTO), ("agent-handoff", HANDOFF)):
    rf = recent_files(d)
    if rf:
        age_min = (now - rf[0][0]) / 60.0
        log(f"[{label}] 最近文件: {rf[0][1]} 距今 {age_min:.1f} 分钟")
        for mt, rel in rf:
            log(f"    - {rel}  {(now-mt)/60.0:.1f} 分钟前")
        if age_min < 30:
            blocking_conflict = True
            problems.append(f"单写者互斥不符：{label} 最近文件 {rf[0][1]} 距今 {age_min:.1f} 分钟 < 30")
    else:
        log(f"[{label}] 无文件")

# ---------- 2. 防重复执行 ----------
log("== 2. 防重复执行 ==")
idx = os.path.join(HANDOFF, "_索引.md")
if os.path.exists(idx):
    with open(idx, encoding="utf-8") as f:
        idx_text = f.read()
    has_g24 = "| G24" in idx_text
    log(f"_索引.md 含 G24 行: {has_g24}")
    if has_g24:
        problems.append("防重复执行：_索引.md 已有 G24 行，疑似已执行")
else:
    problems.append("防重复执行：_索引.md 不存在")
report_path = os.path.join(ROOT, "P2-R02-决策落实与场景闭环检查报告.md")
log(f"项目根 P2-R02 报告已存在: {os.path.exists(report_path)}")
if os.path.exists(report_path):
    problems.append("防重复执行：P2-R02 报告已存在")

# ---------- 3. 材料存在性 ----------
log("== 3. 检查源 1-6 存在性 ==")
SRC = {
    "源1 09-08纪要": os.path.join(ROOT, "2026-09-08 汽车物流包装租赁第3次沟通原型演示", "2026-09-08 汽车物流包装租赁第3次沟通原型演示 [会议纪要-最终版].md"),
    "源2 P1-R01": os.path.join(ROOT, "P1-R01-需求梳理与功能框架.md"),
    "源3 _AGENT基线": os.path.join(HANDOFF, "_AGENT基线.md"),
    "源4 P2-R01": os.path.join(ROOT, "P2-R01-产品需求文档.md"),
    "源5 原型目录": PROTO,
    "源6 P3-R04": os.path.join(ROOT, "P3-R04-演示场景覆盖梳理.md"),
    "源7 第1次会议目录": os.path.join(ROOT, "2026-08-31 汽车物流包装租赁第1次对接"),
}
for k, v in SRC.items():
    ok = os.path.exists(v)
    log(f"{k}: {'存在' if ok else '缺失'} — {v}")
    if not ok and not k.startswith("源7"):
        problems.append(f"材料缺失：{k} {v}")
    elif not ok and k.startswith("源7"):
        notices.append(f"源7 缺失（按需不强制）：{v}")
# 附：demo-data / A02 / A05 / A06
for extra, p in (
    ("demo-data.js", os.path.join(PROTO, "_data", "demo-data.js")),
    ("A02", os.path.join(PROTO, "P3-R01-A02-页面清单.md")),
    ("A05", os.path.join(PROTO, "P3-R01-A05-字段字典.md")),
    ("A06", os.path.join(PROTO, "P3-R01-A06-实体关系与状态机.md")),
):
    ok = os.path.exists(p)
    log(f"支撑材料 {extra}: {'存在' if ok else '缺失'}")
    if not ok:
        notices.append(f"支撑材料缺失：{extra} {p}")

# ---------- 4. 口径基数 ----------
log("== 4. 口径基数 ==")
html_count = 0
for dirpath, dirnames, filenames in os.walk(PROTO):
    for fn in filenames:
        if fn.lower().endswith(".html"):
            html_count += 1
log(f"原型 HTML 总数 = {html_count}（预期 115）")
if html_count != 115:
    notices.append(f"口径基数：HTML={html_count} != 115，以实际为准")

dd_path = os.path.join(PROTO, "_data", "demo-data.js")
if os.path.exists(dd_path):
    with open(dd_path, encoding="utf-8") as f:
        dd = f.read()
    import re
    # 实体键 = "key": [ 形式
    keys = re.findall(r'"([A-Za-z][A-Za-z0-9_]*)"\s*:\s*\[', dd)
    # 去掉可能嵌套的行对象内数组：粗口径（以顶层数组缩进为准，直接统计唯一键）
    # demo-data 结构为 const demoData = { "orders": [...], ... }；行内数组也匹配，取顶层近似：统计 "key": [ 后该行以 , 或 [ 开头缩进 2 空格的
    ent = re.findall(r'^\s{2}"([A-Za-z][A-Za-z0-9_]*)"\s*:\s*\[', dd, re.M)
    log(f"demo-data 顶导出实体数（缩进 2）= {len(set(ent))}（预期 38）")
    if len(set(ent)) != 38:
        notices.append(f"口径基数：实体数={len(set(ent))} != 38")
    todo_keys = set(re.findall(r'"type"\s*:\s*"(QTCK|DB|RZD|[A-Z]{2,6})"', dd))
    # 更稳：直接数 docNo 键数行
    todo_cnt = len(re.findall(r'"docNo"\s*:', dd))
    log(f"todoItems 行数(docNo 计) = {todo_cnt}（预期 16）")
    if todo_cnt != 16:
        notices.append(f"口径基数：todoItems 行数={todo_cnt} != 16")

p3r04_path = SRC["源6 P3-R04"]
if os.path.exists(p3r04_path):
    with open(p3r04_path, encoding="utf-8") as f:
        p3 = f.read()
    # 主表行数：七节主表 | S-xx | 开头的数据行 —— 先打印含"场景"主表段落供人工核
    rows = re.findall(r'^\|\s*(S\d{1,2}[a-z]?)\s*\|', p3, re.M)
    log(f"P3-R04 主表 S 编号行 = {len(rows)}（预期 76±2）")
    if not (74 <= len(rows) <= 78):
        notices.append(f"口径基数：P3-R04 主表行={len(rows)} 超出 76±2，以实际为准")

# ---------- 5. 工作区状态 ----------
log("== 5. git status ==")
r = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
out = (r.stdout or "").strip()
log(f"git status --porcelain 输出行数 = {len([l for l in out.splitlines() if l.strip()])}")
if out:
    for l in out.splitlines():
        log("  " + l)

# ---------- 6. 开工时间戳 ----------
log("== 6. 开工时间戳 ==")
ts = datetime.datetime.now().isoformat(timespec="seconds")
with open(TS_PATH, "w", encoding="utf-8") as f:
    f.write(ts)
log(f"已写 {TS_PATH} = {ts}")

# ---------- 失败清单占位 ----------
if not os.path.exists(FAILPATH):
    with open(FAILPATH, "w", encoding="utf-8") as f:
        f.write("# goal-failures-g24\n\n（占位：若执行中出现跳过项将逐条登记；收尾给结论行）\n")
    log("失败清单占位已创建")
else:
    log("失败清单已存在，跳过创建")

log("")
log("== 前置校验结论 ==")
if problems:
    for p in problems:
        log("BLOCKING: " + p)
    with open(FAILPATH, "a", encoding="utf-8") as f:
        f.write("\n## 前置校验\n")
        for p in problems:
            f.write(f"- [阻塞] {p}\n")
    sys.exit(2)
else:
    log("PASS：无阻塞性不符")
    if notices:
        for n in notices:
            log("NOTICE: " + n)
    with open(FAILPATH, "a", encoding="utf-8") as f:
        f.write("\n## 前置校验\n- PASS（无阻塞性不符）\n")
        for n in notices:
            f.write(f"- 偏差注记: {n}\n")
