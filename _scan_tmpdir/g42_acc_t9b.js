ObjC.import("Foundation");
var path = "/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js";
var src = $.NSString.stringWithContentsOfFileEncodingError(path, $.NSUTF8StringEncoding, null).js;
var f = new Function("window", src + "\n;return window.DEMO_DATA;");
var d = f({});
Object.keys(d.rentInReturns).forEach(function(k){
  (d.rentInReturns[k].info||[]).forEach(function(it){
    var s = (it.label||"") + " " + (it.text||"");
    if (s.indexOf("押金")>=0) console.log(k + " -> " + it.label + ": " + it.text);
  });
});
