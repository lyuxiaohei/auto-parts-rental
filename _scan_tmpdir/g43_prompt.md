/goal 执行 G43 枚举接线与下拉数据源化——G30 遗留批次立项（基线六.17·道远 09-14 D-93 延续）：PC 全站 select 下拉改字典/实体渲染＋残留占位清洗＋陈旧遗留销账。工作目录（命令与全部相对路径之根，不依赖会话 cwd）：/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/

【交接文档 · 双层路由，先读全文再动手】
1. agent-handoff/_AGENT基线.md——项目铁律：第四节（历史事故与真相）＋第七节（上手清单）逐条适用
2. agent-handoff/20260916-G43-枚举接线与下拉数据源化.md——**任务总纲**：终态与跳过项／T0-T6 细则（含 A 类 20 组值源映射表·B 类措辞统一法）／默认决策表 11 条／验证门 6 条／失败处理／纪律
3. 底稿 _scan_tmpdir/g30_接线差集.md（09-14 时点·G36/G38/G39/G42 后部分过时·以 T0 重扫为准）＋样板：G34 dictOpts（基础数据/客商开票资料.html）＋G35 fill（仓储作业/库存查询.html）

【前置校验 · 先于一切】
1. _索引.md G43 行=⏳ 且基线无 G43 完成追记
2. backup-g43-20260916/ 与 agent-handoff/goal-failures-g43.md 均不存在
3. 单写者互斥：原型目录最近文件 mtime ≥30 分钟（尤其 _data/）；git log 无 G43 提交
4. git status --short 存档 _scan_tmpdir/g43_gitstatus_pre.txt；他人未提交原型改动→允许执行·提交注明「携带并行未提交改动」
任一阻塞性不符 → 写失败清单 agent-handoff/goal-failures-g43.md 后停止

【任务 · 细则全在任务书，此处仅路由】
1. T0 重扫差集（g43_scan.py→g43_接线差集_v2.md·页面×select×现值×目标源矩阵）＋开工备份触碰页与 _data→backup-g43-20260916/ ＋陈旧遗留销账（基线六.5/六.10/六.11/六.15②·索引 G32 行 T3——纯文档带证据划线）
2. T1 共享件 _data/select-source.js（dictOpts/fillDict/fillEntity·JXA 语法门）
3. T2 B 类字典渲染（重扫实有组·预估 14 组·措辞统一=字典 name 原文＋括号说明入 title；跳过 BF/ZQ/KW/FL）
4. T3 A 类实体渲染（20 组·partners/products/projects/locations/users·roles/todoItems 审核人并集/五单号组前 30 条倒序/账期近 12 期动态·银行账户跳过仅注记）
5. T4 残留占位清洗（「待定选项（演示数据）」全站=0·实测 6 处 5 页以重扫为准）
6. T5 验证门取证 → T6 回写三件＋A05/A02/P2-R01 D-153

【完成判定 · 证据全部贴进对话】
1. 命令级：select-source.js JXA new Function 编译退出 0＋demo-data.js 语法门 0——贴输出
2. 全量审计：开工快照 audit_results_g43pre.json → 收尾重跑 0 坏页（页数实测为准）＋g43pre 逐键 diff 新增 0——贴汇总行与 diff
3. 断言级：python 一键逐组断言（页面运行时 option 集合=运行时字典/实体值集合·Counter 比对·白名单「全部/其他（演示）/其他终端用户」）＋「待定选项（演示数据）」全站 grep=0——逐行 [PASS/FAIL] 贴输出
4. 渲染级：PW 抽验 ≥10 页（B 类≥5 组＋A 类≥5 组·表单与筛选两类）＋截图 ≥6 张存 _scan_tmpdir/g43_shots/
5. 独立验收：只读子 agent 按门 1~4 复验（自跑取证·不引用执行者自述·仅可写 _scan_tmpdir/g43_accept/）·结论逐项 [PASS/FAIL]＋总判定行原样贴对话；FAIL 修复重派（同项最多 2 轮）
6. 失败清单结论行（空清单给「无失败项」）
7. git 提交输出行（前缀 G43·禁 push·禁 add -A·只 add 本任务涉及文件与自有产物）

【约束】
- 无人值守：全程不得向用户提问；按任务书默认决策表执行，拿不准按最简合理默认并在收尾注明；一个 goal 会话内完成·幂等可续跑不重做
- 零改动红线：mobile/ 五页、业务口径与值域、?audit=1/打印机制、G30 白名单既有演示注记、m-auth/m-done/go()/mGuard；跳过 BF/ZQ（G21 两层口径）/KW（已接线）/FL（已并 WL）/银行账户（无实体·注记）
- 既有 5 页局部 dictOpts 不回归不删；「其他（演示）」等 append 保留；演示扩展值保留
- 读取-精确替换＋assert 计数＋幂等；HTML 改后标签配平；_data 每轮改动后语法门·失败即回滚本轮
- 单写者互斥全程有效（共享文件 mtime 突变→停手重读再继续）；禁 git add -A；收尾三件缺一不算完成（任务档＋索引＋基线）

or stop after 150 turns
