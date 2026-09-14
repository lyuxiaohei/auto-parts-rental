# -*- coding: utf-8 -*-
"""G28：P1-R08 索引建立后的回写（P1-R01 10.2 行+基线文档地图行+索引 G28 行+任务档）"""
import io, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"

# ---- 1. P1-R01 附录 10.2 加 P1-R08 行（表尾插入）----
fp = ROOT + r"\P1-R01-需求梳理与功能框架.md"
t = io.open(fp, encoding="utf-8", newline="").read()
NL = "\r\n" if t.count("\r\n") > (t.count("\n") - t.count("\r\n")) else "\n"
assert "P1-R08" not in t
i = t.find("### 10.2")
assert i > 0
# 表尾=10.2 后首个表格的最后一条 | 行（其后是非表格内容）
seg = t[i:]
last_pipe = None
for line in seg.split(NL):
    if line.startswith("|"):
        last_pipe = line
    elif last_pipe is not None and not line.startswith("|"):
        break
assert last_pipe, "未找到 10.2 表行"
new_row = "| P1-R08 | ./P1-R08-项目文件索引.md | 项目文件索引（2026-09-14 G28 建：全项目文件/文件夹地图——场景导航+根目录分组地图+原型/agent-handoff 导览+防误认三条；文件增删改名须同步本索引） |"
assert t.count(last_pipe) == 1
t = t.replace(last_pipe, last_pipe + NL + new_row, 1)
io.open(fp, "w", encoding="utf-8", newline="").write(t)
print("PASS P1-R01 10.2 加 P1-R08 行")

# ---- 2. 基线文档地图加行（P2-R02 行后）----
fp2 = ROOT + r"\agent-handoff\_AGENT基线.md"
t2 = io.open(fp2, encoding="utf-8", newline="").read()
NL2 = "\r\n" if t2.count("\r\n") > (t2.count("\n") - t2.count("\r\n")) else "\n"
assert "P1-R08" not in t2
anchor = None
for line in t2.split(NL2):
    if line.startswith("| P2-R02-"):
        anchor = line
        break
assert anchor, "未找到 P2-R02 文档地图行"
row = "| `P1-R08-项目文件索引.md` | 项目文件索引（2026-09-14 G28：全项目文件/文件夹地图·场景导航+目录导览+防误认三条） | **找东西入口**；文件增删改名必同步（并同步 P1-R01 附录 10.2） |"
t2 = t2.replace(anchor, anchor + NL2 + row, 1)
# 快照标题与当前块不动（轻量任务不滚动主块，在 G27 块尾补一句）
old27 = "上一任务 G25 ✅ 423a8b1；任务总账=agent-handoff/_索引.md"
new27 = "上一任务 G25 ✅ 423a8b1；任务总账=agent-handoff/_索引.md" + NL2 + "- **追记（09-14 G28）**：P1-R08-项目文件索引.md 建（全项目找东西入口·场景导航+目录地图）——文件增删改名须同步 P1-R08 与 P1-R01 附录 10.2"
assert t2.count(old27) == 1
t2 = t2.replace(old27, new27, 1)
io.open(fp2, "w", encoding="utf-8", newline="").write(t2)
print("PASS 基线文档地图加 P1-R08 行+G27 块追记 G28")

# ---- 3. _索引挂 G28 行 ----
fp3 = ROOT + r"\agent-handoff\_索引.md"
t3 = io.open(fp3, encoding="utf-8", newline="").read()
NL3 = "\r\n" if t3.count("\r\n") > (t3.count("\n") - t3.count("\r\n")) else "\n"
assert "| G28 |" not in t3
row3 = ("| G28 | 09-14 | 项目文件索引（道远要求：文档文件夹过多·建索引方便找关键文档/文件夹）｜"
        "P1-R08-项目文件索引.md 新建：场景导航 10 行（看需求/查口径/演示/拍板/交接/术语/会议原文/历史/工具）"
        "+根目录地图三组（活文档 5/只读 7 类/工作区 8）+P3-R01 与 agent-handoff 两目录导览+防误认三条（备份≠现状·zip≠最新·空号不复用）｜"
        "P1-R01 附录 10.2 加行｜基线文档地图加行+G27 块追记｜纯文档零原型改动 | ✅ | （哈希待回填） | （同段提交） | 20260914-G28-项目文件索引.md |")
t3 = t3.rstrip(NL3) + NL3 + row3 + NL3
io.open(fp3, "w", encoding="utf-8", newline="").write(t3)
print("PASS 索引 G28 行已挂（哈希待回填）")
