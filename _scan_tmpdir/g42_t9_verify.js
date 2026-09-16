var n=0,bad=[];
Object.keys(D.rentInReturns).forEach(function(k){
  var has=(D.rentInReturns[k].info||[]).some(function(x){return (x.label+x.text).indexOf('押金')>=0;});
  if(has)n++;else bad.push(k);
});
OUT.push({name:'T9 3/3 押金 info', ok:n===3, detail:'n='+n+' bad='+bad.join(',')});
