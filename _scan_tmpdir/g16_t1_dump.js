// G16 T1: dump demo-data.js to JSON for field-dictionary extraction
// 运行：node _scan_tmpdir/g16_t1_dump.js（在原型根 P3-R01-包装租赁管理后台原型 下执行时改路径）
const path = require('path');
const dataPath = path.resolve(__dirname, '..', 'P3-R01-包装租赁管理后台原型', '_data', 'demo-data.js');
global.window = {};
require(dataPath);
const D = global.window.DEMO_DATA;
const fs = require('fs');
const out = path.resolve(__dirname, 'g16_data_dump.json');
fs.writeFileSync(out, JSON.stringify(D, null, 1), 'utf-8');
// 概览输出（键 + 每实体记录数）
const keys = Object.keys(D).filter(k => !k.startsWith('_'));
const summary = keys.map(k => {
  const v = D[k];
  const n = (v && typeof v === 'object') ? Object.keys(v).length : 0;
  return `${k}\t${n}`;
});
fs.writeFileSync(path.resolve(__dirname, 'g16_dump_summary.txt'), `实体数: ${keys.length}\n` + summary.join('\n'), 'utf-8');
console.log('dump ok ->', out);
