Object.keys(D.projects).forEach(function(k){
  var f = (D.projects[k].row && D.projects[k].row.fields) || D.projects[k].fields || {};
  OUT.push({key:k, name:f.name||'', status:f.status||''});
});
