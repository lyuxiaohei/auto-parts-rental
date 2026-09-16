ObjC.import("Foundation");
var path = "/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js";
var src = $.NSString.stringWithContentsOfFileEncodingError(path, $.NSUTF8StringEncoding, null).js;
var f = new Function("window", src + "\n;return window.DEMO_DATA;");
var d = f({});
var rf = d.refunds;
console.log("refunds=" + Object.keys(rf).length + " keys=" + JSON.stringify(Object.keys(rf)));
["TKD-20260916-004","TKD-20260916-005"].forEach(function(k){
  var r = rf[k];
  if (!r) { console.log(k + " MISSING"); return; }
  var st = (r.row && r.row.fields && r.row.fields.status) || "?";
  var ty = (r.row && r.row.fields && r.row.fields.refundType) || "";
  var infoS = JSON.stringify(r.info||[]);
  console.log(k + " status=" + st + " typeField=" + ty + " infoHasType=" + infoS);
});
var ap12 = d.payableBills["AP-20260905-012"];
var tl = JSON.stringify(ap12.timeline || []);
console.log("AP-20260905-012 timelineHasTKD005=" + (tl.indexOf("TKD-20260916-005")>=0));
var tlItems = (ap12.timeline||[]).filter(function(t){ return String(t.text).indexOf("TKD")>=0; });
console.log("timeline TKD entries=" + JSON.stringify(tlItems));
