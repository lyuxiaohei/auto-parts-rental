var got=false;
Object.keys(D.stockEvents).forEach(function(k){
  var f=D.stockEvents[k].row.fields;
  if(!got && f.side==='客户在租'){ OUT.push({name:'sample '+k, ok:true, detail:JSON.stringify(D.stockEvents[k].row)}); got=true; }
});
