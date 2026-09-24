const fs = require('fs');
global.window = {};
require(require('path').join(__dirname, '..', 'P3-R01-包装租赁管理后台原型/_data/demo-data.js'));
const D = window.DEMO_DATA;
console.log('assetTracks formTitle:', D.assetTracks[Object.keys(D.assetTracks)[0]].formTitle);
console.log('rentTracks formTitle:', D.rentTracks[Object.keys(D.rentTracks)[0]].formTitle);
const s = fs.readFileSync('P3-R01-包装租赁管理后台原型/_data/demo-data.js', 'utf8');
console.log('器具 残留:', s.split('器具').length - 1);
let i = -1, n = 0;
while ((i = s.indexOf('器具', i + 1)) > -1 && n < 10) {
  n++;
  console.log(' #' + n, JSON.stringify(s.slice(i - 40, i + 20)));
}
