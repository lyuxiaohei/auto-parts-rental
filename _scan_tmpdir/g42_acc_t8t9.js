ObjC.import("Foundation");
var path = "/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js";
var src = $.NSString.stringWithContentsOfFileEncodingError(path, $.NSUTF8StringEncoding, null).js;
var f = new Function("window", src + "\n;return window.DEMO_DATA;");
var d = f({});
console.log("returnInbounds=" + Object.keys(d.returnInbounds).length + " has_TZRK-20260915-012=" + ("TZRK-20260915-012" in d.returnInbounds));
console.log("stockEvents=" + Object.keys(d.stockEvents).length + " has_EV-20260915-023=" + ("EV-20260915-023" in d.stockEvents));
console.log("stockFlows=" + Object.keys(d.stockFlows).length);
var rir = d.rentInReturns;
console.log("rentInReturns=" + Object.keys(rir).length);
Object.keys(rir).forEach(function(k){
  var info = rir[k].info || [];
  var hasDeposit = JSON.stringify(info).indexOf("押金") >= 0;
  var depLine = "";
  info.forEach(function(it){ if (it.text && String(it.text).indexOf("押金")>=0) depLine = it.text; });
  console.log(k + " infoHas押金=" + hasDeposit + " | " + depLine);
});
