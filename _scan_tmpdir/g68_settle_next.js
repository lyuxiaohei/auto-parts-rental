const fs = require('fs');
const s = fs.readFileSync('P3-R01-包装租赁管理后台原型/_data/demo-data.js', 'utf8');
const start = s.indexOf('  partners: {');
const end = s.indexOf('\n  /* ', start + 1000) > 0 ? s.length : s.length;
const seg = s.slice(start, end);
let i = -1, n = 0;
while ((i = seg.indexOf("'label': '结算周期'", i + 1)) > -1) {
  n++;
  const ls = seg.lastIndexOf('\n', i) + 1;
  const le = seg.indexOf('\n', i);
  const ne = seg.indexOf('\n', le + 1);
  console.log('#' + n);
  console.log('  ROW: ' + JSON.stringify(seg.slice(ls, le)));
  console.log('  NXT: ' + JSON.stringify(seg.slice(le + 1, ne)));
}
console.log('总数:', n);
console.log('=== DW-0001 现态（协议税点已删验证）===');
let j = -1;
while ((j = seg.indexOf('协议税点', j + 1)) > -1) console.log('  残留:', JSON.stringify(seg.slice(j - 20, j + 40)));
console.log('协议税点残留数:', seg.split('协议税点').length - 1);
