# -*- coding: utf-8 -*-
"""G34 试点 步骤2：列表页入口改造 + 死脚本清理 + 弹窗模板下线

A. 把「税率三件套换算」「项目→绑定供应商联动」两脚本移植到新页面
B. 列表页：入口 openModal→go、删除内嵌 createModal 段、删除服务它的三个脚本
C. 删除 弹窗/新建采购订单.html
"""
import io, os

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
PROTO = os.path.join(ROOT, r'P3-R01-包装租赁管理后台原型')
L_P = os.path.join(PROTO, r'采购管理\采购订单列表.html')
N_P = os.path.join(PROTO, r'采购管理\采购订单新建.html')
T_P = os.path.join(PROTO, r'采购管理\弹窗\新建采购订单.html')

def rd(p):
    return io.open(p, encoding='utf-8', newline='').read().replace('\r\n', '\n')

def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace('\r\n', '\n').replace('\n', '\r\n'))

L = rd(L_P)
N = rd(N_P)
print(f'列表页 {len(L)} 字符 | 新页 {len(N)} 字符')

import re

def div_balance(src):
    """跳过 script/style 后的 div 栈扫描 -> (未闭合数, 多余闭合数)"""
    s = re.sub(r'<script\b.*?</script>', '', src, flags=re.S)
    s = re.sub(r'<style\b.*?</style>', '', s, flags=re.S)
    stack = 0; extra = 0
    for m in re.finditer(r'<div\b[^>]*>|</div>', s):
        if m.group(0).startswith('</'):
            if stack: stack -= 1
            else: extra += 1
        else:
            stack += 1
    return stack, extra

bal_before_L = div_balance(L)
print(f'列表页历史结构：未闭合={bal_before_L[0]} 多余闭合={bal_before_L[1]}（既有状态·非本次引入）')

# ============ A. 移植两个脚本到新页 ============
i1 = L.index('<script>/*F-A 税率三件套双向换算')
j1 = L.index('</script>', i1) + len('</script>')
tax_js = L[i1:j1]
assert 'data-tax' in tax_js and 'fmtAmt' in tax_js

i2 = L.index('<script>/* 项目→绑定供应商联动')
j2 = L.index('</script>', i2) + len('</script>')
prj_js = L[i2:j2]
assert 'cmProject' in prj_js and 'PRJ_SUPPLIERS' in prj_js

anchor = '''<script>
function poToggleQj(sel) {
  var r = document.getElementById("poQjRow");
  if (r) r.style.display = (sel.options[sel.selectedIndex].text === "器具") ? "flex" : "none";
}
</script>'''
assert N.count(anchor) == 1, f'poToggleQj 锚点异常 {N.count(anchor)}'
add = ''
if N.count('F-A 税率三件套') == 0:
    add += '\n' + tax_js          # 骨架源已含则跳过
if N.count('var PRJ_SUPPLIERS') == 0:
    add += '\n' + prj_js          # 骨架源无此脚本，须补
if add:
    N = N.replace(anchor, anchor + add)
assert N.count('F-A 税率三件套') == 1, '税率脚本计数异常'
assert N.count('var PRJ_SUPPLIERS') == 1, '联动脚本未就位'
print('[A] 脚本就位：税率三件套（骨架源已有·继承）+ 项目→供应商联动（已补）')

# ============ B. 列表页改造 ============
# B1 新建按钮
b1_old = """<button class="btn btn-sm" onclick="openModal('createModal')">新建采购订单</button>"""
b1_new = """<button class="btn btn-sm" onclick="go('../采购管理/采购订单新建.html')">新建采购订单</button>"""
assert L.count(b1_old) == 1, f'新建按钮锚点异常 {L.count(b1_old)}'
L = L.replace(b1_old, b1_new)

# B2 编辑链接（2 处）
b2_old = """<a onclick="openModal('createModal')">编辑</a>"""
b2_new = """<a onclick="go('../采购管理/采购订单新建.html?mode=edit')">编辑</a>"""
n2 = L.count(b2_old)
assert n2 == 2, f'编辑链接锚点异常 {n2}'
L = L.replace(b2_old, b2_new)
print(f'[B1/B2] 入口已改：新建按钮 1 处 + 编辑链接 {n2} 处 → go()')

# B3 删除内嵌 createModal 段（注释 + modal + 尾随空行）
m1 = '<!-- 弹窗已提取到 弹窗/新建采购订单.html，构建时注入 -->'
m2 = '<!-- 弹窗已提取到 弹窗/采购订单审核.html，构建时注入 -->'
i = L.index(m1); j = L.index(m2)
removed = L[i:j]
assert 'id="createModal"' in removed and 'modal-footer' in removed
assert 'id="auditModal"' not in removed
L = L[:i] + L[j:]
print(f'[B3] 内嵌 createModal 段已删（{len(removed)} 字符，含注释）')

# B4 删除三个服务脚本
for marker, label in [('<script>/*F-A 税率三件套双向换算', '税率三件套'),
                      ('<script>/* G31 T5 关联销售订单搜索下拉', '关联销售订单搜索'),
                      ('<script>/* 项目→绑定供应商联动', '项目→供应商联动')]:
    ii = L.index(marker)
    jj = L.index('</script>', ii) + len('</script>')
    # 连带其后空行
    k = jj
    while k < len(L) and L[k] == '\n':
        k += 1
    seg = L[ii:k]
    L = L[:ii] + L[k:]
    print(f'[B4] 死脚本已删：{label}（{len(seg)} 字符）')

# 规整连续空行
import re as _re
before = L.count('\n\n\n\n')
L = _re.sub(r'\n{4,}', '\n\n\n', L)
print(f'[B4] 空行规整：{before} 处 4+ 连续空行 → {L.count(chr(10)*4)}')

# ============ C. 删除弹窗模板 ============
assert os.path.exists(T_P)
os.remove(T_P)
print(f'[C] 弹窗模板已下线：{os.path.basename(T_P)}')

# ============ 写回与断言 ============
assert L.count('id="createModal"') == 0, 'createModal 残留'
assert L.count("openModal('createModal')") == 0, 'openModal(createModal) 残留'
assert L.count('poSoSearch') == 0, 'poSoSearch 残留'
assert L.count('PRJ_SUPPLIERS') == 0, '项目联动脚本应已移出列表页'
assert L.count('go(\'../采购管理/采购订单新建.html\')') == 1
assert L.count('go(\'../采购管理/采购订单新建.html?mode=edit\')') == 2
bal_L = div_balance(L)
bal_N = div_balance(N)
assert bal_L == bal_before_L, f'列表页结构被改变：{bal_before_L} -> {bal_L}'
assert bal_N == (0, 0), f'新页配平异常 {bal_N}'
print(f'[校验] 结构：列表页 {bal_L}（与删除前一致）| 新页 {bal_N}（配平）| 残留断言全过')

wr(L_P, L)
wr(N_P, N)
print(f'[写出] 列表页 {len(L)} 字符 | 新页 {len(N)} 字符')
print('完成')
