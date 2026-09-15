# -*- coding: utf-8 -*-
"""G35 前置修复：BOM 添加子项 / 库存查询术语 / 采购入库去业务类型

道远 09-15 报告三项：
 ① 新建 BOM「添加子项」按钮无反应（应为新增一行）
 ② 库存查询视角名：散件→物料、组合→BOM（D-128）
 ③ 采购入库去掉「业务类型」字段（D-129）
策略：先从备份还原，再统一改，保证可重跑。
"""
import io, os, re, shutil, json, subprocess

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
P = os.path.join(ROOT, r'P3-R01-包装租赁管理后台原型')
BK = os.path.join(ROOT, r'_scan_tmpdir\backup-g35-20260915')

FILES = [r'基础数据\BOM维护.html', r'仓储作业\库存查询.html',
         r'采购管理\采购入库列表.html', r'采购管理\采购入库录单.html', r'_data\demo-data.js']

# ---------- 0. 从备份还原（保证可重跑） ----------
for rel in FILES:
    src = os.path.join(BK, rel)
    assert os.path.exists(src), f'备份缺失 {rel}'
    shutil.copy2(src, os.path.join(P, rel))
print(f'[0] 已还原 {len(FILES)} 个文件至未改状态')

def rd(p): return io.open(p, encoding='utf-8', newline='').read()
def wr(p, s):
    crlf = '\r\n' in rd(p)
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace('\r\n', '\n').replace('\n', '\r\n' if crlf else '\n'))

# ========== 1. BOM维护：添加子项按钮接通 ==========
p1 = os.path.join(P, r'基础数据\BOM维护.html')
t = rd(p1).replace('\r\n', '\n')
old_b = '<div class="head-btns"><button class="btn btn-dashed btn-sm">添加子项</button></div>'
assert t.count(old_b) == 1, '添加子项按钮锚点异常'
t = t.replace(old_b, '<div class="head-btns"><button class="btn btn-dashed btn-sm" onclick="addBomRow(this)">添加子项</button></div>')

fn_anchor = "function closeModal(id) { document.getElementById(id).classList.remove('show'); }"
assert t.count(fn_anchor) == 1, 'closeModal 锚点异常'
bom_fn = fn_anchor + """

/* 添加子项：克隆末行→清空待填→重编号（道远 09-15 报"按钮无反应"修复） */
function addBomRow(btn) {
  var card = btn.closest('.card');
  var tbody = card ? card.querySelector('tbody') : null;
  if (!tbody) return;
  var last = tbody.querySelector('tr:last-child');
  if (!last) return;
  var row = last.cloneNode(true);
  row.querySelectorAll('input').forEach(function (i) { i.value = ''; });
  row.querySelectorAll('.v').forEach(function (v) { v.textContent = '选择子项'; });
  var tds = row.querySelectorAll('td');
  if (tds[2]) tds[2].innerHTML = '';
  if (tds[3]) tds[3].innerHTML = '<span class="tag tag-gray">自购</span>';
  if (tds[4]) tds[4].textContent = '—';
  if (tds[6]) tds[6].innerHTML = '<span style="color:var(--text-2)">—</span>';
  tbody.appendChild(row);
  var rows = tbody.querySelectorAll('tr');
  rows.forEach(function (r, i) { r.cells[0].textContent = i + 1; });
}"""
t = t.replace(fn_anchor, bom_fn)
wr(p1, t)
print('[1] BOM维护：按钮接通 addBomRow')

# ========== 2. 库存查询：视角术语 ==========
p2 = os.path.join(P, r'仓储作业\库存查询.html')
t = rd(p2).replace('\r\n', '\n')
for a, b in [('>散件视角<', '>物料视角<'), ('>组合视角<', '>BOM 视角<')]:
    c = t.count(a)
    assert c == 1, f'视角名锚点异常 {a} x{c}'
    t = t.replace(a, b)
