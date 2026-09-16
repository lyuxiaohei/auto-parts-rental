['projectDocs','boardRows','profitRows'].forEach(function(e){
  var ent=D[e]||{};
  OUT.push({name:e+' keys', ok:true, detail:Object.keys(ent).join(',')});
});
OUT.push({name:'projectDocs AR-20260905-0029 full', ok:true, detail:JSON.stringify(D.projectDocs['AR-20260905-0029']).slice(0,800)});
OUT.push({name:'boardRows sample', ok:true, detail:JSON.stringify(D.boardRows[Object.keys(D.boardRows)[0]]).slice(0,500)});
OUT.push({name:'profitRows sample', ok:true, detail:JSON.stringify(D.profitRows[Object.keys(D.profitRows)[0]]).slice(0,600)});
