
global.window={};
require(String.raw`D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型/_data/demo-data.js`);
var D=window.DEMO_DATA;
var out={};
['purchaseOrders','purchaseInbounds','purchaseReturns','rentInOrders','rentInbounds','rentInReturns','leaseOrders','comboOutbounds','returnInbounds','transferOutbounds','stocktakes','otherInbounds','otherOutbounds','salesOrders','salesOutbounds','salesReturns','receipts','payments','invoices','refunds','transfers'].forEach(function(e){
  var k=Object.keys(D[e])[0]; out[e]={key:k, labels:(D[e][k].formRows||[]).map(function(f){return f.label;})};
});
console.log(JSON.stringify(out));
