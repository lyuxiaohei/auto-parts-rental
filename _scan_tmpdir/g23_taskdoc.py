# -*- coding: utf-8 -*-
"""G23 任务文档标 ✅+执行记录+哈希回填（9daca20）到 任务文档/索引/基线 三处"""
import io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
H1 = "9daca20"

def patch(path, old, new, tag, n=1):
    t = open(path, encoding="utf-8").read()
    if new in t and old not in t:
        print(f"[SKIP] {tag}（已是目标态）")
        return True
    c = t.count(old)
    if c != n:
        print(f"[FAIL] {tag} 出现 {c} 次（预期 {n}）")
        return False
    open(path, "w", encoding="utf-8", newline="").write(t.replace(old, new))
    print(f"[PASS] {tag}")
    return True

ok = True
tdoc = ROOT + r"\agent-handoff\20260912-G23-PRD文档生成.md"
idx = ROOT + r"\agent-handoff\_索引.md"
base = ROOT + r"\agent-handoff\_AGENT基线.md"

# 1. 任务文档头部 ✅+哈希
ok &= patch(tdoc,
    "> **状态**：⏳ 待执行（收尾时改 ✅ 并回填 commit 哈希）\n> **commit**：（待回填）",
    f"> **状态**：✅ 已执行（2026-09-12 无人值守会话·主机 Win·ZCode）\n> **commit**：{H1}（工作批次）｜收尾回写批次见 git log 次条",
    "任务文档头部 ✅+哈希")

