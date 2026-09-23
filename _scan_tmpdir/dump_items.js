const fs = require('fs');
global.window = {};
eval(fs.readFileSync(process.argv[2], 'utf8'));
const D = window.DEMO_DATA;
const out = {};
for (const [ent, recs] of Object.entries(D)) {
  if (typeof recs !== 'object' || recs === null) continue;
  const rows = [];
  for (const [key, rec] of Object.entries(recs)) {
    if (rec && Array.isArray(rec.items)) rows.push([key, rec.items.length, rec.items.map(i => Array.isArray(i) ? i[2] : '?').join('|')]);
  }
  if (rows.length) out[ent] = rows;
}
fs.writeFileSync(process.argv[3], JSON.stringify(out), 'utf8');
console.log('dumped', Object.keys(out).length, 'entities');
