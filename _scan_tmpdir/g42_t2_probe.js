var pb = D.payableBills;
Object.keys(pb).forEach(function(k){
  var f = pb[k].fields || {};
  OUT.push({key:k, supplier:f.supplier||'', type:f.type||'', date:f.date||'', amt:f.amount||f.amt||''});
});
OUT.push({name:'payments-A P-dead-ref', ok:true, detail: JSON.stringify((function(){var r=[];Object.keys(D.payments||{}).forEach(function(k){var s=JSON.stringify(D.payments[k]);if(s.indexOf('AP-20260810-002')>=0)r.push(k);});return r;})())});
