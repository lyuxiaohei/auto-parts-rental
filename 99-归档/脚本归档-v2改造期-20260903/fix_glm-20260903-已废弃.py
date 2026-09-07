# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃（一次性修复，已完成使命）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""GLM 验收修复：修复4（残尾清理）+ 修复1/2/3 页面直改"""
import os, re, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2lib import PROTO, read_page, write_page

def must_replace(h, old, new, tag, count=1):
    n = h.count(old)
    if n != count:
        raise RuntimeError(f'[{tag}] 匹配数 {n} != {count}: {old[:70]}')
    return h.replace(old, new)

# ============================================================
# 修复 4：清理弹窗残尾（modal-overlay 之外的 form-row 片段及其后的游离闭合 div）
# ============================================================
def modal_spans(html):
    spans = []
    for m in re.finditer(r'<div class="modal-overlay"', html):
        depth = 1
        for mm in re.finditer(r'<div|</div>', html[m.end():]):
            depth += 1 if mm.group(0) == '<div' else -1
            if depth == 0:
                spans.append((m.start(), m.end() + mm.end()))
                break
    return spans

TAIL_PAT = re.compile(
    r'\n?[ \t]*<div class="form-row">\s*<span class="form-label"><span class="req">\*</span>审核结论</span>'
    r'[\s\S]*?onclick="closeModal\(\'auditModal\'\)">确认提交</button>\s*</div>\s*</div>\s*</div>')

n_files = 0
for p in sorted(glob.glob(os.path.join(PROTO, '*', '*.html'))):
    if os.sep + '弹窗' + os.sep in p:
        continue
    html = open(p, encoding='utf-8').read()
    spans = modal_spans(html)
    def is_stray(m):
        return not any(s <= m.start() < e for s, e in spans)
    hits = [m for m in TAIL_PAT.finditer(html) if is_stray(m)]
    if not hits:
        continue
    # 从后往前删，避免位置偏移
    for m in reversed(hits):
        html = html[:m.start()] + html[m.end():]
    # 收敛多余空行
    html = re.sub(r'\n{3,}', '\n\n', html)
    open(p, 'w', encoding='utf-8', newline='\n').write(html)
    rel = os.path.relpath(p, PROTO).replace(os.sep, '/')
    print(f'修复4 ✅ {rel}（删除 {len(hits)} 段残尾）')
    n_files += 1
print(f'修复4 共清理 {n_files} 页\n')

# ============================================================
# 修复 1：采购入库列表加「关联采购订单号」列（供应商 后、业务类型 前）
# ============================================================
rel = '仓储作业/采购入库列表.html'
h = read_page(rel)
h = must_replace(h, '<th>供应商</th>', '<th>供应商</th>\n          <th>关联采购订单号</th>', rel)
PO_MAP = {  # 入库单号 → 采购订单号（供应商/物料类型对齐采购订单列表）
    'CGRK-20260828-012': 'PO-20260828-015',   # 苏州联恒 零部件
    'CGRK-20260828-011': 'PO-20260901-017',   # 宁波华塑 器具
    'CGRK-20260827-010': 'PO-20260820-013',   # 常州正大 器具
    'CGRK-20260827-009': 'PO-20260902-018',   # 苏州联恒 零部件（待验收）
    'CGRK-20260826-008': 'PO-20260825-014',   # 宁波华塑 器具
    'CGRK-20260825-006': 'PO-20260830-016',   # 常州正大 器具
    'CGRK-20260824-005': 'PO-20260815-012',   # 苏州联恒 零部件
}
for cgrk, po in PO_MAP.items():
    pat = re.compile(r'(<td><span class="lk">' + cgrk + r'</span></td>\s*<td>[^<]*</td>)')
    h, n = pat.subn(r'\1\n          <td><span class="lk">' + po + '</span></td>', h)
    if n != 1:
        raise RuntimeError(f'[{rel}] {cgrk} 行插入失败 n={n}')
# 数据一致性：宁波华塑是器具供应商，CGRK-20260826-008 的业务类型修正为器具采购
h = must_replace(h, '<td><span class="lk">CGRK-20260826-008</span></td>\n          <td>宁波华塑包装制品有限公司</td>\n          <td><span class="lk">PO-20260825-014</span></td>\n          <td>PRJ-2603</td>\n          <td>零部件采购</td>',
                 '<td><span class="lk">CGRK-20260826-008</span></td>\n          <td>宁波华塑包装制品有限公司</td>\n          <td><span class="lk">PO-20260825-014</span></td>\n          <td>PRJ-2603</td>\n          <td>器具采购</td>', rel)
write_page(rel, h)
print(f'修复1 ✅ {rel}（新增关联采购订单号列，7 行已填）\n')

