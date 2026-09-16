const fs = require('fs');
const path = require('path');
const root = 'D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型';
let s = fs.readFileSync(path.join(root, '_data/demo-data.js'), 'utf8');
s = s.replace(/const\s+demoData\s*=/, 'module.exports =');
s = s.replace(/^window\.DEMO_DATA\s*=\s*/m, 'module.exports.DEMO_DATA = ');
global.window = {};
const tmp = path.join(process.env.TEMP || '/tmp', 'dd_loopcheck.js');
fs.writeFileSync(tmp, s);
const d = require(tmp).DEMO_DATA;
const ks = Object.keys(d);
console.log('实体数:', ks.length);
console.log(ks.join('\n'));
console.log('=== 关键实体行数 ===');
for (const k of ks) {
  const v = d[k];
  const n = Array.isArray(v) ? v.length : (v && typeof v === 'object' ? Object.keys(v).length : '-');
  console.log(k, n);
}
