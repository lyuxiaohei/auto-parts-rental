# G50 移动端样板风样式优化 · 独立验收结论（验收员自查取证）

- 日期：2026-09-16（本机实测，未引用执行者自述）
- 方法：全部命令由验收员亲自执行；审计重跑日志 `g50_accept/audit_rerun.log`，PW 输出 `g50_accept/pw_out.txt`，PW 脚本 `g50_accept/g50_accept_pw.py`；重跑前的 audit_results.json 已备份为 `g50_accept/audit_results_prev_round.json.bak`
- 原型文件零修改（只读复验），唯一写入位置 `_scan_tmpdir/g50_accept/` 与审计脚本自身产物 `audit_results.json`

## 逐项结论

1. [PASS] 门1-全量审计重跑 —— `python3 _scan_tmpdir/audit_interaction.py` 退出码 0；汇总 133/133 页全 0，坏页 0（problems=0/死链=0/JS错=0 全站）。
2. [PASS] 门1-mobile五页各自 —— 审批详情/库存查询/待办审批/我的/登录 五页均 problems=0、dead_links=0、js_errors=0。
3. [PASS] 门1-与g50pre逐键对比 —— 重跑 audit_results.json 与 audit_results_g50pre.json：页集完全一致（133=133，无新增/减少页）；共有页 problems/dead_links/js_errors 三键 diff=0（另查 nav_anomaly 差异亦为 0）。g50pre 本身 133 页 0 坏页属实。
4. [PASS] 门2-_m.js 零改动 —— `diff -q` mobile/_m.js 与 backup-g50-20260915/mobile/_m.js 相同；SHA-256 双方均 `85ccf4fc6d386ad9ce053d59c1c5a73c79786def65729503bf844ca209da9a3e`；`git diff` 对 HEAD 亦无改动；`osascript -l JavaScript` new Function 语法校验 SYNTAX OK（3761 字符）。执行者"零改动跳过 node --check"声明的证据基础成立。
5. [PASS] 门3-登录页（净上下文） —— `.m-logo`=1；品牌名「汽车物流包装租赁」；#m-btn-login=1、#m-btn-wx=1；页面文本含 v1.2；pageerror=0。
6. [PASS] 门3-待办审批 —— `.m-stat-item`=3；`.m-item`=20（≥1）；配色类徽标 40 个、首个 `m-badge m-badge-blue`（命中 m-badge-blue/orange/green/purple/gray/red 之一）。
7. [PASS] 门3-审批详情 —— 取 window.DEMO_DATA.todoItems 首键 SO-20260910-0047 带 ?id= 访问：`.m-banner` 可见且 `#m-banner-state`="待审核"（非空）；`.m-tl-item`=2；`.m-action-bar .m-btn`=2（≥2）。
8. [PASS] 门3-我的 —— `.m-hero`=1；三格与页面内实算逐一相等：#m-st-todo 20/20（todoItems 行数）、#m-st-done 0/0（m-done 键数）、#m-st-type 20/20（类型去重数）；`.m-cell-group .m-cell`=4；文本含 v1.2。
9. [PASS] 门3-库存查询 —— `.m-chip`=6（实测 6 而非任务书第九节所写 7；构成=KC 字典五状态＋全部，与验收指令预期一致）；单行性：所有 chip getBoundingClientRect().top 取整去重={122} 单值；#m-list 卡片=15（≥1）；pageerror=0。
10. [PASS] 门3-守卫回归 —— 无 init_script 净上下文访问库存查询.html，1.4s 后 URL unquote = `file:///…/mobile/登录.html`（跳回登录页）。
11. [PASS] 门3-五页JS错误 —— 登录/待办/详情/我的/库存 pageerror 合计 0。
12. [PASS] 门3-截图 —— `_scan_tmpdir/g50_after/` 恰 5 张 PNG 且非空有效（01-登录 375×812、02-待办审批 407×2844、03-审批详情 407×898、04-我的 407×812、05-库存查询 407×2326）。
13. [PASS] 门4-PC类名grep —— 宽松式 `class="[^"]*(modal|btn|filter-bar)` 命中 6 处（登录×2、审批详情×3、我的×1），逐处甄别全部为 `m-btn`/`m-btn-*` 前缀假阳性；等价 PCRE 负向断言 `class="[^"]*(?<![\w-])(?:modal|btn|filter-bar)\b`（排除 m- 前缀，python3 实现，本机无 GNU grep -P）命中 0。
14. [PASS] 门4-go(次数不减少 —— 五页 cur/bak：登录 2/2、待办审批 1/1、审批详情 3/3、我的 1/1、库存查询 0/0，全部相等未减少。
15. [PASS] 门5-改动面 —— `git status --short` 限定 P3-R01-包装租赁管理后台原型/ 下改动恰为 mobile/ 六文件（五页＋_m.css），`git diff --stat`＝6 files changed, 146 insertions(+), 10 deletions(-)；_m.js 未改；PC 页面、_data/demo-data.js 零改动。仓库其余改动仅为 _scan_tmpdir 产物、agent-handoff 任务书/goal 文档与 backup-g50-20260915/（流程留痕，原型目录外）。

## 备注

- 库存查询 chip 计数：任务书第九节门3原文写「7 个 chip 不换行」，实测 DOM 与源码均为 6（全部/在库/客户端(租出)/客户转租出/退租待入库/租入，对应 KC-01~KC-05 五状态＋全部）。与验收指令「实测应为 6」一致，单行性成立，不构成 FAIL；差异源于任务书文字口径，建议下次任务书修订。
- 审计对比基线按验收指令使用 g50pre（而非 g41baseline），g50pre 133 页 0 坏页已由本验收员独立复核。

## 总判定

总判定：15 PASS / 0 FAIL
