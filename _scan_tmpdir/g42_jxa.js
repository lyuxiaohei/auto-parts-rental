// G42 · node 无机环境替代（G22 先例）：JXA 加载 demo-data.js 并执行传入脚本文件中的断言/统计代码
// 用法: osascript -l JavaScript _scan_tmpdir/g42_jxa.js <snippet.js>
// snippet.js 内可用: D (=window.DEMO_DATA), 并须把结果数组赋给 OUT（每项 {name, ok, detail} 或任意 JSON）
ObjC.import('Foundation');
function run(argv) {
  var ddPath = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js';
  var src = $.NSString.stringWithContentsOfFileEncodingError(ddPath, $.NSUTF8StringEncoding, null).js;
  if (!src) throw new Error('read demo-data.js failed');
  // 语法门：new Function 编译等价 node --check
  var w = {};
  var fn = new Function('window', src);
  fn(w);
  var D = w.DEMO_DATA;
  var OUT = [];
  var snippetPath = argv[0];
  if (snippetPath) {
    var code = $.NSString.stringWithContentsOfFileEncodingError(snippetPath, $.NSUTF8StringEncoding, null).js;
    if (!code) throw new Error('read snippet failed: ' + snippetPath);
    // eslint-disable-next-line no-eval
    var f = new Function('D', 'OUT', code);
    f(D, OUT);
  } else {
    OUT.push({ name: 'syntax-check', ok: true, detail: 'new Function compile OK' });
  }
  return JSON.stringify(OUT, null, 1);
}
