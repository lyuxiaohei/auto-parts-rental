// G54 独立验收 ③ 数据断言 + ④ 备份对比
const fs = require('fs');
const path = require('path');
const ROOT = 'D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁';
const P3 = path.join(ROOT, 'P3-R01-包装租赁管理后台原型');

function loadDemo(p) {
  global.window = {};
  new Function(fs.readFileSync(p, 'utf8'))();
  return window.DEMO_DATA;
}

const D = loadDemo(path.join(P3, '_data/demo-data.js'));
const results = [];
function chk(name, ok, ev) { results.push(`${ok ? 'PASS' : 'FAIL'} ${name} —— ${ev}`); }

// 1. locations
const locKeys = Object.keys(D.locations);
chk('locations=11键', locKeys.length === 11, `actual=${locKeys.length} keys=${locKeys.join(',')}`);
const zfRow = D.locations['XNC-ZF'] && D.locations['XNC-ZF'].row;
chk("locations['XNC-ZF'].row.ops 为空数组", Array.isArray(zfRow && zfRow.ops) && zfRow.ops.length === 0, `ops=${JSON.stringify(zfRow && zfRow.ops)}`);

// 2. dictItems 库位类型组（实际结构 {code:{row:{fields:{category,abbr,name,status}}}}）
const dict = D.dictItems || {};
const kwCodes = Object.keys(dict).filter(k => /^KW-/.test(k));
const kw = kwCodes.map(k => ({ value: k, name: (dict[k].row && dict[k].row.fields ? dict[k].row.fields.name : dict[k].name), cat: (dict[k].row && dict[k].row.fields ? dict[k].row.fields.category : '') }));
const allKwType = kw.every(i => i.cat === '库位类型');
chk('dictItems 库位类型组=5值(KW-01~05) 且 KW-05.name=虚拟仓',
  kw.length === 5 && allKwType && kw.find(i => i.value === 'KW-05').name === '虚拟仓',
  `kw=[${kw.map(i => i.value + ':' + i.name + '/' + i.cat).join(' | ')}]`);

// 3. rentInOrders
const rio = D.rentInOrders || {};
const rioKeys = Object.keys(rio);
let dist = { '直发': 0, '自发': 0 }, bad = [];
for (const k of rioKeys) {
  const t = rio[k].row.fields.type;
  if (t === '直发' || t === '自发') dist[t]++;
  else bad.push(k + '=' + t);
}
chk('rentInOrders=7键且type∈{直发,自发}分布3/4',
  rioKeys.length === 7 && dist['直发'] === 3 && dist['自发'] === 4 && bad.length === 0,
  `keys=${rioKeys.length} dist=${JSON.stringify(dist)} bad=${bad.join(';')}`);

// 4. comboOutbounds chain
const ck = D.comboOutbounds && D.comboOutbounds['CK-20260914-023'];
const chain = ck && ck.chain;
chk('comboOutbounds[CK-20260914-023].chain 长度=3 且首节点含RZD-20260902-008',
  Array.isArray(chain) && chain.length === 3 && JSON.stringify(chain[0]).includes('RZD-20260902-008'),
  `len=${chain ? chain.length : 'undef'} first=${chain ? JSON.stringify(chain[0].name || chain[0]) : ''}`);

// 5. stockFlows
const sfKeys = Object.keys(D.stockFlows || {});
chk('stockFlows 键数=18', sfKeys.length === 18, `actual=${sfKeys.length}`);

// 6. 终态链三键
const rzd = rio['RZD-20260912-010'];
const rzrk = (D.rentReturnInbounds || D.rentInReturns || D.returnInbounds || {})['RZRK-20260912-024'];
// find RZRK anywhere
let rzrkObj = null, rzrkColl = '';
for (const [k, v] of Object.entries(D)) {
  if (v && typeof v === 'object' && !Array.isArray(v) && v['RZRK-20260912-024']) { rzrkObj = v['RZRK-20260912-024']; rzrkColl = k; }
}
const cko = D.comboOutbounds && D.comboOutbounds['CK-20260912-024'];
const rzdStatus = rzd && rzd.row.fields.status;
const rzrkStatus = rzrkObj && rzrkObj.row.fields.status;
const rzrkArea = rzrkObj && (rzrkObj.row.fields.area || rzrkObj.row.fields['库位'] || '');
const ckoStatus = cko && cko.row.fields.status;
// interconnection: RZRK references RZD-20260912-010 and CK-20260912-024?
const rzrkStr = JSON.stringify(rzrkObj || {});
const interRZD = rzrkStr.includes('RZD-20260912-010');
const interCK = rzrkStr.includes('CK-20260912-024');
chk('终态链三键存在且互联',
  !!rzd && !!rzrkObj && !!cko && rzdStatus === '已完结' && rzrkStatus === '已入库' && String(rzrkArea).includes('直发虚拟仓') && ckoStatus === '已出库' && interRZD && interCK,
  `RZD.status=${rzdStatus}; RZRK(coll=${rzrkColl}).status=${rzrkStatus},area=${rzrkArea},refRZD=${interRZD},refCK=${interCK}; CK.status=${ckoStatus}`);

// ④ 备份对比：stockFlows 逐键一致 + locations 前10键一致
const B = loadDemo(path.join(ROOT, 'backup-xnc-20260919/_data/demo-data.js'));
let sfSame = true, sfDiff = [];
const bKeys = Object.keys(B.stockFlows || {});
for (const k of new Set([...sfKeys, ...bKeys])) {
  if (JSON.stringify(D.stockFlows[k]) !== JSON.stringify(B.stockFlows[k])) { sfSame = false; sfDiff.push(k); }
}
chk('红线: 备份vs现行 stockFlows 逐键 JSON 全等', sfSame && sfKeys.length === bKeys.length,
  `keys ${bKeys.length}->${sfKeys.length} diff=[${sfDiff.join(',')}]`);

let locSame = true, locDiff = [];
const aLoc = Object.keys(B.locations || {});
for (const k of aLoc) {
  const b = B.locations[k], c = D.locations[k];
  const j = x => JSON.stringify({ fields: x.row.fields, cells: x.row.cells, ops: x.row.ops });
  if (!c || j(b) !== j(c)) { locSame = false; locDiff.push(k); }
}
chk('红线: 备份 locations 前10键(RA/RB/RC/RD) fields/cells/ops 全等', locSame && aLoc.length === 10,
  `backupLocKeys=${aLoc.length} diff=[${locDiff.join(',')}] XNC-ZF新增=${!!D.locations['XNC-ZF']}`);

// ⑤ 外购区 RW 计数
const dd = fs.readFileSync(path.join(P3, '_data/demo-data.js'), 'utf8');
const rwCount = (dd.match(/外购区 RW/g) || []).length;
chk('demo-data.js 「外购区 RW」计数=0', rwCount === 0, `actual=${rwCount}`);

console.log(results.join('\n'));
const fails = results.filter(r => r.startsWith('FAIL')).length;
console.log(`---- ${results.filter(r => r.startsWith('PASS')).length} PASS / ${fails} FAIL`);
