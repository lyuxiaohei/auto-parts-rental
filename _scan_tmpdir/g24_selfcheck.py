# -*- coding: utf-8 -*-
"""G24 goal-creator 交付自检：路径实测/措辞扫描/结构化计数/字符数/占位预创建"""
import io, os, sys, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"

print("== 1. 路径 os.path.exists 实测 ==")
paths = {
    "项目根": ROOT,
    "基线": ROOT + r"\agent-handoff\_AGENT基线.md",
    "G24任务书": ROOT + r"\agent-handoff\20260912-G24-决策落实与场景闭环检查.md",
    "执行命令": ROOT + r"\_scan_tmpdir\g24_prompt.md",
    "失败清单(待建)": ROOT + r"\agent-handoff\goal-failures-g24.md",
    "索引": ROOT + r"\agent-handoff\_索引.md",
    "09-08纪要最终版": ROOT + r"\2026-09-08 汽车物流包装租赁第3次沟通原型演示\2026-09-08 汽车物流包装租赁第3次沟通原型演示 [会议纪要-最终版].md",
    "P1-R01": ROOT + r"\P1-R01-需求梳理与功能框架.md",
    "P1-R04术语表": ROOT + r"\P1-R04-术语表.md",
    "P2-R01 PRD": ROOT + r"\P2-R01-产品需求文档.md",
    "P3-R04场景梳理": ROOT + r"\P3-R04-演示场景覆盖梳理.md",
    "原型目录": ROOT + r"\P3-R01-包装租赁管理后台原型",
    "A02": ROOT + r"\P3-R01-包装租赁管理后台原型\P3-R01-A02-页面类型与入口对照表.md",
    "A05": ROOT + r"\P3-R01-包装租赁管理后台原型\P3-R01-A05-字段字典.md",
    "A06": ROOT + r"\P3-R01-包装租赁管理后台原型\P3-R01-A06-实体关系与状态机.md",
    "08-31文件夹": ROOT + r"\2026-08-31 汽车物流包装租赁第1次对接",
    "09-02文件夹": ROOT + r"\2026-09-02 汽车物流包装租赁第2次沟通",
    "G23任务文档": ROOT + r"\agent-handoff\20260912-G23-PRD文档生成.md",
}
fail_flag = False
for k, p in paths.items():
    e = os.path.exists(p)
    if not e and k != "失败清单(待建)":
        fail_flag = True
    print(f"[{'PASS' if e else '待建' if '待建' in k or '失败清单' in k else 'FAIL'}] {k}: {p}")

# 失败清单占位预创建（goal-command-anchor-lesson 教训）
fp = paths["失败清单(待建)"]
if not os.path.exists(fp):
    open(fp, "w", encoding="utf-8", newline="\n").write(
        "# goal-failures-g24（占位预创建）\n\n"
        "> 本文件为 G24（决策落实与场景闭环检查）失败清单占位。执行中任一项 assert 失败/材料缺失/结构不符时，"
        "按「任务号/文件/原因」逐条追加于此并继续下一项；收尾报告须含本清单结论行（空清单给「无失败项」）。\n\n"
        "| 任务号 | 文件 | 原因 |\n|---|---|---|\n| （暂无） | | |\n")
    print(f"[PASS] 失败清单占位已预创建: goal-failures-g24.md")
else:
    print(f"[SKIP] 失败清单已存在")

print()
print("== 2. 无等待确认措辞扫描（任务书+命令） ==")
for label, p in (("任务书", paths["G24任务书"]), ("执行命令", paths["执行命令"])):
    t = open(p, encoding="utf-8").read()
    hits = [l.strip()[:60] for l in t.splitlines() if re.search(r"(是否|要不要|请确认|确认后执行|吗？|请示)", l)]
    # 「确认」业务词排除（账单确认/审核确认/验收/确认弹窗等）——只查问句/请示形态
    print(f"[{'FAIL' if hits else 'PASS'}] {label} 等待确认类措辞 {len(hits)} 处" + (f"：{hits[:3]}" if hits else ""))

print()
print("== 3. 结构化达标计数 ==")
tdoc = open(paths["G24任务书"], encoding="utf-8").read()
n_h2 = len(re.findall(r"^## ", tdoc, re.M))
prompt = open(paths["执行命令"], encoding="utf-8").read()
n_blocks = len(re.findall(r"【[^】]+】", prompt))
n_chars = len(prompt)
print(f"[{'PASS' if n_h2 >= 4 else 'FAIL'}] 任务书 ## 标题数 = {n_h2}（≥4）")
print(f"[{'PASS' if n_blocks >= 4 else 'FAIL'}] 命令块标记数 = {n_blocks}（≥4）")
print(f"[{'PASS' if n_chars <= 4000 else 'FAIL'}] 命令字符数 = {n_chars}（≤4000）")

# 默认决策表条数
m = re.search(r"## 默认决策表.*?## 失败处理策略", tdoc, re.S)
n_dec = len(re.findall(r"^\d+\. ", m.group(0), re.M)) if m else 0
print(f"[{'PASS' if n_dec >= 10 else 'FAIL'}] 默认决策表条数 = {n_dec}（≥10）")

# 验证门证据形态点名
vg = re.search(r"## 验证门.*?## 执行记录", tdoc, re.S).group(0)
has_ev = ("python" in vg and "grep" in vg and "PASS" in vg)
print(f"[{'PASS' if has_ev else 'FAIL'}] 验证门证据形态点名（python 断言/grep 输出/PASS 字样）")

print()
print("== 4. 收尾回写+git 硬性检查 ==")
for kw in ["收尾回写", "_索引.md", "哈希回填", "git add -A", "禁 push", "单写者互斥", "mtime"]:
    print(f"[{'PASS' if kw in tdoc else 'FAIL'}] 任务书含「{kw}」")

print()
print(">>> 自检总结：", "全部通过" if not fail_flag else "存在 FAIL（见上）")
