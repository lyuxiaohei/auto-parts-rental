# -*- coding: utf-8 -*-
"""G30.5 修复后自检：goal-creator v7 无人值守清单逐条证据化 + 路径自包含实测
只读；证据打印到 stdout 供贴对话。
"""
import io, os, re, sys, shutil

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
P31 = ROOT + r"\_scan_tmpdir\g31_prompt.md"
P32 = ROOT + r"\_scan_tmpdir\g32_prompt.md"
T31 = ROOT + r"\agent-handoff\20260914-G31-第4次会议原型改造包.md"
T32 = ROOT + r"\agent-handoff\20260914-G32-退货退款与转移出库.md"
BASE = ROOT + r"\agent-handoff\_AGENT基线.md"
IDX = ROOT + r"\agent-handoff\_索引.md"

def rd(p):
    f = io.open(p, encoding="utf-8", newline="")
    c = f.read(); f.close()
    return c

print("=" * 72)
print("§1 结构化达标（实测计数，非目测）")
print("=" * 72)
for tag, p in (("g31_prompt", P31), ("g32_prompt", P32), ("G31 任务书", T31), ("G32 任务书", T32)):
    c = rd(p)
    blocks = len(re.findall(r"【[^】]+】", c))
    heads = len(re.findall(r"^##+ ", c, re.M))
    # 最长连排段：连续非空行（不含表格/列表/标题/块标记行）
    longest = 0; cur = 0
    for line in c.split("\n"):
        s = line.strip()
        if s and not s.startswith(("#", "-", "|", "【", ">", "1.", "2.", "3.", "4.", "5.", "6.", "or stop")) and not re.match(r"^\d+\.", s):
            cur += 1; longest = max(longest, cur)
        else:
            cur = 0
    limit = "OK" if len(c) <= 4000 else "超标" if tag.endswith("prompt") else "N/A（文件不限 4000）"
    print("%-12s 块标记=%-3d 标题=%-3d 最长连排段=%d 行 字符数=%-5d 上限4000=%s"
          % (tag, blocks, heads, longest, len(c), limit))

print()
print("=" * 72)
print("§2 无人值守措辞扫描（搜提问类词，期望 0）")
print("=" * 72)
probes = ["是否", "要不要", "请您", "请确认", "确认后", "可以吗", "吗？", "？\n", "等待用户", "询问用户"]
for tag, p in (("g31_prompt", P31), ("g32_prompt", P32), ("G31 任务书", T31), ("G32 任务书", T32)):
    c = rd(p)
    hits = {}
    for w in probes:
        n = c.count(w)
        if n: hits[w] = n
    # 特别标出含「确认」的行号，人工复核是否提问式
    ctx = [(i, l.strip()[:90]) for i, l in enumerate(c.split("\n"), 1) if "确认" in l or "拍板" in l]
    print("%-12s 提问词命中=%s" % (tag, hits if hits else "无（0 处）"))
    for i, l in ctx[:6]:
        print("              确认/拍板语境 L%-3d %s" % (i, l))

print()
print("=" * 72)
print("§3 路径自包含实测（os.path.exists 逐条）")
print("=" * 72)
paths = [
    (BASE, "基线（g31/g32 prompt 路由 1）", True),
    (T31, "G31 任务书（g31 prompt 路由 2）", True),
    (T32, "G32 任务书（g32 prompt 路由 2）", True),
    (IDX, "索引台账（前置校验引用）", True),
    (ROOT + r"\P2-R01-产品需求文档.md", "拍板依据源", True),
    (ROOT + r"\_scan_tmpdir\g31_ledger.py", "G31 立项产物（豁免项）", True),
    (ROOT + r"\_scan_tmpdir\audit_results_g17baseline.json", "g17 审计基线（前置校验④）", True),
    (ROOT + r"\_scan_tmpdir\g17_audit_diff.py", "g17 diff 脚本（前置校验④）", True),
    (ROOT + r"\_scan_tmpdir\v32_menu_verify.py", "菜单断言脚本（完成判定①）", True),
    (ROOT + r"\_scan_tmpdir\verify_listfull.py", "listfull 断言脚本（完成判定②）", True),
    (ROOT + r"\agent-handoff\goal-failures-g31.md", "G31 失败清单（应不存在·失败时创建）", False),
    (ROOT + r"\agent-handoff\goal-failures-g32.md", "G32 失败清单（应不存在·失败时创建）", False),
    (ROOT + r"\_scan_tmpdir\backup-g31-20260914", "G31 备份目录（应不存在·开工创建）", False),
]
fails = 0
for p, note, want in paths:
    ex = os.path.exists(p)
    ok = (ex == want)
    if not ok: fails += 1
    print("[%s] exists=%-5s want=%-5s  %s" % ("OK" if ok else "!!", ex, want, note))
