# -*- coding: utf-8 -*-
"""G34 试点迭代 4：道远 09-15 样式细化四条

1. 备注文本域、预计到货日期宽度统一为 380px（与表单其他控件一致）
2. 预计到货日期改日期选择器（type=date）
3. 提交条按钮右对齐 → 居中
4. 明细表税率下拉补全样式（与其他下拉一致）
"""
import io, os

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
N_P = os.path.join(ROOT, r'P3-R01-包装租赁管理后台原型\采购管理\采购订单新建.html')

N = io.open(N_P, encoding='utf-8', newline='').read().replace('\r\n', '\n')

# ---- 1. 备注文本域宽度 520 → 380 ----
old1 = '<div class="input-box" style="width:520px;height:auto;padding:6px 11px;"><textarea'
assert N.count(old1) == 1, '备注容器锚点异常'
N = N.replace(old1, '<div class="input-box" style="width:380px;height:auto;padding:6px 11px;"><textarea')
print('[1] 备注文本域宽度 520px → 380px（与表单控件一致）')

# ---- 2. 预计到货日期：宽度 180 → 380 + 日期选择器 ----
old2 = '<div class="input-box" style="width:180px;"><input type="text" value="2026-09-15" placeholder="请输入"></div>'
assert N.count(old2) == 1, '预计到货日期锚点异常'
N = N.replace(old2, '<div class="input-box" style="width:380px;"><input type="date" value="2026-09-15"></div>')
print('[2] 预计到货日期：宽度 380px + type=date（日期选择器）')

# ---- 3. 提交条按钮居中 ----
old3a = 'padding:10px 160px 10px 24px; display:flex; justify-content:flex-end;'
assert N.count(old3a) == 1, '提交条 padding 锚点异常'
N = N.replace(old3a, 'padding:10px 24px; display:flex; justify-content:center;')
print('[3] 提交条：右对齐 → 居中（padding 恢复常规 24px）')

# ---- 4. 税率下拉补全样式（与其他下拉一致） ----
CS = 'width:100%;min-width:80px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;'
n4 = N.count('<select data-tax="rate" style="width:80px;">')
assert n4 == 3, f'税率下拉锚点异常 {n4}'
N = N.replace('<select data-tax="rate" style="width:80px;">', f'<select data-tax="rate" style="{CS}">')
print(f'[4] 税率下拉补全样式（{n4} 处 = 默认行 2 + poSoPick 模板 1）')

# ---- 校验 ----
assert 'type="date"' in N and N.count('<textarea') == 1
assert 'justify-content:center' in N
assert N.count('style="width:520px;') == 0, '仍有 520px 宽控件'
assert N.count('style="width:180px;"') == 0, '仍有 180px 宽控件'
print(f'[校验] 控件宽度已统一 380px；提交条居中；税率下拉样式已补全')

io.open(N_P, 'w', encoding='utf-8', newline='').write(N.replace('\r\n', '\n').replace('\n', '\r\n'))
print(f'[写出] {N_P} —— {len(N)} 字符')
