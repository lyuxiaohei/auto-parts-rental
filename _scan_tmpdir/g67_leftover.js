const fs = require('fs');
const s = fs.readFileSync('P3-R01-包装租赁管理后台原型/_data/demo-data.js', 'utf8');
['关联租入单', '关联盘点单', '关联赔偿单'].forEach((w) => {
  const p = "'label': '" + w + "'";
  let i = -1, n = 0;
  while ((i = s.indexOf(p, i + 1)) > -1) {
    n++;
    console.log('--- ' + p + ' #' + n);
    console.log(JSON.stringify(s.slice(i - 100, i + 60)));
  }
  if (!n) console.log('--- ' + p + ' 无命中');
});
