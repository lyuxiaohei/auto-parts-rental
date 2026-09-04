# -*- coding: utf-8 -*-
"""R5b：孤儿弹窗补触发 + 组装待审核态 + 组合出库触发器改指 exitConfirmModal。"""
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
def load(p): return io.open(f'{BASE}\\{p}', encoding='utf-8', newline='').read()
def save(p, s): io.open(f'{BASE}\\{p}', 'w', encoding='utf-8', newline='').write(s)

# 1) 组合出库列表：出库确认触发器 7 处改指 exitConfirmModal（幂等）
p = '仓储作业\\组合出库列表.html'
s = load(p)
n = s.count("openModal('auditModal')\">出库确认")
if n:
    s = s.replace("openModal('auditModal')\">出库确认", "openModal('exitConfirmModal')\">出库确认")
    assert n == 7 and "openModal('exitConfirmModal')\">出库确认" in s, n
    save(p, s); print(f'1) 组合出库: {n} 处「出库确认」触发器改指 exitConfirmModal')
else:
    print('1) 组合出库: 已处理（幂等跳过）')

# 2) 组装列表：① 状态页签加 待审核 1；② ZZ-20260829-003 行状态 已完成→待审核；③ 操作列加「组装确认」
p = '仓储作业\\组装列表.html'
s = load(p)
old = '<span class="stab">待组装<span class="stab-count">6</span></span>'
new = '<span class="stab">待审核<span class="stab-count">1</span></span>\r\n  ' + old
assert s.count(old) == 1
s = s.replace(old, new, 1)
tr = re.search(r'<tr>(?:(?!</tr>).)*ZZ-20260829-003.*?</tr>', s, re.S).group(0)
ntr = tr.replace('<span class="tag tag-green">已完成</span>', '<span class="tag tag-orange">待审核</span>', 1)
assert '待审核' in ntr
s = s.replace(tr, ntr, 1)
A1 = '<span class="ops"><a>详情</a><a onclick="go(\'../仓储作业/组装录单.html\')">录单</a></span>'
A2 = '<span class="ops"><a>详情</a><a onclick="go(\'../仓储作业/组装录单.html\')">登记组装</a></span>'
n2 = s.count(A1) + s.count(A2)
s = s.replace(A1, '<span class="ops"><a onclick="openModal(\'auditModal\')">组装确认</a><a>详情</a><a onclick="go(\'../仓储作业/组装录单.html\')">录单</a></span>')
s = s.replace(A2, '<span class="ops"><a onclick="openModal(\'auditModal\')">组装确认</a><a>详情</a><a onclick="go(\'../仓储作业/组装录单.html\')">登记组装</a></span>')
assert n2 >= 5, n2
save(p, s); print(f'2) 组装列表: 页签+待审核态+{n2} 行操作列加「组装确认」')

# 3) 4 个财务页：操作列首加确认入口（auditModal 孤儿补触发）
jobs = [
    ('财务协同\\回款登记.html', '<a>详情</a><a onclick="go(\'../财务协同/银行水单核销.html\')">去核销</a>', '确认收款'),
    ('财务协同\\应付账单.html', '<a onclick="go(\'../财务协同/付款登记.html\')">付款</a><a>详情</a>', '账单确认'),
    ('财务协同\\应收账单.html', '<a>详情</a><a onclick="go(\'../财务协同/开票登记.html\')">开票</a>', '账单确认'),
    ('财务协同\\开票登记.html', '<a>详情</a><a onclick="go(\'../财务协同/应收账单.html\')">查看账单</a>', '开票确认'),
]
for p, anchor, label in jobs:
    s = load(p)
    n = s.count(anchor)
    assert n >= 3, (p, n)
    s = s.replace(anchor, f'<a onclick="openModal(\'auditModal\')">{label}</a>' + anchor)
    save(p, s)
    print(f'3) {p}: {n} 行操作列加「{label}」')
print('=== R5b 完成 ===')
