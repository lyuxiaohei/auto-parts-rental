ObjC.import("Foundation");
var path = "/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js";
var src = $.NSString.stringWithContentsOfFileEncodingError(path, $.NSUTF8StringEncoding, null).js;
// find window.DEMO_DATA assignment; execute in sandbox object
var code = src + "\n;return JSON.stringify({payments: (typeof DEMO_DATA!=='undefined'?DEMO_DATA:null)});";
var f = new Function("window", code.replace(/window\.DEMO_DATA\s*=/, "window.DEMO_DATA ="));
var w = {};
try {
  var out = f(w);
  var d = JSON.parse(out).payments || w.DEMO_DATA;
  console.log("hasPayments=" + (d && d.payments ? true : false));
  if (d && d.payments) {
    var p = d.payments["PAY-20260818-001"];
    console.log("PAY-20260818-001=" + JSON.stringify(p));
    var pb = d.payableBills || {};
    if (p && p.ref) {
      console.log("refValue=" + p.ref);
      console.log("refInPayableBills=" + (p.ref in pb || Object.keys(pb).indexOf(p.ref) >= 0));
    }
    console.log("payableBillsKeyCount=" + Object.keys(pb).length);
  }
} catch (e) {
  console.log("ERR: " + e.message);
}
