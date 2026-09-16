ObjC.import("Foundation");
var path = "/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/_data/demo-data.js";
var src = $.NSString.stringWithContentsOfFileEncodingError(path, $.NSUTF8StringEncoding, null).js;
var f = new Function("window", src + "\n;return window.DEMO_DATA;");
var d = f({});
var rb = Object.keys(d.receivableBills), pb = Object.keys(d.payableBills);
var counts = {};
function tally(entName, obj){
  Object.keys(obj).forEach(function(k){
    var s = JSON.stringify(obj[k]);
    var re = /(?:AR|AP)-[A-Z0-9-]+/g, m;
    while ((m = re.exec(s))) {
      var tok = m[0].replace(/[\"',.\]\}]$/,"");
      var key = entName + "|" + tok;
      counts[key] = (counts[key]||0) + 1;
    }
  });
}
tally("projectDocs", d.projectDocs);
tally("boardRows", d.boardRows);
tally("profitRows", d.profitRows);
var bad = [], total = 0, uniq = {};
Object.keys(counts).forEach(function(key){
  var tok = key.split("|")[1];
  uniq[tok] = true;
  var inRB = rb.indexOf(tok)>=0, inPB = pb.indexOf(tok)>=0;
  var prefixOk = (tok.indexOf("AR-")===0 || tok.indexOf("AP-")===0);
  total += counts[key];
  if (prefixOk && !inRB && !inPB) bad.push(key + " x" + counts[key]);
});
console.log("receivableBills=" + rb.length + " payableBills=" + pb.length);
console.log("total_token_occurrences=" + total + " unique_tokens=" + Object.keys(uniq).length);
console.log("all_tokens=" + JSON.stringify(Object.keys(uniq)));
console.log("notInKeySet=" + JSON.stringify(bad));
