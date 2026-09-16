# G42 独立验收复验记录（只读）

- 验收员：独立只读子 agent（未引用执行者自述，全部证据为实测）
- 日期：2026-09-16
- 对象：`/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型`（下称 P）＋ `_data/demo-data.js`
- 断言真值源：`agent-handoff/20260916-G42-闭环缺口修复与数据补齐.md`（任务组 T1~T11「断言」行）
- 方法：JXA `new Function` 编译/运行时提取（本机无 node 的先例口径）＋ python 正则 ＋ Playwright chromium 渲染
- 取证脚本：`_scan_tmpdir/g42_acc_*.js|py`

## 逐项结论

[PASS] 1 语法门 —— `osascript -l JavaScript` + `new Function(src)` 编译 demo-data.js：`COMPILE_OK length=645474`（退出 0）。

[PASS] 2 T1 BOM维护 —— `基础数据/BOM维护.html`：`提交审核` grep 0 次；`暂 存` 1 次、`取 消` 1 次（均在 submit-bar）。

[PASS] 3 T2 付款死引用 —— demo-data.js 全文件 `AP-20260810-002` = 0 次；运行时提取 `payments['PAY-20260818-001'].row.fields.ref = "AP-20260815-003"`，`payableBills` 13 键实测清单含 `AP-20260815-003`（refInKeys=true；info 关联应付/fees/chain/timeline 四处均为 AP-20260815-003，一致）。

[PASS] 4 T3 租赁单新建/列表 —— 新建页「所属项目」select 内 PRJ-2601~2606 各恰 1 个 option（select 内计数 1/1/1/1/1/1，全文件亦各 1）；select 内「东海商用」「星途」「长风汽制」0 次（三词在全文件的出现位于「客户：」下拉的客商全称「东海商用汽车有限公司宁波分公司/星途新能源汽车科技有限公司/长风汽车制造有限公司」，非所属项目 select，属合法客户选项）；`租赁单列表.html` 筛选 `<option>PRJ-2606</option>` 1 次。

[PASS] 5 T4 应收账单预收 —— `财务协同/应收账单.html` 类型筛选含 `<option>预收</option>`；运行时 dictItems「应收账单类型」组=7 行：ARB-01 租赁费…ARB-06 预付款（保证金）、ARB-07 预收；`系统管理/数据字典.html` 静态卡「应收账单类型」`<span class="cnt">7</span>`；演示行 `AR-2026-09-PRJ2601-YS` 仍在 receivableBills（PRJ-2601·安吉智行物流·预收·已收）未动。

[PASS] 6 T5 用户权限 —— head-btns 实测：`<button class="btn btn-default btn-sm" onclick="go('../系统管理/权限配置.html')">权限配置</button><button ...>新增用户</button>`；head-btns 行内「角色管理」0 次（全文件 3 处均为侧边导航菜单链接与 pnp 说明卡文案，非头部按钮）。

[PASS] 7 T6 应收生成残留 pin —— `财务协同/应收生成.html`：`FP3-01` 0 次、`proto-pin` 0 次、`protoNotesFab` 0 次、含「标注」的按钮 0 个（「标注」字样全 0）；div 开 91 = 闭 91 配平；业务关键词账单类型/计费模式在位（渲染见第 14 项同源机制，本页由 T6 静态计数证明）。

[PASS] 8 T7a partners 税号 —— 运行时 partners=8 键（DW-0001~0004、DW-0101~0103、DW-0201）8/8 有 `invoiceTaxNo`，全部 18 位、9 开头、第 3~8 位=131015、第 9~17 位=MA1F+A0001~A0008（序号递增）、末位数字（4/5/6/7/8/9/0/1）：91131015MA1FA00014 / …A00025 / …A00036 / …A00047 / …A00058 / …A00069 / …A00070 / …A00081；partners 8/8 的 info2 开票资料段含「纳税人识别号」行；`客商详情.html?id=DW-0001` 渲染后实测含「开票资料/纳税人识别号/91131015MA1FA00014」（见第 14 项，0 JS 错）。

[PASS] 9 T7b 排查报告 —— `_scan_tmpdir/g42_detail_newfield_diff.md` 存在（34 行），末行 `**修复后差集：0**`。

