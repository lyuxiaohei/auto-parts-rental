/* P3-R05 排查·demo-data 结构化提取：每实体 rows(fields/cells/ops/info/feeCols/fees) 摘要 */
const fs = require('fs');
const path = require('path');
const file = path.join(__dirname, '..', 'P3-R01-包装租赁管理后台原型', '_data', 'demo-data.js');
global.window = {};
eval(fs.readFileSync(file, 'utf8'));
const D = global.window.DEMO_DATA;
const out = {};
for (const ent of Object.keys(D)) {
  if (ent === '_meta') continue;
  const recs = D[ent] || {};
  const summary = { count: 0, records: {} };
  for (const k of Object.keys(recs)) {
    const r = recs[k] || {};
    const row = r.row || {};
    summary.count++;
    summary.records[k] = {
      fieldKeys: Object.keys(row.fields || {}),
      status: (row.fields || {}).status,
      cellsLen: Array.isArray(row.cells) ? row.cells.length : null,
      ops: (row.ops || []).map(o => o.t),
      note: row.note,
      infoLabels: (r.info || []).map(i => i.label + (i.tag !== undefined ? '(tag)' : '')),
      feeCols: r.feeCols || null,
      feesCells: (r.fees || []).map(f => (f.cells || []).length),
      chainLen: (r.chain || []).length,
      timelineLen: (r.timeline || []).length,
      title: r.title || null
    };
  }
  out[ent] = summary;
}
fs.writeFileSync(path.join(__dirname, 'p3r05_data.json'), JSON.stringify(out, null, 1), 'utf8');
console.log('实体数:', Object.keys(out).length, '总记录:', Object.values(out).reduce((a, b) => a + b.count, 0));
