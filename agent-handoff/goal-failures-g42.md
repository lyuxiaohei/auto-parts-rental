# G42 失败清单（闭环缺口修复与数据补齐 · 2026-09-16）

> **结论：无失败项**。以下为登记性记录（过程性事故均已当轮发现、当轮修复、终验全绿），不影响完成判定。

## R-1 · T10 projectDocs 替换行漏条目闭合 `}`（当轮修复）

- 现象：e2_new（AR-2026-07-PRJ2601 行）行尾 `]}},` 少一个条目闭合 `}`，JXA 语法门报 `line 17328: Unexpected token ';'`（实际为未闭合结构在 EOF 外溢报）。
- 证据：`osascript -l JavaScript` 编译失败复现；python repr 行尾实勘 `…应收账单.html')"}]},`。
- 处置：三步修复（补逗号→正则修引号→按 `]} },` 标准形态补 `}`），修复后语法门＋T10 Counter 断言全过。原状可回溯 `_scan_tmpdir/g42_dd_broken.js`。
- 教训：单行 JS 实体行尾三连闭合（row/entry）在模板串里最易掉一个；写模板时以邻行行尾逐字符比对。

## R-2 · T7b 实体键缩进异常致首轮漏插 6 行（当轮补插）

- 现象：locations/XNC-AJZX（5 空格）、RA-A-01-01（3 空格）、rentInOrders/RZD-20260910-009 的键行不符 4 空格标准缩进，首轮正则 `\n    'KEY': {` 未命中 → 273/273 预期差 6 行。
- 证据：`g42_t7b_check.js`（每记录新标签断言）报缺 6 处。
- 处置：3 键定向补插（风格自动探测），复跑断言 `缺 0 处`，终扫复查差集 0。

## R-3 · stockFlows=18 与任务书预估 17 不符（实测口径·非缺陷）

- 现象：T8 断言「stockFlows 快照不动」时实测 18 键，任务书语境沿用的 17 系 G25 期旧值（G37 曾 +XNC-ZZ-PLT2/PLT 两行）。
- 证据：开工前备份 `_scan_tmpdir/g42_dd_backup/demo-data.js.bak` JXA 实数 = 18 = 完工后 18（未触碰）。
- 处置：按默认决策 9「收尾数字一律运行时实算」改按 18 判定；文档引用同步 18。

## 附 · 环境说明

- 本机（副机 macOS）无 node（`command not found`）：语法门与数据断言全程以 `osascript -l JavaScript` 的 `new Function` 编译/执行等价替代（G22 先例·检查器 `_scan_tmpdir/g42_jxa.js`），验证门 1 的「node --check」以该等价口径满足并在对话注明。
