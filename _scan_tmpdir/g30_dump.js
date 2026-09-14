global.window={};global.document={};
require("D:/\u5de5\u4f5c\u53f0-\u5415\u9053\u8fdc/5-\u3010ACTIVE\u3011\u6c7d\u8f66\u7269\u6d41\u5305\u88c5\u79df\u8d41/P3-R01-\u5305\u88c5\u79df\u8d41\u7ba1\u7406\u540e\u53f0\u539f\u578b/_data/demo-data.js");
var di=window.DEMO_DATA.dictItems,ks=Object.keys(di),g={};
for(var i=0;i<ks.length;i++){var c=di[ks[i]].row.fields.category;g[c]=(g[c]||0)+1;}
console.log(JSON.stringify({n:ks.length,g:Object.keys(g).length,kc:g["库存状态"],rku:g["入库类型"],cku:g["出库类型"],arb:g["应收账单类型"],apb:g["应付账单类型"],fy:g["费用分类"],fp:g["发票类型"],kst:g["客商类型"],sjq:g["数据权限范围"],pdk:g["盘点口径"],zq:g["周期单位"],fl:g["物料分类"],dj:g["待办单据类型"],dw:g["计量单位"],zf:g["支付方式"],zf02:di["ZF-02"].row.fields.name,dj01:di["DJ-01"].row.fields.name,dj16:di["DJ-16"].row.fields.name}));
