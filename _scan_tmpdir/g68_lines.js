const fs = require('fs');
const s = fs.readFileSync('P3-R01-包装租赁管理后台原型/_data/demo-data.js', 'utf8');
console.log('=== 协议税点 行原文 ===');
let i = -1, n = 0;
while ((i = s.indexOf('协议税点', i + 1)) > -1) {
  n++;
  const a = s.lastIndexOf('\n', i) + 1;
  const b = s.indexOf('\n', i);
  console.log(JSON.stringify(s.slice(a, b)));
}
console.log('协议税点 总数:', n);
console.log('=== 结算周期 行原文（partners 区段） ===');
i = s.indexOf('partners: {') > -1 ? 0 : 0;
let j = s.indexOf('partners: {');
const seg = s.slice(j, s.indexOf('  /* ', j + 100) > 0 ? s.indexOf('\n\n', j) : s.length);
let m = -1, c = 0;
while ((m = seg.indexOf('结算周期', m + 1)) > -1) {
  c++;
  const a = seg.lastIndexOf('\n', m) + 1;
  const b = seg.indexOf('\n', m);
  console.log(JSON.stringify(seg.slice(a, b)));
}
console.log('=== 各记录 联系电话 行 ===');
global.window = {};
require(require('path').join(__dirname, '..', 'P3-R01-包装租赁管理后台原型/_data/demo-data.js'));
Object.keys(window.DEMO_DATA.partners).forEach((k) => {
  const r = window.DEMO_DATA.partners[k];
  const rows = r.formRows || [];
  const phone = rows.filter((x) => x.label === '联系电话')[0];
  const settle = rows.filter((x) => x.label === '结算周期')[0];
  console.log(k, '| 电话行:', JSON.stringify(phone), '| 结算周期行:', JSON.stringify(settle));
});
