var b = D.payableBills['AP-20260815-003'];
OUT.push({name:'AP-20260815-003', ok:true, detail: JSON.stringify({billType:b.billType, btype:(b.row&&b.row.fields||{}).btype, amount:b.amount, supplier:(b.row&&b.row.fields||{}).supplier})});
