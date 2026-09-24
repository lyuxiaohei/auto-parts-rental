const fs = require('fs');
const src = fs.readFileSync('P3-R01-包装租赁管理后台原型/_data/demo-data.js', 'utf8');
function c(p) { const m = src.split(p).length - 1; return m; }
const pats = [
  "'label': '月租'", "'label': '退回日期'", "'label': '归还日期'", "'label': '建单日期'",
  "'label': '订单号'", "'label': '登记单号'", "'label': '购方名称（客户）'",
  "'label': '关联应付账单'", "'label': '关联应收账单'", "'label': '关联租赁单'",
  "'label': '关联销售订单'", "'label': '关联采购入库'", "'label': '关联销售出库'",
  "'label': '关联退款单'", "'label': '付款方'", "'label': '名称'",
  "'label': '客户（带出）'", "'label': '供应商（带出）'", "'label': '所属项目（带出）'",
  "'label': '物料类别'", "'label': '器具编码'", "'label': '租金'", "'label': '关联退货单'",
  "label: '关联采购订单'", "label: '关联采购入库'", "label: '关联租入单'",
  "label: '关联租入入库'", "label: '关联丢损赔偿单'",
  "'label': '客户端（on-hire）'", "器具 / 组合件",
  "（带出）"
];
pats.forEach((p) => console.log(c(p) + ' × ' + p));
