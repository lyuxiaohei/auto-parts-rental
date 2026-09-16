
var tkl=[],thc=[];Object.keys(D.dictItems).forEach(function(k){var f=D.dictItems[k].row.fields;if(f.category==='退款类型')tkl.push(f.name);if(f.category==='退货类型')thc.push(f.name);});
OUT.push({name:'t11a', ok: tkl.join(',')==='采购退货退款,销售退货退款,预收退回,多付退回' && thc.length===2, detail:'TKL:'+tkl.join('|')+' THC:'+thc.length});
OUT.push({name:'t11b', ok: Object.keys(D.refunds).length===5 && !!D.refunds['TKD-20260916-004'] && !!D.refunds['TKD-20260916-005'], detail:'n='+Object.keys(D.refunds).length});
OUT.push({name:'t11c', ok: JSON.stringify(D).indexOf('应付退款（对供应商）')<0 && JSON.stringify(D).indexOf('应收退款（对客户）')<0, detail:'demo-data 旧方向词=0'});
OUT.push({name:'t11d', ok: JSON.stringify(D.payableBills['AP-20260905-012']).indexOf('TKD-20260916-005')>=0, detail:'AP-012 timeline 引用 005'});
