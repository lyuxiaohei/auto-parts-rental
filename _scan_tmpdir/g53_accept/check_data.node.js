
global.window = {};
require(process.argv[2]);
const D = global.window.DEMO_DATA;
const ENT20 = ['purchaseOrders','purchaseInbounds','purchaseReturns','rentInOrders','rentInbounds','rentInReturns','leaseOrders','comboOutbounds','returnInbounds','transferOutbounds','stocktakes','otherInbounds','otherOutbounds','salesOrders','salesOutbounds','salesReturns','receipts','payments','invoices','refunds'];

const res = { entities: {}, oldLabels: {}, newLabels: {}, samples: {}, sweep: { entitiesChecked: 0, recordsChecked: 0, rowsChecked: 0, bad: [] } };

function recsOf(ent) {
  const v = D[ent];
  if (!v) return null;
  return Array.isArray(v) ? v : Object.values(v);
}

// ---------- 3a: old labels must be 0-hit inside the 20 entities ----------
const OLD = ['\u5173\u8054\u539f\u5355', '\u9001\u8fbe\u5730\u70b9', '\u4ef7\u7a0e\u5408\u8ba1', '\u9a8c\u6536\u65b9\u5f0f'];
// 关联原单 / 送达地点 / 价税合计 / 验收方式
OLD.forEach(l => res.oldLabels[l] = { hits: 0, where: [] });
for (const ent of ENT20) {
  const recs = recsOf(ent);
  if (!recs) { res.entities[ent] = { missing: true }; continue; }
  res.entities[ent] = { records: recs.length };
  recs.forEach((rec, i) => {
    const blob = JSON.stringify({ formRows: rec.formRows, items: rec.items });
    OLD.forEach(l => {
      if (blob.indexOf(l) !== -1) {
        res.oldLabels[l].hits++;
        res.oldLabels[l].where.push(ent + '#' + i);
      }
    });
  });
}

// ---------- 3b: new labels >=1 hit in the designated entity formRows ----------
function labelHits(ent, label) {
  const recs = recsOf(ent) || [];
  let n = 0;
  recs.forEach(rec => {
    (rec.formRows || []).forEach(fr => {
      if (fr && fr.label != null && String(fr.label) === label) n++;
    });
  });
  return n;
}
const NEW = [
  ['purchaseReturns', '\u5173\u8054\u91c7\u8d2d\u5165\u5e93'],        // 关联采购入库
  ['purchaseOrders',  '\u5173\u8054\u9500\u552e\u8ba2\u5355\u53f7'],  // 关联销售订单号
  ['comboOutbounds',  '\u6536\u8d27\u5730\u70b9'],                    // 收货地点
  ['returnInbounds',  '\u9000\u56de\u65e5\u671f'],                    // 退回日期
  ['stocktakes',      '\u76d8\u70b9\u65e5\u671f'],                    // 盘点日期
  ['invoices',        '\u5f00\u7968\u91d1\u989d'],                    // 开票金额
];
NEW.forEach(p => { res.newLabels[p[1] + ' @' + p[0]] = labelHits(p[0], p[1]); });

// ---------- 5: sampled row-length checks (map key = 单号) ----------
const SAMPLES = [
  ['purchaseInbounds', 'CGRK-20260828-012'],
  ['returnInbounds',   'TZRK-20260902-008'],
  ['leaseOrders',      'ZL-20260823-033'],
];
for (const [ent, key] of SAMPLES) {
  const map = D[ent];
  const rec = map ? map[key] : undefined;
  if (!rec) { res.samples[ent + '/' + key] = { found: false }; continue; }
  const cols = (rec.itemCols || []).length;
  const lens = (rec.items || []).map(r => r.length);
  res.samples[ent + '/' + key] = {
    found: true,
    itemTitle: rec.itemTitle || '',
    itemCols: cols,
    itemRowCount: lens.length,
    rowLengths: lens.join(','),
    allMatch: lens.every(n => n === cols)
  };
}

// ---------- 5: full sweep over the 20 entities ----------
for (const ent of ENT20) {
  const recs = recsOf(ent);
  if (!recs) continue;
  res.sweep.entitiesChecked++;
  recs.forEach(rec => {
    res.sweep.recordsChecked++;
    const cols = (rec.itemCols || []).length;
    (rec.items || []).forEach((row, ri) => {
      res.sweep.rowsChecked++;
      if (!Array.isArray(row) || row.length !== cols) {
        res.sweep.bad.push(ent + ' row' + ri + ' len=' + (Array.isArray(row) ? row.length : 'notArray') + ' cols=' + cols);
      }
    });
  });
}
res.sweep.badCount = res.sweep.bad.length;
res.sweep.badSample = res.sweep.bad.slice(0, 20);
console.log(JSON.stringify(res, null, 1));
