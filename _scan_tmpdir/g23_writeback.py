# -*- coding: utf-8 -*-
"""G23 T4 收尾回写：P1-R01 附录两处 + _AGENT基线 三处 + _索引 G23 行（哈希占位待回填）
精确替换+assert 计数+幂等（重复运行不叠加）"""
import io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"

def patch(path, old, new, n=1, tag=""):
    t = open(path, encoding="utf-8").read()
    if new in t and old not in t:
        print(f"[SKIP] {tag} 已是目标态（幂等）")
        return True
    c = t.count(old)
    if c != n:
        print(f"[FAIL] {tag}：「{old[:36]}…」出现 {c} 次（预期 {n}）")
        return False
    open(path, "w", encoding="utf-8", newline="").write(t.replace(old, new))
    print(f"[PASS] {tag}")
    return True

ok = True

# ============ 1. P1-R01 附录两处 ============
p1 = ROOT + r"\P1-R01-需求梳理与功能框架.md"
ok &= patch(p1,
    "- 预留：P2 = 功能调研/PRD；P4 = 技术方案；P5 = 开发与测试（启用时在此声明）",
    "- **P2 = 功能调研/PRD（已启用，2026-09-12）**：P2-R01 = 产品需求文档（见 10.2 清单）；预留：P4 = 技术方案；P5 = 开发与测试（启用时在此声明）",
    1, "P1-R01 10.1 启用声明")

ok &= patch(p1,
    "| P1-R05 | ./agent-handoff/20260909-56fc58d-P1-R05-交接文档-冻结.md |",
    "| P2-R01 | ./P2-R01-产品需求文档.md | 产品需求文档 **V1.0**（2026-09-12 G23 生成：需求基线=G22 后原型现状[115 HTML·38 实体·待办 16 类]+09-08 会议纪要最终版+基线拍板至 2026-09-12；prd-auto-generator 标准模式模块级 3 段 × 10 模块[PRJ/SAL/LEA/PUR/WHS/BAS/FIN/SYS/WF/MOB]·UC 89/AC 55·Mermaid 12·待确认清单 12 项；术语按 P1-R04 V0.6；生成过程原型只读零改动） |\n| P1-R05 | ./agent-handoff/20260909-56fc58d-P1-R05-交接文档-冻结.md |",
    1, "P1-R01 10.2 加 P2-R01 行")

# ============ 2. _AGENT基线 三处 ============
base = ROOT + r"\agent-handoff\_AGENT基线.md"

# 2a 文档地图 P1-R01 版本行 V0.6→V0.7（保留行内说明文字，仅改版本号段）
ok &= patch(base,
    "| `P1-R01-需求梳理与功能框架.md` | 需求主档 V0.6：REQ 21 条 / FP 38 个 / US 18 条 |",
    "| `P1-R01-需求梳理与功能框架.md` | 需求主档 V0.7（09-10 G07：FP4-01/02 随台账合并改写）：REQ 21 条 / FP 38 个 / US 18 条 |",
    1, "基线·文档地图 P1-R01 V0.7 更正")

# 2b 文档地图加 P2-R01 行（插在 P1-R01 html 行之后）
ok &= patch(base,
    "| `P1-R01-需求梳理与功能框架.html` | 外发版 | **快照，勿直接编辑** |",
    "| `P1-R01-需求梳理与功能框架.html` | 外发版 | **快照，勿直接编辑** |\n| `P2-R01-产品需求文档.md` | 产品需求文档 V1.0（2026-09-12 G23：需求基线=G22 后原型+09-08 纪要最终版+拍板至 09-12；10 模块 3 段·UC 89/AC 55·待确认 12 项；术语 V0.6） | **最新需求真值源**（原型变更后做增量版本） |",
    1, "基线·文档地图加 P2-R01 行")

# 2c 当前任务块：G22 行前插 G23 行（G22 行保留为「上一任务」语义已在其文内）
g22_anchor = "- **当前任务**：✅ **G22 租赁出库称呼统一与杂项清理（2026-09-12·4ff7f5a·ZCode 无人值守·副机 macOS 会话）**"
g23_line = (
    "- **当前任务**：✅ **G23 PRD 文档生成（2026-09-12·哈希见 _索引·ZCode 无人值守·主机 Win 会话）**——"
    "P2-R01-产品需求文档.md V1.0 新建（1377 行）：范围边界（In 10 模块/Out 14 项）+角色列表（9 内部+3 外部）+待确认清单 12 项+"
    "模块 3 段 × 10（PRJ/SAL/LEA/PUR/WHS/BAS/FIN/SYS/WF/MOB·UC 89/AC 55 Given-When-Then 强绑定）+"
    "五单据流转（三链+预收预付冲抵·Mermaid 2）+六接口时序（路凯/吉客云·待客户答复标注）+七实时通信判定不产出；"
    "计费口径三段式/无日租金/退租两事件/待办 16 类含租赁出库审核/组合出库旧称呼全文 0；"
    "验证门：g23_verify 36/36 PASS·质量检查 3 项 PASS·原型零改动（mtime≤开工时间戳·git P3-R01 前缀 0 行）；"
    "回写四件（本文档/索引/基线/P1-R01 附录 10.1 启用+10.2 行）；失败清单 goal-failures-g23.md 失败 0 项·偏差 9 条闭环；"
    "上一任务 G22 ✅ 4ff7f5a；**任务总账=`agent-handoff/_索引.md`**；遗留新增：P2-R01 增量维护机制（原型变更后续版）、"
    "待确认清单 12 项随客户答复回填\n"
    + g22_anchor.replace("- **当前任务**：✅ **G22", "- **上一任务**：✅ **G22")
)
ok &= patch(base, g22_anchor, g23_line, 1, "基线·当前任务块滚动")

# ============ 3. _索引 G23 行（哈希占位） ============
idx = ROOT + r"\agent-handoff\_索引.md"
# 末行追加（表格尾）
t = open(idx, encoding="utf-8").read()
if "| G23 |" in t:
    print("[SKIP] 索引 G23 行已存在（幂等）")
else:
    g22_last = None
    for l in t.splitlines():
        if l.startswith("| G22 |"):
            g22_last = l
    if not g22_last:
        print("[FAIL] 索引未找到 G22 行锚")
        ok = False
    else:
        g23_idx = ("| G23 | 09-12 | PRD 文档生成（P2-R01 V1.0 新建 1377 行·prd-auto-generator 标准模式："
                   "范围边界 In 10 模块/Out 14+角色 9 内 3 外+待确认 12｜模块 3 段 × 10[PRJ/SAL/LEA/PUR/WHS/BAS/FIN/SYS/WF/MOB]"
                   "·UC 89/AC 55·Mermaid 12｜五单据流转+六接口时序+七实时通信判定｜术语 V0.6 废弃词 0·组合出库 0｜"
                   "原型只读零改动·g23_verify 36/36｜回写四件+P1-R01 附录 10.1 P2 启用声明+10.2 行） | ✅ | {HASH} | 20260912-G23-PRD文档生成.md |")
        open(idx, "w", encoding="utf-8", newline="").write(t.rstrip("\n") + "\n" + g23_idx + "\n")
        print("[PASS] 索引 G23 行（{HASH} 占位）")

print()
print(">>> 回写脚本执行", "全部成功" if ok else "存在失败", "")
sys.exit(0 if ok else 1)
