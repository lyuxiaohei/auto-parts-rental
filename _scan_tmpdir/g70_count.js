const fs = require('fs');
const s = fs.readFileSync('P3-R01-包装租赁管理后台原型/_data/demo-data.js', 'utf8');
['华东中心仓 / 全库区', '华东中心仓 / 组装区 RD', '华东中心仓 / 成品区 RB', '华东中心仓 / 原料区 RA', '华东中心仓 / 退货区 RC', "'label': '盘点范围'", "label: '盘点范围'"].forEach((w) => {
  console.log(s.split(w).length - 1 + ' × ' + w);
});
const i = s.indexOf('盘点范围');
console.log('首处上下文:', JSON.stringify(s.slice(i - 60, i + 60)));
