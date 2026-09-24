const fs = require('fs');
const s = fs.readFileSync('P3-R01-包装租赁管理后台原型/P3-R01-A03-标注数据.json', 'utf8');
const key = '"基础数据/客商新建.html": [';
const i = s.indexOf(key);
const j = s.indexOf('],', i);
console.log(JSON.stringify(s.slice(j - 320, j + 70)));
