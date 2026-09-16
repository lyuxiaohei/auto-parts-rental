var kc=[];
Object.keys(D.dictItems).forEach(function(k){
  var f=D.dictItems[k].row.fields;
  if(f.category==='库存状态')kc.push(k+' '+f.name);
});
OUT.push({name:'KC 库存状态字典', ok:true, detail:kc.join(' | ')||'无该组'});
