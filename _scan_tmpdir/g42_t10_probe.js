var arKeys = Object.keys(D.receivableBills), apKeys = Object.keys(D.payableBills);
OUT.push({name:'AR keys', ok:true, detail:arKeys.join(' | ')});
OUT.push({name:'AP keys', ok:true, detail:apKeys.join(' | ')});
['projectDocs','boardRows','profitRows'].forEach(function(e){
  var ent=D[e]||{}; var hits=[];
  Object.keys(ent).forEach(function(k){
    var js=JSON.stringify(ent[k]);
    (js.match(/A[RP]-[0-9]{8}-[0-9A-Za-z\-]+/g)||[]).forEach(function(m){ hits.push(k+':'+m); });
  });
  OUT.push({name:e+' 假单号扫描', ok:true, detail:hits.join(' | ')||'none'});
});