# 2. 执行记录节追加
record = """
## 执行记录（收尾时填）

> **执行**：2026-09-12 无人值守（ZCode·主机 Win 会话）；全程原型只读零改动。

**前置校验 7 条**：①单写者互斥——原型目录/agent-handoff 最近 30 分钟 0 改动（任务书自身豁免）②防重复——索引无 G23 行、根无 P2-R01 ③技能 7 文件在位 ④材料 11 项齐全（会议纪要最终版定位成功）⑤口径基数——HTML=115 ✓/实体=38 ✓（products/assetTracks 带注释前缀定义，正则两轮修正后命中）/todoItems=16 ✓（含 CK-20260910-022）/A05 读数 325 字段行 ⑥开工存档 e925771 ⑦时间戳 2026-09-12T09:54:52 落盘。

**第 0 步**：7 源通读（基线/纪要最终版/术语表 V0.6/P1-R01 V0.7/A02 v3.4/A05/A06+demo-data 实测提取）+技能 7 文件+G22 执行记录；实测修正两处滞后记录——projects.suppliers 字段 8/8 行有值（A05/A06 缺口 #4 已过时，B7）、文件名实为 产品档案.html（A02 第三节菜单名口径混入，路径引用以实际文件为准）。

**T1**：一、范围边界（In 10 模块 F-01~F-10 表+演示支撑页注记/Out 14 项——四移除模块/客户端自助下单/扫码/采购计划/归属权/路凯替换/维修/期初/独立台账/到期提醒/日租金/AI 导单）+二.1 角色列表（9 内部源=roles+3 外部：客户/供应商/路凯）+1.3 待确认清单 12 项（纪要 T1-T7+基线待客户答复+挂起决策）。

**T2**：模块 3 段 × 10 全段落盘（分模块追加写）：PRJ（6 UC+测试账号全文唯一块）→SAL（8）→LEA（14·租出链+租入链+退租两事件）→PUR（9）→WHS（11·库存状态流转图）→BAS（9·两级维度+四价三段式+productTaxes）→FIN（11·应收应付四来源+分期互算+核销）→SYS（7·可审单据矩阵）→WF（7·16 类待办+?audit=1）→MOB（7·双键域登录态）——UC 共 89/AC 55，全部 Given-When-Then 强绑定；每模块 ≥1 Mermaid+状态流转含守卫条件+异常与边界（非功能并入）；字段说明表 9 列/每模块核心实体全列+统计口径公式行+表尾 A05 注记。计费与单据口径按 G22 后现状写死：三段式租价/无日租金/退租两事件/台账合并/「租赁出库」称呼（旧称呼 0）/待办 16 类含租赁出库审核。模块归属两处按 A02/菜单现状裁决（B3 BOM 归 BAS/B4 库存查询归 WHS）。

**T3**：五、单据流转（三链分述+总图+预收预付冲抵支线=Mermaid 2 张）｜六、接口时序（路凯数据对接 2 点+吉客云替换 3 项，全程标注「对接细节待客户方答复」）｜七、实时通信判定不产出（一句话+依据）｜质量检查 3 项在 g23_verify 36/36 基础上出结论：编号 PASS（三段标题各=1·UC 定义 89 无重复·序号连续）/追溯 PASS（AC 55 行对应用例列 100% 回链）/范围 PASS（10 模块全覆盖·测试账号输出块仅 1·In Scope 模块全覆盖）。

**术语修正 17 处**（g23_fix_terms.py+补 1）：运营方 2（预付运营方→预付供应商/路凯兼运营方→兼系统对接方）/在租台账 2（释义句改「G07 前独立页」）/费用分类→费用类型/叙述态裸单号 5→单据编号/语境外裸盘点 6→白名单复合词/分类下拉值→物料分类下拉值；修后 g23_verify 废弃词 22 词形全部 0 命中。

**T4 回写四件**：本档 ✅+执行记录+哈希｜_索引 G23 行（哈希 9daca20）｜_AGENT基线——当前任务块滚动 G23（G22 转「上一任务」）+文档地图加 P2-R01 行+P1-R01 版本行 V0.6→V0.7 更正（滞后清偿）｜P1-R01 附录仅两处——10.1「预留：P2」→「P2 已启用 2026-09-12」+10.2 加 P2-R01 行（P1-R05 行后插入）；其余正文零改动。

**验证门 6 条证据**：
1. `python _scan_tmpdir/g23_verify.py` → **36/36 PASS**（≥500 行=1377/章节计数 3×=1/10 模块三段各=1/UC 定义 89 重复 0/AC 55 行绑定 100%/mermaid 12≥11 每模块 ≥1/废弃词 22 词形逐词 0+组合出库 0/测试账号输出块 1/Out Scope 四模块各 ≥1/计费单价·租入资产入库方式·吉客云各 ≥1）——初版 2 处脚本匹配误报修正后复跑（B8），PRD 内容未随脚本返工
2. 原型零改动：140 文件 mtime 全部 ≤ 2026-09-12T09:54:52，违例清单=空
3. `git status --porcelain` P3-R01 前缀=0 行（改动=P2-R01 新建+四件+g23_* 工具，全在白名单）
4. 质量检查 3 项结论行：编号 **PASS**｜追溯 **PASS**｜范围 **PASS**
5. 回写四件 grep 证据（见验证门 5 输出贴收尾报告）
6. git 两段提交：工作批次 **9daca20**（G23 前缀·含 PRD+工具+失败清单）+收尾回写批次（次条）；未 push（本地领先 origin）

**默认决策命中**：D1 标准模式/D2 项目根单文件 P2-R01·V1.0·只产 md/D3 冲突按来源优先级裁决/D4 多字母代号 10 模块无撞码/D5 编排 PRJ→MOB/D6 字段表 9 列以模板为准/D7 术语 V0.6 零新增零改表/D8 MOB 入 In Scope+登录页归 MOB/D9 Mermaid 无 CDN/D10 G22 后现状（旧称呼 0）/D11 中文·UC 89 自然界定/D12 头部基线快照声明。表外最简默认：A02 第三节菜单名与实际文件名不一致时路径按实际文件名引用（产品档案.html 等 4 先例）。

**偏差闭环**：B1-B9 共 9 条（见 goal-failures-g23.md），全部闭环。

**失败清单结论行：失败 0 项 · 偏差 9 条闭环 · 无未决项。**
"""

t = open(tdoc, encoding="utf-8").read()
old_tail = "## 执行记录（收尾时填）"
if record.strip()[:20] in t:
    print("[SKIP] 执行记录已存在（幂等）")
elif t.count(old_tail) != 1:
    print("[FAIL] 执行记录锚不唯一"); ok = False
else:
    open(tdoc, "w", encoding="utf-8", newline="").write(t.replace(old_tail, record.rstrip("\n") + "\n"))
    print("[PASS] 执行记录追加")

# 3. 索引哈希回填
ok &= patch(idx, "| ✅ | {HASH} | 20260912-G23-PRD文档生成.md |",
            f"| ✅ | {H1} | 20260912-G23-PRD文档生成.md |", "索引哈希回填")

# 4. 基线当前任务块哈希回填
ok &= patch(base, "✅ **G23 PRD 文档生成（2026-09-12·哈希见 _索引·ZCode 无人值守·主机 Win 会话）**",
            f"✅ **G23 PRD 文档生成（2026-09-12·{H1}·ZCode 无人值守·主机 Win 会话）**", "基线哈希回填")

print()
print(">>> ", "全部成功" if ok else "存在失败")
sys.exit(0 if ok else 1)
