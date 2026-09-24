const fs = require('fs');
const s = fs.readFileSync('P3-R01-包装租赁管理后台原型/_data/demo-data.js', 'utf8');
console.log('协议税点 残留:', s.split('协议税点').length - 1);
console.log("'label': '结算周期' 残留行:", s.split("'label': '结算周期'").length - 1);
let i = -1, n = 0;
while ((i = s.indexOf("'label': '结算周期'", i + 1)) > -1) {
  n++;
  const a = s.lastIndexOf('\n', i) + 1;
  const b = s.indexOf('\n', i);
  console.log('#' + n, JSON.stringify(s.slice(a, b)));
}
