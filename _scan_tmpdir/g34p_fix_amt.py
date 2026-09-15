# -*- coding: utf-8 -*-
"""G34 试点修正：明细表「含税金额」列由 readonly input 改为文本 td.auto-cell

对齐项目表单页样板（采购入库录单.html 用 <td class="td-num auto-cell">4,800</td>，审计 0 问题）；
readonly input 会被 audit 判为 input-not-editable（audit 无豁免逻辑）。
"""
import io, os

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
N_P = os.path.join(ROOT, r'P3-R01-包装租赁管理后台原型\采购管理\采购订单新建.html')

N = io.open(N_P, encoding='utf-8', newline='').read().replace('\r\n', '\n')
orig_len = len(N)

# 1) 明细表两行默认值
for val in ['7,250.00', '3,720.00']:
    old = f'<td class="td-num"><input data-tax="amt" class="auto" value="{val}" readonly></td>'
    new = f'<td class="td-num auto-cell" data-tax="amt">{val}</td>'
    c = N.count(old)
    assert c == 1, f'{val} 锚点异常 {c}'
    N = N.replace(old, new)
    print(f'[1] 默认行 {val} → 文本 td.auto-cell')

# 2) poSoPick 模板行
old_pick = """'<td class="td-num"><input data-tax="amt" class="auto" readonly></td>'"""
new_pick = """'<td class="td-num auto-cell" data-tax="amt"></td>'"""
assert N.count(old_pick) == 1, f'poSoPick amt 锚点异常 {N.count(old_pick)}'
N = N.replace(old_pick, new_pick)
print('[2] poSoPick 模板 → 文本 td.auto-cell')

# 3) 税率换算脚本：amt 兼容 input / td
old_js = """    var amt = tr.querySelector('input[data-tax="amt"]');
    if (amt) amt.value = (num(q('qty')) * num(q('incl'))).toLocaleString('zh-CN', {minimumFractionDigits: 2, maximumFractionDigits: 2});"""
new_js = """    var amt = tr.querySelector('[data-tax="amt"]');
    if (amt) { var v = (num(q('qty')) * num(q('incl'))).toLocaleString('zh-CN', {minimumFractionDigits: 2, maximumFractionDigits: 2}); if (amt.tagName === 'INPUT') amt.value = v; else amt.textContent = v; }"""
assert N.count(old_js) == 1, f'税率脚本 amt 锚点异常 {N.count(old_js)}'
N = N.replace(old_js, new_js)
print('[3] 税率换算脚本：amt 兼容 input/td')

# 4) 校验
assert 'class="auto" readonly' not in N, 'readonly auto 残留'
assert N.count('auto-cell" data-tax="amt"') == 3, f'auto-cell 数量异常 {N.count(chr(34)+" data-tax"+chr(34))}'
io.open(N_P, 'w', encoding='utf-8', newline='').write(N.replace('\r\n', '\n').replace('\n', '\r\n'))
print(f'[写出] {orig_len} → {len(N)} 字符')