wr(p2, t)
print('[2] 库存查询：散件→物料 视角、组合→BOM 视角')

# 2b 术语全站统一（含页面 pin 文案与 A03 标注数据源·盘点录入页）
for _a, _b in [('散件视角', '物料视角'), ('零件视角', '物料视角'), ('组合视角', 'BOM 视角')]:
    t = t.replace(_a, _b)
wr(p2, t)
for rel2 in [r'仓储作业\盘点录入.html', r'P3-R01-A03-标注数据.json']:
    fp = os.path.join(P, rel2)
    x = rd(fp)
    for _a, _b in [('散件视角', '物料视角'), ('零件视角', '物料视角'), ('组合视角', 'BOM 视角')]:
        x = x.replace(_a, _b)
    wr(fp, x)
print('[2b] 盘点录入页 + A03 标注数据 术语同步')

# ========== 3. 采购入库列表：删业务类型 ==========
p3 = os.path.join(P, r'采购管理\采购入库列表.html')
t = rd(p3).replace('\r\n', '\n')
m = re.search(r'\n\s*<div class="ff ff-row-extra"><span class="ff-label">业务类型：</span>.*?\n\s*</div>', t, re.S)
assert m, '业务类型筛选块未找到'
t = t[:m.start()] + t[m.end():]
assert t.count('<th>业务类型</th>') == 1, '列头锚点异常'
t = t.replace('<th>业务类型</th>', '')
t, n_cfg = re.subn(r",\s*\{ label: '业务类型', field: 'bizType' \}", "", t)
assert n_cfg == 1, f'filters 配置锚点异常 {n_cfg}'
wr(p3, t)
print('[3] 采购入库列表：筛选块 + 列头 + filters 配置 三处已删')

# ========== 4. 采购入库录单：删业务类型表单行 ==========
p4 = os.path.join(P, r'采购管理\采购入库录单.html')
t = rd(p4).replace('\r\n', '\n')
m = re.search(r'\n\s*<div class="form-row">\s*\n\s*<div class="form-label"><span class="req">\*</span>业务类型：</div>.*?\n\s*</div>\n', t, re.S)
assert m, '录单页业务类型表单行未找到'
t = t[:m.start()] + t[m.end():]
wr(p4, t)
print('[4] 采购入库录单：业务类型表单行已删')

# ========== 5. demo-data：删 cells 第 4 格 + fields.bizType ==========
p5 = os.path.join(P, r'_data\demo-data.js')
t = rd(p5).replace('\r\n', '\n')
i = t.find('purchaseInbounds: {')
j = t.find('\n  salesOutbounds: {', i)
assert i > 0 and j > i, 'purchaseInbounds 段定位失败'
seg = t[i:j]
cnt = {'cells': 0}

def fix_cells(m):
    arr = json.loads(m.group(1))
    if len(arr) >= 4:
        del arr[3]
        cnt['cells'] += 1
    return '"cells": ' + json.dumps(arr, ensure_ascii=False)

seg2 = re.sub(r'"cells": (\[.*?\])(?=, "ops")', fix_cells, seg, flags=re.S)
seg2, n_bt = re.subn(r', "bizType": "[^"]*"', '', seg2)
t = t[:i] + seg2 + t[j:]
wr(p5, t)
print(f"[5] demo-data：{cnt['cells']} 条 cells 去第 4 格、{n_bt} 处 fields.bizType 已删")

# ========== 6. 校验 ==========
r = subprocess.run(['node', '--check', p5], capture_output=True, text=True)
assert r.returncode == 0, 'node --check 失败: ' + r.stderr[:300]
print('[6] node --check: PASS')
assert '业务类型' not in rd(p3) and '业务类型' not in rd(p4), '业务类型残留'
assert '散件视角' not in rd(p2) and '组合视角' not in rd(p2), '旧视角名残留'
assert 'addBomRow' in rd(p1)
print('[6] 残留断言全过：业务类型 0、旧视角名 0、addBomRow 已接')
