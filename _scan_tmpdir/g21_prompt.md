/goal 执行 G21 租价计费三段式改造（物料档案两租价结构化 + 计费方式字典落地 + 租入单域口径统一；前置语境：G20 已收尾 ✅ 6f38c32）。工作目录（命令与全部相对路径之根，不依赖会话 cwd）：`D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\`

【交接文档 · 双层路由，先读全文再动手】
- `D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\agent-handoff\_AGENT基线.md`——项目铁律：第四节（历史事故与真相）+ 第七节（上手清单）逐条适用
- `D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\agent-handoff\20260911-G21-租价计费三段式.md`——本 goal 全量细则：前置校验 6 条 / 第 0 步阅读清单 / 任务三组 / 默认决策表 8 条 / 验证门 7 条；一切锚文本、写死字符串、计数预期以该文档为准

【前置校验 · 先于一切】
1. `_索引.md` 有 `| G20 |` 行且 ✅+commit 非空；无 G21 行
2. `demo-data.js` 不含 `rentInMode`；`系统管理/数据字典.html` 不含「按年计租」
3. 原型目录与 `agent-handoff/` 最近文件 mtime ≥30 分钟（单写者互斥）
4. `git status` 有改动先存档提交（不 push）；原型 HTML 总数=115；建 `backup-g21-20260911/`
——任一不符 → 停止并写失败清单（路径见下），逐条处理口径见任务文档前置校验节

【任务】
- T1 计费方式字典落地为值源：dictItems 追加 BF-04 按年/BF-05 按日 + BF-03 按张停用；数据字典.html 静态卡片 5 行+去暂估+cnt 3→5；pin-2「计费方式（预留）」改文案走 A03/A04 双轮重注入
- T2 档案两租价三段式（形态 B）：demo-data products 12 行加 `rentInMode/rentInPrice/rentalMode/rentalPrice` 四键（值表写死于文档）；产品档案 createModal 与新建产品模板两表单行→「计费方式（按时间周期/按次）+周期单位（月/年/日默认月）+数值」三段控件+单位后缀联动 JS；列表 cells 与详情 info 零改动
- T3 租入单域口径统一：段标题×2 与明细 select×4「月租/按套→按月/按次」+ rentInOrders feeSecTitle×5 + 项目详情「按天计租 · 按张计费」残留清除；改后全站 按天=0、元/天=0
——全部改动点、写死字符串与不动项见任务文档任务节

【完成判定 · 证据全部贴进对话】
1. `python _scan_tmpdir/g21_verify.py`（新建留档）→ 逐行 PASS（逐项计数预期写死于任务文档验证门 1）
2. `node --check P3-R01-包装租赁管理后台原型/_data/demo-data.js` → 退出码 0
3. `python _scan_tmpdir/audit_interaction.py` → 死链 0 / JS 错 0（115 页）；`python _scan_tmpdir/g17_audit_diff.py` → 新增问题 0
4. `python _scan_tmpdir/v32_menu_verify.py` → 14/14；`python _scan_tmpdir/verify_listfull.py` 三批 → 现行口径全过
5. `python _scan_tmpdir/g21_pw.py`（留档）→ 5 用例 PASS/FAIL 清单 + 截图 `_scan_tmpdir/g21-*.png`（用例明细写死于任务文档验证门 6）
6. A03→A04 双轮重注入 → 输出「零告警」行

【约束】
- 无人值守：全程不需要也不得向用户提问；默认决策表 8 条内事项按表执行，表外按最简合理默认执行并在收尾报告注明
- assert 失败/锚点不匹配 → 跳过该项 → 记入 `D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\agent-handoff\goal-failures-g21.md`（任务号/文件/原因）→ 继续下一项；禁止卡死等待、禁止猜测性改写、禁止静默吞掉；收尾必须含失败清单结论行（空清单给「无失败项」）
- 精确替换+assert 计数+幂等；HTML 块改动配平自检；改内嵌 JS 字符串后必跑该页 audit；中文路径 python 内嵌处理；禁裸 open('w') 整页写入；验证数字自重跑
- 收尾回写三件（硬性）：任务文档标 ✅+执行记录+commit 哈希回填头部；`_索引.md` 挂 G21 行；`_AGENT基线.md` 快照滚动；A05 四价登记块与 dictItems 变更同步
- git 批次（硬性）：`git add -A && git commit`（信息前缀 G21，禁 push），哈希回填任务文档与索引行