[PASS] 10 T8 转租退租演示行 —— 运行时计数：returnInbounds=10 键（`TZRK-20260915-012` 在键）、stockEvents=23 键（`EV-20260915-023` 在键）、stockFlows=18 键（未动）。

[PASS] 11 T9 租入押金 —— rentInReturns=3 行 info 均含「押金」：GHCK-20260903-001（已归还·RZD-20260815-003）`押金退还: ¥84,000.00 原路退回`、GHCK-20260903-002（待审核·RZD-20260815-005）`押金退还: ¥12,000.00（归还审核通过后原路退回）`、GHCK-20260831-003（已归还·RZD-20260701-001）`押金退还: ¥10,800.00 原路退回`——三笔金额与关联租入单押金字段实测值 84,000/12,000/10,800 一致；`租入归还审核.html` 含「押金随归还审核原路退还」1 次。

[PASS] 12 T10 单号互通 —— Counter 逐单号（非 set）：projectDocs/boardRows/profitRows 三实体 `AR-`/`AP-` token 共 18 次出现、10 个唯一单号（AR-2026-08-PRJ2601、AR-2026-07-PRJ2601、AP-20260901-008、AR-2026-08-PRJ2602、AP-20260830-007、AR-2026-08-PRJ2603、AP-20260903-009、AR-2026-09-PRJ2604-S1、AP-20260903-010、AR-2026-09-PRJ2603-U1），100% ∈ receivableBills(17 键)∪payableBills(13 键)，notInKeySet=[]；旧假单号 `AR-20260905-0029`、`AR-20260831-0028` demo-data.js 全文件 0 次。

[PASS] 13 T11 退款扩值 —— 退款新建.html 四值各 3 次（select+form-tip）；退款登记.html 四值全在（采购退货退款 4/销售退货退款 2/预收退回 1/多付退回 1，渲染实测含「采购退货退款（供应商·我方收款）」「销售退货退款（客户·我方付款）」）；dictItems 退款类型 TKL 组=4 行（TKL-01 采购退货退款/TKL-02 销售退货退款/TKL-03 预收退回/TKL-04 多付退回）、退货类型 THC 组仍=2 行（收货拒收/入库后退货）不受扰；数据字典「退款类型」cnt=4；refunds=5 键（TKD-20260914-001/002/003+新增 004/005），TKD-20260916-004=待审核·预收退回·关联 AR-2026-09-PRJ2601-YS·20,000.00，TKD-20260916-005=已确认·多付退回·关联 AP-20260905-012·10,000.00；demo-data.js 与两退款页「应付退款（对供应商）」「应收退款（对客户）」均 0 次；payableBills['AP-20260905-012'].timeline 实测含 `多付退回落单 · 退款登记 TKD-20260916-005（¥10,000 原路退回）`。

[PASS] 14 渲染抽验 —— Playwright chromium 3 页 file:// 加载，pageerror 收集 JS 错=0，业务 token 全在位：①客商详情?id=DW-0001（开票资料/纳税人识别号/91131015MA1FA00014）②退款登记（采购退货退款（供应商·我方收款）/销售退货退款（客户·我方付款）/预收退回/多付退回）③损益报表（表格行含 AR-2026-08-PRJ2601）。

[PASS] 15 旧 token 全库 —— P 目录（html/js/md；实测无 backup-* 目录需排除）grep：`AP-20260810-002`=0、`应付退款（对供应商）`=0、`应收退款（对客户）`=0；`待转移` 仅 1 处＝`P3-R01-A05-字段字典.md:910` 枚举沿革注记行（「待转移改待审核·审核页承载」），`确认转移`=0——均在允许范围（A05/A06 沿革注记）。

## 附注（非断言项观察，不计判定）

- T9「押金标准待客户」注记：全库（html/js/md，含旧 20260911 zip 抽查）0 处，未见被删痕迹（该词形历史上即不存在于现存文件），不构成断言违背。
- 任务书中的 Windows 绝对路径（D:\…）与本机 macOS 路径已按项目根映射执行。

总判定：15 PASS / 0 FAIL
