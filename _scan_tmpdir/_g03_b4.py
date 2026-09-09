# -*- coding: utf-8 -*-
"""G03 B4 收尾原子批：G03 文档✅+执行记录 / _索引.md G03 行 / _AGENT基线 快照终态 / 记忆库双写。
全部幂等：已含目标形态则跳过；替换类操作 assert 命中计数。"""
import io, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
done = []

def rw(path, pairs):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    for old, new, must in pairs:
        if new in s:
            print('跳过（已存在）:', p.name, new[:30]); continue
        n = s.count(old)
        if must:
            assert n == 1, f'{p.name} 期望1处实得{n}: {old[:40]}'
            s = s.replace(old, new)
        elif n:
            s = s.replace(old, new)
    p.write_text(s, encoding='utf-8', newline='')
    done.append(str(p))

# ── 1. G03 文档：头部✅+commit回填、执行记录 ──
g03 = ROOT / 'agent-handoff/20260909-G03-复验收与总收口.md'
rw(g03, [
    ('状态 ⏳ 待执行 ｜ commit：〈收尾回填〉',
     '状态 ✅ 已完成 ｜ commit：3b7092f（段1·spotcheck）+ 6f920c2（段2·收口文档）+ 本提交（段3·终锚）', True),
    ('（空·待执行后填写：提交哈希/各门证据/偏差与默认决策命中）',
     '''- **执行**：2026-09-09 无人值守三连跑 3/3 完成。前置校验 4 条全过（G03 锚 0／G01 dccaa23+G02 df4bda7 在案／_data 最近写入距今 312 分钟／备份在位／工作区 clean）。
- **B1**：`_scan_tmpdir/v32_spotcheck.py` 38 项断言（v3.1 复验收 14 项+v3.2 新断言 9 项+角色页数据驱动实测 9 项+其余结构与跳转）——**38 过 / 0 败**；提交①=3b7092f。首跑 2 败（A4/B3）经定位为断言脚本口径 bug（A4 项目管理组切片误跨组、B3 应付小标签归并误计组尾「项目损益」），按 C 表「修复一次→复跑该断言」修复后 38/38 全绿，**非原型缺陷，原型本 goal 零改动**。
- **B2**：P1-R01 附录 10.2 P3-R01 行尾追加「09-09·菜单重组 v3.2（G01-G03 三连跑）」记录句（同 v3.1 先例，不另起行不抹历史）。
- **B3**：失败清单 G03 行终态=失败 0 项+总结论行（G01-G03 全绿；G04 行保持「—」待下轮）；提交②=6f920c2。
- **B4**：三件套+基线终态+记忆库（p3r01-prototype-baseline.md 新建+MEMORY.md 索引行）——本提交（段3·终锚）。
- **默认决策命中**：记忆库 `p3r01-prototype-baseline.md` 实查不存在（基线声明的双写载体此前未落盘）→按 C 表「记忆库同步」语义新建该文件并补 MEMORY.md 索引行，与基线快照双写同步；抽验总数 38（≥16 下限达标）。
- **验证门证据**：①`==== 菜单重组 v3.2 抽验：38 过 / 0 败 ====` ②P1-R01 命中「菜单重组 v3.2」追加句 1 处 ③_索引 G01/G02/G03 三行 ✅ 且 commit 非空 ④基线含「菜单 v3.2」「111 页」、记忆库含 v3.2 现状句 ⑤失败清单总结论行=失败 0 项 ⑥git log 含「G03-复验收·执行」。''', True),
])

# ── 2. _索引.md：G03 行终态 ──
rw(ROOT / 'agent-handoff/_索引.md', [
    ('| G03 | 09-09 | v3.1 复验收+P1-R01 追加句+三连跑总收口 | ⏳ 待执行 | （收尾回填） | 20260909-G03-复验收与总收口.md |',
     '| G03 | 09-09 | v3.1 复验收+P1-R01 追加句+三连跑总收口 | ✅ | 3b7092f/6f920c2+段3终锚 | 20260909-G03-复验收与总收口.md |', True),
])

