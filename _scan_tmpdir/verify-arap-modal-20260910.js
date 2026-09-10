/* 静态断言：arap-modal 改造验证（2026-09-10） */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', 'P3-R01-包装租赁管理后台原型');
const read = p => fs.readFileSync(path.join(ROOT, p), 'utf8');

const ap = read('财务协同/应付账单.html');
const ar = read('财务协同/应收账单.html');
const apc = read('财务协同/弹窗/应付账单新建.html');
const arc = read('财务协同/弹窗/应收账单生成.html');
const dd = read('_data/demo-data.js');

let pass = 0, fail = 0;
function chk(name, cond) {
  console.log((cond ? 'PASS' : 'FAIL') + '  ' + name);
  cond ? pass++ : fail++;
}
function count(s, sub) { return s.split(sub).length - 1; }

/* --- A. 应付账单.html --- */
chk('A-P1 页面流无 #instCard（全局 0 次）', count(ap, 'instCard') === 0);
chk('A-P2 instModal 弹窗存在', ap.includes('id="instModal"'));
chk('A-P3 instModal 标题带演示账单号', ap.includes('分期付款计划 · AP-20260905-013 对客户应付 68,400.00'));
chk('A-P4 data-note="4" 保留在 instModal 的 th 上', /<div class="modal-overlay" id="instModal">[\s\S]*?<th data-note="4">期次<\/th>/.test(ap));
chk('A-P5 instModal 含 去付款登记 按钮', /id="instModal"[\s\S]*?去付款登记/.test(ap) && ap.includes("go('../财务协同/付款登记.html')"));
chk('A-P6 createModal 5 项账单类型', ['采购应付（按采购订单自动汇总）', '租金应付（按租入单自动汇总）', '丢损赔偿（赔付供应商）', '对客户应付（赔付客户：交付延误·断产·回款违约金）', '无订单预付款（付供应商保证金，T2 挂账侧待财务确认）'].every(t => ap.includes(t)));
chk('A-P7 createModal 加宽 720px', /id="createModal"[\s\S]*?width:720px/.test(ap));
chk('A-P8 createModal 分期计划区（cmInstN/cmInstBody）', ap.includes('id="cmInstN"') && ap.includes('id="cmInstBody"'));
chk('A-P9 createModal 条件字段（关联采购订单号/关联租入单号/费用分类）', ap.includes('id="cmRefPo"') && ap.includes('id="cmRefRent"') && ap.includes('id="cmFeeCatRow"'));
chk('A-P10 互算工厂 createInstPlan + 两实例', count(ap, 'createInstPlan({') >= 2 && ap.includes('function createInstPlan(cfg)'));
chk('A-P11 footer 取消/保存草稿/提交审核', ['取消', '保存草稿', '提交审核'].every(t => ap.includes(t)));
chk('A-P12 类型联动脚本（客户/供应商名单）', ap.includes('一汽解放汽车有限公司') && ap.includes('cmPartyLabel'));

/* --- B. 应收账单.html --- */
chk('B-P1 createModal 5 项账单类型', ['租赁费（按组合出库自动汇总）', '销售费（按销售出库自动汇总）', '丢损赔偿（客户赔付我方）', '供应商应收（供应商赔付我方）', '预收·保证金（收客户，无订单直接建单）'].every(t => ar.includes(t)));
chk('B-P2 垃圾选项已清除（待定选项=0，账单类型行无「全部」option）', count(ar, '待定选项') === 0 && !/<select[^>]*id="cmBtype"[^>]*>[^<]*<option[^>]*>全部</.test(ar));
chk('B-P3 分期收款计划区', ar.includes('分期收款计划') && ar.includes('id="cmInstN"') && ar.includes('id="cmInstBody"'));
chk('B-P4 pn-hint 类型说明更新（含供应商应收）', ar.includes('id="cmTypeHint"'));
chk('B-P5 客户名单含安吉智行物流', ar.includes('安吉智行物流'));
chk('B-P6 互算工厂存在', ar.includes('function createInstPlan(cfg)'));

/* --- C. 弹窗副本同步 --- */
chk('C-P1 应付账单新建.html 同步 5 类型 + 分期区', ['对客户应付（赔付客户：交付延误·断产·回款违约金）', 'id="cmInstBody"', 'function createInstPlan(cfg)'].every(t => apc.includes(t)));
chk('C-P2 应收账单生成.html 同步 5 类型 + 分期区', ['供应商应收（供应商赔付我方）', 'id="cmInstBody"', 'function createInstPlan(cfg)'].every(t => arc.includes(t)));
chk('C-P3 预览页无待定选项', count(apc, '待定选项') === 0 && count(arc, '待定选项') === 0);

/* --- D. demo-data.js --- */
chk('D-P1 分期付款 op 改为 openModal(\'instModal\')', dd.includes('"t": "分期付款", "act": "openModal(\'instModal\')"'));
chk('D-P2 应付实体无残留 go 付款登记 的分期付款 op', !/"t": "分期付款", "act": "go\('/.test(dd));

/* --- 通用 --- */
chk('G-P1 改动文件无 console.log 残留', [ap, ar, apc, arc].every(s => !s.includes('console.log')));
chk('G-P2 应付页列表筛选/演示行保留（data-note 1/2/3 仍在）', ['data-note="1"', 'data-note="2"', 'data-note="3"'].every(t => ap.includes(t)));

console.log('\n== 合计 PASS ' + pass + ' / FAIL ' + fail + ' ==');
process.exit(fail ? 1 : 0);