# ============================================================
# 修复 2a：应收账单加 3 行「销售费」记录（表格最上方）
# ============================================================
rel = '财务协同/应收账单.html'
h = read_page(rel)
SALES_ROWS = '''        <tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">AR-2026-09-PRJ2601-S1</span></td>
          <td>2026-09</td>
          <td>PRJ-2601</td>
          <td>一汽解放汽车有限公司</td>
          <td>销售费（按销售出库自动汇总）<div style="color:#8c8c8c;font-size:11px;">关联 XSCK-20260902-015 等 2 单</div></td>
          <td><span class="td-num"><b>10,200.00</b></span></td>
          <td><span class="td-num">0.00</span></td>
          <td><span class="tag tag-red">未开票</span></td>
          <td><span class="tag tag-blue">自动生成</span></td>
          <td>2026-09-03 00:06</td>
          <td><span class="ops"><a>详情</a><a onclick="go('../财务协同/开票登记.html')">开票</a><a onclick="go('../财务协同/银行水单核销.html')">核销</a></span></td>
        </tr>
        <tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">AR-2026-09-PRJ2604-S1</span></td>
          <td>2026-09</td>
          <td>PRJ-2604</td>
          <td>东风本田汽车有限公司</td>
          <td>销售费（按销售出库自动汇总）<div style="color:#8c8c8c;font-size:11px;">关联 XSCK-20260901-014</div></td>
          <td><span class="td-num"><b>1,280.00</b></span></td>
          <td><span class="td-num">0.00</span></td>
          <td><span class="tag tag-red">未开票</span></td>
          <td><span class="tag tag-blue">自动生成</span></td>
          <td>2026-09-02 00:06</td>
          <td><span class="ops"><a>详情</a><a onclick="go('../财务协同/开票登记.html')">开票</a><a onclick="go('../财务协同/银行水单核销.html')">核销</a></span></td>
        </tr>
        <tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">AR-2026-08-PRJ2602-S1</span></td>
          <td>2026-08</td>
          <td>PRJ-2602</td>
          <td>上汽大众宁波分公司</td>
          <td>销售费（按销售出库自动汇总）<div style="color:#8c8c8c;font-size:11px;">关联 XSCK-20260826-012</div></td>
          <td><span class="td-num"><b>6,050.00</b></span></td>
          <td><span class="td-num">6,050.00</span></td>
          <td><span class="tag tag-green">已结清</span></td>
          <td><span class="tag tag-blue">自动生成</span></td>
          <td>2026-08-31 00:06</td>
          <td><span class="ops"><a>详情</a><a onclick="go('../财务协同/开票登记.html')">开票</a><a onclick="go('../财务协同/银行水单核销.html')">核销</a></span></td>
        </tr>
'''
h = must_replace(h, '<tbody>\n        <tr>\n          <td><input type="checkbox" class="cb"></td>\n          <td><span class="lk">AR-2026-08-PRJ2601</span></td>',
                 '<tbody>\n' + SALES_ROWS + '        <tr>\n          <td><input type="checkbox" class="cb"></td>\n          <td><span class="lk">AR-2026-08-PRJ2601</span></td>', rel)
write_page(rel, h)
print(f'修复2a ✅ {rel}（新增 3 行销售费记录）\n')

# ============================================================
# 修复 3a：组合出库列表加「关联租赁单号」列（客户 后）
# ============================================================
rel = '仓储作业/组合出库列表.html'
h = read_page(rel)
h = must_replace(h, '<th>客户</th>', '<th>客户</th>\n          <th>关联租赁单号</th>', rel)
# 按行客户/项目填租赁单号（与租赁单列表一致）
ZL_BY_ROW = [
    ('CK-20260830-015', 'ZL-20260610-015'),
    ('CK-20260830-014', 'ZL-20260828-031'),
]
# 先读出库单号列全部行，逐行处理
rows = re.findall(r'(<tr>\s*<td><input type="checkbox"[\s\S]*?</tr>)', h)
print('组合出库行数:', len(rows))
ZL_DEFAULT = ['ZL-20260815-028', 'ZL-20260720-022', 'ZL-20260610-015', 'ZL-20260301-006', 'ZL-20260828-031']
i = 0
def add_zl(m):
    global i
    row = m.group(1)
    ck = re.search(r'<span class="lk">(CK-[\d-]+)</span>', row).group(1)
    zl = dict(ZL_BY_ROW).get(ck, ZL_DEFAULT[i % len(ZL_DEFAULT)])
    i += 1
    # 在 客户 td 后插入
    cells = list(re.finditer(r'<td>[^<]*</td>', row))
    # 客户 td = 第 4 个（cb/单号/项目/客户）
    cust = cells[3]
    new_row = row[:cust.end()] + '\n          <td><span class="lk">' + zl + '</span></td>' + row[cust.end():]
    return new_row
h = re.sub(r'(<tr>\s*<td><input type="checkbox"[\s\S]*?</tr>)', add_zl, h)
write_page(rel, h)
print(f'修复3a ✅ {rel}（新增关联租赁单号列）\n')

# ============================================================
# 修复 3b：租赁单列表「已审核/在租」行加「出库」链接
# ============================================================
rel = '包装管理/租赁单列表.html'
h = read_page(rel)
OUT = '<a onclick="go(\'../仓储作业/组合出库列表.html\')">出库</a>'
n1 = h.count('<span class="ops"><a>详情</a><a>关闭</a></span>')
h = h.replace('<span class="ops"><a>详情</a><a>关闭</a></span>',
              '<span class="ops">' + OUT + '<a>详情</a><a>关闭</a></span>')
n2 = h.count('<span class="ops"><a>详情</a><a onclick="go(\'../包装管理/退租申请列表.html\')">创建退租申请</a></span>')
h = h.replace('<span class="ops"><a>详情</a><a onclick="go(\'../包装管理/退租申请列表.html\')">创建退租申请</a></span>',
              '<span class="ops">' + OUT + '<a>详情</a><a onclick="go(\'../包装管理/退租申请列表.html\')">创建退租申请</a></span>')
print(f'修复3b ✅ {rel}（已审核行 {n1} 处 + 在租行 {n2} 处加「出库」）\n')
write_page(rel, h)

print('页面直改部分完成')