# ── 3. _AGENT基线.md：快照滚动至 v3.2 终态 ──
base = ROOT / 'agent-handoff/_AGENT基线.md'
rw(base, [
    ('`_data/demo-data.js` 增 roles 实体 9 条（G01）',
     '`_data/demo-data.js` 增 roles 实体 9 条（G01，demo-data 合计 **31 实体**=30+roles）', False),
    ('- **当前任务**：菜单重组 v3.2 四连投喂 ⏳（G01 角色管理数据驱动化 ✅ dccaa23（2026-09-09）→**G02 菜单 v3.2 侧边栏重写 ✅ df4bda7（2026-09-09）**→G03 复验收与总收口→G04 三连跑独立验收·纯只读 20 项；G03/G04 两条命令按序投喂（各自全新会话），全史锚+前置链校验，共享备份 backup-menuregroup32-20260909（已建·117 文件）与失败清单 goal-failures-menuregroup32-20260909.html）；**任务总账=`agent-handoff/_索引.md`**',
     '- **当前任务**：菜单重组 v3.2 四连投喂（G01 角色管理数据驱动化 ✅ dccaa23→G02 菜单 v3.2 侧边栏重写 ✅ df4bda7→**G03 复验收与总收口 ✅ 3b7092f/6f920c2+段3终锚**→G04 三连跑独立验收·纯只读 20 项·待投喂；2026-09-09，共享备份 backup-menuregroup32-20260909 与失败清单 goal-failures-menuregroup32-20260909.html 留档，三连跑总结论=失败 0 项）；**任务总账=`agent-handoff/_索引.md`**', True),
])

# ── 4. 记忆库：p3r01-prototype-baseline.md + MEMORY.md 索引行 ──
memdir = None
proj = Path(r"C:\Users\Administrator\.claude\projects")
for d in proj.glob('D*5--ACTIVE*/memory'):
    if (d / 'package-rental-project-facts.md').exists():
        memdir = d; break
assert memdir, '记忆库目录未定位'
print('记忆库目录:', memdir)

mf = memdir / 'p3r01-prototype-baseline.md'
if not mf.exists():
    mf.write_text('''---
name: p3r01-prototype-baseline
description: P3-R01 原型基线现状（与 agent-handoff/_AGENT基线.md 双写同步）：111 页/菜单 v3.2/demo-data 31 实体/G01-G03 三连跑完成
metadata:
  node_type: memory
  type: project
---

P3-R01 包装租赁管理后台原型基线现状（2026-09-09 G03 收口，与 `agent-handoff/_AGENT基线.md`「当前基线快照」双写同步）：

- **111 页**=40 业务页（含 系统管理/角色管理.html）+ 独立弹窗模板（G01 新增 弹窗/权限配置.html、弹窗/新增角色.html）+ F01 导航图（v3.0 唯一演示图）。
- **菜单 v3.2 终版**（G02，40 页侧边栏统一）：八组序=项目管理(项目看板/项目列表)→基础资料→采购管理→销售管理→租赁管理→仓储管理→财务管理→系统管理；我的待办一级；**项目损益=财务管理组尾普通项「项目损益」**（→财务协同/盈亏报表.html）；组名 财务协同→财务管理、仓储作业→仓储管理（仅侧边栏标签层，目录名与文件零移动）；小标签恰 8 处；盘点录入退出菜单（其页 selected=盘点）。
- demo-data **31 实体**=30+roles（G01 增 roles 9 条 RL-01~RL-09；角色管理页 renderListPage 接线 noCheckbox/keyHtml 模式，openRolePerm 权限配置弹窗=9 项勾选矩阵+数据权限三单选，新增角色 createModal 三字段=角色名称/说明/数据权限范围）。
- 验证资产：audit_interaction.py（111 页 死链 0/JS 0，F01 豁免，相对执行前基线 diff 新增 0）、verify_listfull.py 三批 100/88/55、v32_menu_verify.py 14 项、v32_spotcheck.py 38 项（v3.1 复验收+v3.2 新断言+角色页实测）；失败清单 `goal-failures-menuregroup32-20260909.html` 总结论=失败 0 项。
- 三连跑（2026-09-09 全部完成）：G01 dccaa23→G02 df4bda7→G03 3b7092f/6f920c2+段3终锚；任务总账=`agent-handoff/_索引.md`；历史全量=P1-R05 冻结版。

**Why:** 接手会话先读本条+_AGENT基线.md 即得菜单/页数/实体数现行口径，避免引用冻结版 v3.1 前旧口径。
**How to apply:** 菜单/侧边栏相关改动以 v3.2 八组序为基准；改完滚动本条与 _AGENT基线.md「当前基线快照」双写。
''', encoding='utf-8', newline='')
    print('记忆库文件已建:', mf)
else:
    print('记忆库文件已存在，跳过:', mf)
done.append(str(mf))

mm = memdir / 'MEMORY.md'
s = mm.read_text(encoding='utf-8')
line = '- [P3-R01 原型基线现状](p3r01-prototype-baseline.md) — 111 页/菜单 v3.2 八组终版/demo-data 31 实体（30+roles）/G01-G03 三连跑 2026-09-09 完成'
if 'p3r01-prototype-baseline.md' not in s:
    s = s.rstrip('\n') + '\n' + line + '\n'
    mm.write_text(s, encoding='utf-8', newline='')
    print('MEMORY.md 索引行已加')
else:
    print('MEMORY.md 索引行已存在，跳过')

print('B4 改写完成:', len(done), '文件')
