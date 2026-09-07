# /goal 弹窗美观化 失败/事故清单（2026-09-05）

## 最终遗留豁免（2 项，均为规则内豁免非失败）
- >34 字长文案豁免 ×1：文本天然换行（详见 modal-fix-summary.json exempt_longtext）
- 基础数据/BOM.html ×1：门禁要求不动，其违例只测不改（modal-fix-summary.json exempt_bom）

## 事故记录（均已当次修复，未遗留）
1. **BOM.html 误改（已还原）**：goal_modal_beauty.py 排除名单写正斜杠 `基础数据/BOM.html`，Windows rglob 相对路径为反斜杠 → 排除未生效，BOM.html 被①②误改。因该文件另有前次任务未提交改动（modal-lg 780/菜单重组）不能 git 还原，按精确逆替换还原，复核 git diff 仅剩既有 8 行改动。脚本留档版已改反斜杠。
2. **行盒聚类 bug（已重放修复）**：goal_modal_fix.py 首版用 round(top/10) 聚类判行数，十进制边界（如 184.2→18 / 187.0→19）把同一行拆成两行，tag 行被误判多行 → 产生误修复。发现后从备份整体还原全部文件 → 重放①②③（确定性脚本）→ 以正确聚类（top 排序+10px 容差锚点法）重跑④，最终违例 0、无伪影残留。
3. **F01 JS 错 1 条（瞬态，非本任务）**：全量审计中 F01 报 ERR_CONNECTION_RESET——其 <link> 引 fonts.googleapis.com 外链，一次网络抖动；单独复测 F01 0/0/0。F01 本任务未触碰。
4. **交接文档追加被 bash 吃反引号（已修复）**：内联 python -c 里的 Markdown 反引号被 bash 当命令替换，写入内容 4 处代码空缺；goal_fix_handoff.py 精确修复，反引号 8 对配平。
5. **还原后一次 write OSError Errno 22（瞬态文件锁）**：还原备份后立即重放时 1 个文件写入失败（疑似杀毒瞬时锁），重试成功；终态经磁盘核验（480 残留 2=BOM 预期、A/B 形态 123/123、dval 旧 1=BOM、drow 全宽 29）。
