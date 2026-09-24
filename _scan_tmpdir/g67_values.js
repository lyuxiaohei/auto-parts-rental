const fs = require('fs');
const src = fs.readFileSync('P3-R01-包装租赁管理后台原型/_data/demo-data.js', 'utf8');
function count(p) { return src.split(p).length - 1; }
console.log('unquoted label: \'登记单号\' =', count("label: '登记单号'"));
['关联应收账单', '关联采购入库', '关联销售出库', '关联退款单', '关联退货单', '付款方', '关联采购订单', '关联租入单', '关联租入入库', '关联丢损赔偿单', '关联应付账单'].forEach((w) => {
  console.log(w, 'quoted=', count("'label': '" + w + "'"), 'unquoted=', count("label: '" + w + "'"));
});
console.log('客户端（ =', count('客户端（'), '| 客户端( =', count('客户端('));
global.window = {};
require(require('path').join(__dirname, '..', 'P3-R01-包装租赁管理后台原型/_data/demo-data.js'));
const D = window.DEMO_DATA;
console.log('SO keys:', Object.keys(D.salesOrders).join(','));
console.log('PO keys:', Object.keys(D.purchaseOrders).join(','));
Object.keys(D.rentInReturns).forEach((k) => {
  const r = D.rentInReturns[k];
  const cells = r.row.cells;
  console.log('rentInReturns', k, '| 归还时间cell:', cells[7], '| 详情text:', (r.formRows || []).filter((x) => x.label === '归还日期')[0].text);
});
Object.keys(D.refunds).forEach((k) => {
  const r = D.refunds[k];
  const ref = (r.formRows || []).filter((x) => x.label === '关联退货单');
  console.log('refunds', k, '| 关联退货单 ref 值:', ref.length ? ref[0].text : '—', '| 明细列:', (r.itemCols || []).join('/'));
});
