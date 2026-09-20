global.window = {};
require('D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型/_data/demo-data.js');
var D = window.DEMO_DATA;
var BASE = {
  purchaseOrders: ['订单号', '状态', '所属项目', '供应商', '物料类型', '关联销售订单号', '客户（带出）', '预计到货日期', '备注'],
  comboOutbounds: ['出库单号', '状态', '所属项目', '关联租赁单', '关联销售订单', '客户（带出）', '出库类型', '出库库位', '收货地点', '要货日期', '出库备注'],
  stocktakes: ['盘点单号', '状态', '盘点库房', '盘点范围', '盘点口径', '盘点人', '盘点日期', '处理方式', '复盘人', '备注']
};
['purchaseOrders', 'comboOutbounds', 'stocktakes'].forEach(function (e) {
  var k = Object.keys(D[e])[0];
  var labels = D[e][k].formRows.map(function (f) { return f.label; });
  var extra = labels.filter(function (l) { return BASE[e].indexOf(l) < 0; });
  console.log(e + ' 合理多出=' + JSON.stringify(extra));
});
