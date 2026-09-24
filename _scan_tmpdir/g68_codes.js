const fs = require('fs');
const s = fs.readFileSync('P3-R01-包装租赁管理后台原型/_data/demo-data.js', 'utf8');
const i = s.indexOf("'label': '结算周期'");
const a = s.lastIndexOf('\n', i) + 1;
const b = s.indexOf('\n', i);
const line = s.slice(a, b);
console.log('line:', line);
console.log('codes:', [...line].map((c) => c.charCodeAt(0)).join(','));
