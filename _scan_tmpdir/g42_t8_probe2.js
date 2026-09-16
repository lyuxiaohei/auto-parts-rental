OUT.push({name:'ZY-20260914-001', ok:true, detail:JSON.stringify(D.transferOutbounds['ZY-20260914-001'].row.fields)});
var sides={};Object.keys(D.stockEvents).forEach(function(k){var f=D.stockEvents[k].row.fields;sides[f.side]=(sides[f.side]||0)+1;});
OUT.push({name:'stockEvents sides', ok:true, detail:JSON.stringify(sides)});
OUT.push({name:'EV cells len', ok:true, detail:'len='+(D.stockEvents['EV-20260903-022'].row.cells.length)+' cols? check page'});
