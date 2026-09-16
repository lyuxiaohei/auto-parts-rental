var ents=Object.keys(D).filter(function(k){return k!=='_meta'});
OUT.push({name:'实体数(不含 _meta)', ok:true, detail:ents.length+'：'+ents.join(',')});
var groups={},cnt=0;Object.keys(D.dictItems).forEach(function(k){var f=D.dictItems[k].row.fields;groups[f.category]=(groups[f.category]||0)+1;cnt++;});
OUT.push({name:'dictItems', ok:true, detail:'项='+cnt+' 组='+Object.keys(groups).length});
OUT.push({name:'关键行数', ok:true, detail:'todoItems='+Object.keys(D.todoItems).length+' refunds='+Object.keys(D.refunds).length+' returnInbounds='+Object.keys(D.returnInbounds).length+' stockEvents='+Object.keys(D.stockEvents).length+' partners='+Object.keys(D.partners).length+' products='+Object.keys(D.products).length+' projectDocs='+Object.keys(D.projectDocs).length});
OUT.push({name:'rentInReturns/transferOutbounds/payments', ok:true, detail:'rentInReturns='+Object.keys(D.rentInReturns).length+' transferOutbounds='+Object.keys(D.transferOutbounds).length+' payments='+Object.keys(D.payments).length});
