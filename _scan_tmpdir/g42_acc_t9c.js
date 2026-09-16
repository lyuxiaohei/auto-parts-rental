ObjC.import("Foundation");
var path = "/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js";
var src = $.NSString.stringWithContentsOfFileEncodingError(path, $.NSUTF8StringEncoding, null).js;
var f = new Function("window", src + "\n;return window.DEMO_DATA;");
var d = f({});
Object.keys(d.rentInReturns).forEach(function(k){
  var r = d.rentInReturns[k];
  var st = (r.row && r.row.fields && r.row.fields.status) || "?";
  var ref = (r.row && r.row.fields && (r.row.fields.ref || r.row.fields.rentInOrder)) || "?";
  console.log(k + " status=" + st + " ref=" + ref);
});
var rio = d.rentInOrders || {};
Object.keys(rio).forEach(function(k){
  var s = JSON.stringify(rio[k]);
  var dep = s.match(/押金[^0-9]*([0-9,]+)/);
  console.log("rentInOrder " + k + " deposit=" + (dep?dep[1]:"?"));
});
