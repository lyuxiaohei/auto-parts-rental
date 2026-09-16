var k0 = Object.keys(D.payableBills)[0];
OUT.push({name:'sample', ok:true, detail: JSON.stringify(D.payableBills[k0]).slice(0,1200)});
var pb = D.payableBills;
Object.keys(pb).forEach(function(k){
  var r = pb[k].row || pb[k];
  var f = r.fields || r;
  OUT.push({key:k, supplier:(f.supplier||f['供应商']||''), type:(f.type||f['类型']||f.billType||''), date:(f.date||f['日期']||''), amt: JSON.stringify(r).match(/58,?000/)?'HAS58000':''});
});
