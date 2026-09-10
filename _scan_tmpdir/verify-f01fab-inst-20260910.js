/* 静态断言：f01-fab 注入 + 分期自由笔数（2026-09-10 第二轮） */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', 'P3-R01-包装租赁管理后台原型');
const read = p => fs.readFileSync(path.isAbsolute(p) ? p : path.join(ROOT, p), 'utf8');

let pass = 0, fail = 0;
function chk(name, cond) {
  console.log((cond ? 'PASS' : 'FAIL') + '  ' + name);
  cond ? pass++ : fail++;
}

/* --- 任务1 f01-fab --- */
function walk(dir) {
  let out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out = out.concat(walk(p));
    else if (e.name.endsWith('.html')) out.push(p);
  }
  return out;
}
const pages = walk(ROOT);
const withFab = pages.filter(p => read(p).includes('f01-fab'));
chk('T1-P1 f01-fab 注入页数 = 107（108 - F01自身）', withFab.length === 107 && pages.length === 108);
chk('T1-P2 F01 自身无按钮', !read('P3-R01-F01-业务流程导航图.html').includes('f01-fab'));
// 路径深度抽查
chk('T1-P3 根级 我的待办.html → 无前缀', read('我的待办.html').includes("location.href='P3-R01-F01-业务流程导航图.html'"));
chk('T1-P4 一层 应付账单.html → ../', read('财务协同/应付账单.html').includes("location.href='../P3-R01-F01-业务流程导航图.html'"));
chk('T1-P5 两层 弹窗/租入归还新建.html → ../../', read('租赁管理/弹窗/租入归还新建.html').includes("location.href='../../P3-R01-F01-业务流程导航图.html'"));
chk('T1-P6 有标注页用 fab-row 并排（pn-fab 包进容器）', read('财务协同/应付账单.html').includes('<div class="fab-row"><div class="f01-fab"'));
chk('T1-P7 全部注入页 f01-fab 恰好 1 个 div', withFab.every(p => read(p).split('class="f01-fab"').length - 1 === 1));

/* --- 任务2 分期自由笔数 --- */
const f7 = ['财务协同/应付账单.html', '财务协同/应收账单.html', '财务协同/付款登记.html',
  '财务协同/弹窗/应付账单新建.html', '财务协同/弹窗/应收账单生成.html', '财务协同/弹窗/付款登记新建.html'];
chk('T2-P1 「分 1/2/3 期」全站残留 = 0', pages.every(p => !/分 [123] 期/.test(read(p))));
chk('T2-P2 期数 select 全清（cmInstN/instN/instNM）', f7.every(f => !/id="(cmInstN|instN|instNM)"/.test(read(f))));
chk('T2-P3 添加/剩余全排按钮在位', read('财务协同/应付账单.html').includes('id="cmInstAdd"') && read('财务协同/应付账单.html').includes('id="instAdd"') && read('财务协同/付款登记.html').includes('id="instAddM"'));
chk('T2-P4 「笔次」表头替换「期次」（7文件均无旧表头）', f7.every(f => { const s = read(f); return s.includes('笔次') && !s.includes('<th>期次</th>'); }));
chk('T2-P5 instModal data-note="4" 保留', /<div class="modal-overlay" id="instModal">[\s\S]*?<th data-note="4">笔次<\/th>/.test(read('财务协同/应付账单.html')));
chk('T2-P6 默认演示 2 笔 60/40', f7.every(f => read(f).includes('cfg.defs || [60, 40]')));
chk('T2-P7 合计行含 已排合计/剩余/账单金额', read('财务协同/应付账单.html').includes('已排合计') && read('财务协同/应付账单.html').includes('剩余 <b id='));
chk('T2-P8 无 console.log 残留', f7.every(f => !read(f).includes('console.log')));
chk('T2-P9 弹窗副本与主页面工厂一致', ['财务协同/弹窗/应付账单新建.html', '财务协同/弹窗/应收账单生成.html', '财务协同/弹窗/付款登记新建.html'].every(f => read(f).includes('function createInstPlan(cfg)')));

console.log('\n== 合计 PASS ' + pass + ' / FAIL ' + fail + ' ==');
process.exit(fail ? 1 : 0);
