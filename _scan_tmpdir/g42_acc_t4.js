ObjC.import("Foundation");
var path = "/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js";
var src = $.NSString.stringWithContentsOfFileEncodingError(path, $.NSUTF8StringEncoding, null).js;
var f = new Function("window", src + "\n;return window.DEMO_DATA;");
var d = f({});
var di = d.dictItems;
// find 应收账单类型 group
var keys = Object.keys(di);
console.log("dictItemsGroups=" + keys.length);
for (var i=0;i<keys.length;i++){
  var g = di[keys[i]];
  var nameField = (g && g.name) ? g.name : keys[i];
  if (String(nameField).indexOf("应收账单类型")>=0 || String(keys[i]).indexOf("应收")>=0){
    console.log("group=" + keys[i] + " name=" + nameField);
    console.log("json=" + JSON.stringify(g).substring(0, 900));
  }
}
