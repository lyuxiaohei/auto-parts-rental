OUT.push({name:'T8 returnInbounds=10', ok:Object.keys(D.returnInbounds).length===10, detail:'n='+Object.keys(D.returnInbounds).length});
OUT.push({name:'T8 stockEvents=23', ok:Object.keys(D.stockEvents).length===23, detail:'n='+Object.keys(D.stockEvents).length});
OUT.push({name:'T8 keys present', ok:!!D.returnInbounds['TZRK-20260915-012']&&!!D.stockEvents['EV-20260915-023'], detail:'both keys in'});
OUT.push({name:'T8 stockFlows untouched=17', ok:Object.keys(D.stockFlows).length===17, detail:'n='+Object.keys(D.stockFlows).length});
