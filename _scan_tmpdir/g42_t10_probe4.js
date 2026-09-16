Object.keys(D.boardRows).forEach(function(k){
  var r=D.boardRows[k];
  OUT.push({name:'board '+k, ok:true, detail:JSON.stringify(r.row.cells.map(function(c){return c.replace(/<[^>]+>/g,'')}))});
});
Object.keys(D.profitRows).forEach(function(k){
  var r=D.profitRows[k];
  OUT.push({name:'profit '+k, ok:true, detail:JSON.stringify(r.row.cells.map(function(c){return c.replace(/<[^>]+>/g,'')}))});
});
Object.keys(D.payableBills).forEach(function(k){
  var f=D.payableBills[k].row.fields;
  OUT.push({name:'AP '+k, ok:true, detail:'project='+(f.project||'?')+' btype='+f.btype+' supplier='+f.supplier+' amt='+D.payableBills[k].amount});
});
