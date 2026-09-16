Object.keys(D.transferOutbounds).forEach(function(k){
  var f=D.transferOutbounds[k].row.fields;
  OUT.push({key:k, from:f.from||f['转出方']||'', to:f.to||f['接收方']||'', mat:f.mat||'', qty:f.qty||'', status:f.status||'', cust:f.customer||''});
});
OUT.push({name:'stockEvents 客户在租 samples', ok:true, detail:(function(){
  var r=[];Object.keys(D.stockEvents).forEach(function(k){var f=D.stockEvents[k].row.fields;if(f.side==='客户在租'&&/WBX|安吉|XNC/.test(JSON.stringify(f)))r.push(k+':'+f.date+' '+f.customer+' '+f.mat+' '+f.qty+' '+f.dir+' '+f.note);});
  return r.join(' || ')||'none';
})()});
OUT.push({name:'stockEvents keys tail', ok:true, detail:Object.keys(D.stockEvents).slice(-3).join(',')+' total='+Object.keys(D.stockEvents).length});
OUT.push({name:'returnInbounds keys', ok:true, detail:Object.keys(D.returnInbounds).join(',')});
