ObjC.import("Foundation");
var path = "/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js";
var src = $.NSString.stringWithContentsOfFileEncodingError(path, $.NSUTF8StringEncoding, null).js;
var f = new Function("window", src + "\n;return window.DEMO_DATA;");
var d = f({});
console.log("AR-2026-09-PRJ2601-YS in receivableBills=" + ("AR-2026-09-PRJ2601-YS" in d.receivableBills));
var b = d.receivableBills["AR-2026-09-PRJ2601-YS"];
console.log("type=" + (b.row&&b.row.fields?(b.row.fields.billType||b.row.fields.type):"?"));
console.log("amount=" + JSON.stringify(b.row.fields).substring(0,200));
