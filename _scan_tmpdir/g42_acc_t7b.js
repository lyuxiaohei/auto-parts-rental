ObjC.import("Foundation");
var path = "/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js";
var src = $.NSString.stringWithContentsOfFileEncodingError(path, $.NSUTF8StringEncoding, null).js;
var f = new Function("window", src + "\n;return window.DEMO_DATA;");
var d = f({});
var p = d.partners["DW-0001"];
console.log("DW-0001 topKeys=" + JSON.stringify(Object.keys(p)));
if (p.info2) console.log("info2=" + JSON.stringify(p.info2));
var cnt = 0;
Object.keys(d.partners).forEach(function(k){
  var has = d.partners[k].info2 ? JSON.stringify(d.partners[k].info2).indexOf("纳税人识别号")>=0 : false;
  if (has) cnt++;
});
console.log("partners_with_info2_纳税人识别号=" + cnt + "/8");
