['发票类型','结算周期'].forEach(function(cat){
  var vals=[];
  Object.keys(D.dictItems).forEach(function(k){
    var f=(D.dictItems[k].row&&D.dictItems[k].row.fields)||{};
    if(f.category===cat) vals.push(k+' '+f.name);
  });
  OUT.push({name:cat, ok:true, detail:vals.join(' | ')});
});
