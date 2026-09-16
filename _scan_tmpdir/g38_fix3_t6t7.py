# -*- coding: utf-8 -*-
"""G38 T6+T7：两录单页缺列修复＋托列删除（结构改动·正则锚定＋断言＋配平）"""
import io, re, sys

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def read(p):
    return io.open(p, encoding='utf-8', newline='').read()

def write(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)

def balance(t):
    """标签配平自检：返回 dict"""
    return {k: t.count('<' + k) - t.count('</' + k + '>') for k in ('table', 'thead', 'tbody', 'tr', 'th', 'td', 'div', 'span', 'select')}

def cells_of(tr_html):
    return len(re.findall(r'<td(\s[^>]*)?>', tr_html))

# ============ 1. 采购入库录单 ============
P1 = BASE + r'\采购管理\采购入库录单.html'
t = read(P1)
b0 = balance(t)

# 1a. thead 重写
m = re.search(r'<thead>.*?</thead>', t, re.S)
assert m, 'thead not found'
old_thead = m.group(0)
for kw in ('零件号 / 物料编码', '托数 *', '每托数量 *', '入库总数', '未税单价(元)', '含税金额(元)'):
    assert kw in old_thead, 'thead missing ' + kw
new_thead = ('<thead><tr><th style="width:44px;">序号</th><th>物料编码</th><th>名称规格</th><th>基本单位</th>'
             '<th style="width:110px;">数量 *</th>'
             '<th style="font-size:13.5px;font-weight:700;">未税单价(元)</th>'
             '<th style="font-size:13.5px;font-weight:700;">税率</th>'
             '<th style="font-size:13.5px;font-weight:700;">含税单价(元)</th>'
             '<th>含税金额(元)</th>'
             '<th style="width:130px;">批次号</th><th>入库库位</th><th class="sticky-op">操作</th></tr></thead>')
t = t.replace(old_thead, new_thead, 1)

# 1b. 三行：删托三列→数量＋四价格
ROWS = [
    ('LJ-A100', '10', '480', '4,800', '4800', '6.80', '7.68', '36,864.00'),
    ('LJ-B200', '8', '400', '3,200', '3200', '4.20', '4.75', '15,200.00'),
    ('LJ-D400', '6', '120', '720', '720', '36.00', '40.68', '29,289.60'),
]
for code, tqty, tper, tot, qty, excl, incl, amt in ROWS:
    old_core = re.compile(
        r'<td class="td-num"><input value="%s"></td>\s*'
        r'<td class="td-num"><input value="%s"></td>\s*'
        r'<td class="td-num auto-cell">%s</td>' % (re.escape(tqty), re.escape(tper), re.escape(tot)))
    new_core = ('<td class="td-num"><input value="%s"></td>\n          '
                '<td class="td-num"><input value="%s"></td>\n          '
                '<td class="td-num"><input value="13%%"></td>\n          '
                '<td class="td-num auto-cell">%s</td>\n          '
                '<td class="td-num auto-cell">%s</td>') % (qty, excl, incl, amt)
    t, n = old_core.subn(new_core, t)
    assert n == 1, 'row %s core matched %d' % (code, n)

# 1c. 行格数断言（12）
tb = re.search(r'<tbody>(.*?)</tbody>', t, re.S).group(1)
trs = re.findall(r'<tr[^>]*>.*?</tr>', tb, re.S)
assert len(trs) == 3, 'rows %d' % len(trs)
for i, tr in enumerate(trs):
    c = cells_of(tr)
    assert c == 12, 'row %d cells %d' % (i + 1, c)

b1 = balance(t)
assert b0 == b1, 'balance changed %r -> %r' % (b0, b1)
write(P1, t)
print('采购入库录单 OK：thead 12 列·3 行×12 格·配平一致')

# ============ 2. 租赁出库录单 ============
P2 = BASE + r'\租赁管理\租赁出库录单.html'
t = read(P2)
b0 = balance(t)

INS = {
    'ZH-2601-A': ('180', '2.40', '2.71', '487.80'),
    'ZH-2602-B': ('0', '0.15', '0.17', '0.00'),
}
for code, (qty, excl, incl, amt) in INS.items():
    # 行内锚：含该编码的 <tr> 块
    rm = re.search(r'<tr[^>]*>(?:(?!</tr>).)*?<span class="v">%s</span>(?:(?!</tr>).)*?</tr>' % code, t, re.S)
    assert rm, 'row %s not found' % code
    row = rm.group(0)
    assert cells_of(row) == 8, 'row %s cells %d (expect 8)' % (code, cells_of(row))
    old_qty = '<td class="td-num"><input value="%s"></td>' % qty
    assert row.count(old_qty) == 1, 'qty cell %s x%d' % (code, row.count(old_qty))
    new_cells = (old_qty + '\n          <td class="td-num"><input value="%s"></td>\n          '
                 '<td class="td-num"><input value="13%%"></td>\n          '
                 '<td class="td-num auto-cell">%s</td>\n          '
                 '<td class="td-num auto-cell">%s</td>') % (excl, incl, amt)
    new_row = row.replace(old_qty, new_cells, 1)
    assert cells_of(new_row) == 12, 'new row %s cells %d' % (code, cells_of(new_row))
    t = t.replace(row, new_row, 1)

b1 = balance(t)
assert b0 == b1, 'balance changed %r -> %r' % (b0, b1)
write(P2, t)
print('租赁出库录单 OK：2 行×12 格·配平一致')

# ============ 3. 采购入库列表（T7·到货托数列删除＋T4·入库库区→入库库房） ============
P3 = BASE + r'\采购管理\采购入库列表.html'
t = read(P3)
assert t.count('<th>到货托数</th>') == 1
t = t.replace('<th>到货托数</th>\n          ', '')  # thead 删列（含换行缩进）
t = t.replace('<th>到货托数</th>', '')
n_lab = t.count('入库库区')
assert n_lab == 3, '入库库区 x%d' % n_lab
t = t.replace('入库库区', '入库库房')
write(P3, t)
print('采购入库列表 OK：到货托数列删·入库库区→入库库房 ×3')

# ============ 4. 租入入库列表（T4：入库库区→入库库房＋入库时间→入库日期） ============
P4 = BASE + r'\租入管理\租入入库列表.html'
t = read(P4)
n1 = t.count('入库库区'); n2 = t.count('入库时间')
t = t.replace('入库库区', '入库库房').replace('入库时间', '入库日期')
write(P4, t)
print('租入入库列表 OK：入库库区→入库库房 ×%d·入库时间→入库日期 ×%d' % (n1, n2))