print("节点可用：node →", shutil.which("node") or "未找到")

print()
print("=" * 72)
print("§4 三道保险在位核查")
print("=" * 72)
checks = [
    ("保险1 默认决策表", T31, "默认决策表"), ("保险1 默认决策表", T32, "默认决策表"),
    ("保险2 失败清单路径", T31, "失败清单"), ("保险2 失败清单路径", T32, "失败清单"),
    ("保险3 验证门段", T31, "验证门"), ("保险3 验证门段", T32, "验证门"),
    ("prompt 默认决策表指向", P31, "默认决策表在任务书内"), ("prompt 默认决策表指向", P32, "默认决策表在任务书内"),
    ("prompt 失败留档", P31, "goal-failures-g31.md"), ("prompt 失败留档", P32, "goal-failures-g32.md"),
    ("prompt 回写三件", P31, "收尾回写三件"), ("prompt 回写三件", P32, "回写证据"),
    ("prompt git 批次", P31, "一 goal 至少一提交"), ("prompt git 批次", P32, "一 goal 至少一提交"),
    ("prompt 互斥前置", P31, "单写者互斥"), ("prompt 互斥前置", P32, "单写者互斥"),
    ("prompt 根路径声明", P31, "工作目录（命令与全部相对路径之根"), ("prompt 根路径声明", P32, "工作目录（命令与全部相对路径之根"),
    ("红线 D-122", P31, "D-122"), ("红线 T3 无拍板零改动", P32, "无道远拍板零原型改动"),
    ("stop 限额", P31, "or stop after"), ("stop 限额", P32, "or stop after"),
]
for name, p, need in checks:
    c = rd(p)
    print("[%s] %-26s ← %s" % ("OK" if need in c else "!!", name, need))
    if need not in c: fails += 1

print()
print("=" * 72)
print("§5 编号链复核（修复后）")
print("=" * 72)
c = rd(ROOT + r"\P2-R01-产品需求文档.md")
rows = re.findall(r"^\| (D-\d+) \|", c, re.M)
import collections
cnt = collections.Counter(rows)
print("D 行数=%d 唯一号=%d 重号=%s 断号=%s"
      % (len(rows), len(cnt), {k: v for k, v in cnt.items() if v > 1} or "无",
         [n for n in range(1, 127) if ("D-%02d" % n) not in cnt] or "无"))
print("残留检查 · 'D-97~D-125' 出现次数 =", c.count("D-97~D-125"), "（期望 0）")
print("残留检查 · 'G31 T10' 出现次数 =", c.count("G31 T10"), "（期望 0）")
print("残留检查 · '3:25-3:59' 出现次数 =", c.count("3:25-3:59"), "（期望 0）")
print("会议纪要 md 残留 '29 条':",
      rd(ROOT + r"\2026-09-14 汽车物流包装租赁第4次会议原型演示\2026-09-14 汽车物流包装租赁第4次会议原型演示 [会议纪要].md").count("29 条"),
      "（期望 0）")

print()
print("自检结论：%s（失败项 %d）" % ("全部通过" if fails == 0 else "存在未通过项，见上 !!", fails))
