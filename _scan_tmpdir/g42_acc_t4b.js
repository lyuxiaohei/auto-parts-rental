ObjC.import("Foundation");
var path = "/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js";
var src = $.NSString.stringWithContentsOfFileEncodingError(path, $.NSUTF8StringEncoding, null).js;
var f = new Function("window", src + "\n;return window.DEMO_DATA;");
var d = f({});
var di = d.dictItems;
var arRows = [], tkRows = [], thRows = [];
Object.keys(di).forEach(function(k){
  var cat = di[k].row.fields.category;
  if (cat === "应收账单类型") arRows.push(k + ":" + di[k].row.fields.abbr + "/" + di[k].row.fields.name);
  if (cat === "退款类型") tkRows.push(k + ":" + di[k].row.fields.abbr + "/" + di[k].row.fields.name);
  if (cat === "退货类型") thRows.push(k + ":" + di[k].row.fields.abbr + "/" + di[k].row.fields.name);
});
console.log("AR组(" + arRows.length + ")=" + JSON.stringify(arRows, null, 0));
console.log("TK组(" + tkRows.length + ")=" + JSON.stringify(tkRows, null, 0));
console.log("TH组(" + thRows.length + ")=" + JSON.stringify(thRows, null, 0));
console.log("has_ARB07=" + (arRows.some(function(r){return r.indexOf("ARB-07")===0;})));
console.log("ARB07_has_预收=" + arRows.some(function(r){return r.indexOf("ARB-07")===0 && r.indexOf("预收")>=0;}));
