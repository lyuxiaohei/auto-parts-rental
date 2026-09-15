
global.window = {};
const fs = require('fs');
eval(fs.readFileSync(process.argv[2], 'utf8'));
const D = global.window.DEMO_DATA;
function dist(ent, fld) {
  const out = [];
  Object.keys(D[ent] || {}).forEach(k => {
    const f = (D[ent][k].row || {}).fields || {};
    if (f[fld] && out.indexOf(f[fld]) < 0) out.push(f[fld]);
  });
  return out;
}
console.log('projects keys:', Object.keys(D.projects).join(','));
console.log('payableBills.period:', dist('payableBills','period').join(' | '));
console.log('salesOutbounds.warehouse:', dist('salesOutbounds','warehouse').join(' | '));
console.log('returnInbounds.warehouse:', dist('returnInbounds','warehouse').join(' | '));
console.log('todoItems.project:', dist('todoItems','project').join(' | '));
console.log('todoItems.submitter:', dist('todoItems','submitter').join(' | '));
console.log('bomList.updater:', dist('bomList','updater').join(' | '));
console.log('salesOrders.agent:', dist('salesOrders','agent').join(' | '));
console.log('rentInbounds.maker:', dist('rentInbounds','maker').join(' | '));
console.log('rentInbounds.area:', dist('rentInbounds','area').join(' | '));
console.log('rentInReturns.maker:', dist('rentInReturns','maker').join(' | '));
console.log('stockFlows.cls:', dist('stockFlows','cls').join(' | '));
// opLogs result from cells
const rs = [];
Object.keys(D.opLogs).forEach(k => {
  const c = D.opLogs[k].row.cells;
  const v = String(c[c.length-1]).replace(/<[^>]+>/g, '');
  if (rs.indexOf(v) < 0) rs.push(v);
});
console.log('opLogs result(cell tag):', rs.join(' | '));
// purchaseInbounds maker/area from cells: idx5=area? idx7=maker?
Object.keys(D.purchaseInbounds).filter(k=>D.purchaseInbounds[k].row).slice(0,3).forEach(k => {
  const c = D.purchaseInbounds[k].row.cells.map(x => String(x).replace(/<[^>]+>/g, ''));
  console.log('PI', k, 'cells:', JSON.stringify(c));
});
// dict WL values
const wl = [];
Object.keys(D.dictItems).forEach(k => {
  const f = (D.dictItems[k].row || {}).fields || {};
  if (f.category === '物料类型') wl.push(f.name);
});
console.log('dict 物料类型:', wl.join(' | '));
