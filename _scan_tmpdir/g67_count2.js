const fs = require('fs');
const src = fs.readFileSync('P3-R01-包装租赁管理后台原型/_data/demo-data.js', 'utf8');
function show(label, n, len) {
  let i = -1, c = 0;
  while ((i = src.indexOf(label, i + 1)) > -1 && c < n) {
    console.log('--- ' + label + ' #' + (++c));
    console.log(src.slice(Math.max(0, i - 60), i + (len || 70)).replace(/\n/g, '\\n'));
  }
}
show("关联应付账单", 1);
show("登记单号", 1, 60);
show("购方名称", 1);
show("关联销售出库", 2);
show("关联退款单", 1);
show("付款方", 1, 40);
show("关联退货单", 1);
show("月租", 1, 40);
show("退回日期", 2, 40);
console.log('=== 计数器 ===');
['label: \'登记单号\'', "label: '购方名称（客户）'", "label: '关联应付账单'", "label: '关联销售出库'", "label: '关联退款单'", "label: '付款方'", "'label': '退货类型'", "label: '关联退货单'"].forEach((p) => console.log(src.split(p).length - 1 + ' × ' + p));
