['AR-2026-08-PRJ2601','AR-2026-07-PRJ2601','AR-20260910-PRJ2601-YJ','AR-2026-09-PRJ2601-D1','AR-2026-09-PRJ2601-YS','AR-2026-08-PRJ2602','AR-2026-09-PRJ2603-U1'].forEach(function(k){
  var b=D.receivableBills[k]; if(!b){OUT.push({name:k,ok:false,detail:'MISSING'});return;}
  var f=b.row.fields;
  OUT.push({name:k, ok:true, detail:'btype='+(f.btype||'?')+' period='+(f.period||'?')+' status='+(f.status||'?')+' date='+(f.date||'?')+' amt='+(b.amount||'?')});
});
