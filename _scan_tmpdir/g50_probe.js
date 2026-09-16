var st={};var n=0;
Object.keys(D.stockFlows).forEach(function(k){
  var f=(D.stockFlows[k].row&&D.stockFlows[k].row.fields)||{};
  if(!f.status)return; n++;
  st[f.status]=(st[f.status]||0)+1;
});
OUT.push({name:'stockFlows 状态值域', ok:true, detail:'有效行='+n+' 状态='+JSON.stringify(st)});
var ti=Object.keys(D.todoItems).map(function(k){return D.todoItems[k].row.fields.type});
var uniq=[];ti.forEach(function(t){if(uniq.indexOf(t)<0)uniq.push(t)});
OUT.push({name:'todoItems', ok:true, detail:'行='+ti.length+' 类型去重='+uniq.length+'（'+uniq.join(',')+'）'});
