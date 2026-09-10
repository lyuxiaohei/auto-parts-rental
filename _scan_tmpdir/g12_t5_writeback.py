# -*- coding: utf-8 -*-
"""G12 T5：三件回写（任务文档/_索引/_AGENT基线）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HASH = 'd9aa5b1'

# ===== 1. 任务文档 =====
p = r'agent-handoff\20260910-G12-数据驱动查漏收口.md'
txt = open(p, encoding='utf-8').read()
old_head = '> **状态**：⏳ 待执行 ｜ **commit**：（执行后回填） ｜ **起草**：2026-09-10 道远拍板（G11 之后、G13 会议功能补全之前）'
new_head = '> **状态**：✅ 已完成（2026-09-10） ｜ **commit**：d9aa5b1（+开工前存量存档 29e4496） ｜ **起草**：2026-09-10 道远拍板（G11 之后、G13 会议功能补全之前）'
assert txt.count(old_head) == 1
txt = txt.replace(old_head, new_head, 1)

rec = '''## 执行记录（2026-09-10 · commit d9aa5b1）

**前置校验**：①单写检查——F01 两文件 5~7 分钟前有写（另一会话 v3.4 重写 WIP），120 秒复采样无推进+demo-data.js 149 分钟静默 → 按基线七.0.② 先存档提交 29e4496 分股后开工（偏差留档 goal-failures §1）；②commit 哈希为空 ✓；③audit 自跑存 audit_results_g12baseline.json ✓；④复扫 **12 业务页+43 弹窗**未引（任务书 11+43——多出「我的待办.html」以实扫为准收口，偏差留档 §2）→ g12-scan.json。

**T1**：g12-metrics.json 提取 55 文件结构指标 → g12-classify.json：**A=9 页**（我的待办 15 行/操作日志 10/数据字典=道远点名/用户权限 11/项目档案 7/项目详情 6 主表/BOM 预分类 A/盈亏报表·混合/项目看板·混合）+ **B=46**（盘点录入/组合出库录单/采购入库录单 3 录单页+43 弹窗全 maxrow≤5）。

**T2**：demo-data.js 存量复核 28 实体（任务书写 31，以实数为准）→ 新增 9 实体（28→37）：opLogs 12/users 12/dictItems 45（10 分类）/todoItems 12/projects 8/projectDocs 11/boardRows 6/profitRows 6/bomList 6；补丁：todoItems+time、profitRows+code（list-generic select 分支不认 _key）；_meta 滚动 2026-09-10。

**T3**：7 页 renderListPage（操作日志 noOps/用户权限 stabField=side/项目档案[含嵌套 span 标签精确匹配]/项目详情 stabField=type/BOM/盈亏报表 noOps/项目看板）+2 页自写渲染器（我的待办：#todoBody 实体重建+filterTodo 原逻辑不变+统计卡计数联动；数据字典：dic-item 分类切换+标题/计数/pager 联动+空态占位）。**list-generic.js 增 noOps 开关**（无操作列页；顺带 ops 缺失防御，向后兼容，偏差留档 §4）。备份 backup-g12-20260910/（10 文件）。

**T4**：agent-handoff/g12-whitelist.md——B 页 3+弹窗 43 逐文件+6 条页内静态块附注（用户权限角色二表 openRolePerm 依赖/数据字典计费方式卡 3 行/混合页卡片区/盈亏聚合页签/两个演示占位下拉）。

**T5 验证门证据**：
1. audit 门 PASS：108 页 死链=0 JS错=0，相对 g12baseline 逐键 diff 新增=0（g12_gates1.py 输出）。
2. grep 门 PASS：A=9，含 demo-data.js 引用=9（N=N，逐文件 ✓ 清单见 g12_gates1.py 输出）。
3. PW 门 PASS 4/4（g12_gate3.py）：数据字典 分类切换 缺损6→银行账户3→支付方式2+标题/计数联动；操作日志 12 行（≥6）筛选「操作类型=新增」→5；用户权限 12 行筛选「所属方=客户」→4；项目档案 8 行筛选「客户名称=一汽解放」→3。
4. 白名单门 PASS：git 改动 37 文件 ∩ B 类 46 文件 = ∅。
5. 回归门 PASS：verify_listfull 三批 100/88/43 断言失败 0（batch3 清单修复 G07 陈旧引用：租出台账→租赁单列表·在租台账删除·宿主库存查询 batch1 已覆盖，偏差留档 §3）。
6. 失败清单门 PASS：goal-failures-g12-20260910.md 存在+结论行（失败 0/偏差 5）。
7. 收尾门：提交 d9aa5b1（47 文件 +27288/-39）；推送结果见下。

**偏差汇总**（全文见 goal-failures-g12-20260910.md）：①前置校验1 字面偏差（F01 WIP，分股存档处置）②实扫 12 页 vs 任务书 11 页（我的待办收口为 A 类）③batch3 工具陈旧修复 ④noOps 开关增补 ⑤A 页内局部静态块 6 处附注。失败 0 项。'''
txt = txt.replace('## 执行记录（执行后填写）\n\n（占位）', rec.rstrip())
assert '## 执行记录（2026-09-10' in txt
open(p, 'w', encoding='utf-8', newline='\n').write(txt)
print('1/3 任务文档回写 ✓')

# ===== 2. _索引.md =====
p = r'agent-handoff\_索引.md'
txt = open(p, encoding='utf-8').read()
old = '| G12 | 09-10 | 数据驱动查漏收口（54 未引文件分类判定[A 应驱动/B 白名单]·A 类接 renderListPage+激活筛选·数据字典字段分类交互=道远点名·demo-data 实体查重补齐·g12-whitelist.md 留档·audit diff 新增 0+PW 抽 4 页） | ⏳ | 待执行 |'
new = '| G12 | 09-10 | 数据驱动查漏收口（实扫 55 未引文件[12 页+43 弹窗·多出我的待办]分类 A=9/B=46·A 类 7 页 renderListPage+2 页自写渲染器[我的待办实体重建/数据字典分类切换=道远点名·计数联动]·demo-data 28→37 实体[+opLogs/users/dictItems/todoItems/projects/projectDocs/boardRows/profitRows/bomList]·list-generic 增 noOps·g12-whitelist.md 46 文件·七门全过[audit diff 0/grep 9=9/PW 4/4/白名单∅/verify 100·88·43/失败清单 0 失败 5 偏差]·batch3 清单修复 G07 陈旧） | ✅ | d9aa5b1 |'
assert txt.count(old) == 1
txt = txt.replace(old, new, 1)
open(p, 'w', encoding='utf-8', newline='\n').write(txt)
print('2/3 _索引 G12 行回写 ✓')
