Object.keys(D.partners).forEach(function(k){
  var e = D.partners[k]; var r = e.row || e;
  OUT.push({key:k, cells:(r.cells||[]).join(' | '), infoLen:((e.info||[]).length), infoLabels:(e.info||[]).map(function(x){return x.label}).join(',')});
});
