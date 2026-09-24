const fs = require('fs');
const src = fs.readFileSync('P3-R01-包装租赁管理后台原型/_data/demo-data.js', 'utf8');
let i = -1, c = 0;
while ((i = src.indexOf("'label': '归还时间'", i + 1)) > -1) {
  c++;
  const start = src.lastIndexOf("{ 'label': '归还类型'", i);
  console.log('#' + c + ' ' + JSON.stringify(src.slice(start, i + 60)));
}
