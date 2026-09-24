const fs = require('fs');
const files = {
  a03: 'P3-R01-包装租赁管理后台原型/P3-R01-A03-标注数据.json',
  notes: 'P3-R01-包装租赁管理后台原型/_data/notes-data.js'
};
const keys = ['租赁管理/租赁出库录单.html', '基础数据/BOM维护.html', '租入管理/归还出库新建.html', '租赁管理/租赁出库列表.html'];
Object.keys(files).forEach((tag) => {
  const s = fs.readFileSync(files[tag], 'utf8');
  keys.forEach((k) => {
    const i = s.indexOf('"' + k + '": [');
    if (i < 0) { console.log('[' + tag + '] ' + k + ' 未找到'); return; }
    let j = i, depth = 0, end = -1;
    for (let x = i; x < s.length; x++) {
      if (s[x] === '[') depth++;
      else if (s[x] === ']') { depth--; if (depth === 0) { end = x; break; } }
    }
    console.log('===== [' + tag + '] ' + k);
    console.log(s.slice(Math.max(0, end - 300), end + 80));
  });
});
