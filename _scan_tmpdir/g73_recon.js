const fs = require('fs');
const path = require('path');
const ROOT = 'P3-R01-包装租赁管理后台原型';
global.window = {};
require(path.join(__dirname, '..', ROOT, '_data', 'demo-data.js'));
const D = window.DEMO_DATA;

function walk(dir, out = []) {
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f);
    const st = fs.statSync(p);
    if (st.isDirectory()) { if (f === 'mobile') continue; walk(p, out); } else if (f.endsWith('.html')) out.push(p.replace(/\\/g, '/'));
  }
  return out;
}
const FILES = walk(ROOT);
const CONTENT = {};
FILES.forEach((f) => { CONTENT[f] = fs.readFileSync(f, 'utf8'); });

const out = [];
out.push('# G73/G74 任务排查底稿（生成单跳转 + 批量审核铺开）');
out.push('');

// A. 批量审核现状
out.push('## A. 批量审核现状');
const batchPages = FILES.filter((f) => /批量审核/.test(CONTENT[f]));
batchPages.forEach((f) => out.push('- 已有批量审核: ' + f));
out.push('');

// 含审核 op 的实体 → 对应列表页
out.push('## A2. 含「审核」op 的实体 → 列表页/行');
Object.keys(D).forEach((e) => {
  if (e === '_meta') return;
  const rows = [];
  Object.keys(D[e] || {}).forEach((k) => {
    const ops = ((D[e][k].row || {}).ops) || [];
    ops.forEach((o) => { if (o.t === '审核') rows.push(k); });
  });
  if (!rows.length) return;
  const pages = FILES.filter((f) => new RegExp("entity\\s*:\\s*'" + e + "'").test(CONTENT[f]));
  out.push('- ' + e + '（' + rows.length + ' 行: ' + rows.join(',') + '）');
  pages.forEach((p) => out.push('    - 列表页: ' + p));
});
out.push('');

// B. 生成XX单 ops（数据侧）
out.push('## B. 数据侧「生成」op 全量（t / act）');
Object.keys(D).forEach((e) => {
  if (e === '_meta') return;
  Object.keys(D[e] || {}).forEach((k) => {
    const ops = ((D[e][k].row || {}).ops) || [];
    ops.forEach((o) => {
      if (o.t.indexOf('生成') > -1) out.push('- ' + e + ' | ' + k + ' | ' + o.t + ' => ' + (o.act || '（无跳转）'));
    });
  });
});
out.push('');

// C. 页面静态行「生成」按钮（含 onclick 原文）
out.push('## C. 页面静态「生成」按钮（onclick 原文）');
FILES.forEach((f) => {
  const lines = CONTENT[f].split('\n');
  lines.forEach((ln, i) => {
    if (/生成[^<>]{0,8}单|生成入库|生成出库|生成采购|生成租入|生成应付|生成应收/.test(ln) && /onclick|<a/.test(ln)) {
      out.push('- ' + f + ':' + (i + 1) + ' :: ' + ln.trim().slice(0, 260));
    }
  });
});
out.push('');

// D. 新建/录单页清单（可用跳转目标）
out.push('## D. 新建/录单类页面清单');
FILES.filter((f) => /新建|录单/.test(f)).forEach((f) => out.push('- ' + f));
out.push('');

// E. batch-btn-js 覆盖（批量按钮禁用/启用机制）
out.push('## E. 含 batch-btn-js 的页面（批量按钮启用机制已件）');
FILES.filter((f) => CONTENT[f].indexOf('batch-btn-js') > -1).forEach((f) => out.push('- ' + f));
out.push('');

// F. showGen 定义（盘点列表）
out.push('## F. showGen 定义（盘点列表.html）');
{
  const f = ROOT + '/仓储作业/盘点列表.html';
  const s = CONTENT[f] || '';
  const i = s.indexOf('function showGen');
  out.push(i > -1 ? s.slice(i, i + 900) : '（未找到 showGen）');
}
out.push('');

// G. 采购订单列表 G64 批量审核参考实现（modal + JS 行号）
out.push('## G. 采购订单列表 G64 参考实现（行号）');
{
  const f = ROOT + '/采购管理/采购订单列表.html';
  const lines = (CONTENT[f] || '').split('\n');
  lines.forEach((ln, i) => {
    if (/poBatchModal|poBatchAudit|poBatchSubmit|批量审核/.test(ln)) out.push('- ' + f + ':' + (i + 1) + ' :: ' + ln.trim().slice(0, 200));
  });
}
out.push('');

// H. 退租入库列表批量审核现状
out.push('## H. 退租入库列表批量审核现状');
{
  const f = ROOT + '/租赁管理/退租入库列表.html';
  const lines = (CONTENT[f] || '').split('\n');
  lines.forEach((ln, i) => {
    if (/批量审核|g57BatchAudit/.test(ln)) out.push('- ' + f + ':' + (i + 1) + ' :: ' + ln.trim().slice(0, 200));
  });
}

fs.writeFileSync('_scan_tmpdir/g73_recon.md', out.join('\n'), 'utf8');
console.log('written: _scan_tmpdir/g73_recon.md, lines=' + out.length);
