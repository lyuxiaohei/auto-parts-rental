var probe={'stocktakes':null,'products':null,'locations':null,'bomVersions':null,'rentInOrders':null,'rentInReturns':null,'leaseOrders':null,'comboOutbounds':null,'returnInbounds':null,'transferOutbounds':null,'payments':null,'invoices':null,'refunds':null,'purchaseOrders':null,'purchaseInbounds':null,'purchaseReturns':null,'salesOrders':null,'salesOutbounds':null,'salesReturns':null};
Object.keys(probe).forEach(function(e){
  var ent=D[e]||{}; var k=Object.keys(ent)[0];
  var f=(ent[k].row&&ent[k].row.fields)||{};
  OUT.push({name:e, ok:true, detail:'fields='+Object.keys(f).join(',')});
});
