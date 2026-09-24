const fs = require('fs');
const src = fs.readFileSync('P3-R01-包装租赁管理后台原型/_data/demo-data.js', 'utf8');
const SO = ['SO-20260903-0047', 'SO-20260902-0046', 'SO-20260901-0045', 'SO-20260831-0044', 'SO-20260830-0043', 'SO-20260828-0041', 'SO-20260827-0039', 'SO-20260820-0036'];
const PO = ['PO-20260910-019', 'PO-20260902-018', 'PO-20260901-017', 'PO-20260830-016', 'PO-20260828-015', 'PO-20260825-014', 'PO-20260820-013', 'PO-20260815-012'];
console.log('=== 订单状态 旧串（16）===');
PO.concat(SO).forEach((n) => {
  const i = src.indexOf("'text': '" + n + "' },");
  if (i < 0) { console.log(n, 'NOT FOUND'); return; }
  console.log(JSON.stringify(src.slice(i, i + 70)));
});
console.log('=== 归还时间 行（3）===');
let i = -1, c = 0;
while ((i = src.indexOf("'label': '归还时间'", i + 1)) > -1 && c < 3) {
  c++;
  console.log(c, JSON.stringify(src.slice(i, i + 55)));
  console.log('   pre:', JSON.stringify(src.slice(Math.max(0, i - 90), i)));
}
