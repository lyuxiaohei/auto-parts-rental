/* G66 全量字段名扫描（只读）：
 * 提取每个实体在 列表(thead列头) / 新建(.form-label) / 详情(demo-data formRows) / 编辑(op 目标) 四处的字段名，输出对照清单。
 * 用法: node _scan_tmpdir/g66_field_scan.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = 'P3-R01-包装租赁管理后台原型';
global.window = {};
require(path.join(__dirname, '..', ROOT, '_data', 'demo-data.js'));
const D = window.DEMO_DATA;

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f);
    const st = fs.statSync(p);
    if (st.isDirectory()) {
      if (f === 'mobile' || f === 'P3-R01-F01-业务流程导航图' || f === '弹窗' || f.startsWith('P3-R01-F01')) continue;
      walk(p, out);
    } else if (f.endsWith('.html')) out.push(p.replace(/\\/g, '/'));
  }
  return out;
}
const FILES = walk(ROOT);
const CONTENT = {};
FILES.forEach((f) => { CONTENT[f] = fs.readFileSync(f, 'utf8'); });

function strip(h) {
  return h.replace(/<[^>]*>/g, '').replace(/&times;/g, '×').replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
}
function mainThead(html) {
  const blocks = [...html.matchAll(/<thead[^>]*>([\s\S]*?)<\/thead>/g)].map((x) => x[1]);
  let best = null, bc = 0;
  for (const b of blocks) {
    const ths = [...b.matchAll(/<th([^>]*)>([\s\S]*?)<\/th>/g)].map((t) => {
      const cm = /colspan\s*=\s*"?(\d+)/.exec(t[1]);
      return { label: strip(t[2]) || '（空）', span: cm ? +cm[1] : 1 };
    });
    const total = ths.reduce((a, s) => a + s.span, 0);
    if (total > bc) { bc = total; best = ths; }
  }
  return best;
}
function formLabels(html) {
  return [...html.matchAll(/<div class="form-label"[^>]*>([\s\S]*?)<\/div>/g)]
    .map((x) => strip(x[1]).replace(/^\*\s*/, '').replace(/[:：]$/, ''))
    .filter(Boolean);
}
function filterLabels(html) {
  return [...html.matchAll(/<span class="ff-label">([\s\S]*?)<\/span>/g)].map((x) => strip(x[1]).replace(/[:：]$/, ''));
}
function cardTitles(html) {
  return [...html.matchAll(/<h3 class="card-title"[^>]*>([\s\S]*?)<\/h3>/g)].map((x) => strip(x[1]));
}
function norm(s) {
  return String(s).replace(/[*＊]/g, '').replace(/[（(]/g, '(').replace(/[）)]/g, ')')
    .replace(/\s+/g, '').replace(/[:：]$/, '');
}

const entities = Object.keys(D).filter((k) => k !== '_meta');

const out = [];
out.push('# G66 全量字段名扫描（列表 / 新建 / 详情 / 编辑）');
out.push('> 只读扫描·' + new Date().toISOString().slice(0, 16).replace('T', ' '));
out.push('');

const summary = [];

