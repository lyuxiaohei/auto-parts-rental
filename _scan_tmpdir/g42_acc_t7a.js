ObjC.import("Foundation");
var path = "/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js";
var src = $.NSString.stringWithContentsOfFileEncodingError(path, $.NSUTF8StringEncoding, null).js;
var f = new Function("window", src + "\n;return window.DEMO_DATA;");
var d = f({});
var partners = d.partners;
var keys = Object.keys(partners);
console.log("partnersCount=" + keys.length);
keys.forEach(function(k){
  var rec = partners[k];
  // invoiceTaxNo might be in row.fields or info
  var tax = null;
  if (rec.row && rec.row.fields && rec.row.fields.invoiceTaxNo) tax = rec.row.fields.invoiceTaxNo;
  var infoTax = null;
  if (rec.info) rec.info.forEach(function(it){ if (it.label.indexOf("纳税人识别号")>=0 || it.label.indexOf("税号")>=0) infoTax = it.text; });
  // deep search fallback
  if (!tax) { var s = JSON.stringify(rec); var mm = s.match(/9\\d{16}/); if (mm) tax = mm[0]; }
  console.log(k + " | fieldTaxNo=" + tax + " | infoTax=" + infoTax);
});
