const fs = require('fs');
const path = require('path');
const root = 'D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型';
let s = fs.readFileSync(path.join(root, '_data/demo-data.js'), 'utf8');
s = s.replace(/const\s+demoData\s*=/, 'module.exports =');
s = s.replace(/^window\.DEMO_DATA\s*=\s*/m, 'module.exports.DEMO_DATA = ');
global.window = {};
const tmp = path.join(process.env.TEMP, 'dd_v2.js');
fs.writeFileSync(tmp, s);
const d = require(tmp).DEMO_DATA;

// 1. dictItems 应收账单类型组
const arTypes = Object.values(d.dictItems).filter(v => v && v.row && v.row.fields && v.row.fields.category === '应收账单类型');
console.log('== dictItems 应收账单类型 ==');
arTypes.forEach(v => console.log(' ', v.row.fields.abbr || v.row.fields.name, '|', v.row.fields.status));

// 2. payableBills 键 + 是否含 AP-20260810-002
const apKeys = Object.keys(d.payableBills);
console.log('== payableBills keys (', apKeys.length, ') ==');
console.log(apKeys.join(', '));
console.log('AP-20260810-002 在 payableBills?', apKeys.includes('AP-20260810-002'));

// 3. projects 名称
console.log('== projects ==');
Object.keys(d.projects).forEach(k => {
  const r = d.projects[k].row || d.projects[k];
  const name = (r.fields && (r.fields.name || r.fields.projectName)) || (Array.isArray(r.cells) ? r.cells[0] : '?');
  console.log(' ', k, '|', typeof name === 'string' ? name.replace(/<[^>]+>/g, '') : JSON.stringify(name).slice(0, 60));
});

// 4. receivableBills billType 分布
console.log('== receivableBills billType 分布 ==');
const bt = {};
Object.keys(d.receivableBills).forEach(k => {
  const r = d.receivableBills[k].row || d.receivableBills[k];
  const t = (r.fields && r.fields.billType) || '?';
  bt[t] = (bt[t] || 0) + 1;
});
console.log(JSON.stringify(bt));

// 5. refunds 类型分布
console.log('== refunds ==');
Object.keys(d.refunds).forEach(k => {
  const r = d.refunds[k].row || d.refunds[k];
  console.log(' ', k, '|', r.fields && (r.fields.refundType || r.fields.type), '|', r.fields && r.fields.status);
});

// 6. rentInReturns 是否有押金字段
console.log('== rentInReturns fields keys ==');
Object.keys(d.rentInReturns).forEach(k => {
  const r = d.rentInReturns[k].row || d.rentInReturns[k];
  console.log(' ', k, '| fields:', Object.keys(r.fields || {}).join(','), '| info押金?', JSON.stringify(r.info || '').includes('押金'));
});
