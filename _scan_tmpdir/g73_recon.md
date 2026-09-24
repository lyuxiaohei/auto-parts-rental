# G73/G74 任务排查底稿（生成单跳转 + 批量审核铺开）

## A. 批量审核现状
- 已有批量审核: P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图/P3-R01-F01-业务流程导航图-退租归还与财务.html
- 已有批量审核: P3-R01-包装租赁管理后台原型/租赁管理/退租入库列表.html
- 已有批量审核: P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html

## A2. 含「审核」op 的实体 → 列表页/行
- leaseOrders（2 行: ZL-20260823-033,ZL-20260901-032）
    - 列表页: P3-R01-包装租赁管理后台原型/租赁管理/租赁单列表.html
- rentInOrders（1 行: RZD-20260902-008）
    - 列表页: P3-R01-包装租赁管理后台原型/租入管理/租入单列表.html
- comboOutbounds（11 行: CK-20260910-022,CK-20260914-023,CK-20260912-024,CK-20260903-016,CK-20260830-015,CK-20260830-014,CK-20260829-013,CK-20260829-012,CK-20260828-011,CK-20260824-009,CK-20260828-010）
    - 列表页: P3-R01-包装租赁管理后台原型/租赁管理/租赁出库列表.html
- returnInbounds（3 行: TZRK-20260902-010,TZRK-20260903-009,TZRK-20260902-008）
    - 列表页: P3-R01-包装租赁管理后台原型/租赁管理/退租入库列表.html
- rentInReturns（1 行: GHCK-20260903-002）
    - 列表页: P3-R01-包装租赁管理后台原型/租入管理/归还出库列表.html
- purchaseOrders（1 行: PO-20260910-019）
    - 列表页: P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html
- salesOrders（3 行: SO-20260903-0047,SO-20260902-0046,SO-20260901-0045）
    - 列表页: P3-R01-包装租赁管理后台原型/销售管理/销售订单列表.html
- salesOutbounds（1 行: XSCK-20260902-015）
    - 列表页: P3-R01-包装租赁管理后台原型/销售管理/销售出库列表.html
- otherInbounds（1 行: QTRK-20260901-003）
    - 列表页: P3-R01-包装租赁管理后台原型/仓储作业/其他入库列表.html
- otherOutbounds（1 行: QTCK-20260901-004）
    - 列表页: P3-R01-包装租赁管理后台原型/仓储作业/其他出库列表.html
- stocktakes（5 行: PD-202608-03,PD-202608-02,PD-202607-02,PD-202607-01,PD-202606-01）
    - 列表页: P3-R01-包装租赁管理后台原型/仓储作业/盘点列表.html
- transfers（1 行: DB-20260901-003）
    - 列表页: P3-R01-包装租赁管理后台原型/仓储作业/库存调拨列表.html
- purchaseReturns（1 行: CGTH-20260915-004）
    - 列表页: P3-R01-包装租赁管理后台原型/采购管理/采购退货单列表.html
- salesReturns（1 行: XSTH-20260911-003）
    - 列表页: P3-R01-包装租赁管理后台原型/销售管理/销售退货单列表.html
- transferOutbounds（1 行: ZY-20260915-005）
    - 列表页: P3-R01-包装租赁管理后台原型/租赁管理/转移出库列表.html

## B. 数据侧「生成」op 全量（t / act）
- rentInOrders | RZD-20260815-003 | 生成租金应付 => go('../财务协同/应付账单.html')
- rentInOrders | RZD-20260815-005 | 生成租金应付 => go('../财务协同/应付账单.html')
- purchaseOrders | PO-20260902-018 | 生成入库单 => go('../采购管理/采购入库列表.html')
- purchaseOrders | PO-20260830-016 | 生成入库单 => go('../采购管理/采购入库列表.html')
- purchaseOrders | PO-20260828-015 | 生成入库单 => go('../采购管理/采购入库列表.html')
- stocktakes | PD-202608-02 | 生成入库 => showGen('in', event)
- stocktakes | PD-202607-02 | 生成出库 => showGen('out', event)
- stocktakes | PD-202606-01 | 生成入库 => showGen('in', event)

