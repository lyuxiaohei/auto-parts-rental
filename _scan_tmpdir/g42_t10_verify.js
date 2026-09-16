var arKeys=Object.keys(D.receivableBills), apKeys=Object.keys(D.payableBills);
function collect(obj){var c={};Object.keys(obj).forEach(function(k){var js=JSON.stringify(obj[k]);(js.match(/A[RP]-[0-9]{8}-[0-9A-Za-z\-]+|A[RP]-[0-9]{4}-[0-9]{2}-[A-Za-z0-9\-]+/g)||[]).forEach(function(m){c[m]=(c[m]||0)+1;});});return c;}
var pd=collect(D.projectDocs), br=collect(D.boardRows), pr=collect(D.profitRows);
var allBad=[]; var total=0;
[pd,br,pr].forEach(function(c){Object.keys(c).forEach(function(m){total+=c[m];
  if(m.indexOf('AR-')===0 && arKeys.indexOf(m)<0) allBad.push('AR伪造:'+m);
  if(m.indexOf('AP-')===0 && apKeys.indexOf(m)<0) allBad.push('AP伪造:'+m);
});});
OUT.push({name:'T10 三实体单号全∈实有键集(Counter逐单号)', ok:allBad.length===0, detail:'引用总数='+total+' bad='+(allBad.join(';')||'无')});
OUT.push({name:'T10 projectDocs 新键在位', ok:!!D.projectDocs['AR-2026-08-PRJ2601']&&!!D.projectDocs['AR-2026-07-PRJ2601'], detail:'两键在'});
var lkCnt=(JSON.stringify(D.boardRows).split('class=\\"lk\\"').length-1)+(JSON.stringify(D.profitRows).split('class=\\"lk\\"').length-1);
OUT.push({name:'T10 board+profit lk 注入≥24', ok:lkCnt>=24, detail:'lk 总数='+lkCnt});
