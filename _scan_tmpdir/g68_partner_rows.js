const fs = require('fs');
global.window = {};
require(require('path').join(__dirname, '..', 'P3-R01-包装租赁管理后台原型/_data/demo-data.js'));
const D = window.DEMO_DATA;
Object.keys(D.partners).forEach((k) => {
  const r = D.partners[k];
  const rows = r.formRows || [];
  const idx = [];
  rows.forEach((x, i) => {
    if (x.label === '协议税点' || x.label === '结算周期' || x.label === '发票类型') {
      idx.push(i + ':' + (x.label === '协议税点' ? '税点' : x.label) + '=' + String(x.text).slice(0, 18));
    }
  });
  console.log(k, '| 类型:' + r.row.fields.type, '|', idx.join(' , '));
});
