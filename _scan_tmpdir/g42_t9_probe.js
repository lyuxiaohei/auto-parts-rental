Object.keys(D.rentInReturns).forEach(function(k){
  var f=D.rentInReturns[k].row.fields;
  OUT.push({key:k, ref:f.ref, status:f.status, date:f.date});
});
Object.keys(D.rentInOrders).forEach(function(k){
  var f=D.rentInOrders[k].row.fields||{};
  var dep=null;
  (D.rentInOrders[k].info||[]).forEach(function(x){if(x.label==='押金')dep=x.text;});
  OUT.push({name:'RZD '+k, ok:true, detail:'status='+(f.status||'?')+' depositInfo='+(dep||'-')});
});