entities.forEach((ent) => {
  const recs = D[ent] || {};
  const keys = Object.keys(recs);
  if (!keys.length) return;
  const withRow = keys.filter((k) => recs[k].row);
  const sample = recs[withRow[0] || keys[0]];

  // 页面定位
  const listPages = FILES.filter((f) => /entity(?:'|\"|\s)*[:=]\s*['"]/.test(CONTENT[f]) && CONTENT[f].includes("'" + ent + "'"));
  const detailPages = FILES.filter((f) => new RegExp("ENT\\s*=\\s*['\"]" + ent + "['\"]").test(CONTENT[f]));
  // 新建页：列表页 head-btns 里 新建/录单 按钮目标
  const createPages = [];
  listPages.forEach((f) => {
    const html = CONTENT[f];
    const m = [...html.matchAll(/onclick="go\('([^']+)'\)"[^>]*>(新建[^<]*|录单[^<]*|新增[^<]*)</g)];
    m.forEach((x) => {
      let t = x[1].replace(/^\.\.\//, '');
      createPages.push(t);
    });
  });
  // 编辑载体：ops 编辑 act 目标
  let editTarget = '';
  (sample && sample.row && sample.row.ops ? sample.row.ops : []).forEach((o) => {
    if (o.t === '编辑' && o.act) {
      const mm = /go\('([^']+)'\)/.exec(o.act);
      if (mm) editTarget = mm[1].replace(/^\.\.\//, '');
    }
  });

  // 详情字段（demo-data formRows 首条）
  const detailLabels = (sample.formRows || []).map((r) => r.label);
  const itemCols = sample.itemCols || [];

  // 列表列头
  const listLabels = [];
  listPages.forEach((f) => {
    const ths = mainThead(CONTENT[f]);
    if (ths) listLabels.push({ page: f.replace(ROOT + '/', ''), labels: ths.map((t) => t.label + (t.span > 1 ? '(' + t.span + ')' : '')) });
  });

  // 新建字段
  const createLabels = [];
  [...new Set(createPages)].forEach((cp) => {
    const full = ROOT + '/' + cp.replace(/\\/g, '/');
    if (CONTENT[full]) createLabels.push({ page: cp, labels: formLabels(CONTENT[full]) });
  });

  // 统一判定（粗比对：列表↔新建↔详情 两两不匹配项）
  const L = new Set((listLabels[0] ? listLabels[0].labels : []).map(norm).filter((x) => x && x !== '（空）'));
  const C = new Set((createLabels[0] ? createLabels[0].labels : []).map(norm));
  const T = new Set(detailLabels.map(norm));
  const onlyL = [...L].filter((x) => !C.has(x) && !T.has(x));
  const onlyC = [...C].filter((x) => !L.has(x) && !T.has(x));
  const onlyT = [...T].filter((x) => !L.has(x) && !C.has(x));

  out.push('## ' + ent + '（' + keys.length + ' 条）');
  out.push('- 列表页: ' + (listPages.join(' | ') || '—'));
  out.push('- 详情页: ' + (detailPages.join(' | ') || '—'));
  out.push('- 新建页: ' + ([...new Set(createPages)].join(' | ') || '—'));
  out.push('- 编辑载体: ' + (editTarget || '—'));
  listLabels.forEach((x) => out.push('- 列表列头[' + x.page + ']: ' + x.labels.join(' / ')));
  createLabels.forEach((x) => out.push('- 新建字段[' + x.page + ']: ' + x.labels.join(' / ')));
  out.push('- 详情字段: ' + detailLabels.join(' / '));
  if (itemCols.length) out.push('- 明细列: ' + itemCols.join(' / '));
  const flags = [];
  if (onlyL.length) flags.push('仅列表有: ' + onlyL.join('、'));
  if (onlyC.length) flags.push('仅新建有: ' + onlyC.join('、'));
  if (onlyT.length) flags.push('仅详情有: ' + onlyT.join('、'));
  out.push('- ⚠️ 差异: ' + (flags.length ? flags.join(' ｜ ') : '（粗比对未见单向独有）'));
  out.push('');

  summary.push({ ent, list: listPages.length, create: createLabels.length, detail: detailPages.length, warn: flags.length });
});

fs.writeFileSync('_scan_tmpdir/g66_field_inventory.md', out.join('\n'), 'utf8');
console.log('实体数:', entities.length, '· 页面文件数:', FILES.length);
console.log('有差异标记的实体数:', summary.filter((s) => s.warn).length);
summary.filter((s) => s.warn).forEach((s) => console.log(' ⚠️ ' + s.ent));
console.log('输出: _scan_tmpdir/g66_field_inventory.md');
