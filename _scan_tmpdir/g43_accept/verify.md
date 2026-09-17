# G43 独立验收报告（只读复验）

- 验收员：独立验收 agent（不信任执行者自述，全部取证命令自行执行）
- 日期：2026-09-17
- 工作目录：/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/
- 取证产物：本目录 g2_diff.py（门2脚本）、g3_assert_out.txt（门3完整输出）、g4_pw_out.txt（门4完整输出）

## 门 1 命令级 [PASS]

a) `osascript -l JavaScript` 编译 `P3-R01-包装租赁管理后台原型/_data/select-source.js` → 输出 `OK`
b) 同法编译 `P3-R01-包装租赁管理后台原型/_data/demo-data.js` → 输出 `OK`

证据：两条命令均实跑，返回值均为字符串 `OK`，无语法错误。

## 门 2 全量审计与 diff [PASS]

对 `_scan_tmpdir/audit_results_g43pre.json`（前态）与 `_scan_tmpdir/audit_results_g43post.json`（收尾）自行写脚本比对（g2_diff.py），汇总行：

```
(1) pages pre=133 post=133 equal_and_133=True
(2) post pages with problems>0: 0 -> True
(3) dead_links pre=0 post=0 all_zero=True
(4) js_errors non-net::ERR_ pre=0 post=0 (exempt net::ERR_: pre=0 post=2) -> True
(5) problem-key diff pre=0 post=0 NEW-in-post=0 -> True
GATE2 OVERALL: PASS (5/5)
```

说明：post 有 2 条 js_errors，均为 `net::ERR_CONNECTION_RESET`（P3-R01-F01-业务流程导航图.html），属断网豁免类；非豁免类 js_errors 两快照均为 0；⑤ 键差集（page/cat/type/where.tag/where.id/row[:24]/text[:16]/detail[:24]）新增为 0。

## 门 3 逐组断言复跑 [PASS]

自行运行 `python3 _scan_tmpdir/g43_assert.py`（exit=0），完整输出存 g3_assert_out.txt：103 行 [PASS]、0 行 [FAIL]，末尾总判定行：

```
总判定：103 PASS / 0 FAIL
```

占位清零检查：`grep -rl "待定选项（演示数据）" P3-R01-包装租赁管理后台原型/` → 无输出（exit=1，全目录 0 命中）。

## 门 4 渲染级抽验 [PASS]

自行运行 `python3 _scan_tmpdir/g43_pw.py`（exit=0），完整输出存 g4_pw_out.txt，末尾总判定行：

```
总判定：14 PASS / 0 FAIL
```

14 页（B 类 b01–b06 + A 类 a01–a08）值域断言＋联动断言全过；14 张截图已由本次运行写入 `_scan_tmpdir/g43_shots/`（文件时间戳 2026-09-17 09:48，共 14 个 PNG，非执行者遗留）。

## 总判定：4 PASS / 0 FAIL