## C. 页面静态「生成」按钮（onclick 原文）
- P3-R01-包装租赁管理后台原型/租赁管理/租赁出库录单.html:460 :: <button class="btn btn-sm" style="margin-left:8px;" onclick="go('../采购管理/采购订单列表.html')">生成采购订单</button>
- P3-R01-包装租赁管理后台原型/租赁管理/租赁出库录单.html:461 :: <button class="btn btn-sm" style="margin-left:6px;" onclick="go('../租入管理/租入单列表.html')">生成租入单</button>
- P3-R01-包装租赁管理后台原型/租赁管理/租赁单新建.html:395 :: <button class="btn btn-sm" style="margin-left:8px;" onclick="go('../采购管理/采购订单列表.html')">生成采购订单</button>
- P3-R01-包装租赁管理后台原型/租赁管理/租赁单新建.html:396 :: <button class="btn btn-sm" style="margin-left:6px;" onclick="go('../租入管理/租入单列表.html')">生成租入单</button>
- P3-R01-包装租赁管理后台原型/财务协同/应收账单.html:388 :: <div class="head-btns"><button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="go('../财务协同/应收生成.html')">手动生成账单</button></div>
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:459 :: <td class="sticky-op"><span class="ops"><a onclick="go('../采购管理/采购入库列表.html')">生成入库单</a><a>关闭</a></span></td>
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:475 :: <td class="sticky-op"><span class="ops"><a onclick="go('../采购管理/采购入库列表.html')">生成入库单</a><a>关闭</a></span></td>
- P3-R01-包装租赁管理后台原型/销售管理/销售出库新建.html:384 :: <button class="btn btn-sm" style="margin-left:8px;" onclick="go('../采购管理/采购订单列表.html')">生成采购订单</button>
- P3-R01-包装租赁管理后台原型/销售管理/销售订单新建.html:384 :: <button class="btn btn-sm" style="margin-left:8px;" onclick="go('../采购管理/采购订单列表.html')">生成采购订单</button>
- P3-R01-包装租赁管理后台原型/销售管理/销售订单新建.html:385 :: <button class="btn btn-sm" style="margin-left:6px;" onclick="go('../租入管理/租入单列表.html')">生成租入单</button>

## D. 新建/录单类页面清单
- P3-R01-包装租赁管理后台原型/仓储作业/其他入库新建.html
- P3-R01-包装租赁管理后台原型/仓储作业/其他出库新建.html
- P3-R01-包装租赁管理后台原型/仓储作业/调拨新建.html
- P3-R01-包装租赁管理后台原型/基础数据/客商新建.html
- P3-R01-包装租赁管理后台原型/基础数据/库位新建.html
- P3-R01-包装租赁管理后台原型/基础数据/物料新建.html
- P3-R01-包装租赁管理后台原型/租入管理/归还出库新建.html
- P3-R01-包装租赁管理后台原型/租入管理/租入单新建.html
- P3-R01-包装租赁管理后台原型/租赁管理/租赁出库录单.html
- P3-R01-包装租赁管理后台原型/租赁管理/租赁单新建.html
- P3-R01-包装租赁管理后台原型/租赁管理/转移出库新建.html
- P3-R01-包装租赁管理后台原型/租赁管理/退租入库新建.html
- P3-R01-包装租赁管理后台原型/系统管理/字典项新建.html
- P3-R01-包装租赁管理后台原型/系统管理/用户新建.html
- P3-R01-包装租赁管理后台原型/系统管理/角色新建.html
- P3-R01-包装租赁管理后台原型/财务协同/付款新建.html
- P3-R01-包装租赁管理后台原型/财务协同/应付新建.html
- P3-R01-包装租赁管理后台原型/财务协同/开票新建.html
- P3-R01-包装租赁管理后台原型/财务协同/收款新建.html
- P3-R01-包装租赁管理后台原型/财务协同/退款新建.html
- P3-R01-包装租赁管理后台原型/采购管理/采购入库录单.html
- P3-R01-包装租赁管理后台原型/采购管理/采购订单新建.html
- P3-R01-包装租赁管理后台原型/采购管理/采购退货新建.html
- P3-R01-包装租赁管理后台原型/销售管理/销售出库新建.html
- P3-R01-包装租赁管理后台原型/销售管理/销售订单新建.html
- P3-R01-包装租赁管理后台原型/销售管理/销售退货新建.html
- P3-R01-包装租赁管理后台原型/项目管理/项目新建.html

