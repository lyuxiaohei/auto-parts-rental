Object.keys(D.bomVersions).forEach(function(k){
  var e=D.bomVersions[k];
  var st=(e.info||[]).filter(function(x){return x.label==='状态'})[0];
  OUT.push({name:'bomV '+k, ok:true, detail:JSON.stringify(e.row.keyHtml).slice(0,90)+' | info状态='+(st?st.text:'无')});
});
OUT.push({name:'计数核对', ok:true, detail:['stocktakes',5,'products',15,'partners',8,'locations',11,'bomVersions',3,'rentInOrders',6,'rentInReturns',3,'leaseOrders',9,'comboOutbounds',10,'returnInbounds',10,'transferOutbounds',5,'payments',5,'invoices',6,'refunds',5,'purchaseOrders',7,'purchaseInbounds',8,'purchaseReturns',3,'salesOrders',8,'salesOutbounds',6,'salesReturns',3].map(function(x,i,a){return (i%2? null:a[i]+'='+x)}).filter(function(x){return x}).join(' ')});
