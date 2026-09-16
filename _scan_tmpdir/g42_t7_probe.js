Object.keys(D.partners).forEach(function(k){
  var e = D.partners[k]; var r = e.row || e; var f = r.fields || r;
  OUT.push({key:k, name:f.name||'', type:f.type||'', hasTax:('invoiceTaxNo' in f), keys:Object.keys(f).join(',')});
});
