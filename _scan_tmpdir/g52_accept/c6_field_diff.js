// G52 独立验收 ⑥ A03 原文 vs NOTES_DATA 逐条全字段语义 diff（node vm 语义比对，非文本 diff）
// 用法: node c6_field_diff.js  （在原型目录下运行，或用绝对路径）
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const PROTO_ROOT = 'D:\\工作台-吕道远\\5-【ACTIVE】汽车物流包装租赁\\P3-R01-包装租赁管理后台原型';
const SAMPLE_KEYS = [
  '财务协同/银行回单核销.html', // 样板页 4 条
  '首页/项目看板.html',          // 首页模块 7 条
  '仓储作业/库存查询.html'       // 仓储模块 6 条
];

const code = fs.readFileSync(path.join(PROTO_ROOT, '_data', 'notes-data.js'), 'utf8');
const ctx = { window: {} };
vm.createContext(ctx);
vm.runInContext(code, ctx);
const NOTES_DATA = ctx.window.NOTES_DATA;

const a03 = JSON.parse(fs.readFileSync(path.join(PROTO_ROOT, 'P3-R01-A03-标注数据.json'), 'utf8'));

const FIELDS = ['id', 'title', 'note', 'fp', 'req', 'selector'];
let totalDiff = 0;

for (const key of SAMPLE_KEYS) {
  const ndArr = NOTES_DATA[key] || [];
  const aArr = a03[key] || [];
  let pageDiff = 0;
  if (ndArr.length !== aArr.length) {
    console.log(`[${key}] 条数不一致 A03=${aArr.length} ND=${ndArr.length}`);
    pageDiff++;
  }
  const n = Math.max(ndArr.length, aArr.length);
  for (let i = 0; i < n; i++) {
    const a = aArr[i], b = ndArr[i];
    for (const f of FIELDS) {
      const av = a ? a[f] : undefined;
      const bv = b ? b[f] : undefined;
      if (JSON.stringify(av) !== JSON.stringify(bv)) {
        pageDiff++;
        console.log(`[${key}] entry#${i} field ${f} DIFF:\n  A03=${JSON.stringify(av)}\n  ND =${JSON.stringify(bv)}`);
      }
    }
  }
  console.log(`[${key}] A03 ${aArr.length} 条 / ND ${ndArr.length} 条 -> field diffs = ${pageDiff}`);
  totalDiff += pageDiff;
}

console.log('----');
console.log(`抽样 3 页全字段语义 diff 总数 = ${totalDiff}（0 为通过）`);
