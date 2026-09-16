var ok = 0, bad = [];
Object.keys(D.partners).forEach(function(k){
  var f = D.partners[k].row.fields;
  var t = f.invoiceTaxNo || '';
  var good = /^9[A-Z0-9]131015MA1F[A-Z0-9]{5}\d$/.test(t) && t.length === 18;
  var info2ok = (D.partners[k].info2 || []).length === 5 && D.partners[k].info2[1].label === '纳税人识别号';
  if (good && info2ok) ok++; else bad.push(k + ':' + t + ':len' + t.length + ':i2' + info2ok);
});
OUT.push({name:'T7a partners invoiceTaxNo 8/8 + info2 5rows', ok: ok === 8, detail: 'ok=' + ok + ' bad=' + bad.join(';')});