## E. 含 batch-btn-js 的页面（批量按钮启用机制已件）
- P3-R01-包装租赁管理后台原型/仓储作业/其他入库列表.html
- P3-R01-包装租赁管理后台原型/仓储作业/其他出库列表.html
- P3-R01-包装租赁管理后台原型/仓储作业/库存调拨列表.html
- P3-R01-包装租赁管理后台原型/仓储作业/收发存.html
- P3-R01-包装租赁管理后台原型/仓储作业/盘点列表.html
- P3-R01-包装租赁管理后台原型/基础数据/产品档案.html
- P3-R01-包装租赁管理后台原型/基础数据/客商管理.html
- P3-R01-包装租赁管理后台原型/基础数据/库位档案.html
- P3-R01-包装租赁管理后台原型/我的待办.html
- P3-R01-包装租赁管理后台原型/租入管理/归还出库列表.html
- P3-R01-包装租赁管理后台原型/租入管理/租入入库列表.html
- P3-R01-包装租赁管理后台原型/租入管理/租入单列表.html
- P3-R01-包装租赁管理后台原型/租赁管理/租赁出库列表.html
- P3-R01-包装租赁管理后台原型/租赁管理/租赁单列表.html
- P3-R01-包装租赁管理后台原型/租赁管理/转移出库列表.html
- P3-R01-包装租赁管理后台原型/租赁管理/退租入库列表.html
- P3-R01-包装租赁管理后台原型/财务协同/付款登记.html
- P3-R01-包装租赁管理后台原型/财务协同/应付账单.html
- P3-R01-包装租赁管理后台原型/财务协同/应收账单.html
- P3-R01-包装租赁管理后台原型/财务协同/开票登记.html
- P3-R01-包装租赁管理后台原型/财务协同/收款登记.html
- P3-R01-包装租赁管理后台原型/财务协同/退款登记.html
- P3-R01-包装租赁管理后台原型/采购管理/采购入库列表.html
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html
- P3-R01-包装租赁管理后台原型/采购管理/采购退货单列表.html
- P3-R01-包装租赁管理后台原型/销售管理/销售出库列表.html
- P3-R01-包装租赁管理后台原型/销售管理/销售订单列表.html
- P3-R01-包装租赁管理后台原型/销售管理/销售退货单列表.html

## F. showGen 定义（盘点列表.html）
（未找到 showGen）

## G. 采购订单列表 G64 参考实现（行号）
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:383 :: <div class="head-btns"><button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-default btn-sm" onclick="if(this.style.opacity!=='.45')poBatchAudit()">批量审核</button><button class="btn
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:762 :: <!-- G64 批量审核（2026-09-24 道远拍板·方案 A 弹窗集中结论；单条审核仍走审核页＝两种交互分开） -->
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:763 :: <div class="modal-overlay" id="poBatchModal">
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:765 :: <div class="modal-header"><span class="modal-title">批量审核</span><span class="modal-close" onclick="closeModal('poBatchModal')">&times;</span></div>
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:767 :: <div class="pn-hint" style="margin:0 0 10px;">已勾选 <b id="poBatchCount">0</b> 张待审核采购订单 · 批量审核仅做集中结论；需复核明细请点单号进「采购订单审核」逐单办理</div>
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:786 :: <div class="modal-footer"><button class="btn btn-default" onclick="closeModal('poBatchModal')">取消</button><button class="btn" onclick="poBatchSubmit()">确认提交</button></div>
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:790 :: /* G64 批量审核：勾选待审核单 → 弹窗集中结论（单条审核＝审核页整页复核，两交互分开） */
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:792 :: var m = document.getElementById('poBatchModal');
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:795 :: document.querySelectorAll('#poBatchModal .radio').forEach(function (r) {
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:807 :: function poBatchAudit() {
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:825 :: document.querySelectorAll('#poBatchModal .radio').forEach(function (r, i) { r.classList.toggle('checked', i === 0); });
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:828 :: openModal('poBatchModal');
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:830 :: function poBatchSubmit() {
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:832 :: var rc = document.querySelector('#poBatchModal .radio.checked');
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:834 :: closeModal('poBatchModal');
- P3-R01-包装租赁管理后台原型/采购管理/采购订单列表.html:835 :: poToast('已批量审核 ' + n + ' 单：' + v + '（演示）');

## H. 退租入库列表批量审核现状
- P3-R01-包装租赁管理后台原型/租赁管理/退租入库列表.html:380 :: <div class="head-btns"><button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="if(this.style.opacity!=='.45')g57BatchAudit()">批量审核</button></div>
- P3-R01-包装租赁管理后台原型/租赁管理/退租入库列表.html:688 :: function g57BatchAudit() {
- P3-R01-包装租赁管理后台原型/租赁管理/退租入库列表.html:690 :: showToast(n ? '已提交批量审核：' + n + ' 单清洗完工待审核（演示）' : '请先勾选需审核的清洗完工单据');