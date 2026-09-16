var EXPECT={
 stocktakes:['盘点库房','处理方式','复盘人','备注'],
 products:['物料型号','供应商内部编码','备注'],
 partners:['联系电话','备注'],
 locations:['规格/承载','备注'],
 bomVersions:['状态','备注'],
 rentInOrders:['所属项目','备注'],
 rentInReturns:['备注'],
 leaseOrders:['单据类型','建单日期','备注'],
 comboOutbounds:['要货日期','出库备注'],
 returnInbounds:['验收备注'],
 transferOutbounds:['备注'],
 payments:['备注'],
 invoices:['备注'],
 refunds:['备注'],
 purchaseOrders:['所属项目','客户','备注'],
 purchaseInbounds:['到货日期','质检要求','随货单据'],
 purchaseReturns:['备注'],
 salesOrders:['要求交货日期'],
 salesOutbounds:['出库日期','备注'],
 salesReturns:['备注']
};
var bad=[];
Object.keys(EXPECT).forEach(function(e){
  var ent=D[e]||{};
  Object.keys(ent).forEach(function(k){
    var labels=(ent[k].info||[]).map(function(x){return x.label});
    EXPECT[e].forEach(function(lb){
      if(labels.indexOf(lb)<0) bad.push(e+'/'+k+':'+lb);
    });
  });
});
OUT.push({name:'T7b 每记录新标签齐全', ok:bad.length===0, detail:'缺 '+bad.length+' 处：'+bad.slice(0,12).join(' | ')});
